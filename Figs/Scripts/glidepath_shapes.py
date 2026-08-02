"""
glidepath_shapes.py
-------------------
Generates a figure illustrating the five canonical glidepath shapes discussed
in the lifecycle allocation literature (DE, RE, U-shaped, Inverted-U, Static).

Accumulation (age 25-65) and decumulation (age 65-95) phases are shown as
shaded background regions.  Equity allocation lines are coloured using the
inferno colormap.  Output is saved as ../glidepath-shapes.png.
"""

import os
import numpy as np
import matplotlib.pyplot as plt

script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, "..", "glidepath_shapes.png")
age_start = 25
age_retire = 65
age_end = 95
N = 300  # total points across full range
N_half = 150  # points per phase

ages_all = np.linspace(age_start, age_end, N)
ages_acc = np.linspace(age_start, age_retire, N_half)
ages_dec = np.linspace(age_retire, age_end, N_half)

# Concatenated age axis for compound shapes (no duplicate at 65)
ages_compound = np.concatenate([ages_acc, ages_dec[1:]])

# 1. Declining equity (DE) — conventional TDF / industry default
de = np.linspace(0.90, 0.10, N)

# 2. Rising equity (RE) — contrarian mirror (Estrada accumulation logic /
#    Pfau & Kitces retirement logic applied throughout)
re = np.linspace(0.10, 0.90, N)

# 3. U-shaped (Pfau & Kitces 2014):
#    DE during accumulation → RE during decumulation
u_eq = np.concatenate(
    [np.linspace(0.90, 0.20, N_half), np.linspace(0.20, 0.80, N_half)[1:]]
)

# 4. Inverted-U (Estrada 2014 / 2015):
#    RE during accumulation → DE during decumulation
invu_eq = np.concatenate(
    [np.linspace(0.30, 0.90, N_half), np.linspace(0.90, 0.20, N_half)[1:]]
)

static = np.full(N, 0.60)

# Distinct, colorblind-friendly line palette with strong separation.
c_de = "#0072B2"  # blue
c_re = "#D55E00"  # vermillion
c_u = "#009E73"  # bluish green
c_invu = "#CC79A7"  # reddish purple
c_static = "#F0E442"  # yellow

fig, ax = plt.subplots(figsize=(8.5, 4.8))

# Phase shading
ax.axvspan(age_start, age_retire, alpha=0.07, color="steelblue", zorder=0)
ax.axvspan(age_retire, age_end, alpha=0.07, color="tomato", zorder=0)

# Vertical line at retirement
ax.axvline(age_retire, color="dimgrey", linewidth=1.0, linestyle="--", zorder=1)

# Glidepath lines
lw = 2.3
ax.plot(ages_all, de * 100, color=c_de, linewidth=lw, label="Declining equity (DE)")
ax.plot(ages_all, re * 100, color=c_re, linewidth=lw, label="Rising equity (RE)")
ax.plot(
    ages_compound, u_eq * 100, color=c_u, linewidth=lw, label="U-shaped (Pfau & Kitces)"
)
ax.plot(
    ages_compound,
    invu_eq * 100,
    color=c_invu,
    linewidth=lw,
    label="Inverted-U (Estrada)",
)
ax.plot(
    ages_all,
    static * 100,
    color=c_static,
    linewidth=lw,
    linestyle=(0, (5, 2)),
    label="Static 60/40",
)

# Phase region labels
ax.text(
    45,
    96,
    "Accumulation",
    ha="center",
    va="top",
    fontsize=9.5,
    color="steelblue",
    fontstyle="italic",
    alpha=0.85,
)
ax.text(
    80,
    96,
    "Decumulation",
    ha="center",
    va="top",
    fontsize=9.5,
    color="tomato",
    fontstyle="italic",
    alpha=0.85,
)

# Age 65 annotation — placed just right of the dashed line, near the bottom
ax.text(
    65.8,
    4,
    "Age 65\n(retirement)",
    ha="left",
    va="bottom",
    fontsize=8.0,
    color="dimgrey",
    linespacing=1.4,
)

ax.set_xlabel("Age", fontsize=11)
ax.set_ylabel("Equity allocation (%)", fontsize=11)
ax.set_xlim(age_start, age_end)
ax.set_ylim(0, 100)
ax.set_yticks(range(0, 101, 20))
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x)}%"))
ax.tick_params(labelsize=9)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.legend(
    fontsize=8.5,
    loc="lower right",
    framealpha=0.92,
    edgecolor="lightgrey",
    handlelength=2.2,
)

plt.tight_layout()
plt.savefig(output_path, dpi=200, bbox_inches="tight")
print(f"Saved: {os.path.normpath(output_path)}")
plt.show()
