#!/usr/bin/env python3
"""
Stem-Based Analysis — Session 2
================================
Now that EVERY track has separated Vocal + Instrumental stems, we can:

1. VALIDATE the separation quality by comparing Elissa's AI-separated stems
   against the official (ground-truth) stems.
2. DIRECT vocal prominence measurement (vocal_dB - instrumental_dB) on ALL
   tracks — no more mid/side proxy needed!
3. FREQUENCY analysis: where does each stem sit spectrally?
4. CONSISTENCY: does the vocal level fluctuate across the track?

This completely replaces the proxy approach from Session 1.
"""
import numpy as np
import librosa
import os

SR = 22050
WIN_SEC = 1.0
SILENCE_THRESH_DB = -40

DATA = "/home/akbar/Jupyter_Notebooks/OpenCode/audio_engineering/data"
OUT = "/home/akbar/Jupyter_Notebooks/OpenCode/audio_engineering/LABS/session_2026-07-28T200947"
PLOTS = os.path.join(OUT, "plots")

TRACKS = [
    ("Elissa",           "elisa_maktooba_leek"),
    ("Ya Dar Maya (orig)", "يا دار مية - 28-07-2026"),
    ("SONG_A",           "يا دار مية - 28-07-2026_SONG_A"),
    ("SONG_B",           "يا دار مية - 28-07-2026_SONG_B"),
    ("SONG_C",           "يا دار مية - 28-07-2026_SONG_C"),
    ("SONG_D",           "يا دار مية - 28-07-2026_SONG_D"),
]


def rms_db(x):
    r = np.sqrt(np.mean(x**2) + 1e-12)
    return 20 * np.log10(r + 1e-12)


def windows(sig, sr, win=WIN_SEC):
    n = int(win * sr)
    for i in range(0, len(sig) - n, n):
        yield sig[i:i + n]


def load_stem(track_dir, suffix):
    """Load a stem file from the track subdirectory."""
    path = os.path.join(DATA, track_dir, f"{track_dir}-{suffix}.mp3")
    if not os.path.exists(path):
        print(f"  WARNING: {path} not found")
        return None, None
    y, sr = librosa.load(path, sr=SR, mono=True)
    return y, sr


def vocal_prominence(voc, inst, sr):
    """Compute vocal_dB - instrumental_dB over active windows."""
    n = min(len(voc), len(inst))
    voc, inst = voc[:n], inst[:n]
    diffs = []
    voc_levels = []
    inst_levels = []
    for v_win, i_win in zip(windows(voc, sr), windows(inst, sr)):
        vdb = rms_db(v_win)
        if vdb < SILENCE_THRESH_DB:
            continue
        idb = rms_db(i_win)
        diffs.append(vdb - idb)
        voc_levels.append(vdb)
        inst_levels.append(idb)
    return np.array(diffs), np.array(voc_levels), np.array(inst_levels)


def spectral_profile(y, sr):
    """Return frequency bins and median magnitude spectrum."""
    S = np.abs(librosa.stft(y, n_fft=2048))
    mag = np.median(S, axis=1)
    freqs = librosa.fft_frequencies(sr=sr, n_fft=2048)
    return freqs, mag


def summarize_prominence(name, diffs):
    if len(diffs) == 0:
        return f"{name:25s}  NO DATA"
    return (f"{name:25s}  n={len(diffs):4d}  "
            f"median={np.median(diffs):+6.2f} dB  "
            f"mean={np.mean(diffs):+6.2f} dB  "
            f"p25={np.percentile(diffs, 25):+6.2f}  p75={np.percentile(diffs, 75):+6.2f}  "
            f"std={np.std(diffs):.2f}")


def main():
    os.makedirs(PLOTS, exist_ok=True)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    print("=" * 70)
    print("STEM-BASED ANALYSIS")
    print("=" * 70)

    # =========================================================
    # 1. DIRECT VOCAL PROMINENCE — ALL TRACKS (real stems now!)
    # =========================================================
    # =========================================================
    print()
    print("2. VOCAL PROMINENCE — ALL TRACKS (direct stems)")
    print("-" * 50)
    print(f"  {'Track':25s}  {'n':>4s}  {'Median':>7s}  {'Mean':>7s}  {'p25':>7s}  {'p75':>7s}  {'Std':>5s}")
    print(f"  {'-'*25}  {'-'*4}  {'-'*7}  {'-'*7}  {'-'*7}  {'-'*7}  {'-'*5}")

    all_results = {}
    for name, track_dir in TRACKS:
        voc, sr_v = load_stem(track_dir, "Vocals")
        inst, sr_i = load_stem(track_dir, "Instrumental")
        if voc is None or inst is None:
            continue
        diffs, voc_levels, inst_levels = vocal_prominence(voc, inst, sr_v)
        all_results[name] = {
            "diffs": diffs,
            "voc_levels": voc_levels,
            "inst_levels": inst_levels,
        }
        print(" ", summarize_prominence(name, diffs))

    # =========================================================
    # 2. VOCAL LEVEL CONSISTENCY
    # =========================================================
    print()
    print("3. VOCAL LEVEL CONSISTENCY")
    print("-" * 50)
    print("  How much does the vocal-instrumental balance fluctuate?")
    print(f"  {'Track':25s}  {'Std Dev':>8s}  {'IQR':>8s}  {'Range':>8s}")
    print(f"  {'-'*25}  {'-'*8}  {'-'*8}  {'-'*8}")
    for name, result in all_results.items():
        d = result["diffs"]
        std = np.std(d)
        iqr = np.percentile(d, 75) - np.percentile(d, 25)
        rng = np.max(d) - np.min(d)
        print(f"  {name:25s}  {std:6.2f} dB  {iqr:6.2f} dB  {rng:6.2f} dB")

    # =========================================================
    # 3. SPECTRAL ANALYSIS: Vocal vs Instrumental
    # =========================================================
    print()
    print("4. SPECTRAL PROFILE: Vocal vs Instrumental")
    print("-" * 50)

    fig, axes = plt.subplots(len(TRACKS), 1, figsize=(12, 3 * len(TRACKS)))
    if len(TRACKS) == 1:
        axes = [axes]

    for idx, (name, track_dir) in enumerate(TRACKS):
        voc, sr_v = load_stem(track_dir, "Vocals")
        inst, sr_i = load_stem(track_dir, "Instrumental")
        if voc is None or inst is None:
            continue
        freqs, voc_spec = spectral_profile(voc, sr_v)
        _, inst_spec = spectral_profile(inst, sr_i)

        ax = axes[idx]
        ax.semilogx(freqs, 20 * np.log10(voc_spec + 1e-12), label="Vocal", alpha=0.8)
        ax.semilogx(freqs, 20 * np.log10(inst_spec + 1e-12), label="Instrumental", alpha=0.8)
        ax.axvspan(2000, 5000, color='yellow', alpha=0.15, label="2-5 kHz band")
        ax.set_title(f"{name} — Vocal vs Instrumental Spectrum")
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Magnitude (dB)")
        ax.set_xlim(20, 10000)
        ax.legend()
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS, "spectral_profiles.png"), dpi=150)
    plt.close()
    print(f"  Spectral profiles: plots/spectral_profiles.png")

    # =========================================================
    # 4. FREQUENCY BAND BREAKDOWN
    # =========================================================
    print()
    print("5. FREQUENCY BAND ENERGY DISTRIBUTION")
    print("-" * 50)

    bands = {
        "Sub (20-60 Hz)":   (20, 60),
        "Bass (60-250 Hz)": (60, 250),
        "Low-Mid (250-500)": (250, 500),
        "Mid (500-2k)":     (500, 2000),
        "Presence (2-5k)":  (2000, 5000),
        "Treble (5-20k)":   (5000, 20000),
    }

    def band_energy(y, sr, low, high):
        S = np.abs(librosa.stft(y, n_fft=2048)) ** 2
        freqs = librosa.fft_frequencies(sr=sr, n_fft=2048)
        mask = (freqs >= low) & (freqs < high)
        total = np.sum(S, axis=0) + 1e-12
        band = np.sum(S[mask], axis=0)
        return np.median(band / total)

    print(f"  {'Track':25s}", end="")
    for bname in bands:
        print(f"  {bname:>14s}", end="")
    print()
    print(f"  {'-'*25}  {'-'*14}  {'-'*14}  {'-'*14}  {'-'*14}  {'-'*14}  {'-'*14}")

    for name, track_dir in TRACKS:
        voc, sr_v = load_stem(track_dir, "Vocals")
        if voc is None:
            continue
        print(f"  {name:25s}", end="")
        for bname, (lo, hi) in bands.items():
            ratio = band_energy(voc, sr_v, lo, hi)
            print(f"  {ratio:13.3%}", end="")
        print()

    print()
    print(f"  {'Track':25s}  {'Elissa vocal vs Inst':>21s}")
    print(f"  {'-'*25}  {'-'*21}")
    elissa_voc, sr_ev = load_stem("elisa_maktooba_leek", "Vocals")
    elissa_inst, sr_ei = load_stem("elisa_maktooba_leek", "Instrumental")
    if elissa_voc is not None:
        for bname, (lo, hi) in bands.items():
            v_ratio = band_energy(elissa_voc, sr_ev, lo, hi)
            i_ratio = band_energy(elissa_inst, sr_ei, lo, hi)
            ratio_diff = v_ratio / (i_ratio + 1e-12)
            print(f"  {bname:25s}  vocal={v_ratio:.3%}  inst={i_ratio:.3%}  "
                  f"v/i ratio={ratio_diff:.2f}x")

    print()
    print("DONE. Plots saved to plots/.")


if __name__ == "__main__":
    main()
