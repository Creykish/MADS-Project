"""
Unit tests for spending module.

Tests cover:
- Constants: NZ Super rates, expenditure guidelines
- Consumption floors: Fixed, declining, and composite floors
- Desired spending rules: All withdrawal rules from thesis Section 4.1.4
- Income sources: NZ Super, constant income, composite income
- SpendingPolicy: Complete policy with wealth constraints

All tests verify thesis equations and NZ institutional details.
"""

import pytest
import torch
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.spending import (
    # Constants
    NZ_SUPER_SINGLE,
    NZ_SUPER_COUPLE,
    EXPENDITURE_GUIDELINES,
    get_inflation_since,
    # Consumption floors
    NoConsumptionFloor,
    FixedRealFloor,
    DecliningRealFloor,
    CompositeFloor,
    # Desired spending
    ConstantRealSpending,
    DecliningRealSpending,
    PercentageOfWealth,
    PercentageOfInitialWealth,
    SixPercentRule,
    InflatedFourPercentRule,
    FixedDateRule,
    # Income
    NoIncome,
    ConstantRealIncome,
    NZSuper,
    CompositeIncome,
    # Policy
    SpendingPolicy,
)


# ==================== Test Fixtures ====================


@pytest.fixture
def wealth_history():
    """Sample wealth history: 5 sims, 10 time steps."""
    return torch.tensor([
        [500_000, 480_000, 460_000, 440_000, 420_000, 400_000, 380_000, 360_000, 340_000, 320_000],
        [500_000, 490_000, 475_000, 455_000, 435_000, 415_000, 395_000, 375_000, 355_000, 335_000],
        [500_000, 470_000, 445_000, 425_000, 405_000, 385_000, 365_000, 345_000, 325_000, 305_000],
        [500_000, 485_000, 465_000, 445_000, 425_000, 405_000, 385_000, 365_000, 345_000, 325_000],
        [500_000, 475_000, 455_000, 435_000, 415_000, 395_000, 375_000, 355_000, 335_000, 315_000],
    ], dtype=torch.float32)


@pytest.fixture
def cumulative_inflation():
    """Sample cumulative inflation: 2% per year."""
    n_sims = 5
    n_timesteps = 10
    inflation_per_year = 1.02
    
    # Create inflation multipliers
    time_steps = torch.arange(n_timesteps, dtype=torch.float32)
    inflation = inflation_per_year ** time_steps
    
    # Broadcast to (n_sims, n_timesteps)
    return inflation.unsqueeze(0).expand(n_sims, -1)


# ==================== Test Constants ====================


class TestConstants:
    """Test NZ Super constants and helpers."""
    
    def test_nz_super_rates(self):
        """Test that NZ Super rates match thesis values."""
        assert NZ_SUPER_SINGLE == 28_900.0
        assert NZ_SUPER_COUPLE == 44_400.0
    
    def test_expenditure_guidelines(self):
        """Test expenditure guidelines are present."""
        assert "no_frills_provincial_single" in EXPENDITURE_GUIDELINES
        assert "choices_metro_couple" in EXPENDITURE_GUIDELINES
        assert EXPENDITURE_GUIDELINES["no_frills_provincial_single"] == 32_000.0
    
    def test_get_inflation_since(self, cumulative_inflation):
        """Test inflation calculation between time steps."""
        # From t=0 to t=5 should be roughly 1.02^5 ≈ 1.1041
        multiplier = get_inflation_since(0, 5, cumulative_inflation)
        
        assert multiplier.shape == (5,)  # n_sims
        expected = 1.02 ** 5
        assert torch.allclose(multiplier, torch.tensor(expected), atol=1e-4)
    
    def test_inflation_since_raises_on_invalid(self, cumulative_inflation):
        """Test that t < t_0 raises error."""
        with pytest.raises(ValueError, match="t must be >= t_0"):
            get_inflation_since(5, 3, cumulative_inflation)


# ==================== Test Consumption Floors ====================


class TestConsumptionFloors:
    """Test consumption floor classes."""
    
    def test_no_floor(self, wealth_history, cumulative_inflation):
        """Test NoConsumptionFloor returns zeros."""
        floor = NoConsumptionFloor()
        result = floor.calculate(wealth_history, time_step=5, cumulative_inflation=cumulative_inflation)
        
        assert result.shape == (5,)
        assert torch.all(result == 0)
    
    def test_fixed_real_floor(self, wealth_history, cumulative_inflation):
        """Test FixedRealFloor adjusts for inflation."""
        floor = FixedRealFloor(init_floor=30_000, t_0=0)
        result = floor.calculate(wealth_history, time_step=5, cumulative_inflation=cumulative_inflation)
        
        # Should be 30,000 * 1.02^5
        expected = 30_000 * (1.02 ** 5)
        assert torch.allclose(result, torch.tensor(expected), atol=1.0)
    
    def test_declining_real_floor(self, wealth_history, cumulative_inflation):
        """Test DecliningRealFloor with 2% annual decline."""
        floor = DecliningRealFloor(init_floor=40_000, decline_rate=0.02, t_0=0)
        result = floor.calculate(wealth_history, time_step=5, cumulative_inflation=cumulative_inflation)
        
        # Real decline: 40,000 * (1 - 0.02)^5 = 40,000 * 0.98^5
        # Then inflate to nominal: * 1.02^5
        real_declined = 40_000 * (0.98 ** 5)
        expected = real_declined * (1.02 ** 5)
        assert torch.allclose(result, torch.tensor(expected), atol=1.0)
    
    def test_composite_floor_takes_max(self, wealth_history, cumulative_inflation):
        """Test CompositeFloor takes maximum of component floors."""
        floor1 = FixedRealFloor(init_floor=25_000, t_0=0)
        floor2 = FixedRealFloor(init_floor=35_000, t_0=0)
        
        composite = CompositeFloor([floor1, floor2], t_0=0)
        result = composite.calculate(wealth_history, time_step=3, cumulative_inflation=cumulative_inflation)
        
        # Should equal the higher floor (35,000 * inflation)
        expected = 35_000 * (1.02 ** 3)
        assert torch.allclose(result, torch.tensor(expected), atol=1.0)
    
    def test_floor_respects_time_bounds(self, wealth_history, cumulative_inflation):
        """Test floor returns zero outside time bounds."""
        floor = FixedRealFloor(init_floor=30_000, t_0=2, t_end=7)
        
        # Before t_0
        result_before = floor.calculate(wealth_history, time_step=1, cumulative_inflation=cumulative_inflation)
        assert torch.all(result_before == 0)
        
        # After t_end
        result_after = floor.calculate(wealth_history, time_step=8, cumulative_inflation=cumulative_inflation)
        assert torch.all(result_after == 0)
        
        # Within bounds
        result_within = floor.calculate(wealth_history, time_step=5, cumulative_inflation=cumulative_inflation)
        assert torch.all(result_within > 0)


# ==================== Test Tensor Methods ====================


class TestConsumptionFloorTensorMethods:
    """Test vectorized calculate_tensor methods for consumption floors."""
    
    def test_no_floor_tensor(self, wealth_history, cumulative_inflation):
        """Test NoConsumptionFloor.calculate_tensor returns zeros."""
        floor = NoConsumptionFloor()
        result = floor.calculate_tensor(wealth_history, cumulative_inflation)
        
        n_sims, n_timesteps = cumulative_inflation.shape
        assert result.shape == (n_sims, n_timesteps)
        assert torch.all(result == 0)
    
    def test_fixed_real_floor_tensor(self, wealth_history, cumulative_inflation):
        """Test FixedRealFloor.calculate_tensor matches loop-based calculate."""
        floor = FixedRealFloor(init_floor=30_000, t_0=0)
        
        # Calculate using tensor method
        result_tensor = floor.calculate_tensor(wealth_history, cumulative_inflation)
        
        # Calculate using loop (reference)
        n_sims, n_timesteps = cumulative_inflation.shape
        result_loop = torch.zeros((n_sims, n_timesteps))
        for t in range(n_timesteps):
            result_loop[:, t] = floor.calculate(
                wealth_history[:, :t+1], t, cumulative_inflation=cumulative_inflation
            )
        
        assert result_tensor.shape == (n_sims, n_timesteps)
        assert torch.allclose(result_tensor, result_loop, atol=1.0)
    
    def test_declining_real_floor_tensor(self, wealth_history, cumulative_inflation):
        """Test DecliningRealFloor.calculate_tensor matches loop-based calculate."""
        floor = DecliningRealFloor(init_floor=40_000, decline_rate=0.02, t_0=0)
        
        # Calculate using tensor method
        result_tensor = floor.calculate_tensor(wealth_history, cumulative_inflation)
        
        # Calculate using loop (reference)
        n_sims, n_timesteps = cumulative_inflation.shape
        result_loop = torch.zeros((n_sims, n_timesteps))
        for t in range(n_timesteps):
            result_loop[:, t] = floor.calculate(
                wealth_history[:, :t+1], t, cumulative_inflation=cumulative_inflation
            )
        
        assert result_tensor.shape == (n_sims, n_timesteps)
        assert torch.allclose(result_tensor, result_loop, atol=1.0)
    
    def test_composite_floor_tensor(self, wealth_history, cumulative_inflation):
        """Test CompositeFloor.calculate_tensor takes maximum across floors."""
        floor1 = FixedRealFloor(init_floor=25_000, t_0=0)
        floor2 = DecliningRealFloor(init_floor=45_000, decline_rate=0.03, t_0=0)
        
        composite = CompositeFloor([floor1, floor2], t_0=0)
        
        # Calculate using tensor method
        result_tensor = composite.calculate_tensor(wealth_history, cumulative_inflation)
        
        # Calculate using loop (reference)
        n_sims, n_timesteps = cumulative_inflation.shape
        result_loop = torch.zeros((n_sims, n_timesteps))
        for t in range(n_timesteps):
            result_loop[:, t] = composite.calculate(
                wealth_history[:, :t+1], t, cumulative_inflation=cumulative_inflation
            )
        
        assert result_tensor.shape == (n_sims, n_timesteps)
        assert torch.allclose(result_tensor, result_loop, atol=1.0)
    
    def test_floor_tensor_respects_time_bounds(self, wealth_history, cumulative_inflation):
        """Test calculate_tensor respects t_0 and t_end bounds."""
        floor = FixedRealFloor(init_floor=30_000, t_0=2, t_end=7)
        
        result = floor.calculate_tensor(wealth_history, cumulative_inflation)
        n_sims, n_timesteps = cumulative_inflation.shape
        
        # Before t_0 should be zero
        assert torch.all(result[:, 0] == 0)
        assert torch.all(result[:, 1] == 0)
        
        # After t_end should be zero
        assert torch.all(result[:, 8] == 0)
        assert torch.all(result[:, 9] == 0)
        
        # Within bounds should be positive
        assert torch.all(result[:, 2] > 0)
        assert torch.all(result[:, 5] > 0)
        assert torch.all(result[:, 7] > 0)
    
    def test_tensor_method_correctness_all_timesteps(self, wealth_history, cumulative_inflation):
        """Test tensor method produces identical results to loop for all timesteps."""
        floor = DecliningRealFloor(init_floor=50_000, decline_rate=0.015, t_0=0)
        
        # Tensor method
        result_tensor = floor.calculate_tensor(wealth_history, cumulative_inflation)
        
        # Loop method (ground truth)
        n_sims, n_timesteps = cumulative_inflation.shape
        result_loop = torch.zeros((n_sims, n_timesteps))
        for t in range(n_timesteps):
            result_loop[:, t] = floor.calculate(
                wealth_history[:, :t+1], t, cumulative_inflation=cumulative_inflation
            )
        
        # Should be identical within floating point precision
        assert torch.allclose(result_tensor, result_loop, rtol=1e-5, atol=1e-3)
    
    def test_tensor_method_with_nonzero_t0(self, wealth_history, cumulative_inflation):
        """Test tensor method with t_0 > 0."""
        floor = FixedRealFloor(init_floor=35_000, t_0=3, adjust_init_floor_for_inflation=True)
        
        # Tensor method
        result_tensor = floor.calculate_tensor(wealth_history, cumulative_inflation)
        
        # Loop method
        n_sims, n_timesteps = cumulative_inflation.shape
        result_loop = torch.zeros((n_sims, n_timesteps))
        for t in range(n_timesteps):
            result_loop[:, t] = floor.calculate(
                wealth_history[:, :t+1], t, cumulative_inflation=cumulative_inflation
            )
        
        assert torch.allclose(result_tensor, result_loop, atol=1.0)


# ==================== Test Desired Spending Rules ====================


class TestDesiredSpending:
    """Test desired spending rule classes."""
    
    def test_constant_real_spending(self, wealth_history, cumulative_inflation):
        """Test ConstantRealSpending adjusts for inflation."""
        rule = ConstantRealSpending(amount_real=40_000, t_0=0)
        result = rule.calculate(wealth_history, time_step=5, cumulative_inflation=cumulative_inflation)
        
        expected = 40_000 * (1.02 ** 5)
        assert torch.allclose(result, torch.tensor(expected), atol=1.0)
    
    def test_declining_real_spending(self, wealth_history, cumulative_inflation):
        """Test DecliningRealSpending with 2% annual decline."""
        rule = DecliningRealSpending(initial_real=50_000, decline_rate=0.02, t_0=0)
        result = rule.calculate(wealth_history, time_step=5, cumulative_inflation=cumulative_inflation)
        
        # 50,000 * 0.98^5 (real decline) * 1.02^5 (inflation)
        real_amount = 50_000 * (0.98 ** 5)
        expected = real_amount * (1.02 ** 5)
        assert torch.allclose(result, torch.tensor(expected), atol=1.0)
    
    def test_percentage_of_wealth(self, wealth_history, cumulative_inflation):
        """Test PercentageOfWealth uses current wealth."""
        rule = PercentageOfWealth(rate=0.04)
        result = rule.calculate(wealth_history, time_step=5, cumulative_inflation=cumulative_inflation)
        
        expected = wealth_history[:, 5] * 0.04
        assert torch.allclose(result, expected)
    
    def test_percentage_of_initial_wealth(self, wealth_history, cumulative_inflation):
        """Test PercentageOfInitialWealth uses initial wealth."""
        rule = PercentageOfInitialWealth(rate=0.04, adjust_for_inflation=True)
        result = rule.calculate(wealth_history, time_step=5, cumulative_inflation=cumulative_inflation)
        
        # 4% of initial wealth (500,000) adjusted for inflation
        initial = wealth_history[:, 0]
        expected = initial * 0.04 * (1.02 ** 5)
        assert torch.allclose(result, expected, atol=1.0)
    
    def test_six_percent_rule(self, wealth_history, cumulative_inflation):
        """Test SixPercentRule (6% of initial, not inflation-adjusted)."""
        rule = SixPercentRule()
        result = rule.calculate(wealth_history, time_step=5, cumulative_inflation=cumulative_inflation)
        
        # 6% of initial wealth, NOT adjusted for inflation
        initial = wealth_history[:, 0]
        expected = initial * 0.06
        assert torch.allclose(result, expected, atol=1.0)
    
    def test_inflated_four_percent_rule(self, wealth_history, cumulative_inflation):
        """Test InflatedFourPercentRule (4% of initial, inflation-adjusted)."""
        rule = InflatedFourPercentRule()
        result = rule.calculate(wealth_history, time_step=5, cumulative_inflation=cumulative_inflation)
        
        # 4% of initial wealth, adjusted for inflation
        initial = wealth_history[:, 0]
        expected = initial * 0.04 * (1.02 ** 5)
        assert torch.allclose(result, expected, atol=1.0)
    
    def test_fixed_date_rule(self, wealth_history, cumulative_inflation):
        """Test FixedDateRule divides by remaining years."""
        rule = FixedDateRule(t_0=0, t_end=20)
        result = rule.calculate(wealth_history, time_step=5, cumulative_inflation=cumulative_inflation)
        
        # Wealth at t=5 divided by (20 - 5) = 15 years
        expected = wealth_history[:, 5] / 15
        assert torch.allclose(result, expected)
    
    def test_fixed_date_rule_at_terminal(self, wealth_history, cumulative_inflation):
        """Test FixedDateRule at terminal date returns all wealth."""
        rule = FixedDateRule(t_0=0, t_end=5)
        result = rule.calculate(wealth_history, time_step=5, cumulative_inflation=cumulative_inflation)
        
        # At t=5 (terminal), should return all remaining wealth
        expected = wealth_history[:, 5]
        assert torch.allclose(result, expected)
    
    def test_spending_rule_respects_time_bounds(self, wealth_history, cumulative_inflation):
        """Test spending rules return zero outside time bounds."""
        rule = ConstantRealSpending(amount_real=40_000, t_0=2, t_end=7)
        
        # Before t_0
        result_before = rule.calculate(wealth_history, time_step=1, cumulative_inflation=cumulative_inflation)
        assert torch.all(result_before == 0)
        
        # After t_end
        result_after = rule.calculate(wealth_history, time_step=8, cumulative_inflation=cumulative_inflation)
        assert torch.all(result_after == 0)


# ==================== Test Income Sources ====================


class TestIncomeSources:
    """Test income source classes."""
    
    def test_no_income(self, wealth_history, cumulative_inflation):
        """Test NoIncome returns zeros."""
        income = NoIncome()
        result = income.calculate(wealth_history, time_step=5, cumulative_inflation=cumulative_inflation)
        
        assert result.shape == (5,)
        assert torch.all(result == 0)
    
    def test_constant_real_income(self, wealth_history, cumulative_inflation):
        """Test ConstantRealIncome adjusts for inflation."""
        income = ConstantRealIncome(amount_real=20_000, t_0=0)
        result = income.calculate(wealth_history, time_step=5, cumulative_inflation=cumulative_inflation)
        
        expected = 20_000 * (1.02 ** 5)
        assert torch.allclose(result, torch.tensor(expected), atol=1.0)
    
    def test_nz_super_single(self, wealth_history, cumulative_inflation):
        """Test NZSuper for single person."""
        income = NZSuper(household_type='single', include_winter_energy=True, age_at_t0=65, t_0=0)
        result = income.calculate(wealth_history, time_step=5, cumulative_inflation=cumulative_inflation)
        
        # NZ Super (28,900) + Winter Energy (1,064) = 29,964, adjusted for inflation
        base_amount = 28_900 + 1_064
        expected = base_amount * (1.02 ** 5)
        assert torch.allclose(result, torch.tensor(expected), atol=1.0)
    
    def test_nz_super_couple(self, wealth_history, cumulative_inflation):
        """Test NZSuper for couple."""
        income = NZSuper(household_type='couple', include_winter_energy=True, age_at_t0=65, t_0=0)
        result = income.calculate(wealth_history, time_step=5, cumulative_inflation=cumulative_inflation)
        
        # NZ Super (44,400) + Winter Energy (1,655) = 46,055, adjusted for inflation
        base_amount = 44_400 + 1_655
        expected = base_amount * (1.02 ** 5)
        assert torch.allclose(result, torch.tensor(expected), atol=1.0)
    
    def test_nz_super_without_winter_energy(self, wealth_history, cumulative_inflation):
        """Test NZSuper without Winter Energy Payment."""
        income = NZSuper(household_type='single', include_winter_energy=False, age_at_t0=65, t_0=0)
        result = income.calculate(wealth_history, time_step=5, cumulative_inflation=cumulative_inflation)
        
        expected = 28_900 * (1.02 ** 5)
        assert torch.allclose(result, torch.tensor(expected), atol=1.0)
    
    def test_nz_super_before_eligibility(self, wealth_history, cumulative_inflation):
        """Test NZSuper returns zero before age 65."""
        income = NZSuper(household_type='single', age_at_t0=60, t_0=0)
        
        # At t=3, age is 63 (< 65)
        result = income.calculate(wealth_history, time_step=3, cumulative_inflation=cumulative_inflation)
        assert torch.all(result == 0)
        
        # At t=5, age is 65 (eligible)
        result = income.calculate(wealth_history, time_step=5, cumulative_inflation=cumulative_inflation)
        assert torch.all(result > 0)
    
    def test_composite_income(self, wealth_history, cumulative_inflation):
        """Test CompositeIncome sums multiple sources."""
        nz_super = NZSuper(household_type='single', include_winter_energy=False, age_at_t0=65, t_0=0)
        part_time = ConstantRealIncome(amount_real=15_000, t_0=0)
        
        composite = CompositeIncome([nz_super, part_time])
        result = composite.calculate(wealth_history, time_step=5, cumulative_inflation=cumulative_inflation)
        
        # Sum of both sources
        expected = (28_900 + 15_000) * (1.02 ** 5)
        assert torch.allclose(result, torch.tensor(expected), atol=1.0)
    
    def test_income_respects_time_bounds(self, wealth_history, cumulative_inflation):
        """Test income returns zero outside time bounds."""
        income = ConstantRealIncome(amount_real=20_000, t_0=2, t_end=7)
        
        # Before t_0
        result_before = income.calculate(wealth_history, time_step=1, cumulative_inflation=cumulative_inflation)
        assert torch.all(result_before == 0)
        
        # After t_end
        result_after = income.calculate(wealth_history, time_step=8, cumulative_inflation=cumulative_inflation)
        assert torch.all(result_after == 0)


# ==================== Test SpendingPolicy ====================


class TestSpendingPolicy:
    """Test complete SpendingPolicy class."""
    
    def test_basic_policy(self, wealth_history, cumulative_inflation):
        """Test basic policy with no income or floor."""
        rule = PercentageOfWealth(rate=0.04)
        policy = SpendingPolicy(spending=rule)
        
        consumption = policy.calculate_consumption(
            wealth_history, time_step=5, cumulative_inflation=cumulative_inflation
        )
        
        # Should be 4% of current wealth
        expected = wealth_history[:, 5] * 0.04
        assert torch.allclose(consumption, expected)
    
    def test_policy_with_income(self, wealth_history, cumulative_inflation):
        """Test policy with NZ Super income."""
        rule = ConstantRealSpending(amount_real=50_000, t_0=0)
        income = NZSuper(household_type='single', include_winter_energy=True, age_at_t0=65, t_0=0)
        
        policy = SpendingPolicy(spending=rule, income=income)
        
        desired = policy.desired_spending(wealth_history, time_step=5, cumulative_inflation=cumulative_inflation)
        inc = policy.income(wealth_history, time_step=5, cumulative_inflation=cumulative_inflation)
        
        # Desired should be 50,000 * inflation
        expected_desired = 50_000 * (1.02 ** 5)
        assert torch.allclose(desired, torch.tensor(expected_desired), atol=1.0)
        
        # Income should be NZ Super + Winter Energy
        expected_income = (28_900 + 1_064) * (1.02 ** 5)
        assert torch.allclose(inc, torch.tensor(expected_income), atol=1.0)
    
    def test_policy_with_floor(self, wealth_history, cumulative_inflation):
        """Test policy enforces consumption floor."""
        # Low desired spending
        rule = PercentageOfWealth(rate=0.01)  # Only 1% of wealth
        floor = FixedRealFloor(init_floor=35_000, t_0=0)
        
        policy = SpendingPolicy(spending=rule, floor=floor)
        
        consumption = policy.calculate_consumption(
            wealth_history, time_step=5, cumulative_inflation=cumulative_inflation
        )
        
        # Floor should be binding (35,000 * inflation > 1% of wealth)
        expected_floor = 35_000 * (1.02 ** 5)
        assert torch.allclose(consumption, torch.tensor(expected_floor), atol=1.0)
    
    def test_wealth_constraint(self, wealth_history, cumulative_inflation):
        """Test policy enforces wealth constraint (can't spend more than available)."""
        # Very high desired spending
        rule = ConstantRealSpending(amount_real=1_000_000, t_0=0)
        policy = SpendingPolicy(spending=rule)
        
        consumption = policy.calculate_consumption(
            wealth_history, time_step=5, cumulative_inflation=cumulative_inflation
        )
        
        # Should be capped at current wealth
        expected = wealth_history[:, 5]
        assert torch.allclose(consumption, expected)
    
    def test_wealth_constraint_with_income(self, wealth_history, cumulative_inflation):
        """Test wealth constraint includes income."""
        # High desired spending
        rule = ConstantRealSpending(amount_real=500_000, t_0=0)
        income = NZSuper(household_type='single', include_winter_energy=True, age_at_t0=65, t_0=0)
        
        policy = SpendingPolicy(spending=rule, income=income)
        
        consumption = policy.calculate_consumption(
            wealth_history, time_step=5, cumulative_inflation=cumulative_inflation
        )
        
        # Should be capped at wealth + income
        inc = (28_900 + 1_064) * (1.02 ** 5)
        expected = wealth_history[:, 5] + inc
        assert torch.allclose(consumption, expected, atol=1.0)
    
    def test_wealth_delta(self, wealth_history, cumulative_inflation):
        """Test calculate_wealth_delta returns income - consumption."""
        rule = ConstantRealSpending(amount_real=40_000, t_0=0)
        income = NZSuper(household_type='single', include_winter_energy=True, age_at_t0=65, t_0=0)
        
        policy = SpendingPolicy(spending=rule, income=income)
        
        delta = policy.calculate_wealth_delta(
            wealth_history, time_step=5, cumulative_inflation=cumulative_inflation
        )
        
        # Delta = income - consumption
        inc = (28_900 + 1_064) * (1.02 ** 5)
        cons = 40_000 * (1.02 ** 5)
        expected = inc - cons
        assert torch.allclose(delta, torch.tensor(expected), atol=1.0)
    
    def test_complete_policy_integration(self, wealth_history, cumulative_inflation):
        """Test complete policy with all components."""
        # Declining spending rule
        rule = DecliningRealSpending(initial_real=60_000, decline_rate=0.02, t_0=0)
        
        # NZ Super income
        income = NZSuper(household_type='couple', include_winter_energy=True, age_at_t0=65, t_0=0)
        
        # Floor that declines with age
        floor = DecliningRealFloor(init_floor=40_000, decline_rate=0.02, t_0=0)
        
        policy = SpendingPolicy(
            spending=rule,
            income=income,
            floor=floor
        )
        
        consumption = policy.calculate_consumption(
            wealth_history, time_step=5, cumulative_inflation=cumulative_inflation
        )
        
        # Verify consumption is reasonable
        assert consumption.shape == (5,)
        assert torch.all(consumption > 0)
        
        # Verify it respects floor
        floor_value = floor.calculate(wealth_history, time_step=5, cumulative_inflation=cumulative_inflation)
        assert torch.all(consumption >= floor_value - 1.0)  # Allow small numerical error


# ==================== Test Device Handling ====================


class TestDeviceHandling:
    """Test that operations work correctly on different devices."""
    
    def test_spending_on_cpu(self, wealth_history, cumulative_inflation):
        """Test spending calculations on CPU."""
        rule = PercentageOfWealth(rate=0.04)
        policy = SpendingPolicy(spending=rule)
        
        consumption = policy.calculate_consumption(
            wealth_history, time_step=5, cumulative_inflation=cumulative_inflation
        )
        
        assert consumption.device == torch.device('cpu')
    
    @pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA not available")
    def test_spending_on_gpu(self, wealth_history, cumulative_inflation):
        """Test spending calculations on GPU."""
        # Move tensors to GPU
        wealth_gpu = wealth_history.cuda()
        inflation_gpu = cumulative_inflation.cuda()
        
        rule = PercentageOfWealth(rate=0.04)
        policy = SpendingPolicy(spending=rule)
        
        consumption = policy.calculate_consumption(
            wealth_gpu, time_step=5, cumulative_inflation=inflation_gpu
        )
        
        assert consumption.device.type == 'cuda'
        
        # Verify correctness
        expected = wealth_gpu[:, 5] * 0.04
        assert torch.allclose(consumption, expected)


# ==================== Test Edge Cases ====================


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_zero_wealth(self, cumulative_inflation):
        """Test policy behavior with zero wealth.
        
        Without a floor, consumption follows the spending rule (4% of zero = 0).
        With a floor, consumption can utilize available income.
        """
        wealth = torch.zeros(5, 10)
        
        # Without floor: desired spending is 0, so consumption is 0
        rule = PercentageOfWealth(rate=0.04)
        income = NZSuper(household_type='single', age_at_t0=65, t_0=0)
        policy_no_floor = SpendingPolicy(spending=rule, income=income)
        
        consumption_no_floor = policy_no_floor.calculate_consumption(
            wealth, time_step=5, cumulative_inflation=cumulative_inflation
        )
        
        # With zero wealth and no floor, consumption should be 0
        assert torch.allclose(consumption_no_floor, torch.tensor(0.0), atol=1.0)
        
        # With floor: can consume up to income even with zero wealth
        floor = FixedRealFloor(init_floor=30_000, t_0=0)
        policy_with_floor = SpendingPolicy(
            spending=rule, 
            income=income,
            floor=floor
        )
        
        consumption_with_floor = policy_with_floor.calculate_consumption(
            wealth, time_step=5, cumulative_inflation=cumulative_inflation
        )
        
        # Floor is ~33k at t=5, income is ~33k, so can consume min(floor, income)
        expected_income = (28_900 + 1_064) * (1.02 ** 5)
        assert torch.allclose(consumption_with_floor, torch.tensor(expected_income), atol=1.0)
    
    def test_single_simulation(self, cumulative_inflation):
        """Test with single simulation path."""
        wealth = torch.tensor([[500_000, 480_000, 460_000, 440_000, 420_000]], dtype=torch.float32)
        inflation = cumulative_inflation[:1, :5]  # Single sim, 5 timesteps
        
        rule = PercentageOfWealth(rate=0.04)
        policy = SpendingPolicy(spending=rule)
        
        consumption = policy.calculate_consumption(
            wealth, time_step=4, cumulative_inflation=inflation
        )
        
        assert consumption.shape == (1,)
        expected = 420_000 * 0.04
        assert torch.allclose(consumption, torch.tensor([expected]))
    
    def test_negative_wealth_delta(self, wealth_history, cumulative_inflation):
        """Test that wealth delta can be negative (drawdown)."""
        # High spending, low income
        rule = ConstantRealSpending(amount_real=50_000, t_0=0)
        income = ConstantRealIncome(amount_real=10_000, t_0=0)
        
        policy = SpendingPolicy(spending=rule, income=income)
        
        delta = policy.calculate_wealth_delta(
            wealth_history, time_step=5, cumulative_inflation=cumulative_inflation
        )
        
        # Delta should be negative (spending > income)
        assert torch.all(delta < 0)
