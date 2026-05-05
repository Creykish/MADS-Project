## Reference
```
@article{estrada2014glidepath,
  author  = {Estrada, J.},
  title   = {The Glidepath Illusion: An International Perspective},
  journal = {The Journal of Portfolio Management},
  year    = {2014},
  volume  = {40},
  number  = {4},
  pages   = {52--64},
  doi     = {10.3905/jpm.2014.40.4.052}
}
```

## Why This Paper

**Accumulation period only** (companion paper [[Estrada - The Retirement Glidepath]] covers drawdown). The "glidepath illusion" is the idea that lifecycle strategies look prudent by reducing volatility, but actually produce systematically worse wealth outcomes than their mirror strategies. Uses the broadest dataset at time of publication: 19 countries + 2 regions, 1900-2009.

## Setup

- Data: DMS dataset (Dimson-Marsh-Staunton), annual real returns for stocks + government bonds, 19 countries + Europe + World, 1900-2009
- Investor: 40-year working life, $1,000/year real contributions, rebalances annually
- 71 overlapping 40-year periods (1900-1939 to 1970-2009)
- Focus: distribution of terminal wealth (capital at retirement)

**Strategies tested:**

*Symmetric (lifecycle vs mirror):*
| Lifecycle starts | Lifecycle ends | Mirror starts | Mirror ends |
|---|---|---|---|
| 100% stocks | 0% stocks | 0% stocks | 100% stocks |
| 90% stocks | 10% stocks | 10% stocks | 90% stocks |
| 80% stocks | 20% stocks | 20% stocks | 80% stocks |
| 70% stocks | 30% stocks | 30% stocks | 70% stocks |
| 60% stocks | 40% stocks | 40% stocks | 60% stocks |

*Other strategies:*
- 100x40: 100% equity for full 40 years
- 100x30: 100% equity for 30 years, then glide to 50/50 over final 10 years
- 100x20: 100% equity for 20 years, then glide to 50/50 over final 20 years
- 50x40: constant 50/50
- 60x40: constant 60/40

## Key Results

**Mirror (contrarian) strategies beat lifecycle in all 19 countries** on mean and median terminal wealth. The illusion: declining equity looks safer but delivers less wealth.

**US results (80-20 lifecycle vs its mirror):**
- Mirror mean terminal wealth: $137.1k vs lifecycle $110.4k (+24%)
- Mirror median: $132.1k vs lifecycle $101.5k (+30%)

**US results (100-0 lifecycle vs its mirror):**
- Mirror mean: $147.2k vs lifecycle $102.5k (+44%)
- Mirror median: $130.5k vs lifecycle $84.6k (+54%)

**Downside protection:** Min terminal wealth is *higher* under contrarian strategies than lifecycle in all cases. AvgD1 (average of worst decile) and AvgQ1 are also similar or better for contrarian.

-> **The higher variance of contrarian strategies is almost entirely upside variance** - not downside. Lifecycle strategies protect against uncertainty about how bad things get; contrarian strategies deliver more wealth in bad scenarios AND much more in good scenarios.

**Equity-driven strategies (100x40) vs average lifecycle:**
- 100x40 mean: $223.5k vs avg lifecycle $110.5k (more than 2x)
- 100x40 median: ~$189k vs avg lifecycle $100.6k (+88%)
- Lower AvgD1 than lifecycle strategies -> better downside too

**60x40 constant balanced:**
- Beats all lifecycle strategies on mean, median, and downside metrics
- Simpler to implement than any glidepath

## Core Argument: Why Lifecycle Fails

Shiller's (2005) insight: lifecycle funds are aggressive when the portfolio is small (early career) and conservative when the portfolio is large (near retirement). This is backwards. A bad sequence of returns matters **proportional to portfolio size**:
- Age 30: 100% equity, portfolio = $10k -> bad year = -$2k
- Age 60: 20% equity, portfolio = $200k -> bad year (bonds) = -$4k; same bad year at 100% equity = -$40k but that's from a huge base

Contrarian strategies flip this: conservative early (low capital at risk) and aggressive later (more capital working in mean-reverting equity at the horizon that matters).

## The "Illusion" Defined

Three things lifecycle strategies were supposed to deliver that they don't:
1. Lower downside risk in bad scenarios -> false, contrarian is equal or better
2. Less uncertainty about terminal wealth -> true, but the extra uncertainty of contrarian is all upside
3. Lower terminal wealth is an acceptable trade-off for safety -> false, the safety isn't real

## Papers to Follow Up

Papers cited that are high priority for this project:
- **Shiller (2005)** - original "lifecycle too conservative" argument (see [[Shiller - Life-cycle personal accounts proposal for Social Security]])
- **Basu & Drew (2009)** - first paper to systematically test lifecycle vs mirror strategies; supports contrarian
- **Arnott (2012)** & **Arnott et al (2013)** - popular critique of lifecycle; explicitly recommends contrarian
- **Ayres & Nalebuff (2010)** - argue young investors should *leverage* equity to achieve Samuelson share relative to lifetime wealth; contrarian but via leverage not reallocation
- **Pfau & Kitces (2014)** - disagrees: recommends U-shaped glidepath (declining during accumulation, rising during retirement); based on MC sims; contradicted by Estrada's historical evidence -> see [[Estrada - The Retirement Glidepath]]
- **Basu et al (2011)** - dynamic switching strategy (not unidirectional) beats both lifecycle and balanced; worth reading for connection to our wealth-responsive policy

## Findings
[[Declining-risk Strategies are sub-optimal]]
[[All-equity Portfolios Outperform Glidepaths at Long Horizons]]
[[Optimal Glidepath is Inverted U-Shaped Across Full Life Cycle]]