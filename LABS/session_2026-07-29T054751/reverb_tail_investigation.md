# Lab Session 4 — Reverb Tail Investigation (owner-prompted)

## Trigger

Project owner, listening to isolated vocal stems directly: Elissa's vocal
sounds like it was sung with a strong, consistent room reverb ("like
singing in a bathroom"). Suno vocal stems, by contrast, vary between
almost no reverb and limited reverb, as if some inconsistent "deverb"
process is cutting the tail.

This lines up with Session 3's finding that Elissa's residual bleed in
quiet vocal-stem frames was the most tonal/structured (flatness 0.43) of
all six tracks — consistent with a real reverb tail leaking into "silent"
gaps, vs. Suno's mostly noise-like residual (flatness 0.66–0.96).

## Attempt 1 — Decay slope after every local RMS peak

Measured dB/sec decay in the 300ms after every local peak in the vocal
stem's RMS envelope. **Result contradicted the listening impression**:
Elissa showed the *fastest* median decay (−17 dB/sec, T60≈3.5s) while
SONG_C showed the *slowest* (−10.2 dB/sec, T60≈5.9s).

**Diagnosis:** this method picks up ordinary vocal-performance dynamics
(vibrato ripple, note-to-note transitions within a sustained melismatic
line) as "peaks," not just true phrase endings. Elissa's dense
ornamentation likely contaminated the measurement with fast micro-dips
that have nothing to do with room reverb.

## Attempt 2 — Decay slope only right before entering true silence (the hard gate)

Restricted to the ~300ms immediately preceding a transition into the
hard-gated silence found in Session 3 — i.e., genuine phrase endings, not
mid-phrase dips.

| Track | Gate entries (whole track) | Decays used | Median slope (dB/s) | Est. T60 (s) |
|---|---|---|---|---|
| Elissa (ref) | 15 | 12 | −56.6 | 1.06 |
| Ya Dar Maya (orig) | 25 | 21 | −72.2 | 0.83 |
| SONG_A | 14 | 11 | −57.5 | 1.04 |
| SONG_B | 44 | 34 | −51.2 | 1.17 |
| SONG_C | 20 | 17 | −47.2 | 1.27 |
| SONG_D | 26 | 16 | −24.8 | 2.42 |

**Still inconclusive / still doesn't match the listening impression** —
sample sizes are small (11–34 events) and the spread within each track is
huge (IQR often −10 to −130 dB/sec), so the medians aren't reliable.
**This metric should be treated as an open question, not a validated
finding.**

## One structural observation that IS solid

Elissa has far fewer complete silence-gate entries (15) across the whole
5+ minute track than most Suno tracks (SONG_B: 44 in a shorter track).
Her phrasing is much more continuous/melismatic, with fewer true gaps.
This alone could contribute to a "washy"/reverberant impression —
independent of the actual per-note decay time — simply because notes
overlap into each other more.

## What we did instead: exact-timestamp spectrograms for manual review

Rather than force an unreliable automated number, we pulled spectrograms
of 3-second windows centered on real, detected phrase-ending moments:

| Track | Phrase-end timestamp |
|---|---|
| Elissa (ref) | 43.27s |
| Ya Dar Maya (orig) | 19.95s |
| SONG_A | 28.89s |
| SONG_C | 11.61s |

See `plots/reverb_tail_spectrograms.png` (cyan line = the exact gate-entry
moment).

## Recommended Next Step (concrete, per AGENTS.md protocol)

**Manual Audacity check** — solo the vocal stem only, jump to each
timestamp above, and listen to ~1 second after the marked point:

1. Elissa @ **43.27s**
2. Ya Dar Maya (orig) @ **19.95s**
3. SONG_A @ **28.89s**
4. SONG_C @ **11.61s**

Question to answer by ear: at these exact points, does Elissa's tail
audibly ring longer/wetter than the other three, or does it sound similar
once you're listening to a real phrase-ending rather than the track as a
whole? This will tell us whether the "wash" is a true per-note reverb
tail or a phrasing-density effect (per the structural observation above).

## Files

- `scripts/reverb_decay_analysis.py`
- `scripts/plot_reverb_tail_spectrograms.py`
- `reverb_decay_results.json`
- `plots/reverb_tail_spectrograms.png`
