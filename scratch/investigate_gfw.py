import requests
import json
import pandas as pd

API_KEY = "21899f40-1f6d-4ff9-93e1-c10d04513984"
BASE = "https://data-api.globalforestwatch.org"

def check_admin_regions():
    print("Checking admin regions...")
    # Iterate through IDs 1 to 40 to find all Papua-related names
    papua_ids = {}
    for i in range(1, 40):
        url = f"https://production-api.globalforestwatch.org/v2/geostore/admin/IDN/{i}"
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                name = res.json().get('data', {}).get('info', {}).get('name', '')
                if 'papua' in name.lower():
                    papua_ids[i] = name
        except Exception:
            pass
    print("Found Papua regions in GFW GADM:", papua_ids)
    return papua_ids

def test_api_grouping():
    # Test grouping for primary forest loss to see the raw output format
    geostore = "8bec56e0cb4d6c64073c35b61facb7db" # Papua
    endpoint = f"{BASE}/analysis/zonal/{geostore}"
    params = [
        ('sum', 'area__ha'),
        ('group_by', 'umd_tree_cover_loss__year'),
        ('group_by', 'is__umd_regional_primary_forest_2001'),
        ('geostore_origin', 'gfw')
    ]
    headers = {"x-api-key": API_KEY}
    res = requests.get(endpoint, params=params, headers=headers)
    if res.status_code == 200:
        data = res.json().get('data', [])
        print("\nRaw API Response for Primary Forest Loss (first 5 records):")
        for d in data[:5]:
            print(d)
    else:
        print("API Error:", res.text)

if __name__ == "__main__":
    check_admin_regions()
    test_api_grouping()
