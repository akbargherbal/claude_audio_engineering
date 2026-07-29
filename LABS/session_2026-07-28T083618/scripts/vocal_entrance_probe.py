#!/usr/bin/env python3
"""
Vocal-entrance probe.
----------------------
Question we're asking (not answering yet): when the human voice comes in,
does something in the mix "fight" it, or does it arrive clean?

For each track we look at a 6-second window centered on the vocal's first
entrance (3s before -> 3s after), and compute three things per 0.25s slice:

1. low_mid_energy  -> energy in 200-500 Hz ("boxiness" band). If this jumps
   right as the vocal starts, something (usually strings/guitar swell) is
   piling up in the same frequency range the human voice lives in, and your
   ear has to fight through clutter to isolate the words.
2. stereo_width    -> how much signal is in the "side" (L-R) channel vs the
   "mid" (L+R) channel. High width = wide/diffuse. If width spikes exactly
   at vocal entrance, the vocal is arriving inside a wash of reverb/pad
   instead of standing centered and dry.
3. rms_db          -> overall loudness in dB, just to see if there's a
   sudden volume jump masking the entrance regardless of frequency content.

Output: one CSV per track + one comparison plot per track, saved next to
this script's parent LABS/session_.../plots folder.
"""
import os
import numpy as np
import librosa
import csv

DATA_DIR = "/home/claude/work/audio_engineering/data"
OUT_DIR = "/home/claude/work/audio_engineering/LABS/session_2026-07-28T083618"

TRACKS = {
    "elisa_reference": ("elisa_maktooba_leek.mp3", 54.590),
    "SONG_A": ("يا دار مية - 28-07-2026_SONG_A.mp3", 26.058),
    "SONG_B": ("يا دار مية - 28-07-2026_SONG_B.mp3", 25.289),
    "SONG_C": ("يا دار مية - 28-07-2026_SONG_C.mp3", 25.229),
    "SONG_D": ("يا دار مية - 28-07-2026_SONG_D.mp3", 28.718),
}

WINDOW_BEFORE = 3.0
WINDOW_AFTER = 3.0
SLICE = 0.25  # seconds per analysis slice

def analyze(path, onset_time):
    y, sr = librosa.load(path, sr=None, mono=False)  # stereo, native sr
    if y.ndim == 1:
        y = np.vstack([y, y])
    L, R = y[0], y[1]
    mid = (L + R) / 2.0
    side = (L - R) / 2.0

    start = onset_time - WINDOW_BEFORE
    end = onset_time + WINDOW_AFTER
    n_slices = int((end - start) / SLICE)

    rows = []
    for i in range(n_slices):
        t0 = start + i * SLICE
        t1 = t0 + SLICE
        s0, s1 = int(t0 * sr), int(t1 * sr)
        if s0 < 0 or s1 > len(mid):
            continue
        mid_chunk = mid[s0:s1]
        side_chunk = side[s0:s1]

        # RMS loudness (mid channel, i.e. the "mono" sum)
        rms = np.sqrt(np.mean(mid_chunk**2) + 1e-12)
        rms_db = 20 * np.log10(rms + 1e-12)

        # Stereo width: energy ratio side/mid
        mid_energy = np.sum(mid_chunk**2) + 1e-12
        side_energy = np.sum(side_chunk**2) + 1e-12
        width = side_energy / mid_energy

        # Low-mid ("boxy") band energy 200-500 Hz via STFT on mid channel
        n_fft = 2048
        if len(mid_chunk) >= n_fft:
            S = np.abs(np.fft.rfft(mid_chunk, n=n_fft))
            freqs = np.fft.rfftfreq(n_fft, 1 / sr)
            band = (freqs >= 200) & (freqs <= 500)
            low_mid_energy = np.sum(S[band] ** 2)
            total_energy = np.sum(S ** 2) + 1e-12
            low_mid_ratio = low_mid_energy / total_energy
        else:
            low_mid_ratio = np.nan

        rows.append({
            "t_rel_to_onset": round(t0 - onset_time, 2),
            "rms_db": round(rms_db, 2),
            "stereo_width": round(width, 4),
            "low_mid_ratio": round(low_mid_ratio, 4) if not np.isnan(low_mid_ratio) else "",
        })
    return rows

def main():
    for name, (fname, onset) in TRACKS.items():
        path = os.path.join(DATA_DIR, fname)
        print(f"Analyzing {name} (onset={onset}s)...")
        rows = analyze(path, onset)
        out_csv = os.path.join(OUT_DIR, f"entrance_{name}.csv")
        with open(out_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["t_rel_to_onset", "rms_db", "stereo_width", "low_mid_ratio"])
            writer.writeheader()
            writer.writerows(rows)
        print(f"  -> {out_csv}")

if __name__ == "__main__":
    main()
