"""
CP2 — Rebuild PDRB Sektoral Sulawesi via BPS SIMDASI
======================================================
Jalankan: .venv/Scripts/python.exe scripts/rebuild_pdrb_sektoral_sulawesi.py

Sumber: BPS SIMDASI endpoint id=25
  - Tabel: "PDRB Atas Dasar Harga Berlaku Menurut Lapangan Usaha" per provinsi per tahun
  - Coverage: 2014-2024 (dari SIMDASI Sulteng, perlu dicek per provinsi lain)

Output:
  data/processed/sulawesi_pdrb_sektoral_2016_2024.csv
    Schema: provinsi, tahun, sektor_kode, sektor_nama, nilai_miliar_rp, pct_dari_total

Gate Condition CP2:
  - Kolom sektor_kode tidak ada "Tidak ada"
  - Ada minimal sektor A dan B untuk 6 provinsi Sulawesi
  - Coverage tahun: 2016-2024
"""

import re
import time
from pathlib import Path

import pandas as pd
import requests

API_KEY = "06fd644648629502353deaed29fc6383"
BASE_URL = "https://webapi.bps.go.id/v1/api"

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw" / "bps_simdasi"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# MFD codes 6 Provinsi Sulawesi
SULAWESI_PROVS = {
    "7100000": "Sulawesi Utara",
    "7200000": "Sulawesi Tengah",
    "7300000": "Sulawesi Selatan",
    "7400000": "Sulawesi Tenggara",
    "7500000": "Gorontalo",
    "7600000": "Sulawesi Barat",
}

# Tahun yang difetch
TARGET_YEARS = list(range(2014, 2025))  # 2014-2024

# Sektor utama yang ingin diambil (kode KLU)
SEKTOR_UTAMA = {
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M,N",
    "O",
    "P",
    "Q",
    "R,S,T,U",
}


def clean_html(s):
    return re.sub(r"<[^>]*>", "", str(s)).strip()


def parse_number(s, unit_hint="miliar"):
    """
    Convert Indonesian number format ke float dalam miliar rupiah.
    '51.206,64'      -> 51206.64  (miliar, 1 dot = ribuan)
    '31.036.027,00'  -> 31036.027 (juta, 2 dots = ribuan+jutaan) -> dibagi 1000

    Heuristic unit:
      dots=1 -> miliar rupiah (nilai itu sendiri)
      dots>=2 -> juta rupiah -> bagi 1000 agar jadi miliar
    """
    if s is None or str(s).strip() in ["...", "–", "-", "NA", "", "NA"]:
        return None
    s = str(s).replace("\xa0", "").strip()
    dot_count = s.count(".")
    try:
        val = float(s.replace(".", "").replace(",", "."))
        if dot_count >= 2:
            # Data dalam juta rupiah -> konversi ke miliar
            val = round(val / 1000, 3)
        return val
    except ValueError:
        return None


def is_main_sector(row):
    """Cek apakah baris adalah sektor utama (A, B, C, dst) bukan sub-sektor."""
    label_raw = row.get("label_raw", "").strip()
    html = row.get("label", "")
    # Sektor utama punya div "col-md-2 text-center" berisi huruf
    if "col-md-2 text-center" in html:
        # Ambil isi setelah col-md-2 text-center
        match = re.search(r"col-md-2 text-center[^>]*>(.*?)</div>", html, re.DOTALL)
        if match:
            letter = match.group(1).strip()
            if letter and not letter[0].isdigit() and len(letter) <= 8:
                return True
    # Fallback: label_raw diawali huruf besar diikuti spasi + nama
    parts = label_raw.split(" ", 1)
    if (
        parts
        and len(parts[0]) <= 8
        and parts[0].replace(",", "").replace(" ", "").isalpha()
    ):
        return True
    return False


def get_sektor_kode(row):
    """Ekstrak kode sektor (A, B, C, dll) dari label."""
    html = row.get("label", "")
    match = re.search(r"col-md-2 text-center[^>]*>(.*?)</div>", html, re.DOTALL)
    if match:
        return match.group(1).strip()
    # Fallback dari label_raw
    label_raw = row.get("label_raw", "").strip()
    parts = label_raw.split(" ", 1)
    if parts and len(parts[0]) <= 8:
        return parts[0]
    return "?"


def get_sektor_nama(row):
    """Ekstrak nama sektor dari label (tanpa kode huruf di depan)."""
    label_raw = row.get("label_raw", "").strip()
    # Hapus kode huruf di awal jika ada
    parts = label_raw.split(" ", 1)
    if parts and len(parts[0]) <= 8 and not parts[0][0].isdigit():
        return parts[1].strip() if len(parts) > 1 else label_raw
    return label_raw


def find_pdrb_table_id(mfd_code, provinsi):
    """Cari id_tabel PDRB lapangan usaha (harga berlaku) untuk satu provinsi."""
    url = (
        f"{BASE_URL}/interoperabilitas/datasource/simdasi/id/23"
        f"/wilayah/{mfd_code}/mms_id/531/key/{API_KEY}/"
    )
    try:
        resp = requests.get(url, timeout=30).json()
        content = resp["data"][1] if len(resp.get("data", [])) > 1 else {}
        tables = content.get("data", [])
        for t in tables:
            if not isinstance(t, dict):
                continue
            judul = t.get("judul", "").lower()
            # Target: PDRB harga berlaku + lapangan usaha (bukan distribusi/laju/perkapita)
            if (
                ("pdrb" in judul or "produk domestik regional" in judul)
                and ("lapangan usaha" in judul or "industry" in judul.lower())
                and "berlaku" in judul
                and "distribusi" not in judul
                and "laju" not in judul
                and "kapita" not in judul
                and "kabupaten" not in judul
            ):
                return (
                    t.get("id_tabel"),
                    t.get("judul"),
                    t.get("ketersediaan_tahun", []),
                )
    except Exception as e:
        print(f"    [!] Error find table: {e}")
    return None, None, []


def fetch_pdrb_table(table_id, mfd_code, provinsi, year):
    """Fetch data dari satu tabel PDRB untuk satu tahun."""
    url = (
        f"{BASE_URL}/interoperabilitas/datasource/simdasi/id/25"
        f"/id_tabel/{table_id}/wilayah/{mfd_code}/tahun/{year}/key/{API_KEY}/"
    )
    try:
        resp = requests.get(url, timeout=30).json()
        if resp.get("data-availability") != "available":
            return []

        content = resp["data"][1] if len(resp.get("data", [])) > 1 else {}
        rows = content.get("data", [])
        col_key = (
            list(content.get("kolom", {}).keys())[0] if content.get("kolom") else None
        )
        if not col_key or not rows:
            return []

        results = []
        for r in rows:
            if not is_main_sector(r):
                continue
            kode = get_sektor_kode(r)
            nama = get_sektor_nama(r)
            variables = r.get("variables", {})
            val_raw = (
                variables.get(col_key, {}).get("value_raw")
                if isinstance(variables, dict)
                else None
            )
            nilai = parse_number(val_raw)

            results.append(
                {
                    "provinsi": provinsi,
                    "tahun": year,
                    "sektor_kode": kode,
                    "sektor_nama": nama,
                    "nilai_miliar_rp": nilai,
                }
            )
        return results
    except Exception as e:
        print(f"    [!] Error fetch year {year}: {e}")
        return []


# ── Main ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 65)
    print("  CP2 — REBUILD PDRB SEKTORAL SULAWESI (via SIMDASI)")
    print("=" * 65)

    all_rows = []
    table_registry = {}  # mfd_code -> (table_id, judul, available_years)

    # Step 1: Temukan table_id untuk setiap provinsi
    print("\n>>> STEP 1: Cari Table ID PDRB per Provinsi")
    for mfd, provinsi in SULAWESI_PROVS.items():
        tid, judul, avail_years = find_pdrb_table_id(mfd, provinsi)
        table_registry[mfd] = (tid, provinsi, avail_years)
        if tid:
            print(f"  [OK] {provinsi}: {tid[:20]}... | Tahun: {avail_years}")
        else:
            print(f"  [!!] {provinsi}: TIDAK DITEMUKAN")
        time.sleep(1)

    # Step 2: Fetch data per provinsi per tahun
    print("\n>>> STEP 2: Fetch Data PDRB per Provinsi per Tahun")
    for mfd, (tid, provinsi, avail_years) in table_registry.items():
        if not tid:
            print(f"\n  [SKIP] {provinsi} — table ID tidak ditemukan")
            continue

        print(f"\n  [{provinsi}] table_id={tid[:20]}...")

        # Hanya fetch tahun yang tersedia
        years_to_fetch = [y for y in TARGET_YEARS if y in (avail_years or TARGET_YEARS)]
        if not years_to_fetch:
            years_to_fetch = TARGET_YEARS  # coba semua jika avail_years kosong

        prov_rows = 0
        for year in years_to_fetch:
            rows = fetch_pdrb_table(tid, mfd, provinsi, year)
            if rows:
                all_rows.extend(rows)
                prov_rows += len(rows)
                print(f"    [+] {year}: {len(rows)} sektor")
            else:
                print(f"    [-] {year}: tidak ada data")
            time.sleep(1)

        print(f"  Total rows {provinsi}: {prov_rows}")

    # Step 3: Build processed file
    print("\n" + "=" * 65)
    print("  STEP 3: Build Processed File")
    print("=" * 65)

    if not all_rows:
        print("[FAIL] Tidak ada data yang berhasil difetch!")
    else:
        df = pd.DataFrame(all_rows)

        # Save raw SEBELUM filter (untuk audit)
        raw_path = RAW_DIR / "pdrb_sektoral_sulawesi_raw.csv"
        df.to_csv(raw_path, index=False)
        print(f"[RAW] {raw_path.name} — {len(df)} baris (sebelum filter)")

        # ── FILTER: hanya 17 sektor utama KLU ──────────────────────────────
        # is_main_sector() kadang menangkap sub-sektor (Angkutan, Industri, Jasa,
        # Tanaman) dan baris total (Produk Domestik Bruto). Filter eksplisit lebih aman.
        VALID_KODE = {
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M,N",
            "O",
            "P",
            "Q",
            "R,S,T,U",
        }
        df_dirty = df[~df["sektor_kode"].isin(VALID_KODE)]
        if not df_dirty.empty:
            print(f"[FILTER] Buang {len(df_dirty)} baris sub-sektor/total:")
            print(f"         Kode dibuang: {sorted(df_dirty['sektor_kode'].unique())}")
        df = df[df["sektor_kode"].isin(VALID_KODE)].copy()
        print(f"[FILTER] Setelah filter: {len(df)} baris (17 sektor utama KLU)")

        # Tambah pct_dari_total per provinsi per tahun
        total_per_prov_tahun = (
            df.groupby(["provinsi", "tahun"])["nilai_miliar_rp"]
            .sum()
            .rename("total_pdrb")
            .reset_index()
        )
        df = df.merge(total_per_prov_tahun, on=["provinsi", "tahun"], how="left")
        df["pct_dari_total"] = (df["nilai_miliar_rp"] / df["total_pdrb"] * 100).round(2)
        df = df.drop(columns=["total_pdrb"])

        # Sort
        df = df.sort_values(["provinsi", "tahun", "sektor_kode"]).reset_index(drop=True)

        # Save processed
        proc_path = PROCESSED_DIR / "sulawesi_pdrb_sektoral_2016_2024.csv"
        df.to_csv(proc_path, index=False)
        print(f"[PROCESSED] {proc_path.name} — {len(df)} baris")

        # Preview
        print("\nPreview per provinsi:")
        print(
            df.groupby(["provinsi", "tahun"])
            .size()
            .reset_index(name="sektor_count")
            .to_string()
        )

        # Gate Condition Check
        print("\n" + "=" * 65)
        print("  GATE CONDITION CHECK")
        print("=" * 65)
        has_no_tdk_ada = not (df["sektor_kode"] == "Tidak ada").any()
        has_sektor_A = (
            "A" in df["sektor_kode"].values
            or df["sektor_nama"].str.contains("Pertanian", na=False).any()
        )
        has_sektor_B = (
            "B" in df["sektor_kode"].values
            or df["sektor_nama"].str.contains("Pertambangan", na=False).any()
        )
        all_6_provs = len(df["provinsi"].unique()) == 6
        has_2016_2024 = {2016, 2022, 2024}.issubset(set(df["tahun"].unique()))

        checks = [
            (has_no_tdk_ada, "Kolom sektor_kode tidak ada 'Tidak ada'"),
            (has_sektor_A, "Ada sektor A (Pertanian)"),
            (has_sektor_B, "Ada sektor B (Pertambangan)"),
            (all_6_provs, f"Semua 6 provinsi ada (punya: {df['provinsi'].nunique()})"),
            (
                has_2016_2024,
                f"Coverage 2016-2024 terpenuhi (tahun: {sorted(df['tahun'].unique())[:5]}...)",
            ),
        ]
        all_pass = True
        for passed, label in checks:
            status = "PASS" if passed else "FAIL"
            if not passed:
                all_pass = False
            print(f"  [{status}] {label}")

        print()
        if all_pass:
            print("  CP2 SELESAI — Semua gate condition terpenuhi.")
            print("  Siap lanjut ke CP3 (Populasi Kabupaten via SIMDASI).")
        else:
            print("  CP2 PARTIAL — Cek log di atas.")
            print(
                "  Fallback: gunakan sulawesi_pdrb_per_kapita_sdgs.csv + sulawesi_tk_sektor_sdgs.csv dari CP1."
            )
