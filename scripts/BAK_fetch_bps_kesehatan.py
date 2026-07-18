import os
import time
import requests
import pandas as pd
from pathlib import Path

API_KEY = "06fd644648629502353deaed29fc6383"
BASE_URL = "https://webapi.bps.go.id/v1/api"
DOMAIN = "0000" # Domain Nasional
VAR_ID = 42     # Kasus Penyakit (Hanya sampai 2015)

# Setup direktori
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / 'data' / 'raw'
os.makedirs(RAW_DIR, exist_ok=True)
output_file = RAW_DIR / 'BAK_bps_kesehatan_provinsi_2014_2015.csv'

# Tahun 2014-2024 (ID: 114-124) dalam chunk max 2 tahun
year_chunks = [
    "114:115", "116:117", "118:119", 
    "120:121", "122:123", "124"
]

all_data = []

print("="*50)
print(" MULAI EKSTRAKSI DATA KESEHATAN (VAR 42 - PENYAKIT)")
print("="*50)

for chunk in year_chunks:
    print(f"[*] Mengambil data tahun (ID: {chunk})...")
    url = f"{BASE_URL}/list/model/data/domain/{DOMAIN}/var/{VAR_ID}/th/{chunk}/key/{API_KEY}/"
    
    try:
        resp = requests.get(url)
        data = resp.json()
        
        if data.get("data-availability") == "available":
            vervars = data.get("vervar", [])
            turvars = data.get("turvar", [])
            tahuns = data.get("tahun", [])
            turtahuns = data.get("turtahun", [])
            datacontent = data.get("datacontent", {})
            
            vervar_dict = {str(v['val']): v['label'] for v in vervars}
            turvar_dict = {str(t['val']): t['label'] for t in turvars}
            tahun_dict = {str(th['val']): th['label'] for th in tahuns}
            
            for v_val, v_label in vervar_dict.items():
                for t_val, t_label in turvar_dict.items():
                    for th_val, th_label in tahun_dict.items():
                        tt_val = "0" 
                        if turtahuns:
                            tt_val = str(turtahuns[0]['val'])
                            
                        key = f"{v_val}{VAR_ID}{t_val}{th_val}{tt_val}"
                        
                        nilai = datacontent.get(key)
                        if nilai is not None:
                            all_data.append({
                                'provinsi': v_label,
                                'tahun': th_label,
                                'jenis_penyakit': t_label,
                                'jumlah_kasus': nilai,
                                'satuan': 'Kasus'
                            })
        else:
            print(f"  [-] Data tidak tersedia untuk chunk {chunk}")
            
    except Exception as e:
        print(f"  [X] Error pada chunk {chunk}: {e}")
        
    time.sleep(1)

if all_data:
    df = pd.DataFrame(all_data)
    
    df['jenis_penyakit'] = df['jenis_penyakit'].astype(str).str.replace(r'<[^>]*>', '', regex=True)
    df['provinsi'] = df['provinsi'].astype(str).str.title()
    
    df.to_csv(output_file, index=False)
    print(f"\n✅ SUKSES! Data Kesehatan berhasil diekstrak.")
    print(f"✅ Total Baris: {len(df)}")
    print(f"✅ Tersimpan di: {output_file}")
else:
    print("\n❌ GAGAL: Tidak ada data yang berhasil diekstrak.")
