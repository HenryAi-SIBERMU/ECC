import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings()

url = "https://footprint.info.yorku.ca/data/"
print(f"Downloading {url} ...")
try:
    r = requests.get(url, verify=False, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(r.text, 'html.parser')

    links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if 'csv' in href.lower() or 'excel' in href.lower() or 'xls' in href.lower() or 'zip' in href.lower() or 'data' in href.lower():
            links.append((a.text.strip(), href))
            
    print("Potential Data Links:")
    for text, href in set(links):
        print(f"- [{text}] : {href}")
        
except Exception as e:
    print(f"Error: {e}")
