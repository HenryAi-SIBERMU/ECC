import requests
API_KEY = '06fd644648629502353deaed29fc6383'
domain_id = '1100'
url = f'https://webapi.bps.go.id/v1/api/list/model/subject/domain/{domain_id}/key/{API_KEY}/'
resp = requests.get(url).json()
subs = resp.get('data', [])[1]
print("ACEH SUBJECTS:")
for s in subs:
    print(f"[{s['sub_id']}] {s['title']}")
