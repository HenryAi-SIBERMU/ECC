"""
GFW DRIVER DATA - Using Beta Land API
=====================================

Fetch tree cover loss BY DRIVER menggunakan specialized endpoint:
POST /v0/land/tree_cover_loss_by_driver

Ini endpoint yang BETUL untuk driver data!

Author: CELIOS Research  
Date: 14 Juni 2026
"""

import requests
import pandas as pd
import json
from pathlib import Path
import time

API_KEY = "21899f40-1f6d-4ff9-93e1-c10d04513984"
BASE = "https://data-api.globalforestwatch.org"

PROVINCES = {
    "Sulawesi Utara": "31",
    "Sulawesi Tengah": "29",
    "Sulawesi Selatan": "30",
    "Sulawesi Tenggara": "32",
    "Gorontalo": "11",
    "Sulawesi Barat": "33"
}


def create_driver_analysis(province_name, admin_code, canopy_cover=30):
    """Create tree cover loss by driver analysis via Beta Land API"""
    
    endpoint = f"{BASE}/v0/land/tree_cover_loss_by_driver"
    
    payload = {
        "aoi": {
            "type": "admin",
            "country": "IDN",
            "region": admin_code
        },
        "canopy_cover": canopy_cover
    }
    
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    print(f"\n🚀 Creating driver analysis for {province_name} (admin code: {admin_code})...")
    
    try:
        response = requests.post(endpoint, json=payload, headers=headers, timeout=120)
        
        if response.status_code == 202:
            data = response.json()
            resource_link = data['data']['link']
            resource_id = resource_link.split('/')[-1]
            
            print(f"  ✅ Analysis created! Resource ID: {resource_id}")
            print(f"  📍 Link: {resource_link}")
            
            return resource_id, resource_link
        else:
            print(f"  ❌ Failed: {response.status_code}")
            print(f"  {response.text[:500]}")
            return None, None
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return None, None


def get_driver_analysis_result(resource_id, max_retries=30, wait_seconds=10):
    """Poll for analysis result"""
    
    endpoint = f"{BASE}/v0/land/tree_cover_loss_by_driver/{resource_id}"
    headers = {"x-api-key": API_KEY}
    
    print(f"\n⏳ Polling for result (max {max_retries} retries, {wait_seconds}s interval)...")
    
    for i in range(max_retries):
        try:
            response = requests.get(endpoint, headers=headers, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                status = data['data']['status']
                
                print(f"  [{i+1}/{max_retries}] Status: {status}")
                
                if status == 'saved':
                    print(f"  ✅ Analysis complete!")
                    result = data['data']['result']
                    return result
                    
                elif status == 'failed':
                    print(f"  ❌ Analysis failed!")
                    print(f"  Message: {data['data'].get('message', 'No error message')}")
                    return None
                    
                elif status in ['pending', 'processing']:
                    time.sleep(wait_seconds)
                    continue
                    
            else:
                print(f"  ⚠️ Status {response.status_code}, retrying...")
                time.sleep(wait_seconds)
                
        except Exception as e:
            print(f"  ⚠️ Error: {e}, retrying...")
            time.sleep(wait_seconds)
    
    print(f"  ❌ Timeout after {max_retries} retries")
    return None


def parse_driver_result(result, province_name):
    """Parse result into pandas DataFrame"""
    
    if not result:
        return pd.DataFrame()
    
    # Debug: print result structure
    print(f"\n📋 DEBUG: Result type = {type(result)}")
    if isinstance(result, dict):
        print(f"  Keys: {result.keys()}")
        
        # Try 'yearly_tree_cover_loss_by_driver' first (more detailed)
        if 'yearly_tree_cover_loss_by_driver' in result:
            data_list = result['yearly_tree_cover_loss_by_driver']
            print(f"  Using 'yearly_tree_cover_loss_by_driver' - {len(data_list) if isinstance(data_list, list) else 'not a list'} items")
        elif 'tree_cover_loss_by_driver' in result:
            data_list = result['tree_cover_loss_by_driver']
            print(f"  Using 'tree_cover_loss_by_driver' - {len(data_list) if isinstance(data_list, list) else 'not a list'} items")
        else:
            print(f"  ⚠️ No known key found, trying as direct data")
            data_list = [result]
    else:
        data_list = result if isinstance(result, list) else [result]
    
    all_data = []
    
    for entry in data_list:
        if isinstance(entry, dict):
            # Print first entry for debugging
            if not all_data:
                print(f"  📄 First entry keys: {entry.keys()}")
            
            row = {
                'province': province_name,
                'year': entry.get('loss_year') or entry.get('umd_tree_cover_loss__year') or entry.get('year'),
                'driver': entry.get('drivers_type') or entry.get('tsc_tree_cover_loss_drivers__type') or entry.get('driver') or entry.get('dominant_driver'),
                'area_ha': entry.get('loss_area_ha') or entry.get('area__ha') or entry.get('area') or entry.get('total_area'),
                'co2_emissions_mg': entry.get('gross_carbon_emissions_Mg') or entry.get('co2_emissions'),
                'is_primary': entry.get('is__umd_regional_primary_forest_2001') or entry.get('is_primary_forest')
            }
            all_data.append(row)
    
    df = pd.DataFrame(all_data)
    print(f"  ✅ Parsed {len(df)} rows")
    return df


def main():
    print("\n" + "="*70)
    print("GFW DRIVER DATA FETCH - Beta Land API")
    print("="*70)
    print(f"API Key: {API_KEY[:20]}...")
    print(f"Provinces: {len(PROVINCES)}")
    print(f"Method: POST /v0/land/tree_cover_loss_by_driver")
    
    all_results = []
    resource_ids = {}
    
    # Step 1: Create analyses or use existing
    print("\n" + "="*70)
    print("STEP 1: Creating/Getting analyses")
    print("="*70)
    
    for province_name, admin_code in PROVINCES.items():
        resource_id, link = create_driver_analysis(province_name, admin_code)
        
        # If resource exists (409), extract ID from error message
        if not resource_id:
            # Resource already exists, need to search/get it
            # For now, try a test GET
            print(f"  ℹ️ Resource already exists for {province_name}, skipping creation")
        else:
            resource_ids[province_name] = resource_id
        
        time.sleep(2)  # Rate limiting
    
    # Hardcode existing resource IDs from first run
    if not resource_ids:
        print("\n⚠️ Using existing resource IDs from previous run...")
        resource_ids = {
            "Sulawesi Utara": "f3aba402-33ba-558a-8c24-5cd6f931ecbc",
            "Sulawesi Tengah": "b615cac2-48e4-504a-897a-966cdb3ec033",
            "Sulawesi Selatan": "cb6017fd-129b-5112-be45-982fba8fe73a",
            "Sulawesi Tenggara": "6bf45d8c-3a82-5fa7-9596-3fd5bf998fd5",
            "Gorontalo": "a8bd743f-6807-5313-ad2a-7a11ece729d5",
            "Sulawesi Barat": "0fce2a14-be60-5b0a-a389-c0526eadbd64"
        }
    
    # Step 2: Poll for results
    print("\n" + "="*70)
    print("STEP 2: Polling for results")
    print("="*70)
    
    for province_name, resource_id in resource_ids.items():
        print(f"\n{'='*70}")
        print(f"Province: {province_name}")
        print(f"Resource ID: {resource_id}")
        print(f"{'='*70}")
        
        result = get_driver_analysis_result(resource_id, max_retries=20, wait_seconds=15)
        
        if result:
            df = parse_driver_result(result, province_name)
            if not df.empty:
                all_results.append(df)
                print(f"  ✅ Got {len(df)} rows for {province_name}")
        
        time.sleep(5)  # Rate limiting between provinces
    
    # Step 3: Consolidate & Save
    print("\n" + "="*70)
    print("STEP 3: Saving results")
    print("="*70)
    
    if all_results:
        combined = pd.concat(all_results, ignore_index=True)
        
        output_dir = Path("data/raw/klhk_gfw/land_api_fetch")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / "loss_by_driver_sulawesi_2001_2025.csv"
        combined.to_csv(output_file, index=False)
        
        print(f"\n✅ SUCCESS!")
        print(f"  Total rows: {len(combined)}")
        print(f"  File: {output_file}")
        
        # Summary by driver
        print(f"\n📊 SUMMARY BY DRIVER:")
        summary = combined.groupby('driver')['area_ha'].sum().sort_values(ascending=False)
        for driver, area in summary.items():
            print(f"  {driver}: {area:,.0f} ha")
            
    else:
        print(f"\n❌ No data collected")
    
    print("\n" + "="*70)
    print("DONE!")
    print("="*70)


if __name__ == "__main__":
    main()
