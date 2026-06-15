"""
GFW COMPLETE DATA FETCH - ALL 19 DASHBOARD CARDS
================================================

Fetch SEMUA data dari GFW dashboard menggunakan QUERY API + SPECIALIZED ENDPOINTS.
Target: 19 cards × 6 provinsi = COMPLETE DATASET!

Datasets:
1. Tree Cover Loss ✅ (sudah ada)
2. Primary Forest Loss ✅ (sudah ada)
3. Tree Cover Loss by Driver 🔥 (KRUSIAL!)
4. Primary Forest Loss by Driver 🔥 (SUPER KRUSIAL!)
5. CO2 Emissions
6. Tree Cover by Land Category ✅ (partial)
7. Primary Forest by Land Category
8. Tree Cover Loss by Land Category
9. Fire Alerts (NASA VIIRS)
10. GLAD Alerts
11. Tree Cover Extent 2000/2010/Current
12. Tree Cover Gain ✅ (sudah ada)
13. Biomass Loss
14. Loss in Protected Areas ✅ (sudah ada)
15. Primary Forest Loss in Protected Areas
16. Loss by Land Cover ✅ (sudah ada)
17. Deforestation Rate
18. Forest Cover Change
19. Plantation types

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

# Sulawesi Province Admin Codes (from docs)
PROVINCES = {
    "Sulawesi Utara": {"code": "31", "iso": "ID-ND"},
    "Sulawesi Tengah": {"code": "29", "iso": "ID-CT"},
    "Sulawesi Selatan": {"code": "30", "iso": "ID-SN"},
    "Sulawesi Tenggara": {"code": "32", "iso": "ID-SG"},
    "Gorontalo": {"code": "11", "iso": "ID-GT"},
    "Sulawesi Barat": {"code": "33", "iso": "ID-SR"}
}

# Geostore mapping (from previous fetch)
GEOSTORE_FILE = Path("data/raw/klhk_gfw/sulawesi_geostore_mapping.json")
with open(GEOSTORE_FILE) as f:
    GEOSTORE_MAPPING = json.load(f)


def query_dataset(dataset, version, sql, geostore_id=None):
    """Universal query function untuk GFW datasets"""
    endpoint = f"{BASE}/dataset/{dataset}/{version}/query/json"
    
    params = {"sql": sql}
    if geostore_id:
        params["geostore_id"] = geostore_id
        params["geostore_origin"] = "gfw"
    
    headers = {"x-api-key": API_KEY}
    
    try:
        response = requests.get(endpoint, params=params, headers=headers, timeout=180)
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and len(data['data']) > 0:
                return pd.DataFrame(data['data'])
            else:
                print(f"  ⚠️ No data returned")
                return None
        else:
            print(f"  ❌ Status {response.status_code}: {response.text[:300]}")
            return None
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return None


def download_by_aoi(dataset, version, sql, aoi, filename="export.csv"):
    """Download data by Area of Interest"""
    endpoint = f"{BASE}/dataset/{dataset}/{version}/download_by_aoi/csv"
    
    params = {
        "sql": sql,
        "aoi": json.dumps(aoi),
        "filename": filename
    }
    
    headers = {"x-api-key": API_KEY}
    
    try:
        response = requests.get(endpoint, params=params, headers=headers, timeout=300)
        
        if response.status_code == 200:
            # Parse CSV response
            from io import StringIO
            df = pd.read_csv(StringIO(response.text))
            return df
        else:
            print(f"  ❌ Download failed: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return None


def fetch_loss_by_driver(province_name, admin_code, geostore_id):
    """3. Tree Cover Loss by Driver (KRUSIAL!)"""
    print(f"\n[NEW-1/13] Tree Cover Loss by Driver...")
    
    sql = """
    SELECT 
        tsc_tree_cover_loss_drivers__type as driver,
        umd_tree_cover_loss__year as year,
        SUM(area__ha) as area_ha
    FROM data
    WHERE umd_tree_cover_loss__year >= 2001
    GROUP BY tsc_tree_cover_loss_drivers__type, umd_tree_cover_loss__year
    ORDER BY umd_tree_cover_loss__year, tsc_tree_cover_loss_drivers__type
    """
    
    df = query_dataset("tsc_tree_cover_loss_drivers", "latest", sql, geostore_id)
    
    if df is not None:
        df['province'] = province_name
        return df
    
    return pd.DataFrame()


def fetch_primary_loss_by_driver(province_name, admin_code, geostore_id):
    """4. Primary Forest Loss by Driver (SUPER KRUSIAL!)"""
    print(f"[NEW-2/13] Primary Forest Loss by Driver...")
    
    sql = """
    SELECT 
        tsc_tree_cover_loss_drivers__type as driver,
        umd_tree_cover_loss__year as year,
        is__umd_regional_primary_forest_2001 as is_primary,
        SUM(area__ha) as area_ha
    FROM data
    WHERE umd_tree_cover_loss__year >= 2001
      AND is__umd_regional_primary_forest_2001 = true
    GROUP BY tsc_tree_cover_loss_drivers__type, umd_tree_cover_loss__year, is__umd_regional_primary_forest_2001
    ORDER BY umd_tree_cover_loss__year, tsc_tree_cover_loss_drivers__type
    """
    
    df = query_dataset("tsc_tree_cover_loss_drivers", "latest", sql, geostore_id)
    
    if df is not None:
        df['province'] = province_name
        return df
    
    return pd.DataFrame()


def fetch_co2_emissions(province_name, admin_code, geostore_id):
    """5. CO2 Emissions from Tree Cover Loss"""
    print(f"[NEW-3/13] CO2 Emissions...")
    
    sql = """
    SELECT 
        umd_tree_cover_loss__year as year,
        SUM(whrc_aboveground_co2_emissions__Mg) as co2_emissions_mg,
        SUM(area__ha) as area_ha
    FROM data
    WHERE umd_tree_cover_loss__year >= 2001
    GROUP BY umd_tree_cover_loss__year
    ORDER BY umd_tree_cover_loss__year
    """
    
    # Try carbon emissions dataset
    df = query_dataset("gfw_forest_carbon_gross_emissions", "latest", sql, geostore_id)
    
    if df is not None:
        df['province'] = province_name
        return df
    
    return pd.DataFrame()


def fetch_fire_alerts(province_name, admin_code, geostore_id):
    """9. Fire Alerts (NASA VIIRS) - 2016-2024"""
    print(f"[NEW-4/13] Fire Alerts...")
    
    sql = """
    SELECT 
        DATE_TRUNC('month', alert__date) as month,
        COUNT(*) as alert_count,
        AVG(confidence__cat) as avg_confidence
    FROM data
    WHERE alert__date >= '2016-01-01'
    GROUP BY DATE_TRUNC('month', alert__date)
    ORDER BY month
    """
    
    df = query_dataset("nasa_viirs_fire_alerts", "latest", sql, geostore_id)
    
    if df is not None:
        df['province'] = province_name
        return df
    
    return pd.DataFrame()


def fetch_glad_alerts(province_name, admin_code, geostore_id):
    """10. GLAD Alerts - Deforestation alerts"""
    print(f"[NEW-5/13] GLAD Alerts...")
    
    sql = """
    SELECT 
        umd_glad_alerts__isoweek as isoweek,
        umd_glad_alerts__date as date,
        COUNT(*) as alert_count
    FROM data
    WHERE umd_glad_alerts__date >= '2016-01-01'
    GROUP BY umd_glad_alerts__isoweek, umd_glad_alerts__date
    ORDER BY umd_glad_alerts__date
    """
    
    df = query_dataset("umd_glad_alerts", "latest", sql, geostore_id)
    
    if df is not None:
        df['province'] = province_name
        return df
    
    return pd.DataFrame()


def fetch_tree_cover_extent(province_name, admin_code, geostore_id):
    """11. Tree Cover Extent 2000/2010"""
    print(f"[NEW-6/13] Tree Cover Extent 2000 & 2010...")
    
    all_data = []
    
    # Extent 2000
    sql_2000 = """
    SELECT 
        SUM(area__ha) as tree_cover_2000_ha,
        AVG(umd_tree_cover_density_2000__threshold) as avg_density
    FROM data
    WHERE umd_tree_cover_density_2000__threshold >= 30
    """
    
    df_2000 = query_dataset("umd_tree_cover_density_2000", "latest", sql_2000, geostore_id)
    if df_2000 is not None:
        df_2000['year'] = 2000
        df_2000['province'] = province_name
        all_data.append(df_2000)
    
    time.sleep(1)
    
    # Extent 2010
    sql_2010 = """
    SELECT 
        SUM(area__ha) as tree_cover_2010_ha,
        AVG(umd_tree_cover_density_2010__threshold) as avg_density
    FROM data
    WHERE umd_tree_cover_density_2010__threshold >= 30
    """
    
    df_2010 = query_dataset("umd_tree_cover_density_2010", "latest", sql_2010, geostore_id)
    if df_2010 is not None:
        df_2010['year'] = 2010
        df_2010['province'] = province_name
        all_data.append(df_2010)
    
    if all_data:
        return pd.concat(all_data, ignore_index=True)
    
    return pd.DataFrame()


def fetch_biomass_loss(province_name, admin_code, geostore_id):
    """13. Biomass Loss"""
    print(f"[NEW-7/13] Biomass Loss...")
    
    sql = """
    SELECT 
        umd_tree_cover_loss__year as year,
        SUM(whrc_aboveground_biomass_stock_2000__Mg_ha_1) as biomass_loss_mg
    FROM data
    WHERE umd_tree_cover_loss__year >= 2001
    GROUP BY umd_tree_cover_loss__year
    ORDER BY umd_tree_cover_loss__year
    """
    
    df = query_dataset("umd_tree_cover_loss", "latest", sql, geostore_id)
    
    if df is not None:
        df['province'] = province_name
        return df
    
    return pd.DataFrame()


def fetch_primary_loss_in_protected(province_name, admin_code, geostore_id):
    """15. Primary Forest Loss in Protected Areas"""
    print(f"[NEW-8/13] Primary Forest Loss in Protected Areas...")
    
    sql = """
    SELECT 
        umd_tree_cover_loss__year as year,
        wdpa_protected_areas__iucn_cat as iucn_category,
        is__umd_regional_primary_forest_2001 as is_primary,
        SUM(area__ha) as area_ha
    FROM data
    WHERE umd_tree_cover_loss__year >= 2001
      AND is__umd_regional_primary_forest_2001 = true
    GROUP BY umd_tree_cover_loss__year, wdpa_protected_areas__iucn_cat, is__umd_regional_primary_forest_2001
    ORDER BY umd_tree_cover_loss__year
    """
    
    df = query_dataset("umd_tree_cover_loss", "latest", sql, geostore_id)
    
    if df is not None:
        df['province'] = province_name
        return df
    
    return pd.DataFrame()


def fetch_primary_by_category(province_name, admin_code, geostore_id):
    """7. Primary Forest by Land Category"""
    print(f"[NEW-9/13] Primary Forest by Land Category...")
    
    sql = """
    SELECT 
        wdpa_protected_areas__iucn_cat as category,
        is__umd_regional_primary_forest_2001 as is_primary,
        SUM(area__ha) as area_ha
    FROM data
    WHERE is__umd_regional_primary_forest_2001 = true
    GROUP BY wdpa_protected_areas__iucn_cat, is__umd_regional_primary_forest_2001
    """
    
    df = query_dataset("umd_tree_cover_loss", "latest", sql, geostore_id)
    
    if df is not None:
        df['province'] = province_name
        return df
    
    return pd.DataFrame()


def fetch_loss_by_category(province_name, admin_code, geostore_id):
    """8. Tree Cover Loss by Land Category"""
    print(f"[NEW-10/13] Tree Cover Loss by Land Category...")
    
    # Try multiple category layers
    categories = [
        ("wdpa_protected_areas__iucn_cat", "protected_areas"),
        ("gfw_plantations__type", "plantations"),
        ("idn_forest_area__type", "forest_area_type")
    ]
    
    all_data = []
    
    for layer, cat_name in categories:
        sql = f"""
        SELECT 
            umd_tree_cover_loss__year as year,
            {layer} as category,
            SUM(area__ha) as area_ha
        FROM data
        WHERE umd_tree_cover_loss__year >= 2001
        GROUP BY umd_tree_cover_loss__year, {layer}
        ORDER BY umd_tree_cover_loss__year
        """
        
        df = query_dataset("umd_tree_cover_loss", "latest", sql, geostore_id)
        if df is not None:
            df['category_type'] = cat_name
            df['province'] = province_name
            all_data.append(df)
        
        time.sleep(0.5)
    
    if all_data:
        return pd.concat(all_data, ignore_index=True)
    
    return pd.DataFrame()


def fetch_plantation_types(province_name, admin_code, geostore_id):
    """19. Plantation Types (Oil Palm, Wood Fiber)"""
    print(f"[NEW-11/13] Plantation Types...")
    
    all_data = []
    
    # Oil Palm
    sql_palm = """
    SELECT 
        gfw_oil_palm__type as plantation_type,
        rspo_oil_palm__certification_status as rspo_status,
        SUM(area__ha) as area_ha
    FROM data
    GROUP BY gfw_oil_palm__type, rspo_oil_palm__certification_status
    """
    
    df_palm = query_dataset("gfw_oil_palm", "latest", sql_palm, geostore_id)
    if df_palm is not None:
        df_palm['commodity'] = 'oil_palm'
        df_palm['province'] = province_name
        all_data.append(df_palm)
    
    time.sleep(1)
    
    # Wood Fiber
    sql_fiber = """
    SELECT 
        gfw_wood_fiber__type as plantation_type,
        SUM(area__ha) as area_ha
    FROM data
    GROUP BY gfw_wood_fiber__type
    """
    
    df_fiber = query_dataset("gfw_wood_fiber", "latest", sql_fiber, geostore_id)
    if df_fiber is not None:
        df_fiber['commodity'] = 'wood_fiber'
        df_fiber['province'] = province_name
        all_data.append(df_fiber)
    
    if all_data:
        return pd.concat(all_data, ignore_index=True)
    
    return pd.DataFrame()


def fetch_deforestation_rate(province_name, admin_code, geostore_id):
    """17. Deforestation Rate (calculated from loss + extent)"""
    print(f"[NEW-12/13] Deforestation Rate...")
    
    sql = """
    SELECT 
        umd_tree_cover_loss__year as year,
        SUM(area__ha) as loss_ha
    FROM data
    WHERE umd_tree_cover_loss__year >= 2001
    GROUP BY umd_tree_cover_loss__year
    ORDER BY umd_tree_cover_loss__year
    """
    
    df = query_dataset("umd_tree_cover_loss", "latest", sql, geostore_id)
    
    if df is not None:
        df['province'] = province_name
        # Calculate rate (will need baseline extent)
        return df
    
    return pd.DataFrame()


def fetch_forest_cover_change(province_name, admin_code, geostore_id):
    """18. Net Forest Cover Change (loss - gain)"""
    print(f"[NEW-13/13] Forest Cover Change (Net)...")
    
    # Get loss
    sql_loss = """
    SELECT 
        umd_tree_cover_loss__year as year,
        SUM(area__ha) as loss_ha
    FROM data
    WHERE umd_tree_cover_loss__year >= 2001
    GROUP BY umd_tree_cover_loss__year
    """
    
    df_loss = query_dataset("umd_tree_cover_loss", "latest", sql_loss, geostore_id)
    
    # Get gain
    sql_gain = """
    SELECT 
        SUM(area__ha) as gain_ha
    FROM data
    WHERE is__umd_tree_cover_gain = true
    """
    
    df_gain = query_dataset("umd_tree_cover_gain", "latest", sql_gain, geostore_id)
    
    if df_loss is not None:
        df_loss['province'] = province_name
        if df_gain is not None and not df_gain.empty:
            # Distribute gain across years (gain is 2000-2012 total)
            gain_per_year = df_gain['gain_ha'].iloc[0] / 12  # 12 years
            df_loss['gain_ha'] = gain_per_year
            df_loss['net_change_ha'] = df_loss['gain_ha'] - df_loss['loss_ha']
        return df_loss
    
    return pd.DataFrame()


def fetch_province_complete(province_name, admin_code, geostore_id):
    """Fetch ALL NEW datasets untuk 1 provinsi"""
    
    print("\n" + "="*70)
    print(f"FETCHING: {province_name}")
    print(f"Admin Code: {admin_code}")
    print(f"Geostore: {geostore_id}")
    print("="*70)
    
    datasets = {}
    
    datasets['loss_by_driver'] = fetch_loss_by_driver(province_name, admin_code, geostore_id)
    time.sleep(1)
    
    datasets['primary_loss_by_driver'] = fetch_primary_loss_by_driver(province_name, admin_code, geostore_id)
    time.sleep(1)
    
    datasets['co2_emissions'] = fetch_co2_emissions(province_name, admin_code, geostore_id)
    time.sleep(1)
    
    datasets['fire_alerts'] = fetch_fire_alerts(province_name, admin_code, geostore_id)
    time.sleep(1)
    
    datasets['glad_alerts'] = fetch_glad_alerts(province_name, admin_code, geostore_id)
    time.sleep(1)
    
    datasets['tree_cover_extent'] = fetch_tree_cover_extent(province_name, admin_code, geostore_id)
    time.sleep(1)
    
    datasets['biomass_loss'] = fetch_biomass_loss(province_name, admin_code, geostore_id)
    time.sleep(1)
    
    datasets['primary_loss_in_protected'] = fetch_primary_loss_in_protected(province_name, admin_code, geostore_id)
    time.sleep(1)
    
    datasets['primary_by_category'] = fetch_primary_by_category(province_name, admin_code, geostore_id)
    time.sleep(1)
    
    datasets['loss_by_category'] = fetch_loss_by_category(province_name, admin_code, geostore_id)
    time.sleep(1)
    
    datasets['plantation_types'] = fetch_plantation_types(province_name, admin_code, geostore_id)
    time.sleep(1)
    
    datasets['deforestation_rate'] = fetch_deforestation_rate(province_name, admin_code, geostore_id)
    time.sleep(1)
    
    datasets['forest_cover_change'] = fetch_forest_cover_change(province_name, admin_code, geostore_id)
    
    return datasets


def main():
    print("\n" + "="*70)
    print("GFW COMPLETE DATA FETCH - ALL 19 DASHBOARD CARDS")
    print("="*70)
    print(f"API Key: {API_KEY[:20]}...")
    print(f"Provinces: {len(PROVINCES)}")
    print(f"NEW Datasets: 13")
    print(f"Total queries: ~{len(PROVINCES) * 15} (accounting for retries)")
    
    all_datasets = {}
    
    for dataset_name in [
        'loss_by_driver',
        'primary_loss_by_driver',
        'co2_emissions',
        'fire_alerts',
        'glad_alerts',
        'tree_cover_extent',
        'biomass_loss',
        'primary_loss_in_protected',
        'primary_by_category',
        'loss_by_category',
        'plantation_types',
        'deforestation_rate',
        'forest_cover_change'
    ]:
        all_datasets[dataset_name] = []
    
    # Fetch data untuk setiap provinsi
    for province_name, province_info in PROVINCES.items():
        admin_code = province_info['code']
        geostore_id = GEOSTORE_MAPPING.get(province_name)
        
        if not geostore_id:
            print(f"⚠️ Skipping {province_name} - no geostore ID")
            continue
        
        province_data = fetch_province_complete(province_name, admin_code, geostore_id)
        
        for dataset_name, df in province_data.items():
            if not df.empty:
                all_datasets[dataset_name].append(df)
    
    # Consolidate & Save
    print("\n" + "="*70)
    print("CONSOLIDATING & SAVING")
    print("="*70)
    
    output_dir = Path("data/raw/klhk_gfw/complete_fetch")
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
    print("COMPLETE FETCH DONE!")
    print("="*70)
    print(f"Output directory: {output_dir}")
    print(f"Files created: {len([f for f in output_dir.glob('*.csv')])}")
    
    # Summary
    total_rows = sum(len(pd.concat(df_list)) for df_list in all_datasets.values() if df_list)
    print(f"\n📊 TOTAL DATA POINTS: {total_rows:,} rows")
    print(f"🎯 SUCCESS RATE: {len([d for d in all_datasets.values() if d])}/13 datasets")


if __name__ == "__main__":
    main()
