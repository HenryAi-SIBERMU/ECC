"""
Direct check BPS API - try different approaches
"""
import requests
import json

API_KEY = "06fd644648629502353deaed29fc6383"
BASE_URL = "https://webapi.bps.go.id/v1/api"

print("="*80)
print("BPS API DIRECT CHECK - INVESTMENT DATA")
print("="*80)

# Try 1: Check subject/category list
print("\n1. Checking subject categories...")
url = f"{BASE_URL}/subject"
params = {"key": API_KEY, "type": "all"}

try:
    r = requests.get(url, params=params, timeout=30)
    data = r.json()
    
    if data.get("status") == "OK":
        subjects = data.get("data", [[]])[1]
        print(f"   Found {len(subjects)} subjects")
        
        # Filter for investment/pertambangan
        inv_subjects = [s for s in subjects if any(k in str(s).lower() for k in ['invest', 'modal', 'tambang', 'pertambangan'])]
        
        if inv_subjects:
            print(f"\n   Investment/Mining related subjects:")
            for subj in inv_subjects[:10]:
                print(f"   - {subj}")
        else:
            print("\n   ❌ No investment/mining subjects found in list")
            print(f"\n   Sample subjects (first 10):")
            for subj in subjects[:10]:
                print(f"   - {subj}")
    else:
        print(f"   ❌ Status: {data.get('status')}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Try 2: Direct data query with model keywords
print("\n2. Trying direct data queries...")

# Common BPS model keywords for investment
models_to_try = [
    "pmdn",  # Penanaman Modal Dalam Negeri
    "pma",   # Penanaman Modal Asing  
    "investasi",
    "realisasi_investasi"
]

for model in models_to_try:
    print(f"\n   Trying model: {model}")
    url = f"{BASE_URL}/data"
    params = {
        "key": API_KEY,
        "model": model,
        "domain": "0000"  # National
    }
    
    try:
        r = requests.get(url, params=params, timeout=30)
        data = r.json()
        
        if data.get("status") == "OK":
            records = data.get("data", [])
            if records:
                print(f"   ✅ Found {len(records)} records!")
                print(f"   Sample (first entry):")
                print(json.dumps(records[0], indent=2, ensure_ascii=False))
                break
            else:
                print(f"   ⚠️  Status OK but no data")
        else:
            print(f"   ❌ Status: {data.get('status')}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

# Try 3: Check what PMDN data we already have
print("\n" + "="*80)
print("3. Checking existing BPS PMDN data (yang udah di-download)")
print("="*80)

import csv

try:
    with open('data/raw/bps_pmdn/bps_investasi_pmdn_sulawesi_2016_2026.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
        print(f"\n✅ Found existing PMDN data: {len(rows)} rows")
        print(f"\nColumns: {list(rows[0].keys())}")
        print(f"\nSample data (first 5 rows):")
        for i, row in enumerate(rows[:5], 1):
            print(f"\n{i}. {row['provinsi']} | {row['tahun']} | {row['indikator']}")
            print(f"   Nilai: {row['nilai']} {row['satuan']}")
        
        # Check if there's sector breakdown
        unique_indicators = set([r['indikator'] for r in rows])
        print(f"\nUnique indicators ({len(unique_indicators)}):")
        for ind in sorted(unique_indicators):
            print(f"   - {ind}")
        
except FileNotFoundError:
    print("   ❌ File not found")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "="*80)
print("KESIMPULAN")
print("="*80)
print("""
1. BPS API dynamic tables: TIDAK TERSEDIA (list-not-available)
2. Direct data queries: Perlu model/endpoint yang tepat
3. Existing PMDN data: TERSEDIA tapi agregat (semua sektor, bukan mining specific)

RECOMMENDATION:
- BPS PMDN data yang ada = agregat level provinsi (SEMUA SEKTOR)
- Untuk investment mining-specific, TIDAK ADA di BPS API
- Alternative: IDX annual reports, company websites, manual extraction
""")
