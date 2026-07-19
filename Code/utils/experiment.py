import zipfile
import json
import io
import os
import warnings
from typing import Any, Dict, List, Optional
from dataclasses import asdict, dataclass

import numpy as np

# ---------------------------------------------------------------------------
# Fixed-policy experiment dataclasses and helpers
# ---------------------------------------------------------------------------

@dataclass
class SimulationConfig:
    """Configuration parameters for a simulation experiment."""
    # Simulation parameters
    N_ASSETS: int
    N_SIMULATIONS: int
    SIMULATION_YEARS: int
    RETURN_SAMPLER: str

    # Wealth & spending parameters
    INITIAL_WEALTH: float
    DESIRED_SPENDING: float
    SPENDING_DECLINE_RATE: float
    CONSUMPTION_FLOOR: float
    FLOOR_DECLINE_RATE: float
    INCOME_TYPE: str

    # Optimization parameters
    INITIAL_POLICY: list
    OPTIMIZER_TYPE: str

    # Policy structure defaults (1, 1) -> constant/fixed allocation
    TIME_NODE_COUNT: int = 1
    WEALTH_NODE_COUNT: int = 1


@dataclass
class OptimizationResult:
    """Results from a fixed-policy optimization run."""
    best_policy: np.ndarray
    best_utility: float
    policy_history: np.ndarray
    cost_history: np.ndarray
    wealth_simulated: np.ndarray
    consumption_simulated: np.ndarray
    cumulative_inflation: np.ndarray
    time_nodes: Optional[np.ndarray] = None
    wealth_nodes: Optional[np.ndarray] = None


class LazyArrayStore:
    """Loads archived arrays on first access and caches them in memory."""

    def __init__(self, filepath: str, arrays_meta: Dict[str, Dict[str, Any]]):
        self._filepath = filepath
        self._arrays_meta = arrays_meta
        self._cache: Dict[str, np.ndarray] = {}

    def get(self, name: str) -> np.ndarray:
        if name in self._cache:
            return self._cache[name]
        if name not in self._arrays_meta:
            raise KeyError(f"Array '{name}' not found in archive metadata")

        with zipfile.ZipFile(self._filepath, "r") as zf:
            arr = _read_array_from_archive(zf, self._arrays_meta[name])

        self._cache[name] = arr
        return arr

    def get_optional(self, name: str) -> Optional[np.ndarray]:
        if name not in self._arrays_meta:
            return None
        return self.get(name)


class LazyOptimizationResult:
    """Optimization result wrapper that lazily loads ndarray fields from disk."""

    def __init__(self, best_utility: float, array_store: LazyArrayStore):
        self.best_utility = float(best_utility)
        self._array_store = array_store
        self._warned_missing_fields: set[str] = set()

    def _warn_missing_optional_array(self, name: str) -> None:
        if name in self._warned_missing_fields:
            return
        warnings.warn(
            (
                f"Optional array '{name}' is missing from this experiment archive. "
                "This is expected for older file versions; returning None."
            ),
            UserWarning,
            stacklevel=2,
        )
        self._warned_missing_fields.add(name)

    @property
    def best_policy(self) -> np.ndarray:
        return self._array_store.get("best_policy")

    @property
    def policy_history(self) -> np.ndarray:
        return self._array_store.get("policy_history")

    @property
    def cost_history(self) -> np.ndarray:
        return self._array_store.get("cost_history")

    @property
    def wealth_simulated(self) -> np.ndarray:
        return self._array_store.get("wealth_simulated")

    @property
    def consumption_simulated(self) -> np.ndarray:
        return self._array_store.get("consumption_simulated")

    @property
    def cumulative_inflation(self) -> np.ndarray:
        return self._array_store.get("cumulative_inflation")

    @property
    def time_nodes(self) -> Optional[np.ndarray]:
        arr = self._array_store.get_optional("time_nodes")
        if arr is None:
            self._warn_missing_optional_array("time_nodes")
        return arr

    @property
    def wealth_nodes(self) -> Optional[np.ndarray]:
        arr = self._array_store.get_optional("wealth_nodes")
        if arr is None:
            self._warn_missing_optional_array("wealth_nodes")
        return arr

    def materialize(self) -> OptimizationResult:
        """Load and return a fully materialized OptimizationResult."""
        return OptimizationResult(
            best_policy=self.best_policy,
            best_utility=self.best_utility,
            policy_history=self.policy_history,
            cost_history=self.cost_history,
            wealth_simulated=self.wealth_simulated,
            consumption_simulated=self.consumption_simulated,
            cumulative_inflation=self.cumulative_inflation,
            time_nodes=self.time_nodes,
            wealth_nodes=self.wealth_nodes,
        )


def experiment_filename(config: SimulationConfig) -> str:
    """Return the canonical archive filename for a given SimulationConfig."""
    time_node_count = config.TIME_NODE_COUNT
    wealth_node_count = config.WEALTH_NODE_COUNT

    if time_node_count > 1 and wealth_node_count > 1:
        return (
            f"experiment_{config.INITIAL_WEALTH}_{config.RETURN_SAMPLER}_"
            f"{time_node_count}tnodes_{wealth_node_count}wnodes.zip"
        )
    if time_node_count > 1:
        return (
            f"experiment_{config.INITIAL_WEALTH}_{config.RETURN_SAMPLER}_"
            f"{time_node_count}tnodes.zip"
        )
    if wealth_node_count > 1:
        return (
            f"experiment_{config.INITIAL_WEALTH}_{config.RETURN_SAMPLER}_"
            f"{wealth_node_count}wnodes.zip"
        )
    return f"experiment_{config.INITIAL_WEALTH}_{config.RETURN_SAMPLER}.zip"


def _write_array_to_archive(zf: zipfile.ZipFile, name: str, arr: np.ndarray) -> Dict[str, Any]:
    """Write a numpy array as .npy inside the archive."""
    np_arr = np.asarray(arr)
    path = f"arrays/{name}.npy"
    buf = io.BytesIO()
    np.save(buf, np_arr, allow_pickle=False)
    zf.writestr(path, buf.getvalue())
    return {
        "path": path,
        "format": "npy",
    }


def _read_array_from_archive(zf: zipfile.ZipFile, meta: Dict[str, Any]) -> np.ndarray:
    """Read an array saved by _write_array_to_archive."""
    raw = zf.read(meta["path"])
    if meta.get("format") != "npy":
        raise ValueError(f"Unsupported array format: {meta.get('format')}")
    return np.load(io.BytesIO(raw), allow_pickle=False)


def save_experiment(
    config: SimulationConfig,
    result: OptimizationResult,
    results_dir: str = "Results",
) -> None:
    """Persist a (config, result) pair to *results_dir* as a structured zip archive.

    Archive contents:
    - metadata.json: config + scalar metrics
    - arrays/*.npy: ndarray payloads from OptimizationResult
    """
    os.makedirs(results_dir, exist_ok=True)
    filename = experiment_filename(config)
    filepath = os.path.join(results_dir, filename)

    arrays_meta: Dict[str, Any] = {}
    array_fields = {
        "best_policy": result.best_policy,
        "policy_history": result.policy_history,
        "cost_history": result.cost_history,
        "wealth_simulated": result.wealth_simulated,
        "consumption_simulated": result.consumption_simulated,
        "cumulative_inflation": result.cumulative_inflation,
        "time_nodes": result.time_nodes,
        "wealth_nodes": result.wealth_nodes,
    }

    with zipfile.ZipFile(filepath, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, value in array_fields.items():
            if value is None:
                continue
            arrays_meta[name] = _write_array_to_archive(zf, name, np.asarray(value))

        metadata = {
            "schema_version": 1,
            "config": asdict(config),
            "result_scalars": {
                "best_utility": float(result.best_utility),
            },
            "arrays": arrays_meta,
        }
        zf.writestr("metadata.json", json.dumps(metadata, indent=2))

    print(f"Experiment saved to {filepath}")


def load_experiment(filepath: str, lazy_arrays: bool = True) -> Dict[str, Any]:
    """Load a single experiment archive and return ``{'config': ..., 'result': ...}``.

    Parameters
    ----------
    filepath:
        Path to the archived experiment zip.
    lazy_arrays:
        If True, array payloads are loaded on first access instead of immediately.
    """
    with zipfile.ZipFile(filepath, "r") as zf:
        metadata = json.loads(zf.read("metadata.json").decode("utf-8"))

        config = SimulationConfig(**metadata["config"])
        arrays_meta = metadata["arrays"]
        best_utility = float(metadata["result_scalars"]["best_utility"])

    if lazy_arrays:
        result = LazyOptimizationResult(
            best_utility=best_utility,
            array_store=LazyArrayStore(filepath=filepath, arrays_meta=arrays_meta),
        )
    else:
        with zipfile.ZipFile(filepath, "r") as zf:
            arrays = {
                name: _read_array_from_archive(zf, arr_meta)
                for name, arr_meta in arrays_meta.items()
            }

        if "time_nodes" not in arrays:
            warnings.warn(
                (
                    "Optional array 'time_nodes' is missing from this experiment archive. "
                    "This is expected for older file versions; returning None."
                ),
                UserWarning,
                stacklevel=2,
            )
        if "wealth_nodes" not in arrays:
            warnings.warn(
                (
                    "Optional array 'wealth_nodes' is missing from this experiment archive. "
                    "This is expected for older file versions; returning None."
                ),
                UserWarning,
                stacklevel=2,
            )

        result = OptimizationResult(
            best_policy=arrays["best_policy"],
            best_utility=best_utility,
            policy_history=arrays["policy_history"],
            cost_history=arrays["cost_history"],
            wealth_simulated=arrays["wealth_simulated"],
            consumption_simulated=arrays["consumption_simulated"],
            cumulative_inflation=arrays["cumulative_inflation"],
            time_nodes=arrays.get("time_nodes"),
            wealth_nodes=arrays.get("wealth_nodes"),
        )

    return {"config": config, "result": result}


def load_experiments(
    results_dir: str = "Results",
    return_sampler: Optional[str] = None,
    lazy_arrays: bool = True,
) -> List[Dict[str, Any]]:
    """Load all experiment archives from *results_dir*.

    Parameters
    ----------
    results_dir:
        Directory containing ``experiment_*.zip`` files.
    return_sampler:
        If provided, only load experiments whose ``RETURN_SAMPLER`` matches.
    lazy_arrays:
        If True, array payloads are loaded on first access instead of immediately.

    Returns
    -------
    List of ``{'config': SimulationConfig, 'result': OptimizationResult}`` dicts,
    sorted by ``INITIAL_WEALTH``.
    """
    files = [
        f for f in os.listdir(results_dir)
        if f.startswith("experiment") and f.endswith(".zip")
    ]
    experiments = []
    for fname in files:
        payload = load_experiment(os.path.join(results_dir, fname), lazy_arrays=lazy_arrays)
        if return_sampler is None or payload["config"].RETURN_SAMPLER == return_sampler:
            experiments.append(payload)
    # Ensure mixed fixed-wealth (numeric) and distributed (None) runs are sortable.
    # Sort order: distributed (None) first, then increasing numeric wealth.
    experiments.sort(
        key=lambda e: (
            e["config"].INITIAL_WEALTH is not None,
            float(e["config"].INITIAL_WEALTH)
            if e["config"].INITIAL_WEALTH is not None
            else float("-inf"),
        )
    )
    return experiments