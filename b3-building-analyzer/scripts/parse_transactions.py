#!/usr/bin/env python3
"""
B³ Building Analyzer — Transaction Data Parser & Normalizer

Usage:
    python parse_transactions.py <input_file> [--format csv|json|text] [--output building_data.json]

Accepts CSV, Excel, JSON, or semi-structured text and normalizes to the B³ schema.
"""

import json
import re
import sys
import os
from datetime import datetime
from pathlib import Path

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False


# --- Column Name Mapping ---
COLUMN_MAP = {
    # Price variants
    'sold price': 'price', 'close price': 'price', 'sale price': 'price',
    'closing price': 'price', 'price': 'price', 'sold_price': 'price',
    'last_sold_price': 'price', 'amount': 'price',
    # Rent variants
    'rent': 'rent', 'monthly rent': 'rent', 'rent price': 'rent',
    'asking rent': 'rent', 'lease price': 'rent',
    # Date variants
    'close date': 'date', 'sold date': 'date', 'sale date': 'date',
    'closing date': 'date', 'date': 'date', 'closed': 'date',
    'lease start': 'date', 'rent date': 'date',
    # DOM variants
    'days on market': 'dom', 'dom': 'dom', 'days on mkt': 'dom',
    'market time': 'dom', 'days_on_market': 'dom',
    # Sqft variants
    'sf': 'sqft', 'sqft': 'sqft', 'square feet': 'sqft', 'sq ft': 'sqft',
    'interior sf': 'sqft', 'square_feet': 'sqft', 'size': 'sqft',
    # Unit variants
    'unit': 'unit', 'apt': 'unit', 'unit #': 'unit', 'apartment': 'unit',
    'unit_number': 'unit', 'apt #': 'unit',
    # Bedroom variants
    'beds': 'bedrooms', 'bedrooms': 'bedrooms', 'br': 'bedrooms',
    'bed': 'bedrooms', 'bedroom': 'bedrooms', 'num_beds': 'bedrooms',
    # List price
    'list price': 'list_price', 'asking price': 'list_price',
    'original price': 'list_price', 'listed price': 'list_price',
    # Type
    'type': 'transaction_type', 'transaction type': 'transaction_type',
    'trans_type': 'transaction_type',
}


def normalize_columns(df):
    """Map various column names to standard names."""
    renamed = {}
    for col in df.columns:
        key = col.strip().lower()
        if key in COLUMN_MAP:
            renamed[col] = COLUMN_MAP[key]
    return df.rename(columns=renamed)


def parse_unit(unit_str):
    """Extract floor number and line letter from unit string."""
    if not unit_str or not isinstance(unit_str, str):
        return None, None, None
    
    unit_str = unit_str.strip().upper()
    # Remove common prefixes
    unit_str = re.sub(r'^(UNIT|APT|#)\s*', '', unit_str)
    
    # Pattern: number + letter(s), e.g. "6E", "10B", "14D"
    match = re.match(r'(\d+)\s*([A-Z]+)', unit_str)
    if match:
        floor = int(match.group(1))
        line = match.group(2)
        return unit_str, floor, line
    
    # Pattern: letter + number, e.g. "E6"
    match = re.match(r'([A-Z]+)\s*(\d+)', unit_str)
    if match:
        line = match.group(1)
        floor = int(match.group(2))
        return f"{floor}{line}", floor, line
    
    return unit_str, None, None


def parse_price(price_val):
    """Clean price string to numeric."""
    if isinstance(price_val, (int, float)):
        return float(price_val)
    if not isinstance(price_val, str):
        return None
    cleaned = re.sub(r'[,$\s]', '', price_val)
    try:
        return float(cleaned)
    except ValueError:
        return None


def parse_date(date_val):
    """Parse various date formats to YYYY-MM-DD."""
    if isinstance(date_val, datetime):
        return date_val.strftime('%Y-%m-%d')
    if not isinstance(date_val, str):
        return None
    
    date_val = date_val.strip()
    formats = [
        '%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', '%m-%d-%Y',
        '%b %d, %Y', '%B %d, %Y', '%b %Y', '%B %Y',
        '%d %b %Y', '%d %B %Y', '%Y/%m/%d',
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_val, fmt).strftime('%Y-%m-%d')
        except ValueError:
            continue
    return date_val


def parse_bedrooms(bed_val):
    """Normalize bedroom count. Studio = 0."""
    if isinstance(bed_val, (int, float)):
        return int(bed_val)
    if not isinstance(bed_val, str):
        return None
    bed_val = bed_val.strip().lower()
    if bed_val in ('studio', '0', 'st'):
        return 0
    match = re.search(r'(\d+)', bed_val)
    if match:
        return int(match.group(1))
    return None


def detect_sponsor(transactions):
    """Mark first sale per unit as sponsor sale."""
    first_sale = {}
    # Sort by date
    sorted_txns = sorted(transactions, key=lambda x: x.get('date', ''))
    
    for txn in sorted_txns:
        if txn.get('type') != 'sale':
            continue
        unit = txn.get('unit')
        if unit and unit not in first_sale:
            first_sale[unit] = txn.get('date')
    
    for txn in sorted_txns:
        if txn.get('type') != 'sale':
            txn['is_sponsor'] = False
            txn['is_resale'] = False
            continue
        unit = txn.get('unit')
        if unit and txn.get('date') == first_sale.get(unit):
            txn['is_sponsor'] = True
            txn['is_resale'] = False
        else:
            txn['is_sponsor'] = False
            txn['is_resale'] = True
    
    return sorted_txns


def parse_csv_excel(filepath):
    """Parse CSV or Excel file."""
    if not HAS_PANDAS:
        print("ERROR: pandas required. Install with: pip install pandas --break-system-packages")
        sys.exit(1)
    
    ext = Path(filepath).suffix.lower()
    if ext in ('.xlsx', '.xls', '.xlsm'):
        df = pd.read_excel(filepath)
    else:
        df = pd.read_csv(filepath)
    
    df = normalize_columns(df)
    transactions = []
    
    for _, row in df.iterrows():
        unit_raw = str(row.get('unit', ''))
        unit, floor, line = parse_unit(unit_raw)
        
        # Determine transaction type
        txn_type = 'sale'
        price = None
        if 'rent' in row and pd.notna(row.get('rent')):
            txn_type = 'rental'
            price = parse_price(row.get('rent'))
        elif 'transaction_type' in row:
            t = str(row['transaction_type']).lower()
            if 'rent' in t or 'lease' in t:
                txn_type = 'rental'
                price = parse_price(row.get('rent', row.get('price')))
            else:
                price = parse_price(row.get('price'))
        else:
            price = parse_price(row.get('price'))
        
        sqft = parse_price(row.get('sqft')) if 'sqft' in row and pd.notna(row.get('sqft')) else None
        
        txn = {
            'unit': unit,
            'line': line,
            'floor': floor,
            'type': txn_type,
            'date': parse_date(row.get('date')),
            'price': price,
            'sqft': sqft,
            'ppsf': round(price / sqft, 2) if price and sqft else None,
            'bedrooms': parse_bedrooms(row.get('bedrooms')),
            'dom': int(row['dom']) if 'dom' in row and pd.notna(row.get('dom')) else None,
            'list_price': parse_price(row.get('list_price')) if 'list_price' in row else None,
        }
        
        if txn_type == 'rental':
            txn['rent_ppsf'] = round(price / sqft, 2) if price and sqft else None
        
        transactions.append(txn)
    
    return transactions


def parse_text(text):
    """Parse semi-structured pasted text (e.g., from StreetEasy)."""
    transactions = []
    lines = text.strip().split('\n')
    
    for raw_line in lines:
        raw_line = raw_line.strip()
        if not raw_line:
            continue
        
        # Try pattern: Unit XXX | N BR | $X,XXX,XXX | Sold/Rented Date
        match = re.search(
            r'(?:unit\s+)?(\d+[A-Z]+)\s*[\|,]\s*(\d+)\s*(?:BR|Bed|bed)'
            r'\s*[\|,]\s*\$?([\d,]+)\s*[\|,]\s*(sold|rented|leased)?\s*([\w\s,]+\d{4})',
            raw_line, re.IGNORECASE
        )
        if match:
            unit, floor, line_letter = parse_unit(match.group(1))
            txn_type = 'rental' if match.group(4) and 'rent' in match.group(4).lower() else 'sale'
            transactions.append({
                'unit': unit,
                'line': line_letter,
                'floor': floor,
                'type': txn_type,
                'date': parse_date(match.group(5).strip()),
                'price': parse_price(match.group(3)),
                'bedrooms': parse_bedrooms(match.group(2)),
                'sqft': None,
                'ppsf': None,
                'dom': None,
                'list_price': None,
            })
    
    return transactions


def validate_transactions(transactions):
    """Run data quality checks and return warnings."""
    warnings = []
    
    for i, txn in enumerate(transactions):
        if txn.get('price'):
            if txn['type'] == 'sale':
                if txn['price'] < 100000:
                    warnings.append(f"Row {i}: Sale price ${txn['price']:,.0f} for {txn.get('unit')} seems too low")
                if txn['price'] > 50000000:
                    warnings.append(f"Row {i}: Sale price ${txn['price']:,.0f} for {txn.get('unit')} seems too high")
            if txn['type'] == 'rental':
                if txn['price'] < 1000:
                    warnings.append(f"Row {i}: Rent ${txn['price']:,.0f} for {txn.get('unit')} seems too low")
                if txn['price'] > 100000:
                    warnings.append(f"Row {i}: Rent ${txn['price']:,.0f} for {txn.get('unit')} seems too high")
        
        if txn.get('ppsf'):
            if txn['ppsf'] < 500 or txn['ppsf'] > 10000:
                warnings.append(f"Row {i}: PPSF ${txn['ppsf']:,.0f} for {txn.get('unit')} is outside normal Manhattan range")
        
        if not txn.get('unit'):
            warnings.append(f"Row {i}: Missing unit number")
        if not txn.get('date'):
            warnings.append(f"Row {i}: Missing date for {txn.get('unit')}")
    
    # Check for duplicates
    seen = set()
    for txn in transactions:
        key = (txn.get('unit'), txn.get('date'), txn.get('price'))
        if key in seen:
            warnings.append(f"Duplicate: {txn.get('unit')} on {txn.get('date')} at ${txn.get('price', 0):,.0f}")
        seen.add(key)
    
    return warnings


def build_output(address, transactions, metadata=None):
    """Build final output JSON."""
    building = {
        'address': address,
        'neighborhood': metadata.get('neighborhood', '') if metadata else '',
        'type': metadata.get('type', '') if metadata else '',
        'year_built': metadata.get('year_built') if metadata else None,
        'total_units': metadata.get('total_units') if metadata else None,
        'floors': metadata.get('floors') if metadata else None,
    }
    
    # Detect sponsor sales
    transactions = detect_sponsor(transactions)
    
    # Summary stats
    sales = [t for t in transactions if t['type'] == 'sale']
    rentals = [t for t in transactions if t['type'] == 'rental']
    resales = [t for t in transactions if t.get('is_resale')]
    
    summary = {
        'total_transactions': len(transactions),
        'total_sales': len(sales),
        'total_rentals': len(rentals),
        'total_resales': len(resales),
        'date_range': {
            'earliest': min((t['date'] for t in transactions if t.get('date')), default=None),
            'latest': max((t['date'] for t in transactions if t.get('date')), default=None),
        },
        'lines_found': sorted(set(t['line'] for t in transactions if t.get('line'))),
        'bedroom_mix': {},
    }
    
    # Bedroom mix (transaction-weighted)
    bed_counts = {}
    for t in sales:
        beds = t.get('bedrooms')
        if beds is not None:
            label = 'Studio' if beds == 0 else f'{beds} Bed'
            bed_counts[label] = bed_counts.get(label, 0) + 1
    total = sum(bed_counts.values())
    summary['bedroom_mix'] = {k: round(v / total * 100, 1) for k, v in bed_counts.items()} if total > 0 else {}
    
    return {
        'building': building,
        'summary': summary,
        'transactions': transactions,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python parse_transactions.py <input_file> [--output output.json]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = 'building_data.json'
    
    if '--output' in sys.argv:
        idx = sys.argv.index('--output')
        if idx + 1 < len(sys.argv):
            output_file = sys.argv[idx + 1]
    
    ext = Path(input_file).suffix.lower()
    
    if ext in ('.csv', '.xlsx', '.xls', '.xlsm'):
        transactions = parse_csv_excel(input_file)
    elif ext == '.json':
        with open(input_file) as f:
            data = json.load(f)
        if isinstance(data, list):
            transactions = data
        elif 'transactions' in data:
            transactions = data['transactions']
        else:
            print("ERROR: JSON must be a list of transactions or have a 'transactions' key")
            sys.exit(1)
    elif ext == '.txt':
        with open(input_file) as f:
            text = f.read()
        transactions = parse_text(text)
    else:
        # Try as CSV
        transactions = parse_csv_excel(input_file)
    
    # Validate
    warnings = validate_transactions(transactions)
    if warnings:
        print(f"\n⚠️  {len(warnings)} data quality warnings:")
        for w in warnings:
            print(f"  - {w}")
        print()
    
    # Build output
    address = input("Building address (e.g., '45 Christopher Street'): ") if sys.stdin.isatty() else "Unknown"
    result = build_output(address, transactions)
    
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2, default=str)
    
    print(f"\n✅ Parsed {len(transactions)} transactions")
    print(f"   Sales: {result['summary']['total_sales']}")
    print(f"   Rentals: {result['summary']['total_rentals']}")
    print(f"   Resales: {result['summary']['total_resales']}")
    print(f"   Lines: {', '.join(result['summary']['lines_found'])}")
    print(f"   Output: {output_file}")


if __name__ == '__main__':
    main()
