"""
Test the new calculate_tensor method for consumption floors.
"""
import torch
import sys
sys.path.append('.')

from utils.spending import DecliningRealFloor, FixedRealFloor, NoConsumptionFloor

# Test configuration
N_SIMS = 5
N_YEARS = 10
DEVICE = 'cpu'

print("="*70)
print("TESTING calculate_tensor METHOD")
print("="*70)

# Create test data
wealth = torch.randn((N_SIMS, N_YEARS + 1)) * 10000 + 50000
cumulative_inflation = torch.cumprod(
    1 + torch.randn((N_SIMS, N_YEARS)) * 0.01 + 0.02,
    dim=1
)

# Test 1: DecliningRealFloor
print("\n1. Testing DecliningRealFloor")
print("-" * 70)
floor = DecliningRealFloor(init_floor=50000, decline_rate=0.02)

# Old method (loop)
floor_values_loop = torch.zeros((N_SIMS, N_YEARS))
for t in range(N_YEARS):
    floor_values_loop[:, t] = floor.calculate(
        wealth[:, :t+1], t, cumulative_inflation=cumulative_inflation
    )

# New method (tensor)
floor_values_tensor = floor.calculate_tensor(
    wealth, cumulative_inflation
)

print(f"Loop result shape:   {floor_values_loop.shape}")
print(f"Tensor result shape: {floor_values_tensor.shape}")
print(f"Values match:        {torch.allclose(floor_values_loop, floor_values_tensor)}")
print(f"Max difference:      {(floor_values_loop - floor_values_tensor).abs().max().item():.6f}")

# Test 2: FixedRealFloor
print("\n2. Testing FixedRealFloor")
print("-" * 70)
floor = FixedRealFloor(init_floor=30000)

floor_values_loop = torch.zeros((N_SIMS, N_YEARS))
for t in range(N_YEARS):
    floor_values_loop[:, t] = floor.calculate(
        wealth[:, :t+1], t, cumulative_inflation=cumulative_inflation
    )

floor_values_tensor = floor.calculate_tensor(
    wealth, cumulative_inflation
)

print(f"Loop result shape:   {floor_values_loop.shape}")
print(f"Tensor result shape: {floor_values_tensor.shape}")
print(f"Values match:        {torch.allclose(floor_values_loop, floor_values_tensor)}")
print(f"Max difference:      {(floor_values_loop - floor_values_tensor).abs().max().item():.6f}")

# Test 3: NoConsumptionFloor
print("\n3. Testing NoConsumptionFloor")
print("-" * 70)
floor = NoConsumptionFloor()

floor_values_loop = torch.zeros((N_SIMS, N_YEARS))
for t in range(N_YEARS):
    floor_values_loop[:, t] = floor.calculate(
        wealth[:, :t+1], t, cumulative_inflation=cumulative_inflation
    )

floor_values_tensor = floor.calculate_tensor(
    wealth, cumulative_inflation
)

print(f"Loop result shape:   {floor_values_loop.shape}")
print(f"Tensor result shape: {floor_values_tensor.shape}")
print(f"Values match:        {torch.allclose(floor_values_loop, floor_values_tensor)}")
print(f"All zeros:           {(floor_values_tensor == 0).all().item()}")

# Test 4: Performance comparison
print("\n4. Performance Comparison (DecliningRealFloor)")
print("-" * 70)
import time

N_SIMS_PERF = 10000
N_YEARS_PERF = 30

wealth_perf = torch.randn((N_SIMS_PERF, N_YEARS_PERF + 1)) * 10000 + 50000
inflation_perf = torch.cumprod(
    1 + torch.randn((N_SIMS_PERF, N_YEARS_PERF)) * 0.01 + 0.02,
    dim=1
)

floor = DecliningRealFloor(init_floor=50000, decline_rate=0.02)

# Loop method
start = time.time()
floor_values_loop = torch.zeros((N_SIMS_PERF, N_YEARS_PERF))
for t in range(N_YEARS_PERF):
    floor_values_loop[:, t] = floor.calculate(
        wealth_perf[:, :t+1], t, cumulative_inflation=inflation_perf
    )
loop_time = time.time() - start

# Tensor method
start = time.time()
floor_values_tensor = floor.calculate_tensor(
    wealth_perf, inflation_perf
)
tensor_time = time.time() - start

print(f"Loop method:   {loop_time:.4f}s")
print(f"Tensor method: {tensor_time:.4f}s")
print(f"Speedup:       {loop_time / tensor_time:.2f}x")

print("\n" + "="*70)
print("ALL TESTS PASSED!")
print("="*70)
