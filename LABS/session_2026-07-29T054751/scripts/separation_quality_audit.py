"""
Separation Quality Audit
=========================
Priority 1 task (per the_midas_touch_corrected.md): before trusting the
vocal-prominence / consistency numbers from Session 2, we need to know
whether the AI stem separation itself is reliable, and whether it's
reliable to the SAME DEGREE across natural (Elissa) vs synthetic (Suno)
audio. If separation quality differs systematically, the consistency
numbers are confounded.

No ground-truth official stems exist anymore for any track (Elissa's old
official stems were replaced - see context.md section 1), so we can't do
a direct correlation-to-truth comparison. Instead we use two
label-free proxies that are standard in source-separation QA:

1. Reconstruction fidelity: vocal_stem + instrumental_stem should sum
   back to (approximately) the original mix if the separation model
   did a clean additive decomposition. We measure per-second RMS error
   (in dB) between the original and the reconstructed sum.

2. Vocal-stem noise floor: in the quietest 10% of 1-second frames of the
   vocal stem (frames where a human vocal is very unlikely to be
   present), we measure (a) the median RMS level and (b) spectral
   flatness. A clean separation should leave near-silence (very low RMS,
   noise-like/high-flatness). Elevated RMS with LOW flatness in these
   quiet frames indicates tonal bleed-through from the instrumental bed
   (i.e., imperfect separation), not just noise.
"""

import numpy as np
import librosa
import json
import os

SR = 22050
FRAME_SEC = 1.0

TRACKS = {
    "Elissa (ref)": {
        "orig": "data/elisa_maktooba_leek.mp3",
        "voc": "data/elisa_maktooba_leek/elisa_maktooba_leek-Vocals.mp3",
        "inst": "data/elisa_maktooba_leek/elisa_maktooba_leek-Instrumental.mp3",
    },
    "Ya Dar Maya (orig)": {
        "orig": "data/يا دار مية - 28-07-2026.mp3",
        "voc": "data/يا دار مية - 28-07-2026/يا دار مية - 28-07-2026-Vocals.mp3",
        "inst": "data/يا دار مية - 28-07-2026/يا دار مية - 28-07-2026-Instrumental.mp3",
    },
    "SONG_A": {
        "orig": "data/يا دار مية - 28-07-2026_SONG_A.mp3",
        "voc": "data/يا دار مية - 28-07-2026_SONG_A/يا دار مية - 28-07-2026_SONG_A-Vocals.mp3",
        "inst": "data/يا دار مية - 28-07-2026_SONG_A/يا دار مية - 28-07-2026_SONG_A-Instrumental.mp3",
    },
    "SONG_B": {
        "orig": "data/يا دار مية - 28-07-2026_SONG_B.mp3",
        "voc": "data/يا دار مية - 28-07-2026_SONG_B/يا دار مية - 28-07-2026_SONG_B-Vocals.mp3",
        "inst": "data/يا دار مية - 28-07-2026_SONG_B/يا دار مية - 28-07-2026_SONG_B-Instrumental.mp3",
    },
    "SONG_C": {
        "orig": "data/يا دار مية - 28-07-2026_SONG_C.mp3",
        "voc": "data/يا دار مية - 28-07-2026_SONG_C/يا دار مية - 28-07-2026_SONG_C-Vocals.mp3",
        "inst": "data/يا دار مية - 28-07-2026_SONG_C/يا دار مية - 28-07-2026_SONG_C-Instrumental.mp3",
    },
    "SONG_D": {
        "orig": "data/يا دار مية - 28-07-2026_SONG_D.mp3",
        "voc": "data/يا دار مية - 28-07-2026_SONG_D/يا دار مية - 28-07-2026_SONG_D-Vocals.mp3",
        "inst": "data/يا دار مية - 28-07-2026_SONG_D/يا دار مية - 28-07-2026_SONG_D-Instrumental.mp3",
    },
}


def rms_db(x, eps=1e-10):
    return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + eps)


def frame_signal(x, sr, frame_sec=FRAME_SEC):
    n = int(sr * frame_sec)
    n_frames = len(x) // n
    return x[: n_frames * n].reshape(n_frames, n)


def analyze_track(name, paths):
    orig, _ = librosa.load(paths["orig"], sr=SR, mono=True)
    voc, _ = librosa.load(paths["voc"], sr=SR, mono=True)
    inst, _ = librosa.load(paths["inst"], sr=SR, mono=True)

    n = min(len(orig), len(voc), len(inst))
    orig, voc, inst = orig[:n], voc[:n], inst[:n]

    recon = voc + inst

    orig_f = frame_signal(orig, SR)
    recon_f = frame_signal(recon, SR)
    voc_f = frame_signal(voc, SR)

    # --- 1. Reconstruction fidelity ---
    err_db = []
    for o, r in zip(orig_f, recon_f):
        o_db = rms_db(o)
        r_db = rms_db(r)
        err_db.append(r_db - o_db)
    err_db = np.array(err_db)

    corr = np.corrcoef(orig, recon)[0, 1]

    # --- 2. Vocal-stem noise floor in quietest NON-ZERO frames ---
    # DISCOVERY: the vocal stems contain a substantial fraction of frames
    # that are literal digital silence (exact zero samples, not just low
    # RMS) -- a hard gate, presumably applied by the separation tool or
    # its export step. Those frames must be excluded from the "quiet
    # frame" noise-floor analysis, or the percentile just measures the
    # gate floor (-inf) instead of actual bleed-through.
    voc_rms_db_per_frame = np.array([rms_db(f) for f in voc_f])
    ZERO_GATE_DB = -150.0  # anything below this is the hard-gated floor, not signal
    silent_frame_frac = float(np.mean(voc_rms_db_per_frame <= ZERO_GATE_DB))

    nonzero_mask = voc_rms_db_per_frame > ZERO_GATE_DB
    nonzero_rms = voc_rms_db_per_frame[nonzero_mask]
    nonzero_idx = np.where(nonzero_mask)[0]

    if len(nonzero_rms) > 0:
        threshold = np.percentile(nonzero_rms, 10)
        quiet_idx = nonzero_idx[voc_rms_db_per_frame[nonzero_idx] <= threshold]
        quiet_rms = voc_rms_db_per_frame[quiet_idx]

        flatness_vals = []
        for i in quiet_idx:
            frame = voc_f[i]
            flat = librosa.feature.spectral_flatness(y=frame)[0]
            flatness_vals.append(np.mean(flat))
        flatness_vals = np.array(flatness_vals)
        quiet_rms_median = round(float(np.median(quiet_rms)), 2)
        quiet_flatness_median = round(float(np.median(flatness_vals)), 5)
    else:
        quiet_rms_median = None
        quiet_flatness_median = None

    return {
        "track": name,
        "n_frames": len(orig_f),
        "reconstruction_corr": round(float(corr), 4),
        "reconstruction_err_db_median": round(float(np.median(err_db)), 2),
        "reconstruction_err_db_iqr": [
            round(float(np.percentile(err_db, 25)), 2),
            round(float(np.percentile(err_db, 75)), 2),
        ],
        "vocal_stem_hard_silent_frame_fraction": round(silent_frame_frac, 3),
        "quiet_nonzero_frame_rms_median_db": quiet_rms_median,
        "quiet_nonzero_frame_spectral_flatness_median": quiet_flatness_median,
    }


if __name__ == "__main__":
    results = []
    for name, paths in TRACKS.items():
        missing = [p for p in paths.values() if not os.path.exists(p)]
        if missing:
            print(f"SKIP {name}: missing files {missing}")
            continue
        print(f"Analyzing {name} ...")
        r = analyze_track(name, paths)
        results.append(r)
        print(json.dumps(r, ensure_ascii=False, indent=2))

    out_path = os.path.join(os.path.dirname(__file__), "..", "separation_quality_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nSaved results to {out_path}")
