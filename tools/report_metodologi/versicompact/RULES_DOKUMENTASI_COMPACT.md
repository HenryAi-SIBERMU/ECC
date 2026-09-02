# Standar & Aturan Baku Dokumentasi Laporan Metodologi Statistik (Versi Compact)
**Center of Economic and Law Studies (CELIOS) — Riset D3TLH Sulawesi**

Dokumen ini merupakan **SOP (Standard Operating Procedure)** wajib dalam menyusun laporan **Metodologi Statistik Versi Compact** untuk seluruh bab riset Daya Dukung dan Daya Tampung Lingkungan Hidup (D3TLH) Sulawesi periode 2014–2024.

Standar baku ini dirumuskan dan diverifikasi berdasarkan implementasi final **Bab 1 Versi Compact** yang berukuran **tepat 2 lembar halaman Word** di [`tools/report_metodologi/versicompact/bab_1/`](file:///C:/Users/yooma/OneDrive/Desktop/duniahub/client/4.%20Celios2/tools/report_metodologi/versicompact/bab_1/).

---

## 1. Prinsip Utama & Batasan Panjang Dokumen (Page Budget)

1. **Target Panjang Halaman:**
   - **MAKSIMAL 2 HINGGA 4 LEMBAR (HALAMAN)** per bab saat dibuka di Microsoft Word (DOCX).
   - Verifikasi wajib menggunakan penghitungan statistik Word (*ComputeStatistics wdStatisticPages*).
2. **Kesesuaian Mutlak dengan Dokumen Root Non-Compact:**
   - **TIDAK BOLEH** menambah narasi, opini, atau metafora buatan di luar dokumen metodologi non-compact/full (`Metodologi_Bab{X}_....md`).
   - Seluruh teks pengantar, sitasi regulasi, nama lembaga, angka statistik, formulasi matematika, dan kesimpulan empiris **MURNI BERSUMBER DARI DOKUMEN ROOT NON-COMPACT**.
3. **Bebas dari Segala Bentuk Improvisasi Buatan:**
   - **DILARANG** menambahkan blok *Humanizing Scale* / *Skala Humanisasi* buatan (seperti konversi ke cangkir kopi, lapangan bola, upah per detik buruh, truk tronton, dsb.) jika tidak ada dalam dokumen root.
   - **DILARANG** menambahkan blok *Catatan Keterbatasan Data (Caveats)* terpisah di luar metodologi resmi.
4. **Tanpa Icon / Emoji (No Icon Policy):**
   - Dokumen harus 100% formal dan akademis. Tidak boleh ada emoji atau icon grafis seperti `⚠️`, `🔎`, `✅`, `❌`, `📌`, dll.

---

## 2. Struktur Header & Penomoran Hierarki

Setiap bab versi compact wajib mengikuti konvensi penamaan dan hierarki yang selaras dengan root non-compact:

### A. Header Banner & Judul Dokumen
- **Header Banner:**  
  `CELIOS — CENTER OF ECONOMIC AND LAW STUDIES  |  LAPORAN RISET METODOLOGI D3TLH` (Font 7.5 pt bold, warna `#2E7D32`).
- **Judul Utama Bab (Heading 1):**  
  `# BAB {ROMAWI}: METODOLOGI ANALISIS {NAMA BAB SECARA LENGKAP}`  
  *(Sama persis dengan judul non-compact, Font 10.5 pt bold, border bawah hijau `#1B5E20`).*
- **Paragraf Pengantar:**  
  Paragraf pengantar resmi D3TLH yang menjelaskan ruang lingkup studi 2014–2024.

### B. Penomoran Sub-Bab Langsung (Tanpa Kata 'Poin')
- Penomoran langsung merujuk pada nomor bab dan sub-bab root:
  - `## {Bab}.1 {Judul Sub-Bab Sesuai Root}`
    - `### {Bab}.1.1 {Judul Topik Sesuai Root}`
    - `### {Bab}.1.2 {Judul Topik Sesuai Root}`
  - `## {Bab}.2 {Judul Sub-Bab Sesuai Root}`
  - `## {Bab}.3 {Judul Sub-Bab Sesuai Root}`
  - ...
  - `## {Bab}.X Matriks Indikator dan Sumber Data Resmi Bab {Bab}`
  - `## {Bab}.Y Bagan Alur Kerangka Kerja Riset Bab {Bab}`
- **DILARANG:** Menuliskan kata `"Poin X.X"` atau `"POIN X.X"`. Gunakan langsung nomornya: `X.1`, `X.2`, dst.

---

## 3. Spesifikasi Layout & Tipografi Padat (Ultra-Dense Layout)

Untuk menjamin dokumen muat dalam **2–4 lembar**, spesifikasi file Word (`.docx`) wajib menggunakan parameter berikut:

| Parameter Dokumen | Nilai Baku | Keterangan Teknis |
| :--- | :--- | :--- |
| **Ukuran Kertas** | A4 (21.0 cm × 29.7 cm) | Standar publikasi dokumen resmi |
| **Margin Halaman** | **1.2 cm di seluruh sisi** | Top, Bottom, Left, Right = `Cm(1.2)` (lebar cetak efektif 18.6 cm) |
| **Font Normal (Body)** | **Calibri 8.5 pt** | Warna teks `#222222`, rata kanan-kiri (*Justified*) |
| **Line Spacing Normal** | **1.05** | Spacing Before = `Pt(0)`, Spacing After = `Pt(2)` |
| **Heading 1 (Judul Bab)** | **Calibri 10.5 pt Bold** | Warna `#1B5E20`, Space Before = `Pt(4)`, After = `Pt(2)` |
| **Heading 2 (Sub-Bab)** | **Calibri 9.5 pt Bold** | Warna `#1B5E20`, Space Before = `Pt(4)`, After = `Pt(1.5)`, border bawah tipis |
| **Heading 3 (Topik)** | **Calibri 8.5 pt Bold** | Warna `#2E7D32`, Space Before = `Pt(3)`, After = `Pt(1)` |
| **Teks Sumber Data** | **Calibri 7.5 pt Italic** | Callout box hijau lembut `#F1F8E9` dengan border kiri `#2E7D32` |
| **Formulasi Matematis** | **Consolas 7.5 pt** | Format horizontal 1–2 baris dengan latar `#EDF7EE` dan border kiri `#43A047` |
| **Font Tabel** | **Calibri 7.0–7.5 pt** | Teks sel padat, baris genap berselang-seling `#F9FBF9` |
| **Padding Sel Tabel** | **Atas/Bawah 20–30 dxa, Kiri/Kanan 50 dxa** | Meminimalkan tinggi vertikal baris tabel |

---

## 4. Teknik Pemadatan Konten (Condensation Guidelines)

### A. Pemadatan Formulasi Matematika
- Tampilkan persamaan inti dalam 1 atau 2 baris horizontal secara telanjang.
- Keterangan variabel dituliskan langsung secara *inline* setelah simbol pemisah `|`:
  ```text
  χ² = Σ [ (O - E)² / E ] ; E_ij = (R_i * C_j) / N ; OR = (a * d) / (b * c)
  Ket: O = observasi aktual, E = frekuensi harapan, OR = rasio keunggulan risiko kelompok perlakuan
  ```
- Hindari membuat daftar bullet vertikal panjang untuk setiap variabel jika memakan ruang baris.

### B. Sintesis Tabel Efisien
- Jangan menduplikasi tabel mentah berukuran puluhan baris.
- Gabungkan temuan inferensial ke dalam **1 Tabel Sintesis Panel Utama** (memuat variabel independen $X$, dependen $Y$, nilai $\chi^2$, $p$-value, Odds Ratio, derajat bebas, dan kesimpulan ilmiah).
- Untuk perbandingan spasial wilayah (seperti 13 kabupaten atau 6 provinsi), tampilkan kelompok sentra utama secara rinci dan agregasikan kelompok non-sentra ke dalam baris rata-rata komparatif.
- Pastikan setiap bab tetap menyertakan:
  1. Tabel Reklasifikasi Kerangka Hukum / Konseptual
  2. Tabel Matriks Spasial / Data Temuan Kunci
  3. Tabel Hasil Uji Inferensial Statistik (Chi-Square & Risk Odds Ratio)
  4. Tabel Inventarisasi Infrastruktur / Aktor / Emisi (jika relevan)
  5. Tabel Matriks Indikator dan Sumber Data Primer Resmi
  6. Tabel Tahapan Alur Riset (Fase I s.d. IV)

### C. Narasi Temuan Empiris yang Padat
- Fokuskan narasi pada 3–4 poin temuan kuantitatif paling signifikan yang didukung langsung oleh angka hasil kalkulasi tabel.
- Gunakan cetak tebal (*bold*) untuk angka kunci, nama daerah sentra, status signifikansi statistik ($p < 0.05$), dan kelipatan risiko.

---

## 5. Struktur Folder dan Penamaan File Standar

Setiap bab versi compact wajib dikelola secara rapi di dalam subdirektori masing-masing:

```text
tools/report_metodologi/
├── RULES_DOKUMENTASI.md               <-- Standar Versi Full/Teknis 4 Pilar
├── bab_1/
│   ├── Metodologi_Bab1_Ekspansi_Industri.md
│   ├── Metodologi_Bab1_Ekspansi_Industri_Compact.docx  (salinan)
│   └── Metodologi_Bab1_Ekspansi_Industri_Compact.md    (salinan)
├── versicompact/
│   ├── RULES_DOKUMENTASI_COMPACT.md   <-- DOKUMEN INI (Acuan Baku Versi Compact)
│   ├── ref/                           <-- File referensi parsing (PDF & Image lama)
│   ├── bab_1/                         <-- Folder Hasil Bab 1
│   │   ├── generate_bab1_compact.py   <-- Skrip generator python-docx
│   │   ├── Metodologi_Bab1_Ekspansi_Industri_Compact.docx (Tepat 2 Lembar)
│   │   └── Metodologi_Bab1_Ekspansi_Industri_Compact.md
│   ├── bab_2/                         <-- Folder untuk Bab 2 (Next)
│   │   ├── generate_bab2_compact.py
│   │   ├── Metodologi_Bab2_Kualitas_Lingkungan_Compact.docx (Target 2-4 Lembar)
│   │   └── Metodologi_Bab2_Kualitas_Lingkungan_Compact.md
│   └── bab_{X}/                       <-- Folder untuk Bab-Bab Berikutnya
```

---

## 6. Checklist Verifikasi Sebelum Finalisasi Bab

Sebelum suatu bab versi compact dinyatakan tuntas, jalankan verifikasi berikut:

- [ ] **Uji Jumlah Halaman Word:** Jalankan skrip statistik Word COM dan pastikan `Page count` berada di rentang **2 hingga 4 halaman**.
- [ ] **Kesesuaian Header:** Judul `# BAB X: ...` dan penomoran sub-bab (`X.1`, `X.2`, ...) identik dengan file root non-compact.
- [ ] **Bebas Icon:** Tidak ada emoji (`⚠️`, `🔎`, dll.) di seluruh teks maupun tabel.
- [ ] **Bebas Improvisasi:** Tidak ada blok *Humanizing Scale* atau *Caveats* buatan; semua data murni dari metodologi non-compact.
- [ ] **Kelengkapan Rumus & Tabel:** Seluruh formulasi matematika inti dan tabel data primer tersaji lengkap dalam format ringkas.
- [ ] **Sinkronisasi File:** File hasil generate tersedia di `versicompact/bab_{X}/` dan disalin ke `bab_{X}/`.
- [ ] **Git Commit:** Seluruh perubahan di-commit dengan pesan deskriptif.
