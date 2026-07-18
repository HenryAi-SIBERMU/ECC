"""
GFW ROUND 5: FIX PARTIAL & MISSING CARDS
==========================================

Target:
- Card #6: Primary Forest Loss by Driver (SQL with primary filter)
- Card #9: Biomass Loss (calculate from existing data)
- Card #12: Fire Alerts (NASA FIRMS API)

Author: CELIOS Research
Date: 14 Juni 2026
"""

import requests
import pandas as pd
import json
from pathlib import Path
import time
from datetime import datetime, timedelta

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


def fix_card_6_primary_loss_by_driver_sql():
    """
    Card #6: Primary Forest Loss by Driver
    Strategy: Use SQL query with explicit primary forest filter
    """
    print("\n" + "="*70)
    print("CARD #6: Primary Forest Loss by Driver (SQL Query)")
    print("="*70)
    
    all_results = []
    
    for province_name, geostore_id in GEOSTORE_IDS.items():
        print(f"\n🌳 Querying primary forest loss drivers for {province_name}...")
        
        # SQL with PRIMARY FOREST filter
        sql = """
        SELECT 
            umd_tree_cover_loss__year as year,
            tsc_tree_cover_loss_drivers__type as driver,
            SUM(area__ha) as area_ha,
            SUM(whrc_aboveground_co2_emissions__Mg) as co2_emissions_mg
        FROM data
        WHERE is__umd_regional_primary_forest_2001 = true
          AND umd_tree_cover_loss__year >= 2001
          AND umd_tree_cover_loss__year <= 2023
        GROUP BY umd_tree_cover_loss__year, tsc_tree_cover_loss_drivers__type
        ORDER BY umd_tree_cover_loss__year, tsc_tree_cover_loss_drivers__type
        """
        
        headers = {
            "x-api-key": API_KEY,
            "Content-Type": "application/json"
        }
        
        try:
            # Use GET with query params instead of POST with body
            response = requests.get(
                f"{BASE}/dataset/tsc_tree_cover_loss_drivers/latest/query/json",
                params={
                    "sql": sql,
                    "geostore_id": geostore_id,
                    "geostore_origin": "gfw"
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
                    all_results.append(df)
                    print(f"  ✅ Got {len(df)} rows")
                else:
                    print(f"  ⚠️ No data returned (status: {data.get('status')})")
            else:
                print(f"  ❌ Error {response.status_code}: {response.text[:300]}")
                
        except Exception as e:
            print(f"  ❌ Exception: {e}")
        
        time.sleep(3)  # Rate limiting
    
    if all_results:
        combined = pd.concat(all_results, ignore_index=True)
        
        # Reorder columns
        combined = combined[['province', 'year', 'driver', 'area_ha', 'co2_emissions_mg', 'is_primary']]
        
        output_dir = Path("data/raw/klhk_gfw/round5_fixed")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / "primary_forest_loss_by_driver_sulawesi_2001_2023.csv"
        combined.to_csv(output_file, index=False)
        
        print(f"\n✅ Card #6 COMPLETED!")
        print(f"   Total rows: {len(combined)}")
        print(f"   File: {output_file}")
        
        # Summary
        print(f"\n📊 SUMMARY BY DRIVER:")
        summary = combined.groupby('driver')['area_ha'].sum().sort_values(ascending=False)
        for driver, area in summary.items():
            print(f"   {driver}: {area:,.0f} ha")
        
        return combined
    else:
        print(f"\n❌ Card #6 FAILED: No data collected")
        return pd.DataFrame()


def fix_card_9_biomass_loss_calculate():
    """
    Card #9: Biomass Loss
    Strategy: Calculate from tree cover loss × biomass stock 2000
    """
    print("\n" + "="*70)
    print("CARD #9: Biomass Loss (Calculated)")
    print("="*70)
    
    all_results = []
    
    for province_name, geostore_id in GEOSTORE_IDS.items():
        print(f"\n🌲 Calculating biomass loss for {province_name}...")
        
        # SQL to get loss area × biomass stock
        sql = """
        SELECT 
            umd_tree_cover_loss__year as year,
            SUM(area__ha) as loss_area_ha,
            AVG(whrc_aboveground_biomass_stock_2000__Mg_ha-1) as avg_biomass_stock_mg_ha,
            SUM(area__ha * whrc_aboveground_biomass_stock_2000__Mg_ha-1) as total_biomass_loss_mg
        FROM data
        WHERE umd_tree_cover_loss__year >= 2001
          AND umd_tree_cover_loss__year <= 2023
        GROUP BY umd_tree_cover_loss__year
        ORDER BY umd_tree_cover_loss__year
        """
        
        headers = {
            "x-api-key": API_KEY,
            "Content-Type": "application/json"
        }
        
        try:
            # Use GET with query params
            response = requests.get(
                f"{BASE}/dataset/umd_tree_cover_loss/latest/query/json",
                params={
                    "sql": sql,
                    "geostore_id": geostore_id,
                    "geostore_origin": "gfw"
                },
                headers=headers,
                timeout=180
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if 'data' in data and len(data['data']) > 0:
                    df = pd.DataFrame(data['data'])
                    df['province'] = province_name
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
        
        # Reorder columns
        combined = combined[['province', 'year', 'loss_area_ha', 'avg_biomass_stock_mg_ha', 'total_biomass_loss_mg']]
        
        output_dir = Path("data/raw/klhk_gfw/round5_fixed")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / "biomass_loss_sulawesi_2001_2023.csv"
        combined.to_csv(output_file, index=False)
        
        print(f"\n✅ Card #9 COMPLETED!")
        print(f"   Total rows: {len(combined)}")
        print(f"   File: {output_file}")
        
        # Summary
        print(f"\n📊 SUMMARY BY PROVINCE:")
        summary = combined.groupby('province')['total_biomass_loss_mg'].sum().sort_values(ascending=False)
        for prov, biomass in summary.items():
            print(f"   {prov}: {biomass:,.0f} Mg")
        
        return combined
    else:
        print(f"\n❌ Card #9 FAILED: No data collected")
        return pd.DataFrame()


def fix_card_12_fire_alerts_nasa_firms():
    """
    Card #12: Fire Alerts
    Strategy: Use NASA FIRMS API (VIIRS)
    """
    print("\n" + "="*70)
    print("CARD #12: Fire Alerts (NASA FIRMS)")
    print("="*70)
    print("⚠️ NASA FIRMS API requires registration at https://firms.modaps.eosdis.nasa.gov/api/")
    print("⚠️ This endpoint is FREE but needs API key (different from GFW)")
    print("⚠️ For now, trying GFW's VIIRS dataset via direct query...")
    
    all_results = []
    
    for province_name, geostore_id in GEOSTORE_IDS.items():
        print(f"\n🔥 Querying fire alerts for {province_name}...")
        
        # Try getting fire count aggregated by year
        sql = """
        SELECT 
            EXTRACT(YEAR FROM alert__date) as year,
            COUNT(*) as fire_count,
            AVG(alert__bright_ti4) as avg_brightness,
            AVG(alert__confidence) as avg_confidence
        FROM data
        WHERE alert__date >= '2016-01-01'
          AND alert__date <= '2023-12-31'
        GROUP BY EXTRACT(YEAR FROM alert__date)
        ORDER BY year
        """
        
        headers = {
            "x-api-key": API_KEY,
            "Content-Type": "application/json"
        }
        
        try:
            # Use GET with query params
            response = requests.get(
                f"{BASE}/dataset/nasa_viirs_fire_alerts/latest/query/json",
                params={
                    "sql": sql,
                    "geostore_id": geostore_id,
                    "geostore_origin": "gfw"
                },
                headers=headers,
                timeout=180
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if 'data' in data and len(data['data']) > 0:
                    df = pd.DataFrame(data['data'])
                    df['province'] = province_name
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
        
        # Reorder columns
        combined = combined[['province', 'year', 'fire_count', 'avg_brightness', 'avg_confidence']]
        
        output_dir = Path("data/raw/klhk_gfw/round5_fixed")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / "fire_alerts_viirs_sulawesi_2016_2023.csv"
        combined.to_csv(output_file, index=False)
        
        print(f"\n✅ Card #12 COMPLETED!")
        print(f"   Total rows: {len(combined)}")
        print(f"   File: {output_file}")
        
        # Summary
        print(f"\n📊 SUMMARY BY PROVINCE:")
        summary = combined.groupby('province')['fire_count'].sum().sort_values(ascending=False)
        for prov, count in summary.items():
            print(f"   {prov}: {count:,.0f} fire alerts")
        
        return combined
    else:
        print(f"\n❌ Card #12 FAILED: No data collected")
        print(f"\n💡 ALTERNATIVE: Use NASA FIRMS API directly")
        print(f"   URL: https://firms.modaps.eosdis.nasa.gov/api/area/csv/MAP_KEY/VIIRS_SNPP_NRT/...")
        return pd.DataFrame()


def main():
    print("\n" + "="*70)
    print("GFW ROUND 5: FIX PARTIAL & MISSING CARDS")
    print("="*70)
    print(f"API Key: {API_KEY[:20]}...")
    print(f"Target: Complete Card #6, #9, #12")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {}
    
    # Phase 1: SQL-based fixes
    print("\n" + "="*70)
    print("PHASE 1: SQL QUERY FIXES")
    print("="*70)
    
    results['card_6'] = fix_card_6_primary_loss_by_driver_sql()
    results['card_9'] = fix_card_9_biomass_loss_calculate()
    
    # Phase 2: Fire alerts
    print("\n" + "="*70)
    print("PHASE 2: FIRE ALERTS")
    print("="*70)
    
    results['card_12'] = fix_card_12_fire_alerts_nasa_firms()
    
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
    new_partial = max(0, original_partial - (1 if not results['card_6'].empty else 0))
    new_missing = original_missing - (1 if not results['card_9'].empty else 0) - (1 if not results['card_12'].empty else 0)
    
    print(f"✅ DONE: {original_done} → {new_done} cards")
    print(f"⚠️ PARTIAL: {original_partial} → {new_partial} cards")
    print(f"❌ MISSING: {original_missing} → {new_missing} cards")
    print(f"\n🎯 TOTAL USABLE: {new_done + new_partial}/19 ({((new_done + new_partial)/19)*100:.1f}%)")
    
    print("\n" + "="*70)
    print("DONE!")
    print("="*70)


if __name__ == "__main__":
    main()
