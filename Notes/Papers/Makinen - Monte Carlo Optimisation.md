## Reference

Mäkinen, R. A. E., & Toivanen, J. (2024). Monte Carlo expected wealth and risk measure trade-off portfolio optimization. *SIAM Journal on Financial Mathematics*, forthcoming.

## Why This Paper

My methodological foundation. Shows how to optimize dynamic wealth-responsive policies using MC + quasi-Newton. Exactly what I'm doing for NZ retirement.

## The Method

**DP sucks:**
- Solve Bellman backwards on grids
- Curse of dimensionality kills you with many state variables

**Their way (mine too):**
1. Parameterize policy: $p_i(t, W)$ (allocation as function of time & wealth)
2. Simulate K MC paths forward
3. Compute objective: $E[W_T] - \lambda Var[W_T]$ 
4. Get gradient (they use adjoint method)
5. Update params with BFGS
6. Repeat

Validates my approach - shows it converges, handles constraints, scales to multiple assets.

## Gradients

**Problem:** Need $\nabla_{\theta} J$ without re-simulating for every parameter.

**Their solution:** Derive analytical adjoint equations. Cost ~2x forward sim instead of Nx.

**My solution:** Just use PyTorch autograd. Mäkinen overstates autodiff inefficiency - works fine for 2-3 assets. Way simpler than deriving adjoint equations.

## Objectives

Test mean-variance vs mean-semivariance:

$E[W_T] - \lambda Var[W_T]$ vs $E[W_T] - \lambda Semivar[W_T]$

Semivariance = only penalize downside: $E[(W - \bar{W})^2 \cdot \mathbb{1}_{W < \bar{W}}]$

Result: Semivar slightly more aggressive (tolerates upside vol), but similar frontiers. Semivar more sensible theoretically.

## Key Result: Time AND Wealth Matter

**Time:** Early = aggressive, late = conservative

**Wealth:** High = conservative (hit target), low = aggressive (need growth)

**Their parameterization:** $p_i(t, W) = \sum_{j,k} \theta_{ijk} t^j W^k$ (polynomial)

**For me:** Could use polynomial, piecewise linear, or logit: $\frac{1}{1+e^{-(\theta_0 + \theta_1 \cdot age + \theta_2 \cdot W + ...)}}$

Wealth-responsive >> time-only policies.

## Constraints

Handle with L-BFGS-B (box constraints on params):
- No short-selling: $p_i \geq 0$
- No leverage: $\sum p_i \leq 1$
- Budget constraint built into sim

All stuff I need too.

## Performance

**Scale:**
- 5 assets, 40 periods, 50k paths
- ~50-100 params (poly degree 3 in time, 2 in wealth)
- Converges in 50-200 iterations
- **Minutes on workstation**

DP would be infeasible at this scale (curse of dimensionality).

For my problem (single/couple, age 25-100, 2-3 assets): should solve fast. MC sim is bottleneck, not optimization.

## Key Equations

**Wealth evolution:**
$$ W_{n+1} = W_n (1 + r) + W_n \sum_i p_i(t_n, W_n)(\mu_i - r) + W_n \sum_i p_i(t_n, W_n) \sigma_i Z_i^n $$

**Objective:**
$$ \max_p \quad \frac{1}{K} \sum_k W_k(T) - \lambda \left( \frac{1}{K} \sum_k (W_k(T) - \bar{W})^2 \right) $$

## My Implementation

**Use PyTorch autograd** instead of deriving adjoint (simpler, works fine for 2-3 assets)

**Optimizer:** scipy.optimize.minimize with L-BFGS-B or PyTorch optimizer

**Policy:** Control matrix or logit function of (age, wealth)

**Paths:** Start 10k-50k, increase if noisy

**Validation:** Try different initializations to check convergence

This paper = my methodological template.

## Related

[[Parker et al - Simple Allocation Rules and Optimal Portfolio Choice]] - deep RL version
[[Cocco - Consumption and Portfolio Choice over the Life Cycle]] - traditional DP approach  
[[Merton - Lifetime Portfolio Selection under Uncertainty]] - analytical continuous-time solution