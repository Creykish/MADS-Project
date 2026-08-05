"""Utility functions for analysis notebooks."""



import numpy as np
import matplotlib.pyplot as plt
import polars as pl

ASSET_COLOURS = {
    'Cash': '#000000',
    'Bonds': '#6464FF',
    'Stocks': '#ff6464',
}

RETURN_SAMPLER_DISPLAY_NAMES = {
    'cholesky': 'IID GBM',
    'block_bootstrapped': 'Block Bootstrapped\n(1870-2020)',
    'block_bootstrapped_1950': 'Block Bootstrapped\n(1950-2020)',
}


def _ordered_samplers(samplers: list[str]) -> list[str]:
    """Order samplers by canonical display-name mapping key order."""
    canonical = [s for s in RETURN_SAMPLER_DISPLAY_NAMES if s in samplers]
    extras = sorted(s for s in samplers if s not in RETURN_SAMPLER_DISPLAY_NAMES)
    return canonical + extras

def _wealth_bucket_key(x: np.ndarray, bucket: float = 50_000.0) -> np.ndarray:
    """Bucket wealth values for alignment across datasets."""
    return np.round(x / bucket).astype(int)


def plot_metric_vs_node_baseline(
    outcome_data: pl.DataFrame,
    nodes_to_plot: list[int],
    samplers_to_plot: list[str],
    node_dimension: str = 'wealth',
    metric: str = 'bankruptcy_density',
    baseline_node_count: int = 1,
    metric_label: str | None = None,
    diff_label: str = 'Difference from Baseline',
    rel_diff_label: str = 'Relative Difference from Baseline',
    top_ylim: tuple[float, float] | None = None,
    diff_ylim: tuple[float, float] | None = None,
    rel_diff_ylim: tuple[float, float] | None = None,
    top_as_percent: bool = True,
    diff_as_percent: bool = True,
    rel_diff_as_percent: bool = True,
    sampler_display_names: dict[str, str] | None = None,
) -> tuple[plt.Figure, np.ndarray]:
    """
    Plot a metric against varying node counts (wealth or time), with baseline comparison.
    
    Generalizes plotting across either wealth or time node dimensions.
    
    Parameters
    ----------
    outcome_data : pl.DataFrame
        DataFrame with outcome metrics and experiment configuration. Should contain
        columns: 'sampler', 'n_wealth_nodes', 'n_time_nodes', 'simulated_initial_wealth',
        and the metric column.
    nodes_to_plot : list[int]
        List of node counts to include in the plot.
    samplers_to_plot : list[str]
        List of return samplers to plot.
    node_dimension : str, default 'wealth'
        Dimension to vary: 'wealth' (n_wealth_nodes) or 'time' (n_time_nodes).
    metric : str, default 'bankruptcy_density'
        Metric column to plot.
    baseline_node_count : int, default 1
        Node count to use as baseline for difference calculations.
    metric_label : str | None
        Y-axis label for the metric. If None, derived from metric name.
    diff_label : str
        Y-axis label for absolute difference plot.
    rel_diff_label : str
        Y-axis label for relative difference plot.
    top_ylim : tuple[float, float] | None
        Y-limits for the metric plot.
    diff_ylim : tuple[float, float] | None
        Y-limits for the difference plot.
    rel_diff_ylim : tuple[float, float] | None
        Y-limits for the relative difference plot.
    top_as_percent : bool
        Format metric y-axis as percentages.
    diff_as_percent : bool
        Format difference y-axis as percentages.
    rel_diff_as_percent : bool
        Format relative difference y-axis as percentages.
    sampler_display_names : dict[str, str] | None
        Mapping of sampler names to display labels. If None, uses sampler names as-is.
    
    Returns
    -------
    tuple[plt.Figure, np.ndarray]
        Figure and axes array.
    """
    # Validate node_dimension
    if node_dimension not in ('wealth', 'time'):
        raise ValueError(f"node_dimension must be 'wealth' or 'time', got {node_dimension!r}")
    
    # Set column names based on dimension
    if node_dimension == 'wealth':
        varying_col = 'n_wealth_nodes'
    else:
        varying_col = 'n_time_nodes'
    
    # Default sampler display names
    if sampler_display_names is None:
        sampler_display_names = {s: s for s in samplers_to_plot}

    ordered_samplers = _ordered_samplers(samplers_to_plot)
    
    fig, axes = plt.subplots(
        3,
        len(ordered_samplers),
        figsize=(12, 7),
        dpi=300,
        squeeze=True,
        sharex=True,
    )

    linestyles = [None, '--', '-.', ':', (0, (3, 1, 1, 1)), (0, (5, 1))]
    markers = ['o', 's', '^', 'D', 'v', '*']

    if len(ordered_samplers) == 1:
        axes = axes.reshape(3, 1)

    metric_label = metric_label or metric.replace('_', ' ').title()
    denom = max(nodes_to_plot) - min(nodes_to_plot)

    for j, sampler in enumerate(ordered_samplers):
        ax1: plt.Axes = axes[0, j]
        ax2: plt.Axes = axes[1, j]
        ax3: plt.Axes = axes[2, j]

        sampler_data = outcome_data.filter(pl.col('sampler') == sampler)

        def _select_node_subset(node_count: int) -> pl.DataFrame:
            """Select data for a specific node count, preferring distributed initial wealth."""
            node_all = sampler_data.filter(pl.col(varying_col) == node_count).sort('simulated_initial_wealth')
            if node_all.height == 0:
                return node_all
            node_distributed = node_all.filter(pl.col('initial_wealth').is_null())
            if node_distributed.height > 0:
                return node_distributed
            return node_all

        baseline_data = _select_node_subset(baseline_node_count)

        baseline_x = np.asarray(baseline_data['simulated_initial_wealth'].to_list(), dtype=float)
        baseline_y = np.asarray(baseline_data[metric].to_list(), dtype=float)

        baseline_mask = np.isfinite(baseline_x) & np.isfinite(baseline_y)
        baseline_x = baseline_x[baseline_mask]
        baseline_y = baseline_y[baseline_mask]
        baseline_key = _wealth_bucket_key(baseline_x)

        sampler_common_x = []

        for n in nodes_to_plot:
            this_data = _select_node_subset(n)

            x = np.asarray(this_data['simulated_initial_wealth'].to_list(), dtype=float)
            y = np.asarray(this_data[metric].to_list(), dtype=float)

            mask = np.isfinite(x) & np.isfinite(y)
            x = x[mask]
            y = y[mask]
            x_key = _wealth_bucket_key(x)

            common_key, base_idx, this_idx = np.intersect1d(baseline_key, x_key, return_indices=True)
            if common_key.size == 0:
                print(
                    f"Warning: no overlapping simulated_initial_wealth buckets for sampler '{sampler}' and {varying_col}={n}. Skipping."
                )
                continue

            common_x = baseline_x[base_idx]
            baseline_y_aligned = baseline_y[base_idx]
            y_aligned = y[this_idx]

            diff_abs = y_aligned - baseline_y_aligned
            diff_rel = np.divide(
                y_aligned,
                baseline_y_aligned,
                out=np.full_like(y_aligned, 1, dtype=float),
                where=baseline_y_aligned != 0,
            ) - 1.0

            c = plt.cm.inferno(0.5 if denom == 0 else (n - min(nodes_to_plot)) / denom)
            linestyle = linestyles[nodes_to_plot.index(n) % len(linestyles)]
            marker = markers[nodes_to_plot.index(n) % len(markers)]
            node_label = 'Baseline' if n == baseline_node_count else f'{n}'

            ax1.plot(
                common_x,
                y_aligned,
                marker=marker,
                markersize=4,
                label=node_label,
                color=c,
                linestyle=linestyle,
            )

            sampler_common_x.append(common_x)

            if n == baseline_node_count:
                continue

            ax2.plot(
                common_x,
                diff_abs,
                marker=marker,
                markersize=4,
                label=f"{n}",
                color=c,
                linestyle=linestyle,
                zorder=10
            )

            ax3.plot(
                common_x,
                diff_rel,
                marker=marker,
                markersize=4,
                label=f"{n}",
                color=c,
                linestyle=linestyle,
                zorder=10
            )

        if sampler_common_x:
            x_joined = np.concatenate(sampler_common_x)
            x_min = float(np.nanmin(x_joined))
            x_max = float(np.nanmax(x_joined))
        else:
            fallback_x = np.asarray(
                sampler_data['simulated_initial_wealth'].to_list(),
                dtype=float,
            )
            fallback_x = fallback_x[np.isfinite(fallback_x)]
            if fallback_x.size > 0:
                x_min = float(np.nanmin(fallback_x))
                x_max = float(np.nanmax(fallback_x))
            else:
                x_min, x_max = 0.0, 1.0

        ax1.set_xlim(x_min, x_max)
        ax2.set_xlim(x_min, x_max)
        ax3.set_xlim(x_min, x_max)

        ax2.axhline(0.0, color='black', linestyle='--', linewidth=1.0, zorder=5)
        ax3.axhline(0.0, color='black', linestyle='--', linewidth=1.0, zorder=5)

        ax1.text(0.02, 1.01, _get_plot_letter(j, 0, len(ordered_samplers)), transform=ax1.transAxes, fontsize=16, va='bottom', ha='left')
        ax2.text(0.02, 1.01, _get_plot_letter(j, 1, len(ordered_samplers)), transform=ax2.transAxes, fontsize=16, va='bottom', ha='left')
        ax3.text(0.02, 1.01, _get_plot_letter(j, 2, len(ordered_samplers)), transform=ax3.transAxes, fontsize=16, va='bottom', ha='left')

        if top_ylim is not None:
            ax1.set_ylim(*top_ylim)
        if diff_ylim is not None:
            ax2.set_ylim(*diff_ylim)
        if rel_diff_ylim is not None:
            ax3.set_ylim(*rel_diff_ylim)

        if top_as_percent:
            ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.0%}'.format(y)))
        if diff_as_percent:
            ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
        if rel_diff_as_percent:
            ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.1%}'.format(y)))

        ax1.set_title(sampler_display_names[sampler], fontsize=12, fontweight='bold', pad=8)
        ax3.set_xlabel('Simulated Initial Wealth', fontsize=10)

    for plot in axes.flatten():
        plot.grid(True, which='both', linestyle='--', linewidth=0.5, color='white')
        plot.set_facecolor('#c4c4c4')

    axes[0, 0].set_ylabel(metric_label, fontsize=10)
    axes[1, 0].set_ylabel(diff_label, fontsize=10)
    axes[2, 0].set_ylabel(rel_diff_label, fontsize=10)

    def _safe_k_formatter(x: float, _: int) -> str:
        if not np.isfinite(x):
            return ''
        return f'${int(x/1000)}k'

    for j in range(len(ordered_samplers)):
        axes[2, j].xaxis.set_major_formatter(plt.FuncFormatter(_safe_k_formatter))
        axes[2, j].tick_params(axis='x', rotation=45)

    fig.tight_layout()

    handles, labels = axes[0, 0].get_legend_handles_labels()
    if handles:
        fig.legend(
            handles=handles,
            labels=labels,
            loc='upper center',
            bbox_to_anchor=(0.5, 1.06),
            ncol=len(nodes_to_plot),
            fontsize=9,
            frameon=True,
            title='Node Count',
            title_fontsize=10,
            facecolor='#c4c4c4',
            edgecolor='black',
        )

    return fig, axes


def _get_plot_letter(row_idx: int, col_idx: int, n_cols: int) -> str:
    """Generate plot letter label (a), b), c), etc.)."""
    letter = chr(ord('a') + row_idx * n_cols + col_idx)
    return f'{letter}).'


def plot_metric_vs_known_wealth_fixed_baseline(
    outcome_node_data: pl.DataFrame,
    fixed_baseline_data: pl.DataFrame,
    nodes_to_plot: list[int],
    samplers_to_plot: list[str],
    node_dimension: str = 'wealth',
    metric: str = 'bankruptcy_density',
    metric_label: str | None = None,
    diff_label: str = 'Difference from Fixed Baseline',
    rel_diff_label: str = 'Relative Difference from Fixed Baseline',
    top_ylim: tuple[float, float] | None = None,
    diff_ylim: tuple[float, float] | None = None,
    rel_diff_ylim: tuple[float, float] | None = None,
    top_as_percent: bool = True,
    diff_as_percent: bool = True,
    rel_diff_as_percent: bool = True,
    sampler_display_names: dict[str, str] | None = None,
    baseline_label: str = 'Baseline',
    legend_title: str = 'Node Count',
) -> tuple[plt.Figure, np.ndarray]:
    """
    Compare outcome metrics against a fixed baseline, varying either wealth or time node dimensions.
    
    Parameters
    ----------
    outcome_node_data : pl.DataFrame
        DataFrame with varying node outcomes and experiment configuration.
    fixed_baseline_data : pl.DataFrame
        DataFrame with baseline outcomes (fixed allocation or glidepath).
    nodes_to_plot : list[int]
        List of node counts to include in the plot.
    samplers_to_plot : list[str]
        List of return samplers to plot.
    node_dimension : str, default 'wealth'
        Dimension to vary: 'wealth' (n_wealth_nodes) or 'time' (n_time_nodes).
    metric : str, default 'bankruptcy_density'
        Metric column to plot.
    metric_label : str | None
        Y-axis label for the metric. If None, derived from metric name.
    diff_label : str
        Y-axis label for absolute difference plot.
    rel_diff_label : str
        Y-axis label for relative difference plot.
    top_ylim : tuple[float, float] | None
        Y-limits for the metric plot.
    diff_ylim : tuple[float, float] | None
        Y-limits for the difference plot.
    rel_diff_ylim : tuple[float, float] | None
        Y-limits for the relative difference plot.
    top_as_percent : bool
        Format metric y-axis as percentages.
    diff_as_percent : bool
        Format difference y-axis as percentages.
    rel_diff_as_percent : bool
        Format relative difference y-axis as percentages.
    sampler_display_names : dict[str, str] | None
        Mapping of sampler names to display labels. If None, uses sampler names as-is.
    
    Returns
    -------
    tuple[plt.Figure, np.ndarray]
        Figure and axes array.
    """
    # Validate node_dimension
    if node_dimension not in ('wealth', 'time'):
        raise ValueError(f"node_dimension must be 'wealth' or 'time', got {node_dimension!r}")
    
    # Set column name based on dimension
    if node_dimension == 'wealth':
        varying_col = 'n_wealth_nodes'
    else:
        varying_col = 'n_time_nodes'
    
    # Default sampler display names
    if sampler_display_names is None:
        sampler_display_names = {s: s for s in samplers_to_plot}

    ordered_samplers = _ordered_samplers(samplers_to_plot)
    
    fig, axes = plt.subplots(
        3,
        len(ordered_samplers),
        figsize=(12, 7),
        dpi=300,
        squeeze=True,
        sharex=True,
    )

    linestyles = [None, '--', '-.', ':', (0, (3, 1, 1, 1)), (0, (5, 1))]
    markers = ['o', 's', '^', 'D', 'v', '*']

    if len(ordered_samplers) == 1:
        axes = axes.reshape(3, 1)

    metric_label = metric_label or metric.replace('_', ' ').title()
    denom = max(nodes_to_plot) - min(nodes_to_plot)

    for j, sampler in enumerate(ordered_samplers):
        ax1: plt.Axes = axes[0, j]
        ax2: plt.Axes = axes[1, j]
        ax3: plt.Axes = axes[2, j]

        baseline_data = fixed_baseline_data.filter(pl.col('sampler') == sampler).sort('simulated_initial_wealth')
        baseline_x = np.asarray(baseline_data['simulated_initial_wealth'].to_list(), dtype=float)
        baseline_y = np.asarray(baseline_data[metric].to_list(), dtype=float)

        baseline_mask = np.isfinite(baseline_x) & np.isfinite(baseline_y)
        baseline_x = baseline_x[baseline_mask]
        baseline_y = baseline_y[baseline_mask]
        baseline_key = _wealth_bucket_key(baseline_x)

        # Always show fixed baseline explicitly on the top row.
        if baseline_x.size > 0:
            ax1.plot(
                baseline_x,
                baseline_y,
                marker='o',
                markersize=4,
                label=baseline_label,
                color='blue',
                linestyle='-',
                zorder=12,
            )

        sampler_common_x = []

        for n in nodes_to_plot:
            this_data = outcome_node_data.filter(
                (pl.col('sampler') == sampler)
                & (pl.col(varying_col) == n)
            ).sort('simulated_initial_wealth')

            x = np.asarray(this_data['simulated_initial_wealth'].to_list(), dtype=float)
            y = np.asarray(this_data[metric].to_list(), dtype=float)

            mask = np.isfinite(x) & np.isfinite(y)
            x = x[mask]
            y = y[mask]
            x_key = _wealth_bucket_key(x)

            common_key, base_idx, this_idx = np.intersect1d(baseline_key, x_key, return_indices=True)
            if common_key.size == 0:
                print(
                    f"Warning: no overlapping simulated_initial_wealth buckets for sampler '{sampler}' and {varying_col}={n}. Skipping."
                )
                continue

            common_x = baseline_x[base_idx]
            baseline_y_aligned = baseline_y[base_idx]
            y_aligned = y[this_idx]

            diff_abs = y_aligned - baseline_y_aligned
            diff_rel = np.divide(
                y_aligned,
                baseline_y_aligned,
                out=np.full_like(y_aligned, 1, dtype=float),
                where=baseline_y_aligned != 0,
            ) - 1.0

            c = plt.cm.inferno(0.5 if denom == 0 else (n - min(nodes_to_plot)) / denom)
            linestyle = linestyles[nodes_to_plot.index(n) % len(linestyles)]
            marker = markers[nodes_to_plot.index(n) % len(markers)]

            ax1.plot(
                common_x,
                y_aligned,
                marker=marker,
                markersize=4,
                label=f'{n}',
                color=c,
                linestyle=linestyle,
            )

            sampler_common_x.append(common_x)

            ax2.plot(
                common_x,
                diff_abs,
                marker=marker,
                markersize=4,
                label=f'{n}',
                color=c,
                linestyle=linestyle,
                zorder=10
            )

            ax3.plot(
                common_x,
                diff_rel,
                marker=marker,
                markersize=4,
                label=f'{n}',
                color=c,
                linestyle=linestyle,
                zorder=10
            )

        if sampler_common_x:
            x_joined = np.concatenate(sampler_common_x)
            x_min = float(np.nanmin(x_joined))
            x_max = float(np.nanmax(x_joined))
        else:
            fallback_x = np.asarray(
                fixed_baseline_data.filter(pl.col('sampler') == sampler)['simulated_initial_wealth'].to_list(),
                dtype=float,
            )
            fallback_x = fallback_x[np.isfinite(fallback_x)]
            if fallback_x.size > 0:
                x_min = float(np.nanmin(fallback_x))
                x_max = float(np.nanmax(fallback_x))
            else:
                x_min, x_max = 0.0, 1.0

        ax1.set_xlim(x_min, x_max)
        ax2.set_xlim(x_min, x_max)
        ax3.set_xlim(x_min, x_max)

        ax2.axhline(0.0, color='black', linestyle='--', linewidth=1.0, zorder=5)
        ax3.axhline(0.0, color='black', linestyle='--', linewidth=1.0, zorder=5)

        ax1.text(0.02, 1.01, _get_plot_letter(j, 0, len(ordered_samplers)), transform=ax1.transAxes, fontsize=16, va='bottom', ha='left')
        ax2.text(0.02, 1.01, _get_plot_letter(j, 1, len(ordered_samplers)), transform=ax2.transAxes, fontsize=16, va='bottom', ha='left')
        ax3.text(0.02, 1.01, _get_plot_letter(j, 2, len(ordered_samplers)), transform=ax3.transAxes, fontsize=16, va='bottom', ha='left')

        if top_ylim is not None:
            ax1.set_ylim(*top_ylim)
        if diff_ylim is not None:
            ax2.set_ylim(*diff_ylim)
        if rel_diff_ylim is not None:
            ax3.set_ylim(*rel_diff_ylim)

        if top_as_percent:
            ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.0%}'.format(y)))
        if diff_as_percent:
            ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
        if rel_diff_as_percent:
            ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.1%}'.format(y)))

        ax1.set_title(sampler_display_names[sampler], fontsize=12, fontweight='bold', pad=8)
        ax3.set_xlabel('Simulated Initial Wealth', fontsize=10)

    for plot in axes.flatten():
        plot.grid(True, which='both', linestyle='--', linewidth=0.5, color='white')
        plot.set_facecolor('#c4c4c4')

    axes[0, 0].set_ylabel(metric_label, fontsize=10)
    axes[1, 0].set_ylabel(diff_label, fontsize=10)
    axes[2, 0].set_ylabel(rel_diff_label, fontsize=10)

    def _safe_k_formatter(x: float, _: int) -> str:
        if not np.isfinite(x):
            return ''
        return f'${int(x/1000)}k'

    for j in range(len(ordered_samplers)):
        axes[2, j].xaxis.set_major_formatter(plt.FuncFormatter(_safe_k_formatter))
        axes[2, j].tick_params(axis='x', rotation=45)

    fig.tight_layout()

    handles, labels = axes[0, 0].get_legend_handles_labels()
    if handles:
        fig.legend(
            handles=handles,
            labels=labels,
            loc='upper center',
            bbox_to_anchor=(0.5, 1.06),
            ncol=len(nodes_to_plot)+1,
            fontsize=9,
            frameon=True,
            title=legend_title,
            title_fontsize=10,
            facecolor='#c4c4c4',
            edgecolor='black',
        )

    return fig, axes
