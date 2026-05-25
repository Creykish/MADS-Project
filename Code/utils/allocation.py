"""
Asset allocation policies for retirement portfolios.

Implements asset allocation policy classes as described in Section 4.1.2 of the thesis.
All policies satisfy the constraints in Equation 13: allocations are non-negative,
sum to at most 1.0, with residual allocated to the safe asset (index 0).

Different strategies for determining portfolio allocation:
- ConstantAllocation: Fixed allocation (static policy)
- TimeBasedPolicy: Age-based glidepath with linear interpolation (Equation 14)
- WealthBasedPolicy: Wealth-dependent allocation with linear interpolation
- ControlMatrixPolicy: 2D time x wealth control surface with bilinear interpolation
  (Mäkinen & Toivanen, 2024)

References
----------
Mäkinen, R. A. E., & Toivanen, J. (2024). Monte carlo expected wealth and 
    risk measure trade-off portfolio optimization. SIAM Journal on Financial Mathematics.
"""

import torch
from abc import ABC, abstractmethod


def project_onto_simplex(x: torch.Tensor, epsilon: float = 1e-8) -> torch.Tensor:
    """
    Project allocations onto the constraint set (Equation 13).
    
    Enforces: x >= 0 and sum(x) <= 1.0
    Uses simplex projection to find the closest feasible point.
    
    Parameters
    ----------
    x : torch.Tensor
        Allocation tensor to project. Can be any shape (..., n_assets-1)
        representing risky asset allocations only.
    epsilon : float, optional
        Small buffer to ensure sum is strictly < 1.0 (default: 1e-8)
        
    Returns
    -------
    torch.Tensor
        Projected allocations satisfying constraints.
        
    Notes
    -----
    This implements Euclidean projection onto the simplex:
        argmin ||y - x||^2  s.t.  y >= 0, sum(y) <= 1
        
    Algorithm from Duchi et al. (2008) "Efficient Projections onto the L1-Ball"
    adapted for the <= 1 constraint rather than == 1.
    """
    original_shape = x.shape
    x_flat = x.reshape(-1, x.shape[-1])  # Flatten to (batch, n_assets-1)
    
    projected = torch.zeros_like(x_flat)
    
    for i in range(x_flat.shape[0]):
        xi = x_flat[i]
        
        # If already feasible, return as-is
        if (xi >= 0).all() and xi.sum() <= 1.0:
            projected[i] = xi
            continue
        
        # Sort in descending order
        sorted_x, _ = torch.sort(xi, descending=True)
        
        # Find the threshold
        cumsum = torch.cumsum(sorted_x, dim=0)
        k_array = torch.arange(1, len(sorted_x) + 1, device=x.device, dtype=x.dtype)
        
        # For sum <= 1 constraint, target is 1 - epsilon
        target = 1.0 - epsilon
        condition = sorted_x - (cumsum - target) / k_array > 0
        
        if condition.any():
            k = torch.where(condition)[0][-1] + 1
            threshold = (cumsum[k-1] - target) / k
            projected[i] = torch.clamp(xi - threshold, min=0.0)
        else:
            # If all negative, project to zero
            projected[i] = torch.zeros_like(xi)
    
    return projected.reshape(original_shape)


def project_simple(x: torch.Tensor, epsilon: float = 1e-8) -> torch.Tensor:
    """
    Simple projection onto constraint set (fast approximation).
    
    Enforces: x >= 0 and sum(x) <= 1.0
    Uses simple clipping and rescaling.
    
    Parameters
    ----------
    x : torch.Tensor
        Allocation tensor to project
    epsilon : float, optional
        Small buffer to ensure sum is strictly < 1.0
        
    Returns
    -------
    torch.Tensor
        Projected allocations satisfying constraints.
        
    Notes
    -----
    This is faster but less accurate than project_onto_simplex.
    Steps:
    1. Clip negative values to 0
    2. If sum > 1, scale down: x = x / sum(x) * (1 - epsilon)
    
    Good for optimization where exact projection is less critical.
    """
    # Clip negative values
    x_proj = torch.clamp(x, min=0.0)
    
    # Scale down if sum exceeds 1
    sums = x_proj.sum(dim=-1, keepdim=True)
    scale = torch.where(
        sums > 1.0,
        (1.0 - epsilon) / sums,
        torch.ones_like(sums)
    )
    
    return x_proj * scale


class AllocationPolicy(ABC):
    """Base class for allocation policies."""

    def __init__(
        self, n_assets: int, n_sims: int, device: torch.device = torch.device("cpu")
    ):
        """
        Parameters
        ----------
        n_assets : int
            Total number of assets (including safe asset at index 0)
        n_sims : int
            Number of simulation paths
        """
        self.n_assets = n_assets
        self.n_sims = n_sims
        self.device = device

    @abstractmethod
    def get_allocation(self, **kwargs) -> torch.Tensor:
        pass


class ConstantAllocation(AllocationPolicy):
    """Constant allocation regardless of time or wealth.
    
    Implements a static allocation policy where the allocation to each asset
    remains fixed across all time periods and wealth levels.
    """

    def __init__(
        self,
        n_assets: int,
        n_sims: int,
        device: torch.device = torch.device("cpu"),
    ):
        """
        Parameters
        ----------
        n_assets : int
            Total number of assets (including safe asset at index 0)
        n_sims : int
            Number of simulation paths
        device : torch.device, optional
            Device for tensor operations
        """
        super().__init__(n_assets, n_sims, device)

    def get_allocation(self, policy_settings: torch.Tensor, **kwargs) -> torch.Tensor:
        """Return the same allocation for all simulations.
        
        Parameters
        ----------
        policy_settings : torch.Tensor
            1D tensor of length (n_assets-1) specifying risky asset allocations.
            Safe asset (index 0) receives residual: 1 - sum(risky allocations).
            
        Returns
        -------
        torch.Tensor
            Shape (n_sims, n_assets) with constant allocation across all paths.
        """
        assert policy_settings.shape == torch.Size(
            [self.n_assets - 1]
        ), "Allocation must be a 1D tensor of length n_assets - 1 (risky assets only)"
        assert (policy_settings >= 0).all(), "All allocations must be non-negative (Equation 13)"
        assert policy_settings.sum() <= 1.0, "Sum of allocations cannot exceed 1.0 (Equation 13)"

        self.allocation = torch.zeros(self.n_assets, device=self.device)
        self.allocation[1:] = policy_settings.to(device=self.device)
        self.allocation[0] = 1.0 - self.allocation[1:].sum()
        
        # Validate final allocation satisfies constraints (Equation 13)
        assert torch.allclose(self.allocation.sum(), torch.tensor(1.0)), "Total allocation must sum to 1.0"
        assert (self.allocation >= 0).all(), "Allocations must be non-negative"
        assert (self.allocation <= 1).all(), "Allocations cannot exceed 1.0"

        return self.allocation.unsqueeze(0).expand(self.n_sims, -1)


class TimeBasedPolicy(AllocationPolicy):
    """Time/age-based allocation with linear interpolation between nodes.
    
    Implements age-based glidepath as described in Equation 14: a_t = f(t; θ).
    Uses linear interpolation between discrete policy nodes.
    """

    def __init__(
        self,
        n_assets: int,
        n_sims: int,
        time_nodes: torch.Tensor,
        device: torch.device = torch.device("cpu"),
    ):
        """
        Parameters
        ----------
        n_assets : int
            Total number of assets (including safe asset at index 0)
        n_sims : int
            Number of simulation paths
        time_nodes : torch.Tensor
            Strictly increasing time points corresponding to policy settings
        device : torch.device, optional
            Device for tensor operations
        """
        super().__init__(n_assets, n_sims, device)
        self.time_nodes = time_nodes.to(device=self.device)
        assert torch.all(
            self.time_nodes[1:] > self.time_nodes[:-1]
        ), "Time nodes must be strictly increasing"

    def get_allocation(
        self, t: float | int, policy_settings: torch.Tensor, **kwargs
    ) -> torch.Tensor:
        """Linear interpolation between policy nodes based on time.
        
        Parameters
        ----------
        t : float or int
            Current time index (must be within time_nodes range)
        policy_settings : torch.Tensor
            Shape (n_time_nodes, n_assets-1) specifying risky allocations at each node
            
        Returns
        -------
        torch.Tensor
            Shape (n_sims, n_assets) with interpolated allocation.
        """
        assert (
            t >= self.time_nodes[0] and t <= self.time_nodes[-1]
        ), "Time index out of bounds for policy nodes"
        assert (
            policy_settings.shape[0] == self.time_nodes.shape[0]
        ), "Number of policy nodes must match number of node times"
        assert (
            policy_settings.shape[1] == self.n_assets - 1
        ), "Policy nodes must specify allocations for risky assets only (n_assets - 1)"
        assert (
            (policy_settings >= 0).all() and (policy_settings.sum(dim=1) <= 1.0).all()
        ), "Policy settings must satisfy constraints (Equation 13)"
    
        policy_settings = policy_settings.to(device=self.device)

        allocation = torch.zeros(self.n_assets, device=self.device)
        x_1 = torch.searchsorted(self.time_nodes, t)
        x_0 = x_1 - 1
        y_0 = policy_settings[x_0]
        y_1 = policy_settings[x_1]
        alpha = (t - self.time_nodes[x_0]) / (
            self.time_nodes[x_1] - self.time_nodes[x_0]
        )
        risky_alloc = (1 - alpha) * y_0 + alpha * y_1
        allocation[1:] = risky_alloc
        allocation[0] = 1 - allocation[1:].sum()
        
        # Validate interpolated allocation satisfies constraints
        assert (allocation >= 0).all(), "Interpolated allocation must be non-negative"
        assert allocation.sum() <= 1.0 + 1e-6, "Interpolated allocation must sum to at most 1.0"
        
        return allocation.unsqueeze(0).expand(self.n_sims, -1)


class WealthBasedPolicy(AllocationPolicy):
    """Wealth-based allocation policy with linear interpolation between nodes.
    
    Allocation depends on current wealth level, with linear interpolation
    between discrete wealth nodes.
    """

    def __init__(
        self,
        n_assets: int,
        n_sims: int,
        wealth_nodes: torch.Tensor,
        device: torch.device = torch.device("cpu"),
    ):
        """
        Parameters
        ----------
        n_assets : int
            Total number of assets (including safe asset at index 0)
        n_sims : int
            Number of simulation paths
        wealth_nodes : torch.Tensor
            Strictly increasing wealth levels corresponding to policy settings
        device : torch.device, optional
            Device for tensor operations
        """
        super().__init__(n_assets, n_sims, device)
        self.wealth_nodes = wealth_nodes.to(device=self.device)
        assert torch.all(
            self.wealth_nodes[1:] > self.wealth_nodes[:-1]
        ), "Wealth nodes must be strictly increasing"

    def get_allocation(
        self, wealth: torch.Tensor, policy_settings: torch.Tensor, **kwargs
    ) -> torch.Tensor:
        """Linear interpolation between policy nodes based on wealth.
        
        Parameters
        ----------
        wealth : torch.Tensor
            Current wealth levels, shape (n_sims,)
        policy_settings : torch.Tensor
            Shape (n_wealth_nodes, n_assets-1) specifying risky allocations at each node
            
        Returns
        -------
        torch.Tensor
            Shape (n_sims, n_assets) with interpolated allocation.
        """
        w = wealth.clamp(self.wealth_nodes[0], self.wealth_nodes[-1]).to(
            device=self.device
        )
        assert (
            policy_settings.shape[0] == self.wealth_nodes.shape[0]
        ), "Number of policy nodes must match number of wealth nodes"
        assert (
            policy_settings.shape[1] == self.n_assets - 1
        ), "Policy nodes must specify allocations for risky assets only (n_assets - 1)"
        assert (
            (policy_settings >= 0).all() and (policy_settings.sum(dim=1) <= 1.0).all()
        ), "Policy settings must satisfy constraints (Equation 13)"
        
        x_1 = torch.searchsorted(self.wealth_nodes, w)
        x_0 = x_1 - 1

        y_0 = policy_settings[x_0]
        y_1 = policy_settings[x_1]

        alpha = (w - self.wealth_nodes[x_0]) / (self.wealth_nodes[x_1] - self.wealth_nodes[x_0])
        alpha = alpha.unsqueeze(1)  # Reshape from (n_sims,) to (n_sims, 1) for broadcasting
        risky_alloc = (1 - alpha) * y_0 + alpha * y_1
        
        # Initialize allocation as 2D tensor (n_sims, n_assets)
        allocation = torch.zeros(self.n_sims, self.n_assets, device=self.device)
        allocation[:, 1:] = risky_alloc
        allocation[:, 0] = 1 - allocation[:, 1:].sum(dim=1)

        # Validate interpolated allocation satisfies constraints
        assert (allocation >= 0).all(), "Interpolated allocation must be non-negative"
        assert (allocation.sum(dim=1) <= 1.0 + 1e-6).all(), "Interpolated allocation must sum to at most 1.0"
        
        return allocation


class ControlMatrixPolicy(AllocationPolicy):
    """2D control matrix policy (time x wealth) with bilinear interpolation.
    
    Implements the control matrix approach from Mäkinen & Toivanen (2024).
    Allocation depends jointly on time and wealth, with bilinear interpolation
    between discrete grid points as illustrated in thesis Figure 3.
    """

    def __init__(
        self,
        n_assets: int,
        n_sims: int,
        time_nodes: torch.Tensor,
        wealth_nodes: torch.Tensor,
        device: torch.device = torch.device("cpu"),
    ):
        """
        Parameters
        ----------
        n_assets : int
            Total number of assets (including safe asset at index 0)
        n_sims : int
            Number of simulation paths
        time_nodes : torch.Tensor
            Strictly increasing time points for the control grid
        wealth_nodes : torch.Tensor
            Strictly increasing wealth levels for the control grid
        device : torch.device, optional
            Device for tensor operations
        """
        super().__init__(n_assets, n_sims, device)
        self.time_nodes = time_nodes.to(device=self.device)
        self.wealth_nodes = wealth_nodes.to(device=self.device)
        assert torch.all(
            self.time_nodes[1:] > self.time_nodes[:-1]
        ), "Time nodes must be strictly increasing"
        assert torch.all(
            self.wealth_nodes[1:] > self.wealth_nodes[:-1]
        ), "Wealth nodes must be strictly increasing"

    def get_allocation(
        self,
        t: float | int,
        wealth: torch.Tensor,
        policy_settings: torch.Tensor,
        **kwargs
    ) -> torch.Tensor:
        """Bilinear interpolation between policy nodes based on time and wealth.
        
        Parameters
        ----------
        t : float or int
            Current time index (must be within time_nodes range)
        wealth : torch.Tensor
            Current wealth levels, shape (n_sims,)
        policy_settings : torch.Tensor
            Shape (n_time_nodes, n_wealth_nodes, n_assets-1) specifying the
            control matrix of risky asset allocations
            
        Returns
        -------
        torch.Tensor
            Shape (n_sims, n_assets) with bilinearly interpolated allocation.
        """
        assert (
            t >= self.time_nodes[0] and t <= self.time_nodes[-1]
        ), "Time index out of bounds for policy nodes"
        assert (
            policy_settings.shape[0] == self.time_nodes.shape[0]
        ), "Number of time nodes must match first dimension of policy settings"
        assert (
            policy_settings.shape[1] == self.wealth_nodes.shape[0]
        ), "Number of wealth nodes must match second dimension of policy settings"
        assert (
            policy_settings.shape[2] == self.n_assets - 1
        ), "Policy settings must specify allocations for risky assets only (n_assets - 1)"
        assert (
            wealth.shape == torch.Size([self.n_sims])
        ), "Wealth input must be a 1D tensor of shape (n_sims,)"
        assert (
            (policy_settings >= 0).all() and (policy_settings.sum(dim=2) <= 1.0).all()
        ), "Policy settings must satisfy constraints (Equation 13): non-negative and sum <= 1"

        policy_settings = policy_settings.to(device=self.device)
        
        w = wealth.clamp(self.wealth_nodes[0], self.wealth_nodes[-1]).to(
            device=self.device
        )
        t_ = torch.tensor([t] * self.n_sims, device=self.device)
        t_1 = torch.searchsorted(self.time_nodes, t_)
        t_0 = t_1 - 1
        w_1 = torch.searchsorted(self.wealth_nodes, w)
        w_0 = w_1 - 1

        q_00 = policy_settings[t_0, w_0]
        q_01 = policy_settings[t_0, w_1]
        q_10 = policy_settings[t_1, w_0]
        q_11 = policy_settings[t_1, w_1]

        alpha_t = (t_ - self.time_nodes[t_0]) / (
            self.time_nodes[t_1] - self.time_nodes[t_0]
        )
        alpha_w = (w - self.wealth_nodes[w_0]) / (
            self.wealth_nodes[w_1] - self.wealth_nodes[w_0]
        )

        allocations = (1 - alpha_t).unsqueeze(1) * (
            (1 - alpha_w).unsqueeze(1) * q_00 + alpha_w.unsqueeze(1) * q_01
        ) + alpha_t.unsqueeze(1) * (
            (1 - alpha_w).unsqueeze(1) * q_10 + alpha_w.unsqueeze(1) * q_11
        )
        allocations = torch.cat(
            [1 - allocations.sum(dim=1, keepdim=True), allocations], dim=1
        )
        
        # Validate interpolated allocations satisfy constraints
        assert (allocations >= -1e-6).all(), "Interpolated allocations must be non-negative"
        assert (allocations.sum(dim=1) <= 1.0 + 1e-6).all(), "Interpolated allocations must sum to at most 1.0"
        
        return allocations
