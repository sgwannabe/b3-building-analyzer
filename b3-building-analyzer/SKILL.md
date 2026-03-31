---
name: b3-building-analyzer
description: Analyze NYC residential condo buildings using the B³ (Building Block Benchmark) scoring system. Use this skill whenever the user provides transaction data for a NYC building and wants an investment analysis, building report, B³ score, or any evaluation of a condo asset's investment quality. Trigger on phrases like "analyze this building", "B³ score", "building analysis", "run the numbers on this building", "investment thesis", or when the user uploads transaction data (sales, rentals, DOM) for a specific NYC address. Also trigger when the user mentions line-by-line performance, rent capture, liquidity scoring, PPSF trends, or stack analysis for a condo building. This skill handles ALL input formats — CSV, Excel, pasted text, JSON, or mixed — and produces blog posts, PDFs, and/or PPTX decks.
---

# B³ Building Analyzer

You are producing an institutional-grade investment analysis for a specific NYC condo building. The analysis must go beyond data description — it must **synthesize a thesis**: why this building is or isn't a good investment, and for whom.

## Why This Skill Exists

The core problem: generic AI analysis of transaction data produces flat summaries — "prices went up", "rents are high", "units sell fast." That's useless. An investor needs to understand the **interplay** between metrics. A building where rents grew 40% in 3 years AND prices appreciated AND units sell in 45 days tells a completely different story than a building where only one of those is true. This skill forces you to find and articulate that story.

## Step 0: Read the B³ Methodology

Before doing anything, read `references/b3-methodology.md` in this skill's directory. It contains the exact scoring formulas, classification logic, and the analytical framework you must follow. Do not improvise the scoring.

## Step 1: Parse & Normalize the Input Data

The user may provide data in any format. Your job is to normalize it into a structured dataset. Read `references/input-parsing.md` for format-specific guidance.

Regardless of input format, you need to extract these fields per transaction:

| Field | Required | Notes |
|-------|----------|-------|
| unit | Yes | e.g., "6E", "10B" |
| transaction_type | Yes | "sale" or "rental" |
| date | Yes | Close date or lease start |
| price | Yes | Sale price or monthly rent |
| sqft | If available | For PPSF calculation |
| bedrooms | Yes | 0=studio, 1, 2, 3+ |
| DOM | If available | Days on market |
| is_sponsor | If determinable | First sale = sponsor |

Write a Python script to parse the data into a clean JSON structure. Save to a `building_data.json` file in your working directory. You can use `scripts/parse_transactions.py` from this skill's directory as a starting point.

## Step 2: Derive Line-Level Metrics

This is the analytical core. Group transactions by **line (stack)** — the letter suffix of the unit number (e.g., all "E" units form Line E).

For each line, calculate:

### Sales Metrics
- **Resale PPSF trajectory**: Plot PPSF over time for resales only (exclude sponsor sales)
- **CAGR**: For units with buy→sell pairs, compute annualized return
- **DOM distribution**: Median, min, max days on market
- **Ask-to-close spread**: If list price is available, compute discount %

### Rental Metrics
- **Rent PPSF**: Monthly rent ÷ sqft (if sqft unavailable, use building average for that bedroom count)
- **Rent growth**: Same-unit rent changes over time
- **Rental absorption speed**: DOM for rental listings

### Cross-Metric Synthesis (THIS IS THE KEY PART)

This is the section that makes this skill different from generic AI analysis. Generic AI will produce: "Rents are high. Prices went up. DOM is low." — three separate observations. That is useless.

What you MUST produce instead is a **causal chain**: "BECAUSE rents grew X% AND prices appreciated AND units sell in Y days — all three happening at the same time — THEREFORE this building is [classification] and we recommend [action] for [investor type]."

The key word is **simultaneously**. A building where rents grew 40% but takes 200 days to sell is a completely different investment than one where rents grew 40% AND sells in 47 days. The interplay between metrics is the thesis — not the metrics themselves.

After computing individual metrics, build the causal argument:

1. **The Income Story** (Rent Capture): Are rents growing? By how much, over what period? What does this mean for the owner's cash flow?
2. **The Equity Story** (Appreciation): Is the asset growing in value? Which lines? Over what timeframe?
3. **The Exit Story** (Liquidity): Can the owner leave when they want to? How quickly? At what discount from ask?
4. **The Convergence** (THIS IS THE THESIS): Are all three happening at the same time? If yes — the owner earns growing income WHILE their asset appreciates AND they can exit anytime. State this explicitly. Do NOT just list the three metrics with "+" signs between them. Write it as a connected argument: "Because A is true, and at the same time B is true, and on top of that C is true, the result is D — and therefore we recommend E."

If the metrics diverge (e.g., high rent but low liquidity), that divergence IS the thesis — explain what kind of investor it suits and why.

## Step 3: Score Using B³ System

Apply the B³ scoring exactly as defined in `references/b3-methodology.md`. The three pillars:

- **Liquidity (L)**: Weight 0.35
- **Rent Capture (R)**: Weight 0.30
- **Appreciation (A)**: Weight 0.35

Composite = (L × 0.35) + (R × 0.30) + (A × 0.35)

Classify the building based on the composite and pillar scores per the methodology.

## Step 4: Build the Investment Thesis

This is where most AI analyses fail. You are NOT writing a data summary. You are writing an **investment thesis** — a narrative argument for a specific type of investor.

### Thesis Construction Framework

Answer these questions in order. Each answer feeds into the next:

1. **What type of asset is this?** (Core/Defensive, Value-Add, Opportunistic, Speculative)
2. **Who is the ideal owner?** (Risk-averse wealth preserver? Active value-add investor? Speculative flipper?)
3. **What is the primary return driver?** (Yield? Appreciation? Liquidity premium? Combination?)
4. **What is the risk profile?** (What could go wrong? Which lines are vulnerable? Floor sensitivity?)
5. **What is the thesis in one sentence?** This becomes the opening and closing of the report.

### Thesis Sentence Pattern
The thesis must synthesize ALL three B³ pillars into a single narrative. Examples:

- "45 Christopher is a Core/Defensive asset that excels at wealth preservation — elite rent capture ($100-$123/SF) combined with rapid liquidity (47-day DOM) makes it ideal for risk-averse investors who prioritize yield and exit optionality over explosive appreciation."
- "100 Example St is a Value-Add play — strong appreciation in premium lines (E, F) but lagging rent capture suggests renovation-driven repositioning could unlock significant yield upside."

The thesis sentence must reference specific numbers from the data, not vague descriptors.

## Step 5: Structure the Transaction Examples

Divide notable transactions into two categories:

### Winners (Appreciation / Strong Returns)
For each, identify the **driver** using this taxonomy:
- **Market regime timing**: Bought/sold at favorable cycle points
- **Line-level premium persistence**: The specific line consistently outperforms
- **Unit size/mix**: Entry-level units in high demand
- **Renovation premium capture**: Value-add at unit level

### Laggards (Flat / Depreciation / Slow Sales)
For each, identify the **driver**:
- **Market regime timing**: Poor entry/exit timing
- **Liquidity shift**: DOM expanded, forced price cuts
- **Line-level drag**: Specific lines underperform
- **Floor penalty**: Lower floors punished disproportionately

## Step 6: Identify Risks & Red Flags

Always check for:
- Floor-level sensitivity (lower floors with high DOM or large discounts)
- Renovation premium distortion (wide PPSF spread suggesting condition variance)
- Line-specific underperformance that drags building averages
- Sponsor inventory overhang (if applicable)
- HOA/tax burden (flag if data is unavailable — this is a limitation)

## Step 7: Generate Output

The user may want one or more output formats. Read the relevant files:

- **Blog post (Markdown/HTML)**: Follow the 10-section template in `references/output-templates.md`
- **PDF report**: Use `matplotlib` for charts and a PDF library (e.g., `reportlab`, `weasyprint`, or `fpdf2`) to assemble the report. See `references/output-templates.md` for the PDF-specific section.
- **PPTX deck**: Use `python-pptx` to generate slides. See `references/output-templates.md` for the deck structure.
- **Instagram carousel**: Generate 6 square slides (1080×1080) using `scripts/generate_instagram.py` as a template. See `references/output-templates.md` for the slide structure.
- **All of the above**: Generate each sequentially

### Output Structure (All Formats)

Every output must follow this exact section order:

1. **Building Overview** — Classification, type, scale, justification
2. **Unit Mix & Composition** — Transaction-weighted breakdown
3. **Line (Stack) Performance** — Resale-only metrics by line
4. **Building-Wide PPSF Trend** — Normalized timeline with regime analysis
5. **Rent Capture Analysis** — Rent PPSF, absorption, growth rates
6. **B³ Scoring** — Individual pillar scores with justification
7. **Composite Score & Classification** — Final score and category
8. **Transaction Examples** — Winners and Laggards with drivers
9. **Risks & Red Flags** — Honest assessment of vulnerabilities
10. **Executive Summary** — Thesis sentence + key metrics + recommendation

The Executive Summary should echo the thesis from Step 4, not introduce new information.

## Critical Reminders

- **Never describe data without interpreting it.** "PPSF rose from $1,700 to $2,600" is description. "The building captured the 2013-15 boom fully, with PPSF rising 53% — and critically, it held those gains through the subsequent plateau" is analysis.
- **NEVER list metrics with "+" signs. ALWAYS write causal chains.** Wrong: "Elite rent capture ($100/SF) + rapid liquidity (47-day DOM) + steady appreciation = fortress." Right: "Rents grew 40% in 3 years — that's growing income. At the same time, prices have been appreciating for a decade — that's growing equity. On top of that, units sell in 47 days — that's exit optionality. When all three happen simultaneously, the owner earns more each year, gets richer each year, and can leave anytime. This is why we recommend ownership." The difference: the first is a formula, the second is an argument. Always write the argument.
- **Name the investor.** Every building has an ideal owner profile. State it explicitly.
- **Make a recommendation.** Don't just classify — tell the reader whether to buy, hold, or avoid, and for which investor type. The thesis must end with an action, not just a label.
- **Be honest about weaknesses.** A credible analysis acknowledges laggards and risks. Cherry-picking winners destroys trust.
- **Use specific numbers.** Never say "strong appreciation" — say "5% CAGR on the E-line, outperforming NYXRCSA by 2.1pp."
