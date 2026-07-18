import requests
import re
import urllib3
urllib3.disable_warnings()

r = requests.get('https://tailing.grida.no/', verify=False)
html = r.text
print("HTML Length:", len(html))

# Look for json or endpoints
matches = re.findall(r'[\'"]([^\'"]+\.(?:json|geojson))[\'"]', html)
print("Found JSON references:", matches)

matches2 = re.findall(r'[\'"](/api/[^\'"]+)[\'"]', html)
print("Found API references:", matches2)
