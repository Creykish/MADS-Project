import yaml
import zipfile
import json
import pickle
import io
from pathlib import Path
from typing import Any, Dict, Optional
from dataclasses import dataclass, field

# Lazy import to avoid circular dependency
def _get_create_generator_from_config():
    """Lazy import to avoid circular dependency."""
    from .return_generators import create_generator_from_config
    return create_generator_from_config


@dataclass
class ExperimentResults:
    """Container for experiment results."""
    policy: Optional[Any] = None  # Optimized policy (numpy array, torch tensor, etc.)
    cost_history: Optional[Any] = None  # Cost history during optimization
    extra: Dict[str, Any] = field(default_factory=dict)  # Additional results


@dataclass
class Experiment:
    """
    Container for experiment configuration and results.
    Supports saving/loading to zip files with intelligent format selection.
    Tracks generator metadata for full reproducibility.
    """

    name: str
    description: str
    parameters: Dict[str, Any]
    results: ExperimentResults = field(default_factory=ExperimentResults)
    generator_config: Dict[str, Any] = field(default_factory=dict)  # Metadata about return generator

    def add_result(self, name: str, data: Any) -> None:
        """Add a result to the experiment (stored in extra dict)."""
        self.results.extra[name] = data
    
    def set_generator_config(self, generator_type: str, **kwargs) -> None:
        """
        Record metadata about the return generator used.
        
        Examples
        --------
        # For Cholesky bootstrap
        exp.set_generator_config("cholesky", mean_returns=mean_ret, cov_matrix=cov)
        
        # For block bootstrap
        exp.set_generator_config("block_bootstrap", path="path/to/data.npy")
        """
        self.generator_config = {
            "type": generator_type,
            "config": kwargs
        }

    def get_result(self, name: str) -> Any:
        """Retrieve a result by name from extra dict."""
        return self.results.extra.get(name)

    def reconstruct_generator(self):
        """
        Reconstruct the return generator from saved config.
        
        Returns
        -------
        ReturnGenerator or None
            The reconstructed generator, or None if no config was saved.
        """
        if not self.generator_config:
            return None
        
        create_fn = _get_create_generator_from_config()
        return create_fn(self.generator_config["config"])
    
    def save_to_zip(self, filepath: str) -> None:
        """
        Save experiment config and results to a zip file.

        Results are saved based on their type:
        - dict/list: saved as JSON
        - pd.DataFrame: saved as parquet
        - numpy arrays: saved as pickle
        - other: saved as pickle
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(filepath, "w", zipfile.ZIP_DEFLATED) as zf:
            # Save metadata
            metadata = {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
                "generator_config": self.generator_config,
            }
            zf.writestr("metadata.yaml", yaml.dump(metadata))

            # Save results
            if self.results.policy is not None:
                self._save_result_to_zip(zf, "policy", self.results.policy)
            if self.results.cost_history is not None:
                self._save_result_to_zip(zf, "cost_history", self.results.cost_history)
            for result_name, data in self.results.extra.items():
                self._save_result_to_zip(zf, result_name, data)

    def _save_result_to_zip(
        self, zf: zipfile.ZipFile, name: str, data: Any
    ) -> None:
        """Save a single result to the zip file with appropriate format."""
        try:
            import pandas as pd

            is_dataframe = isinstance(data, pd.DataFrame)
        except ImportError:
            is_dataframe = False

        try:
            import numpy as np

            is_array = isinstance(data, np.ndarray)
        except ImportError:
            is_array = False

        if isinstance(data, (dict, list)):
            # Save as JSON
            zf.writestr(f"results/{name}.json", json.dumps(data))
        elif is_dataframe:
            # Save DataFrame as parquet
            buffer = io.BytesIO()
            data.to_parquet(buffer, index=True)
            zf.writestr(f"results/{name}.parquet", buffer.getvalue())
        elif is_array:
            # Save array as pickle
            zf.writestr(f"results/{name}.pkl", pickle.dumps(data))
        else:
            # Default to pickle for other objects
            zf.writestr(f"results/{name}.pkl", pickle.dumps(data))

    @classmethod
    def load_from_zip(cls, filepath: str) -> "Experiment":
        """Load experiment from a zip file."""
        filepath = Path(filepath)

        with zipfile.ZipFile(filepath, "r") as zf:
            # Load metadata
            metadata_yaml = zf.read("metadata.yaml").decode("utf-8")
            metadata = yaml.safe_load(metadata_yaml)

            # Load results
            policy = None
            cost_history = None
            extra = {}
            result_files = [f for f in zf.namelist() if f.startswith("results/")]

            for result_file in result_files:
                name, ext = cls._parse_result_filename(result_file)
                data = cls._load_result_from_zip(zf, result_file, ext)
                
                if name == "policy":
                    policy = data
                elif name == "cost_history":
                    cost_history = data
                else:
                    extra[name] = data

        results = ExperimentResults(policy=policy, cost_history=cost_history, extra=extra)
        
        return cls(
            name=metadata["name"],
            description=metadata["description"],
            parameters=metadata["parameters"],
            generator_config=metadata.get("generator_config", {}),
            results=results,
        )

    @staticmethod
    def _parse_result_filename(filename: str) -> tuple:
        """Extract name and extension from result filename."""
        # Remove 'results/' prefix
        name_with_ext = filename.replace("results/", "")
        # Split name and extension
        if "." in name_with_ext:
            name, ext = name_with_ext.rsplit(".", 1)
            return name, ext
        return name_with_ext, ""

    @staticmethod
    def _load_result_from_zip(zf: zipfile.ZipFile, filename: str, ext: str) -> Any:
        """Load a result from the zip file based on its extension."""
        data = zf.read(filename)

        if ext == "json":
            return json.loads(data.decode("utf-8"))
        elif ext == "parquet":
            import pandas as pd

            return pd.read_parquet(io.BytesIO(data))
        elif ext == "pkl":
            return pickle.loads(data)
        else:
            # Try JSON first, then pickle as fallback
            try:
                return json.loads(data.decode("utf-8"))
            except Exception:
                return pickle.loads(data)

    def __repr__(self) -> str:
        """String representation of the experiment."""
        parts = []
        if self.results.policy is not None:
            parts.append(f"policy ({type(self.results.policy).__name__})")
        if self.results.cost_history is not None:
            parts.append(f"cost_history ({type(self.results.cost_history).__name__})")
        for name, data in self.results.extra.items():
            parts.append(f"{name} ({type(data).__name__})")
        result_summary = ", ".join(parts)
        return f"Experiment(name={self.name!r}, results=[{result_summary}])"