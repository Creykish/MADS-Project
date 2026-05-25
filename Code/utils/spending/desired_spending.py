"""
Desired spending rules for retirement.

These rules determine what the household wants to spend, independent of 
wealth constraints or income sources.

Implements withdrawal rules from thesis Section 4.1.4.
"""

import torch
from typing import Optional
from abc import ABC, abstractmethod
from .constants import get_inflation_since


class DesiredSpendingRule(ABC):
    """
    Abstract base for desired spending rules.

    These rules determine what the household *wants* to spend,
    independent of wealth constraints or income sources.
    """

    def __init__(
        self,
        t_0: int = 0,
        t_end: Optional[int] = None,
    ):
        self.t_0 = t_0
        self.t_end = t_end

    def calculate(
        self, wealth: torch.Tensor, time_step: int, **kwargs
    ) -> torch.Tensor:
        if self.t_end is not None and time_step > self.t_end:
            return torch.zeros_like(wealth[:, time_step])
        if time_step < self.t_0:
            return torch.zeros_like(wealth[:, time_step])
        return self._calculate(wealth, time_step, **kwargs)

    @abstractmethod
    def _calculate(
        self, wealth: torch.Tensor, time_step: int, **kwargs
    ) -> torch.Tensor:
        """
        Calculate desired spending for this time step.

        Parameters
        ----------
        wealth : torch.Tensor
            Wealth history up to current time step, shape (n_sims, time_step + 1)
        time_step : int
            Current time step
        **kwargs : dict
            Additional context (inflation, age, etc.)

        Returns
        -------
        torch.Tensor
            Desired spending for this time step, shape (n_sims,)
        """
        pass


class ConstantRealSpending(DesiredSpendingRule):
    """
    Fixed real spending, adjusted for inflation.

    Parameters
    ----------
    amount_real : float
        Annual spending in year-0 real terms

    Examples
    --------
    >>> rule = ConstantRealSpending(amount_real=40_000)
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
        nominal = self.amount_real * get_inflation_since(
            self.t_0, time_step, cumulative_inflation
        )
        return nominal


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

    Examples
    --------
    >>> rule = DecliningRealSpending(initial_real=50_000, decline_rate=0.02)
    """

    def __init__(
        self,
        initial_real: float,
        decline_rate: float = 0.02,
        t_0: int = 0,
        t_end: Optional[int] = None,
    ):
        self.initial_real = initial_real
        self.decline_rate = decline_rate
        super().__init__(t_0=t_0, t_end=t_end)

    def _calculate(
        self,
        wealth: torch.Tensor,
        time_step: int,
        cumulative_inflation: torch.Tensor,
        **kwargs,
    ) -> torch.Tensor:
        elapsed = time_step - self.t_0
        real_amount = self.initial_real * ((1 - self.decline_rate) ** elapsed)
        nominal = real_amount * cumulative_inflation[:, time_step]
        return nominal


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

    def __init__(self, rate: float, t_0: int = 0, t_end: Optional[int] = None):
        super().__init__(t_0=t_0, t_end=t_end)
        self.rate = rate

    def _calculate(
        self,
        wealth: torch.Tensor,
        time_step: int,
        cumulative_inflation: torch.Tensor,
        **kwargs,
    ) -> torch.Tensor:
        return wealth[:, time_step] * self.rate


class PercentageOfInitialWealth(DesiredSpendingRule):
    """
    Spend percentage of initial wealth, inflation-adjusted.

    Bengen's (1994) formulation: withdraw X% of starting portfolio,
    then adjust for inflation each year.

    Parameters
    ----------
    rate : float
        Withdrawal rate (e.g., 0.04)
    adjust_for_inflation : bool
        Whether to adjust for inflation (default True)

    Examples
    --------
    >>> rule = PercentageOfInitialWealth(rate=0.04)
    """

    def __init__(
        self,
        rate: float,
        adjust_for_inflation: bool = True,
        t_0: int = 0,
        t_end: Optional[int] = None,
    ):
        self.rate = rate
        self.adjust_for_inflation = adjust_for_inflation
        super().__init__(t_0=t_0, t_end=t_end)

    def _calculate(
        self,
        wealth: torch.Tensor,
        time_step: int,
        cumulative_inflation: torch.Tensor,
        **kwargs,
    ) -> torch.Tensor:
        amount = self.rate * wealth[:, 0]  # Initial wealth is at time_step=0
        if self.adjust_for_inflation:
            amount = amount * get_inflation_since(0, time_step, cumulative_inflation)
        return amount


class SixPercentRule(PercentageOfInitialWealth):
    """
    6% rule: Withdraw 6% of initial wealth, not adjusted for inflation.

    Thesis Section 4.1.4: "This rule front-loads spending and is well-aligned 
    with the empirical finding that real spending declines by approximately 2% 
    per year after age 65."

    Examples
    --------
    >>> rule = SixPercentRule()
    """

    def __init__(
        self, t_0: int = 0, t_end: Optional[int] = None
    ):
        super().__init__(
            rate=0.06,
            t_0=t_0,
            t_end=t_end,
            adjust_for_inflation=False,
        )


class InflatedFourPercentRule(PercentageOfInitialWealth):
    """
    Inflated 4% rule: Bengen's original 4% withdrawal, inflation-adjusted.

    Thesis Section 4.1.4: c_t = 0.04 × w_0 × s_t

    Examples
    --------
    >>> rule = InflatedFourPercentRule()
    """

    def __init__(
        self, t_0: int = 0, t_end: Optional[int] = None
    ):
        super().__init__(
            rate=0.04,
            t_0=t_0,
            t_end=t_end,
            adjust_for_inflation=True,
        )


class FixedDateRule(DesiredSpendingRule):
    """
    Divide current wealth by years remaining to a fixed terminal date.

    Thesis Section 4.1.4: c_t = w_t / (T - t)

    Parameters
    ----------
    t_end : int
        Terminal time step (required)

    Examples
    --------
    >>> rule = FixedDateRule(t_end=30)  # Exhaust by time step 30
    """

    def __init__(
        self,
        t_0: int = 0,
        t_end: Optional[int] = None,
    ):
        if t_end is None:
            raise ValueError("t_end must be specified for FixedDateRule")
        super().__init__(t_0=t_0, t_end=t_end)

    def _calculate(
        self,
        wealth: torch.Tensor,
        time_step: int,
        cumulative_inflation: torch.Tensor,
        **kwargs,
    ) -> torch.Tensor:
        w_t = wealth[:, time_step]
        remaining_years = self.t_end - time_step
        if remaining_years <= 0:
            return w_t  # Spend everything at or after t_end
        return w_t / remaining_years  # Spend equal amounts until t_end
