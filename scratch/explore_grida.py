import requests
from bs4 import BeautifulSoup
import json
import urllib3
urllib3.disable_warnings()

url = "https://tailing.grida.no/"
print(f"Mengakses {url} ...")

try:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    resp = requests.get(url, headers=headers, verify=False)
    resp.raise_for_status()
    
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    # Check for embedded json or data attributes
    found = False
    for script in soup.find_all('script'):
        if script.string and 'window.' in script.string and 'data' in script.string.lower():
            print("Found script containing potential data:")
            print(script.string[:500])
            found = True
            
    if not found:
        print("No obvious embedded data in scripts. Checking common API endpoints...")
        
        endpoints = [
            "https://tailing.grida.no/api/dams",
            "https://tailing.grida.no/api/facilities",
            "https://tailing.grida.no/data/dams.json",
            "https://tailing.grida.no/data/facilities.geojson"
        ]
        
        for ep in endpoints:
            r = requests.get(ep, headers=headers, verify=False)
            print(f"Testing {ep}: Status {r.status_code}")
            if r.status_code == 200:
                print(r.text[:500])
                
except Exception as e:
    print(f"Error: {e}")
