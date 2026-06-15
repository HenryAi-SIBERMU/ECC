"""
Fetch Sulawesi Deforestation - FINAL VERSION
Using admin boundary AOI approach

Author: CELIOS Research
Date: 14 Juni 2026
"""

import requests
import pandas as pd
from pathlib import Path
import json

API_KEY = "21899f40-1f6d-4ff9-93e1-c10d04513984"
BASE = "https://data-api.globalforestwatch.org"

# Sulawesi provinces with admin codes
SULAWESI_PROVINCES = {
    'Sulawesi Utara': {'admin_code': '31', 'bps_code': '71'},
    'Sulawesi Tengah': {'admin_code': '29', 'bps_code': '72'},
    'Sulawesi Selatan': {'admin_code': '30', 'bps_code': '73'},
    'Sulawesi Tenggara': {'admin_code': '32', 'bps_code': '74'},
    'Gorontalo': {'admin_code': '11', 'bps_code': '75'},
    'Sulawesi Barat': {'admin_code': '33', 'bps_code': '76'}
}

def fetch_province_data(province_name, admin_code):
    """Fetch tree cover loss for one province using download_by_aoi"""
    
    print(f"\n{'='*60}")
    print(f"Fetching: {province_name} (admin code: {admin_code})")
    print(f"{'='*60}")
    
    # SQL query
    sql = """
    SELECT 
        umd_tree_cover_loss__year as year,
        SUM(area__ha) as deforestation_ha
    FROM data
    WHERE umd_tree_cover_loss__year >= 2016 
      AND umd_tree_cover_loss__year <= 2023
    GROUP BY umd_tree_cover_loss__year
    ORDER BY umd_tree_cover_loss__year
    """
    
    # AOI definition - admin boundary
    aoi = json.dumps({
        "type": "admin",
        "country": "IDN",
        "region": admin_code
    })
    
    endpoint = f"{BASE}/dataset/umd_tree_cover_loss/latest/download_by_aoi/json"
    
    params = {
        "sql": sql,
        "aoi": aoi
    }
    
    headers = {
        "x-api-key": API_KEY
    }
    
    try:
        response = requests.get(endpoint, params=params, headers=headers, timeout=120)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if 'data' in data:
                df = pd.DataFrame(data['data'])
                df['province'] = province_name
                df['admin_code'] = admin_code
                print(f"✅ Success! Rows: {len(df)}")
                print(df)
                return df
            else:
                print(f"⚠️ No 'data' key in response")
                print(response.text[:500])
                return pd.DataFrame()
        else:
            print(f"❌ Failed: {response.text[:500]}")
            return pd.DataFrame()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return pd.DataFrame()

def main():
    print("\n" + "="*70)
    print("FETCHING SULAWESI DEFORESTATION DATA - FINAL VERSION")
    print("="*70)
    print(f"API Key: {API_KEY[:20]}...")
    print(f"Provinces: {len(SULAWESI_PROVINCES)}")
    print(f"Years: 2016-2023 (8 years)")
    
    all_data = []
    
    for province_name, info in SULAWESI_PROVINCES.items():
        df = fetch_province_data(province_name, info['admin_code'])
        if not df.empty:
            all_data.append(df)
    
    if all_data:
        # Consolidate
        final_df = pd.concat(all_data, ignore_index=True)
        
        print("\n" + "="*70)
        print("CONSOLIDATION COMPLETE")
        print("="*70)
        print(f"Total rows: {len(final_df)}")
        print(f"Provinces: {final_df['province'].nunique()}")
        print(f"Years: {sorted(final_df['year'].unique())}")
        
        # Save
        output_dir = Path("data/raw/gfw")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / "sulawesi_deforestation_2016_2023.csv"
        final_df.to_csv(output_file, index=False)
        
        print(f"\n✅ Saved to: {output_file}")
        print("\nSample data:")
        print(final_df.head(10))
        
    else:
        print("\n❌ No data collected")

if __name__ == "__main__":
    main()
