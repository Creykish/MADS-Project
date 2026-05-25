"""
Complete spending policy combining rules, floors, and income.

Implements the wealth constraint from thesis Section 4.1.4:
- Wealth constraint: ĉ_t = min(c_t, w_t + v_t)
- Net contributions: π_t = -ĉ_t + v_t
"""

import torch
from typing import Optional
from .desired_spending import DesiredSpendingRule
from .income import IncomeSource, NoIncome
from .consumption_floors import ConsumptionFloor, NoConsumptionFloor


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
    consumption_floor : Optional[ConsumptionFloor]
        Minimum consumption floor. Defaults to no floor.

    Examples
    --------
    >>> from .desired_spending import InflatedFourPercentRule
    >>> from .income import NZSuper
    >>> from .consumption_floors import FixedRealFloor
    >>>
    >>> rule = InflatedFourPercentRule()
    >>> income = NZSuper(household_type='single')
    >>> floor = FixedRealFloor(init_floor=30_000)
    >>> policy = SpendingPolicy(rule, income, floor)
    """

    def __init__(
        self,
        spending: DesiredSpendingRule,
        income: Optional[IncomeSource] = None,
        floor: Optional[ConsumptionFloor] = None,
    ):
        self.spending_rule = spending
        self.income_source = income if income is not None else NoIncome()
        self.consumption_floor = (
            floor if floor is not None else NoConsumptionFloor()
        )

    def desired_spending(
        self,
        wealth: torch.Tensor,
        time_step: int,
        cumulative_inflation: torch.Tensor,
        **kwargs
    ) -> torch.Tensor:
        """
        Calculate desired spending (before constraints).

        Returns
        -------
        torch.Tensor
            Desired spending amount
        """
        return self.spending_rule.calculate(
            wealth=wealth,
            time_step=time_step,
            cumulative_inflation=cumulative_inflation,
            **kwargs
        )

    def income(
        self,
        wealth: torch.Tensor,
        time_step: int,
        cumulative_inflation: torch.Tensor,
        **kwargs
    ) -> torch.Tensor:
        """
        Calculate income received.

        Returns
        -------
        torch.Tensor
            Income amount
        """
        return self.income_source.calculate(
            wealth=wealth,
            time_step=time_step,
            cumulative_inflation=cumulative_inflation,
            **kwargs
        )

    def floor(
        self,
        wealth: torch.Tensor,
        time_step: int,
        cumulative_inflation: torch.Tensor,
        **kwargs
    ) -> torch.Tensor:
        """
        Calculate consumption floor.

        Returns
        -------
        torch.Tensor
            Consumption floor amount
        """
        return self.consumption_floor.calculate(
            wealth=wealth,
            time_step=time_step,
            cumulative_inflation=cumulative_inflation,
            **kwargs
        )

    def calculate_consumption(
        self,
        wealth: torch.Tensor,
        time_step: int,
        cumulative_inflation: torch.Tensor,
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
        desired = self.desired_spending(wealth, time_step, cumulative_inflation, **kwargs)
        minimum = self.floor(wealth, time_step, cumulative_inflation, **kwargs)
        spending = torch.maximum(desired, minimum)  # Ensure we meet the floor
        inc = self.income(wealth, time_step, cumulative_inflation, **kwargs)
        available = wealth[:, time_step] + inc

        # Can't consume more than available
        actual = torch.minimum(spending, available)
        return actual

    def calculate_wealth_delta(
        self, wealth: torch.Tensor, time_step: int, cumulative_inflation: torch.Tensor, **kwargs
    ) -> torch.Tensor:
        """
        Calculate change in wealth.

        Delta = income - consumption (negative = drawdown)

        Returns
        -------
        torch.Tensor
            Change in wealth
        """
        inc = self.income(wealth, time_step, cumulative_inflation, **kwargs)
        cons = self.calculate_consumption(wealth, time_step, cumulative_inflation, **kwargs)
        return inc - cons
