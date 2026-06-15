"""
Merge 11 file intermediate_kemenkes (2014-2024) → processed CSV.
Indikator: ISPA/Pneumonia, Diare, Kusta, Malaria.

Output:
- nasional_kesehatan_detail_2014_2024.csv (semua provinsi)
- sulawesi_kesehatan_detail_2014_2024.csv (6 provinsi Sulawesi)
"""
import pandas as pd
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw" / "intermediate_kemenkes"
OUT_DIR = BASE_DIR / "data" / "processed"

SULAWESI_PROVS = [
    "Sulawesi Utara", "Sulawesi Tengah", "Sulawesi Selatan",
    "Sulawesi Tenggara", "Gorontalo", "Sulawesi Barat",
]


def main():
    print("=" * 60)
    print("  MERGE KEMENKES DETAIL (ISPA, Diare, Kusta, Malaria)")
    print("=" * 60)

    all_dfs = []
    for tahun in range(2014, 2025):
        f = RAW_DIR / f"kemenkes_bersih_{tahun}.csv"
        if f.exists():
            df = pd.read_csv(f)
            all_dfs.append(df)
            indikator_list = df["indikator"].unique()
            print(f"  [{tahun}] {len(df)} baris, indikator: {list(indikator_list)}")
        else:
            print(f"  [{tahun}] File tidak ditemukan!")

    if not all_dfs:
        print("[!] Tidak ada data untuk di-merge")
        return

    # Merge semua tahun
    df_merged = pd.concat(all_dfs, ignore_index=True)

    # Normalisasi nama provinsi (strip whitespace)
    df_merged["provinsi"] = df_merged["provinsi"].str.strip()

    # Pastikan tahun integer
    df_merged["tahun"] = df_merged["tahun"].astype(int)

    # Pastikan nilai numeric
    df_merged["nilai"] = pd.to_numeric(df_merged["nilai"], errors="coerce")

    print(f"\n[*] Total merged: {len(df_merged)} baris")
    print(f"[*] Tahun: {df_merged['tahun'].min()}-{df_merged['tahun'].max()}")
    print(f"[*] Indikator: {sorted(df_merged['indikator'].unique())}")
    print(f"[*] Provinsi: {df_merged['provinsi'].nunique()} unique")

    # 1. Simpan NASIONAL
    out_nas = OUT_DIR / "nasional_kesehatan_detail_2014_2024.csv"
    df_merged.to_csv(out_nas, index=False, encoding="utf-8")
    print(f"\n[OK] Nasional: {len(df_merged)} baris → {out_nas.name}")

    # 2. Filter & simpan SULAWESI
    mask = df_merged["provinsi"].isin(SULAWESI_PROVS)
    df_sul = df_merged[mask].copy()
    out_sul = OUT_DIR / "sulawesi_kesehatan_detail_2014_2024.csv"
    df_sul.to_csv(out_sul, index=False, encoding="utf-8")
    print(f"[OK] Sulawesi: {len(df_sul)} baris → {out_sul.name}")

    # Preview Sulawesi
    print(f"\n=== PREVIEW SULAWESI (ISPA/Pneumonia) ===")
    ispa_sul = df_sul[df_sul["indikator"] == "Kasus ISPA/Pneumonia"]
    pivot = ispa_sul.pivot_table(index="provinsi", columns="tahun", values="nilai")
    print(pivot.to_string())

    print(f"\n=== PREVIEW SULAWESI (Diare) ===")
    diare_sul = df_sul[df_sul["indikator"] == "Kasus Diare Dilayani"]
    pivot2 = diare_sul.pivot_table(index="provinsi", columns="tahun", values="nilai")
    print(pivot2.to_string())


if __name__ == "__main__":
    main()
