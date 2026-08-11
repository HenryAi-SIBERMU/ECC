import requests

r = requests.get('https://production-api.globalforestwatch.org/v2/geostore/admin/IDN/26')
if r.status_code == 200:
    subregions = r.json().get('data', {}).get('attributes', {}).get('subregions', {})
    print(f"Found {len(subregions)} subregions for Sulsel:")
    for k, v in list(subregions.items())[:10]:
        print(f"  Kabupaten ID {k}: {v.get('name')}")
