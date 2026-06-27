"""
CP4 — Build Master Demografi & Employment Shift Fase 4
=======================================================
Jalankan: .venv/Scripts/python.exe scripts/build_demografi_fase4.py

Input utama:
  - sulawesi_populasi_kab_simdasi.csv       (CP3)
  - sulawesi_pdrb_sektoral_2016_2024.csv    (CP2)
  - sulawesi_tk_sektor_sdgs.csv             (CP1)
  - sulawesi_kemiskinan_kab_sdgs.csv        (CP1)
  - zoonosis_kab_kota_2015_2024.csv         (existing)
  - sulawesi_investasi_pmdn_2016_2024.csv   (existing)

Output:
  - data/processed/sulawesi_demografi_master_fase4.csv
  - data/processed/sulawesi_employment_shift_fase4.csv
  - data/processed/sulawesi_pdrb_shift_index_2016_2024.csv
"""

import re
from pathlib import Path

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED = BASE_DIR / "data" / "processed"

SMELTER_KABS = {
    "Morowali",
    "Morowali Utara",
    "Banggai",
    "Konawe",
    "Konawe Utara",
    "Kolaka",
    "Luwu Timur",
}


def norm_name(s):
    return str(s).strip().title()


def build_demografi_master():
    print("\n=== BUILD DEMOGRAFI MASTER ===")
    pop = pd.read_csv(PROCESSED / "sulawesi_populasi_kab_simdasi.csv")
    miskin = pd.read_csv(PROCESSED / "sulawesi_kemiskinan_kab_sdgs.csv")
    zoonosis = pd.read_csv(PROCESSED / "zoonosis_kab_kota_2015_2024.csv")
    inv = pd.read_csv(PROCESSED / "sulawesi_investasi_pmdn_2016_2024.csv")

    # Window riset utama
    df = pop[(pop["tahun"] >= 2014) & (pop["tahun"] <= 2024)].copy()
    df["kabupaten_norm"] = df["kabupaten"].apply(norm_name)
    df["provinsi_norm"] = df["provinsi"].apply(norm_name)

    # Ensure is_smelter explicit
    df["is_smelter"] = df["kabupaten"].isin(SMELTER_KABS)

    # Anomaly flag: YoY > 2x median provinsi-tahun (hanya jika YoY tidak null)
    med = df.groupby(["provinsi", "tahun"])["laju_pertumbuhan_yoy_pct"].transform(
        "median"
    )
    df["anomali_pertumbuhan_flag"] = (df["laju_pertumbuhan_yoy_pct"].notna()) & (
        df["laju_pertumbuhan_yoy_pct"] > (2 * med)
    )

    # ── Merge kemiskinan kab/kota (Var 621) ─────────────────────────────
    # Penting: jangan merge hanya kabupaten+tahun karena ada nama ambigu dan
    # file SDGs berisi provinsi aggregate + kab/kota. Gunakan wilayah_val
    # untuk derive provinsi dan buang aggregate provinsi (kode berakhiran 00).
    prov_code_map = {
        71: "Sulawesi Utara",
        72: "Sulawesi Tengah",
        73: "Sulawesi Selatan",
        74: "Sulawesi Tenggara",
        75: "Gorontalo",
        76: "Sulawesi Barat",
    }
    miskin = miskin.rename(columns={"wilayah": "kabupaten", "nilai": "pct_miskin"})
    miskin["wilayah_val"] = pd.to_numeric(miskin["wilayah_val"], errors="coerce")
    miskin["tahun"] = pd.to_numeric(miskin["tahun"], errors="coerce")
    miskin = miskin[miskin["wilayah_val"].notna()].copy()
    # Keep only kabupaten/kota rows, exclude province aggregate 7100/7200/etc.
    miskin = miskin[(miskin["wilayah_val"] >= 7100) & (miskin["wilayah_val"] <= 7699)]
    miskin = miskin[miskin["wilayah_val"] % 100 != 0].copy()
    miskin["provinsi"] = (miskin["wilayah_val"] // 100).map(prov_code_map)
    miskin["kabupaten_norm"] = miskin["kabupaten"].apply(norm_name)
    miskin["provinsi_norm"] = miskin["provinsi"].apply(norm_name)
    miskin_small = (
        miskin[["provinsi_norm", "kabupaten_norm", "tahun", "pct_miskin", "var_id"]]
        .drop_duplicates(["provinsi_norm", "kabupaten_norm", "tahun"])
        .copy()
    )
    miskin_small = miskin_small.rename(columns={"var_id": "pct_miskin_var_id"})
    df = df.merge(
        miskin_small, on=["provinsi_norm", "kabupaten_norm", "tahun"], how="left"
    )

    # ── Merge DBD cases dari zoonosis ───────────────────────────────────
    z = zoonosis.copy()
    z = z[z["jenis_penyakit"].str.upper() == "DBD"].copy()
    z["kabupaten_norm"] = z["kabupaten_kota"].apply(norm_name)
    z["tahun"] = pd.to_numeric(z["tahun"], errors="coerce")
    z_agg = z.groupby(["kabupaten_norm", "tahun"], as_index=False).agg(
        dbd_kasus=("total_kasus", "sum"), dbd_meninggal=("meninggal", "sum")
    )
    df = df.merge(z_agg, on=["kabupaten_norm", "tahun"], how="left")
    df["dbd_kasus"] = df["dbd_kasus"].fillna(0).astype(int)
    df["dbd_meninggal"] = df["dbd_meninggal"].fillna(0).astype(int)

    # ── Merge PMDN provinsi ─────────────────────────────────────────────
    # PMDN punya 2 indikator per provinsi-tahun (Nilai + Jumlah Proyek).
    # Untuk master demografi, pakai hanya nilai investasi agar tidak menggandakan rows.
    inv = inv[inv["indikator"].str.contains("Nilai", case=False, na=False)].copy()
    inv = inv.rename(columns={"nilai": "pmdn_nilai_juta_rp"})
    inv["provinsi_norm"] = inv["provinsi"].apply(norm_name)
    inv["tahun"] = pd.to_numeric(inv["tahun"], errors="coerce")
    inv_small = (
        inv[["provinsi_norm", "tahun", "pmdn_nilai_juta_rp"]]
        .drop_duplicates(["provinsi_norm", "tahun"])
        .copy()
    )
    df = df.merge(inv_small, on=["provinsi_norm", "tahun"], how="left")

    # Rename/arrange columns
    out_cols = [
        "provinsi",
        "kabupaten",
        "tahun",
        "jumlah_penduduk_rb",
        "kepadatan_per_km2",
        "laju_pertumbuhan_sumber_pct",
        "laju_pertumbuhan_yoy_pct",
        "anomali_pertumbuhan_flag",
        "is_smelter",
        "iup_kumulatif",
        "pct_miskin",
        "dbd_kasus",
        "dbd_meninggal",
        "pmdn_nilai_juta_rp",
    ]
    df_out = (
        df[out_cols]
        .sort_values(["provinsi", "kabupaten", "tahun"])
        .reset_index(drop=True)
    )

    out = PROCESSED / "sulawesi_demografi_master_fase4.csv"
    df_out.to_csv(out, index=False)
    print(f"[SAVED] {out.name} — {len(df_out)} baris")
    print(
        f"  Provinsi: {df_out['provinsi'].nunique()} | Kabupaten: {df_out['kabupaten'].nunique()} | Tahun: {df_out['tahun'].min()}-{df_out['tahun'].max()}"
    )
    print(
        f"  Smelter kab: {sorted(df_out[df_out['is_smelter']]['kabupaten'].unique())}"
    )
    print(
        f"  Null key pop: {df_out[['jumlah_penduduk_rb', 'kepadatan_per_km2', 'is_smelter']].isnull().sum().sum()}"
    )
    return df_out


def build_employment_shift():
    print("\n=== BUILD EMPLOYMENT / PDRB SHIFT ===")
    pdrb = pd.read_csv(PROCESSED / "sulawesi_pdrb_sektoral_2016_2024.csv")
    tk = pd.read_csv(PROCESSED / "sulawesi_tk_sektor_sdgs.csv")

    # Pivot PDRB sektor kunci
    key = pdrb[pdrb["sektor_kode"].isin(["A", "B", "C", "F"])].copy()
    pivot_pct = key.pivot_table(
        index=["provinsi", "tahun"],
        columns="sektor_kode",
        values="pct_dari_total",
        aggfunc="first",
    ).reset_index()
    pivot_val = key.pivot_table(
        index=["provinsi", "tahun"],
        columns="sektor_kode",
        values="nilai_miliar_rp",
        aggfunc="first",
    ).reset_index()

    # Rename columns
    pivot_pct = pivot_pct.rename(
        columns={
            "A": "pct_pdrb_pertanian_A",
            "B": "pct_pdrb_pertambangan_B",
            "C": "pct_pdrb_industri_C",
            "F": "pct_pdrb_konstruksi_F",
        }
    )
    pivot_val = pivot_val.rename(
        columns={
            "A": "nilai_pertanian_miliar",
            "B": "nilai_pertambangan_miliar",
            "C": "nilai_industri_miliar",
            "F": "nilai_konstruksi_miliar",
        }
    )

    shift = pivot_pct.merge(pivot_val, on=["provinsi", "tahun"], how="left")
    shift["pct_industri_tambang_BC"] = (
        shift["pct_pdrb_pertambangan_B"] + shift["pct_pdrb_industri_C"]
    ).round(2)
    shift["agriculture_to_industry_shift_index"] = (
        (shift["pct_industri_tambang_BC"] / shift["pct_pdrb_pertanian_A"])
        .replace([np.inf, -np.inf], np.nan)
        .round(3)
    )

    # Merge SDGs employment-ish vars
    tk_small = tk.pivot_table(
        index=["wilayah", "tahun"], columns="var_name", values="nilai", aggfunc="first"
    ).reset_index()
    tk_small = tk_small.rename(columns={"wilayah": "provinsi"})
    shift = shift.merge(tk_small, on=["provinsi", "tahun"], how="left")

    # Delta from first to latest per province for narrative
    shift = shift.sort_values(["provinsi", "tahun"]).reset_index(drop=True)
    for col in [
        "pct_pdrb_pertanian_A",
        "pct_industri_tambang_BC",
        "agriculture_to_industry_shift_index",
    ]:
        first = shift.groupby("provinsi")[col].transform("first")
        shift[f"delta_{col}_from_first"] = (shift[col] - first).round(2)

    out1 = PROCESSED / "sulawesi_employment_shift_fase4.csv"
    out2 = PROCESSED / "sulawesi_pdrb_shift_index_2016_2024.csv"
    shift.to_csv(out1, index=False)
    shift.to_csv(out2, index=False)
    print(f"[SAVED] {out1.name} — {len(shift)} baris")
    print(f"[SAVED] {out2.name} — {len(shift)} baris")
    print("  Sulteng shift sample:")
    print(
        shift[shift["provinsi"] == "Sulawesi Tengah"][
            [
                "tahun",
                "pct_pdrb_pertanian_A",
                "pct_industri_tambang_BC",
                "agriculture_to_industry_shift_index",
            ]
        ].to_string(index=False)
    )
    return shift


if __name__ == "__main__":
    demografi = build_demografi_master()
    shift = build_employment_shift()

    print("\n=== GATE CONDITION CP4 ===")
    checks = [
        (len(demografi) > 0, "demografi master tidak kosong"),
        (
            demografi[
                ["provinsi", "kabupaten", "tahun", "jumlah_penduduk_rb", "is_smelter"]
            ]
            .isnull()
            .sum()
            .sum()
            == 0,
            "kolom kunci demografi non-null",
        ),
        (len(shift) > 0, "employment shift tidak kosong"),
        (
            shift[
                ["provinsi", "tahun", "pct_pdrb_pertanian_A", "pct_industri_tambang_BC"]
            ]
            .isnull()
            .sum()
            .sum()
            == 0,
            "kolom kunci shift non-null",
        ),
    ]
    all_pass = True
    for ok, label in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}")
        all_pass = all_pass and ok
    print("\n  CP4 SELESAI." if all_pass else "\n  CP4 PARTIAL — cek log.")
