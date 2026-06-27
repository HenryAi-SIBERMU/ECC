import requests
import pandas as pd
import json
import os
import time

import urllib.request
import urllib.parse
import json
import pandas as pd
import os
import time

def scrape_bnpb_dibi():
    print("Mencari dataset Bencana melalui CKAN API BNPB...")
    
    # Langkah 1: Gunakan package_search untuk mencari id resource datastore yang aktif untuk kata kunci "bencana"
    search_url = "https://data.bnpb.go.id/api/3/action/package_search?q=bencana&rows=50"
    
    try:
        req = urllib.request.Request(search_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            
        packages = data.get('result', {}).get('results', [])
        active_resources = []
        
        # Mengekstrak semua resource_id yang datastore_active = true
        for pkg in packages:
            for res in pkg.get('resources', []):
                if res.get('datastore_active'):
                    active_resources.append({
                        'pkg_title': pkg.get('title'),
                        'resource_id': res.get('id'),
                        'res_name': res.get('name')
                    })
                    
        print(f"Menemukan {len(active_resources)} resource Datastore aktif terkait bencana.")
        
        all_records = []
        
        # Langkah 2: Lakukan iterasi datastore_search ke resource yang aktif menggunakan API standar CKAN
        for res in active_resources[:5]: # Batasi 5 contoh pertama untuk mencegah overload
            res_id = res['resource_id']
            print(f"Mengekstrak data dari: {res['pkg_title']} (ID: {res_id})")
            
            # Endpoint persis seperti di dokumentasi (screenshot)
            query_url = f"https://data.bnpb.go.id/api/3/action/datastore_search?resource_id={res_id}&limit=100"
            try:
                q_req = urllib.request.Request(query_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(q_req) as q_response:
                    q_data = json.loads(q_response.read())
                    records = q_data.get('result', {}).get('records', [])
                    all_records.extend(records)
            except Exception as e:
                print(f" Gagal membaca resource {res_id}: {e}")
                
            time.sleep(1) # Delay wajar

        if all_records:
            df = pd.DataFrame(all_records)
            output_dir = os.path.join("data", "raw")
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, "bencana_bnpb_ckan_sample.csv")
            df.to_csv(output_path, index=False)
            print(f"\nBerhasil mengekstrak {len(df)} baris data via CKAN API ke {output_path}")
            print("Skrip dapat dimodifikasi lebih lanjut untuk memfilter spesifik Sulawesi 2014-2024.")
        else:
            print("Tidak ada record yang berhasil ditarik.")
            
    except Exception as e:
        print(f"Terjadi kesalahan saat memanggil CKAN API: {e}")

if __name__ == "__main__":
    scrape_bnpb_dibi()
