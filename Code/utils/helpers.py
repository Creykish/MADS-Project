"""
Helper utilities for data loading and common operations.

Convenience functions for:
- Loading historical return data
- Sampling operations
- Data processing
"""

import torch
import pandas as pd
from typing import Optional, Tuple


def sample_without_replacement(tensor: torch.Tensor, n_samples: int) -> torch.Tensor:
    """
    Sample rows from tensor without replacement.
    
    Efficient batching for stochastic optimization without duplicates.
    
    Parameters
    ----------
    tensor : torch.Tensor
        Input tensor to sample from
    n_samples : int
        Number of samples to draw
    
    Returns
    -------
    torch.Tensor
        Sampled rows
    
    Examples
    --------
    >>> all_returns = torch.randn(10000, 40, 2)
    >>> batch = sample_without_replacement(all_returns, 1000)
    >>> batch.shape
    torch.Size([1000, 40, 2])
    """
    n = tensor.shape[0]
    if n_samples > n:
        raise ValueError(f"Cannot sample {n_samples} from {n} rows")
    indices = torch.randperm(n, device=tensor.device)[:n_samples]
    return tensor[indices]


def load_historical_returns(
    source: str = "sallypy",
    bonds_ticker: str = "BMK0017",
    stocks_ticker: str = "BMK0188",
    csv_path: Optional[str] = None
) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame]:
    """
    Load historical return data from various sources.
    
    Parameters
    ----------
    source : str
        Data source: 'sallypy' or 'csv'
    bonds_ticker : str
        Ticker for bond returns (sallypy only)
    stocks_ticker : str
        Ticker for stock returns (sallypy only)
    csv_path : Optional[str]
        Path to CSV file (required if source='csv')
    
    Returns
    -------
    Tuple[pd.DataFrame, pd.Series, pd.DataFrame]
        (yearly_returns, mean_returns, cov_matrix)
    
    Examples
    --------
    >>> # Load from sallypy
    >>> yearly, mean, cov = load_historical_returns(source="sallypy")
    >>> 
    >>> # Load from CSV
    >>> yearly, mean, cov = load_historical_returns(
    ...     source="csv",
    ...     csv_path="data/returns.csv"
    ... )
    """
    if source == "sallypy":
        try:
            from sallypy.repos import TimeSeriesRepo
            ts_repo = TimeSeriesRepo()
            returns = ts_repo.get_monthly_returns([bonds_ticker, stocks_ticker])
            returns.columns = ["Bonds", "Stocks"]
            returns.dropna(inplace=True)
            yearly_returns = returns.resample("YE").apply(lambda x: (1 + x).prod() - 1)
        except ImportError:
            raise ImportError("sallypy not available. Use csv_path instead.")
    
    elif source == "csv":
        if csv_path is None:
            raise ValueError("csv_path required when source='csv'")
        returns = pd.read_csv(csv_path, index_col=0, parse_dates=True)
        yearly_returns = returns.resample("YE").apply(lambda x: (1 + x).prod() - 1)
    
    else:
        raise ValueError(f"Unknown source: {source}")
    
    mean_returns = yearly_returns.mean()
    cov_matrix = yearly_returns.cov()
    
    return yearly_returns, mean_returns, cov_matrix


def calculate_statistics(
    wealth: torch.Tensor,
    consumption: torch.Tensor
) -> dict:
    """
    Calculate summary statistics from simulation results.
    
    Parameters
    ----------
    wealth : torch.Tensor
        Wealth trajectories (n_sims, n_timesteps + 1)
    consumption : torch.Tensor
        Consumption values (n_sims, n_timesteps)
    
    Returns
    -------
    dict
        Dictionary of statistics
    
    Examples
    --------
    >>> stats = calculate_statistics(wealth, consumption)
    >>> print(f"Mean terminal wealth: ${stats['mean_terminal_wealth']:,.0f}")
    >>> print(f"Bankruptcy rate: {stats['bankruptcy_rate']:.2%}")
    """
    n_sims = wealth.shape[0]
    
    # Convert to numpy for easier stats calculation
    wealth_np = wealth.cpu().numpy() if wealth.is_cuda else wealth.numpy()
    consumption_np = consumption.cpu().numpy() if consumption.is_cuda else consumption.numpy()
    
    stats = {
        # Terminal wealth
        'mean_terminal_wealth': float(wealth_np[:, -1].mean()),
        'median_terminal_wealth': float(pd.Series(wealth_np[:, -1]).median()),
        'terminal_wealth_10th': float(pd.Series(wealth_np[:, -1]).quantile(0.1)),
        'terminal_wealth_90th': float(pd.Series(wealth_np[:, -1]).quantile(0.9)),
        
        # Consumption
        'mean_consumption': float(consumption_np.mean()),
        'median_consumption': float(pd.Series(consumption_np.flatten()).median()),
        
        # Risk metrics
        'bankruptcy_rate': float((wealth_np[:, -1] == 0).sum() / n_sims),
        'wealth_depletion_rate': float((wealth_np[:, -1] < 10000).sum() / n_sims),
    }
    
    return stats
