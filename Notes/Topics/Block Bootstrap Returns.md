A simulation method for asset returns that resamples historical data in blocks (consecutive periods) rather than drawing individual observations randomly. This preserves the time-series structure of returns including momentum, mean reversion, changing correlations, and volatility clustering.

## Why It Matters

Most lifecycle models assume IID (independent and identically distributed) returns: each period is drawn independently from the same distribution. This is mathematically convenient but empirically wrong.

**[[Anarkulova et al - Beyond the Status Quo (Critical Assessment of Lifecycle Advice)]] (2025)** shows that the choice between IID and block bootstrap fundamentally changes the optimal portfolio:
- IID + domestic-only data -> conventional advice: **38% stocks at age 65**
- Block bootstrap + international data -> **100% equity throughout**

The two methods produce opposite conclusions because they give different answers about the long-run properties of stocks vs bonds.

## What Block Bootstrap Preserves

- **Mean reversion in stocks:** A run of bad returns tends to be followed by better-than-average returns (and vice versa) -> variance shrinks at long horizons -> variance ratio < 1
- **Persistence in bonds:** Bond return shocks are more persistent -> variance grows at long horizons -> variance ratio > 1
- **Time-varying correlations:** Stock/bond correlation rises from ~0.1 at 1 month to **0.45** at 30 years (diversification shrinks)
- **Inflation dynamics:** Bond/inflation correlation = -0.78 shows up properly; not averaged away
- **Momentum:** Short-run momentum in returns is preserved

## IID Gets the Long-run Properties Wrong

Under IID:
- Variance scales exactly linearly with time
- Correlations are constant at 1-month level
- Bond/inflation relationship is diluted
- Result: bonds look like safe diversifiers at all horizons -> glidepath to bonds looks rational

Under block bootstrap:
- Stocks become relatively safer at long horizons
- Bonds become relatively riskier at long horizons
- Bond/stock diversification benefit disappears
- Result: 100% equity dominates

## The Variance Ratio Test

Variance ratio at horizon T = Var(T-period return) / (T * Var(1-period return))

| Asset | 1-month VR | 30-year VR |
|---|---|---|
| Domestic stocks | 1.0 | 0.75 |
| Bonds | 1.0 | 2.30 |
| Bills | 1.0 | ~2.0 |

This is the decisive evidence against bonds for long-horizon investors.

## Related
[[Life-cycle Asset Allocation]]\n[[100% Stock Portfolio]]\n[[Risk Return Tradeoff of Assets]]\n[[Return Predictability]]\n[[Declining-risk Strategies are sub-optimal]]\n[[Anarkulova et al - Beyond the Status Quo (Critical Assessment of Lifecycle Advice)]]
