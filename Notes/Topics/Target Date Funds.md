Mutual funds or superannuation funds that automatically adjust [[Asset Allocation]] along a [[Decreasing Equity Strategy]] glidepath as the investor approaches a target retirement year. The most common practical implementation of lifecycle investment advice.

## How They Work

- Investor picks a target year fund (e.g. "2045 Fund" for someone retiring in 2045)
- Fund starts equity-heavy (often 90-100% stocks) and automatically rebalances toward bonds over time
- At target date, fund typically holds 30-40% equity, 60-70% bonds/fixed income
- Many [[Target Date Funds]] continue the glidepath post-retirement ("through" vs "to" designs)

**[[Dolvin - Asset Allocation for Retirement Simple Heuristics and Target-Date Funds]] (2010):**
- Most TDFs approximate the 120-minus-age rule ([[Age in Bonds Rule]])
- Equity at age 40: ~80%; at retirement (65): ~30-40%

## Evaluation: The Parker et al Finding

**[[Parker et al - Simple Allocation Rules and Optimal Portfolio Choice]] (2024):**
Using deep reinforcement learning to solve the optimal lifecycle problem:
- TDFs track average optimal behavior reasonably well up to age ~50
- After age 50 and through retirement: TDFs are **too conservative**
- Optimal equity at retirement: ~60%; TDF: 30-40%
- Welfare loss from using TDF vs optimal: **1.7-2.8% of lifetime consumption** equivalent
  - Lower bound (1.7%): can re-optimize other decisions after TDF
  - Upper bound (2.8%): fully locked into TDF
- Key sources of welfare loss: TDFs don't respond to wealth level, business cycle, or return predictability signals

## Evaluation: The Anarkulova et al Finding

**[[Anarkulova et al - Beyond the Status Quo (Critical Assessment of Lifecycle Advice)]] (2025):**
- TDF investors need **63% more savings** than all-equity investors to achieve the same utility
- TDF ruin probability: **19.7%** vs all-equity **6.7%** - TDFs create more ruin risk, not less
- The conventional logic (shift to bonds = safety) fails at long horizons because bond variance ratio = 2.30 at 30 years

## Why TDFs Persist

- Behavioral appeal: automatic, "set and forget"
- Regulatory default: QDIA status in US 401(k)s; KiwiSaver default in NZ
- Marketing narrative: "safer as you get older" is intuitive even if incorrect
- Low cognitive burden: single fund decision

## NZ KiwiSaver Context

KiwiSaver funds in NZ use a similar lifecycle approach. The evidence suggests NZ KiwiSaver participants in conservative/balanced funds at retirement are likely:
- Significantly over-allocated to bonds/fixed income
- Missing out on the equity risk premium
- Potentially facing higher ruin risk than an all-equity holder

With [[Pensions & Social Security]] (NZ Super) as the consumption floor, the case for conservative KiwiSaver funds at retirement is especially weak.

## Related
[[Life-cycle Asset Allocation]]\n[[Decreasing Equity Strategy]]\n[[Age in Bonds Rule]]\n[[Declining-risk Strategies are sub-optimal]]\n[[Block Bootstrap Returns]]\n[[Pensions & Social Security]]\n[[Parker et al - Simple Allocation Rules and Optimal Portfolio Choice]]\n[[Anarkulova et al - Beyond the Status Quo (Critical Assessment of Lifecycle Advice)]]
