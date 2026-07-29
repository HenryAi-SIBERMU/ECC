"""
Fetch Data Akses Air Minum Layak Kabupaten via BPS SIMDASI
==========================================================
Output: data/processed/sulawesi_air_bersih_kab_simdasi.csv
"""

import re
import time
from pathlib import Path
import pandas as pd
import requests
import urllib3
urllib3.disable_warnings()

API_KEY = "06fd644648629502353deaed29fc6383"
BASE_URL = "https://webapi.bps.go.id/v1/api"

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

SULAWESI_PROVS = {
    "7100000": "Sulawesi Utara",
    "7200000": "Sulawesi Tengah",
    "7300000": "Sulawesi Selatan",
    "7400000": "Sulawesi Tenggara",
    "7500000": "Gorontalo",
    "7600000": "Sulawesi Barat",
}

def clean(s):
    return re.sub(r"<[^>]*>", "", str(s)).strip()

def parse_num(s):
    if not s or str(s).strip() in ["...", "–", "-", "NA", "", "~0"]:
        return None
    try:
        return float(str(s).replace(".", "").replace(",", "."))
    except:
        return None

def find_water_table(mfd):
    """Cari table_id untuk Sumber Air Minum Layak."""
    for mms_id in [521, 522]:
        url = f"{BASE_URL}/interoperabilitas/datasource/simdasi/id/23/wilayah/{mfd}/mms_id/{mms_id}/key/{API_KEY}/"
        try:
            resp = requests.get(url, timeout=30, verify=False).json()
            tables = (
                resp.get("data", [{}, {}])[1].get("data", [])
                if len(resp.get("data", [])) > 1 else []
            )
            for t in tables:
                j = t.get("judul", "").lower()
                if "sumber air minum layak" in j and ("kabupaten" in j or "kota" in j):
                    return t.get("id_tabel"), t.get("ketersediaan_tahun", [])
        except:
            pass
        time.sleep(1)
    return None, []

def fetch_water_year(table_id, mfd, provinsi, year):
    url = f"{BASE_URL}/interoperabilitas/datasource/simdasi/id/25/id_tabel/{table_id}/wilayah/{mfd}/tahun/{year}/key/{API_KEY}/"
    try:
        resp = requests.get(url, timeout=30, verify=False).json()
        if resp.get("data-availability") != "available":
            return []
        
        content = resp["data"][1] if len(resp.get("data", [])) > 1 else {}
        cols = content.get("kolom", {})
        rows = content.get("data", [])
        if not rows or not cols:
            return []

        # Find the column for percentage
        col_pct = None
        for k, v in cols.items():
            nm = v.get("nama_variabel", "").lower()
            if "persentase" in nm or "rumah tangga" in nm or "air" in nm:
                col_pct = k
                break
                
        if not col_pct:
            # Fallback, just pick the first data column
            col_pct = list(cols.keys())[-1]

        skip_labels = {"jumlah", "total", "sulawesi", provinsi.lower(), "provinsi " + provinsi.lower()}
        
        results = []
        for r in rows:
            label = clean(r.get("label_raw", r.get("label", "")))
            if not label or label.lower() in skip_labels:
                continue
                
            vrs = r.get("variables", {})
            val = parse_num(vrs.get(col_pct, {}).get("value_raw"))
            
            if val is not None:
                results.append({
                    "Provinsi": provinsi,
                    "Kabupaten": label,
                    "Tahun": year,
                    "Persentase_Air_Layak": val
                })
        return results
    except Exception as e:
        print(f"    [!] {year}: {e}")
        return []

if __name__ == "__main__":
    print("=" * 65)
    print("  FETCHING DATA AKSES AIR MINUM LAYAK SULAWESI (SIMDASI)")
    print("=" * 65)

    all_rows = []
    for mfd, provinsi in SULAWESI_PROVS.items():
        print(f"\n[{provinsi}]")
        tid, avail_years = find_water_table(mfd)
        if not tid:
            print("  [!!] Tabel tidak ditemukan")
            continue
        print(f"  Table ID: {tid[:15]}... | Tahun: {avail_years}")
        
        for yr in avail_years:
            rows = fetch_water_year(tid, mfd, provinsi, yr)
            if rows:
                all_rows.extend(rows)
                print(f"  [+] {yr}: {len(rows)} kabupaten")
            else:
                print(f"  [-] {yr}: tidak ada data")
            time.sleep(1)

    if not all_rows:
        print("\n[FAIL] Tidak ada data yang berhasil ditarik.")
    else:
        df = pd.DataFrame(all_rows)
        df["Tahun"] = df["Tahun"].astype(int)
        
        # Add is_smelter flag
        SMELTER_KABS = {"Morowali", "Morowali Utara", "Banggai", "Konawe", "Konawe Utara", "Kolaka", "Luwu Timur"}
        df["is_smelter"] = df["Kabupaten"].apply(lambda x: any(sk in x for sk in SMELTER_KABS))
        
        df = df.sort_values(["Provinsi", "Kabupaten", "Tahun"]).reset_index(drop=True)
        out = PROCESSED_DIR / "sulawesi_air_bersih_kab_simdasi.csv"
        df.to_csv(out, index=False)
        print(f"\n[SAVED] {out.name} — {len(df)} baris")
        
        print("\n=== SAMPLE DATA (Morowali) ===")
        print(df[df["Kabupaten"].str.contains("Morowali")])
