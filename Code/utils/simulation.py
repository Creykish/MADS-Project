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
    cumulative_inflation: torch.Tensor,
    allocation_policy: AllocationPolicy,
    spending_policy: SpendingPolicy,
    initial_wealth: float | torch.Tensor,
    policy_settings: torch.Tensor,
    **kwargs
) -> Tuple[torch.Tensor, torch.Tensor]:
    """
    Simulate wealth and consumption trajectories.

    Parameters
    ----------
    returns : torch.Tensor
        Simulated returns, shape (n_sims, n_timesteps, n_assets)
    cumulative_inflation : torch.Tensor
        Cumulative inflation factors, shape (n_sims, n_timesteps)
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
    """
    n_sims = returns.shape[0]
    n_timesteps = returns.shape[1]

    wealth_history = []
    consumption_history = []

    # Initialize
    if isinstance(initial_wealth, torch.Tensor):
        wealth_t = initial_wealth.to(dtype=returns.dtype, device=returns.device)
    else:
        wealth_t = torch.full(
            (n_sims,), initial_wealth, dtype=returns.dtype, device=returns.device
        )
    wealth = torch.zeros(
        (n_sims, n_timesteps + 1), dtype=returns.dtype, device=returns.device
    )
    consumption = torch.zeros(
        (n_sims, n_timesteps), dtype=returns.dtype, device=returns.device
    )
    wealth[:, 0] = wealth_t

    for t in range(n_timesteps):
        # Calculate spending (pass wealth history up to current time)
        wealth_history = wealth[:, :t+1]
        delta_wealth = spending_policy.calculate_wealth_delta(
            wealth_history, t, cumulative_inflation, **kwargs
        )
        consumption_t = spending_policy.calculate_consumption(
            wealth_history, t, cumulative_inflation, **kwargs
        )
        consumption[:, t] = consumption_t

        # Wealth after spending
        wealth_after_spending = wealth_t + delta_wealth

        # Get allocation(s) from policy
        allocations = allocation_policy.get_allocation(
            t=t, wealth=wealth_after_spending, policy_settings=policy_settings, **kwargs
        )  # Shape: (n_sims, n_assets)

        # Apply returns across all assets
        returns_t = returns[:, t, :]  # Shape: (n_sims, n_assets)
        asset_growth = (allocations * (1 + returns_t)).sum(dim=-1)  # Shape: (n_sims,)

        # Update wealth
        next_wealth = wealth_after_spending * asset_growth
        next_wealth = torch.maximum(next_wealth, torch.zeros_like(next_wealth))

        wealth[:, t + 1] = next_wealth
        wealth_t = next_wealth

    return wealth, consumption
