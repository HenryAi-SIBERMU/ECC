import os
import time
import re
import requests
import pandas as pd
from pathlib import Path

API_KEY = "06fd644648629502353deaed29fc6383"
BASE_URL = "https://webapi.bps.go.id/v1/api"

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / 'data' / 'raw'
os.makedirs(RAW_DIR, exist_ok=True)

# VAR 793 = Realisasi Investasi PMDN per Provinsi - Jumlah Investasi
# VAR 794 = Realisasi Investasi PMDN per Provinsi - Jumlah Proyek
# VAR 795 = Realisasi Investasi PMA per Provinsi (kemungkinan)
VARS_TO_FETCH = {
    793: "Investasi PMDN - Nilai (Juta Rp)",
    794: "Investasi PMDN - Jumlah Proyek",
}

SULAWESI_PROVS = [
    "sulawesi utara", "sulawesi tengah", "sulawesi selatan",
    "sulawesi tenggara", "gorontalo", "sulawesi barat"
]

# Tahun 2016-2026 (ID 116-126), chunk 2 tahun
year_chunks = [
    "116:117", "118:119", "120:121",
    "122:123", "124:125", "126"
]

all_data = []

print("=" * 60)
print("  EKSTRAKSI INVESTASI PMDN SULAWESI (BPS API 2016-2026)")
print("=" * 60)

for var_id, var_name in VARS_TO_FETCH.items():
    print(f"\n[*] Mengambil: {var_name} (Var {var_id})")
    for chunk in year_chunks:
        url = f"{BASE_URL}/list/model/data/domain/0000/var/{var_id}/th/{chunk}/key/{API_KEY}/"
        try:
            resp = requests.get(url, timeout=30)
            data = resp.json()
            if not isinstance(data, dict) or data.get("data-availability") != "available":
                time.sleep(1)
                continue

            vervars  = data.get("vervar", [])
            turvars  = data.get("turvar", [])
            tahuns   = data.get("tahun", [])
            turtahun = data.get("turtahun", [])
            dc       = data.get("datacontent", {})
            tt_val   = str(turtahun[0]['val']) if turtahun else "0"

            tahun_dict  = {str(t['val']): t['label'] for t in tahuns}
            turvar_dict = {str(t['val']): t['label'] for t in turvars}

            for v in vervars:
                prov_label = re.sub(r'<[^>]*>', '', v.get('label', '')).strip()
                # Filter Sulawesi saja
                if not any(s in prov_label.lower() for s in SULAWESI_PROVS):
                    continue
                v_val = str(v['val'])
                for th_val, th_label in tahun_dict.items():
                    for t_val in turvar_dict:
                        key = f"{v_val}{var_id}{t_val}{th_val}{tt_val}"
                        nilai = dc.get(key) if isinstance(dc, dict) else None
                        if nilai is not None:
                            all_data.append({
                                'provinsi': prov_label.title(),
                                'tahun': th_label,
                                'indikator': var_name,
                                'nilai': nilai,
                                'satuan': 'Juta Rp' if 'Nilai' in var_name else 'Proyek'
                            })
        except Exception as e:
            print(f"  [!] Error chunk {chunk}: {e}")
        time.sleep(1.5)

output_file = RAW_DIR / 'bps_investasi_pmdn_sulawesi_2016_2026.csv'
if all_data:
    df = pd.DataFrame(all_data)
    df.to_csv(output_file, index=False)
    print(f"\n[SUKSES] {len(df)} baris tersimpan ke: {output_file}")
    print("\nPreview:")
    print(df.head(12).to_string(index=False))
else:
    print("\n[GAGAL] Tidak ada data investasi yang berhasil diambil.")
