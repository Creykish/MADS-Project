## Reference
```
@article{bengen1994withdrawal,
  author  = {Bengen, William P.},
  title   = {Determining Withdrawal Rates Using Historical Data},
  journal = {Journal of Financial Planning},
  year    = {1994},
  volume  = {7},
  number  = {4},
  pages   = {171--180},
  month   = {10}
}
```

## Why This Paper

The foundational "4% rule" paper. Uses historical portfolio longevity charts (1926 onwards, Ibbotson data) to determine safe withdrawal rates and optimal equity allocations for retirement portfolios. Shows that using average returns to compute withdrawal rates is a logical fallacy - sequence risk and major financial events dominate outcomes. Coins the "4% rule" as the maximum safe first-year withdrawal rate for a 30-year retirement. Frequently cited by Bengen 1996, Blanchett 2007, Pfau & Kitces 2014, Estrada 2015, Anarkulova 2025.

## Setup

- Data: Ibbotson Associates SBBI 1992 Yearbook, actual historical annual returns from 1926
- Two asset classes: intermediate-term Treasury notes + common stocks
- Metric: "portfolio longevity" = how many years before portfolio is exhausted by withdrawals
- Scenario structure: each start year = one scenario; bars show longevity for each cohort
- Withdrawals: real (inflation-adjusted) each year after the first; first-year withdrawal = fixed % of initial portfolio value
- No distributional assumptions; pure historical simulation
- Rebalancing: continuous to target allocation

## Key Results

### The 4% rule
- 3% withdrawal rate: all cohorts since 1926 survive 50+ years (used as the "cap" on charts)
- 4% withdrawal rate: minimum portfolio longevity ~33 years across all historical cohorts -> "safe" for a 30-year retirement
- 4.25%: can fail in as few as 28 years
- 5%: cohorts retiring late 1960s/early 1970s run out in ~20 years -> not safe for typical life expectancy
- 6%: 31 out of ~51 cohorts fail within 30 years (<40% success rate for 30-year horizon)

### Why averages don't work
The scenario where a planner uses long-run mean returns (10.3% stocks, 5.1% bonds, 3% inflation -> 5% real return -> withdraw 5%) appears safe on averages but fails badly when "events" hit:
- Sequence risk: a bad early period depletes the portfolio permanently
- Inflation compounds withdrawals faster than assumed
- The 1973-74 "Big Bang" affects portfolios that began retirement up to 20 years earlier

### The three financial "events"
| Event | Period | Severity | Why |
|---|---|---|---|
| "Big Bang" | 1973-74 | Most severe | Stock crash + high inflation combined; depletes both real returns and purchasing power |
| "Big Dipper" | 1937-41 | Moderate | Large stock decline but moderate inflation; affects 9-10 years of prior cohorts |
| "Little Dipper" | Early Depression | Least severe | Huge stock decline but deflation cushions it; purchasing power of remaining assets rises |

Key insight: deflation is not what to fear - it is the combination of falling asset prices AND rising inflation that destroys retirement portfolios. The 1929 crash itself (a deflationary period) was less damaging than the 1973-74 stagflation.

### Optimal equity allocation: 50-75%

Worst-case portfolio longevity (across all withdrawal rates and cohorts):
- 0% stocks: consistently worst (bond returns insufficient for 30-year real withdrawals)
- 25% stocks: also consistently short
- 50% stocks: near-optimal for worst-case longevity; peaked at this level
- 75% stocks: essentially tied with 50% on worst-case longevity (1 year difference), but substantially higher median and upper-tail wealth

-> Start equity between 50% and 75%. Minimum 50%. Above 75% is counterproductive: depression-era cohorts (deflation + stock crash) start to fail the 30-year minimum.

**Key trade-off:** 50% to 75% equity has virtually the same worst-case longevity, but average portfolio value after 20 years is +123% higher with 75% equity -> the "cost" of extra equity risk is near-zero for worst-case outcomes but the upside is enormous.

### Should you change allocation mid-retirement?

General answer: **no, maintain initial allocation**. Evidence from 3 client types:

**"Black holes"** (bad luck early - e.g. retired 1929):
- Temptation: reduce equity to "salvage" remaining capital after stock crash
- This is exactly wrong: selling at bottom locks in losses; bonds can't recover
- 1929 retiree at end of 1932 with 75% stocks survives to 1992 with $1.7M
- Same retiree switching to 0% stocks: exhausted by 1946
- 100% stocks from 1932: $42M by 1992 (extreme case but illustrates recovery power)
- Best practical advice: hold 75% equity + reduce withdrawals slightly if possible

**"Stars"** (good luck early - e.g. retired 1958):
- Temptation: increase withdrawals and/or increase equity allocation on a high
- Exactly wrong: excess returns today cushion future losses; the "Big Bang" came for 1958 retirees too
- After 1967 boom, client with inflated withdrawals hit 8% withdrawal rate by 1974 -> disaster
- Best advice: no radical changes; any withdrawal increase must be moderate

**"Asteroids"** (average experience - e.g. retired 1942-46, 1959-60):
- No changes requested or needed
- Average first decade provides cushion for second-decade events
- Maintain allocation and plan

### The "black hole" insight (sequence risk)

This is an early articulation of sequence-of-returns risk: bad returns early in retirement are far more damaging than bad returns late, because early withdrawals at low portfolio values permanently reduce the compounding base. The 1973-74 event's damage "reaches back" 20+ years to affect portfolios that began retirement in the early 1950s.

## Recommendations Summary

> "I counsel my clients to withdraw at no more than a four-percent rate during the early years of retirement"

> "despite advice you may have heard to the contrary, the historical record supports an allocation of between 50-percent and 75-percent stocks as the best starting allocation"

> "stock allocations below 50 percent and above 75 percent are counterproductive"

> "there is no need to change the initial asset allocation [mid-retirement]. It is likely to do more harm than good"

## Relationship to Other Papers

- [[Blanchett - Dynamic Allocation Strategies for Distribution Portfolios]] (2007): extends this by testing 43 glide paths vs static; confirms 4% rule and static allocations, refines equity to 60/40 with risk-adjustment
- [[Pfau & Kitces - Reducing Retirement Risk with a Rising Equity Glide Path]] (2014): cites Bengen as establishing the static-is-good baseline; then argues rising equity (not static) is better via MC
- [[Estrada - The Retirement Glidepath]] (2015): uses same historical rolling-period methodology as Bengen; confirms static beats declining-equity
- [[Estrada - The Glidepath Illusion]] (2014): Bengen's logic (bad early outcomes dominate) is the same mechanism Estrada uses to critique accumulation glidepaths
- Bengen 1996 (`bengen1996asset`) extends this paper to consider small-cap stocks and dynamic asset allocation changes

## Findings
[[4% Rule - Safe Initial Withdrawal Rate for a 30-Year Retirement]]
[[Retirees Spend Less in Retirement than Predicted by Theory]]
