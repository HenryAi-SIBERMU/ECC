import requests
import pandas as pd
import json
from pathlib import Path
import time

API_KEY = "21899f40-1f6d-4ff9-93e1-c10d04513984"
BASE = "https://data-api.globalforestwatch.org"
PRODUCTION_BASE = "https://production-api.globalforestwatch.org"

# GADM 3.6 IDs for Papua Region
PAPUA_REGIONS = {
    'Papua': 24,         # IDN.24
    'Papua Barat': 15    # IDN.15
}

def get_admin_geostore(admin_id):
    """Fetch geostore ID using admin API."""
    endpoint = f"{PRODUCTION_BASE}/v2/geostore/admin/IDN/{admin_id}"
    print(f"Fetching geostore for IDN.{admin_id}...")
    try:
        res = requests.get(endpoint, timeout=30)
        if res.status_code == 200:
            data = res.json()
            geostore_id = data.get('data', {}).get('id')
            print(f"Found Geostore ID: {geostore_id}")
            return geostore_id
        else:
            print(f"Failed to get geostore: {res.status_code} - {res.text[:100]}")
    except Exception as e:
        print(f"Error: {e}")
    return None

def fetch_deforestation(province, geostore_id):
    """Fetch deforestation (tree cover loss) for a geostore from 2016 to 2026."""
    print(f"\nFetching deforestation data for {province}...")
    endpoint = f"{BASE}/analysis/zonal/{geostore_id}"
    
    params = [
        ('sum', 'area__ha'),
        ('group_by', 'umd_tree_cover_loss__year'),
        ('geostore_origin', 'gfw')
    ]
    
    headers = {"x-api-key": API_KEY}
    
    try:
        res = requests.get(endpoint, params=params, headers=headers, timeout=120)
        if res.status_code == 200:
            data = res.json()
            if 'data' in data and len(data['data']) > 0:
                df = pd.DataFrame(data['data'])
                if 'umd_tree_cover_loss__year' in df.columns:
                    df['year'] = pd.to_numeric(df['umd_tree_cover_loss__year'], errors='coerce')
                    df = df[(df['year'] >= 2016) & (df['year'] <= 2026)]
                    df['province'] = province
                    df = df.rename(columns={'area__ha': 'deforestation_ha'})
                    df = df[['province', 'year', 'deforestation_ha']]
                    print(f"Fetched {len(df)} records for {province}")
                    return df
            print(f"No matching data found.")
            return None
        else:
            print(f"API Error: {res.status_code}")
            return None
    except Exception as e:
        print(f"Error during fetch: {e}")
        return None

def main():
    print("="*60)
    print("FETCHING PAPUA DEFORESTATION DATA (2016-2026)")
    print("="*60)
    
    all_data = []
    
    for province, admin_id in PAPUA_REGIONS.items():
        geostore_id = get_admin_geostore(admin_id)
        if geostore_id:
            df = fetch_deforestation(province, geostore_id)
            if df is not None and not df.empty:
                all_data.append(df)
            time.sleep(1)  # Respect rate limit
            
    if all_data:
        # Combine all data
        final_df = pd.concat(all_data, ignore_index=True)
        final_df = final_df.sort_values(by=['province', 'year']).reset_index(drop=True)
        
        # 1. Save RAW Data
        raw_dir = Path("../../data/raw/gfw")
        raw_dir.mkdir(parents=True, exist_ok=True)
        raw_file = raw_dir / "papua_deforestation_raw_2016_2026.csv"
        final_df.to_csv(raw_file, index=False)
        print(f"\nRAW Data saved to {raw_file}")
        
        # 2. Process Data (e.g. aggregate all Papua regions into one if needed, or just clean up)
        # For clean data, we will just ensure proper types, maybe sum the total for "Seluruh Papua"
        processed_dir = Path("../../data/processed/gfw")
        processed_dir.mkdir(parents=True, exist_ok=True)
        
        # Add a total row per year
        totals = final_df.groupby('year')['deforestation_ha'].sum().reset_index()
        totals['province'] = 'Total Seluruh Papua'
        totals = totals[['province', 'year', 'deforestation_ha']]
        
        processed_df = pd.concat([final_df, totals], ignore_index=True)
        processed_df = processed_df.sort_values(by=['year', 'province']).reset_index(drop=True)
        
        clean_file = processed_dir / "papua_deforestation_clean_2016_2026.csv"
        processed_df.to_csv(clean_file, index=False)
        print(f"PROCESSED Data saved to {clean_file}")
        
        print("\nSample Data:")
        print(processed_df.head(10))
    else:
        print("\nFailed to fetch any data.")

if __name__ == "__main__":
    main()
