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

- **Separation Quality Audit [Session 3]:** No old official stems remain for a ground-truth check, so quality was audited via (a) reconstruction fidelity (`vocal+instrumental` vs. original mix) and (b) residual bleed in the quietest vocal-stem frames.
  - **Hard gate discovered:** 21%–31% of vocal-stem frames across ALL six tracks are literal digital-zero silence (not just quiet) — a uniform artifact of the separation/export step, not a Suno-vs-natural difference.
  - **Elissa-specific reconstruction gap:** Elissa's `vocal+instrumental` sum is **2.75 dB quieter** than the original mix (Suno tracks: ≈0 dB gap) — likely reverb/room ambience/mastering effects not cleanly attributable to either stem.
  - **Elissa has the most residual bleed of all six tracks:** quietest non-gated vocal frames sit at −88.3 dB with LOW spectral flatness (0.43 = tonal, structured bleed), vs. Suno tracks at −101 to −125 dB with flatness 0.66–0.96 (mostly noise-like, little bleed). **Ya Dar Maya (orig) and SONG_A have the cleanest separation of all six tracks.**
  - **Implication for Session 2 numbers:** Ya Dar Maya (orig)'s 13.55 dB consistency std is trustworthy (clean separation → real mix variance, not noise). SONG_B/SONG_C variance numbers carry a caution flag (moderate bleed could inflate them). Elissa's own reference numbers (+3.33 dB, 4.11 dB std) also carry a caution flag — it's the *noisiest* stem set, not the cleanest, despite being the "gold reference" track.
  - Full detail: `LABS/session_2026-07-29T054751/separation_quality_audit.md`

- **Reverb Tail Investigation [Session 4, prompted by owner's direct listening]:** Owner reported hearing an obvious, consistent reverb ("singing in a bathroom") on Elissa's isolated vocal, vs. inconsistent/minimal reverb on Suno vocals (as if a "deverb" step cuts it unevenly). This lines up with the flatness pattern from the separation audit (Elissa's residual bleed was the most tonal/structured of all six tracks).
  - **Automated decay-slope quantification was inconclusive.** Two attempts (peak-to-peak decay, then decay-into-hard-gate decay) gave noisy, sometimes contradictory results (e.g. Elissa was NOT the slowest-decaying by this metric) — sample sizes per track were small (11–34 usable events) with huge spread (IQR often spanning −10 to −130 dB/sec). **This method should not be trusted as-is; treat as an open question, not a finding.**
  - Elissa has far fewer true silence-gate entries (15) across the whole track than most Suno tracks (SONG_B: 44) — i.e., Elissa's phrasing is much more continuous/melismatic with fewer complete gaps, which could itself be contributing to the "wash"/reverb impression independent of actual decay time.
  - **Next concrete step (recommended, not yet done):** manual Audacity A/B listen at exact timestamps — solo the vocal stem only, listen right at/after these phrase endings: **Elissa @ 43.27s**, **Ya Dar Maya (orig) @ 19.95s**, **SONG_A @ 28.89s**, **SONG_C @ 11.61s**. These are real detected phrase-end/gate-entry points, not arbitrary. Spectrograms of these exact windows are saved at `LABS/session_2026-07-29T054751/plots/reverb_tail_spectrograms.png`.

---

## 4. Pedagogical Pause — Curriculum Track [Session 5]

- **Decision:** After Labs 1-4 (see Section 3 above), the project owner requested a deliberate pause from open research to build a beginner-friendly theory + practice curriculum, so he can properly understand the audio-engineering concepts (RMS/dB, stereo field, stems, spectral analysis, separation quality, reverb) that the prior labs' scripts already used but never explained from first principles.
- **Format:** 6 standalone Jupyter notebooks under `notebooks/`, one per session/phase (never all at once — see Execution Protocol below), each following the *actual dramatic arc of Labs 1-4* (naive proxy hypothesis → confirmed → broke under real stems → tool itself had to be audited → automated reverb metric failed → back to human listening) rather than a generic textbook order. Each notebook must ground every theoretical concept in the repo's real audio samples (Elissa reference track vs. Suno tracks/stems), include `matplotlib` visualizations, and end with a folded **Self-Check** Q&A section.
- **Approved Notebook Index (6 total):**
  1. `00_sound_loudness_vocabulary.ipynb` — Sound, Loudness & the Vocabulary Every Script Uses (waveform, sample rate, RMS, dB laws, instrument vs. human voice basics).
  2. `01_stereo_field_first_hypothesis.ipynb` — The Stereo Field & Our First (Flawed) Hypothesis (Mid/Side decomposition; rebuild the Lab 1 proxy and see how it became "confirmed" too fast).
  3. `02_real_stems_vs_proxy.ipynb` — Real Stems vs. Proxy: When the "Confirmed" Finding Broke (AI stems vs. proxy; mean gap vs. std-dev/consistency).
  4. `03_reading_a_spectrum.ipynb` — Reading a Spectrum: Where Sounds "Live" in Frequency (FFT/STFT, frequency bands, presence band check).
  5. `04_auditing_the_tool.ipynb` — Auditing the Tool Before Trusting the Numbers (separation quality audit, hard gate, residual bleed).
  6. `05_chasing_reverb.ipynb` — Chasing Reverb: When Automated Metrics Fail (reverb tail investigation, why decay-slope metrics failed, return to spectrograms/listening).
- **Execution Protocol (strict, to prevent token exhaustion / mid-notebook cutoffs):**
  1. One notebook per session/phase — never generate multiple notebooks in one pass.
  2. Each notebook must be executed locally (`jupyter nbconvert --execute`) and confirmed error-free before being handed off.
  3. After delivering a notebook + summary, STOP and wait for the project owner's explicit confirmation before starting the next one.
- **Status:** Notebook 00 (Sound & Loudness Vocabulary) complete. Notebook 01 (Stereo Field & First Hypothesis) complete — rebuilds the Lab 1 Mid/Side proxy from scratch (reproduces the exact original numbers: Elissa proxy median +10.73 dB, Suno tracks −2.10 to −3.06 dB gap vs Elissa), includes a calibration check against Elissa's real stems (proxy over-reports by +7.40 dB vs ground truth), and ends by flagging the untested "relative ranking survives" assumption that Notebook 02 goes on to break. Notebook 02 (Real Stems vs. Proxy) complete — measures vocal_dB − instrumental_dB directly on all six tracks' real stems (reproduces the exact Session 2 numbers: Elissa +3.33 dB/std 4.11, Ya Dar Maya +3.29 dB/std 13.55, SONG_A +2.62/std 5.13, SONG_B +3.36/std 8.11, SONG_C +2.40/std 6.61, SONG_D +2.17/std 4.79), shows the proxy's ~2-3 dB gap mostly evaporates under direct measurement, reframes the real gap as **consistency** (2-3x more fluctuation on Ya Dar Maya/SONG_B vs. Elissa) rather than average level, and explicitly parks the separation-quality/spectral confound for Notebooks 03-04 rather than chasing it early. Notebook 03 (Reading a Spectrum) complete this session — builds FFT/STFT/spectrogram vocabulary from scratch on real project audio, reproduces the presence-band check (Elissa 5.10% vs. Suno tracks 5.43–6.85% in the 2-5 kHz band, confirming the "missing presence" hypothesis was correctly ruled out), and closes by visualizing (not yet explaining) the Notebook 02 loose thread: Elissa's vocal stem carries ~11% of its energy in the 250-500 Hz Low-Mid band, visibly more than the Suno vocal stems — explicitly left as an open question for Notebook 04 to adjudicate (genuine mixing difference vs. separation-tool artifact). Notebooks 04-05 not yet started.
- **Build scripts:** `LABS/session_2026-07-29T172033/scripts/build_notebook_01.py`, `build_notebook_02.py`, `build_notebook_03.py` — all executed end-to-end with `jupyter nbconvert --execute` and confirmed error-free before handoff (build_notebook_01.py had two bugs fixed this session: an undefined `rms` variable in `rms_db()`, and three docstrings using `\"\"\"` inside `r"""`-wrapped code blocks that produced invalid Python syntax — both are common traps when generating notebook cells via raw strings, worth double-checking in future build scripts).
- **Next session starting point:** Build Notebook 04 (`04_auditing_the_tool.ipynb` — separation quality audit, hard gate, residual bleed), reusing the exact numbers/method already on record in Section 3 above (hard gate: 21-31% of vocal-stem frames are digital-zero silence across all six tracks; Elissa has the most residual bleed of all six despite being the "gold reference," with −88.3 dB flatness 0.43 vs. Suno's −101 to −125 dB flatness 0.66-0.96) and explicitly resolving the Low-Mid confound Notebook 03 just surfaced.

---

## 5. Active Research Questions & Next Session Ideas

1. ~~**Vocal Level Verification:** Verify if the ~3 dB vocal prominence gap holds true across all tracks.~~ **DONE** — Gap is smaller (~0–1.2 dB) than proxy suggested; the real issue is consistency.
2. ~~**Frequency Presence Analysis:** Check 2-5 kHz presence band.~~ **DONE** — Not a treble deficiency.
3. ~~**Separation Quality Audit:** Quantify how well the AI separation model works on Suno vs natural audio.~~ **DONE [Session 3]** — Suno tracks separate more cleanly than Elissa overall; Ya Dar Maya (orig) & SONG_A are cleanest, SONG_B/C have moderate bleed, Elissa has the most bleed of all six. See finding above.
4. **Consistency Analysis (High Priority):** Why do Suno tracks (especially Ya Dar Maya orig and SONG_B) show 2–3× higher variance in vocal-instrumental balance? Is it actual mix fluctuation or separation artifacts? — **Now partially answered:** Ya Dar Maya orig's high variance is confirmed real (clean separation). SONG_B still needs the bleed-adjusted re-check before trusting its exact number.
5. **Spectral Masking Map:** For each track, compute the spectral overlap between vocal and instrumental stems at 1-second resolution. Where does the instrumental bed "step on" the vocal's frequency territory?
6. **Stereo Width During Vocal Passages:** Compare instrumental stem stereo width between Elissa and Suno during sections where the vocal is active. Does Suno's backing get wider/ washier when the vocal should be centered?
7. **Intervention Test — Vocal Boost:** Boost the vocal stem of SONG_D (the closest to Elissa in level) by ~1 dB and compare A/B. Does it close the perceived quality gap?
8. **Intervention Test — Dynamic Compression:** Apply gentle compression to the vocal stem of Ya Dar Maya orig to reduce the 13.55 dB variance to match Elissa's 4.11 dB. Does consistency alone fix the perception?
9. **Instrumental Stem Isolation Quality:** Compare the instrumental stems across tracks — does Suno's instrumental have more energy in vocal-range frequencies (200-500 Hz, 2-5 kHz) that would mask the vocal even at equal levels?
10. **Audacity Manual Listen:** For each track, solo the vocal stem and listen. Does the Suno vocal stem sound clean, or is there audible bleed/artifacts from the separation?

---

## 6. Session Log

- **[This session]** Curriculum work: fixed 2 real bugs in `build_notebook_01.py` (found via actually executing the notebook, not just building it — the build step alone doesn't catch runtime/syntax errors inside generated cells), delivered a `.git`-and-audio-free zip export of the repo on request, then built and verified Notebooks 02 and 03 in sequence per the Execution Protocol. All three notebooks in `notebooks/` are confirmed to execute cleanly end-to-end as of this session.

