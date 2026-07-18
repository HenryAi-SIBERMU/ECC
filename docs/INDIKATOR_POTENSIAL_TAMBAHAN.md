# Indikator Potensial Tambahan
## Dataset yang Bisa Ditambahkan ke Dashboard D3TLH

**Tanggal:** 14 Juni 2026
**Status:** Identifikasi dari raw data yang belum masuk processed

---

## 1. Anggaran Belanja Lingkungan Hidup per Provinsi (2020-2024)

**Sumber:** SLHI 2024 (halaman 327) — sudah ter-extract di `data/raw/klhk_slhi_extracted/SLHI_2024_IKU_extracted.txt`

**Relevansi Checkpoint:** #9 (Kegagalan Tata Kelola)

**Indikator:**
- Anggaran belanja LH per provinsi (juta rupiah), 2020-2024
- Bisa dibandingkan dengan tingkat kerusakan lingkungan → governance gap analysis

**Coverage:** Semua 38 provinsi termasuk 6 Sulawesi

**Status Data:** Sudah ada di extracted text, tinggal parsing

**Potensi Crosstab:**
- Anggaran LH vs Jumlah Izin Tambang → apakah anggaran cukup untuk pengawasan?
- Anggaran LH vs Indeks Kualitas Lingkungan → korelasi spending vs outcome
- Tren anggaran LH vs Tren Kerusakan → apakah budget mengikuti kebutuhan?

---

## 2. IKA per Provinsi (Indeks Kualitas Air)

**Sumber:** SLHI PDFs 2015-2025 (`data/raw/klhk_sulut_kualitas_air/SLHI_*.pdf` dan `data/raw/slhi_historical/SLHI_*.pdf`)

**Relevansi Checkpoint:** #4 (Penurunan Kualitas Lingkungan)

**Indikator:**
- Indeks Kualitas Air (IKA) per provinsi, tahunan
- Nilai komposit parameter kualitas air (pH, DO, BOD, COD, TSS, dll)

**Coverage:** Semua provinsi (di SLHI PDF), tapi baru IKU yang diekstrak

**Status Data:** Masih di dalam PDF, perlu ekstraksi tambahan (Camelot/Tabula)

**Potensi Crosstab:**
- Jumlah Smelter vs IKA → dampak industri terhadap kualitas air
- Investasi Nikel vs IKA → korelasi ekonomi vs pencemaran air
- IKA vs Kasus Diare → dampak kualitas air terhadap kesehatan

---

## 3. IKAL per Provinsi (Indeks Kualitas Air Laut)

**Sumber:** SLHI PDFs 2015-2025

**Relevansi Checkpoint:** #4 (Penurunan Kualitas Lingkungan)

**Indikator:**
- Indeks Kualitas Air Laut (IKAL) per provinsi
- Nilai komposit parameter kualitas air laut

**Coverage:** Provinsi pesisir termasuk semua 6 Sulawesi

**Status Data:** Masih di dalam PDF

**Potensi Crosstab:**
- Jumlah Smelter Pesisir vs IKAL → dampak smelter terhadap laut
- Ekspor Hasil Laut vs IKAL → korelasi pencemaran laut vs produktivitas perikanan

---

## 4. IKL / IKTL per Provinsi (Indeks Kualitas Lahan / Tutupan Lahan)

**Sumber:** SLHI PDFs 2015-2025

**Relevansi Checkpoint:** #4 (Penurunan Kualitas Lingkungan), #8 (Audit D3TLH)

**Indikator:**
- Indeks Kualitas Lahan (IKL) — kualitas tanah/lahan
- Indeks Kualitas Tutupan Lahan (IKTL) — kondisi tutupan hutan & vegetasi

**Coverage:** Semua provinsi

**Status Data:** Masih di dalam PDF

**Potensi Crosstab:**
- Luas Izin Tambang vs IKL → alih fungsi lahan
- Deforestasi vs IKTL → kualitas tutupan lahan menurun?
- IKL vs Konflik Agraria → degradasi lahan memicu konflik?

---

## 5. Status Mutu Air Sungai per Provinsi (Metode STORET)

**Sumber:** SLHI PDFs (ada definisi metode STORET di extracted text)

**Relevansi Checkpoint:** #4 (Penurunan Kualitas Lingkungan)

**Indikator:**
- Klasifikasi mutu air sungai: Kelas A (baik), B (cemar ringan), C (cemar sedang), D (cemar berat)
- Per provinsi, tahunan

**Coverage:** Semua provinsi

**Status Data:** Masih di dalam PDF

**Potensi Crosstab:**
- Smelter di Daerah Aliran Sungai vs Status Mutu Sungai → dampak langsung
- Status Mutu Sungai vs Kasus Penyakit Kulit → kesehatan masyarakat

---

## 6. KPA CATAHU — Statistik Konflik Agraria Agregat (2016-2025)

**Sumber:** 9 PDF CATAHU di `data/raw/kpa_ylbhi_tanahkita/`

**Relevansi Checkpoint:** #6 (Konflik Sosial dan Resistensi)

**Indikator Tambahan (melengkapi tanahkita yang sudah ada):**
- Jumlah konflik agraria per tahun (nasional)
- Luas lahan konflik per tahun
- Jumlah korban kriminalisasi per tahun
- Breakdown per sektor (pertambangan, perkebunan, dll)

**Coverage:** Nasional (bisa di-filter untuk Sulawesi)

**Status Data:** 9 PDF belum di-parse

**Potensi Crosstab:**
- Konflik Sektor Tambang vs Jumlah Izin Tambang → eskalasi konflik seiring izin
- Kriminalisasi vs Ekspansi Industri → pola represi
- Luas Lahan Konflik vs Luas Kawasan Industri → overlap

---

## 7. Data Kesehatan Detail: ISPA, Diare, Kusta, Malaria (2014-2024) ✅ SUDAH DIPROSES

**Sumber:** `data/raw/intermediate_kemenkes/kemenkes_bersih_*.csv`

**Status:** ✅ Sudah masuk processed sebagai:
- `nasional_kesehatan_detail_2014_2024.csv` (1,480 baris)
- `sulawesi_kesehatan_detail_2014_2024.csv` (258 baris)

**Indikator:** ISPA/Pneumonia, Diare, Kusta, Malaria per provinsi per tahun

---

## 8. BPS 1372 (Belum Teridentifikasi)

**Sumber:** `data/raw/bps_1372.html` + `bps_1372.xlsx`

**Status:** Belum dicek isinya

**Action:** Investigasi dulu, tentukan relevansi

---

## Prioritas Eksekusi

| Prioritas | Indikator | Effort | Value |
|:---:|---|:---:|:---:|
| 1 | Anggaran Belanja LH | Mudah (sudah di text) | Tinggi — governance indicator baru |
| 2 | IKA per Provinsi | Sedang (PDF extract) | Tinggi — langsung Checkpoint 4 |
| 3 | IKL/IKTL per Provinsi | Sedang (PDF extract) | Tinggi — land degradation |
| 4 | KPA CATAHU agregat | Sedang (PDF parse) | Sedang — suplemen konflik |
| 5 | IKAL per Provinsi | Sedang (PDF extract) | Sedang — laut/pesisir |
| 6 | Status Mutu Sungai | Sedang (PDF extract) | Sedang — air quality detail |
| 7 | BPS 1372 | Mudah (investigasi) | Rendah — belum tahu isi |
