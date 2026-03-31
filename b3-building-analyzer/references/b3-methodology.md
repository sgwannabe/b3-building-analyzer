# B³ Scoring Methodology

## Overview

B³ (Building Block Benchmark) evaluates NYC condo buildings on three pillars: **Liquidity**, **Rent Capture**, and **Appreciation**. Each pillar is scored 0–100 independently, then combined into a weighted composite that determines the building's investment classification.

The philosophy: a building's investment quality is not a single number — it's a profile. A building with 95 Liquidity / 90 Rent Capture / 40 Appreciation tells a very different story than 60/60/80. The composite gives a headline, but the pillar breakdown tells you WHO should own it and WHY.

---

## Pillar 1: Liquidity Score (Weight: 0.35)

Liquidity measures how quickly and reliably units sell in the resale market.

### Inputs
- **Median DOM (Days on Market)**: Primary metric. Resales only (exclude sponsor).
- **DOM Consistency**: Standard deviation of DOM across transactions.
- **Transaction Volume**: Number of resales per year relative to building size.
- **Ask-to-Close Spread**: Average discount from list price (if available).

### Scoring Bands

| Median DOM | Base Score |
|-----------|-----------|
| ≤ 30 days | 90–100 |
| 31–60 days | 75–89 |
| 61–90 days | 60–74 |
| 91–120 days | 45–59 |
| 121–180 days | 30–44 |
| > 180 days | 0–29 |

### Adjustments
- **Consistency bonus (+5)**: If DOM std dev < 30 days (reliable liquidity)
- **Volume bonus (+5)**: If ≥ 5 resales/year per 100 units
- **Spread penalty (-5)**: If average ask-to-close spread > 5%
- **Outlier penalty (-5)**: If any single unit took > 200 days AND building has < 20 total resales (small sample distortion)

### Interpretation
- **85+**: Elite liquidity. Investors can exit with high confidence within 60 days.
- **70–84**: Strong. Normal market conditions support efficient exits.
- **55–69**: Moderate. Some units may linger; pricing discipline required.
- **Below 55**: Illiquid. Exit risk is a material concern.

---

## Pillar 2: Rent Capture Score (Weight: 0.30)

Rent Capture measures how effectively the building converts ownership into rental income.

### Inputs
- **Rent PPSF**: Monthly rent per square foot across all rental transactions.
- **Rent Absorption Speed**: DOM for rental listings.
- **Rent Growth Rate**: Year-over-year or same-unit rent increases.
- **Rent Consistency**: Spread between highest and lowest rent PPSF for same bedroom count.

### Scoring Bands (Rent PPSF — Manhattan Condo Baseline)

| Rent PPSF | Base Score |
|----------|-----------|
| ≥ $100/SF | 90–100 |
| $80–$99/SF | 75–89 |
| $60–$79/SF | 60–74 |
| $45–$59/SF | 45–59 |
| < $45/SF | 0–44 |

### Adjustments
- **Growth bonus (+5)**: If rent growth > 20% over trailing 3 years
- **Absorption bonus (+5)**: If median rental DOM < 30 days
- **Consistency bonus (+3)**: If rent PPSF spread for same bedroom count < 15%
- **Data penalty (-10)**: If fewer than 5 rental transactions available (insufficient confidence)

### Interpretation
- **85+**: Elite rent capture. Building commands premium rents with fast absorption. Investors can rely on consistent income streams.
- **70–84**: Strong rental performance. Above-market rents with reasonable absorption.
- **55–69**: Adequate. Rents are market-rate; income is reliable but not exceptional.
- **Below 55**: Weak rental profile. Below-market rents or slow absorption.

---

## Pillar 3: Appreciation Score (Weight: 0.35)

Appreciation measures long-term price growth and resilience through market cycles.

### Inputs
- **Building-wide PPSF CAGR**: Annualized growth across all resales.
- **Line-level CAGR variance**: How much do individual lines deviate from building average?
- **Cycle resilience**: Did PPSF hold during the 2020 correction? Recovery speed?
- **New highs**: Has the building set new PPSF records in the most recent 2 years?
- **Benchmark comparison**: Building CAGR vs. NYXRCSA index (or relevant sub-market index).

### Scoring Bands (Annualized CAGR)

| CAGR | Base Score |
|------|-----------|
| ≥ 6% | 90–100 |
| 4–5.9% | 75–89 |
| 2–3.9% | 60–74 |
| 0–1.9% | 40–59 |
| Negative | 0–39 |

### Adjustments
- **Resilience bonus (+5)**: If building PPSF did not decline > 10% during 2020 correction
- **New high bonus (+5)**: If new PPSF records set in most recent 2 years
- **Benchmark bonus (+5)**: If building CAGR exceeds sub-market index by > 2pp
- **Line variance penalty (-5)**: If any major line (≥ 5 transactions) has negative CAGR
- **Data penalty (-10)**: If fewer than 10 resale transactions available

### Interpretation
- **85+**: Strong compounder. Consistent appreciation with cycle resilience.
- **70–84**: Solid growth. Outperforms or matches market benchmarks.
- **55–69**: Moderate. Keeps pace with inflation but doesn't generate real returns in all lines.
- **Below 55**: Weak appreciation. Some lines may have lost value.

---

## Composite Score Calculation

```
Composite = (Liquidity × 0.35) + (Rent Capture × 0.30) + (Appreciation × 0.35)
```

## Building Classification

Classification depends on BOTH the composite score AND the pillar profile:

### Core / Defensive (Composite ≥ 75, all pillars ≥ 55)
- **Profile**: High liquidity, strong rent capture, steady appreciation
- **Ideal owner**: Risk-averse investor prioritizing wealth preservation and income
- **Narrative**: "Fortress asset — reliable yield, easy exit, steady growth"

### Core Plus (Composite ≥ 70, at least two pillars ≥ 75)
- **Profile**: Strong in two areas with one moderate area
- **Ideal owner**: Balanced investor willing to accept one area of moderate performance
- **Narrative**: "Strong asset with one area of upside potential"

### Value-Add (Composite 55–74, at least one pillar ≥ 75, at least one pillar < 60)
- **Profile**: Uneven — strong in one area, weak in another
- **Ideal owner**: Active investor who can address the weak pillar
- **Narrative**: "Opportunity to reposition — strength in X offsets weakness in Y"

### Opportunistic (Composite 40–54)
- **Profile**: Below-average across multiple pillars
- **Ideal owner**: Speculative investor betting on specific catalysts
- **Narrative**: "Higher risk, potentially higher reward if catalyst materializes"

### Distressed (Composite < 40)
- **Profile**: Weak across all pillars
- **Ideal owner**: Deep value / turnaround specialist
- **Narrative**: "Broken asset requiring significant intervention"

---

## Connecting the Score to the Thesis

The classification alone is not the thesis. The thesis emerges from HOW the pillars interact:

### Pattern: High Liquidity + High Rent + Moderate Appreciation
→ "Income fortress" — investors buy for yield and exit optionality, not capital gains. Ideal for retirees, trust funds, passive investors.

### Pattern: Moderate Liquidity + Low Rent + High Appreciation
→ "Appreciation play" — values are rising but rental yield is thin. Ideal for buy-and-hold investors focused on net worth growth.

### Pattern: High Liquidity + Low Rent + Low Appreciation
→ "Trading asset" — easy to buy and sell, but holding generates neither income nor growth. Ideal for short-term flippers.

### Pattern: Low Liquidity + High Rent + High Appreciation
→ "Patient capital" — excellent returns if you can get in and wait, but exit timing is uncertain. Ideal for long-horizon investors who don't need flexibility.

Always map the specific pillar combination to an investor profile and explain WHY that profile fits.
