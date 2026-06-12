# Product Requirements Document (PRD)
## CELIOS Environmental Carrying Capacity Intelligence System (ECCIS)
### Dashboard Interaktif Daya Dukung Lingkungan Hidup Indonesia

---

**Versi:** 1.0  
**Tanggal:** Mei 2026  
**Status:** Draft — Menunggu Persetujuan Tim  
**Pemilik Produk:** CELIOS Research Division  
**Referensi Teknis:** `docs/framework-riset-ecc.md` | `docs/paper-fondasi-ecc-swiader2020.md`

---

## Daftar Isi

1. [Latar Belakang & Konteks](#1-latar-belakang--konteks)
2. [Pernyataan Masalah](#2-pernyataan-masalah)
3. [Tujuan Produk](#3-tujuan-produk)
4. [Pengguna & Pemangku Kepentingan](#4-pengguna--pemangku-kepentingan)
5. [Fitur Utama & Persyaratan](#5-fitur-utama--persyaratan)
6. [Narasi Pengguna (User Stories)](#6-narasi-pengguna-user-stories)
7. [Alur Penggunaan](#7-alur-penggunaan)
8. [Indikator Keberhasilan](#8-indikator-keberhasilan)
9. [Keterbatasan & Asumsi](#9-keterbatasan--asumsi)
10. [Glosarium](#10-glosarium)

---

## 1. Latar Belakang & Konteks

### 1.1 Konteks Kebijakan

Indonesia menghadapi tekanan ekologis yang meningkat seiring pertumbuhan penduduk, urbanisasi, dan
industrialisasi. Peraturan Pemerintah No. 22 Tahun 2021 mewajibkan penilaian **Daya Dukung dan Daya
Tampung Lingkungan Hidup (DDDTLH)** sebagai dasar perencanaan tata ruang dan kebijakan pembangunan.

Namun, hingga kini **belum ada satu platform terpadu** yang menyajikan data daya dukung lingkungan
secara komprehensif, terukur, dan dapat diakses publik di tingkat provinsi seluruh Indonesia.

### 1.2 Kesenjangan yang Ada

| Kondisi Saat Ini | Yang Dibutuhkan |
|------------------|-----------------|
| Data lingkungan tersebar di puluhan instansi (BPS, KLHK, PLN, BNPB) | Satu platform terintegrasi |
| Laporan DDDTLH hanya tersedia dalam format PDF statis | Visualisasi interaktif & mudah diakses |
| Tidak ada metrik standar yang membandingkan antar provinsi | Indeks terstandar & komparatif |
| Advokasi kebijakan bergantung pada data anekdotal | Bukti kuantitatif berbasis metodologi ilmiah |
| Publik tidak memiliki akses terhadap posisi ekologis daerahnya | Dashboard terbuka & komunikatif |

### 1.3 Landasan Ilmiah

Metodologi utama diadaptasi dari **Świąder et al. (2020)** — studi Environmental Carrying Capacity
Assessment yang telah diterapkan di level munisipal Eropa, diadaptasi untuk konteks 38 provinsi Indonesia
dengan sumber data lokal (BPS, PLN, KLHK, ESDM, BNPB).

---

## 2. Pernyataan Masalah

> **Pemerintah daerah, peneliti, dan masyarakat sipil di Indonesia tidak memiliki akses terhadap
> informasi yang terstandar, terukur, dan mudah dipahami mengenai seberapa besar tekanan aktivitas
> manusia terhadap kemampuan alam setiap provinsi untuk memulihkan dirinya.**

Akibatnya:
- Kebijakan pembangunan dirumuskan tanpa mempertimbangkan batas ekologis wilayah
- Advokasi lingkungan kesulitan membuktikan urgensi dengan data kuantitatif
- Ketimpangan ekologis antar wilayah tidak terlihat dan tidak terukur
- Perusahaan besar tidak memiliki tolok ukur dampak operasional terhadap daya dukung lokal

---

## 3. Tujuan Produk

### 3.1 Tujuan Utama

Membangun **dashboard riset interaktif berbasis web** yang menghitung, memvisualisasikan, dan
mengkomunikasikan status daya dukung lingkungan hidup seluruh 38 provinsi Indonesia — dinyatakan
melalui perbandingan antara **jejak karbon total (Carbon Footprint)** dan
**kemampuan pulih alam (Biocapacity)**.

### 3.2 Tujuan Spesifik

| # | Tujuan | Indikator Tercapai |
|---|--------|-------------------|
| T-01 | Mengukur jejak karbon 7 sektor aktivitas per provinsi | 38 provinsi × 7 sektor terhitung |
| T-02 | Mengukur biokapasitas lahan per provinsi | 38 provinsi × 4 tipe lahan terhitung |
| T-03 | Mengidentifikasi provinsi dalam kondisi defisit ekologis | Peta status defisit/cadangan tersedia |
| T-04 | Menyusun Indeks Kerentanan Lingkungan (IKL) komposit | Ranking IKL 38 provinsi tersedia |
| T-05 | Menyediakan basis bukti untuk advokasi kebijakan | Policy brief dapat diekspor dari dashboard |
| T-06 | Mendokumentasikan metodologi secara transparan | Halaman dokumentasi riset tersedia publik |

### 3.3 Yang Bukan Tujuan Produk Ini

- ❌ Bukan sistem peringatan dini bencana (itu domain BNPB)
- ❌ Bukan platform GIS/pemetaan wilayah secara detail
- ❌ Bukan sistem real-time (data diperbarui tahunan)
- ❌ Bukan aplikasi mobile
- ❌ Bukan sistem manajemen database lembaga pemerintah

---

## 4. Pengguna & Pemangku Kepentingan

### 4.1 Pengguna Utama (Primary Users)

| Segmen | Peran | Kebutuhan Utama |
|--------|-------|-----------------|
| **Peneliti & Akademisi** | Mengakses metodologi dan data untuk sitasi | Data dapat diunduh, metodologi transparan, referensi ilmiah tersedia |
| **Analis Kebijakan CELIOS** | Menghasilkan temuan riset untuk publikasi | Visualisasi siap presentasi, narasi otomatis, ekspor data |
| **Jurnalis & Media** | Meliput isu lingkungan berbasis data | Angka mudah dibaca, infografis siap pakai, fakta terverifikasi |

### 4.2 Pengguna Sekunder (Secondary Users)

| Segmen | Peran | Kebutuhan Utama |
|--------|-------|-----------------|
| **Pejabat Pemerintah Daerah** | Memahami posisi ekologis provinsinya | Perbandingan antar provinsi, rekomendasi tindakan |
| **LSM & Advokat Lingkungan** | Basis data untuk kampanye dan advokasi | Bukti kuantitatif defisit ekologis, grafik siap pakai |
| **Perusahaan (ESG/CSR)** | Menilai dampak operasional terhadap lingkungan | Scorecard per wilayah operasi, indeks kerentanan |
| **Mahasiswa & Publik Umum** | Belajar tentang kondisi lingkungan Indonesia | Tampilan sederhana, penjelasan konsep, infografis |

### 4.3 Pemangku Kepentingan (Stakeholders)

- **CELIOS** — pemilik produk dan pemberi mandat riset
- **KLHK** — sumber data utama dan pemangku kebijakan
- **BPS** — penyedia data statistik nasional
- **PLN & ESDM** — sumber data energi
- **Komunitas ilmiah** — validasi metodologi

---

## 5. Fitur Utama & Persyaratan

### Modul A — Beranda & Ringkasan Nasional

**Deskripsi:** Halaman pertama yang dilihat pengunjung. Menampilkan kondisi daya dukung lingkungan
Indonesia secara keseluruhan dalam format yang langsung dapat dipahami.

**Persyaratan Fungsional:**

| Kode | Fitur | Prioritas |
|------|-------|-----------|
| A-01 | Tampilkan total jejak karbon nasional (tCO₂ equivalen) | 🔴 Wajib |
| A-02 | Tampilkan total biokapasitas nasional (global hectare) | 🔴 Wajib |
| A-03 | Tampilkan status ECC nasional: Defisit / Cadangan | 🔴 Wajib |
| A-04 | Tampilkan "Jumlah Bumi" — berapa bumi yang dibutuhkan jika semua penduduk hidup seperti rata-rata Indonesia | 🔴 Wajib |
| A-05 | Tampilkan perubahan tahun ke tahun (pertumbuhan CF & BC) | 🟡 Penting |
| A-06 | Ringkasan: berapa provinsi dalam kondisi defisit vs cadangan | 🔴 Wajib |
| A-07 | Pilihan bahasa: Bahasa Indonesia / English | 🟡 Penting |
| A-08 | Navigasi sidebar ke semua modul | 🔴 Wajib |

---

### Modul B — Overview Nasional (Halaman 1)

**Deskripsi:** Gambaran komparatif CF vs BC seluruh 38 provinsi dalam satu tampilan.

| Kode | Fitur | Prioritas |
|------|-------|-----------|
| B-01 | Grafik batang CF vs BC per provinsi (dapat diurutkan) | 🔴 Wajib |
| B-02 | Peta choropleth Indonesia — warna berdasarkan status ECC | 🔴 Wajib |
| B-03 | Tabel ringkasan dengan filter dan pencarian provinsi | 🔴 Wajib |
| B-04 | Highlight 5 provinsi defisit terbesar & 5 cadangan terbesar | 🟡 Penting |
| B-05 | Ekspor data tabel ke format CSV | 🟢 Tambahan |

---

### Modul C — Jejak Karbon Sektoral (Halaman 2)

**Deskripsi:** Menjawab pertanyaan: *Sektor aktivitas apa yang paling besar menyumbang tekanan
ekologis per provinsi?*

| Kode | Fitur | Prioritas |
|------|-------|-----------|
| C-01 | Grafik batang bertumpuk (stacked bar) — kontribusi 7 sektor per provinsi | 🔴 Wajib |
| C-02 | Peta gelembung (bubble map) — ukuran = total CF, warna = sektor dominan | 🔴 Wajib |
| C-03 | Filter pemilihan sektor untuk highlight | 🟡 Penting |
| C-04 | Perbandingan sektor: provinsi kepulauan vs daratan besar | 🟡 Penting |
| C-05 | Hasil uji statistik asosiasi sektor vs status ECC (dapat disembunyikan) | 🟢 Tambahan |
| C-06 | Penjelasan singkat metodologi per sektor | 🔴 Wajib |

**7 Sektor yang Diukur:**
Ketahanan Pangan · Sanitasi · Pengelolaan Sampah · Konsumsi Air · Energi Listrik · Gas LPG · Transportasi

---

### Modul D — Defisit Ekologis (Halaman 3)

**Deskripsi:** Menjawab: *Seberapa besar kesenjangan antara daya dukung alam dan beban aktivitas
manusia di setiap provinsi?*

| Kode | Fitur | Prioritas |
|------|-------|-----------|
| D-01 | Grafik scatter CF (sumbu X) vs BC (sumbu Y) — garis diagonal = titik seimbang | 🔴 Wajib |
| D-02 | Grafik gap defisit/cadangan — diurutkan dari terbesar | 🔴 Wajib |
| D-03 | Indikator efisiensi ekologis per provinsi (%) | 🟡 Penting |
| D-04 | Simulasi skenario: jika populasi tumbuh X%, bagaimana status ECC berubah? | 🟢 Tambahan |
| D-05 | Highlight wilayah yang mendekati titik kritis (rasio ECC > 0.8) | 🟡 Penting |

---

### Modul E — Indeks Kerentanan Lingkungan / IKL (Halaman 4)

**Deskripsi:** Menjawab: *Provinsi mana yang paling rentan secara ekologis — mempertimbangkan
tidak hanya defisit, tetapi juga kemiskinan, kepadatan, dan ketimpangan?*

| Kode | Fitur | Prioritas |
|------|-------|-----------|
| E-01 | Ranking IKL 38 provinsi (komposit 6 indikator) | 🔴 Wajib |
| E-02 | Grafik radar per provinsi — profil 6 dimensi kerentanan | 🔴 Wajib |
| E-03 | Peta IKL — gradasi warna kerentanan rendah-tinggi | 🔴 Wajib |
| E-04 | Slider bobot indikator — pengguna dapat menyesuaikan bobot | 🟡 Penting |
| E-05 | Penjelasan setiap dimensi kerentanan dalam bahasa awam | 🔴 Wajib |
| E-06 | Korelasi IKL dengan IPM dan PDRB | 🟢 Tambahan |

**6 Dimensi IKL:**
Rasio ECC · Defisit per Kapita · Ketersediaan Lahan Hijau · Kepadatan Penduduk · Indeks Pembangunan Manusia · Ketimpangan (Gini)

---

### Modul F — Eksplorasi Data (Halaman 5)

**Deskripsi:** Antarmuka eksplorasi data terbuka bagi pengguna yang ingin menggali lebih dalam.

| Kode | Fitur | Prioritas |
|------|-------|-----------|
| F-01 | Tabel data lengkap 38 provinsi dengan semua variabel | 🔴 Wajib |
| F-02 | Filter multi-kolom (wilayah, status ECC, rentang nilai) | 🔴 Wajib |
| F-03 | Tampilan grafik untuk setiap kolom yang dipilih | 🟡 Penting |
| F-04 | Unduhan CSV dataset lengkap | 🟡 Penting |
| F-05 | Metadata setiap variabel (definisi, satuan, sumber) | 🟡 Penting |

---

### Modul G — Dokumentasi Riset (Halaman 6)

**Deskripsi:** Transparansi metodologi — menampilkan seluruh dokumen riset dalam format yang mudah
dibaca di dalam dashboard.

| Kode | Fitur | Prioritas |
|------|-------|-----------|
| G-01 | Daftar dokumen riset yang dapat dipilih (dropdown) | 🔴 Wajib |
| G-02 | Render dokumen markdown langsung di dashboard | 🔴 Wajib |
| G-03 | Tombol unduhan dokumen (PDF/MD) | 🟡 Penting |
| G-04 | Tag metadata dokumen (topik, tanggal, penulis) | 🟢 Tambahan |

**Dokumen yang tersedia:**
- Framework Riset ECC (dokumen ini)
- Ringkasan Paper Metodologi Świąder et al. (2020)
- Panduan Interpretasi Indeks ECC
- Catatan Data & Sumber

---

### Modul H — Validasi Metode (Halaman 7)

**Deskripsi:** Membuktikan relevansi metodologi dengan literatur ilmiah yang ada.

| Kode | Fitur | Prioritas |
|------|-------|-----------|
| H-01 | Daftar paper ilmiah relevan yang ditemukan secara otomatis | 🟡 Penting |
| H-02 | Skor relevansi setiap paper terhadap metodologi ECC | 🟡 Penting |
| H-03 | Filter berdasarkan tahun, jurnal, dan topik | 🟢 Tambahan |

---

### Modul I — Penemuan Bibliometrik (Halaman 8)

**Deskripsi:** Memetakan lanskap ilmiah ECC di Indonesia dan Asia Tenggara.

| Kode | Fitur | Prioritas |
|------|-------|-----------|
| I-01 | Visualisasi metode analisis yang paling sering digunakan dalam riset ECC | 🟡 Penting |
| I-02 | Peta jaringan kata kunci (keyword network) | 🟢 Tambahan |
| I-03 | Tren publikasi ECC dari waktu ke waktu | 🟢 Tambahan |

---

### Modul J — Visualisasi Multidimensi (Halaman 9)

**Deskripsi:** Eksplorasi hubungan antar variabel ECC secara bersamaan melalui visualisasi lanjutan.

| Kode | Fitur | Prioritas |
|------|-------|-----------|
| J-01 | Grafik koordinat paralel (parallel coordinates) — semua dimensi ECC sekaligus | 🟡 Penting |
| J-02 | Interaktif: pengguna dapat memfilter rentang nilai per dimensi | 🟡 Penting |
| J-03 | Highlight provinsi tertentu untuk dibandingkan | 🟢 Tambahan |

---

### Modul K — Infografis ECC (Halaman 10 & 11)

**Deskripsi:** Konten visual siap pakai untuk komunikasi publik dan media.

| Kode | Fitur | Prioritas |
|------|-------|-----------|
| K-01 | Kartu infografis per provinsi — status ECC dalam satu pandangan | 🔴 Wajib |
| K-02 | Perbandingan visual antar pulau besar | 🟡 Penting |
| K-03 | Ringkasan scorecard nasional — semua indikator utama | 🔴 Wajib |
| K-04 | Unduhan infografis sebagai gambar | 🟢 Tambahan |

---

## 6. Narasi Pengguna (User Stories)

### Dari Perspektif Peneliti

> *"Sebagai peneliti lingkungan, saya ingin melihat metodologi lengkap kalkulasi CF per sektor,
> sehingga saya dapat memverifikasi dan mensitasi hasil riset ini dalam publikasi saya."*

> *"Sebagai peneliti, saya ingin mengunduh dataset provinsi dalam format CSV, sehingga saya dapat
> melakukan analisis lanjutan menggunakan perangkat saya sendiri."*

### Dari Perspektif Analis Kebijakan

> *"Sebagai analis kebijakan, saya ingin mengetahui provinsi mana yang paling mendesak untuk
> mendapatkan intervensi kebijakan pengurangan jejak karbon, sehingga saya dapat memprioritaskan
> rekomendasi policy brief CELIOS."*

> *"Sebagai analis kebijakan, saya ingin dapat mengubah bobot indikator IKL, sehingga saya bisa
> menguji skenario kebijakan yang berbeda."*

### Dari Perspektif Jurnalis

> *"Sebagai jurnalis, saya ingin mendapatkan angka defisit ekologis DKI Jakarta dibandingkan
> Kalimantan Timur dalam satu tampilan, sehingga saya dapat menulis berita yang berimbang."*

> *"Sebagai jurnalis, saya ingin melihat infografis yang langsung siap digunakan, sehingga saya
> tidak perlu membuat grafik sendiri."*

### Dari Perspektif Pejabat Daerah

> *"Sebagai kepala dinas lingkungan hidup provinsi, saya ingin melihat posisi provinsi saya
> dibandingkan rata-rata nasional dan provinsi serupa, sehingga saya dapat merumuskan target
> penurunan jejak karbon yang realistis."*

### Dari Perspektif Perusahaan / ESG

> *"Sebagai manajer keberlanjutan perusahaan, saya ingin melihat indeks kerentanan lingkungan
> di wilayah operasi kami, sehingga saya dapat menyusun laporan ESG yang relevan secara lokal."*

---

## 7. Alur Penggunaan

### 7.1 Alur Kunjungan Umum (Publik)

```
Masuk ke Beranda
    → Baca kondisi nasional (Jumlah Bumi, status defisit/reserve)
    → Klik Overview Nasional → Lihat peta & perbandingan provinsi
    → Klik provinsi spesifik → Lihat detail
    → Klik Infografis → Unduh/bagikan visual
```

### 7.2 Alur Riset (Akademisi)

```
Masuk ke Dokumentasi Riset
    → Baca metodologi & formula
    → Pindah ke Eksplorasi Data
    → Filter variabel yang dibutuhkan
    → Unduh CSV
    → Cek Validasi Metode → Lihat referensi ilmiah
```

### 7.3 Alur Advokasi (LSM/Analis)

```
Masuk ke Indeks Kerentanan (IKL)
    → Lihat ranking provinsi
    → Sesuaikan bobot indikator → Uji skenario
    → Pindah ke Defisit Ekologis → Kuantifikasi gap
    → Pindah ke Jejak Karbon Sektoral → Identifikasi penyebab
    → Infografis → Ekspor visual untuk kampanye
```

---

## 8. Indikator Keberhasilan

### 8.1 Indikator Produk

| Indikator | Target | Cara Ukur |
|-----------|--------|-----------|
| Kelengkapan data | 38 dari 38 provinsi terisi | Cek dataset sebelum publikasi |
| Akurasi kalkulasi | Selisih < 5% dari referensi GFN | Validasi silang dengan data GFN nasional |
| Responsivitas tampilan | Halaman terbuka < 3 detik | Uji performa |
| Ketersediaan bilingual | Semua teks tersedia ID + EN | Review konten |

### 8.2 Indikator Dampak

| Indikator | Target (12 bulan pasca-rilis) |
|-----------|-------------------------------|
| Kunjungan dashboard | > 5.000 pengguna unik |
| Sitasi dalam publikasi | > 3 publikasi ilmiah |
| Media coverage | > 10 artikel media |
| Policy engagement | > 2 instansi pemerintah menggunakan data |
| Unduhan dataset | > 500 unduhan CSV |

---

## 9. Keterbatasan & Asumsi

### 9.1 Keterbatasan yang Diterima

| Keterbatasan | Penjelasan | Dampak pada Produk |
|---|---|---|
| **Data tidak real-time** | Semua data bersumber dari laporan tahunan | Dashboard diperbarui 1x/tahun |
| **Skala provinsi** | Analisis tidak mencapai tingkat kabupaten/kota | Tidak bisa untuk kebijakan level lokal |
| **Faktor emisi generik** | Menggunakan IPCC Tier 1 bukan studi LCA lokal yang mahal | Angka bersifat estimasi, bukan pengukuran langsung |
| **GFN factors agregat** | Yield & Equivalence Factor GFN tidak tersedia per provinsi | Digunakan nilai nasional Indonesia (mengurangi ketepatan antarwilayah) |
| **Data PDAM tidak terpusat** | Konsumsi air per provinsi diestimasi dari standar SNI | Variasi aktual antar wilayah tidak tertangkap |

### 9.2 Asumsi yang Dipegang

- Seluruh data publik dari BPS, PLN, KLHK, ESDM, dan BNPB dapat diakses secara legal dan gratis
- Metodologi Świąder et al. (2020) dapat diadaptasi untuk konteks Indonesia dengan penyesuaian sumber data lokal
- Baseline tahun 2023 digunakan sebagai titik awal; data tahun sebelumnya untuk perbandingan tren
- Dashboard bersifat terbuka (tidak berbayar, tidak memerlukan login) untuk akses publik

---

## 10. Glosarium

| Istilah | Penjelasan |
|---------|------------|
| **ECC** | Environmental Carrying Capacity — Daya Dukung Lingkungan Hidup |
| **CF / Carbon Footprint** | Total emisi gas rumah kaca yang dihasilkan aktivitas manusia, diukur dalam global hectare (gha) |
| **BC / Biocapacity** | Kemampuan ekosistem untuk memperbaharui sumber daya alam dan menyerap emisi, diukur dalam global hectare (gha) |
| **Ecological Deficit** | Kondisi di mana CF > BC — alam tidak sanggup menampung beban aktivitas manusia |
| **Ecological Reserve** | Kondisi di mana BC > CF — alam masih memiliki kapasitas berlebih |
| **gha (global hectare)** | Satuan ukur biokapasitas yang mempertimbangkan produktivitas rata-rata global seluruh lahan di bumi |
| **Jumlah Bumi** | Berapa planet bumi yang dibutuhkan jika seluruh manusia di dunia hidup seperti penduduk wilayah yang diukur |
| **IKL** | Indeks Kerentanan Lingkungan — indeks komposit yang mengukur seberapa rentan suatu wilayah terhadap krisis ekologis |
| **GFN** | Global Footprint Network — lembaga internasional penyedia data dan faktor standar perhitungan jejak ekologis |
| **DDDTLH** | Daya Dukung dan Daya Tampung Lingkungan Hidup — terminologi resmi dalam regulasi Indonesia (PP 22/2021) |
| **Yield Factor** | Rasio produktivitas lahan suatu negara terhadap rata-rata produktivitas lahan global |
| **Equivalence Factor** | Faktor konversi yang menyetarakan berbagai jenis lahan ke dalam satuan global hectare |
| **IPCC Tier 1** | Pendekatan perhitungan emisi paling dasar menggunakan faktor emisi standar internasional tanpa pengukuran langsung |
| **PROPER** | Program Penilaian Peringkat Kinerja Perusahaan — sistem peringkat lingkungan dari KLHK untuk perusahaan di Indonesia |

---

## 11. Fase Pengembangan Dashboard

> Pengembangan dilakukan secara bertahap. Setiap fase menghasilkan sesuatu yang
> **langsung dapat dijalankan dan diuji** — tidak ada fase yang menggantung tanpa output nyata.
> Urutan ini dirancang agar setiap sesi kerja dapat diselesaikan secara mandiri.

---

### FASE 0.1 — Kerangka Aplikasi (App Shell)
**Output:** Seluruh struktur halaman dapat dijalankan di browser — logo, sidebar, navigasi, dan banner pengembangan aktif  
**Kriteria selesai:** `streamlit run Dashboard.py` menampilkan beranda, semua 11 halaman dapat diakses via sidebar, halaman Dokumentasi Riset menampilkan `framework-riset-ecc.md` secara langsung

| Langkah | Deskripsi |
|---------|-----------|
| 0.1.1 | Copy aset logo CELIOS dari proyek EBT ke `refrensi/` |
| 0.1.2 | Update `.streamlit/config.toml` — tema hijau ECC, sidebar navigation dinonaktifkan |
| 0.1.3 | Selesaikan `src/components/sidebar.py` — logo, toggle bahasa, navigasi 2 grup (Analisis & Resources) |
| 0.1.4 | Selesaikan `Dashboard.py` — favicon logo, CSS Inter, 3 kartu narasi riset, banner pengembangan |
| 0.1.5 | Buat 10 halaman stub (hal. 1–5, 7–11) — masing-masing: page_config, sidebar, judul, caption, banner pengembangan |
| 0.1.6 | Buat halaman 6 Dokumentasi Riset — baca dan render `docs/framework-riset-ecc.md` langsung |
| 0.1.7 | Verifikasi: semua 11 halaman terbuka tanpa error, navigasi sidebar berfungsi penuh |

**Kontribusi ke Publikasi Ilmiah:** Tidak langsung — fase ini hanya infrastruktur tampilan

---

### FASE 1 — Fondasi Data
**Output:** File CSV data simulasi 38 provinsi siap dipakai dashboard  
**Kriteria selesai:** `python data/prepare_data.py` berhasil menghasilkan `provinsi_ecc.csv` dan `nasional_summary.csv`

| Langkah | Deskripsi |
|---------|-----------|
| 1.1 | Buat `data/pipeline/constants.py` — faktor GFN, faktor emisi IPCC, faktor emisi grid PLN |
| 1.2 | Buat `data/pipeline/generate_mock_data.py` — simulasi data realistis 38 provinsi (CF + BC per komponen) |
| 1.3 | Buat `data/prepare_data.py` — orkestrasi pipeline, ekspor ke `data/processed/` |
| 1.4 | Verifikasi: buka CSV, pastikan 38 baris × semua kolom terisi |

**Kontribusi ke Publikasi Ilmiah: ~12–16 halaman**

| Subbab yang Dihasilkan | Isi | Est. Hal |
|------------------------|-----|:--------:|
| Bab Metodologi — Sumber & Pipeline Data | Penjelasan 8 instansi sumber data, cara pengumpulan, keterbatasan | 4–5 |
| Bab Metodologi — 48 Variabel & Formula | Formula CF per sektor, formula BC, GFN factors, cara kalkulasi ECC | 5–7 |
| Lampiran Teknis — Tabel Data 38 Provinsi | Tabel lengkap semua variabel per provinsi sebagai lampiran | 3–4 |

---

### FASE 2 — Kerangka Aplikasi (App Shell)
**Output:** Dashboard dapat dijalankan di browser dengan sidebar dan halaman beranda  
**Kriteria selesai:** `streamlit run Dashboard.py` menampilkan halaman beranda dengan 4 KPI card dan navigasi sidebar berfungsi

| Langkah | Deskripsi |
|---------|-----------|
| 2.1 | Selesaikan `src/utils/data_loader.py` — fungsi load CSV + helper format angka |
| 2.2 | Selesaikan `src/components/sidebar.py` — logo CELIOS, pilihan bahasa, navigasi 11 halaman |
| 2.3 | Selesaikan `Dashboard.py` — 4 KPI card nasional, 3 ringkasan narasi, custom CSS |
| 2.4 | Verifikasi: semua link navigasi tidak error 404 |

**Kontribusi ke Publikasi Ilmiah: ~8–12 halaman**

| Subbab yang Dihasilkan | Isi | Est. Hal |
|------------------------|-----|:--------:|
| Ringkasan Eksekutif / Temuan Utama | 4 angka kunci nasional (CF total, BC total, Jumlah Bumi, jumlah provinsi defisit) dalam format infografis | 3–4 |
| Pendahuluan — Urgensi Riset | Konteks DDDTLH, mengapa ECC penting untuk Indonesia, gap kebijakan | 3–4 |
| Pendahuluan — Tiga Pertanyaan Riset | Narasi 3 narasi utama sebagai kerangka bab-bab berikutnya | 2–3 |

---

### FASE 3 — Halaman 1: Overview Nasional
**Output:** Halaman pertama dashboard berfungsi penuh  
**Kriteria selesai:** Peta choropleth 38 provinsi tampil + grafik batang CF vs BC + tabel dengan filter

| Langkah | Deskripsi |
|---------|-----------|
| 3.1 | Grafik batang CF vs BC per provinsi (dapat diurutkan) |
| 3.2 | Peta choropleth Indonesia — warna berdasarkan status ECC (merah/hijau) |
| 3.3 | Tabel ringkasan dengan filter dan highlight 5 teratas/terbawah |
| 3.4 | Tombol unduhan CSV |

**Kontribusi ke Publikasi Ilmiah: ~18–25 halaman**

| Subbab yang Dihasilkan | Isi | Est. Hal |
|------------------------|-----|:--------:|
| Kondisi ECC Indonesia 2023 | Narasi Jumlah Bumi Indonesia, status nasional defisit/cadangan, perbandingan dengan rata-rata global & ASEAN | 3–4 |
| Peta & Analisis Regional | Peta choropleth + narasi per pulau besar: Jawa, Sumatera, Kalimantan, Sulawesi, Papua — pola dan penyebab | 4–5 |
| Profil 5 Provinsi Defisit Terbesar | Per provinsi: angka CF vs BC, sektor penyebab utama, konteks demografi & ekonomi | 3–4 |
| Profil 5 Provinsi Cadangan Terbesar | Per provinsi: apa yang membuatnya masih aman, potensi yang bisa dioptimalkan | 3–4 |
| Tren Perubahan 2022 vs 2023 | Narasi provinsi yang memburuk vs membaik, faktor penyebab perubahan | 2–3 |
| Perbandingan Indonesia vs Dunia | Posisi Indonesia dalam konteks global & ASEAN, implikasi diplomatik & kebijakan iklim | 2–3 |

---

### FASE 4 — Halaman 2: Jejak Karbon Sektoral
**Output:** Analisis 7 sektor aktivitas per provinsi  
**Kriteria selesai:** Stacked bar 7 sektor tampil + filter sektor berfungsi + penjelasan metodologi per sektor

| Langkah | Deskripsi |
|---------|-----------|
| 4.1 | Grafik batang bertumpuk (stacked bar) 7 sektor × 38 provinsi |
| 4.2 | Peta gelembung — ukuran = total CF, warna = sektor dominan |
| 4.3 | Filter pemilihan sektor + perbandingan antar pulau |
| 4.4 | Expander metodologi per sektor (penjelasan non-teknis) |

**Kontribusi ke Publikasi Ilmiah: ~30–40 halaman** *(bab paling tebal)*

| Subbab yang Dihasilkan | Isi | Est. Hal |
|------------------------|-----|:--------:|
| Sektor 1 — Ketahanan Pangan | Temuan CF pangan per provinsi, korelasi dengan pola konsumsi & kemiskinan, provinsi dengan CF pangan tertinggi | 4–5 |
| Sektor 2 — Sanitasi & Air Limbah | Infrastruktur IPAL per provinsi, gap pengolahan limbah cair, emisi dari sektor ini | 3–4 |
| Sektor 3 — Pengelolaan Sampah | Volume sampah per provinsi, TPA terbuka vs sanitary landfill, emisi CH₄ dari TPA | 4–5 |
| Sektor 4 — Konsumsi Air Bersih | Konsumsi vs ketersediaan air, emisi dari sistem distribusi, kesenjangan akses antar wilayah | 3–4 |
| Sektor 5 — Energi Listrik | Faktor emisi grid PLN per wilayah, ketimpangan akses vs konsumsi, potensi EBT mengurangi CF | 4–5 |
| Sektor 6 — Gas & LPG Rumah Tangga | Distribusi LPG per provinsi, program konversi minyak tanah, kontribusi CF rumah tangga | 3–4 |
| Sektor 7 — Transportasi & Kendaraan | Pertumbuhan kendaraan bermotor, emisi per km, perbedaan kota besar vs daerah | 4–5 |
| Analisis Cross-Sektoral | Sektor dominan per wilayah, pola Jawa vs luar Jawa, peta sektor penyumbang terbesar | 3–4 |
| Temuan Statistik Asosiasi | Apakah sektor dominan berkorelasi dengan status defisit? Implikasi kebijakan prioritas | 2–3 |

---

### FASE 5 — Halaman 3: Defisit Ekologis
**Output:** Visualisasi gap CF vs BC  
**Kriteria selesai:** Scatter plot CF×BC dengan garis keseimbangan tampil + grafik gap diurutkan + highlight provinsi kritis

| Langkah | Deskripsi |
|---------|-----------|
| 5.1 | Scatter plot CF (X) vs BC (Y) — garis diagonal = titik seimbang, label provinsi |
| 5.2 | Grafik gap defisit/cadangan diurutkan dari terbesar |
| 5.3 | Indikator efisiensi ekologis per provinsi (%) |
| 5.4 | Highlight provinsi mendekati titik kritis (rasio ECC > 0.8) |

**Kontribusi ke Publikasi Ilmiah: ~20–26 halaman**

| Subbab yang Dihasilkan | Isi | Est. Hal |
|------------------------|-----|:--------:|
| Cara Membaca Defisit Ekologis | Penjelasan konsep gap CF vs BC, arti scatter plot, makna garis keseimbangan untuk pembaca awam | 2–3 |
| Profil 10 Provinsi Defisit Kritis | Per provinsi: besaran defisit, sektor penyebab dominan, konteks industri & urbanisasi | 5–7 |
| Profil 10 Provinsi Cadangan Ekologis | Mengapa masih aman, potensi yang dimiliki, risiko jika pola pembangunan tidak berubah | 4–5 |
| 18 Provinsi Mendekati Titik Kritis | Analisis provinsi dengan rasio ECC 0.7–0.99 — siapa yang paling berisiko dalam 5 tahun ke depan | 3–4 |
| Efisiensi Ekologis per Provinsi | Siapa paling efisien (BC tinggi, CF rendah) dan siapa paling boros, konteks kebijakan tataguna lahan | 2–3 |
| Skenario Proyeksi 2025–2030 | Jika populasi tumbuh 1,5%/tahun — berapa provinsi akan masuk kondisi defisit? | 2–3 |

---

### FASE 6 — Halaman 4: Indeks Kerentanan Lingkungan (IKL)
**Output:** Indeks komposit 6 dimensi + ranking  
**Kriteria selesai:** Ranking IKL 38 provinsi tampil + grafik radar + slider bobot berfungsi

| Langkah | Deskripsi |
|---------|-----------|
| 6.1 | Kalkulasi IKL (MinMaxScaler × 6 bobot) di dalam halaman |
| 6.2 | Tabel ranking IKL + badge warna kerentanan |
| 6.3 | Grafik radar profil 6 dimensi per provinsi (pilih provinsi) |
| 6.4 | Peta IKL choropleth |
| 6.5 | Slider bobot interaktif — pengguna sesuaikan → IKL otomatis recalculate |

**Kontribusi ke Publikasi Ilmiah: ~22–28 halaman**

| Subbab yang Dihasilkan | Isi | Est. Hal |
|------------------------|-----|:--------:|
| Konstruksi IKL: 6 Dimensi | Penjelasan setiap dimensi, justifikasi bobot default, referensi metodologi serupa | 4–5 |
| Ranking IKL 38 Provinsi | Tabel ranking + narasi pola: kelompok Kritis / Waspada / Stabil / Aman | 4–5 |
| Klaster Kerentanan & Profil 4 Klaster | Siapa masuk klaster mana, karakteristik tiap klaster, peta visualisasi | 4–5 |
| Profil 10 Provinsi Paling Rentan | Per provinsi: skor IKL, dimensi paling lemah, konteks sosial-ekonomi, rekomendasi prioritas | 5–6 |
| Korelasi IKL vs IPM | Apakah provinsi miskin = paling rentan ekologis? Temuan dan anomali yang menarik | 2–3 |
| Korelasi IKL vs PDRB | Apakah kaya secara ekonomi = aman secara ekologis? Membongkar asumsi pembangunan | 2–3 |

---

### FASE 7 — Halaman 5: Eksplorasi Data
**Output:** Antarmuka eksplorasi data terbuka  
**Kriteria selesai:** Tabel lengkap dapat difilter + metadata variabel tersedia + unduhan CSV berfungsi

| Langkah | Deskripsi |
|---------|-----------|
| 7.1 | Tabel data lengkap 38 provinsi dengan semua variabel |
| 7.2 | Filter multi-kolom (wilayah, status ECC, rentang nilai) |
| 7.3 | Tampilan grafik otomatis untuk kolom yang dipilih |
| 7.4 | Tooltip metadata per kolom (definisi, satuan, sumber data) |
| 7.5 | Unduhan CSV |

**Kontribusi ke Publikasi Ilmiah: ~6–10 halaman**

| Subbab yang Dihasilkan | Isi | Est. Hal |
|------------------------|-----|:--------:|
| Lampiran — Kamus Data (Data Dictionary) | Definisi, satuan, sumber setiap variabel dari 48 variabel | 4–5 |
| Catatan Metodologi — Keterbatasan Data | Variabel mana yang menggunakan estimasi, mana yang dari data primer | 2–3 |

---

### FASE 8 — Halaman 6: Dokumentasi Riset
**Output:** Semua dokumen riset dapat dibaca di dalam dashboard  
**Kriteria selesai:** Dropdown dokumen berfungsi + render markdown + tombol unduhan

| Langkah | Deskripsi |
|---------|-----------|
| 8.1 | Daftar dokumen dari folder `docs/` (otomatis detect file `.md`) |
| 8.2 | Render markdown dengan metadata (judul, tanggal, tag topik) |
| 8.3 | Tombol unduhan file |

**Kontribusi ke Publikasi Ilmiah: ~5–8 halaman**

| Subbab yang Dihasilkan | Isi | Est. Hal |
|------------------------|-----|:--------:|
| Bab Metodologi — Transparansi & Reprodusibilitas | Penjelasan bahwa semua dokumen metodologi tersedia publik, cara mengakses | 2–3 |
| Daftar Pustaka & Referensi | Referensi paper Świąder (2020), GFN, IPCC, BPS, dan sumber data lainnya | 3–5 |

---

### FASE 9 — Halaman 7 & 8: Validasi & Bibliometrik
**Output:** Dua halaman berbasis pencarian literatur ilmiah  
**Kriteria selesai:** Pencarian paper dari OpenAlex API berfungsi + skor relevansi tampil

| Langkah | Deskripsi |
|---------|-----------|
| 9.1 | Integrasi OpenAlex API — harvest paper ECC/ecological footprint |
| 9.2 | Kalkulasi skor relevansi (TF-IDF cosine similarity) |
| 9.3 | Tampilan daftar paper + filter tahun/jurnal (hal. 7) |
| 9.4 | Visualisasi tren bibliometrik + kata kunci dominan (hal. 8) |

**Kontribusi ke Publikasi Ilmiah: ~6–10 halaman**

| Subbab yang Dihasilkan | Isi | Est. Hal |
|------------------------|-----|:--------:|
| Tinjauan Literatur | Lanskap riset ECC global & Asia Tenggara, posisi riset ini dalam konteks ilmiah | 3–5 |
| Validasi Metodologi | Perbandingan metodologi Świąder (2020) dengan studi serupa, justifikasi adaptasi untuk Indonesia | 3–5 |

---

### FASE 10 — Halaman 9, 10, 11: Visualisasi Lanjutan & Infografis
**Output:** Tiga halaman visual komunikasi  
**Kriteria selesai:** Parallel coordinates D3.js tampil + kartu infografis 38 provinsi + scorecard nasional

| Langkah | Deskripsi |
|---------|-----------|
| 10.1 | D3.js Parallel Coordinates — embed HTML/JS ke Streamlit (hal. 9) |
| 10.2 | Grid kartu infografis per provinsi — status ECC dalam satu pandangan (hal. 10) |
| 10.3 | Scorecard nasional — semua indikator utama dalam satu halaman (hal. 11) |

**Kontribusi ke Publikasi Ilmiah: ~18–25 halaman**

| Subbab yang Dihasilkan | Isi | Est. Hal |
|------------------------|-----|:--------:|
| Analisis Multidimensi — Pola Tersembunyi | Temuan dari parallel coordinates: cluster provinsi yang serupa secara multidimensi | 4–5 |
| Infografis per Provinsi (38 provinsi) | Kartu 1 halaman per provinsi dengan semua indikator ECC utama — bisa jadi lampiran atau Volume 2 | 8–12 |
| Scorecard Nasional | Satu halaman ringkasan semua indikator — siap jadi halaman penutup atau sampul dalam | 2–3 |
| Rekomendasi Kebijakan — per Wilayah | Rekomendasi spesifik Jawa, Kalimantan, Sumatera, Papua berdasarkan temuan multidimensi | 4–5 |

---

### FASE 11 — Lokalisasi & Poles Akhir
**Output:** Dashboard siap publikasi, bilingual, performa optimal  
**Kriteria selesai:** Semua teks tersedia dalam Bahasa Indonesia dan English + tidak ada error saat dijalankan

| Langkah | Deskripsi |
|---------|-----------|
| 11.1 | Ekstrak semua string teks ke file lokalisasi `.po` (ID + EN) |
| 11.2 | Kompilasi file `.mo` — uji perpindahan bahasa |
| 11.3 | Audit CSS — konsistensi warna, tipografi, responsivitas |
| 11.4 | Optimasi performa — pastikan semua halaman terbuka < 3 detik |
| 11.5 | Uji akhir seluruh 11 halaman dari halaman 1 hingga 11 |

---

### FASE 12 — Integrasi Data Nyata *(Opsional — setelah API Key tersedia)*
**Output:** Dashboard menggunakan data live dari BPS, PLN, SIPSN  
**Kriteria selesai:** `prepare_data.py` dapat berjalan dengan data aktual tanpa mock

| Langkah | Deskripsi |
|---------|-----------|
| 12.1 | `data/pipeline/fetch_bps.py` — integrasi BPS WebAPI (butuh `BPS_API_KEY`) |
| 12.2 | `data/pipeline/fetch_pln.py` — scrape/parse PDF Statistik PLN |
| 12.3 | `data/pipeline/fetch_sipsn.py` — scrape tabel SIPSN KLHK |
| 12.4 | Validasi silang: bandingkan hasil data nyata vs mock, sesuaikan jika ada selisih besar |
| 12.5 | Update `data/prepare_data.py` — ganti mock dengan live pipeline |

---

### Ringkasan Fase

| Fase | Nama | Modul PRD | Est. Sesi | Kontribusi Publikasi |
|------|------|-----------|:---------:|:--------------------:|
| 1 | Fondasi Data | — | 1 sesi | ~12–16 hal |
| 2 | App Shell | A (Beranda) | 1 sesi | ~8–12 hal |
| 3 | Overview Nasional | B | 1 sesi | ~18–25 hal |
| 4 | Jejak Karbon Sektoral | C | 1 sesi | **~30–40 hal** |
| 5 | Defisit Ekologis | D | 1 sesi | ~20–26 hal |
| 6 | Indeks Kerentanan (IKL) | E | 1–2 sesi | ~22–28 hal |
| 7 | Eksplorasi Data | F | 1 sesi | ~6–10 hal |
| 8 | Dokumentasi Riset | G | 1 sesi | ~5–8 hal |
| 9 | Validasi & Bibliometrik | H, I | 1–2 sesi | ~6–10 hal |
| 10 | Visualisasi & Infografis | J, K | 1–2 sesi | ~18–25 hal |
| 11 | Lokalisasi & Poles | — | 1 sesi | — |
| 12 | Integrasi Data Nyata | — | 2–3 sesi | — |
| **Total** | | | **~13–17 sesi** | **~145–200 hal** |

> **Catatan:** Satu "sesi" = satu sesi kerja yang menghasilkan output yang dapat langsung dijalankan
> dan diuji. Fase 1–8 adalah inti produk minimum yang sudah dapat dipublikasikan.
> Fase 9–12 adalah peningkatan lanjutan.
>
> Estimasi halaman publikasi berdasarkan format laporan CELIOS (50% narasi, 50% visual).
> **Fase 4 (Jejak Karbon Sektoral) adalah bab terpanjang** karena 7 sektor × analisis mendalam per sektor.

---

*Dokumen ini ditujukan untuk seluruh pemangku kepentingan proyek CELIOS ECCIS — peneliti, analis kebijakan, mitra komunikasi, dan pengambil keputusan — tanpa memerlukan latar belakang teknis informatika.*

*Versi berikutnya akan mencakup wireframe antarmuka dan spesifikasi visualisasi.*

**Dibuat oleh:** Tim Riset CELIOS  
**Terakhir diperbarui:** Mei 2026


---

> [!NOTE]
> ## 📖 Ekstraksi PageIndex (Świąder 2020)
> Dokumen ini telah divalidasi dan diperbarui berdasarkan ekstraksi hierarki mendalam oleh PageIndex. Temuan metodologis kunci yang harus diintegrasikan ke dalam fase ini:
> 1. **Komposisi Defisit Ekologis (Carbon Footprint)**: Secara empiris, penyumbang terbesar adalah **Listrik (66,6%)**, **Mobilitas (16,8%)**, dan **Pangan (6,4%)**. Ketiga sektor ini harus menjadi prioritas utama analisis data.
> 2. **Ketimpangan Spasial (Urban vs Rural)**: Pusat populasi/industri padat bisa jadi menyumbang **75% dari total defisit ekologis** absolut, meskipun persentase pertumbuhannya lebih kecil dari wilayah rural (efek ketimpangan terpusat).
> 3. **Mitigasi Tata Ruang**: Pelarangan alih fungsi **lahan pertanian (*good-quality soils*)** terbukti menjadi variabel mitigasi paling kuat (berdampak hingga penurunan 62% ekspansi CF) dibandingkan perlindungan kawasan hutan lindung standar. Analisis spasial harus memasukkan status *agricultural soil* sebagai variabel krusial.
> 4. **Radius Defisit**: Defisit ekologis tidak hanya berhenti di batas administratif, melainkan menyebar secara radius (contoh di Wrocłąw melebar dari 107km ke 141km) mendesak kapasitas wilayah/provinsi tetangganya.
