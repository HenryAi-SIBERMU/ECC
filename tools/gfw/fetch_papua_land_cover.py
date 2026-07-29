import requests
import pandas as pd
from pathlib import Path
import time
from datetime import datetime

API_KEY = "21899f40-1f6d-4ff9-93e1-c10d04513984"
BASE = "https://data-api.globalforestwatch.org"
PRODUCTION_BASE = "https://production-api.globalforestwatch.org"

PAPUA_REGIONS = {
    'Papua': 24,
    'Papua Barat': 15
}

INDICATORS = [
    {
        'name': 'Tutupan Lahan (ESA 2015)',
        'layer': 'esa_land_cover_2015__class',
        'group_by': ['umd_tree_cover_loss__year', 'esa_land_cover_2015__class']
    },
    {
        'name': 'Tipe Konsesi (Plantations)',
        'layer': 'gfw_plantations__type',
        'group_by': ['umd_tree_cover_loss__year', 'gfw_plantations__type']
    }
]

def get_admin_geostore(admin_id):
    endpoint = f"{PRODUCTION_BASE}/v2/geostore/admin/IDN/{admin_id}"
    try:
        res = requests.get(endpoint, timeout=30)
        if res.status_code == 200:
            return res.json().get('data', {}).get('id')
    except Exception:
        pass
    return None

def fetch_indicator(geostore_id, group_by_layers):
    endpoint = f"{BASE}/analysis/zonal/{geostore_id}"
    params = [('sum', 'area__ha')]
    for layer in group_by_layers:
        params.append(('group_by', layer))
    params.append(('geostore_origin', 'gfw'))
    headers = {"x-api-key": API_KEY}
    try:
        res = requests.get(endpoint, params=params, headers=headers, timeout=120)
        if res.status_code == 200:
            data = res.json().get('data', [])
            if data:
                return pd.DataFrame(data)
    except Exception as e:
        print(f"Error fetching {group_by_layers}: {e}")
    return pd.DataFrame()

def main():
    print("Fetching Land Cover and Concession Data for Papua...")
    all_data = {
        'Tutupan Lahan (ESA 2015)': [],
        'Tipe Konsesi (Plantations)': []
    }
    
    for province, admin_id in PAPUA_REGIONS.items():
        geostore_id = get_admin_geostore(admin_id)
        if not geostore_id: continue
            
        print(f"\nProcessing {province} (IDN.{admin_id})")
        for ind in INDICATORS:
            print(f"  Fetching {ind['name']}...")
            df = fetch_indicator(geostore_id, ind['group_by'])
            if not df.empty and 'umd_tree_cover_loss__year' in df.columns:
                df['year'] = pd.to_numeric(df['umd_tree_cover_loss__year'], errors='coerce')
                df = df[(df['year'] >= 2016) & (df['year'] <= 2026)]
                
                category_col = ind['group_by'][1]
                if category_col in df.columns:
                    # Filter out NaN/null categories (meaning not in a specific land cover / concession)
                    df = df[df[category_col].notna()]
                    invalid = ['false', '0', 'unknown', 'none', 'nan', 'null']
                    df = df[~df[category_col].astype(str).str.lower().isin(invalid)]
                    
                    # Rename category column for clarity
                    df = df.rename(columns={category_col: 'kategori', 'area__ha': 'loss_area_ha'})
                    df['province'] = province
                    all_data[ind['name']].append(df[['year', 'province', 'kategori', 'loss_area_ha']])
                    print(f"    -> Found {len(df)} records.")
            time.sleep(1)

    # Save to Excel
    output_dir = Path("../../data/processed/gfw")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "Papua_Deforestation_by_LandCover_Concession.xlsx"
    
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        for sheet_name, df_list in all_data.items():
            if df_list:
                df_combined = pd.concat(df_list, ignore_index=True)
                # Pivot table to make it readable: rows=year, cols=kategori
                # Group by year and kategori first in case of multiple provinces
                df_agg = df_combined.groupby(['year', 'kategori'])['loss_area_ha'].sum().reset_index()
                pivot_df = df_agg.pivot(index='year', columns='kategori', values='loss_area_ha').reset_index()
                pivot_df.columns.name = None
                pivot_df.rename(columns=lambda x: f"{x} (ha)" if x != 'year' else x, inplace=True)
                
                # Excel Sheet name rules (max 31 chars)
                safe_sheet_name = sheet_name[:31].replace('/', '_').replace('\\', '_')
                pivot_df.to_excel(writer, sheet_name=f"Total {safe_sheet_name}", index=False)
                
                # Also save raw tidy data for researcher
                df_combined.to_excel(writer, sheet_name=f"Raw {safe_sheet_name[:20]}", index=False)
                print(f"Saved sheet: {safe_sheet_name}")

    print(f"\nSUCCESS! Excel file created at: {output_file.resolve()}")

if __name__ == "__main__":
    main()
