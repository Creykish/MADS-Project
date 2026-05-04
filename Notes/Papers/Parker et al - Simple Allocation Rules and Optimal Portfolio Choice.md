## Reference

Duarte, V., Fonseca, J., Goodman, A., & Parker, J. A. (2024). Simple allocation rules and optimal portfolio choice over the lifecycle. *Working Paper*. MIT and NBER.

## Summary

This is a landmark paper for my research - it uses deep reinforcement learning to solve a highly realistic lifecycle model and evaluates how well simple age-based portfolio rules (like Target Date Funds) perform relative to fully optimal behavior. Critical for understanding whether the simple heuristics I might derive are actually optimal or leaving value on the table.

### Key Innovation: Machine Learning Solution Method

The authors solve a lifecycle model with 20+ state variables using policy gradient algorithms (deep reinforcement learning). This is computationally infeasible with traditional numerical dynamic programming.

**Model Features (Comprehensively Realistic):**
- Dual-earner household (husband and wife)
- Gender-specific earnings profiles with stochastic, left-skewed shocks
- Three asset classes: stocks, bonds, money market
- Liquid accounts + tax-advantaged retirement accounts (with employer match, withdrawal penalties)
- Housing: rent, own with mortgage, or own outright
- Refinancing costs, cash-in-advance constraint
- Progressive tax system with consumption floor
- Retirement: pension based on lifetime earnings, medical expense shocks, mortality risk, bequest motive

**Why This Matters to Me:**
I'm using a similar problem structure (Monte Carlo-based optimization with realistic constraints). This paper validates that approach and shows what a "fully optimal" solution looks like in a realistic setting.

### Main Substantive Finding #1: Age-Based Rules Work Pretty Well During Accumulation

**Average Optimal Equity Share (Retirement Accounts):**
- Age 25-50: 80-85% in stocks
- Age 50-65: Gradually declining
- Retirement: ~60% in stocks

**Typical Target Date Fund:**
- Until age 40: ~90% stocks
- Age 50: ~75% stocks
- Retirement: Declining to 30-40% stocks

**Validation:** TDFs track average optimal behavior quite well until age 50. This is reassuring - the simple age-based rules that emerged from earlier research (Samuelson, Merton, Cocco et al.) are decent approximations.

**But:** TDFs are too conservative in retirement, holding only 30-40% stocks vs optimal 60%.

### Main Finding #2: Huge Heterogeneity in Optimal Portfolios

While average optimal portfolios match TDFs, the **90th percentile** holds nearly 100% stocks at all ages, while **10th percentile** holds <20% during retirement.

**Optimal equity shares vary most by:**
1. **Wealth level** - Wealthier households hold more stocks (can tolerate volatility)
2. **Business cycle state** - Higher stocks in expansions
3. **Dividend-price ratio** - Higher stocks when expected returns high

**Implication for My Research:**
Simple age-based rules miss important heterogeneity. I should:
- Report distribution of optimal allocations, not just means
- Show how allocation depends on wealth level (critical for NZ context)
- Consider return predictability (dividend yields)

### Main Finding #3: Welfare Cost of Simple Rules

**Consumption-equivalent loss** from following TDF instead of fully optimal:
- **1.7% of consumption** if household re-optimizes other decisions
- **2.8% of consumption** if household can't re-optimize

From start-of-life perspective (with discounting): 0.45-0.59% due to low weight on late-life losses.

**Comparison: Constant 2/3 stocks rule:**
Similar losses to TDF despite being much simpler, because TDFs are too conservative in retirement.

**My Interpretation:**
- Simple rules aren't terrible (~2% consumption loss is meaningful but not catastrophic)
- Most loss comes from being too conservative in retirement
- Opportunity for improvement by customizing on wealth, cycle, valuations

**For my research:** I should quantify welfare losses from simpler rules vs my optimization to show value of customization.

### Methodological Contribution: Deep Reinforcement Learning

**Traditional NDP Approach:**
1. Define state space on grids
2. Solve Bellman equation recursively using numerical integration
3. Computationally expensive, scales poorly with states

**Their Approach (Policy Gradient):**
1. Parameterize policy functions as neural networks
2. Simulate many sample paths with current policy
3. Use gradient descent to improve policy (maximize expected lifetime utility)
4. No grids, no numerical integration - just simulation

**Advantages:**
- Much faster (hardware optimized for ML)
- Scales to 20+ states easily
- Easier to program (less error-prone)
- Captures how investors actually learn (from others' experiences)

**Relevance to My Work:**
I'm using Monte Carlo simulation + quasi-Newton optimization (similar spirit, different implementation). Their validation of this approach vs traditional methods is valuable. I should cite this as precedent for simulation-based optimization.

However, they optimize over neural network weights while I optimize directly over policy parameters. Trade-offs:
- Neural nets more flexible (can capture complex nonlinearities)
- Direct parameterization more interpretable (can examine policy directly)

---

## Asset Return Generating Process (DETAILED)

Three assets: short-term government bills (j=1), long-term corporate bonds (j=2), equities (j=3).

### State Variables for Returns

**Two aggregate risk drivers:**

1. **Business cycle state** $e_t \in \{0,1\}$ — 0 = expansion, 1 = recession. Evolves via 2×2 Markov transition matrix $P_e$ (estimated from NBER recession dates 1915–2015).

2. **Dividend-price ratio (log)** $v_t$ — AR(1) with recession-state-dependent intercept:
$$v_t = \theta^v_0 + \theta^v_1 v_{t-1} + \theta^v_2 \Delta e_t^+ + \theta^v_3 \Delta e_t^- + \varepsilon^v_t$$
where $\Delta e_t^+ = \max\{0, e_t - e_{t-1}\}$ (recession starts), $\Delta e_t^- = \max\{0, e_{t-1} - e_t\}$ (recession ends). This captures the well-documented fact that dividend yields spike in recessions and revert in recoveries — and that expected returns are high when yields are high (value signal).

Dividend yield data: Jordà, Knoll, Kuvshinov, Schularick & Taylor (2019), US 1915–2015.

### Log Return Process

Log gross return on asset $j$ at time $t$:
$$\ln R_{j,t} = \theta^j_0 + \theta^j_1 v_{t-1} + \theta^j_2 \Delta e_t^+ + \theta^j_3 \Delta e_t^- + \varepsilon^j_t$$

- **Intercept shifts** at recession start/end $\to$ captures asymmetric cycle effects on returns
- **Loading on $v_{t-1}$** $\to$ return predictability from dividend yield: when yields are high, expected returns are high (for equity especially)
- **Transitory shock** $\varepsilon^j_t$ $\to$ asset-specific noise

**Key feature:** $v_t$ and $e_t$ are correlated with each other *and* with the labor income process $\to$ this creates realistic co-movement between portfolio returns and wages (i.e., equity is a worse hedge when you need it most: in recessions your income also falls).

### Parameters

All $\theta$ parameters estimated from 1915–2015 US data:
- Bills and long corporate bonds: from Jordà et al. (2019)
- Equity: same source
- Corporate bond index: Dow Jones Total Corporate Bond index

Full parameter vectors listed in paper's online appendix (too long for Table I).

### What This Captures

| Feature | How modelled |
|---|---|
| Return predictability | $v_{t-1}$ loading in return equation |
| Business cycle variation in returns | $\Delta e_t^+$, $\Delta e_t^-$ intercept shifts |
| Correlation between assets | Common $v_t$, $e_t$ drivers |
| Labor income–return correlation | Both load on $e_t$ |
| Serial correlation in expected returns | AR(1) in $v_t$ |

### Implications for Portfolio Choice

The predictability in returns (via dividend yield $v_t$) means the optimal portfolio is **not** constant even for a given wealth level and age — it varies with valuations. This is why "state variables" like $v_t$ and $e_t$ appear in the state space $\Xi_t$.

The authors find $v_t$ and $e_t$ are among the **top drivers of cross-household heterogeneity** in optimal equity shares — bigger effect than age alone in many cases. This is the justification for their claim that further customising TDFs to account for market conditions could add substantial welfare gains.

### Comparison to Simpler Models

Cocco, Gomes & Maenhout (2005): i.i.d. returns (no predictability). Wachter (2010): dividend yield predictability but no business cycle. This paper: both, plus correlation with labour income $\to$ more realistic but more state variables to track.

**For my model:** I currently assume i.i.d. returns. Adding a simple AR(1) predictability channel (like CAPE ratio loading) would be a meaningful extension — and this paper gives the structural motivation for it.


### Key Results by Wealth Level

**Low Wealth Households:**
- Optimal equity share rises with age until 45 (building human capital)
- More responsive to state variables (less buffer)
- Higher welfare costs from simple rules

**High Wealth Households:**
- Optimal equity share relatively stable until 50
- Less responsive to state variables (wealth provides buffer)
- Similar welfare costs from simple rules

**Implication:** I should show results stratified by wealth level. NZ context with universal NZ Super may make low-wealth optimization very different from US.

### Why TDFs Are Too Conservative in Retirement

The paper shows TDFs decline to 30-40% stocks by late retirement while optimal is ~60%.

**Possible Explanations:**
1. **Bequest motive** - If leaving bequest, longer horizon justifies more stocks
2. **Declining consumption** - If consumption falls with age, less need for safe assets
3. **Pension floor** - SS/annuity provides bond-like floor, can take more risk with residual
4. **Required minimum distributions** - Force drawdowns, making portfolio effectively shorter-lived

**Relevance to NZ:**
- NZ Super is generous universal floor (~$46k/year couple)
- Consumption declines ~2%/year real (from RIIG paper)
- High home ownership (housing = implicit safe asset)

All three factors suggest NZ retirees can hold *more* stocks in retirement than TDFs suggest. My optimization should test this.

### Optimal Portfolios Respond to Return Predictability

When expected stock returns are high (low valuations, high dividend yields):
- Optimal equity share increases
- Effect is larger for wealthier households
- Suggests value of tactical allocation based on valuations

**Implication:** I should consider whether to include return predictability in my model. Arguments:
- **For:** More realistic, captures what sophisticated investors do
- **Against:** Most people don't time the market, simpler model more policy-relevant
- **Compromise:** Solve with return predictability, show both tactical and fixed rules

### Comparison to Prior Literature

**Cocco, Gomes & Maenhout (2005):**
- Single-earner lifecycle model
- Found declining equity shares with age (similar to this paper)
- But simpler model (no housing, taxes, etc.)

**This paper's contribution:**
- Validates CGM findings in much more realistic setting
- Shows simple rules derived from CGM work pretty well
- Quantifies heterogeneity and welfare costs

**My position relative to this paper:**
- I'm solving NZ-specific version with different institutions
- Focus on retirees (they cover full lifecycle)
- Simpler model than Parker et al, more complex than CGM
- Similar to Makinen & Toivanen (Monte Carlo optimization)

### Implications for My Research Design

**What I Should Do:**
1. **Report distributions not just means** - Show 10th, 50th, 90th percentile optimal allocations
2. **Stratify by wealth** - Critical for policy relevance in NZ
3. **Compare to simple rules** - Age-based, constant allocation, target date glide path
4. **Calculate welfare costs** - Consumption-equivalent losses from suboptimal rules
5. **Test sensitivity to assumptions** - Bequest motive, risk aversion, return predictability

**What I Can Simplify (vs Their Model):**
1. **No housing** - Most NZ retirees own outright, separate decision
2. **No labor income** - Focus on retirees (though could model flexible retirement)
3. **Simpler tax treatment** - NZ has no capital gains tax, simpler system
4. **Single person or couple-equivalent** - Avoid dual-earner complexity

**What I Should Add (NZ-Specific):**
1. **NZ Superannuation** - Universal pension floor
2. **KiwiSaver** - Accumulation vehicle with employer/govt matching
3. **Residential care means testing** - Asset test around $250k affects late-life strategy
4. **Declining consumption profile** - 2%/year real decline (empirically validated)

### Key Quotes & Results to Reference

**On simple rules working well during accumulation:**
> "Both for optimizing households and for households that under-save, the average fully-optimal portfolio at each age conforms well to current simple age-dependent prescriptive rules until shortly before retirement"

**On heterogeneity:**
> "Fully-optimal equity shares have substantial heterogeneity, particularly by wealth level, state of the business cycle, and dividend-price ratio"

**On welfare costs:**
> "The consumption-equivalent losses from conditioning portfolio shares on age alone are substantial, around 2 to 3 percent of consumption"

**On conservative TDFs in retirement:**
> "The average optimal equity share declines linearly to about 60% at retirement, after which it is roughly constant. In contrast, equity shares in TDFs typically decline more rapidly to reach 50% at retirement and then continue to decline slowly after retirement to 30-40%"

### Open Questions They Raise

1. **Why don't people follow optimal rules?**
   - Behavioral barriers
   - Information costs
   - Complexity of optimization
   - My simpler approach may be more tractable

2. **Should TDF glide paths be steeper or flatter?**
   - Current glide paths too conservative in retirement
   - But one-size-fits-all may not work
   - Customization by wealth needed

3. **How to incorporate return predictability in practice?**
   - Most people can't time markets well
   - But systematic rules (e.g., rebalance to target based on P/E ratios) might help

### Critical Takeaways for My Paper

1. **Simple age-based rules aren't terrible** - They capture average optimal behavior pretty well, validating decades of research
   
2. **But heterogeneity matters** - Wealth level, return expectations, and individual circumstances create wide dispersion in optimal allocations
   
3. **TDFs too conservative in retirement** - Holding 60% vs 30% stocks in retirement is important for long-term outcomes
   
4. **Machine learning methods validated** - Deep RL can solve problems traditional methods can't, similar in spirit to my Monte Carlo approach
   
5. **Welfare costs are moderate** - 2-3% consumption loss from simple rules is meaningful but shows rules aren't disastrously bad

For my NZ-focused research, I should:
- Solve for optimal allocation conditional on wealth level (not just age)
- Compare to NZ-equivalent of TDFs (conservative balanced funds?)
- Quantify value of customization in NZ context
- Show if/why NZ retirees can hold more stocks than US models suggest

## Related Papers

[[Cocco - Consumption and Portfolio Choice over the Life Cycle]]
[[Makinen - Monte Carlo Optimisation]]
[[Dolvin - Asset Allocation for Retirement Simple Heuristics and Target-Date Funds]]

## Methodological Links

This paper's use of deep RL connects to [[Makinen - Monte Carlo Optimisation]]'s use of Monte Carlo + quasi-Newton methods. Both avoid traditional dynamic programming, enabling more realistic models.
