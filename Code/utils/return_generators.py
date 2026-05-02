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
    def generate(self, n_simulations: int, n_timesteps: int) -> np.ndarray:
        """
        Generate return scenarios.
        
        Returns
        -------
        np.ndarray
            Shape (n_simulations, n_timesteps, n_assets)
        """
        pass


class CholeskyBootstrapReturns(ReturnGenerator):
    """Generate returns using Cholesky decomposition of covariance matrix."""
    
    def __init__(self, mean_returns: pd.Series, cov_matrix: pd.DataFrame):
        """
        Parameters
        ----------
        mean_returns : pd.Series
            Expected returns for each asset
        cov_matrix : pd.DataFrame
            Covariance matrix of returns
        """
        self.mean_returns = mean_returns
        self.cov_matrix = cov_matrix
        self.n_assets = len(mean_returns)
    
    def generate(self, n_simulations: int, n_timesteps: int) -> np.ndarray:
        """Generate returns via Cholesky decomposition."""
        rng = np.random.default_rng()
        returns = rng.multivariate_normal(
            self.mean_returns.values.flatten(),
            self.cov_matrix.values,
            size=(n_simulations, n_timesteps)
        )
        return returns


class BlockBootstrapReturns(ReturnGenerator):
    """Generate returns using block bootstrap of historical data."""
    
    def __init__(self, historical_returns: pd.DataFrame, block_size: int = 12):
        """
        Parameters
        ----------
        historical_returns : pd.DataFrame
            Historical return data
        block_size : int
            Size of blocks to sample (e.g., 12 for 1-year blocks)
        """
        self.historical_returns = historical_returns
        self.block_size = block_size
        self.n_assets = historical_returns.shape[1]
    
    def generate(self, n_simulations: int, n_timesteps: int) -> np.ndarray:
        """Generate returns via block bootstrap."""
        n_blocks_needed = int(np.ceil(n_timesteps / self.block_size))
        historical_data = self.historical_returns.values
        n_historical = len(historical_data)
        
        returns = np.zeros((n_simulations, n_timesteps, self.n_assets))
        
        for sim in range(n_simulations):
            simulated = []
            for _ in range(n_blocks_needed):
                start_idx = np.random.randint(0, n_historical - self.block_size)
                block = historical_data[start_idx:start_idx + self.block_size]
                simulated.append(block)
            
            simulated = np.vstack(simulated)[:n_timesteps]
            returns[sim] = simulated
        
        return returns
