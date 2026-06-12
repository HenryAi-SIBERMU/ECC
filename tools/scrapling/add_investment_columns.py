"""
Add investment & IUP columns to existing minerbaone_sulawesi_companies.csv
"""
import csv
from pathlib import Path

BASE_DIR = Path(__file__).parent
INPUT_FILE = BASE_DIR.parent.parent / "data" / "processed" / "minerbaone_sulawesi_companies.csv"
OUTPUT_FILE = BASE_DIR.parent.parent / "data" / "processed" / "minerbaone_sulawesi_full.csv"
PERMITS_FILE = BASE_DIR / "output" / "full" / "minerbaone_permits.csv"

print("="*70)
print("ADD INVESTMENT & IUP COLUMNS")
print("="*70)

# Load permits to check IUP status
print("\n[1/2] Loading permits to check IUP status...")
iup_companies = set()
with open(PERMITS_FILE, 'r', encoding='utf-8', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        jenis_izin = row.get('jenis_perizinan', '')
        if 'IUP' in jenis_izin:
            iup_companies.add(row.get('id_badan_usaha', ''))

print(f"  ✓ Found {len(iup_companies):,} companies with IUP")

# Load existing CSV and add columns
print("\n[2/2] Adding investment & IUP columns...")
rows = []
with open(INPUT_FILE, 'r', encoding='utf-8', newline='') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    
    # Add new columns
    new_columns = [
        'has_iup',  # Legal IUP status
        'investment_value_usd_million',  # USD million
        'investment_value_idr_billion',  # IDR billion
        'investment_year',  # Year
        'production_capacity_ton_year',  # Ton/year
        'capacity_type',  # ore/ferronickel/NPI/RKEF
        'operational_status',  # operational/construction/planned
        'data_source_investment',  # Source URL/document
        'data_source_capacity',  # Source URL/document
        'notes'  # Additional notes
    ]
    
    # Remove has_nickel_permit from fieldnames if exists, add at end
    if 'has_nickel_permit' in fieldnames:
        fieldnames = list(fieldnames)
        fieldnames.remove('has_nickel_permit')
    
    final_fieldnames = fieldnames + new_columns + ['has_nickel_permit']
    
    for row in reader:
        # Add IUP status
        id_bu = row.get('id_badan_usaha', '')
        row['has_iup'] = 'YES' if id_bu in iup_companies else 'NO'
        
        # Add placeholder columns
        row['investment_value_usd_million'] = ''
        row['investment_value_idr_billion'] = ''
        row['investment_year'] = ''
        row['production_capacity_ton_year'] = ''
        row['capacity_type'] = ''
        row['operational_status'] = ''
        row['data_source_investment'] = ''
        row['data_source_capacity'] = ''
        row['notes'] = ''
        
        rows.append(row)

# Write output
with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=final_fieldnames, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(rows)

# Stats
total = len(rows)
with_iup = sum(1 for row in rows if row['has_iup'] == 'YES')
with_nickel = sum(1 for row in rows if row.get('has_nickel_permit') == 'YES')

print("\n" + "="*70)
print("RESULTS")
print("="*70)
print(f"Total Companies:       {total:,}")
print(f"Companies with IUP:    {with_iup:,} ({100*with_iup/total:.1f}%)")
print(f"Companies with Nickel: {with_nickel:,} ({100*with_nickel/total:.1f}%)")
print(f"Illegal (NO IUP):      {total-with_iup:,} ({100*(total-with_iup)/total:.1f}%)")

print(f"\n✓ Saved to: {OUTPUT_FILE}")
print("\nNext Step: Run Google dorking to fill investment columns!")
print("See: docs/DORKING_PLAN_MINING_INVESTMENT.md")
print("="*70)
