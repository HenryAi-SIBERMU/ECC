"""
ESDM Data Gap Analysis
Compares MinerbaOne scraped data against ESDM requirements
and analyzes CGS Nickel Smelter dataset
"""
import pandas as pd
from datetime import datetime
import openpyxl

print("="*100)
print("ESDM DATA COLLECTION - GAP ANALYSIS REPORT")
print("="*100)
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# ============================================================================
# PART 1: MinerbaOne Permits Analysis
# ============================================================================
print("\n" + "="*100)
print("PART 1: MINERBAONE PERMITS DATA")
print("="*100)

df_permits = pd.read_csv('output/full/minerbaone_permits.csv')
df_permits['tanggal_berlaku'] = pd.to_datetime(df_permits['tanggal_berlaku'], errors='coerce')
df_permits['year_issued'] = df_permits['tanggal_berlaku'].dt.year

print(f"\nTotal permits scraped: {len(df_permits):,}")
print(f"Time period: {df_permits['year_issued'].min()} - {df_permits['year_issued'].max()}")
print(f"Permits from 2016-2026: {len(df_permits[df_permits['year_issued'].between(2016, 2026)]):,}")

# Fix Sulawesi detection (case-sensitive issue)
df_permits['lokasi_upper'] = df_permits['lokasi_perizinan'].fillna('').str.upper()
sulawesi_mask = (
    df_permits['lokasi_upper'].str.contains('SULAWESI') |
    df_permits['lokasi_upper'].str.contains('GORONTALO')
)
df_sulawesi = df_permits[sulawesi_mask].copy()

print(f"\n📍 Sulawesi permits: {len(df_sulawesi):,} ({len(df_sulawesi)/len(df_permits)*100:.1f}%)")

# Sulawesi provinces breakdown
sulawesi_provinces = {
    'Sulawesi Selatan': ['SULAWESI SELATAN', 'SULSEL'],
    'Sulawesi Tengah': ['SULAWESI TENGAH', 'SULTENG'],
    'Sulawesi Tenggara': ['SULAWESI TENGGARA', 'SULTRA'],
    'Sulawesi Utara': ['SULAWESI UTARA', 'SULUT'],
    'Sulawesi Barat': ['SULAWESI BARAT', 'SULBAR'],
    'Gorontalo': ['GORONTALO']
}

print("\nSulawesi provinces breakdown:")
for province, keywords in sulawesi_provinces.items():
    mask = df_permits['lokasi_upper'].str.contains('|'.join(keywords), na=False)
    count = mask.sum()
    area = df_permits[mask]['luas_ha'].sum()
    nickel_count = ((df_permits['komoditas'].str.contains('ikel', case=False, na=False)) & mask).sum()
    print(f"  {province:25s}: {count:4,} permits | {area:12,.0f} ha | {nickel_count:3,} nickel")

# Nickel analysis
nickel_mask = df_permits['komoditas'].str.contains('ikel', case=False, na=False)
df_nickel = df_permits[nickel_mask].copy()
df_nickel_sulawesi = df_permits[nickel_mask & sulawesi_mask].copy()

print(f"\n🔋 NICKEL PERMITS:")
print(f"  National total: {len(df_nickel):,} permits")
print(f"  Sulawesi: {len(df_nickel_sulawesi):,} permits ({len(df_nickel_sulawesi)/len(df_nickel)*100:.1f}% of all nickel)")
print(f"  Nickel area in Sulawesi: {df_nickel_sulawesi['luas_ha'].sum():,.0f} hectares")
print(f"  Operational nickel (Sulawesi): {(df_nickel_sulawesi['tahap_kegiatan'] == 'OPERASI PRODUKSI').sum():,}")

# ============================================================================
# PART 2: CGS Nickel Smelter Dataset Analysis
# ============================================================================
print("\n" + "="*100)
print("PART 2: CGS/UMD NICKEL SMELTER DATASET")
print("="*100)

try:
    # Read the Excel file
    cgs_file = '../../data/raw/ESDM/CGS_Nickel_Smelter_Dataset_V1.xlsx'
    df_cgs = pd.read_excel(cgs_file, sheet_name=0)
    
    print(f"\n✅ CGS dataset loaded successfully")
    print(f"Total smelters in dataset: {len(df_cgs)}")
    print(f"\nColumns available:")
    for i, col in enumerate(df_cgs.columns, 1):
        print(f"  {i:2d}. {col}")
    
    # Check for capacity data
    capacity_cols = [col for col in df_cgs.columns if 'capacity' in col.lower() or 'kapasitas' in col.lower()]
    if capacity_cols:
        print(f"\n🎯 CAPACITY DATA FOUND:")
        for col in capacity_cols:
            non_null = df_cgs[col].notna().sum()
            print(f"  - {col}: {non_null}/{len(df_cgs)} entries")
    
    # Check for investment data
    investment_cols = [col for col in df_cgs.columns if 'invest' in col.lower() or 'nilai' in col.lower()]
    if investment_cols:
        print(f"\n💰 INVESTMENT DATA FOUND:")
        for col in investment_cols:
            non_null = df_cgs[col].notna().sum()
            print(f"  - {col}: {non_null}/{len(df_cgs)} entries")
    
    # Location analysis
    location_cols = [col for col in df_cgs.columns if 'location' in col.lower() or 'lokasi' in col.lower() or 'province' in col.lower()]
    if location_cols:
        print(f"\n📍 LOCATION DATA:")
        for col in location_cols:
            print(f"  - {col}")
            if df_cgs[col].dtype == 'object':
                sulawesi_cgs = df_cgs[df_cgs[col].str.contains('Sulawesi', case=False, na=False)]
                print(f"    Sulawesi smelters: {len(sulawesi_cgs)}")
    
    # Show sample data
    print(f"\n📋 SAMPLE CGS DATA (first 3 rows):")
    print(df_cgs.head(3).to_string())
    
except FileNotFoundError:
    print(f"\n❌ CGS dataset not found at: {cgs_file}")
    df_cgs = None
except Exception as e:
    print(f"\n⚠️ Error reading CGS dataset: {str(e)}")
    df_cgs = None

# ============================================================================
# PART 3: GAP ANALYSIS AGAINST REQUIREMENTS
# ============================================================================
print("\n" + "="*100)
print("PART 3: GAP ANALYSIS vs. ESDM REQUIREMENTS")
print("="*100)

requirements = {
    "1️⃣ Jumlah Izin Tambang/Smelter": {
        "target": "±3,000+ entries covering 2016-2026",
        "minerbaone_status": "✅ COMPLETE",
        "minerbaone_data": f"{len(df_permits):,} total permits, {len(df_permits[df_permits['year_issued'].between(2016, 2026)]):,} from 2016-2026",
        "cgs_status": "✅ AVAILABLE" if df_cgs is not None else "❓ CHECK FILE",
        "cgs_data": f"{len(df_cgs):,} smelters" if df_cgs is not None else "Not loaded",
        "recommendation": "✓ Use MinerbaOne as primary source for permit counts\n     ✓ Use CGS for smelter-specific validation"
    },
    
    "2️⃣ Kapasitas Produksi": {
        "target": "Production capacity (ton/year) per facility",
        "minerbaone_status": "❌ NOT AVAILABLE",
        "minerbaone_data": "No capacity column in permits data",
        "cgs_status": "✅ LIKELY AVAILABLE" if df_cgs is not None else "❓ CHECK FILE",
        "cgs_data": "Check capacity columns in CGS dataset" if df_cgs is not None else "Not loaded",
        "recommendation": "⚠ CRITICAL GAP - Merge CGS capacity data with MinerbaOne permits\n     - Match by company name + location\n     - Manual validation needed for accuracy"
    },
    
    "3️⃣ Nilai Investasi": {
        "target": "Investment value (USD/IDR) per facility",
        "minerbaone_status": "❌ NOT AVAILABLE",
        "minerbaone_data": "Not in MinerbaOne API",
        "cgs_status": "🟡 PARTIAL" if df_cgs is not None else "❓ CHECK FILE",
        "cgs_data": "Check investment columns in CGS dataset" if df_cgs is not None else "Not loaded",
        "recommendation": "⚠ CRITICAL GAP - Multiple options:\n     1. Use CGS investment data (if available)\n     2. Use BPS PMDN data (already obtained - 96 rows)\n     3. Manual scraping from BKPM NSWI\n     4. Allocate proportionally by capacity"
    },
    
    "4️⃣ Luas Kawasan (Area)": {
        "target": "Mining/smelter area in hectares",
        "minerbaone_status": "✅ COMPLETE",
        "minerbaone_data": f"{df_permits['luas_ha'].notna().sum():,} permits ({df_permits['luas_ha'].notna().sum()/len(df_permits)*100:.1f}%) have area data\n     Total area: {df_permits['luas_ha'].sum():,.0f} hectares\n     Sulawesi: {df_sulawesi['luas_ha'].sum():,.0f} hectares",
        "cgs_status": "🟡 MAY HAVE",
        "cgs_data": "Check if CGS has land area data",
        "recommendation": "✓ MinerbaOne data sufficient for area coverage\n     ✓ 48.7% coverage (acceptable - focus on IUP/IUPK permits)\n     ✓ IPP permits (51%) are applications, not issued licenses"
    }
}

print("\n")
for req_name, req_data in requirements.items():
    print(f"\n{req_name}")
    print(f"{'='*100}")
    print(f"TARGET: {req_data['target']}")
    print(f"\nMINERBAONE DATA:")
    print(f"  Status: {req_data['minerbaone_status']}")
    print(f"  Data: {req_data['minerbaone_data']}")
    print(f"\nCGS/UMD DATASET:")
    print(f"  Status: {req_data['cgs_status']}")
    print(f"  Data: {req_data['cgs_data']}")
    print(f"\nRECOMMENDATION:")
    for line in req_data['recommendation'].split('\n'):
        print(f"  {line}")

# ============================================================================
# PART 4: FINAL RECOMMENDATIONS
# ============================================================================
print("\n" + "="*100)
print("PART 4: ACTION PLAN & NEXT STEPS")
print("="*100)

print("""
✅ COMPLETED SUCCESSFULLY:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. MinerbaOne full scrape: 8,396 permits (7,722 from 2016-2026)
2. Permit details: Company info, directors, shareholders, permits
3. Location coverage: Nationwide including Sulawesi focus areas
4. Commodity data: Nickel, coal, and 50+ other minerals
5. Area data: 4,092 permits with luas_ha (9M+ hectares total)
6. Nickel in Sulawesi: Identified and tracked

⚠️ CRITICAL GAPS IDENTIFIED:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. KAPASITAS PRODUKSI (Production Capacity)
   - Not available in MinerbaOne API
   - SOLUTION: Extract from CGS dataset + merge with permits
   
2. NILAI INVESTASI (Investment Value)
   - Not available in MinerbaOne API
   - SOLUTION: Use CGS data OR BPS PMDN (already downloaded)

📋 IMMEDIATE NEXT STEPS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 1: Analyze CGS Dataset in Detail [PRIORITY: HIGH]
  ├─ Read all sheets in CGS_Nickel_Smelter_Dataset_V1.xlsx
  ├─ Extract capacity data (ton/year)
  ├─ Extract investment data (USD/IDR)
  ├─ Extract company names and locations
  └─ Export to CSV for merging

STEP 2: Merge MinerbaOne + CGS Data [PRIORITY: HIGH]
  ├─ Match nickel permits from MinerbaOne with CGS smelters
  ├─ Join by: company name + location (fuzzy matching)
  ├─ Add capacity and investment columns to permits data
  └─ Create master dataset: permits + capacity + investment

STEP 3: Fill Investment Gaps with BPS Data [PRIORITY: MEDIUM]
  ├─ Read BPS PMDN data (already downloaded)
  ├─ Allocate provincial investment to specific permits
  ├─ Proportional allocation by capacity or area
  └─ Document methodology clearly

STEP 4: Data Quality & Validation [PRIORITY: MEDIUM]
  ├─ Check for duplicates (same company, different permit types)
  ├─ Validate Sulawesi nickel smelter counts vs. known facilities
  ├─ Cross-reference with industry reports
  └─ Flag low-confidence matches for manual review

STEP 5: Final Dataset Creation [PRIORITY: HIGH]
  ├─ Combine all sources into master CSV
  ├─ Required columns:
  │   - company_name, permit_number, commodity
  │   - province, kabupaten, coordinates (if available)
  │   - capacity_ton_year, investment_usd, area_ha
  │   - operational_status, year_issued
  │   - data_source (minerbaone/cgs/bps)
  │   - confidence_level (high/medium/low)
  └─ Output: data/processed/esdm_master_2016_2026.csv

STEP 6: Create Data Dictionary & Report [PRIORITY: LOW]
  └─ Document all sources, methodology, limitations

💡 ESTIMATED TIME:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Step 1-2: 4-6 hours (CGS analysis + data merging)
- Step 3: 2-3 hours (BPS investment allocation)
- Step 4-5: 3-4 hours (validation + final dataset)
- Step 6: 1-2 hours (documentation)
TOTAL: 10-15 hours of work

🎯 SUCCESS CRITERIA:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Minimum 200+ nickel smelters/mines with full metadata
✓ Capacity data for 70%+ of operational facilities
✓ Investment data for 60%+ of facilities (direct or allocated)
✓ Area coverage for 80%+ of issued permits (IUP/IUPK)
✓ Complete Sulawesi coverage for impact analysis
✓ Date range: 2016-2026 well represented

""")

print("="*100)
print("ANALYSIS COMPLETE - READY FOR NEXT PHASE")
print("="*100)
