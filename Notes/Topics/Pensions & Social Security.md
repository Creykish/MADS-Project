Public pension systems that provide income guarantees in retirement. These fundamentally alter the retirement savings and spending problem by reducing downside risk and providing a consumption floor.

## NZ Super

New Zealand's universal public pension — paid to all residents aged 65+ regardless of income or assets.

**Key features:**
- Not means-tested (unlike Australian Age Pension, US SSI)
- Inflation-linked (adjusted annually)
- 2025 rates (after tax): Single $27,013/year, Couple $41,557/year
- Residency requirement: 10 years since age 20 (changing to 20 years for post-1977 births)

**Coverage:**
- ~40% of NZ 65+ rely entirely on NZ Super
- ~20% have minimal additional savings
- As KiwiSaver matures, future retirees will have more private savings alongside NZ Super

**Impact on spending:**
- For No Frills provincial single: NZ Super covers 89% of spending → only ~$3,200/year drawdown needed
- For No Frills metro single: ~$9,700/year drawdown needed
- As spending declines ~2%/year in real terms after 65, NZ Super progressively covers a larger share

**Impact on asset allocation:**
NZ Super acts like an inflation-linked annuity — a riskless asset in the retiree's implicit portfolio. De Nardi et al. show social security "has a big impact on elderly savings." Combined with modest financial wealth, the implicit portfolio of many NZ retirees is already heavily weighted to safe assets via NZ Super's present value.

## Comparative Systems

| Country | System | Means-tested? | Typical rate |
|---|---|---|---|
| New Zealand | NZ Super | No | ~$27k single |
| Australia | Age Pension | Yes (assets + income) | ~AUD$28k single |
| United States | Social Security | Earnings-based | Variable |
| United Kingdom | State Pension | No | ~£11.5k |

NZ's universal system creates cleaner optimisation problems (no means-test kink) but also means public spending pressure grows with population ageing — fiscal sustainability concern for 2040s+.

## Modelling

Model as deterministic inflation-linked annuity from age 65:
$$I_{super}(t) = B_{super} \cdot (1+\pi)^{t-65}, \quad t \geq 65$$
Where $B_{super}$ is couple or single rate and $\pi$ is CPI.

**Related:**
[[Consumption Floor]]
[[Matthews - NZ Retirement Expenditure Guidelines 2025]]
[[RIIG - Spending Patterns Through Retirement]]
[[Precautionary Saving]]
[[De Nardi French Jones - Differential Mortality and Medical Expenses]]
