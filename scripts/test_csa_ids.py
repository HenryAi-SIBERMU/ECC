import requests
API_KEY = '06fd644648629502353deaed29fc6383'

def fetch_csa_id(domain):
    subjects = []
    for page in range(1, 5):
        url = f'https://webapi.bps.go.id/v1/api/list/model/subjectcsa/domain/{domain}/page/{page}/key/{API_KEY}/'
        try:
            resp = requests.get(url).json()
            data = resp.get('data', [])
            if len(data) > 1 and isinstance(data[1], list):
                subjects.extend(data[1])
            else:
                break
        except:
            break
    
    # Find PDRB
    for s in subjects:
        t = s.get('title', '').lower()
        if 'pdrb' in t or 'domestik regional' in t or 'national account' in t or 'ekonomi' in t:
            print(f"[{domain}] [{s['sub_id']}] {s['title']}")

print("Mencari ID Ekonomi / PDRB di CSA:")
fetch_csa_id("0000")
fetch_csa_id("1100")
fetch_csa_id("1200")
