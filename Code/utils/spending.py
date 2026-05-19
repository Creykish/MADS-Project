"""
Spending/consumption policies for retirement.

Modular architecture with three layers:
1. DesiredSpendingRule: Calculates what the household wants to spend
2. IncomeSource: Calculates income received (pensions, wages, etc.)
3. SpendingPolicy: Combines rules + income, applies wealth constraints

This allows hot-swapping spending rules and income sources independently.

Examples
--------
>>> # NZ retiree with declining spending
>>> rule = DecliningRealSpending(initial=50_000, decline_rate=0.02)
>>> income = NZSuper(household_type='single')
>>> policy = SpendingPolicy(spending_rule=rule, income_source=income)

>>> # 4% rule with no external income
>>> rule = PercentageOfWealth(rate=0.04)
>>> policy = SpendingPolicy(spending_rule=rule)

>>> # Combine multiple income sources
>>> nz_super = NZSuper(household_type='couple')
>>> part_time = ConstantRealIncome(amount=15_000, end_age=70, age_at_t0=65)
>>> income = CompositeIncome([nz_super, part_time])
>>> policy = SpendingPolicy(spending_rule=rule, income_source=income)
"""

import torch
from typing import Optional, Literal, List
from abc import ABC, abstractmethod
from .inflation import Inflation, ConstantInflation


# ==================== NZ Super and Expenditure Constants ====================

# NZ Super 2025/26 rates (after-tax, annual)
NZ_SUPER_SINGLE = 28_900.0  # Single person living alone
NZ_SUPER_SINGLE_SHARING = 26_700.0  # Single person sharing
NZ_SUPER_COUPLE = 44_400.0  # Couple combined

# Winter Energy Payment (annual)
WINTER_ENERGY_SINGLE = 1_064.0  # $20.46/week * 52 weeks
WINTER_ENERGY_COUPLE = 1_655.0  # $31.82/week * 52 weeks

# Retirement Expenditure Guidelines 2025 (annual)
# Source: Matthews (2025) - NZ Fin-Ed Centre, Massey University
EXPENDITURE_GUIDELINES = {
    # Singles
    'no_frills_provincial_single': 32_000.0,
    'no_frills_metro_single': 38_400.0,
    'choices_provincial_single': 47_700.0,
    'choices_metro_single': 52_800.0,
    
    # Couples
    'no_frills_provincial_couple': 48_300.0,
    'no_frills_metro_couple': 57_100.0,
    'choices_provincial_couple': 79_100.0,
    'choices_metro_couple': 92_600.0,
}


# ==================== Layer 1: Desired Spending Rules ====================

class DesiredSpendingRule(ABC):
    """
    Abstract base for desired spending rules.
    
    These rules determine what the household *wants* to spend,
    independent of wealth constraints or income sources.
    """
    
    @abstractmethod
    def calculate(
        self,
        wealth: torch.Tensor,
        time_step: int,
        **kwargs
    ) -> torch.Tensor:
        """
        Calculate desired spending for this period.
        
        Parameters
        ----------
        wealth : torch.Tensor
            Current wealth (may or may not be used by rule)
        time_step : int
            Current time step (0-indexed)
        **kwargs : dict
            Additional context (age, etc.)
        
        Returns
        -------
        torch.Tensor
            Desired spending amount
        """
        pass


class ConstantRealSpending(DesiredSpendingRule):
    """
    Fixed real spending, adjusted for inflation.
    
    Parameters
    ----------
    amount_real : float
        Annual spending in year-0 real terms
    inflation : Inflation
        Inflation model
    
    Examples
    --------
    >>> rule = ConstantRealSpending(amount_real=40_000)
    """
    
    def __init__(
        self,
        amount_real: float,
        inflation: Inflation = ConstantInflation(0.02)
    ):
        self.amount_real = amount_real
        self.inflation = inflation
    
    def calculate(self, wealth: torch.Tensor, time_step: int, **kwargs) -> torch.Tensor:
        nominal = self.amount_real * self.inflation.get_multiplier(time_step)
        return torch.full_like(wealth, nominal)


class DecliningRealSpending(DesiredSpendingRule):
    """
    Real spending declining at constant rate.
    
    S(t) = S_0 * (1 - decline_rate)^t
    
    Reflects empirical pattern in retirement (Le 2023, RIIG 2024).
    
    Parameters
    ----------
    initial_real : float
        Initial spending in year-0 real terms
    decline_rate : float
        Annual real decline rate (e.g., 0.02 for 2%/year)
    inflation : Inflation
        Inflation model
    
    Examples
    --------
    >>> rule = DecliningRealSpending(initial_real=50_000, decline_rate=0.02)
    """
    
    def __init__(
        self,
        initial_real: float,
        decline_rate: float = 0.02,
        inflation: Inflation = ConstantInflation(0.02)
    ):
        self.initial_real = initial_real
        self.decline_rate = decline_rate
        self.inflation = inflation
    
    def calculate(self, wealth: torch.Tensor, time_step: int, **kwargs) -> torch.Tensor:
        real_amount = self.initial_real * ((1 - self.decline_rate) ** time_step)
        nominal = real_amount * self.inflation.get_multiplier(time_step)
        return torch.full_like(wealth, nominal)


class PercentageOfWealth(DesiredSpendingRule):
    """
    Spend fixed percentage of current wealth.
    
    Classic example: 4% rule (Bengen 1994).
    
    Parameters
    ----------
    rate : float
        Spending rate (e.g., 0.04 for 4%)
    
    Examples
    --------
    >>> rule = PercentageOfWealth(rate=0.04)
    """
    
    def __init__(self, rate: float):
        self.rate = rate
    
    def calculate(self, wealth: torch.Tensor, time_step: int, **kwargs) -> torch.Tensor:
        return wealth * self.rate


class PercentageOfInitialWealth(DesiredSpendingRule):
    """
    Spend percentage of initial wealth, inflation-adjusted.
    
    Bengen's (1994) formulation: withdraw X% of starting portfolio,
    then adjust for inflation each year.
    
    Parameters
    ----------
    rate : float
        Withdrawal rate (e.g., 0.04)
    initial_wealth : float
        Starting portfolio value
    inflation : Inflation
        Inflation model
    
    Examples
    --------
    >>> rule = PercentageOfInitialWealth(rate=0.04, initial_wealth=1_000_000)
    """
    
    def __init__(
        self,
        rate: float,
        initial_wealth: float,
        inflation: Inflation = ConstantInflation(0.02)
    ):
        self.rate = rate
        self.initial_wealth = initial_wealth
        self.inflation = inflation
    
    def calculate(self, wealth: torch.Tensor, time_step: int, **kwargs) -> torch.Tensor:
        real_amount = self.initial_wealth * self.rate
        nominal = real_amount * self.inflation.get_multiplier(time_step)
        return torch.full_like(wealth, nominal)


class FloorCeilingRule(DesiredSpendingRule):
    """
    Percentage-of-wealth with floor and optional ceiling.
    
    Spending = max(floor, min(ceiling, wealth * rate))
    Floor and ceiling decline in real terms if specified.
    
    Parameters
    ----------
    rate : float
        Target withdrawal rate
    floor_real : float
        Minimum spending in year-0 real terms
    ceiling_real : Optional[float]
        Maximum spending in year-0 real terms (None = no ceiling)
    decline_rate : float
        Real decline in floor/ceiling (default 0 = constant)
    inflation : Inflation
        Inflation model
    
    Examples
    --------
    >>> rule = FloorCeilingRule(
    ...     rate=0.04,
    ...     floor_real=30_000,
    ...     ceiling_real=80_000,
    ...     decline_rate=0.02
    ... )
    """
    
    def __init__(
        self,
        rate: float,
        floor_real: float,
        ceiling_real: Optional[float] = None,
        decline_rate: float = 0.0,
        inflation: Inflation = ConstantInflation(0.02)
    ):
        self.rate = rate
        self.floor_real = floor_real
        self.ceiling_real = ceiling_real
        self.decline_rate = decline_rate
        self.inflation = inflation
    
    def calculate(self, wealth: torch.Tensor, time_step: int, **kwargs) -> torch.Tensor:
        # Calculate floor
        real_floor = self.floor_real * ((1 - self.decline_rate) ** time_step)
        nominal_floor = real_floor * self.inflation.get_multiplier(time_step)
        
        # Target from wealth
        target = wealth * self.rate
        
        # Apply floor
        spending = torch.maximum(target, torch.full_like(wealth, nominal_floor))
        
        # Apply ceiling if specified
        if self.ceiling_real is not None:
            real_ceiling = self.ceiling_real * ((1 - self.decline_rate) ** time_step)
            nominal_ceiling = real_ceiling * self.inflation.get_multiplier(time_step)
            spending = torch.minimum(spending, torch.full_like(wealth, nominal_ceiling))
        
        return spending


class ExpenditureTierRule(DesiredSpendingRule):
    """
    NZ expenditure guideline tier with declining consumption.
    
    Based on Matthews (2025) Retirement Expenditure Guidelines.
    Spending declines in real terms at specified rate.
    
    Parameters
    ----------
    tier : str
        One of the EXPENDITURE_GUIDELINES keys, or use tier_name + household_type
    tier_name : Optional[str]
        'no_frills_provincial', 'no_frills_metro', 'choices_provincial', 'choices_metro'
    household_type : Optional[Literal['single', 'couple']]
        Used with tier_name to construct full key
    initial_real : Optional[float]
        Custom initial spending (overrides tier)
    decline_rate : float
        Annual real decline (default 2%)
    inflation : Inflation
        Inflation model
    
    Examples
    --------
    >>> # Using tier name + household
    >>> rule = ExpenditureTierRule(
    ...     tier_name='choices_metro',
    ...     household_type='single'
    ... )
    
    >>> # Using full tier key
    >>> rule = ExpenditureTierRule(tier='choices_metro_single')
    
    >>> # Custom amount
    >>> rule = ExpenditureTierRule(initial_real=60_000, decline_rate=0.015)
    """
    
    def __init__(
        self,
        tier: Optional[str] = None,
        tier_name: Optional[str] = None,
        household_type: Optional[Literal['single', 'couple']] = None,
        initial_real: Optional[float] = None,
        decline_rate: float = 0.02,
        inflation: Inflation = ConstantInflation(0.02)
    ):
        self.decline_rate = decline_rate
        self.inflation = inflation
        
        # Determine initial spending
        if initial_real is not None:
            self.initial_real = initial_real
        elif tier is not None:
            if tier not in EXPENDITURE_GUIDELINES:
                raise ValueError(f"Invalid tier: {tier}. Must be one of {list(EXPENDITURE_GUIDELINES.keys())}")
            self.initial_real = EXPENDITURE_GUIDELINES[tier]
        elif tier_name is not None and household_type is not None:
            full_key = f"{tier_name}_{household_type}"
            if full_key not in EXPENDITURE_GUIDELINES:
                raise ValueError(
                    f"Invalid tier_name: {tier_name}. "
                    f"Valid: no_frills_provincial, no_frills_metro, choices_provincial, choices_metro"
                )
            self.initial_real = EXPENDITURE_GUIDELINES[full_key]
        else:
            raise ValueError(
                "Must specify either: tier, (tier_name + household_type), or initial_real"
            )
    
    def calculate(self, wealth: torch.Tensor, time_step: int, **kwargs) -> torch.Tensor:
        real_amount = self.initial_real * ((1 - self.decline_rate) ** time_step)
        nominal = real_amount * self.inflation.get_multiplier(time_step)
        return torch.full_like(wealth, nominal)


# ==================== Layer 2: Income Sources ====================

class IncomeSource(ABC):
    """
    Abstract base for income sources.
    
    Income is received before consumption decisions are made.
    """
    
    @abstractmethod
    def calculate(
        self,
        wealth: torch.Tensor,
        time_step: int,
        **kwargs
    ) -> torch.Tensor:
        """
        Calculate income for this period.
        
        Parameters
        ----------
        wealth : torch.Tensor
            Current wealth (usually not used by income sources)
        time_step : int
            Current time step
        **kwargs : dict
            Additional context (age, etc.)
        
        Returns
        -------
        torch.Tensor
            Income amount
        """
        pass


class NoIncome(IncomeSource):
    """No external income. Default."""
    
    def calculate(self, wealth: torch.Tensor, time_step: int, **kwargs) -> torch.Tensor:
        return torch.zeros_like(wealth)


class ConstantRealIncome(IncomeSource):
    """
    Constant real income, optionally age-limited.
    
    Parameters
    ----------
    amount_real : float
        Annual income in year-0 real terms
    start_age : Optional[int]
        Age when income starts (None = from t=0)
    end_age : Optional[int]
        Age when income stops (None = forever)
    age_at_t0 : int
        Age at time step 0
    inflation : Inflation
        Inflation model
    
    Examples
    --------
    >>> # Part-time work from 65-70
    >>> income = ConstantRealIncome(
    ...     amount_real=15_000,
    ...     start_age=65,
    ...     end_age=70,
    ...     age_at_t0=65
    ... )
    """
    
    def __init__(
        self,
        amount_real: float,
        start_age: Optional[int] = None,
        end_age: Optional[int] = None,
        age_at_t0: int = 65,
        inflation: Inflation = ConstantInflation(0.02)
    ):
        self.amount_real = amount_real
        self.start_age = start_age
        self.end_age = end_age
        self.age_at_t0 = age_at_t0
        self.inflation = inflation
    
    def calculate(self, wealth: torch.Tensor, time_step: int, **kwargs) -> torch.Tensor:
        age = self.age_at_t0 + time_step
        
        # Check age bounds
        if self.start_age is not None and age < self.start_age:
            return torch.zeros_like(wealth)
        if self.end_age is not None and age >= self.end_age:
            return torch.zeros_like(wealth)
        
        # Return inflation-adjusted income
        nominal = self.amount_real * self.inflation.get_multiplier(time_step)
        return torch.full_like(wealth, nominal)


class NZSuper(IncomeSource):
    """
    New Zealand Superannuation.
    
    Universal pension from age 65, indexed to wages/CPI.
    
    Parameters
    ----------
    household_type : Literal['single', 'single_sharing', 'couple']
        Household composition
    include_winter_energy : bool
        Include Winter Energy Payment (default True)
    start_age : int
        Age when NZ Super begins (default 65)
    age_at_t0 : int
        Age at time step 0 (default 65)
    inflation : Inflation
        Inflation model (should track wage floor in reality)
    
    Examples
    --------
    >>> income = NZSuper(household_type='single', include_winter_energy=True)
    """
    
    def __init__(
        self,
        household_type: Literal['single', 'single_sharing', 'couple'],
        include_winter_energy: bool = True,
        start_age: int = 65,
        age_at_t0: int = 65,
        inflation: Inflation = ConstantInflation(0.02)
    ):
        self.household_type = household_type
        self.include_winter_energy = include_winter_energy
        self.start_age = start_age
        self.age_at_t0 = age_at_t0
        self.inflation = inflation
        
        # Set base amounts
        if household_type == 'single':
            self.nz_super_base = NZ_SUPER_SINGLE
            self.winter_energy_base = WINTER_ENERGY_SINGLE
        elif household_type == 'single_sharing':
            self.nz_super_base = NZ_SUPER_SINGLE_SHARING
            self.winter_energy_base = WINTER_ENERGY_SINGLE
        elif household_type == 'couple':
            self.nz_super_base = NZ_SUPER_COUPLE
            self.winter_energy_base = WINTER_ENERGY_COUPLE
        else:
            raise ValueError("household_type must be 'single', 'single_sharing', or 'couple'")
    
    def calculate(self, wealth: torch.Tensor, time_step: int, **kwargs) -> torch.Tensor:
        age = self.age_at_t0 + time_step
        
        # Calculate total annual payment
        annual_amount = self.nz_super_base
        if self.include_winter_energy:
            annual_amount += self.winter_energy_base
        
        # Adjust for inflation
        nominal = annual_amount * self.inflation.get_multiplier(time_step)
        
        # Only receive if eligible age
        if age >= self.start_age:
            return torch.full_like(wealth, nominal)
        else:
            return torch.zeros_like(wealth)


class CompositeIncome(IncomeSource):
    """
    Combine multiple income sources.
    
    Parameters
    ----------
    sources : List[IncomeSource]
        Income sources to combine (summed)
    
    Examples
    --------
    >>> nz_super = NZSuper(household_type='couple')
    >>> part_time = ConstantRealIncome(amount_real=20_000, end_age=70, age_at_t0=65)
    >>> income = CompositeIncome([nz_super, part_time])
    """
    
    def __init__(self, sources: List[IncomeSource]):
        if not sources:
            raise ValueError("Must provide at least one income source")
        self.sources = sources
    
    def calculate(self, wealth: torch.Tensor, time_step: int, **kwargs) -> torch.Tensor:
        total = torch.zeros_like(wealth)
        for source in self.sources:
            total = total + source.calculate(wealth, time_step, **kwargs)
        return total


# ==================== Layer 3: Complete Spending Policy ====================

class SpendingPolicy:
    """
    Complete spending policy combining desired spending rule + income sources.
    
    Applies wealth constraint: actual consumption ≤ wealth + income
    
    Parameters
    ----------
    spending_rule : DesiredSpendingRule
        Rule for desired spending
    income_source : Optional[IncomeSource]
        Income source(s). Defaults to no income.
    
    Examples
    --------
    >>> # NZ retiree with declining spending
    >>> rule = DecliningRealSpending(initial_real=50_000, decline_rate=0.02)
    >>> income = NZSuper(household_type='single')
    >>> policy = SpendingPolicy(spending_rule=rule, income_source=income)
    
    >>> # 4% rule, no income
    >>> rule = PercentageOfWealth(rate=0.04)
    >>> policy = SpendingPolicy(spending_rule=rule)
    
    >>> # Couple with tier spending + NZ Super + part-time work
    >>> rule = ExpenditureTierRule(tier_name='choices_metro', household_type='couple')
    >>> nz_super = NZSuper(household_type='couple')
    >>> work = ConstantRealIncome(amount_real=15_000, end_age=70, age_at_t0=65)
    >>> income = CompositeIncome([nz_super, work])
    >>> policy = SpendingPolicy(spending_rule=rule, income_source=income)
    """
    
    def __init__(
        self,
        spending_rule: DesiredSpendingRule,
        income_source: Optional[IncomeSource] = None
    ):
        self.spending_rule = spending_rule
        self.income_source = income_source if income_source is not None else NoIncome()
    
    def desired_spending(
        self,
        wealth: torch.Tensor,
        time_step: int,
        **kwargs
    ) -> torch.Tensor:
        """
        Calculate desired spending (before constraints).
        
        Returns
        -------
        torch.Tensor
            Desired spending amount
        """
        return self.spending_rule.calculate(wealth, time_step, **kwargs)
    
    def income(
        self,
        wealth: torch.Tensor,
        time_step: int,
        **kwargs
    ) -> torch.Tensor:
        """
        Calculate income received.
        
        Returns
        -------
        torch.Tensor
            Income amount
        """
        return self.income_source.calculate(wealth, time_step, **kwargs)
    
    def calculate_consumption(
        self,
        wealth: torch.Tensor,
        time_step: int,
        **kwargs
    ) -> torch.Tensor:
        """
        Calculate actual consumption (after applying wealth constraint).
        
        Consumption cannot exceed wealth + income.
        
        Returns
        -------
        torch.Tensor
            Actual consumption (≤ desired, ≤ wealth + income)
        """
        desired = self.desired_spending(wealth, time_step, **kwargs)
        inc = self.income(wealth, time_step, **kwargs)
        available = wealth + inc
        
        # Can't consume more than available
        actual = torch.minimum(desired, available)
        return actual
    
    def calculate_wealth_delta(
        self,
        wealth: torch.Tensor,
        time_step: int,
        **kwargs
    ) -> torch.Tensor:
        """
        Calculate change in wealth.
        
        Delta = income - consumption (negative = drawdown)
        
        Returns
        -------
        torch.Tensor
            Change in wealth
        """
        inc = self.income(wealth, time_step, **kwargs)
        cons = self.calculate_consumption(wealth, time_step, **kwargs)
        return inc - cons


# ==================== Convenience Functions ====================

def make_nz_retirement_policy(
    tier: Literal['no_frills', 'choices'],
    location: Literal['provincial', 'metro'],
    household_type: Literal['single', 'couple'],
    decline_rate: float = 0.02,
    include_winter_energy: bool = True,
    **kwargs
) -> SpendingPolicy:
    """
    Create NZ retirement policy with expenditure tier + NZ Super.
    
    Parameters
    ----------
    tier : Literal['no_frills', 'choices']
        Expenditure tier
    location : Literal['provincial', 'metro']
        Location
    household_type : Literal['single', 'couple']
        Household type
    decline_rate : float
        Real spending decline rate (default 2%)
    include_winter_energy : bool
        Include Winter Energy Payment (default True)
    **kwargs
        Additional arguments for ExpenditureTierRule
    
    Returns
    -------
    SpendingPolicy
        Complete policy
    
    Examples
    --------
    >>> policy = make_nz_retirement_policy('choices', 'metro', 'single')
    >>> policy = make_nz_retirement_policy('no_frills', 'provincial', 'couple', decline_rate=0.015)
    """
    rule = ExpenditureTierRule(
        tier_name=f"{tier}_{location}",
        household_type=household_type,
        decline_rate=decline_rate,
        **kwargs
    )
    
    income = NZSuper(
        household_type=household_type,
        include_winter_energy=include_winter_energy
    )
    
    return SpendingPolicy(spending_rule=rule, income_source=income)

