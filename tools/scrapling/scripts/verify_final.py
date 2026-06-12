#!/usr/bin/env python3
"""Verify final scraped data"""

import pandas as pd

df = pd.read_csv('output/tanahkita_konflik.csv')

print("="*80)
print("FINAL DATA VERIFICATION - CELIOS ECC Data Konflik")
print("="*80)

print(f"\n✅ Total rows scraped: {len(df)}")
print(f"✅ Duplicates: {df.duplicated().sum()}")
print(f"✅ Nomor range: {df['nomor'].min()} - {df['nomor'].max()}")

print(f"\n📊 Non-null counts:")
for col in df.columns:
    non_null = df[col].notna().sum()
    pct = (non_null / len(df)) * 100
    print(f"  {col:15s}: {non_null:4d} / {len(df)} ({pct:5.1f}%)")

print(f"\n🏷️  Status distribution:")
print(df['status'].value_counts())

print(f"\n📅 Tahun distribution:")
print(df['tahun'].value_counts().sort_index())

print(f"\n📍 Lokasi distribution (top 10):")
print(df['lokasi'].value_counts().head(10))

print(f"\n📝 Sample first 5 entries:")
print(df[['nomor', 'tahun', 'judul']].head(5).to_string(index=False))

print(f"\n📝 Sample last 5 entries:")
print(df[['nomor', 'tahun', 'judul']].tail(5).to_string(index=False))

print("\n" + "="*80)
print("✅ DATA READY FOR CELIOS ECC ANALYSIS!")
print("="*80)
print(f"\n📁 Files generated:")
print(f"   - tanahkita_konflik.csv ({len(df)} rows)")
print(f"   - tanahkita_konflik.json (same data)")
print(f"\n🎯 Next steps:")
print(f"   1. Load ke Pandas untuk EDA")
print(f"   2. Clean & normalize data")
print(f"   3. Extract spatial coordinates dari lokasi")
print(f"   4. Link dengan data BPS, KLHK, PLN")

