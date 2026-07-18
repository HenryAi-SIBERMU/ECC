import requests

API_KEY = '06fd644648629502353deaed29fc6383'

print("--- CEK PAD (VAR 787) DI DOMAIN 7301 (KAB SELAYAR) ---")
url = f'https://webapi.bps.go.id/v1/api/list/model/data/domain/7301/var/787/th/116/key/{API_KEY}/'
resp = requests.get(url).json()
print("Response 787:", resp.get('status'), resp.get('message', ''))

print("--- CARI SUBJECT DI DOMAIN 7301 ---")
url_sub = f'https://webapi.bps.go.id/v1/api/list/model/subject/domain/7301/key/{API_KEY}/'
subs = requests.get(url_sub).json().get('data', [[], []])[1]
for s in subs[:5]:
    print(s.get('sub_id'), s.get('title'))
