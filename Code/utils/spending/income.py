"""
Income sources for retirement.

Includes NZ Super, wages, and other income streams.

Implements income modeling from thesis Section 4.1.4 and NZ Super from Section 2.2.
"""

import torch
from typing import Optional, Literal, List
from abc import ABC, abstractmethod
from .constants import (
    NZ_SUPER_SINGLE,
    NZ_SUPER_SINGLE_SHARING,
    NZ_SUPER_COUPLE,
    NZ_SUPER_ELIGIBILITY_AGE,
    WINTER_ENERGY_SINGLE,
    WINTER_ENERGY_COUPLE,
    get_inflation_since,
)


class IncomeSource(ABC):
    """
    Abstract base for income sources.

    Income is received before consumption decisions are made.
    """

    def __init__(
        self,
        t_0: int = 0,
        t_end: Optional[int] = None,
    ):
        self.t_0 = t_0
        self.t_end = t_end

    def calculate(
        self,
        wealth: torch.Tensor,
        time_step: int,
        cumulative_inflation: torch.Tensor,
        **kwargs,
    ) -> torch.Tensor:
        if self.t_end is not None and time_step > self.t_end:
            return torch.zeros_like(wealth[:, time_step])
        if time_step < self.t_0:
            return torch.zeros_like(wealth[:, time_step])
        return self._calculate(
            wealth, time_step, cumulative_inflation=cumulative_inflation, **kwargs
        )

    @abstractmethod
    def _calculate(
        self,
        wealth: torch.Tensor,
        time_step: int,
        cumulative_inflation: torch.Tensor,
        **kwargs,
    ) -> torch.Tensor:
        """
        Calculate income for this period.

        Parameters
        ----------
        wealth : torch.Tensor
            Wealth history up to current time step, shape (n_sims, time_step + 1)
        time_step : int
            Current time step
        **kwargs : dict
            Additional context (age, etc.)

        Returns
        -------
        torch.Tensor
            Income amount, shape (n_sims,)
        """
        pass


class NoIncome(IncomeSource):
    """No external income. Default."""

    def _calculate(
        self,
        wealth: torch.Tensor,
        time_step: int,
        cumulative_inflation: torch.Tensor,
        **kwargs,
    ) -> torch.Tensor:
        return torch.zeros_like(wealth[:, time_step])


class ConstantRealIncome(IncomeSource):
    """
    Constant real income, optionally age-limited.

    Parameters
    ----------
    amount_real : float
        Annual income in year-0 real terms
    t_0 : int
        Time step when income starts (default 0)
    t_end : Optional[int]
        Time step when income stops (None = forever)

    Examples
    --------
    >>> # Part-time work from t=0 to t=5
    >>> income = ConstantRealIncome(amount_real=15_000, t_0=0, t_end=5)
    """

    def __init__(
        self,
        amount_real: float,
        t_0: int = 0,
        t_end: Optional[int] = None,
    ):
        super().__init__(t_0=t_0, t_end=t_end)
        self.amount_real = amount_real

    def _calculate(
        self,
        wealth: torch.Tensor,
        time_step: int,
        cumulative_inflation: torch.Tensor,
        **kwargs,
    ) -> torch.Tensor:
        nominal = self.amount_real * cumulative_inflation[:, time_step]
        return nominal


class NZSuper(IncomeSource):
    """
    New Zealand Superannuation.

    Universal pension from age 65, indexed to wages/CPI.
    
    Thesis Section 2.2.1: "The Act mandates annual adjustment for CPI inflation 
    subject to a binding wage floor."

    Note: Current implementation only adjusts for CPI inflation, not the wage floor.

    Parameters
    ----------
    household_type : Literal['single', 'single_sharing', 'couple']
        Household composition
    include_winter_energy : bool
        Include Winter Energy Payment (default True)
    age_at_t0 : int
        Age at time step 0 (default 65)
    t_0 : int
        Time step when policy starts
    t_end : Optional[int]
        Time step when policy ends

    Examples
    --------
    >>> income = NZSuper(household_type='single', include_winter_energy=True)
    """

    def __init__(
        self,
        household_type: Literal["single", "single_sharing", "couple"],
        include_winter_energy: bool = True,
        age_at_t0: int = 65,
        t_0: int = 0,
        t_end: Optional[int] = None,
    ):
        super().__init__(t_0=t_0, t_end=t_end)
        self.household_type = household_type
        self.include_winter_energy = include_winter_energy
        self.age_at_t0 = age_at_t0

        # Set base amounts
        if household_type == "single":
            self.nz_super_base = NZ_SUPER_SINGLE
            self.winter_energy_base = WINTER_ENERGY_SINGLE
        elif household_type == "single_sharing":
            self.nz_super_base = NZ_SUPER_SINGLE_SHARING
            self.winter_energy_base = WINTER_ENERGY_SINGLE
        elif household_type == "couple":
            self.nz_super_base = NZ_SUPER_COUPLE
            self.winter_energy_base = WINTER_ENERGY_COUPLE
        else:
            raise ValueError(
                "household_type must be 'single', 'single_sharing', or 'couple'"
            )

    def _calculate(
        self,
        wealth: torch.Tensor,
        time_step: int,
        cumulative_inflation: torch.Tensor,
        **kwargs,
    ) -> torch.Tensor:
        age = self.age_at_t0 + time_step
        if age < NZ_SUPER_ELIGIBILITY_AGE:
            return torch.zeros_like(wealth[:, time_step])

        # Calculate total annual payment
        annual_amount = self.nz_super_base
        if self.include_winter_energy:
            annual_amount += self.winter_energy_base

        # Adjust for inflation
        nominal = annual_amount * cumulative_inflation[:, time_step]
        return nominal


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
    >>> part_time = ConstantRealIncome(amount_real=20_000, t_end=5)
    >>> income = CompositeIncome([nz_super, part_time])
    """

    def __init__(
        self, sources: List[IncomeSource], t_0: int = 0, t_end: Optional[int] = None
    ):
        if not sources:
            raise ValueError("Must provide at least one income source")
        self.sources = sources
        self.t_0 = t_0
        self.t_end = t_end

    def _calculate(
        self,
        wealth: torch.Tensor,
        time_step: int,
        cumulative_inflation: torch.Tensor,
        **kwargs,
    ) -> torch.Tensor:
        total = torch.zeros_like(wealth[:, time_step])
        for source in self.sources:
            total = total + source.calculate(
                wealth, time_step, cumulative_inflation=cumulative_inflation, **kwargs
            )
        return total
