import requests

api_key = '06fd644648629502353deaed29fc6383'
domain = '7100' # Sulawesi Utara
keyword = 'lingkungan hidup'
url = f'https://webapi.bps.go.id/v1/api/list/model/publication/domain/{domain}/keyword/{keyword.replace(" ", "%20")}/key/{api_key}'

try:
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    data = r.json()
    pubs = data.get('data', [])
    
    items = pubs[1] if isinstance(pubs, list) and len(pubs) > 1 else pubs
    
    print("Publikasi Lingkungan Hidup Sulut:")
    for p in items:
        title = p.get('title', '')
        print(f"- {title} (ID: {p.get('pub_id')})")
        print(f"  Link PDF: {p.get('pdf')}")
            
except Exception as e:
    print(f'Error: {e}')
