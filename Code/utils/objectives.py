"""
Objective and cost functions for portfolio optimization.

Provides various metrics for evaluating and optimizing retirement strategies:
- Utility functions (log consumption utility)
- Risk measures (terminal wealth, shortfall probability)
- Regularization penalties (smoothness)
"""

import torch


def log_consumption_utility(consumption: torch.Tensor, epsilon: float = 1e-8) -> torch.Tensor:
    """
    Negative log consumption utility (for minimization).
    
    Standard economic utility function with diminishing marginal utility.
    Minimizing the negative is equivalent to maximizing utility.
    
    Parameters
    ----------
    consumption : torch.Tensor
        Consumption values (n_sims, n_timesteps)
    epsilon : float
        Small constant to avoid log(0)
    
    Returns
    -------
    torch.Tensor
        Scalar cost (negative mean log utility)
    
    Examples
    --------
    >>> cost = log_consumption_utility(consumption)
    >>> # Use in optimization to maximize consumption utility
    >>> cost.backward()
    """
    consumption_safe = torch.maximum(consumption, torch.tensor(epsilon, device=consumption.device))
    log_utility = torch.log(consumption_safe)
    return -log_utility.mean()


def terminal_wealth_objective(
    wealth: torch.Tensor,
    target_percentile: float = 0.1,
    penalty_below_target: float = 1.0
) -> torch.Tensor:
    """
    Penalize outcomes with low terminal wealth.
    
    Focuses optimization on worst-case scenarios by penalizing
    simulations that fall below a target percentile.
    
    Parameters
    ----------
    wealth : torch.Tensor
        Wealth trajectories (n_sims, n_timesteps + 1)
    target_percentile : float
        Focus on this percentile (e.g., 0.1 for 10th percentile)
    penalty_below_target : float
        Weight for violations
    
    Returns
    -------
    torch.Tensor
        Scalar penalty
    
    Examples
    --------
    >>> # Penalize 10th percentile being too low
    >>> cost = terminal_wealth_objective(wealth, target_percentile=0.1)
    """
    terminal = wealth[:, -1]
    target = torch.quantile(terminal, target_percentile)
    shortfall = torch.relu(target - terminal)
    return penalty_below_target * shortfall.mean()


def smoothness_penalty(
    parameters: torch.Tensor,
    weight: float = 0.01,
    dimension: str = 'time'
) -> torch.Tensor:
    """
    Penalize rapid changes in allocation parameters.
    
    Encourages smooth allocation paths by penalizing large differences
    between adjacent time steps or wealth levels.
    
    Parameters
    ----------
    parameters : torch.Tensor
        Policy parameters (1D for time-based, 2D for control matrix)
    weight : float
        Penalty weight
    dimension : str
        'time', 'wealth', or 'both'
        - 'time': penalize changes across time dimension
        - 'wealth': penalize changes across wealth dimension
        - 'both': penalize both (only for 2D matrices)
    
    Returns
    -------
    torch.Tensor
        Scalar penalty
    
    Examples
    --------
    >>> # For time-based policy nodes
    >>> penalty = smoothness_penalty(policy_nodes, weight=0.01)
    >>> 
    >>> # For 2D control matrix, penalize both dimensions
    >>> penalty = smoothness_penalty(control_matrix, weight=0.001, dimension='both')
    """
    if parameters.ndim == 1:
        # 1D case (time-based policy)
        differences = parameters[1:] - parameters[:-1]
        return weight * (differences ** 2).sum()
    
    elif parameters.ndim == 2:
        # 2D case (control matrix)
        penalty = 0.0
        if dimension in ['time', 'both']:
            time_diff = parameters[1:, :] - parameters[:-1, :]
            penalty += weight * (time_diff ** 2).sum()
        if dimension in ['wealth', 'both']:
            wealth_diff = parameters[:, 1:] - parameters[:, :-1]
            penalty += weight * (wealth_diff ** 2).sum()
        return penalty
    
    else:
        raise ValueError(f"Unsupported parameter dimensionality: {parameters.ndim}")


def shortfall_probability(
    consumption: torch.Tensor,
    threshold: float,
    penalty_weight: float = 1.0
) -> torch.Tensor:
    """
    Penalize probability of consumption falling below threshold.
    
    Parameters
    ----------
    consumption : torch.Tensor
        Consumption values (n_sims, n_timesteps)
    threshold : float
        Minimum acceptable consumption
    penalty_weight : float
        Weight for penalty
    
    Returns
    -------
    torch.Tensor
        Scalar penalty
    """
    shortfalls = (consumption < threshold).float()
    prob = shortfalls.mean()
    return penalty_weight * prob


def bankruptcy_penalty(
    wealth: torch.Tensor,
    penalty_weight: float = 100.0
) -> torch.Tensor:
    """
    Heavily penalize bankruptcy (wealth reaching zero).
    
    Parameters
    ----------
    wealth : torch.Tensor
        Wealth trajectories (n_sims, n_timesteps + 1)
    penalty_weight : float
        Weight for bankruptcy penalty
    
    Returns
    -------
    torch.Tensor
        Scalar penalty
    """
    bankruptcies = (wealth[:, -1] == 0).float()
    bankruptcy_rate = bankruptcies.mean()
    return penalty_weight * bankruptcy_rate
