import os
import time
import requests
import pandas as pd
from pathlib import Path

API_KEY = "06fd644648629502353deaed29fc6383"
BASE_URL = "https://webapi.bps.go.id/v1/api"

# Setup direktori
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / 'data' / 'raw'
os.makedirs(RAW_DIR, exist_ok=True)
output_file = RAW_DIR / 'bps_pdrb_sulawesi_2016_2026.csv'

# Daftar 6 Provinsi di Sulawesi (Domain ID BPS)
PROVINSI_DOMAINS = {
    "7100": "Sulawesi Utara",
    "7200": "Sulawesi Tengah", 
    "7300": "Sulawesi Selatan", 
    "7400": "Sulawesi Tenggara",
    "7500": "Gorontalo", 
    "7600": "Sulawesi Barat"
}

# Chunk ID Tahun: 2016-2026
year_chunks = [
    "116:117", "118:119", "120:121", 
    "122:123", "124:125", "126"
]

all_data = []

def cari_var_id_pdrb(domain_id):
    """Mencari Var ID spesifik untuk PDRB (Lapangan Usaha, Harga Berlaku) di provinsi tertentu."""
    # 1. Cari Subject ID untuk PDRB
    sub_url = f"{BASE_URL}/list/model/subject/domain/{domain_id}/key/{API_KEY}/"
    try:
        sub_resp = requests.get(sub_url).json()
        sub_data = sub_resp.get('data', [])
        if isinstance(sub_data, list) and len(sub_data) > 1 and isinstance(sub_data[1], list):
            sub_data = sub_data[1]
            
        pdrb_sub_id = None
        for s in sub_data:
            if isinstance(s, dict) and 'sub_name' in s:
                name = s['sub_name'].lower()
                if 'pdrb' in name or 'domestik regional' in name:
                    if 'pengeluaran' not in name: # Kita butuh Lapangan Usaha, bukan pengeluaran
                        pdrb_sub_id = s['sub_id']
                        break
                        
        if not pdrb_sub_id:
            # Fallback jika subject tidak ditemukan dengan filter kuat
            for s in sub_data:
                if isinstance(s, dict) and 'sub_name' in s:
                    name = s['sub_name'].lower()
                    if 'pdrb' in name:
                        pdrb_sub_id = s['sub_id']
                        break

        if not pdrb_sub_id:
            return 111 # Fallback hardcode
            
        # 2. Cari Var ID di dalam subject tersebut
        var_url = f"{BASE_URL}/list/model/var/domain/{domain_id}/subject/{pdrb_sub_id}/key/{API_KEY}/"
        var_resp = requests.get(var_url).json()
        var_data = var_resp.get('data', [])
        if isinstance(var_data, list) and len(var_data) > 1 and isinstance(var_data[1], list):
            var_data = var_data[1]
            
        for v in var_data:
            if isinstance(v, dict) and 'title' in v:
                t = v['title'].lower()
                # Kita cari PDRB berdasarkan lapangan usaha atas dasar harga berlaku
                if 'pdrb' in t and 'lapangan usaha' in t and 'berlaku' in t:
                    return v['var_id']
        
        # Fallback jika tidak ada kata 'berlaku', ambil yg lapangan usaha
        for v in var_data:
            if isinstance(v, dict) and 'title' in v:
                t = v['title'].lower()
                if 'pdrb' in t and 'lapangan usaha' in t:
                    return v['var_id']
                    
        # Fallback terakhir
        for v in var_data:
            if isinstance(v, dict) and 'title' in v:
                t = v['title'].lower()
                if 'pdrb' in t:
                    return v['var_id']

    except Exception:
        pass
        
    return 111 # Fallback absolute default

print("="*60)
print(" MULAI EKSTRAKSI DATA PDRB (AUTO-SEARCH VAR ID)")
print("="*60)

for domain_id, nama_prov in PROVINSI_DOMAINS.items():
    print(f"\n[*] Memproses Provinsi: {nama_prov} (Domain {domain_id})")
    
    var_id = cari_var_id_pdrb(domain_id)
    print(f"  -> Ditemukan Var ID PDRB: {var_id}")
    
    for chunk in year_chunks:
        url = f"{BASE_URL}/list/model/data/domain/{domain_id}/var/{var_id}/th/{chunk}/key/{API_KEY}/"
        
        try:
            resp = requests.get(url)
            data = resp.json()
            
            if data.get("data-availability") == "available":
                turvars = data.get("turvar", [])
                tahuns = data.get("tahun", [])
                turtahuns = data.get("turtahun", [])
                datacontent = data.get("datacontent", {})
                
                turvar_dict = {str(t['val']): t['label'] for t in turvars}
                tahun_dict = {str(th['val']): th['label'] for th in tahuns}
                
                for t_val, t_label in turvar_dict.items():
                    for th_val, th_label in tahun_dict.items():
                        tt_val = "0"
                        if turtahuns:
                            tt_val = str(turtahuns[0]['val'])
                            
                        # Key = var(ID) + turvar + tahun + turtahun
                        # Di level provinsi, vervar biasanya kosong untuk data provinsi tunggal
                        key = f"{var_id}{t_val}{th_val}{tt_val}"
                        
                        # Coba berbagai kemungkinan key karena formatnya kadang gila
                        # Misal: domain_val + var + turvar + tahun + turtahun
                        key2 = f"{domain_id}{var_id}{t_val}{th_val}{tt_val}"
                        # BPS sering menyembunyikan vervar dengan val 0
                        key3 = f"0{var_id}{t_val}{th_val}{tt_val}"
                        
                        nilai = datacontent.get(key) or datacontent.get(key2) or datacontent.get(key3)
                        
                        # Fallback brute force cari key yang berakhiran {t_val}{th_val}{tt_val}
                        if nilai is None:
                            suffix = f"{var_id}{t_val}{th_val}{tt_val}"
                            for k, v in datacontent.items():
                                if k.endswith(suffix):
                                    nilai = v
                                    break
                                    
                        if nilai is not None:
                            all_data.append({
                                'provinsi': nama_prov,
                                'tahun': th_label,
                                'lapangan_usaha': t_label,
                                'nilai_milyar_rp': nilai,
                                'satuan': 'Juta Rupiah' # API BPS PDRB biasanya dalam Juta Rupiah
                            })
            else:
                pass
                
        except Exception as e:
            pass
            
        time.sleep(1)

if all_data:
    df = pd.DataFrame(all_data)
    df.to_csv(output_file, index=False)
    print(f"\n✅ SUKSES! Data PDRB berhasil diekstrak.")
    print(f"✅ Total Baris: {len(df)}")
    print(f"✅ Tersimpan di: {output_file}")
else:
    print("\n❌ GAGAL: Tidak ada data yang berhasil diekstrak.")
