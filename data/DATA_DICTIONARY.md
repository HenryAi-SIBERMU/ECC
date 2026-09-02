# 📖 Kamus Data & Silsilah (Data Provenance)
Dokumen ini memetakan **seluruh dataset di folder `data/processed`** ke sumber asalnya (baik dari BPS, ekstraksi PDF KLHK, scraping, maupun NGO).

## Master Summary (Keseluruhan)

| No | Nama File Processed | Sumber Asli (Raw/Master) | Kategori/Medium | Script Transformasi | Digunakan pada Bab/Sub-bab | Deskripsi / Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `sulawesi_ekspor_komoditas_2020_2026.csv` | `data/raw/eksporimpor/` | API BPS | - | Bab 12 | Rincian ekspor by komoditas spesifik. |
| 2 | `sulawesi_ekspor_2022_2026.csv` | `data/raw/eksporimpor/` | API BPS | - | Bab 12 | Agregat total ekspor Sulawesi. |
| 3 | `sulawesi_ekspor_detail_2020_2026.csv` | `data/raw/eksporimpor/` | API BPS | - | Bab 12 | Rincian ekspor by HS Code. |
| 4 | `sulawesi_ekspor_negara_2020_2026.csv` | `data/raw/eksporimpor/` | API BPS | - | Bab 12 | Rincian ekspor tujuan negara. |
| 5 | `sulawesi_pdrb_sektoral_2016_2024.csv` | `data/raw/bps_pdrb/` | API BPS (Subject 52, Var 141/153) | - | Bab 1.1.1, 1.1.3, 9.3 | Data PDRB Sektoral Sulawesi, diklasifikasi menjadi Ekstraktif dan Akar Rumput. |
| 6 | `sulawesi_pdrb_sektoral_kabupaten_2016_2024.csv` | `data/raw/bps_pdrb/` | API BPS (Subject 52, Var 141/153) | - | Bab 1.1.2 | Data PDRB Sektoral tingkat Kabupaten Sulawesi. |
| 7 | `sulawesi_esdm_nikel.csv` | `minerbaone_permits.csv` (MODI ESDM) & `CGS_Dataset.xlsx` | Database Smelter CGS & ESDM MODI | Gabungan Data / Manual | Bab 1.2 & 2.1 | Master data Fasilitas Smelter Nikel di Sulawesi. |
| 8 | `sulawesi_gfw_master_1_dekade_2014_2023_v3.csv` | `data/raw/klhk_gfw/` | Ekspor Platform | - | Bab 1.2, 1.3, 1.4, 2.3, 5.1, 5.4, 7.1, 8.3 | Master deforestasi GFW. Memuat 'Total Deforestasi Alam' & 'Deforestasi Tambang/Sawit' (Dipakai sbg Variabel Y - Dampak Ekologis pada Crosstab). |
| 9 | `sulawesi_pltu_captive.csv` | `data/raw/izin_ESDM/gem-data/Global-Coal-Plant-Tracker-January-2026.xlsx` | NGO (GEM) - Filter: Captive & Sulawesi | `tools/esdm/extract_pltu_captive.py` | Bab 1.2, 2.2, 7.3, 8.1 | Data PLTU khusus penyokong industri (Captive). |
| 10 | `sulawesi_izin_baru_per_tahun.csv` | `minerbaone_permits.csv` (MODI ESDM) | Data Registry ESDM MODI | `tools/esdm/extract_izin_timeline.py` | Bab 1.3, 2.3, 5.1, 5.4, 7.1 | Agregasi IUP (Jumlah Izin & Luas Konsesi). Dipakai sbg Variabel X (Tekanan Ekspansi) pada uji Crosstab melawan data GFW. |
| 11 | `sulawesi_investasi_pmdn_2016_2024.csv` | `nasional_investasi_pmdn_2016_2024.csv` | Reshape dari Master | Agregasi Pandas | Bab 1.4, 8.3 | Realisasi PMDN Sulawesi. Dipakai sbg Variabel X pada uji statistik crosstab. |
| 12 | `sulawesi_pad_2016_2024.csv` | `data/raw/bps_pad/` | API BPS | - | Bab 1.4, 8.3 | Data total agregat PAD level provinsi Sulawesi tanpa breakdown komponen. |
| 13 | `sulawesi_pad_breakdown_2016_2024.csv` | `data/raw/bps_pad/` | API BPS | - | Bab 1.4 | Data Pendapatan Asli Daerah (PAD) level provinsi Sulawesi (Breakdown Pajak dll). |
| 14 | `sulawesi_investasi_nikel.csv` | `data/raw/izin_ESDM/` | Reshape | - | Bab 1.4, 13 | Investasi spesifik Nikel. |
| 15 | `sulawesi_logistik_simpul_nikel.csv` | `data/raw/osint_logistik_pelabuhan/` | Dorking & Ekstraksi Teks | - | Bab 1.5 & 1.6 | Data detail fasilitas pelabuhan (kapasitas/DWT), status PSN smelter, serta titik koordinat rute ekspor nikel. |
| 16 | gee_nasa_no2_sulawesi_monthly_raw.csv | Google Earth Engine (Sentinel-5P) | API Satelit GEE | - | Bab 2 & 2.2 | Data bulanan konsentrasi Nitrogen Dioksida (NO2) dari satelit Copernicus TROPOMI. |
| 17 | `sulawesi_ika_2016_2024.csv` | `data/raw/klhk_ika/` | Scraping PDF KLHK | Table OCR | Bab 2.1 & 3.6 | Indeks Kualitas Air. |
| 18 | `sulawesi_limbah_b3_ngo_proxy.csv` | `data/raw/klhk_ngo_reports/` | Ekstraksi PDF (`ARKL_Morowali.pdf`, `Riset-Final-WALHI-SULTRA.pdf`) | - | Bab 2.1 | Estimasi limbah B3 oleh NGO (AEER, WALHI, dll). |
| 19 | `sulawesi_sungai_tercemar.csv` | `data/raw/klhk_ngo_reports/` | Ekstraksi PDF (`Arinto-Sangadji-HPAL-dalam-Industri-Nikel.pdf`, `Riset-Final-WALHI-SULTRA.pdf`) | - | Bab 2.1 | Data spasial sungai & pesisir yang tercemar tailing / sedimen nikel di Sulawesi. |
| 20 | `sulawesi_gfw_loss_by_driver_2014_2023_v3.csv` | `data/raw/klhk_gfw/` | GFW API Export (CSV/JSON) | Agregasi Pandas | Bab 2.2 & 2.4 | Driver penyebab deforestasi spesifik (Tambang/Sawit vs lainnya). Memuat konversi hilangnya biomassa ke estimasi emisi Jejak Karbon (CO2 ekuivalen) dari model satelit GFW. |
| 21 | `sulawesi_iku_2015_2024.csv` | `data/raw/klhk_iku/` | Scraping PDF KLHK | Table OCR | Bab 2.2 | Indeks Kualitas Udara. |
| 22 | `sulawesi_kawasan_nikel_luas.csv` | `sulawesi_esdm_nikel.csv` | Reshape | Hitung Luasan | Bab 2.3, 8.1 | Agregat luasan lahan. |
| 23 | gbif_sulawesi_occurrences.csv | data/raw/ | GBIF API | - | Bab 2.5 | Data titik koordinat perjumpaan spesies endemik Sulawesi. |
| 24 | sulawesi_biodiversitas_iucn_fase5_exploded.csv | IUCN API | API Scraping | ools/scraper/iucn_scraper.py | Bab 2.5 | Data status ancaman (Red List) dan keterangan Mining Threat. |
| 25 | sulawesi_faskes_agregat_v3.csv | `data/raw/bps_kemenkesispadiaremalaria/` | API BPS | - | Bab 3.1 | Data fasilitas kesehatan. |
| 26 | `sulawesi_kesehatan_detail_2014_2024.csv` | nasional_kesehatan_... | Reshape | Pemotongan array | Bab 3.2, 3.3, 3.5, 3.6, 8.2, 8.3 | Data panel historis beban penyakit lingkungan (ISPA, Diare, Malaria) per provinsi. |
| 27 | zoonosis_kab_kota_2015_2024.csv | data/raw/profil kesehatan_nasional_kemenkes/ | Data Agregat Kemenkes | Filter | Bab 3.4, 9 | Data anomali zoonosis distrik (Malaria, DBD). |
| 28 | indonesia-prov.geojson | data/raw/ | GeoJSON Polygon | - | Bab 3.5 | Peta wilayah batas administrasi provinsi se-Indonesia. |
| 29 | ika_ngo_cr6_gabungan.csv | Laporan NGO (AEER/WALHI) | Uji Lab Lapangan | - | Bab 3.6 | Data bukti klinis paparan Cr6+ di muara sungai/laut kawasan tambang. |
| 30 | `sulawesi_limbah_b3.csv` | `data/raw/D3TLH/` | Data Laporan | - | Bab 3.7 | Volume B3 proxy. |
| 31 | `sulawesi_konflik_agraria_tanahkita.csv` | `data/raw/konflik_kpa_ylbhi_tanahkita/` | API Tanahkita | `extract_...` | Bab 4.1 - 4.5, 8.1 | Data konflik KPA & YLBHI. |
| 32 | `sulawesi_gfw_kawasan_lindung_loss_2014_2023_v3.csv` | Master GFW | Reshape dari Master | Agregasi Pandas | Bab 5.2 | Batas zona lindung. |
| 33 | `sulawesi_gfw_hutan_primer_loss_2014_2023_v3.csv` | Master GFW | Reshape dari Master | Agregasi Pandas | Bab 5.2 | Hutan primer spesifik. |
| 34 | `kpa_masalah_izin_perusahaan.csv` | Laporan CATAHU KPA | Scraping PDF | - | Bab 5.3 | Ekstraksi profil konflik by perusahaan. |
| 35 | `sulawesi_konflik_tambang_fpic.csv` | NGO Jatam/Walhi | Web Scraping | - | Bab 5.3 | Pelanggaran FPIC. |
| 36 | `kpa_catahu_2025_izin_ilegal_sulawesi.csv` | `data/raw/konflik_kpa_ylbhi_tanahkita/` | Scraping PDF | - | Bab 5.3, 7.1, 12, 13 | Data profil izin ilegal dari KPA. |
| 37 | `sulawesi_bencana_bnpb_2014_2024.csv` | Data DIBI BNPB | API / CSV Eksport | - | Bab 6, 12, 13 | Frekuensi Bencana Ekologis. |
| 38 | `sulawesi_kawasan_nikel_luas_per_provinsi.csv` | `sulawesi_esdm_nikel.csv` | Reshape | Agregasi | Bab 6, 12 | Luas per provinsi. |
| 39 | `sulawesi_izin_raw_details.csv` | Minerbaone | Data Sekunder | - | Bab 7.1 | Detail raw data IUP. |
| 40 | `sulawesi_konflik_hukum.csv` | `data/raw/konflik_kpa_ylbhi_tanahkita/` | Web Scraping | - | Bab 7.2 | Data konflik dari ranah hukum. |
| 41 | `sulawesi_demografi_master_fase4.csv` | API BPS SIMDASI (via `fetch_simdasi_populasi_kab.py`) | Agregasi & Cleaning | - | Bab 9.1, 9.2, 9.4 | Data master demografi. Raw data (JSON) ditarik via API langsung ke `processed/sulawesi_populasi_kab_simdasi.csv` tanpa file CSV mentah. |
| 42 | `sulawesi_employment_shift_fase4.csv` | BPS SIMDASI | Transformasi Shift Index | - | Bab 9.3, 9.4 | Data index pergeseran proporsi lapangan kerja dan struktur ekonomi. |
| 43 | `nasional_ekspor_2022_2026.csv` | `data/raw/eksporimpor/` | API BPS | - | Master Data (ETL) | Data agregat ekspor nasional. |
| 44 | `nasional_gfn_historis_1_dekade.csv` | `data/raw/klhk_gfn/` | Data Sekunder GFN | - | Master Data (ETL) | Jejak ekologi (Global Footprint Network) nasional. |
| 45 | `nasional_ika_2015_2024.csv` | `data/raw/klhk_ika/` | Scraping PDF KLHK | - | Master Data (ETL) | Data pembanding baseline IKA Nasional. |
| 46 | `nasional_investasi_pmdn_2016_2024.csv` | `data/raw/bps_pmdn/` | API BPS / BKPM | Request JSON | Master Data (ETL) | Realisasi PMDN agregat Nasional. |
| 47 | `nasional_kesehatan_2014_2024.csv` | `data/raw/profil_kesehatan_kemenkes/` | Ekstraksi PDF | Agregasi | Master Data (ETL) | Data agregat penderita ISPA/Diare/Malaria nasional. |
| 48 | `nasional_kesehatan_detail_2014_2024.csv` | `data/raw/profil_kesehatan_kemenkes/` | Ekstraksi PDF | - | Master Data (ETL) | Versi detail nasional. (Potensi duplikat). |
| 49 | `nasional_konflik_agraria_tanahkita.csv` | `data/raw/konflik_kpa_ylbhi_tanahkita/` | API Tanahkita | `extract_konflik_hukum.py` | Master Data (ETL) | Master dataset konflik nasional. |
| 50 | `nasional_konversi_gfn.csv` | `data/raw/klhk_gfn/` | Data Sekunder GFN | - | Master Data (ETL) | Konversi biokapasitas. |
| 51 | `nasional_limbah_b3_2020_2024.csv` | `data/raw/D3TLH/` | Scraping Laporan | - | Master Data (ETL) | Volume limbah B3 nasional. |
| 52 | `sulut_ika_1_dekade_2016_2024.csv` | `sulawesi_ika_2016_2024.csv` | Reshape | Potensi duplikat | Tidak Ditampilkan | Kandidat dihapus. |
