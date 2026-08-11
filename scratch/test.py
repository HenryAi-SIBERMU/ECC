import requests

url = 'https://data-api.globalforestwatch.org/dataset/tsc_tree_cover_loss_drivers/latest/download_by_aoi/csv'
params = {
    'sql': 'SELECT umd_tree_cover_loss__year as year, tsc_tree_cover_loss_drivers__type as driver, sum(area__ha) as area_ha FROM data GROUP BY umd_tree_cover_loss__year, tsc_tree_cover_loss_drivers__type',
    'aoi': '{"type":"admin","country":"IDN","region":"26"}'
}
headers = {'x-api-key': '21899f40-1f6d-4ff9-93e1-c10d04513984'}

try:
    r = requests.get(url, params=params, headers=headers)
    print("Status:", r.status_code)
    print("Output:", r.text[:500])
except Exception as e:
    print("Error:", e)
