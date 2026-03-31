# Input Parsing Guide

The user may provide building transaction data in any of the following formats. Your job is to normalize everything into a single JSON structure before analysis.

## Target Schema

Every transaction must be normalized to this shape:

```json
{
  "building": {
    "address": "45 Christopher Street",
    "neighborhood": "West Village",
    "type": "Pre-war Condo",
    "year_built": 1931,
    "total_units": 112,
    "floors": 17
  },
  "transactions": [
    {
      "unit": "6E",
      "line": "E",
      "floor": 6,
      "type": "sale",
      "date": "2021-05-15",
      "price": 3554000,
      "sqft": 1200,
      "ppsf": 2961.67,
      "bedrooms": 2,
      "dom": 28,
      "list_price": 3595000,
      "is_sponsor": false,
      "is_resale": true
    }
  ]
}
```

## Format Detection & Parsing

### CSV / Excel
Most common. Look for column headers like: Unit, Address, Close Date, Sold Price, List Price, DOM, SF, Beds.

Parsing steps:
1. Read the file with pandas
2. Normalize column names (map common variants)
3. Extract unit number, split into floor (numeric prefix) and line (letter suffix)
4. Determine sponsor vs resale: first recorded sale for a unit = sponsor
5. Compute PPSF if sqft is available

Common column name variants to handle:
- Price: "Sold Price", "Close Price", "Sale Price", "Price", "Closing Price"
- Date: "Close Date", "Sold Date", "Sale Date", "Date", "Closing Date"
- DOM: "Days on Market", "DOM", "Days On Mkt", "Market Time"
- Sqft: "SF", "Sqft", "Square Feet", "Sq Ft", "Interior SF"
- Unit: "Unit", "Apt", "Unit #", "Apartment"

### Pasted Text (StreetEasy / Listings)
The user may paste listing data directly. Look for patterns like:
- "Unit 6E | 2 BR | $3,554,000 | Sold May 2021"
- Tabular text with inconsistent spacing

Parse with regex, extracting unit, bedroom count, price, date, and any other available fields.

### JSON / Structured Data
If already structured, validate against the target schema and fill in computed fields (line, floor, PPSF, is_sponsor).

### Mixed Format
The user may provide sales data in one format and rental data in another. Parse each separately, then merge into a single transaction list with the `type` field distinguishing "sale" from "rental".

## Derived Fields

After parsing, compute:
- **line**: Extract letter suffix from unit (e.g., "6E" → "E")
- **floor**: Extract numeric prefix (e.g., "6E" → 6)
- **ppsf**: price / sqft (sales only)
- **rent_ppsf**: (monthly_rent × 12) / sqft OR monthly_rent / sqft depending on convention — use monthly for this system
- **is_sponsor**: First sale chronologically for each unit = sponsor
- **is_resale**: NOT is_sponsor for sales

## Data Quality Checks

After parsing, validate:
1. No duplicate transactions (same unit + same date + same price)
2. Prices are in reasonable range (flag anything < $100K or > $50M for NYC condos)
3. PPSF is reasonable (flag < $500 or > $10,000 for Manhattan)
4. Dates are properly ordered
5. Unit numbers follow expected pattern (number + letter)

Report any data quality issues to the user before proceeding with analysis.

## Handling Missing Data

- **Missing sqft**: Use building averages by bedroom count if available, or neighborhood medians. Flag units where sqft was imputed.
- **Missing DOM**: Exclude from liquidity calculations. Note the gap in the report.
- **Missing bedroom count**: Infer from unit line if consistent (e.g., if all "E" units are 2-bed, assume unknown E units are 2-bed). Otherwise flag.
- **Missing list price**: Cannot compute ask-to-close spread. Skip that adjustment in scoring.
