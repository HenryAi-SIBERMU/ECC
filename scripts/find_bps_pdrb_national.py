import requests
API_KEY = '06fd644648629502353deaed29fc6383'
for page in range(1, 7):
    url = f'https://webapi.bps.go.id/v1/api/list/model/subject/domain/0000/page/{page}/key/{API_KEY}/'
    resp = requests.get(url).json()
    subs = resp.get('data', [])[1]
    for s in subs:
        title = s.get('title', '').lower()
        if 'pdrb' in title or 'pdb' in title or 'produk domestik' in title or 'regional' in title:
            print(f"[{s['sub_id']}] {s['title']}")
