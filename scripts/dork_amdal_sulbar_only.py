import os
import sys
import time
import csv
from pathlib import Path

import pandas as pd

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PROCESSED = BASE_DIR / "data" / "processed"
DATA_RAW = BASE_DIR / "data" / "raw"

sys.path.append(str(BASE_DIR))
from tools.google_dork.google_dorker import google_dork  # type: ignore


def run_sulbar_dorking(limit: int = 50):
    esdm_path = DATA_PROCESSED / "sulawesi_esdm_nikel.csv"
    # Simpan hasil khusus Sulbar ke file terpisah supaya tidak mengganggu yang lama
    out_dir = DATA_RAW / "amdal_leaks"
    out_dir.mkdir(parents=True, exist_ok=True)
    output_csv = out_dir / "amdal_dork_results_sulbar.csv"

    print("[*] Membaca data perusahaan Sulawesi Barat dari ESDM...")
    try:
        df = pd.read_csv(esdm_path)
    except Exception as e:
        print(f"[!] Gagal membaca {esdm_path}: {e}")
        return

    if "provinsi" not in df.columns or "nama_perusahaan" not in df.columns:
        print("[!] Kolom 'provinsi' / 'nama_perusahaan' tidak ditemukan di sulawesi_esdm_nikel.csv")
        return

    # Filter hanya perusahaan di Sulawesi Barat
    df_sulbar = df[df["provinsi"] == "Sulawesi Barat"].copy()
    if df_sulbar.empty:
        print("[!] Tidak ada entri provinsi 'Sulawesi Barat' di sulawesi_esdm_nikel.csv")
        return

    # Pastikan luas numerik agar bisa di-sort
    if "total_luas_ha" in df_sulbar.columns:
        df_sulbar["total_luas_ha"] = pd.to_numeric(df_sulbar["total_luas_ha"], errors="coerce").fillna(0)
        df_sulbar = df_sulbar.sort_values(by="total_luas_ha", ascending=False)

    if limit > 0:
        df_sulbar = df_sulbar.head(limit)

    print(f"[*] Ditemukan {len(df_sulbar)} perusahaan di Sulawesi Barat (limit={limit}).")

    # Siapkan file output (append-safe)
    file_exists = output_csv.exists()
    with open(output_csv, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow([
                "nama_perusahaan",
                "lokasi",
                "luas_ha",
                "dork_query",
                "pdf_title",
                "pdf_link",
                "pdf_snippet",
            ])

        for idx, row in df_sulbar.iterrows():
            nama_pt = str(row.get("nama_perusahaan", "")).strip()
            lokasi = str(row.get("lokasi_izin", "")).strip()
            luas = row.get("total_luas_ha", 0)

            if not nama_pt:
                continue

            query = f'"{nama_pt}" "AMDAL" OR "RKL-RPL" "limbah" OR "tailing" filetype:pdf'
            print(f"\n[*] Dorking Sulbar: {nama_pt} ({luas} Ha)")

            try:
                results = google_dork(query, num_results=3)
                if not results:
                    writer.writerow([nama_pt, lokasi, luas, query, "TIDAK DITEMUKAN", "", ""])
                else:
                    for res in results:
                        writer.writerow([
                            nama_pt,
                            lokasi,
                            luas,
                            query,
                            res.get("title", ""),
                            res.get("link", ""),
                            res.get("snippet", ""),
                        ])
                time.sleep(1)  # jaga rate limit API

            except Exception as e:
                print(f"[!] Error saat dorking {nama_pt}: {e}")
                writer.writerow([nama_pt, lokasi, luas, query, f"ERROR: {e}", "", ""])
                break

    print(f"\n[*] Selesai dorking Sulbar. Hasil disimpan di: {output_csv}")


if __name__ == "__main__":
    # Default: dork semua perusahaan Sulbar (tanpa limit ketat, tapi bisa diubah)
    run_sulbar_dorking(limit=0)
