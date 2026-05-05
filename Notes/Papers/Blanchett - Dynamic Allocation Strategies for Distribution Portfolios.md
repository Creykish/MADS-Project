## Reference
```
@article{blanchett2007dynamic,
  author  = {Blanchett, David M.},
  title   = {Dynamic Allocation Strategies for Distribution Portfolios: Determining the Optimal Distribution Glide Path},
  journal = {Journal of Financial Planning},
  year    = {2007},
  volume  = {20},
  number  = {12},
  pages   = {68--81}
}
```

## Why This Paper

Tests 43 different distribution glide paths (static + 4 types of declining-equity dynamics) across 1,071 scenarios (21 distribution periods x 61 withdrawal rates). Introduces the "Success to Variability ratio" as a risk-adjusted metric. Conclusion: **static allocations are remarkably efficient; 60/40 is optimal for most retirees**. Widely cited by Pfau & Kitces (2014) and Estrada (2015) as evidence that static beats dynamic declining-equity strategies.

## Setup

- Data: bootstrapped from 4 asset classes, monthly returns 1927-2006 (80 years, 960 months)
  - Cash (3-month T-bill)
  - Intermediate-term bond (Moody's Aaa, 10-year duration)
  - Domestic large-blend equity (Fama-French Big Neutral)
  - International equity (Global Financial Data World ex-USA)
- Portfolio: fixed ratio between categories (cash:bonds = 50:50; domestic:intl equity = 67:33); equity allocation is the single decision variable
- Real returns (CPI-U adjusted); geometric returns used (not arithmetic)
- Annual withdrawal at start of year; portfolio rebalanced monthly
- 10,000 MC runs per scenario; pure bootstrapping (no distributional assumptions)
- Distribution periods: 20-40 years (1-year increments)
- Real withdrawal rates: 3-8% (0.1% increments)
- Total: 43 glide paths x 1,071 scenarios = 10,000 runs each = 450 million total simulations

**Glide paths tested:**
| Type | Description |
|---|---|
| Constant | Fixed equity % for entire period (11 variants: 0/100 to 100/0 in 10pp steps) |
| Linear | Equity decreases 1%/year throughout retirement |
| Stair | Equity decreases 10% every 10 years |
| Concave | Equity decreases fast early, then increasingly slowly (convex shape downward) |
| Convex | Equity decreases slowly early, then increasingly fast |

All dynamic strategies only reduce equity (no rising paths tested - this predates Pfau & Kitces 2014).

## Key Results

### Static beats dynamic
Constant (static) glide paths had the **lowest probability of failure for all but one of the 9 illustrative scenarios** and consistently across the full 1,071 scenarios. The concave shape (used by most real target-date funds) was the best among dynamic strategies, but still lost to static.

### 100/0 equity is best by raw probability of success
The 100% equity static portfolio had the lowest failure probability in the majority of the 1,071 scenarios - particularly for long distribution periods and high withdrawal rates where differences were largest. For short periods and low withdrawal rates, multiple strategies tied at near-zero failure.

**Key observation:** failure probability differences are large only in aggressive scenarios (long + high withdrawal):
- 4% withdrawal, 20-year period: range of failure probabilities across all 43 paths = only 1.56pp
- 6% withdrawal, 40-year period: range = 62.45pp (37.55% to 100%)
-> For conservative scenarios, choice of glide path barely matters; for aggressive scenarios, equity allocation is critical

### The Success to Variability ratio

100/0 equity has ~7x the portfolio standard deviation of 0/100 bonds. Blanchett introduces:

$$\text{Success to Variability Ratio} = \frac{\text{Probability of Success}}{\text{Standard Deviation of Portfolio}}$$

Under this measure:
- 0/100 bonds is optimal for 25% of scenarios (never optimal by raw probability)
- 100/0 equity drops from optimal in 56% of scenarios (by raw prob) to 7% of scenarios (by S/V ratio)
- A balanced ~60/40 portfolio sits in between: good enough success probability without the volatility penalty

### "Humped" withdrawal rate curve at 5% failure tolerance
At a 5% maximum failure rate, the highest sustainable real withdrawal rates came from **balanced portfolios (50/50 and 40/60)**, not 100% equity. At 20% failure tolerance, 100% equity wins. The crossover point depends on acceptable failure probability.

### Concave is best among dynamic strategies
If equity must decline (e.g. client preference), concave shape (like real TDFs: fast initial reduction, slower later) is optimal in 89% of non-static scenarios. The "standard" linear reduction is clearly suboptimal.

### Fees matter a lot
60/40 at 4% withdrawal has 3.58% failure probability. Add 1.5%/year in fees -> effectively a 5.5% withdrawal -> failure probability jumps to **28.99%** (8x higher). Fee drag is a major compounding risk for retirees.

## Conclusion

> "Based on the research conducted for this paper, as well as other qualitative and practical considerations, the optimal allocation for most retirees is likely a balanced portfolio, such as a 60 percent equity and 40 percent fixed income/cash allocation."

## Relationship to Other Papers

- Supports [[Estrada - The Retirement Glidepath]] (2015): static 60/40 beats declining-equity glide paths in retirement drawdown
- Partially supports [[Pfau & Kitces - Reducing Retirement Risk with a Rising Equity Glide Path]] (2014): Pfau & Kitces cite Blanchett as finding "fixed asset allocations provided superior results compared to approaches that reduce allocation to equities later in retirement" - consistent. But Blanchett doesn't test rising-equity paths, which Pfau & Kitces argue would be even better.
- Does not test rising-equity (RE) paths at all -> can't speak to the Pfau & Kitces RE recommendation
- Higher equity -> lower failure probability is consistent with [[All-equity Portfolios Outperform Glidepaths at Long Horizons]], but tempered by the S/V ratio argument (100/0 too volatile for most people)
- The S/V ratio framework is analogous to a utility argument for moderate risk aversion -> connects to [[Investor Risk Perception]]

## Findings
[[Declining-risk Strategies are sub-optimal]]
