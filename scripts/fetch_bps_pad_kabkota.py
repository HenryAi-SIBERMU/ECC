import os
import time
import requests
import pandas as pd
from pathlib import Path

API_KEY = "06fd644648629502353deaed29fc6383"
BASE_URL = "https://webapi.bps.go.id/v1/api"
VAR_ID = 787

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / 'data' / 'raw'
os.makedirs(RAW_DIR, exist_ok=True)
output_file = RAW_DIR / 'bps_pad_sulawesi_2016_2026.csv'

# Chunk Tahun (2016=116, ..., 2026=126)
year_chunks = [
    "116:117", "118:119", "120:121",
    "122:123", "124:125", "126"
]

# 6 Domain Provinsi Sulawesi
PROV_SULAWESI = {
    "7100": "Sulawesi Utara",
    "7200": "Sulawesi Tengah",
    "7300": "Sulawesi Selatan",
    "7400": "Sulawesi Tenggara",
    "7500": "Gorontalo",
    "7600": "Sulawesi Barat"
}

# Var 787: Vervar adalah KATEGORI, bukan wilayah
# Val 2 = Pendapatan Asli Daerah
# Val 1 = PENDAPATAN DAERAH (total)
# Val 7 = Dana Perimbangan
# Val 14 = JUMLAH

TARGET_VERVARS = {
    "1": "Total Pendapatan Daerah",
    "2": "Pendapatan Asli Daerah (PAD)",
    "7": "Dana Perimbangan",
    "14": "JUMLAH KESELURUHAN"
}

all_data = []

print("=" * 60)
print("  EKSTRAKSI DATA PAD PER PROVINSI SULAWESI (2016-2026)")
print("=" * 60)

for dom_id, prov_name in PROV_SULAWESI.items():
    print(f"\n[*] {prov_name} (Domain {dom_id})...")
    for chunk in year_chunks:
        url = f"{BASE_URL}/list/model/data/domain/{dom_id}/var/{VAR_ID}/th/{chunk}/key/{API_KEY}/"
        try:
            resp = requests.get(url, timeout=30)
            data = resp.json()

            if not isinstance(data, dict):
                time.sleep(1)
                continue

            if data.get("data-availability") == "available":
                vervars = data.get("vervar", [])
                turvars = data.get("turvar", [])
                tahuns = data.get("tahun", [])
                dc = data.get("datacontent", {})

                vervar_dict = {str(v['val']): v['label'] for v in vervars}
                turvar_dict = {str(t['val']): t['label'] for t in turvars}
                tahun_dict = {str(t['val']): t['label'] for t in tahuns}
                turtahuns = data.get("turtahun", [])
                tt_val = str(turtahuns[0]['val']) if turtahuns else "0"

                if isinstance(dc, dict):
                    for th_val, th_label in tahun_dict.items():
                        for t_val, t_label in turvar_dict.items():
                            for vv_val, vv_label in vervar_dict.items():
                                key = f"{vv_val}{VAR_ID}{t_val}{th_val}{tt_val}"
                                nilai = dc.get(key)
                                if nilai is not None:
                                    import re
                                    clean_label = re.sub(r'<[^>]*>', '', vv_label).strip()
                                    all_data.append({
                                        'domain_id': dom_id,
                                        'provinsi': prov_name,
                                        'tahun': th_label,
                                        'kategori': clean_label,
                                        'nilai_rupiah': nilai,
                                        'satuan': 'Rupiah'
                                    })
        except Exception as e:
            print(f"  [!] Error chunk {chunk}: {e}")

        time.sleep(1.5)  # Rate limit aman

if all_data:
    df = pd.DataFrame(all_data)
    df.to_csv(output_file, index=False)
    print(f"\n[SUKSES] Total {len(df)} baris tersimpan ke: {output_file}")
    print("\nPreview data:")
    print(df.head(10).to_string(index=False))
else:
    # Fallback: coba ambil dari domain 0000 dengan filter kode wilayah
    print("\n[INFO] Mencoba fallback ke domain 0000 Nasional...")
    for chunk in year_chunks:
        url = f"{BASE_URL}/list/model/data/domain/0000/var/{VAR_ID}/th/{chunk}/key/{API_KEY}/"
        try:
            resp = requests.get(url, timeout=30)
            data = resp.json()
            if isinstance(data, dict) and data.get("data-availability") == "available":
                vervars = data.get("vervar", [])
                tahuns = data.get("tahun", [])
                dc = data.get("datacontent", {})
                tahun_dict = {str(t['val']): t['label'] for t in tahuns}
                turvars = data.get("turvar", [])
                tt = data.get("turtahun", [])
                tt_val = str(tt[0]['val']) if tt else "0"

                if isinstance(dc, dict):
                    for v in vervars:
                        import re
                        label = re.sub(r'<[^>]*>', '', v.get('label', '')).strip()
                        for th_val, th_label in tahun_dict.items():
                            for t in turvars:
                                key = f"{v['val']}{VAR_ID}{t['val']}{th_val}{tt_val}"
                                nilai = dc.get(key)
                                if nilai is not None:
                                    all_data.append({
                                        'domain_id': '0000',
                                        'provinsi': 'NASIONAL',
                                        'tahun': th_label,
                                        'kategori': label,
                                        'nilai_rupiah': nilai,
                                        'satuan': 'Rupiah'
                                    })
        except Exception as e:
            print(f"  [!] Fallback error chunk {chunk}: {e}")
        time.sleep(1.5)

    if all_data:
        df = pd.DataFrame(all_data)
        df.to_csv(output_file, index=False)
        print(f"\n[SUKSES - NASIONAL] Total {len(df)} baris tersimpan ke: {output_file}")
    else:
        print("\n[GAGAL] Tidak ada data yang dapat diambil dari API BPS.")
