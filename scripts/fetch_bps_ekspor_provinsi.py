import os
import time
import requests
import pandas as pd

API_KEY = "06fd644648629502353deaed29fc6383"
BASE_URL = "https://webapi.bps.go.id/v1/api"
DOMAIN = "0000" # Domain Nasional karena Var 2346/2347 ada di Nasional

# Var 2346: Nilai Ekspor Nonmigas Bulanan Menurut Provinsi Asal Barang
# Var 2347: Nilai Ekspor Migas Bulanan Menurut Provinsi Asal Barang
VARS_TO_FETCH = {
    2346: "Ekspor Non-Migas",
    2347: "Ekspor Migas"
}

# Provinsi Sulawesi di Vervar
SULAWESI_PROVS = [
    "Sulawesi Utara", "Sulawesi Tengah", "Sulawesi Selatan",
    "Sulawesi Tenggara", "Gorontalo", "Sulawesi Barat"
]

year_chunks = [
    "116:117", "118:119", "120:121",
    "122:123", "124:125", "126"
]

output_file = os.path.join(os.path.dirname(__file__), "raw", "bps_ekspor_sulawesi_2016_2026.csv")

all_data = []

print("="*50)
print(" MULAI EKSTRAKSI DATA EKSPOR SULAWESI (BPS API)")
print("="*50)

for var_id, var_name in VARS_TO_FETCH.items():
    print(f"\n[*] Mengambil {var_name} (Var ID: {var_id})...")
    
    for chunk in year_chunks:
        url = f"{BASE_URL}/list/model/data/domain/{DOMAIN}/var/{var_id}/th/{chunk}/key/{API_KEY}/"
        try:
            resp = requests.get(url, timeout=30)
            data = resp.json()
            
            if data.get("data-availability") == "available":
                vervars = data.get("vervar", [])
                turvars = data.get("turvar", [])
                tahuns = data.get("tahun", [])
                datacontent = data.get("datacontent", {})
                
                vervar_dict = {str(v['val']): v['label'] for v in vervars}
                turvar_dict = {str(t['val']): t['label'] for t in turvars}
                tahun_dict = {str(th['val']): th['label'] for th in tahuns}
                
                for v_val, v_label in vervar_dict.items():
                    # Filter khusus Sulawesi
                    if any(prov.lower() in v_label.lower() for prov in SULAWESI_PROVS):
                        for t_val, t_label in turvar_dict.items():
                            for th_val, th_label in tahun_dict.items():
                                # Cari key di datacontent
                                # Format: v_val + var_id + t_val + th_val + "0"
                                key = f"{v_val}{var_id}{t_val}{th_val}0"
                                nilai = datacontent.get(key)
                                
                                if nilai is not None:
                                    all_data.append({
                                        'provinsi': v_label,
                                        'tahun': th_label,
                                        'bulan': t_label,
                                        'kategori': var_name,
                                        'nilai_ekspor': nilai,
                                        'satuan': 'Juta USD' # Biasanya Ekspor BPS dalam Juta/Ribu USD
                                    })
            else:
                print(f"  [-] Chunk {chunk} tidak ada data.")
        except Exception as e:
            print(f"  [X] Error chunk {chunk}: {e}")
            
        time.sleep(1) # Rate limit

if all_data:
    df = pd.DataFrame(all_data)
    # Lakukan agregasi per tahun jika ada bulan
    if 'bulan' in df.columns and len(df['bulan'].unique()) > 1:
        # Konversi ke numeric dan abaikan null
        df['nilai_ekspor'] = pd.to_numeric(df['nilai_ekspor'], errors='coerce')
        # Group by agregat tahunan
        df_yearly = df.groupby(['provinsi', 'tahun', 'kategori', 'satuan'])['nilai_ekspor'].sum().reset_index()
        df_yearly.to_csv(output_file, index=False)
        print(f"\n[SUKSES] Ekspor Tahunan Sulawesi terekstrak sebanyak {len(df_yearly)} baris.")
    else:
        df.to_csv(output_file, index=False)
        print(f"\n[SUKSES] Ekspor Sulawesi terekstrak sebanyak {len(df)} baris.")
        
    print(f"File tersimpan di {output_file}")
else:
    print("\n[GAGAL] Tidak ada data Ekspor yang didapat.")
