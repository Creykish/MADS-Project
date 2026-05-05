## Reference
```
@article{pfau2014rising,
  author  = {Pfau, Wade D. and Kitces, Michael E.},
  title   = {Reducing Retirement Risk with a Rising Equity Glide Path},
  journal = {Journal of Financial Planning},
  year    = {2014},
  volume  = {27},
  number  = {1},
  pages   = {38--45},
  url     = {https://www.financialplanningassociation.org/article/journal/JAN14-reducing-retirement-risk-rising-equity-glide-path}
}
```

## Why This Paper

The main challenge to [[Estrada - The Retirement Glidepath]] (2015) and to the conventional declining-equity-in-retirement view. Argues that a **rising equity glide path during retirement** reduces both the probability and magnitude of portfolio failure. Combined with a declining-equity accumulation phase, this implies a **U-shaped glidepath** across the full life cycle - the opposite of Estrada's inverted-U recommendation.

This is a widely cited paper in the practitioner literature. The disagreement between Pfau & Kitces and Estrada is essentially methodological: MC vs historical rolling periods.

## Setup

- 10,000 Monte Carlo simulations (not historical rolling periods - key methodological distinction)
- Lognormal return distribution
- 121 glide path combinations: start equity 0-100% in 10pp steps, end equity 0-100% in 10pp steps -> linear annual adjustment between them
- Withdrawal rates: 4% and 5% initial, inflation-adjusted
- Retirement horizons: 20, 30, 40 years (baseline = 30)
- 3 capital market assumption sets:
  1. **Evensky/MoneyGuidePro** (baseline, as of July 2013): moderate real returns
  2. **Low rate environment**: compressed bond returns, historical equity risk premium
  3. **Historical**: Ibbotson SBBI long-run averages (higher returns + larger equity premium)

**Outcome measures:**
1. Failure rate (prob portfolio depleted before end)
2. Magnitude of failure: wealth at P5 of distribution (shortfall if negative)
3. Upside potential: median terminal wealth
4. Maximum sustainable withdrawal rate at P10

## Key Results

**Rising equity glide paths dominate across all scenarios:**
- Optimal range: start ~20-40% equity, end ~60-80% equity
- A 30->60% rising path beats a static 60/40 on both failure rate AND magnitude of failure
- Portfolios starting at 10-30% equity with rising glide paths fare "far better" than static 50-60% portfolios

**Optimal glide paths (Evensky baseline, 4% withdrawal, 30-year retirement):**
- Failure rate: best results from starting ~30% equity, ending ~80%
- Magnitude of failure (P5): start ~10% equity, rise to ~50%
- MWR at P10: start ~20% equity, end ~40%

**At higher withdrawal rates (5%):** optimal starting equity rises somewhat as the portfolio needs more growth. But rising glide paths still dominate.

**In low rate environment:** rising glide paths still win; optimal starting equity even lower (near 0%) rising to ~30-40%.

**With historical returns (Ibbotson):** rising glide paths perform "even better" - optimal ~30->70%.

**For median outcomes (upside):** higher equity throughout is better (no surprise). The rising glide path advantage is specifically about downside/failure risk, not expected wealth.

## The Mechanism: Sequence-of-Returns Risk

This is the core argument. Citing Kitces (2008): in a 30-year retirement, the outcome is dictated almost entirely by **real returns in the first 15 years**.
- Good first half: portfolio so far ahead that later bear market can't destroy the goal
- Bad first half: portfolio stressed, so good returns in second half are critical to survival

**Problem with declining equity in this context:**
- Bad first half scenario -> equity falling from 60% to 30% means *least* equity exactly when good returns finally arrive in second half
- The portfolio is already depleted; it can't benefit from the recovery

**Rising equity addresses this:**
- Bad first half: portfolio is conservative early (less drawdown), then systematically dollar-cost-averages into cheap equities through the downturn
- Maximum equity exposure arrives exactly when stocks have recovered and the portfolio needs growth to survive
- Good first half: the retiree is already so far ahead that the rising equity doesn't matter (they've secured the goal)

-> "Heads you win, tails you don't lose" dynamic specific to the failure-risk frame

## Practical Implications / Design

- **Start retirement at 20-40% equity** (much lower than typical TDF landing allocation of 30-50%)
- **Rise to 60-80% equity** by end of retirement
- This means *less* average equity exposure than a static 60/40, but better failure outcomes
- The "bucket strategy" (spend bonds first, let equity grow) is effectively a rising glide path operationally
- Partial annuitization creates a similar effect (Kitces & Pfau 2013)

Caveat from the authors: older retirees with rising equity may have behavioral/risk tolerance issues. But the rising path ends at 60-80% equity, no more than many static approaches anyway.

## Why This Contradicts Estrada (2015)

Estrada (2015) uses **historical rolling periods** (81 periods from 1900-2009) and finds DE beats RE in retirement. Pfau & Kitces use **Monte Carlo** with IID lognormal returns and find RE beats DE.

The key difference:
- Historical rolling periods preserve actual return sequences including autocorrelation, clustering of bad years, mean reversion
- IID Monte Carlo loses all time-series structure -> sequence risk is "random" and symmetric
- With IID returns, rising equity hedges against a random bad draw; with historical returns, market regimes cluster differently

Additionally, Estrada measures terminal wealth and failure rate jointly; Pfau & Kitces specifically focus on failure risk and failure magnitude, not just mean/median terminal wealth. When Estrada looks at failure rates, DE wins. When Pfau & Kitces look at failure rates with MC, RE wins.

**Bottom line:** The methodological difference (MC vs historical + IID vs non-IID) drives the contradiction. Anarkulova (2025) argues block bootstrap is better than both because it preserves return dynamics without relying on a limited historical sample. Anarkulova finds 100% equity optimal, not a rising RE path.

## Relationship to Other Papers

- Supports Pfau & Kitces' own prior work recommending conservative starting allocations
- Extends Bengen (1996)'s finding that a 1%/yr phasedown in stocks is reasonable -> suggests that was already too aggressive, should be rising not declining
- Consistent with Blanchett (2007): static allocations beat declining, though Blanchett doesn't test rising
- The "bucket strategy" framing connects to practitioner audience
- Contradicted by Estrada (2015) on the same retirement period question using historical data
- Contradicted by Anarkulova (2025) which finds 100% equity dominates all glidepath approaches

## Findings
[[Optimal Glidepath is Inverted U-Shaped Across Full Life Cycle]]
