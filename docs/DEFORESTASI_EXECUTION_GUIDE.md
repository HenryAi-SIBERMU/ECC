# Panduan Eksekusi: Akuisisi Data Deforestasi Sulawesi
## Step-by-Step Execution Guide

**Target:** Data laju deforestasi Sulawesi 2016-2024  
**Sources:** GFW API (primary) + SLHI PDFs (validation)  
**Timeline:** 1-2 hari untuk data collection + consolidation  
**Dibuat:** 14 Juni 2026

---

## 📋 PRE-REQUISITES

### 1. Check Python Environment

```bash
python --version  # Should be 3.8+
```

### 2. Install Dependencies

```bash
# Core dependencies (already installed in project)
pip install requests pandas numpy

# PDF extraction dependencies
pip install camelot-py[cv] tabula-py
# OR if camelot fails:
pip install "camelot-py[base]"
```

### 3. Verify SLHI Files

```bash
# Check if SLHI PDFs ada
ls data/raw/klhk_sulut_kualitas_air/SLHI_*.pdf

# Expected: SLHI_2015.pdf sampai SLHI_2025.pdf (11 files)
```

---

## 🚀 PHASE 1: GFW API Data Fetch (PRIMARY SOURCE)

### Step 1.1: Test GFW API Connection

```bash
cd tools/gfw
python gfw_api_client.py
```

**Expected Output:**
```
Testing GFW API Client...
Fetching sample data for Sulawesi Selatan...
Response keys: ['data', 'attributes', ...]
```

**If fails:**
- Check internet connection
- Check GFW API status: https://www.globalforestwatch.org
- Try different endpoint in `gfw_api_client.py`

### Step 1.2: Fetch Full Sulawesi Data

```bash
python fetch_sulawesi_deforestation.py
```

**Expected Duration:** 5-10 minutes  
**Output File:** `data/raw/gfw/sulawesi_deforestation_2016_2024.csv`

**Expected Console Output:**
```
============================================================
FETCHING SULAWESI DEFORESTATION DATA FROM GFW
============================================================
Output directory: data/raw/gfw
Processing Sulawesi Utara...
Processing Sulawesi Tengah...
...
Total rows fetched: 54
Provinces covered: 6
Years covered: [2016, 2017, ..., 2024]
```

### Step 1.3: Inspect Output

```bash
# Check file size
ls -lh data/raw/gfw/sulawesi_deforestation_2016_2024.csv

# Preview first 10 rows
head -10 data/raw/gfw/sulawesi_deforestation_2016_2024.csv
```

**Quality Check:**
- ✅ File size > 1 KB (data ada)
- ✅ Total rows = 54 (6 provinces × 9 years)
- ✅ Semua provinsi covered
- ✅ No obvious missing values

**If data quality low:**
1. Check `gfw_api_client.py` response parsing logic
2. Print raw API response untuk inspect structure:
   ```python
   print(json.dumps(data, indent=2))
   ```
3. Adjust column extraction logic di `fetch_sulawesi_deforestation.py`

---

## 🚀 PHASE 2: SLHI PDF Extraction (GOVERNMENT VALIDATION)

### Step 2.1: Verify PDF Files

```bash
# List all SLHI PDFs
ls -lh data/raw/klhk_sulut_kualitas_air/SLHI_*.pdf

# Expected: 11 files (2015-2025)
# Size: 5-50 MB per file
```

### Step 2.2: Run PDF Extraction

```bash
cd ../../  # Back to project root
python tools/pdf_extraction/extract_deforestasi_slhi.py
```

**Expected Duration:** 10-30 minutes (depends on PDF size & table complexity)

**Expected Console Output:**
```
======================================================================
EXTRACTING DEFORESTATION DATA FROM SLHI PDFS
======================================================================
Found 11 SLHI PDF files
  - SLHI_2015.pdf
  - SLHI_2016.pdf
  ...

Processing SLHI_2015.pdf (Year: 2015)...
  Extracted 8 tables
  Table 3 appears relevant, extracting...
    Extracted: Sulawesi Utara - 2015
    Extracted: Sulawesi Tengah - 2015
    ...
  Found 2 relevant tables

Total extracted data points: 66
Provinces covered: 6
Years covered: [2015, 2016, ..., 2025]
```

**Output File:** `data/raw/klhk_slhi/deforestasi_sulawesi_slhi_extracted.csv`

### Step 2.3: Manual Validation (CRITICAL!)

```bash
# Open CSV dan check extraction quality
# Focus on 'raw_row' column untuk verify accuracy
```

**Manual Check:**
1. Buka file CSV di Excel/LibreOffice
2. Check column `raw_row` untuk setiap baris
3. Verify bahwa numeric values extracted correctly
4. **If extraction quality < 70%:**
   - Manual PDF inspection required
   - Adjust table detection logic
   - Consider alternative: Manual copy-paste dari PDF ke CSV

**Common Issues:**
- ❌ Table structure berbeda per tahun
- ❌ Province names typo/variants
- ❌ Numbers dengan delimiter inconsistent
- ❌ Multi-page tables terpotong

**Fix Strategy:**
- Update `TABLE_KEYWORDS` di `extract_deforestasi_slhi.py`
- Adjust `extract_sulawesi_data()` parsing logic
- Add province name variants/aliases

---

## 🚀 PHASE 3: Data Consolidation (MERGE & VALIDATE)

### Step 3.1: Run Consolidation Script

```bash
python scripts/consolidate_deforestasi.py
```

**Expected Duration:** 2-5 minutes

**Expected Console Output:**
```
======================================================================
CONSOLIDATING DEFORESTATION DATA
======================================================================
Loaded GFW data: 54 rows
Loaded SLHI data: 66 rows
Using GFW as primary data source
Merging SLHI data for cross-validation
Missing data points: 0 / 54

======================================================================
DATA QUALITY REPORT
======================================================================
total_rows: 54
provinces_covered: 6
years_covered: [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
completeness_pct: 100.0
gfw_slhi_correlation: 0.85
avg_discrepancy_pct: 12.5
```

**Output File:** `data/processed/sulawesi_deforestasi_2016_2024.csv`

### Step 3.2: Quality Validation

**Acceptance Criteria:**
- ✅ Completeness: 100% (no missing years per province)
- ✅ GFW-SLHI Correlation: > 0.7 (good agreement)
- ✅ Average Discrepancy: < 20% (reasonable variance)
- ✅ No extreme outliers (>3 std dev)

**If validation fails:**
1. **Low correlation (<0.5):**
   - Data sources measuring different things
   - One source has systematic error
   - Need manual review & source selection
   
2. **High discrepancy (>30%):**
   - Check unit conversion (SLHI might use different units)
   - Verify both sources reference same geography
   - Consider using only GFW jika SLHI questionable
   
3. **Missing data:**
   - Interpolate untuk minor gaps (<2 consecutive years)
   - Flag provinces dengan major gaps
   - Document limitations di research report

### Step 3.3: Final Output Inspection

```bash
# Preview final data
head -20 data/processed/sulawesi_deforestasi_2016_2024.csv

# Check statistics
python -c "
import pandas as pd
df = pd.read_csv('data/processed/sulawesi_deforestasi_2016_2024.csv')
print(df.describe())
print('\nPer-province summary:')
print(df.groupby('province')['deforestation_rate_ha'].agg(['mean', 'min', 'max']))
"
```

---

## 📊 EXPECTED FINAL OUTPUT SCHEMA

```csv
province,year,deforestation_rate_ha,forest_cover_pct,data_source,confidence_level,deforestation_rate_ha_slhi,forest_cover_pct_slhi,deforestation_discrepancy_pct,is_interpolated,deforestation_yoy_change_pct,cumulative_deforestation_ha
Sulawesi Utara,2016,12500.5,65.3,GFW_Hansen,High,13200.0,64.8,5.6,False,-,12500.5
Sulawesi Utara,2017,13200.8,64.8,GFW_Hansen,High,13500.0,64.2,2.3,False,5.6,25701.3
...
```

**Column Definitions:**
- `deforestation_rate_ha`: Annual deforestation in hectares (GFW primary)
- `forest_cover_pct`: % forest cover remaining
- `data_source`: GFW_Hansen (primary) or SLHI_YYYY (government)
- `confidence_level`: High/Medium/Low
- `deforestation_rate_ha_slhi`: SLHI value untuk cross-validation
- `deforestation_discrepancy_pct`: % difference GFW vs SLHI
- `is_interpolated`: Boolean flag untuk interpolated values
- `deforestation_yoy_change_pct`: Year-over-year % change
- `cumulative_deforestation_ha`: Cumulative loss since 2016

---

## 🎯 SUCCESS METRICS

### Minimum Success (PHASE 1 Complete):
- ✅ GFW data: 54 rows (6 provinces × 9 years)
- ✅ Data quality: >80% complete
- ✅ Ready for analysis tanpa SLHI cross-validation

### Ideal Success (PHASE 1+2+3 Complete):
- ✅ GFW + SLHI data: Both sources available
- ✅ Cross-validation: Correlation >0.7
- ✅ Consolidated data: 100% complete dengan quality flags
- ✅ Ready untuk Checkpoint 4 analysis

---

## 🐛 TROUBLESHOOTING GUIDE

### Issue 1: GFW API Returns Empty Response

**Symptoms:** `data` key empty atau status "error"

**Solutions:**
1. Check API endpoint status:
   ```bash
   curl https://production-api.globalforestwatch.org/v1/umd-loss-gain?iso=IDN&admin1=30
   ```
2. Try alternative GFW API versions:
   - v1: `https://production-api.globalforestwatch.org`
   - v2: `https://data-api.globalforestwatch.org`
3. Check admin codes - might need adjustment
4. Review GFW API changelog untuk breaking changes

### Issue 2: SLHI PDF Extraction Fails

**Symptoms:** `camelot.read_pdf()` error or zero tables extracted

**Solutions:**
1. Install system dependencies:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install ghostscript python3-tk
   
   # macOS
   brew install ghostscript tcl-tk
   
   # Windows
   # Download Ghostscript installer dari https://ghostscript.com/
   ```
2. Try alternative: `tabula-py`
   ```python
   import tabula
   tables = tabula.read_pdf("file.pdf", pages="all")
   ```
3. Fallback: Manual extraction (copy-paste dari PDF)

### Issue 3: Consolidation Merge Mismatch

**Symptoms:** Low row count after merge, many NaN values

**Solutions:**
1. Check province name consistency:
   ```python
   print(df_gfw['province'].unique())
   print(df_slhi['province'].unique())
   ```
2. Standardize province names:
   ```python
   province_mapping = {
       'SULAWESI UTARA': 'Sulawesi Utara',
       'Sulut': 'Sulawesi Utara',
       # Add variants...
   }
   df['province'] = df['province'].replace(province_mapping)
   ```
3. Check year formats (int vs string)

### Issue 4: Data Quality Low (<70%)

**Symptoms:** Many missing values, low correlation, high discrepancy

**Solutions:**
1. **Use GFW only:** Drop SLHI cross-validation
   - GFW sudah sufficient sebagai peer-reviewed source
   - Document limitation di research report
   
2. **Manual SLHI review:**
   - Inspect PDF manually
   - Copy-paste key tables ke CSV
   - Use as selective validation (not full dataset)
   
3. **Supplement dengan source lain:**
   - NASA FIRMS fire data (proxy)
   - Auriga NGO reports
   - Academic papers dengan Sulawesi data

---

## 📚 NEXT STEPS AFTER DATA COLLECTION

### 1. Update PRD Log (CRITICAL!)

```bash
# Update docs/prd-fase1-d3tlh.md
# Add log entry untuk Deforestation data collection
```

**Log Template:**
```markdown
* **[14 Juni 2026] Deforestasi Data Collection - GFW + SLHI (Prioritas #4):**
  - 🎯 **TARGET:** Laju deforestasi Sulawesi 2016-2024
  - ✅ **GFW API:** [X] rows fetched, [completeness]%
  - ✅ **SLHI PDFs:** [Y] rows extracted dari 11 PDFs
  - ✅ **CONSOLIDATED:** data/processed/sulawesi_deforestasi_2016_2024.csv
  - 📊 **QUALITY:** Correlation=[Z], Discrepancy=[W]%
  - 📄 **DOKUMENTASI:** docs/DEFORESTASI_DATA_STRATEGY.md
```

### 2. Use Data in Dashboard

```bash
# Update pages/2_Kualitas_Lingkungan.py
# Add deforestation visualization
```

**Checkpoint 4 Analysis:**
- Luas Industri (ESDM) vs Deforestasi crosstab
- Mining expansion vs Forest loss temporal correlation
- Spatial overlay: Smelter locations vs Deforestation hotspots

### 3. Cross-Reference Analysis

**Correlation Studies:**
```python
# Load multiple datasets
df_deforestasi = pd.read_csv('data/processed/sulawesi_deforestasi_2016_2024.csv')
df_mining = pd.read_csv('data/processed/sulawesi_esdm_nikel.csv')
df_ika = pd.read_csv('data/processed/sulawesi_ika_2016_2024.csv')

# Analyze correlations
# Mining expansion → Deforestation
# Deforestation → Water quality (IKA)
# Deforestation → Health burden
```

### 4. Research Report Integration

**Key Findings to Document:**
- Annual deforestation rate per province
- Cumulative forest loss 2016-2024
- Correlation dengan mining/smelter expansion
- Environmental carrying capacity (D3TLH) vs actual forest loss
- Policy failure evidence: Permits issued despite high deforestation

---

## ✅ COMPLETION CHECKLIST

- [ ] **Phase 1: GFW API**
  - [ ] Dependencies installed
  - [ ] API connection tested
  - [ ] Data fetched (54 rows minimum)
  - [ ] Output file saved

- [ ] **Phase 2: SLHI Extraction**
  - [ ] PDF files verified (11 files)
  - [ ] Extraction script executed
  - [ ] Manual validation completed
  - [ ] Output file saved

- [ ] **Phase 3: Consolidation**
  - [ ] Merge script executed
  - [ ] Quality validation passed
  - [ ] Final output saved
  - [ ] Data ready for analysis

- [ ] **Documentation**
  - [ ] PRD log updated
  - [ ] Data quality report documented
  - [ ] Limitations noted
  - [ ] Next steps planned

---

**Document Version:** 1.0  
**Last Updated:** 14 Juni 2026  
**Status:** ✅ Ready for Execution  
**Estimated Total Time:** 1-2 days (including validation)
