# Product Requirements Document (PRD) — FASE 1
## Studi Evaluasi D3TLH: Daya Dukung dan Daya Tampung Lingkungan Hidup
### "MELAMPAUI BATAS: Kegagalan Kebijakan D3TLH Dalam Mengendalikan Ekspansi Industri"

---

**Versi:** 2.0 (Step-by-Step Development Roadmap)  
**Pemilik Produk:** CELIOS Research Division  
**Referensi:** `docs/framework-fase1-d3tlh.md` | `refrensi/Ref/OUTLINE STUDI D3TLH.docx`  
**Status Data:** ⚠️ Belum dimulai — Menunggu eksekusi Checkpoint 1  

---

> [!IMPORTANT]
> ## 🚫 Kebijakan Data: No Mock Data — Pure Data Driven
> Setiap temuan, angka, dan Crosstab dalam riset ini **wajib didukung oleh sumber data resmi dan terverifikasi** (BPS, KLHK, ESDM, Kemenkes, KPA, YLBHI, pemberitaan, dll.). Tidak ada data simulasi.

---

## 🏗️ Roadmap Development Fase 1 (Checkpoints)

Pengembangan Fase 1 (Riset D3TLH) ini dipecah menjadi **9 Checkpoint**. Setiap Checkpoint merupakan satu *milestone* yang jelas, di mana Checkpoint 3 hingga 8 mewakili pengerjaan satu "Page" (Halaman Dashboard/Bab Laporan) khusus untuk menguji hipotesa tertentu melalui Crosstab.

### 🗄️ Tahap Fondasi
#### [ ] Checkpoint 1: Akuisisi Data Mentah (Data Fetching & OSINT Mining)
- **Target:** Mendapatkan seluruh dataset yang dibutuhkan untuk riset dengan pendekatan OSINT dan Web Scraping tingkat lanjut.
- **Strategi Akuisisi (The 3 Pillars):**
  1. **API Interception:** Penggunaan HTTP request langsung ke WebAPI (BPS) atau mengendus *hidden endpoint* (XHR/JSON) di balik *dashboard* interaktif pemerintah.
  2. **Stealth Scraping:** Penggunaan framework **Scrapling** (StealthyFetcher) untuk menembus portal web pemerintah (seperti ESDM/KLHK) yang diproteksi anti-bot/Cloudflare.
  3. **Deep PDF Parsing:** Penggunaan **Camelot** / **Tabula-py** untuk mengekstrak tabel data mentah secara presisi dari dalam Laporan Tahunan PDF milik NGO (KPA/YLBHI) yang tidak menyediakan *database* terbuka.
- **Blueprint Data Target & Prioritas Eksekusi:**

| Prioritas | Sumber Institusi | Tingkat Kesulitan | Target Portal Resmi | Alternatif OSINT / 3rd Party | Variabel Data yang Diambil | Rentang Waktu | Estimasi Volume Data | Metode Akuisisi (Tools) | Status Akses |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **#1** | **BPS** | Mudah 🟢 | `webapi.bps.go.id` | - | Persentase Keluhan Kesehatan Umum (Var 222) | 2016 - 2026 (1 Dekade) | ±380 baris | **API Client** (`requests`) | ✅ Gratis |
| **#1.5** | **Kemenkes** | Menengah 🟡 | Profil Kesehatan Indonesia (Pusdatin PDF) | - | Kasus ISPA, Penyakit Kulit, Gangguan Pernapasan | 2016 - 2026 (1 Dekade) | ±500 baris | **Camelot / Tabula-py** (PDF Parser) | ✅ Gratis |
| **#2** | **KPA / YLBHI** | Menengah 🟡 | `kpa.or.id` (Catatan Akhir Tahun KPA) | `putusan3.mahkamahagung.go.id`, `pasal.id`, `bhumi.atrbpn.go.id` | Jumlah Konflik Agraria, Luas Lahan Konflik, Kriminalisasi Warga | 2016 - 2026 (1 Dekade) | ±500 data poin | **Camelot** / **Scrapling** | ✅ Gratis |
| **#3** | **ESDM / BKPM** | Sulit 🟠 | `modi.esdm.go.id` / `nswi.bkpm.go.id` | `geoportal.esdm.go.id`, Geoportal One Map (BIG/KLHK) | Jumlah izin tambang/smelter, Kapasitas Produksi, Nilai Investasi, Luas Kawasan Industri | 2016 - 2026 (1 Dekade) | ±3.000+ entri | **Scrapling** (XHR Intercept) / Web Scraping | 🔴 Sebagian Beli / Request Formal ke BKPMD |
| **#3.5** | **BPS / Kemendag / Kemenkeu** | Menengah 🟡 | `bps.go.id` / `kemendag.go.id` / `djpk.kemenkeu.go.id` | - | Nilai Ekspor per Sektor, PAD per Kabupaten/Kota Sulawesi | 2016 - 2026 (1 Dekade) | ±300 baris | **API Client / Scrapling** | ✅ Gratis |
| **#4** | **KLHK** | Paling Sulit 🔴 | `sipsn.menlhk.go.id` / PROPER | `openaq.org` (Air Quality), NASA FIRMS (Emisi/Api) | Indeks Kualitas Air, Laju Deforestasi, Data Limbah B3, Kualitas Udara (PM2.5) | 2016 - 2026 (1 Dekade) | ±400 baris | **Scrapling / API OpenAQ** | ⚠️ Bisa Bayar (jika butuh data BMKG lengkap) |
| **#5** | **Portal Berita / Media** | Menengah 🟡 | - | OSINT (Google Dorks, DuckDuckGo, Mongabay, dll.) | Berita Kasus/Anomali (Kerusakan Lingkungan, Konflik, Kriminalisasi, Krisis Air) di Sulawesi | 2016 - 2026 (1 Dekade) | ±100 kasus | **Scrapling** / **DuckDuckGo API** | ⚠️ Bisa Bayar (Google CSE API) |

> **Keterangan Variabel BPS:**  
> \**Di dalam sistem BPS, penyakit spesifik seperti ISPA dan Penyakit Kulit tidak memiliki ID Variabel sendiri, melainkan tergabung sebagai sub-item di dalam keranjang variabel induk:*  
> *- **Var 42**: "Jumlah Kasus Penyakit" (Memuat data ISPA, Pneumonia/Gangguan Napas, Diare, dll).*  
> *- **Var 222**: "Keluhan Kesehatan" (Memuat persentase keluhan demam, batuk, penyakit kulit).*

- **Output:** Semua file PDF, file JSON hasil intercept, dan CSV kasar tersimpan rapi di folder `data/raw/`.

**📝 Log Eksekusi & History (Checkpoint 1):**

* **[04 Juni 2026] BPS API (Prioritas #1) - Percobaan 1 (Data Kesehatan):**
  - ✅ **SUKSES:** Kunci API BPS valid. Skrip awal `fetch_bps_d3tlh.py` sempat mengalami *error* untuk indikator Kesehatan (Var ID 42 & 222) karena parameter tahun mentah (2014-2024).
  - ✅ **REVISI SUKSES (BYPASS):** Setelah misteri ID Tahun (th/114) terpecahkan, data Kesehatan ternyata **TERSEDIA** dan merespons dengan status "OK". 
  - 🔄 **UPDATE STRATEGI 1:** Pembatalan teknik PDF Parser Kemenkes. Seluruh data kesehatan (ISPA, Penyakit Kulit, dll) **resmi diambil kembali menggunakan BPS API** melalui script terpisah: `data/fetch_bps_kesehatan.py`.

* **[04 Juni 2026] Scraping Berita & Pelacakan Aktor (Prioritas Baru):**
  - ✅ **UPDATE STRATEGI:** Membatalkan target PDRB BPS dan mengalihkan fokus riset ke penelusuran aktor (50 Orang Terkaya) di industri pengolahan alam Sulawesi, serta melakukan *scraping* berita terkait kasus/peristiwa anomali di lapangan. Pendekatan murni berfokus pada investasi, ekspor, dan pencemaran riil.

* **[04 Juni 2026] BPS API (Prioritas #1) - Percobaan 8 (Evaluasi Data Kesehatan):**
  - ⚠️ **KENDALA DATA:** Setelah script `fetch_bps_kesehatan.py` (Domain 0000) dijalankan, ditemukan bahwa BPS hanya merekap *Var 42 (Jumlah Kasus Penyakit)* hingga tahun **2015**. Data tahun 2016-2024 tidak tersedia. Selain itu, penyakit ISPA dan Penyakit Kulit tidak ada di rincian.
  - 🔄 **STRATEGI HYBRID (KEPUTUSAN FINAL):** Atas instruksi user, riset akan menggunakan strategi Hybrid Makro-Mikro untuk Kesehatan:
    1. **Maksimalkan BPS (Makro):** Script `fetch_bps_kesehatan.py` yang baru diubah untuk mengambil **Persentase Keluhan Kesehatan Umum (Var 222)** yang datanya *full* 10 tahun (2014-2024). Ini berguna untuk membuktikan korelasi makro penurunan daya dukung lingkungan.
    2. **PDF Parser Kemenkes (Mikro):** Untuk indikator mikro spesifik **ISPA & Penyakit Kulit**, akan diekstrak menggunakan teknik PDF Parsing dari Laporan Profil Kesehatan Indonesia.
  - 💾 **BACKUP (BAK):** Tabel hasil ekstraksi penyakit terperinci (Var 42) dari tahun 2014-2015 yang disukai user tetap disimpan sebagai arsip di `data/raw/BAK_bps_kesehatan_provinsi_2014_2015.csv`, dan script aslinya diarsipkan sebagai `data/BAK_fetch_bps_kesehatan.py`.

* **[04 Juni 2026] KPA / YLBHI (Prioritas #2) - Tahap 1 (Akuisisi PDF):**
  - 🔍 **PROSES:** Mulai menelusuri ketersediaan laporan tahunan KPA (Konsorsium Pembaruan Agraria) dan YLBHI terkait Konflik Agraria periode 2014-2024.
  - ⚠️ **STATUS AWAL:** Laporan PDF tidak ditemukan di *local repository* (`refrensi/`).
  - 🔄 **TINDAKAN:** Menginisiasi pencarian terbuka (Web Search OSINT) di internet untuk mengunduh arsip digital "Catatan Akhir Tahun KPA" secara terstruktur.

* **[08 Juni 2026] Evaluasi Outline & Realignment Target (Koreksi Fatal):**
  - ⚠️ **KENDALA PEMAHAMAN:** Terdapat bias asumsi dari AI yang memasukkan "PDRB (Produk Domestik Regional Bruto) 38 Provinsi" ke dalam kerangka kerja, meskipun variabel ini sama sekali tidak pernah diminta oleh tim riset CELIOS di dalam `OUTLINE STUDI D3TLH.docx`. AI membuang-buang waktu mencoba memetakan API BPS untuk PDRB.
  - ✅ **REVISI SUKSES (BIMBINGAN USER):** User meluruskan kesalahpahaman ini dengan memberikan dokumen `OUTLINE STUDI D3TLH WITH COMMENT.pdf`. Isi outline secara *letterlijk* sudah sangat jelas — tidak ada PDRB. Indikator ekonomi yang benar di Bab VIII (Distribusi Manfaat vs Beban) adalah:
    - **Sisi Manfaat:** Investasi, Ekspor, PAD.
    - **Sisi Biaya:** Kesehatan, Konflik, Pencemaran.
  - 🔄 **KEPUTUSAN FINAL:** Melakukan pembersihan dokumen Framework dan PRD untuk membuang semua improvisasi terkait PDRB BPS dan klaim variabel yang tidak ada di outline. Seluruh *blueprint* dikembalikan 100% ke indikator yang tertulis di outline resmi.

* **[09 Juni 2026] BPS API (Prioritas #3.5) - Eksplorasi PAD, Ekspor, dan Investasi:**
  - 🔍 **TEMUAN KRUSIAL (PAD):** Setelah ekskavasi mendalam terhadap seluruh Var ID dan Domain BPS, dikonfirmasi bahwa **API BPS TIDAK menyediakan data PAD per Kabupaten/Kota**. Var 787 di domain Nasional hanya tersedia sebagai agregat 14 kategori akuntansi (Pendapatan Daerah, PAD, Dana Perimbangan, dll.) untuk seluruh Indonesia — tanpa breakdown per wilayah. Var ID yang sama di domain Provinsi/Kabupaten mengacu ke variabel berbeda (misal: Var 787 di domain 7100 = "Akses Internet", bukan PAD).
  - ⚠️ **LIMITASI EKSPOR:** Seluruh range Var ID BPS yang dicek (1–2500) **tidak memiliki data Ekspor dengan breakdown per Provinsi**. Static Table BPS Sulsel pun hanya tersedia hingga tahun 2013. Data Ekspor per Provinsi untuk 2016–2026 **tidak dapat diakses via BPS API**.
  - ✅ **DATASET BERHASIL DIPEROLEH (INVESTASI PMDN):** Ditemukan VAR 793 & 794 = *Realisasi Investasi PMDN per Provinsi*. Berhasil diekstrak untuk 6 Provinsi Sulawesi rentang 2016–2026. File tersimpan di `data/raw/bps_investasi_pmdn_sulawesi_2016_2026.csv` (**96 baris**).
  - 🗺️ **RENCANA SUMBER ALTERNATIF:**
    - **PAD per Kab/Kota:** Sumber resmi → **DJPK Kemenkeu** (djpk.kemenkeu.go.id) yang mempublikasikan realisasi APBD per Kab/Kota secara tahunan.
    - **Ekspor per Sektor/Provinsi:** Sumber resmi → **BPS Ekspor Static Table** (per komoditas) atau **Kemendag/UNCTAD** yang memiliki API perdagangan internasional.

* **[09 Juni 2026] BPS Website (Prioritas #3.5) - Percobaan Scraping Otomatis PAD & Ekspor:**
  - 🎯 **TARGET:** Mengakuisisi data PAD per Kabupaten/Kota dan Ekspor Nasional melalui web scraping otomatis dari website BPS.
  - **PERCOBAAN 1 - PLAYWRIGHT (Browser Automation):**
    - ⚠️ **KENDALA:** Website BPS Provinsi (Query Builder) menggunakan **Cloudflare Turnstile** anti-bot protection yang memblokir Playwright dan Selenium.
    - ❌ **HASIL:** Scraping gagal, mendapat HTTP 403 Forbidden.
  - **PERCOBAAN 2 - SCRAPLING STEALTHYFETCHER:**
    - 🔧 **METODE:** Menggunakan StealthyFetcher dengan browser fingerprint bypass untuk menembus Cloudflare.
    - ⚠️ **KENDALA:** Form BPS Query Builder sangat bergantung pada JavaScript async (AJAX). Data dropdown dan tabel dimuat setelah page load, membuat timing scraping menjadi sangat kompleks.
    - ⚠️ **HASIL PARSIAL:** Berhasil bypass Cloudflare, namun form tidak terisi dengan benar karena masalah timing JavaScript.
  - **PERCOBAAN 3 - BPS API DEEP SEARCH:**
    - 🔧 **METODE:** Menggunakan tools `bps_client.py` dan `deep_search.py` untuk mencari table metadata PAD di 30,613 tabel BPS.
    - ❌ **HASIL:** 0 tabel ditemukan untuk PAD Sulawesi (kode provinsi 7100-7600). Mayoritas table listing mengembalikan response `"list-not-available"`.
  - 🔄 **KEPUTUSAN FINAL (USER APPROVED):** Menggunakan strategi **MANUAL DOWNLOAD + AUTOMATED PROCESSING**:
    1. User download data manual via browser (bypass Cloudflare naturally)
    2. Script otomatis untuk cleaning, consolidation, dan processing
    3. Total waktu efektif: ~2 jam (manual) vs berhari-hari troubleshooting scraping

* **[09 Juni 2026] Dokumentasi Panduan Manual Download (Prioritas #3.5):**
  - ✅ **DELIVERABLE 1 - PAD Data (6 Provinsi Sulawesi):**
    - 📄 **Panduan:** `docs/PANDUAN_DOWNLOAD_MANUAL_PAD.md` (2,500+ kata, form field lengkap)
    - 🎯 **Target:** Query Builder BPS per Provinsi (sulut/sulteng/sulsel/sultra/gorontalo/sulbar.bps.go.id)
    - 📊 **Data:** Realisasi Pendapatan Asli Daerah (PAD) per Kabupaten/Kota, 2016-2024
    - ⏱️ **Estimasi:** 45-60 menit untuk 6 provinsi
    - 📁 **Output Folder:** `tools/scrapling/bps_eksporpad/downloads/`
    - ✅ **Script Processing:** `process_pad_downloads.py` (siap merge 6 CSV → 1 consolidated file)
  - ✅ **DELIVERABLE 2 - Ekspor Nasional:**
    - 📄 **Panduan:** `docs/PANDUAN_DOWNLOAD_EKSPOR_NASIONAL.md` (3,000+ kata, batch download strategy)
    - 🎯 **Target:** BPS Exim Portal (bps.go.id/id/exim)
    - 📊 **Data:** 
      - Ekspor per Sektor (HS 2 Digit): 10 kode prioritas + 10 kode sekunder
      - Ekspor per Pelabuhan: 6 pelabuhan Sulawesi
      - Ekspor per Negara: 10 negara Asia trading partners
    - ⚠️ **CONSTRAINT DISCOVERY:** 
      - Max 5 tahun per download → Perlu BATCH 1 (2016-2020) & BATCH 2 (2021-2024)
      - Kode HS WAJIB dipilih spesifik (tidak bisa kosong/select all)
      - Max 10-15 kode HS/pelabuhan/negara per download
    - 📁 **Total Downloads:** 6-8 files (mandatory + optional)
    - ⏱️ **Estimasi:** 45-75 menit
    - 📁 **Output Folder:** `tools/bpsapi/output/ekspor/`
    - ✅ **Script Processing:** `process_ekspor_downloads.py` (akan merge batch files per dataset)
  - ✅ **DELIVERABLE 3 - Dokumen Pendukung:**
    - 📄 `CHECKLIST_DOWNLOAD_BPS.md` - Printable checklist dengan data check boxes
    - 📄 `QUICK_REFERENCE_BPS.md` - Reference card ringkas
    - 📄 `BPS_DATA_COLLECTION_SUMMARY.md` - Executive summary & technical details
  - ✅ **TECHNICAL DOCUMENTATION:**
    - 📄 `tools/bpsapi/DATA_AVAILABILITY_REPORT.md` - Laporan lengkap API limitations
    - 📄 `tools/bpsapi/FINAL_RECOMMENDATION.md` - Justifikasi manual download approach
  - 💡 **LESSONS LEARNED:**
    1. Cloudflare Turnstile tidak bisa di-bypass fully dengan automated tools
    2. JavaScript-heavy forms dengan async loading sangat sulit di-scrape
    3. BPS API metadata incomplete (30,613 tables listed, mayoritas not available)
    4. Manual + automation hybrid lebih efisien untuk one-time data collection
    5. Good documentation saves more time than perfect automation

* **[09 Juni 2026] STATUS AKHIR DATA EKONOMI (Prioritas #3.5):**
  - ✅ **INVESTASI PMDN:** Berhasil via BPS API (96 rows, 2016-2026)
  - ⏳ **PAD:** Menunggu manual download (6 files, estimasi 1 jam)
  - ⏳ **EKSPOR:** Menunggu manual download (6-8 files, estimasi 1 jam)
  - 📋 **NEXT ACTION:** User execute manual download → Run processing scripts → Lanjut Checkpoint 2

#### [ ] Checkpoint 2: Data Structuring (`prepare_data.py`)

- **Target:** Menyatukan data mentah menjadi Master Dataset.
- **Tugas:** Menulis script pembersihan, standarisasi nama provinsi/kabupaten, dan penggabungan indikator.
- **Output:** File `data/processed/d3tlh_master.csv` (Cross-section & Time-series).

---

### 📊 Tahap Analisis (Pembuatan Page/Bab)

Sesuai dengan `OUTLINE STUDI D3TLH.docx`, analisis dibagi menjadi **8 Page/Bab Utama** (1 banding 1 tanpa improvisasi).

#### [ ] Checkpoint 3: Page 1 — Ekspansi Industri dan Intensifikasi Ruang
- **Fokus Pembahasan:** Membaca pola pertumbuhan industri sebagai sumber tekanan utama.
- **Pengujian Crosstab:**
  1. *Jumlah Izin* vs *Tahun* ➔ (Tren pertumbuhan)
  2. *Jumlah Smelter* vs *Luas Lahan* ➔ (Intensifikasi ruang)
  3. *Investasi* vs *Jumlah Izin* ➔ (Pola ekspansi ekonomi)

#### [ ] Checkpoint 4: Page 2 — Penurunan Kualitas Lingkungan & Tekanan Ekologis
- **Fokus Pembahasan:** Menguji apakah pertumbuhan industri diikuti penurunan kualitas lingkungan.
- **Pengujian Crosstab:**
  1. *Jumlah Smelter* vs *Kualitas Air* ➔ (Dampak terhadap air)
  2. *PLTU Captive* vs *Kualitas Udara* ➔ (Dampak emisi)
  3. *Luas Industri* vs *Deforestasi* ➔ (Tekanan ruang)

#### [ ] Checkpoint 5: Page 3 — Beban Kesehatan dan Dampak Sosial
- **Fokus Pembahasan:** Membaca dampak sosial yang selama ini tidak diperhitungkan dalam D3TLH.
- **Pengujian Crosstab (Before-After):**
  1. *Ekspansi Industri* vs *ISPA*, *Penyakit Kulit*, dan *Gangguan Napas*.

#### [ ] Checkpoint 6: Page 4 — Konflik Sosial dan Resistensi Masyarakat
- **Fokus Pembahasan:** Menguji apakah industrialisasi menghasilkan eskalasi konflik sosial.
- **Pengujian Crosstab:**
  1. *Periode Ekspansi* vs *Konflik Agraria* dan *Kriminalisasi*.

#### [ ] Checkpoint 7: Page 5 — Pola Penerbitan Izin Setelah Tekanan Ekologis Meningkat
- **Fokus Pembahasan:** Menguji apakah negara tetap menerbitkan izin meski indikator lingkungan memburuk.
- **Pengujian Crosstab:**
  1. *Status Ekologis (Normal/Tertekan/Kritis)* vs *Jumlah Izin Baru*.

#### [ ] Checkpoint 8: Page 6 — Audit Metodologi D3TLH (Blind Spots)
- **Fokus Pembahasan:** Menguji *blind spots* dalam metodologi D3TLH (Apa yang diukur vs hilang).
- **Pengujian Crosstab:**
  1. *Indikator D3TLH* vs *Dampak Nyata (Air ➔ Penyakit, Limbah ➔ Konflik, Emisi ➔ Displacement)*.

#### [ ] Checkpoint 9: Page 7 — Kegagalan Tata Kelola D3TLH
- **Fokus Pembahasan:** Membaca hubungan antara status D3TLH dan keputusan izin yang diterbitkan.
- **Pengujian Crosstab:**
  1. *Status Daya Dukung (Aman/Tertekan/Kritis)* vs *Keputusan Izin Keluar*.

#### [ ] Checkpoint 10: Page 8 — Distribusi Manfaat dan Beban Ekologis
- **Fokus Pembahasan:** Membaca ketimpangan distribusi (siapa untung, siapa rugi) dengan melacak Aktor/Korporasi yang beroperasi di Sulawesi.
- **Pengujian Crosstab:**
  1. *Manfaat Ekonomi (Investasi/Ekspor/PAD & 50 Aktor Terkaya)* vs *Beban Ekologis (Penyakit/Pencemaran/Konflik di Sulawesi)*.

---

### 📝 Tahap Finalisasi
#### [ ] Checkpoint 11: Kompilasi Laporan & Diseminasi
- **Target:** Menyusun temuan dari Checkpoint 3–10 menjadi Laporan Riset Final yang komprehensif.
- **Output:** Dokumen `.docx` dan `.md` siap rilis untuk publikasi dan landasan bagi Fase 2.

---

> [!NOTE]
> ## 📖 Ekstraksi PageIndex (Świąder 2020)
> Dokumen ini telah divalidasi dan diperbarui berdasarkan ekstraksi hierarki mendalam oleh PageIndex. Temuan metodologis kunci yang harus diintegrasikan ke dalam analisis:
> 1. **Komposisi Defisit Ekologis (Carbon Footprint)**: Secara empiris, penyumbang terbesar adalah **Listrik (66,6%)**, **Mobilitas (16,8%)**, dan **Pangan (6,4%)**. 
> 2. **Ketimpangan Spasial (Urban vs Rural)**: Pusat populasi/industri padat menyumbang **75% dari total defisit ekologis**.
> 3. **Mitigasi Tata Ruang**: Pelarangan alih fungsi **lahan pertanian (*good-quality soils*)** adalah variabel mitigasi terkuat.
> 4. **Radius Defisit**: Defisit ekologis menyebar secara radius (mendobrak batas administratif). Cross-tabulasi spasial harus mempertimbangkan dampak ke provinsi/kabupaten tetangga.
