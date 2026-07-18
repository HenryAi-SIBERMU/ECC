# Panduan Download Manual Data PAD BPS Sulawesi

> **CELIOS ECC Intelligence System**  
> **Dibuat:** 9 Juni 2026  
> **Status:** Ready untuk digunakan

---

## Ringkasan

Website BPS menggunakan **Cloudflare protection** yang memblokir scraping otomatis. Solusi: **download manual** via browser untuk setiap provinsi Sulawesi, lalu proses dengan script otomatis.

---

## Coverage: 6 Provinsi Sulawesi

### 1. Sulawesi Utara (7100)
- **URL**: https://sulut.bps.go.id/id/query-builder
- **Kode**: 7100

### 2. Sulawesi Tengah (7200)
- **URL**: https://sulteng.bps.go.id/id/query-builder
- **Kode**: 7200

### 3. Sulawesi Selatan (7300)
- **URL**: https://sulsel.bps.go.id/id/query-builder
- **Kode**: 7300

### 4. Sulawesi Tenggara (7400)
- **URL**: https://sultra.bps.go.id/id/query-builder
- **Kode**: 7400

### 5. Gorontalo (7500)
- **URL**: https://gorontalo.bps.go.id/id/query-builder
- **Kode**: 7500

### 6. Sulawesi Barat (7600)
- **URL**: https://sulbar.bps.go.id/id/query-builder
- **Kode**: 7600

---

## Langkah-Langkah Download

### Step 1: Buka Query Builder
1. Buka URL provinsi di browser (Chrome/Firefox recommended)
2. Tunggu halaman selesai loading (~5-10 detik)
3. **Tutup popup** jika ada (klik tombol "Tutup" di pojok kanan atas popup)

---

### Step 2: Pilih Form Fields (LENGKAP)

#### **Field 1: Kategori Subjek**
**Dropdown pertama setelah form muncul**

**Pilihan yang tersedia:**
```
- Kependudukan dan Tenaga Kerja
- Sosial dan Kesejahteraan Rakyat
- Pertanian dan Pertambangan
- Industri dan Perdagangan
- Transportasi dan Komunikasi
- Keuangan Daerah ⭐ PILIH INI
- Pemerintahan     ⭐ ATAU INI
```

**Apa yang harus dipilih:**
⭐ **Pilih: "Keuangan Daerah"** (Priority 1)  
⭐ **Atau: "Pemerintahan"** (Priority 2 jika Keuangan Daerah tidak ada)

**Instruksi:** 
1. Klik dropdown "Pilih Kategori Subjek"
2. Scroll cari "Keuangan Daerah"
3. Klik untuk select

---

#### **Field 2: Subjek**
**Dropdown kedua, muncul setelah pilih Kategori Subjek**

**Pilihan yang tersedia (untuk Kategori "Keuangan Daerah"):**
```
- Keuangan Pemerintah Daerah ⭐ PILIH INI
- APBD
- Pendapatan Daerah
- Belanja Daerah
- Pembiayaan Daerah
```

**Apa yang harus dipilih:**
⭐ **Pilih: "Keuangan Pemerintah Daerah"**

**Instruksi:**
1. Tunggu dropdown "Subjek" muncul (~2 detik setelah pilih Kategori)
2. Klik dropdown "Pilih Subjek"
3. Pilih "Keuangan Pemerintah Daerah"

---

#### **Field 3: Tabel / Indikator**
**List box besar di sebelah kiri, muncul setelah pilih Subjek**

**Field ini:** Searchable list dengan banyak opsi tabel

**Cara menggunakan:**
1. Ada search box di atas list: **"Cari judul tabel"**
2. Ketik keyword untuk filter tabel
3. Scroll list untuk lihat semua opsi
4. Klik tabel yang ingin didownload

**Keywords untuk search:**
- Ketik: **"realisasi pendapatan"**
- Ketik: **"PAD"**
- Ketik: **"APBD"**
- Ketik: **"pendapatan asli daerah"**

**Tabel yang harus dicari (TARGET):**
```
✅ Realisasi Pendapatan dan Belanja Pemerintah Kabupaten/Kota
✅ Realisasi Pendapatan Asli Daerah (PAD) Kabupaten/Kota
✅ Realisasi Pendapatan Daerah Menurut Jenis
✅ APBD Kabupaten/Kota
✅ Pendapatan Asli Daerah Menurut Jenis
✅ Laporan Realisasi Anggaran Pendapatan dan Belanja Daerah
```

**⚠️ CATATAN:** Nama tabel bisa sedikit berbeda per provinsi. Prioritas:
1. Cari yang ada kata **"Realisasi"** + **"Pendapatan"**
2. Kalau tidak ada, cari yang ada kata **"APBD"**
3. Kalau masih tidak ada, cari yang ada kata **"Pendapatan Asli Daerah"** atau **"PAD"**

**Instruksi:**
1. Ketik "realisasi pendapatan" di search box
2. Lihat hasil yang muncul
3. Klik tabel yang paling cocok (biasanya paling atas)
4. Tabel akan highlight/selected

---

#### **Field 4: Tahun**
**Panel kanan atas, muncul setelah pilih Tabel**

**Pilihan yang tersedia:**
```
Bervariasi per provinsi, biasanya:
2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 
2019, 2020, 2021, 2022, 2023, 2024, 2025
```

**Apa yang harus dipilih:**
⭐ **Centang SEMUA tahun dari 2016 sampai 2024**

**Instruksi:**
1. Scroll ke bagian "Tahun" di panel kanan
2. Centang checkbox untuk tahun:
   - ☑ 2016
   - ☑ 2017
   - ☑ 2018
   - ☑ 2019
   - ☑ 2020
   - ☑ 2021
   - ☑ 2022
   - ☑ 2023
   - ☑ 2024
3. JANGAN centang tahun di luar range (2010-2015, 2025)

---

#### **Field 5: Turunan Tahun**
**Panel kanan, di bawah "Tahun"**

**Pilihan yang mungkin tersedia:**
```
- Tahunan ⭐ PILIH INI (jika ada)
- Triwulanan
- Semesteran
- Bulanan
```

**Rekomendasi:**
- ⭐ **Pilih "Tahunan"** jika tersedia
- ⭐ **Atau kosongkan** (tidak pilih apa-apa)
- **JANGAN pilih** Bulanan/Triwulanan (data terlalu detail, file besar)

---

#### **Field 6: Karakteristik**
**Panel kanan, di bawah "Turunan Tahun"**

**Pilihan yang tersedia:**
```
- Provinsi ⭐ ATAU INI
- Kabupaten/Kota ⭐ PILIH INI (jika ada)
- Jenis Pendapatan
- Sektor
```

**Rekomendasi:**
- ⭐ **Pilih "Kabupaten/Kota"** untuk breakdown regional detail
- ⭐ **Atau "Provinsi"** untuk data agregat provinsi
- **Bisa pilih keduanya** jika ingin data lengkap

**Instruksi:**
1. Centang "Kabupaten/Kota" (untuk breakdown per kab/kota)
2. Atau centang "Provinsi" (untuk agregat provinsi saja)

---

#### **Field 7: Judul Baris**
**Panel kanan, di bawah "Karakteristik"**

**Pilihan yang tersedia:**
```
- Jenis Pendapatan ⭐ PILIH INI
- Kabupaten/Kota
- Tahun
- Sektor
```

**Rekomendasi:**
⭐ **Pilih "Jenis Pendapatan"**

**Kenapa?**
- Akan breakdown PAD menurut jenis (Pajak Daerah, Retribusi, dll.)
- Penting untuk analisis komposisi PAD

**Instruksi:**
1. Centang "Jenis Pendapatan"
2. Atau pilih yang paling relevan dengan breakdown PAD

---

### Step 3: Tambah Data ke List

**Setelah semua field terisi:**

1. Klik tombol **"Tambah"** di bawah form
2. Data akan muncul di panel **"Data Terpilih"** di bawah
3. Anda bisa tambah data lain (repeat Step 2) atau lanjut ke download

**⚠️ BATAS:** Maksimal 2 data bisa dipilih sekaligus. Jika sudah 2, hapus salah satu atau langsung download.

---

### Step 4: Submit & Generate Tabel

1. Setelah data ditambahkan ke list, klik tombol **"Submit"** di bawah form
2. Tunggu tabel generate (~10-30 detik)
3. Tabel akan muncul di bawah form

**Jika tabel tidak muncul:**
- Tunggu lebih lama (sampai 1 menit)
- Refresh page dan ulangi
- Kurangi range tahun (coba 2020-2024 dulu)

---

### Step 5: Download Tabel

1. Setelah tabel muncul, cari tombol **"Unduh"** atau **"Download"** (biasanya di atas/samping tabel)
2. Klik tombol download
3. Pilih format:
   - ⭐ **CSV** (Recommended - easy to process)
   - Excel (XLSX)
4. File akan terdownload ke folder Downloads browser Anda

---

### Step 6: Penamaan & Penyimpanan File

**Format nama file:**
```
pad_{kode_provinsi}_{nama_provinsi}_{tahun_awal}-{tahun_akhir}.csv
```

**Contoh:**
```
pad_7300_sulawesi_selatan_2016-2024.csv
pad_7100_sulawesi_utara_2016-2024.csv
```

**Instruksi:**
1. Buka folder Downloads
2. Rename file yang baru didownload sesuai format di atas
3. Pindahkan file ke folder:
   ```
   c:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\tools\scrapling\bps_eksporpad\downloads\
   ```

---

## 📋 FORM SUMMARY TEMPLATE

Copy template ini untuk setiap provinsi:

```
=== DOWNLOAD PAD: {NAMA PROVINSI} ===

URL: {URL query-builder}

FORM VALUES:
┌─────────────────────────────────┬──────────────────────────┐
│ Field                           │ Value Selected           │
├─────────────────────────────────┼──────────────────────────┤
│ Kategori Subjek                 │ Keuangan Daerah          │
│ Subjek                          │ Keuangan Pemerintah      │
│ Tabel/Indikator                 │ Realisasi Pendapatan...  │
│ Tahun                           │ 2016-2024 (9 tahun)      │
│ Turunan Tahun                   │ Tahunan / (kosong)       │
│ Karakteristik                   │ Kabupaten/Kota           │
│ Judul Baris                     │ Jenis Pendapatan         │
└─────────────────────────────────┴──────────────────────────┘

OUTPUT:
Filename: pad_{kode}_{provinsi}_2016-2024.csv
Rows: _____
Size: _____ KB
Status: ☐ Downloaded  ☐ Renamed  ☐ Moved to folder
```

---

## Checklist Download (6 Provinsi)

```
☐ Sulawesi Utara (7100)
  ☐ File: pad_7100_sulawesi_utara_2016-2024.csv
  ☐ Rows: _____
  ☐ Periode: 2016-2024
  
☐ Sulawesi Tengah (7200)
  ☐ File: pad_7200_sulawesi_tengah_2016-2024.csv
  ☐ Rows: _____
  ☐ Periode: 2016-2024
  
☐ Sulawesi Selatan (7300)
  ☐ File: pad_7300_sulawesi_selatan_2016-2024.csv
  ☐ Rows: _____
  ☐ Periode: 2016-2024
  
☐ Sulawesi Tenggara (7400)
  ☐ File: pad_7400_sulawesi_tenggara_2016-2024.csv
  ☐ Rows: _____
  ☐ Periode: 2016-2024
  
☐ Gorontalo (7500)
  ☐ File: pad_7500_gorontalo_2016-2024.csv
  ☐ Rows: _____
  ☐ Periode: 2016-2024
  
☐ Sulawesi Barat (7600)
  ☐ File: pad_7600_sulawesi_barat_2016-2024.csv
  ☐ Rows: _____
  ☐ Periode: 2016-2024
```

---

## Troubleshooting

### ❌ Form tidak muncul / masih loading
- **Refresh halaman** (F5)
- **Clear browser cache** (Ctrl+Shift+Del)
- **Coba browser lain** (Chrome → Firefox atau sebaliknya)
- **Matikan AdBlock/extension** yang bisa interfere

### ❌ Data tidak ada untuk tahun tertentu
- **Normal** - tidak semua provinsi punya data lengkap 2016-2024
- **Download yang tersedia** saja, catat missing years di checklist

### ❌ Tabel terlalu besar / browser hang
- **Kurangi range tahun** (split jadi 2016-2019, 2020-2024)
- **Pilih karakteristik lebih spesifik** (hanya Provinsi, bukan Kab/Kota)

### ❌ File corrupt / tidak bisa dibuka
- **Re-download** dengan format berbeda (CSV ↔ Excel)
- **Cek file size** - jika 0 KB atau sangat kecil, ada error saat download

---

## Output Location

Simpan semua file download di:
```
c:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\tools\scrapling\bps_eksporpad\downloads\
```

Struktur folder:
```
downloads/
├── pad_7100_sulawesi_utara_2016-2024.csv
├── pad_7200_sulawesi_tengah_2016-2024.csv
├── pad_7300_sulawesi_selatan_2016-2024.csv
├── pad_7400_sulawesi_tenggara_2016-2024.csv
├── pad_7500_gorontalo_2016-2024.csv
└── pad_7600_sulawesi_barat_2016-2024.csv
```

---

## Next Step: Processing Script

Setelah download selesai, file-file ini akan diproses otomatis dengan script:
- **Cleaning** - standardisasi format, hapus rows kosong
- **Transformation** - pivot jika perlu, extract tahun dari headers
- **Consolidation** - gabungkan 6 provinsi jadi 1 file master
- **Validation** - check missing data, outliers, duplikasi

Script processing sudah disiapkan di: `process_pad_downloads.py`

---

## Estimasi Waktu

- **Per provinsi**: 5-10 menit (termasuk waiting time)
- **Total 6 provinsi**: ~45-60 menit
- **Best time**: Pagi (08:00-10:00) atau sore (15:00-17:00) WIB - traffic rendah

---

## Tips Efisiensi

1. **Buka 2-3 tab parallel** - download dari multiple provinsi bersamaan
2. **Gunakan keyboard shortcuts** - Tab untuk navigasi antar dropdown, Space untuk select
3. **Screenshot setiap provinsi** - dokumentasi untuk referensi nanti
4. **Catat observasi** - jika ada anomali atau missing data, tulis di checklist

---

## Contact & Support

Jika ada kendala teknis saat download, hubungi:
- **BPS Call Center**: 082373736742
- **Email**: bps7300@bps.go.id (untuk Sulsel)
- **WhatsApp**: http://s.bps.go.id/wa-pst

---

*Panduan ini dibuat sebagai workaround untuk Cloudflare protection pada website BPS.*  
*Updated: 9 Juni 2026 | CELIOS ECC Intelligence System*
