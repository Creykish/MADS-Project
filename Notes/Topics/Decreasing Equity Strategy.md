A [[Life-cycle Asset Allocation]] strategy that decreases exposure to risky assets (equities) as the investor ages. The most common form of glidepath advice. Implemented via [[Target Date Funds]] and the [[Age in Bonds Rule]].

## Theoretical Justification

**Human capital argument** ([[Cocco - Consumption and Portfolio Choice over the Life Cycle]]):
- Young investor: large [[Human Capital]] (PV of future wages) + small financial wealth
- Human capital = bond-like (stable wages behave like a long-duration bond)
- To achieve target total-portfolio risk, financial portfolio should be equity-heavy when young
- As worker ages -> human capital depletes -> financial portfolio should shift toward bonds
- Result: equity share naturally declines over working life

**Labor flexibility amplifier** ([[Merton & Bodie - Labor supply flexibility and portfolio choice in a life cycle model]]):
- Workers can adjust hours, retire early/late -> creates a labor hedge
- More labor flexibility -> higher financial risk tolerance -> more equity when young
- Risky human capital (volatile job, commission income) -> reduce equity in financial portfolio

## Conventional Implementations

- [[Age in Bonds Rule]]: hold % bonds = age (60-year-old -> 60% bonds)
- "120-minus-age" variant: stocks = 120 - age (60-year-old -> 60% stocks)
- [[Target Date Funds]]: automatic annual rebalancing along a glidepath

Dolvin (2010): most TDFs approximate 120-minus-age and end at 30-40% equity at retirement.

## Criticisms and Failures

**[[Declining-risk Strategies are sub-optimal]]:**

1. **[[Estrada - The Glidepath Illusion]] (2014):** Studied 19 countries with historical data. [[Increasing Equity Strategy]] outperforms decreasing in 19/19 countries on terminal wealth. The "glidepath illusion" = investors think declining risk is safer, but it produces worse outcomes.

2. **[[Anarkulova et al - Beyond the Status Quo (Critical Assessment of Lifecycle Advice)]] (2025):** With [[Block Bootstrap Returns]], bonds are worse diversifiers at long horizons than short ones. The variance ratio for bonds at 30 years = 2.30 (rising risk). For stocks = 0.75 (mean reversion). 60/40 requires **94% more savings** than 100% equity to match utility.

3. **[[Dolvin - Asset Allocation for Retirement Simple Heuristics and Target-Date Funds]] (2010):** [[100% Stock Portfolio]] outperforms all glidepath heuristics in bootstrapped simulations.

4. **[[Shiller - Life-cycle personal accounts proposal for Social Security]] (2006):** Decreasing equity approach for US Social Security personal accounts likely produces worse outcomes than all-equity.

5. **[[Parker et al - Simple Allocation Rules and Optimal Portfolio Choice]] (2024):** TDFs too conservative in retirement; optimal equity at retirement = ~60% vs TDF = 30-40%.

## When Decreasing Equity May Be Rational

- Investor has genuinely bond-like human capital (stable government job)
- [[Destitution Risk]] is paramount - investor cannot tolerate any large drawdown
- Near-term spending needs require capital preservation
- High risk aversion (gamma > 5)
- Richer investor with more than enough for consumption needs -> preserve capital for bequests

## Related
[[Life-cycle Asset Allocation]]
[[Increasing Equity Strategy]]
[[100% Stock Portfolio]]
[[Age in Bonds Rule]]
[[Target Date Funds]]
[[Human Capital]]
[[Declining-risk Strategies are sub-optimal]]