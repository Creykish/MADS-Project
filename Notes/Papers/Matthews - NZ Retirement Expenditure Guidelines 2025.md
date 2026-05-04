## Reference

Matthews, C. (2025). *New Zealand Retirement Expenditure Guidelines 2025*. NZ Fin-Ed Centre / Massey University. (Annual update, 14th edition since 2012.)

---

## Methodology

**Data source:** Stats NZ 2022/23 Household Economic Survey (HES), triennial. Inflation-adjusted to 30 June 2025.

**Who's in:** "Retired" = households where at least one income source is NZ Super, war pension, or other govt pension. **Not** necessarily fully retired — many still have investment income or employment income. HES doesn't separate these.

**Two budget tiers:**
- **No Frills** = 2nd quintile (21st–40th percentile by household income) — basic, few luxuries
- **Choices** = 4th quintile (61st–80th percentile) — comfortable, some treats

Deliberate choice to skip 1st and 5th quintiles to avoid outlier distortion. Means ~20% of retired households spend *less* than No Frills.

**Critical caveat:** HES is **cross-sectional**, not longitudinal. Age-group differences in spending could be:
1. Age effects (actual spending declines with age as you get older)
2. Cohort effects (older cohorts had lower lifetime income, different preferences)
3. Selection effects (healthier/wealthier people survive to 85+)

RIIG and Le & Richardson assume age effects dominate - reasonable but not proven.

---

**NZ Super (after tax):**
- Single: $519.47/week = **$27,013/year**
- Couple: $799.18/week = **$41,557/year**

**Weekly spending (annual in brackets):**

| Household | No Frills Metro | No Frills Provincial | Choices Metro | Choices Provincial |
|---|---|---|---|---|
| Single | $705 ($36,680) | $581 ($30,210) | $791 ($41,130) | $772 ($40,140) |
| Couple | $937 ($48,740) | $1,061 ($55,170) | $1,780 ($92,570) | $1,243 ($64,660) |

**Gap above NZ Super (= savings drawdown needed):**

| Household | No Frills Metro | No Frills Provincial | Choices Metro | Choices Provincial |
|---|---|---|---|---|
| Single | **$9,670/yr** | **$3,200/yr** | **$14,120/yr** | **$13,130/yr** |
| Couple | **$7,180/yr** | **$13,610/yr** | **$51,010/yr** | **$23,100/yr** |

Single No Frills Provincial: NZ Super covers **89%** of spending. Tiny drawdown needed (~$3k/yr).

Choices Metro couple is the outlier — $92k/year spending requires $51k drawdown. Likely because the 4th quintile includes part-time earners/investment income people, not pure retirees.

---

## Expenditure Composition

Biggest spending categories (% of total):
- **Housing & household utilities:** 16–35% (largest for 6 of 8 groups)
- **Food:** 14–22%
- **Transport:** 12–24% (third for 5 groups)
- **Recreation & culture:** 5–24%

For **No Frills Metro single** specifically:
- Food: 18.9%, Grocery food: 10.7%
- Insurance: 13.2%
- Property rates: 6.1%
- Household energy: 7.4%

All household groups over-index CPI on: grocery food, insurance, property rates, household energy.

---

## Inflation (2024→2025)

CPI for period: 2.70%. Retiree inflation range: 2.54%–3.16%.

Why retirees diverge from CPI:
- Over-index on property rates (+11.9% sub-index) and household energy
- Under-index on telecoms (–25.2% sub-index — pensioners don't buy new phones much)
- Food CPI ran above headline, and food is large share of retiree budget

**For my model:** don't use headline CPI for retirement spending. Retiree-specific inflation runs ~0–0.5% above CPI historically. Call it 0.3% excess.

---

## Housing in Retirement

**Renting costs:**
- Share of multi-bedroom property: ~$250/week = $13,000/year
- One/two-bedroom alone: $400–500/week = $20,800–26,000/year
- Lump sum to fund rental (at 4.8% drawdown rate implied): ~$271,000 for shared, ~$430,000–$540,000 alone

These guidelines are calibrated on the **current cohort of retirees** who have ~66% home ownership. Future generations expected to have lower home ownership → the guidelines will need upward revision or a separate "renter" track.

**Retirement village:**
- Not obviously cheaper — initial capital + weekly fees
- Lifestyle advantages but complex ORA (Occupation Right Agreement) legal structure
- Should model separately from owner-occupier

---

## The Fixed-Spending Assumption Problem

RIIG and Le & Richardson show that real spending declines with age. But the Massey guidelines are published as fixed nominal amounts for each age group, implicitly treating them as constant real targets.

These guidelines are published as annual figures — implicitly treating them as a constant real target throughout retirement. That's what they're used for in industry ("you need $X/year in retirement").

But cross-referencing with RIIG and Le & Richardson:

| Age group | Spending index (65-74 = 100) |
|---|---|
| 65–74 | 100 |
| 75–79 | ~88 |
| 80–84 | ~75 |
| 85+ | ~56–64 |

RIIG: **~2% real decline per year** after 65.
Le & Richardson: **44% lower** at 85+ vs 65-74.

So the Massey guidelines figures represent **early-retirement spending** (roughly the 65-69 age band dominates the HES retired sample). Using them as a fixed real target massively overstates needs for late retirement.

**Quantifying the error:**
- Assume 25-year retirement (65–90), 2% real annual decline
- Present value of actual consumption path relative to constant real path ≈ 0.82 (assuming ~5% real discount rate)
- Industry benchmark overstates savings need by ~18–22%

More directly: if nominal spending is roughly flat (inflation ≈ 2%, real decline ≈ 2%), then:
- The No Frills Metro single figure of ~$36,700 at age 65 is also the figure at age 80, 85, 90 in *nominal* terms
- But that's the *actual* spending — which is declining in real terms
- Standard planning assumes $36,700 × (1.02)^20 = $54,500 at age 85 in nominal terms — wrong by ~$18k/year

This means the conventional approach is planning for spending that never actually occurs.

---

## What These Numbers Mean for Model Calibration

**Use as age-65 anchor, not constant target.**

At age 65:
- Minimum floor: NZ Super = $27k single / $42k couple (certain)
- No Frills: $37k single / $49k couple (metro)
- Choices: $41k single / $65–93k couple

Then apply RIIG's 2% real annual decline:
$$ C_t = C_{65} \times (0.98)^{t-65} $$

Or step-function version (from RIIG / Le & Richardson data):
- 65–74: $C_{65}$
- 75–84: $0.88 \times C_{65}$
- 85+: $0.65 \times C_{65}$

**What the drawdown needs actually are over a retirement:**

For No Frills Metro single, with 2% real decline and NZ Super floor:
- Age 65: ~$9,670/yr drawdown
- Age 75: ~$7,900/yr drawdown (or less if NZ Super keeps up)
- Age 85: ~$6,500/yr drawdown (or 0 if spending drops below NZ Super)

Actually once spending drops enough, NZ Super may fully cover — **effectively zero drawdown needed for No Frills Provincial retiree within ~10 years of retirement.**

**Critical implication for model:** NZ Super is not just a floor, for modest retirees it becomes the *ceiling* within a decade or so. Financial assets are really only needed for:
1. Early retirement discretionary spending (travel, activities)
2. Housing costs if renting
3. Aged care costs ($60–80k/year, means-tested at ~$240k)
4. Bequest motive

---

## Means Testing / Residential Care

Paper notes aged care subsidies are asset-tested. Threshold ~$240,000 in financial assets (home usually exempt). Worth modelling the kink — households near this threshold face implicit ~100% marginal tax on savings above it.

---

## For My Model

**Consumption parameters:**
- Use Choices Metro couple ($1,780/wk = $92,570/yr) as upper bound for affluent retirees
- Use No Frills Provincial single ($581/wk = $30,210/yr) as near-minimum (close to NZ Super)
- NZ Super = guaranteed floor income — model as deterministic annuity from age 65

**Inflation:**
- Use CPI + 0.3% for retiree-specific basket

**Spending decline:**
- 2% real/year (RIIG), confirmed by Le & Richardson 44% drop 65-74 → 85+
- Build into utility function or consumption constraint directly

**Renter vs owner:**
- Separate model tracks needed — $13k–$26k/year in housing costs for renters vs near-zero for outright owners
- This gap is not temporary — it persists lifetime

**Key unanswered question:**
Are the Choices figures "real" — i.e., retired households genuinely spending $92k/year from savings — or are many in the 4th quintile still earning? Paper acknowledges this but doesn't separate it. Could be that Choices is biased upward and not representative of pure retirees.

---

## Related

[[RIIG - Spending Patterns Through Retirement]] — 2% real decline, drawdown implications
[[Le and Richardson - Expenditure Patterns of NZ Retiree Households]] — age-specific NZ spending data
[[Te Ara Ahunga Ora - Introduction to NZ Superannuation]] — NZ Super rates and adequacy
