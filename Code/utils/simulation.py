"""
Core simulation engine for wealth trajectory modeling.

Orchestrates return generation, allocation decisions, and spending to simulate
complete retirement wealth and consumption paths.
"""

import torch
from typing import Tuple
from .allocation import AllocationPolicy
from .spending import SpendingPolicy


def simulate_wealth_trajectory(
    returns: torch.Tensor,
    allocation_policy: AllocationPolicy,
    spending_policy: SpendingPolicy,
    initial_wealth: float,
    **kwargs
) -> Tuple[torch.Tensor, torch.Tensor]:
    """
    Simulate wealth and consumption trajectories.
    
    Parameters
    ----------
    returns : torch.Tensor
        Simulated returns, shape (n_sims, n_timesteps, n_assets)
    allocation_policy : AllocationPolicy
        Policy determining allocation across all assets.
        Returns full allocation tensor of shape (n_sims, n_assets) where
        allocations sum to 1.0 across assets for each simulation.
    spending_policy : SpendingPolicy
        Policy determining consumption/spending
    initial_wealth : float
        Starting wealth
    **kwargs
        Additional parameters passed to policies
    
    Returns
    -------
    Tuple[torch.Tensor, torch.Tensor]
        (wealth, consumption)
        wealth: shape (n_sims, n_timesteps + 1)
        consumption: shape (n_sims, n_timesteps)
    
    Examples
    --------
    >>> # 2-asset example (bonds, stocks)
    >>> returns = torch.tensor(return_data)  # shape: (1000, 40, 2)
    >>> allocation = ConstantAllocation(0.6)  # Returns [0.4, 0.6] per sim
    >>> spending = FloorCeilingSpending(rate=0.04, floor_real=30000)
    >>> wealth, consumption = simulate_wealth_trajectory(
    ...     returns, allocation, spending, initial_wealth=500000
    ... )
    >>> 
    >>> # 3-asset example (bonds, stocks, real estate)
    >>> returns_3asset = torch.tensor(return_data_3)  # shape: (1000, 40, 3)
    >>> # Policy returns e.g. [0.3, 0.5, 0.2] per sim
    >>> wealth, consumption = simulate_wealth_trajectory(
    ...     returns_3asset, allocation, spending, initial_wealth=500000
    ... )
    """
    n_sims = returns.shape[0]
    n_timesteps = returns.shape[1]
    
    wealth_history = []
    consumption_history = []
    
    # Initialize
    wealth_t = torch.full(
        (n_sims,), initial_wealth,
        dtype=returns.dtype,
        device=returns.device
    )
    wealth_history.append(wealth_t)
    
    for t in range(n_timesteps):
        # Calculate spending
        delta_wealth = spending_policy.calculate_wealth_delta(
            wealth_t, t, **kwargs
        )
        consumption = spending_policy.calculate_consumption(
            wealth_t, t, **kwargs
        )
        consumption_history.append(consumption)
        
        # Wealth after spending
        wealth_after_spending = wealth_t + delta_wealth
        
        # Get allocation(s) from policy
        allocations = allocation_policy.get_allocation(
            t=t, wealth=wealth_after_spending, **kwargs
        )  # Shape: (n_sims, n_assets)

        # Apply returns across all assets
        returns_t = returns[:, t, :]  # Shape: (n_sims, n_assets)
        asset_growth = (allocations * (1 + returns_t)).sum(dim=-1) # Shape: (n_sims,)
        
        # Update wealth
        next_wealth = wealth_after_spending * asset_growth
        next_wealth = torch.maximum(next_wealth, torch.zeros_like(next_wealth))
        
        wealth_history.append(next_wealth)
        wealth_t = next_wealth
    
    wealth = torch.stack(wealth_history, dim=1)
    consumption = torch.stack(consumption_history, dim=1)
    
    return wealth, consumption
