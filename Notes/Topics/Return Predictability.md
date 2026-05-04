The empirical finding that future equity returns can be partially predicted using current observable variables, particularly the dividend-price ratio. This violates the IID (independent and identically distributed) return assumption used in many lifecycle models.

## Key Predictors

- **Dividend-price (D/P) ratio:** High D/P -> high expected future returns. Low D/P -> low expected future returns
- **Business cycle state:** Expansion vs recession affects expected returns, volatility, and correlations between assets
- **P/E ratios (Shiller CAPE):** High CAPE -> lower future 10-year returns historically

## Why It Matters for [[Life-cycle Asset Allocation]]

**[[Parker et al - Simple Allocation Rules and Optimal Portfolio Choice]] (2024):**
- Incorporates a Markov business cycle model: state e_t in {0,1} (recession/expansion)
- Log dividend-price ratio v_t follows AR(1) with recession-state-dependent intercepts
- Optimal allocation varies with BOTH the business cycle state AND the current dividend yield
- When D/P is high -> buy more stocks (expected returns higher)
- In recession state -> reduce stocks (higher uncertainty, lower expected returns)
- This is entirely missed by [[Target Date Funds]] and [[Age in Bonds Rule]] which only respond to age

**Implications:**
- Age is a poor single predictor of optimal allocation
- Wealth + business cycle + valuation levels all matter more for within-period allocation decisions
- See [[Optimal Allocation Depends on Wealth and Cycle State]]

## [[Block Bootstrap Returns]] and Predictability

[[Anarkulova et al - Beyond the Status Quo (Critical Assessment of Lifecycle Advice)]] (2025):
- Block bootstrap preserves momentum and mean reversion in returns
- This captures the predictability embedded in return sequences
- IID bootstrap loses all predictability structure -> gives wrong optimal allocation
- Block bootstrap -> mean reversion in stocks, persistence in bonds -> 100% equity optimal
- IID -> conventional allocation advice (38% stocks at 65) -> dramatically sub-optimal in reality

## Short-run vs Long-run Predictability

- Short-run: predictability is weak (efficient markets at short horizons)
- Long-run: dividends predict returns better at 5-10 year horizons than 1-month
- Variance ratios: stocks VR=0.75 at 30 years (mean reversion) -> partially reflects long-run predictability

## Related
[[Life-cycle Asset Allocation]]\n[[Block Bootstrap Returns]]\n[[Risk Return Tradeoff of Assets]]\n[[Asset Allocation]]\n[[Target Date Funds]]\n[[Optimal Allocation Depends on Wealth and Cycle State]]\n[[Parker et al - Simple Allocation Rules and Optimal Portfolio Choice]]\n[[Anarkulova et al - Beyond the Status Quo (Critical Assessment of Lifecycle Advice)]]
