"""
Extract raw ekspor Excel (Sulsel BPS) ke processed CSV.

Struktur Excel:
- Row 0: Judul
- Row 1: Negara tujuan (header group)
- Row 2: Pelabuhan per negara
- Row 3: Sub-header (empty)
- Row 4: Column headers (Kode HS, Tahun)
- Row 5+: Data rows

Output:
- sulawesi_ekspor_detail_2020_2026.csv (long format: hs_code, deskripsi, tahun, negara, pelabuhan, nilai)
- sulawesi_ekspor_negara_2020_2026.csv (aggregated by country + year)
"""
import pandas as pd
import numpy as np
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw" / "eksporimpor"
OUT_DIR = BASE_DIR / "data" / "processed"

XLSX = RAW_DIR / "exim_sulsel.bps.go.id_Selasa, 09 Juni 2026 pukul 12.24.09.xlsx"


def parse_excel():
    """Parse Excel into structured data."""
    df_raw = pd.read_excel(XLSX, header=None)
    print(f"Raw shape: {df_raw.shape}")

    # Extract country info from Row 1
    # Countries at specific columns: CHINA(3), INDIA(62), JAPAN(107), SINGAPORE(156), USA(179), Total(214)
    country_starts = {}
    for col_idx in range(df_raw.shape[1]):
        val = df_raw.iloc[1, col_idx]
        if pd.notna(val) and val not in ("Negara/Wilayah/Entitas Tertentu", "Totals"):
            country_starts[col_idx] = str(val).strip()

    # Add Total column
    country_starts[214] = "TOTAL"

    print(f"Countries found: {list(country_starts.values())}")

    # Determine column ranges per country
    sorted_cols = sorted(country_starts.keys())
    country_ranges = {}
    for i, col_start in enumerate(sorted_cols):
        if i + 1 < len(sorted_cols):
            col_end = sorted_cols[i + 1]
        else:
            col_end = df_raw.shape[1]
        country_ranges[country_starts[col_start]] = (col_start, col_end)

    print(f"Country column ranges: {country_ranges}")

    # Extract port names from Row 2
    port_map = {}  # col_idx -> (country, port_name)
    for country, (col_start, col_end) in country_ranges.items():
        for col_idx in range(col_start, col_end):
            port_val = df_raw.iloc[2, col_idx]
            if pd.notna(port_val):
                port_map[col_idx] = (country, str(port_val).strip())

    print(f"Ports found: {len(port_map)}")
    for col_idx, (country, port) in list(port_map.items())[:10]:
        print(f"  Col {col_idx}: {country} / {port}")

    # Data starts at row 5
    # Col 0 = HS Code + Description, Col 1 = Year, Col 2 = (likely empty or subcategory)
    # Col 3+ = Values per port

    records = []
    current_hs = None
    current_desc = None

    for row_idx in range(5, df_raw.shape[0]):
        col0 = df_raw.iloc[row_idx, 0]
        year = df_raw.iloc[row_idx, 1]

        # Update HS code if present
        if pd.notna(col0):
            hs_str = str(col0).strip()
            # Parse HS code and description: "[03023200] Yellowfin tunas..."
            if hs_str.startswith("["):
                bracket_end = hs_str.find("]")
                if bracket_end > 0:
                    current_hs = hs_str[1:bracket_end]
                    current_desc = hs_str[bracket_end + 1:].strip()
                else:
                    current_hs = hs_str
                    current_desc = hs_str
            else:
                current_hs = hs_str
                current_desc = hs_str

        # Skip if no year
        if pd.isna(year):
            continue

        year = int(year)

        # Extract values for each port
        for col_idx, (country, port) in port_map.items():
            val = df_raw.iloc[row_idx, col_idx]
            if pd.notna(val):
                try:
                    val_float = float(val)
                    if val_float > 0:
                        records.append({
                            "kode_hs": current_hs,
                            "deskripsi": current_desc,
                            "tahun": year,
                            "negara_tujuan": country,
                            "pelabuhan": port,
                            "nilai_usd": val_float,
                        })
                except (ValueError, TypeError):
                    pass

        # Also get the Total column (col 214)
        total_val = df_raw.iloc[row_idx, 214]
        if pd.notna(total_val):
            try:
                total_float = float(total_val)
                if total_float > 0:
                    records.append({
                        "kode_hs": current_hs,
                        "deskripsi": current_desc,
                        "tahun": year,
                        "negara_tujuan": "TOTAL",
                        "pelabuhan": "SEMUA",
                        "nilai_usd": total_float,
                    })
            except (ValueError, TypeError):
                pass

    return pd.DataFrame(records)


def main():
    print("=" * 60)
    print("  EXTRACT EKSPOR DETAIL (SULSEL BPS)")
    print("=" * 60)
    print()

    df = parse_excel()
    print(f"\n[*] Total records: {len(df)}")
    print(f"[*] Tahun range: {df['tahun'].min()}-{df['tahun'].max()}")
    print(f"[*] Negara: {sorted(df['negara_tujuan'].unique())}")
    print(f"[*] HS codes: {df['kode_hs'].nunique()} unique")

    # 1. Save detail file (long format)
    out_detail = OUT_DIR / "sulawesi_ekspor_detail_2020_2026.csv"
    df.to_csv(out_detail, index=False, encoding="utf-8")
    print(f"\n[OK] Detail: {len(df)} baris → {out_detail.name}")

    # 2. Aggregate by country + year
    df_agg = (
        df.groupby(["negara_tujuan", "tahun"])["nilai_usd"]
        .sum()
        .reset_index()
    )
    out_negara = OUT_DIR / "sulawesi_ekspor_negara_2020_2026.csv"
    df_agg.to_csv(out_negara, index=False, encoding="utf-8")
    print(f"[OK] Per Negara: {len(df_agg)} baris → {out_negara.name}")

    # 3. Aggregate by HS code + year (top commodities)
    df_komoditas = (
        df.groupby(["kode_hs", "deskripsi", "tahun"])["nilai_usd"]
        .sum()
        .reset_index()
    )
    out_komoditas = OUT_DIR / "sulawesi_ekspor_komoditas_2020_2026.csv"
    df_komoditas.to_csv(out_komoditas, index=False, encoding="utf-8")
    print(f"[OK] Per Komoditas: {len(df_komoditas)} baris → {out_komoditas.name}")

    # Preview top commodities
    print("\n=== TOP 10 KOMODITAS (by total value) ===")
    top = (
        df_komoditas.groupby(["kode_hs", "deskripsi"])["nilai_usd"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    for _, row in top.iterrows():
        desc = row["deskripsi"][:60] + "..." if len(row["deskripsi"]) > 60 else row["deskripsi"]
        print(f"  {row['kode_hs']}  {row['nilai_usd']:>15,.2f} USD  {desc}")

    # Preview per country
    print("\n=== EKSPOR PER NEGARA (total) ===")
    country_totals = (
        df_agg[df_agg["negara_tujuan"] != "TOTAL"]
        .groupby("negara_tujuan")["nilai_usd"]
        .sum()
        .sort_values(ascending=False)
    )
    for country, total in country_totals.items():
        print(f"  {country:25s} {total:>18,.2f} USD")


if __name__ == "__main__":
    main()
