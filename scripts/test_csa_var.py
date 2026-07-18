import requests
API_KEY = '06fd644648629502353deaed29fc6383'
url = f'https://webapi.bps.go.id/v1/api/list/model/var/domain/0000/subjectcsa/531/key/{API_KEY}/'
resp = requests.get(url).json()
print("URL:", url)
print("Keys:", resp.keys())
print("Data:", resp.get('data', []))
