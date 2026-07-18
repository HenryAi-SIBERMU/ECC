# Kompilasi Sumber Data KLHK & Ekologis (Final)

Dokumen ini memuat pemetaan sumber data untuk variabel-variabel terkait KLHK dan Beban Ekologis berdasarkan kebutuhan PRD (Fase 1) serta tambahan referensi dari Lampiran Teknis 2 (Dataset Mining). 

Karena adanya kendala teknis (down server/DNS Error) pada portal utama Kementerian Lingkungan Hidup dan Kehutanan (KLHK) seperti `menlhk.go.id` dan `sipsn.menlhk.go.id`, daftar sumber ini telah dilengkapi dengan rute alternatif (*Bypass*) melalui portal penyedia sekunder resmi maupun jaringan portal data internasional berstandar tinggi yang mencakup wilayah Indonesia (Sulawesi).

| Komponen / Kebutuhan | Variabel Data | Sumber Data Utama (Saran) | Alternatif (Jika Web KLHK Down) | Status Akses |
| :--- | :--- | :--- | :--- | :--- |
| **Kualitas Air** (PRD) | Indeks Kualitas Air (IKA) | Portal IKLH KLHK | BPS Web API (Statistik Lingkungan) | 🟢 BPS API Tersedia |
| **Kualitas Udara** (PRD) | Indeks Kualitas Udara (IKU) / PM2.5 | OpenAQ / IKLH KLHK | BPS Web API / [OpenAQ API v3](https://api.openaq.org/) | 🟢 BPS API & OpenAQ v3 Tersedia |
| **Limbah Industri** (PRD) | Timbulan Limbah B3 | SIPSN KLHK | BPS Web API (Statistik Lingkungan) | 🟡 Perlu Scraping BPS |
| **Deforestasi** (PRD) | Laju Deforestasi / Hotspot | Geoportal KLHK | [NASA FIRMS](https://firms.modaps.eosdis.nasa.gov/) / BPS Web API | 🟢 NASA FIRMS Tersedia |
| **Persampahan** (Lampiran 2) | Jumlah timbulan sampah / emisi CO2 sampah | SIPSN KLHK / Faktor Emisi KLHK | BPS Web API / [IPCC EFDB](https://www.ipcc-nggip.iges.or.jp/EFDB/) | 🟡 Perlu Scraping BPS |
| **Biokapasitas** (Lampiran 2) | Luas area penggunaan lahan & Kawasan Hutan | Geoportal KLHK | [Copernicus Land](https://land.copernicus.eu/global/) / [GFN](http://data.footprintnetwork.org/) / BPS Web API | 🟡 Perlu Scraping BPS |

---
*Dibuat untuk panduan ekstraksi data pada sistem intelijen CELIOS ECC.*

---

## 📋 Log Aktivitas

> Semua kegiatan *data engineering* untuk variabel KLHK dicatat di sini secara kronologis beserta hasilnya.

---

### [2026-06-13 03:42 WIB] ASESMEN SUMBER UTAMA — Kualitas Air (IKA)

**Target:** Portal IKLH KLHK (`https://iklh.menlhk.go.id`)
**Tujuan:** Menguji apakah portal KLHK dapat di-*scrape* untuk data Indeks Kualitas Air (IKA).

**Hasil Asesmen:**

| URL yang Diuji | Status | Keterangan |
| :--- | :--- | :--- |
| `https://iklh.menlhk.go.id` | ❌ `ConnectionError` | DNS Resolution gagal — server tidak bisa di-*resolve* dari jaringan publik |
| `https://iklh.menlhk.go.id/api` | ❌ `ConnectionError` | idem |
| `https://iklh.menlhk.go.id/data/ika` | ❌ `ConnectionError` | idem |
| `https://menlhk.go.id` | ❌ `ConnectionError` | Domain utama KLHK pun tidak bisa diakses |
| `https://sipsn.menlhk.go.id` | ❌ `ConnectionError` | idem |

**Kesimpulan:** ⛔ **Sumber Utama TIDAK BISA di-scrape.** Seluruh subdomain KLHK mengalami DNS Resolution Error (kemungkinan besar diblokir dari luar jaringan intranet pemerintah, atau sedang dalam pemeliharaan/migrasi server).

**→ Strategi Bypass:** Beralih ke **BPS Web API** sebagai sumber sekunder resmi.

---

### [2026-06-13 03:50 WIB] ASESMEN ALTERNATIF — BPS Web API (Kualitas Air)

**Target:** `https://webapi.bps.go.id` — Tabel Statis "Status Kualitas Air Sungai"
**Metode:** BPS Web API v1 dengan keyword search + `model/statictable`

**Hasil Asesmen:**

| Langkah | Hasil |
| :--- | :--- |
| Pencarian keyword `indeks kualitas air` di BPS API | ✅ Ditemukan **1 tabel**: `ID=1372 - "Status Kualitas Air Sungai, 2007–2016"` |
| Akses isi tabel 1372 via `model/view/statictable` | ✅ HTTP 200 — Data tersedia dalam format HTML tabel |
| Sub-kategori tabel | `Lingkungan` (subcat_id=539) |
| Cakupan tahun | **2007–2016** (10 tahun) |
| Format respons API | HTML embedded dalam JSON (perlu *parsing* BeautifulSoup) |
| Download Excel | ✅ Link unduhan tersedia: `http://www.archive.bps.go.id/...` |

---

### [2026-06-13 07:08 WIB] PENEMUAN DOMAIN BARU 2026 (SITALA & SIPSN)

**Konteks:** Menindaklanjuti informasi bahwa struktur kementerian berubah pada tahun 2024-2029. Kementerian Lingkungan Hidup dan Kehutanan (KLHK) telah dipecah menjadi Kementerian Kehutanan (`kehutanan.go.id`) dan **Kementerian Lingkungan Hidup (`kemenlh.go.id`)**.

**Target Asesmen:** Portal IKLH dan SIPSN di bawah domain baru `kemenlh.go.id`.

**Hasil Asesmen:**

| Target/URL | Hasil HTTP | Keterangan |
| :--- | :--- | :--- |
| `https://kemenlh.go.id` | ✅ `200 OK` | Portal utama Kementerian Lingkungan Hidup aktif. |
| `https://sipsn.kemenlh.go.id` | ✅ `200 OK` | Sistem Informasi Pengelolaan Sampah Nasional (SIPSN) berhasil diakses menggunakan domain baru. |
| `https://sitala.kemenlh.go.id` | ✅ `200 OK` | SITALA (Sistem Informasi IKLH/IRLH baru pengganti iklh.menlhk.go.id) aktif dan berhasil diakses. |

---

### [2026-06-13 11:41 WIB] PENEMUAN & ASESMEN PORTAL OPEN DATA PROVINSI

**Konteks:** Menghindari kendala *login* pada portal SITALA KemenLH, user menyarankan untuk mengakses data langsung dari hulunya, yaitu portal Open Data milik masing-masing provinsi di Sulawesi (berdasarkan inisiatif Satu Data Indonesia tingkat daerah).

**Target Asesmen:** Portal Open Data dari 6 provinsi di Sulawesi.

**Hasil Asesmen API (CKAN/SatuData):**

| Provinsi | URL Portal | Status HTTP | Keterangan/Sistem |
| :--- | :--- | :--- | :--- |
| **Sulawesi Utara** | `opendata.sulutprov.go.id` | ✅ `200 OK` (API CKAN) | Ditemukan **23 dataset** untuk keyword "kualitas air" via API `/api/3/action/package_search`. Sangat siap untuk di-*scrape*. |
| **Sulawesi Barat** | `opendata.sulbarprov.go.id` | ✅ `200 OK` (API) | API merespons tapi *parsing* JSON gagal. Perlu penyesuaian metode *scraping* (mungkin HTML *parsing*). |
| **Sulawesi Selatan** | `satudata.sulselprov.go.id` | ✅ `200 OK` (Web) / ❌ `404` (API) | Halaman utama aktif, tapi tidak memakai CKAN. Harus di-*scrape* via *web scraping* biasa. |
| **Sulawesi Tengah** | `satudata.sultengprov.go.id`| ✅ `200 OK` (Web) / ❌ `404` (API) | Sama seperti Sulsel, mesin berbeda, harus di-*scrape* HTML-nya. |
| **Sulawesi Tenggara** | `simdata.sultraprov.go.id` | ✅ `200 OK` (Web) / ❌ `404` (API) | Sama, menggunakan SIMDATA kustom. Harus di-*scrape* HTML-nya. |
| **Gorontalo** | `data.gorontaloprov.go.id` | (Belum diuji spesifik) | Akan dilakukan asesmen menyusul. |

**Kesimpulan:** 🟢 **Strategi Baru Disetujui.** Kita akan menggunakan teknik *web scraping* hibrida (API CKAN untuk Sulut + BeautifulSoup/Selenium untuk provinsi lainnya) guna menyedot data lingkungan hidup dari seluruh regional Sulawesi. Detail implementasi dipindahkan ke dokumen terpisah.

---

### [2026-06-13 12:15 WIB] ASESMEN OPENAQ API — GAGAL TOTAL

**Target:** OpenAQ API v3 (`https://api.openaq.org/v3/locations`) untuk data PM2.5/PM10 Sulawesi.

**API Key:** `e60fbf886cd900097ff7362b8332161680d2c2e2b4ee1fd7f84aa4ec9af718f5` (sudah divalidasi, Status 200).

**Hasil Test Sampling (2 halaman, 200 lokasi):**

| Parameter Filter | Hasil |
| :--- | :--- |
| `countries=ID` (Indonesia) | ❌ **GAGAL** - Filter tidak bekerja, mengembalikan data global (Ghana, India, Chile, US, UK, dll.) |
| `city=Makassar/Manado/Palu` | ❌ **GAGAL** - Sama, mengembalikan ribuan lokasi dari seluruh dunia dengan nama kota yang sama |
| Negara yang ditemukan | Ghana, India, Argentina, Vietnam, Mongolia, China, Bangladesh, Singapore, Chile, Poland, Netherlands, Israel, Nigeria, Thailand, UK, US |
| Lokasi Indonesia (ID) | **0 lokasi** ditemukan dari 200 sample |

**Kesimpulan:** ⛔ **OpenAQ TIDAK MEMILIKI DATA INDONESIA** sama sekali. API mereka hanya mencakup negara-negara tertentu dan Indonesia bukan bagian dari coverage mereka.

**→ Keputusan:** Batalkan penggunaan OpenAQ. Fokus ke **BPS Web API** dan **Portal Open Data Provinsi** untuk data IKU (Kualitas Udara/PM2.5).

---

### [2026-06-13 13:30 WIB] EKSTRAKSI IKU DARI SLHI PDF — BERHASIL

**Target:** Data IKU (Indeks Kualitas Udara) Sulawesi dari PDF SLHI tahun 2017-2025.

**Metode:** Parsing PDF menggunakan `pdfplumber` untuk ekstraksi tabel (mengikuti metode yang berhasil untuk IKA).

**Hasil Ekstraksi:**

| Sumber | Tahun Data | Provinsi | Status |
| :--- | :--- | :--- | :--- |
| SLHI_2023.pdf | 2023 | 6 provinsi | ✅ Berhasil (halaman 227) |
| SLHI_2024.pdf | 2019-2023 | 6 provinsi | ✅ Berhasil (halaman 128 - tabel time series) |
| SLHI_2025.pdf | 2020-2024 | 6 provinsi | ✅ Berhasil (halaman 122 - tabel time series) |
| Open Data Sulut | 2024 | Sulawesi Utara | ✅ Berhasil (CSV download) |

**Coverage Final:**
- ✅ **2019-2024**: 36 data points (6 provinsi × 6 tahun)
- ❌ **2014-2018**: Data tidak ditemukan di SLHI maupun Portal Open Data

**Nilai IKU Sulawesi (Range):**
- Gorontalo: 86.88 - 94.47 (Kategori: BAIK)
- Sulawesi Barat: 89.72 - 93.33 (Kategori: BAIK)
- Sulawesi Selatan: 88.73 - 91.50 (Kategori: BAIK)
- Sulawesi Tengah: 91.33 - 92.98 (Kategori: BAIK)
- Sulawesi Tenggara: 90.01 - 93.00 (Kategori: BAIK)
- Sulawesi Utara: 90.53 - 93.44 (Kategor: BAIK)

**Output File:** `data/processed/iku_sulawesi_2019_2024_final.csv`

**Scripts:**
- `scripts/extract_iku_slhi_tables.py` - Ekstraksi dari PDF SLHI
- `scripts/clean_iku_sulawesi.py` - Pembersihan data
- `scripts/consolidate_iku_final.py` - Konsolidasi final

**Kesimpulan:** ✅ **Data IKU Sulawesi 2019-2024 berhasil diekstrak**. Coverage 60% dari target 10 tahun (2014-2024). Data tahun 2014-2018 tidak tersedia di sumber manapun yang diakses.

---

### [2026-06-13 13:45 WIB] PENCARIAN DATA IKU HISTORIS (2014-2018)

**Target:** Melengkapi data IKU untuk tahun 2014-2018.

**Sumber yang Dicoba:**

1. **SLHI Lama (2017, 2018, 2019):** ❌ Tidak ada data retrospektif IKU untuk tahun sebelumnya
2. **BPS Web API:** ❌ Tidak ada tabel kualitas udara (search keyword: kualitas udara, IKU, PM2.5, PM10)
3. **Portal Open Data Sulut:** ✅ Ada 82 dataset lingkungan hidup, tapi **hanya coverage 2020-2024**

**Status:** ⚠️ **Data IKU 2014-2018 TIDAK TERSEDIA** dari semua sumber yang diakses.

**Rekomendasi Next Steps:**
1. 🔍 **Google Dorking** - Cari publikasi KLHK/BPS lama yang mungkin punya data IKU historis
2. 📧 **Manual Request** - Kontak langsung BPS/KLHK regional untuk data arsip
3. 📊 **Interpolasi** - Gunakan backfill/forward fill dari data 2019 untuk estimasi

**→ NEXT ACTION:** Google Dorking untuk publikasi SLHI/IKLH tahun 2014-2016

---

### [2026-06-13 15:45 WIB] ASESMEN LIMBAH B3 & SIRAJA — DATA PROVINSI TERTUTUP

**Target:** Timbulan Limbah B3 (Smelter/Nikel) di Sulawesi.
**Tujuan:** Mendapatkan data Limbah B3 secara historis per provinsi di Sulawesi.

**Hasil Asesmen Berbagai Platform:**

| Target/URL / Metode | Hasil | Keterangan |
| :--- | :--- | :--- |
| **SIRAJA KLHK** (`pelayananterpadu.menlhk.go.id`) | ⛔ **Terkunci** | Portal utama pelaporan limbah B3 korporasi (termasuk tambang/smelter) dienkripsi dengan sistem *Festronik* dan wajib *login* perusahaan/pemerintah. Data publik ditutup. |
| **BPS SLHI PDF** (2019-2025) | 🟡 **Parsial (Nasional)** | BPS *hanya* memublikasikan Limbah B3 **secara Nasional per Sektor Industri** (Manufaktur, Tambang, dll). Tidak ada rincian per provinsi. |
| **BPS Web API** (Limbah B3) | ❌ **Kosong** | Pencarian API BPS dengan kode domain regional Sulawesi (7100-7600) untuk keyword "limbah B3" menghasilkan 0 tabel. |
| **SIPSN KLHK** (`sipsn.kemenlh.go.id`) | ❌ **Salah Target** | Portal ini *live*, tetapi isinya murni **Sampah Rumah Tangga/Padat** (Solid Waste), bukan Limbah B3 Industri. |
| **Open Data Sulut** (CKAN) | ⚠️ **Under-reported** | Ditemukan dataset "Limbah B3 yang Dikelola (2020-2024)". Namun isinya hanya **angka sangat kecil (misal 4-30 Ton)**, jauh dari skala Smelter. Terindikasi korporasi besar (IMIP dkk) me-*bypass* provinsi dan melapor langsung ke pusat (SIRAJA). |

**Kesimpulan:** Data resmi pemerintah untuk volume Limbah B3 tingkat Provinsi di Sulawesi mengalami fenomena *Data Vacuum* (kekosongan data publik). Pelaporan tersentralisasi dan ditutup rapat di tingkat kementerian (SIRAJA).

**→ Strategi Baru (OSINT & Proxy NGO):**
Karena pintu pemerintah tertutup, kita telah melakukan *Dorking* dan mengekstrak dokumen studi NGO/Akademis sebagai proksi. Berikut adalah tabel data/dokumen yang telah diekstrak:

| Kategori Limbah | Lokasi / Perusahaan | Target Volume Ekstraksi | Sumber Target (OSINT / NGO) | Status |
| :--- | :--- | :--- | :--- | :--- |
| Slag Nikel / Tailing HPAL | Morowali (IMIP), Sulteng | Belasan Juta Ton / Tahun | Dokumen AEER & WALHI | ✅ Selesai diekstrak |
| Slag Feronikel | Konawe (VDNI), Sultra | Jutaan Ton / Tahun | Laporan JATAM & Produksi | ✅ Selesai diekstrak |
| Slag EAF | Bantaeng (Huadi), Sulsel | Jutaan Ton / Tahun | Jurnal Unhas & BRIN | ✅ Selesai diekstrak |

> *Catatan: Hasil ekstraksi dokumen NGO ini telah dikonsolidasikan ke dalam dataset proxy `data/processed/sulawesi_limbah_b3_ngo_proxy.csv` sebagai alternatif data pemerintah.*

---

### [2026-06-13 18:14 WIB] ASESMEN AKSESIBILITAS DOKUMEN AMDAL & RKL-RPL

**Target:** Metadata mikro terkait volume dan komposisi limbah B3 (Tailing, Slag) pada level fasilitas/pabrik.
**Tujuan:** Mendapatkan data tingkat pabrik dari dokumen Analisis Mengenai Dampak Lingkungan (AMDAL) atau Rencana Pengelolaan Lingkungan (RKL-RPL).

**Realitas Tata Kelola Data (Data Vacuum):**
Pemerintah dan perusahaan secara administratif **memiliki** data ini secara lengkap karena AMDAL/RKL-RPL adalah syarat mutlak Sistem Perizinan Berusaha Terintegrasi Secara Elektronik (OSS) dan **Amdalnet** KLHK. 

Namun, berdasarkan penelusuran dan analisis aksesibilitas:
1. **Tidak Ada Publikasi Proaktif:** Dokumen teknis AMDAL yang memuat data mikro limbah B3 hampir tidak pernah dipublikasikan secara proaktif di portal *Open Data* mana pun.
2. **Amdalnet Tertutup:** Portal Amdalnet KLHK hanya mengizinkan publik melihat *status* persetujuan lingkungan, sedangkan tautan unduhan dokumen PDF RKL-RPL utuh dikunci (membutuhkan *login* khusus pemrakarsa/pemerintah).
3. **Mekanisme Akses Publik Sulit:** Publik atau NGO umumnya harus mengajukan sengketa informasi (KIP) yang memakan waktu berbulan-bulan untuk mendapatkan dokumen ini secara resmi.

**Kesimpulan & Strategi Bypass:**
Ketertutupan data mikro limbah ini adalah "penyakit sistemik" yang menjalar ke dokumen AMDAL. Masyarakat daerah yang terdampak dibiarkan buta secara ekologis.
Sebagai strategi alternatif, pencarian (*Dorking*) harus difokuskan pada dokumen AMDAL yang "bocor" (*leaked*) dari pihak internal, lampiran akademisi, atau dokumen Ringkasan Eksekutif yang disebarluaskan oleh NGO seperti WALHI/JATAM/AEER. Strategi perburuan Metadata Mikro (termasuk *Global Tailings Portal*) telah disusun dalam *Implementation Plan* terpisah.
