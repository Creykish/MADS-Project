## Reference

Merton, R. C. (1969). Lifetime portfolio selection under uncertainty: The continuous-time case. *The Review of Economics and Statistics*, 51(3), 247-257.

Irlam, G. (2018). Lifetime portfolio selection: A simple derivation. *Working Paper*.

## The Big Result

With CRRA utility + lognormal returns, optimal allocation is **constant** and **independent of wealth**.

**Optimal risky share:**

$$ \pi^* = \frac{\mu - r}{\gamma \sigma^2} $$

- $\mu$ = expected return
- $r$ = riskless rate  
- $\gamma$ = risk aversion
- $\sigma$ = volatility

**Myopic:** Depends only on current opportunities, not time horizon or wealth level.

**Example:** $\gamma=2$ means same allocation whether you have $10k or $1M.

## CRRA Utility

$$ U(C) = \frac{C^{1-\gamma}}{1-\gamma} $$

$\gamma$ = coefficient of relative risk aversion:
- $\gamma = 1$: log utility $U(C) = \ln(C)$  
- $\gamma > 1$: risk averse (higher = more averse)
- Typical range: 1-10, literature often uses 2-5

**Key property:** Optimal portfolio share independent of wealth level.

## Optimal Consumption

Constant fraction of wealth: $C_t = \beta W_t$

Where $\beta$ determined by patience, risk aversion, investment opportunities.

**Wealth evolution:**
$$ dW_t = (r + \pi^*(\mu - r))W_t dt + \pi^* \sigma W_t dZ_t - C_t dt $$

**Extensions needed:**
- Labor income → time-varying allocation (Cocco 2005)
- Constraints → numerical DP (Cocco 2005)  
- Housing → more state variables
- Return predictability → intertemporal hedging (Campbell & Viceira 2002)

## Irlam (2018) - Discrete Time Version

Simple discrete-time derivation, no stochastic calculus needed.

**Key insight:** If returns lognormal with mean $m$ and std $s$:

$$ \mu = \ln(m) - \frac{1}{2}\sigma^2, \quad \sigma = \sqrt{\ln(1 + (s/m)^2)} $$

Discrete-time optimal allocation:
$$ \pi^* = \frac{1}{\gamma} \cdot \frac{\ln(1 + \mu_{excess})}{\sigma^2} $$

Converges to Merton's continuous-time result as dt → 0.

Better for calibration (observe annual returns) and easier to explain.

## Why Merton Doesn't Apply to NZ Retirees

1. **Labor income + human capital** → allocation should vary with age
2. **NZ Super** → acts like ~$800k riskless asset → implies high equity in financial portfolio
3. **Can't borrow against future NZ Super** → constraints bind
4. **Consumption declines ~2%/year in retirement** (empirical) → violates constant consumption rule

**What I keep:** CRRA utility, risk-return intuition

**What I add:** Finite lifetime, mortality, age-varying consumption, NZ Super, constraints, numerical solution (MC + optimization)

## Useful Bits

**Calibration check:** My optimization should recover $\pi^* = \frac{\mu-r}{\gamma\sigma^2}$ in simple case (no labor, no NZ Super, no constraints).

**Risk aversion values:**
- $\gamma = 1$: log utility, 50-70% stocks
- $\gamma = 3$: moderate, 40-60% stocks  
- $\gamma = 5$: high aversion, 20-40% stocks

Solve for range $\gamma \in [2, 5]$.

**Return calibration:**
- Historical US stocks: 8% real, 20% vol
- Need NZ data for NZX

**Key equations:**

$U(C) = \frac{C^{1-\gamma}}{1-\gamma}$ 

$\pi^* = \frac{\mu - r}{\gamma \sigma^2}$

$C_t = \beta W_t$

$dW = [(r + \pi(\mu-r))W - C]dt + \pi \sigma W dZ$

## Related

[[Cocco - Consumption and Portfolio Choice over the Life Cycle]] - numerical with labor income
[[Makinen - Monte Carlo Optimisation]] - my computational method
[[Parker et al - Simple Allocation Rules and Optimal Portfolio Choice]] - modern treatment

## Topics
[[Life-cycle Asset Allocation]]
[[Asset Allocation]]
[[Human Capital]]