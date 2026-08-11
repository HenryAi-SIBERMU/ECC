"""
Merge Manual GFW Driver Downloads into V3 Driver Dataset
=========================================================

Combines:
1. API Fetch V3 (Gorontalo, Sulbar, Sulteng, Sultra)
2. Manual GFW Downloads (Sulawesi Selatan, Sulawesi Utara)

Maps manual driver taxonomy (8 classes) -> Beta API taxonomy (4 classes) to ensure seamless 6-province dataset.
"""

import pandas as pd
from pathlib import Path

# Paths
API_V3_FILE = Path("data/raw/klhk_gfw/land_api_fetch/loss_by_driver_sulawesi_2001_2025_v3.csv")
MANUAL_SULSEL = Path("tools/gfw/manual/extracted/sulsel/treecover_loss__ha.csv")
MANUAL_SULUT = Path("tools/gfw/manual/extracted/sulut/treecover_loss__ha.csv")
OUTPUT_FILE = Path("data/raw/klhk_gfw/land_api_fetch/loss_by_driver_sulawesi_2001_2025_v3.csv")

# Category Mapping (Fine-grained -> Beta API 4-class)
DRIVER_MAP = {
    'Permanent agriculture': 'Commodity driven deforestation',
    'Hard commodities': 'Commodity driven deforestation',
    'Settlements & Infrastructure': 'Commodity driven deforestation',
    'Logging': 'Forestry',
    'Shifting cultivation': 'Shifting agriculture',
    'Wildfire': 'Unknown',
    'Other natural disturbances': 'Unknown',
    'Unknown': 'Unknown'
}

def process_manual_file(file_path, province_name):
    df = pd.read_csv(file_path)
    
    # Map driver names
    df['driver'] = df['wri_google_tree_cover_loss_drivers__driver'].map(DRIVER_MAP).fillna('Unknown')
    df['year'] = df['umd_tree_cover_loss__year']
    df['area_ha'] = df['umd_tree_cover_loss__ha']
    df['co2_emissions_mg'] = df['gfw_gross_emissions_co2e_all_gases__Mg']
    df['province'] = province_name
    df['is_primary'] = None  # Neutral filler for primary forest flag
    
    # Group by province, year, driver to match API V3 structure
    grouped = df.groupby(['province', 'year', 'driver'], as_index=False).agg({
        'area_ha': 'sum',
        'co2_emissions_mg': 'sum'
    })
    grouped['is_primary'] = None
    return grouped

def main():
    print("🚀 Merging API V3 + Manual Downloads for Sulsel & Sulut...")
    
    # 1. Load API V3 (4 provinces)
    df_api = pd.read_csv(API_V3_FILE)
    print(f"  API V3 existing rows: {len(df_api)} for {df_api['province'].unique().tolist()}")
    
    # 2. Process Manual Sulsel & Sulut
    df_sulsel = process_manual_file(MANUAL_SULSEL, "Sulawesi Selatan")
    print(f"  Manual Sulsel processed: {len(df_sulsel)} rows")
    
    df_sulut = process_manual_file(MANUAL_SULUT, "Sulawesi Utara")
    print(f"  Manual Sulut processed: {len(df_sulut)} rows")
    
    # 3. Filter out any existing Sulsel/Sulut from API (if any) and append manual ones
    df_api_clean = df_api[~df_api['province'].isin(['Sulawesi Selatan', 'Sulawesi Utara'])]
    
    combined = pd.concat([df_api_clean, df_sulsel, df_sulut], ignore_index=True)
    combined.sort_values(by=['province', 'year', 'driver'], inplace=True)
    
    # 4. Save merged CSV
    combined.to_csv(OUTPUT_FILE, index=False)
    
    print("\n✅ SUCCESS! Complete 6-Province V3 Driver Data Saved!")
    print(f"  Total Rows: {len(combined)}")
    print(f"  Provinces ({len(combined['province'].unique())}): {combined['province'].unique().tolist()}")
    print(f"  File: {OUTPUT_FILE}")
    
    print("\n📊 Summary by Province (Total Driver Loss Area):")
    summary = combined.groupby('province')['area_ha'].sum()
    for prov, area in summary.items():
        print(f"  - {prov}: {area:,.2f} ha")

if __name__ == "__main__":
    main()
