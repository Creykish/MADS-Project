"""
Metrics for evaluating retirement simulation results.

Functions for computing wealth and consumption statistics from
Monte Carlo simulation outputs.
"""

from typing import Optional
import numpy as np


def compute_wealth_metrics(wealth: np.ndarray) -> dict:
    """Compute wealth metrics from simulated wealth paths.

    Parameters
    ----------
    wealth:
        Array of shape ``(N_SIMULATIONS, T+1)`` where column 0 is initial wealth.

    Returns
    -------
    dict with keys:
        ``bankruptcy_rate_terminal``, ``bankruptcy_rate_ever``,
        ``bankruptcy_density``,
        ``terminal_mean``, ``terminal_median``,
        ``terminal_p05``, ``terminal_p25``, ``terminal_p75``, ``terminal_p95``.
    """
    wealth = np.asarray(wealth)
    paths = wealth[:, 1:]   # exclude initial wealth column
    terminal = wealth[:, -1]

    return {
        "bankruptcy_rate_terminal": float(np.mean(terminal <= 0)),
        "bankruptcy_rate_ever": float(np.mean(np.any(paths <= 0, axis=1))),
        "bankruptcy_density": float(np.mean(paths <= 0)),
        "terminal_mean": float(np.mean(terminal)),
        "terminal_median": float(np.median(terminal)),
        "terminal_p05": float(np.quantile(terminal, 0.05)),
        "terminal_p25": float(np.quantile(terminal, 0.25)),
        "terminal_p75": float(np.quantile(terminal, 0.75)),
        "terminal_p95": float(np.quantile(terminal, 0.95)),
    }


def compute_consumption_metrics(
    consumption: np.ndarray,
    cumulative_inflation: Optional[np.ndarray] = None,
) -> dict:
    """Compute consumption metrics from simulated consumption paths.

    Parameters
    ----------
    consumption:
        Nominal consumption array of shape ``(N_SIMULATIONS, T)``.
    cumulative_inflation:
        Cumulative inflation array of shape ``(N_SIMULATIONS, T)`` or ``(T,)``.
        When provided, real-consumption metrics are included.

    Returns
    -------
    dict with keys:
        ``consumption_mean``, ``consumption_median``,
        ``consumption_p05``, ``consumption_p25``, ``consumption_p75``, ``consumption_p95``
        (nominal, pooled across all time steps), plus the same set prefixed
        ``real_`` when *cumulative_inflation* is provided.
    """
    consumption = np.asarray(consumption)
    flat = consumption.ravel()

    metrics = {
        "consumption_mean": float(np.mean(flat)),
        "consumption_median": float(np.median(flat)),
        "consumption_p05": float(np.quantile(flat, 0.05)),
        "consumption_p25": float(np.quantile(flat, 0.25)),
        "consumption_p75": float(np.quantile(flat, 0.75)),
        "consumption_p95": float(np.quantile(flat, 0.95)),
    }

    if cumulative_inflation is not None:
        inflation = np.asarray(cumulative_inflation)
        real = consumption / inflation
        real_flat = real.ravel()
        metrics.update({
            "real_consumption_mean": float(np.mean(real_flat)),
            "real_consumption_median": float(np.median(real_flat)),
            "real_consumption_p05": float(np.quantile(real_flat, 0.05)),
            "real_consumption_p25": float(np.quantile(real_flat, 0.25)),
            "real_consumption_p75": float(np.quantile(real_flat, 0.75)),
            "real_consumption_p95": float(np.quantile(real_flat, 0.95)),
        })

    return metrics


def compute_experiment_metrics(config, result) -> dict:
    """Compute all metrics for a single (config, result) experiment pair.

    Combines :func:`compute_wealth_metrics` and
    :func:`compute_consumption_metrics` and attaches identifying metadata.

    Parameters
    ----------
    config:
        A :class:`~utils.experiment.SimulationConfig` instance.
    result:
        An :class:`~utils.experiment.OptimizationResult` instance.

    Returns
    -------
    Flat dict suitable for use as a :class:`pandas.DataFrame` row.
    """
    wealth = np.asarray(result.wealth_simulated)
    consumption = np.asarray(result.consumption_simulated)
    inflation = np.asarray(result.cumulative_inflation)

    metrics: dict = {
        "sampler": config.RETURN_SAMPLER,
        "initial_wealth": float(config.INITIAL_WEALTH),
        "n_simulations": int(config.N_SIMULATIONS),
        "years": int(config.SIMULATION_YEARS),
    }
    metrics.update(compute_wealth_metrics(wealth))
    metrics.update(compute_consumption_metrics(consumption, cumulative_inflation=inflation))
    return metrics


def pool_experiment_metrics(experiments: list) -> dict:
    """Pool wealth and consumption across a list of experiments and compute metrics.

    Parameters
    ----------
    experiments:
        List of ``{'config': SimulationConfig, 'result': OptimizationResult}`` dicts
        as returned by :func:`~utils.experiment.load_experiments`.

    Returns
    -------
    Flat dict of pooled metrics (no ``sampler`` / ``initial_wealth`` keys).
    """
    all_wealth_paths = []
    all_consumption = []
    all_inflation = []

    for payload in experiments:
        res = payload["result"]
        w = np.asarray(res.wealth_simulated)
        c = np.asarray(res.consumption_simulated)
        inf = np.asarray(res.cumulative_inflation)
        all_wealth_paths.append(w)
        all_consumption.append(c)
        all_inflation.append(inf)

    pooled_wealth = np.concatenate(all_wealth_paths, axis=0)
    pooled_consumption = np.concatenate(all_consumption, axis=0)
    pooled_inflation = np.concatenate(all_inflation, axis=0)

    metrics = {"n_terminal_obs": int(pooled_wealth.shape[0])}
    metrics.update(compute_wealth_metrics(pooled_wealth))
    metrics.update(compute_consumption_metrics(pooled_consumption, cumulative_inflation=pooled_inflation))
    return metrics
