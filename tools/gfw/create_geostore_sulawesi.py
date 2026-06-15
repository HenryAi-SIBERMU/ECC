"""
Create Geostore untuk Sulawesi Provinces
Lalu fetch deforestation data

Author: CELIOS
Date: 14 Juni 2026
"""

import requests
import json
import pandas as pd
from pathlib import Path

API_KEY = "21899f40-1f6d-4ff9-93e1-c10d04513984"
BASE = "https://data-api.globalforestwatch.org"

# Approximate bounding boxes untuk Sulawesi provinces
# Format: [min_lng, min_lat, max_lng, max_lat]
SULAWESI_BOUNDARIES = {
    'Sulawesi Utara': {
        'bbox': [123.5, 0.3, 127.0, 5.5],
        'name_en': 'North Sulawesi'
    },
    'Sulawesi Tengah': {
        'bbox': [119.5, -3.5, 124.0, 2.0],
        'name_en': 'Central Sulawesi'
    },
    'Sulawesi Selatan': {
        'bbox': [119.0, -8.0, 122.5, -2.5],
        'name_en': 'South Sulawesi'
    },
    'Sulawesi Tenggara': {
        'bbox': [121.0, -6.0, 124.5, -3.0],
        'name_en': 'Southeast Sulawesi'
    },
    'Gorontalo': {
        'bbox': [121.5, 0.3, 123.5, 1.5],
        'name_en': 'Gorontalo'
    },
    'Sulawesi Barat': {
        'bbox': [118.5, -3.5, 120.0, -0.5],
        'name_en': 'West Sulawesi'
    }
}

def create_geostore(province_name, bbox):
    """
    Create geostore dari bounding box.
    
    Args:
        province_name: Nama provinsi
        bbox: [min_lng, min_lat, max_lng, max_lat]
    
    Returns:
        Geostore UUID atau None
    """
    print(f"\nCreating geostore: {province_name}")
    print(f"BBox: {bbox}")
    
    # Convert bbox to polygon
    min_lng, min_lat, max_lng, max_lat = bbox
    
    geojson = {
        "geojson": {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [min_lng, min_lat],
                    [max_lng, min_lat],
                    [max_lng, max_lat],
                    [min_lng, max_lat],
                    [min_lng, min_lat]
                ]]
            }
        }
    }
    
    try:
        response = requests.post(
            f"{BASE}/geostore/",
            json=geojson,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code in [200, 201]:
            data = response.json()
            # Response: {"data": {"id": "UUID", ...}}
            geostore_id = data.get('data', {}).get('id')
            if geostore_id:
                print(f"✅ Geostore ID: {geostore_id}")
                return geostore_id
            else:
                print(f"⚠️ No ID in response: {data}")
                return None
        else:
            print(f"❌ Failed: {response.text[:300]}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def query_deforestation(geostore_id, province_name):
    """Query tree cover loss via analysis/zonal endpoint"""
    
    print(f"\n{'='*60}")
    print(f"Querying deforestation: {province_name}")
    print(f"Geostore: {geostore_id}")
    print(f"{'='*60}")
    
    endpoint = f"{BASE}/analysis/zonal/{geostore_id}"
    
    params = {
        "sum": ["area__ha"],
        "group_by": ["umd_tree_cover_loss__year"],
        "geostore_origin": "gfw"
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
                
                # Filter 2016-2023
                if 'umd_tree_cover_loss__year' in df.columns:
                    # Convert year to int
                    df['umd_tree_cover_loss__year'] = pd.to_numeric(df['umd_tree_cover_loss__year'], errors='coerce')
                    df = df[df['umd_tree_cover_loss__year'].between(2016, 2023)]
                    df['province'] = province_name
                    df.rename(columns={
                        'umd_tree_cover_loss__year': 'year',
                        'area__ha': 'deforestation_ha'
                    }, inplace=True)
                    
                    print(f"✅ Success! Rows: {len(df)}")
                    print(df)
                    return df
                else:
                    print("⚠️ No year column in response")
                    print(df.head())
                    return pd.DataFrame()
            else:
                print(f"⚠️ No 'data' in response")
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
    print("GFW DEFORESTATION DATA FETCH - GEOSTORE APPROACH")
    print("="*70)
    print(f"API Key: {API_KEY[:20]}...")
    print(f"Provinces: {len(SULAWESI_BOUNDARIES)}")
    
    all_data = []
    geostore_mapping = {}
    
    # Step 1: Create geostores
    print("\n" + "="*70)
    print("STEP 1: Creating Geostores")
    print("="*70)
    
    for province_name, info in SULAWESI_BOUNDARIES.items():
        geostore_id = create_geostore(province_name, info['bbox'])
        if geostore_id:
            geostore_mapping[province_name] = geostore_id
    
    print(f"\n✅ Created {len(geostore_mapping)} geostores")
    
    # Step 2: Query deforestation for each province
    print("\n" + "="*70)
    print("STEP 2: Querying Deforestation Data")
    print("="*70)
    
    for province_name, geostore_id in geostore_mapping.items():
        df = query_deforestation(geostore_id, province_name)
        if not df.empty:
            all_data.append(df)
    
    # Step 3: Consolidate
    if all_data:
        print("\n" + "="*70)
        print("STEP 3: Consolidation")
        print("="*70)
        
        final_df = pd.concat(all_data, ignore_index=True)
        
        print(f"Total rows: {len(final_df)}")
        print(f"Provinces: {final_df['province'].nunique()}")
        print(f"Years: {sorted(final_df['year'].unique())}")
        
        # Save
        output_dir = Path("data/raw/gfw")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / "sulawesi_deforestation_2016_2023_gfw.csv"
        final_df.to_csv(output_file, index=False)
        
        print(f"\n✅ Saved to: {output_file}")
        print("\nSample data:")
        print(final_df.head(20))
        
        # Save geostore mapping
        mapping_file = output_dir / "sulawesi_geostore_mapping.json"
        with open(mapping_file, 'w') as f:
            json.dump(geostore_mapping, f, indent=2)
        print(f"\n✅ Geostore mapping saved to: {mapping_file}")
        
    else:
        print("\n❌ No data collected")

if __name__ == "__main__":
    main()
