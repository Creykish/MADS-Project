The theoretically optimal [[Life-cycle Asset Allocation]] depends on the investor's wealth level and the current state of the business cycle, not just their age. Age-only rules like [[Target Date Funds]] and [[Age in Bonds Rule]] miss these dimensions entirely.

## Evidence from Parker et al (2024)

[[Parker et al - Simple Allocation Rules and Optimal Portfolio Choice]] solves the lifecycle model using deep reinforcement learning (policy gradient), allowing optimal allocation to vary with 20+ state variables:

**Wealth heterogeneity (key finding):**
- 90th percentile household by wealth: holds ~**100% stocks** at essentially all ages
- 10th percentile household by wealth: holds <**20% stocks** in retirement
- Wealthier households can afford more equity: even a large drawdown still leaves them above the [[Consumption Floor]]
- Poorer households near the floor cannot absorb losses -> shift to capital preservation

**Business cycle state:**
- Expansion state -> more equities (higher expected returns, lower uncertainty)
- Recession state -> less equities
- This is a first-order effect that simple age rules miss entirely

**Return predictability (dividend-price ratio):**
- High D/P ratio -> higher expected future returns -> buy more equities
- Low D/P ratio -> lower expected future returns -> reduce equity
- See [[Return Predictability]]

## Evidence from Makinen & Toivanen (2024)

[[Makinen - Monte Carlo Optimisation]] uses Monte Carlo + quasi-Newton optimization:
- Wealth-responsive policy >> time-only policy in terms of objective function value
- Optimal allocation at any age is a function of both time AND current wealth
- Models parameterize policy as p_i(t, W) -> 2D policy surface is needed
- Both upside and downside wealth changes warrant allocation adjustments

## Implication for Simple Rules

[[Target Date Funds]] allocate based on age only. The Parker result shows this ignores:
1. Whether you're rich or poor relative to your consumption floor
2. Whether the economy is expanding or contracting
3. Whether current valuations imply good or bad forward returns

The average TDF roughly tracks the *average* optimal policy. But there is enormous dispersion around that average - especially at retirement age.

## NZ Context

NZ retirees have a strong universal [[Consumption Floor]] (NZ Super). This effectively makes most NZ retirees act like "wealthy" households in the Parker framework:
- Even if financial portfolio -> 0, NZ Super remains
- -> higher optimal equity for more NZ retirees than the average international finding would suggest

## Related
[[Life-cycle Asset Allocation]]\n[[Target Date Funds]]\n[[Return Predictability]]\n[[Human Capital]]\n[[Consumption Floor]]\n[[Pensions & Social Security]]\n[[TDFs Are Too Conservative in Retirement]]\n[[Parker et al - Simple Allocation Rules and Optimal Portfolio Choice]]\n[[Makinen - Monte Carlo Optimisation]]
