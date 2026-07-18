#!/usr/bin/env python3
"""
Search Zoonosis Tables from BPS API Cache
CELIOS ECC Intelligence System
"""

import pandas as pd
from pathlib import Path

# Sulawesi province codes
SULAWESI_CODES = ['7100', '7200', '7300', '7400', '7500', '7600']

ZOONOSIS_KEYWORDS = [
    'malaria',
    'demam berdarah',
    'dbd',
    'dengue',
    'rabies',
    'kusta',
    'zoonosis',
    'filariasis',
    'leptospirosis'
]

def check_sulawesi_availability(results_df: pd.DataFrame, label: str):
    """Check if data available for Sulawesi provinces"""
    print(f"\n[TARGET] CHECKING SULAWESI AVAILABILITY: {label}")
    print("="*80)
    
    if results_df.empty:
        print("[X] No data to check (empty results)")
        return pd.DataFrame()
    
    # Check each Sulawesi province
    sulawesi_results = {}
    
    for code in SULAWESI_CODES:
        matches = results_df[results_df['domain'] == code]
        province_name = {
            '7100': 'Sulawesi Utara',
            '7200': 'Sulawesi Tengah',
            '7300': 'Sulawesi Selatan',
            '7400': 'Sulawesi Tenggara',
            '7500': 'Gorontalo',
            '7600': 'Sulawesi Barat'
        }[code]
        
        sulawesi_results[province_name] = len(matches)
        
        if len(matches) > 0:
            print(f"[V] {province_name} ({code}): {len(matches)} tables")
        else:
            print(f"[X] {province_name} ({code}): No tables")
    
    # Check national level
    national = results_df[results_df['domain'] == '0000']
    print(f"\n[ID] NATIONAL (0000): {len(national)} tables")
    
    # Check all Sulawesi-related (including cities/regencies)
    all_sulawesi = results_df[
        results_df['domain'].str.startswith(tuple(['71', '72', '73', '74', '75', '76']))
    ]
    print(f"[SULAWESI]  ALL SULAWESI REGION (71*, 72*, 73*, 74*, 75*, 76*): {len(all_sulawesi)} tables")
    
    return all_sulawesi


def main():
    print("="*80)
    print("SEARCH: ZOONOSIS (MALARIA, DBD) DATA")
    print("="*80)
    
    csv_path = Path("tools/bpsapi/output/all_bps_tables.csv")
    if not csv_path.exists():
        print(f"[X] Cache file not found: {csv_path}")
        print("Please run deep_search.py first.")
        return

    print("\n[V] Loading BPS tables cache...")
    tables_df = pd.read_csv(csv_path)
    # Fill NaN titles with empty string to avoid errors in str.contains
    tables_df['title'] = tables_df['title'].fillna('')
    # Convert domain to string so 7100 matches '7100' instead of int 7100
    tables_df['domain'] = tables_df['domain'].astype(str)
    print(f"[V] Loaded {len(tables_df)} tables")

    all_results = []
    
    for keyword in ZOONOSIS_KEYWORDS:
        matches = tables_df[
            tables_df['title'].str.contains(keyword, case=False, regex=False)
        ]
        
        if len(matches) > 0:
            print(f"\n[V] Keyword '{keyword}': {len(matches)} tables found")
            all_results.append(matches)
        else:
            print(f"   Keyword '{keyword}': No matches")
            
    if all_results:
        combined = pd.concat(all_results).drop_duplicates(subset=['var_id', 'domain'])
        print(f"\n[STAT] TOTAL UNIQUE: {len(combined)} tables related to Zoonosis")
        
        # Check Availability
        sulawesi_df = check_sulawesi_availability(combined, "ZOONOSIS")
        
        # Save results
        out_file = "tools/bpsapi/output/zoonosis_search_results.csv"
        combined.to_csv(out_file, index=False, encoding='utf-8-sig')
        print(f"\n[SAVE] Saved full results: {out_file}")
        
        if not sulawesi_df.empty:
            out_sulawesi = "tools/bpsapi/output/zoonosis_sulawesi_only.csv"
            sulawesi_df.to_csv(out_sulawesi, index=False, encoding='utf-8-sig')
            print(f"[SAVE] Saved Sulawesi-only results: {out_sulawesi}")
            
            print("\n[SAMPLE] SAMPLE SULAWESI TABLES (first 10):")
            print(sulawesi_df[['var_id', 'title', 'domain', 'sub_name']].head(10).to_string())
    else:
        print("\n[X] NO RESULTS for Zoonosis keywords.")

if __name__ == "__main__":
    main()
