"""
Spending/consumption policies for retirement.

Implements spending rules and income sources as described in thesis Section 4.1.4
"Modelling Contributions and Withdrawals" and Section 2.2 "Retirement in New Zealand".
"""

from .constants import (
    NZ_SUPER_SINGLE,
    NZ_SUPER_SINGLE_SHARING,
    NZ_SUPER_COUPLE,
    NZ_SUPER_ELIGIBILITY_AGE,
    WINTER_ENERGY_SINGLE,
    WINTER_ENERGY_COUPLE,
    EXPENDITURE_GUIDELINES,
    get_inflation_since,
)

from .consumption_floors import (
    ConsumptionFloor,
    NoConsumptionFloor,
    FixedRealFloor,
    DecliningRealFloor,
    CompositeFloor,
)

from .desired_spending import (
    DesiredSpendingRule,
    ConstantRealSpending,
    DecliningRealSpending,
    PercentageOfWealth,
    PercentageOfInitialWealth,
    SixPercentRule,
    InflatedFourPercentRule,
    FixedDateRule,
)

from .income import (
    IncomeSource,
    NoIncome,
    ConstantRealIncome,
    NZSuper,
    CompositeIncome,
)

from .spending_policy import SpendingPolicy

__all__ = [
    # Constants
    "NZ_SUPER_SINGLE",
    "NZ_SUPER_SINGLE_SHARING",
    "NZ_SUPER_COUPLE",
    "NZ_SUPER_ELIGIBILITY_AGE",
    "WINTER_ENERGY_SINGLE",
    "WINTER_ENERGY_COUPLE",
    "EXPENDITURE_GUIDELINES",
    "get_inflation_since",
    # Consumption Floors
    "ConsumptionFloor",
    "NoConsumptionFloor",
    "FixedRealFloor",
    "DecliningRealFloor",
    "CompositeFloor",
    # Desired Spending
    "DesiredSpendingRule",
    "ConstantRealSpending",
    "DecliningRealSpending",
    "PercentageOfWealth",
    "PercentageOfInitialWealth",
    "SixPercentRule",
    "InflatedFourPercentRule",
    "FixedDateRule",
    # Income
    "IncomeSource",
    "NoIncome",
    "ConstantRealIncome",
    "NZSuper",
    "CompositeIncome",
    # Policy
    "SpendingPolicy",
]
