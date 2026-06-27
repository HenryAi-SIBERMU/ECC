# 📖 Kamus Data & Silsilah (Data Provenance)
Dokumen ini memetakan **seluruh dataset di folder `data/processed`** ke sumber asalnya (baik dari BPS, ekstraksi PDF KLHK, scraping, maupun NGO).

## Master Summary (Keseluruhan)

| No | Nama File Processed | Sumber Asli (Raw/Master) | Kategori/Medium | Script Transformasi | Deskripsi / Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `kpa_catahu_2025_izin_ilegal_sulawesi.csv` | `data/raw/konflik_kpa_ylbhi_tanahkita/` | Scraping PDF | - | Data profil izin ilegal dari KPA. |
| 2 | `kpa_masalah_izin_perusahaan.csv` | Laporan CATAHU KPA | Scraping PDF | - | Ekstraksi profil konflik by perusahaan. |
| 3 | `nasional_ekspor_2022_2026.csv` | `data/raw/eksporimpor/` | API BPS | - | Data agregat ekspor nasional. |
| 4 | `nasional_gfn_historis_1_dekade.csv` | `data/raw/klhk_gfn/` | Data Sekunder GFN | - | Jejak ekologi (Global Footprint Network) nasional. |
| 5 | `nasional_ika_2015_2024.csv` | `data/raw/klhk_ika/` | Scraping PDF KLHK | - | Data pembanding baseline IKA Nasional. |
| 6 | `nasional_investasi_pmdn_2016_2024.csv` | `data/raw/bps_pmdn/` | API BPS / BKPM | Request JSON | Realisasi PMDN agregat Nasional. |
| 7 | `nasional_kesehatan_2014_2024.csv` | `data/raw/profil_kesehatan_kemenkes/` | Ekstraksi PDF | Agregasi | Data agregat penderita ISPA/Diare/Malaria nasional. |
| 8 | `nasional_kesehatan_detail_2014_2024.csv` | `data/raw/profil_kesehatan_kemenkes/` | Ekstraksi PDF | - | Versi detail nasional. (Potensi duplikat). |
| 9 | `nasional_konflik_agraria_tanahkita.csv` | `data/raw/konflik_kpa_ylbhi_tanahkita/` | API Tanahkita | `extract_konflik_hukum.py` | Master dataset konflik nasional. |
| 10 | `nasional_konversi_gfn.csv` | `data/raw/klhk_gfn/` | Data Sekunder GFN | - | Konversi biokapasitas. |
| 11 | `nasional_limbah_b3_2020_2024.csv` | `data/raw/D3TLH/` | Scraping Laporan | - | Volume limbah B3 nasional. |
| 12 | `sulawesi_bencana_bnpb_2014_2024.csv` | Data DIBI BNPB | API / CSV Eksport | - | Frekuensi Bencana Ekologis. |
| 13 | `sulawesi_ekspor_2022_2026.csv` | `data/raw/eksporimpor/` | API BPS | - | Agregat total ekspor Sulawesi. |
| 14 | `sulawesi_ekspor_detail_2020_2026.csv` | `data/raw/eksporimpor/` | API BPS | - | Rincian ekspor by HS Code. |
| 15 | `sulawesi_ekspor_komoditas_2020_2026.csv` | `data/raw/eksporimpor/` | API BPS | - | Rincian ekspor by komoditas spesifik. |
| 16 | `sulawesi_ekspor_negara_2020_2026.csv` | `data/raw/eksporimpor/` | API BPS | - | Rincian ekspor tujuan negara. |
| 17 | `sulawesi_esdm_nikel.csv` | `data/raw/izin_ESDM/` | Data Registry ESDM | `tools/esdm/` | Master data Fasilitas Smelter Nikel. |
| 18 | `sulawesi_faskes_agregat.csv` | `data/raw/bps_kemenkesispadiaremalaria/` | API BPS | - | Data fasilitas kesehatan. |
| 19 | `sulawesi_gfw_hutan_primer_loss_2014_2023.csv` | Master GFW | Reshape dari Master | Agregasi Pandas | Hutan primer spesifik. |
| 20 | `sulawesi_gfw_kawasan_lindung_loss_2014_2023.csv` | Master GFW | Reshape dari Master | Agregasi Pandas | Batas zona lindung. |
| 21 | `sulawesi_gfw_loss_by_driver_2014_2023.csv` | Master GFW | Reshape dari Master | Agregasi Pandas | Driver spesifik (Mining/Commodity). |
| 22 | `sulawesi_gfw_master_1_dekade_2014_2023.csv` | `data/raw/klhk_gfw/` | Ekspor Platform | - | Master tree cover loss. |
| 23 | `sulawesi_ika_2016_2024.csv` | `data/raw/klhk_ika/` | Scraping PDF KLHK | Table OCR | Indeks Kualitas Air. |
| 24 | `sulawesi_iku_2015_2024.csv` | `data/raw/klhk_iku/` | Scraping PDF KLHK | Table OCR | Indeks Kualitas Udara. |
| 25 | `sulawesi_investasi_nikel.csv` | `data/raw/izin_ESDM/` | Reshape | - | Investasi spesifik Nikel. |
| 26 | `sulawesi_investasi_pmdn_2016_2024.csv` | nasional_investasi_... | Reshape dari Master | Agregasi Pandas | Realisasi PMDN Sulawesi. |
| 27 | `sulawesi_izin_baru_per_tahun.csv` | Minerbaone | Data Sekunder | - | Tren IUP per tahun. |
| 28 | `sulawesi_izin_raw_details.csv` | Minerbaone | Data Sekunder | - | Detail raw data IUP. |
| 29 | `sulawesi_kawasan_nikel_luas.csv` | `sulawesi_esdm_nikel.csv` | Reshape | Hitung Luasan | Agregat luasan lahan. |
| 30 | `sulawesi_kawasan_nikel_luas_per_provinsi.csv` | `sulawesi_esdm_nikel.csv` | Reshape | Agregasi | Luas per provinsi. |
| 31 | `sulawesi_kesehatan_detail_2014_2024.csv` | nasional_kesehatan_... | Reshape | Pemotongan array | Filter 6 Provinsi. |
| 32 | `sulawesi_konflik_agraria_tanahkita.csv` | `data/raw/konflik_kpa_ylbhi_tanahkita/` | API Tanahkita | `extract_...` | Data konflik KPA & YLBHI. |
| 33 | `sulawesi_konflik_hukum.csv` | `data/raw/konflik_kpa_ylbhi_tanahkita/` | Web Scraping | - | Data konflik dari ranah hukum. |
| 34 | `sulawesi_konflik_tambang_fpic.csv` | NGO Jatam/Walhi | Web Scraping | - | Pelanggaran FPIC. |
| 35 | `sulawesi_limbah_b3.csv` | `data/raw/D3TLH/` | Data Laporan | - | Volume B3 proxy. |
| 36 | `sulawesi_limbah_b3_ngo_proxy.csv` | NGO Laporan | Scraping | - | Estimasi limbah B3 oleh NGO. |
| 37 | `sulawesi_pad_2016_2024.csv` | `data/raw/bps_pad/` | API BPS | - | PAD Total. |
| 38 | `sulawesi_pad_breakdown_2016_2024.csv` | `data/raw/bps_pad/` | API BPS | - | Rincian PAD. |
| 39 | `sulawesi_pltu_captive.csv` | Global Energy Monitor | Data Sekunder NGO | Manual Filter | Data PLTU Captive. |
| 40 | `sulut_ika_1_dekade_2016_2024.csv` | `sulawesi_ika_2016_2024.csv` | Reshape | Potensi duplikat | Kandidat dihapus. |

---

## 2. Fase 2: Algoritma Validasi Deduplikasi (Data Science 2026 Golden Standard)

Untuk memastikan folder `data/processed` tetap bersih, bebas ambiguitas, dan berfungsi sebagai *Single Source of Truth*, sistem deduplikasi ini di-upgrade menggunakan pendekatan **Golden Standard Data Science 2026**. Algoritma ini berjalan secara hierarkis dari level fisik (byte) hingga level semantik (makna data):

### A. Data Fingerprinting & Locality Sensitive Hashing (LSH)
1. **MinHash / Jaccard Similarity:** Tidak lagi sekadar mengandalkan SHA-256 (yang rentan gagal hanya karena beda 1 karakter spasi). Kami akan memindai nilai *MinHash* setiap baris data untuk mencari tingkat kemiripan (Jaccard Index) antar dataset.
2. **Aksi:** Jika *similarity score* > 98%, meskipun nama file dan struktur kolomnya sedikit berbeda, sistem akan mendeteksinya sebagai data yang berulang (redundant).

### B. Semantic Schema Matching
1. **Type Inference & Column Mapping:** Membandingkan dataset bukan dari teks nama kolomnya (`==`), melainkan dari makna datanya. Sistem akan menyadari bahwa kolom bernama `thn` di File A adalah entitas yang persis sama dengan kolom `tahun` di File B.
2. **Subset Validation:** Memeriksa apakah File A (misal: *sulut_ika_1_dekade*) secara semantik merupakan himpunan bagian murni (subset) dari File B (*sulawesi_ika_2016_2024*).
3. **Aksi:** Jika File A secara fungsional telah ter-cover 100% oleh File B, maka File A akan dihapus.

### C. Entity Resolution & Record Linkage (Fuzzy Matching)
1. **Pengecekan Duplikasi Baris (Row-level):** Menggunakan algoritma *Jaro-Winkler* atau *Levenshtein Distance* untuk mengidentifikasi duplikasi baris dengan variasi penulisan.
2. **Contoh Kasus:** Sistem akan otomatis menggabungkan "PT. Vale Indonesia" dan "Vale Indonesia Tbk" sebagai satu entitas perusahaan yang sama.
3. **Aksi:** Baris yang berduplikasi secara fuzzy akan di-merger (*keep last* atau *sum/aggregate* tergantung jenis metriknya) untuk mencegah inflasi data palsu.

# 📖 Kamus Data & Silsilah (Data Provenance)
Dokumen ini memetakan **seluruh dataset di folder `data/processed`** ke sumber asalnya (baik dari BPS, ekstraksi PDF KLHK, scraping, maupun NGO).

## Master Summary (Keseluruhan)

| No | Nama File Processed | Sumber Asli (Raw/Master) | Kategori/Medium | Script Transformasi | Deskripsi / Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `kpa_catahu_2025_izin_ilegal_sulawesi.csv` | `data/raw/konflik_kpa_ylbhi_tanahkita/` | Scraping PDF | - | Data profil izin ilegal dari KPA. |
| 2 | `kpa_masalah_izin_perusahaan.csv` | Laporan CATAHU KPA | Scraping PDF | - | Ekstraksi profil konflik by perusahaan. |
| 3 | `nasional_ekspor_2022_2026.csv` | `data/raw/eksporimpor/` | API BPS | - | Data agregat ekspor nasional. |
| 4 | `nasional_gfn_historis_1_dekade.csv` | `data/raw/klhk_gfn/` | Data Sekunder GFN | - | Jejak ekologi (Global Footprint Network) nasional. |
| 5 | `nasional_ika_2015_2024.csv` | `data/raw/klhk_ika/` | Scraping PDF KLHK | - | Data pembanding baseline IKA Nasional. |
| 6 | `nasional_investasi_pmdn_2016_2024.csv` | `data/raw/bps_pmdn/` | API BPS / BKPM | Request JSON | Realisasi PMDN agregat Nasional. |
| 7 | `nasional_kesehatan_2014_2024.csv` | `data/raw/profil_kesehatan_kemenkes/` | Ekstraksi PDF | Agregasi | Data agregat penderita ISPA/Diare/Malaria nasional. |
| 8 | `nasional_kesehatan_detail_2014_2024.csv` | `data/raw/profil_kesehatan_kemenkes/` | Ekstraksi PDF | - | Versi detail nasional. (Potensi duplikat). |
| 9 | `nasional_konflik_agraria_tanahkita.csv` | `data/raw/konflik_kpa_ylbhi_tanahkita/` | API Tanahkita | `extract_konflik_hukum.py` | Master dataset konflik nasional. |
| 10 | `nasional_konversi_gfn.csv` | `data/raw/klhk_gfn/` | Data Sekunder GFN | - | Konversi biokapasitas. |
| 11 | `nasional_limbah_b3_2020_2024.csv` | `data/raw/D3TLH/` | Scraping Laporan | - | Volume limbah B3 nasional. |
| 12 | `sulawesi_bencana_bnpb_2014_2024.csv` | Data DIBI BNPB | API / CSV Eksport | - | Frekuensi Bencana Ekologis. |
| 13 | `sulawesi_ekspor_2022_2026.csv` | `data/raw/eksporimpor/` | API BPS | - | Agregat total ekspor Sulawesi. |
| 14 | `sulawesi_ekspor_detail_2020_2026.csv` | `data/raw/eksporimpor/` | API BPS | - | Rincian ekspor by HS Code. |
| 15 | `sulawesi_ekspor_komoditas_2020_2026.csv` | `data/raw/eksporimpor/` | API BPS | - | Rincian ekspor by komoditas spesifik. |
| 16 | `sulawesi_ekspor_negara_2020_2026.csv` | `data/raw/eksporimpor/` | API BPS | - | Rincian ekspor tujuan negara. |
| 17 | `sulawesi_esdm_nikel.csv` | `data/raw/izin_ESDM/` | Data Registry ESDM | `tools/esdm/` | Master data Fasilitas Smelter Nikel. |
| 18 | `sulawesi_faskes_agregat.csv` | `data/raw/bps_kemenkesispadiaremalaria/` | API BPS | - | Data fasilitas kesehatan. |
| 19 | `sulawesi_gfw_hutan_primer_loss_2014_2023.csv` | Master GFW | Reshape dari Master | Agregasi Pandas | Hutan primer spesifik. |
| 20 | `sulawesi_gfw_kawasan_lindung_loss_2014_2023.csv` | Master GFW | Reshape dari Master | Agregasi Pandas | Batas zona lindung. |
| 21 | `sulawesi_gfw_loss_by_driver_2014_2023.csv` | Master GFW | Reshape dari Master | Agregasi Pandas | Driver spesifik (Mining/Commodity). |
| 22 | `sulawesi_gfw_master_1_dekade_2014_2023.csv` | `data/raw/klhk_gfw/` | Ekspor Platform | - | Master tree cover loss. |
| 23 | `sulawesi_ika_2016_2024.csv` | `data/raw/klhk_ika/` | Scraping PDF KLHK | Table OCR | Indeks Kualitas Air. |
| 24 | `sulawesi_iku_2015_2024.csv` | `data/raw/klhk_iku/` | Scraping PDF KLHK | Table OCR | Indeks Kualitas Udara. |
| 25 | `sulawesi_investasi_nikel.csv` | `data/raw/izin_ESDM/` | Reshape | - | Investasi spesifik Nikel. |
| 26 | `sulawesi_investasi_pmdn_2016_2024.csv` | nasional_investasi_... | Reshape dari Master | Agregasi Pandas | Realisasi PMDN Sulawesi. |
| 27 | `sulawesi_izin_baru_per_tahun.csv` | Minerbaone | Data Sekunder | - | Tren IUP per tahun. |
| 28 | `sulawesi_izin_raw_details.csv` | Minerbaone | Data Sekunder | - | Detail raw data IUP. |
| 29 | `sulawesi_kawasan_nikel_luas.csv` | `sulawesi_esdm_nikel.csv` | Reshape | Hitung Luasan | Agregat luasan lahan. |
| 30 | `sulawesi_kawasan_nikel_luas_per_provinsi.csv` | `sulawesi_esdm_nikel.csv` | Reshape | Agregasi | Luas per provinsi. |
| 31 | `sulawesi_kesehatan_detail_2014_2024.csv` | nasional_kesehatan_... | Reshape | Pemotongan array | Filter 6 Provinsi. |
| 32 | `sulawesi_konflik_agraria_tanahkita.csv` | `data/raw/konflik_kpa_ylbhi_tanahkita/` | API Tanahkita | `extract_...` | Data konflik KPA & YLBHI. |
| 33 | `sulawesi_konflik_hukum.csv` | `data/raw/konflik_kpa_ylbhi_tanahkita/` | Web Scraping | - | Data konflik dari ranah hukum. |
| 34 | `sulawesi_konflik_tambang_fpic.csv` | NGO Jatam/Walhi | Web Scraping | - | Pelanggaran FPIC. |
| 35 | `sulawesi_limbah_b3.csv` | `data/raw/D3TLH/` | Data Laporan | - | Volume B3 proxy. |
| 36 | `sulawesi_limbah_b3_ngo_proxy.csv` | NGO Laporan | Scraping | - | Estimasi limbah B3 oleh NGO. |
| 37 | `sulawesi_pad_2016_2024.csv` | `data/raw/bps_pad/` | API BPS | - | PAD Total. |
| 38 | `sulawesi_pad_breakdown_2016_2024.csv` | `data/raw/bps_pad/` | API BPS | - | Rincian PAD. |
| 39 | `sulawesi_pltu_captive.csv` | Global Energy Monitor | Data Sekunder NGO | Manual Filter | Data PLTU Captive. |
| 40 | `sulut_ika_1_dekade_2016_2024.csv` | `sulawesi_ika_2016_2024.csv` | Reshape | Potensi duplikat | Kandidat dihapus. |

---

## 2. Fase 2: Algoritma Validasi Deduplikasi (Data Science 2026 Golden Standard)

Untuk memastikan folder `data/processed` tetap bersih, bebas ambiguitas, dan berfungsi sebagai *Single Source of Truth*, sistem deduplikasi ini di-upgrade menggunakan pendekatan **Golden Standard Data Science 2026**. Algoritma ini berjalan secara hierarkis dari level fisik (byte) hingga level semantik (makna data):

### A. Data Fingerprinting & Locality Sensitive Hashing (LSH)
1. **MinHash / Jaccard Similarity:** Tidak lagi sekadar mengandalkan SHA-256 (yang rentan gagal hanya karena beda 1 karakter spasi). Kami akan memindai nilai *MinHash* setiap baris data untuk mencari tingkat kemiripan (Jaccard Index) antar dataset.
2. **Aksi:** Jika *similarity score* > 98%, meskipun nama file dan struktur kolomnya sedikit berbeda, sistem akan mendeteksinya sebagai data yang berulang (redundant).

### B. Semantic Schema Matching
1. **Type Inference & Column Mapping:** Membandingkan dataset bukan dari teks nama kolomnya (`==`), melainkan dari makna datanya. Sistem akan menyadari bahwa kolom bernama `thn` di File A adalah entitas yang persis sama dengan kolom `tahun` di File B.
2. **Subset Validation:** Memeriksa apakah File A (misal: *sulut_ika_1_dekade*) secara semantik merupakan himpunan bagian murni (subset) dari File B (*sulawesi_ika_2016_2024*).
3. **Aksi:** Jika File A secara fungsional telah ter-cover 100% oleh File B, maka File A akan dihapus.

### C. Entity Resolution & Record Linkage (Fuzzy Matching)
1. **Pengecekan Duplikasi Baris (Row-level):** Menggunakan algoritma *Jaro-Winkler* atau *Levenshtein Distance* untuk mengidentifikasi duplikasi baris dengan variasi penulisan.
2. **Contoh Kasus:** Sistem akan otomatis menggabungkan "PT. Vale Indonesia" dan "Vale Indonesia Tbk" sebagai satu entitas perusahaan yang sama.
3. **Aksi:** Baris yang berduplikasi secara fuzzy akan di-merger (*keep last* atau *sum/aggregate* tergantung jenis metriknya) untuk mencegah inflasi data palsu.

### D. Eksekusi Refactoring (Safe Deletion & Lineage Rerouting)
1. **Deduplication Audit:** File yang terbukti redundan akan dihapus dari `data/processed/`.
2. **Automated Rerouting:** Meluncurkan skrip Python (*Abstract Syntax Tree / Regex Parser*) untuk memindai seluruh *file* `pages/*.py`. Semua baris kode `pd.read_csv(...)` yang memanggil dataset lama akan otomatis di-refactor agar merujuk ke Master Dataset yang paling valid.

---

## 3. Log Temuan Audit (Dry-Run Phase)

Berdasarkan investigasi eksekusi skrip *Golden Standard* pada bulan Juni 2026, telah ditemukan dua anomali redundansi di dalam *repository* ini:

* **[23 Juni 2026] Redundansi Semantik (Subset Data):**
  - 🔍 **TEMUAN:** `sulawesi_ekspor_2022_2026.csv` secara absolut adalah subset 100% dari file master `nasional_ekspor_2022_2026.csv`.
  - ❌ **STATUS:** **DITOLAK (Dibatalkan).** Eksekusi fisik pembongkaran file dibatalkan. Mengubah *routing* file di kode UI berisiko tinggi memunculkan *error* pada *dashboard* (*breaking changes*). Keberadaan file ini secara mandiri tidak menimbulkan bias kalkulasi data.

* **[23 Juni 2026] Duplikasi Entitas (Fuzzy Match / Record Linkage):**
  - 🔍 **TEMUAN:** Pada file `sulawesi_esdm_nikel.csv`, algoritma mendeteksi `STARGATE DUA PASIFIC RESOURCES` memiliki *Jaro-Winkler ratio* **92.9%** terhadap `STARGATE PASIFIC RESOURCES`.
  - ✅ **STATUS:** **DITOLAK (Bukan Duplikat).** Hasil verifikasi manual membuktikan bahwa ini adalah dua entitas legal yang terpisah (Induk & Anak Perusahaan) yang memiliki Nomor Induk Berusaha (NIB) dan blok konsesi (luas Ha) yang berbeda, meskipun berada di alamat kantor yang sama. Entitas ini dipertahankan secara terpisah.

---

## 4. Pemetaan Kualitas Data (Analisis Data Bolong / Null pada Metrik)

Berdasarkan pemindaian lanjutan secara spesifik pada kolom berjenis metrik fisik dan finansial (mengandung kata kunci `luas`, `kapasitas`, `nilai`, `jumlah`, `produksi`), ditemukan **indikasi data bolong (Missing Values)** di mana nilai kosong terekam sebagai `0`, `0.0`, atau `NaN`. 

Tabel berikut memetakan tingkat kekosongan dan mengklasifikasikan apakah `0` tersebut adalah fakta alamiah (*Structural Zero*) atau cacat data (*Missing Zero*):

| Nama File | Total Sel Metrik | Persentase Bolong | Contoh Kolom Terdampak | Jenis Kekosongan (Zero Type) | Keterangan OSINT | Link Validasi | Rekomendasi Imputasi |
|---|---|---|---|---|---|---|---|
| `sulawesi_konflik_agraria_tanahkita.csv` | 2272 | **81.0%** | luas_ha, jumlah_luka... | **Missing Zeroes** | Laporan lapangan NGO (Tanahkita) parsial / korban tidak didata | - | MICE / KNN |
| `sulawesi_esdm_nikel.csv` | 7002 | **66.8%** | total_luas_ha, kapasitas... | **Missing Zeroes** | Data tidak dilaporkan korporasi ke ESDM / form kosong | - | MICE / KNN |
| `sulawesi_izin_baru_per_tahun.csv` | 132 | **31.1%** | Jumlah_Izin, Luas_Ha... | **Structural Zeros** | Efek **Moratorium Clean & Clear** (2015-2018) & penarikan wewenang UU Minerba (2020) menunda izin. | [MODI ESDM](https://modi.esdm.go.id/) | **Dilarang Diubah** |
| `sulawesi_ekspor_2022_2026.csv` | 51 | **29.4%** | nilai | **Structural Zeros** | Secara riil nol (0) volume bongkar muat untuk komoditas tsb. | [BPS Ekspor](https://bps.go.id/) | **Dilarang Diubah** |
| `sulawesi_kawasan_nikel_luas.csv` | 3112 | **23.7%** | total_luas_ha... | **Missing Zeroes** | Poligon konsesi terbit tanpa disertai input luas hektar di web | - | MICE / KNN |
| `sulawesi_faskes_agregat.csv` | 2269 | **16.0%** | jumlah | **Structural Zeros** | Secara administratif memang belum ada faskes terbangun. | - | **Dilarang Diubah** |
| `nasional_ekspor_2022_2026.csv` | 343 | **13.7%** | nilai | **Structural Zeros** | Tidak ada transaksi pada bulan spesifik. | - | **Dilarang Diubah** |
| `sulawesi_kawasan_nikel_luas_per_provinsi.csv` | 12 | **8.3%** | total_luas_amdal_ha | **Missing Zeroes** | Ekstraksi Amdal otomatis kehilangan metadata luas. | - | MICE / KNN |
| `sulawesi_pad_breakdown_2016_2024.csv` | 125 | **6.4%** | nilai_juta_rupiah | **Structural Zeros** | Pemda terkait tidak menarik jenis retribusi/pajak tersebut. | [DJPK](https://djpk.kemenkeu.go.id/) | **Dilarang Diubah** |
| `kpa_masalah_izin_perusahaan.csv` | 21 | **4.8%** | luas_ha | **Missing Zeroes** | Data luasan tidak dirinci di dokumen CATAHU KPA PDF. | - | Basic Mean |
| `nasional_kesehatan_detail_2014_2024.csv` | 1480 | **2.3%** | nilai | **Structural Zeros** | Benar-benar nihil kasus / 0 penderita dilaporkan. | - | **Dilarang Diubah** |
| `sulawesi_izin_raw_details.csv` | 574 | **1.9%** | luas_ha | **Missing Zeroes** | Anomali / korupsi data arsip MODI. | - | MICE / KNN |
| `sulawesi_kesehatan_detail_2014_2024.csv` | 258 | **1.6%** | nilai | **Structural Zeros** | Nol kasus di provinsi/tahun spesifik secara medis. | - | **Dilarang Diubah** |

---

## 5. Penanganan Data Imbalance & Structural Zeros

Dalam konteks Data Science dan pemodelan prediktif, tidak semua data yang bernilai `0` boleh di-*treatment* sebagai data kosong (*Missing Value*) yang harus di-imputasi (diisi ulang menggunakan KNN atau MICE). 

Terdapat prinsip pembeda yang sangat krusial di *repository* ini:

### A. Structural Zeros (Nol Faktual) - Dilarang Diubah
Angka `0` yang muncul secara organik sebagai konsekuensi dari hukum bisnis/alam. 
- **Studi Kasus Pilot:** Pada file `sulawesi_izin_baru_per_tahun.csv`, ditemukan nilai Luas Hektar bernilai `0`. Angka ini linier dengan kolom sebelahnya di mana Jumlah Izin yang terbit pada tahun tersebut memang `0`.
- **Verifikasi OSINT / Dorking:** Penelusuran silang di portal Minerba ESDM membuktikan bahwa angka `0` ini adalah fakta sejarah, bukan gagal *scrape*. Nol izin baru muncul secara spesifik pada era **Moratorium Izin (Penertiban Clean and Clear / CNC 2015-2017)** dan masa **Transisi Kewenangan Daerah ke Pusat (UU No 3/2020)** di mana pemerintah memang menghentikan penerbitan IUP baru di wilayah seperti Gorontalo dan Sulbar.
- **Aturan Eksekusi:** Jika kita memaksa algoritma MICE/KNN menebak angka tersebut, AI akan menciptakan **izin tambang fiktif** di tengah masa moratorium pemerintah. Oleh karena itu, *Structural Zeros* **HARUS DIPERTAHANKAN** secara mutlak apa adanya.

### B. Missing Zeros (Data Bolong) - Wajib Diimputasi
Angka `0` atau `NaN` yang terjadi karena kegagalan pencatatan data padahal entitas tersebut beroperasi.
- **Studi Kasus:** Pada file `sulawesi_esdm_nikel.csv`, banyak pabrik nikel yang beroperasi penuh namun kapasitas produksinya ditulis `0`. Ini adalah *Missing Zeros*.
- **Aturan Eksekusi:** Diperlukan penanganan *Data Imbalance* atau teknik imputasi lanjutan (MICE / KNN Imputer) untuk menebak angka tersebut berdasarkan profil perusahaan tetangga yang mirip, agar metrik analitik di *dashboard* tidak jatuh (*bias*) ke bawah.
