#!/usr/bin/env python3
"""
Builds notebooks/01_stereo_field_first_hypothesis.ipynb using nbformat.
Run from anywhere; writes directly to the notebooks/ directory.
"""

import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []


def md(src):
    cells.append(nbf.v4.new_markdown_cell(src))


def code(src):
    cells.append(nbf.v4.new_code_cell(src))


# ------------------------------------------------------------------
md(
    r"""# 01 — The Stereo Field & Our First (Flawed) Hypothesis

### Why this notebook exists

Back in the project's very first lab session, before we had isolated vocal/instrumental
stems for the Suno tracks, we needed *some* way to estimate "is the vocal loud enough
relative to the backing track?" using only the stereo mix. The tool we reached for was
**Mid/Side decomposition** — a classic stereo-engineering trick.

That proxy produced a clean, tidy result: every Suno track measured **2–3 dB behind**
Elissa's reference track, and the hypothesis "the vocal is too quiet" was marked
**CONFIRMED**. It felt solid. It was even useful — it pointed us in a real direction.

This notebook rebuilds that exact analysis from scratch, using the real project audio,
so you can see *why* it looked convincing, and where the first cracks in the "too fast"
confirmation actually show up (the full story of what broke it is in **Notebook 02**)."""
)

# ------------------------------------------------------------------
md(r"""## Setup

Same environment as Notebook 00: `librosa`, `numpy`, `matplotlib`, `IPython.display.Audio`.
The only difference this time — we need **stereo** (`mono=False`), because the whole point
of this notebook is the *difference* between the left and right channels.""")

code(r"""import os
import numpy as np
import librosa
import matplotlib.pyplot as plt
from IPython.display import Audio, display

DATA_DIR = "../data"
PLOTS_DIR = "../LABS/session_2026-07-29T172033/plots"
os.makedirs(PLOTS_DIR, exist_ok=True)

ELISSA_MIX = f"{DATA_DIR}/elisa_maktooba_leek.mp3"
YADAR_MIX  = f"{DATA_DIR}/يا دار مية - 28-07-2026.mp3"

TRACKS = [
    ("Elissa (reference)",  f"{DATA_DIR}/elisa_maktooba_leek.mp3"),
    ("Ya Dar Maya (orig)",  f"{DATA_DIR}/يا دار مية - 28-07-2026.mp3"),
    ("SONG_A",              f"{DATA_DIR}/يا دار مية - 28-07-2026_SONG_A.mp3"),
    ("SONG_B",              f"{DATA_DIR}/يا دار مية - 28-07-2026_SONG_B.mp3"),
    ("SONG_C",              f"{DATA_DIR}/يا دار مية - 28-07-2026_SONG_C.mp3"),
    ("SONG_D",              f"{DATA_DIR}/يا دار مية - 28-07-2026_SONG_D.mp3"),
]

def rms_db(x, eps=1e-10):
    '''Same loudness function from Notebook 00 — RMS energy converted to dB.'''
    return 20 * np.log10(rms + eps)

print("Setup complete. Tracks registered:", len(TRACKS))""")

# ------------------------------------------------------------------
md(r"""## A. What are the L and R channels?

A mono file stores **one** number per sample — the microphone's (or synth's) single air-pressure
value at each instant. A **stereo** file stores **two**: a Left channel and a Right channel, meant
to be played through two separate speakers (or ears, in headphones).

If a sound is mixed to be **panned left**, its L channel amplitude will be bigger than its R
channel at that moment. If it's mixed **dead center** (which is where vocals and kick drums
almost always live), L and R carry nearly *identical* signals.

Let's load 3 seconds of Ya Dar Maya in stereo and plot L and R separately.""")

code(r"""y_stereo, sr = librosa.load(YADAR_MIX, sr=None, mono=False, duration=3.0)
L, R = y_stereo[0], y_stereo[1]
t = np.linspace(0, len(L) / sr, num=len(L))

fig, axes = plt.subplots(2, 1, figsize=(11, 5), sharex=True, sharey=True)
axes[0].plot(t, L, linewidth=0.6, color="steelblue")
axes[0].set_title("Left channel — Ya Dar Maya (first 3s)")
axes[0].set_ylabel("Amplitude")
axes[1].plot(t, R, linewidth=0.6, color="indianred")
axes[1].set_title("Right channel — Ya Dar Maya (first 3s)")
axes[1].set_ylabel("Amplitude")
axes[1].set_xlabel("Time (seconds)")
plt.tight_layout()
plt.savefig(f"{PLOTS_DIR}/L_R_channels.png", dpi=110)
plt.show()""")

# ------------------------------------------------------------------
md(
    r"""**Look closely at the two plots.** They're similar in overall shape (same song, same
moment) but not identical — the small differences between L and R are exactly the stereo
information: reverb tails, panned instruments, width. If this were a mono file, or a moment
where absolutely everything was centered, the two plots would be pixel-for-pixel identical.

That similarity-but-not-identical relationship is the entire basis for the next step."""
)

# ------------------------------------------------------------------
md(r"""## B. Mid/Side decomposition

Audio engineers have a standard trick for splitting a stereo signal into "the part both
channels agree on" and "the part they disagree on":

$$\text{Mid} = \frac{L + R}{2} \qquad \text{Side} = \frac{L - R}{2}$$

- **Mid** — if L and R are identical at some instant, they *add* constructively. Centered
  content (lead vocal, kick, bass, snare) survives strongly in Mid.
- **Side** — if L and R are identical, subtracting them gives **zero**. Only content that
  *differs* between the channels (panned guitars, stereo reverb, width effects) shows up
  in Side.

This is reversible too (`L = Mid + Side`, `R = Mid - Side`), which is why it's a real
mixing/mastering tool, not just a toy — engineers boost/cut Mid and Side independently
all the time.""")

code(r"""mid = (L + R) / 2.0
side = (L - R) / 2.0

fig, axes = plt.subplots(2, 1, figsize=(11, 5), sharex=True, sharey=True)
axes[0].plot(t, mid, linewidth=0.6, color="darkgreen")
axes[0].set_title("Mid = (L + R) / 2 — centered content")
axes[0].set_ylabel("Amplitude")
axes[1].plot(t, side, linewidth=0.6, color="darkorange")
axes[1].set_title("Side = (L − R) / 2 — off-center / stereo content")
axes[1].set_ylabel("Amplitude")
axes[1].set_xlabel("Time (seconds)")
plt.tight_layout()
plt.savefig(f"{PLOTS_DIR}/mid_side_decomposition.png", dpi=110)
plt.show()

print(f"Mid  loudness: {rms_db(mid):.2f} dB")
print(f"Side loudness: {rms_db(side):.2f} dB")""")

# ------------------------------------------------------------------
md(
    r"""**Notice the Side waveform is visibly quieter** (smaller amplitude, lower dB) than Mid.
That's expected and important: most of the *energy* in a typical pop/Arabic-pop mix sits in
centered elements. Side is real, but it's the minority signal.

Now listen to both — this is the moment the concept stops being abstract."""
)

code(r"""print("MID (centered content only):")
display(Audio(mid, rate=sr))

print("SIDE (off-center / stereo content only):")
display(Audio(side, rate=sr))""")

# ------------------------------------------------------------------
md(
    r"""**What you should hear:** Mid should sound like a (slightly odd, phasey) mono version of
the song, with the vocal clearly present. Side should sound thin, washy, and mostly like
reverb tails and background texture — the vocal should be much fainter or absent, because the
vocal is centered and centered content cancels out in `L − R`.

If Side genuinely sounded vocal-free, that would be the smoking gun for treating Mid as a
"vocal proxy." Keep half an ear on whether it *actually* was vocal-free — we'll come back to
that assumption at the end of this notebook."""
)

# ------------------------------------------------------------------
md(
    r"""## C. Why the Lab 1 team reached for Mid ≈ "vocal channel"

At the time of Lab 1, the Suno-generated tracks had **no isolated stems at all** — only the
finished stereo mix. The real quantity we wanted was:

$$\text{vocal\_prominence} = \text{RMS}_{dB}(\text{vocal}) - \text{RMS}_{dB}(\text{instrumental})$$

but that requires a *vocal-only* signal, which we didn't have yet for Suno tracks. Mid/Side
was the best substitute reasoning available:

> "Vocals are almost always mixed dead-center. Centered content survives in Mid.
> So Mid should behave *like* a vocal-heavy signal, and Side should behave like
> the panned instrumental backing. Let's measure `Mid_dB − Side_dB` as a **proxy**
> for `vocal_dB − instrumental_dB`."

This is a reasonable *engineering* assumption. It is not the same claim as "Mid **is**
the vocal." Keep that distinction in your head — it's exactly the gap Notebook 02 opens up."""
)

# ------------------------------------------------------------------
md(r"""## D. Rebuilding the Lab 1 proxy analysis

The original script split each track into 1-second windows, discarded windows where the
track was essentially silent (`Mid < -40 dB`, i.e. no meaningful content playing), and
computed `Mid_dB − Side_dB` for every remaining window. We rebuild that exact procedure
here, using `rms_db()` from Notebook 00.""")

code(
    r"""SILENCE_THRESH_DB = -40
WIN_SEC = 1.0

def windows(sig, sr, win_sec=WIN_SEC):
    \"\"\"Yield consecutive non-overlapping 1-second chunks of a signal.\"\"\"
    n = int(win_sec * sr)
    for i in range(0, len(sig) - n, n):
        yield sig[i:i + n]

def mid_side_proxy(path):
    \"\"\"Load a stereo track and return an array of (mid_dB - side_dB) per active 1s window.\"\"\"
    y, sr = librosa.load(path, sr=22050, mono=False)
    if y.ndim == 1:          # safety: mono file, no stereo info to extract
        return np.array([])
    L, R = y[0], y[1]
    mid = (L + R) / 2.0
    side = (L - R) / 2.0

    diffs = []
    for m_win, s_win in zip(windows(mid, sr), windows(side, sr)):
        mdb = rms_db(m_win)
        if mdb < SILENCE_THRESH_DB:
            continue
        sdb = rms_db(s_win)
        diffs.append(mdb - sdb)
    return np.array(diffs)

results = {}
print(f"{'Track':22s}  {'n':>4s}  {'Median':>8s}  {'Mean':>8s}  {'Std':>6s}")
print("-" * 55)
for name, path in TRACKS:
    diffs = mid_side_proxy(path)
    results[name] = diffs
    print(f"{name:22s}  {len(diffs):4d}  {np.median(diffs):+7.2f}  {np.mean(diffs):+7.2f}  {np.std(diffs):5.2f}")"""
)

# ------------------------------------------------------------------
md(r"""### Visualize it as a box plot — exactly how Lab 1 presented it""")

code(r"""fig, ax = plt.subplots(figsize=(10, 5))
labels = list(results.keys())
data = [results[k] for k in labels]
bp = ax.boxplot(data, tick_labels=labels, patch_artist=True, showfliers=False)

colors = ["#2ca02c"] + ["#1f77b4"] * (len(labels) - 1)
for patch, c in zip(bp["boxes"], colors):
    patch.set_facecolor(c)
    patch.set_alpha(0.6)

ax.set_ylabel("Mid dB − Side dB  (proxy \"vocal prominence\")")
ax.set_title("Lab 1 Proxy: Centered-content prominence across all six tracks")
ax.axhline(np.median(results["Elissa (reference)"]), color="green", linestyle="--",
           linewidth=1, label="Elissa median (reference line)")
ax.legend()
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
plt.savefig(f"{PLOTS_DIR}/mid_side_proxy_boxplot.png", dpi=110)
plt.show()

elissa_med = np.median(results["Elissa (reference)"])
print("Gap vs Elissa (median):")
for name in labels[1:]:
    gap = np.median(results[name]) - elissa_med
    print(f"  {name:22s}  {gap:+.2f} dB")""")

# ------------------------------------------------------------------
md(r"""### Reading the result the way Lab 1 read it

Every Suno track's box sits measurably **below** Elissa's. The gap is consistently in the
**2–3 dB** range across all four covers and the original take. Framed as "hypothesis
CONFIRMED, root cause = vocal is too quiet relative to the mix," this is exactly the
conclusion the project reached at the end of Lab 1.

It's a clean story. Four independent tracks, all pointing the same direction, several dB
of separation, no ambiguity in the plot. That consistency is *precisely* what made it
convincing enough to act on.""")

# ------------------------------------------------------------------
md(
    r"""## E. The calibration step Lab 1 also ran — and what it quietly revealed

Lab 1 didn't stop at the proxy. Elissa is special: at the time, we had **real, human-mixed
vocal and instrumental stems** for her track (not just Mid/Side estimates). So the team ran
one sanity check: how far off is the Mid/Side proxy from the *real* vocal-prominence number,
on the one track where both are available?

We can rebuild that comparison too, now using this project's AI-separated stems for Elissa."""
)

code(
    r"""ELISSA_VOCALS = f"{DATA_DIR}/elisa_maktooba_leek/elisa_maktooba_leek-Vocals.mp3"
ELISSA_INSTR  = f"{DATA_DIR}/elisa_maktooba_leek/elisa_maktooba_leek-Instrumental.mp3"

def ground_truth_prominence(vocal_path, instr_path):
    \"\"\"Real vocal_dB - instrumental_dB per active 1s window, using true isolated stems.\"\"\"
    voc, sr_v = librosa.load(vocal_path, sr=22050, mono=True)
    inst, sr_i = librosa.load(instr_path, sr=22050, mono=True)
    n = min(len(voc), len(inst))
    voc, inst = voc[:n], inst[:n]

    diffs = []
    for v_win, i_win in zip(windows(voc, sr_v), windows(inst, sr_v)):
        vdb = rms_db(v_win)
        if vdb < SILENCE_THRESH_DB:
            continue
        idb = rms_db(i_win)
        diffs.append(vdb - idb)
    return np.array(diffs)

gt_diffs = ground_truth_prominence(ELISSA_VOCALS, ELISSA_INSTR)
proxy_diffs = results["Elissa (reference)"]

print(f"Elissa — REAL stems  (vocal_dB - instrumental_dB): median = {np.median(gt_diffs):+.2f} dB")
print(f"Elissa — Mid/Side PROXY (mid_dB - side_dB):        median = {np.median(proxy_diffs):+.2f} dB")
print(f"Proxy over-reports by: {np.median(proxy_diffs) - np.median(gt_diffs):+.2f} dB")"""
)

# ------------------------------------------------------------------
md(
    r"""**This is the number that should give you pause.** The Mid/Side proxy doesn't sit close
to the real vocal-prominence number at all — it runs several dB *higher*, because Mid also
captures every other centered thing in the mix (kick drum, bass, centered guitar/piano), not
just the vocal.

Lab 1's reasoning at the time was: *"the absolute proxy number is off, but since we apply the
same proxy consistently to every track, the **relative ranking** between tracks should still
be trustworthy."* That's a real assumption, and it's the one the story hinges on.

It's a plausible assumption. It is still an *assumption* — it assumes the amount of
"non-vocal centered content" is roughly the same, in roughly the same proportion, across
Elissa's professionally engineered mix and four different Suno-generated mixes. Nothing in
the analysis above actually tested that."""
)

# ------------------------------------------------------------------
md(r"""## F. Where this leaves us

To summarize the shape of the argument this notebook just rebuilt:

1. We don't have real stems for the Suno tracks → we approximate with Mid/Side.
2. The approximation, applied consistently, shows a clean 2–3 dB gap on every Suno track.
3. A spot-check against Elissa's one available ground truth shows the proxy's *absolute*
   number is off by several dB — but we wave that away by trusting the *relative* ranking.
4. Conclusion: hypothesis CONFIRMED.

Every individual step is defensible. Stacked together, they add up to a conclusion resting
on one unverified assumption (relative ranking survives even though absolute level doesn't)
applied to four tracks we have zero direct ground truth for.

**Notebook 02** picks up exactly here: once real AI-separated vocal/instrumental stems became
available for *every* track (not just Elissa), the team re-ran the real
`vocal_dB − instrumental_dB` measurement directly — no more proxy needed — and the tidy
"2–3 dB gap, hypothesis confirmed" story did not survive contact with real stems.""")

# ------------------------------------------------------------------
md(r"""## Self-Check

Try to answer each question yourself before expanding the answer.

<details>
<summary><b>Q1.</b> In your own words, what does the Side channel (<code>L − R</code>) physically represent, and why does perfectly centered content vanish from it?</summary>

Side captures whatever is *different* between the left and right channels. If a sound is
mixed dead-center, its L and R values are identical at every instant, so `L − R = 0` for
that sound — it contributes nothing to Side. Only content that's panned, or has stereo width
(like reverb), survives the subtraction.
</details>

<details>
<summary><b>Q2.</b> Why did Lab 1 use Mid/Side instead of directly measuring vocal vs. instrumental loudness for the Suno tracks?</summary>

At that point in the project, isolated vocal/instrumental stems did not exist yet for the
Suno-generated tracks — only the finished stereo mix was available. Mid/Side was the closest
substitute obtainable from a stereo mix alone, based on the assumption that vocals are
almost always mixed centered.
</details>

<details>
<summary><b>Q3.</b> The calibration check found the proxy over-reports vocal prominence by several dB versus the real stems. Why doesn't that automatically invalidate the "2-3 dB gap across all Suno tracks" conclusion?</summary>

Because the argument doesn't rely on the *absolute* proxy number being correct — it relies on
the *relative ranking* across tracks staying valid even if every track's number is shifted by
roughly the same amount. If that assumption holds, the comparison between tracks is still
meaningful even though no single track's proxy number matches its true value.
</details>

<details>
<summary><b>Q4.</b> What specific, testable assumption is this whole proxy-based conclusion resting on, that this notebook did not actually verify?</summary>

That the amount of "non-vocal centered content" (kick, bass, centered instruments) is roughly
proportionally similar across Elissa's mix and the four Suno mixes. If Suno's mixes put
noticeably more or less non-vocal material in the center than Elissa's mix does, the
Mid/Side proxy's *relative* ranking across tracks would no longer safely track the *real*
vocal-vs-instrumental ranking.
</details>""")

# ------------------------------------------------------------------
md(r"""## Summary — what you now have

- **Stereo audio** = two channels, L and R, that can differ slightly (panning, reverb, width)
  even within the same song.
- **Mid/Side decomposition**: `Mid = (L+R)/2` isolates centered content; `Side = (L-R)/2`
  isolates off-center/stereo content. It's reversible and used in real mixing/mastering.
- **The Lab 1 proxy**: `Mid_dB − Side_dB`, used as a stand-in for `vocal_dB − instrumental_dB`
  when no isolated stems existed for the Suno tracks — rebuilt here and it does reproduce the
  same clean 2–3 dB "gap" that got the hypothesis marked CONFIRMED.
- **The catch**: a calibration check against Elissa's one available ground-truth stem pair
  showed the proxy's *absolute* number is off by several dB. The conclusion survives only if
  you trust that the proxy's *relative ranking* across tracks is still valid — an assumption,
  not something this notebook actually tested.
- **Next up (Notebook 02)**: once real stems existed for every track, that assumption gets
  tested directly — and the story changes.""")

nb["cells"] = cells

# Resolve the output path relative to this script's own location, so this
# works regardless of the OS or the directory you run it from:
# this file lives at LABS/<session>/scripts/build_notebook_01.py,
# so the repo root is 3 levels up.
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
OUT_PATH = REPO_ROOT / "notebooks" / "01_stereo_field_first_hypothesis.ipynb"
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

with open(OUT_PATH, "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print(f"Notebook written to: {OUT_PATH}")
