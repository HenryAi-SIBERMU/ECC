import requests

url = 'https://data-api.globalforestwatch.org/dataset/umd_tree_cover_loss/latest/download_by_aoi/csv'
params = {
    'sql': 'SELECT umd_tree_cover_loss__year, SUM(area__ha) FROM data GROUP BY umd_tree_cover_loss__year',
    'aoi': '{"type":"admin","country":"IDN","region":"26"}'
}
headers = {'x-api-key': '21899f40-1f6d-4ff9-93e1-c10d04513984'}

try:
    r = requests.get(url, params=params, headers=headers)
    print("Status:", r.status_code)
    print("Output:", r.text[:300])
except Exception as e:
    print("Error:", e)
