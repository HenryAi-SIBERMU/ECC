import os
import sys
import time
import pandas as pd
from pathlib import Path
import csv

# Add tools to path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from tools.google_dork.google_dorker import google_dork

def run_targeted_dorking(limit=50):
    input_csv = BASE_DIR / 'data' / 'processed' / 'sulawesi_esdm_nikel.csv'
    output_csv = BASE_DIR / 'data' / 'processed' / 'amdal_dork_results.csv'
    
    print("[*] Membaca data perusahaan dari ESDM...")
    try:
        df = pd.read_csv(input_csv)
    except Exception as e:
        print(f"[!] Gagal membaca CSV: {e}")
        return
        
    # Convert total_luas_ha to numeric (in case of string issues)
    df['total_luas_ha'] = pd.to_numeric(df['total_luas_ha'], errors='coerce').fillna(0)
    
    # Sort by total_luas_ha descending and get top 'limit'
    top_companies = df.sort_values(by='total_luas_ha', ascending=False).head(limit)
    
    print(f"[*] Berhasil memfilter Top {limit} perusahaan dengan area konsesi terbesar.")
    
    # Prepare output CSV
    file_exists = output_csv.exists()
    
    with open(output_csv, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['nama_perusahaan', 'lokasi', 'luas_ha', 'dork_query', 'pdf_title', 'pdf_link', 'pdf_snippet'])
            
        count = 0
        for idx, row in top_companies.iterrows():
            count += 1
            nama_pt = row['nama_perusahaan']
            lokasi = row['lokasi_izin']
            luas = row['total_luas_ha']
            
            # Construct the Query
            query = f'"{nama_pt}" "AMDAL" OR "RKL-RPL" "limbah" OR "tailing" filetype:pdf'
            
            print(f"\n[{count}/{limit}] Mencari: {nama_pt} ({luas} Ha)")
            
            # Execute Dork
            # Using try-except to catch potential API limits
            try:
                results = google_dork(query, num_results=3) # Ambil 3 hasil teratas saja per PT
                
                if not results:
                    writer.writerow([nama_pt, lokasi, luas, query, 'TIDAK DITEMUKAN', '', ''])
                else:
                    for res in results:
                        writer.writerow([nama_pt, lokasi, luas, query, res['title'], res['link'], res['snippet']])
                        
                # Be polite to the API
                time.sleep(1)
                
            except Exception as e:
                print(f"[!] Terjadi error saat dorking untuk {nama_pt}: {e}")
                writer.writerow([nama_pt, lokasi, luas, query, f'ERROR: {e}', '', ''])
                break # Stop if quota is exceeded or major error
                
    print(f"\n[*] Selesai! Hasil dorking tersimpan di: {output_csv}")

if __name__ == "__main__":
    run_targeted_dorking(50)
