"""
Ambil data Nasional (PMDN + Ekspor) dari BPS API,
lalu proses data Sulawesi dari raw ke processed.

Output:
- nasional_investasi_pmdn_2016_2024.csv
- nasional_ekspor_2016_2024.csv
- sulawesi_investasi_pmdn_2016_2024.csv
- sulawesi_ekspor_2016_2024.csv
- sulawesi_pad_2016_2024.csv
"""
import os
import re
import time
import requests
import pandas as pd
from pathlib import Path

API_KEY = "06fd644648629502353deaed29fc6383"
BASE_URL = "https://webapi.bps.go.id/v1/api"

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
OUT_DIR = BASE_DIR / "data" / "processed"
os.makedirs(OUT_DIR, exist_ok=True)

SULAWESI_PROVS = [
    "sulawesi utara", "sulawesi tengah", "sulawesi selatan",
    "sulawesi tenggara", "gorontalo", "sulawesi barat",
]

# Tahun 2016-2026 (ID 116-126), chunk 2 tahun
YEAR_CHUNKS = [
    "116:117", "118:119", "120:121",
    "122:123", "124:125", "126",
]


# ============================================================
# FETCH: PMDN Nasional (semua provinsi)
# ============================================================
def fetch_pmdn_nasional():
    """Fetch PMDN all provinces from BPS API."""
    VARS = {
        793: ("Investasi PMDN - Nilai (Juta Rp)", "Juta Rp"),
        794: ("Investasi PMDN - Jumlah Proyek", "Proyek"),
    }

    all_data = []
    print("[*] Fetch: Investasi PMDN Nasional (Var 793, 794)")

    for var_id, (var_name, satuan) in VARS.items():
        print(f"    Indikator: {var_name}")
        for chunk in YEAR_CHUNKS:
            url = f"{BASE_URL}/list/model/data/domain/0000/var/{var_id}/th/{chunk}/key/{API_KEY}/"
            try:
                resp = requests.get(url, timeout=30)
                data = resp.json()
                if data.get("data-availability") != "available":
                    time.sleep(1)
                    continue

                vervars = data.get("vervar", [])
                turvars = data.get("turvar", [])
                tahuns = data.get("tahun", [])
                turtahun = data.get("turtahun", [])
                dc = data.get("datacontent", {})
                tt_val = str(turtahun[0]["val"]) if turtahun else "0"

                tahun_dict = {str(t["val"]): t["label"] for t in tahuns}
                turvar_dict = {str(t["val"]): t["label"] for t in turvars}

                for v in vervars:
                    prov_label = re.sub(r"<[^>]*>", "", v.get("label", "")).strip()
                    v_val = str(v["val"])
                    for th_val, th_label in tahun_dict.items():
                        for t_val in turvar_dict:
                            key = f"{v_val}{var_id}{t_val}{th_val}{tt_val}"
                            nilai = dc.get(key) if isinstance(dc, dict) else None
                            if nilai is not None:
                                all_data.append({
                                    "provinsi": prov_label.title(),
                                    "tahun": th_label,
                                    "indikator": var_name,
                                    "nilai": nilai,
                                    "satuan": satuan,
                                })
            except Exception as e:
                print(f"    [!] Error chunk {chunk}: {e}")
            time.sleep(1.5)

    if all_data:
        df = pd.DataFrame(all_data)
        # Bersihkan tahun (ambil 4 digit angka)
        df["tahun"] = df["tahun"].astype(str).str.extract(r"(\d{4})")
        df = df.dropna(subset=["tahun"])
        df["tahun"] = df["tahun"].astype(int)

        # Simpan nasional
        out_nas = OUT_DIR / "nasional_investasi_pmdn_2016_2024.csv"
        df.to_csv(out_nas, index=False, encoding="utf-8")
        print(f"    [OK] Nasional: {len(df)} baris → {out_nas.name}")

        # Filter Sulawesi
        mask = df["provinsi"].str.lower().apply(
            lambda x: any(s in x for s in SULAWESI_PROVS)
        )
        df_sul = df[mask].copy()
        out_sul = OUT_DIR / "sulawesi_investasi_pmdn_2016_2024.csv"
        df_sul.to_csv(out_sul, index=False, encoding="utf-8")
        print(f"    [OK] Sulawesi: {len(df_sul)} baris → {out_sul.name}")
        return True
    else:
        print("    [!] Gagal fetch PMDN nasional")
        return False


# ============================================================
# FETCH: Ekspor Nasional (semua provinsi)
# ============================================================
def fetch_ekspor_nasional():
    """Fetch Ekspor all provinces from BPS API, aggregate yearly."""
    VARS = {
        2346: "Ekspor Non-Migas",
        2347: "Ekspor Migas",
    }

    all_data = []
    print("[*] Fetch: Ekspor Nasional (Var 2346, 2347)")

    for var_id, var_name in VARS.items():
        print(f"    Kategori: {var_name}")
        for chunk in YEAR_CHUNKS:
            url = f"{BASE_URL}/list/model/data/domain/0000/var/{var_id}/th/{chunk}/key/{API_KEY}/"
            try:
                resp = requests.get(url, timeout=30)
                data = resp.json()
                if data.get("data-availability") != "available":
                    time.sleep(1)
                    continue

                vervars = data.get("vervar", [])
                turvars = data.get("turvar", [])
                tahuns = data.get("tahun", [])
                turtahun = data.get("turtahun", [])
                dc = data.get("datacontent", {})

                # Untuk ekspor: turvar=0, turtahun=bulan(1-12)+tahunan(13)
                turvar_val = str(turvars[0]["val"]) if turvars else "0"
                turtahun_dict = {str(t["val"]): t["label"] for t in turtahun}
                tahun_dict = {str(th["val"]): th["label"] for th in tahuns}

                for v in vervars:
                    prov_label = re.sub(r"<[^>]*>", "", v.get("label", "")).strip()
                    v_val = str(v["val"])
                    for th_val, th_label in tahun_dict.items():
                        for tt_val, tt_label in turtahun_dict.items():
                            # Key: vervar + var_id + turvar + tahun + turtahun
                            key = f"{v_val}{var_id}{turvar_val}{th_val}{tt_val}"
                            nilai = dc.get(key) if isinstance(dc, dict) else None
                            if nilai is not None:
                                all_data.append({
                                    "provinsi": prov_label,
                                    "tahun": th_label,
                                    "bulan": tt_label,
                                    "kategori": var_name,
                                    "nilai_ekspor": nilai,
                                    "satuan": "Juta USD",
                                })
            except Exception as e:
                print(f"    [!] Error chunk {chunk}: {e}")
            time.sleep(1.5)

    if all_data:
        df = pd.DataFrame(all_data)
        df["nilai_ekspor"] = pd.to_numeric(df["nilai_ekspor"], errors="coerce")

        # Bersihkan tahun
        df["tahun"] = df["tahun"].astype(str).str.extract(r"(\d{4})")
        df = df.dropna(subset=["tahun"])
        df["tahun"] = df["tahun"].astype(int)

        # Agregasi tahunan (jumlahkan bulanan)
        df_yearly = (
            df.groupby(["provinsi", "tahun", "kategori", "satuan"])["nilai_ekspor"]
            .sum()
            .reset_index()
        )
        df_yearly.rename(columns={"nilai_ekspor": "nilai"}, inplace=True)

        # Simpan nasional
        out_nas = OUT_DIR / "nasional_ekspor_2016_2024.csv"
        df_yearly.to_csv(out_nas, index=False, encoding="utf-8")
        print(f"    [OK] Nasional: {len(df_yearly)} baris → {out_nas.name}")

        # Filter Sulawesi
        mask = df_yearly["provinsi"].str.lower().apply(
            lambda x: any(s in x for s in SULAWESI_PROVS)
        )
        df_sul = df_yearly[mask].copy()
        out_sul = OUT_DIR / "sulawesi_ekspor_2016_2024.csv"
        df_sul.to_csv(out_sul, index=False, encoding="utf-8")
        print(f"    [OK] Sulawesi: {len(df_sul)} baris → {out_sul.name}")
        return True
    else:
        print("    [!] Gagal fetch Ekspor nasional")
        return False


# ============================================================
# PROCESS: PMDN Sulawesi dari raw (fallback kalau fetch gagal)
# ============================================================
def process_pmdn_sulawesi():
    """Copy raw PMDN Sulawesi ke processed (kalau fetch_nasional sudah buat, skip)."""
    out_sul = OUT_DIR / "sulawesi_investasi_pmdn_2016_2024.csv"
    if out_sul.exists():
        print(f"[*] PMDN Sulawesi sudah ada → {out_sul.name} (skip)")
        return

    raw_file = RAW_DIR / "bps_pmdn" / "bps_investasi_pmdn_sulawesi_2016_2026.csv"
    if not raw_file.exists():
        raw_file = RAW_DIR / "bps_pad" / "bps_investasi_pmdn_sulawesi_2016_2026.csv"

    if raw_file.exists():
        df = pd.read_csv(raw_file)
        df.to_csv(out_sul, index=False, encoding="utf-8")
        print(f"[*] PMDN Sulawesi: {len(df)} baris → {out_sul.name} (dari raw)")
    else:
        print("[!] Raw PMDN Sulawesi tidak ditemukan")


# ============================================================
# PROCESS: PAD Sulawesi dari raw API data
# ============================================================
def process_pad_sulawesi():
    """
    Proses PAD Sulawesi dari bps_pad_sulawesi_2016_2026.csv.
    Hanya ambil domain 7100 (Sulawesi Utara) yang berisi perbandingan provinsi.
    Domain 7400 berisi data listrik (bukan PAD), jadi di-skip.
    """
    raw_file = RAW_DIR / "bps_pad" / "bps_pad_sulawesi_2016_2026.csv"
    out_file = OUT_DIR / "sulawesi_pad_2016_2024.csv"

    if not raw_file.exists():
        print("[!] Raw PAD tidak ditemukan")
        return

    df = pd.read_csv(raw_file)
    print(f"[*] PAD raw: {len(df)} baris total")

    # Filter hanya domain 7100 (data PAD per provinsi)
    # Domain 7400 adalah data pelanggan listrik (bukan PAD)
    df_pad = df[df["domain_id"] == 7100].copy()

    # Filter hanya data per provinsi (bukan "INDONESIA" sebagai baseline)
    provinsi_sulawesi = [
        "Sulawesi Utara", "Sulawesi Tengah", "Sulawesi Selatan",
        "Sulawesi Tenggara", "Gorontalo", "Sulawesi Barat",
    ]
    df_pad = df_pad[df_pad["kategori"].isin(provinsi_sulawesi)].copy()

    # Rename kolom untuk konsistensi
    df_pad = df_pad.rename(columns={"kategori": "provinsi"})

    # Bersihkan tahun
    df_pad["tahun"] = pd.to_numeric(df_pad["tahun"], errors="coerce")
    df_pad = df_pad.dropna(subset=["tahun"])
    df_pad["tahun"] = df_pad["tahun"].astype(int)

    df_pad.to_csv(out_file, index=False, encoding="utf-8")
    print(f"    [OK] Sulawesi: {len(df_pad)} baris → {out_file.name}")


# ============================================================
# MAIN
# ============================================================
def main():
    print("=" * 60)
    print("  PROSES DATA: PMDN, Ekspor, PAD → Nasional + Sulawesi")
    print("=" * 60)
    print()

    # 1. Fetch PMDN Nasional dari BPS API
    pmdn_ok = fetch_pmdn_nasional()
    print()

    # 2. Fetch Ekspor Nasional dari BPS API
    ekspor_ok = fetch_ekspor_nasional()
    print()

    # 3. Fallback PMDN Sulawesi dari raw (kalau fetch gagal)
    if not pmdn_ok:
        process_pmdn_sulawesi()
    print()

    # 4. Process PAD Sulawesi dari raw
    process_pad_sulawesi()
    print()

    # Summary
    print("=" * 60)
    print("  RINGKASAN FILE DI PROCESSED:")
    print("=" * 60)
    for f in sorted(OUT_DIR.glob("*.csv")):
        lines = sum(1 for _ in open(f, encoding="utf-8")) - 1
        print(f"  {f.name:50s} ({lines} baris)")


if __name__ == "__main__":
    main()
