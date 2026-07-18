"""
Filter Tanahkita konflik agraria: Nasional → Sulawesi only
Sumber: data/raw/kpa_ylbhi_tanahkita/tanahkita_konflik.csv
Output:
  - data/processed/tanahkita_konflik_agraria_nasional.csv  (copy dari raw)
  - data/processed/tanahkita_konflik_agraria_sulawesi.csv  (filter Sulawesi)
"""

import pandas as pd
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(BASE, "data", "raw", "kpa_ylbhi_tanahkita", "tanahkita_konflik.csv")
OUT_DIR = os.path.join(BASE, "data", "processed")

# 6 provinsi Sulawesi
SULAWESI_PROVINSI = [
    "Sulawesi Utara",
    "Sulawesi Tengah",
    "Sulawesi Selatan",
    "Sulawesi Tenggara",
    "Sulawesi Barat",
    "Gorontalo",
]

# Kabupaten/Kota di Sulawesi untuk fallback matching
SULAWESI_KABUPATEN = [
    # Sulawesi Utara
    "Kota Manado", "Kota Bitung", "Kota Tomohon", "Kota Kotamobagu",
    "Kab. Minahasa", "Kab. Minahasa Utara", "Kab. Minahasa Selatan",
    "Kab. Minahasa Tenggara", "Kab. Bolaang Mongondow", "Kab. Bolaang Mongondow Utara",
    "Kab. Bolaang Mongondow Selatan", "Kab. Bolaang Mongondow Timur",
    "Kab. Kepulauan Sangihe", "Kab. Kepulauan Talaud", "Kab. Kepulauan Siau Tagulandang Biaro",
    "Kab. Minut", "Kab. Minhasel", "Kab. Minutara", "Kab. Minsel", "Kab. Mitr",
    # Gorontalo
    "Kota Gorontalo", "Kab. Gorontalo", "Kab. Gorontalo Utara",
    "Kab. Boalemo", "Kab. Bone Bolango", "Kab. Pohuwato",
    # Sulawesi Tengah
    "Kota Palu", "Kab. Donggala", "Kab. Poso", "Kab. Toli-Toli",
    "Kab. Buol", "Kab. Morowali", "Kab. Morowali Utara", "Kab. Banggai",
    "Kab. Banggai Kepulauan", "Kab. Banggai Laut", "Kab. Parigi Moutong",
    "Kab. Sigi", "Kab. Tojo Una-Una",
    # Sulawesi Barat
    "Kab. Mamuju", "Kab. Mamuju Tengah", "Kab. Mamasa", "Kab. Majene",
    "Kab. Polewali Mandar", "Kab. Pasangkayu",
    # Sulawesi Tenggara
    "Kota Kendari", "Kota Bau-Bau", "Kab. Kolaka", "Kab. Konawe",
    "Kab. Muna", "Kab. Buton", "Kab. Kolaka Utara", "Kab. Konawe Selatan",
    "Kab. Buton Utara", "Kab. Kolaka Timur", "Kab. Konawe Utara",
    "Kab. Buton Selatan", "Kab. Buton Tengah", "Kab. Muna Barat",
    "Kab. Konawe Kepulauan", "Kab. Bombana", "Kab. Wakatobi",
    "Kab. Kolaka", "Kab. Konawe",
    # Sulawesi Selatan
    "Kota Makassar", "Kota Parepare", "Kota Palopo",
    "Kab. Gowa", "Kab. Maros", "Kab. Takalar", "Kab. Jeneponto",
    "Kab. Bantaeng", "Kab. Bulukumba", "Kab. Sinjai", "Kab. Selayar",
    "Kab. Wajo", "Kab. Sidenreng Rappang", "Kab. Pinrang",
    "Kab. Enrekang", "Kab. Tana Toraja", "Kab. Toraja Utara",
    "Kab. Barru", "Kab. Pangkajene Kepulauan", "Kab. Luwu",
    "Kab. Luwu Utara", "Kab. Luwu Timur", "Kab. Bone",
    "Kab. Soppeng",
]


def load_data():
    """Load raw CSV"""
    df = pd.read_csv(RAW, encoding="utf-8")
    print(f"✓ Loaded {len(df)} records from raw")
    print(f"  Columns: {list(df.columns)}")
    return df


def is_sulawesi(row):
    """
    Cek apakah record ini berlokasi di Sulawesi.
    Mencari di kolom: judul, deskripsi, lokasi
    """
    text = " ".join([
        str(row.get("judul", "")),
        str(row.get("deskripsi", "")),
        str(row.get("lokasi", "")),
    ]).lower()

    # Cek nama provinsi
    for prov in SULAWESI_PROVINSI:
        if prov.lower() in text:
            return True

    # Cek nama kabupaten/kota
    for kab in SULAWESI_KABUPATEN:
        if kab.lower() in text:
            return True

    # Keyword khusus Sulawesi
    keywords_sulawesi = [
        "morowali", "kolaka", "luwu", "bone", "sangihe", "bitung",
        "gorontalo", "mamuju", "pinrang", "boalemo", "banggai",
        "buol", "donggala", "poso", "toli-toli", "selayar", "wakatobi",
        "bombana", "konawe", "muna", "buton", "enrekang", "tana toraja",
        "toraja utara", "barru", "pangkajene", "maros", "gowa",
        "takalar", "jeneponto", "bantaeng", "bulukumba", "sinjai",
        "wajo", "sidenreng", "rapang", "soppeng", "lutim", "lutra",
        "palopo", "parepare", "makassar", "kendari", "palu",
        "manado", "kotamobagu", "tomohon",
        "wawonii", "wawoni", "lore lindu", "tinanggea",
        "parigi moutong", "bangkep",
    ]
    for kw in keywords_sulawesi:
        if kw in text:
            return True

    return False


def main():
    df = load_data()

    # === 1. Simpan file nasional ===
    out_nasional = os.path.join(OUT_DIR, "tanahkita_konflik_agraria_nasional.csv")
    df.to_csv(out_nasional, index=False, encoding="utf-8")
    print(f"✓ Nasional: {len(df)} records → {out_nasional}")

    # === 2. Filter Sulawesi ===
    mask = df.apply(is_sulawesi, axis=1)
    df_sul = df[mask].copy()
    out_sulawesi = os.path.join(OUT_DIR, "tanahkita_konflik_agraria_sulawesi.csv")
    df_sul.to_csv(out_sulawesi, index=False, encoding="utf-8")
    print(f"✓ Sulawesi: {len(df_sul)} records → {out_sulawesi}")

    # === 3. Summary ===
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Total nasional:  {len(df)} records")
    print(f"Sulawesi:        {len(df_sul)} records ({len(df_sul)/len(df)*100:.1f}%)")
    print(f"\nSulawesi records:")
    for _, row in df_sul.iterrows():
        print(f"  #{row['nomor']} ({row['tahun']}) {row['judul'][:80]}")

    # === 4. Pindahkan file lama ke BAK ===
    old_file = os.path.join(OUT_DIR, "sulawesi_konflik_lahan.csv")
    bak_dir = os.path.join(OUT_DIR, "BAK")
    if os.path.exists(old_file):
        os.makedirs(bak_dir, exist_ok=True)
        bak_file = os.path.join(bak_dir, "sulawesi_konflik_lahan.csv")
        os.rename(old_file, bak_file)
        print(f"\n✓ Moved old file → {bak_file}")


if __name__ == "__main__":
    main()
