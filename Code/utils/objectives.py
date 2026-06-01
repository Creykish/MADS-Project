"""
Objective and cost functions for portfolio optimization.

Provides various metrics for evaluating and optimizing retirement strategies:
- Utility functions (log consumption utility)
- Risk measures (terminal wealth, shortfall probability)
- Regularization penalties (smoothness)
"""

import torch
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .spending import ConsumptionFloor

class Objective(ABC):
    """Base class for optimization objectives."""
    
    @abstractmethod
    def evaluate(self, wealth: torch.Tensor, consumption: torch.Tensor) -> torch.Tensor:
        """
        Evaluate the objective function.
        
        Parameters
        ----------
        wealth : torch.Tensor
            Wealth trajectories (n_sims, n_timesteps + 1)
        consumption : torch.Tensor
            Consumption trajectories (n_sims, n_timesteps)
        
        Returns
        -------
        torch.Tensor
            Scalar cost to minimize
        """
        pass


class LogConsumptionUtility(Objective):
    """Negative log consumption utility (for maximization)."""
    
    def __init__(self, epsilon: float = 1e-8, scaling: float = 1.0):
        self.epsilon = epsilon
        self.scaling = scaling
    
    def evaluate(self, wealth: torch.Tensor, consumption: torch.Tensor) -> torch.Tensor:
        consumption_safe = torch.maximum(consumption, torch.tensor(self.epsilon, device=consumption.device))
        log_utility = torch.log(consumption_safe) * self.scaling
        return -log_utility.mean()
    

class CRRAUtility(Objective):
    """
    CRRA (Constant Relative Risk Aversion) utility objective.
    
    Utility function: U(C) = (x^(1-γ) - 1) / (1-γ) where x = C / C_floor
    
    Consumption is measured as multiples of the consumption floor, and
    utility is zero when C = C_floor.
    
    Parameters
    ----------
    gamma : float
        Coefficient of relative risk aversion (γ)
        - γ = 1: log utility (use LogConsumptionUtility instead)
        - γ > 1: more risk averse
        - γ < 1: less risk averse
        Typical range: 1-10, literature often uses 2-5
    consumption_floor : ConsumptionFloor
        Minimum consumption level (subsistence). Dynamic floor that varies 
        with time/inflation. Utility is zero when C = C_floor.
    epsilon : float
        Small constant to avoid invalid operations on consumption at/below floor
    scaling : float
        Scaling factor for the utility values
    normalize : bool
        If True and gamma > 1, normalize utility
    
    Notes
    -----
    From Merton (1969): With CRRA utility and lognormal returns, 
    optimal allocation is constant and independent of wealth.
    See: Merton - Lifetime Portfolio Selection under Uncertainty
    
    The consumption floor formulation is common in life-cycle models where
    there is a minimum subsistence level (e.g., from social insurance).
    """
    
    def __init__(self, gamma: float = 2.0, consumption_floor: 'ConsumptionFloor' = None, 
                 epsilon: float = 1e-8, scaling: float = 1.0, normalize: bool = False):
        if gamma < 0:
            raise ValueError(f"gamma must be non-negative, got {gamma}")
        if abs(gamma - 1.0) < 1e-6:
            raise ValueError("gamma = 1 is undefined for CRRA. Use LogConsumptionUtility instead.")
        if consumption_floor is None:
            raise ValueError("consumption_floor (ConsumptionFloor object) is required")
        
        self.gamma = gamma
        self.consumption_floor = consumption_floor
        self.epsilon = epsilon
        self.scaling = scaling
        self.normalize = normalize
    
    def evaluate(self, wealth: torch.Tensor, consumption: torch.Tensor, 
                 cumulative_inflation: torch.Tensor = None) -> torch.Tensor:
        """
        Evaluate negative CRRA utility (for minimization).
        
        Parameters
        ----------
        wealth : torch.Tensor
            Wealth trajectories (n_sims, n_timesteps + 1)
        consumption : torch.Tensor
            Consumption trajectories (n_sims, n_timesteps)
        cumulative_inflation : torch.Tensor, optional
            Cumulative inflation (n_sims, n_timesteps). Required if using dynamic floor.
        
        Returns
        -------
        torch.Tensor
            Scalar cost (negative mean CRRA utility)
        """
        # Calculate floor values (shape: n_sims, n_timesteps)
        if cumulative_inflation is None:
            raise ValueError("cumulative_inflation required for ConsumptionFloor")
        
        floor_values = self.consumption_floor.calculate_tensor(
            wealth=wealth,
            cumulative_inflation=cumulative_inflation
        )
        
        # Ensure consumption is above floor
        consumption_safe = torch.maximum(
            consumption, 
            floor_values + self.epsilon
        )
        
        # Consumption as multiples of floor: x = C / C_floor
        # Shifted CRRA: U(x) = (x^(1-γ) - 1) / (1-γ), where U(1) = 0
        x = consumption_safe / torch.maximum(
            floor_values,
            torch.tensor(self.epsilon, device=consumption.device)
        )
        utility = ((x ** (1 - self.gamma)) - 1.0) / (1 - self.gamma)
        
        if self.normalize and self.gamma > 1:
            utility = utility * (self.gamma - 1)  # Normalize so limit is 1 as consumption → ∞

        utility = utility * self.scaling
        
        return -utility.mean()


class TerminalWealthObjective(Objective):
    """Penalize low terminal wealth outcomes."""
    
    def __init__(self, target_percentile: float = 0.1, penalty_below_target: float = 1.0):
        self.target_percentile = target_percentile
        self.penalty_below_target = penalty_below_target
    
    def evaluate(self, wealth: torch.Tensor, consumption: torch.Tensor) -> torch.Tensor:
        terminal = wealth[:, -1]
        target = torch.quantile(terminal, self.target_percentile)
        shortfall = torch.relu(target - terminal)
        return self.penalty_below_target * shortfall.mean()
    

class SigmoidWealthPenalty(Objective):
    """Penalty for wealth below zero using a sigmoid function."""
    
    def __init__(self, steepness: float = 0.00001):
        self.steepness = steepness
    
    def evaluate(self, wealth: torch.Tensor, consumption: torch.Tensor) -> torch.Tensor:
        penalty = -torch.sum(torch.sigmoid(self.steepness * (wealth)))/wealth.numel()
        return penalty


class CombinedObjective(Objective):
    """Combine multiple objectives with weights."""
    
    def __init__(self, objectives: list[Objective], weights: list[float]):
        assert len(objectives) == len(weights), "Objectives and weights must have the same length"
        self.objectives = objectives
        self.weights = weights
    
    def evaluate(self, wealth: torch.Tensor, consumption: torch.Tensor) -> torch.Tensor:
        total_cost = 0.0
        for obj, weight in zip(self.objectives, self.weights):
            total_cost += weight * obj.evaluate(wealth, consumption)
        return total_cost


def log_consumption_utility(consumption: torch.Tensor, epsilon: float = 1e-8, scaling: float = 1.0) -> torch.Tensor:
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
    log_utility = torch.log(consumption_safe) * scaling
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


def sigmoid_wealth_penalty(
    wealth: torch.Tensor,
    steepness: float = 0.00001
) -> torch.Tensor:
    """
    Penalty for wealth below zero using a sigmoid function.
    """
    penalty = -torch.sum(torch.sigmoid(steepness * (wealth)))/wealth.numel()
    return penalty

