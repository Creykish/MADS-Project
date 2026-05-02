"""
Utility module for retirement portfolio optimization.

Provides modular components for:
- Asset return generation (bootstrap, parametric, etc.)
- Allocation policies (age-based, wealth-based, 2D control matrix)
- Spending/income policies (fixed, percentage, floor+ceiling, pension)
- Simulation engines
"""

import numpy as np
import pandas as pd
import torch
from typing import Callable, Optional, Tuple
from abc import ABC, abstractmethod


# ============================================================================
# RETURN GENERATORS
# ============================================================================

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


# ============================================================================
# ALLOCATION POLICIES
# ============================================================================

class AllocationPolicy(ABC):
    """Base class for allocation policies."""
    
    @abstractmethod
    def get_allocation(
        self,
        time_idx: torch.Tensor,
        wealth: torch.Tensor,
        **kwargs
    ) -> torch.Tensor:
        """
        Get allocation to risky assets.
        
        Parameters
        ----------
        time_idx : torch.Tensor
            Current time indices
        wealth : torch.Tensor
            Current wealth levels
        
        Returns
        -------
        torch.Tensor
            Allocation to risky asset(s) for each simulation
        """
        pass


class ConstantAllocation(AllocationPolicy):
    """Constant allocation regardless of time or wealth."""
    
    def __init__(self, allocation: float):
        """
        Parameters
        ----------
        allocation : float
            Fixed allocation to risky assets (0-1)
        """
        self.allocation = allocation
    
    def get_allocation(self, time_idx: torch.Tensor, wealth: torch.Tensor, **kwargs) -> torch.Tensor:
        return torch.full_like(wealth, self.allocation)


class TimeBasedPolicy(AllocationPolicy):
    """Time/age-based allocation with linear interpolation between nodes."""
    
    def __init__(self, policy_nodes: torch.Tensor, n_timesteps: int):
        """
        Parameters
        ----------
        policy_nodes : torch.Tensor
            Allocation values at key time points
        n_timesteps : int
            Total number of timesteps
        """
        self.policy_nodes = policy_nodes
        self.n_timesteps = n_timesteps
        self.n_nodes = len(policy_nodes)
    
    def get_allocation(self, time_idx: torch.Tensor, wealth: torch.Tensor, **kwargs) -> torch.Tensor:
        """Linear interpolation between policy nodes."""
        # Node positions evenly spaced across timeline
        node_positions = torch.linspace(
            0, self.n_timesteps - 1, self.n_nodes,
            device=self.policy_nodes.device
        )
        
        result = torch.zeros_like(time_idx)
        
        for i, t in enumerate(time_idx):
            right_idx = torch.searchsorted(node_positions, t, right=True)
            
            if right_idx == 0:
                result[i] = self.policy_nodes[0]
            elif right_idx >= self.n_nodes:
                result[i] = self.policy_nodes[-1]
            else:
                left_idx = right_idx - 1
                left_pos = node_positions[left_idx]
                right_pos = node_positions[right_idx]
                weight = (t - left_pos) / (right_pos - left_pos)
                result[i] = (1 - weight) * self.policy_nodes[left_idx] + weight * self.policy_nodes[right_idx]
        
        return result


class ControlMatrixPolicy(AllocationPolicy):
    """2D control matrix policy (time × wealth) with bilinear interpolation."""
    
    def __init__(
        self,
        control_matrix: torch.Tensor,
        n_timesteps: int,
        max_wealth: float
    ):
        """
        Parameters
        ----------
        control_matrix : torch.Tensor
            Shape (n_time_nodes, n_wealth_nodes)
        n_timesteps : int
            Total number of timesteps in simulation
        max_wealth : float
            Maximum wealth bound for interpolation
        """
        self.control_matrix = control_matrix
        self.n_timesteps = n_timesteps
        self.max_wealth = max_wealth
        self.n_time_nodes, self.n_wealth_nodes = control_matrix.shape
    
    def get_allocation(self, time_idx: torch.Tensor, wealth: torch.Tensor, **kwargs) -> torch.Tensor:
        """Bilinear interpolation over time and wealth dimensions."""
        # Map to grid coordinates
        time_grid_coord = time_idx * (self.n_time_nodes - 1) / (self.n_timesteps - 1)
        wealth_grid_coord = wealth * (self.n_wealth_nodes - 1) / self.max_wealth
        
        # Clamp to valid range
        time_grid_coord = torch.clamp(time_grid_coord, 0, self.n_time_nodes - 1)
        wealth_grid_coord = torch.clamp(wealth_grid_coord, 0, self.n_wealth_nodes - 1)
        
        # Get floor and ceiling indices
        t0 = torch.floor(time_grid_coord).long()
        t1 = torch.clamp(t0 + 1, max=self.n_time_nodes - 1)
        w0 = torch.floor(wealth_grid_coord).long()
        w1 = torch.clamp(w0 + 1, max=self.n_wealth_nodes - 1)
        
        # Fractional parts for interpolation
        t_frac = time_grid_coord - t0.float()
        w_frac = wealth_grid_coord - w0.float()
        
        # Get corner values
        Q00 = self.control_matrix[t0, w0]
        Q01 = self.control_matrix[t0, w1]
        Q10 = self.control_matrix[t1, w0]
        Q11 = self.control_matrix[t1, w1]
        
        # Bilinear interpolation
        result = (
            Q00 * (1 - t_frac) * (1 - w_frac) +
            Q01 * (1 - t_frac) * w_frac +
            Q10 * t_frac * (1 - w_frac) +
            Q11 * t_frac * w_frac
        )
        
        return result


# ============================================================================
# SPENDING/INCOME POLICIES
# ============================================================================

class SpendingPolicy(ABC):
    """Base class for spending policies."""
    
    @abstractmethod
    def calculate_spending(
        self,
        wealth: torch.Tensor,
        time_step: int,
        **kwargs
    ) -> torch.Tensor:
        """
        Calculate spending for current period.
        
        Parameters
        ----------
        wealth : torch.Tensor
            Current wealth
        time_step : int
            Current time step
        
        Returns
        -------
        torch.Tensor
            Spending amount
        """
        pass


class PercentageOfWealth(SpendingPolicy):
    """Spend a fixed percentage of current wealth."""
    
    def __init__(self, rate: float):
        """
        Parameters
        ----------
        rate : float
            Percentage to spend (e.g., 0.04 for 4%)
        """
        self.rate = rate
    
    def calculate_spending(self, wealth: torch.Tensor, time_step: int, **kwargs) -> torch.Tensor:
        spending = wealth * self.rate
        return torch.minimum(spending, wealth)  # Can't spend more than you have


class FloorCeilingSpending(SpendingPolicy):
    """Spend percentage of wealth with a floor and optional ceiling."""
    
    def __init__(
        self,
        rate: float,
        floor_real: float,
        inflation: float = 0.03,
        real_decline_rate: float = 0.0,
        ceiling_real: Optional[float] = None
    ):
        """
        Parameters
        ----------
        rate : float
            Target spending rate as % of wealth
        floor_real : float
            Minimum spending in real terms (year 0)
        inflation : float
            Annual inflation rate
        real_decline_rate : float
            Annual decline in real spending needs
        ceiling_real : Optional[float]
            Maximum spending in real terms (year 0)
        """
        self.rate = rate
        self.floor_real = floor_real
        self.inflation = inflation
        self.real_decline_rate = real_decline_rate
        self.ceiling_real = ceiling_real
    
    def calculate_spending(self, wealth: torch.Tensor, time_step: int, **kwargs) -> torch.Tensor:
        # Adjust floor for real decline and inflation
        real_floor = self.floor_real * ((1 - self.real_decline_rate) ** time_step)
        nominal_floor = real_floor * ((1 + self.inflation) ** time_step)
        
        # Percentage-based spending
        percentage_spending = wealth * self.rate
        
        # Apply floor
        spending = torch.maximum(
            torch.full_like(wealth, nominal_floor),
            percentage_spending
        )
        
        # Apply ceiling if specified
        if self.ceiling_real is not None:
            real_ceiling = self.ceiling_real * ((1 - self.real_decline_rate) ** time_step)
            nominal_ceiling = real_ceiling * ((1 + self.inflation) ** time_step)
            spending = torch.minimum(spending, torch.full_like(wealth, nominal_ceiling))
        
        # Can't spend more than available
        spending = torch.minimum(spending, wealth)
        
        return spending


class PensionPlusPercentage(SpendingPolicy):
    """Fixed pension income plus percentage of wealth spending."""
    
    def __init__(
        self,
        pension_real: float,
        wealth_rate: float = 0.0,
        inflation: float = 0.03,
        pension_start_age: int = 65,
        current_age_at_t0: int = 65
    ):
        """
        Parameters
        ----------
        pension_real : float
            Annual pension income in real terms
        wealth_rate : float
            Additional spending as % of wealth
        inflation : float
            Annual inflation rate
        pension_start_age : int
            Age when pension starts
        current_age_at_t0 : int
            Age at time step 0
        """
        self.pension_real = pension_real
        self.wealth_rate = wealth_rate
        self.inflation = inflation
        self.pension_start_age = pension_start_age
        self.current_age_at_t0 = current_age_at_t0
    
    def calculate_spending(self, wealth: torch.Tensor, time_step: int, **kwargs) -> torch.Tensor:
        current_age = self.current_age_at_t0 + time_step
        
        # Pension component (inflation-adjusted)
        if current_age >= self.pension_start_age:
            pension = self.pension_real * ((1 + self.inflation) ** time_step)
        else:
            pension = 0.0
        
        # Wealth-based component
        wealth_spending = wealth * self.wealth_rate
        
        # Total spending
        spending = wealth_spending + pension
        
        # Can't spend more than wealth + pension
        spending = torch.minimum(spending, wealth + pension)
        
        return spending


# ============================================================================
# SIMULATION ENGINE
# ============================================================================

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
        For 2 assets: [:, :, 0] = bonds, [:, :, 1] = stocks
    allocation_policy : AllocationPolicy
        Policy determining allocation to risky assets
    spending_policy : SpendingPolicy
        Policy determining consumption/spending
    initial_wealth : float
        Starting wealth
    
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
    wealth_t = torch.full(
        (n_sims,), initial_wealth,
        dtype=returns.dtype,
        device=returns.device
    )
    wealth_history.append(wealth_t)
    
    for t in range(n_timesteps):
        # Calculate spending
        spending_t = spending_policy.calculate_spending(
            wealth_t, t, **kwargs
        )
        consumption_history.append(spending_t)
        
        # Wealth after spending
        wealth_after_spending = wealth_t - spending_t
        
        # Get allocation
        time_indices = torch.full_like(wealth_after_spending, float(t))
        risky_allocation = allocation_policy.get_allocation(
            time_indices, wealth_after_spending, **kwargs
        )
        safe_allocation = 1 - risky_allocation
        
        # Apply returns (assuming 2 assets: safe and risky)
        safe_return = returns[:, t, 0]
        risky_return = returns[:, t, 1]
        
        portfolio_return = (
            safe_allocation * (1 + safe_return) +
            risky_allocation * (1 + risky_return)
        )
        
        # Update wealth
        next_wealth = wealth_after_spending * portfolio_return
        next_wealth = torch.maximum(next_wealth, torch.zeros_like(next_wealth))
        
        wealth_history.append(next_wealth)
        wealth_t = next_wealth
    
    wealth = torch.stack(wealth_history, dim=1)
    consumption = torch.stack(consumption_history, dim=1)
    
    return wealth, consumption


# ============================================================================
# COST/OBJECTIVE FUNCTIONS
# ============================================================================

def log_consumption_utility(consumption: torch.Tensor, epsilon: float = 1e-8) -> torch.Tensor:
    """
    Negative log consumption utility (for minimization).
    
    Standard economic utility function with diminishing marginal utility.
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
    
    Parameters
    ----------
    wealth : torch.Tensor
        Wealth trajectories
    target_percentile : float
        Focus on this percentile (e.g., 0.1 for 10th percentile)
    penalty_below_target : float
        Weight for violations
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
    
    Parameters
    ----------
    parameters : torch.Tensor
        Policy parameters (1D for time-based, 2D for control matrix)
    weight : float
        Penalty weight
    dimension : str
        'time', 'wealth', or 'both'
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


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def sample_without_replacement(tensor: torch.Tensor, n_samples: int) -> torch.Tensor:
    """Sample rows from tensor without replacement."""
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
    Load historical return data.
    
    Returns
    -------
    Tuple[pd.DataFrame, pd.Series, pd.DataFrame]
        (yearly_returns, mean_returns, cov_matrix)
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
