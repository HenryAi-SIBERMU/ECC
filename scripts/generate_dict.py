import os

processed_dir = 'data/processed'
files = sorted([f for f in os.listdir(processed_dir) if f.endswith('.csv')])

mapping = {
    'kpa_catahu_2025_izin_ilegal_sulawesi.csv': ['`data/raw/konflik_kpa_ylbhi_tanahkita/`', 'Scraping PDF', '-', 'Data profil izin ilegal dari KPA.'],
    'kpa_masalah_izin_perusahaan.csv': ['Laporan CATAHU KPA', 'Scraping PDF', '-', 'Ekstraksi profil konflik by perusahaan.'],
    'nasional_ekspor_2022_2026.csv': ['`data/raw/eksporimpor/`', 'API BPS', '-', 'Data agregat ekspor nasional.'],
    'nasional_gfn_historis_1_dekade.csv': ['`data/raw/klhk_gfn/`', 'Data Sekunder GFN', '-', 'Jejak ekologi (Global Footprint Network) nasional.'],
    'nasional_ika_2015_2024.csv': ['`data/raw/klhk_ika/`', 'Scraping PDF KLHK', '-', 'Data pembanding baseline IKA Nasional.'],
    'nasional_investasi_pmdn_2016_2024.csv': ['`data/raw/bps_pmdn/`', 'API BPS / BKPM', 'Request JSON', 'Realisasi PMDN agregat Nasional.'],
    'nasional_kesehatan_2014_2024.csv': ['`data/raw/profil_kesehatan_kemenkes/`', 'Ekstraksi PDF', 'Agregasi', 'Data agregat penderita ISPA/Diare/Malaria nasional.'],
    'nasional_kesehatan_detail_2014_2024.csv': ['`data/raw/profil_kesehatan_kemenkes/`', 'Ekstraksi PDF', '-', 'Versi detail nasional. (Potensi duplikat).'],
    'nasional_konflik_agraria_tanahkita.csv': ['`data/raw/konflik_kpa_ylbhi_tanahkita/`', 'API Tanahkita', '`extract_konflik_hukum.py`', 'Master dataset konflik nasional.'],
    'nasional_konversi_gfn.csv': ['`data/raw/klhk_gfn/`', 'Data Sekunder GFN', '-', 'Konversi biokapasitas.'],
    'nasional_limbah_b3_2020_2024.csv': ['`data/raw/D3TLH/`', 'Scraping Laporan', '-', 'Volume limbah B3 nasional.'],
    'sulawesi_bencana_bnpb_2014_2024.csv': ['Data DIBI BNPB', 'API / CSV Eksport', '-', 'Frekuensi Bencana Ekologis.'],
    'sulawesi_ekspor_2022_2026.csv': ['`data/raw/eksporimpor/`', 'API BPS', '-', 'Agregat total ekspor Sulawesi.'],
    'sulawesi_ekspor_detail_2020_2026.csv': ['`data/raw/eksporimpor/`', 'API BPS', '-', 'Rincian ekspor by HS Code.'],
    'sulawesi_ekspor_komoditas_2020_2026.csv': ['`data/raw/eksporimpor/`', 'API BPS', '-', 'Rincian ekspor by komoditas spesifik.'],
    'sulawesi_ekspor_negara_2020_2026.csv': ['`data/raw/eksporimpor/`', 'API BPS', '-', 'Rincian ekspor tujuan negara.'],
    'sulawesi_esdm_nikel.csv': ['`data/raw/izin_ESDM/`', 'Data Registry ESDM', '`tools/esdm/`', 'Master data Fasilitas Smelter Nikel.'],
    'sulawesi_faskes_agregat.csv': ['`data/raw/bps_kemenkesispadiaremalaria/`', 'API BPS', '-', 'Data fasilitas kesehatan.'],
    'sulawesi_gfw_hutan_primer_loss_2014_2023.csv': ['Master GFW', 'Reshape dari Master', 'Agregasi Pandas', 'Hutan primer spesifik.'],
    'sulawesi_gfw_kawasan_lindung_loss_2014_2023.csv': ['Master GFW', 'Reshape dari Master', 'Agregasi Pandas', 'Batas zona lindung.'],
    'sulawesi_gfw_loss_by_driver_2014_2023.csv': ['Master GFW', 'Reshape dari Master', 'Agregasi Pandas', 'Driver spesifik (Mining/Commodity).'],
    'sulawesi_gfw_master_1_dekade_2014_2023.csv': ['`data/raw/klhk_gfw/`', 'Ekspor Platform', '-', 'Master tree cover loss.'],
    'sulawesi_ika_2016_2024.csv': ['`data/raw/klhk_ika/`', 'Scraping PDF KLHK', 'Table OCR', 'Indeks Kualitas Air.'],
    'sulawesi_iku_2015_2024.csv': ['`data/raw/klhk_iku/`', 'Scraping PDF KLHK', 'Table OCR', 'Indeks Kualitas Udara.'],
    'sulawesi_investasi_nikel.csv': ['`data/raw/izin_ESDM/`', 'Reshape', '-', 'Investasi spesifik Nikel.'],
    'sulawesi_investasi_pmdn_2016_2024.csv': ['nasional_investasi_...', 'Reshape dari Master', 'Agregasi Pandas', 'Realisasi PMDN Sulawesi.'],
    'sulawesi_izin_baru_per_tahun.csv': ['Minerbaone', 'Data Sekunder', '-', 'Tren IUP per tahun.'],
    'sulawesi_izin_raw_details.csv': ['Minerbaone', 'Data Sekunder', '-', 'Detail raw data IUP.'],
    'sulawesi_kawasan_nikel_luas.csv': ['`sulawesi_esdm_nikel.csv`', 'Reshape', 'Hitung Luasan', 'Agregat luasan lahan.'],
    'sulawesi_kawasan_nikel_luas_per_provinsi.csv': ['`sulawesi_esdm_nikel.csv`', 'Reshape', 'Agregasi', 'Luas per provinsi.'],
    'sulawesi_kesehatan_detail_2014_2024.csv': ['nasional_kesehatan_...', 'Reshape', 'Pemotongan array', 'Filter 6 Provinsi.'],
    'sulawesi_konflik_agraria_tanahkita.csv': ['`data/raw/konflik_kpa_ylbhi_tanahkita/`', 'API Tanahkita', '`extract_...`', 'Data konflik KPA & YLBHI.'],
    'sulawesi_konflik_hukum.csv': ['`data/raw/konflik_kpa_ylbhi_tanahkita/`', 'Web Scraping', '-', 'Data konflik dari ranah hukum.'],
    'sulawesi_konflik_tambang_fpic.csv': ['NGO Jatam/Walhi', 'Web Scraping', '-', 'Pelanggaran FPIC.'],
    'sulawesi_limbah_b3.csv': ['`data/raw/D3TLH/`', 'Data Laporan', '-', 'Volume B3 proxy.'],
    'sulawesi_limbah_b3_ngo_proxy.csv': ['NGO Laporan', 'Scraping', '-', 'Estimasi limbah B3 oleh NGO.'],
    'sulawesi_pad_2016_2024.csv': ['`data/raw/bps_pad/`', 'API BPS', '-', 'PAD Total.'],
    'sulawesi_pad_breakdown_2016_2024.csv': ['`data/raw/bps_pad/`', 'API BPS', '-', 'Rincian PAD.'],
    'sulawesi_pltu_captive.csv': ['Global Energy Monitor', 'Data Sekunder NGO', 'Manual Filter', 'Data PLTU Captive.'],
    'sulut_ika_1_dekade_2016_2024.csv': ['`sulawesi_ika_2016_2024.csv`', 'Reshape', 'Potensi duplikat', 'Kandidat dihapus.']
}

markdown_output = f"""# 📖 Kamus Data & Silsilah (Data Provenance)
Dokumen ini memetakan **seluruh {len(files)} dataset di folder `data/processed`** ke sumber asalnya (baik dari BPS, ekstraksi PDF KLHK, scraping, maupun NGO).

## Master Summary (Keseluruhan)

| No | Nama File Processed | Sumber Asli (Raw/Master) | Kategori/Medium | Script Transformasi | Deskripsi / Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
"""

for i, f in enumerate(files, 1):
    if f in mapping:
        m = mapping[f]
        markdown_output += f"| {i} | `{f}` | {m[0]} | {m[1]} | {m[2]} | {m[3]} |\n"
    else:
        markdown_output += f"| {i} | `{f}` | Unknown | Unknown | Unknown | Belum terpetakan |\n"

with open('data/DATA_DICTIONARY.md', 'w', encoding='utf-8') as file:
    file.write(markdown_output)

print(f"Successfully mapped all {len(files)} files to DATA_DICTIONARY.md.")
