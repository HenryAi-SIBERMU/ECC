# RENCANA PENGUMPULAN DATA: IUP TANPA FPIC & TAMBANG TANPA IZIN

## TUJUAN:
Menyusun dataset untuk narasi kritis di Page 5 tentang:
1. **IUP yang terbit tanpa FPIC** (Free, Prior, and Informed Consent)
2. **Tambang ilegal/tanpa izin** yang beroperasi

---

## STRATEGI PENGUMPULAN DATA:

### **FASE 1: GUNAKAN DATA YANG SUDAH ADA** ✅

#### A. Data Konflik Agraria Tanahkita (SUDAH ADA)
**File**: `data/processed/nasional_konflik_agraria_tanahkita.csv`

**Filter untuk Sulawesi + Pertambangan:**
- Status: "Pertambangan", "Tambang Emas", "Nikel", "Batubara"
- Lokasi: Contains "Sulawesi"
- Indikasi: Konflik dengan masyarakat adat, penolakan, kriminalisasi

**Expected Output**: 5-15 kasus konflik tambang di Sulawesi

---

#### B. Data Perusahaan Tambang (SUDAH ADA)
**File**: `tools/scrapling/output/full/minerbaone_details.csv`

**Content**: 
- 24,000+ perusahaan tambang terdaftar di Minerba.One
- Data: nama perusahaan, NIB, NPWP, alamat, jenis usaha
- **CATATAN**: Data ini adalah perusahaan TERDAFTAR, bukan yang tanpa izin

**Gunakan untuk**: Cross-reference perusahaan yang disebutkan dalam konflik

---

### **FASE 2: DORKING & WEB SCRAPING** 🔍

#### C. Google Dorking untuk Temukan Kasus FPIC Violations

**Target Sources:**
1. **Tanahkita.id** - Database konflik agraria
2. **EJAtlas.org** - Environmental Justice Atlas
3. **AMAN** (Aliansi Masyarakat Adat Nusantara)
4. **WALHI** (Wahana Lingkungan Hidup Indonesia)
5. **JATAM** (Jaringan Advokasi Tambang)
6. **Climate Rights International**
7. **Mighty Earth**

**Dorking Queries:**
```
site:tanahkita.id "Sulawesi" "tambang" "tanpa konsultasi"
site:tanahkita.id "IUP" "masyarakat adat" "konflik"
site:walhi.or.id "tambang nikel" "Sulawesi" "FPIC"
site:jatam.org "IUP" "ilegal" "Sulawesi"
"tambang nikel" "Sulawesi" "tanpa izin AMDAL"
"free prior informed consent" "nickel mining" "Sulawesi"
"PT" "nikel" "Sulawesi" "konflik agraria"
```

---

#### D. Scraping Target Websites

**1. Tanahkita.id - Konflik Detail Pages**
- URL Pattern: `https://tanahkita.id/data/data/konflik/detil/[ID]`
- Target Fields:
  - Nama perusahaan
  - Lokasi (provinsi, kabupaten)
  - Narasi konflik (check for FPIC violations keywords)
  - Luas lahan (hektar)
  - Dampak jiwa
  - Status IUP/izin
  - Indikasi kriminalisasi

**Keywords untuk Filter:**
- "tanpa konsultasi"
- "tanpa persetujuan"
- "tanpa sosialisasi"
- "masyarakat tidak dilibatkan"
- "FPIC dilanggar"
- "izin tidak jelas"
- "izin bermasalah"
- "tambang ilegal"

---

**2. JATAM Database**
- Website: https://www.jatam.org
- Target: Laporan investigasi tambang bermasalah
- Format: PDF reports, article pages

---

**3. WALHI Regional Sulawesi**
- Sulawesi Tengah WALHI
- Sulawesi Tenggara WALHI
- Sulawesi Selatan WALHI

---

### **FASE 3: API & GOVERNMENT DATA** 🏛️

#### E. ESDM Open Data (Jika Tersedia)
**Target**: 
- List IUP Nikel Sulawesi
- Status AMDAL
- Status operasi

**API/Website**:
- https://geoportal.esdm.go.id
- https://modi.esdm.go.id (Minerba Online Data Indonesia)

**CATATAN**: Data pemerintah biasanya tidak akan label "tanpa FPIC" atau "ilegal" - perlu cross-reference dengan laporan NGO

---

#### F. Cross-Check dengan GIS Data
**Data yang Sudah Ada**:
- `sulawesi_kawasan_nikel_luas.csv` - Luas kawasan IUP per provinsi
- `sulawesi_izin_baru_per_tahun.csv` - Izin baru per tahun

**Analisis**:
- Korelasi antara wilayah adat/hutan konservasi dengan kawasan tambang
- Identifikasi overlap antara IUP dan wilayah yang seharusnya dilindungi

---

### **FASE 4: MANUAL RESEARCH & LAPORAN NGO** 📄

#### G. Download & Extract dari Laporan NGO

**Target Reports:**
1. **Climate Rights International** - "Indonesia Nickel Industry" (2024-2025)
2. **Mighty Earth** - "From Forests to Electric Vehicles" (2024)
3. **JATAM Annual Reports** (2020-2024)
4. **WALHI Sulawesi Reports**
5. **KPA Catatan Akhir Tahun** (2020-2024)

**Information to Extract**:
- Nama perusahaan spesifik
- Lokasi tambang
- Jenis pelanggaran (FPIC, AMDAL, izin)
- Dampak ke masyarakat
- Status legal

---

## EXPECTED OUTPUT DATASET:

### **File 1: `sulawesi_iup_fpic_violations.csv`**
```csv
nama_perusahaan,lokasi_provinsi,lokasi_kabupaten,komoditas,luas_ha,tahun_iup,jenis_pelanggaran,dampak_masyarakat,sumber_laporan,url_referensi
PT ABC Mining,Sulawesi Tengah,Morowali,Nikel,5000,2018,"Tanpa FPIC, AMDAL tidak memadai","1200 jiwa kehilangan lahan",Climate Rights International,https://...
```

### **File 2: `sulawesi_tambang_ilegal.csv`**
```csv
nama_perusahaan,lokasi,status_izin,jenis_pelanggaran,tahun_operasi,sumber_laporan
PT XYZ,Kolaka,Tidak ada IUP,Operasi tanpa izin,2020,JATAM Report
```

### **File 3: `sulawesi_konflik_agraria_tambang_processed.csv`**
Filter dari tanahkita.csv:
- Sulawesi only
- Pertambangan sector
- With FPIC/consultation issues

---

## TOOLS & SCRIPTS YANG DIPERLUKAN:

### **Script 1: Filter Tanahkita Data**
```python
# File: scripts/filter_tanahkita_sulawesi_mining.py
# Filter konflik agraria yang relevan dengan Sulawesi + tambang
```

### **Script 2: Google CSE Dorking**
```python
# File: scripts/dork_fpic_violations.py
# Search untuk kasus FPIC violations via Google CSE
```

### **Script 3: Tanahkita Detail Scraper**
```python
# File: scripts/scrape_tanahkita_details.py
# Extract detail narasi dari konflik pages
```

### **Script 4: Cross-Reference IUP & Konflik**
```python
# File: scripts/cross_ref_iup_konflik.py
# Match perusahaan dalam minerbaone_details.csv dengan konflik
```

---

## TIMELINE ESTIMASI:

**FASE 1** (2-3 jam):
- ✅ Filter data tanahkita yang sudah ada
- ✅ Create processed dataset dari existing data

**FASE 2** (4-6 jam):
- 🔍 Google dorking untuk kasus baru
- 🕷️ Scraping tanahkita detail pages
- 🕷️ Scraping JATAM/WALHI websites

**FASE 3** (2-3 jam):
- 🏛️ Check ESDM open data
- 🗺️ GIS overlay analysis

**FASE 4** (3-4 jam):
- 📄 Manual download laporan NGO (PDF)
- 📊 Extract data from reports
- ✍️ Compile final dataset

**TOTAL**: 11-16 jam kerja

---

## RISIKO & MITIGASI:

### **Risk 1**: Data FPIC violations tidak eksplisit dalam database pemerintah
**Mitigasi**: Cross-reference dengan laporan NGO yang kredibel (CRI, Mighty Earth, JATAM)

### **Risk 2**: Tanahkita detail pages banyak yang tidak lengkap
**Mitigasi**: Use multiple sources (EJAtlas, AMAN, WALHI)

### **Risk 3**: Tidak ada "list resmi" tambang ilegal
**Mitigasi**: Identifikasi dari laporan media, NGO, dan kronologi konflik

---

## PRIORITAS EKSEKUSI:

**PRIORITAS 1** (HARI INI):
1. ✅ Filter `nasional_konflik_agraria_tanahkita.csv` untuk Sulawesi + Pertambangan
2. ✅ Create quick dataset dengan 10-15 kasus yang sudah terdokumentasi
3. ✅ Buat visualisasi sederhana untuk Page 5

**PRIORITAS 2** (BESOK):
1. 🔍 Dorking untuk kasus tambahan
2. 🕷️ Scraping detail dari tanahkita
3. 📄 Download 2-3 laporan NGO utama

**PRIORITAS 3** (LUSA):
1. 🏛️ Cross-check dengan data ESDM (jika ada)
2. ✍️ Compile comprehensive dataset
3. 📊 Create advanced visualizations

---

## SUMBER REFERENSI KREDIBEL:

1. **Climate Rights International** ⭐⭐⭐⭐⭐
2. **Mighty Earth** ⭐⭐⭐⭐⭐
3. **JATAM (Jaringan Advokasi Tambang)** ⭐⭐⭐⭐⭐
4. **WALHI** ⭐⭐⭐⭐⭐
5. **AMAN** ⭐⭐⭐⭐⭐
6. **Tanahkita.id** ⭐⭐⭐⭐
7. **EJAtlas** ⭐⭐⭐⭐
8. **Business & Human Rights Resource Centre** ⭐⭐⭐⭐
9. **Mongabay Indonesia** ⭐⭐⭐⭐
10. **KPA (Konsorsium Pembaruan Agraria)** ⭐⭐⭐⭐

---

## NEXT STEPS:

**Mau saya lanjutkan dengan:**
1. ✅ **PRIORITAS 1**: Filter data tanahkita yang sudah ada dan buat quick dataset?
2. 🔍 **Dorking script**: Buat script untuk cari kasus FPIC violations via CSE?
3. 🕷️ **Scraping script**: Buat scraper untuk tanahkita detail pages?
4. 📊 **Visualisasi**: Langsung buat visualisasi di Page 5 dengan data yang ada?

**Pilih mana yang mau dikerjakan dulu?**
