# context.md — Persistent Project Memory & Knowledge Base

This file stores the project's cumulative audio engineering findings, reference track data, track lineage, and active research hypotheses. **Read this file at the start of every session to load current project state.**

---

## 1. Project Reference Data

- **Gold Reference Track:** Elissa — "Maktouba Leek" (`data/elisa_maktooba_leek.mp3`).
  - **AI-Separated Stems:** `data/elisa_maktooba_leek/` — `-Vocals.mp3` and `-Instrumental.mp3`.
  - Official stems (`data/elisa_stems/`) have been replaced by AI-separated stems.
- **Primary Suno Test Track:** "Ya Dar Maya" (`data/يا دار مية - 28-07-2026.mp3`).
- **AI-Separated Stems Available for ALL tracks** — each track now has its own subdirectory with `-Vocals.mp3` and `-Instrumental.mp3` stems. This enables direct vocal prominence measurement without proxy methods.

---

## 2. Critical Audio Data Caveats

- **`.srt` Timestamp Offset:** `.srt` files have a known ~3-4 second timing offset. **Never trust `.srt` timestamps for sub-second audio analysis.** Always verify onset timing by ear or waveform analysis first.
- **Track Lineage (Cover Confound):** `data/يا دار مية - 28-07-2026.mp3` is the original base take. Tracks `SONG_A`, `SONG_B`, `SONG_C`, and `SONG_D` are **covers** generated from this base take with low audio influence (~25%). They are NOT independent fresh prompt generations.

---

## 3. Key Findings to Date

- **Debunked Hypothesis — "Swell Clash" (Lab 04):**
  - _Earlier belief:_ Backing orchestral swells clashing with vocal entrances cause poor quality.
  - _Finding:_ Testing against the Elissa reference track showed low-mid energy and stereo width actually _increase_ at vocal entrance. What happens in professional mixes is compositional "call-and-response," not a frequency crash.

- **REFINED Hypothesis — "Vocal Consistency & Spectral Masking" [Session 2 Update]:**
  - _Earlier mid/side proxy was misleading._ The proxy showed a ~3 dB gap because it captured centered instruments, not just vocals. Direct stem analysis reveals a different picture.
  - _Direct Stem Measurement (AI-separated vocal & instrumental):_
    - Elissa:  **+3.33 dB** median (validates AI separation vs old official stems' +2.60 dB)
    - Ya Dar Maya: **+3.29 dB** (gap: −0.04 dB — essentially identical)
    - SONG_A: **+2.62 dB** (gap: −0.71 dB)
    - SONG_B: **+3.36 dB** (gap: +0.03 dB)
    - SONG_C: **+2.40 dB** (gap: −0.93 dB)
    - SONG_D: **+2.17 dB** (gap: −1.16 dB)
  - **Key Finding — Not a level gap, but a CONSISTENCY problem:**
    - Elissa vocal std: **4.11 dB** (tight, controlled)
    - Ya Dar Maya std: **13.55 dB** (3× more fluctuation!)
    - SONG_B std: **8.11 dB** (2× more fluctuation)
  - _2-5 kHz Presence Band:_ Suno tracks have EQUAL or HIGHER energy (5.4%–6.9%) vs Elissa (5.1%). Not a treble issue.
  - _Spectral Profile:_ Elissa's vocal concentrates energy in low-mid (250-500 Hz) at ~11%, while Suno vocal stems show much less energy across the board — possibly indicating poorer separation quality for synthetic audio.
  - _Revised Conclusion:_ The perceived quality gap is NOT primarily a simple level balance problem. It appears to be a combination of: (a) **inconsistent vocal-instrumental balance** across the track, (b) potentially **poorer separation quality** for Suno's synthetic audio (the AI model may struggle to cleanly extract vocals from Suno's unique timbre), and (c) possible **spectral masking** where the instrumental bed occupies the same critical bands as the vocals.

---

## 4. Active Research Questions & Next Session Ideas

1. ~~**Vocal Level Verification:** Verify if the ~3 dB vocal prominence gap holds true across all tracks.~~ **DONE** — Gap is smaller (~0–1.2 dB) than proxy suggested; the real issue is consistency.
2. ~~**Frequency Presence Analysis:** Check 2-5 kHz presence band.~~ **DONE** — Not a treble deficiency.
3. **Separation Quality Audit:** Quantify how well the AI separation model works on Suno vs natural audio. Compare residual bleed, separation confidence. If separation is poor on Suno tracks, the stem-based measurements may be unreliable.
4. **Consistency Analysis (High Priority):** Why do Suno tracks (especially Ya Dar Maya orig and SONG_B) show 2–3× higher variance in vocal-instrumental balance? Is it actual mix fluctuation or separation artifacts?
5. **Spectral Masking Map:** For each track, compute the spectral overlap between vocal and instrumental stems at 1-second resolution. Where does the instrumental bed "step on" the vocal's frequency territory?
6. **Stereo Width During Vocal Passages:** Compare instrumental stem stereo width between Elissa and Suno during sections where the vocal is active. Does Suno's backing get wider/ washier when the vocal should be centered?
7. **Intervention Test — Vocal Boost:** Boost the vocal stem of SONG_D (the closest to Elissa in level) by ~1 dB and compare A/B. Does it close the perceived quality gap?
8. **Intervention Test — Dynamic Compression:** Apply gentle compression to the vocal stem of Ya Dar Maya orig to reduce the 13.55 dB variance to match Elissa's 4.11 dB. Does consistency alone fix the perception?
9. **Instrumental Stem Isolation Quality:** Compare the instrumental stems across tracks — does Suno's instrumental have more energy in vocal-range frequencies (200-500 Hz, 2-5 kHz) that would mask the vocal even at equal levels?
10. **Audacity Manual Listen:** For each track, solo the vocal stem and listen. Does the Suno vocal stem sound clean, or is there audible bleed/artifacts from the separation?
