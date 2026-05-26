"""
time_interpolation_example.py
-----------------------------
Illustrates linear interpolation for a time-based allocation policy with 3 assets
and 3 time nodes. Shows how discrete theta values at nodes are interpolated to
produce smooth allocation trajectories.

Left panel: discrete theta matrix with nodes marked
Right panel: continuous interpolated allocations as stacked area chart
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, "..", "time_interpolation_example.png")

# Define 3 time nodes over a 30-year retirement horizon
time_nodes = np.array([0, 15, 30]) 
M = len(time_nodes)

theta = np.array([
    [0.70, 0.20],  
    [0.50, 0.30], 
    [0.10, 0.60], 
])

# Compute safe asset allocations (residual)
safe_asset_nodes = 1.0 - theta.sum(axis=1)

# Create fine time grid for interpolation
T = 30
time_fine = np.linspace(0, T, 301)

# Allocate arrays for interpolated allocations
risky1_interp = np.zeros_like(time_fine)
risky2_interp = np.zeros_like(time_fine)
safe_interp = np.zeros_like(time_fine)


def phi(theta_vec):
    """
    Simple transformation to ensure allocations sum to 1 and are non-negative.
    Here we just use the identity since we already ensure theta sums to <= 1.
    In a more complex case, this could be a softmax or other function.
    """
    risky1 = theta_vec[0]
    risky2 = theta_vec[1]
    safe = 1.0 - risky1 - risky2
    return np.array([risky1, risky2, safe])

def interpolate_theta(t, time_nodes, theta):
    """
    Linearly interpolate theta values for time t based on the discrete nodes.
    """
    if t <= time_nodes[0]:
        return theta[0]
    elif t >= time_nodes[-1]:
        return theta[-1]
    else:
        idx = np.searchsorted(time_nodes, t) - 1
        idx = np.clip(idx, 0, M - 2)
        t_i = time_nodes[idx]
        t_ip1 = time_nodes[idx + 1]
        alpha = (t - t_i) / (t_ip1 - t_i)
        return (1 - alpha) * theta[idx] + alpha * theta[idx + 1]


# Linear interpolation between nodes
for i, t in enumerate(time_fine):
    theta_interp = interpolate_theta(t, time_nodes, theta)
    allocation_interp = phi(theta_interp)

    risky1_interp[i] = allocation_interp[0]
    risky2_interp[i] = allocation_interp[1]
    safe_interp[i] = allocation_interp[2]

# Use inferno colormap 
cmap = cm.get_cmap("inferno")
color_stock = cmap(0.85) 
color_bonds = cmap(0.55)
color_cash = cmap(0.15)

# Create figure with two panels
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), constrained_layout=True)

# LEFT PANEL: LaTeX-style matrix visualization of theta
ax1.set_title("a). Policy Settings θ", loc="left", fontsize=11)
ax1.axis('off')

# Display the matrix in a cleaner format
# Main theta label
ax1.text(0.25, 0.60, r'$\theta =$', 
         ha='right', va='center', fontsize=20,
         transform=ax1.transAxes)

# Draw matrix brackets and values
bracket_x_left = 0.3
bracket_x_right = 0.6
bracket_y_positions = [0.70, 0.60, 0.50]

# Left bracket
ax1.plot([bracket_x_left, bracket_x_left - 0.02, bracket_x_left - 0.02, bracket_x_left],
         [0.75, 0.75, 0.45, 0.45], 'k-', linewidth=2.5, transform=ax1.transAxes)

# Right bracket
ax1.plot([bracket_x_right, bracket_x_right + 0.02, bracket_x_right + 0.02, bracket_x_right],
         [0.75, 0.75, 0.45, 0.45], 'k-', linewidth=2.5, transform=ax1.transAxes)


# Matrix values
for i in range(M):
    row_str = f'{theta[i, 0]:.2f}   {theta[i, 1]:.2f}'
    ax1.text(0.45, bracket_y_positions[i], row_str, 
             ha='center', va='center', fontsize=16, family='monospace',
             transform=ax1.transAxes)

# Add row labels (time nodes)
row_label_x = 0.65
for i, t in enumerate(time_nodes):
    ax1.text(row_label_x, bracket_y_positions[i], f'$t={int(t)}$', 
             ha='left', va='center', fontsize=10,
             transform=ax1.transAxes, color='dimgrey')

# Add column labels (asset classes)
col_label_y = 0.8
ax1.text(0.38, col_label_y, 'Stocks', 
         ha='center', va='top', fontsize=9,
         transform=ax1.transAxes, color=color_stock, weight='bold')
ax1.text(0.52, col_label_y, 'Bonds', 
         ha='center', va='top', fontsize=9,
         transform=ax1.transAxes, color=color_bonds, weight='bold')

# Add note about cash being residual
ax1.text(0.45, 0.25, r'Cash allocation $= 1 - \sum \theta_i$ (residual via $\varphi$)', 
         ha='center', va='center', fontsize=9, style='italic',
         transform=ax1.transAxes, color=color_cash,
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

ax1.set_xlim(0, 0.8)
ax1.set_ylim(.2, 1)

# RIGHT PANEL: Continuous interpolated allocations
ax2.set_title("b). Interpolated Allocation", loc="left", fontsize=11)

# Create stacked area plot
ax2.fill_between(time_fine, 0, safe_interp * 100, 
                  color=color_cash, alpha=0.85, label='Cash')
ax2.fill_between(time_fine, safe_interp * 100, 
                  (safe_interp + risky2_interp) * 100,
                  color=color_bonds, alpha=0.85, label='Bonds')
ax2.fill_between(time_fine, (safe_interp + risky2_interp) * 100, 100,
                  color=color_stock, alpha=0.85, label='Stocks')

# Mark the discrete nodes with vertical lines
for node in time_nodes:
    ax2.axvline(node, color='black', linewidth=1.2, linestyle='--', 
                alpha=0.5, zorder=3)

# Add markers at node points to show discrete values
node_indices = [np.argmin(np.abs(time_fine - node)) for node in time_nodes]
for i, idx in enumerate(node_indices):

    alloc = phi(theta[i]) * 100

    cash_y = alloc[2]
    bonds_y = cash_y + alloc[1]
    stocks_y = bonds_y + alloc[0]
    ax2.scatter(time_fine[idx], cash_y, color=color_cash, edgecolor='k', zorder=4)
    ax2.scatter(time_fine[idx], bonds_y, color=color_bonds, edgecolor='k', zorder=4)
    ax2.scatter(time_fine[idx], stocks_y, color=color_stock, edgecolor='k', zorder=4)


ax2.set_xlim(0, 30)
ax2.set_ylim(0, 108)
ax2.set_xlabel('Time since retirement (years)', fontsize=10)
ax2.set_ylabel('Portfolio allocation (%)', fontsize=10)
ax2.legend(loc='upper left', framealpha=0.95, fontsize=9)
ax2.grid(True, alpha=0.3, linestyle=':')
ax2.set_ylim(0, 100)


plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Saved figure to {output_path}")
plt.show()


if __name__ == "__main__":
    pass
