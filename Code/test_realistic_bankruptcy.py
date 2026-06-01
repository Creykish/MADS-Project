"""
Test with realistic scenario: declining spending + positive returns.
"""
import torch
import numpy as np
import sys
sys.path.append('.')

from utils.spending import *
from utils.allocation import *
from utils import simulate_wealth_trajectory

# Test configuration matching the notebook
N_SIMS = 1000
N_YEARS = 30
DEVICE = 'cpu'

INITIAL_WEALTH = 10_000
INCOME_TYPE = 'couple'
DESIRED = 57_100  # Mimicking the bug where desired = floor
FLOOR = 57_100
DECLINE_RATE = 0.02

print("="*70)
print("REALISTIC BANKRUPTCY TEST")
print("="*70)
print(f"Initial wealth:     ${INITIAL_WEALTH:,}")
print(f"NZ Super (incl WE): ${46_055:,}/year")  
print(f"Initial floor:      ${FLOOR:,}/year")
print(f"Decline rate:       {DECLINE_RATE:.1%}/year")
print("="*70)

# Calculate when floor drops below income
nz_super_total = 46_055
years_to_breakeven = np.log(nz_super_total / FLOOR) / np.log(1 - DECLINE_RATE)
floor_at_30_years = FLOOR * (1 - DECLINE_RATE) ** 30

print(f"\nKEY INSIGHT:")
print(f"  Year 0:  Floor = ${FLOOR:,.0f}, Income = ${nz_super_total:,.0f} → Deficit ${FLOOR - nz_super_total:,.0f}")
print(f"  Year {years_to_breakeven:.1f}: Floor drops to ${nz_super_total:,.0f} → Breakeven!")
print(f"  Year 30: Floor = ${floor_at_30_years:,.0f} → Surplus ${nz_super_total - floor_at_30_years:,.0f}")
print("="*70)

# Setup policies
desired_spending = DecliningRealSpending(DESIRED, decline_rate=DECLINE_RATE)
consumption_floor = DecliningRealFloor(init_floor=FLOOR, decline_rate=DECLINE_RATE)
income = NZSuper(INCOME_TYPE)

spending_policy = SpendingPolicy(
    spending=desired_spending,
    floor=consumption_floor,
    income=income
)

# Test with modest positive returns (3% real on conservative portfolio)
# Simulate a 30/70 stocks/bonds portfolio with ~3% real return
np.random.seed(42)
returns = torch.tensor(
    np.random.normal(0.03, 0.05, (N_SIMS, N_YEARS, 3)),  # 3% mean, 5% std
    dtype=torch.float32
)
cumulative_inflation = torch.ones((N_SIMS, N_YEARS))

# Create allocation policy - conservative portfolio
allocation_policy = ConstantAllocation(3, N_SIMS, DEVICE)
policy = torch.tensor([0.1, 0.2], device=DEVICE, dtype=torch.float32)  # Mostly in safe asset

# Simulate
wealth, consumption = simulate_wealth_trajectory(
    returns=returns,
    cumulative_inflation=cumulative_inflation,
    allocation_policy=allocation_policy,
    spending_policy=spending_policy,
    initial_wealth=INITIAL_WEALTH,
    policy_settings=policy
)

# Analyze results
terminal_wealth = wealth[:, -1]
bankruptcy_rate = (terminal_wealth == 0).sum().item() / N_SIMS
min_wealth = wealth.min(dim=1)[0]  # Minimum wealth across all time steps
ever_bankrupt_rate = (min_wealth == 0).sum().item() / N_SIMS

print("\nRESULTS:")
print("="*70)
print(f"Bankruptcy rate (terminal):       {bankruptcy_rate:.1%}")
print(f"Ever hit zero wealth:             {ever_bankrupt_rate:.1%}")
print(f"Mean terminal wealth:             ${terminal_wealth.mean().item():,.0f}")
print(f"Median terminal wealth:           ${terminal_wealth.median().item():,.0f}")
print("="*70)

# Show wealth trajectory for one path that hit zero
if (min_wealth == 0).any():
    idx = (min_wealth == 0).nonzero()[0].item()
    print(f"\nSample path that hit zero (path {idx}):")
    print("="*70)
    for t in [0, 5, 10, 15, 20, 25, 29]:
        print(f"Year {t:2d}: Wealth = ${wealth[idx, t].item():>10,.0f}, Consumption = ${consumption[idx, t].item():>10,.0f}")
    print(f"Year 30: Wealth = ${wealth[idx, 30].item():>10,.0f}")
    print("="*70)
