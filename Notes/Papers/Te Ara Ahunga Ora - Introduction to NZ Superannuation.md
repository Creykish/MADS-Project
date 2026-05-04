## Reference

Te Ara Ahunga Ora Retirement Commission. (2021). *An introduction to New Zealand Superannuation*. Policy Papers 2021 | 03.

## Summary

Essential reference for understanding NZ Superannuation (NZ Super), the universal public pension that forms the foundation of retirement income in New Zealand. Understanding NZ Super is critical for my lifecycle optimization model because it provides a substantial guaranteed income floor that reduces downside risk and affects optimal asset allocation decisions.

### Key Features of NZ Super

**Eligibility Requirements:**
- Age 65 or older
- NZ citizen or permanent resident
- Living in NZ, Cook Islands, Niue, or Tokelau
- **Residency requirement:** Currently 10 years since age 20, with 5 years since age 50
  - Changing to 20 years for those born after July 1977 (phased implementation)
  - Time in countries with pension agreements (Australia, Canada, UK, etc.) can count

**Not Means-Tested:**
- Everyone eligible receives it regardless of income or assets
- This is crucial: unlike many countries, NZ doesn't reduce pension based on wealth
- Creates very different optimization problem than US (with means-tested SSI)

**Payment Levels (I need to update with current 2024 rates):**
- Universal benefit, adjusted for inflation
- Higher for couples, lower for singles
- Different rates for "living alone" vs "sharing"

**Portability:**
- Can receive reduced NZ Super if living in certain Pacific nations (50-100% depending on years of residency)
- Different rules for countries with pension agreements
- Must be in NZ to apply initially

### Implications for My Lifecycle Model

**1. Guaranteed Income Floor**

NZ Super provides a substantial certain income from age 65 onwards. Based on current rates (I need to verify exact amounts):
- Single living alone: ~$26,000/year
- Single sharing: ~$24,000/year  
- Couple: ~$40,000/year (combined)

From Le & Richardson (2023), median couple spending is ~$40,000-45,000/year. This means **NZ Super covers the majority of median retiree spending**.

**Modeling implication:** I should include NZ Super as:
$$ I_{super}(t) = \begin{cases}
0 & t < 65 \\
B_{super} \cdot (1+\pi)^{t-65} & t \geq 65
\end{cases} $$

Where $B_{super}$ is base benefit (couple or single rate) and $\pi$ is inflation indexation.

**2. No Asset or Income Testing**

Unlike US means-tested programs, NZ Super is universal. This means:
- No penalty for accumulating wealth
- No cliff effects in optimization
- Simplifies modeling (no discontinuities in budget constraint)

**Contrast with US/Australia:**
- US has means-tested SSI for low income
- Australia has asset-tested Age Pension
- Creates complex incentives around asset holdings

**For my model:** NZ's universal system means optimal behavior is "cleaner" - no need to game means tests or hide assets.

**3. Changes Optimal Risk-Taking**

NZ Super acts like a **riskless asset** or **inflation-indexed bond**. If I hold:
- Financial wealth: $W$
- NZ Super PV at 65: $PV_{super} \approx B_{super} \times 20$ (rough annuity value)

Then my "total wealth" at 65 is $W + PV_{super}$.

**Implication for asset allocation:**
If I have $50k in financial assets and NZ Super worth ~$800k (present value of future payments), my *implicit* allocation is already ~94% bonds. So I should hold financial assets almost entirely in stocks!

This is similar to Bodie, Merton & Samuelson (1991) argument about human capital as bond-like. NZ Super is even more bond-like (literally guaranteed by government).

**My model should account for this** by defining:
$$ \pi_{stocks}^{total} = \frac{W_{stocks}}{W_{total} + PV_{NZSuper}} $$

Not just $\pi_{stocks}^{financial} = W_{stocks}/W_{financial}$.

**4. Reduces Need for Precautionary Savings**

NZ Super provides strong consumption floor. Combined with public healthcare, this substantially reduces precautionary savings motive.

From [[Precautionary Saving and Social Insurance]]: Social insurance crowds out private precautionary savings. In NZ:
- Universal pension (NZ Super)
- Universal healthcare
- Asset-tested residential care support

This means optimal wealth accumulation in NZ may be **lower** than in countries without these programs.

**For my model:** I should model household as having preference for consumption above NZ Super level, rather than overall consumption:
$$ U(C_t) = u(C_t - \bar{C}_{NZSuper}) $$

Or use floor-ceiling consumption constraint as in [[RIIG - Spending Patterns Through Retirement]] recommendations.

### Changing Residency Requirements

The paper notes residency requirement increasing from 10 to 20 years (phased in).

**Affects:**
- Recent immigrants (longer before eligible)
- New Zealanders who lived overseas (time overseas doesn't count unless in agreement country)

**Modeling consideration:** For my baseline model, assume full eligibility. But sensitivity analysis could explore:
- Partial eligibility (prorated benefits)
- Delayed eligibility (age > 65)
- Uncertainty about future eligibility (policy risk)

### Interaction with Other Income

**Not reduced by:**
- Investment income
- Part-time work earnings
- KiwiSaver withdrawals
- Rental income

**Tax treatment:**
- NZ Super is taxable income
- But no means testing

This makes lifecycle optimization simpler - earning more never reduces NZ Super entitlement.

### Comparison to Other Countries

**Tier 1 Classification:**
OECD classifies NZ Super as "Tier 1" (poverty prevention). But it's more generous than most Tier 1 systems:
- Higher replacement rate than many countries
- Universal (vs means-tested)
- Indexed to wages/inflation

**Similar systems:**
- Netherlands (AOW) - universal pension
- Denmark - universal basic pension plus means-tested supplement
- New Zealand's is simpler (no supplement, no testing)

**Different from:**
- United States (Social Security + means-tested SSI)
- Australia (means-tested Age Pension)
- UK (means-tested Pension Credit)

### Integration with My Research

**Baseline Model Assumptions:**
1. All retirees receive full NZ Super from age 65
2. Couples receive couple rate, singles receive single rate
3. Benefits indexed to inflation (conservative) or wage growth (aggressive)
4. No policy risk (benefits continue at current levels)

**Sensitivity Analyses:**
1. Reduced benefits (policy risk scenario)
2. Delayed eligibility (later age 65)
3. Partial benefits (recent immigrants)
4. Real reduction in benefits over time

**Key Research Questions:**
1. **Optimal KiwiSaver contributions given NZ Super?**
   - High floor reduces need to save
   - But may want consumption above floor
   - Optimal contribution rate?

2. **Optimal asset allocation given NZ Super as bond-like?**
   - Does universal pension justify 100% stocks in financial portfolio?
   - How does this vary with wealth level?

3. **Bequest motives with NZ Super?**
   - NZ Super is annuitized (dies with recipient)
   - Leaves only financial/housing wealth for bequests
   - How does this affect savings behavior?

4. **Early vs late retirement decision?**
   - NZ Super starts at 65 regardless
   - No actuarial adjustment for claiming age (unlike US Social Security)
   - Creates strong incentive to claim at 65
   - But may want to work longer to build wealth for discretionary spending

### Key Numbers to Remember (Need to Update to 2024 Rates)

**Current rates (I'll verify these):**
- Single living alone: ~$472.99/week = ~$24,595/year (before tax)
- Single sharing: ~$435.65/week = ~$22,654/year (before tax)
- Married/couple: ~$726.40/week = ~$37,773/year (before tax, combined)

**After-tax (approximate, depends on other income):**
- Single living alone: ~$22,000/year
- Couple: ~$35,000/year

**Comparison to median spending (from Le & Richardson 2023):**
- Median couple spending: $40,245/year
- NZ Super covers ~87% of median spending
- Need only $5,000/year from savings to reach median

This is **critical finding**: Most couples can maintain median lifestyle with minimal additional savings beyond NZ Super.

### Related Policies Not in This Paper

**I should also model (separate reading):**
1. **KiwiSaver** - Accumulation vehicle, employer/govt match
2. **Residential care subsidies** - Asset-tested, affects late-life portfolio
3. **SuperGold Card** - Discounts for over-65s
4. **Accommodation Supplement** - Means-tested housing support (for renters)

### Critical Takeaways for My Model

1. **NZ Super is generous and universal** - Provides strong consumption floor without means testing
   
2. **Acts as implicit bond holdings** - Should consider total wealth (financial + PV of NZ Super) when determining asset allocation
   
3. **Reduces precautionary savings need** - Combined with public healthcare, creates less downside risk than US/Australia
   
4. **Simplifies optimization** - No cliff effects, discontinuities, or gaming of means tests
   
5. **Most retirees can live on NZ Super alone** - Based on median spending data, many couples need minimal additional income

For my research, I should:
- Include NZ Super as certain income stream from age 65
- Calculate "total wealth" including PV of NZ Super for allocation decisions  
- Compare optimal savings with/without NZ Super to show its value
- Test sensitivity to potential policy changes
- Show how NZ Super makes NZ retirees' optimization different from US

## Related Papers

[[Le and Richardson - Expenditure Patterns of NZ Retiree Households]]
[[RIIG - Spending Patterns Through Retirement]]
[[Precautionary Saving and Social Insurance]]
