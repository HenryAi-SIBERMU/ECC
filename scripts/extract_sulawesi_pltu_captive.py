import os
import glob
import sys
from typing import Dict, Optional

import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
GEM_DIR = os.path.join(BASE_DIR, "data", "raw", "izin_ESDM", "gem-data")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "processed", "sulawesi_pltu_captive.csv")


def find_gcpt_file() -> str:
    """Find Global Coal Plant Tracker Excel file under GEM_DIR.

    We allow multiple possible filenames but will pick the first match.
    """
    if not os.path.isdir(GEM_DIR):
        raise FileNotFoundError(f"GEM data directory not found: {GEM_DIR}")

    patterns = [
        "Global-Coal-Plant-Tracker-*.xlsx",
        "Global-Coal-Plant-Tracker*.xlsx",
    ]
    for pattern in patterns:
        paths = glob.glob(os.path.join(GEM_DIR, pattern))
        if paths:
            return paths[0]

    raise FileNotFoundError("Global Coal Plant Tracker Excel file not found in gem-data directory.")


def find_column(df: pd.DataFrame, candidates) -> Optional[str]:
    """Return first column name whose lowercased name contains any candidate substring.

    This makes the script robust to minor schema/name changes.
    """
    cols_lower = {c.lower(): c for c in df.columns}
    for cand in candidates:
        cand_lower = cand.lower()
        for c_lower, orig in cols_lower.items():
            if cand_lower in c_lower:
                return orig
    return None


def identify_columns(df: pd.DataFrame) -> Dict[str, Optional[str]]:
    """Best-effort mapping of logical fields to actual column names in GCPT file."""
    mapping = {
        "country": find_column(df, ["country"]),
        "plant_name": find_column(df, ["plant_name", "plant", "name"]),
        "subplant_name": find_column(df, ["unit_name", "subplant", "block_name"]),
        "province": find_column(df, ["province", "region", "state", "subnational"]),
        "owner": find_column(df, ["owner", "operator", "parent", "company"]),
        "capacity_mw": find_column(df, ["capacity", "mw"]),
        "status": find_column(df, ["status"]),
        "year_start": find_column(df, ["start_year", "year", "comm", "operation"]),
        "fuel": find_column(df, ["fuel", "coal"]),
        "plant_type": find_column(df, ["captive", "grid", "plant_type", "ownership"]),
        "latitude": find_column(df, ["lat"]),
        "longitude": find_column(df, ["lon", "lng", "long"]),
        "plant_id": find_column(df, ["id", "identifier", "plant_id"]),
    }
    return mapping


SULAWESI_PROVINCE_KEYWORDS = [
    "sulawesi",
    "gorontalo",  # provinsi di pulau Sulawesi
]


CAPTIVE_KEYWORDS = [
    # Industrial parks & well-known nickel clusters
    "morowali", "imip", "indonesia morowali industrial park",
    "weda bay", "iwip", "indonesia weda bay industrial park",
    "bahodopi", "konawe", "konsel", "kolaka", "pomalaa",
    "virtue dragon", "vdni", "ceria", "obsi", "obsidian",
]


def filter_indonesia_sulawesi(df: pd.DataFrame, cols: Dict[str, Optional[str]]) -> pd.DataFrame:
    """Filter to rows located in Indonesia and on the island of Sulawesi.

    We use the country column if available, then a text filter on province/region.
    """
    country_col = cols["country"]
    if country_col and country_col in df.columns:
        df = df[df[country_col].astype(str).str.contains("indonesia", case=False, na=False)]

    province_col = cols["province"]
    if province_col and province_col in df.columns:
        mask = pd.Series(False, index=df.index)
        prov_series = df[province_col].astype(str).str.lower()
        for kw in SULAWESI_PROVINCE_KEYWORDS:
            mask = mask | prov_series.str.contains(kw, na=False)
        df = df[mask]

    return df


def derive_captive_flag(row: pd.Series, cols: Dict[str, Optional[str]]) -> bool:
    """Heuristic to label whether a plant is captive.

    1) If there is a dedicated plant_type/grid column with values indicating 'captive', use that.
    2) Otherwise, fall back to string matching on plant_name / owner.
    """
    # 1. Dedicated column, if present
    plant_type_col = cols.get("plant_type")
    if plant_type_col and plant_type_col in row.index:
        val = str(row[plant_type_col]).lower()
        if any(k in val for k in ["captive", "off-grid", "industrial"]):
            return True

    # 2. Heuristic based on plant_name / owner / province
    text_parts = []
    for key in ["plant_name", "subplant_name", "owner", "province"]:
        col = cols.get(key)
        if col and col in row.index:
            text_parts.append(str(row[col]))
    text = " ".join(text_parts).lower()
    if any(kw in text for kw in CAPTIVE_KEYWORDS):
        return True

    return False


def choose_gcpt_sheet(gcpt_path: str) -> str:
    """Pilih sheet GCPT yang berisi tabel plant-level (bukan cover).

    Strategi: baca beberapa baris pertama dari tiap sheet, lalu pilih yang
    punya paling banyak kolom kunci (country/plant/capacity/status/fuel).
    """
    xls = pd.ExcelFile(gcpt_path)
    best_sheet = xls.sheet_names[0]
    best_score = -1

    for sheet in xls.sheet_names:
        try:
            head = pd.read_excel(xls, sheet_name=sheet, nrows=5)
        except Exception:
            continue
        cols = identify_columns(head)
        score = sum(
            1
            for key in ["country", "plant_name", "capacity_mw", "status", "fuel"]
            if cols.get(key)
        )
        if score > best_score and head.shape[1] >= 5:
            best_score = score
            best_sheet = sheet

    print(f"[INFO] Selected GCPT sheet: {best_sheet} (score={best_score})")
    return best_sheet


def build_sulawesi_pltu_captive() -> None:
    gcpt_path = find_gcpt_file()
    print(f"[INFO] Using GCPT file: {gcpt_path}")

    # Pilih sheet data yang benar (bukan cover)
    sheet_name = choose_gcpt_sheet(gcpt_path)
    df = pd.read_excel(gcpt_path, sheet_name=sheet_name)
    print(f"[INFO] Loaded GCPT sheet '{sheet_name}' with shape: {df.shape}")

    cols = identify_columns(df)
    print("[INFO] Column mapping:")
    for k, v in cols.items():
        print(f"  {k}: {v}")

    # Filter Indonesia + Sulawesi
    df = filter_indonesia_sulawesi(df, cols)
    print(f"[INFO] After Indonesia+Sulawesi filter: {df.shape}")

    # Heuristic filter: keep only coal plants (jika ada kolom fuel)
    # Catatan: GCPT sudah spesifik PLTU batubara; di beberapa versi, kolom
    # "Conversion to (fuel)" bukan tipe bahan bakar, tapi faktor konversi.
    # Jika filter ke "coal" mengosongkan data, kita rollback ke sebelum filter.
    fuel_col = cols.get("fuel")
    if fuel_col and fuel_col in df.columns:
        before = df.copy()
        before_shape = df.shape
        df = df[df[fuel_col].astype(str).str.contains("coal", case=False, na=False)]
        if df.empty:
            print("[WARN] fuel=coal filter produced 0 rows; reverting to unfiltered frame (assume GCPT is coal-only).")
            df = before
        else:
            print(f"[INFO] After fuel=coal filter: {before_shape} -> {df.shape}")
    else:
        print("[WARN] Fuel column not detected, skipping fuel=coal filter.")

    if df.empty:
        print("[WARN] No rows left after filters. Check column mapping / sheet selection.")

    # Derive captive flag (heuristik). Untuk saat ini **jangan** dijadikan filter keras,
    # supaya semua PLTU di Sulawesi tetap masuk ke output dan flag bisa direview manual.
    if not df.empty:
        df["captive_flag"] = df.apply(lambda r: derive_captive_flag(r, cols), axis=1)
    else:
        df["captive_flag"] = []  # keep column for schema

    print(f"[INFO] Rows after filtering to Sulawesi coal plants (before captive flag filter): {df.shape}")

    # Pilih subset kolom yang bersih untuk output
    out_cols = []
    for key in ["plant_id", "plant_name", "subplant_name", "province",
                "owner", "status", "year_start", "capacity_mw",
                "fuel", "latitude", "longitude"]:
        col = cols.get(key)
        if col and col in df.columns and col not in out_cols:
            out_cols.append(col)

    # Tambahkan flag captive di akhir
    if "captive_flag" in df.columns:
        out_cols.append("captive_flag")

    if out_cols:
        df_out = df[out_cols].copy()
    else:
        print("[WARN] No mapped columns found, saving raw filtered frame.")
        df_out = df.copy()

    df_out.insert(0, "source", "GEM Global Coal Plant Tracker (January 2026)")

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df_out.to_csv(OUTPUT_PATH, index=False)
    print(f"[INFO] Saved processed PLTU data to: {OUTPUT_PATH}")
    print("[INFO] Preview:")
    print(df_out.head())


if __name__ == "__main__":
    try:
        build_sulawesi_pltu_captive()
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
