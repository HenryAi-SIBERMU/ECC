import os
import sys
import re
from typing import Tuple

import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")

ESDM_PATH = os.path.join(PROCESSED_DIR, "sulawesi_esdm_nikel.csv")
AMDAL_PATH = os.path.join(RAW_DIR, "amdal_leaks", "amdal_dork_results.csv")
OUTPUT_PATH = os.path.join(PROCESSED_DIR, "sulawesi_kawasan_nikel_luas.csv")


def normalize_name(name: str) -> str:
    """Normalisasi nama perusahaan untuk keperluan join kasar.

    - Uppercase
    - Hilangkan 'PT', 'P.T.', 'TBK', 'PERSEROAN TERBATAS', tanda baca umum
    - Hilangkan spasi ganda
    """
    if not isinstance(name, str):
        name = str(name) if name is not None else ""
    n = name.upper()
    # Hilangkan akronim hukum umum
    for token in ["PT ", "P.T. ", "P.T ", "PERSEROAN TERBATAS ", " TBK", " TBK."]:
        n = n.replace(token, " ")
    # Hilangkan tanda baca
    n = re.sub(r"[.,'\"]", " ", n)
    # Hilangkan spasi berlebih
    n = re.sub(r"\s+", " ", n).strip()
    return n


def load_esdm() -> pd.DataFrame:
    if not os.path.exists(ESDM_PATH):
        raise FileNotFoundError(f"ESDM processed file not found: {ESDM_PATH}")
    df = pd.read_csv(ESDM_PATH)
    if "nama_perusahaan" not in df.columns:
        raise ValueError("Expected column 'nama_perusahaan' in sulawesi_esdm_nikel.csv")
    if "total_luas_ha" not in df.columns:
        raise ValueError("Expected column 'total_luas_ha' in sulawesi_esdm_nikel.csv")

    df["nama_norm"] = df["nama_perusahaan"].apply(normalize_name)
    return df


def load_amdal() -> pd.DataFrame:
    if not os.path.exists(AMDAL_PATH):
        raise FileNotFoundError(f"AMDAL dork results not found: {AMDAL_PATH}")
    df = pd.read_csv(AMDAL_PATH)
    if "nama_perusahaan" not in df.columns or "luas_ha" not in df.columns:
        raise ValueError("Expected columns 'nama_perusahaan' and 'luas_ha' in amdal_dork_results.csv")

    df["nama_norm"] = df["nama_perusahaan"].apply(normalize_name)
    # Agregasi luas_ha per perusahaan
    agg = (
        df.groupby("nama_norm", as_index=False)["luas_ha"]
        .sum()
        .rename(columns={"luas_ha": "luas_amdal_ha"})
    )
    return agg


def build_kawasan_luas() -> Tuple[pd.DataFrame, pd.DataFrame]:
    esdm = load_esdm()
    amdal_agg = load_amdal()

    print(f"[INFO] Loaded ESDM nikel: {esdm.shape}")
    print(f"[INFO] Loaded AMDAL aggregated: {amdal_agg.shape}")

    # Kita hanya butuh subset kolom inti dari ESDM
    keep_cols = [
        "nama_perusahaan",
        "provinsi",
        "lokasi_izin" if "lokasi_izin" in esdm.columns else "lokasi_izin".replace("lokasi_izin", "lokasi_izin"),
        "total_luas_ha",
        "nama_norm",
    ]
    keep_cols = [c for c in keep_cols if c in esdm.columns]

    esdm_sub = esdm[keep_cols].copy()

    # Join kasar ke AMDAL
    merged = esdm_sub.merge(amdal_agg, on="nama_norm", how="left")

    # Tambah metadata sumber
    merged["sumber_luas_iup"] = "Minerbaone/CGS merged (sulawesi_esdm_nikel.csv)"
    merged["sumber_luas_amdal"] = "AMDAL dorking (amdal_dork_results.csv)"

    # Susun kembali urutan kolom
    ordered_cols = [
        "nama_perusahaan",
        "provinsi" if "provinsi" in merged.columns else None,
        "lokasi_izin" if "lokasi_izin" in merged.columns else None,
        "total_luas_ha",
        "luas_amdal_ha",
        "nama_norm",
        "sumber_luas_iup",
        "sumber_luas_amdal",
    ]
    ordered_cols = [c for c in ordered_cols if c is not None and c in merged.columns]
    merged = merged[ordered_cols].copy()

    # Juga buat agregat sederhana per provinsi untuk gambaran makro
    if "provinsi" in merged.columns:
        by_prov = (
            merged.groupby("provinsi", as_index=False)
            .agg({"total_luas_ha": "sum", "luas_amdal_ha": "sum"})
            .rename(
                columns={
                    "total_luas_ha": "total_luas_iup_ha",
                    "luas_amdal_ha": "total_luas_amdal_ha",
                }
            )
        )
    else:
        by_prov = pd.DataFrame()

    return merged, by_prov


def main() -> None:
    try:
        merged, by_prov = build_kawasan_luas()
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(PROCESSED_DIR, exist_ok=True)
    merged.to_csv(OUTPUT_PATH, index=False)
    print(f"[INFO] Saved kawasan nikel luas per perusahaan to: {OUTPUT_PATH}")
    print("[INFO] Preview perusahaan:")
    print(merged.head())

    if not by_prov.empty:
        prov_out = os.path.join(PROCESSED_DIR, "sulawesi_kawasan_nikel_luas_per_provinsi.csv")
        by_prov.to_csv(prov_out, index=False)
        print(f"[INFO] Saved kawasan nikel luas per provinsi to: {prov_out}")
        print("[INFO] Preview provinsi:")
        print(by_prov.head())


if __name__ == "__main__":
    main()
