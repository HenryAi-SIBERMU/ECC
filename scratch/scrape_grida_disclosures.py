import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings()

url = "https://tailing.grida.no/disclosures"
print(f"Downloading {url} ...")
r = requests.get(url, verify=False)
soup = BeautifulSoup(r.text, 'html.parser')

tables = soup.find_all('table')
print(f"Ditemukan {len(tables)} tabel.")

if len(tables) > 0:
    rows = tables[0].find_all('tr')
    print(f"Tabel pertama punya {len(rows)} baris.")
    for i in range(min(5, len(rows))):
        cells = [td.text.strip() for td in rows[i].find_all(['th', 'td'])]
        print(f"Baris {i}: {cells}")
        
        # Cari link download
        links = rows[i].find_all('a', href=True)
        if links:
            for a in links:
                print(f"  Link: {a['href']}")
