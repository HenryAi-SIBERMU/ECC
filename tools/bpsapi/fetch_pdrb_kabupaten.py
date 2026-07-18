import os
import json
import time
import requests
import pandas as pd
from datetime import datetime
from tqdm import tqdm

API_KEY = "06fd644648629502353deaed29fc6383"
BASE_URL = "https://webapi.bps.go.id/v1/api"

# Fokus Sulawesi Tengah (72) dan Sulawesi Tenggara (74)
TARGET_PROVINCES = {"72": "Sulawesi Tengah", "74": "Sulawesi Tenggara"}

def get_kabupaten_list(prov_code):
    url = f"{BASE_URL}/domain/type/kabbyprov/prov/{prov_code}/key/{API_KEY}/"
    try:
        resp = requests.get(url)
        data = resp.json().get('data', [])
        if len(data) > 1:
            return [(d['domain_id'], d['domain_name']) for d in data[1]]
    except Exception as e:
        print(f"Error fetching regency list for {prov_code}: {e}")
    return []

def find_pdrb_var_id(domain_id):
    url = f"{BASE_URL}/list/model/data/domain/{domain_id}/key/{API_KEY}/"
    try:
        resp = requests.get(url)
        data = resp.json().get('data', [])
        if len(data) > 1:
            for item in data[1]:
                title = str(item.get('title', '')).lower()
                # Kita mencari ADHB Sektoral (Atas Dasar Harga Berlaku, Lapangan Usaha)
                if 'pdrb' in title and 'lapangan usaha' in title and 'berlaku' in title and 'seri 2010' in title:
                    return item['var_id']
                if 'pdrb' in title and 'lapangan usaha' in title and 'berlaku' in title:
                    return item['var_id']
    except Exception as e:
        print(f"Error finding var_id for {domain_id}: {e}")
    return None

def fetch_data_for_var(domain_id, var_id):
    url = f"{BASE_URL}/data/domain/{domain_id}/var/{var_id}/key/{API_KEY}/"
    try:
        resp = requests.get(url)
        return resp.json()
    except Exception as e:
        print(f"Error fetching data for {domain_id}: {e}")
    return None

def map_bps_data(bps_data, prov_name, kab_name):
    # Struktur Data BPS API sangat spesifik
    # datacontent[vervar_id][turvar_id][tahun_id] = nilai
    # vervar = list sektor (variabel vertikal)
    # tahun = list tahun
    if 'datacontent' not in bps_data or 'vervar' not in bps_data or 'tahun' not in bps_data:
        return []
    
    datacontent = bps_data['datacontent']
    vervar_dict = {str(item['val']): item['label'] for item in bps_data['vervar']}
    tahun_dict = {str(item['val']): item['label'] for item in bps_data['tahun']}
    
    turvar_val = str(bps_data['turvar'][0]['val']) if 'turvar' in bps_data and len(bps_data['turvar']) > 0 else '0'
    
    records = []
    
    for v_id, turvars in datacontent.items():
        if v_id not in vervar_dict:
            continue
        sektor_nama = vervar_dict[v_id].strip()
        
        # PDRB total biasanya bernama "Produk Domestik Regional Bruto" atau "Total", kita akan filter nanti
        if turvar_val in turvars:
            years_data = turvars[turvar_val]
        else:
            # kadang turvar tidak ter nested
            years_data = turvars
            
        for y_id, value in years_data.items():
            if y_id not in tahun_dict:
                continue
            tahun = int(tahun_dict[y_id])
            if 2016 <= tahun <= 2024:
                try:
                    val_float = float(value)
                    records.append({
                        "provinsi": prov_name,
                        "kabupaten": kab_name,
                        "tahun": tahun,
                        "sektor_nama": sektor_nama,
                        "nilai_miliar_rp": val_float
                    })
                except (ValueError, TypeError):
                    pass # skip invalid values
    return records

def clean_and_map_sectors(df):
    """
    Membersihkan penamaan sektor agar standard 17 Sektor PDRB
    """
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
    
    # Simple mapping by substring since BPS often prepends KBLI code letters
    def find_standard_sector(raw_name):
        raw_name = raw_name.upper()
        if "PRODUK DOMESTIK REGIONAL BRUTO" in raw_name or raw_name == "PDRB":
            return "TOTAL"
            
        for key, std_name in mapping.items():
            # e.g., "A. Pertanian..."
            if raw_name.startswith(f"{key}.") or raw_name.startswith(f"{key} ") or raw_name == key:
                return std_name
            # Fallback exact match on words
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
    
    # Remove prefix alphabet mapping (e.g. "C. Industri Pengolahan") if present in Standard name? No standard is clean.
    df['sektor_nama'] = df['sektor_standard']
    return df[['provinsi', 'kabupaten', 'tahun', 'sektor_nama', 'nilai_miliar_rp']]

def main():
    print("Mencari Kabupaten di Sulteng dan Sultra...")
    all_data = []
    
    for prov_code, prov_name in TARGET_PROVINCES.items():
        kabs = get_kabupaten_list(prov_code)
        print(f"\nProvinsi {prov_name}: ditemukan {len(kabs)} kabupaten/kota.")
        
        for dom_id, kab_name in tqdm(kabs, desc=prov_name):
            var_id = find_pdrb_var_id(dom_id)
            if not var_id:
                # Default var_id if search fails (often 141 or 153 for PDRB ADHB LU)
                var_id = 141
            
            bps_data = fetch_data_for_var(dom_id, var_id)
            if bps_data and 'datacontent' in bps_data:
                records = map_bps_data(bps_data, prov_name, kab_name)
                all_data.extend(records)
            time.sleep(0.5) # Rate limiting
            
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
        print(f"\n✅ Selesai! Data tersimpan di: {out_path}")
        print(f"Total Baris: {len(df)}")
    else:
        print("❌ Gagal mengambil data.")

if __name__ == '__main__':
    main()
