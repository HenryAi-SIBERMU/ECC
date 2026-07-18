"""
FIX MISSING & PARTIAL GFW CARDS
================================

Attempt to complete missing cards via API retry with corrected parameters.

Target Cards:
- Card #4: Primary Forest by Category (need new fetch with primary flag)
- Card #6: Primary Loss by Driver (need refetch with primary filter)
- Card #11: Primary Loss in Protected Areas (cross-reference)
- Card #12: Fire Alerts (fix SQL query)
- Card #13: GLAD Alerts (try different version)
- Card #16: Current Tree Cover (calculation)

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

GEOSTORE_IDS = {
    "Sulawesi Utara": "89b35f128c9cfe7685e1738c89a0a730",
    "Sulawesi Tengah": "fce1e175169936334347ae17207381a0",
    "Sulawesi Selatan": "abc6fc008f433d3dbdc65861bdcc8a87",
    "Sulawesi Tenggara": "fe2e396191a0e8b6e70aa03dd225d7f7",
    "Gorontalo": "db937e7121c426140dd91072c14bbdaf",
    "Sulawesi Barat": "77f83070a9b4111e24a7cfdea73a5adb"
}


def fix_card_11_cross_reference():
    """
    Card #11: Primary Loss in Protected Areas
    Strategy: Cross-reference primary_forest_loss + loss_in_protected_areas
    """
    print("\n" + "="*70)
    print("CARD #11: Primary Loss in Protected Areas")
    print("="*70)
    
    # Load datasets
    primary_loss = pd.read_csv("data/raw/klhk_gfw/mega_fetch_v2/primary_forest_loss_sulawesi_2001_2025.csv")
    protected_loss = pd.read_csv("data/raw/klhk_gfw/mega_fetch_v2/loss_in_protected_areas_sulawesi_2001_2025.csv")
    
    print(f"Primary loss data: {len(primary_loss)} rows")
    print(f"Protected areas loss: {len(protected_loss)} rows")
    
    # Filter primary forest only
    if 'is__umd_regional_primary_forest_2001' in primary_loss.columns:
        primary_only = primary_loss[primary_loss['is__umd_regional_primary_forest_2001'] == True].copy()
        print(f"Primary forest rows: {len(primary_only)}")
        
        # Check if protected_loss has protected area names
        print(f"\nProtected loss columns: {protected_loss.columns.tolist()}")
        
        # For now, just aggregate primary loss (assuming it overlaps with protected areas)
        # This is a PROXY - not perfect cross-reference
        result = primary_only.groupby(['province', 'year']).agg({
            'area__ha': 'sum'
        }).reset_index()
        
        result.rename(columns={'area__ha': 'primary_loss_ha'}, inplace=True)
        
        output_dir = Path("data/raw/klhk_gfw/fixed_cards")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / "primary_loss_in_protected_areas_proxy.csv"
        result.to_csv(output_file, index=False)
        
        print(f"\n✅ Card #11 PROXY created: {len(result)} rows")
        print(f"   File: {output_file}")
        print(f"   ⚠️ NOTE: This is proxy data (primary loss aggregated)")
        print(f"   ⚠️ For accurate data, need GFW API endpoint that combines both filters")
        
        return result
    else:
        print("❌ No primary forest flag found")
        return pd.DataFrame()


def fix_card_12_fire_alerts():
    """
    Card #12: Fire Alerts
    Strategy: Use NASA FIRMS or VIIRS dataset via GFW
    """
    print("\n" + "="*70)
    print("CARD #12: Fire Alerts (VIIRS)")
    print("="*70)
    
    # Try VIIRS fire alerts via query endpoint
    all_results = []
    
    for province_name, geostore_id in GEOSTORE_IDS.items():
        print(f"\n🔥 Fetching fire alerts for {province_name}...")
        
        # Try using fire_alerts_viirs dataset
        sql = f"""
        SELECT 
            '{province_name}' as province,
            alert__date as date,
            COUNT(*) as alert_count,
            AVG(alert__bright_ti4) as avg_brightness
        FROM fire_alerts_viirs
        WHERE alert__date >= '2016-01-01' 
          AND alert__date <= '2024-12-31'
        GROUP BY alert__date
        ORDER BY alert__date
        """
        
        payload = {
            "geostore_id": geostore_id,
            "sql": sql
        }
        
        headers = {
            "x-api-key": API_KEY,
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                f"{BASE}/dataset/fire_alerts_viirs/latest/query",
                json=payload,
                headers=headers,
                timeout=120
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and len(data['data']) > 0:
                    df = pd.DataFrame(data['data'])
                    all_results.append(df)
                    print(f"  ✅ Got {len(df)} rows")
                else:
                    print(f"  ⚠️ No data returned")
            else:
                print(f"  ❌ Error {response.status_code}: {response.text[:200]}")
                
        except Exception as e:
            print(f"  ❌ Exception: {e}")
        
        time.sleep(2)
    
    if all_results:
        combined = pd.concat(all_results, ignore_index=True)
        
        output_dir = Path("data/raw/klhk_gfw/fixed_cards")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / "fire_alerts_viirs_sulawesi_2016_2024.csv"
        combined.to_csv(output_file, index=False)
        
        print(f"\n✅ Card #12 COMPLETED: {len(combined)} rows")
        print(f"   File: {output_file}")
        return combined
    else:
        print(f"\n❌ Card #12 FAILED: No data collected")
        return pd.DataFrame()


def fix_card_13_glad_alerts():
    """
    Card #13: GLAD Alerts
    Strategy: Try different dataset versions or integrated_alerts
    """
    print("\n" + "="*70)
    print("CARD #13: GLAD Deforestation Alerts")
    print("="*70)
    
    # Try integrated_deforestation_alerts instead
    all_results = []
    
    for province_name, geostore_id in GEOSTORE_IDS.items():
        print(f"\n🚨 Fetching GLAD alerts for {province_name}...")
        
        sql = f"""
        SELECT 
            '{province_name}' as province,
            alert__date as date,
            umd_tree_cover_loss__year as year,
            SUM(area__ha) as alert_area_ha
        FROM integrated_deforestation_alerts
        WHERE umd_tree_cover_loss__year >= 2016
          AND umd_tree_cover_loss__year <= 2024
        GROUP BY alert__date, umd_tree_cover_loss__year
        ORDER BY alert__date
        """
        
        payload = {
            "geostore_id": geostore_id,
            "sql": sql
        }
        
        headers = {
            "x-api-key": API_KEY,
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                f"{BASE}/dataset/integrated_deforestation_alerts/latest/query",
                json=payload,
                headers=headers,
                timeout=120
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and len(data['data']) > 0:
                    df = pd.DataFrame(data['data'])
                    all_results.append(df)
                    print(f"  ✅ Got {len(df)} rows")
                else:
                    print(f"  ⚠️ No data returned")
            else:
                print(f"  ❌ Error {response.status_code}: {response.text[:200]}")
                
        except Exception as e:
            print(f"  ❌ Exception: {e}")
        
        time.sleep(2)
    
    if all_results:
        combined = pd.concat(all_results, ignore_index=True)
        
        output_dir = Path("data/raw/klhk_gfw/fixed_cards")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / "glad_alerts_sulawesi_2016_2024.csv"
        combined.to_csv(output_file, index=False)
        
        print(f"\n✅ Card #13 COMPLETED: {len(combined)} rows")
        print(f"   File: {output_file}")
        return combined
    else:
        print(f"\n❌ Card #13 FAILED: No data collected")
        return pd.DataFrame()


def fix_card_16_calculate_current():
    """
    Card #16: Current Tree Cover
    Strategy: Calculate = extent_2000 - cumulative_loss + gain
    """
    print("\n" + "="*70)
    print("CARD #16: Current Tree Cover (Calculated)")
    print("="*70)
    
    # Load data
    extent = pd.read_csv("data/raw/klhk_gfw/complete_fetch/tree_cover_extent_sulawesi_2001_2025.csv")
    loss = pd.read_csv("data/raw/klhk_gfw/mega_fetch_v2/tree_cover_loss_sulawesi_2001_2025.csv")
    gain = pd.read_csv("data/raw/klhk_gfw/mega_fetch_v2/tree_cover_gain_sulawesi_2001_2025.csv")
    
    print(f"Extent data: {len(extent)} rows")
    print(f"Loss data: {len(loss)} rows")
    print(f"Gain data: {len(gain)} rows")
    
    # Get baseline (year 2000)
    baseline = extent[extent['year'] == 2000].copy()
    baseline = baseline[['province', 'tree_cover_2000_ha']].copy()
    baseline.rename(columns={'tree_cover_2000_ha': 'extent_2000_ha'}, inplace=True)
    
    # Calculate cumulative loss per province
    cumulative_loss = loss.groupby('province')['tree_cover_loss_ha'].sum().reset_index()
    cumulative_loss.rename(columns={'tree_cover_loss_ha': 'total_loss_ha'}, inplace=True)
    
    # Get total gain per province (check column name first)
    gain_col = 'tree_cover_gain_ha' if 'tree_cover_gain_ha' in gain.columns else 'gain_area_ha'
    if gain_col in gain.columns:
        total_gain = gain.groupby('province')[gain_col].sum().reset_index()
        total_gain.rename(columns={gain_col: 'total_gain_ha'}, inplace=True)
    else:
        print(f"⚠️ Gain columns: {gain.columns.tolist()}")
        total_gain = pd.DataFrame({'province': baseline['province'].unique(), 'total_gain_ha': 0})
    
    # Merge
    result = baseline.merge(cumulative_loss, on='province', how='left')
    result = result.merge(total_gain, on='province', how='left')
    
    # Fill NaN with 0
    result['total_loss_ha'] = result['total_loss_ha'].fillna(0)
    result['total_gain_ha'] = result['total_gain_ha'].fillna(0)
    
    # Calculate current tree cover
    result['current_tree_cover_ha'] = result['extent_2000_ha'] - result['total_loss_ha'] + result['total_gain_ha']
    result['year'] = 2024  # Current year
    
    # Select columns
    result = result[['province', 'year', 'extent_2000_ha', 'total_loss_ha', 'total_gain_ha', 'current_tree_cover_ha']]
    
    output_dir = Path("data/raw/klhk_gfw/fixed_cards")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "current_tree_cover_calculated_2024.csv"
    result.to_csv(output_file, index=False)
    
    print(f"\n✅ Card #16 COMPLETED: {len(result)} rows")
    print(f"   File: {output_file}")
    print(f"\n📊 SUMMARY:")
    for _, row in result.iterrows():
        print(f"   {row['province']}: {row['current_tree_cover_ha']:,.0f} ha")
    
    return result


def main():
    print("\n" + "="*70)
    print("FIX MISSING & PARTIAL GFW CARDS")
    print("="*70)
    print(f"API Key: {API_KEY[:20]}...")
    print(f"Target: Complete missing cards via API retry")
    
    results = {}
    
    # Fix calculable cards first
    print("\n" + "="*70)
    print("PHASE 1: CALCULABLE CARDS (No API needed)")
    print("="*70)
    
    results['card_16'] = fix_card_16_calculate_current()
    results['card_11'] = fix_card_11_cross_reference()
    
    # Fix API-dependent cards
    print("\n" + "="*70)
    print("PHASE 2: API RETRY CARDS")
    print("="*70)
    
    results['card_12'] = fix_card_12_fire_alerts()
    results['card_13'] = fix_card_13_glad_alerts()
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    completed = sum(1 for df in results.values() if not df.empty)
    total = len(results)
    
    print(f"✅ Completed: {completed}/{total} cards")
    
    for card_name, df in results.items():
        status = "✅ SUCCESS" if not df.empty else "❌ FAILED"
        rows = len(df) if not df.empty else 0
        print(f"   {card_name}: {status} ({rows} rows)")
    
    print("\n" + "="*70)
    print("REMAINING ISSUES:")
    print("="*70)
    print("⚠️ Card #4 & #6: Need API refetch with primary forest filter")
    print("⚠️ Card #9: Biomass Loss - Invalid layer (may need manual)")
    print("⚠️ Card #11: Currently proxy - need proper API endpoint")
    
    print("\n" + "="*70)
    print("DONE!")
    print("="*70)


if __name__ == "__main__":
    main()
