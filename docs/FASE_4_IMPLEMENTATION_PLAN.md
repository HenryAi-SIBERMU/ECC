# FASE 4: Analisis Demografi, Sosial, & Ketenagakerjaan
**CELIOS ECC Intelligence System - Implementation Plan**  
**Date:** 26 Juni 2026  
**Status:** IN PROGRESS

---

## 🎯 Objective

**TARGET:** Mengukur pergeseran struktur sosial di lingkar tambang/smelter

**NARASI KRITIS:**
Ekspansi industri nikel di Sulawesi tidak hanya merusak ekologi, tetapi juga memicu **pergeseran masif struktur sosial** di lingkar tambang:
1. **Migrasi besar-besaran** pekerja dari luar provinsi → tekanan demografi
2. **Urbanisasi dipaksakan** → desa berubah jadi kota industri tanpa infrastruktur memadai
3. **Transisi ekonomi brutal** → masyarakat agraris dipaksa jadi buruh industri, kehilangan akses lahan

---

## 📋 Roadmap Tasks (From Rev1 Document)

### Task 1: Ekstraksi Data Migrasi Penduduk
**Target:** Data migrasi antar kabupaten/provinsi (dampak smelter)
**Source:** BPS - Data Migrasi Risen/Masuk/Keluar

### Task 2: Pengambilan Data Perubahan Pola Ruang
**Target:** Data urbanisasi (perubahan desa → kota)
**Source:** BPS - Data Klasifikasi Perkotaan/Perdesaan, Kepadatan Penduduk

### Task 3: Mapping Perubahan Jenis Pekerjaan
**Target:** Peralihan dari sektor agraris ke industri
**Source:** BPS - Data Ketenagakerjaan per Sektor, Sakernas

---

## 📊 Data Availability Assessment

### A. Migration Data (Migrasi Penduduk)

**BPS API Search:**
- ❓ **Status:** NEED TO SEARCH
- 🔍 **Search keywords:** "migrasi", "penduduk datang", "penduduk pergi", "mobilitas"
- 📍 **Domains:** Sulawesi provinces (7100, 7200, 7300, 7400, 7500, 7600)
- 📅 **Period:** 2014-2024 (1 dekade, before & after smelter boom)

**Expected Variables:**
- Jumlah penduduk datang (migrasi masuk)
- Jumlah penduduk pergi (migrasi keluar)
- Migrasi risen (antar kabupaten dalam provinsi)
- Migrasi sirkuler (temporary worker migration)

**Alternative Sources:**
1. BPS Provincial Publications (Sulawesi Dalam Angka)
2. BPS "Statistik Mobilitas Penduduk dan Tenaga Kerja"
3. Manual download from BPS provincial query-builder

### B. Urbanization Data (Perubahan Pola Ruang)

**BPS API Search:**
- ❓ **Status:** NEED TO SEARCH
- 🔍 **Search keywords:** "perkotaan", "perdesaan", "klasifikasi wilayah", "kepadatan penduduk"
- 📍 **Domains:** Sulawesi provinces + kabupaten near smelters
- 📅 **Period:** 2014-2024

**Expected Variables:**
- Jumlah desa yang berubah jadi kelurahan
- Persentase penduduk perkotaan vs perdesaan
- Kepadatan penduduk (jiwa/km²)
- Laju urbanisasi (% per tahun)

**Target Kabupaten (Smelter Locations):**
- **Sulawesi Tengah:** Morowali, Morowali Utara, Banggai
- **Sulawesi Tenggara:** Konawe, Konawe Utara, Kolaka
- **Sulawesi Selatan:** Luwu Timur
- **Sulawesi Utara:** Minahasa (potensi ekspansi)

**Alternative Sources:**
1. Permendagri data on desa → kelurahan conversion
2. BPS "Indikator Strategis Kependudukan"
3. Podes (Potensi Desa) dataset

### C. Employment Structure Data (Perubahan Jenis Pekerjaan)

**BPS API Search:**
- ❓ **Status:** NEED TO SEARCH
- 🔍 **Search keywords:** "ketenagakerjaan", "lapangan usaha", "sektor", "sakernas", "pekerjaan utama"
- 📍 **Domains:** Sulawesi provinces
- 📅 **Period:** 2014-2024

**Expected Variables:**
- Jumlah pekerja sektor pertanian/perkebunan/perikanan
- Jumlah pekerja sektor industri pengolahan
- Jumlah pekerja sektor pertambangan
- Persentase angkatan kerja per sektor

**BPS Codes:**
- Klasifikasi Lapangan Usaha (KLU):
  - **A:** Pertanian, Kehutanan, Perikanan
  - **B:** Pertambangan dan Penggalian
  - **C:** Industri Pengolahan
  - **F:** Konstruksi

**Alternative Sources:**
1. Sakernas (Survei Angkatan Kerja Nasional) - provincial level
2. BPS "Keadaan Angkatan Kerja Provinsi"
3. Kemendagri data on occupational shifts

---

## 🔍 Phase 1: Data Discovery (CURRENT STEP)

### Step 1.1: Search BPS API for Migration Data
```python
# Search for migration-related dynamic tables
keywords = ["migrasi", "penduduk datang", "penduduk pergi", "mobilitas", "perpindahan"]
domains = ["7100", "7200", "7300", "7400", "7500", "7600"]

for domain in domains:
    tables = client.list_dynamic_tables(domain=domain)
    for table in tables:
        if any(kw in table['title'].lower() for kw in keywords):
            print(f"FOUND: {domain} - {table}")
```

**Output:** List of available migration tables per province

### Step 1.2: Search BPS API for Urbanization Data
```python
keywords = ["perkotaan", "perdesaan", "klasifikasi", "kepadatan", "urbanisasi"]
# Same search approach
```

### Step 1.3: Search BPS API for Employment Data
```python
keywords = ["tenaga kerja", "ketenagakerjaan", "lapangan usaha", "sektor", "pekerjaan"]
# Same search approach
```

### Step 1.4: Document Findings
Create detailed report:
- What data is available via API
- What needs manual download
- What is completely unavailable (requires scraping or alternative source)

---

## 🛠️ Phase 2: Data Extraction

### Option A: Via BPS API (if available)
```python
# Fetch migration data
migration_data = client.get_dynamic_table(
    domain='7300',
    var_id='XXXX',  # To be determined from search
    year='2014:2024'
)
```

### Option B: Manual Download + Processing
If API not available:
1. Create download guide (like PAD/Ekspor)
2. User downloads from BPS provincial websites
3. Create processing script to consolidate

### Option C: Web Scraping (last resort)
For data not available via API or manual download:
1. Target: BPS provincial publications (PDF)
2. Tool: LlamaParse or pdfplumber
3. Extract tables from "Sulawesi Dalam Angka" yearbooks

---

## 📊 Phase 3: Data Processing

### Output Files (Target)

1. **`sulawesi_migrasi_2014_2024.csv`**
   - Columns: `provinsi`, `kabupaten`, `tahun`, `migrasi_masuk`, `migrasi_keluar`, `migrasi_neto`
   - Rows: ~600 (6 provinces × 10 years × ~10 kabupaten/province)

2. **`sulawesi_urbanisasi_2014_2024.csv`**
   - Columns: `provinsi`, `kabupaten`, `tahun`, `pct_perkotaan`, `pct_perdesaan`, `kepadatan_per_km2`, `desa_to_kelurahan_count`
   - Rows: ~600

3. **`sulawesi_ketenagakerjaan_sektor_2014_2024.csv`**
   - Columns: `provinsi`, `tahun`, `sektor`, `jumlah_pekerja`, `pct_dari_total`
   - Rows: ~300 (6 provinces × 10 years × 5 major sectors)

### Processing Script Structure
```python
# tools/process_demografi_fase4.py

def process_migration_data(raw_files):
    """Consolidate migration data from multiple sources"""
    # Clean column names
    # Standardize province names
    # Calculate net migration
    # Add smelter proximity flag
    return df

def process_urbanization_data(raw_files):
    """Process urbanization metrics"""
    # Calculate urbanization rate
    # Flag kabupaten with smelters
    # Compute growth rates
    return df

def process_employment_data(raw_files):
    """Aggregate employment by sector"""
    # Group by major sectors
    # Calculate sector shifts
    # Identify agriculture → industry transitions
    return df
```

---

## 📈 Phase 4: Dashboard Integration

### New Section or Page?

**RECOMMENDATION:** Add to existing **Page 3 (Beban Kesehatan)** as new sections

**Why?**
- Social impacts are directly related to health burden
- Migration → overcrowding → disease spread
- Urbanization → loss of clean water/sanitation → health crisis
- Job shifts → stress, unsafe working conditions → health issues

### Proposed Structure: Page 3 New Sections

#### **3.6 Ledakan Migrasi: Tekanan Demografi di Kawasan Smelter**
- **Visual:** Line chart showing migration trends (masuk vs keluar) over time
- **Comparison:** Smelter kabupaten vs non-smelter kabupaten
- **Narrative:** "Sejak 2017, kabupaten dengan smelter mengalami lonjakan migrasi masuk hingga 300%, menciptakan tekanan demografi ekstrem"

#### **3.7 Urbanisasi Dipaksakan: Desa Berubah Jadi Kota Tanpa Infrastruktur**
- **Visual:** Bar chart or heatmap showing urbanization rate by kabupaten
- **Highlight:** Morowali, Konawe (highest rates)
- **Narrative:** "Urbanisasi di kawasan smelter terjadi tanpa perencanaan matang—kepadatan penduduk melonjak tapi infrastruktur kesehatan tidak berkembang"

#### **3.8 Transisi Ekonomi Brutal: Dari Petani Jadi Buruh Industri**
- **Visual:** Stacked area chart showing employment sector shifts
- **Comparison:** 2014 (pre-boom) vs 2024 (post-boom)
- **Narrative:** "Masyarakat agraris kehilangan akses lahan, dipaksa jadi buruh industri dengan upah rendah dan risiko kesehatan tinggi"

---

## 🔄 Alternative Approach (If Data Limited)

If comprehensive data NOT available from BPS:

### Proxy Indicators

1. **Migration Proxy:**
   - Use population growth rate anomalies
   - Compare pre-smelter vs post-smelter population spikes
   - Flag kabupaten with >5% annual growth (abnormal for non-urban areas)

2. **Urbanization Proxy:**
   - Use population density increases
   - Count number of kecamatan classified as urban
   - Infrastructure expansion (road, electricity connection)

3. **Employment Proxy:**
   - Use PMDN investment in industrial sector as employment indicator
   - Cross-reference with number of IUP permits (more permits = more mining jobs)
   - Use PDRB sector contribution shifts (agriculture decline = job shift)

### Data We ALREADY Have:
- ✅ `sulawesi_investasi_pmdn_2016_2024.csv` (can use as industrial employment proxy)
- ✅ `sulawesi_esdm_nikel.csv` (mining permits = job creation indicator)
- ✅ `data/raw/bps_pdrb/bps_pdrb_sulawesi_2016_2026.csv` (PDRB by sector = employment indicator)

---

## ⏱️ Timeline

### Week 1 (Current): Data Discovery
- [x] Read roadmap document
- [ ] Search BPS API for migration data
- [ ] Search BPS API for urbanization data
- [ ] Search BPS API for employment data
- [ ] Create data availability report

### Week 2: Data Extraction
- [ ] Extract available data from API
- [ ] Create manual download guide (if needed)
- [ ] Download manual data (if needed)
- [ ] Set up processing scripts

### Week 3: Data Processing & Analysis
- [ ] Clean and consolidate data
- [ ] Calculate derived metrics (migration rate, urbanization rate, sector shifts)
- [ ] Flag smelter vs non-smelter kabupaten
- [ ] Generate summary statistics

### Week 4: Dashboard Implementation
- [ ] Create Section 3.6 (Migration visualization)
- [ ] Create Section 3.7 (Urbanization visualization)
- [ ] Create Section 3.8 (Employment sector shifts)
- [ ] Write narrative connecting to health burden
- [ ] Testing and refinement

---

## 🎯 Success Criteria

### Data Quality
- ✅ Time series coverage: minimum 2014-2024 (1 dekade)
- ✅ Geographic coverage: all 6 Sulawesi provinces
- ✅ Granularity: kabupaten level (not just province aggregates)

### Narrative Impact
- ✅ Clear before/after comparison (pre-smelter vs post-smelter boom)
- ✅ Quantified social shifts (e.g., "300% increase in migration")
- ✅ Direct link to health/environmental impacts already shown in other sections

### Visualization Quality
- ✅ Interactive charts with year sliders
- ✅ Smelter vs non-smelter comparison
- ✅ Executive summary with key statistics

---

## 📞 Next Actions

### Immediate (Agent):
1. ✅ Create this implementation plan
2. ⏳ Run BPS API search for migration data
3. ⏳ Run BPS API search for urbanization data
4. ⏳ Run BPS API search for employment data
5. ⏳ Create data availability report

### User Decision Required:
- Approve approach (comprehensive data vs proxy indicators)
- Confirm dashboard location (Page 3 vs new page)
- Prioritize tasks if data availability limited

---

*Document created: 26 Juni 2026*  
*CELIOS ECC Intelligence System - Fase 4 Execution*
