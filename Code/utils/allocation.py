"""
Asset allocation policies for retirement portfolios.

Different strategies for determining portfolio allocation:
- ConstantAllocation: Fixed allocation
- TimeBasedPolicy: Age-based with interpolated nodes
- ControlMatrixPolicy: 2D time×wealth control surface
"""

import torch
from abc import ABC, abstractmethod


class AllocationPolicy(ABC):
    """Base class for allocation policies."""
    
    @abstractmethod
    def get_allocation(
        self,
        time_idx: torch.Tensor,
        wealth: torch.Tensor,
        **kwargs
    ) -> torch.Tensor:
        """
        Get allocation to risky assets.
        
        Parameters
        ----------
        time_idx : torch.Tensor
            Current time indices
        wealth : torch.Tensor
            Current wealth levels
        
        Returns
        -------
        torch.Tensor
            Allocation to risky asset(s) for each simulation
        """
        pass


class ConstantAllocation(AllocationPolicy):
    """Constant allocation regardless of time or wealth."""
    
    def __init__(self, allocation: float):
        """
        Parameters
        ----------
        allocation : float
            Fixed allocation to risky assets (0-1)
        """
        self.allocation = allocation
    
    def get_allocation(self, time_idx: torch.Tensor, wealth: torch.Tensor, **kwargs) -> torch.Tensor:
        return torch.full_like(wealth, self.allocation)


class TimeBasedPolicy(AllocationPolicy):
    """Time/age-based allocation with linear interpolation between nodes."""
    
    def __init__(self, policy_nodes: torch.Tensor, n_timesteps: int):
        """
        Parameters
        ----------
        policy_nodes : torch.Tensor
            Allocation values at key time points
        n_timesteps : int
            Total number of timesteps
        """
        self.policy_nodes = policy_nodes
        self.n_timesteps = n_timesteps
        self.n_nodes = len(policy_nodes)
    
    def get_allocation(self, time_idx: torch.Tensor, wealth: torch.Tensor, **kwargs) -> torch.Tensor:
        """Linear interpolation between policy nodes."""
        # Node positions evenly spaced across timeline
        node_positions = torch.linspace(
            0, self.n_timesteps - 1, self.n_nodes,
            device=self.policy_nodes.device
        )
        
        result = torch.zeros_like(time_idx)
        
        for i, t in enumerate(time_idx):
            right_idx = torch.searchsorted(node_positions, t, right=True)
            
            if right_idx == 0:
                result[i] = self.policy_nodes[0]
            elif right_idx >= self.n_nodes:
                result[i] = self.policy_nodes[-1]
            else:
                left_idx = right_idx - 1
                left_pos = node_positions[left_idx]
                right_pos = node_positions[right_idx]
                weight = (t - left_pos) / (right_pos - left_pos)
                result[i] = (1 - weight) * self.policy_nodes[left_idx] + weight * self.policy_nodes[right_idx]
        
        return result


class ControlMatrixPolicy(AllocationPolicy):
    """2D control matrix policy (time × wealth) with bilinear interpolation."""
    
    def __init__(
        self,
        control_matrix: torch.Tensor,
        n_timesteps: int,
        max_wealth: float
    ):
        """
        Parameters
        ----------
        control_matrix : torch.Tensor
            Shape (n_time_nodes, n_wealth_nodes)
        n_timesteps : int
            Total number of timesteps in simulation
        max_wealth : float
            Maximum wealth bound for interpolation
        """
        self.control_matrix = control_matrix
        self.n_timesteps = n_timesteps
        self.max_wealth = max_wealth
        self.n_time_nodes, self.n_wealth_nodes = control_matrix.shape
    
    def get_allocation(self, time_idx: torch.Tensor, wealth: torch.Tensor, **kwargs) -> torch.Tensor:
        """Bilinear interpolation over time and wealth dimensions."""
        # Map to grid coordinates
        time_grid_coord = time_idx * (self.n_time_nodes - 1) / (self.n_timesteps - 1)
        wealth_grid_coord = wealth * (self.n_wealth_nodes - 1) / self.max_wealth
        
        # Clamp to valid range
        time_grid_coord = torch.clamp(time_grid_coord, 0, self.n_time_nodes - 1)
        wealth_grid_coord = torch.clamp(wealth_grid_coord, 0, self.n_wealth_nodes - 1)
        
        # Get floor and ceiling indices
        t0 = torch.floor(time_grid_coord).long()
        t1 = torch.clamp(t0 + 1, max=self.n_time_nodes - 1)
        w0 = torch.floor(wealth_grid_coord).long()
        w1 = torch.clamp(w0 + 1, max=self.n_wealth_nodes - 1)
        
        # Fractional parts for interpolation
        t_frac = time_grid_coord - t0.float()
        w_frac = wealth_grid_coord - w0.float()
        
        # Get corner values
        Q00 = self.control_matrix[t0, w0]
        Q01 = self.control_matrix[t0, w1]
        Q10 = self.control_matrix[t1, w0]
        Q11 = self.control_matrix[t1, w1]
        
        # Bilinear interpolation
        result = (
            Q00 * (1 - t_frac) * (1 - w_frac) +
            Q01 * (1 - t_frac) * w_frac +
            Q10 * t_frac * (1 - w_frac) +
            Q11 * t_frac * w_frac
        )
        
        return result
