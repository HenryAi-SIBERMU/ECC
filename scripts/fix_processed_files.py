"""
Fix issues in processed files:
1. sulawesi_pad: duplicate provinsi column, rename to clear indicator
2. ekspor: normalize province names (Title Case), fix year range in filename
"""
import os
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUT_DIR = BASE_DIR / "data" / "processed"
BAK_DIR = OUT_DIR / "BAK"
os.makedirs(BAK_DIR, exist_ok=True)


def fix_pad():
    """Fix sulawesi_pad_2016_2024.csv:
    - Original has duplicate 'provinsi' column
    - Rename to clear structure: provinsi, tahun, kategori_pad, nilai, satuan
    """
    f = OUT_DIR / "sulawesi_pad_2016_2024.csv"
    if not f.exists():
        print("[!] File PAD tidak ditemukan")
        return

    df = pd.read_csv(f)
    print(f"[*] PAD original: {len(df)} baris, kolom: {list(df.columns)}")

    # The CSV has: domain_id, provinsi, tahun, kategori(=provinsi2), nilai_rupiah, satuan
    # Read raw to get actual column positions
    df_raw = pd.read_csv(f, header=None, skiprows=1)
    # Columns: 0=domain_id, 1=provinsi(domain), 2=tahun, 3=kategori(provinsi_data), 4=nilai, 5=satuan
    df_clean = pd.DataFrame({
        "domain_id": df_raw[0].values,
        "provinsi_asal": df_raw[1].values,
        "tahun": df_raw[2].values,
        "provinsi": df_raw[3].values,
        "nilai": df_raw[4].values,
        "satuan": df_raw[5].values,
    })

    # Filter hanya provinsi Sulawesi (bukan "INDONESIA" baseline)
    provinsi_sul = [
        "Sulawesi Utara", "Sulawesi Tengah", "Sulawesi Selatan",
        "Sulawesi Tenggara", "Gorontalo", "Sulawesi Barat",
    ]
    df_clean = df_clean[df_clean["provinsi"].isin(provinsi_sul)]

    # Drop domain_id dan provinsi_asal (redundant)
    df_clean = df_clean[["provinsi", "tahun", "nilai", "satuan"]].copy()

    # Bersihkan tahun
    df_clean["tahun"] = pd.to_numeric(df_clean["tahun"], errors="coerce")
    df_clean = df_clean.dropna(subset=["tahun"])
    df_clean["tahun"] = df_clean["tahun"].astype(int)

    # Rename tahun column to reflect actual content
    # Note: nilai dalam file ini adalah rasio/per kapita, bukan total PAD
    out = OUT_DIR / "sulawesi_pad_2016_2024.csv"
    df_clean.to_csv(out, index=False, encoding="utf-8")
    print(f"    [OK] Fixed: {len(df_clean)} baris → {out.name}")
    print(f"    Tahun range: {df_clean['tahun'].min()}-{df_clean['tahun'].max()}")


def fix_ekspor():
    """Fix ekspor files:
    - Normalize province names to Title Case
    - Update filename year range to match actual data
    """
    for scope in ["nasional", "sulawesi"]:
        f = OUT_DIR / f"{scope}_ekspor_2016_2024.csv"
        if not f.exists():
            continue

        df = pd.read_csv(f)
        print(f"\n[*] Ekspor {scope}: {len(df)} baris")
        print(f"    Tahun actual: {df['tahun'].min()}-{df['tahun'].max()}")

        # Normalize province names to Title Case
        df["provinsi"] = df["provinsi"].str.title()

        # Get actual year range
        tahun_min = int(df["tahun"].min())
        tahun_max = int(df["tahun"].max())
        new_name = f"{scope}_ekspor_{tahun_min}_{tahun_max}.csv"

        # Move old file to BAK
        bak_file = BAK_DIR / f.name
        os.rename(f, bak_file)
        print(f"    Moved old → BAK/{f.name}")

        # Save with new name
        out = OUT_DIR / new_name
        df.to_csv(out, index=False, encoding="utf-8")
        print(f"    [OK] Fixed: {len(df)} baris → {new_name}")


if __name__ == "__main__":
    print("=" * 60)
    print("  FIX PROCESSED FILES")
    print("=" * 60)
    fix_pad()
    fix_ekspor()

    print("\n" + "=" * 60)
    print("  FILE LISTING:")
    print("=" * 60)
    for f in sorted(OUT_DIR.glob("*.csv")):
        lines = sum(1 for _ in open(f, encoding="utf-8")) - 1
        print(f"  {f.name:50s} ({lines} baris)")
