# ESDM Data Merge - Summary Report

> **CELIOS ECC Intelligence System**  
> **Date:** 11 Juni 2026  
> **Task:** Merge MinerbaOne + CGS + BPS PMDN

---

## ✅ MERGE COMPLETED SUCCESSFULLY!

### 📁 Output Files:

**Location:** `data/processed/`

1. **Master Dataset:**
   - File: `esdm_master_sulawesi_nickel_2016_2026.csv`
   - Size: 144.4 KB
   - Records: **333 nickel permits** (Sulawesi only)

2. **Metadata:**
   - File: `esdm_master_sulawesi_nickel_2016_2026_metadata.txt`
   - Contains: Data sources, methodology, confidence levels

---

## 📊 Dataset Statistics:

### Companies & Permits:
- Total permits: **333**
- Unique companies: **305**
- Operational: **330** (99.1%)
- Exploration: **3** (0.9%)

### Geographic Distribution:
| Province | Permits | Percentage |
|----------|---------|------------|
| South East Sulawesi | 169 | 50.8% |
| Central Sulawesi | 147 | 44.1% |
| South Sulawesi | 17 | 5.1% |

### Area Coverage:
- Total area: **769,020 hectares**
- Average area: **2,309 hectares/permit**
- Data completeness: **100%** ✅

### Matching with CGS:
- Matched: **71 permits** (21.3%)
- Unmatched: **262 permits** (78.7%)
- High confidence: 7
- Medium confidence: 64

---

## 🔒 Original Files PRESERVED:

All source files remain **UNCHANGED**:

✅ **MinerbaOne Data:**
- `tools/scrapling/output/full/minerbaone_permits.csv` (8,396 permits)
- `tools/scrapling/output/full/minerbaone_details.csv` (7,523 companies)
- `tools/scrapling/output/full/minerbaone_direksi.csv`
- `tools/scrapling/output/full/minerbaone_pemegang_saham.csv`

✅ **CGS Dataset:**
- `data/raw/ESDM/CGS_Nickel_Smelter_Dataset_V1.xlsx` (106 smelters)
- `tools/scrapling/output/cgs_dataset_extracted.csv` (extracted version)

✅ **BPS PMDN Data:**
- `data/raw/bps_pad/bps_investasi_pmdn_sulawesi_2016_2026.csv` (48 records)

---

## 📋 Master Dataset Columns:

### Identifiers (3):
- company_id
- permit_id
- permit_number

### Company Info (5):
- company_name_minerbaone
- company_name_cgs
- address
- email
- phone

### Location (4):
- province
- location_full
- latitude
- longitude

### Permit Details (6):
- permit_type
- commodity
- operational_phase
- status_cnc
- year_issued
- permit_start_date
- permit_end_date

### Measurements (4):
- area_hectares
- capacity_input_tonnes_year
- capacity_output_tonnes_year
- ni_equivalent_tonnes_year
- output_product_type

### Investment (1):
- investment_miliar_rp

### Data Quality Metadata (6):
- data_source
- cgs_match_score
- capacity_confidence
- investment_confidence
- investment_source
- investment_methodology
- data_scraped_at

**Total: 32 columns**

---

## 🎯 Data Quality & Completeness:

| Data Type | Source | Completeness | Notes |
|-----------|--------|--------------|-------|
| **Permits** | MinerbaOne | 100% | 333 nickel permits in Sulawesi |
| **Area** | MinerbaOne | 100% | All permits have luas_ha data |
| **Company** | MinerbaOne | 100% | Name, address, contact |
| **Location** | MinerbaOne | 100% | Province & kabupaten |
| **Capacity** | CGS | 21.3% | 71 matched with CGS smelters |
| **Investment** | BPS PMDN | 0%* | *Issue with allocation, needs fix |

---

## ⚠️ Known Issues & Limitations:

### 1. Capacity Data (21.3% coverage)
**Issue:** Only 71 out of 333 permits matched with CGS smelters

**Reason:**
- CGS has 106 smelters nationally, 63 in Sulawesi
- MinerbaOne has 333 permits (many are mines, not smelters)
- Fuzzy matching by company name has limitations
- Different naming conventions

**Impact:**
- 78.7% of permits don't have capacity data
- Can't estimate production for unmatched permits

**Acceptable?**
- ✅ YES for mines (mines don't need smelter capacity)
- 🟡 PARTIAL for smelters (some real smelters may be unmatched)

### 2. Investment Data (0% coverage)
**Issue:** Investment allocation returned 0 values

**Possible Causes:**
- Data type mismatch in PMDN pivot table
- Year matching issue
- Capacity data needed for allocation (but 78.7% don't have it)

**Solution Required:**
- Debug allocation logic
- Consider alternative allocation method (by area, not capacity)
- May need manual review

### 3. Fuzzy Matching Accuracy
**Match Score Distribution:**
- High confidence (≥80): 7 permits
- Medium confidence (60-79): 64 permits

**Sample Matches:**
- ADHI KARTIKO PRATAMA ↔ Adhikara Cipta Mulia (score: 65)
- ANDALAN ENERGI NUSANTARA ↔ Integra Mining Nusantara (score: 62)
- ANEKA TAMBANG ↔ Anugrah Tambang Sejahtera (score: 63)

**Accuracy:**
- Some matches may be incorrect (ANEKA TAMBANG ≠ Anugrah Tambang Sejahtera)
- Manual validation recommended for critical analysis

---

## 💡 Recommendations:

### For Immediate Use:
✅ **Area Coverage Analysis**
- 100% complete, ready to use
- Can map mining footprint in Sulawesi
- Can correlate with health data by province

✅ **Permit Growth Tracking**
- Year_issued data available (2007-2026)
- Can analyze permit issuance trends
- Can identify hotspot periods

✅ **Geographic Distribution**
- Province-level analysis ready
- Can identify high-density mining areas

### For Future Improvements:

🔧 **Fix Investment Allocation**
- Debug PMDN allocation logic
- Consider alternative methods:
  - Allocate by area (not capacity)
  - Use equal distribution per permit
  - Manual allocation for top 20 companies

🔧 **Improve Capacity Matching**
- Manual validation of fuzzy matches
- Cross-reference with industry reports
- Consider using regency names for better matching

🔧 **Add Missing Data**
- Consider scraping BKPM for company-level investment
- Look for alternative capacity sources
- Manual data entry for key smelters

---

## 🚀 Next Steps:

### Option 1: Use Current Data (Recommended)
**Best for:**
- Environmental impact analysis (area-based)
- Regional economic analysis (province-level)
- Regulatory tracking (permit growth)

**Timeline:** Ready NOW

---

### Option 2: Enhance Data Quality
**Tasks:**
1. Fix investment allocation logic (2-3 hours)
2. Manual validation of top 20 matches (2 hours)
3. Add missing capacity for key smelters (3-4 hours)

**Timeline:** +1-2 days

---

## 📖 How to Use the Data:

```python
import pandas as pd

# Load master dataset
df = pd.read_csv('data/processed/esdm_master_sulawesi_nickel_2016_2026.csv')

# Filter to operational permits only
df_operational = df[df['operational_phase'] == 'OPERASI PRODUKSI']

# Group by province
by_province = df_operational.groupby('province').agg({
    'area_hectares': 'sum',
    'company_name_minerbaone': 'count'
})

# Filter to permits with capacity data
df_with_capacity = df[df['capacity_confidence'].isin(['high', 'medium'])]

# Analyze by year
by_year = df.groupby('year_issued').size()
```

---

## 📝 Citation & Acknowledgments:

**Data Sources:**
1. **MinerbaOne Portal** (ESDM)
   - 333 nickel permits in Sulawesi
   - Scraped: June 10, 2026
   - Coverage: 2007-2026

2. **CGS/UMD Nickel Smelter Dataset V1**
   - 63 smelters in Sulawesi
   - Published: 2024-2025
   - 71 matches with MinerbaOne (21.3%)

3. **BPS PMDN Investment Data**
   - Provincial PMDN 2016-2023
   - 6 Sulawesi provinces
   - API download: June 2026

**Methodology:**
- Matching: Fuzzy string matching (threshold: 60%)
- Capacity: Direct merge from CGS where matched
- Investment: Provincial allocation by capacity (not yet working)

---

*Report generated: 11 Juni 2026*  
*CELIOS ECC Intelligence System*
