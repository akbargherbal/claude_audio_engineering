"""
Reverb Decay Quantification
============================
Triggered by a direct listening observation (project owner, Session 4):
Elissa's isolated vocal stem has an obvious, consistent reverb tail
("like singing in a bathroom"), while Suno vocal stems vary between
almost no reverb and limited reverb, as if something (an aggressive
gate/"deverb" step) is cutting the tail inconsistently.

This script quantifies that impression: after each vocal energy peak, we
measure the decay slope (dB per second) of the RMS envelope over the
following ~300 ms, using only points BEFORE the hard-silence gate found
in Session 3 (< -150 dB floor) so the gate itself doesn't get measured
as "instant decay". A slow slope (small dB/sec) = long reverb tail. A
fast slope (large dB/sec) = little/no reverb, or a hard cutoff.
"""

import numpy as np
import librosa
import json
import os

SR = 22050
HOP = 256          # ~11.6 ms per frame
FRAME_LEN = 2048
GATE_FLOOR_DB = -150.0
DECAY_WINDOW_SEC = 0.3   # look at 300ms after each peak
MIN_DECAY_POINTS = 4     # need at least this many valid points to fit a slope

VOCAL_STEMS = {
    "Elissa (ref)": "data/elisa_maktooba_leek/elisa_maktooba_leek-Vocals.mp3",
    "Ya Dar Maya (orig)": "data/يا دار مية - 28-07-2026/يا دار مية - 28-07-2026-Vocals.mp3",
    "SONG_A": "data/يا دار مية - 28-07-2026_SONG_A/يا دار مية - 28-07-2026_SONG_A-Vocals.mp3",
    "SONG_B": "data/يا دار مية - 28-07-2026_SONG_B/يا دار مية - 28-07-2026_SONG_B-Vocals.mp3",
    "SONG_C": "data/يا دار مية - 28-07-2026_SONG_C/يا دار مية - 28-07-2026_SONG_C-Vocals.mp3",
    "SONG_D": "data/يا دار مية - 28-07-2026_SONG_D/يا دار مية - 28-07-2026_SONG_D-Vocals.mp3",
}


def analyze_decay(name, path):
    y, _ = librosa.load(path, sr=SR, mono=True)
    rms = librosa.feature.rms(y=y, frame_length=FRAME_LEN, hop_length=HOP)[0]
    rms_db = 20 * np.log10(rms + 1e-10)
    frame_times = librosa.frames_to_time(np.arange(len(rms_db)), sr=SR, hop_length=HOP)

    valid = rms_db > GATE_FLOOR_DB

    # v2 method: only look at the run of valid frames immediately BEFORE
    # a transition into the hard-gated silence region. That transition
    # is a genuine phrase-ending -- not a vibrato ripple or mid-phrase dip.
    decay_window_points = int(DECAY_WINDOW_SEC * SR / HOP)
    decay_slopes = []
    gate_entry_count = 0
    gate_entry_times = []

    for i in range(1, len(valid)):
        if valid[i - 1] and not valid[i]:
            gate_entry_count += 1
            gate_entry_times.append(round(float(frame_times[i]), 2))
            start = max(0, i - decay_window_points)
            seg_db = rms_db[start:i]
            seg_valid = valid[start:i]
            if not np.all(seg_valid):
                # trim to the longest valid run ending right at i
                # (skip if there's a gap inside the window)
                first_invalid = np.where(~seg_valid)[0]
                start2 = start + first_invalid[-1] + 1
                seg_db = rms_db[start2:i]
            if len(seg_db) >= MIN_DECAY_POINTS:
                seg_t = np.arange(len(seg_db)) * (HOP / SR)
                slope, intercept = np.polyfit(seg_t, seg_db, 1)
                if slope < 0:
                    decay_slopes.append(slope)

    decay_slopes = np.array(decay_slopes)
    if len(decay_slopes) == 0:
        return {"track": name, "n_gate_entries": gate_entry_count, "n_decays_used": 0,
                "gate_entry_times_sec": gate_entry_times}

    median_slope = float(np.median(decay_slopes))
    t60_est = 60.0 / abs(median_slope) if median_slope != 0 else None

    return {
        "track": name,
        "n_gate_entries": gate_entry_count,
        "n_decays_used": len(decay_slopes),
        "median_decay_slope_db_per_sec": round(median_slope, 1),
        "decay_slope_iqr": [
            round(float(np.percentile(decay_slopes, 25)), 1),
            round(float(np.percentile(decay_slopes, 75)), 1),
        ],
        "estimated_T60_sec": round(t60_est, 3) if t60_est else None,
        "gate_entry_times_sec": gate_entry_times,
    }


if __name__ == "__main__":
    results = []
    for name, path in VOCAL_STEMS.items():
        if not os.path.exists(path):
            print(f"SKIP {name}: missing {path}")
            continue
        print(f"Analyzing {name} ...")
        r = analyze_decay(name, path)
        results.append(r)
        print(json.dumps(r, ensure_ascii=False, indent=2))

    out_path = os.path.join(os.path.dirname(__file__), "..", "reverb_decay_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nSaved results to {out_path}")
