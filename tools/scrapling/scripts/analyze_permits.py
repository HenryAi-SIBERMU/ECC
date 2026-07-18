import pandas as pd
from datetime import datetime

# Load permits data
df = pd.read_csv('output/full/minerbaone_permits.csv')

print("=" * 70)
print("MINERBAONE PERMITS DATA COMPLETENESS ANALYSIS")
print("=" * 70)
print()

# Basic statistics
print(f"📊 DATASET OVERVIEW")
print(f"   Total Permits: {len(df):,}")
print(f"   Total Companies: {df['id_badan_usaha'].nunique():,}")
print()

# Date range analysis
df['tanggal_berlaku'] = pd.to_datetime(df['tanggal_berlaku'], errors='coerce')
df['tanggal_berakhir'] = pd.to_datetime(df['tanggal_berakhir'], errors='coerce')
print(f"📅 DATE RANGE (tanggal_berlaku)")
print(f"   Earliest: {df['tanggal_berlaku'].min()}")
print(f"   Latest: {df['tanggal_berlaku'].max()}")
print(f"   Year Range: {df['tanggal_berlaku'].dt.year.min()} - {df['tanggal_berlaku'].dt.year.max()}")
print()

# Luas HA analysis
print(f"📏 LUAS KAWASAN (luas_ha)")
luas_non_null = df['luas_ha'].notna().sum()
luas_null = df['luas_ha'].isna().sum()
print(f"   Non-null: {luas_non_null:,} ({luas_non_null/len(df)*100:.1f}%)")
print(f"   Null: {luas_null:,} ({luas_null/len(df)*100:.1f}%)")
if luas_non_null > 0:
    print(f"   Min: {df['luas_ha'].min():.2f} ha")
    print(f"   Max: {df['luas_ha'].max():.2f} ha")
    print(f"   Mean: {df['luas_ha'].mean():.2f} ha")
    print(f"   Total: {df['luas_ha'].sum():,.2f} ha")
print()

# Jenis Perizinan
print(f"📜 JENIS PERIZINAN")
for jenis, count in df['jenis_perizinan'].value_counts().items():
    print(f"   {jenis}: {count:,} ({count/len(df)*100:.1f}%)")
print()

# Tahap Kegiatan
print(f"⚙️  TAHAP KEGIATAN")
for tahap, count in df['tahap_kegiatan'].value_counts().head(10).items():
    print(f"   {tahap}: {count:,}")
print()

# Top Komoditas
print(f"💎 TOP 10 KOMODITAS")
for komoditas, count in df['komoditas'].value_counts().head(10).items():
    if pd.notna(komoditas):
        print(f"   {komoditas}: {count:,}")
print()

# Nickel specific analysis (for Sulawesi focus)
nickel_df = df[df['komoditas'].str.contains('Nikel|Nickel', case=False, na=False)]
print(f"🔋 NICKEL-SPECIFIC DATA")
print(f"   Total Nickel Permits: {len(nickel_df):,}")
if len(nickel_df) > 0:
    print(f"   Nickel Area (luas_ha): {nickel_df['luas_ha'].sum():,.2f} ha")
    print(f"   Nickel Locations:")
    for loc, count in nickel_df['lokasi_perizinan'].value_counts().head(5).items():
        print(f"      {loc}: {count}")
print()

# Sulawesi provinces analysis
sulawesi_keywords = ['SULAWESI', 'MOROWALI', 'KOLAKA', 'KONAWE', 'BOMBANA', 
                      'LUWU', 'DONGGALA', 'POSO', 'BANGGAI']
sulawesi_df = df[df['lokasi_perizinan'].str.contains('|'.join(sulawesi_keywords), case=False, na=False)]
print(f"🌴 SULAWESI-FOCUSED DATA")
print(f"   Total Sulawesi Permits: {len(sulawesi_df):,}")
if len(sulawesi_df) > 0:
    print(f"   Sulawesi Area (luas_ha): {sulawesi_df['luas_ha'].sum():,.2f} ha")
    print(f"   Top Komoditas in Sulawesi:")
    for komoditas, count in sulawesi_df['komoditas'].value_counts().head(5).items():
        if pd.notna(komoditas):
            print(f"      {komoditas}: {count}")
print()

# Year distribution (for 2016-2026 target)
df_with_year = df[df['tanggal_berlaku'].notna()].copy()
df_with_year['year'] = df_with_year['tanggal_berlaku'].dt.year
print(f"📈 YEAR DISTRIBUTION (2016-2026 Target)")
for year in range(2016, 2027):
    count = len(df_with_year[df_with_year['year'] == year])
    print(f"   {year}: {count:,}")
print()

# Check for capacity/investment fields (likely NOT in permits)
print(f"🔍 DATA FIELDS AVAILABLE")
print(f"   Columns: {', '.join(df.columns.tolist())}")
print()

print("=" * 70)
print("ASSESSMENT COMPLETE")
print("=" * 70)
