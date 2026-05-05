[[ssrn-4590406.pdf]]
## Reference
```

@misc{anarkulova2025beyond,
  author       = {Anarkulova, A. and Cederburg, S. and O'Doherty, M. S.},
  title        = {Beyond the Status Quo: A Critical Assessment of Lifecycle Investment Advice},
  year         = {2025},
  month        = mar,
  url          = {https://doi.org/10.2139/ssrn.4590406},
  note         = {SSRN Working Paper}
}
```
Anarkulova, A., Cederburg, S., & O'Doherty, M. S. (2025). Beyond the status quo: A critical assessment of lifecycle investment advice. *SSRN Working Paper*, https://doi.org/10.2139/ssrn.4590406

## Summary
Authors studied [[Life-cycle Asset Allocation]] strategies. Used block-bootstrapping to generate portfolio returns and to optimise the strategy. 

Found [[100% Stock Portfolio]] to be most effective with block-bootstrapped data. IID yeilds higher dependence on fized income assets. 

**Optimal portfolio throughout life:**
- 33% domestic stocks, 67% international stocks
- **0% bonds, 0% bills**
- (nearly) all-equity is optimal in every tested scenario
- truly optimal includes a brief tactical bond allocation at exact retirement date (27% bonds at 65), quickly reverting to 100% equity after.

- Only exception: 27% bills at exact age 65 (tactical for rigid 4% rule)

**Welfare cost of traditional advice:**

To match same utility:
- 60/40 balanced requires 19.44% savings rate (vs 10% optimal) = **94% more savings**
- Representative TDF requires 16.27% savings rate = **63% more savings**

Traditional advice costs retirees nearly half their potential wealth.

## Why Bonds Fail at Long Horizons

**Short-term (1 month) stats mislead:**
- Bonds: 0.95% return, 9.51% vol
- International stocks: 7.03% return, 23.26% vol, correlation 0.21
- Looks like bonds diversify

**Long-term (30 year) reality:**
- Bonds variance ratio: **2.30** (variance INCREASES at longer horizons!)
- Stocks variance ratio: **0.75** (variance DECREASES!)
- Bond/stock correlation: **0.45** (diversification shrinks)
- Bond/inflation correlation: **-0.78** (terrible for real returns)
- Stock/inflation correlation: **-0.01** (preserves purchasing power)

Bonds are worse in every dimension for long-horizon investors.

## Why Standard Models Get It Wrong

**Three mistakes:**

1. **IID returns assumption** → misses mean reversion, bond persistence, changing correlations
2. **Domestic-only** → ignores international stocks (better diversifier than bonds)
3. **Short-horizon focus** → uses 1-period stats, misses variance ratio effects

## Key Method: Block Bootstrap

**Not IID.**

Resample sequences of consecutive returns (1-12 months, average 6.5).

Preserves:
- Mean reversion in stocks
- Momentum in bonds
- Changing correlations
- All time-series properties

Data: 2,600+ country-months from 39 developed countries, 1875-2023.

**Test:** With IID + domestic-only, they get conventional advice (38% stocks, 14% bonds, 48% bills at 65). 

With block bootstrap + international → all-equity.

## Performance on All Metrics

Optimal (100% equity) vs benchmarks:

**Retirement wealth:**
- TDF: 71% of optimal (39% less)
- 60/40: 67% of optimal (50% less)

**Capital preservation (probability of ruin):**
- Optimal: 6.7%
- TDF: 19.7%
- 60/40: 16.9%

**All-equity is SAFEST.** Contradicts intuition.

**Income & bequests:** Optimal generates higher consumption + 2x larger bequests.

## International Stocks = Bond Substitute

**Why 67% international?**
- Lower long-horizon correlation with domestic than bonds have
- Better inflation hedge (-0.01 vs -0.78)
- Higher returns

**NZ implications:**
- NZ market is 0.1% of global
- Should be even higher international weight
- Home bias indefensible

## Robustness

Tested 12+ variations (post-WWII only, different γ, bequest motives, labor income correlations, flexible withdrawal, leverage, etc.).

**All yield all-equity.**

Only exception: highest valuation quintile with market timing → 9% bonds (still 91% equity).

Result is robust, not artifact.

## For My NZ Research

**Direct implications:**

1. **NZ Super as implicit bonds:** ~$800k PV of guaranteed income → justifies 100% equity in financial portfolio?

2. **Must use block bootstrap** (or similar time-series method) with NZ data

3. **Include international stocks explicitly:** NZX50 + MSCI World, optimize weights

4. **Long-horizon perspective:** Wealth at 90, not next-year volatility

5. **Report all metrics:** ruin probability, not just mean/variance

**Questions:**

1. Do NZ bonds have same poor long-horizon properties?
2. With higher NZ Super floor ($26k vs US SSI $9k), is all-equity even more justified?
3. What should KiwiSaver defaults be?

**Challenge to conventional wisdom:**
- TDF glidepaths are costly
- "Age in bonds" rule is wrong
- All-equity preserves capital better than bonds

## Model Details

$$ \max E\left[\sum_{t=0}^{T} \beta^t u(C_t) + B(W_T)\right] $$

- CRRA utility
- Stochastic labor income (Guvenen et al 2021)
- Social Security included
- Longevity risk
- Block bootstrap returns
- Monte Carlo + quasi-Newton optimization (like Makinen)

## The TDF Policy Critique

**Pension Protection Act 2006 QDIA regs:** Require "mix of equity and fixed income based on age"

**Their findings:**
- Required "mix" costs 63% more savings
- Age-based changes unnecessary
- Fixed income doesn't preserve capital (opposite)

**Policy implication:** QDIA regs may be counter-productive.

**NZ:** KiwiSaver defaults are conservative (max 25% growth). Should they be aggressive (80-100% equity) given NZ Super?

## Related

[[Makinen - Monte Carlo Optimisation]] - same optimization method
[[Merton - Lifetime Portfolio Selection under Uncertainty]] - theoretical foundation
[[Cocco - Consumption and Portfolio Choice over the Life Cycle]] - traditional model with bonds
[[Anderson French Lam - Asset Run-Down at End of Life Cycle]] - slow asset depletion puzzle

## Findings
[[All-equity Portfolios Outperform Glidepaths at Long Horizons]]
[[Declining-risk Strategies are sub-optimal]]
[[TDFs Are Too Conservative in Retirement]]
[[NZ Super Acts as Implicit Bond Justifying Higher Equity]]
