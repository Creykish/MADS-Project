"""
Constants for New Zealand retirement spending and income.

Based on thesis Section 2.2 "Retirement in New Zealand".
"""

import torch

# ==================== NZ Super and Expenditure Constants ====================

# NZ Super 2025/26 rates (after-tax, annual)
NZ_SUPER_SINGLE = 28_900.0  # Single person living alone
NZ_SUPER_SINGLE_SHARING = 26_700.0  # Single person sharing
NZ_SUPER_COUPLE = 44_400.0  # Couple combined

NZ_SUPER_ELIGIBILITY_AGE = 65  # Age when NZ Super begins

# Winter Energy Payment (annual)
WINTER_ENERGY_SINGLE = 1_064.0  # $20.46/week * 52 weeks
WINTER_ENERGY_COUPLE = 1_655.0  # $31.82/week * 52 weeks

# Retirement Expenditure Guidelines 2025 (annual)
# Source: Matthews (2025) - NZ Fin-Ed Centre, Massey University
EXPENDITURE_GUIDELINES = {
    # Singles
    "no_frills_provincial_single": 32_000.0,
    "no_frills_metro_single": 38_400.0,
    "choices_provincial_single": 47_700.0,
    "choices_metro_single": 52_800.0,
    # Couples
    "no_frills_provincial_couple": 48_300.0,
    "no_frills_metro_couple": 57_100.0,
    "choices_provincial_couple": 79_100.0,
    "choices_metro_couple": 92_600.0,
}


def get_inflation_since(
    t_0: int,
    t: int,
    cumulative_inflation: torch.Tensor,
) -> torch.Tensor:
    """
    Get cumulative inflation multiplier from time t_0 to t.

    Parameters
    ----------
    t_0 : int
        Starting time step (e.g., 0)
    t : int
        Current time step
    cumulative_inflation : torch.Tensor
        Cumulative inflation multipliers, shape (n_sims, n_timesteps)

    Returns
    -------
    torch.Tensor
        Inflation multiplier from t_0 to t, shape (n_sims,)
    """
    if t < t_0:
        raise ValueError("t must be >= t_0")
    return cumulative_inflation[:, t] / cumulative_inflation[:, t_0]
