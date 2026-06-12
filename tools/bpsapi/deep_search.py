#!/usr/bin/env python3
"""
Deep Search for Ekspor & PAD Data
CELIOS ECC Intelligence System

Comprehensive search with multiple keywords and approaches
"""

import stadata
import pandas as pd
import json
from pathlib import Path

# API Key
API_KEY = "06fd644648629502353deaed29fc6383"

# Sulawesi province codes
SULAWESI_CODES = ['7100', '7200', '7300', '7400', '7500', '7600']

# Multiple search terms for ekspor
EKSPOR_KEYWORDS = [
    'ekspor',
    'export',
    'perdagangan',
    'trade',
    'luar negeri',
    'foreign trade',
    'migas',
    'non migas',
    'komoditas',
    'commodity'
]

# Multiple search terms for PAD
PAD_KEYWORDS = [
    'pad',
    'pendapatan asli daerah',
    'pendapatan daerah',
    'penerimaan daerah',
    'keuangan daerah',
    'apbd',
    'anggaran',
    'fiskal',
    'pajak daerah',
    'retribusi',
    'revenue',
    'local revenue',
    'regional income'
]


def search_with_keywords(tables_df: pd.DataFrame, keywords: list, label: str) -> pd.DataFrame:
    """Search tables using multiple keywords"""
    print(f"\n🔍 SEARCHING: {label}")
    print("="*80)
    
    all_results = []
    
    for keyword in keywords:
        matches = tables_df[
            tables_df['title'].str.contains(keyword, case=False, na=False)
        ]
        
        if len(matches) > 0:
            print(f"\n✅ Keyword '{keyword}': {len(matches)} tables found")
            all_results.append(matches)
        else:
            print(f"   Keyword '{keyword}': No matches")
    
    if all_results:
        # Combine and remove duplicates
        combined = pd.concat(all_results).drop_duplicates(subset=['var_id'])
        print(f"\n📊 TOTAL UNIQUE: {len(combined)} tables")
        return combined
    else:
        print(f"\n❌ NO RESULTS for {label}")
        return pd.DataFrame()


def check_sulawesi_availability(results_df: pd.DataFrame, label: str):
    """Check if data available for Sulawesi provinces"""
    print(f"\n🎯 CHECKING SULAWESI AVAILABILITY: {label}")
    print("="*80)
    
    if results_df.empty:
        print("❌ No data to check (empty results)")
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
            print(f"✅ {province_name} ({code}): {len(matches)} tables")
        else:
            print(f"❌ {province_name} ({code}): No tables")
    
    # Check national level
    national = results_df[results_df['domain'] == '0000']
    print(f"\n🇮🇩 NATIONAL (0000): {len(national)} tables")
    
    # Check all Sulawesi-related (including cities/regencies)
    all_sulawesi = results_df[
        results_df['domain'].str.startswith(tuple(['71', '72', '73', '74', '75', '76']))
    ]
    print(f"🏝️  ALL SULAWESI REGION (71*, 72*, 73*, 74*, 75*, 76*): {len(all_sulawesi)} tables")
    
    return all_sulawesi


def analyze_subject_categories(tables_df: pd.DataFrame):
    """Analyze available subject categories"""
    print(f"\n📚 SUBJECT CATEGORIES ANALYSIS")
    print("="*80)
    
    if 'subcat' in tables_df.columns:
        subjects = tables_df['subcat'].value_counts().head(20)
        print("\nTop 20 Subject Categories:")
        for subj, count in subjects.items():
            print(f"  {subj}: {count} tables")
    
    if 'sub_name' in tables_df.columns:
        sub_names = tables_df['sub_name'].value_counts().head(20)
        print("\nTop 20 Sub Names:")
        for name, count in sub_names.items():
            print(f"  {name}: {count} tables")


def main():
    print("="*80)
    print("DEEP SEARCH: EKSPOR & PAD DATA")
    print("="*80)
    
    # Initialize client
    client = stadata.Client(API_KEY)
    
    print("\n📥 Fetching all dynamic tables...")
    print("⏳ This may take a few moments (30,613 tables)...")
    
    tables = client.list_dynamictable(all=True)
    print(f"✅ Loaded {len(tables)} tables")
    
    # Save original data
    print("\n💾 Saving full table list...")
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    tables.to_csv("output/all_bps_tables.csv", index=False, encoding='utf-8-sig')
    print(f"   Saved: output/all_bps_tables.csv ({len(tables)} rows)")
    
    # Search for EKSPOR
    print("\n" + "="*80)
    ekspor_results = search_with_keywords(tables, EKSPOR_KEYWORDS, "EKSPOR DATA")
    
    if not ekspor_results.empty:
        # Check Sulawesi availability
        ekspor_sulawesi = check_sulawesi_availability(ekspor_results, "EKSPOR")
        
        # Save results
        ekspor_results.to_csv("output/ekspor_search_results.csv", index=False, encoding='utf-8-sig')
        print(f"\n💾 Saved: output/ekspor_search_results.csv")
        
        # Show sample
        print("\n📋 SAMPLE EKSPOR TABLES (first 10):")
        print(ekspor_results[['var_id', 'title', 'domain', 'sub_name']].head(10).to_string())
    
    # Search for PAD
    print("\n" + "="*80)
    pad_results = search_with_keywords(tables, PAD_KEYWORDS, "PAD DATA")
    
    if not pad_results.empty:
        # Check Sulawesi availability
        pad_sulawesi = check_sulawesi_availability(pad_results, "PAD")
        
        # Save results
        pad_results.to_csv("output/pad_search_results.csv", index=False, encoding='utf-8-sig')
        print(f"\n💾 Saved: output/pad_search_results.csv")
        
        # Show sample
        print("\n📋 SAMPLE PAD TABLES (first 10):")
        print(pad_results[['var_id', 'title', 'domain', 'sub_name']].head(10).to_string())
    
    # Analyze subject categories
    print("\n" + "="*80)
    analyze_subject_categories(tables)
    
    # SUMMARY
    print("\n" + "="*80)
    print("📊 SEARCH SUMMARY")
    print("="*80)
    
    summary = {
        "total_tables": len(tables),
        "ekspor_found": len(ekspor_results),
        "ekspor_sulawesi": len(ekspor_results[
            ekspor_results['domain'].str.startswith(tuple(['71', '72', '73', '74', '75', '76']))
        ]) if not ekspor_results.empty else 0,
        "ekspor_national": len(ekspor_results[ekspor_results['domain'] == '0000']) if not ekspor_results.empty else 0,
        "pad_found": len(pad_results),
        "pad_sulawesi": len(pad_results[
            pad_results['domain'].str.startswith(tuple(['71', '72', '73', '74', '75', '76']))
        ]) if not pad_results.empty else 0,
        "pad_national": len(pad_results[pad_results['domain'] == '0000']) if not pad_results.empty else 0,
    }
    
    print(f"\nTotal tables scanned: {summary['total_tables']:,}")
    print(f"\n📦 EKSPOR:")
    print(f"  - Total found: {summary['ekspor_found']}")
    print(f"  - Sulawesi region: {summary['ekspor_sulawesi']}")
    print(f"  - National level: {summary['ekspor_national']}")
    
    print(f"\n💰 PAD:")
    print(f"  - Total found: {summary['pad_found']}")
    print(f"  - Sulawesi region: {summary['pad_sulawesi']}")
    print(f"  - National level: {summary['pad_national']}")
    
    # Save summary
    with open("output/search_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Summary saved: output/search_summary.json")
    
    print("\n" + "="*80)
    print("✅ DEEP SEARCH COMPLETE!")
    print("="*80)
    print("\nFiles generated:")
    print("  1. output/all_bps_tables.csv - All 30K+ tables")
    print("  2. output/ekspor_search_results.csv - Ekspor matches")
    print("  3. output/pad_search_results.csv - PAD matches")
    print("  4. output/search_summary.json - Summary statistics")


if __name__ == "__main__":
    main()
