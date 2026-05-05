# Post-Retirement Glidepath

The [[Life-cycle Asset Allocation]] literature is relatively settled on accumulation: [[Decreasing Equity Strategy|declining-equity]] strategies (TDFs, age-in-bonds rules) are probably suboptimal, and high or rising equity throughout working life does better on most metrics. Post-retirement is far messier. Three distinct positions appear in the literature:

- **[[Decreasing Equity Strategy|Declining equity (DE)]]** in retirement: start high equity at retirement, reduce toward bonds over time (conventional lifecycle logic) -> [[Estrada - The Retirement Glidepath]] (2015)
- **[[Increasing Equity Strategy|Rising equity (RE)]]** in retirement: start conservative, increase equity as retirement progresses -> [[Pfau & Kitces - Reducing Retirement Risk with a Rising Equity Glide Path]] (2014)
- **Static/constant allocation**: don't bother managing a glidepath at all -> [[Blanchett - Dynamic Allocation Strategies for Distribution Portfolios]] (2007), [[Bengen - Determining Withdrawal Rates Using Historical Data]] (1994), [[Parker et al - Simple Allocation Rules and Optimal Portfolio Choice]] (2024)

The static camp is actually the most consistent across studies, but it doesn't map neatly onto the U-shape vs inverted-U debate, so it often gets underemphasised.

---

## The U-Shape Argument (Pfau & Kitces 2014)

Pfau & Kitces argue for a **U-shaped glidepath** across the full life cycle: declining equity during accumulation (conventional lifecycle) followed by *rising* equity during retirement. Their mechanism is sequence-of-returns risk.

The core insight (from Kitces 2008, cited in the paper) is that in a 30-year retirement, outcomes are determined almost entirely by real returns in the **first 15 years**. If the first half is bad, the portfolio is stressed; if the second half is bad but the first half was good, the portfolio can absorb it. This creates an asymmetry:

- A **DE** strategy leaves the portfolio with least equity exactly when it needs recovery most. After a bad early period, equity has been phased out just as stocks become cheap and a bounce would be most valuable.
- A **RE** strategy starts conservative (less damage from early crash), systematically buys into depressed equities through the bad period, then benefits from the recovery at maximum equity exposure. "Heads you win, tails you don't lose."

Their results from 10,000 Monte Carlo runs across 121 glide path combinations: optimal starting equity in retirement is ~20-40%, rising to ~60-80% by end. A 30->60% rising path beats a static 60/40 on *both* failure rate and failure magnitude. This holds across three different capital market assumption sets (baseline, low-rate, historical Ibbotson).

The practical implication is that the "bucket strategy" (spend bonds/cash first, let equity grow) is operationally equivalent to a rising equity glidepath.

---

## The Inverted-U Argument (Estrada 2015)

Estrada reaches the opposite conclusion using historical rolling periods across 19 countries + world index (DMS data, 1900-2009). Testing 81 rolling 30-year retirement windows with a 4% real withdrawal rule:

- **US:** DE failure rates 4.9-8.6%; RE mirrors 8.6-21.0% -> DE wins by a factor of ~2x
- **International (avg 19 countries):** DE 31-32% vs RE 39-49% -> DE still wins, gap narrows
- DE also dominates on terminal wealth (mean, median, upside percentiles) and downside protection

The mechanism Estrada gives: DE starts equity-heavy when the portfolio is **largest**, so equity gains in early retirement compound on a large base. Ending with bonds is capital preservation as the portfolio shrinks. RE strategies get to high equity only when the portfolio has already been depleted by withdrawals and is too small for equity gains to matter.

Combined with [[Estrada - The Glidepath Illusion]] (2014) for accumulation (rising equity wins during working life), Estrada's full-lifecycle recommendation is an **inverted U**: low equity early career -> build to peak equity at retirement -> decline through drawdown. See [[Optimal Glidepath is Inverted U-Shaped Across Full Life Cycle]].

---

## The Static Camp (Blanchett 2007, Bengen 1994, Parker et al. 2024)

Both sides of the DE vs RE debate tend to be outperformed by simply not managing a glidepath at all.

**[[Blanchett - Dynamic Allocation Strategies for Distribution Portfolios]] (2007)** is the clearest statement. Testing 43 glide paths (11 constant + 4 types of DE dynamics, no RE tested) across 1,071 scenarios using bootstrapped monthly returns 1927-2006:
- Static allocations have the lowest probability of failure in all but one scenario
- 100% equity wins on raw failure probability; 60/40 wins on his risk-adjusted "Success to Variability ratio" (prob. success / portfolio SD) -> **60/40 recommended for most retirees**
- 100/0 equity has ~7x the portfolio volatility of 0/100 bonds; once penalised for this, the 60/40 dominates
- The concave shape (fast DE early, slower later - real TDF shape) is best *among* DE strategies, but still loses to static
- Note: Blanchett did not test rising-equity paths, so static vs RE remains untested in his framework

**[[Bengen - Determining Withdrawal Rates Using Historical Data]] (1994)** finds worst-case portfolio longevity peaks at 50-75% equity and provides no evidence that dynamically managing away from this helps. His explicit recommendation: no reason to change initial allocation mid-retirement. The "black hole/star/asteroid" taxonomy demonstrates that the intuitive responses to good or bad early returns (change allocation) are both wrong.

**[[Parker et al - Simple Allocation Rules and Optimal Portfolio Choice]] (2024)** solves a full lifecycle model with 20+ state variables using deep reinforcement learning. Optimal post-retirement equity share is ~60% - approximately constant, not clearly rising or declining. TDFs that drop to 30-40% equity in retirement are too conservative; welfare cost 1.7-2.8% of lifetime consumption.

---

## Why Do They Disagree? The Methodological Divide

The DE vs RE contradiction is almost entirely explained by a single methodological difference: **Monte Carlo with IID returns** (Pfau & Kitces) vs **historical rolling periods** (Estrada, Bengen) vs **block bootstrap** (Blanchett, Anarkulova).

| Feature | IID Monte Carlo | Historical Rolling Periods | Block Bootstrap |
|---|---|---|---|
| Autocorrelation | Destroyed | Preserved | Approximately preserved |
| Return clustering / regimes | None | Preserved | Approximately preserved |
| Mean reversion in equities | None | Preserved | Preserved |
| Bond persistence | None | Preserved | Preserved |
| Sample size | Unlimited | Very limited (~81 non-overlapping 30yr periods) | Moderate |
| Parametric assumptions | Lognormal | None | None |

With IID Monte Carlo, sequence risk is symmetric and random - bad returns are equally likely at any point with no autocorrelation. In this world, starting conservatively and increasing equity is a clean hedge: if you're unlucky early you've protected capital; the equity you buy later doesn't inherit autocorrelated bad returns.

With historical data, bad periods cluster. A recession tends to be followed by a recovery; valuations mean-revert; equity variance ratios are below 1 at 30-year horizons. [[Anarkulova et al - Beyond the Status Quo (Critical Assessment of Lifecycle Advice)]] (2025) provides the sharpest statement: under block bootstrap, equity variance ratio is **0.75** at 30 years (variance *falls* with horizon) while bond variance ratio is **2.30** (variance *rises*). Bond/inflation correlation is -0.78 vs stock/inflation correlation of -0.01.

Under these conditions, starting conservative means your early portfolio still faces a structured bad period, and the equity you accumulate into later comes at higher valuations than IID assumes. Anarkulova finds all-equity failure rate 6.7% vs TDF 19.7% vs 60/40 16.9% -> glidepath portfolios have ~3x the failure risk of all-equity.

---

## Other Sources of Disagreement

**What is being optimised:**
- Raw failure probability -> tends to favour more equity (Blanchett, Estrada) or RE if IID (Pfau & Kitces)
- Risk-adjusted failure (S/V ratio) -> moderate static 60/40 (Blanchett)
- Terminal wealth / bequest -> strongly favours high equity throughout
- Expected utility with risk aversion -> depends heavily on gamma; moderate risk aversion (gamma ~3-4) often satisfied by 60-70% equity; high risk aversion (gamma > 5) can justify bonds even under block bootstrap

**US vs international:**
Bengen and Blanchett use US data only. Estrada's 19-country scope is important: US DE failure rates (4.9-8.6%) look reassuring but international averages (31-32%) are alarming. The survivorship bias issue - international median equity premium ~2pp lower than US, see [[US Equity Returns Show Survivorship Bias Relative to International Experience]] - bites across all strategies.

**Time horizon and withdrawal rate interaction:**
Blanchett's most important contextual finding: for low withdrawal rates and short periods, the choice of glidepath barely matters - difference in failure rates across all 43 strategies is only 1.56pp at 4% WR, 20-year period. The disagreements in the literature are most consequential for aggressive scenarios: long retirements (30-40 years) at moderate-to-high withdrawal rates (5%+). In these scenarios the range in failure probabilities is up to **62.45pp** across glidepaths. See [[4% Rule - Safe Initial Withdrawal Rate for a 30-Year Retirement]].

---

## Where Does This Leave the U-Shape?

The full-lifecycle **U-shape** (Pfau & Kitces) requires:
1. Declining equity during accumulation to be correct -> contradicted by [[Estrada - The Glidepath Illusion]] (2014), [[Anarkulova et al - Beyond the Status Quo (Critical Assessment of Lifecycle Advice)]] (2025), [[Parker et al - Simple Allocation Rules and Optimal Portfolio Choice]] (2024)
2. Rising equity during retirement to be correct -> contradicted by [[Estrada - The Retirement Glidepath]] (2015) and implicit in Blanchett (2007)

The **inverted U** (Estrada) has better empirical support when using historical rolling periods, but it requires DE to win in retirement, which is only true historically - under IID MC it loses.

The **static 60/40** position is the most robust across methodologies: Blanchett finds it best under bootstrap, Bengen under historical, Parker et al. under RL. The disagreement between DE and RE is somewhat academic relative to the shared finding that *dynamic glidepath management adds limited value over a sensible static allocation*.

The strongest empirical claim in the literature (Anarkulova 2025) rejects the entire framing. At the long horizons relevant to retirement, fixed income is the risky asset - not equities. The answer to the glidepath question is approximately **100% equity throughout**, with possibly a brief tactical bond allocation at the exact point of retirement to hedge rigid annual withdrawal rules. The welfare cost of traditional "safe" bond-heavy advice is enormous: 60/40 requires 94% more savings to achieve the same utility as all-equity; TDFs require 63% more.

---

## NZ Context

NZ Super provides a guaranteed income floor that partially resolves the sequence-of-returns risk problem which drives much of this debate. If Super covers essential spending, the KiwiSaver balance is effectively a bequest/discretionary vehicle - which argues for higher equity even in early retirement, weakening the case for DE or RE management altogether. See [[NZ Super Acts as Implicit Bond Justifying Higher Equity]] and [[4% Rule - Safe Initial Withdrawal Rate for a 30-Year Retirement]].

## Related
[[Decreasing Equity Strategy]]
[[Increasing Equity Strategy]]
[[Life-cycle Asset Allocation]]
[[Target Date Funds]]
[[Optimal Glidepath is Inverted U-Shaped Across Full Life Cycle]]
[[Declining-risk Strategies are sub-optimal]]
[[4% Rule - Safe Initial Withdrawal Rate for a 30-Year Retirement]]
[[Block Bootstrap Returns]]
