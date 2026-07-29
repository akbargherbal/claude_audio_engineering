# Lab Session 3 — Separation Quality Audit (Priority 1)

## Question

Before trusting the Session 2 "consistency" numbers (Elissa std 4.11 dB vs.
Ya Dar Maya orig std 13.55 dB), is the AI stem separation itself reliable —
and reliable to the *same degree* across the natural (Elissa) and
synthetic (Suno) tracks? If not, the consistency gap could be partly a
measurement artifact, not a real mix difference.

No ground-truth official stems exist anymore for comparison (Elissa's old
official stems were replaced — `context.md` §1), so this audit uses two
label-free proxies instead.

## Method

For each track: load original mix + vocal stem + instrumental stem (same
duration, 22.05 kHz mono).

1. **Reconstruction fidelity** — `vocal + instrumental` should sum back to
   the original mix if separation is a clean additive decomposition.
   Measured per-second RMS error (dB) and full-signal correlation.
2. **Vocal-stem residual audit** — looked at the quietest 1-second frames
   of the vocal stem (where no singing should be present) and measured
   their RMS level and spectral flatness (flatness → 1.0 = pure noise;
   low flatness = tonal/structured residual, i.e. bleed from the
   instrumental bed).

## Unexpected Discovery

The vocal stems are **not** continuously "quiet-but-present" in
non-singing sections — a large fraction of frames (**21%–31%, all six
tracks**) are literal digital-zero silence, not just low-level. This
looks like a hard gate applied by the separation tool/export step, and it
applies uniformly — it is **not** a Suno-vs-natural difference. The first
version of this script's "quiet frame" metric was measuring this gate
floor (-200 dB) instead of real residual signal, so it was re-run
excluding hard-gated frames.

## Results

| Track | Reconstruction err (median dB) | Reconstruction corr | Hard-silent frames | Residual RMS (quietest non-gated, dB) | Residual flatness |
|---|---|---|---|---|---|
| Elissa (ref) | **−2.75** | 0.9993 | 31.2% | **−88.3** | **0.43** |
| Ya Dar Maya (orig) | −0.0 | 0.9999 | 21.0% | −120.1 | 0.96 |
| SONG_A | −0.0 | 0.9999 | 27.9% | −125.1 | 0.96 |
| SONG_B | −0.0 | 0.9999 | 30.0% | −101.5 | 0.67 |
| SONG_C | −0.0 | 1.0000 | 22.2% | −100.9 | 0.68 |
| SONG_D | −0.32 | 1.0000 | 27.4% | −110.6 | 0.66 |

## Interpretation

1. **Reconstruction gap is Elissa-specific.** Summing Elissa's two stems
   comes back **2.75 dB quieter** than the original mix (still 0.9993
   correlated in shape). All Suno tracks reconstruct almost perfectly
   (≈0 dB gap). This is consistent with Elissa being a real studio
   recording with room ambience/reverb tails and mastering effects that
   don't cleanly attribute to either the vocal or the instrumental stem —
   the separation model quietly "loses" ~2.75 dB of that content. Suno's
   audio, being synthetic, has less of this un-attributable material, so
   the split is closer to perfectly additive.
2. **Elissa's "silent" gaps aren't silent — they carry real bleed.** In
   the quietest non-gated vocal-stem frames, Elissa sits at **−88.3 dB
   with low flatness (0.43)** — meaning there's a real, structured (not
   just noisy) low-level signal leaking into the vocal stem even when no
   one is singing. That's almost certainly instrumental bleed-through.
3. **Suno tracks split more cleanly, but not uniformly.** Ya Dar Maya
   (orig) and SONG_A are the cleanest (residual near −120 to −125 dB,
   flatness ~0.96 → essentially just noise floor, no meaningful bleed).
   SONG_B, C, and D sit in between (−101 to −111 dB, flatness ~0.66–0.68)
   — some tonal bleed, but still far cleaner than Elissa.
4. **This complicates, but doesn't overturn, the Session 2 consistency
   finding.** Ya Dar Maya (orig) — the track with the *worst* consistency
   score (13.55 dB std) — has one of the *cleanest* separations here. So
   the wild vocal-level swings measured in Session 2 are unlikely to be a
   separation artifact; they look like a genuine property of that mix.
   SONG_B and SONG_C's moderate consistency scores, however, now carry a
   caveat: some of their measured variance could be inflated by residual
   bleed rather than pure vocal-level change.

## Revised Confidence on Session 2 Findings

- **Ya Dar Maya (orig) high variance (13.55 dB): still trustworthy** —
  clean separation, so this is a real mix inconsistency, not noise.
- **SONG_B / SONG_C variance numbers: use with caution** — moderate
  residual bleed could be adding some spurious variance.
- **Elissa's own baseline (std 4.11 dB, +3.33 dB median prominence): use
  with caution too** — its separation carries the most bleed of all six
  tracks, so the "reference" itself isn't as clean as assumed.

## Files

- `scripts/separation_quality_audit.py`
- `scripts/plot_separation_quality.py`
- `separation_quality_results.json`
- `plots/separation_quality_audit.png`
