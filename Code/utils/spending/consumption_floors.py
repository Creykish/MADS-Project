"""
Consumption floor rules for retirement spending.

Floors define minimum spending levels that must be met regardless of wealth constraints.
"""

import torch
from typing import Optional, List
from abc import ABC, abstractmethod
from .constants import get_inflation_since


class ConsumptionFloor(ABC):
    """
    Abstract base for consumption floor rules.

    These rules determine the minimum consumption level, which can be used
    in conjunction with desired spending rules to ensure a basic standard of living.
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
        return self.calculate_floor(wealth, time_step, **kwargs)

    @abstractmethod
    def calculate_floor(
        self, wealth: torch.Tensor, time_step: int, **kwargs
    ) -> torch.Tensor:
        """
        Calculate consumption floor for this time step.

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
            Consumption floor for this time step, shape (n_sims,)
        """
        pass


class NoConsumptionFloor(ConsumptionFloor):
    """No consumption floor. Default."""

    def calculate_floor(
        self, wealth: torch.Tensor, time_step: int, **kwargs
    ) -> torch.Tensor:
        return torch.zeros_like(wealth[:, time_step])


class FixedRealFloor(ConsumptionFloor):
    """
    Fixed real consumption floor, adjusted for inflation.

    Parameters
    ----------
    init_floor : float
        Annual consumption floor in year-0 real terms
    adjust_init_floor_for_inflation : bool
        Whether to adjust initial floor from year 0 to t_0

    Examples
    --------
    >>> floor = FixedRealFloor(init_floor=30_000)
    """

    def __init__(
        self,
        init_floor: float,
        adjust_init_floor_for_inflation: bool = True,
        t_0: int = 0,
        t_end: Optional[int] = None,
    ):
        super().__init__(t_0=t_0, t_end=t_end)
        self.init_floor = init_floor
        self.adjust_init_floor_for_inflation = adjust_init_floor_for_inflation

    def calculate_floor(
        self,
        wealth: torch.Tensor,
        time_step: int,
        cumulative_inflation: torch.Tensor,
        **kwargs,
    ) -> torch.Tensor:
        if self.adjust_init_floor_for_inflation:
            nominal_init_floor = self.init_floor * get_inflation_since(
                0, self.t_0, cumulative_inflation
            )
        else:
            nominal_init_floor = self.init_floor
        floor = nominal_init_floor * get_inflation_since(self.t_0, time_step, cumulative_inflation)
        return floor


class DecliningRealFloor(FixedRealFloor):
    """
    Real consumption floor declining at constant rate.

    S(t) = S_0 * (1 - decline_rate)^t

    Reflects empirical pattern in retirement (Le 2023, RIIG 2024).

    Parameters
    ----------
    init_floor : float
        Initial consumption floor in year-0 real terms
    decline_rate : float
        Annual real decline rate (e.g., 0.02 for 2%)
    adjust_for_inflation : bool
        Whether to adjust the floor for inflation

    Examples
    --------
    >>> floor = DecliningRealFloor(init_floor=30_000, decline_rate=0.02)
    """

    def __init__(
        self,
        init_floor: float,
        decline_rate: float = 0.02,
        adjust_for_inflation: bool = True,
        t_0: int = 0,
        t_end: Optional[int] = None,
    ):
        super().__init__(
            init_floor=init_floor,
            adjust_init_floor_for_inflation=adjust_for_inflation,
            t_0=t_0,
            t_end=t_end,
        )
        self.decline_rate = decline_rate
    
    def calculate_floor(
        self,
        wealth: torch.Tensor,
        time_step: int,
        cumulative_inflation: torch.Tensor,
        **kwargs,
    ) -> torch.Tensor:
        floor = super().calculate_floor(wealth, time_step, cumulative_inflation)
        elapsed = time_step - self.t_0
        declining_floor = floor * ((1 - self.decline_rate) ** elapsed)
        return declining_floor


class CompositeFloor(ConsumptionFloor):
    """
    Combine multiple consumption floors.

    Parameters
    ----------
    floors : List[ConsumptionFloor]
        Consumption floors to combine (take maximum)

    Examples
    --------
    >>> floor1 = FixedRealFloor(init_floor=30_000)
    >>> floor2 = DecliningRealFloor(init_floor=40_000, decline_rate=0.02)
    >>> composite_floor = CompositeFloor([floor1, floor2])
    """

    def __init__(
        self, floors: List[ConsumptionFloor], t_0: int = 0, t_end: Optional[int] = None
    ):
        if not floors:
            raise ValueError("Must provide at least one consumption floor")
        self.floors = floors
        self.t_0 = t_0
        self.t_end = t_end

    def calculate_floor(
        self,
        wealth: torch.Tensor,
        time_step: int,
        cumulative_inflation: torch.Tensor,
        **kwargs,
    ) -> torch.Tensor:
        floor_values = torch.stack(
            [floor.calculate(wealth, time_step, cumulative_inflation=cumulative_inflation, **kwargs) for floor in self.floors]
        )
        return torch.max(floor_values, dim=0).values  # Take maximum of all floors
