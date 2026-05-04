[[Life-cycle Asset Allocation]] strategies that decrease equity exposure with age ([[Decreasing Equity Strategy]]) consistently produce worse outcomes than constant or increasing equity strategies, across multiple datasets, methodologies, and countries.

## Key Evidence

**[[Estrada - The Glidepath Illusion]] (2014):**
- Tested declining vs increasing vs constant equity glidepaths across 19 developed markets
- [[Increasing Equity Strategy]] outperformed [[Decreasing Equity Strategy]] in **all 19 countries**
- Significant differences in terminal wealth: increasing equity -> substantially more assets at death
- Named the phenomenon the "glidepath illusion": declining risk appears prudent but is actually inferior

**[[Anarkulova et al - Beyond the Status Quo (Critical Assessment of Lifecycle Advice)]] (2025):**
- [[Block Bootstrap Returns]] reveal the mechanism: stocks mean-revert (variance ratio 0.75 at 30 yrs), bonds diverge (variance ratio 2.30 at 30 yrs)
- The asset that glidepaths shift toward (bonds) is actually riskier than the asset they shift away from (equities) at retirement horizons
- Ruin probability: all-equity 6.7% vs TDF 19.7% vs 60/40 16.9% -> glidepath portfolios have 3x the ruin risk
- Welfare cost: 60/40 requires 94% more savings; TDF requires 63% more savings to match all-equity utility

**[[Dolvin - Asset Allocation for Retirement Simple Heuristics and Target-Date Funds]] (2010):**
- Bootstrapped historical returns: [[100% Stock Portfolio]] outperforms all age-in-bonds variants
- Most TDFs use ~120-minus-age rule and end at 30-40% equity in retirement -> too conservative

**[[Shiller - Life-cycle personal accounts proposal for Social Security]] (2006):**
- Tested the age-in-bonds approach for proposed Social Security personal accounts
- 100% equity would likely have produced better outcomes than the proposed declining-equity scheme
- Used historical US data 1871-2004

**[[Parker et al - Simple Allocation Rules and Optimal Portfolio Choice]] (2024):**
- RL-solved optimal policy: equity at retirement ~60% vs TDF 30-40%
- TDFs too conservative post-retirement; welfare cost 1.7-2.8% of lifetime consumption
- Deep RL accounts for business cycle, dividend yield, wealth level -> all favor higher equity than TDFs provide

## The Mechanism

Glidepaths shift from assets with declining long-run variance (stocks, VR=0.75) to assets with rising long-run variance (bonds, VR=2.30). The conventional wisdom is based on short-run statistics where bonds look safe, but at the 30-year horizons relevant to retirement planning, this reverses.

Additionally, bonds have a -0.78 correlation with inflation -> they destroy real purchasing power when inflation rises. Stocks are approximately inflation neutral (corr = -0.01).

## Does Any Declining-Equity Strategy Make Sense?

The human capital argument ([[Human Capital]]) provides a theoretical justification that the evidence doesn't completely overturn - the mechanism is real (human capital is bond-like) but the conclusion changes if the replacement asset (bonds) is itself suboptimal. Declining equity can still be rational for:
- Very high risk aversion (gamma > 5)
- Investors without NZ Super or other consumption floors
- Short time horizons near retirement where sequence-of-returns risk dominates

## Related
[[Life-cycle Asset Allocation]]
[[Decreasing Equity Strategy]]
[[100% Stock Portfolio]]
[[Increasing Equity Strategy]]
[[Block Bootstrap Returns]]
[[Target Date Funds]]