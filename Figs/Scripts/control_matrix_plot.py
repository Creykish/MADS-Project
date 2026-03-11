import numpy as np
import matplotlib.pyplot as plt


def bilinear_interpolate_grid(matrix, time_points, wealth_points, time_fine, wealth_fine):
    """Bilinear interpolation from a coarse (time x wealth) grid onto a finer grid."""
    t_mesh, w_mesh = np.meshgrid(time_fine, wealth_fine, indexing="ij")

    t0 = np.floor(t_mesh).astype(int)
    w0 = np.floor(w_mesh).astype(int)
    t1 = np.clip(t0 + 1, 0, len(time_points) - 1)
    w1 = np.clip(w0 + 1, 0, len(wealth_points) - 1)

    # Keep indices inside valid range.
    t0 = np.clip(t0, 0, len(time_points) - 1)
    w0 = np.clip(w0, 0, len(wealth_points) - 1)

    dt = t_mesh - t0
    dw = w_mesh - w0

    q00 = matrix[t0, w0]
    q10 = matrix[t1, w0]
    q01 = matrix[t0, w1]
    q11 = matrix[t1, w1]

    return (
        q00 * (1 - dt) * (1 - dw)
        + q10 * dt * (1 - dw)
        + q01 * (1 - dt) * dw
        + q11 * dt * dw
    )


def main():
    # Rows are time steps 0..5, columns are wealth levels 0..4.
    control_matrix = np.array(
        [
            [98.0, 91.0, 79.5, 66.0, 53.5],
            [94.0, 83.0, 72.0, 57.5, 41.0],
            [86.5, 88.0, 63.0, 49.5, 36.0],
            [78.0, 62.5, 67.0, 38.0, 27.5],
            [60.0, 54.0, 35.0, 22.0, 12.0],
            [45.0, 30.5, 21.0, 9.5, 3.0],
        ],
        dtype=float,
    )

    time_points = np.arange(6)
    wealth_points = np.arange(5)

    time_fine = np.linspace(0, 5, 251)
    wealth_fine = np.linspace(0, 4, 201)
    interpolated = bilinear_interpolate_grid(
        control_matrix, time_points, wealth_points, time_fine, wealth_fine
    )

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), constrained_layout=True)

    # Left panel: coarse control matrix with exact cells.
    im1 = ax1.imshow(
        control_matrix.T,
        origin="lower",
        cmap="inferno",
        vmin=0,
        vmax=100,
        aspect="auto",
        extent=[-0.5, 5.5, -0.5, 4.5],
    )
    ax1.set_title("a). Control Matrix (Discrete)", loc="left")
    ax1.set_xlabel("Time step")
    ax1.set_ylabel("Wealth level")
    ax1.set_xticks(time_points)
    ax1.set_yticks(wealth_points)

    for t in time_points:
        for w in wealth_points:
            ax1.text(t, w, f"{int(control_matrix[t, w])}%", ha="center", va="center", color="white", fontsize=8)

    # Right panel: bilinearly interpolated heat map.
    im2 = ax2.imshow(
        interpolated.T,
        origin="lower",
        cmap="inferno",
        vmin=0,
        vmax=100,
        aspect="auto",
        extent=[time_fine.min(), time_fine.max(), wealth_fine.min(), wealth_fine.max()],
    )
    ax2.set_title("b). Interpolated Heat Map (Bilinear)", loc="left")
    ax2.set_xlabel("Time step")
    ax2.set_ylabel("Wealth level")

    # Overlay original grid points.
    t_grid, w_grid = np.meshgrid(time_points, wealth_points)
    ax2.scatter(t_grid, w_grid, s=12, c="white", alpha=0.8, edgecolors="none")

    cbar = fig.colorbar(im2, ax=[ax1, ax2], shrink=0.95)
    cbar.set_label("Risky asset allocation (%)")
    plt.savefig("./Figs/example_control_matrix_plot.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    main()
