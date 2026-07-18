import os
import time
import requests
import pandas as pd
from tqdm import tqdm

API_KEY = "06fd644648629502353deaed29fc6383"
BASE_URL = "https://webapi.bps.go.id/v1/api/interoperabilitas/datasource/simdasi"

TARGET_PROVINCES = {
    "7200000": "Sulawesi Tengah", 
    "7400000": "Sulawesi Tenggara"
}

YEARS = list(range(2016, 2025))

def get_kabupaten(prov_code):
    url = f"{BASE_URL}/id/27/parent/{prov_code}/key/{API_KEY}/"
    res = requests.get(url).json()
    if res.get('status') == 'OK':
        return [(d['kode'], d['nama']) for d in res['data'][1]['data']]
    return []

def get_id_tabel(kab_code):
    url = f"{BASE_URL}/id/23/wilayah/{kab_code}/key/{API_KEY}/"
    res = requests.get(url).json()
    if res.get('status') == 'OK':
        tables = res['data'][1].get('data', [])
        for t in tables:
            judul = t.get('judul', '').lower()
            if 'produk domestik' in judul and 'berlaku' in judul and 'lapangan usaha' in judul and 'distribusi' not in judul and 'laju' not in judul and 'indeks' not in judul:
                return t['id_tabel']
    return None

def fetch_table_data(kab_code, year, id_tabel):
    url = f"{BASE_URL}/id/25/wilayah/{kab_code}/tahun/{year}/id_tabel/{id_tabel}/key/{API_KEY}/"
    res = requests.get(url).json()
    if res.get('status') == 'OK' and len(res.get('data', [])) > 1:
        return res['data'][1].get('data', [])
    return []

def clean_and_map_sectors(df):
    mapping = {
        'A': 'Pertanian, Kehutanan, dan Perikanan',
        'B': 'Pertambangan dan Penggalian',
        'C': 'Industri Pengolahan',
        'D': 'Pengadaan Listrik dan Gas',
        'E': 'Pengadaan Air, Pengelolaan Sampah, Limbah dan Daur Ulang',
        'F': 'Konstruksi',
        'G': 'Perdagangan Besar dan Eceran; Reparasi Mobil dan Sepeda Motor',
        'H': 'Transportasi dan Pergudangan',
        'I': 'Penyediaan Akomodasi dan Makan Minum',
        'J': 'Informasi dan Komunikasi',
        'K': 'Jasa Keuangan dan Asuransi',
        'L': 'Real Estate',
        'M,N': 'Jasa Perusahaan',
        'O': 'Administrasi Pemerintahan, Pertahanan dan Jaminan Sosial Wajib',
        'P': 'Jasa Pendidikan',
        'Q': 'Jasa Kesehatan dan Kegiatan Sosial',
        'R,S,T,U': 'Jasa Lainnya'
    }
    
    def find_standard_sector(raw_name):
        raw_name = raw_name.upper()
        if "PRODUK DOMESTIK REGIONAL BRUTO" in raw_name or raw_name == "PDRB":
            return "TOTAL"
            
        for key, std_name in mapping.items():
            if raw_name.startswith(f"{key}.") or raw_name.startswith(f"{key} ") or raw_name == key:
                return std_name
            if std_name.upper()[:15] in raw_name:
                return std_name
                
        # Some edge cases
        if "PERTANIAN" in raw_name: return mapping['A']
        if "PERTAMBANGAN" in raw_name: return mapping['B']
        if "INDUSTRI" in raw_name: return mapping['C']
        if "LISTRIK" in raw_name: return mapping['D']
        if "AIR" in raw_name and "SAMPAH" in raw_name: return mapping['E']
        if "KONSTRUKSI" in raw_name: return mapping['F']
        if "PERDAGANGAN" in raw_name: return mapping['G']
        if "TRANSPORTASI" in raw_name: return mapping['H']
        if "AKOMODASI" in raw_name: return mapping['I']
        if "INFORMASI" in raw_name: return mapping['J']
        if "KEUANGAN" in raw_name: return mapping['K']
        if "REAL ESTATE" in raw_name or "REAL ESTAT" in raw_name: return mapping['L']
        if "JASA PERUSAHAAN" in raw_name: return mapping['M,N']
        if "ADMINISTRASI PEMERINTAHAN" in raw_name: return mapping['O']
        if "PENDIDIKAN" in raw_name: return mapping['P']
        if "KESEHATAN" in raw_name: return mapping['Q']
        if "JASA LAINNYA" in raw_name: return mapping['R,S,T,U']
        return raw_name
        
    df['sektor_standard'] = df['sektor_nama'].apply(find_standard_sector)
    df = df[df['sektor_standard'] != "TOTAL"].copy()
    df['sektor_nama'] = df['sektor_standard']
    return df[['provinsi', 'kabupaten', 'tahun', 'sektor_nama', 'nilai_miliar_rp']]

def parse_value(val_str):
    if not val_str or val_str == '-': return 0.0
    val_str = str(val_str).replace('.', '').replace(',', '.')
    try:
        return float(val_str)
    except:
        return 0.0

def main():
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    all_data = []
    
    for prov_code, prov_name in TARGET_PROVINCES.items():
        kabs = get_kabupaten(prov_code)
        print(f"\nProvinsi {prov_name}: ditemukan {len(kabs)} kabupaten/kota.")
        
        for kab_code, kab_name in tqdm(kabs, desc=prov_name):
            id_tabel = get_id_tabel(kab_code)
            if not id_tabel:
                continue
                
            for year in YEARS:
                rows = fetch_table_data(kab_code, year, id_tabel)
                for row in rows:
                    if 'label_raw' not in row or 'variables' not in row:
                        continue
                    
                    sektor_nama = row['label_raw']
                    
                    # SIMDASI variables structure is a dict with random keys
                    val_str = "0"
                    for k, v in row['variables'].items():
                        if isinstance(v, dict) and 'value_raw' in v:
                            val_str = v['value_raw']
                            break
                            
                    nilai = parse_value(val_str)
                    all_data.append({
                        "provinsi": prov_name,
                        "kabupaten": kab_name,
                        "tahun": year,
                        "sektor_nama": sektor_nama,
                        "nilai_miliar_rp": nilai
                    })
                time.sleep(0.3)
                
    df = pd.DataFrame(all_data)
    if not df.empty:
        df = clean_and_map_sectors(df)
        
        # Hitung Persentase dari total per kabupaten per tahun
        df_total = df.groupby(['provinsi', 'kabupaten', 'tahun'])['nilai_miliar_rp'].sum().reset_index(name='total_pdrb')
        df = df.merge(df_total, on=['provinsi', 'kabupaten', 'tahun'])
        df['pct_dari_total'] = (df['nilai_miliar_rp'] / df['total_pdrb']) * 100
        df = df.drop(columns=['total_pdrb'])
        
        # Save Output
        out_dir = "../../data/processed"
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "sulawesi_pdrb_sektoral_kabupaten_2016_2024.csv")
        df.to_csv(out_path, index=False)
        print(f"\nSelesai! Data tersimpan di: {out_path}")
        print(f"Total Baris: {len(df)}")
    else:
        print("Gagal mengambil data.")

if __name__ == '__main__':
    main()
