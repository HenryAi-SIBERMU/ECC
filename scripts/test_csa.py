import requests
API_KEY = '06fd644648629502353deaed29fc6383'

def fetch_csa(domain):
    url = f'https://webapi.bps.go.id/v1/api/list/model/subjectcsa/domain/{domain}/key/{API_KEY}/'
    resp = requests.get(url).json()
    data = resp.get('data', [])
    if len(data) > 1 and isinstance(data[1], list):
        return [s.get('title') for s in data[1][:5]]
    return "None"

print("Nasional (0000):", fetch_csa("0000"))
print("Aceh (1100):", fetch_csa("1100"))
print("Sumut (1200):", fetch_csa("1200"))
