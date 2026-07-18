import requests

API_KEY = '06fd644648629502353deaed29fc6383'

def check_var_th(var_id, th='116'):
    print(f"\n--- Mengambil Var ID: {var_id} Tahun: 2016 ---")
    url = f'https://webapi.bps.go.id/v1/api/list/model/data/domain/0000/var/{var_id}/th/{th}/key/{API_KEY}/'
    
    try:
        resp = requests.get(url, timeout=30).json()
        if resp.get('data-availability') == 'available':
            print("Data Available!")
            vervars = resp.get("vervar", [])
            turvars = resp.get("turvar", [])
            print(f"Jumlah Vervar (Vertikal): {len(vervars)}")
            for v in vervars[:3]: print("  -", v['label'])
            print(f"Jumlah Turvar (Turunan): {len(turvars)}")
            for t in turvars[:3]: print("  -", t['label'])
        else:
            print("Not available:", resp.get('message', 'No message'))
    except Exception as e:
        print("Error:", e)

check_var_th(787)   # PAD
check_var_th(2346)  # Ekspor
check_var_th(2347)
check_var_th(1079)  # Pemerintahan Desa?
check_var_th(2389)
