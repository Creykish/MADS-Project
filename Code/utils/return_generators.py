"""
Return generation strategies for retirement portfolio simulation.

Provides different methods for generating asset return scenarios:
- CholeskyBootstrapReturns: Parametric method using mean and covariance
- BlockBootstrapReturns: Non-parametric method preserving time dependencies
"""

import numpy as np
import pandas as pd
from abc import ABC, abstractmethod


class ReturnGenerator(ABC):
    """Base class for return generators."""
    
    @abstractmethod
    def generate(self, n_simulations: int, n_timesteps: int) -> tuple[np.ndarray, np.ndarray]:
        """
        Generate return scenarios.
        
        Returns
        -------
        tuple[np.ndarray, None | np.ndarray]
            - Simulated returns: shape (n_simulations, n_timesteps, n_assets)
            - Inflation factor: shape (n_simulations, n_timesteps)
        """
        pass


class CholeskyBootstrapReturns(ReturnGenerator):
    """Generate returns using Cholesky decomposition of covariance matrix."""
    
    def __init__(self, mean_returns: np.ndarray, cov_matrix: np.ndarray, inflation_idx: int = -1):
        """
        Parameters
        ----------
        mean_returns : np.ndarray
            Expected returns for each asset
        cov_matrix : np.ndarray
            Covariance matrix of returns
        """
        self.mean_returns = mean_returns
        self.cov_matrix = cov_matrix
        self.n_assets = len(mean_returns)
        self.inflation_idx = inflation_idx
    
    def export_config(self) -> dict:
        """Export configuration for reproducibility."""
        return {
            "type": "cholesky",
            "mean_returns": self.mean_returns.tolist(),
            "cov_matrix": self.cov_matrix.tolist(),
        }
    
    def generate(self, n_simulations: int, n_timesteps: int) -> tuple[np.ndarray, np.ndarray]:
        """Generate returns via Cholesky decomposition."""
        rng = np.random.default_rng()
        returns = rng.multivariate_normal(
            self.mean_returns.flatten(),
            self.cov_matrix,
            size=(n_simulations, n_timesteps)
        )

        inflation = returns[:, :, self.inflation_idx]
        # drop inflation from returns
        returns = np.delete(returns, self.inflation_idx, axis=2)
        # cumulative product to get inflation factor
        inflation_factor = np.cumprod(1 + inflation, axis=1)

        return returns, inflation_factor


class BlockBootstrapReturnsLoader(ReturnGenerator):
    """Generate returns using block bootstrap from historical data."""
    
    def __init__(self, path_to_data: str):
        """
        Parameters
        ----------
        path_to_data : str
            Path to historical returns data (CSV or similar)
        """
        self.path_to_data = path_to_data
        self.data = np.load(path_to_data)  # shape (n_scenarios, n_timesteps, n_assets+1)
        self.n_assets = self.data.shape[2] - 1  # assuming last column is inflation
        self.data_n_timesteps = self.data.shape[1]  # number of time steps in historical data
        self.data_n_sims = self.data.shape[0]  # number of historical scenarios available

    def export_config(self) -> dict:
        """Export configuration for reproducibility."""
        return {
            "type": "block_bootstrap",
            "path_to_data": str(self.path_to_data),
            "n_assets": self.n_assets,
            "data_shape": (self.data_n_sims, self.data_n_timesteps, self.n_assets + 1),
        }
    
    def generate(self, n_simulations: int, n_timesteps: int) -> tuple[np.ndarray, np.ndarray]:
        """Generate returns via block bootstrap."""
        if n_timesteps > self.data_n_timesteps:
            raise ValueError("Requested timesteps exceed historical data length.")
        if n_simulations > self.data_n_sims:
            raise ValueError("Requested simulations exceed historical data scenarios.")
        
        # Randomly sample blocks of historical data
        rng = np.random.default_rng()
        indices = rng.choice(self.data_n_sims, size=n_simulations, replace=True)
        sampled_data = self.data[indices, :n_timesteps, :]
        returns = sampled_data[:, :, :-1]  # all but last column
        inflation = sampled_data[:, :, -1]  # last column is inflation
        # cumulative product to get inflation factor
        inflation_factor = np.cumprod(1 + inflation, axis=1)
        return returns, inflation_factor
    

def create_generator_from_config(config: dict) -> ReturnGenerator:
    """
    Factory method to reconstruct a return generator from exported config.
    
    Parameters
    ----------
    config : dict
        Configuration dictionary from export_config()
        
    Returns
    -------
    ReturnGenerator
        Reconstructed generator instance
    """
    gen_type = config.get("type")
    
    if gen_type == "cholesky":
        return CholeskyBootstrapReturns(
            mean_returns=np.array(config["mean_returns"]),
            cov_matrix=np.array(config["cov_matrix"]),
        )
    elif gen_type == "block_bootstrap":
        return BlockBootstrapReturnsLoader(config["path_to_data"])
    else:
        raise ValueError(f"Unknown generator type: {gen_type}")
