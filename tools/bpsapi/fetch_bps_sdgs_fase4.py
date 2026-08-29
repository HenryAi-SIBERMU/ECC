"""
CP1 — Fetch BPS SDGs Variables untuk Fase 4
============================================
Jalankan dengan: .venv/Scripts/python.exe scripts/fetch_bps_sdgs_fase4.py

Temuan dari eksplorasi API (penting untuk dipahami sebelum menjalankan):

  GRUP A — Province-level (vervar = 38 Provinsi, filter val 7100-7600):
    288  : PDRB Per Kapita per Provinsi
    296  : Laju Pertumbuhan PDRB Per Kapita per Provinsi
    1344 : Nilai Tambah Pertanian / TK Pertanian per Provinsi
    2153 : Proporsi Kerja Informal per Provinsi
    1241 : % Rumah Tangga Akses Hunian Layak per Provinsi
    1214 : Proporsi Nilai Tambah Manufaktur ke PDB per Provinsi
    1172 : Upah Rata-rata Per Jam per Provinsi

  GRUP B — Kabupaten/Kota level (vervar = 552 wilayah, filter val 7100-7699):
    621  : % Penduduk Miskin per Kabupaten/Kota

  SKIP (bukan province-level):
    1217 : vervar = Jenis Industri (nasional, bukan provinsi)
    2154 : vervar = Perkotaan/Perdesaan (nasional)
    2190 : list-not-available
    2191 : list-not-available

Output raw  : data/raw/bps_sdgs/sdgs_var_{ID}_raw.csv
Output processed:
    sulawesi_tk_sektor_sdgs.csv        (Grup A: 2153, 1214, 1344)
    sulawesi_pdrb_per_kapita_sdgs.csv  (Grup A: 288, 296)
    sulawesi_upah_hunian_sdgs.csv      (Grup A: 1172, 1241)
    sulawesi_kemiskinan_kab_sdgs.csv   (Grup B: 621 — kabupaten level)
"""

import re
import time
from pathlib import Path

import pandas as pd
import requests

# ── Config ────────────────────────────────────────────────────────────────
API_KEY = "06fd644648629502353deaed29fc6383"
BASE_URL = "https://webapi.bps.go.id/v1/api"
DOMAIN = "0000"
RATE_WAIT = 1.5  # detik antar request

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw" / "bps_sdgs"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# Tahun 2014-2024 → BPS ID 114-124
YEAR_CHUNKS = ["114:115", "116:117", "118:119", "120:121", "122:123", "124"]

# Grup A: vervar = 38 Provinsi — filter val 7100, 7200, 7300, 7400, 7500, 7600
SULAWESI_PROV_VALS = {7100, 7200, 7300, 7400, 7500, 7600}

GRUP_A = {
    288: "PDRB Per Kapita",
    296: "Laju Pertumbuhan PDRB Per Kapita",
    1344: "Nilai Tambah Pertanian per TK Pertanian",
    2153: "Proporsi Kerja Informal",
    1241: "Persen Hunian Layak",
    1214: "Proporsi Nilai Tambah Manufaktur ke PDB",
    1172: "Upah Rata-rata Per Jam",
}

# Grup B: vervar = kab/kota — filter val 7100-7699 (seluruh wilayah Sulawesi)
GRUP_B = {
    621: "Persen Penduduk Miskin",
}


def clean_html(s):
    return re.sub(r"<[^>]*>", "", str(s)).strip()


def fetch_var_data(var_id, var_name, sulawesi_val_filter):
    """
    Fetch satu var. sulawesi_val_filter: set atau lambda val -> bool.
    Return DataFrame dengan kolom: wilayah, turvar_label, tahun, nilai, var_id, var_name.
    """
    all_rows = []
    print(f"\n  [VAR {var_id}] {var_name}")

    for chunk in YEAR_CHUNKS:
        url = (
            f"{BASE_URL}/list/model/data/domain/{DOMAIN}"
            f"/var/{var_id}/th/{chunk}/key/{API_KEY}/"
        )
        try:
            resp = requests.get(url, timeout=30)
            data = resp.json()
        except Exception as e:
            print(f"    [!] chunk {chunk} — error: {e}")
            time.sleep(RATE_WAIT)
            continue

        if data.get("data-availability") != "available":
            print(f"    [-] chunk {chunk} — not available")
            time.sleep(RATE_WAIT)
            continue

        vervars = data.get("vervar", [])
        turvars = data.get("turvar", [])
        tahuns = data.get("tahun", [])
        turtahun = data.get("turtahun", [])
        dc = data.get("datacontent", {})

        if not dc:
            print(f"    [-] chunk {chunk} — datacontent kosong")
            time.sleep(RATE_WAIT)
            continue

        tt_val = str(turtahun[0]["val"]) if turtahun else "0"
        tahun_dict = {str(t["val"]): t["label"] for t in tahuns}
        turvar_dict = (
            {str(t["val"]): t["label"] for t in turvars} if turvars else {"0": var_name}
        )

        chunk_count = 0
        for v in vervars:
            v_val_int = v["val"]
            # Filter Sulawesi
            if callable(sulawesi_val_filter):
                if not sulawesi_val_filter(v_val_int):
                    continue
            else:
                if v_val_int not in sulawesi_val_filter:
                    continue

            v_val = str(v_val_int)
            v_label = clean_html(v.get("label", ""))

            for t_val, t_label in turvar_dict.items():
                for th_val, th_label in tahun_dict.items():
                    key = f"{v_val}{var_id}{t_val}{th_val}{tt_val}"
                    nilai = dc.get(key)
                    if nilai is not None:
                        all_rows.append(
                            {
                                "wilayah": v_label.title(),
                                "wilayah_val": v_val_int,
                                "turvar_label": clean_html(t_label),
                                "tahun": th_label,
                                "nilai": nilai,
                                "var_id": var_id,
                                "var_name": var_name,
                            }
                        )
                        chunk_count += 1

        print(f"    [+] chunk {chunk} — {chunk_count} baris Sulawesi")
        time.sleep(RATE_WAIT)

    return pd.DataFrame(all_rows) if all_rows else pd.DataFrame()


def save_raw(var_id, df):
    if df.empty:
        return
    path = RAW_DIR / f"sdgs_var_{var_id}_raw.csv"
    df.to_csv(path, index=False)
    print(f"    [RAW] {path.name} — {len(df)} baris")


# ── Main ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 65)
    print("  CP1 — BPS SDGs FASE 4: DEMOGRAFI & KETENAGAKERJAAN")
    print("=" * 65)

    collected = {}  # var_id -> DataFrame

    # ── Grup A: Province-level ───────────────────────────────────────────
    print("\n>>> GRUP A — Province-level (filter val Sulawesi: 7100-7600)")
    for var_id, var_name in GRUP_A.items():
        df = fetch_var_data(var_id, var_name, SULAWESI_PROV_VALS)
        save_raw(var_id, df)
        collected[var_id] = df

    # ── Grup B: Kabupaten-level ──────────────────────────────────────────
    print("\n>>> GRUP B — Kabupaten/Kota level (filter val 7100-7699)")
    for var_id, var_name in GRUP_B.items():
        df = fetch_var_data(var_id, var_name, lambda v: 7100 <= v <= 7699)
        save_raw(var_id, df)
        collected[var_id] = df

    # ── Build Processed Files ────────────────────────────────────────────
    print("\n" + "=" * 65)
    print("  BUILDING PROCESSED FILES")
    print("=" * 65)

    def save_processed(fname, df, label):
        if df.empty:
            print(f"  [--] {fname} — kosong, skip")
            return
        path = PROCESSED_DIR / fname
        df.to_csv(path, index=False)
        print(f"  [OK] {fname} — {len(df)} baris")
        # Preview per wilayah
        if "wilayah" in df.columns:
            counts = df.groupby("wilayah")["nilai"].count()
            print("       " + " | ".join(f"{w}: {n}" for w, n in counts.items()))

    # 1. TK Sektor (2153, 1214, 1344)
    df_tk = pd.concat(
        [collected.get(v, pd.DataFrame()) for v in [2153, 1214, 1344]],
        ignore_index=True,
    )
    save_processed("sulawesi_tk_sektor_sdgs.csv", df_tk, "TK Sektor")

    # 2. PDRB Per Kapita (288, 296)
    df_pdrb = pd.concat(
        [collected.get(v, pd.DataFrame()) for v in [288, 296]], ignore_index=True
    )
    save_processed("sulawesi_pdrb_per_kapita_sdgs.csv", df_pdrb, "PDRB Per Kapita")

    # 3. Upah & Hunian (1172, 1241)
    df_upah = pd.concat(
        [collected.get(v, pd.DataFrame()) for v in [1172, 1241]], ignore_index=True
    )
    save_processed("sulawesi_upah_hunian_sdgs.csv", df_upah, "Upah & Hunian")

    # 4. Kemiskinan Kabupaten (621)
    df_miskin = collected.get(621, pd.DataFrame())
    save_processed("sulawesi_kemiskinan_kab_sdgs.csv", df_miskin, "Kemiskinan Kab")

    # ── Gate Condition Summary ───────────────────────────────────────────
    print("\n" + "=" * 65)
    print("  GATE CONDITION CHECK")
    print("=" * 65)
    output_files = [
        "sulawesi_tk_sektor_sdgs.csv",
        "sulawesi_pdrb_per_kapita_sdgs.csv",
        "sulawesi_upah_hunian_sdgs.csv",
        "sulawesi_kemiskinan_kab_sdgs.csv",
    ]
    all_pass = True
    for fname in output_files:
        fpath = PROCESSED_DIR / fname
        if fpath.exists():
            n = len(pd.read_csv(fpath))
            status = "PASS" if n > 0 else "FAIL (kosong)"
            if n == 0:
                all_pass = False
        else:
            status = "FAIL (tidak ada)"
            all_pass = False
        print(f"  [{status}] {fname}")

    print()
    if all_pass:
        print("  CP1 SELESAI — Semua gate condition terpenuhi.")
        print("  Siap lanjut ke CP2 (PDRB Sektoral Rebuild) dan CP3 (SIMDASI).")
    else:
        print("  CP1 PARTIAL — Cek log di atas untuk var yang gagal.")
