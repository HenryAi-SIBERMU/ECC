# Rencana Implementasi: Tool Ekstraksi Laporan Metodologi (DOCX & LaTeX)

Berdasarkan asesmen terhadap struktur direktori `pages/` (kode antarmuka Streamlit) dan `docs/` (dokumentasi teknis), kita memiliki kumpulan metodologi riset yang sangat kaya dan mendalam. Metodologi ini tersebar di berbagai tempat—mulai dari *tag* *inline* di dashboard hingga dokumen penjabaran matematis.

Tujuan dari *task* ini adalah membuat *tool* generator otomatis (mirip `streamlittopdf`) yang khusus merakit dan mengekstrak seluruh kepingan metodologi tersebut menjadi satu **Laporan Metodologi Riset** yang komprehensif, akademis, dan siap cetak (DOCX & LaTeX).

---

## 1. Inventarisasi Sumber Metodologi

Dari hasil pemindaian (*scanning*), berikut adalah metodologi yang saat ini digunakan dan akan dirangkum ke dalam laporan:

### A. Bersumber dari Dashboard (`pages/*.py`)
*   **Analisis Statistik Ekologis & Epidemiologis:** *Chi-Square (χ²)*, *Odds Ratio* (95% CI & 90% CI), *Crosstabulation* (Sentra vs Non-Sentra), *Panel Data Analysis*.
*   **Analisis Spasial & Geospasial:** *Spatial Overlay* (ESDM x GFW x Peta Konflik), *Spatial Logistic Mapping*, Pemetaan GBIF & *IUCN Red List*, Peta Tematik (*Choropleth* & *Bubble Map*).
*   **Analisis Ekonomi & Demografi:** *PDRB Sector Shift Index* (Efek Kanibalisasi Tambang), *Comparative Density Analysis*, Proxy Migrasi dari Time-Series Populasi, *Wealth Database Analysis*.
*   **Analisis Sosial & Hukum:** *Frequency Profiling (NLP Text Parsing)* terhadap laporan konflik (Tanah Kita, CATAHU KPA), *Open Source Intelligence* (OSINT) pelacakan infrastruktur, *Thematic Coding*.

### B. Bersumber dari Dokumen Teknis (`docs/*.md`)
*   `Metode_Crosstab_Ekologis.md`: Detail transformasi *binning* data (*Within-Province Variance*) dan *Golden Standard* Epidemiologi (kalkulasi *Odds Ratio* untuk *Sacrifice Zones*).
*   `metodologi_klasifikasi_ekstraktif.md`: Dasar hukum dan logika *supply-chain* untuk reklasifikasi sektor BPS (menggabungkan Pertambangan, Smelter/Industri Pengolahan, dan PLTU Captive/Listrik).
*   `Metode Model_Matematis_Skoring_ECC.md`: Formulasi matematis indeks *Ecological Collapse*.
*   `metodologi_nlp_aktor.md` & `metodologi_rugi_ekologis.md`: Pendekatan kualitatif-kuantitatif untuk pemetaan oligarki dan valuasi kerugian lingkungan.
*   `Metodologi imputasi augmentasi data.md`: Penanganan *missing data*.

---

## 2. Arsitektur Tool Generator

Kita akan membangun modul baru di direktori `tools/methodology_to_pdf/`. 

### Komponen Utama:
1.  **`extract_methodology.py` (Script Parser & Compiler Markdown)**
    *   Script ini akan membaca file-file Markdown kunci dari folder `docs/` yang berisi landasan matematis dan akademis.
    *   Mengekstrak deskripsi singkat/tag dari file `pages/` (sebagai pelengkap/katalog visual).
    *   Menyusun semua temuan ke dalam satu *template* Markdown master (`laporan_metodologi_master.md`).
2.  **`compile_metodologi.py` (Script Konversi DOCX/LaTeX)**
    *   Menggunakan Pandoc (sama seperti `streamlittopdf`) untuk mengonversi `laporan_metodologi_master.md` menjadi *output* akhir.
    *   Akan menggunakan penamaan file dinamis ber-timestamp (contoh: `v2_31072026_Laporan_Metodologi_1785501000.docx`) untuk menghindari masalah *cache* atau *file lock* di MS Word.

---

## 3. Rencana Struktur (Outline) Laporan Metodologi

Script ekstraktor akan diatur agar memproduksi laporan dengan *outline* bab berikut:

*   **BAB 1: Desain Riset dan Pendekatan Ekonomi Politik Ekologi** (Membahas *framework* pembuktian terbalik dan *Open Source Intelligence*).
*   **BAB 2: Metodologi Pengumpulan dan Standardisasi Data** (Membahas OSINT, teknik ekstraksi BPS/ESDM/TanahKita, dan augmentasi data).
*   **BAB 3: Analisis Statistik Spasial dan Epidemiologis** (Membahas detail *Chi-Square*, *Odds Ratio*, perhitungan batas signifikansi, dan metode Geospasial).
*   **BAB 4: Klasifikasi Sektoral dan Pemodelan Indeks** (Memasukkan Reklasifikasi BPS menjadi Ekstraktif dan Pemodelan Matematis ECC).
*   **BAB 5: Analisis Teks dan Investigasi Aktor** (Memasukkan metodologi NLP untuk pemetaan konflik dan aktor).

---

## 4. Langkah Eksekusi (Menunggu Persetujuan)

Jika rencana di atas sudah sesuai dengan visi *Laporan Metodologi* yang Anda inginkan, saya akan:
1.  Membuat folder `tools/methodology_to_pdf`.
2.  Menulis logika ekstraksi (`extract_methodology.py`) yang membaca `docs/` dan `pages/`.
3.  Menulis logika kompilasi Pandoc (`compile_metodologi.py`).
4.  Menjalankan tes generasi laporan pertama.

Apakah ada tambahan atau penyesuaian untuk kerangka laporan metodologi ini sebelum saya mulai *coding* alatnya?
