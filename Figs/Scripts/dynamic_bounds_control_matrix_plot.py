"""
Heatmap visualisation of ControlMatrixDynamicBoundsPolicy.

Two-panel figure:
  a) Discrete control-matrix nodes with time-varying wealth bounds shown
     as a scatter plot.
  b) Interpolated risky-asset allocation heatmap in (time, wealth) space,
     with the dynamic bound envelope overlaid.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import numpy as np
import torch
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import BoundaryNorm
from Code.utils.allocation import ControlMatrixDynamicBoundsPolicy

# ---------------------------------------------------------------------------
# Policy configuration
# ---------------------------------------------------------------------------

# Time nodes (e.g. years 0..4 in a 5-step investment horizon)
time_nodes = torch.tensor([0.0, 1.0, 2.0, 3.0, 4.0])

# Dynamic wealth bounds: bounds shift over time.
# Each row is [w_low, w_mid_low, w_mid_high, w_high] at the corresponding time node.
# Here the grid drifts upward during accumulation then contracts during drawdown.
wealth_nodes = torch.tensor(
    [
        [0.50, 1.00, 1.50, 2.00],   # t=0
        [0.60, 1.20, 1.80, 2.40],   # t=1  (growing)
        [0.70, 1.40, 2.10, 2.80],   # t=2  (peak)
        [0.60, 1.20, 1.80, 2.40],   # t=3  (declining)
        [0.40, 0.80, 1.20, 1.60],   # t=4  (contracted)
    ]
)

# Policy settings: risky-asset allocation (%) at each (time, wealth) node.
# Higher wealth → lower equity tilt (liability-matching intuition).
# Earlier time → higher equity tilt.
policy_pct = torch.tensor(
    [
        [85.0, 75.0, 60.0, 45.0],   # t=0
        [80.0, 68.0, 52.0, 38.0],   # t=1
        [72.0, 60.0, 44.0, 30.0],   # t=2
        [60.0, 48.0, 34.0, 20.0],   # t=3
        [45.0, 32.0, 20.0, 10.0],   # t=4
    ]
)
policy_settings = (policy_pct / 100.0).unsqueeze(-1)  # (5, 4, 1)

n_sims = 1  # dummy — only need the policy shape
policy = ControlMatrixDynamicBoundsPolicy(
    n_assets=2,
    n_sims=n_sims,
    time_nodes=time_nodes,
    wealth_nodes=wealth_nodes,
)

# ---------------------------------------------------------------------------
# Evaluate on a fine (time × wealth) grid
# ---------------------------------------------------------------------------

time_fine = np.linspace(float(time_nodes[0]) + 1e-6, float(time_nodes[-1]) - 1e-6, 300)
wealth_fine = np.linspace(
    float(wealth_nodes.min()) - 0.1,
    float(wealth_nodes.max()) + 0.1,
    300,
)

# Build heatmap: allocation[i_time, i_wealth] = risky fraction
allocation_grid = np.full((len(time_fine), len(wealth_fine)), np.nan)

for i, t in enumerate(time_fine):
    w_tensor = torch.tensor(wealth_fine, dtype=torch.float32)
    alloc = policy.get_allocation(
        t=t,
        wealth=w_tensor,
        policy_settings=policy_settings,
    )
    allocation_grid[i, :] = alloc[:, 1].detach().numpy() * 100.0  # risky %

# ---------------------------------------------------------------------------
# Build bound envelope for overlay
# ---------------------------------------------------------------------------

t_np = time_nodes.numpy()
wn_np = wealth_nodes.numpy()

# Interpolate min/max wealth bounds along fine time axis
bound_lo = np.interp(time_fine, t_np, wn_np[:, 0])
bound_hi = np.interp(time_fine, t_np, wn_np[:, -1])

# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5), constrained_layout=True)

vmin, vmax = 0, 100
cmap = "inferno"

# ---- Left panel: discrete nodes ----------------------------------------

for ti, (t_val, wn_row, ps_row) in enumerate(
    zip(t_np, wn_np, policy_pct.numpy())
):
    sc = ax1.scatter(
        np.full(len(wn_row), t_val),
        wn_row,
        c=ps_row,
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        s=140,
        zorder=3,
        edgecolors="white",
        linewidths=0.6,
    )
    # Annotate with value
    for w_val, pct in zip(wn_row, ps_row):
        ax1.text(
            t_val, w_val, f"{int(pct)}%",
            ha="center", va="center",
            color="white", fontsize=7, fontweight="bold",
        )

# Connect bound envelopes between nodes
ax1.plot(t_np, wn_np[:, 0], color="steelblue", lw=1.4, ls="--", label="Wealth bounds")
ax1.plot(t_np, wn_np[:, -1], color="steelblue", lw=1.4, ls="--")
ax1.fill_between(t_np, wn_np[:, 0], wn_np[:, -1], alpha=0.08, color="steelblue")

# Faint lines for intermediate wealth nodes
for col in range(1, wn_np.shape[1] - 1):
    ax1.plot(t_np, wn_np[:, col], color="grey", lw=0.7, ls=":", alpha=0.6)

ax1.set_title("a). Control Matrix (Discrete)", loc="left")
ax1.set_xlabel("Time")
ax1.set_ylabel("Wealth")
ax1.set_xticks(t_np)
ax1.legend(fontsize=8)

# ---- Right panel: interpolated heatmap ---------------------------------

im = ax2.imshow(
    allocation_grid.T,
    origin="lower",
    cmap=cmap,
    vmin=vmin,
    vmax=vmax,
    aspect="auto",
    extent=[time_fine[0], time_fine[-1], wealth_fine[0], wealth_fine[-1]],
)

# Dynamic bound envelope
ax2.plot(time_fine, bound_lo, color="white", lw=1.6, ls="--", label="Wealth bounds")
ax2.plot(time_fine, bound_hi, color="white", lw=1.6, ls="--")

# Shade out-of-bounds regions
ax2.fill_between(
    time_fine, wealth_fine[0], bound_lo, color="black", alpha=0.45, zorder=2
)
ax2.fill_between(
    time_fine, bound_hi, wealth_fine[-1], color="black", alpha=0.45, zorder=2
)

# Overlay node positions
for ti, (t_val, wn_row) in enumerate(zip(t_np, wn_np)):
    ax2.scatter(
        np.full(len(wn_row), t_val), wn_row,
        s=30, c="white", alpha=0.9, edgecolors="none", zorder=4,
    )

ax2.set_title("b). Interpolated Allocation (Dynamic Bounds)", loc="left")
ax2.set_xlabel("Time")
ax2.set_ylabel("Wealth")
ax2.legend(fontsize=8)

cbar = fig.colorbar(im, ax=[ax1, ax2], shrink=0.9)
cbar.set_label("Risky asset allocation (%)")

out_path = os.path.join(os.path.dirname(__file__), "..", "dynamic_bounds_control_matrix.png")
plt.savefig(out_path, dpi=300, bbox_inches="tight")
print(f"Saved to {os.path.abspath(out_path)}")
plt.show()
