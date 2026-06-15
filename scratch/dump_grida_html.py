import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings()

url = "https://tailing.grida.no/"
print(f"Downloading {url} ...")
r = requests.get(url, verify=False)
soup = BeautifulSoup(r.text, 'html.parser')

links = []
for a in soup.find_all('a', href=True):
    links.append(a['href'])

print("Semua Link di Homepage:")
for l in sorted(set(links)):
    print(l)
