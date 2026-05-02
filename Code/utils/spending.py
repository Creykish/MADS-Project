"""
Spending/consumption policies for retirement.

Different strategies for determining retirement spending:
- PercentageOfWealth: Simple percentage rule (e.g., 4% rule)
- FloorCeilingSpending: Percentage with minimum floor and optional ceiling
- PensionPlusPercentage: Fixed pension income plus variable spending
"""

import torch
from typing import Optional
from abc import ABC, abstractmethod


class SpendingPolicy(ABC):
    """Base class for spending policies."""
    
    @abstractmethod
    def calculate_spending(
        self,
        wealth: torch.Tensor,
        time_step: int,
        **kwargs
    ) -> torch.Tensor:
        """
        Calculate spending for current period.
        
        Parameters
        ----------
        wealth : torch.Tensor
            Current wealth
        time_step : int
            Current time step
        
        Returns
        -------
        torch.Tensor
            Spending amount
        """
        pass


class PercentageOfWealth(SpendingPolicy):
    """Spend a fixed percentage of current wealth."""
    
    def __init__(self, rate: float):
        """
        Parameters
        ----------
        rate : float
            Percentage to spend (e.g., 0.04 for 4%)
        """
        self.rate = rate
    
    def calculate_spending(self, wealth: torch.Tensor, time_step: int, **kwargs) -> torch.Tensor:
        spending = wealth * self.rate
        return torch.minimum(spending, wealth)  # Can't spend more than you have


class PercentageOfInitialWealth(SpendingPolicy):
    """Spend a percentage of initial wealth, adjusted for inflation."""
    
    def __init__(self, rate: float, initial_wealth: float, inflation: float = 0.03):
        """
        Parameters
        ----------
        rate : float
            Percentage to spend (e.g., 0.04 for 4%)
        initial_wealth : float
            Initial wealth at time step 0
        inflation : float
            Annual inflation rate
        """
        self.rate = rate
        self.initial_wealth = initial_wealth
        self.inflation = inflation
    
    def calculate_spending(self, wealth: torch.Tensor, time_step: int, **kwargs) -> torch.Tensor:
        # Adjust initial wealth for inflation
        adjusted_initial_wealth = self.initial_wealth * ((1 + self.inflation) ** time_step)
        spending = adjusted_initial_wealth * self.rate
        return torch.minimum(spending, wealth)  # Can't spend more than you have


class FloorCeilingSpending(SpendingPolicy):
    """Spend percentage of wealth with a floor and optional ceiling."""
    
    def __init__(
        self,
        rate: float,
        floor_real: float,
        inflation: float = 0.03,
        real_decline_rate: float = 0.0,
        ceiling_real: Optional[float] = None
    ):
        """
        Parameters
        ----------
        rate : float
            Target spending rate as % of wealth
        floor_real : float
            Minimum spending in real terms (year 0)
        inflation : float
            Annual inflation rate
        real_decline_rate : float
            Annual decline in real spending needs
        ceiling_real : Optional[float]
            Maximum spending in real terms (year 0)
        """
        self.rate = rate
        self.floor_real = floor_real
        self.inflation = inflation
        self.real_decline_rate = real_decline_rate
        self.ceiling_real = ceiling_real
    
    def calculate_spending(self, wealth: torch.Tensor, time_step: int, **kwargs) -> torch.Tensor:
        # Adjust floor for real decline and inflation
        real_floor = self.floor_real * ((1 - self.real_decline_rate) ** time_step)
        nominal_floor = real_floor * ((1 + self.inflation) ** time_step)
        
        # Percentage-based spending
        percentage_spending = wealth * self.rate
        
        # Apply floor
        spending = torch.maximum(
            torch.full_like(wealth, nominal_floor),
            percentage_spending
        )
        
        # Apply ceiling if specified
        if self.ceiling_real is not None:
            real_ceiling = self.ceiling_real * ((1 - self.real_decline_rate) ** time_step)
            nominal_ceiling = real_ceiling * ((1 + self.inflation) ** time_step)
            spending = torch.minimum(spending, torch.full_like(wealth, nominal_ceiling))
        
        # Can't spend more than available
        spending = torch.minimum(spending, wealth)
        
        return spending


class PensionPlusPercentage(SpendingPolicy):
    """Fixed pension income plus percentage of wealth spending."""
    
    def __init__(
        self,
        pension_real: float,
        wealth_rate: float = 0.0,
        inflation: float = 0.03,
        pension_start_age: int = 65,
        current_age_at_t0: int = 65
    ):
        """
        Parameters
        ----------
        pension_real : float
            Annual pension income in real terms
        wealth_rate : float
            Additional spending as % of wealth
        inflation : float
            Annual inflation rate
        pension_start_age : int
            Age when pension starts
        current_age_at_t0 : int
            Age at time step 0
        """
        self.pension_real = pension_real
        self.wealth_rate = wealth_rate
        self.inflation = inflation
        self.pension_start_age = pension_start_age
        self.current_age_at_t0 = current_age_at_t0
    
    def calculate_spending(self, wealth: torch.Tensor, time_step: int, **kwargs) -> torch.Tensor:
        current_age = self.current_age_at_t0 + time_step
        
        # Pension component (inflation-adjusted)
        if current_age >= self.pension_start_age:
            pension = self.pension_real * ((1 + self.inflation) ** time_step)
        else:
            pension = 0.0
        
        # Wealth-based component
        wealth_spending = wealth * self.wealth_rate
        
        # Total spending
        spending = wealth_spending + pension
        
        # Can't spend more than wealth + pension
        spending = torch.minimum(spending, wealth + pension)
        
        return spending
