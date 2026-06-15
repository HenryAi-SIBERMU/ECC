"""
GFW MEGA DATA FETCH - All Widgets/Cards via API
================================================

Fetch SEMUA data dari GFW dashboard untuk 6 provinsi Sulawesi:
1. Tree cover loss
2. Primary forest loss  
3. Tree cover by land category
4. Forest loss by driver
5. CO2 emissions
6. Fire alerts
7. Protected areas analysis
8. Dan semua data lainnya!

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
    """
    Universal zonal statistics query.
    
    Args:
        geostore_id: Geostore UUID
        sum_layers: List of layers to sum (e.g., ['area__ha'])
        group_by_layers: List of layers to group by
        filters: List of filter dicts
    
    Returns:
        DataFrame or None
    """
    endpoint = f"{BASE}/analysis/zonal/{geostore_id}"
    
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
                print(f"  ⚠️ No data in response")
                return None
        else:
            print(f"  ❌ Status {response.status_code}: {response.text[:200]}")
            return None
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return None


def fetch_1_tree_cover_loss(province, geostore_id):
    """1. Tree Cover Loss (Total) - Bar chart hijau"""
    print(f"\n[1/10] Tree Cover Loss...")
    
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
    """2. Primary Forest Loss - Bar chart pink"""
    print(f"[2/10] Primary Forest Loss...")
    
    df = query_zonal(
        geostore_id,
        sum_layers=["area__ha"],
        group_by_layers=["umd_tree_cover_loss__year"],
        filters=[{"layer": "is__umd_regional_primary_forest_2001", "value": "true"}]
    )
    
    if df is not None and 'umd_tree_cover_loss__year' in df.columns:
        df = df.rename(columns={
            'umd_tree_cover_loss__year': 'year',
            'area__ha': 'primary_forest_loss_ha'
        })
        df['province'] = province
        df['year'] = pd.to_numeric(df['year'], errors='coerce')
        return df
    
    return pd.DataFrame()


def fetch_3_loss_by_driver(province, geostore_id):
    """3. Forest Loss by Driver - Donut/Table"""
    print(f"[3/10] Forest Loss by Driver...")
    
    df = query_zonal(
        geostore_id,
        sum_layers=["area__ha"],
        group_by_layers=["tsc_tree_cover_loss_drivers__type", "umd_tree_cover_loss__year"]
    )
    
    if df is not None:
        df['province'] = province
        if 'umd_tree_cover_loss__year' in df.columns:
            df['year'] = pd.to_numeric(df['umd_tree_cover_loss__year'], errors='coerce')
        return df
    
    return pd.DataFrame()


def fetch_4_primary_loss_by_driver(province, geostore_id):
    """4. Primary Forest Loss by Driver"""
    print(f"[4/10] Primary Forest Loss by Driver...")
    
    df = query_zonal(
        geostore_id,
        sum_layers=["area__ha"],
        group_by_layers=["tsc_tree_cover_loss_drivers__type", "umd_tree_cover_loss__year"],
        filters=[{"layer": "is__umd_regional_primary_forest_2001", "value": "true"}]
    )
    
    if df is not None:
        df['province'] = province
        if 'umd_tree_cover_loss__year' in df.columns:
            df['year'] = pd.to_numeric(df['umd_tree_cover_loss__year'], errors='coerce')
        return df
    
    return pd.DataFrame()


def fetch_5_co2_emissions(province, geostore_id):
    """5. CO2 Emissions from Tree Cover Loss"""
    print(f"[5/10] CO2 Emissions...")
    
    df = query_zonal(
        geostore_id,
        sum_layers=["whrc_aboveground_co2_emissions__Mg"],
        group_by_layers=["umd_tree_cover_loss__year"]
    )
    
    if df is not None and 'umd_tree_cover_loss__year' in df.columns:
        df = df.rename(columns={
            'umd_tree_cover_loss__year': 'year',
            'whrc_aboveground_co2_emissions__Mg': 'co2_emissions_mg'
        })
        df['province'] = province
        df['year'] = pd.to_numeric(df['year'], errors='coerce')
        return df
    
    return pd.DataFrame()


def fetch_6_tree_cover_by_category(province, geostore_id):
    """6. Tree Cover by Land Category - Donut chart"""
    print(f"[6/10] Tree Cover by Land Category...")
    
    categories = [
        "wdpa_protected_areas__iucn_cat",
        "gfw_plantations__type",
        "is__gfw_mining",
        "is__gfw_peatlands",
        "is__gfw_oil_palm"
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


def fetch_7_loss_in_protected_areas(province, geostore_id):
    """7. Tree Cover Loss in Protected Areas"""
    print(f"[7/10] Loss in Protected Areas...")
    
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


def fetch_8_tree_cover_gain(province, geostore_id):
    """8. Tree Cover Gain"""
    print(f"[8/10] Tree Cover Gain...")
    
    df = query_zonal(
        geostore_id,
        sum_layers=["area__ha"],
        group_by_layers=["is__umd_tree_cover_gain"]
    )
    
    if df is not None:
        df['province'] = province
        return df
    
    return pd.DataFrame()


def fetch_9_loss_by_land_cover(province, geostore_id):
    """9. Tree Cover Loss by Land Cover Type (ESA)"""
    print(f"[9/10] Loss by Land Cover Type...")
    
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


def fetch_10_tree_cover_extent(province, geostore_id):
    """10. Tree Cover Extent (Baseline)"""
    print(f"[10/10] Tree Cover Extent 2000...")
    
    # Query extent dengan threshold 30%
    df = query_zonal(
        geostore_id,
        sum_layers=["area__ha"],
        group_by_layers=["umd_tree_cover_density_2000__30"]
    )
    
    if df is not None:
        df['province'] = province
        return df
    
    return pd.DataFrame()


def fetch_province_complete(province_name, geostore_id):
    """Fetch ALL data untuk 1 provinsi"""
    
    print("\n" + "="*70)
    print(f"FETCHING: {province_name}")
    print(f"Geostore: {geostore_id}")
    print("="*70)
    
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
    print("\n" + "="*70)
    print("GFW MEGA DATA FETCH - ALL WIDGETS FOR SULAWESI")
    print("="*70)
    print(f"API Key: {API_KEY[:20]}...")
    print(f"Provinces: {len(GEOSTORE_MAPPING)}")
    print(f"Datasets per province: 10")
    print(f"Total queries: {len(GEOSTORE_MAPPING) * 10}")
    
    all_datasets = {}
    
    for dataset_name in [
        'tree_cover_loss',
        'primary_forest_loss',
        'loss_by_driver',
        'primary_loss_by_driver',
        'co2_emissions',
        'tree_cover_by_category',
        'loss_in_protected_areas',
        'tree_cover_gain',
        'loss_by_land_cover',
        'tree_cover_extent'
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
    
    output_dir = Path("data/raw/klhk_gfw/mega_fetch")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for dataset_name, df_list in all_datasets.items():
        if df_list:
            consolidated = pd.concat(df_list, ignore_index=True)
            output_file = output_dir / f"{dataset_name}_sulawesi_2001_2023.csv"
            consolidated.to_csv(output_file, index=False)
            print(f"✅ {dataset_name}: {len(consolidated)} rows → {output_file.name}")
        else:
            print(f"⚠️ {dataset_name}: No data")
    
    print("\n" + "="*70)
    print("MEGA FETCH COMPLETE!")
    print("="*70)
    print(f"Output directory: {output_dir}")
    print(f"Files created: {len([f for f in output_dir.glob('*.csv')])}")


if __name__ == "__main__":
    main()
