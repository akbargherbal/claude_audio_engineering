"""
Plots the three human-verified reverb-tail segments in Elissa's vocal
(confirmed by ear, see LABS/session_2026-07-29T054751/reverb_tail_investigation.md
and the owner's timestamps), alongside a comparable Ya Dar Maya (Suno) segment.

NOTE ON ARABIC TEXT: matplotlib does not perform Arabic script shaping or
bidi reordering, so Arabic lyric text in plot titles renders as disconnected,
visually-reversed glyphs. We use Latin transliteration in the titles instead
(the original Arabic is kept in a comment below for reference).
"""
import numpy as np
import librosa
import matplotlib.pyplot as plt

def mmss_to_sec(s):
    m, rest = s.split(':')
    return int(m) * 60 + float(rest)

# Original Arabic lyrics (kept for reference; do not use directly as plot text):
#   "قول بقى يا حبيبي.. حبيبي"
#   "طب ده أنا أيامي.."
#   "وحياتي واقفة عليك"
segments = [
    ("\"'ol ba'a ya habibi.. habibi\"", mmss_to_sec('02:20.37'), mmss_to_sec('02:20.78')),
    ("\"tab da ana ayami..\"", mmss_to_sec('02:27.13'), mmss_to_sec('02:27.66')),
    ("\"we hayati wa'fa 'aleek\"", mmss_to_sec('02:32.60'), mmss_to_sec('02:33.70')),
]

y, sr = librosa.load('data/elisa_maktooba_leek/elisa_maktooba_leek-Vocals.mp3', sr=22050, mono=True)
y2, sr2 = librosa.load('data/يا دار مية - 28-07-2026/يا دار مية - 28-07-2026-Vocals.mp3', sr=22050, mono=True)

fig, axes = plt.subplots(4, 1, figsize=(10, 9))
pad = 0.15
for ax, (text, start, end) in zip(axes[:3], segments):
    s_idx = int((start - pad) * sr); e_idx = int((end + pad) * sr)
    seg = y[s_idx:e_idx]
    t = np.arange(len(seg)) / sr - pad
    ax.plot(t, seg, linewidth=0.5, color="#c0392b")
    ax.axvspan(0, end - start, color="yellow", alpha=0.2)
    ax.set_title(f"Elissa — {text}  (tail={end-start:.2f}s, confirmed by ear)")
    ax.set_ylim(-0.06, 0.06)

# comparable Suno segment (Ya Dar Maya, ~153.19s, best available real signal before cutoff)
s_idx = int((152.19) * sr2); e_idx = int((153.34) * sr2)
seg2 = y2[s_idx:e_idx]
t2 = np.arange(len(seg2)) / sr2
axes[3].plot(t2, seg2, linewidth=0.5, color="#2980b9")
axes[3].set_title("Ya Dar Maya (orig) — comparable region (~152.2–153.3s): decays ~58 dB/s (vs Elissa's 3.5–15 dB/s)")
axes[3].set_ylim(-0.06, 0.06)

plt.tight_layout()
plt.savefig('LABS/session_2026-07-29T054751/plots/human_verified_reverb_tails.png', dpi=130)
print("saved")
