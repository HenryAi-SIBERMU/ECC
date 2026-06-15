# Strategi Akuisisi Data Laju Deforestasi Sulawesi
## Checkpoint 1 - Prioritas #4 (KLHK - Deforestasi)

---

**Target:** Laju Deforestasi Sulawesi 2016-2024  
**Use Case:** Checkpoint 4 - Penurunan Kualitas Lingkungan & Tekanan Ekologis  
**Status:** 🔄 Planning Phase  
**Dibuat:** 14 Juni 2026  

---

## 📊 TARGET DATA SPECIFICATION

### Data Requirements:
- **Variabel Utama:**
  - Laju deforestasi (hektar/tahun)
  - Tutupan hutan (% dari total luas wilayah)
  - Kehilangan hutan (forest loss) dalam hektar
  - Perubahan penggunaan lahan
  
- **Coverage Geografis:**
  - 6 Provinsi Sulawesi (Sulut, Sulteng, Sulsel, Sultra, Gorontalo, Sulbar)
  - Granularity: Per provinsi (minimum), per kabupaten (ideal)
  
- **Time Series:**
  - Rentang: 2016-2024 (9 tahun)
  - Frequency: Annual (tahunan)
  
- **Expected Volume:**
  - ~54-450 data points (6 provinsi × 9 tahun, atau breakdown per kabupaten)

### Data Output Target:
```
data/processed/sulawesi_deforestasi_2016_2024.csv

Columns:
- province (string)
- year (int)
- deforestation_rate_ha (float) - Laju deforestasi dalam hektar
- forest_cover_pct (float) - Persentase tutupan hutan
- forest_loss_ha (float) - Kehilangan hutan tahunan
- total_area_ha (float) - Total luas wilayah
- data_source (string) - Sumber data
- confidence_level (string) - High/Medium/Low
- notes (string) - Catatan metodologi
```

---

## 🎯 MULTI-TIER ACQUISITION STRATEGY

### **TIER 1: Government Official Sources (FREE, HIGH CREDIBILITY)**

#### 1A. KLHK - Direktorat Jenderal Planologi Kehutanan ⭐⭐⭐⭐⭐

##### **SIMONTANA (Sistem Monitoring Hutan Nasional)**
- **Portal:** http://simontana.menlhk.go.id
- **Data Available:**
  - ✅ Laju deforestasi per provinsi (annual)
  - ✅ Tutupan hutan & perubahan tutupan lahan
  - ✅ Peta interaktif deforestasi
  - ✅ Download formats: PDF, Excel, Shapefile (GIS)
  
- **Access Method:** 
  - Web scraping + Form automation
  - API exploration (check for hidden endpoints)
  - Manual download sebagai fallback
  
- **Tools/Scripts:**
  ```
  tools/klhk/scrape_simontana_deforestasi.py
  tools/klhk/parse_simontana_reports.py
  ```

- **Expected Output:**
  ```
  data/raw/klhk_simontana/deforestasi_sulawesi_20XX.pdf
  data/raw/klhk_simontana/tutupan_hutan_sulawesi_20XX.xlsx
  ```

##### **Statistik KLHK Portal**
- **Portal:** http://statistik.menlhk.go.id
- **Alternative:** http://data.menlhk.go.id
- **Data Available:**
  - ✅ Statistik Lingkungan Hidup Kehutanan Indonesia
  - ✅ Laju deforestasi netto & bruto
  - ✅ Perubahan tutupan lahan per provinsi
  
- **Access Method:**
  - Check portal data terbuka KLHK
  - Direct download statistical reports
  - API exploration jika tersedia
  
- **Tools/Scripts:**
  ```
  tools/klhk/scrape_statistik_klhk.py
  scripts/download_klhk_reports.py
  ```

##### **SLHI (Status Lingkungan Hidup Indonesia)** ✅ ALREADY HAVE
- **Source:** `data/raw/klhk_sulut_kualitas_air/SLHI_*.pdf`
- **Coverage:** SLHI 2015-2025 (11 files sudah downloaded)
- **Action Required:** 
  - Re-extract deforestation sections dari SLHI PDFs
  - Focus on "Tutupan Hutan" & "Kehilangan Hutan" sections
  
- **Tools/Scripts:**
  ```
  tools/pdf_extraction/extract_deforestasi_slhi.py
  scripts/parse_slhi_forest_sections.py
  ```

- **Expected Output:**
  ```
  data/raw/klhk_slhi/deforestasi_sulawesi_2015_2025_extracted.csv
  data/raw/intermediate_deforestasi/slhi_forest_cover_*.csv
  ```

---

#### 1B. BPS - Statistik Lingkungan Hidup ⭐⭐⭐⭐

##### **BPS API - Forest Variables**
- **Endpoint:** https://webapi.bps.go.id/v1/api/list
- **Target Variables:**
  - "Luas kawasan hutan"
  - "Tutupan lahan/hutan"
  - "Lahan kritis"
  - "Perubahan penggunaan lahan"
  
- **Domain Search:**
  - 0000 (Nasional aggregate)
  - 7100 (Sulawesi Utara)
  - 7200 (Sulawesi Tengah)
  - 7300 (Sulawesi Selatan)
  - 7400 (Sulawesi Tenggara)
  - 7500 (Gorontalo)
  - 7600 (Sulawesi Barat)
  
- **Tools/Scripts:**
  ```
  tools/bpsapi/search_deforestasi.py
  tools/bpsapi/fetch_forest_variables.py
  ```

- **Expected Variables:**
  ```python
  # Possible BPS Variable IDs (TBD):
  # - Var XXX: "Luas Hutan per Provinsi"
  # - Var YYY: "Lahan Kritis"
  # - Var ZZZ: "Tutupan Lahan"
  ```

##### **BPS Publications - Statistik Lingkungan Hidup**
- **Portal:** https://www.bps.go.id/id/publication
- **Search:** "Statistik Lingkungan Hidup Indonesia"
- **Years:** 2016-2024 (annual publications)
- **Data Available:**
  - ✅ Luas hutan per provinsi
  - ✅ Deforestasi & degradasi hutan
  - ✅ Perubahan tutupan lahan
  
- **Access Method:**
  - Bulk download PDF/Excel publications
  - PDF table extraction dengan Camelot/Tabula
  
- **Tools/Scripts:**
  ```
  scripts/download_bps_lingkungan_hidup.py
  tools/pdf_extraction/extract_forest_tables_bps.py
  ```

---

### **TIER 2: Geospatial & Satellite Data (FREE, PEER-REVIEWED)**

#### 2A. Global Forest Watch (GFW) ⭐⭐⭐⭐⭐ **HIGHLY RECOMMENDED**

##### **Overview:**
- **Website:** https://www.globalforestwatch.org
- **API:** https://data.globalforestwatch.org
- **Data Source:** Hansen et al. (2013) High-Resolution Global Maps of 21st-Century Forest Cover Change (Science)
- **Credibility:** ⭐⭐⭐⭐⭐ (Used by World Bank, FAO, UNEP, CIFOR)

##### **Data Available:**
- ✅ Tree cover loss (annual, 2001-2023)
- ✅ 30m spatial resolution
- ✅ Province/regency level aggregation
- ✅ Deforestation alerts (GLAD, RADD)
- ✅ Forest cover change statistics
- ✅ API: FREE & well-documented

##### **API Endpoints:**
```
GET /v1/forest-change/glad-alerts
GET /v1/forest-change/hansen
GET /v1/forest-change/umd-loss-gain

Parameters:
- country: IDN (Indonesia)
- admin: Province/Regency code
- period: 2016-01-01,2024-12-31
- format: json/csv
```

##### **Python SDK Available:**
```bash
pip install gfwpy
```

##### **Tools/Scripts:**
```
tools/gfw/fetch_sulawesi_deforestation.py
tools/gfw/gfw_api_client.py
scripts/process_gfw_data.py
```

##### **Expected Output:**
```
data/raw/gfw/sulawesi_tree_cover_loss_2016_2024.csv
data/raw/gfw/sulawesi_forest_change_annual.json
```

##### **Strengths:**
- ✅ Global standard untuk forest monitoring
- ✅ Peer-reviewed & academically cited
- ✅ Konsisten metodologi across years
- ✅ Granular sampai kabupaten level
- ✅ Free API dengan good documentation
- ✅ Python-friendly (SDK available)

##### **Use Case in Research:**
```
Primary data source untuk cross-validation dengan data pemerintah.
Jika data KLHK incomplete/unavailable → GFW sebagai main source.
High academic credibility untuk publication.
```

---

#### 2B. NASA FIRMS (Fire Information for Resource Management System) ⭐⭐⭐⭐

##### **Overview:**
- **Website:** https://firms.modaps.eosdis.nasa.gov
- **API:** https://firms.modaps.eosdis.nasa.gov/api/
- **Data Source:** VIIRS & MODIS satellite fire detection
- **Use Case:** Proxy indicator untuk deforestation activities

##### **Data Available:**
- ✅ Fire/hotspot detection (near real-time)
- ✅ Historical archive 2000-present
- ✅ Geographic coordinates + confidence level
- ✅ Free API dengan registration

##### **Correlation with Deforestation:**
```
Fire hotspots → Indicator land clearing activities
→ Mining site preparation
→ Plantation expansion (palm oil, etc.)
→ Illegal logging & burning

Spatial overlay:
Fire hotspots (FIRMS) × Mining locations (Minerbaone) 
→ Deforestation attribution analysis
```

##### **Tools/Scripts:**
```
tools/nasa_firms/fetch_sulawesi_fires.py
tools/nasa_firms/overlay_fires_mining.py
scripts/correlate_fires_deforestation.py
```

##### **Expected Output:**
```
data/raw/nasa_firms/sulawesi_fire_hotspots_2016_2024.csv
data/processed/fires_mining_overlay.csv
```

---

#### 2C. Copernicus/ESA Land Cover ⭐⭐⭐⭐

##### **Overview:**
- **Portal:** https://land.copernicus.eu/global/products/lc
- **Data:** Land Cover 100m (annual updates)
- **Alternative:** Google Earth Engine datasets

##### **Data Available:**
- ✅ Land cover classification (forest, cropland, urban, etc.)
- ✅ Annual change detection
- ✅ 100m spatial resolution
- ✅ Global coverage including Indonesia

##### **Access Method:**
- Direct download via Copernicus portal
- Google Earth Engine (requires coding)

##### **Tools/Scripts:**
```
tools/copernicus/download_land_cover_sulawesi.py
# OR use Google Earth Engine Python API
```

---

### **TIER 3: Research & NGO Datasets (HIGH CREDIBILITY)**

#### 3A. CIFOR (Center for International Forestry Research) ⭐⭐⭐⭐⭐

##### **Overview:**
- **Website:** https://www.cifor.org/knowledge/data/
- **Focus:** Indonesia forest & land use research
- **Credibility:** ⭐⭐⭐⭐⭐ (Leading forestry research institution)

##### **Data Available:**
- ✅ Forest cover change datasets (various years)
- ✅ Deforestation drivers analysis
- ✅ Province-level research publications
- ✅ Peer-reviewed data supplements

##### **Search Keywords:**
```
"CIFOR Sulawesi deforestation"
"CIFOR Indonesia forest cover change"
"CIFOR land use change Sulawesi"
site:cifor.org forest loss Sulawesi
```

##### **Access Method:**
- Search CIFOR data portal
- Download publication supplements
- Email collaboration request: dataservices@cifor.org

##### **Expected Datasets:**
```
Published research papers dengan data supplement (CSV/Shapefile)
Potentially: Province-level forest loss estimates 2016-2024
```

---

#### 3B. Auriga Nusantara ⭐⭐⭐⭐⭐ **LOCAL EXPERT**

##### **Overview:**
- **Website:** https://www.auriga.or.id
- **Focus:** Forest monitoring, advocacy, indigenous rights
- **Credibility:** ⭐⭐⭐⭐⭐ (Leading Indonesian forest NGO)

##### **Data Available:**
- ✅ Annual deforestation maps Indonesia
- ✅ Investigative reports with data supplements
- ✅ Province-specific analysis (including Sulawesi)
- ✅ Mining & forest destruction correlation studies

##### **Collaboration Request:**
```
Email to: auriga@auriga.or.id
Subject: Research Collaboration - Sulawesi Deforestation Data Request (2016-2024)

Content:
- Introduce CELIOS & D3TLH research
- Request access to Sulawesi deforestation dataset
- Offer data sharing & co-authorship opportunities
```

##### **Expected Response:**
- Published reports download links
- Internal dataset (CSV) jika research collaboration approved
- References to other Sulawesi-specific studies

---

#### 3C. WALHI & Local NGOs ⭐⭐⭐⭐

##### **Organizations:**
- WALHI Sulawesi Selatan/Tengah/Tenggara/Utara
- JATAM (Jaringan Advokasi Tambang)
- KIARA (Coastal & marine ecosystems)
- Local university research centers

##### **Data Available:**
- ✅ Field monitoring reports
- ✅ Mining impact studies (deforestation estimates)
- ✅ Legal case documents dengan environmental evidence
- ✅ Community impact assessments

##### **Already Have:**
```
data/raw/klhk_ngo_reports/
- ARKL_Morowali.pdf
- Riset-Final-WALHI-SULTRA.pdf
- Arinto-Sangadji-HPAL-dalam-Industri-Nikel-Nov-2024_compressed.pdf
```

##### **Action Required:**
- Re-extract deforestation mentions dari existing PDFs
- Search for additional WALHI reports 2016-2024
- Contact WALHI regional offices untuk internal data

##### **Tools/Scripts:**
```
tools/parsing/extract_deforestasi_ngo_reports.py
scripts/consolidate_ngo_deforestation_estimates.py
```

---

### **TIER 4: Google Dorking Campaign ⭐⭐⭐⭐**

##### **Strategy:** Replicate IKU Dorking Success (320+ URLs found)

##### **Target Queries:**
```python
QUERIES = [
    # Government sources
    'site:menlhk.go.id "laju deforestasi" Sulawesi filetype:pdf',
    'site:menlhk.go.id "tutupan hutan" Sulawesi 2016..2024',
    'site:bps.go.id "luas hutan" Sulawesi filetype:xlsx',
    'site:data.go.id deforestasi Sulawesi',
    '"SIMONTANA" deforestasi Sulawesi',
    
    # Research & academic
    'site:cifor.org "forest cover change" Sulawesi',
    'site:.edu "deforestation" Sulawesi Indonesia filetype:pdf',
    '"forest loss" Sulawesi 2016..2024 site:.org',
    
    # NGO & advocacy
    'site:auriga.or.id deforestasi Sulawesi',
    'site:walhi.or.id "kehilangan hutan" Sulawesi',
    'site:jatam.or.id tambang deforestasi Sulawesi',
    
    # Reports & publications
    'intitle:"deforestasi" Sulawesi 2016..2024',
    'intitle:"tutupan hutan" Sulawesi filetype:pdf',
    '"forest cover" Sulawesi "2016" OR "2024" filetype:pdf',
    '"land use change" Sulawesi mining',
    
    # Specific provinces
    '"Sulawesi Selatan" deforestasi 2016..2024',
    '"Sulawesi Tengah" kehilangan hutan',
    'Morowali deforestasi tambang',
    
    # Combined indicators
    'Sulawesi (deforestasi OR "forest loss") (tambang OR smelter)',
    '"tutupan hutan" AND "pertambangan" AND Sulawesi',
]
```

##### **Expected Results:**
- 150-250 potential documents
- Mix of: Government reports, academic papers, NGO studies, news investigations

##### **Tools/Scripts:**
```
scripts/dork_deforestasi_sulawesi.py
tools/google_dork/google_dorker.py (reuse from IKU campaign)
scripts/batch_download_dork_results.py
tools/parsing/parse_deforestation_documents.py
```

##### **Expected Output:**
```
data/raw/dork_deforestasi/
  ├── search_results.csv (metadata all URLs)
  ├── pdfs/ (downloaded documents)
  └── extracted/ (parsed data)

docs/cse_dorking_results/
  └── DEFORESTASI_DORK_RESULTS.md (analysis)
```

---

## 📋 RECOMMENDED EXECUTION PLAN

### **PHASE 1: Quick Wins (1-2 Days) ⚡**

#### **Priority 1: Global Forest Watch API** - FASTEST
```bash
# Day 1 - Morning
1. Setup GFW API credentials (free registration)
2. python tools/gfw/fetch_sulawesi_deforestation.py
3. Output: data/raw/gfw/sulawesi_tree_cover_loss_2016_2024.csv

Expected Result:
✅ Complete dataset 2016-2023 (2024 might be partial)
✅ Per province breakdown
✅ High credibility (Hansen et al. Science 2013)
✅ Ready for immediate use
```

#### **Priority 2: Re-extract SLHI PDFs** - ALREADY HAVE FILES
```bash
# Day 1 - Afternoon
1. python tools/pdf_extraction/extract_deforestasi_slhi.py
2. Target: SLHI 2015-2025 PDFs (11 files already downloaded)
3. Output: data/raw/klhk_slhi/deforestasi_extracted.csv

Expected Result:
✅ Government official data (KLHK)
✅ 2015-2024 coverage (10 years)
✅ Cross-validation dengan GFW
```

#### **Priority 3: BPS API Search** - EXPLORATORY
```bash
# Day 2
1. python tools/bpsapi/search_deforestasi.py
2. Search all Var IDs related to "hutan", "lahan", "tutupan"
3. If found → extract data via BPS API

Expected Result:
✅ Official BPS statistics (if available)
⚠️ Might not exist (BPS forest data often limited)
```

---

### **PHASE 2: Comprehensive Collection (3-5 Days)**

#### **Step 1: KLHK Portal Scraping**
```bash
# Day 3-4
python tools/klhk/scrape_simontana.py
python tools/klhk/scrape_statistik_klhk.py

Target:
- SIMONTANA annual reports
- KLHK statistics portal
- Any available GIS/shapefile data
```

#### **Step 2: Google Dorking Campaign**
```bash
# Day 4-5
python scripts/dork_deforestasi_sulawesi.py

Expected:
- 150-250 document URLs
- Batch download overnight
- PDF parsing Day 6
```

#### **Step 3: NGO Dataset Request**
```bash
# Day 5 (async - email sent, wait for response)
Email to:
1. auriga@auriga.or.id (Auriga Nusantara)
2. contact@cifor.org (CIFOR Indonesia)
3. walhi.sulteng@gmail.com (WALHI regional)

Subject: "Research Collaboration - Sulawesi Deforestation Data Request"
Follow-up after 3-5 days if no response
```

---

### **PHASE 3: Consolidation & Quality Check (2-3 Days)**

#### **Data Consolidation Script:**
```bash
python scripts/consolidate_deforestasi.py

Process:
1. Load all source datasets
2. Standardize province names
3. Harmonize units (all to hectares)
4. Handle missing years via interpolation
5. Calculate confidence scores
6. Output final consolidated CSV
```

#### **Input Sources (Priority Order):**
1. **GFW API data** (primary - highest credibility)
2. **SLHI extracted data** (government official)
3. **BPS data** (if available)
4. **KLHK SIMONTANA** (government detailed)
5. **NGO reports** (ground truth validation)
6. **Dorking results** (supplementary)

#### **Output Schema:**
```csv
province,year,deforestation_rate_ha,forest_cover_pct,forest_loss_ha,total_area_ha,data_source,confidence_level,notes
Sulawesi Utara,2016,12500.5,65.3,12500.5,1587000,GFW_Hansen,High,"Hansen et al. 2013 methodology"
Sulawesi Utara,2017,13200.8,64.8,13200.8,1587000,GFW_Hansen,High,"Hansen et al. 2013 methodology"
...
Sulawesi Selatan,2024,18900.2,52.1,18900.2,4680000,SLHI_2025,Medium,"KLHK official report"
```

#### **Quality Validation:**
```bash
python scripts/validate_deforestasi_data.py

Checks:
- No missing years 2016-2024
- All 6 provinces covered
- Cross-validation between sources (< 20% deviation)
- Flag outliers for manual review
- Generate data quality report
```

---

## 🎯 SUCCESS METRICS

### **Minimum Success Criteria:**
- ✅ Data coverage: 2016-2024 (9 years)
- ✅ Geographic coverage: All 6 Sulawesi provinces
- ✅ At least 2 independent data sources for cross-validation
- ✅ Data credibility: Peer-reviewed OR government official

### **Ideal Success Criteria:**
- ✅ Annual data points for all provinces (54 data points minimum)
- ✅ Kabupaten-level breakdown (if available)
- ✅ 3+ independent sources untuk triangulasi
- ✅ GFW as primary source (global standard)
- ✅ Government data (KLHK/BPS) for official validation

### **Output Deliverables:**
```
1. data/processed/sulawesi_deforestasi_2016_2024.csv
2. docs/DEFORESTASI_DATA_COLLECTION_REPORT.md
3. data/raw/gfw/ (GFW API outputs)
4. data/raw/klhk_slhi/ (SLHI extractions)
5. data/raw/dork_deforestasi/ (Dorking results)
```

---

## 🚀 NEXT IMMEDIATE ACTIONS

### **Action 1: Setup GFW API** (30 mins)
```bash
# Register for GFW API key
# https://data.globalforestwatch.org/documents/gfw-api-key

# Install dependencies
pip install gfwpy requests pandas

# Test API connection
python tools/gfw/test_gfw_connection.py
```

### **Action 2: Create Scripts Structure** (1 hour)
```bash
mkdir -p tools/gfw
mkdir -p tools/klhk
mkdir -p data/raw/gfw
mkdir -p data/raw/klhk_deforestasi
mkdir -p data/raw/dork_deforestasi

touch tools/gfw/fetch_sulawesi_deforestation.py
touch tools/gfw/gfw_api_client.py
touch tools/pdf_extraction/extract_deforestasi_slhi.py
touch scripts/consolidate_deforestasi.py
```

### **Action 3: Execute Phase 1** (2 days)
```bash
# Run Priority 1, 2, 3 sequentially
# Expected: 80% data collected in 2 days
```

---

## 📚 REFERENCES & RESOURCES

### **Key Papers:**
1. Hansen, M. C., et al. (2013). High-resolution global maps of 21st-century forest cover change. *Science*, 342(6160), 850-853.
   - https://doi.org/10.1126/science.1244693
   
2. Curtis, P. G., et al. (2018). Classifying drivers of global forest loss. *Science*, 361(6407), 1108-1111.
   - https://doi.org/10.1126/science.aau3445

### **API Documentation:**
- Global Forest Watch API: https://data.globalforestwatch.org/documents
- NASA FIRMS API: https://firms.modaps.eosdis.nasa.gov/api/
- BPS API: https://webapi.bps.go.id/developer/

### **Indonesian Forest Monitoring:**
- KLHK SIMONTANA: http://simontana.menlhk.go.id
- Auriga Forest Maps: https://www.auriga.or.id/peta
- CIFOR Indonesia: https://www.cifor.org/knowledge/data/

---

**Document Version:** 1.0  
**Last Updated:** 14 Juni 2026  
**Next Review:** After Phase 1 completion  
**Contact:** CELIOS Research Division
