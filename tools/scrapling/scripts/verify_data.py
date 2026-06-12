#!/usr/bin/env python3
"""Verify scraped data quality"""

import pandas as pd

df = pd.read_csv('output/tanahkita_konflik_full.csv')

print("="*80)
print("DATA VERIFICATION REPORT")
print("="*80)

print(f"\n📊 Total rows scraped: {len(df)}")
print(f"📋 Columns: {list(df.columns)}")

print(f"\n📈 Data types:")
print(df.dtypes)

print(f"\n✅ Non-null counts:")
print(df.count())

print(f"\n📝 Sample data (first 3 rows):")
print(df.head(3)[['nomor', 'tahun', 'judul', 'lokasi', 'status']])

print(f"\n📝 Sample data (last 3 rows):")
print(df.tail(3)[['nomor', 'tahun', 'judul', 'lokasi', 'status']])

print(f"\n🏷️  Status distribution:")
print(df['status'].value_counts())

print(f"\n📅 Tahun distribution:")
print(df['tahun'].value_counts().sort_index())

print(f"\n📍 Lokasi distribution (top 10):")
print(df['lokasi'].value_counts().head(10))

print(f"\n🔗 Detail URLs sample:")
print(df['detail_url'].head(5))

print("\n" + "="*80)
print("✅ VERIFICATION COMPLETE")
print("="*80)
