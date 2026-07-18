#!/usr/bin/env python3
"""
Check STATIC tables for PAD data
"""

import stadata
import pandas as pd

API_KEY = "06fd644648629502353deaed29fc6383"

print("="*80)
print("Checking STATIC Tables for PAD Data")
print("="*80)

client = stadata.Client(API_KEY)

print("\n📥 Loading static tables for Sulawesi Selatan (7300)...")
try:
    static = client.list_statictable(all=False, domain=['7300'])
    print(f"✅ Total static tables: {len(static)}")
    
    if not static.empty:
        # Search for financial data
        pad_static = static[
            static['title'].str.contains('pendapatan|belanja|keuangan|apbd|realisasi', 
                                        case=False, na=False, regex=True)
        ]
        print(f"\n💰 Financial static tables: {len(pad_static)}")
        
        if not pad_static.empty:
            print("\n📊 Sample tables:")
            print(pad_static[['table_id', 'title']].head(20).to_string())
        else:
            print("\n❌ No financial static tables found")
            print("\nAll static tables:")
            print(static[['table_id', 'title']].head(20).to_string())
    else:
        print("\n❌ No static tables found for domain 7300")
        
except Exception as e:
    print(f"\n❌ Error: {e}")

print("\n" + "="*80)
print("CONCLUSION:")
print("="*80)
print("Data di screenshot Anda kemungkinan:")
print("1. Dari publikasi/tabel statis BPS (bukan dynamic table)")
print("2. Butuh table_id spesifik untuk diakses")
print("3. Atau hanya tersedia via web interface (perlu scraping)")
