import requests
import urllib3
urllib3.disable_warnings()

BASE_URL = 'https://webapi.bps.go.id/v1/api/interoperabilitas/datasource/simdasi'
headers = {'User-Agent': 'Mozilla/5.0'}
wilayah_id = '7200' # Sulteng

# 1. Get Subjects
url_sub = f'{BASE_URL}/id/22/wilayah/{wilayah_id}/'
res = requests.get(url_sub, headers=headers, verify=False, timeout=10)
data = res.json()
print("Response from API:", data)
