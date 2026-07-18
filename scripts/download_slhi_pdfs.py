import requests, os

api_key = '06fd644648629502353deaed29fc6383'
domain = '0000' # Nasional
keyword = 'statistik lingkungan hidup'
output_dir = r'c:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\data\raw\sulut_kualitas_air'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

page = 1
downloaded = []

while True:
    url = f'https://webapi.bps.go.id/v1/api/list/model/publication/domain/{domain}/keyword/{keyword.replace(" ", "%20")}/page/{page}/key/{api_key}'
    try:
        r = requests.get(url, timeout=15)
        data = r.json()
        
        if data.get('data-availability') == 'list-not-found':
            break
            
        pubs = data.get('data', [])
        items = pubs[1] if isinstance(pubs, list) and len(pubs) > 1 else pubs
        
        for p in items:
            title = p.get('title', '')
            if 'Statistik Lingkungan Hidup Indonesia' in title:
                for year in ['2025', '2026']:
                    if year in title:
                        print(f'Found: {title}')
                        pdf_url = p.get('pdf')
                        try:
                            print(f'  Downloading...')
                            resp = requests.get(pdf_url, timeout=60)
                            resp.raise_for_status()
                            file_path = os.path.join(output_dir, f'SLHI_{year}.pdf')
                            with open(file_path, 'wb') as f:
                                f.write(resp.content)
                            print(f'  -> Saved to {file_path}')
                            downloaded.append(year)
                        except Exception as e:
                            print(f'  -> Failed: {e}')
    except Exception as e:
        print(f"Error on page {page}: {e}")
        
    page += 1
    if len(downloaded) >= 3 or page > 5:
        break

print('Download selesai.')
