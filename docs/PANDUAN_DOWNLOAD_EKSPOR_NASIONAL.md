
# PANDUAN LENGKAP DOWNLOAD DATA EKSPOR NASIONAL

> **CELIOS ECC Intelligence System**  
> **URL:** https://www.bps.go.id/id/exim  
> **Periode data terbaru:** April 2026

---

## 📋 FORM FIELDS - LENGKAP

### Field 1: **Pilih Data** 
**Wajib diisi**

**Pilihan:**
- ⭐ **Ekspor** ← **PILIH INI**
- Impor

**Instruksi:** Klik radio button **Ekspor**

---

### Field 2: **Agregasi**
**Wajib diisi**

**Pilihan:**
1. ⭐ **Menurut Kode HS** ← **PILIH INI DULU (Priority 1)**
   - Breakdown per komoditas ekspor
   - Best for sector analysis
   
2. **Menurut Pelabuhan** ← **PILIH INI KEDUA (Priority 2)**
   - Breakdown per pelabuhan ekspor
   - Useful untuk regional routing
   
3. **Menurut Negara/Wilayah/Entitas Tertentu** ← **PILIH INI KETIGA (Priority 3)**
   - Breakdown per negara tujuan
   - Useful untuk market analysis

**Instruksi:** Pilih dari dropdown. Anda perlu download **3 kali** (sekali per agregasi)

---

### Field 3: **Tahun**
**Wajib diisi**

**Pilihan yang tersedia:**
```
2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026
```

**⚠️ BATAS MAKSIMAL:** Maksimal **5 tahun** dapat dipilih sekaligus

**Apa yang harus dipilih:**
⭐ **BATCH 1:** Pilih tahun 2016, 2017, 2018, 2019, 2020 (5 tahun)  
⭐ **BATCH 2:** Pilih tahun 2021, 2022, 2023, 2024 (4 tahun)

**Cara memilih multiple:**
1. Klik dropdown "Pilih Tahun"
2. **Untuk BATCH 1:** Centang checkbox: 2016, 2017, 2018, 2019, 2020
3. **Untuk BATCH 2:** Centang checkbox: 2021, 2022, 2023, 2024
4. Jangan centang 2015, 2025, 2026 (di luar range target)

**⚠️ PENTING:** Anda perlu download **2 kali** untuk setiap agregasi (BATCH 1 dan BATCH 2)

---

### Field 4: **Bulan**
**Opsional** (hanya muncul setelah pilih Tahun)

**Pilihan yang tersedia:**
```
01 - Januari
02 - Februari  
03 - Maret
04 - April
05 - Mei
06 - Juni
07 - Juli
08 - Agustus
09 - September
10 - Oktober
11 - November
12 - Desember
```

**Rekomendasi:**
- ⭐ **KOSONGKAN** (jangan pilih bulan) → akan dapat data **tahunan agregat**
- Atau pilih **Desember** saja → data akumulatif full year

**Alasan:** Data tahunan lebih stabil dan cukup untuk ECC model

---

### Field 5: **Jenis HS** 
**Muncul jika pilih Agregasi "Menurut Kode HS"**

**Pilihan:**
1. ⭐ **HS 2 Digit** ← **PILIH INI**
   - Kategori besar (99 komoditas)
   - Cukup untuk sector analysis
   - File size manageable
   
2. **HS Full** (HS 6-8 Digit)
   - Detail sangat tinggi (ribuan komoditas)
   - File size sangat besar
   - **TIDAK RECOMMENDED** untuk download pertama

**Instruksi:** Pilih **HS 2 Digit**

---

### Field 6: **Kode HS**
**Muncul jika pilih "Menurut Kode HS"**

**Field ini:** Multi-select dropdown dengan search

**⚠️ ATURAN PENTING:** 
- **TIDAK BOLEH dikosongkan** - HARUS pilih kode HS spesifik
- Default "pilih semua" TIDAK TERSEDIA di field ini
- **Batas maksimal:** ~20-30 kode HS per download (tergantung kompleksitas data)

**Apa yang harus dipilih:**

#### **BATCH 1: Kode HS Prioritas Tinggi (Sulawesi)** ⭐⭐⭐
Pilih 10 kode ini untuk download pertama:
```
03 → Ikan, udang, dan crustacea
08 → Buah-buahan dan kacang
09 → Kopi, teh, dan rempah-rempah
15 → Lemak dan minyak nabati/hewani
16 → Olahan daging dan ikan
24 → Tembakau dan produk tembakau
44 → Kayu dan barang dari kayu
72 → Besi dan baja
85 → Mesin dan peralatan listrik
87 → Kendaraan dan bagiannya
```

#### **BATCH 2: Kode HS Sekunder** ⭐⭐
Pilih 10 kode ini untuk download kedua:
```
01 → Hewan hidup
02 → Daging dan jeroan
04 → Produk susu, telur, madu
07 → Sayuran
10 → Sereal (beras, jagung)
21 → Berbagai olahan makanan
27 → Bahan bakar mineral
39 → Plastik dan barang dari plastik
40 → Karet dan barang dari karet
64 → Alas kaki
```

#### **BATCH 3: Kode HS Tambahan** ⭐
Pilih sisanya jika diperlukan (opsional):
```
25 → Garam, belerang, tanah, batu
26 → Bijih, slag, abu
28 → Produk kimia anorganik
29 → Produk kimia organik
48 → Kertas dan karton
...dan lainnya
```

**Cara memilih:**
1. Klik dropdown "Kode HS"
2. Ketik kode atau nama (misal: "03" atau "ikan")
3. Klik hasil yang muncul dari list
4. Repeat hingga 10 kode terpilih
5. **JANGAN pilih lebih dari 10-15 kode** dalam 1 download

**⚠️ PERINGATAN:** 
- Jika pilih > 15 kode HS, tabel bisa sangat besar dan browser crash
- Jika browser hang, kurangi jumlah kode atau kurangi range tahun
- Download terpisah per batch lebih aman dan stabil

---

### Field 7: **Pelabuhan**
**Muncul jika pilih Agregasi "Menurut Pelabuhan"**

**Field ini:** Multi-select dropdown

**⚠️ BATAS MAKSIMAL:** Maksimal **10-15 pelabuhan** dapat dipilih sekaligus

**Pilihan pelabuhan utama Sulawesi:**
```
MAKASSAR/UPT (Sulawesi Selatan)
BITUNG (Sulawesi Utara)
PANTOLOAN (Sulawesi Tengah)
KENDARI (Sulawesi Tenggara)
GORONTALO (Gorontalo)
MAMUJU (Sulawesi Barat)
```

**Pilihan pelabuhan nasional lainnya:**
```
TANJUNG PRIOK (Jakarta)
TANJUNG PERAK (Surabaya)
BELAWAN (Medan)
BALIKPAPAN (Kalimantan Timur)
BANJARMASIN (Kalimantan Selatan)
```

**Rekomendasi:**
- ⭐ **BATCH 1:** Pilih **6 pelabuhan Sulawesi** (Makassar, Bitung, Pantoloan, Kendari, Gorontalo, Mamuju)
- ⭐ **BATCH 2 (opsional):** Pilih **5 pelabuhan nasional utama** (Priok, Perak, Belawan, Balikpapan, Banjarmasin)
- Atau **KOSONGKAN** untuk include semua pelabuhan nasional (jika sistem mengizinkan)

**Catatan:** Jika kosongkan dan download gagal/timeout, gunakan strategi batch di atas

---

### Field 8: **Negara/Wilayah/Entitas Tertentu**
**Muncul jika pilih Agregasi "Menurut Negara"**

**Field ini:** Multi-select dropdown dengan search

**⚠️ BATAS MAKSIMAL:** Maksimal **15-20 negara** dapat dipilih sekaligus

**Pilihan negara tujuan utama Indonesia:**

#### **BATCH 1: Top Trading Partners Asia** ⭐⭐⭐
```
CHINA
JAPAN
SINGAPORE
INDIA
MALAYSIA
THAILAND
KOREA, REPUBLIC OF (SOUTH KOREA)
TAIWAN
VIETNAM
PHILIPPINES
```

#### **BATCH 2: Trading Partners Western & Oceania** ⭐⭐
```
UNITED STATES OF AMERICA (USA)
AUSTRALIA
GERMANY
NETHERLANDS
ITALY
UNITED KINGDOM
FRANCE
SPAIN
BELGIUM
CANADA
```

#### **BATCH 3: Other Trading Partners** ⭐
```
SAUDI ARABIA
UNITED ARAB EMIRATES
BRAZIL
MEXICO
RUSSIA
TURKEY
EGYPT
SOUTH AFRICA
...dan lainnya
```

**Rekomendasi:**
- ⭐ **BATCH 1 (Priority):** Pilih **10 negara Asia** (trading partners utama)
- ⭐ **BATCH 2 (Optional):** Pilih **10 negara Western/Oceania**
- ⭐ Atau **KOSONGKAN** untuk include semua negara (jika sistem mengizinkan)

**Catatan:** Jika kosongkan dan browser hang/timeout, gunakan strategi batch

---

## 🎯 KOMBINASI FORM YANG HARUS DIDOWNLOAD

**⚠️ PENTING:** Karena ada batas maksimal field selection, Anda perlu download dalam **BATCH** terpisah

---

### DATASET A: Ekspor per Sektor (HS 2 Digit)

**Total downloads:** 4 files (2 batch tahun × 2 batch kode HS = 4)

#### **Download A1: HS Prioritas Tinggi (2016-2020)**

| Field | Value |
|-------|-------|
| Pilih Data | **Ekspor** |
| Agregasi | **Menurut Kode HS** |
| Tahun | **2016, 2017, 2018, 2019, 2020** (BATCH 1) |
| Bulan | **(kosong)** |
| Jenis HS | **HS 2 Digit** |
| Kode HS | **03, 08, 09, 15, 16, 24, 44, 72, 85, 87** (10 kode) |

**Output:** `ekspor_hs_prioritas_2016-2020.csv`

---

#### **Download A2: HS Prioritas Tinggi (2021-2024)**

| Field | Value |
|-------|-------|
| Pilih Data | **Ekspor** |
| Agregasi | **Menurut Kode HS** |
| Tahun | **2021, 2022, 2023, 2024** (BATCH 2) |
| Bulan | **(kosong)** |
| Jenis HS | **HS 2 Digit** |
| Kode HS | **03, 08, 09, 15, 16, 24, 44, 72, 85, 87** (10 kode yang sama) |

**Output:** `ekspor_hs_prioritas_2021-2024.csv`

---

#### **Download A3: HS Sekunder (2016-2020)** ⭐ Optional

| Field | Value |
|-------|-------|
| Pilih Data | **Ekspor** |
| Agregasi | **Menurut Kode HS** |
| Tahun | **2016, 2017, 2018, 2019, 2020** |
| Bulan | **(kosong)** |
| Jenis HS | **HS 2 Digit** |
| Kode HS | **01, 02, 04, 07, 10, 21, 27, 39, 40, 64** (10 kode) |

**Output:** `ekspor_hs_sekunder_2016-2020.csv`

---

#### **Download A4: HS Sekunder (2021-2024)** ⭐ Optional

| Field | Value |
|-------|-------|
| Pilih Data | **Ekspor** |
| Agregasi | **Menurut Kode HS** |
| Tahun | **2021, 2022, 2023, 2024** |
| Bulan | **(kosong)** |
| Jenis HS | **HS 2 Digit** |
| Kode HS | **01, 02, 04, 07, 10, 21, 27, 39, 40, 64** (10 kode yang sama) |

**Output:** `ekspor_hs_sekunder_2021-2024.csv`

---

### DATASET B: Ekspor per Pelabuhan

**Total downloads:** 2 files (2 batch tahun)

#### **Download B1: Pelabuhan Sulawesi (2016-2020)**

| Field | Value |
|-------|-------|
| Pilih Data | **Ekspor** |
| Agregasi | **Menurut Pelabuhan** |
| Tahun | **2016, 2017, 2018, 2019, 2020** |
| Bulan | **(kosong)** |
| Pelabuhan | **Makassar, Bitung, Pantoloan, Kendari, Gorontalo, Mamuju** (6 Sulawesi) |

**Output:** `ekspor_pelabuhan_sulawesi_2016-2020.csv`

---

#### **Download B2: Pelabuhan Sulawesi (2021-2024)**

| Field | Value |
|-------|-------|
| Pilih Data | **Ekspor** |
| Agregasi | **Menurut Pelabuhan** |
| Tahun | **2021, 2022, 2023, 2024** |
| Bulan | **(kosong)** |
| Pelabuhan | **Makassar, Bitung, Pantoloan, Kendari, Gorontalo, Mamuju** (6 yang sama) |

**Output:** `ekspor_pelabuhan_sulawesi_2021-2024.csv`

---

### DATASET C: Ekspor per Negara Tujuan

**Total downloads:** 2 files (2 batch tahun)

#### **Download C1: Negara Asia (2016-2020)**

| Field | Value |
|-------|-------|
| Pilih Data | **Ekspor** |
| Agregasi | **Menurut Negara/Wilayah/Entitas Tertentu** |
| Tahun | **2016, 2017, 2018, 2019, 2020** |
| Bulan | **(kosong)** |
| Negara | **China, Japan, Singapore, India, Malaysia, Thailand, South Korea, Taiwan, Vietnam, Philippines** |

**Output:** `ekspor_negara_asia_2016-2020.csv`

---

#### **Download C2: Negara Asia (2021-2024)**

| Field | Value |
|-------|-------|
| Pilih Data | **Ekspor** |
| Agregasi | **Menurut Negara/Wilayah/Entitas Tertentu** |
| Tahun | **2021, 2022, 2023, 2024** |
| Bulan | **(kosong)** |
| Negara | **China, Japan, Singapore, India, Malaysia, Thailand, South Korea, Taiwan, Vietnam, Philippines** (10 yang sama) |

**Output:** `ekspor_negara_asia_2021-2024.csv`

---

## 📊 DOWNLOAD SUMMARY

### Minimum Downloads (Priority)
```
✅ Dataset A (HS Prioritas): 2 files
✅ Dataset B (Pelabuhan): 2 files  
✅ Dataset C (Negara Asia): 2 files
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total MINIMUM: 6 files
```

### Full Downloads (Recommended)
```
✅ Dataset A (HS Prioritas): 2 files
✅ Dataset A (HS Sekunder): 2 files
✅ Dataset B (Pelabuhan): 2 files
✅ Dataset C (Negara Asia): 2 files
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total FULL: 8 files
```

---

## 📸 SCREENSHOT REFERENCE

**Form tampak seperti ini:**
```
┌─────────────────────────────────────────┐
│ Pilih Data: ○ Ekspor  ○ Impor          │
├─────────────────────────────────────────┤
│ Agregasi: [Pilih Agregasi ▼]           │
│           - Menurut Kode HS             │
│           - Menurut Pelabuhan           │
│           - Menurut Negara              │
├─────────────────────────────────────────┤
│ Tahun: [Pilih Tahun ▼]                 │
│        ☑ 2016  ☑ 2017  ☑ 2018          │
├─────────────────────────────────────────┤
│ Bulan: [Pilih Bulan ▼] (opsional)      │
├─────────────────────────────────────────┤
│ [Field dinamis sesuai agregasi]        │
├─────────────────────────────────────────┤
│         [ Buat Tabel ]                  │
└─────────────────────────────────────────┘
```

---

## ▶️ LANGKAH EKSEKUSI

### DATASET A: Ekspor per Sektor (HS 2 Digit)

#### Download A1 (Priority: ⭐⭐⭐)
1. Buka https://www.bps.go.id/id/exim
2. Pilih **Ekspor**
3. Agregasi: **Menurut Kode HS**
4. Tahun: Centang **2016, 2017, 2018, 2019, 2020** (5 tahun BATCH 1)
5. Bulan: **Kosongkan**
6. Jenis HS: **HS 2 Digit**
7. Kode HS: Pilih **10 kode prioritas** (03, 08, 09, 15, 16, 24, 44, 72, 85, 87)
8. Klik **"Buat Tabel"**
9. Tunggu 10-30 detik
10. Klik **"Unduh"** → pilih **CSV**
11. Save as: `ekspor_hs_prioritas_2016-2020.csv`
12. Pindahkan ke: `tools/bpsapi/output/ekspor/`

#### Download A2 (Priority: ⭐⭐⭐)
1. **Refresh page** (F5)
2. Pilih **Ekspor**
3. Agregasi: **Menurut Kode HS**
4. Tahun: Centang **2021, 2022, 2023, 2024** (4 tahun BATCH 2)
5. Bulan: **Kosongkan**
6. Jenis HS: **HS 2 Digit**
7. Kode HS: Pilih **10 kode yang sama** (03, 08, 09, 15, 16, 24, 44, 72, 85, 87)
8. Klik **"Buat Tabel"**
9. Download CSV
10. Save as: `ekspor_hs_prioritas_2021-2024.csv`

#### Download A3 & A4 (Optional: ⭐)
Ulangi langkah di atas dengan **Kode HS Sekunder** (01, 02, 04, 07, 10, 21, 27, 39, 40, 64)

---

### DATASET B: Ekspor per Pelabuhan

#### Download B1 (Priority: ⭐⭐)
1. **Refresh page**
2. Pilih **Ekspor**
3. Agregasi: **Menurut Pelabuhan**
4. Tahun: **2016, 2017, 2018, 2019, 2020**
5. Bulan: **Kosongkan**
6. Pelabuhan: Pilih **Makassar, Bitung, Pantoloan, Kendari, Gorontalo, Mamuju**
7. Klik **"Buat Tabel"**
8. Download CSV
9. Save as: `ekspor_pelabuhan_sulawesi_2016-2020.csv`

#### Download B2 (Priority: ⭐⭐)
1. **Refresh page**
2. Pilih **Ekspor**
3. Agregasi: **Menurut Pelabuhan**
4. Tahun: **2021, 2022, 2023, 2024**
5. Pelabuhan: **6 pelabuhan yang sama**
6. Download CSV
7. Save as: `ekspor_pelabuhan_sulawesi_2021-2024.csv`

---

### DATASET C: Ekspor per Negara

#### Download C1 (Priority: ⭐⭐)
1. **Refresh page**
2. Pilih **Ekspor**
3. Agregasi: **Menurut Negara**
4. Tahun: **2016-2020**
5. Bulan: **Kosongkan**
6. Negara: Pilih **10 negara Asia** (China, Japan, Singapore, India, Malaysia, Thailand, South Korea, Taiwan, Vietnam, Philippines)
7. Klik **"Buat Tabel"**
8. Download CSV
9. Save as: `ekspor_negara_asia_2016-2020.csv`

#### Download C2 (Priority: ⭐⭐)
1. **Refresh page**
2. Pilih **Ekspor**
3. Agregasi: **Menurut Negara**
4. Tahun: **2021-2024**
5. Negara: **10 negara yang sama**
6. Download CSV
7. Save as: `ekspor_negara_asia_2021-2024.csv`

---

## Output Files

### Minimum (6 files):
```
ekspor_hs_prioritas_2016-2020.csv          ⭐⭐⭐
ekspor_hs_prioritas_2021-2024.csv          ⭐⭐⭐
ekspor_pelabuhan_sulawesi_2016-2020.csv    ⭐⭐
ekspor_pelabuhan_sulawesi_2021-2024.csv    ⭐⭐
ekspor_negara_asia_2016-2020.csv           ⭐⭐
ekspor_negara_asia_2021-2024.csv           ⭐⭐
```

### Full (8 files jika include sekunder):
```
+ ekspor_hs_sekunder_2016-2020.csv         ⭐
+ ekspor_hs_sekunder_2021-2024.csv         ⭐
```

## Lokasi Penyimpanan
```
c:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\tools\bpsapi\output\ekspor\
```

## Estimasi Waktu
- Per dataset (2 batch): 15-20 menit
- Total minimum (6 files): ~45-60 menit
- Total full (8 files): ~60-75 menit

## Troubleshooting
- **Tabel tidak muncul**: Kurangi range tahun (coba 3-4 tahun saja) atau kurangi jumlah kode HS (max 10)
- **Browser hang**: Data terlalu besar, refresh dan pilih lebih sedikit field (5 kode HS atau 3 tahun)
- **Download gagal**: Coba format berbeda (CSV ↔ Excel) atau split menjadi batch lebih kecil
- **Error "Maximum field exceeded"**: Terlalu banyak field dipilih, kurangi jumlah tahun/kode HS/pelabuhan/negara
- **Kode HS tidak bisa dikosongkan**: HARUS pilih kode spesifik, gunakan 10 kode prioritas yang sudah disebutkan


---

## ⏱️ ESTIMASI WAKTU

| Download | Estimasi | Kompleksitas |
|----------|----------|--------------|
| A1: HS Priority 2016-2020 | 8-10 menit | ⭐⭐⭐ (Mandatory) |
| A2: HS Priority 2021-2024 | 8-10 menit | ⭐⭐⭐ (Mandatory) |
| A3: HS Secondary 2016-2020 | 8-10 menit | ⭐ (Optional) |
| A4: HS Secondary 2021-2024 | 8-10 menit | ⭐ (Optional) |
| B1: Pelabuhan 2016-2020 | 5-8 menit | ⭐⭐ (Good to have) |
| B2: Pelabuhan 2021-2024 | 5-8 menit | ⭐⭐ (Good to have) |
| C1: Negara 2016-2020 | 5-8 menit | ⭐⭐ (Good to have) |
| C2: Negara 2021-2024 | 5-8 menit | ⭐⭐ (Good to have) |
| **Total Minimum (6 files)** | **45-60 menit** | |
| **Total Full (8 files)** | **60-75 menit** | |

---

## ✅ CHECKLIST

```
DATASET A: Ekspor per Sektor (HS)
☐ A1: HS Priority 2016-2020 ⭐⭐⭐ MANDATORY
  ☐ 10 kode HS selected (03, 08, 09, 15, 16, 24, 44, 72, 85, 87)
  ☐ 5 years selected (2016-2020)
  ☐ CSV downloaded
  ☐ File: ekspor_hs_prioritas_2016-2020.csv
  
☐ A2: HS Priority 2021-2024 ⭐⭐⭐ MANDATORY
  ☐ 10 kode HS yang sama
  ☐ 4 years selected (2021-2024)
  ☐ CSV downloaded
  ☐ File: ekspor_hs_prioritas_2021-2024.csv
  
☐ A3: HS Secondary 2016-2020 ⭐ OPTIONAL
  ☐ 10 kode HS sekunder
  ☐ File: ekspor_hs_sekunder_2016-2020.csv
  
☐ A4: HS Secondary 2021-2024 ⭐ OPTIONAL
  ☐ 10 kode HS sekunder
  ☐ File: ekspor_hs_sekunder_2021-2024.csv

DATASET B: Ekspor per Pelabuhan
☐ B1: Pelabuhan 2016-2020 ⭐⭐
  ☐ 6 pelabuhan Sulawesi selected
  ☐ 5 years (2016-2020)
  ☐ File: ekspor_pelabuhan_sulawesi_2016-2020.csv
  
☐ B2: Pelabuhan 2021-2024 ⭐⭐
  ☐ 6 pelabuhan yang sama
  ☐ 4 years (2021-2024)
  ☐ File: ekspor_pelabuhan_sulawesi_2021-2024.csv
  
DATASET C: Ekspor per Negara
☐ C1: Negara Asia 2016-2020 ⭐⭐
  ☐ 10 negara Asia selected
  ☐ 5 years (2016-2020)
  ☐ File: ekspor_negara_asia_2016-2020.csv
  
☐ C2: Negara Asia 2021-2024 ⭐⭐
  ☐ 10 negara yang sama
  ☐ 4 years (2021-2024)
  ☐ File: ekspor_negara_asia_2021-2024.csv

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MINIMUM: 6 files ✅
FULL: 8 files ✅
```

---

## 🆘 TROUBLESHOOTING

### ❌ Tombol "Buat Tabel" tidak aktif
**Penyebab:** Belum pilih semua field wajib
**Solusi:** 
- Pastikan **Pilih Data** sudah dipilih (Ekspor)
- Pastikan **Agregasi** sudah dipilih
- Pastikan **Tahun** sudah dipilih minimal 1

### ❌ Tabel tidak muncul setelah klik "Buat Tabel"
**Penyebab:** Data terlalu besar atau loading lambat
**Solusi:**
- Tunggu 30-60 detik
- Refresh page dan coba lagi
- Kurangi range tahun (coba 2020-2024 dulu)

### ❌ Browser hang/freeze
**Penyebab:** Terlalu banyak data di-load sekaligus
**Solusi:**
- Close tab, buka tab baru
- Gunakan **HS 2 Digit** bukan HS Full
- Jangan pilih > 10 kode HS sekaligus
- Pilih tahun lebih sedikit (split jadi 2016-2020, 2021-2024)

### ❌ File download corrupt / 0 KB
**Penyebab:** Download interrupted
**Solusi:**
- Re-download
- Coba format berbeda (Excel jika CSV gagal)
- Check disk space

### ❌ Data missing untuk tahun tertentu
**Penyebab:** Data memang belum tersedia/published
**Solusi:**
- **Normal** - BPS publish data dengan delay
- Catat missing years di checklist
- Lanjutkan dengan data yang available

---

## 📊 EXPECTED OUTPUT

### File A1 & A2: ekspor_hs_prioritas_*.csv
**Struktur:**
```
Kode_HS | Deskripsi | 2016 | 2017 | 2018 | 2019 | 2020 | (atau 2021-2024)
03      | Ikan      | xxx  | xxx  | xxx  | xxx  | xxx  |
08      | Buah      | xxx  | xxx  | xxx  | xxx  | xxx  |
09      | Kopi      | xxx  | xxx  | xxx  | xxx  | xxx  |
...
```

**Estimasi size:** 30-100 KB per file  
**Estimasi rows:** 10 kode HS × 5 years (A1) atau 10 × 4 years (A2)

### File B1 & B2: ekspor_pelabuhan_sulawesi_*.csv
**Struktur:**
```
Pelabuhan | Tahun | Berat_KG | Nilai_USD |
MAKASSAR  | 2016  | xxx      | xxx       |
MAKASSAR  | 2017  | xxx      | xxx       |
BITUNG    | 2016  | xxx      | xxx       |
...
```

**Estimasi size:** 15-50 KB per file  
**Estimasi rows:** 6 pelabuhan × 5 years (B1) atau 6 × 4 years (B2)

### File C1 & C2: ekspor_negara_asia_*.csv
**Struktur:**
```
Negara     | Tahun | Berat_KG | Nilai_USD |
CHINA      | 2016  | xxx      | xxx       |
CHINA      | 2017  | xxx      | xxx       |
JAPAN      | 2016  | xxx      | xxx       |
...
```

**Estimasi size:** 30-100 KB per file  
**Estimasi rows:** 10 negara × 5 years (C1) atau 10 × 4 years (C2)

---

## 💾 FILE MANAGEMENT

### Output Folder Structure
```
tools/bpsapi/output/ekspor/
├── ekspor_hs_prioritas_2016-2020.csv          ⭐⭐⭐ MANDATORY
├── ekspor_hs_prioritas_2021-2024.csv          ⭐⭐⭐ MANDATORY
├── ekspor_hs_sekunder_2016-2020.csv           ⭐ OPTIONAL
├── ekspor_hs_sekunder_2021-2024.csv           ⭐ OPTIONAL
├── ekspor_pelabuhan_sulawesi_2016-2020.csv    ⭐⭐ 
├── ekspor_pelabuhan_sulawesi_2021-2024.csv    ⭐⭐
├── ekspor_negara_asia_2016-2020.csv           ⭐⭐
└── ekspor_negara_asia_2021-2024.csv           ⭐⭐
```

### Backup
Setelah download selesai, backup files:
```bash
# Copy ke folder backup (Windows CMD)
xcopy ekspor\*.csv ekspor\backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%\ /Y
```

---

## 🔄 NEXT STEP: PROCESSING

Setelah files downloaded, jalankan processing script:

```bash
cd tools\bpsapi
python process_ekspor_downloads.py
```

Script akan:
1. ✅ Read multiple batch files (6-8 CSV files)
2. ✅ Merge batches per dataset (merge 2016-2020 + 2021-2024)
3. ✅ Clean & standardize columns
4. ✅ Map HS codes to sector names
5. ✅ Map pelabuhan to provinces
6. ✅ Aggregate by year
7. ✅ Calculate growth rates
8. ✅ Generate 3 consolidated datasets:
   - `ekspor_hs_consolidated_2016-2024.csv`
   - `ekspor_pelabuhan_consolidated_2016-2024.csv`
   - `ekspor_negara_consolidated_2016-2024.csv`

---

## 📞 BANTUAN

**BPS Call Center:**
- Phone: 082373736742
- Email: bps@bps.go.id
- WhatsApp: http://s.bps.go.id/wa-pst

**Website issues:**
- Clear browser cache: Ctrl+Shift+Del
- Try different browser (Chrome, Firefox, Edge)
- Use Incognito/Private mode

---

## 📝 CATATAN PENTING

1. **Data update frequency**: BPS publish data bulanan dengan delay ~2 bulan
2. **Data revisi**: BPS bisa revisi data historis, check "Periode data terbaru" notice di halaman
3. **Missing data**: Normal untuk beberapa komoditas/periode tidak ada data
4. **Aggregation**: Data sudah diagregasi oleh BPS, bukan raw trade data
5. **Currency**: Semua nilai dalam **USD** (US Dollar)
6. **Weight**: Semua berat dalam **Kilogram (KG)**

---

*Panduan created: 9 Juni 2026*  
*Data source: BPS Data Ekspor Impor Nasional*  
*CELIOS ECC Intelligence System*
