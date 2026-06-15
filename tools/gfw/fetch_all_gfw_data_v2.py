"""
GFW MEGA DATA FETCH V2 - Corrected Layer Names
================================================

Fetch data GFW menggunakan layer names yang VALID berdasarkan API documentation.
Layer names disesuaikan dari error messages dan API docs.

Author: CELIOS Research
Date: 14 Juni 2026
"""

import requests
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import time

API_KEY = "21899f40-1f6d-4ff9-93e1-c10d04513984"
BASE = "https://data-api.globalforestwatch.org"

# Load geostore mapping
GEOSTORE_FILE = Path("data/raw/klhk_gfw/sulawesi_geostore_mapping.json")
with open(GEOSTORE_FILE) as f:
    GEOSTORE_MAPPING = json.load(f)

print(f"Loaded {len(GEOSTORE_MAPPING)} geostores")


def query_zonal(geostore_id, sum_layers, group_by_layers=None, filters=None):
    """Universal zonal statistics query."""
    endpoint = f"{BASE}/analysis/zonal/{geostore_id}"
    
    # Build params
    params_list = []
    for layer in sum_layers:
        params_list.append(('sum', layer))
    
    if group_by_layers:
        for layer in group_by_layers:
            params_list.append(('group_by', layer))
    
    if filters:
        for f in filters:
            filter_str = json.dumps(f)
            params_list.append(('filters', filter_str))
    
    params_list.append(('geostore_origin', 'gfw'))
    
    headers = {"x-api-key": API_KEY}
    
    try:
        response = requests.get(endpoint, params=params_list, headers=headers, timeout=120)
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and len(data['data']) > 0:
                return pd.DataFrame(data['data'])
            else:
                print(f"  ⚠️ No data in response")
                return None
        else:
            print(f"  ❌ Status {response.status_code}: {response.text[:300]}")
            return None
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return None


def fetch_1_tree_cover_loss(province, geostore_id):
    """1. Tree Cover Loss (Total) - WORKING"""
    print(f"\n[1/7] Tree Cover Loss...")
    
    df = query_zonal(
        geostore_id,
        sum_layers=["area__ha"],
        group_by_layers=["umd_tree_cover_loss__year"]
    )
    
    if df is not None and 'umd_tree_cover_loss__year' in df.columns:
        df = df.rename(columns={
            'umd_tree_cover_loss__year': 'year',
            'area__ha': 'tree_cover_loss_ha'
        })
        df['province'] = province
        df['year'] = pd.to_numeric(df['year'], errors='coerce')
        return df
    
    return pd.DataFrame()


def fetch_2_primary_forest_loss(province, geostore_id):
    """2. Primary Forest Loss - Using correct filter syntax"""
    print(f"[2/7] Primary Forest Loss...")
    
    # Try with simpler filter
    df = query_zonal(
        geostore_id,
        sum_layers=["area__ha"],
        group_by_layers=["umd_tree_cover_loss__year", "is__umd_regional_primary_forest_2001"]
    )
    
    if df is not None:
        df['province'] = province
        if 'umd_tree_cover_loss__year' in df.columns:
            df['year'] = pd.to_numeric(df['umd_tree_cover_loss__year'], errors='coerce')
        return df
    
    return pd.DataFrame()


def fetch_3_tree_cover_by_category(province, geostore_id):
    """3. Tree Cover by Land Category - WORKING"""
    print(f"[3/7] Tree Cover by Land Category...")
    
    categories = [
        "wdpa_protected_areas__iucn_cat",
        "gfw_plantations__type"
    ]
    
    all_data = []
    
    for category in categories:
        df = query_zonal(
            geostore_id,
            sum_layers=["area__ha"],
            group_by_layers=[category]
        )
        if df is not None:
            df['category_type'] = category
            df['province'] = province
            all_data.append(df)
        time.sleep(0.5)
    
    if all_data:
        return pd.concat(all_data, ignore_index=True)
    
    return pd.DataFrame()


def fetch_4_loss_in_protected_areas(province, geostore_id):
    """4. Tree Cover Loss in Protected Areas - WORKING"""
    print(f"[4/7] Loss in Protected Areas...")
    
    df = query_zonal(
        geostore_id,
        sum_layers=["area__ha"],
        group_by_layers=["umd_tree_cover_loss__year", "wdpa_protected_areas__iucn_cat"]
    )
    
    if df is not None:
        df['province'] = province
        if 'umd_tree_cover_loss__year' in df.columns:
            df['year'] = pd.to_numeric(df['umd_tree_cover_loss__year'], errors='coerce')
        return df
    
    return pd.DataFrame()


def fetch_5_tree_cover_gain(province, geostore_id):
    """5. Tree Cover Gain - WORKING"""
    print(f"[5/7] Tree Cover Gain...")
    
    df = query_zonal(
        geostore_id,
        sum_layers=["area__ha"],
        group_by_layers=["is__umd_tree_cover_gain"]
    )
    
    if df is not None:
        df['province'] = province
        return df
    
    return pd.DataFrame()


def fetch_6_loss_by_land_cover(province, geostore_id):
    """6. Tree Cover Loss by Land Cover Type (ESA) - WORKING"""
    print(f"[6/7] Loss by Land Cover Type...")
    
    df = query_zonal(
        geostore_id,
        sum_layers=["area__ha"],
        group_by_layers=["umd_tree_cover_loss__year", "esa_land_cover_2015__class"]
    )
    
    if df is not None:
        df['province'] = province
        if 'umd_tree_cover_loss__year' in df.columns:
            df['year'] = pd.to_numeric(df['umd_tree_cover_loss__year'], errors='coerce')
        return df
    
    return pd.DataFrame()


def fetch_7_tree_cover_density(province, geostore_id):
    """7. Tree Cover Density 2000 & 2010"""
    print(f"[7/7] Tree Cover Density...")
    
    all_data = []
    
    # Try different density thresholds
    for density_layer in ["umd_tree_cover_density_2000__30", "umd_tree_cover_density_2010__30"]:
        df = query_zonal(
            geostore_id,
            sum_layers=["area__ha"],
            group_by_layers=[density_layer]
        )
        if df is not None:
            df['density_layer'] = density_layer
            df['province'] = province
            all_data.append(df)
        time.sleep(0.5)
    
    if all_data:
        return pd.concat(all_data, ignore_index=True)
    
    return pd.DataFrame()


def fetch_province_complete(province_name, geostore_id):
    """Fetch ALL valid data untuk 1 provinsi"""
    
    print("\n" + "="*70)
    print(f"FETCHING: {province_name}")
    print(f"Geostore: {geostore_id}")
    print("="*70)
    
    datasets = {}
    
    datasets['tree_cover_loss'] = fetch_1_tree_cover_loss(province_name, geostore_id)
    time.sleep(1)
    
    datasets['primary_forest_loss'] = fetch_2_primary_forest_loss(province_name, geostore_id)
    time.sleep(1)
    
    datasets['tree_cover_by_category'] = fetch_3_tree_cover_by_category(province_name, geostore_id)
    time.sleep(1)
    
    datasets['loss_in_protected_areas'] = fetch_4_loss_in_protected_areas(province_name, geostore_id)
    time.sleep(1)
    
    datasets['tree_cover_gain'] = fetch_5_tree_cover_gain(province_name, geostore_id)
    time.sleep(1)
    
    datasets['loss_by_land_cover'] = fetch_6_loss_by_land_cover(province_name, geostore_id)
    time.sleep(1)
    
    datasets['tree_cover_density'] = fetch_7_tree_cover_density(province_name, geostore_id)
    
    return datasets


def main():
    print("\n" + "="*70)
    print("GFW MEGA DATA FETCH V2 - CORRECTED LAYER NAMES")
    print("="*70)
    print(f"API Key: {API_KEY[:20]}...")
    print(f"Provinces: {len(GEOSTORE_MAPPING)}")
    print(f"Datasets per province: 7")
    print(f"Total queries: ~{len(GEOSTORE_MAPPING) * 10}")
    
    all_datasets = {}
    
    for dataset_name in [
        'tree_cover_loss',
        'primary_forest_loss',
        'tree_cover_by_category',
        'loss_in_protected_areas',
        'tree_cover_gain',
        'loss_by_land_cover',
        'tree_cover_density'
    ]:
        all_datasets[dataset_name] = []
    
    # Fetch data untuk setiap provinsi
    for province_name, geostore_id in GEOSTORE_MAPPING.items():
        province_data = fetch_province_complete(province_name, geostore_id)
        
        for dataset_name, df in province_data.items():
            if not df.empty:
                all_datasets[dataset_name].append(df)
    
    # Consolidate & Save
    print("\n" + "="*70)
    print("CONSOLIDATING & SAVING")
    print("="*70)
    
    output_dir = Path("data/raw/klhk_gfw/mega_fetch_v2")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for dataset_name, df_list in all_datasets.items():
        if df_list:
            consolidated = pd.concat(df_list, ignore_index=True)
            output_file = output_dir / f"{dataset_name}_sulawesi_2001_2025.csv"
            consolidated.to_csv(output_file, index=False)
            print(f"✅ {dataset_name}: {len(consolidated)} rows → {output_file.name}")
        else:
            print(f"⚠️ {dataset_name}: No data")
    
    print("\n" + "="*70)
    print("MEGA FETCH V2 COMPLETE!")
    print("="*70)
    print(f"Output directory: {output_dir}")
    print(f"Files created: {len([f for f in output_dir.glob('*.csv')])}")


if __name__ == "__main__":
    main()
