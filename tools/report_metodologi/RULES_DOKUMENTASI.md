# Standar & Aturan Dokumentasi (SOP) Proyek Celios2

Dokumen ini merupakan **SOP (Standard Operating Procedure)** wajib yang harus diikuti setiap kali *engineer* atau AI ditugaskan untuk menyusun dokumentasi proyek Celios2. 

Terdapat **4 Pilar Dokumentasi Utama** yang WAJIB dibuat secara serentak dan lengkap untuk setiap topik atau bab analisis. 

> **ATURAN PRESISI TEMPLATE (BERLAKU UNTUK KESELURUHAN 4 PILAR):** 
> Setiap kali agen menyusun 4 pilar untuk sub-bab baru, agen **WAJIB** meniru format, struktur *markdown*, *flowchart*, *tabel postman*, dan gaya bahasa dari dokumen sub-bab sebelumnya yang sudah disahkan. **Hal ini berlaku tanpa pengecualian untuk KE-4 PILAR**, mulai dari Pilar 1 (Metodologi Analisis), Pilar 2 (ETL), Pilar 3 (Fakta Data), hingga Pilar 4 (Indeks Coding). Jangan mengarang format baru! (Contoh referensi mutlak: `bab_1/1.1_Metodologi_ETL_PDRB.md`, `1.1_Fakta_Data_PDRB.md`, dst).

> **ATURAN SINKRONISASI NARASI 100% (DOCX & STREAMLIT PAGE):**
> Penamaan sub-bab, kerangka narasi, dan judul *heading* (seperti H2, H3, H4) di dalam dokumen *generator skrip* (misal: `generate_bab1.py`) maupun di dalam dokumen 4 Pilar **WAJIB** linier dan sinkron 100% dengan teks aktual yang dirender di halaman Streamlit (`pages/*.py`). Agen **DILARANG KERAS** mengarang istilah atau *heading* akademis baru di DOCX jika istilah tersebut tidak ada secara *word-for-word* di antarmuka Streamlit. Seluruh dokumen laporan metodologi harus mencerminkan persis apa yang dibaca pengguna di *dashboard*.
---

## Pilar 1: Metodologi Analisis (Per Bab)
**Fokus:** Menjelaskan *business logic*, metode inferensi, dan persamaan matematis dari temuan analisis akhir. Dokumentasi ini digenerate secara terprogram (via Python) ke format DOCX, HTML, dan Markdown.

> **⚠️ PENGINGAT KERAS UNTUK AGEN (PILAR 1):**
> Pilar 1 **TIDAK PERNAH** dibuat sebagai file Markdown (`.md`) mandiri terpisah. Pilar 1 wajib diimplementasikan (di-*coding*) **LANGSUNG ke dalam file *generator script* Python** (contoh: `generate_bab1.py`), agar dirender secara otomatis ke dalam DOCX bersama bagian dokumen lainnya. Saat pengguna meminta "Lanjut Pilar 1", artinya Anda harus mengedit file Python generatornya!

**Struktur Komponen Wajib (Pembagian Tugas A-E):**
1. **A. Pengantar & Kerangka Narasi:** Berfungsi murni sebagai **konteks awal/latar belakang** analisis. **Penting:** Bagian ini BUKAN tempat untuk menjabarkan teknis metodologi (itu tugas B & C) ataupun membocorkan hasil akhir data (itu tugas D & E). Narasi pengantar di bagian A WAJIB bersumber langsung dari narasi aktual di halaman Streamlit.
2. **B. Alur Logika Metodologis (Flowchart):** Bagan Mermaid JS yang memetakan *step-by-step* logika pengujian. Pada DOCX, *flowchart* wajib dirender menjadi gambar (contoh: via API `mermaid.ink`).
   > **STANDAR UKURAN FLOWCHART DI DOCX:**
   > - **Flowchart dengan percabangan (Lebar):** Gunakan `width=Cm(15)` agar proporsional dan membentang penuh di margin halaman.
   > - **Flowchart vertikal lurus tanpa cabang (sekuensial):** WAJIB diubah orientasinya menjadi menyamping/horizontal (`flowchart LR`) dan gunakan `width=Cm(15)`. Jangan biarkan menggunakan `flowchart TD` dengan lebar 15 Cm karena tingginya akan meraksasa (*kegedean*) melampaui batas halaman vertikal.
3. **C. Formulasi Matematis:** Penjabaran rumus atau persamaan statistik yang dipakai secara transparan, dilengkapi keterangan definisi variabel yang jelas.
4. **D. Matriks Hasil Uji Empiris:** Tabel luaran hasil pengujian data aktual (misal: Matriks Chi-Square, Odds Ratio, hasil dekomposisi).
5. **E. Analisis Temuan Empiris:** Penjabaran kesimpulan/pembacaan dari tabel hasil uji (Bagian D) yang fleksibel mengikuti kondisi data.

---

## Pilar 2: End-to-End Data Pipeline (Acquisition to Cleaning)
**Fokus:** Menjelaskan *End-to-End Pipeline* mulai dari *Data Acquisition*, *ETL / Ingestion*, hingga *Preprocessing & Cleaning*. Hal ini membuktikan bahwa data yang diambil bersifat valid, legal, dan dapat direplikasi secara teknis tanpa tebakan (*no hardcoding* rahasia).

**Komponen Wajib:**
1. **Metadata Header:**
   - Wajib menyertakan *Topik*, *Sumber Data*, dan **Jalur File Eksekutor (*File Path*)**.
   - Skrip Python tidak boleh hanya ditulis nama filenya (misal: `script.py`), melainkan **wajib menyertakan path relatif lengkap** ke folder aslinya (contoh: `tools/esdm/script.py`) agar mudah dilacak (*mapped*).
2. **Stage 1: Data Acquisition (Scraping, Mining, API):** 
   - Penjelasan asal-usul sumber data, *endpoint* API, atau target *scraping*.
   - *Flowchart* spesifik (Mermaid JS) yang memetakan tahapan pemanggilan API atau alur akuisisi data.
   - Penjelasan anatomi *REST Path* atau *URL endpoint* yang digunakan.
3. **Stage 2: ETL / Ingestion:**
   - Bagaimana data mentah (raw) diekstrak dan didaratkan (*landing*) ke direktori lokal (misalnya disimpan sebagai file di `data/raw/`).
4. **Stage 3: Preprocessing & Cleaning:**
   - **Wajib menggunakan Tabel Markdown 4 Kolom** yang berisi: (1) *Tahap Pembersihan*, (2) *Kolom Target*, (3) *Deskripsi Tindakan (Logika Pandas)*, dan (4) *Contoh Transformasi (Before ➔ After)*.
   - Tabel ini mendeskripsikan secara konkret proses normalisasi (contoh: pembersihan tag HTML BPS), imputasi *missing values*, pemfilteran geospasial (Geofencing), dan agregasi/kalkulasi data akhir yang terikat langsung dengan kode Python.
   - Jika ada variabel khusus seperti kamus pemetaan (misal: *Geofencing array*), wajib disajikan juga dalam format tabel agar rapi.
5. **Validasi Integritas & Timeframe:**
   - Panduan nyata berupa uji coba *Postman/cURL* (lengkap dengan *API Key* eksplisit) atau pembuktian log pembersihan untuk memvalidasi algoritma.
   - Pembuktian *array* ketersediaan rentang tahun untuk memastikan keselarasan analisis historis (contoh: runtun 1 dekade 2014-2024).
6. **Output (Data Provenance):**
   - Wajib merujuk pada `data/DATA_DICTIONARY.md`.
   - Wajib menampilkan tabel pendaratan akhir (*Processed CSV*) berisi: *Nama File*, *Sumber Asli*, *Penggunaan pada Sub-bab*, dan *Deskripsi*.

*(Referensi Panduan: Lihat format pada file `Fakta Data_Demografi.md` bagian Metodologi & Validasi Akuisisi Data).*

---

## Pilar 3: Fakta Data (Data Fact & Dictionary)
**Fokus:** Menjadi *Data Dictionary* sekaligus lembar ringkasan temuan data tabular (*raw* maupun *processed*) untuk menjembatani bahasa mesin/akademik ke audiens awam.

**Komponen Wajib:**
1. **Kamus Kolom Dataset (Data Dictionary):**
   - Pemetaan spesifik untuk data *Raw* maupun *Processed*.
   - Tabel 3 Kolom: **Nama Kolom di CSV**, **Penjelasan Teknis (Metodologi/Akademik)**, dan **Penjelasan Bahasa Bayi (Awam)**.
   - *(Referensi Panduan: Lihat format tabel pada file `Fakta Data_GFW.md`)*.
2. **Fakta Data Aktual dalam Tabel Rincian:**
   - Membedah ringkasan data penting, anomali, atau evolusi tren (seperti rincian pertumbuhan per tahun).
   - Tabel harus menyertakan **Keterangan Validasi** untuk cross-check dengan laporan publik lain (misalnya membandingkan agregat lokal Celios vs agregat laporan PDF institusi global).
   - *(Referensi Panduan: Lihat format "Evolusi Historis Kapasitas Nasional" pada file `Fakta Data_PLTU.md`)*.

## Pilar 4: Indeks Coding (Pipeline Teknis)
**Fokus:** Memberikan panduan menyeluruh (*bird's-eye view*) terkait *pipeline* kodingan, tidak hanya sebatas ETL, tetapi juga mencakup logika proses (statistik, *cleaning*) dan visualisasi data per sub-bab. Ini berfungsi sebagai peta indeks bagi *engineer*.

**Komponen Wajib:**
1. **Daftar Indeks Kodingan per Fungsionalitas:**
   - Meliputi tahap ETL, Proses/Logika Statistik (misal: perhitungan Chi-Square, p-value), dan Pembuatan Visualisasi (Chart, Flowchart).
2. **Haram Menaruh Blok Kode Panjang (No Letterlijk Code):**
   - Dilarang menaruh *copy-paste* baris kode sumber secara mentah ke dalam dokumen.
3. **Wajib Menggunakan Hyperlink Line Numbers:**
   - Gunakan fitur tautan (hyperlink) Markdown untuk mengarahkan pembaca langsung ke file dan baris kodenya.
   - Contoh format: `[generate_bab1.py (Baris 400-450)](file:///path/absolute/ke/file/generate_bab1.py#L400-L450)`
4. **Keterkaitan Input-Output (Data Lineage):**
   - Menjelaskan aliran dari data mentah (*raw*) menjadi data matang (*processed*) dan hasil akhirnya (HTML/DOCX).

---

### Peraturan Tambahan
1. Jangan menggabungkan ketiga dokumen ini menjadi satu file raksasa. Mereka memiliki ranah pembaca yang berbeda (Analis Statistika vs Data Engineer vs Jurnalis/Masyarakat Awam).
2. Format penyimpanan harus rapi (konsistensi penggunaan Markdown).
3. Saat *engineer* diinstruksikan membangun bab baru, pastikan untuk memeriksa ketersediaan ketiga pilar ini.
