import requests
import pandas as pd
import json
from pathlib import Path
import time
import os
import sys

# Force UTF-8 encoding for Windows console (fixes emoji crashes)
sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "21899f40-1f6d-4ff9-93e1-c10d04513984"
BASE_DATA = "https://data-api.globalforestwatch.org"

# Target provinces
PAPUA_PROVINCES = [
    'Papua',
    'Papua Barat',
    'Papua Selatan',
    'Papua Tengah',
    'Papua Pegunungan',
    'Papua Barat Daya'
]

def get_papua_features(geojson_path):
    """Extract features for the 6 Papua provinces from GeoJSON."""
    with open(geojson_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    papua_features = {}
    for feat in data['features']:
        prop = feat.get('properties', {})
        name = prop.get('PROVINSI', '')
        
        # Check against our target list
        for target in PAPUA_PROVINCES:
            if target.lower() == str(name).lower():
                papua_features[target] = feat
                break
                
    return papua_features

def create_geostore(province_name, feature):
    """Create geostore from a GeoJSON feature."""
    print(f"\nCreating geostore for: {province_name}")
    
    payload = {
        "geojson": {
            "type": "Feature",
            "geometry": feature['geometry']
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_DATA}/geostore/",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code in [200, 201]:
            data = response.json()
            geostore_id = data.get('data', {}).get('id')
            if geostore_id:
                print(f"[OK] Geostore ID: {geostore_id}")
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

def query_zonal(geostore_id, sum_layers, group_by_layers=None, filters=None):
    """Universal zonal statistics query."""
    endpoint = f"{BASE_DATA}/analysis/zonal/{geostore_id}"
    
    params = {
        "sum": sum_layers,
        "geostore_origin": "gfw"
    }
    
    if group_by_layers:
        params["group_by"] = group_by_layers
    if filters:
        params["filters"] = filters
        
    headers = {"x-api-key": API_KEY}
    
    try:
        response = requests.get(endpoint, params=params, headers=headers, timeout=120)
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and len(data['data']) > 0:
                return pd.DataFrame(data['data'])
            else:
                return None
        else:
            print(f"  ❌ Status {response.status_code}")
            return None
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return None

def fetch_1_tree_cover_loss(province, geostore_id):
    print(f"  [1/10] Tree Cover Loss...")
    df = query_zonal(geostore_id, ["area__ha"], ["umd_tree_cover_loss__year"])
    if df is not None and 'umd_tree_cover_loss__year' in df.columns:
        df = df.rename(columns={'umd_tree_cover_loss__year': 'year', 'area__ha': 'tree_cover_loss_ha'})
        df['province'] = province
        df['year'] = pd.to_numeric(df['year'], errors='coerce')
        return df
    return pd.DataFrame()

def fetch_2_primary_forest_loss(province, geostore_id):
    print(f"  [2/10] Primary Forest Loss...")
    df = query_zonal(geostore_id, ["area__ha"], ["umd_tree_cover_loss__year"], [{"layer": "is__umd_regional_primary_forest_2001", "value": "true"}])
    if df is not None and 'umd_tree_cover_loss__year' in df.columns:
        df = df.rename(columns={'umd_tree_cover_loss__year': 'year', 'area__ha': 'primary_forest_loss_ha'})
        df['province'] = province
        df['year'] = pd.to_numeric(df['year'], errors='coerce')
        return df
    return pd.DataFrame()

def fetch_3_loss_by_driver(province, geostore_id):
    print(f"  [3/10] Forest Loss by Driver...")
    df = query_zonal(geostore_id, ["area__ha"], ["tsc_tree_cover_loss_drivers__type", "umd_tree_cover_loss__year"])
    if df is not None:
        df['province'] = province
        if 'umd_tree_cover_loss__year' in df.columns:
            df['year'] = pd.to_numeric(df['umd_tree_cover_loss__year'], errors='coerce')
        return df
    return pd.DataFrame()

def fetch_4_primary_loss_by_driver(province, geostore_id):
    print(f"  [4/10] Primary Forest Loss by Driver...")
    df = query_zonal(geostore_id, ["area__ha"], ["tsc_tree_cover_loss_drivers__type", "umd_tree_cover_loss__year"], [{"layer": "is__umd_regional_primary_forest_2001", "value": "true"}])
    if df is not None:
        df['province'] = province
        if 'umd_tree_cover_loss__year' in df.columns:
            df['year'] = pd.to_numeric(df['umd_tree_cover_loss__year'], errors='coerce')
        return df
    return pd.DataFrame()

def fetch_5_co2_emissions(province, geostore_id):
    print(f"  [5/10] CO2 Emissions...")
    df = query_zonal(geostore_id, ["whrc_aboveground_co2_emissions__Mg"], ["umd_tree_cover_loss__year"])
    if df is not None and 'umd_tree_cover_loss__year' in df.columns:
        df = df.rename(columns={'umd_tree_cover_loss__year': 'year', 'whrc_aboveground_co2_emissions__Mg': 'co2_emissions_mg'})
        df['province'] = province
        df['year'] = pd.to_numeric(df['year'], errors='coerce')
        return df
    return pd.DataFrame()

def fetch_6_tree_cover_by_category(province, geostore_id):
    print(f"  [6/10] Tree Cover by Category...")
    categories = ["wdpa_protected_areas__iucn_cat", "gfw_plantations__type", "is__gfw_mining", "is__gfw_peatlands", "is__gfw_oil_palm"]
    all_data = []
    for cat in categories:
        df = query_zonal(geostore_id, ["area__ha"], [cat])
        if df is not None:
            df['category_type'] = cat
            df['province'] = province
            all_data.append(df)
        time.sleep(0.5)
    return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()

def fetch_7_loss_in_protected_areas(province, geostore_id):
    print(f"  [7/10] Loss in Protected Areas...")
    df = query_zonal(geostore_id, ["area__ha"], ["umd_tree_cover_loss__year", "wdpa_protected_areas__iucn_cat"])
    if df is not None:
        df['province'] = province
        if 'umd_tree_cover_loss__year' in df.columns:
            df['year'] = pd.to_numeric(df['umd_tree_cover_loss__year'], errors='coerce')
        return df
    return pd.DataFrame()

def fetch_8_tree_cover_gain(province, geostore_id):
    print(f"  [8/10] Tree Cover Gain...")
    df = query_zonal(geostore_id, ["area__ha"], ["is__umd_tree_cover_gain"])
    if df is not None:
        df['province'] = province
        return df
    return pd.DataFrame()

def fetch_9_loss_by_land_cover(province, geostore_id):
    print(f"  [9/10] Loss by Land Cover Type...")
    df = query_zonal(geostore_id, ["area__ha"], ["umd_tree_cover_loss__year", "esa_land_cover_2015__class"])
    if df is not None:
        df['province'] = province
        if 'umd_tree_cover_loss__year' in df.columns:
            df['year'] = pd.to_numeric(df['umd_tree_cover_loss__year'], errors='coerce')
        return df
    return pd.DataFrame()

def fetch_10_tree_cover_extent(province, geostore_id):
    print(f"  [10/10] Tree Cover Extent 2000...")
    df = query_zonal(geostore_id, ["area__ha"], ["umd_tree_cover_density_2000__30"])
    if df is not None:
        df['province'] = province
        return df
    return pd.DataFrame()

def fetch_all_for_province(province_name, geostore_id):
    datasets = {}
    datasets['tree_cover_loss'] = fetch_1_tree_cover_loss(province_name, geostore_id)
    time.sleep(1)
    datasets['primary_forest_loss'] = fetch_2_primary_forest_loss(province_name, geostore_id)
    time.sleep(1)
    datasets['loss_by_driver'] = fetch_3_loss_by_driver(province_name, geostore_id)
    time.sleep(1)
    datasets['primary_loss_by_driver'] = fetch_4_primary_loss_by_driver(province_name, geostore_id)
    time.sleep(1)
    datasets['co2_emissions'] = fetch_5_co2_emissions(province_name, geostore_id)
    time.sleep(1)
    datasets['tree_cover_by_category'] = fetch_6_tree_cover_by_category(province_name, geostore_id)
    time.sleep(1)
    datasets['loss_in_protected_areas'] = fetch_7_loss_in_protected_areas(province_name, geostore_id)
    time.sleep(1)
    datasets['tree_cover_gain'] = fetch_8_tree_cover_gain(province_name, geostore_id)
    time.sleep(1)
    datasets['loss_by_land_cover'] = fetch_9_loss_by_land_cover(province_name, geostore_id)
    time.sleep(1)
    datasets['tree_cover_extent'] = fetch_10_tree_cover_extent(province_name, geostore_id)
    return datasets

def main():
    print("="*60)
    print("FETCHING 6 PAPUA PROVINCES DATA")
    print("="*60)
    
    geojson_path = Path("indonesia-geojson-topojson-maps-with-38-provinces/GeoJSON/indonesia-38-provinces.geojson")
    features = get_papua_features(geojson_path)
    print(f"Found {len(features)} provinces in GeoJSON.")
    
    geostores = {}
    for prov_name, feat in features.items():
        gid = create_geostore(prov_name, feat)
        if gid:
            geostores[prov_name] = gid
        time.sleep(1)
        
    output_dir = Path("../../../data/raw/klhk_gfw/mega_fetch_papua")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_dir / "papua_geostore_mapping.json", 'w') as f:
        json.dump(geostores, f, indent=2)
        
    all_datasets = {k: [] for k in [
        'tree_cover_loss', 'primary_forest_loss', 'loss_by_driver', 'primary_loss_by_driver',
        'co2_emissions', 'tree_cover_by_category', 'loss_in_protected_areas', 
        'tree_cover_gain', 'loss_by_land_cover', 'tree_cover_extent'
    ]}
    
    for prov_name, gid in geostores.items():
        print(f"\n[{prov_name}] Fetching datasets...")
        prov_data = fetch_all_for_province(prov_name, gid)
        for ds_name, df in prov_data.items():
            if not df.empty:
                all_datasets[ds_name].append(df)
                
    print("\nSaving files...")
    for ds_name, dfs in all_datasets.items():
        if dfs:
            combined = pd.concat(dfs, ignore_index=True)
            out_file = output_dir / f"{ds_name}_papua_6_prov.csv"
            combined.to_csv(out_file, index=False)
            print(f"✅ Saved {out_file.name} ({len(combined)} rows)")
            
    print("\nDONE!")

if __name__ == '__main__':
    main()
