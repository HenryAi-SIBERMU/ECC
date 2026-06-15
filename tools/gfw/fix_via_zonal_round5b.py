"""
GFW ROUND 5B: FIX VIA ZONAL ANALYSIS
======================================

Retry using proven ZONAL ANALYSIS approach instead of SQL queries.

Target:
- Card #6: Primary Forest Loss by Driver (zonal with primary filter)
- Card #4: Primary Forest by Category (zonal with primary filter)

Author: CELIOS Research
Date: 14 Juni 2026
"""

import requests
import pandas as pd
import json
from pathlib import Path
import time
from datetime import datetime

API_KEY = "21899f40-1f6d-4ff9-93e1-c10d04513984"
BASE = "https://data-api.globalforestwatch.org"

GEOSTORE_IDS = {
    "Sulawesi Utara": "89b35f128c9cfe7685e1738c89a0a730",
    "Sulawesi Tengah": "fce1e175169936334347ae17207381a0",
    "Sulawesi Selatan": "abc6fc008f433d3dbdc65861bdcc8a87",
    "Sulawesi Tenggara": "fe2e396191a0e8b6e70aa03dd225d7f7",
    "Gorontalo": "db937e7121c426140dd91072c14bbdaf",
    "Sulawesi Barat": "77f83070a9b4111e24a7cfdea73a5adb"
}


def fix_card_6_primary_loss_by_driver_zonal():
    """
    Card #6: Primary Forest Loss by Driver
    Strategy: Zonal analysis with primary forest + driver filters
    """
    print("\n" + "="*70)
    print("CARD #6: Primary Forest Loss by Driver (Zonal Analysis)")
    print("="*70)
    
    all_results = []
    
    for province_name, geostore_id in GEOSTORE_IDS.items():
        print(f"\n🌳 Analyzing primary forest loss drivers for {province_name}...")
        
        url = f"{BASE}/analysis/zonal/{geostore_id}"
        
        params = {
            "sum": ["area__ha", "whrc_aboveground_co2_emissions__Mg"],
            "group_by": ["umd_tree_cover_loss__year", "tsc_tree_cover_loss_drivers__type"],
            "filters": [
                {
                    "layer": "is__umd_regional_primary_forest_2001",
                    "value": "true"  # String, not boolean!
                }
            ],
            "geostore_origin": "gfw"
        }
        
        headers = {"x-api-key": API_KEY}
        
        try:
            response = requests.get(url, params={"json": json.dumps(params)}, headers=headers, timeout=180)
            
            # Alternative: use POST
            if response.status_code != 200:
                response = requests.post(
                    f"{BASE}/analysis/zonal",
                    json={
                        "geostore_id": geostore_id,
                        **params
                    },
                    headers=headers,
                    timeout=180
                )
            
            if response.status_code == 200:
                data = response.json()
                
                if 'data' in data and len(data['data']) > 0:
                    df = pd.DataFrame(data['data'])
                    df['province'] = province_name
                    
                    # Rename columns
                    if 'umd_tree_cover_loss__year' in df.columns:
                        df.rename(columns={
                            'umd_tree_cover_loss__year': 'year',
                            'tsc_tree_cover_loss_drivers__type': 'driver',
                            'area__ha': 'area_ha',
                            'whrc_aboveground_co2_emissions__Mg': 'co2_emissions_mg'
                        }, inplace=True)
                    
                    df['is_primary'] = True
                    all_results.append(df)
                    print(f"  ✅ Got {len(df)} rows")
                else:
                    print(f"  ⚠️ No data returned")
            else:
                print(f"  ❌ Error {response.status_code}: {response.text[:300]}")
                
        except Exception as e:
            print(f"  ❌ Exception: {e}")
        
        time.sleep(3)
    
    if all_results:
        combined = pd.concat(all_results, ignore_index=True)
        
        # Select columns
        cols = ['province', 'year', 'driver', 'area_ha', 'co2_emissions_mg', 'is_primary']
        combined = combined[[c for c in cols if c in combined.columns]]
        
        output_dir = Path("data/raw/klhk_gfw/round5_fixed")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / "primary_forest_loss_by_driver_sulawesi_2001_2023.csv"
        combined.to_csv(output_file, index=False)
        
        print(f"\n✅ Card #6 COMPLETED!")
        print(f"   Total rows: {len(combined)}")
        print(f"   File: {output_file}")
        
        # Summary
        if 'driver' in combined.columns and 'area_ha' in combined.columns:
            print(f"\n📊 SUMMARY BY DRIVER:")
            summary = combined.groupby('driver')['area_ha'].sum().sort_values(ascending=False)
            for driver, area in summary.items():
                print(f"   {driver}: {area:,.0f} ha")
        
        return combined
    else:
        print(f"\n❌ Card #6 FAILED: No data collected")
        return pd.DataFrame()


def fix_card_4_primary_by_category_zonal():
    """
    Card #4: Primary Forest by Land Category
    Strategy: Zonal analysis with primary forest + category breakdown
    """
    print("\n" + "="*70)
    print("CARD #4: Primary Forest by Land Category (Zonal Analysis)")
    print("="*70)
    
    all_results = []
    
    for province_name, geostore_id in GEOSTORE_IDS.items():
        print(f"\n🏞️ Analyzing primary forest by category for {province_name}...")
        
        url = f"{BASE}/analysis/zonal/{geostore_id}"
        
        params = {
            "sum": ["area__ha"],
            "group_by": ["wdpa_protected_areas__iucn_cat", "gfw_plantations__type"],
            "filters": [
                {
                    "layer": "is__umd_regional_primary_forest_2001",
                    "value": "true"
                }
            ],
            "geostore_origin": "gfw"
        }
        
        headers = {"x-api-key": API_KEY}
        
        try:
            response = requests.post(
                f"{BASE}/analysis/zonal",
                json={
                    "geostore_id": geostore_id,
                    **params
                },
                headers=headers,
                timeout=180
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if 'data' in data and len(data['data']) > 0:
                    df = pd.DataFrame(data['data'])
                    df['province'] = province_name
                    df['is_primary'] = True
                    
                    # Rename columns
                    if 'area__ha' in df.columns:
                        df.rename(columns={'area__ha': 'area_ha'}, inplace=True)
                    
                    all_results.append(df)
                    print(f"  ✅ Got {len(df)} rows")
                else:
                    print(f"  ⚠️ No data returned")
            else:
                print(f"  ❌ Error {response.status_code}: {response.text[:300]}")
                
        except Exception as e:
            print(f"  ❌ Exception: {e}")
        
        time.sleep(3)
    
    if all_results:
        combined = pd.concat(all_results, ignore_index=True)
        
        output_dir = Path("data/raw/klhk_gfw/round5_fixed")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / "primary_forest_by_category_sulawesi.csv"
        combined.to_csv(output_file, index=False)
        
        print(f"\n✅ Card #4 COMPLETED!")
        print(f"   Total rows: {len(combined)}")
        print(f"   File: {output_file}")
        
        # Summary
        if 'wdpa_protected_areas__iucn_cat' in combined.columns and 'area_ha' in combined.columns:
            print(f"\n📊 SUMMARY BY PROTECTED AREA CATEGORY:")
            summary = combined.groupby('wdpa_protected_areas__iucn_cat')['area_ha'].sum().sort_values(ascending=False)
            for cat, area in summary.head(5).items():
                print(f"   Category {cat}: {area:,.0f} ha")
        
        return combined
    else:
        print(f"\n❌ Card #4 FAILED: No data collected")
        return pd.DataFrame()


def main():
    print("\n" + "="*70)
    print("GFW ROUND 5B: FIX VIA ZONAL ANALYSIS")
    print("="*70)
    print(f"API Key: {API_KEY[:20]}...")
    print(f"Method: Zonal Analysis (proven working)")
    print(f"Target: Card #4, #6 (PARTIAL → DONE)")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {}
    
    # Fix partial cards
    print("\n" + "="*70)
    print("FIXING PARTIAL CARDS")
    print("="*70)
    
    results['card_6'] = fix_card_6_primary_loss_by_driver_zonal()
    results['card_4'] = fix_card_4_primary_by_category_zonal()
    
    # Summary
    print("\n" + "="*70)
    print("FINAL SUMMARY")
    print("="*70)
    
    completed = sum(1 for df in results.values() if not df.empty)
    total = len(results)
    
    print(f"\n✅ Completed: {completed}/{total} cards")
    
    for card_name, df in results.items():
        if not df.empty:
            print(f"   {card_name}: ✅ SUCCESS ({len(df)} rows)")
        else:
            print(f"   {card_name}: ❌ FAILED")
    
    # Updated card count
    print("\n" + "="*70)
    print("UPDATED 19 CARDS STATUS")
    print("="*70)
    
    original_done = 11
    original_partial = 2
    original_missing = 6
    
    new_done = original_done + completed
    new_partial = max(0, original_partial - completed)
    new_missing = original_missing
    
    print(f"✅ DONE: {original_done} → {new_done} cards")
    print(f"⚠️ PARTIAL: {original_partial} → {new_partial} cards")
    print(f"❌ MISSING: {original_missing} → {new_missing} cards")
    print(f"\n🎯 TOTAL USABLE: {new_done + new_partial}/19 ({((new_done + new_partial)/19)*100:.1f}%)")
    
    if completed == total:
        print(f"\n🎉 ALL PARTIAL CARDS FIXED!")
        print(f"🎯 NEW COVERAGE: {new_done}/19 = {(new_done/19)*100:.1f}%")
    
    print("\n" + "="*70)
    print("DONE!")
    print("="*70)


if __name__ == "__main__":
    main()
