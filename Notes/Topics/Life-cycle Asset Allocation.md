Optimal [[Asset Allocation]] varied over time to maximise investor utility. The central question in this research area is: how should the mix of risky and safe assets change as an investor ages?

## Theoretical Foundations

**Merton (1969):** Under IID returns + CRRA utility, optimal risky share is constant:
- pi* = (mu - r) / (gamma * sigma^2)
- Does not depend on age, wealth, or time horizon
- This is the baseline: glidepaths only make sense if IID assumption is violated or other frictions exist
- See [[Merton - Lifetime Portfolio Selection under Uncertainty]]

**Why constant is not the whole story:**
- Labor income adds a large bond-like asset ([[Human Capital]]) -> justifies more equity when young
- Return predictability (dividend yields, business cycles) -> allocation should vary with state variables
- Constraints (no borrowing against NZ Super, short-selling limits)
- Spending needs in retirement -> bequest vs consumption tradeoff

## The Human Capital Argument for Glidepaths

[[Cocco - Consumption and Portfolio Choice over the Life Cycle]] (2005):
- Human capital for a typical worker resembles a long-duration bond (stable, predictable wages)
- Young investor: total wealth = small financial + large human capital -> overall portfolio is "bond heavy"
- To reach optimal overall risk level, financial portfolio should be equity heavy
- As human capital depletes with age, shift financial portfolio toward bonds
- Result: [[Decreasing Equity Strategy]] is optimal in the presence of human capital

[[Merton & Bodie - Labor supply flexibility and portfolio choice in a life cycle model]] (1992):
- Labor flexibility amplifies this: if you can work more/less, you can hedge investment risk via labor supply
- -> greater flexibility -> more risk-taking in financial portfolio
- Risky human capital (e.g., finance worker, entrepreneur) -> hold LESS equity in financial portfolio

## Critique: The Block Bootstrap Challenge

[[Anarkulova et al - Beyond the Status Quo (Critical Assessment of Lifecycle Advice)]] (2025) overturns the conventional glidepath story:

**The IID failure:**
- Standard models use 1-month return statistics: bonds look like good diversifiers
- But at 30-year horizon, bond variance ratio = **2.30** (variance increases!)
- Stock variance ratio = **0.75** at 30 years (variance decreases -> mean reversion)
- Bond/stock correlation rises from ~0.1 (short) to **0.45** (long horizon)
- Bonds are a bad inflation hedge: corr(bonds, inflation) = **-0.78**
- Stocks are inflation neutral: corr(stocks, inflation) = -0.01

**The optimal portfolio with [[Block Bootstrap Returns]]:**
- 33% domestic + 67% international equities
- 0% bonds, 0% bills (constant throughout life)
- Exception: 27% bills at exact age 65 (tactical for withdrawal mechanics)

**Welfare cost of conventional advice:**
- 60/40 balanced: requires **94% more savings** to match utility of 100% equity investor
- Typical TDF: requires **63% more savings**

## Target Date Funds

[[Target Date Funds]] are the most common practical implementation of a lifecycle glidepath. [[Parker et al - Simple Allocation Rules and Optimal Portfolio Choice]] (2024) uses deep reinforcement learning to evaluate them:

- TDFs track average optimal behavior well up to age 50
- After age 50 and especially in retirement: TDFs too conservative
- Optimal equity at retirement: ~60%; TDF at retirement: 30-40%
- Welfare loss from TDF vs optimal: 1.7-2.8% consumption equivalent
- Key missed factor: optimal allocation depends on wealth level and business cycle state, not just age

## The NZ Super Implicit Bond

In New Zealand, [[Pensions & Social Security]] changes the calculation significantly:
- NZ Super = ~$800k present value (single, from age 65, real terms)
- This is already a large bond-like riskless asset in the retiree's implicit portfolio
- -> financial portfolio can lean even more heavily to equity
- Anarkulova: "NZ Super as implicit bonds justifies 100% equity in financial portfolio"
- Combined with [[Consumption Floor]] logic: if worst-case scenario still yields $28k/year from NZ Super, downside risk is bounded -> tolerance for equity volatility rises

## Practical Strategies

| Strategy | Description | Evidence |
|---|---|---|
| [[Age in Bonds Rule]] | % bonds = age (or 120 - age in stocks) | Conventional, challenged by all evidence |
| [[Decreasing Equity Strategy]] | Reduce equity with age | Theoretically grounded in human capital; empirically suboptimal |
| [[Increasing Equity Strategy]] | Increase equity with age | Estrada (2014): outperforms internationally |
| [[100% Stock Portfolio]] | No bonds ever | Anarkulova (2025), Dolvin (2010), Estrada (2014) |
| [[Target Date Funds]] | Age-based glidepath fund | Parker: ok to 50, too conservative after |

## Related Papers
[[Merton - Lifetime Portfolio Selection under Uncertainty]]
[[Cocco - Consumption and Portfolio Choice over the Life Cycle]]
[[Merton & Bodie - Labor supply flexibility and portfolio choice in a life cycle model]]
[[Anarkulova et al - Beyond the Status Quo (Critical Assessment of Lifecycle Advice)]]
[[Parker et al - Simple Allocation Rules and Optimal Portfolio Choice]]
[[Estrada - The Glidepath Illusion]]
[[Dolvin - Asset Allocation for Retirement Simple Heuristics and Target-Date Funds]]
[[Shiller - Life-cycle personal accounts proposal for Social Security]]
[[Makinen - Monte Carlo Optimisation]]

## Related Topics
[[Human Capital]]
[[Pensions & Social Security]]
[[Consumption Floor]]
[[Destitution Risk]]
[[Return Predictability]]
[[Block Bootstrap Returns]]