## Reference

RIIG (Retirement Income Interest Group). (2024). *Spending patterns through retirement: implications for retirement planning and drawdown*. New Zealand Society of Actuaries.

---

## Central Finding

**Real spending declines ~2%/year after age 65** — i.e., nominal spending is roughly *flat*.

NZ HES data (Chart 2):
- 65–69: highest median spending
- 70–74: ~10% lower
- 75–79: ~15% lower
- 80–84: ~25% lower
- 85+: ~35% lower

Same pattern in US, UK, Australia — not NZ-specific.

---

## Why Spending Falls

1. Mobility declines → travel, recreation drop
2. Home production substitutes for market spending (cook vs eat out)
3. Work-related expenses gone
4. SuperGold Card discounts
5. Geographic shift (metro → provincial)

**Part of the decline is involuntary** (health/mobility constraints, not preference). This matters — can't assume retirees are fully optimising their consumption path.

---

## Implications for Savings Requirements

Traditional planning assumes constant real spending (nominal grows at CPI ~2%/year):
$$ C_t = C_0 \times (1.02)^t $$

RIIG says reality is flat nominal spending:
$$ C_t \approx C_0 $$

Consequence: **savings need at 65 is ~40% lower** under RIIG assumption vs traditional.

Or equivalently: if you use the traditional assumption, you're planning for ~$18k/year in extra spending at age 85 that never actually occurs.

---

## RIIG Rules of Thumb

Four rules for annual drawdown $D_t$ from a fund $W_t$. NZ Super $S_t$ (inflation-linked) provides the floor on top of which these apply.

**6% Rule**
$$ D_t = 0.06 \times W_0 $$
Fixed nominal amount from starting balance. Front-loads spending — suits the empirical 2% real decline pattern well. Risk: fund may run out before death. Best fit for typical declining-spending retiree.

**Inflated 4% Rule**
$$ D_t = 0.04 \times W_0 \times (1+\pi)^t $$
Fixed real amount (nominal grows with inflation $\pi$). Assumes constant real spending — inconsistent with empirical evidence. Fund lasts longer; leaves estate. More conservative.

**Fixed Date Rule**
$$ D_t = \frac{W_t}{T - t} $$
Divide current balance by years remaining to a fixed end date $T$. Assumes NZ Super-only from $T$ onwards. Income varies year-to-year. Maximises spending over a chosen horizon.

**Life Expectancy Rule**
$$ D_t = \frac{W_t}{\mathbb{E}[\text{remaining life} \mid \text{age}_t]} $$
Divide current balance by actuarial life expectancy at current age. Efficient — exhausts fund in expectation over full lifetime. Income falls with age as life expectancy shrinks (roughly), but fund also shrinks so the ratio is fairly stable.


**Savings benchmarks (from paper):**

| Real spending path | Savings needed at 65 (to top up NZ Super to $56k/yr until 90) |
|---|---|
| Constant real (grows 2%/yr nominal) | **$605,000** |
| Flat nominal (0% nominal growth = 2% real decline) | **$375,000** |
| Grows 1%/yr nominal (1% real decline) | **$480,000** |
| Falls 0.5%/yr nominal (2.5% real decline) | **$328,000** |

Assumptions: NZ Super = $27k/yr, investment return = 3.5% after tax/fees, retirement to age 90.

---

## NZ-Specific Context

- NZ Super: ~$27k single / ~$42k couple — strong guaranteed floor
- Public healthcare covers most medical costs (unlike US)
- Residential care subsidy: asset-tested at ~$250k
- These reduce precautionary saving need relative to US models

---

## For My Model

**Consumption function:**
$$ C_t = C_{65} \times (0.98)^{t-65} $$

Or step version (matches HES data better):
- 65–74: $C_{65}$
- 75–84: $0.88 \times C_{65}$
- 85+: $0.65 \times C_{65}$

NZ Super covers a larger fraction of spending over time as spending declines → drawdown need shrinks. For modest retirees (No Frills Provincial), NZ Super may fully cover within ~10 years.

**Key tension for my optimisation:**
- If consumption is front-loaded, effective horizon is shorter
- Does this justify *lower* equity allocation (less time for volatility to average out)?
- Or higher equity (can tolerate near-term volatility if later spending covered by NZ Super)?

---

## Questions

1. Cohort vs age effect? HES cross-sectional data can't definitively separate them.
2. Is the decline partly involuntary (health constraints on utility function vs spending)?
3. Do households optimally front-load knowing spending declines, or do they under-spend early?
4. Does the 2% figure hold across wealth levels? (Rich retirees may have steeper or shallower decline)

---

## Related

[[Matthews - NZ Retirement Expenditure Guidelines 2025]] — NZ spending benchmarks
[[Le and Richardson - Expenditure Patterns of NZ Retiree Households]] — NZ HES data confirming 44% drop 65-74 → 85+
