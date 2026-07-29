import numpy as np
import librosa
import matplotlib.pyplot as plt
import os

SR = 22050

TARGETS = [
    ("Elissa (ref)", "data/elisa_maktooba_leek/elisa_maktooba_leek-Vocals.mp3", 154.95),
    ("Ya Dar Maya (orig)", "data/يا دار مية - 28-07-2026/يا دار مية - 28-07-2026-Vocals.mp3", 144.06),
    ("SONG_A", "data/يا دار مية - 28-07-2026_SONG_A/يا دار مية - 28-07-2026_SONG_A-Vocals.mp3", 146.19),
    ("SONG_C", "data/يا دار مية - 28-07-2026_SONG_C/يا دار مية - 28-07-2026_SONG_C-Vocals.mp3", 144.06),
]

fig, axes = plt.subplots(len(TARGETS), 1, figsize=(11, 10), sharex=True)

results = []
for ax, (name, path, t_gate) in zip(axes, TARGETS):
    y, sr = librosa.load(path, sr=SR, mono=True, offset=max(0, t_gate - 0.5), duration=1.5)
    t = np.arange(len(y)) / sr - 0.5  # 0 = the gate-entry moment

    # Find the last sample index before the gate that is above a tiny
    # "true silence" amplitude threshold, then measure how long
    # non-negligible amplitude persists AFTER the marked gate moment.
    thresh = 0.0005  # linear amplitude, well above digital dither noise
    post_mask = t >= 0
    post_y = np.abs(y[post_mask])
    if np.any(post_y > thresh):
        last_idx = np.where(post_y > thresh)[0][-1]
        tail_duration_ms = (last_idx / sr) * 1000
    else:
        tail_duration_ms = 0.0

    results.append((name, tail_duration_ms))

    ax.plot(t, y, linewidth=0.4, color="#2c3e50")
    ax.axvline(0, color="red", linestyle="--", linewidth=1)
    ax.set_title(f"{name} — tail after gate-moment: {tail_duration_ms:.0f} ms of audible amplitude")
    ax.set_ylim(-0.05, 0.05)  # zoomed in to see the tail, not the loud phrase
    ax.set_ylabel("amplitude")

axes[-1].set_xlabel("time relative to phrase-end (s)")
plt.tight_layout()
here = os.path.dirname(__file__)
out_path = os.path.join(here, "..", "plots", "raw_waveform_tail_comparison.png")
plt.savefig(out_path, dpi=130)
print(f"Saved to {out_path}")
for name, dur in results:
    print(f"{name}: {dur:.0f} ms of amplitude above {thresh} after gate moment")
