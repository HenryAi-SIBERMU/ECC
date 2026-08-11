import requests
import json

def get_aoi_list():
    print("Mendapatkan list AOI (Area of Interest) untuk Indonesia (IDN)...")
    results = []
    
    # GADM 3.6 for Indonesia has 34 provinces (Admin 1)
    for i in range(1, 35):
        try:
            r = requests.get(f"https://production-api.globalforestwatch.org/v2/geostore/admin/IDN/{i}").json()
            
            # Extract data
            name = r.get("data", {}).get("attributes", {}).get("info", {}).get("name", "Unknown")
            hash_id = r.get("data", {}).get("id", "Unknown")
            
            if name != "Unknown":
                results.append({
                    "id": i,
                    "name": name,
                    "hash": hash_id,
                    "aoi_payload": {"type": "admin", "country": "IDN", "region": str(i)}
                })
                print(f"✅ Ditemukan: {name} (ID: {i})")
        except Exception as e:
            pass
            
    # Simpan ke JSON
    with open('data/idn_aoi_list.json', 'w') as f:
        json.dump(results, f, indent=4)
        
    print("\nBerhasil! List AOI disimpan di data/idn_aoi_list.json")
    
if __name__ == "__main__":
    get_aoi_list()
