#!/usr/bin/env python3
"""
Find the CORRECT table for PAD data based on screenshot
"""

import stadata
import pandas as pd

API_KEY = "06fd644648629502353deaed29fc6383"

print("="*80)
print("Finding CORRECT PAD Table (from screenshot)")
print("="*80)

# Initialize
client = stadata.Client(API_KEY)

print("\n📥 Loading all tables...")
tables = client.list_dynamictable(all=True)
print(f"✅ Loaded {len(tables)} tables")

# Search with keywords from screenshot
keywords = [
    'realisasi pendapatan',
    'belanja pemerintah',
    'pendapatan dan belanja',
    'kabupaten/kota',
    'keuangan pemerintah'
]

print(f"\n🔍 Searching with keywords from screenshot...")
for keyword in keywords:
    matches = tables[tables['title'].str.contains(keyword, case=False, na=False)]
    if len(matches) > 0:
        print(f"\n✅ Keyword '{keyword}': {len(matches)} tables")
        
        # Check Sulawesi Selatan specifically
        sulsel = matches[matches['domain'] == '7300']
        if not sulsel.empty:
            print(f"\n🎯 FOUND IN SULAWESI SELATAN (7300)!")
            print(sulsel[['var_id', 'title', 'domain']].to_string())
        else:
            # Check all Sulawesi
            all_sulawesi = matches[
                matches['domain'].str.startswith(('71', '72', '73', '74', '75', '76'))
            ]
            if not all_sulawesi.empty:
                print(f"\n📍 Found in Sulawesi region:")
                print(all_sulawesi[['var_id', 'title', 'domain']].head(10).to_string())

# Also try broad financial keywords
print(f"\n\n🔍 Trying broader search for Sulawesi Selatan (7300)...")
sulsel_all = tables[tables['domain'] == '7300']
print(f"Total tables for Sulsel: {len(sulsel_all)}")

# Check for any financial/keuangan tables
financial = sulsel_all[
    sulsel_all['title'].str.contains('keuangan|pendapatan|belanja|apbd', case=False, na=False, regex=True)
]
print(f"\nFinancial-related tables in Sulsel: {len(financial)}")
if not financial.empty:
    print("\n📊 Sample financial tables:")
    print(financial[['var_id', 'title']].head(20).to_string())
