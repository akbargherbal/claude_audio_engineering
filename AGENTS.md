# AGENTS.md — Workspace, Protocols & Operational Guidelines

This document defines the operational rules, environment capabilities, interaction protocols, and workflow guidelines for AI Assistants working on this project. Read this file at the start of every session alongside `context.md`.

---

## 1. Interaction Protocol with Project Owner

- **No Open-Ended/Expert Questions:** Do NOT ask the project owner open-ended or expert-preference questions (e.g., "What should we look at first?").
- **Concrete & Direct Guidance:** Ask **specific, concrete questions** instead — point him to an exact timestamp or file and ask a specific yes/no or short-answer question in plain language (no jargon required).
- **Bridge Data to Perception:** Connect his descriptions to the numerical data. The numbers serve the user's description and listening experience, not the other way around.
- **Ask, Don't Guess, When a Human Can Just Look/Listen:** If a piece of information can be obtained trivially by the project owner looking at or listening to something (e.g., reading an exact timestamp off a tool he already has open, confirming a file wasn't trimmed), **ask him directly for it** rather than writing speculative code to infer/reconstruct it. Guessing wastes time and produces unreliable results for things a human can just report directly. Reserve code/analysis for things that genuinely require computation, not for substituting a look or a listen.

---

## 2. Division of Labor & Tooling Strategy

The AI Assistant is responsible for proactively recommending the best execution path among three primary tools:

1. **AI Assistant's Sandbox:**
   - Use freely for standard audio analysis, feature extraction, script execution, plotting, and file maintenance (`librosa`, `numpy`, `scipy`, `soundfile`, `ffmpeg`).
2. **Off-Sandbox Heavy Compute (Project Owner Execution):**
   - The sandbox lacks a GPU and has modest RAM.
   - For heavy compute tasks (e.g., large ML models, deep learning stem separation networks, heavy batch processing), **do not run them in the sandbox**.
   - Provide ready-to-run scripts or Google Colab / GCP VM code for the project owner to execute locally or in the cloud.
3. **Audacity (Manual Desktop Tasks):**
   - The project owner uses Audacity for desktop manual audio tasks (e.g., stem splitting, band isolation, plugin application).
   - Recommend Audacity actions when they are faster/easier than coding. Provide step-by-step, plain-language instructions for any suggested Audacity workflows.

---

## 3. GitHub & Sandbox Sync Workflow

The AI Assistant does not have direct push access to GitHub. Follow this sync protocol periodically whenever meaningful progress accumulates:

1. **Work in Sandbox:** Perform analysis, write scripts, and update documentation/memory files within the local sandbox environment.
2. **Build Sync Zip:** Proactively generate a `.zip` archive containing updated code, docs, `context.md`, `AGENTS.md`, and small data files (`.srt`, `.json`, `.csv`).
   - **EXCLUDE:** Audio files (`*.mp3`, `*.wav`), virtual environments (`venv/`), `__pycache__`, `.pyc`, `.DS_Store`, and `.git/`.
3. **Handover:** Provide the zip link to the project owner.
4. **Owner Push & Sync Confirmation:** The project owner extracts the zip over his local repository, commits, and pushes to GitHub. Once notified, the AI Assistant runs `git fetch` / `git pull` in the sandbox and verifies sync (e.g., checking commit hashes).

---

## 4. Session & Workspace Directory Structure

- Every session executes within a dedicated working directory: `LABS/session_<YYYY-MM-DDTHHMMSS>/`.
- **Ephemeral Work:** All experimental scripts, interim outputs, and rough notes live inside `LABS/`. Nothing inside `LABS/` is treated as permanent project memory.
- **Memory Promotion:** Important findings, validated scripts, decisions, and structural updates must be promoted to `context.md` or `AGENTS.md` before concluding work.

---

## 5. Environment & Scripting Assets

- **Pre-installed Python Packages:** `librosa`, `soundfile`, `numpy`, `scipy`, `ffmpeg`.
- **Core Generation Script:** `scripts/maqam_prompt_generator_v3_entrance_fix.py`.
- **Data Directory:** `data/` containing tracks and `.srt` subtitle timing files.