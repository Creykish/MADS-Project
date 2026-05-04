## Reference

Anderson, K., French, E., & Lam, T. (2004). You can't take it with you: Asset run-down at the end of the life cycle. *Economic Perspectives*, Federal Reserve Bank of Chicago, Q3, 40-54.

## The Question

Do elderly run down assets as they age? Answer matters for:
- Estate tax policy (if bequests, tax distorts savings)
- Retirement advice (how conservative should they be?)

## Three Econometric Problems

**Problem 1: Cohort Effects**

Cross-section compares age 70 to age 90 **in same year**.
- 90-year-olds were born 20 years earlier
- Had 40% lower lifetime income (growth ~1.7%/year)
- Cross-section overstates decline

**Problem 2: Differential Mortality**

Rich live longer:
- Age 80 mortality: 10.1% bottom quartile vs 7.0% top quartile  
- Age 70 life expectancy: 11.5 years (poor) vs 14.2 years (rich)
- Survivors are increasingly wealthy → hides decline

**Problem 3: Asset Price Shocks**

Following households over time captures:
- Intentional behavior (consumption/savings)
- Capital gains (unintended)

1993-2000:
- Stocks: +14.9%/year (vs 9.4% historical)
- Housing: +2.3%/year (vs 0.8% historical)
- Assets ~17% higher than expected from appreciation alone

Can't tell if growth = savings or luck.

## Solution: Fixed-Effects Panel

**Data:** AHEAD (Assets and Health Dynamics Among Oldest Old), 6,047 households age 70+, 1993-2000

**Method:** Track same households, use fixed effects to eliminate cohort/mortality bias.

**OLS (cross-section):**
- $283k at 70-74 → $100k at 90-94 (65% decline)

**Fixed-effects (panel):**
- Age 70-74 cohort: +37% from 1993-2000
- But this includes huge asset price boom

**After removing price effects:**
- Assets roughly flat or slightly declining
- Little evidence of intentional run-down

**Heterogeneity:**
- Couples: Strong accumulation (even post-price-shock)
- Singles: Roughly flat
- Hurd (1990) found same pattern

## Life-Cycle Model Simulations

**Model A: No uncertainty**
- Certain death age 82
- Assets decline to zero at death
- **Doesn't fit data**

**Model B: Add longevity risk**
- Uncertain lifespan
- Slower decline (precautionary savings)
- Still too fast vs data

**Model C: Add medical expense risk**
- Plus longevity
- Even slower
- Still too fast

**Model D: Add bequest motive**
- Plus longevity + medical risk
- **Fits data**

**Conclusion:** Slow run-down consistent with bequests, but not proof (could be very high risk aversion, underestimated medical risk, etc).

## Medical Expense Facts

From French & Jones (2004):

**By age (bad health woman):**
- Age 70: $1,200/year
- Age 100: $19,000/year

**Luxury good:**
- Age 95, 20th pct income: $2,700/year
- Age 95, 80th pct income: $16,000/year

**Catastrophic shocks:**
- 1% face $44k lifetime shock
- 0.1% face $125k lifetime shock
- Nursing homes largely uninsured

**Consumption floor:**
- US: SSI $7-9k + Medicaid + food stamps → ~$5k floor
- NZ: Super $26k single, $40k couple (way higher)
- Higher floor → less precautionary need?

## Calibration

**Parameters:**
- CRRA utility: $\gamma = 3$, $\beta = 0.95$
- $r = 4\%$ (fixed)
- Income $Y = \$20k$
- Initial assets $A_{70} = \$300k$
- Bequest: $\theta_B \frac{A^{1-\gamma}}{1-\gamma}$

**Accumulation:**
$$A_{t+1} = (1+r)(A_t + Y_t - m_t - C_t), \quad A_{t+1} \geq 0$$

where $m_t$ = stochastic medical expenses.

## For My NZ Research

**Must account for:**
1. Longevity risk (stochastic death)
2. Medical/aged care risk (~$60-80k/year, subsidy if assets < $240k)
3. Maybe bequest motive (test sensitivity)

**NZ differences:**
- No estate tax (abolished 1992)
- Higher consumption floor (NZ Super $26k vs US SSI $7k)
- Different aged care subsidy than Medicaid
- Higher life expectancy

**Portfolio implications:**
- Precautionary motive says hold liquid buffer
- But Anarkulova shows equity better for capital preservation
- Which dominates?

**Data questions:**
1. Do NZ retirees run down assets? (Use HES/SoFIE panel with FE)
2. How strong is bequest motive in NZ?
3. Distribution of aged care costs?
4. Does higher NZ Super reduce precautionary savings → allow more equity?

## Methodological Lessons

1. **Never use single cross-section** (cohort effects)
2. **Panel + fixed effects** essential  
3. **Separate intentions from price shocks**
4. **Model differential mortality**
5. **Include longevity risk + medical risk + constraints**

## Related

[[De Nardi French Jones - Differential Mortality and Medical Expenses]] - follow-up with better medical expense data
[[Hurd (1989, 1990)]] - earlier work, found similar patterns
[[Palumbo - Uncertain Medical Expenses]] - understated medical expenses
[[Cagetti & DeNardi (2003)]] - estate tax implications
