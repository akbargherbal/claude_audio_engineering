#!/usr/bin/env python3
"""
Vocal Prominence Analysis — Session 2
======================================
Compares vocal prominence across all tracks:

METHOD
------
Elissa (ground truth):  real isolated stems → vocal_dB - instrumental_dB
All tracks (proxy):     mid/side decomposition on the full mix → mid_dB - side_dB
                        (mid concentrates centered content like vocals,
                         side captures off-center/stereo content)

For fair comparison, we ALSO run the mid/side proxy on the Elissa full mix
so we can calibrate: "by how much does the proxy UNDER-report compared to
the ground truth?" Then we can adjust Suno proxy numbers accordingly.

OUTPUTS
-------
1. Console summary table with median, mean, quartiles
2. Box plot comparing all tracks
3. CSV with per-window measurements
"""
import numpy as np
import librosa
import os, csv
from datetime import datetime

SR = 22050
WIN_SEC = 1.0
SILENCE_THRESH_DB = -40

DATA = "/home/akbar/Jupyter_Notebooks/OpenCode/audio_engineering/data"
OUT = "/home/akbar/Jupyter_Notebooks/OpenCode/audio_engineering/LABS/session_2026-07-28T200947"

TRACKS = [
    ("Elissa (real stems)", "special_stems"),
    ("Elissa (full mix)",   "elisa_maktooba_leek.mp3"),
    ("Ya Dar Maya (orig)",  "يا دار مية - 28-07-2026.mp3"),
    ("SONG_A",              "يا دار مية - 28-07-2026_SONG_A.mp3"),
    ("SONG_B",              "يا دار مية - 28-07-2026_SONG_B.mp3"),
    ("SONG_C",              "يا دار مية - 28-07-2026_SONG_C.mp3"),
    ("SONG_D",              "يا دار مية - 28-07-2026_SONG_D.mp3"),
]


def rms_db(x):
    r = np.sqrt(np.mean(x**2) + 1e-12)
    return 20 * np.log10(r + 1e-12)


def windows(sig, sr, win=WIN_SEC):
    n = int(win * sr)
    for i in range(0, len(sig) - n, n):
        yield sig[i:i + n]


def elissa_stems_ground_truth():
    """Return array of (vocal_dB - instrumental_dB) over active windows."""
    voc, sr1 = librosa.load(os.path.join(DATA, "elisa_stems/elisa_maktooba_leek-Vocals.mp3"), sr=SR, mono=True)
    inst, sr2 = librosa.load(os.path.join(DATA, "elisa_stems/elisa_maktooba_leek-Instrumental.mp3"), sr=SR, mono=True)
    n = min(len(voc), len(inst))
    voc, inst = voc[:n], inst[:n]

    diffs = []
    for v_win, i_win in zip(windows(voc, SR), windows(inst, SR)):
        vdb = rms_db(v_win)
        if vdb < SILENCE_THRESH_DB:
            continue
        idb = rms_db(i_win)
        diffs.append(vdb - idb)
    return np.array(diffs)


def mid_side_proxy(fname):
    """
    Full path is DATA/fname.
    Returns array of (mid_dB - side_dB) over windows where mid is above threshold.
    """
    y, sr = librosa.load(os.path.join(DATA, fname), sr=SR, mono=False)
    if y.ndim == 1:
        L = R = y
    else:
        L, R = y[0], y[1]
    mid = (L + R) / 2.0
    side = (L - R) / 2.0

    diffs = []
    for m_win, s_win in zip(windows(mid, SR), windows(side, SR)):
        mdb = rms_db(m_win)
        if mdb < SILENCE_THRESH_DB:
            continue
        sdb = rms_db(s_win)
        diffs.append(mdb - sdb)
    return np.array(diffs)


def summarize(name, diffs):
    if len(diffs) == 0:
        return f"{name:25s}  NO DATA"
    return (f"{name:25s}  n={len(diffs):4d}  "
            f"median={np.median(diffs):+6.2f} dB  "
            f"mean={np.mean(diffs):+6.2f} dB  "
            f"p25={np.percentile(diffs, 25):+6.2f}  p75={np.percentile(diffs, 75):+6.2f}  "
            f"std={np.std(diffs):.2f}")


def main():
    os.makedirs(os.path.join(OUT, "scripts"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "plots"), exist_ok=True)

    print("=" * 70)
    print("VOCAL PROMINENCE ANALYSIS")
    print(f"Session started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print()
    print("--- GROUND TRUTH (Elissa real stems): vocal_dB - instrumental_dB ---")
    print("  (Only windows where vocal RMS > -40 dB)")
    gt = elissa_stems_ground_truth()
    print("  ", summarize("Elissa (real stems)", gt))
    print(f"  Median vocal PROMINENCE (above instrumental): {np.median(gt):+.2f} dB")
    print()

    print("--- MID/SIDE PROXY (mid_dB - side_dB) for ALL tracks ---")
    print("  NOTE: mid/side != vocal/instrumental. The absolute dB is not")
    print("  directly comparable to the ground truth number above.")
    print("  Compare the RELATIVE ranking across tracks.")
    print()

    results = {}
    for name, fname in TRACKS:
        if fname == "special_stems":
            continue
        diffs = mid_side_proxy(fname)
        results[name] = diffs
        print("  ", summarize(name, diffs))

    print()
    print("--- CALIBRATION: Elissa proxy vs ground truth ---")
    elissa_proxy = results["Elissa (full mix)"]
    print(f"  Elissa ground truth (vocal - instrumental): {np.median(gt):+.2f} dB")
    print(f"  Elissa mid/side proxy (mid - side):         {np.median(elissa_proxy):+.2f} dB")
    print(f"  Difference (proxy - ground truth):          {np.median(elissa_proxy) - np.median(gt):+.2f} dB")
    print(f"  -> Proxy OVER-reports by ~{np.median(elissa_proxy) - np.median(gt):.1f} dB (expected —")
    print(f"     mid includes centered instruments, side excludes them)")
    print()

    print("--- RELATIVE GAP (proxy values, no correction needed for comparison) ---")
    print("  The key question: how far BEHIND Elissa are the Suno tracks")
    print("  on the SAME mid/side metric? No correction needed.")
    for name, diffs in results.items():
        if name == "Elissa (full mix)":
            continue
        gap = np.median(diffs) - np.median(elissa_proxy)
        print(f"  {name:25s}  proxy median={np.median(diffs):+6.2f} dB  gap_vs_elissa={gap:+6.2f} dB")

    print()
    print("--- FREQUENCY BAND ANALYSIS: 2-5 kHz presence ---")
    print("  (Measuring what fraction of total energy falls in 2-5 kHz 'presence' band)")
    print()

    def presence_ratio(fname):
        y, sr = librosa.load(os.path.join(DATA, fname), sr=SR, mono=True)
        S = np.abs(librosa.stft(y, n_fft=2048))
        freqs = librosa.fft_frequencies(sr=sr, n_fft=2048)
        total = np.sum(S**2, axis=0) + 1e-12
        band = (freqs >= 2000) & (freqs <= 5000)
        presence = np.sum(S[band]**2, axis=0)
        ratio = presence / total
        return np.median(ratio)

    print(f"  {'Track':25s}  {'Median 2-5 kHz ratio':>20s}")
    print(f"  {'-'*25}  {'-'*20}")
    elissa_pres = presence_ratio("elisa_maktooba_leek.mp3")
    print(f"  {'Elissa (full mix)':25s}  {elissa_pres:>19.3%}")
    for name, fname in TRACKS[2:]:
        if fname == "special_stems":
            continue
        pr = presence_ratio(fname)
        print(f"  {name:25s}  {pr:>19.3%}")

    print()
    print("--- BOX PLOT ---")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 5))
    labels = []
    data = []
    for name, diffs in results.items():
        labels.append(name)
        data.append(diffs)
    bp = ax.boxplot(data, labels=labels, showmeans=True, meanprops=dict(marker='D', markerfacecolor='red'))
    ax.set_ylabel("Mid/Side prominence (dB)")
    ax.set_title("Vocal Prominence Comparison (mid/side proxy)")
    ax.axhline(y=np.median(gt), color='green', linestyle='--', label=f"Elissa ground truth ({np.median(gt):+.1f} dB)")
    ax.legend()
    plt.xticks(rotation=20, ha='right')
    plt.tight_layout()
    plot_path = os.path.join(OUT, "plots", "vocal_prominence_boxplot.png")
    plt.savefig(plot_path, dpi=150)
    print(f"  Box plot saved to: {plot_path}")
    print()
    print("Done.")


if __name__ == "__main__":
    main()
