## Reference
@article{shiller2006lifecycleSocialSecurity,
title = {Life-cycle personal accounts proposal for Social Security: An evaluation of President Bush's proposal},
journal = {Journal of Policy Modeling},
volume = {28},
number = {4},
pages = {427-444},
year = {2006},
issn = {0161-8938},
doi = {https://doi.org/10.1016/j.jpolmod.2005.10.010},
url = {https://www.sciencedirect.com/science/article/pii/S0161893805001341},
author = {Robert J. Shiller},
keywords = {Dynamic portfolio theory, Life-cycle portfolio, Social Security system},
abstract = {The life-cycle portfolio proposal for personal accounts within a Social Security system would have the government undertake the dynamic portfolio allocation program for individuals. This paper evaluates, using U.S. historical data 1871–2004, several versions of conventional life-cycle portfolios. The results show disappointing performance relative to the rhetoric of the promoters of the proposal. Dynamic portfolio theory suggests that the optimal life-cycle portfolio may look very different from the conventional form. Moreover, behavioral finance suggests that the design of a life-cycle portfolio for Social Security should consider the attitudes and habits of individuals and as well as their diversity.}
}

## Why This Paper

Context is Bush's 2005 proposal to add personal Social Security accounts. Workers could divert 4% of payroll into lifecycle funds. Shiller tests whether conventional lifecycle portfolios (85% -> 15% equity glidepath) live up to the hype. The answer is no. This paper is an early, clean empirical takedown of the [[Decreasing Equity Strategy]] using long-run historical data.

## Setup

- Data: US stocks, bonds, money market 1871-2004 (134 years; from Shiller's *Irrational Exuberance* dataset)
- Simulated 91 overlapping 44-year worker careers
- 6 portfolios tested: baseline lifecycle (85->15%), conservative lifecycle (70->10%), aggressive lifecycle (90->40%), 50/50, 100% bonds, 100% equity
- Offset mechanism: accounts credited at 3% real rate -> workers effectively borrow at 3% to invest. Only wins if portfolio beats 3% real return
- Cost: 30 bps per year subtracted from returns

**Portfolios:**

| Portfolio | Initial equity | Final equity |
|---|---|---|
| Baseline lifecycle | 85% | 15% |
| Conservative lifecycle | 70% | 10% |
| Aggressive lifecycle | 90% | 40% |
| 50/50 constant | 50% | 50% |
| All bonds | 0% | 0% |
| All equity | 100% | 100% |

## Key Results (US Historical Data)

**Baseline lifecycle (85->15%):**
- Median net account value: +$15,172
- 32% chance of losing (account ends negative after offset)
- Internal rate of return: 3.4% (barely above 3% offset)
- Compare to traditional Social Security benefit: ~$14,000-21,000/year -> lifecycle adds maybe $1,000/year

**All equity (100%):**
- Median net account value: +$157,708 (10x the lifecycle)
- Only 2% chance of losing
- IRR: 5.9%
- **Stochastically dominates the baseline lifecycle at every percentile** - at no point in the distribution does lifecycle beat all-equity

**All bonds:**
- Negative median, loses 89% of the time -> bonds don't clear the 3% offset rate historically

## The International Returns Adjustment

[[US Equity Returns Show Survivorship Bias Relative to International Experience]]

Dimson, Marsh & Staunton (2002): 15-country median geometric real stock return 1900-2000 = **4.8%** vs US **6.8%**. Gap = 2.2pp. WSJ economist survey for next 44 years: 4.6% expected stocks return (matches international, not US history). Shiller reruns all simulations reducing stock returns by 2.2pp:

**Baseline lifecycle with international return adjustment:**
- Median turns *negative*
- Probability of loss: 71% (up from 32%)
- P10 net value: -$44,761

**All equity with international return adjustment:**
- Probability of loss: 33% (much worse but still better than lifecycle)
- Median still positive: +$27,947

-> The lifecycle plan is even more unattractive under realistic return expectations. This matters for NZ: NZ is a small, open economy -> [[NZ Return Assumptions Should Reflect International Experience Not US History]].

## Theoretical Complications Raised

Shiller reviews heterodox lifecycle theory that goes beyond the standard "young people should be in equities" narrative:

- **Viceira (2001):** High idiosyncratic labor income risk + positive corr(stocks, labor income) -> young people should have *less* equity than retirees. Under some params, optimal is >300% leverage or short positions.
- **Benzoni et al.:** If stocks and labor income are *cointegrated* (correlated over long horizons), young people should SHORT the stock market to hedge human capital.
- **Lynch & Tan:** Recession -> low mean income AND high volatility -> young people should hold *less* stocks than old people.
- **Baxter & Jermann (1997):** Optimal to short domestic stocks, long foreign stocks (hedging domestic human capital). No policy would ever implement this.

Key message: the optimal lifecycle portfolio is *highly parameter-sensitive*. The conventional declining-equity story is not robust to realistic assumptions about labor income dynamics. See [[Human Capital]] and [[Human Capital Justifies Decreasing Equity with Age]].

## Behavioral and Design Issues

- Households vary massively in preferences, circumstances, knowledge -> one-size lifecycle is irrational for many
- The plan in context is leveraged equity buying: the offset is a government loan at 3% real -> economically identical to a margin account at 3%
- Most small investors have anti-equity bias; encouraging leverage is perverse for them even if theoretically fine for others
- Life-cycle funds commercially available at the time (Vanguard 2045, T. Rowe Price 2040) vary enormously and are designed for *supplemental* saving, not replacing Social Security -> design not transferable to mandatory accounts

## Findings
[[Declining-risk Strategies are sub-optimal]]
[[All-equity Portfolios Outperform Glidepaths at Long Horizons]]
[[US Equity Returns Show Survivorship Bias Relative to International Experience]]