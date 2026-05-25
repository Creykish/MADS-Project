"""
Unit tests for allocation policy classes.

Tests cover:
- ConstantAllocation: static allocation policy
- TimeBasedPolicy: age-based glidepath with linear interpolation
- WealthBasedPolicy: wealth-dependent allocation
- ControlMatrixPolicy: 2D control matrix with bilinear interpolation

All tests verify Equation 13 constraints: non-negative allocations summing to 1.0.
"""

import pytest
import torch
from Code.utils.allocation import (
    ConstantAllocation,
    TimeBasedPolicy,
    WealthBasedPolicy,
    ControlMatrixPolicy,
)


class TestConstantAllocation:
    """Test suite for ConstantAllocation policy."""

    def test_initialization(self):
        """Test that ConstantAllocation initializes correctly."""
        policy = ConstantAllocation(n_assets=3, n_sims=100)
        assert policy.n_assets == 3
        assert policy.n_sims == 100
        assert policy.device == torch.device("cpu")

    def test_simple_allocation(self):
        """Test basic allocation with single risky asset."""
        policy = ConstantAllocation(n_assets=2, n_sims=10)
        settings = torch.tensor([0.6])  # 60% risky, 40% safe
        
        allocation = policy.get_allocation(settings)
        
        assert allocation.shape == (10, 2)
        assert torch.allclose(allocation[:, 0], torch.tensor(0.4))  # Safe asset
        assert torch.allclose(allocation[:, 1], torch.tensor(0.6))  # Risky asset
        assert torch.allclose(allocation.sum(dim=1), torch.tensor(1.0))

    def test_multi_asset_allocation(self):
        """Test allocation with multiple risky assets."""
        policy = ConstantAllocation(n_assets=4, n_sims=5)
        settings = torch.tensor([0.3, 0.4, 0.2])  # Three risky assets
        
        allocation = policy.get_allocation(settings)
        
        assert allocation.shape == (5, 4)
        assert torch.allclose(allocation[:, 0], torch.tensor(0.1))  # Safe: 1 - 0.9
        assert torch.allclose(allocation[:, 1], torch.tensor(0.3))
        assert torch.allclose(allocation[:, 2], torch.tensor(0.4))
        assert torch.allclose(allocation[:, 3], torch.tensor(0.2))
        assert torch.allclose(allocation.sum(dim=1), torch.tensor(1.0))

    def test_all_safe_allocation(self):
        """Test 100% allocation to safe asset."""
        policy = ConstantAllocation(n_assets=2, n_sims=5)
        settings = torch.tensor([0.0])  # 0% risky
        
        allocation = policy.get_allocation(settings)
        
        assert torch.allclose(allocation[:, 0], torch.tensor(1.0))
        assert torch.allclose(allocation[:, 1], torch.tensor(0.0))

    def test_all_risky_allocation(self):
        """Test 100% allocation to risky asset."""
        policy = ConstantAllocation(n_assets=2, n_sims=5)
        settings = torch.tensor([1.0])  # 100% risky
        
        allocation = policy.get_allocation(settings)
        
        assert torch.allclose(allocation[:, 0], torch.tensor(0.0))
        assert torch.allclose(allocation[:, 1], torch.tensor(1.0))

    def test_constraint_validation_negative(self):
        """Test that negative allocations raise error."""
        policy = ConstantAllocation(n_assets=2, n_sims=5)
        settings = torch.tensor([-0.1])
        
        with pytest.raises(AssertionError, match="non-negative"):
            policy.get_allocation(settings)

    def test_constraint_validation_exceeds_one(self):
        """Test that allocations exceeding 1.0 raise error."""
        policy = ConstantAllocation(n_assets=2, n_sims=5)
        settings = torch.tensor([1.1])
        
        with pytest.raises(AssertionError, match="cannot exceed 1.0"):
            policy.get_allocation(settings)

    def test_wrong_dimension(self):
        """Test that wrong tensor dimension raises error."""
        policy = ConstantAllocation(n_assets=3, n_sims=5)
        settings = torch.tensor([0.5])  # Should be length 2
        
        with pytest.raises(AssertionError, match="n_assets - 1"):
            policy.get_allocation(settings)


class TestTimeBasedPolicy:
    """Test suite for TimeBasedPolicy."""

    def test_initialization(self):
        """Test TimeBasedPolicy initialization."""
        time_nodes = torch.tensor([0.0, 10.0, 20.0])
        policy = TimeBasedPolicy(n_assets=2, n_sims=10, time_nodes=time_nodes)
        
        assert policy.n_assets == 2
        assert policy.n_sims == 10
        assert torch.equal(policy.time_nodes, time_nodes)

    def test_linear_interpolation_midpoint(self):
        """Test linear interpolation at midpoint."""
        time_nodes = torch.tensor([0.0, 10.0, 20.0])
        policy = TimeBasedPolicy(n_assets=2, n_sims=5, time_nodes=time_nodes)
        
        # Glidepath: 80% risky at t=0, 60% at t=10, 40% at t=20
        settings = torch.tensor([[0.8], [0.6], [0.4]])
        
        # At t=5 (midpoint between 0 and 10), expect 70% risky
        allocation = policy.get_allocation(t=5.0, policy_settings=settings)
        
        assert allocation.shape == (5, 2)
        assert torch.allclose(allocation[:, 0], torch.tensor(0.3), atol=1e-6)
        assert torch.allclose(allocation[:, 1], torch.tensor(0.7), atol=1e-6)

    def test_at_node_point(self):
        """Test that allocation at node equals node value."""
        time_nodes = torch.tensor([0.0, 10.0])
        policy = TimeBasedPolicy(n_assets=2, n_sims=3, time_nodes=time_nodes)
        settings = torch.tensor([[0.9], [0.5]])
        
        allocation = policy.get_allocation(t=10.0, policy_settings=settings)
        
        assert torch.allclose(allocation[:, 1], torch.tensor(0.5))

    def test_declining_glidepath(self):
        """Test typical declining equity glidepath."""
        time_nodes = torch.tensor([65.0, 75.0, 85.0])
        policy = TimeBasedPolicy(n_assets=2, n_sims=10, time_nodes=time_nodes)
        
        # Declining from 80% to 40% equity
        settings = torch.tensor([[0.8], [0.6], [0.4]])
        
        alloc_65 = policy.get_allocation(t=65.0, policy_settings=settings)
        alloc_75 = policy.get_allocation(t=75.0, policy_settings=settings)
        alloc_85 = policy.get_allocation(t=85.0, policy_settings=settings)
        
        assert alloc_65[:, 1].mean() > alloc_75[:, 1].mean() > alloc_85[:, 1].mean()

    def test_multi_asset_interpolation(self):
        """Test interpolation with multiple risky assets."""
        time_nodes = torch.tensor([0.0, 10.0])
        policy = TimeBasedPolicy(n_assets=3, n_sims=5, time_nodes=time_nodes)
        
        # Two risky assets
        settings = torch.tensor([[0.6, 0.2], [0.4, 0.3]])
        
        allocation = policy.get_allocation(t=5.0, policy_settings=settings)
        
        assert allocation.shape == (5, 3)
        assert torch.allclose(allocation.sum(dim=1), torch.tensor(1.0))
        assert (allocation >= 0).all()

    def test_out_of_bounds_time(self):
        """Test that time outside node range raises error."""
        time_nodes = torch.tensor([0.0, 10.0])
        policy = TimeBasedPolicy(n_assets=2, n_sims=5, time_nodes=time_nodes)
        settings = torch.tensor([[0.8], [0.5]])
        
        with pytest.raises(AssertionError, match="out of bounds"):
            policy.get_allocation(t=15.0, policy_settings=settings)

    def test_constraint_preservation(self):
        """Test that interpolation preserves constraints."""
        time_nodes = torch.tensor([0.0, 10.0])
        policy = TimeBasedPolicy(n_assets=2, n_sims=5, time_nodes=time_nodes)
        settings = torch.tensor([[0.9], [0.3]])
        
        allocation = policy.get_allocation(t=5.0, policy_settings=settings)
        
        assert (allocation >= 0).all()
        assert (allocation.sum(dim=1) <= 1.0 + 1e-6).all()


class TestWealthBasedPolicy:
    """Test suite for WealthBasedPolicy."""

    def test_initialization(self):
        """Test WealthBasedPolicy initialization."""
        wealth_nodes = torch.tensor([0.0, 100.0, 500.0])
        policy = WealthBasedPolicy(n_assets=2, n_sims=10, wealth_nodes=wealth_nodes)
        
        assert policy.n_assets == 2
        assert policy.n_sims == 10
        assert torch.equal(policy.wealth_nodes, wealth_nodes)

    def test_wealth_interpolation(self):
        """Test interpolation based on wealth."""
        wealth_nodes = torch.tensor([0.0, 100.0, 200.0])
        policy = WealthBasedPolicy(n_assets=2, n_sims=1, wealth_nodes=wealth_nodes)
        
        # More aggressive at higher wealth
        settings = torch.tensor([[0.3], [0.6], [0.8]])
        
        wealth = torch.tensor([150.0])  # Midpoint between 100 and 200
        allocation = policy.get_allocation(wealth=wealth, policy_settings=settings)
        
        # Should be 70% risky (midpoint between 0.6 and 0.8)
        assert torch.allclose(allocation[:, 1], torch.tensor(0.7), atol=1e-6)

    def test_wealth_clamping_low(self):
        """Test that wealth below minimum is clamped."""
        wealth_nodes = torch.tensor([10.0, 100.0])
        policy = WealthBasedPolicy(n_assets=2, n_sims=1, wealth_nodes=wealth_nodes)
        settings = torch.tensor([[0.3], [0.7]])
        
        wealth = torch.tensor([5.0])  # Below minimum
        allocation = policy.get_allocation(wealth=wealth, policy_settings=settings)
        
        # Should use minimum node allocation
        assert torch.allclose(allocation[:, 1], torch.tensor(0.3))

    def test_wealth_clamping_high(self):
        """Test that wealth above maximum is clamped."""
        wealth_nodes = torch.tensor([10.0, 100.0])
        policy = WealthBasedPolicy(n_assets=2, n_sims=1, wealth_nodes=wealth_nodes)
        settings = torch.tensor([[0.3], [0.7]])
        
        wealth = torch.tensor([200.0])  # Above maximum
        allocation = policy.get_allocation(wealth=wealth, policy_settings=settings)
        
        # Should use maximum node allocation
        assert torch.allclose(allocation[:, 1], torch.tensor(0.7))

    def test_multiple_paths(self):
        """Test allocation for multiple wealth paths simultaneously."""
        wealth_nodes = torch.tensor([0.0, 100.0])
        policy = WealthBasedPolicy(n_assets=2, n_sims=3, wealth_nodes=wealth_nodes)
        settings = torch.tensor([[0.2], [0.8]])
        
        wealth = torch.tensor([0.0, 50.0, 100.0])
        allocation = policy.get_allocation(wealth=wealth, policy_settings=settings)
        
        assert allocation.shape == (3, 2)
        # All paths should have valid allocations
        assert (allocation.sum(dim=1) <= 1.0 + 1e-6).all()


class TestControlMatrixPolicy:
    """Test suite for ControlMatrixPolicy."""

    def test_initialization(self):
        """Test ControlMatrixPolicy initialization."""
        time_nodes = torch.tensor([0.0, 10.0])
        wealth_nodes = torch.tensor([0.0, 100.0])
        policy = ControlMatrixPolicy(
            n_assets=2, n_sims=5, 
            time_nodes=time_nodes, 
            wealth_nodes=wealth_nodes
        )
        
        assert policy.n_assets == 2
        assert policy.n_sims == 5
        assert torch.equal(policy.time_nodes, time_nodes)
        assert torch.equal(policy.wealth_nodes, wealth_nodes)

    def test_bilinear_interpolation_center(self):
        """Test bilinear interpolation at grid center."""
        time_nodes = torch.tensor([0.0, 10.0])
        wealth_nodes = torch.tensor([0.0, 100.0])
        policy = ControlMatrixPolicy(
            n_assets=2, n_sims=1,
            time_nodes=time_nodes,
            wealth_nodes=wealth_nodes
        )
        
        # Control matrix: (time, wealth, assets)
        settings = torch.tensor([
            [[0.2], [0.4]],  # t=0: w=0 -> 20%, w=100 -> 40%
            [[0.6], [0.8]]   # t=10: w=0 -> 60%, w=100 -> 80%
        ])
        
        wealth = torch.tensor([50.0])  # Center of wealth range
        allocation = policy.get_allocation(t=5.0, wealth=wealth, policy_settings=settings)
        
        # Expected: bilinear interpolation gives 50% risky
        # (0.2 + 0.4 + 0.6 + 0.8) / 4 = 0.5
        assert allocation.shape == (1, 2)
        assert torch.allclose(allocation[:, 1], torch.tensor(0.5), atol=1e-6)

    def test_corner_values(self):
        """Test that corners match control matrix values."""
        time_nodes = torch.tensor([0.0, 10.0])
        wealth_nodes = torch.tensor([0.0, 100.0])
        policy = ControlMatrixPolicy(
            n_assets=2, n_sims=1,
            time_nodes=time_nodes,
            wealth_nodes=wealth_nodes
        )
        
        settings = torch.tensor([
            [[0.2], [0.4]],
            [[0.6], [0.8]]
        ])
        
        # Test all four corners
        corners = [
            (0.0, torch.tensor([0.0]), 0.2),
            (0.0, torch.tensor([100.0]), 0.4),
            (10.0, torch.tensor([0.0]), 0.6),
            (10.0, torch.tensor([100.0]), 0.8),
        ]
        
        for t, w, expected_risky in corners:
            allocation = policy.get_allocation(t=t, wealth=w, policy_settings=settings)
            assert torch.allclose(allocation[:, 1], torch.tensor(expected_risky), atol=1e-6)

    def test_wealth_time_response(self):
        """Test that allocation responds to both time and wealth."""
        time_nodes = torch.tensor([65.0, 85.0])
        wealth_nodes = torch.tensor([50.0, 500.0])
        policy = ControlMatrixPolicy(
            n_assets=2, n_sims=1,
            time_nodes=time_nodes,
            wealth_nodes=wealth_nodes
        )
        
        # Conservative at low wealth, aggressive at high wealth
        # More conservative over time
        settings = torch.tensor([
            [[0.3], [0.7]],  # t=65: low->30%, high->70%
            [[0.2], [0.5]]   # t=85: low->20%, high->50%
        ])
        
        # Young and wealthy should be most aggressive
        alloc_young_rich = policy.get_allocation(
            t=65.0, wealth=torch.tensor([500.0]), policy_settings=settings
        )
        
        # Old and poor should be most conservative
        alloc_old_poor = policy.get_allocation(
            t=85.0, wealth=torch.tensor([50.0]), policy_settings=settings
        )
        
        assert alloc_young_rich[:, 1] > alloc_old_poor[:, 1]

    def test_multi_path_allocation(self):
        """Test allocation for multiple paths with varying wealth."""
        time_nodes = torch.tensor([0.0, 10.0])
        wealth_nodes = torch.tensor([0.0, 100.0])
        policy = ControlMatrixPolicy(
            n_assets=2, n_sims=5,
            time_nodes=time_nodes,
            wealth_nodes=wealth_nodes
        )
        
        settings = torch.tensor([
            [[0.3], [0.7]],
            [[0.4], [0.8]]
        ])
        
        wealth = torch.tensor([0.0, 25.0, 50.0, 75.0, 100.0])
        allocation = policy.get_allocation(t=5.0, wealth=wealth, policy_settings=settings)
        
        assert allocation.shape == (5, 2)
        assert (allocation.sum(dim=1) <= 1.0 + 1e-6).all()
        assert (allocation >= -1e-6).all()
        
        # Verify monotonicity: higher wealth should have higher risky allocation
        assert all(allocation[i, 1] <= allocation[i+1, 1] for i in range(4))

    def test_constraint_validation_on_input(self):
        """Test that invalid policy settings are rejected."""
        time_nodes = torch.tensor([0.0, 10.0])
        wealth_nodes = torch.tensor([0.0, 100.0])
        policy = ControlMatrixPolicy(
            n_assets=2, n_sims=1,
            time_nodes=time_nodes,
            wealth_nodes=wealth_nodes
        )
        
        # Invalid: allocation exceeds 1.0
        invalid_settings = torch.tensor([
            [[1.2], [0.8]],
            [[0.6], [0.7]]
        ])
        
        with pytest.raises(AssertionError, match="Equation 13"):
            policy.get_allocation(
                t=5.0, 
                wealth=torch.tensor([50.0]), 
                policy_settings=invalid_settings
            )


class TestConstraintEnforcement:
    """Cross-cutting tests for Equation 13 constraints."""

    @pytest.mark.parametrize("PolicyClass,extra_kwargs", [
        (TimeBasedPolicy, {"time_nodes": torch.tensor([0.0, 10.0])}),
        (WealthBasedPolicy, {"wealth_nodes": torch.tensor([0.0, 100.0])}),
    ])
    def test_sum_to_one(self, PolicyClass, extra_kwargs):
        """Test that all policies produce allocations summing to 1.0."""
        policy = PolicyClass(n_assets=3, n_sims=10, **extra_kwargs)
        settings = torch.tensor([[0.5, 0.3], [0.4, 0.4]])
        
        if PolicyClass == TimeBasedPolicy:
            allocation = policy.get_allocation(t=5.0, policy_settings=settings)
        else:
            allocation = policy.get_allocation(
                wealth=torch.tensor([50.0] * 10), 
                policy_settings=settings
            )
        
        assert torch.allclose(allocation.sum(dim=1), torch.ones(10))

    @pytest.mark.parametrize("PolicyClass,extra_kwargs", [
        (ConstantAllocation, {}),
        (TimeBasedPolicy, {"time_nodes": torch.tensor([0.0, 10.0])}),
        (WealthBasedPolicy, {"wealth_nodes": torch.tensor([0.0, 100.0])}),
    ])
    def test_non_negative(self, PolicyClass, extra_kwargs):
        """Test that all policies produce non-negative allocations."""
        policy = PolicyClass(n_assets=2, n_sims=5, **extra_kwargs)
        
        if PolicyClass == ConstantAllocation:
            settings = torch.tensor([0.6])
            allocation = policy.get_allocation(settings)
        elif PolicyClass == TimeBasedPolicy:
            settings = torch.tensor([[0.8], [0.4]])
            allocation = policy.get_allocation(t=5.0, policy_settings=settings)
        else:
            settings = torch.tensor([[0.8], [0.4]])
            allocation = policy.get_allocation(
                wealth=torch.tensor([50.0] * 5),
                policy_settings=settings
            )
        
        assert (allocation >= -1e-6).all()  # Allow small numerical errors


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
