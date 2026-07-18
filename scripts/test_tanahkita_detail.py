import requests
from bs4 import BeautifulSoup
import json

url = "https://tanahkita.id/data/konflik/detil/S2QwbDdDLWttVEk"
response = requests.get(url, verify=False)
soup = BeautifulSoup(response.content, 'html.parser')

data = {}
tables = soup.find_all('table')
for table in tables:
    for row in table.find_all('tr'):
        cols = row.find_all(['th', 'td'])
        if len(cols) == 2:
            key = cols[0].get_text(strip=True).replace(':', '')
            val = cols[1].get_text(strip=True)
            data[key] = val

print(json.dumps(data, indent=2))
