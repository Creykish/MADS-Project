"""
Test script to verify bankruptcy logic is working correctly.
"""
import torch
import sys
sys.path.append('.')

from utils.spending import *
from utils.allocation import *
from utils import simulate_wealth_trajectory

# Test configuration
N_SIMS = 10
N_YEARS = 5
DEVICE = 'cpu'

# Scenario: Low wealth, high spending floor, moderate income
INITIAL_WEALTH = 10_000
INCOME = 44_400  # NZ Super couple
DESIRED = 57_100  # Same as floor (mimicking the bug)
FLOOR = 57_100

print("="*70)
print("TESTING BANKRUPTCY LOGIC")
print("="*70)
print(f"Initial wealth:     ${INITIAL_WEALTH:,}")
print(f"NZ Super income:    ${INCOME:,}/year")
print(f"Desired spending:   ${DESIRED:,}/year")
print(f"Consumption floor:  ${FLOOR:,}/year")
print(f"Expected deficit:   ${INCOME - FLOOR:,}/year (wealth should decline)")
print("="*70)

# Setup policies
desired_spending = DecliningRealSpending(DESIRED, decline_rate=0.0)  # No decline for simplicity
consumption_floor = DecliningRealFloor(init_floor=FLOOR, decline_rate=0.0)
income = NZSuper('couple')

spending_policy = SpendingPolicy(
    spending=desired_spending,
    floor=consumption_floor,
    income=income
)

# Create zero returns (worst case - no growth)
returns = torch.zeros((N_SIMS, N_YEARS, 3))  # 3 assets, 0% returns
cumulative_inflation = torch.ones((N_SIMS, N_YEARS))  # No inflation

# Create allocation policy (doesn't matter with 0 returns)
allocation_policy = ConstantAllocation(3, N_SIMS, DEVICE)
policy = torch.tensor([0.5, 0.5], device=DEVICE, dtype=torch.float32)

# Simulate
wealth, consumption = simulate_wealth_trajectory(
    returns=returns,
    cumulative_inflation=cumulative_inflation,
    allocation_policy=allocation_policy,
    spending_policy=spending_policy,
    initial_wealth=INITIAL_WEALTH,
    policy_settings=policy
)

print("\nRESULTS (first simulation path):")
print("="*70)
for t in range(N_YEARS + 1):
    if t < N_YEARS:
        print(f"Year {t}: Wealth = ${wealth[0, t].item():>10,.0f}, Consumption = ${consumption[0, t].item():>10,.0f}")
    else:
        print(f"Year {t}: Wealth = ${wealth[0, t].item():>10,.0f}")

print("="*70)
print(f"Terminal wealth = $0 count: {(wealth[:, -1] == 0).sum().item()}/{N_SIMS}")
print(f"Bankruptcy rate: {(wealth[:, -1] == 0).sum().item() / N_SIMS:.0%}")
print("="*70)

# Manual calculation for verification
print("\nMANUAL VERIFICATION:")
print("="*70)
w = INITIAL_WEALTH
for t in range(N_YEARS):
    inc = INCOME
    desired = DESIRED
    floor_t = FLOOR
    spending = max(desired, floor_t)
    available = w + inc
    cons = min(spending, available)
    delta_w = inc - cons
    w_after_spending = w + delta_w
    w_next = w_after_spending * (1 + 0)  # 0% return
    
    print(f"Year {t}:")
    print(f"  Wealth before = ${w:,.0f}")
    print(f"  Income        = ${inc:,.0f}")
    print(f"  Available     = ${available:,.0f}")
    print(f"  Consumption   = ${cons:,.0f}")
    print(f"  Delta wealth  = ${delta_w:,.0f}")
    print(f"  Wealth after  = ${w_after_spending:,.0f}")
    print(f"  Wealth next   = ${w_next:,.0f}")
    
    w = w_next

print("="*70)
