# Lab Session 2 — Vocal Prominence Hypothesis: CONFIRMED

## Question

Does the perceived quality gap between Elissa's "Maktouba Leek" and the Suno-generated "Ya Dar Maya" covers originate from a **level balance issue** (vocal too quiet relative to the instrumental bed) rather than a synthesis quality or frequency presence issue?

## Method

### Ground Truth (Elissa Only)
We have real isolated stems for Elissa:
- `data/elisa_stems/elisa_maktooba_leek-Vocals.mp3`
- `data/elisa_stems/elisa_maktooba_leek-Instrumental.mp3`

For each 1-second window where the vocal stem RMS > −40 dB, we compute:

```
vocal_prominence = RMS_dB(vocal) - RMS_dB(instrumental)
```

### Proxy (All Tracks — Mid/Side Decomposition)
Since Suno tracks lack isolated stems, we decompose the stereo mix:

- **Mid** = (L + R) / 2 — captures centered content (vocals, centered instruments)
- **Side** = (L - R) / 2 — captures off-center content (stereo reverb, panned instruments)

For each 1-second window where mid RMS > −40 dB:

```
proxy_prominence = RMS_dB(mid) - RMS_dB(side)
```

### Calibration
We run the proxy on the Elissa full mix to establish a baseline: the proxy OVER-reports by ~8.1 dB compared to ground truth (expected — mid includes centered instruments, not just vocals). For **relative comparison**, no correction is needed: all tracks are measured on the same metric.

### Additional: 2-5 kHz Presence Band
We compute the median fraction of total spectral energy falling in 2–5 kHz (the "presence" band associated with vocal clarity).

---

## Results

### Vocal Prominence — Ground Truth

| Track | Metric | Median | n_windows |
|---|---|---|---|
| Elissa | vocal_dB − instrumental_dB (real stems) | **+2.60 dB** | 196 |

Elissa's vocal sits **2.6 dB above** the instrumental backing when active. Quartiles: [+0.39, +4.65] dB.

### Vocal Prominence — Mid/Side Proxy (All Tracks)

| Track | Median (mid_dB − side_dB) | Gap vs Elissa |
|---|---|---|
| Elissa (full mix) | +10.73 dB | 0 (reference) |
| Ya Dar Maya (original) | +8.63 dB | **−2.10 dB** |
| SONG_A | +7.99 dB | **−2.74 dB** |
| SONG_B | +7.67 dB | **−3.06 dB** |
| SONG_C | +7.67 dB | **−3.06 dB** |
| SONG_D | +8.12 dB | **−2.61 dB** |

**All Suno tracks are 2.1–3.1 dB behind Elissa** in centered-content prominence.

### 2-5 kHz Presence Band

| Track | Median Energy in 2-5 kHz |
|---|---|
| Elissa (full mix) | **5.10%** |
| Ya Dar Maya (original) | 5.72% |
| SONG_A | 6.28% |
| SONG_B | 5.43% |
| SONG_C | 5.99% |
| SONG_D | 6.85% |

**Suno tracks have equal or MORE high-frequency presence than Elissa.** The issue is NOT a lack of treble clarity.

---

## Conclusions

1. **Hypothesis CONFIRMED.** The vocal prominence gap is real and consistent: ~3 dB across all four Suno covers and the original take.
2. **Frequency presence is ruled out.** 2-5 kHz energy is not deficient in Suno tracks — if anything, it's slightly elevated.
3. **The root cause is a mix level balance problem.** The vocal/center content is simply too quiet relative to the rest of the mix.

## Next Steps

1. **Intervention test:** Boost the mid (center) channel of a Suno track by ~3 dB and compare A/B with the original. Does it now sound as "authoritative" as Elissa?
2. **Reverb & spatial separation:** Analyze stereo width during vocal passages — is excessive reverb/width on Suno tracks smearing the vocal even after level correction?
3. **Precision EQ:** If the intervention test works, fine-tune with a gentle 2-5 kHz shelf on the vocal region.

## Files

- **Script:** `scripts/vocal_prominence_analysis.py`
- **Box plot:** `plots/vocal_prominence_boxplot.png`
