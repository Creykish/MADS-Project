# Utils Module Documentation

A modular framework for retirement portfolio simulation and optimization.

## Overview

The `utils.py` module provides reusable components that can be mixed and matched to test different retirement strategies. All components follow a consistent interface pattern making it easy to swap implementations.

## Architecture

```
┌─────────────────────┐
│  Return Generator   │  → Generates market return scenarios
└─────────────────────┘
         ↓
┌─────────────────────┐
│ Allocation Policy   │  → Determines portfolio allocation
└─────────────────────┘
         ↓
┌─────────────────────┐
│  Spending Policy    │  → Calculates consumption/spending
└─────────────────────┘
         ↓
┌─────────────────────┐
│ Simulation Engine   │  → Runs monte carlo simulation
└─────────────────────┘
         ↓
┌─────────────────────┐
│ Objective Functions │  → Evaluates outcomes
└─────────────────────┘
```

## Quick Start

```python
from utils import (
    CholeskyBootstrapReturns,
    TimeBasedPolicy,
    FloorCeilingSpending,
    simulate_wealth_trajectory
)

# 1. Generate returns
return_gen = CholeskyBootstrapReturns(mean_returns, cov_matrix)
returns = return_gen.generate(n_simulations=1000, n_timesteps=40)

# 2. Define allocation policy
allocation = TimeBasedPolicy(
    policy_nodes=torch.tensor([0.9, 0.6, 0.3]),
    n_timesteps=40
)

# 3. Define spending policy
spending = FloorCeilingSpending(
    rate=0.04,
    floor_real=30000,
    inflation=0.03
)

# 4. Run simulation
wealth, consumption = simulate_wealth_trajectory(
    returns=torch.tensor(returns),
    allocation_policy=allocation,
    spending_policy=spending,
    initial_wealth=500000
)
```

## Components

### 1. Return Generators

Generate market return scenarios using different methodologies.

#### CholeskyBootstrapReturns (Parametric)
Uses mean and covariance matrix. Assumes multivariate normal distribution.

```python
gen = CholeskyBootstrapReturns(mean_returns, cov_matrix)
returns = gen.generate(n_simulations=10000, n_timesteps=40)
```

#### BlockBootstrapReturns (Non-Parametric)
Samples blocks of historical returns. Preserves time dependencies and fat tails.

```python
gen = BlockBootstrapReturns(historical_returns, block_size=12)
returns = gen.generate(n_simulations=10000, n_timesteps=40)
```

**When to use which:**
- Cholesky: Fast, smooth distributions, assumes normality
- Block Bootstrap: Preserves historical return patterns, better for regime changes

---

### 2. Allocation Policies

Determine portfolio allocation to risky assets based on time and/or wealth.

#### ConstantAllocation
Fixed allocation regardless of conditions.

```python
policy = ConstantAllocation(0.6)  # 60% stocks
```

#### TimeBasedPolicy
Age-based allocation with linear interpolation between nodes.

```python
policy = TimeBasedPolicy(
    policy_nodes=torch.tensor([0.9, 0.7, 0.5, 0.3]),
    n_timesteps=40
)
```

Perfect for optimizing glide paths with just a few parameters.

#### ControlMatrixPolicy
2D control surface: allocation varies by both time AND wealth.

```python
# Create 10×15 control matrix
control_matrix = torch.rand(10, 15)  # (time_nodes, wealth_nodes)

policy = ControlMatrixPolicy(
    control_matrix=control_matrix,
    n_timesteps=40,
    max_wealth=1500000
)
```

Provides maximum flexibility but requires more parameters to optimize.

---

### 3. Spending Policies

Determine consumption/spending each period.

#### PercentageOfWealth
Simple percentage rule (e.g., 4% rule).

```python
spending = PercentageOfWealth(rate=0.04)
```

#### FloorCeilingSpending
Percentage of wealth with a minimum floor (and optional ceiling).

```python
spending = FloorCeilingSpending(
    rate=0.04,              # Target spending rate
    floor_real=30000,       # Minimum in today's dollars
    inflation=0.03,         # Inflation adjustment
    real_decline_rate=0.02, # Declining needs (e.g., 2%/year)
    ceiling_real=80000      # Optional maximum
)
```

This models realistic consumption needs with a safety floor.

#### PensionPlusPercentage
Fixed pension income plus variable wealth-based spending.

```python
spending = PensionPlusPercentage(
    pension_real=27456,     # NZ Super ~$27k/year (2024)
    wealth_rate=0.02,       # Additional 2% of wealth
    inflation=0.03,
    pension_start_age=65,
    current_age_at_t0=65
)
```

Perfect for modeling New Zealand retirement with NZ Superannuation.

---

### 4. Simulation Engine

`simulate_wealth_trajectory()` orchestrates all components:

```python
wealth, consumption = simulate_wealth_trajectory(
    returns=returns_tensor,          # (n_sims, n_timesteps, n_assets)
    allocation_policy=allocation,     # AllocationPolicy instance
    spending_policy=spending,         # SpendingPolicy instance
    initial_wealth=500000
)

# Returns:
# wealth:      (n_sims, n_timesteps + 1)
# consumption: (n_sims, n_timesteps)
```

---

### 5. Objective Functions

For optimization.

#### log_consumption_utility
Standard economic utility function with diminishing marginal utility.

```python
cost = log_consumption_utility(consumption)
# Minimize this (equivalent to maximizing utility)
```

#### smoothness_penalty
Penalizes rapid changes in allocation parameters.

```python
penalty = smoothness_penalty(
    policy_nodes,
    weight=0.01,
    dimension='time'  # or 'wealth' or 'both' for 2D
)
```

#### terminal_wealth_objective
Focus on worst-case outcomes.

```python
cost = terminal_wealth_objective(
    wealth,
    target_percentile=0.1,  # Focus on 10th percentile
    penalty_below_target=1.0
)
```

---

## Optimization Example

```python
# Initialize policy parameters
policy_nodes = torch.tensor([0.9, 0.7, 0.5], requires_grad=True)

# Setup
optimizer = torch.optim.Adam([policy_nodes], lr=0.01)
allocation_policy = TimeBasedPolicy(policy_nodes, n_timesteps=40)
spending_policy = FloorCeilingSpending(...)

# Training loop
for iteration in range(1000):
    optimizer.zero_grad()
    
    # Simulate
    wealth, consumption = simulate_wealth_trajectory(
        returns=sample_batch,
        allocation_policy=TimeBasedPolicy(policy_nodes, 40),
        spending_policy=spending_policy,
        initial_wealth=500000
    )
    
    # Calculate objective
    cost = log_consumption_utility(consumption)
    cost += smoothness_penalty(policy_nodes, weight=0.01)
    
    # Optimize
    cost.backward()
    optimizer.step()
    
    with torch.no_grad():
        policy_nodes.clamp_(0.0, 1.0)
```

---

## Extending the Framework

### Adding a New Return Generator

```python
class YourReturnGenerator(ReturnGenerator):
    def __init__(self, ...):
        # Your parameters
        pass
    
    def generate(self, n_simulations: int, n_timesteps: int) -> np.ndarray:
        # Return shape: (n_simulations, n_timesteps, n_assets)
        return your_returns
```

### Adding a New Allocation Policy

```python
class YourPolicy(AllocationPolicy):
    def get_allocation(
        self,
        time_idx: torch.Tensor,
        wealth: torch.Tensor,
        **kwargs
    ) -> torch.Tensor:
        # Return allocation for each simulation
        return allocations  # Same shape as wealth
```

### Adding a New Spending Policy

```python
class YourSpendingPolicy(SpendingPolicy):
    def calculate_spending(
        self,
        wealth: torch.Tensor,
        time_step: int,
        **kwargs
    ) -> torch.Tensor:
        # Return spending for this period
        return spending  # Same shape as wealth
```

---

## Helper Functions

### load_historical_returns
Load and process return data.

```python
# From sallypy
yearly_returns, mean, cov = load_historical_returns(source="sallypy")

# From CSV
yearly_returns, mean, cov = load_historical_returns(
    source="csv",
    csv_path="path/to/returns.csv"
)
```

### sample_without_replacement
Efficiently sample rows from tensor.

```python
batch = sample_without_replacement(all_returns, n_samples=1000)
```

---

## Examples

See `example_using_utils.ipynb` for comprehensive examples including:
- Comparing return generation methods
- Testing different allocation policies
- Evaluating spending strategies
- Optimization workflow

---

## Design Principles

1. **Modularity**: Each component is independent and swappable
2. **Composability**: Components work seamlessly together
3. **Extensibility**: Easy to add new implementations
4. **Type Safety**: Clear interfaces via abstract base classes
5. **PyTorch Integration**: Automatic differentiation for optimization

---

## Contributing

When adding new components:

1. Inherit from appropriate base class
2. Implement all abstract methods
3. Match expected input/output shapes
4. Document parameters and behavior
5. Add example usage
