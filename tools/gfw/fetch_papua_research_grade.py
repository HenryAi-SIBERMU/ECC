import requests
import pandas as pd
from pathlib import Path
import time
from datetime import datetime

API_KEY = "21899f40-1f6d-4ff9-93e1-c10d04513984"
BASE = "https://data-api.globalforestwatch.org"
PRODUCTION_BASE = "https://production-api.globalforestwatch.org"

PAPUA_REGIONS = {
    'Papua': 24,         # IDN.24
    'Papua Barat': 15    # IDN.15
}

# Define the indicators to fetch
INDICATORS = [
    {
        'name': 'Total Deforestation',
        'sum': 'area__ha',
        'unit': 'ha',
        'group_by': ['umd_tree_cover_loss__year']
    },
    {
        'name': 'Primary Forest Loss',
        'sum': 'area__ha',
        'unit': 'ha',
        'group_by': ['umd_tree_cover_loss__year', 'is__umd_regional_primary_forest_2001']
    },
    {
        'name': 'Loss in Protected Areas',
        'sum': 'area__ha',
        'unit': 'ha',
        'group_by': ['umd_tree_cover_loss__year', 'wdpa_protected_areas__iucn_cat']
    },
    {
        'name': 'CO2 Emissions from Deforestation',
        'sum': 'whrc_aboveground_co2_emissions__Mg',
        'unit': 'Mg_CO2',
        'group_by': ['umd_tree_cover_loss__year']
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

def fetch_indicator(geostore_id, group_by_layers, sum_layer='area__ha'):
    endpoint = f"{BASE}/analysis/zonal/{geostore_id}"
    
    params = [('sum', sum_layer)]
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
    print("Fetching Research-Grade Papua Deforestation Data...")
    
    all_data = []
    
    for province, admin_id in PAPUA_REGIONS.items():
        print(f"\nProcessing {province} (IDN.{admin_id})")
        geostore_id = get_admin_geostore(admin_id)
        
        if not geostore_id:
            print(f"Failed to get geostore for {province}")
            continue
            
        print(f"Geostore UUID: {geostore_id}")
        
        for ind in INDICATORS:
            print(f"  Fetching {ind['name']}...")
            df = fetch_indicator(geostore_id, ind['group_by'], ind['sum'])
            
            if not df.empty and 'umd_tree_cover_loss__year' in df.columns:
                # Convert year to numeric and filter 2016-2026
                df['year'] = pd.to_numeric(df['umd_tree_cover_loss__year'], errors='coerce')
                df = df[(df['year'] >= 2016) & (df['year'] <= 2026)]
                
                # Exclude rows where the secondary grouping layer is False or 0 (meaning it didn't happen in that layer)
                if len(ind['group_by']) > 1:
                    secondary_layer = ind['group_by'][1]
                    if secondary_layer in df.columns:
                        df = df[df[secondary_layer].notna()]
                        if df[secondary_layer].dtype == bool:
                            df = df[df[secondary_layer] == True]
                        elif df[secondary_layer].dtype in [int, float]:
                            df = df[df[secondary_layer] > 0]
                        else:
                            # Handle string values like 'true', 'false', 'Unknown'
                            if 'primary_forest' in secondary_layer:
                                df = df[df[secondary_layer].astype(str).str.lower() == 'true']
                            elif 'protected_areas' in secondary_layer:
                                # For protected areas, keep everything that is a valid IUCN cat (exclude Unknown/NaN/False)
                                invalid = ['false', '0', 'unknown', 'none', 'nan', 'null', 'not applicable']
                                df = df[~df[secondary_layer].astype(str).str.lower().isin(invalid)]
                
                # Aggregate by year in case the secondary layer split it into multiple rows (e.g. multiple IUCN categories)
                df_agg = df.groupby('year')[ind['sum']].sum().reset_index()
                
                # Add technical validation metadata
                df_agg['province'] = province
                df_agg['gadm_admin_code'] = f"IDN.{admin_id}"
                df_agg['gfw_geostore_id'] = geostore_id
                # Append unit to indicator name for clarity
                df_agg['indicator_name'] = f"{ind['name']} ({ind['unit']})"
                df_agg['gfw_api_layers_used'] = ", ".join(ind['group_by'])
                df_agg['data_source'] = "GFW Hansen et al. (2013)"
                
                df_agg = df_agg.rename(columns={ind['sum']: 'value'})
                all_data.append(df_agg)
                print(f"    -> Found {len(df_agg)} yearly records.")
            else:
                print(f"    -> No data found.")
            time.sleep(1) # Rate limit

    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        
        # Reorder columns for researcher
        cols = [
            'province', 'gadm_admin_code', 'year', 'indicator_name', 'value',
            'gfw_geostore_id', 'gfw_api_layers_used', 'data_source'
        ]
        final_df = final_df[cols]
        final_df = final_df.sort_values(by=['province', 'indicator_name', 'year'])
        
        output_dir = Path("../../data/processed/gfw")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / "papua_deforestation_research_grade_2016_2026.csv"
        
        final_df.to_csv(output_file, index=False)
        print(f"\nSUCCESS! Research-grade data saved to: {output_file.resolve()}")
    else:
        print("\nFailed to extract data.")

if __name__ == "__main__":
    main()
