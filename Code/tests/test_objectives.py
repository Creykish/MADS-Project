"""
Unit tests for objectives module.

Tests cover:
- CRRA utility with dynamic consumption floors
- Wealth penalties
- Combined objectives
"""

import pytest
import torch
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.objectives import (
    CRRAUtility,
    LogConsumptionUtility,
    SigmoidWealthPenalty,
    TerminalWealthObjective,
    CombinedObjective,
)
from utils.spending import (
    FixedRealFloor,
    DecliningRealFloor,
    NoConsumptionFloor,
)


# ==================== Test Fixtures ====================


@pytest.fixture
def wealth_trajectories():
    """Sample wealth trajectories: 100 sims, 10 time steps."""
    torch.manual_seed(42)
    n_sims = 100
    n_timesteps = 10
    
    # Create realistic declining wealth paths
    initial_wealth = 500_000
    wealth = torch.zeros((n_sims, n_timesteps + 1))
    wealth[:, 0] = initial_wealth
    
    for t in range(n_timesteps):
        # Simulate returns and withdrawals
        returns = torch.randn(n_sims) * 0.1 + 0.05  # 5% mean, 10% std
        withdrawals = 20_000 * (1.02 ** t)  # 2% inflation
        wealth[:, t+1] = torch.maximum(
            (wealth[:, t] - withdrawals) * (1 + returns),
            torch.zeros(n_sims)
        )
    
    return wealth


@pytest.fixture
def consumption_trajectories():
    """Sample consumption trajectories: 100 sims, 10 time steps."""
    torch.manual_seed(42)
    n_sims = 100
    n_timesteps = 10
    
    # Create realistic consumption paths
    base_consumption = 40_000
    consumption = torch.zeros((n_sims, n_timesteps))
    
    for t in range(n_timesteps):
        # Consumption with some variation and inflation
        noise = torch.randn(n_sims) * 5_000
        inflation = 1.02 ** t
        consumption[:, t] = torch.maximum(
            (base_consumption + noise) * inflation,
            torch.tensor(10_000.0)  # Floor
        )
    
    return consumption


@pytest.fixture
def cumulative_inflation():
    """Sample cumulative inflation: 2% per year."""
    n_sims = 100
    n_timesteps = 10
    inflation_per_year = 1.02
    
    time_steps = torch.arange(n_timesteps, dtype=torch.float32)
    inflation = inflation_per_year ** time_steps
    
    return inflation.unsqueeze(0).expand(n_sims, -1)


# ==================== Test CRRA Utility ====================


class TestCRRAUtility:
    """Test CRRA utility with dynamic consumption floors."""
    
    def test_crra_requires_floor(self):
        """Test that CRRAUtility requires a ConsumptionFloor object."""
        with pytest.raises(ValueError, match="consumption_floor.*required"):
            CRRAUtility(gamma=2.0, consumption_floor=None)
    
    def test_crra_with_fixed_floor(self, wealth_trajectories, consumption_trajectories, cumulative_inflation):
        """Test CRRA utility with FixedRealFloor."""
        floor = FixedRealFloor(init_floor=30_000)
        crra = CRRAUtility(gamma=3.0, consumption_floor=floor)
        
        cost = crra.evaluate(
            wealth_trajectories, 
            consumption_trajectories, 
            cumulative_inflation=cumulative_inflation
        )
        
        # Cost should be a scalar
        assert cost.shape == ()
        # Should be finite (not NaN or inf)
        assert torch.isfinite(cost)
        # Cost can be negative (when consumption > floor gives positive utility)
    
    def test_crra_with_declining_floor(self, wealth_trajectories, consumption_trajectories, cumulative_inflation):
        """Test CRRA utility with DecliningRealFloor."""
        floor = DecliningRealFloor(init_floor=40_000, decline_rate=0.02)
        crra = CRRAUtility(gamma=2.5, consumption_floor=floor)
        
        cost = crra.evaluate(
            wealth_trajectories, 
            consumption_trajectories, 
            cumulative_inflation=cumulative_inflation
        )
        
        assert cost.shape == ()
        assert torch.isfinite(cost)
    
    def test_crra_requires_cumulative_inflation(self, wealth_trajectories, consumption_trajectories):
        """Test that CRRA utility requires cumulative_inflation parameter."""
        floor = FixedRealFloor(init_floor=30_000)
        crra = CRRAUtility(gamma=2.0, consumption_floor=floor)
        
        with pytest.raises(ValueError, match="cumulative_inflation required"):
            crra.evaluate(wealth_trajectories, consumption_trajectories)
    
    def test_crra_gamma_validation(self):
        """Test that CRRA validates gamma parameter."""
        floor = FixedRealFloor(init_floor=30_000)
        
        # gamma = 1 should raise error
        with pytest.raises(ValueError, match="gamma = 1 is undefined"):
            CRRAUtility(gamma=1.0, consumption_floor=floor)
        
        # Negative gamma should raise error
        with pytest.raises(ValueError, match="gamma must be non-negative"):
            CRRAUtility(gamma=-1.0, consumption_floor=floor)
    
    def test_crra_normalization(self, wealth_trajectories, consumption_trajectories, cumulative_inflation):
        """Test CRRA normalization option."""
        floor = FixedRealFloor(init_floor=30_000)
        
        crra_unnormalized = CRRAUtility(gamma=3.0, consumption_floor=floor, normalize=False)
        crra_normalized = CRRAUtility(gamma=3.0, consumption_floor=floor, normalize=True)
        
        cost_unnorm = crra_unnormalized.evaluate(
            wealth_trajectories, consumption_trajectories, cumulative_inflation
        )
        cost_norm = crra_normalized.evaluate(
            wealth_trajectories, consumption_trajectories, cumulative_inflation
        )
        
        # Both should be finite
        assert torch.isfinite(cost_unnorm)
        assert torch.isfinite(cost_norm)
        # Normalization should change the value
        assert not torch.isclose(cost_unnorm, cost_norm)
    
    def test_crra_higher_consumption_lower_cost(self, wealth_trajectories, cumulative_inflation):
        """Test that higher consumption leads to lower cost (higher utility)."""
        floor = FixedRealFloor(init_floor=30_000)
        crra = CRRAUtility(gamma=2.0, consumption_floor=floor)
        
        # Low consumption
        low_consumption = torch.ones((100, 10)) * 35_000 * torch.linspace(1.0, 1.2, 10)
        cost_low = crra.evaluate(wealth_trajectories, low_consumption, cumulative_inflation)
        
        # High consumption
        high_consumption = torch.ones((100, 10)) * 50_000 * torch.linspace(1.0, 1.2, 10)
        cost_high = crra.evaluate(wealth_trajectories, high_consumption, cumulative_inflation)
        
        # Higher consumption should have lower cost (higher utility)
        assert cost_high < cost_low
    
    def test_crra_floor_effect(self, wealth_trajectories, cumulative_inflation):
        """Test that higher floor leads to lower utility (higher cost)."""
        # Create consumption that would be above both floors
        good_consumption = torch.ones((100, 10)) * 50_000
        
        floor_low = FixedRealFloor(init_floor=30_000)
        floor_high = FixedRealFloor(init_floor=40_000)
        
        crra_low = CRRAUtility(gamma=2.0, consumption_floor=floor_low)
        crra_high = CRRAUtility(gamma=2.0, consumption_floor=floor_high)
        
        cost_low_floor = crra_low.evaluate(wealth_trajectories, good_consumption, cumulative_inflation)
        cost_high_floor = crra_high.evaluate(wealth_trajectories, good_consumption, cumulative_inflation)
        
        # With same consumption, higher floor means lower ratio x = C/floor,
        # which means lower utility and higher cost
        assert cost_high_floor > cost_low_floor


# ==================== Test Other Objectives ====================


class TestOtherObjectives:
    """Test other objective functions."""
    
    def test_log_consumption_utility(self, wealth_trajectories, consumption_trajectories):
        """Test LogConsumptionUtility."""
        log_util = LogConsumptionUtility(epsilon=1e-8, scaling=1.0)
        cost = log_util.evaluate(wealth_trajectories, consumption_trajectories)
        
        assert cost.shape == ()
        assert torch.isfinite(cost)
        # Negative log utility for minimization
        assert cost < 0  # Since we're taking negative of positive log values
    
    def test_sigmoid_wealth_penalty(self, wealth_trajectories, consumption_trajectories):
        """Test SigmoidWealthPenalty."""
        penalty = SigmoidWealthPenalty(steepness=1e-4)
        cost = penalty.evaluate(wealth_trajectories, consumption_trajectories)
        
        assert cost.shape == ()
        assert torch.isfinite(cost)
        # Penalty should be negative (sigmoid returns values in [0, 1])
        assert cost < 0
    
    def test_terminal_wealth_objective(self, wealth_trajectories, consumption_trajectories):
        """Test TerminalWealthObjective."""
        terminal_obj = TerminalWealthObjective(target_percentile=0.1, penalty_below_target=1.0)
        cost = terminal_obj.evaluate(wealth_trajectories, consumption_trajectories)
        
        assert cost.shape == ()
        assert torch.isfinite(cost)
        assert cost >= 0  # Penalty should be non-negative
    
    def test_combined_objective(self, wealth_trajectories, consumption_trajectories, cumulative_inflation):
        """Test CombinedObjective with multiple objectives."""
        floor = FixedRealFloor(init_floor=30_000)
        crra = CRRAUtility(gamma=2.0, consumption_floor=floor)
        
        # Note: CombinedObjective doesn't pass cumulative_inflation through
        # This is a limitation we might want to fix
        penalty = SigmoidWealthPenalty(steepness=1e-4)
        terminal = TerminalWealthObjective(target_percentile=0.1)
        
        combined = CombinedObjective(
            objectives=[penalty, terminal],
            weights=[1.0, 0.5]
        )
        
        cost = combined.evaluate(wealth_trajectories, consumption_trajectories)
        
        assert cost.shape == ()
        assert torch.isfinite(cost)


# ==================== Test Gradient Flow ====================


class TestGradientFlow:
    """Test that gradients flow correctly through objectives."""
    
    def test_crra_gradient_flow(self, wealth_trajectories, cumulative_inflation):
        """Test that gradients flow through CRRA utility."""
        floor = FixedRealFloor(init_floor=30_000)
        crra = CRRAUtility(gamma=2.0, consumption_floor=floor, normalize=True)
        
        # Create consumption as a leaf tensor with requires_grad
        consumption = torch.ones((100, 10), requires_grad=True)
        consumption.data.fill_(40_000)
        
        cost = crra.evaluate(wealth_trajectories, consumption, cumulative_inflation)
        
        # Backward pass
        cost.backward()
        
        # Gradients should exist and be finite
        assert consumption.grad is not None
        assert torch.all(torch.isfinite(consumption.grad))
        # Gradients should be non-zero (consumption affects utility)
        assert torch.any(consumption.grad != 0)
    
    def test_wealth_penalty_gradient_flow(self):
        """Test that gradients flow through wealth penalty."""
        penalty = SigmoidWealthPenalty(steepness=1e-4)
        
        # Create wealth as a leaf tensor with requires_grad
        wealth = torch.randn((100, 11), requires_grad=True)
        wealth.data.mul_(100_000).add_(200_000)
        consumption = torch.ones((100, 10)) * 40_000
        
        cost = penalty.evaluate(wealth, consumption)
        cost.backward()
        
        assert wealth.grad is not None
        assert torch.all(torch.isfinite(wealth.grad))
        assert torch.any(wealth.grad != 0)


# ==================== Test Edge Cases ====================


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_zero_wealth_handling(self, cumulative_inflation):
        """Test CRRA handles zero wealth correctly."""
        floor = FixedRealFloor(init_floor=30_000)
        crra = CRRAUtility(gamma=2.0, consumption_floor=floor)
        
        # Wealth goes to zero
        wealth = torch.zeros((10, 11))
        consumption = torch.ones((10, 10)) * 20_000
        
        cost = crra.evaluate(wealth, consumption, cumulative_inflation[:10, :])
        
        # Should not be NaN or inf
        assert torch.isfinite(cost)
    
    def test_very_high_gamma(self, wealth_trajectories, consumption_trajectories, cumulative_inflation):
        """Test CRRA with very high risk aversion."""
        floor = FixedRealFloor(init_floor=30_000)
        crra = CRRAUtility(gamma=10.0, consumption_floor=floor)
        
        cost = crra.evaluate(wealth_trajectories, consumption_trajectories, cumulative_inflation)
        
        assert torch.isfinite(cost)
    
    def test_very_low_gamma(self, wealth_trajectories, consumption_trajectories, cumulative_inflation):
        """Test CRRA with very low risk aversion (close to 1)."""
        floor = FixedRealFloor(init_floor=30_000)
        crra = CRRAUtility(gamma=1.1, consumption_floor=floor)
        
        cost = crra.evaluate(wealth_trajectories, consumption_trajectories, cumulative_inflation)
        
        assert torch.isfinite(cost)
