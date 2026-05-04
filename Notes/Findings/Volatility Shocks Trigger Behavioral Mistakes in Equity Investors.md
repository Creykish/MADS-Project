Volatility shocks in equity markets cause investors to systematically reduce equity holdings, perceive assets as riskier, and make sub-optimal portfolio decisions. This is a significant practical caveat to strategies that require holding through high-volatility periods (such as [[100% Stock Portfolio]]).

## Evidence

**[[Huber Huber Kirchler - Volatility Shocks and Investment Behavior]] (2022):**

Finance professionals (n=202) and students (n=282) in a controlled experiment:

- Investment propensity is negatively correlated with shock direction: a downward shock significantly reduces equity allocation
- Finance professionals perceive ALL volatility shocks as riskier (up, down, or flat) -> they reduce equity even after upward volatility episodes
- Satisfaction drops sharply with downward shocks -> emotional response overlays rational allocation
- The effect persists into the post-shock period: allocations do not fully recover even after volatility normalises

**Key behavioral pattern:**
- Rational response: hold through volatility; reassess only if expected returns change
- Actual response: cut equity during and after any volatility spike
- Professionals do this even when the shock involves *no loss* (upward or flat shock)

## Why This Matters for [[100% Stock Portfolio]] Strategies

Long-run all-equity strategies are theoretically optimal ([[All-equity Portfolios Outperform Glidepaths at Long Horizons]]) because:
- Stocks mean-revert at long horizons
- Volatility spikes are followed by recoveries

But this benefit only accrues to investors who *hold through* the volatility. If investors:
1. Sell during a downward volatility shock
2. Do not fully reinvest before the recovery
3. Convert paper losses into realised losses

...then the theoretical outperformance disappears or reverses. The behavioral friction is a real cost not captured in return simulations.

## The Double Penalty

Selling during a volatility shock creates two losses:
1. **Realised loss:** Selling at a depressed price turns a paper loss into a permanent one
2. **Missed recovery:** Missing the rebound that follows high-volatility periods (the mean reversion that makes stocks safer at long horizons per [[Block Bootstrap Returns]])

Both effects combined mean actual returns fall well short of the theoretical all-equity return.

## Interaction with [[Heimer et al - YOLO Mortality Beliefs and Household Finance]]

Biased mortality beliefs already cause young people to undersave and retirees to underconsume. Volatility-triggered behavioral mistakes compound this: investors not only start with wrong savings rates but also earn lower returns by panic-selling during volatile periods.

## Practical Implication

The behavioral case against [[100% Stock Portfolio]] is not that it is theoretically wrong, but that it is psychologically hard to implement. An investor needs to:
- Ignore short-term price movements during volatility spikes
- Resist the urge to reduce equity when perceived risk rises
- Avoid checking portfolio values frequently (myopic loss aversion)

Automated strategies (e.g., default KiwiSaver growth fund with no active switching) partially solve this by removing the decision from the investor. [[Target Date Funds]] attempt to remove this friction but over-correct into conservatism.

## Related
[[100% Stock Portfolio]]
[[Life-cycle Asset Allocation]]
[[Investor Risk Perception]]
[[All-equity Portfolios Outperform Glidepaths at Long Horizons]]
[[Block Bootstrap Returns]]
[[Heimer et al - YOLO Mortality Beliefs and Household Finance]]
[[Mortality Belief Errors Cause Systematic Financial Mistakes]]
[[Huber Huber Kirchler - Volatility Shocks and Investment Behavior]]
