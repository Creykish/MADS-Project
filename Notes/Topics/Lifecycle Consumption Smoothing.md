## Lifecycle Consumption Smoothing

**Core Concept:** Rational households aim to maintain stable consumption over their lifetime despite varying income.

**Mechanics:**
- During accumulation (age 25–65): Save excess income
- During decumulation (age 65–death): Draw down wealth to maintain living standard
- Wealth peaks around retirement; declines thereafter

**Mathematical Basis:**
- Irving Fisher [1930] principle: optimal consumption path equalizes marginal utility across time periods
- Modigliani & Brumberg formalized this for finite-life households
- Leads to hump-shaped wealth accumulation path

**Why It Matters for Glidepaths:**
- If consumption is smooth → portfolio doesn't need to maintain constant risky-asset share (Merton constant-share theorem applies in idealized world)
- But real consumption is NOT smooth:
  - NZ retirees spend 2% less/year in real terms
  - Spending peaks in mid-60s before declining (health, activity constraints)
  - Household composition changes (widowing, downsizing)
- These deviations create need for *dynamic* allocation (time-varying glidepath)

**Key Papers:**
- Fisher [1930] *The Theory of Interest*
- Modigliani & Brumberg [1954] "Utility Analysis and the Consumption Function"
- Merton [1969] "Lifetime Portfolio Selection under Uncertainty"
- Your data: Le & Richardson [2023], RIIG [2024] on actual NZ spending patterns

---

## Human Capital and Labor Income

**Core Concept:** The present value of future labor income is part of household wealth ("human capital"), and younger workers' portfolios should reflect this.

**Mechanics:**
- Human capital is bond-like when the worker is young (stable, salary income)
- Acts as implicit wealth, reducing need for financial wealth in bonds
- As human capital declines (approaching retirement), workers should shift to equities in financial portfolio to maintain total risk

**Bodie, Merton & Samuelson [1992] Contribution:**
- "Labor supply flexibility and portfolio choice in a life cycle model"
- Younger worker: high human capital (large bond-like wealth) → rational to hold more equity in financial portfolio
- Older worker: low human capital (approaching zero) → rational to hold bonds in financial portfolio
- Implication: declining equity glidepath is actually *rational* IF human capital is accounted for

**Why This Is Contested:**
- Anarkulova [2025] doesn't accept the "human capital as bonds" logic
  - Argues labor income is risky (job loss, career interruption)
  - Young workers should diversify via equity in financial portfolio, not rely on bond-like labor income assumption
  - Human capital is real option value, not a true bond

**For Your Research:**
- Document NZ household labor income trajectories by age
- Estimate variance of labor income (e.g., construction vs. public servant)
- Should you adjust asset allocation for human capital risk?
- How does NZ Super change the calculus (guaranteed income replaces need for bond-like financial assets)?

**Related Concepts:**
- [[Income Predictability and Risk]]
- [[Occupational Choice and Portfolio Risk]]

---

## Annuity Markets and Adverse Selection

**Core Concept:** The absence of well-functioning annuity markets creates the "annuity puzzle"—households fail to insure longevity risk.

**The Puzzle:** Why don't retirees buy life annuities to guarantee income for as long as they live?

**Standard Prediction (Fisher):**
- Retirees should annuitize all or most wealth
- Eliminates longevity risk, allows full consumption smoothing
- Leaves optimal portfolio choice mostly moot (all bonds/bonds-equivalent)

**Reality:** Very few retirees buy annuities outside pension systems. Why?

**Adverse Selection (Friedman & Warshawsky [1985]):**
- People who live longer are more likely to buy annuities
- Annuity providers account for this → high premium
- Unfavorable payout for median person → most don't buy
- Creates "market failure"

**Alternative Explanations:**
- Utility from bequests (Masson [1984]): Households value leaving estate
- Preference for flexibility (Felix [2025]): Can't adjust spending if locked into annuity
- Complexity/uncertainty about provider solvency
- Home equity provides implicit annuity (downsize in retirement)

**Implication for NZ:**
- NZ Super acts as *implicit annuity* (guaranteed, indexed income floor)
- Reduces need for retirees to buy private annuities
- Means financial portfolio can remain equities-heavy (NZ Super covers "annuity" part)
- But medical/longevity risk remains uninsured

**For Your Research:**
- Model NZ Super as annuity equivalent; implies higher optimal equity allocation in financial assets
- Should your glidepath account for possibility that household downsizes home, releasing equity?
- Does this suggest wealth-responsive allocation (richer households in housing can hold more equity)?

**Related Papers:**
- Friedman & Warshawsky [1985] *The Cost of Annuities*
- Mitchell et al. [1999] *New Evidence on the Money's Worth of Individual Annuities*

---

## Sequence-of-Returns Risk and Dynamic Allocation

**Core Concept:** The order of returns matters, especially at the transition from accumulation to decumulation. A bad market early in retirement is worse than a bad market late.

**Mechanism:**
- Retirement starts with largest portfolio balance
- Withdrawals for spending deplete the balance
- Bad early returns → portfolio damaged when it's most vulnerable
- Good later returns hit smaller base → less recovery power
- Creating "safe zone" early retirement, risky zone late retirement (Pfau & Kitces)

**The Glidepath Debate Hinges Here:**

| View | Argument | Implication |
|---|---|---|
| **Estrada (historical data)** | Historical returns show mean reversion & clustering; bad periods followed by recovery; DE keeps equity when recovery comes → terminal wealth higher | Declining equity in retirement is optimal |
| **Pfau & Kitces (IID MC)** | With IID returns, bad periods don't necessarily follow recovery pattern; rising equity avoids sequence risk | Rising equity (U-shape) optimal |
| **Anarkulova (block bootstrap)** | Block bootstrap preserves autocorrelation; mean-reversion strong enough that all-equity dominates across all horizons | 100% equity throughout |
| **Parker (DRL + autocorr)** | With autocorrelation, sequence risk is real but NOT solved by rising equity; optimal is roughly flat (60% at retirement) | Nearly-static 60% equity |

**Why Data Source Matters:**
- IID assumptions → sequence risk is "random noise" → rising equity helps
- Historical data + mean reversion → sequence risk is autocorrelated → timing doesn't help much
- Block bootstrap → middle ground

**For Your Research:**
- NZ return data: Is it IID or autocorrelated?
- Test Anarkulova's variance ratios on NZ bonds + equities
- What correlation structure best fits NZ data?
- Does it support all-equity (Anarkulova) or constant allocation (Parker)?

**Related Concepts:**
- [[Volatility Clustering and Mean Reversion]]
- [[Return Predictability in Asset Markets]]
- [[Withdrawal Rate and Portfolio Failure]]

---

## Objective Function and Risk Measure

**Core Concept:** Different papers optimize *different* things. When they reach different conclusions, often it's because they're answering different questions.

**Options:**

1. **Failure probability** (Pfau & Kitces [2014])
   - Minimize: Prob(portfolio depleted before death)
   - Result: U-shaped (rising equity in retirement)

2. **Failure magnitude** (Estrada [2015])
   - Minimize: Expected shortfall if failure occurs
   - Result: Declining equity (preserve capital early)

3. **Success/Variability ratio** (Blanchett [2007])
   - Maximize: Success probability / Portfolio std dev
   - Result: 60/40 static (Pareto frontier)

4. **Expected utility** (Parker [2024])
   - Maximize: $E[U(C_t)]$ with CRRA utility
   - Result: Roughly flat (60% equity) throughout lifecycle
   - Accounts for both failure risk AND utility of wealth

5. **Long-term wealth** (Anarkulova [2025])
   - Maximize: Expected terminal wealth at 90
   - Result: 100% equity (maximizes growth)

**Why It Matters:**
- Failure probability cares about downside (tail risk) → conservative early
- Utility cares about both upside and downside → balanced
- Terminal wealth cares only about growth → aggressive

**For Your Research:**
- Which objective is right for NZ retirees?
- Failure probability if you're poor (need income floor)
- Utility if you're moderate wealth (can tolerate volatility)
- Terminal wealth if you have bequests motive
- **Probably a combination:** Failure prob up to acceptable floor, then utility/growth

**Related Concepts:**
- [[Prospect Theory and Loss Aversion]]
- [[Risk Tolerance and Household Characteristics]]
- [[Quantifying Welfare Cost of Suboptimal Policy]]

---

## Spending Rules and Flexible Consumption

**Core Concept:** Fixed withdrawal rules (e.g., "4% rule") are suboptimal; households should adjust spending based on market performance.

**Fixed-Rate Rules:**
- Bengen [1994]: "4% rule" (withdraw 4% of starting portfolio, inflate for CPI)
- Weakness: Doesn't respond to market conditions
- Can lead to severe depletion in bad sequence, or excess wealth accumulation in good sequence

**Flexible Rules (Felix [2025] argument):**
- Adjust spending based on current portfolio value
- E.g., "spend max(floor, α × wealth)"
- Allows portfolio to recover from downturns
- Matches observed NZ behavior: retirees reduce spending when markets are weak

**Anarkulova [2025] Finding:**
- Under 4% rule + 100% equity: brief tactical shift to bonds at retirement
- Under flexible spending + 100% equity: stay fully equity throughout
- Implication: spending flexibility is AS important as asset allocation choice

**For Your Research:**
- Model spending as declining real trend (your data shows 2%/year decline)
- Allow spending flexibility on top of trend
- This should substantially improve welfare vs. fixed-rate rules
- NZ retirees appear to do this naturally (adjust discretionary spending to market conditions)

**Related Concepts:**
- [[Withdrawal Rate and Portfolio Failure]]
- [[Dynamic Consumption-Savings Decisions]]
- [[Spending Rule Specification]]

---

## Wealth-Responsive vs. Age-Only Allocation

**Core Concept:** Optimal allocation should depend on BOTH age AND wealth level (Makinen [2024] control matrix framework).

**Age-Only (Standard TDF):**
- "At age 60, hold 60% equity" — same for rich and poor
- Simple to communicate and implement
- Ignores household's actual financial situation

**Wealth-Responsive (Control Matrix):**
- "At age 60 with $200k wealth, hold 75% equity; with $600k wealth, hold 50% equity"
- Richer households can tolerate volatility better
- Poorer households need safer portfolio to avoid ruin
- Parker [2024] finds huge heterogeneity: 10th percentile <20% equity in retirement; 90th percentile ~100%

**Why It Matters:**
- NZ Super is wealth-responsive (covers costs for poor retirees, not rich)
- A retiree on NZ Super alone needs safer portfolio
- A retiree with $1M+ can afford equity volatility
- Current policy (KiwiSaver defaults, advice) are age-only → suboptimal

**For Your Research:**
- Your model should allow both age and wealth as state variables
- Makinen [2024] provides optimization framework
- Should investigate: what is welfare gain from wealth-responsive vs. age-only?
- Is it operationally feasible for financial adviser to implement? (Control matrix complexity)

**Related Concepts:**
- [[Control Matrix Optimization]]
- [[State-Space Modeling of Lifecycle Decisions]]

---

## NZ-Specific Factors Not in Standard LCH

1. **Home Equity and Downsizing:** Many retirees own outright; could downsize to fund consumption. LCH doesn't address housing explicitly.

2. **NZ Super as Annuity:** Guaranteed income floor eliminates longevity risk, changes optimal equity allocation vs. countries without it.

3. **Spending Decline Pattern:** NZ empirically shows 2%/year real decline; not captured by LCH constant-consumption assumption.

4. **Housing Rental Market:** NZ renters (14% of aged) face ongoing costs; homeowners face maintenance + rates; affects precautionary saving.

5. **Long-Term Care Costs:** Not public; private residential care expensive; creates precautionary motive not modeled in classical LCH.

6. **KiwiSaver as Forced Saving:** Changes household time-inconsistency problem; may increase actual savings relative to stated preferences.

---

## Research Roadmap

1. **Test LCH predictions on NZ data:**
   - Does W/Y match prediction for growth rate + retirement length?
   - Are bequests <25% of total wealth?
   - Does saving decline in old age (slow vs. fast)?

2. **Estimate NZ return properties:**
   - IID or autocorrelated?
   - Variance ratios at 30-year horizon
   - Inflation correlation (especially bonds)

3. **Specify NZ-calibrated model:**
   - Spending trajectory (2%/year decline)
   - NZ Super as exogenous floor
   - Housing wealth optionality
   - Medical/care cost risk

4. **Optimize asset allocation:**
   - Compare objective functions (failure prob, utility, terminal wealth)
   - Compare return models (IID, historical, block bootstrap)
   - Show wealth-responsive vs. age-only glidepath
   - Quantify welfare gain

5. **Test robustness:**
   - Sensitivity to spending decline rate
   - Sensitivity to NZ Super level (policy scenarios)
   - Sensitivity to retirement age
   - Household heterogeneity (single, couple, children, housing)
