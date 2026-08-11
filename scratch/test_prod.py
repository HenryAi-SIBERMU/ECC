import requests

# Test legacy production-api endpoints used by the GFW Web App Frontend
url1 = 'https://production-api.globalforestwatch.org/v1/dataset/tree-cover-loss/widget/treeCoverLossByDriverGrouped?adm0=IDN&adm1=26'
url2 = 'https://production-api.globalforestwatch.org/v1/gfw-metadata'

r1 = requests.get(url1)
print("Widget API Status:", r1.status_code)
if r1.status_code == 200:
    print("Widget API Data:", r1.text[:500])

# Check GFW dashboard page for IDN 26 (Sulsel)
dash_url = 'https://www.globalforestwatch.org/dashboards/country/IDN/26/'
r_dash = requests.get(dash_url)
print("Dashboard URL Status:", r_dash.status_code)
