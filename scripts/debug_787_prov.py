import requests

API_KEY = "06fd644648629502353deaed29fc6383"

# Cek full response structure dari domain 7300 var 787
url = f"https://webapi.bps.go.id/v1/api/list/model/data/domain/7300/var/787/th/116/key/{API_KEY}/"
resp = requests.get(url).json()

print("Keys at top level:", list(resp.keys()))
print("Data-availability:", resp.get('data-availability'))

# Print datacontent raw
dc = resp.get('datacontent')
print("Datacontent type:", type(dc))
print("Datacontent:", dc)

# Print data
data_field = resp.get('data')
print("\nData field type:", type(data_field))
if isinstance(data_field, list):
    print("Data field len:", len(data_field))
    for i, item in enumerate(data_field):
        print(f"data[{i}] type:", type(item))
        if isinstance(item, dict):
            for k2, v2 in list(item.items())[:5]:
                print(f"  {k2}: {str(v2)[:200]}")
        elif isinstance(item, list):
            print(f"  len={len(item)}, first 3:", item[:3])
