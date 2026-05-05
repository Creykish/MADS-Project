## Reference
```
@article{estrada2015retirement,
  author  = {Estrada, J.},
  title   = {The Retirement Glidepath: An International Perspective},
  journal = {The Journal of Investing},
  year    = {2015},
  volume  = {25},
  number  = {2},
  pages   = {28--36},
  doi     = {10.3905/joi.2016.25.2.028}
}
```

## Why This Paper

Companion to [[Estrada - The Glidepath Illusion]] (2014), which covered the **accumulation period**. This paper covers the **retirement/distribution period**. Key question: once you're drawing down, should you hold more stocks early in retirement (and shift to bonds) or hold fewer stocks early (and shift to equity)? Same dataset, same international scope.

Combined conclusion across both papers: **inverted U-shape** across the full life cycle - see [[Optimal Glidepath is Inverted U-Shaped Across Full Life Cycle]]. This is the direct opposite of Pfau & Kitces (2014)'s U-shape recommendation.

## Setup

- Data: DMS dataset, 19 countries + World, annual real returns 1900-2009
- Nest egg: $1,000 at retirement, 4% initial withdrawal rate, real (inflation-adjusted) withdrawals
- 30-year retirement period
- 81 rolling 30-year periods (1900-1929 to 1980-2009)
- Metric 1: failure rate (portfolio depleted before 30 years)
- Metric 2: terminal wealth distribution (bequest)

**Strategies tested:**

*Declining-equity (DE) - conventional lifecycle logic:*
| Start | End |
|---|---|
| 100% stocks | 0% stocks |
| 90% stocks | 10% stocks |
| 80% stocks | 20% stocks |
| 70% stocks | 30% stocks |

*Rising-equity (RE) mirrors - each starts and ends with opposite allocations to its DE pair*

*Static strategies:* 60x30 (60% equity constant), 50x30, 40x30, and others

## Key Results: Dynamic Strategies

**US failure rates - DE beats RE every time:**
| DE strategy | DE failure | RE mirror | RE failure |
|---|---|---|---|
| 100->0% | 8.6% | 0->100% | 21.0% |
| 90->10% | 6.2% | 10->90% | 17.3% |
| 80->20% | 4.9% | 20->80% | 11.1% |
| 70->30% | 4.9% | 30->70% | 8.6% |

DE failure rates are less than half RE failure rates (except the last pair). This reverses the accumulation finding: **during retirement, declining equity is better, not worse**.

**Terminal wealth (bequest):** DE also beats RE on mean, median, and upside (P90, P95, P99) for US and World.

**Downside (P1, P5, P10):** DE provides equal or better downside protection than RE. Not riskier even by this measure.

**International (average across 19 countries):**
- All failure rates are much higher (31-49%) reflecting non-US market experience
- DE still dominates RE: DE failure ~31-32%, RE failure ~39-49%
- The gap narrows but DE consistently wins

## Key Results: Static Strategies

The 60x30 static strategy **outperforms all dynamic strategies**:
- US failure rate: 4.9% (ties lowest DE strategy)
- US mean terminal wealth: $1,437 (highest of all strategies including DE)
- US median: $1,155 (substantially higher than all DE strategies)

This is the practical recommendation: **don't bother managing a dynamic glidepath during retirement, just hold 60/40 throughout**.

All-equity during retirement (100% stocks throughout):
- US failure rate: 8.6% (higher than 60x30 or best DE strategies)
- But higher mean/median bequest and much higher upside
- World failure rate: 14.8%; Average country: 31.4% -> all-equity is *risky* in retirement in non-US markets

## Why DE Beats RE During Retirement (Mechanism)

The mechanism is the **opposite** of the accumulation case. During drawdown:
- Early retirement: portfolio is largest -> sequence-of-returns risk is highest
- A crash in year 1-5 of retirement with a stock-heavy portfolio is devastating (sell low to fund withdrawals)
- DE starts equity-heavy -> wait, this seems bad? But the portfolio is still large early on and stocks have historically performed well early in the period. More importantly: ending with bonds means capital preservation as portfolio shrinks.
- RE starts bond-heavy: gets to equity late, when portfolio is small and volatility hits a smaller base

Alternatively: DE has a built-in "harvest equity gains early" property. If stocks do well in early retirement (when allocation is high), terminal wealth is large regardless of later allocation.

## Contradiction with Pfau & Kitces (2014)

Pfau & Kitces (2014) recommend a **rising-equity glidepath during retirement** (the RE strategy). Their argument: sequence-of-returns risk is worst early in retirement -> start conservative, increase equity later as the danger window passes. Based on Monte Carlo simulations.

Estrada finds the opposite using historical rolling periods. The disagreement comes down to methodology:
- MC simulations: typically use IID returns, miss sequence structure and mean reversion
- Historical rolling periods: preserve actual return sequences, autocorrelation, and fat tails

The disagreement on methodology matters. See [[Return Predictability]] and [[Block Bootstrap Returns]].

## Combined With 2014 Paper: The Inverted U

| Period | Better strategy |
|---|---|
| Accumulation (working years) | Contrarian / increasing equity |
| Retirement (drawdown years) | Declining equity |
| Overall shape | Inverted U: increase equity to retirement, then decline |

Max equity exposure at the point of retirement itself. But note: the 60/40 static portfolio is "very effective" and simpler than managing a dynamic inverted-U glidepath in both papers. And all-equity is optimal in accumulation (2014 paper).

## Papers to Follow Up

- **Bengen (1994)** - seminal "4% rule" paper; origin of withdrawal rate literature; must-read for spending rules
- **Bengen (1996)** - recommends 1%/year stock reduction in retirement; directly contradicted here
- **Cooley, Huggard & Moritz (1998)** - "Trinity study"; portfolio success rates; uses 25% failure as acceptable
- **Pfau & Kitces (2014)** - argues RE during retirement; U-shape overall; key paper to engage with for any RQ on glidepath shape
- **Blanchett (2007)** - finds static allocations "remarkably efficient"; 60/40 optimal for most retirees; supports Estrada's static finding
- **Kitces & Pfau (2014)** - 60/40 nearly optimal in most situations; consistent with Estrada static result
- **Dimson, Marsh & Staunton (2002)** - the DMS dataset underlying both Estrada papers and much of the international evidence

## Findings
[[Declining-risk Strategies are sub-optimal]]
[[Optimal Glidepath is Inverted U-Shaped Across Full Life Cycle]]
