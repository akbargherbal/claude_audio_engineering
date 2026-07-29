import json
import os
import matplotlib.pyplot as plt

here = os.path.dirname(__file__)
with open(os.path.join(here, "..", "separation_quality_results.json"), encoding="utf-8") as f:
    results = json.load(f)

names = [r["track"] for r in results]
recon_err = [r["reconstruction_err_db_median"] for r in results]
silent_frac = [r["vocal_stem_hard_silent_frame_fraction"] * 100 for r in results]
quiet_rms = [r["quiet_nonzero_frame_rms_median_db"] for r in results]
flatness = [r["quiet_nonzero_frame_spectral_flatness_median"] for r in results]

fig, axes = plt.subplots(2, 2, figsize=(13, 9))

colors = ["#c0392b" if n.startswith("Elissa") else "#2980b9" for n in names]

ax = axes[0, 0]
ax.bar(names, recon_err, color=colors)
ax.set_title("Reconstruction error (vocal+instrumental vs original mix)")
ax.set_ylabel("dB (0 = perfect reconstruction)")
ax.tick_params(axis="x", rotation=30)
ax.axhline(0, color="black", linewidth=0.8)

ax = axes[0, 1]
ax.bar(names, silent_frac, color=colors)
ax.set_title("Fraction of vocal-stem frames that are hard-gated silence")
ax.set_ylabel("% of 1s frames")
ax.tick_params(axis="x", rotation=30)

ax = axes[1, 0]
ax.bar(names, quiet_rms, color=colors)
ax.set_title("Residual level in quietest NON-gated vocal-stem frames")
ax.set_ylabel("dB (lower = cleaner)")
ax.tick_params(axis="x", rotation=30)

ax = axes[1, 1]
ax.bar(names, flatness, color=colors)
ax.set_title("Spectral flatness of that residual (1.0 = pure noise, low = tonal bleed)")
ax.set_ylabel("flatness (0-1)")
ax.tick_params(axis="x", rotation=30)
ax.set_ylim(0, 1.05)

plt.tight_layout()
out_path = os.path.join(here, "..", "plots", "separation_quality_audit.png")
plt.savefig(out_path, dpi=130)
print(f"Saved plot to {out_path}")
