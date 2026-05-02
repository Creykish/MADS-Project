from abc import ABC, abstractmethod


class Inflation(ABC):
    """Base class for inflation models."""
    
    @abstractmethod
    def get_multiplier(self, time_step: int) -> float:
        """
        Get inflation multiplier for a given time step.
        
        Parameters
        ----------
        time_step : int
            Current time step
        
        Returns
        -------
        float
            Inflation multiplier for the current time step
        """
        pass

    @abstractmethod
    def get_inflation_rate(self, time_step: int) -> float:
        """
        Get inflation rate for a given time step.
        
        Parameters
        ----------
        time_step : int
            Current time step
        
        Returns
        -------
        float
            Inflation rate for the current time step
        """
        pass


class ConstantInflation(Inflation):
    """Constant inflation model."""
    
    def __init__(self, rate: float):
        """
        Parameters
        ----------
        rate : float
            Constant inflation rate (e.g., 0.03 for 3%)
        """
        self.rate = rate
    
    def get_inflation_rate(self, time_step: int) -> float:
        return self.rate

    def get_multiplier(self, time_step: int) -> float:
        return (1 + self.rate) ** time_step


class VariableInflation(Inflation):

    def __init__(self, rates: list[float]):
        """
        Parameters
        ----------
        rates : list[float]
            List of inflation rates for each time step
        """
        self.rates = rates
    
    def get_inflation_rate(self, time_step: int) -> float:
        if time_step < len(self.rates):
            return self.rates[time_step]
        else:
            raise IndexError("Time step exceeds length of inflation rates list.")

    def get_multiplier(self, time_step: int) -> float:
        multiplier = 1.0
        for t in range(time_step):
            multiplier *= (1 + self.get_inflation_rate(t))
        return multiplier

