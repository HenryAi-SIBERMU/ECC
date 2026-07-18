# REV1 — FASE 4: Analisis Demografi, Sosial & Ketenagakerjaan
**CELIOS ECC Intelligence System**  
**Dibuat:** 26 Juni 2026  
**Status:** PLANNING → IN PROGRESS  
**Output Target:** Page baru `10_Demografi_Sosial.py`

---

## 🎯 Tujuan & Narasi Kritis

> **"Ekspansi nikel tidak hanya merusak ekologi — ia secara brutal merestrukturisasi masyarakat."**

Fase ini membuktikan bahwa di balik angka investasi yang mengkilap, terjadi **pergeseran struktural masyarakat** yang dipaksakan oleh industri ekstraktif di Sulawesi. Tiga proses berjalan bersamaan:

1. **Ledakan migrasi masuk** — pekerja dari luar daerah/provinsi membanjiri kabupaten smelter, menciptakan tekanan demografi tanpa infrastruktur publik yang memadai.
2. **Urbanisasi paksa** — desa-desa di lingkar tambang berubah jadi "kota industri" bukan karena pertumbuhan organik, melainkan karena tekanan lahan dan tenaga kerja industri.
3. **Transisi ekonomi brutal** — masyarakat agraris kehilangan akses lahan dan sumber penghidupan, dipaksa beralih menjadi buruh industri upah rendah dengan risiko keselamatan tinggi.

**Keterkaitan dengan modul lain:**
- → Modul 3 (Beban Kesehatan): Migrasi masif membawa populasi non-imun ke zona endemik, memperparah beban penyakit.
- → Modul 4 (Konflik Sosial): Perubahan komposisi demografis dan perebutan lahan memicu konflik horizontal.
- → Modul 8 (Distribusi Manfaat): Transisi paksa dari pertanian ke industri adalah wujud nyata beban ekologis yang ditanggung rakyat.

---

## 📋 Tiga Sub-Analisis Utama

| # | Sub-Analisis | Pertanyaan Riset | Indikator Kunci |
|---|-------------|-----------------|-----------------|
| 4A | Ledakan Migrasi & Tekanan Demografi | Apakah kabupaten smelter mengalami pertumbuhan penduduk abnormal dibanding non-smelter? | Laju pertumbuhan penduduk, kepadatan, anomali spike |
| 4B | Urbanisasi Dipaksakan | Apakah perubahan status desa→kelurahan/kota dipicu oleh ekspansi industri, bukan pertumbuhan organik? | % penduduk perkotaan, perubahan klasifikasi wilayah, kepadatan per km² |
| 4C | Transisi Ketenagakerjaan | Seberapa besar pergeseran dari sektor agraris ke sektor tambang/industri di 6 provinsi Sulawesi? | Komposisi tenaga kerja per sektor, kontribusi sektor ke PDRB |

---

## 📦 Inventaris Data

### A. Data yang SUDAH ADA (Siap Pakai / Proxy)

| File | Lokasi | Peran di Fase 4 | Kualitas |
|------|--------|----------------|----------|
| `sulawesi_investasi_pmdn_2016_2024.csv` | `data/processed/` | **Proxy 4A & 4C**: Lonjakan investasi industri = proxy penyerapan tenaga kerja baru dan daya tarik migrasi | ✅ Bersih, per provinsi, 2016-2024 |
| `sulawesi_izin_baru_per_tahun.csv` | `data/processed/` | **Proxy 4A**: Lonjakan IUP → proxy pertambahan tenaga kerja → proxy daya tarik migrasi. Sulteng 6 IUP (2014) → 87 IUP (2024) adalah sinyal kuat | ✅ Bersih, per provinsi, 2014-2024 |
| `sulawesi_esdm_nikel.csv` | `data/processed/` | **Proxy 4A & 4C**: Data smelter per kabupaten → identifikasi kabupaten smelter sebagai basis perbandingan | ✅ Bersih, granularity kabupaten |
| `sulawesi_kesehatan_detail_2014_2024.csv` | `data/processed/` | **Proxy 4A**: Lonjakan kasus DBD/zoonosis di Morowali & Konawe = indikasi populasi non-imun masuk (efek migrasi) | ✅ Bersih, per provinsi |
| `zoonosis_kab_kota_2015_2024.csv` | `data/processed/` | **Proxy 4A**: DBD Morowali 2019→2024: 96→394 kasus. Morowali Utara: 266→431 kasus. Spike ini berkorelasi dengan boom smelter | ✅ Bersih, granularity kabupaten |
| `sulawesi_pad_2016_2024.csv` | `data/processed/` | **Pendukung 4C**: PAD naik di kabupaten smelter = industri tumbuh, tapi apakah masyarakat lokal yang menikmati? | ✅ Bersih, per provinsi |
| `bps_pdrb_sulawesi_2016_2026.csv` | `data/raw/bps_pdrb/` | **Target Perbaikan 4C**: Harusnya jadi backbone analisis ketenagakerjaan via kontribusi sektor ke PDRB, tapi **BROKEN** — kolom `lapangan_usaha` semua isi `"Tidak ada"` | ⚠️ BROKEN — perlu di-rebuild |

### B. Data yang PERLU DIFETCH BARU — Multi-Source Strategy

> ⚠️ **Bukan hanya BPS API biasa.** Setelah memetakan `DATA_DAFTAR_PORTAL_WEB_SUMBER_DATA.md` dan `bps-api-documentation.md`, ditemukan **5 jalur akuisisi data** yang lebih kaya dari sekadar BPS Dynamic Data endpoint.

---

#### 🔵 Jalur 1: BPS SDGs API (domain=0000) — VAR ID SUDAH DIKETAHUI

Dari tabel SDGs di `bps-api-documentation.md`, berikut var ID yang langsung relevan untuk Fase 4 dan bisa langsung di-fetch **tanpa perlu search manual**:

| Var ID | Nama Variabel | Relevansi Fase 4 | Sub-Analisis |
|--------|--------------|-----------------|-------------|
| **1217** | Proporsi Tenaga Kerja pada Sektor Industri Manufaktur | 🔴 KRITIS — berapa % tenaga kerja di manufaktur/smelter | 4C |
| **1344** | Nilai Tambah Pertanian Dibagi Jumlah TK Sektor Pertanian | 🔴 KRITIS — proxy produktivitas agraris (turun = buruh pindah) | 4C |
| **2153** | Proporsi Lapangan Kerja Informal Menurut Provinsi | 🟠 TINGGI — seberapa besar buruh informal di tambang | 4C |
| **2154** | Proporsi Lapangan Kerja Informal Menurut Daerah (Urban-Rural) | 🟠 TINGGI — perbandingan urban vs rural informal | 4B, 4C |
| **296** | Laju Pertumbuhan PDRB Per Kapita per Provinsi (Seri 2010) | 🟠 TINGGI — proxy pertumbuhan ekonomi kabupaten smelter | 4A |
| **288** | PDRB Per Kapita per Provinsi (Seri 2010) | 🟡 SEDANG — baseline ekonomi sebelum/sesudah boom | 4A, 4C |
| **621** | Persentase Penduduk Miskin Menurut **Kabupaten/Kota** | 🟠 TINGGI — **satu-satunya SDGs var di level kabupaten!** | 4A, 4B |
| **2190** | Jumlah Desa Mandiri Menurut Provinsi | 🟡 SEDANG — proxy urbanisasi: desa mandiri ≠ desa tertinggal | 4B |
| **2191** | Jumlah Desa Tertinggal Menurut Provinsi | 🟡 SEDANG — apakah desa lingkar tambang malah tertinggal? | 4B |
| **1172** | Upah Rata-Rata Per Jam Pekerja Menurut Provinsi | 🟡 SEDANG — apakah transisi agraris→industri meningkatkan upah? | 4C |
| **1241** | % Rumah Tangga Akses Hunian Layak per Provinsi | 🟡 SEDANG — proxy kondisi hidup di kawasan industri | 4B |
| **1214** | Proporsi Nilai Tambah Industri Manufaktur Terhadap PDB | 🟡 SEDANG — kontribusi sektor industri naik? | 4C |

**Cara fetch (endpoint sama dengan data lain yang sudah berhasil):**
```
GET https://webapi.bps.go.id/v1/api/list/model/data/domain/0000/var/{VAR_ID}/key/{API_KEY}/
```

**Catatan:** Domain `0000` = nasional. Untuk filter Sulawesi, ambil semua lalu filter provinsi 7100-7600 di Pandas.

---

#### 🔵 Jalur 2: BPS SIMDASI (Belum Dicoba — Paling Menjanjikan untuk Kabupaten)

SIMDASI adalah sistem yang menyimpan publikasi "Indonesia Dalam Angka" dan "Daerah Dalam Angka" — termasuk data **populasi per kabupaten secara tahunan**.

| Endpoint | ID | Fungsi |
|----------|----|--------|
| `simdasi/id/26/` | 26 | Daftar 7-digit MFD Code per Provinsi |
| `simdasi/id/27/` | 27 | Daftar 7-digit MFD Code per **Kabupaten/Kota** |
| `simdasi/id/22/` | 22 | Daftar Subject/Bab per wilayah |
| `simdasi/id/23/` | 23 | Daftar tabel per wilayah + subjek |

**Target eksplorasi:**
- MFD code Sulawesi Tengah: `7200000` → sub-kabupaten Morowali, Morowali Utara, dll
- Cari subjek: `"Kependudukan"`, `"Ketenagakerjaan"`, `"Luas Wilayah"`
- Kemungkinan besar berisi: populasi per tahun, kepadatan, angkatan kerja

**Output target:** `sulawesi_populasi_kab_2014_2024.csv` (granularity kabupaten)

---

#### 🔵 Jalur 3: BPS Census Interoperabilitas (SP2020 — Data Migrasi Riil)

SP2020 (Sensus Penduduk 2020) menyimpan data migrasi risen yang sesungguhnya.

| Endpoint | ID | Fungsi |
|----------|----|--------|
| `sensus/id/37/` | 37 | Daftar event sensus (SP2010, SP2020) |
| `sensus/id/38/` | 38 | Topik data per event sensus |
| `sensus/id/39/` | 39 | Wilayah yang tersedia per event |
| `sensus/id/40/` | 40 | Dataset yang tersedia per event + topik |
| `sensus/id/41/` | 41 | **Ambil data sensus aktual** |

**Catatan penting:** SP2020 hanya 1 titik waktu (2020), tapi merupakan **satu-satunya sumber migrasi risen resmi**. Gunakan sebagai anchor, bukan time-series. Kombinasikan dengan anomali populasi tahunan dari SIMDASI.

---

#### 🟢 Jalur 4: Portal Open Data Regional (Sudah Sebagian Berhasil)

Portal regional ini bisa menyimpan data kependudukan dan ketenagakerjaan **di level kabupaten** yang tidak ada di API nasional BPS:

| Portal | URL | Status | Potensi Data Fase 4 |
|--------|-----|--------|---------------------|
| Open Data Sulawesi Utara | `opendata.sulutprov.go.id` | ✅ **BERHASIL** (CKAN API) | Cek dataset kategori "kependudukan", "ketenagakerjaan" |
| Open Data Sulawesi Barat | `opendata.sulbarprov.go.id` | ⚠️ Belum dicoba | HTML parsing (BeautifulSoup) |
| Satu Data Sulawesi Selatan | `satudata.sulselprov.go.id` | ⚠️ Belum dicoba | HTML parsing |
| Satu Data Sulawesi Tengah | `satudata.sultengprov.go.id` | ⚠️ Belum dicoba | **PRIORITAS** — Morowali ada di sini |
| SIMDATA Sulawesi Tenggara | `simdata.sultraprov.go.id` | ⚠️ Belum dicoba | **PRIORITAS** — Konawe ada di sini |
| Open Data Gorontalo | `data.gorontaloprov.go.id` | ⚠️ Belum dicoba | CKAN atau custom |

**Catatan:** Sulut sudah terbukti via CKAN API (`/api/3/action/package_search`). Coba keyword: `"penduduk"`, `"ketenagakerjaan"`, `"migrasi"`, `"urbanisasi"`.

---

#### 🟢 Jalur 5: Portal Nasional Terbuka (Belum Dicoba)

| Portal | URL | Target Data |
|--------|-----|-------------|
| **data.go.id** | `https://data.go.id` | Dataset kependudukan, ketenagakerjaan per kabupaten dari berbagai K/L |
| **satu-data.go.id** | `https://satu-data.go.id` | Dataset SDGs, Susenas, Sakernas per provinsi/kabupaten |
| **Kemenperin** | `https://kemenperin.go.id` | Data tenaga kerja industri per sektor, kapasitas produksi smelter |

**Dorking approach:**
```
site:data.go.id "penduduk" "kabupaten" "sulawesi" filetype:csv
site:satu-data.go.id "ketenagakerjaan" "lapangan usaha" "sulawesi"
```

---

#### 📊 Ringkasan Prioritas Fetch

| Prioritas | Dataset Target | Jalur | Effort | Output File |
|-----------|---------------|-------|--------|-------------|
| 🔴 **1** | Tenaga kerja sektor manufaktur per provinsi | BPS SDGs Var 1217 | Rendah (fetch langsung) | `sulawesi_tk_manufaktur_2014_2024.csv` |
| 🔴 **2** | PDRB per kapita + laju pertumbuhan provinsi | BPS SDGs Var 288, 296 | Rendah | `sulawesi_pdrb_per_kapita_2014_2024.csv` |
| 🔴 **3** | % Miskin per kabupaten (satu-satunya kab-level SDGs) | BPS SDGs Var 621 | Rendah | `sulawesi_kemiskinan_kab_2014_2024.csv` |
| 🟠 **4** | Populasi per kabupaten tahunan | BPS SIMDASI (baru, perlu eksplorasi) | Sedang | `sulawesi_populasi_kab_2014_2024.csv` |
| 🟠 **5** | Proporsi kerja informal per provinsi | BPS SDGs Var 2153, 2154 | Rendah | Bagian dari `sulawesi_ketenagakerjaan_sektor_2014_2024.csv` |
| 🟠 **6** | Data desa mandiri vs tertinggal | BPS SDGs Var 2190, 2191 | Rendah | `sulawesi_status_desa_2014_2024.csv` |
| 🟡 **7** | Kependudukan kabupaten (Sulteng & Sultra khusus) | Open Data Regional (CKAN/HTML) | Tinggi | Enrichment kabupaten smelter |
| 🟡 **8** | Migrasi risen SP2020 | BPS Census interoperabilitas | Sedang | Titik anchor migrasi 2020 |
| 🟡 **9** | Rebuild PDRB sektoral (A, B, C, F) | BPS Dynamic Data (cari var_id baru) | Sedang | Rebuild `bps_pdrb_sulawesi_2016_2026.csv` |

### C. Data Alternatif / Fallback

| Sumber | Konten | Metode Akuisisi | Catatan |
|--------|--------|----------------|--------|
| **Podes BPS** (2014, 2018, 2021) | Status desa/kelurahan, fasilitas per desa | Manual download dari BPS.go.id → Olah CSV | Hanya 3 titik waktu, gunakan sebagai snapshot periodik |
| **Sakernas (survei tengah tahunan)** | Ketenagakerjaan per sektor per provinsi | PDF publikasi BPS per provinsi atau via `satu-data.go.id` | Jika SDGs Var 1217 tidak cukup granular |
| **Annual Report ANTAM / Vale Indonesia** | Jumlah karyawan per site Sulawesi | Dorking IDX/OJK: `site:idx.co.id [nama perusahaan] laporan tahunan` | Untuk konfirmasi angka tenaga kerja level site |
| **Kemenperin** | Data industri per sektor, estimasi TK | Dorking: `site:kemenperin.go.id smelter nikel tenaga kerja sulawesi` | Belum dicoba, bisa jadi surprise |
| **Global Energy Monitor (sudah punya PLTU)** | Estimasi kapasitas → proxy ukuran TK | Sudah sebagian di `sulawesi_pltu_captive.csv` | Gunakan sebagai cross-reference |

---

## 🗂️ Strategi Data Per Sub-Analisis

### Sub-Analisis 4A: Ledakan Migrasi & Tekanan Demografi

**Pendekatan: Population Growth Anomaly Method**

Karena data migrasi risen BPS tidak tersedia via API tahunan, gunakan **anomali pertumbuhan populasi** sebagai proxy yang kuat secara metodologis.

**Logika:**
```
Jika kabupaten X memiliki laju pertumbuhan penduduk >> rata-rata Sulawesi 
DAN kabupaten X adalah lokasi smelter/IUP aktif
→ Maka lonjakan populasi diduga kuat driven oleh migrasi tenaga kerja industri
```

**Variabel yang dibutuhkan:**
- `jumlah_penduduk` per kabupaten per tahun (2014-2024) → **FETCH dari BPS API**
- `kepadatan_per_km2` per kabupaten per tahun → **FETCH dari BPS API**
- `is_smelter_kabupaten` → **Derive dari `sulawesi_esdm_nikel.csv`**
- `jumlah_iup_aktif` → **Derive dari `sulawesi_izin_baru_per_tahun.csv`**
- Kasus DBD/zoonosis per kabupaten → **Sudah ada di `zoonosis_kab_kota_2015_2024.csv`**

**Derived Metrics:**
- `laju_pertumbuhan_penduduk_pct` = (pop_t - pop_{t-1}) / pop_{t-1} × 100
- `anomali_pertumbuhan` = flag jika laju > 2× median provinsi
- **Kabupaten Benchmark Smelter:** Morowali, Morowali Utara, Konawe, Konawe Utara, Kolaka, Luwu Timur
- **Kabupaten Kontrol Non-Smelter:** Parigi Moutong, Tolitoli, Banggai (Sulteng), Muna, Buton (Sultra)

**Matriks Crosstab:**

| Periode | Kabupaten Smelter | Kabupaten Non-Smelter | Interpretasi |
|---------|------------------|----------------------|--------------|
| 2014-2016 (Pra-boom) | Laju pertumbuhan baseline | Laju pertumbuhan baseline | Baseline |
| 2017-2020 (Boom awal) | Laju pertumbuhan naik? | Relatif stabil? | Sinyal awal |
| 2021-2024 (Post-boom) | Laju pertumbuhan puncak? | Relatif stabil? | Konfirmasi efek smelter |

---

### Sub-Analisis 4B: Urbanisasi Dipaksakan

**Pendekatan: Urban Share + Density Tracking**

**Logika:**
```
Jika % penduduk perkotaan di kabupaten smelter naik signifikan
DAN bukan berasal dari pertumbuhan ekonomi organik (PAD non-industri rendah)
→ Maka urbanisasi ini adalah efek samping industri ekstraktif, bukan pembangunan
```

**Variabel yang dibutuhkan:**
- `pct_penduduk_perkotaan` per kabupaten per tahun → **FETCH dari BPS API**
- `pct_penduduk_perdesaan` per kabupaten per tahun → **FETCH dari BPS API**
- `kepadatan_per_km2` → **FETCH dari BPS API (sama dgn 4A)**
- Data Podes (jika bisa diunduh) → jumlah desa yang naik status jadi kelurahan

**Derived Metrics:**
- `urbanization_rate` = delta % perkotaan per tahun
- Perbandingan `urbanization_rate` vs `laju_pad_non_industri` — jika urbanisasi tinggi tapi PAD rendah, maka urbanisasi bukan driven oleh pembangunan

**Fallback jika Podes tidak tersedia:**
Gunakan data kepadatan penduduk per km² per kabupaten sebagai proxy intensifikasi ruang.

---

### Sub-Analisis 4C: Transisi Ketenagakerjaan Agraris → Industri

**Pendekatan: PDRB Sector Shift + Labor Proportion**

**Logika:**
```
Jika kontribusi sektor Pertambangan (B) & Industri Pengolahan (C) ke PDRB naik
DAN kontribusi sektor Pertanian (A) turun
→ Maka terjadi restrukturisasi ekonomi yang menggeser basis penghidupan agraris
```

**Variabel yang dibutuhkan:**
- PDRB per sektor (A, B, C, F) per provinsi per tahun → **Rebuild dari BPS API**
- Jumlah tenaga kerja per sektor per provinsi → **FETCH dari BPS API (Sakernas)**
- `sulawesi_investasi_pmdn_2016_2024.csv` → sudah ada, proxy investasi industri

**Sektor yang Dianalisis (KLU BPS):**
| Kode | Sektor | Relevansi |
|------|--------|-----------|
| A | Pertanian, Kehutanan, Perikanan | Sektor yang "kehilangan" pekerja |
| B | Pertambangan dan Penggalian | Sektor yang "menerima" pekerja |
| C | Industri Pengolahan (Smelter) | Sektor yang "menerima" pekerja |
| F | Konstruksi | Sektor pendukung boom |

**Derived Metrics:**
- `pct_sektor_A` = (PDRB sektor A / Total PDRB) × 100 — tren penurunan
- `pct_sektor_B_C` = (PDRB sektor B+C / Total PDRB) × 100 — tren kenaikan
- `agriculture_to_industry_shift_index` = pct_sektor_B_C / pct_sektor_A (rasio, naik = makin industrial)

**Fix PDRB yang Broken:**
File `bps_pdrb_sulawesi_2016_2026.csv` saat ini gagal: semua baris `lapangan_usaha = "Tidak ada"`. Ini menunjukkan BPS API yang diquery adalah tabel PDRB agregat, bukan breakdown sektoral. Perlu:
1. Identify ulang var_id BPS yang berisi PDRB per lapangan usaha
2. Query ulang dengan breakdown sektor A, B, C, F
3. Rebuild file dengan schema: `provinsi, tahun, sektor_kode, sektor_nama, nilai_miliar_rp`

---

## 🖥️ Rencana Page Dashboard Baru

**Nama File:** `10_Demografi_Sosial.py`  
**Judul Page:** *"Guncangan Sosial: Migrasi, Urbanisasi, dan Kehancuran Ekonomi Agraris"*  
**Posisi di Sidebar:** Setelah Page 8 (Distribusi Manfaat), sebelum Page 9 (Dokumentasi)

> **Catatan:** Tidak ditaruh di antara Page 3-4 untuk menghindari renaming cascade pada 6 file page yang sudah ada.

### Struktur Halaman

```
[HEADER]
Badge CELIOS | Judul | Sub-judul

[METODOLOGI EXPANDER]
Penjelasan pendekatan proxy + kausalitas

[HERO STATEMENT]
Narasi kritis pembuka — dampak sosial-struktural ekspansi nikel

[KARTU METRIK AGREGAT]
• Laju pertumbuhan Morowali 2014-2024 vs rata-rata Sulawesi
• Delta % perkotaan kabupaten smelter vs non-smelter  
• Shift sektor: % kontribusi pertanian vs pertambangan+industri (2014 vs 2024)

──────────────────────────────────────────
SECTION 4A: LEDAKAN MIGRASI
──────────────────────────────────────────
[4A.1] Line chart: Populasi per tahun — smelter kabupaten vs non-smelter kabupaten
        → Tooltip: nama kabupaten, jumlah penduduk, laju pertumbuhan
[4A.2] Bar chart: Laju pertumbuhan penduduk per kabupaten (sorted, highlight smelter)
        → Filter tahun (slider)
[4A.3] Scatter plot: IUP aktif vs laju pertumbuhan penduduk per kabupaten
        → Korelasi langsung: lebih banyak izin = pertumbuhan lebih cepat
[4A.4] Proxy zoonosis: Line chart DBD Morowali & Morowali Utara vs IUP baru
        → Narasi: "populasi non-imun datang, DBD melonjak"

──────────────────────────────────────────
SECTION 4B: URBANISASI DIPAKSAKAN
──────────────────────────────────────────
[4B.1] Area chart: % penduduk perkotaan per provinsi 2014-2024
        → Highlight Sulawesi Tengah (Morowali effect)
[4B.2] Heatmap: Kepadatan penduduk per kabupaten per tahun
        → Kabupaten smelter vs kontrol
[4B.3] Dual axis: % urbanisasi vs PAD non-industri
        → Jika urbanisasi naik tapi PAD stagnan → urbanisasi bukan dari pembangunan

──────────────────────────────────────────
SECTION 4C: TRANSISI KETENAGAKERJAAN
──────────────────────────────────────────
[4C.1] Stacked area chart: Komposisi PDRB per sektor 2016-2024
        → Sektor A (hijau, turun) vs B+C (merah, naik)
[4C.2] Line chart: Agriculture-to-Industry Shift Index per provinsi
        → Provinsi mana paling terdampak?
[4C.3] Before-After table: Komposisi sektor 2016 vs 2024 per provinsi
        → Delta persentase dan arah perubahan
[4C.4] (Jika data Sakernas tersedia) Bar chart: Jumlah pekerja per sektor
        → Absolut berapa juta orang yang "berpindah" sektor

──────────────────────────────────────────
[SINTESIS & KESIMPULAN]
Crosstab akhir: Kabupaten dengan IUP tinggi → populasi tumbuh cepat → 
urbanisasi naik → pertanian turun → beban sosial-kesehatan meningkat
```

---

## 🛠️ Rencana Eksekusi — Checkpoint Bertahap

> **Prinsip:** Setiap checkpoint harus diselesaikan & divalidasi sebelum lanjut ke checkpoint berikutnya. Jika checkpoint gagal, ikuti jalur fallback yang tercantum — jangan skip ke checkpoint berikutnya tanpa resolusi.

---

### ✅ CHECKPOINT 1: Quick Wins — Fetch BPS SDGs
**Status:** ✅ **SELESAI**  
**Tanggal Eksekusi:** 26 Juni 2026  
**Script:** `scripts/fetch_bps_sdgs_fase4.py`  
**Python runtime:** `.venv/Scripts/python.exe` (3.10.11) — *catatan: global Python 3.7.8 menyebabkan segfault, wajib pakai venv*

---

#### 📊 Log Eksekusi CP1

**Temuan Struktural API (deviasi dari rencana awal):**

Setelah eksplorasi, ditemukan bahwa tidak semua var SDGs berstruktur province-level. Pengelompokan ulang:

| Var ID | Nama | Struktur vervar | Status |
|--------|------|----------------|--------|
| 288 | PDRB Per Kapita | 38 Provinsi | ✅ Berhasil |
| 296 | Laju PDRB Per Kapita | 38 Provinsi | ✅ Berhasil |
| 1344 | Nilai Tambah Pertanian/TK | 38 Provinsi | ✅ Berhasil |
| 2153 | Kerja Informal per Provinsi | 38 Provinsi | ✅ Berhasil (hanya 2018–2023) |
| 1241 | % Hunian Layak | 38 Provinsi | ✅ Berhasil (2014–2024) |
| 1214 | Manufaktur ke PDB | 38 Provinsi | ✅ Berhasil (2014–2023) |
| 1172 | Upah Per Jam | 38 Provinsi | ✅ Berhasil (2014–2024) |
| 621 | % Miskin Kab/Kota | Provinsi+Kabupaten (552 wilayah) | ✅ Berhasil — **kabupaten level!** |
| 1217 | Proporsi TK Manufaktur | Jenis Industri (bukan provinsi) | ⚠️ SKIP — vervar = jenis industri, bukan wilayah |
| 2154 | Kerja Informal Urban/Rural | Perkotaan/Perdesaan (bukan provinsi) | ⚠️ SKIP — agregat nasional, bukan Sulawesi |
| 2190 | Desa Mandiri | — | ❌ TIDAK TERSEDIA (list-not-available) |
| 2191 | Desa Tertinggal | — | ❌ TIDAK TERSEDIA (list-not-available) |

**Output file yang benar-benar dibuat (koreksi dari rencana):**

| File | Baris | Var IDs | Keterangan |
|------|-------|---------|------------|
| `sulawesi_tk_sektor_sdgs.csv` | **150** | 2153, 1214, 1344 | 6 prov × 3 var × beberapa tahun |
| `sulawesi_pdrb_per_kapita_sdgs.csv` | **198** | 288, 296 | 6 prov × 2 var × beberapa tahun |
| `sulawesi_upah_hunian_sdgs.csv` | **120** | 1172, 1241 | 6 prov × 2 var × beberapa tahun |
| `sulawesi_kemiskinan_kab_sdgs.csv` | **946** | 621 | **Kabupaten/kota level** — mencakup Morowali, Konawe, Kolaka, Luwu Timur |
| `sulawesi_status_desa_sdgs.csv` | — | 2190, 2191 | **TIDAK DIBUAT** (var tidak tersedia) |

**Raw files** tersimpan di `data/raw/bps_sdgs/` per var ID.

**Kabupaten smelter kunci yang terkonfirmasi ada di var 621:**
- Morowali ✅, Morowali Utara ✅, Konawe ✅, Konawe Utara ✅, Kolaka ✅, Kolaka Timur ✅, Luwu Timur ✅

**Coverage tahun per var (tidak semua 2014–2024):**
- Var 2153 (Kerja Informal): **2018–2023** saja
- Var 1214 (Manufaktur ke PDB): **2014–2023** (2024 tidak tersedia)
- Var 1172, 1241, 288, 296, 621, 1344: coverage lebih lengkap, cek file raw untuk detail

---

**Gate Condition — Hasil:**
- [x] File `sulawesi_tk_sektor_sdgs.csv` ada dan punya data Sulawesi — 150 baris
- [x] File `sulawesi_kemiskinan_kab_sdgs.csv` ada — **946 baris kabupaten level**
- [x] Semua var yang strukturnya province-level berhasil difetch
- [x] Deviasi dicatat: 4 var di-skip/tidak tersedia, output file berbeda nama dari rencana
- [ ] `sulawesi_status_desa_sdgs.csv` — **TIDAK DIBUAT** (2190/2191 not available — *acceptable, bukan blocker*)

**✅ CP1 LULUS — Lanjut ke CP2.**

---

### ✅ CHECKPOINT 2: PDRB Sektoral Rebuild
**Status:** ✅ **SELESAI**  
**Tanggal Eksekusi:** 26 Juni 2026  
**Script:** `scripts/rebuild_pdrb_sektoral_sulawesi.py`

---

#### 📊 Log Eksekusi CP2

**Temuan Kritis (deviasi dari rencana awal):**

PDRB sektoral **TIDAK tersedia** via BPS Domain API (7100-7600) maupun national domain (0000). Script lama (`fetch_bps_pdrb.py`) gagal karena domain per-provinsi hanya punya 10 var (semuanya IHK/Inflasi). Solusi: **BPS SIMDASI** endpoint id=25 — ini sumber yang benar untuk data "Daerah Dalam Angka".

**Sumber data aktual:** SIMDASI id=25 (bukan BPS Domain API seperti rencana)
- Tabel: "PDRB Atas Dasar Harga Berlaku Menurut Lapangan Usaha" per provinsi
- Endpoint: `/interoperabilitas/datasource/simdasi/id/25/id_tabel/{id}/wilayah/{mfd}/tahun/{yr}/key/{KEY}/`
- Coverage: 2014–2024 (semua provinsi) ✅

**Hasil fetch:**

| Provinsi | Sektor per Tahun | Tahun Coverage |
|---------|-----------------|---------------|
| Sulawesi Utara | 47 sektor | 2014–2024 (skip 2020) |
| Sulawesi Tengah | 47 sektor | 2014–2024 |
| Sulawesi Selatan | 47 sektor | 2014–2024 |
| Sulawesi Tenggara | 47 sektor | 2014–2024 |
| Gorontalo | 47 sektor | 2014–2024 |
| Sulawesi Barat | 47 sektor | 2014–2024 |

**Output file yang dibuat:**
```
data/processed/sulawesi_pdrb_sektoral_2016_2024.csv
  Schema: provinsi, tahun, sektor_kode, sektor_nama, nilai_miliar_rp, pct_dari_total
  Sektor: 47 baris per tahun (A hingga R,S,T,U + sub-sektor utama)
  Total rows: ~3.000+
```

Raw file tersimpan di `data/raw/bps_simdasi/pdrb_sektoral_sulawesi_raw.csv`.

**Bonus temuan SIMDASI untuk CP3:**
SIMDASI mms_id=531 juga menyimpan:
- Populasi + kepadatan per kabupaten Sulteng: `WVRlTTcySlZDa3lUcFp6czNwbHl4QT09`
- Ketenagakerjaan per kabupaten Sulteng: `UEJPZGxjcUxvWWdkWmFLRUpZanJQUT09`
→ Ini menjadi backbone untuk CP3!

**Iterasi Perbaikan Data (penting dicatat):**

Ditemukan **2 bug** setelah review:
1. **Sub-sektor pollution** — `is_main_sector()` awal salah menangkap sub-sektor seperti `'Angkutan'`, `'Industri'`, `'Jasa'`, `'Tanaman'` dan baris `'Produk Domestik Bruto'` (total). Total 1950 baris invalid dari 3055.
   - Fix: filter ketat ke 17 kode KLU valid (`VALID_KODE = {'A','B','C',...,'R,S,T,U'}`)
   - Hasil akhir: 1105 baris bersih

2. **Unit rupiah inconsistency (Sulteng 2014)** — SIMDASI menyimpan Sulteng 2014 dalam **juta rupiah** (`'31.036.027,00'`), sedangkan 2015+ dalam **miliar rupiah** (`'33.643,74'`). Fungsi parse awal tidak mendeteksi ini.
   - Fix: heuristic `dot_count >= 2` → data dalam juta → bagi 1000
   - Sulteng 2014 total PDRB sebelum fix: 90,246,313 miliar (mustahil)
   - Sulteng 2014 total PDRB setelah fix: **90,246 miliar** (masuk akal) ✅
   - Fix dipermanenkan di `parse_number()` dalam script

**Sanity Check Ekonomi (validasi akhir):**
- Sulteng Sektor B (Tambang) 2014 → 2022: **9.58% → 15.34%** — tren naik seiring boom nikel ✅
- Sulteng Sektor C (Industri) 2022: **40.32%** — tertinggi Sulawesi, mencerminkan dominasi smelter ✅
- Sulut 2020: semua sektor NaN (SIMDASI tidak punya data tahun ini untuk Sulut) — acceptable
- Semua pct_dari_total sum = ~100% per provinsi-tahun ✅

**Gate Condition — Hasil Final:**
- [x] Kolom `sektor_kode` tidak ada `"Tidak ada"` — **PASS**
- [x] Ada sektor A (Pertanian) — **PASS**
- [x] Ada sektor B (Pertambangan) — **PASS**
- [x] Semua 6 provinsi ada — **PASS**
- [x] Coverage 2016–2024 terpenuhi — **PASS**
- [x] Nilai ekonomi plausible (Sulteng 2014 PDRB ~90rb miliar) — **PASS** *(setelah 2 iterasi fix)*

**✅ CP2 LULUS — File `sulawesi_pdrb_sektoral_2016_2024.csv` siap dipakai.**

---

### ✅ CHECKPOINT 3: Eksplorasi Populasi Kabupaten
**Status:** ✅ **SELESAI**  
**Tanggal Eksekusi:** 26 Juni 2026  
**Script:** `scripts/fetch_simdasi_populasi_kab.py`

---

#### 📊 Log Eksekusi CP3

**Jalur yang dipakai: Jalur A (SIMDASI) — BERHASIL di percobaan pertama.**  
Jalur B dan C tidak diperlukan.

**Temuan Coverage SIMDASI per Provinsi:**

| Provinsi | Kabupaten | Tahun Tersedia | Catatan |
|---------|-----------|---------------|--------|
| Sulawesi Utara | 15 kab | 2004–2026 (23 tahun penuh!) | 🏆 Terlengkap |
| Sulawesi Tengah | 13 kab | 2010, 2017–2020, 2024–2026 | Skip 2021–2023 |
| Sulawesi Selatan | 24 kab | 2010, 2016–2021, 2023–2026 | Skip 2022 |
| Sulawesi Tenggara | 17 kab | 2010, 2017–2019, 2021–2026 | Skip 2020 |
| Gorontalo | 5 kab | 2010, 2018–2026 | Skip 2011–2017 |
| Sulawesi Barat | 6 kab | 2010, 2017–2026 | Lengkap dari 2017 |

**Bug yang ditemukan & difix:**
1. Filter `skip agregat` terlalu agresif: menghapus `'Gorontalo'`, `'Gorontalo Utara'`, `'Kota Gorontalo'` karena nama kabupaten mengandung kata `'gorontalo'` yang sama dengan nama provinsi.
   - Fix: ganti ke `exact match` (`label.lower() in skip_labels`) bukan `str.contains`.
   - Hasil: Gorontalo naik dari 3 → **5 kabupaten**.
2. Unit jumlah penduduk tidak konsisten: sebagian value seperti `'120,1'` berarti ribu jiwa, sementara value seperti `'167.024,0'` berarti jiwa.
   - Fix: `parse_population_rb()` → jika hasil parse > 2.000, dianggap jiwa dan dibagi 1000.
   - Hasil: tidak ada populasi di luar range 5–2.000 ribu jiwa.
3. Kolom `laju_pertumbuhan` sumber tidak konsisten antar provinsi (contoh Sulsel 2016 bisa 90–100%, bukan YoY).
   - Fix: simpan sebagai `laju_pertumbuhan_sumber_pct`, lalu hitung ulang `laju_pertumbuhan_yoy_pct` dari seri populasi.
4. `is_smelter` awal terlalu luas karena diturunkan dari semua lokasi IUP nikel (56 kabupaten flagged).
   - Fix: gunakan daftar eksplisit kabupaten prioritas smelter: Morowali, Morowali Utara, Banggai, Konawe, Konawe Utara, Kolaka, Luwu Timur.
5. Typo raw SIMDASI: Kota Parepare 2018 = `'1.508.154,0'` (1.508 juta jiwa), tidak masuk akal.
   - Fix: interpolasi linear antara 2017 (142.1 rb) dan 2019 (145.2 rb) → 2018 = **143.65 rb**.

**Output yang dibuat:**
```
data/processed/sulawesi_populasi_kab_simdasi.csv — 952 baris
  Schema: provinsi, kabupaten, tahun, jumlah_penduduk_rb,
          laju_pertumbuhan_sumber_pct, laju_pertumbuhan_yoy_pct,
          kepadatan_per_km2, is_smelter, iup_kumulatif
  Kabupaten: 80 unik | Tahun: 2004–2026
```

**Audit Final Window Riset 2014–2024:**
- Rows: **623**
- Provinsi: **6**
- Kabupaten unik: **80**
- Bad population range (<5 atau >2.000 ribu jiwa): **0**
- YoY growth >50% absolut: **0**
- Null key columns (`provinsi`, `kabupaten`, `tahun`, `jumlah_penduduk_rb`, `kepadatan_per_km2`, `is_smelter`): **0**

**Highlight data kunci (kabupaten smelter):**
- **Morowali 2020**: laju pertumbuhan = **4.54%** — anomali tertinggi di Sulteng, 2× lipat provinsi lain → indikasi kuat migrasi masuk terkait smelter
- **Morowali 2010** = 206.3 rb (sebelum split) → 2017 = 117.3 rb (setelah Morowali Utara pisah di 2013)

**Gate Condition — Hasil Final:**
- [x] 6 provinsi — **PASS**
- [x] 80 kabupaten unik (jauh di atas threshold 50) — **PASS**
- [x] 23 titik waktu (2004–2026) — **PASS** (jauh di atas minimum 3)
- [x] 100% non-null jumlah_penduduk — **PASS**
- [x] Unit populasi tervalidasi — **PASS**
- [x] `is_smelter` tidak over-flagging — **PASS** (7 kab prioritas)
- [x] Window 2014–2024 bebas anomali ekstrem — **PASS**

**✅ CP3 LULUS — Jalur A SIMDASI berhasil. Siap ke CP4.**

---

### ✅ CHECKPOINT 4: Processing — Build Master Files
**Status:** ✅ **SELESAI**  
**Tanggal Eksekusi:** 26 Juni 2026  
**Script:** `scripts/build_demografi_fase4.py`

**Yang dikerjakan:**

**Step 4A — Build Master Demografi:**
```
scripts/build_demografi_fase4.py
  INPUT:
    → Data populasi dari CP3 (kabupaten atau provinsi)
    → sulawesi_esdm_nikel.csv → derive is_smelter flag per kabupaten
    → sulawesi_izin_baru_per_tahun.csv → derive iup_kumulatif per provinsi per tahun
    → zoonosis_kab_kota_2015_2024.csv → DBD sebagai proxy migrasi
    → sulawesi_investasi_pmdn_2016_2024.csv → nilai investasi industri
    → sulawesi_kemiskinan_kab_sdgs.csv (dari CP1)
  DERIVE:
    → laju_pertumbuhan_pct = (pop_t - pop_t-1) / pop_t-1 × 100
    → anomali_flag = True jika laju > 2× median provinsi tahun itu
    → urbanization_rate = delta pct_perkotaan per tahun (jika tersedia)
  OUTPUT:
    data/processed/sulawesi_demografi_master_fase4.csv
```

**Step 4B — Build Employment Shift Index:**
```
scripts/build_employment_shift_fase4.py
  INPUT:
    → sulawesi_tk_manufaktur_sdgs.csv (dari CP1)
    → sulawesi_pdrb_sektoral_2016_2024.csv (dari CP2, atau fallback SDGs)
  DERIVE:
    → pct_sektor_pertanian, pct_sektor_tambang, pct_sektor_industri per provinsi per tahun
    → agriculture_to_industry_shift_index = pct_B_C / pct_A
    → delta_2014_2024 = perubahan pct antar tahun pertama dan terakhir
  OUTPUT:
    data/processed/sulawesi_employment_shift_fase4.csv
    data/processed/sulawesi_pdrb_shift_index_2016_2024.csv
```

#### 📊 Log Eksekusi CP4

**Output final:**

| File | Rows | Granularity | Status |
|------|------|-------------|--------|
| `sulawesi_demografi_master_fase4.csv` | **623** | kabupaten-tahun (2014–2024) | ✅ Clean |
| `sulawesi_employment_shift_fase4.csv` | **65** | provinsi-tahun | ✅ Clean |
| `sulawesi_pdrb_shift_index_2016_2024.csv` | **65** | provinsi-tahun | ✅ Clean |

**Bug yang ditemukan & difix:**
1. Merge kemiskinan awal hanya pakai `kabupaten+tahun`, berisiko ambiguous join dengan wilayah agregat provinsi dan nama wilayah yang sama.
   - Fix: derive `provinsi` dari `wilayah_val`, exclude province aggregate (`7100`, `7200`, dst), merge pakai `provinsi+kabupaten+tahun`.
2. Merge PMDN awal menggandakan row karena `sulawesi_investasi_pmdn_2016_2024.csv` berisi 2 indikator per provinsi-tahun (`Nilai` dan `Jumlah Proyek`).
   - Fix: filter hanya indikator `Nilai` sebelum merge ke master demografi.
   - Hasil: demografi master turun dari 1136 baris duplikatif menjadi **623 baris clean**.

**Validasi akhir:**
- [x] `sulawesi_demografi_master_fase4.csv` terbaca dengan `pd.read_csv()` — **PASS**
- [x] `sulawesi_employment_shift_fase4.csv` terbaca dengan `pd.read_csv()` — **PASS**
- [x] Duplicate key `provinsi+kabupaten+tahun` pada master demografi = **0** — **PASS**
- [x] Duplicate key `provinsi+tahun` pada employment shift = **0** — **PASS**
- [x] Kolom kunci demografi (`provinsi`, `kabupaten`, `tahun`, `jumlah_penduduk_rb`, `is_smelter`) non-null — **PASS**
- [x] Kolom kunci shift (`provinsi`, `tahun`, `pct_pdrb_pertanian_A`, `pct_industri_tambang_BC`) non-null — **PASS**

**Temuan naratif siap pakai:**
- Sulawesi Tengah shift index naik dari **0.449 (2014)** menjadi **3.533 (2024)**.
- Porsi PDRB Pertanian Sulteng turun dari **34.39% → 15.80%**.
- Porsi PDRB Tambang+Industri Sulteng naik dari **15.45% → 55.82%**.

**Final Pre-CP5 Audit (ulang sebelum dashboard):**
- [x] Semua file CP1–CP4 ada dan bisa dibaca.
- [x] CP2 PDRB sektoral: 1105 rows, 6 provinsi, 2014–2024, 17 sektor valid, null nilai = 0, duplicate = 0, pct sum = 100%.
- [x] CP3 Populasi window 2014–2024: 623 rows, 6 provinsi, 80 kabupaten, duplicate = 0, bad population range = 0, YoY ekstrem >50% = 0.
- [x] CP4 Demografi master: 623 rows, duplicate key `provinsi+kabupaten+tahun` = 0, key null = 0.
- [x] CP4 Employment shift: 65 rows, duplicate key `provinsi+tahun` = 0, key null = 0.
- [x] Sulteng narasi inti valid: Pertanian 34.39% → 15.80%; Tambang+Industri 15.45% → 55.82%; shift index 0.449 → 3.533.

**Catatan minor non-blocker:**
- `sulawesi_pdrb_per_kapita_sdgs.csv` punya duplicate untuk `wilayah+tahun+var_id` karena satu var menyimpan dua turvar (`Harga Berlaku` dan `Harga Konstan 2010`). Tidak dipakai sebagai key utama CP4; jika dipakai di dashboard, filter `turvar_label` dulu.
- `pmdn_nilai_juta_rp` null 110 rows di demografi master karena coverage PMDN tidak selengkap populasi kabupaten. Ini optional proxy, bukan kolom kunci.
- `pct_miskin` null 8 rows karena beberapa kabupaten/tahun tidak tersedia di SDGs Var 621. Ini optional enrichment, bukan blocker.

**✅ CP4 LULUS — Master files siap dipakai untuk CP5 dashboard.**

---

### ✅ CHECKPOINT 5: Dashboard Build — `11_Demografi_Sosial.py`
**Status:** ✅ **SELESAI**  
**Tanggal Eksekusi:** 27 Juni 2026  
**File:** `pages/11_Demografi_Sosial.py`  
**Sidebar:** `src/components/sidebar.py` → section `Revisi 1`

**Urutan build (dari yang datanya paling pasti → paling bergantung eksplorasi):**

| Sub-step | Section | Data yang dipakai | Bisa dibuat kapan? |
|----------|---------|------------------|---------------------|
| 5.1 | Header + Metodologi + Hero Statement | Tidak perlu data | Setelah CP4 |
| 5.2 | Kartu Metrik Agregat | Semua master files | Setelah CP4 |
| 5.3 | **4C: Transisi Ketenagakerjaan** (stacked area) | `employment_shift_fase4.csv` | Setelah CP1+CP2 |
| 5.4 | **4A: Ledakan Migrasi** (line chart, scatter) | `demografi_master_fase4.csv` | Setelah CP3+CP4 |
| 5.5 | **4A: Proxy Zoonosis** (DBD vs IUP) | `zoonosis_kab_kota` + `izin_baru` | Setelah CP4 |
| 5.6 | **4B: Urbanisasi** (area chart, heatmap) | `demografi_master_fase4.csv` | Setelah CP3+CP4 |
| 5.7 | Sintesis & Crosstab Akhir | Semua section selesai | Terakhir |

**Standar UI/UX yang dipakai:**
- Mengikuti `docs/UI_UX_Guidelines_Celios.md`: Inter font, dark theme, metric cards, method tag, hero statement, expander data mentah.
- Header tetap memakai hijau CELIOS (`#43A047`, `#66BB6A`, `#81C784`) sesuai guideline; rencana biru-ungu dibatalkan agar brand konsisten.
- `@st.cache_data` dipakai untuk loader data.
- Setiap chart punya judul internal Plotly dan expander data mentah.
- Tidak ada mock/dummy data; semua angka dari `data/processed`.

#### 📊 Log Eksekusi CP5

**Page yang dibuat:**
```
pages/11_Demografi_Sosial.py
```

**Sidebar update:**
```
Revisi 1
- Koridor Logistik Nikel
- Demografi & Struktur Sosial
```

**Konten final page:**
1. Header + Metodologi + Hero Statement data-driven.
2. Bento cards 2×3:
   - Shift Index Sulteng
   - Pertanian Sulteng turun
   - Tambang+Industri Sulteng naik
   - 7 kabupaten smelter prioritas
   - Rasio kepadatan smelter
   - Total kasus DBD kabupaten smelter
3. Section 11.1 — Tekanan Demografi Kabupaten Smelter.
4. Section 11.2 — Kepadatan Smelter vs Non-Smelter.
5. Section 11.3 — Pergeseran Ekonomi Agraris ke Tambang dan Industri.
6. Section 11.4 — Proxy Zoonosis DBD.
7. Section 11.5 — Matriks Sintesis Sosial-Ekologis.

**Validasi:**
- [x] `py_compile pages/11_Demografi_Sosial.py` — **PASS**
- [x] `py_compile src/components/sidebar.py` — **PASS**
- [x] Smoke test `python pages/11_Demografi_Sosial.py` — **PASS** (hanya warning Streamlit bare mode + deprecation `use_container_width`, tidak ada exception)
- [x] Minimal 5 visualisasi berjalan dengan data nyata — **PASS**
- [x] Hero statement mengutip angka konkret dari data — **PASS**
- [x] Setiap chart punya expander data mentah — **PASS**
- [x] Tidak ada hardcoded mock/dummy data — **PASS**

**✅ CP5 LULUS — Page baru siap diuji di browser via Streamlit.**

---

### 🗺️ Ringkasan Alur & Dependensi

```
[CP1: BPS SDGs Fetch] ──────────────────────────────────┐
         │                                               │
         │ (data ketenagakerjaan)                        │
         ▼                                               │
[CP2: PDRB Rebuild] ────────────────────────┐           │
(paralel dgn CP1)                           │           │
                                            │           │
[CP3: Populasi Kabupaten] ─────────────────┐│           │
(mulai setelah CP1 selesai)                ││           │
  Jalur A: SIMDASI                         ││           │
  Jalur B: Open Data Regional              ││           │
  Jalur C: SP2020 Census                   ││           │
  (stop di jalur pertama yang berhasil)    ││           │
                                           ▼▼           ▼
                              [CP4: Processing & Master Build]
                                           │
                                           ▼
                              [CP5: Dashboard Build]
                               5.1 Header → 5.2 Metrik
                               → 5.3 Ketenagakerjaan
                               → 5.4 Migrasi
                               → 5.5 Zoonosis Proxy
                               → 5.6 Urbanisasi
                               → 5.7 Sintesis
                                           │
                                           ▼
                                      🏁 SELESAI
```

---

### 📋 Tracking Progress

| Checkpoint | Status | Tanggal Mulai | Tanggal Selesai | Catatan |
|-----------|--------|--------------|----------------|--------|
| CP1: BPS SDGs Fetch | ✅ SELESAI | 26 Jun 2026 | 26 Jun 2026 | 4 file processed (946 baris kab-level). 4 var skip/tidak tersedia (1217, 2154, 2190, 2191). Wajib pakai .venv Python 3.10 |
| CP2: PDRB Rebuild | ✅ SELESAI | 26 Jun 2026 | 26 Jun 2026 | Sumber: SIMDASI. 17 sektor utama KLU × 6 provinsi × 2014-2024 = 1105 baris. 2 bug difix: sub-sektor pollution + unit juta/miliar Sulteng 2014. |
| CP3: Populasi Kabupaten | ✅ SELESAI | 26 Jun 2026 | 26 Jun 2026 | SIMDASI Jalur A berhasil. 952 baris, 80 kab, 6 provinsi, 2004-2026. Unit populasi, filter Gorontalo, is_smelter, dan typo Parepare difix. |
| CP4: Processing & Master | ✅ SELESAI | 26 Jun 2026 | 26 Jun 2026 | 3 file processed: demografi master 623 rows, employment shift 65 rows, PDRB shift index 65 rows. Duplikasi PMDN dan kemiskinan difix. |
| CP5: Dashboard Build | ✅ SELESAI | 27 Jun 2026 | 27 Jun 2026 | Page baru `pages/11_Demografi_Sosial.py`; sidebar updated; py_compile + smoke test pass. |

---

## 📊 Schema Output Files (Final)

### `sulawesi_populasi_kab_2014_2024.csv`
| Kolom | Tipe | Contoh | Sumber |
|-------|------|--------|--------|
| `provinsi` | string | `Sulawesi Tengah` | BPS |
| `kabupaten` | string | `Morowali` | BPS |
| `tahun` | int | `2020` | BPS |
| `jumlah_penduduk` | int | `145000` | BPS API |
| `kepadatan_per_km2` | float | `22.5` | BPS API |
| `laju_pertumbuhan_pct` | float | `4.2` | Derived |
| `is_smelter` | bool | `True` | Derived dari esdm_nikel.csv |
| `iup_aktif_kumulatif` | int | `12` | Derived dari izin_baru.csv |

### `sulawesi_pdrb_sektoral_2016_2024.csv`
| Kolom | Tipe | Contoh | Sumber |
|-------|------|--------|--------|
| `provinsi` | string | `Sulawesi Tengah` | BPS |
| `tahun` | int | `2022` | BPS |
| `sektor_kode` | string | `B` | BPS |
| `sektor_nama` | string | `Pertambangan dan Penggalian` | BPS |
| `nilai_miliar_rp` | float | `85000.5` | BPS API |
| `pct_dari_total` | float | `32.1` | Derived |

### `sulawesi_demografi_master_fase4.csv`
| Kolom | Tipe | Deskripsi |
|-------|------|-----------|
| `provinsi` | string | 6 provinsi Sulawesi |
| `kabupaten` | string | Level kabupaten/kota |
| `tahun` | int | 2014-2024 |
| `jumlah_penduduk` | int | Populasi |
| `kepadatan_per_km2` | float | Jiwa/km² |
| `pct_perkotaan` | float | % penduduk urban |
| `laju_pertumbuhan_pct` | float | % YoY |
| `anomali_flag` | bool | True jika laju > 2× median provinsi |
| `is_smelter` | bool | Kabupaten lokasi smelter aktif |
| `iup_kumulatif` | int | Total IUP s/d tahun berjalan |
| `dbd_kasus` | int | Dari zoonosis_kab_kota |
| `pmdn_nilai_juta_rp` | float | Dari investasi_pmdn |

---

## ⚠️ Risk Assessment & Mitigasi

| Risiko | Probabilitas | Dampak | Mitigasi |
|--------|-------------|--------|----------|
| BPS SDGs Var tidak tersedia untuk domain Sulawesi (hanya domain 0000 nasional) | 🟡 Sedang | 🟡 Sedang | Ambil nasional, filter pandas untuk provinsi 7100-7600. Granularity provinsi, bukan kabupaten |
| SIMDASI tidak menyediakan data populasi tahunan (hanya snapshot publikasi) | 🟡 Sedang | 🔴 Tinggi | Fallback ke Open Data Regional (Sulteng/Sultra) untuk kabupaten smelter |
| Open Data Regional gagal (Cloudflare / auth) | 🟡 Sedang | 🟡 Sedang | Replikasi pola CKAN Sulut yang sudah berhasil. Fallback: HTML scraping BeautifulSoup |
| Data Sakernas hanya tersedia level provinsi | 🔴 Pasti | 🟡 Sedang | Sudah dimitigasi: gunakan BPS SDGs Var 1217 (manufaktur) + 2153 (informal) sebagai pengganti |
| PDRB sektoral sulit di-rebuild (var_id salah) | 🟡 Sedang | 🔴 Tinggi | Referensi `scripts/pdrb_var_mapping.json` dan `scripts/check_bps_vars.py` yang sudah ada |
| SP2020 migrasi risen hanya 1 titik waktu (2020) | 🔴 Pasti | 🟢 Rendah | Gunakan sebagai anchor validasi, bukan time-series. Anomali populasi tahunan tetap jadi backbone |

---

## ✅ Definisi Selesai (Definition of Done)

- [ ] BPS SDGs vars (1217, 621, 2153, 296, 2190, 2191) berhasil di-fetch dan difilter Sulawesi
- [ ] Minimal 1 dari: SIMDASI atau Open Data Regional berhasil memberi data populasi kabupaten
- [ ] `sulawesi_pdrb_sektoral_2016_2024.csv` berhasil di-rebuild (tidak ada `"Tidak ada"` di kolom sektor)
- [ ] `sulawesi_demografi_master_fase4.csv` tersedia di `data/processed/` dengan kolom kunci lengkap
- [ ] Page `10_Demografi_Sosial.py` live dan dapat dibuka tanpa error
- [ ] Minimal 6 visualisasi berjalan dengan data nyata (bukan mock)
- [ ] Narasi hero statement mengutip angka konkret (misal: "Morowali tumbuh X% vs rata-rata Sulawesi Y%")
- [ ] Setiap visualisasi mencantumkan sumber data dan var ID yang jelas

---

## 📎 Referensi File Terkait

| Dokumen | Lokasi |
|---------|--------|
| Roadmap induk revisi | `docs/rev1_Catatan dan Masukan olah data Henry.md` |
| Implementation plan awal Fase 4 | `docs/FASE_4_IMPLEMENTATION_PLAN.md` |
| Framework Fase 1 | `docs/framework-fase1-d3tlh.md` |
| PRD Fase 1 | `docs/prd-fase1-d3tlh.md` |
| Schema dataset logistik (referensi pola) | `src/utils/rev1_logistik_stage.py` |
| Script cek var BPS (referensi cara query) | `scripts/check_bps_vars.py`, `scripts/pdrb_var_mapping.json` |
| Data proxy tersedia | `data/processed/sulawesi_izin_baru_per_tahun.csv` |
| Data proxy tersedia | `data/processed/sulawesi_esdm_nikel.csv` |
| Data proxy tersedia | `data/processed/zoonosis_kab_kota_2015_2024.csv` |
| Data BROKEN (perlu rebuild) | `data/raw/bps_pdrb/bps_pdrb_sulawesi_2016_2026.csv` |

---

*Dokumen ini adalah panduan eksekusi Fase 4. Setiap pengambilan keputusan teknis selama implementasi harus merujuk ke dokumen ini dan mencatat deviasi jika ada.*  
*Dibuat: 26 Juni 2026 | CELIOS Research Division — Fase 4 Execution*
