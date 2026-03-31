# Output Templates

## Blog Post (Markdown / HTML)

### Structure
The blog post follows a 10-section format. Each section must include both data AND interpretation.

```markdown
# [Building Address]

[THESIS SENTENCE — one paragraph that synthesizes all three B³ pillars into a single investment argument. This is NOT a data summary. It is a recommendation with specific numbers.]

**Author:** [Name]
**Date:** [Date]

---

### 1. BUILDING OVERVIEW (ANALYST FRAMING)
- Type, scale, year built, total units, floors
- **Classification:** [Core/Defensive | Value-Add | etc.]
- **Justification:** 2-3 sentences explaining WHY this classification, referencing specific metrics

### 2. UNIT MIX & COMPOSITION
- Transaction-weighted breakdown (not just total units)
- Analysis of what the mix implies for liquidity and pricing dynamics
- Note imbalances that affect investment thesis

### 3. LINE (STACK) PERFORMANCE — RESALE ONLY
Three sub-sections:
A. **Liquidity** — Fastest and slowest units with DOM, patterns
B. **Price Strength** — PPSF ranges, premium lines, ceiling
C. **Appreciation** — Compounders vs. laggards with CAGR

### 4. BUILDING-WIDE PPSF TREND (NORMALIZED)
- Break into market regimes (boom, plateau, correction, recovery)
- Name each period and describe behavior
- Conclude with whether building is compounding, flat, or declining

### 5. RENT CAPTURE ANALYSIS
A. **Rent Capture by Line** — Specific examples with rent PPSF
B. **Rent Appreciation** — Same-unit rent growth over time
- Conclusion connecting rent growth to broader thesis

### 6. B³ SCORING SYSTEM (0–100)
Three sub-sections with score and justification:
A. **Liquidity Score: [X]/100** — Speed + consistency
B. **Rent Capture Score: [X]/100** — Efficiency + absorption
C. **Appreciation Score: [X]/100** — Magnitude + durability

### 7. COMPOSITE SCORE & CLASSIFICATION
- Show the formula with actual numbers
- State the category and explain what it means for investors

### 8. TRANSACTION EXAMPLES
Two categories:
- **Winners** — 3-4 examples with % change, CAGR, and identified driver
- **Laggards** — 3-4 examples with context and identified driver

### 9. RISKS & RED FLAGS
- Bullet each risk with specific evidence
- Do NOT soften risks — credibility requires honesty

### 10. EXECUTIVE SUMMARY
- Restate thesis sentence
- Key metrics in brief
- Investor recommendation

### B³ SCORECARD (Table)
| Metric | Score |
|--------|-------|
| Liquidity | [X] |
| Rent Capture | [X] |
| Appreciation | [X] |
| COMPOSITE | [X] |
| Category | [Classification] |
```

### Writing Style for Blog
- Professional but accessible — imagine writing for a sophisticated investor, not an academic journal
- Use specific numbers always (never "strong" without a number)
- Bold key terms on first use
- Use horizontal rules between sections
- Keep paragraphs short (3-4 sentences max)

---

## PDF Report

When generating PDF output, use `reportlab`, `weasyprint`, or `fpdf2` in Python.

### PDF-Specific Additions
- Include a cover page with building photo (if available), address, date, and B³ composite score
- Add page numbers and headers
- Include charts/graphs for PPSF trend (Section 4) and B³ radar chart (Section 6)
- Use a summary table on the cover page

### Charts to Generate
1. **PPSF Timeline**: X-axis = date, Y-axis = PPSF, color-coded by line. Mark market regime boundaries.
2. **B³ Radar Chart**: Three axes (Liquidity, Rent Capture, Appreciation) showing the building's profile.
3. **Unit Mix Pie Chart**: Transaction-weighted bedroom distribution.
4. **Rent Growth Chart**: Same-unit rent over time for key examples.

Use matplotlib or plotly to generate charts, save as images, embed in PDF.

---

## PPTX Deck

When generating PPTX output, use `python-pptx` in Python.

### Slide Structure (12-15 slides)

| Slide | Content |
|-------|---------|
| 1 | Title: [Address] — B³ Analysis |
| 2 | Executive Summary (thesis + scorecard) |
| 3 | Building Overview + Classification |
| 4 | Unit Mix & Composition (pie chart) |
| 5 | Line Performance — Liquidity |
| 6 | Line Performance — Price Strength |
| 7 | PPSF Trend Chart (full timeline) |
| 8 | Rent Capture Analysis |
| 9 | Rent Growth Chart |
| 10 | B³ Scores (radar chart + breakdown) |
| 11 | Transaction Examples — Winners |
| 12 | Transaction Examples — Laggards |
| 13 | Risks & Red Flags |
| 14 | Investment Recommendation |
| 15 | Appendix: Data Sources |

### Deck Design Principles
- Maximum 5 bullet points per slide
- Every slide with data must have a "So What?" takeaway line
- Use the building's B³ classification color: Core=Blue, Value-Add=Green, Opportunistic=Orange, Distressed=Red
- Charts should be large (60%+ of slide area)
- Speaker notes should contain the full analytical narrative for each slide
