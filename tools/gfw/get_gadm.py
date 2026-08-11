import requests
import json
for i in range(1, 35):
    try:
        r = requests.get(f"https://production-api.globalforestwatch.org/v2/geostore/admin/IDN/{i}").json()
        name = r.get("data", {}).get("attributes", {}).get("info", {}).get("name")
        h = r.get("data", {}).get("id")
        print(f"{i}: {name} (Hash: {h})")
    except:
        pass
