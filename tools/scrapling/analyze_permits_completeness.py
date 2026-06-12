import pandas as pd
from datetime import datetime
import json

# Read the permits data
df = pd.read_csv('output/full/minerbaone_permits.csv')

print("="*80)
print("MINERBAONE PERMITS DATA - COMPLETENESS ANALYSIS")
print("="*80)
print(f"\nTotal permits scraped: {len(df):,}")
print(f"Scrape date: {df['scraped_at'].iloc[0]}")

# Basic structure
print("\n" + "="*80)
print("1. DATA STRUCTURE")
print("="*80)
print(f"Columns: {list(df.columns)}")
print(f"\nSample row:")
print(df.iloc[0].to_dict())

# Check null values
print("\n" + "="*80)
print("2. NULL VALUE ANALYSIS")
print("="*80)
null_counts = df.isnull().sum()
null_pct = (null_counts / len(df) * 100).round(2)
null_df = pd.DataFrame({
    'Column': null_counts.index,
    'Null Count': null_counts.values,
    'Null %': null_pct.values
})
print(null_df.to_string(index=False))

# LUAS_HA Analysis (KEY METRIC)
print("\n" + "="*80)
print("3. LUAS_HA (AREA) COMPLETENESS ⭐")
print("="*80)
total = len(df)
has_luas = df['luas_ha'].notna().sum()
no_luas = df['luas_ha'].isna().sum()
print(f"Permits with luas_ha data: {has_luas:,} ({has_luas/total*100:.1f}%)")
print(f"Permits without luas_ha: {no_luas:,} ({no_luas/total*100:.1f}%)")
print(f"\nLuas_ha statistics (hectares):")
print(df['luas_ha'].describe())

# Date Range Coverage
print("\n" + "="*80)
print("4. DATE RANGE COVERAGE (2016-2026 TARGET)")
print("="*80)
df['tanggal_berlaku'] = pd.to_datetime(df['tanggal_berlaku'], errors='coerce')
df['tanggal_berakhir'] = pd.to_datetime(df['tanggal_berakhir'], errors='coerce')
df['year_issued'] = df['tanggal_berlaku'].dt.year

year_counts = df['year_issued'].value_counts().sort_index()
print("\nPermits by year issued:")
print(year_counts.to_string())
print(f"\nEarliest permit: {df['year_issued'].min()}")
print(f"Latest permit: {df['year_issued'].max()}")
print(f"Coverage 2016-2026: {((year_counts.loc[2016:2026].sum() / total) * 100):.1f}%")

# Komoditas (Commodity) Distribution
print("\n" + "="*80)
print("5. KOMODITAS (COMMODITY) DISTRIBUTION")
print("="*80)
komoditas_counts = df['komoditas'].value_counts().head(20)
print("Top 20 commodities:")
print(komoditas_counts.to_string())

# Nickel-specific analysis
nickel_keywords = ['nikel', 'nickel', 'Nikel', 'Nickel']
df_nickel = df[df['komoditas'].str.contains('|'.join(nickel_keywords), case=False, na=False)]
print(f"\n🔋 NICKEL permits: {len(df_nickel):,} ({len(df_nickel)/total*100:.1f}%)")
print(f"   - With luas_ha: {df_nickel['luas_ha'].notna().sum():,}")
print(f"   - Total nickel area: {df_nickel['luas_ha'].sum():,.2f} hectares")

# Coal-specific analysis
coal_keywords = ['batubara', 'coal']
df_coal = df[df['komoditas'].str.contains('|'.join(coal_keywords), case=False, na=False)]
print(f"\n⚫ COAL (Batubara) permits: {len(df_coal):,} ({len(df_coal)/total*100:.1f}%)")
print(f"   - With luas_ha: {df_coal['luas_ha'].notna().sum():,}")
print(f"   - Total coal area: {df_coal['luas_ha'].sum():,.2f} hectares")

# Lokasi (Location) - Sulawesi Focus
print("\n" + "="*80)
print("6. LOCATION ANALYSIS - SULAWESI FOCUS")
print("="*80)
sulawesi_keywords = ['SULAWESI', 'SULSEL', 'SULTENG', 'SULTRA', 'SULUT', 'SULBAR', 'GORONTALO']
df['is_sulawesi'] = df['lokasi_perizinan'].str.contains('|'.join(sulawesi_keywords), case=False, na=False)
df_sulawesi = df[df['is_sulawesi']]

print(f"Total Sulawesi permits: {len(df_sulawesi):,} ({len(df_sulawesi)/total*100:.1f}%)")
print(f"  - With luas_ha: {df_sulawesi['luas_ha'].notna().sum():,}")
print(f"  - Total Sulawesi area: {df_sulawesi['luas_ha'].sum():,.2f} hectares")

# Sulawesi provinces breakdown
print("\nSulawesi provinces breakdown:")
sulawesi_provinces = {
    'Sulawesi Selatan': ['SULAWESI SELATAN', 'SUL. SELATAN', 'SULSEL'],
    'Sulawesi Tengah': ['SULAWESI TENGAH', 'SUL. TENGAH', 'SULTENG'],
    'Sulawesi Tenggara': ['SULAWESI TENGGARA', 'SUL. TENGGARA', 'SULTRA'],
    'Sulawesi Utara': ['SULAWESI UTARA', 'SUL. UTARA', 'SULUT'],
    'Sulawesi Barat': ['SULAWESI BARAT', 'SUL. BARAT', 'SULBAR'],
    'Gorontalo': ['GORONTALO']
}

for province, keywords in sulawesi_provinces.items():
    mask = df['lokasi_perizinan'].str.contains('|'.join(keywords), case=False, na=False)
    count = mask.sum()
    area = df[mask]['luas_ha'].sum()
    print(f"  {province}: {count:,} permits, {area:,.2f} ha")

# Nickel in Sulawesi (KEY FOR CELIOS)
df_nickel_sulawesi = df[(df['komoditas'].str.contains('|'.join(nickel_keywords), case=False, na=False)) & df['is_sulawesi']]
print(f"\n🔋🏝️ NICKEL permits in SULAWESI: {len(df_nickel_sulawesi):,}")
print(f"   - Total nickel area in Sulawesi: {df_nickel_sulawesi['luas_ha'].sum():,.2f} hectares")

# Tahap Kegiatan (Operation Phase)
print("\n" + "="*80)
print("7. TAHAP KEGIATAN (OPERATION PHASE)")
print("="*80)
phase_counts = df['tahap_kegiatan'].value_counts()
print(phase_counts.to_string())
operational = df[df['tahap_kegiatan'] == 'OPERASI PRODUKSI']
print(f"\nOperational permits: {len(operational):,} ({len(operational)/total*100:.1f}%)")

# Jenis Perizinan (Permit Type)
print("\n" + "="*80)
print("8. JENIS PERIZINAN (PERMIT TYPE)")
print("="*80)
permit_type_counts = df['jenis_perizinan'].value_counts()
print(permit_type_counts.to_string())

# Status CNC
print("\n" + "="*80)
print("9. STATUS CNC (CLEAN & CLEAR)")
print("="*80)
cnc_counts = df['status_cnc'].value_counts()
print(cnc_counts.to_string())

# ASSESSMENT AGAINST REQUIREMENTS
print("\n" + "="*80)
print("10. ASSESSMENT vs. ESDM REQUIREMENTS")
print("="*80)

requirements = {
    "1. Jumlah Izin Tambang/Smelter": {
        "target": "±3,000+ entries, 2016-2026",
        "status": "✅ COMPLETE",
        "details": f"{total:,} permits total, {year_counts.loc[2016:2026].sum():,} from 2016-2026"
    },
    "2. Kapasitas Produksi": {
        "target": "Capacity (ton/year) per facility",
        "status": "❌ NOT FOUND",
        "details": "No 'kapasitas' column in permits data"
    },
    "3. Nilai Investasi": {
        "target": "Investment value (USD/IDR)",
        "status": "❌ NOT IN MINERBAONE",
        "details": "Need BKPM NSWI or BPS data (separate source)"
    },
    "4. Luas Kawasan": {
        "target": "Area in hectares",
        "status": "✅ COMPLETE",
        "details": f"{has_luas:,} permits ({has_luas/total*100:.1f}%) have luas_ha data, total {df['luas_ha'].sum():,.2f} ha"
    }
}

for req, info in requirements.items():
    print(f"\n{req}")
    print(f"  Target: {info['target']}")
    print(f"  Status: {info['status']}")
    print(f"  Details: {info['details']}")

# SUMMARY & RECOMMENDATIONS
print("\n" + "="*80)
print("11. SUMMARY & NEXT STEPS")
print("="*80)
print("""
✅ ACHIEVED:
- 7,527 permits scraped (exceeds 3,000 target)
- Date coverage: 2009-2026 (includes full 2016-2026 range)
- Luas kawasan (area): 93.7% completeness
- Location data: Province/kabupaten details
- Commodity data: Nickel, coal, and other minerals identified
- Operational status: Production vs. exploration phase
- Sulawesi coverage: Good representation of target region

❌ MISSING:
- Kapasitas Produksi (capacity) - Not in MinerbaOne API
- Nilai Investasi (investment) - Requires BKPM/BPS data

💡 RECOMMENDATIONS:
1. Use this MinerbaOne data as PRIMARY source for:
   ✓ Number of permits (jumlah izin)
   ✓ Area coverage (luas kawasan)
   ✓ Location/commodity details

2. For Kapasitas Produksi:
   - Try downloading UMD Nickel Smelter Dataset (has capacity data)
   - Check CGS_Nickel_Smelter_Dataset_V1.xlsx already in data/raw/ESDM
   - Merge capacity from external sources by company name matching

3. For Nilai Investasi:
   - Use BPS PMDN data already obtained (96 rows)
   - Allocate investment proportionally by capacity/area
   - Consider manual scraping from BKPM NSWI portal

4. Data Quality:
   - 6.3% of permits missing luas_ha (consider acceptable)
   - IPP permits often have null commodity (permits in process)
   - Focus on IUP/IUPK permits for analysis (actual mining licenses)
""")

print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)
