import requests

API_KEY = '06fd644648629502353deaed29fc6383'

def check_var(var_id):
    print(f"\n--- Mengambil Var ID: {var_id} ---")
    url = f'https://webapi.bps.go.id/v1/api/list/model/data/domain/0000/var/{var_id}/key/{API_KEY}/'
    print("URL:", url)
    
    try:
        resp = requests.get(url, timeout=30)
        js = resp.json()
        print("Status BPS:", js.get('status', 'No status field'))
        if 'data' in js and len(js['data']) > 1:
            data = js['data'][1]
            print(f"Data tersimpan: {len(data)} items")
            count = 0
            for k, v in data.items():
                print(f"  {k}: {v}")
                count += 1
                if count >= 2: break
        else:
            print("Tidak ada data atau format berbeda.")
            print("Message:", js.get('message'))
    except Exception as e:
        print("Error fetching data:", e)

check_var(787)
