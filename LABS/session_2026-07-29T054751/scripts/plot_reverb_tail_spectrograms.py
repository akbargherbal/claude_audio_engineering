import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import os

SR = 22050

# (track_name, path, gate_entry_time_sec) -- picked from reverb_decay_results.json,
# choosing an entry with enough surrounding context (not too close to file start/end)
TARGETS = [
    ("Elissa (ref)", "data/elisa_maktooba_leek/elisa_maktooba_leek-Vocals.mp3", 43.27),
    ("Ya Dar Maya (orig)", "data/يا دار مية - 28-07-2026/يا دار مية - 28-07-2026-Vocals.mp3", 19.95),
    ("SONG_A", "data/يا دار مية - 28-07-2026_SONG_A/يا دار مية - 28-07-2026_SONG_A-Vocals.mp3", 28.89),
    ("SONG_C", "data/يا دار مية - 28-07-2026_SONG_C/يا دار مية - 28-07-2026_SONG_C-Vocals.mp3", 11.61),
]

fig, axes = plt.subplots(len(TARGETS), 1, figsize=(10, 12))

for ax, (name, path, t_gate) in zip(axes, TARGETS):
    y, sr = librosa.load(path, sr=SR, mono=True, offset=max(0, t_gate - 1.5), duration=3.0)
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y, n_fft=2048, hop_length=256)), ref=np.max)
    img = librosa.display.specshow(D, sr=sr, hop_length=256, x_axis="time", y_axis="log",
                                    ax=ax, vmin=-80, vmax=0, cmap="magma")
    ax.axvline(1.5, color="cyan", linewidth=1.2, linestyle="--")  # marks the gate-entry moment
    ax.set_title(f"{name} — around phrase end at t={t_gate}s (cyan = gate entry)")
    ax.set_ylim(80, 8000)

plt.tight_layout()
here = os.path.dirname(__file__)
out_path = os.path.join(here, "..", "plots", "reverb_tail_spectrograms.png")
plt.savefig(out_path, dpi=130)
print(f"Saved to {out_path}")
