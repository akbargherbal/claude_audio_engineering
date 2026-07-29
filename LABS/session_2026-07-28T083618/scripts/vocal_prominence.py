#!/usr/bin/env python3
"""
Vocal prominence test.
-----------------------
Question: is the Suno vocal (SONG_A/C) actually quieter relative to the
instrumental than Elissa's vocal is, or does it just *feel* less
commanding for some other reason?

Elissa: we have REAL isolated stems (Instrumental + Vocals), so we can
measure the actual vocal-to-instrumental level ratio in dB, in short
time windows across the vocal-active parts of the song.

Suno tracks (A, C): we do NOT have real stems. As an approximation we
use a center-channel extraction (mid = (L+R)/2 tends to concentrate
centered/panned vocal content since vocals are usually mixed dead
center, while wide reverb/stereo instruments partially cancel out) to
get a rough "vocal-weighted" signal, and compare it to the full mix.
This is a proxy, not a real separation -- treat the Suno numbers as
directional, not as precise as the Elissa ground-truth numbers.

Both are reported as: vocal_level_db - instrumental_level_db, computed
over 1-second windows, restricted to windows where the vocal stem (or
proxy) actually has energy above a silence threshold (so we're not
diluting the measurement with instrumental-only passages).
"""
import numpy as np
import librosa
import os

DATA = "/home/claude/work/audio_engineering/data"

def rms_db(x):
    r = np.sqrt(np.mean(x**2) + 1e-12)
    return 20*np.log10(r + 1e-12)

def windows(sig, sr, win=1.0):
    n = int(win*sr)
    for i in range(0, len(sig)-n, n):
        yield sig[i:i+n]

def elissa_ground_truth():
    voc, sr1 = librosa.load(os.path.join(DATA, "elisa_stems/elisa_maktooba_leek-Vocals.mp3"), sr=None, mono=True)
    inst, sr2 = librosa.load(os.path.join(DATA, "elisa_stems/elisa_maktooba_leek-Instrumental.mp3"), sr=None, mono=True)
    assert sr1 == sr2
    sr = sr1
    n = min(len(voc), len(inst))
    voc, inst = voc[:n], inst[:n]

    diffs = []
    silence_thresh_db = -40
    for v_win, i_win in zip(windows(voc, sr), windows(inst, sr)):
        vdb = rms_db(v_win)
        if vdb < silence_thresh_db:
            continue  # vocal not active in this window
        idb = rms_db(i_win)
        diffs.append(vdb - idb)
    return np.array(diffs)

def suno_proxy(fname):
    y, sr = librosa.load(os.path.join(DATA, fname), sr=None, mono=False)
    L, R = y[0], y[1]
    mid = (L+R)/2.0   # vocal-weighted proxy (centered content)
    side = (L-R)/2.0  # instrumental/width-weighted proxy (off-center content)
    diffs = []
    silence_thresh_db = -40
    for m_win, s_win in zip(windows(mid, sr), windows(side, sr)):
        mdb = rms_db(m_win)
        if mdb < silence_thresh_db:
            continue
        sdb = rms_db(s_win)
        diffs.append(mdb - sdb)
    return np.array(diffs)

def summarize(name, diffs):
    print(f"{name:20s}  n_windows={len(diffs):4d}  median={np.median(diffs):+.2f}dB  "
          f"mean={np.mean(diffs):+.2f}dB  p25={np.percentile(diffs,25):+.2f}dB  p75={np.percentile(diffs,75):+.2f}dB")

if __name__ == "__main__":
    print("=== GROUND TRUTH (real stems): vocal_dB - instrumental_dB ===")
    d = elissa_ground_truth()
    summarize("Elissa (real)", d)

    print()
    print("=== PROXY (center-channel estimate): mid_dB - side_dB ===")
    print("(NOTE: not directly comparable in absolute dB to the ground-truth number above --")
    print(" mid/side is a different decomposition than true vocal/instrumental stems.")
    print(" Compare the RELATIVE ranking and spread between tracks, not the raw dB value.)")
    for name, fname in [
        ("Elissa (proxy, sanity check)", "elisa_maktooba_leek.mp3"),
        ("SONG_A", "يا دار مية - 28-07-2026_SONG_A.mp3"),
        ("SONG_C", "يا دار مية - 28-07-2026_SONG_C.mp3"),
    ]:
        d = suno_proxy(fname)
        summarize(name, d)
