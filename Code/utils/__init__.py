"""
Modular utilities for retirement portfolio optimization.

A flexible framework for Monte Carlo simulation of retirement portfolios
with pluggable return generators, allocation policies, and spending strategies.

Quick Start
-----------
>>> from utils import (
...     CholeskyBootstrapReturns,
...     TimeBasedPolicy,
...     PensionPlusPercentage,
...     simulate_wealth_trajectory
... )
>>> 
>>> # Set up components
>>> returns_gen = CholeskyBootstrapReturns(yearly_returns, n_sims=10000, n_timesteps=40)
>>> allocation = TimeBasedPolicy(times, stock_allocations)
>>> spending = PensionPlusPercentage(pension_income=27456, withdrawal_rate=0.04)
>>> 
>>> # Run simulation
>>> wealth, consumption, stock_pct = simulate_wealth_trajectory(
...     initial_wealth=500_000,
...     returns_gen=returns_gen,
...     allocation_policy=allocation,
...     spending_policy=spending
... )

Package Structure
-----------------
return_generators : Module for return generation strategies
    - ReturnGenerator (ABC)
    - CholeskyBootstrapReturns
    - BlockBootstrapReturns

allocation : Module for asset allocation policies
    - AllocationPolicy (ABC)
    - ConstantAllocation
    - TimeBasedPolicy
    - ControlMatrixPolicy

spending : Module for spending/consumption policies
    - SpendingPolicy (ABC)
    - PercentageOfWealth
    - FloorCeilingSpending
    - PensionPlusPercentage

simulation : Core simulation orchestration
    - simulate_wealth_trajectory

objectives : Objective functions for optimization
    - log_consumption_utility
    - terminal_wealth_objective
    - smoothness_penalty
    - shortfall_probability
    - bankruptcy_penalty

helpers : Utility functions
    - load_historical_returns
    - sample_without_replacement
    - calculate_statistics
"""

# Return generators
from .return_generators import (
    ReturnGenerator,
    CholeskyBootstrapReturns,
    BlockBootstrapReturns,
)

# Allocation policies
from .allocation import (
    AllocationPolicy,
    ConstantAllocation,
    TimeBasedPolicy,
    ControlMatrixPolicy,
)

# Spending policies
from .spending import (
    SpendingPolicy,
    PercentageOfWealth,
    FloorCeilingSpending,
    PensionPlusPercentage,
)

# Simulation
from .simulation import simulate_wealth_trajectory

# Objectives
from .objectives import (
    Objective,
    LogConsumptionUtility,
    TerminalWealthObjective,
    SigmoidWealthPenalty,
)

# Helpers
from .helpers import (
    load_historical_returns,
    sample_without_replacement,
    calculate_statistics,
)

from .inflation import Inflation, ConstantInflation, VariableInflation
# Package metadata
__version__ = "0.1.0"
__author__ = "Callum Davidson"

# Public API
__all__ = [
    # Return generators
    "ReturnGenerator",
    "CholeskyBootstrapReturns",
    "BlockBootstrapReturns",
    
    # Allocation policies
    "AllocationPolicy",
    "ConstantAllocation",
    "TimeBasedPolicy",
    "ControlMatrixPolicy",
    
    # Spending policies
    "SpendingPolicy",
    "PercentageOfWealth",
    "FloorCeilingSpending",
    "PensionPlusPercentage",
    
    # Simulation
    "simulate_wealth_trajectory",
    
    # Objectives
    "log_consumption_utility",
    "terminal_wealth_objective",
    "smoothness_penalty",
    "shortfall_probability",
    "bankruptcy_penalty",
    
    # Helpers
    "load_historical_returns",
    "sample_without_replacement",
    "calculate_statistics",
]
