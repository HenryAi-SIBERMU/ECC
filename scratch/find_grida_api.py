import requests
import re
import urllib3
from urllib.parse import urljoin
urllib3.disable_warnings()

base_url = 'https://tailing.grida.no/'
r = requests.get(base_url, verify=False)
html = r.text

js_files = re.findall(r'src=[\'\"]([^\'\"]+\.js)[\'\"]', html)
print("JS Files found:", js_files)

for js in js_files:
    js_url = urljoin(base_url, js)
    print(f"Fetching {js_url}...")
    try:
        js_content = requests.get(js_url, verify=False).text
        # Look for any json or api paths inside the JS
        paths = re.findall(r'[\'"](/?[\w/-]+\.(?:json|geojson))[\'"]', js_content)
        paths.extend(re.findall(r'[\'"](/api/[\w/-]+)[\'"]', js_content))
        if paths:
            print(f"Found paths in {js}: {list(set(paths))}")
    except Exception as e:
        print(f"Error fetching {js}: {e}")
