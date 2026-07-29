# Lab Session 2 — The Midas Touch, Corrected

## Premise

We previously hypothesized that the quality gap between Elissa and Suno tracks was a **~3 dB vocal level deficit** (based on a mid/side proxy measurement). The user then separated ALL tracks into vocal and instrumental stems using an advanced AI model. This gives us direct ground-truth measurements — no more proxy needed.

## What Changed?

Every track now has a subdirectory in `data/` with:
- `{track}-Vocals.mp3`
- `{track}-Instrumental.mp3`

This enables the first-ever **direct vocal prominence comparison** across all six tracks on equal footing.

---

## Results

### 1. Vocal Prominence (direct stems)

| Track | Median (voc_dB − inst_dB) | Gap vs Elissa |
|---|---|---|
| Elissa | **+3.33 dB** | — |
| Ya Dar Maya (orig) | +3.29 dB | −0.04 dB |
| SONG_A | +2.62 dB | −0.71 dB |
| SONG_B | +3.36 dB | +0.03 dB |
| SONG_C | +2.40 dB | −0.93 dB |
| SONG_D | +2.17 dB | −1.16 dB |

**The ~3 dB gap has largely evaporated.** Median vocal levels are strikingly similar across all tracks. The mid/side proxy was misleading — it was picking up centered instruments, not just vocals.

### 2. Consistency (Standard Deviation)

| Track | Std Dev | IQR | Interpretation |
|---|---|---|---|
| Elissa | **4.11 dB** | 4.27 dB | Tight, professional |
| Ya Dar Maya (orig) | **13.55 dB** | 7.95 dB | **3× wilder** — highly erratic |
| SONG_A | 5.13 dB | 4.74 dB | Comparable to Elissa |
| SONG_B | **8.11 dB** | 5.17 dB | **2× wilder** |
| SONG_C | 6.61 dB | 4.01 dB | Moderately elevated |
| SONG_D | 4.79 dB | 4.14 dB | Comparable to Elissa |

**This is the real finding.** The average vocal level isn't the problem — the **consistency** of that level over time is. The original Ya Dar Maya track varies 3× more than Elissa. Some sections the vocal is buried, others it jumps out.

### 3. Spectral Overview

Elissa's vocal concentrates ~11% of its energy in the 250-500 Hz "body" range. Suno vocal stems show much lower energy concentrations across all bands — likely because the AI separation model was trained primarily on natural audio and is less effective at extracting clean vocals from Suno's synthetic timbre. This means **stem quality varies by source**, and comparisons between tracks should account for this confound.

---

## Revised Hypothesis

**OLD:** "The vocal is ~3 dB too quiet across all Suno tracks."
**NEW:** "The vocal level is roughly correct on average, but its **inconsistency** (wild fluctuations) and potential **spectral masking** by the instrumental bed degrade perceived quality. Additionally, the AI separation model may not extract Suno vocals as cleanly as natural vocals, introducing a measurement confound."

---

## Files

| File | Description |
|---|---|
| `scripts/stem_analysis.py` | Full analysis script |
| `plots/vocal_prominence_boxplot.png` | Box plot from proxy analysis |
| `plots/separation_validation.png` | Waveform comparison (if available) |
| `plots/spectral_profiles.png` | Vocal vs instrumental spectrum, all tracks |

---

## What's Next? (10 Directions)

**Priority 1 — Validate the stem quality itself:**
1. **Separation Quality Audit:** Compare the AI-separated Elissa stems to the old official stems (if still available). Compute correlation, bleed, residual noise.
2. **Manual Listen:** Open the vocal stems in Audacity for each track. Does the Suno vocal sound clean or artifact-ridden?

**Priority 2 — Understand the consistency gap:**
3. **Dynamic Range Analysis:** Where exactly do the vocal dips occur in Ya Dar Maya orig? Are they at specific structural points (verse vs chorus)?
4. **Compression Intervention:** Apply gentle compression to normalize Ya Dar Maya's vocal to Elissa's 4.11 dB std. Does it sound significantly better?

**Priority 3 — Spectral & spatial masking:**
5. **Masking Map:** Compute spectral overlap between vocal and instrumental stems per second. Where does the instrumental bed occupy the same bands as the vocal?
6. **Stereo Width During Vocals:** Is the instrumental bed wider/washier during vocal passages in Suno tracks vs Elissa?
7. **EQ Intervention:** Cut 250-500 Hz from Ya Dar Maya's instrumental by 2-3 dB. Does the vocal emerge more clearly?

**Priority 4 — The ultimate test:**
8. **Hybrid Remix:** Take SONG_D's stems, normalize vocal consistency, apply gentle spectral cleaning, and A/B against the original.
9. **Prompt Engineering (if applicable):** Feed the above findings back into Suno prompting — e.g., "consistent vocal level, dry centered vocal, minimal reverb during verses."
10. **Reference-Track Analysis:** Beyond level, what other mix characteristics differentiate Elissa from Suno? Compression curves? Reverb tails? Transient sharpness?
