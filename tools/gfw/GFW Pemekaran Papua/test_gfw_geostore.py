import json
import requests
from pathlib import Path

API_KEY = "21899f40-1f6d-4ff9-93e1-c10d04513984"
BASE = "https://production-api.globalforestwatch.org"

def main():
    geojson_path = Path("indonesia-geojson-topojson-maps-with-38-provinces/GeoJSON/indonesia-38-provinces.geojson")
    with open(geojson_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    print(f"Total features in GeoJSON: {len(data['features'])}")
    
    # Let's see what properties they use for province name
    print("Sample properties:", data['features'][0]['properties'])
    
    # Find Papua Selatan
    papua_selatan = None
    for feat in data['features']:
        prop = feat.get('properties', {})
        name = prop.get('PROVINSI', '')
        if "papua selatan" in str(name).lower():
            papua_selatan = feat
            break
            
    if not papua_selatan:
        print("Papua Selatan not found. Let's list all province names:")
        names = []
        for feat in data['features']:
            prop = feat.get('properties', {})
            name = prop.get('state') or prop.get('name') or prop.get('provinsi') or prop.get('NAME_1') or str(prop)
            names.append(name)
        print(names)
        return

    print(f"Found Papua Selatan! Geometry type: {papua_selatan['geometry']['type']}")
    
    # Prepare payload for GFW
    # GFW requires {"geojson": {"type": "FeatureCollection", "features": [...]}} or just {"geojson": {"type":"Feature", "geometry": ...}}
    # Typically {"geojson": feature} works or {"geojson": {"type": "FeatureCollection", "features": [feature]}}
    BASE_DATA = "https://data-api.globalforestwatch.org"
    
    payload = {
        "geojson": {
            "type": "Feature",
            "geometry": papua_selatan['geometry']
        }
    }
    
    print("\nSending to GFW API...")
    try:
        response = requests.post(
            f"{BASE_DATA}/geostore/",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        if response.status_code in [200, 201]:
            res_data = response.json()
            geostore_id = res_data.get('data', {}).get('id')
            print(f"SUCCESS! Geostore ID: {geostore_id}")
            
            # Let's try querying tree cover loss for this geostore just to be absolutely sure
            print("\nTesting deforestation query on this geostore...")
            query_url = f"{BASE}/v1/analysis/zonal/{geostore_id}"
            params = {
                "sum": ["area__ha"],
                "group_by": ["umd_tree_cover_loss__year"],
                "geostore_origin": "gfw"
            }
            res2 = requests.get(query_url, params=params, headers={"x-api-key": API_KEY})
            print(f"Analysis Status Code: {res2.status_code}")
            if res2.status_code == 200:
                print("Analysis Data sample:", str(res2.json())[:300])
            else:
                print("Analysis Error:", res2.text[:200])
        else:
            print(f"FAILED: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
