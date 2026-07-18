import requests
import json

API_KEY = '06fd644648629502353deaed29fc6383'

def check_var(var_id):
    url = f'https://webapi.bps.go.id/v1/api/list/model/data/domain/0000/var/{var_id}/key/{API_KEY}/'
    resp = requests.get(url).json()
    if 'data' in resp and len(resp['data']) > 1:
        data = resp['data'][1]
        print(f"\n=== VAR ID {var_id} ===")
        # Print first 2 data points
        for i, (k, v) in enumerate(data.items()):
            if i < 2:
                print(f"{k}: {v}")
            else:
                break
        
        # Check what dimensions are available
        url_vervar = f'https://webapi.bps.go.id/v1/api/list/model/vervar/domain/0000/var/{var_id}/key/{API_KEY}/'
        vervar_resp = requests.get(url_vervar).json()
        if 'data' in vervar_resp and len(vervar_resp['data']) > 1:
            print("Karakteristik vertikal (Vervar):")
            for vv in vervar_resp['data'][1][:3]: # print first 3
                print(vv)
                
        url_turvar = f'https://webapi.bps.go.id/v1/api/list/model/turvar/domain/0000/var/{var_id}/key/{API_KEY}/'
        turvar_resp = requests.get(url_turvar).json()
        if 'data' in turvar_resp and len(turvar_resp['data']) > 1:
            print("Karakteristik turunan (Turvar):")
            for tv in turvar_resp['data'][1][:3]:
                print(tv)

check_var(787)
check_var(2346)
check_var(2347)
check_var(2310)
