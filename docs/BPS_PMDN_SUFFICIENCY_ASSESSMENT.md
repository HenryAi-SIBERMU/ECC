# Assessment: Apakah BPS PMDN Data CUKUP untuk Nilai Investasi?

> **CELIOS ECC Intelligence System**  
> **Created:** 11 Juni 2026  
> **Question:** Apakah data BPS PMDN yang sudah ada CUKUP, atau perlu scrape tambahan?

---

## 📊 Data BPS PMDN yang Sudah Ada

**File:** `data/raw/bps_pad/bps_investasi_pmdn_sulawesi_2016_2026.csv`

### Struktur Data:
```csv
provinsi,tahun,indikator,nilai,satuan
Sulawesi Tengah,2018,Investasi PMDN - Nilai (Juta Rp),8488.9,Juta Rp
```

### Coverage:
- ✅ **6 provinsi Sulawesi** (Utara, Tengah, Selatan, Tenggara, Barat, Gorontalo)
- ✅ **Periode: 2016-2023** (8 tahun)
- ✅ **2 indikator:**
  - Nilai investasi (Juta Rupiah)
  - Jumlah proyek
- ✅ **48 data points** (6 provinsi × 8 tahun)

---

## 🔍 Analisis: CUKUP atau TIDAK CUKUP?

### ✅ Kelebihan Data PMDN BPS:

1. **Coverage Provinsi LENGKAP**
   - Semua 6 provinsi Sulawesi tercakup
   - Data per tahun 2016-2023 (sesuai target ESDM)

2. **Format CLEAN & Numeric**
   - Sudah dalam format Juta Rupiah
   - Siap pakai untuk analisis
   - Tidak perlu parsing/cleaning

3. **Time Series Available**
   - Bisa track trend investasi per tahun
   - Bisa hitung growth rate
   - Bisa korelasi dengan jumlah izin dari MinerbaOne

4. **Jumlah Proyek Included**
   - Ada data berapa banyak proyek per provinsi
   - Bisa dipakai untuk validasi alokasi

### ⚠️ Keterbatasan Data PMDN BPS:

1. **Aggregated di Level PROVINSI**
   - ❌ Tidak ada breakdown per **perusahaan**
   - ❌ Tidak ada breakdown per **smelter/tambang**
   - ❌ Tidak ada breakdown per **sektor** (nickel vs. coal vs. lainnya)
   
   **Impact:** Kita harus **ALOKASI MANUAL** dari provinsi ke individual permits

2. **PMDN = Investasi Domestik Only**
   - ❌ Tidak termasuk **PMA (Foreign Investment)**
   - ❌ Banyak smelter nickel adalah joint venture China/Korea
   
   **Impact:** Nilai investasi akan **UNDERESTIMATE** (lebih rendah dari real)

3. **Tidak Spesifik Sektor Mining**
   - ⚠️ PMDN mencakup **SEMUA sektor** (agriculture, manufacturing, services, dll)
   - ❌ Tidak bisa isolasi investasi mining/smelter saja
   
   **Impact:** Alokasi ke mining harus pakai **ASUMSI** (e.g., 30-50% dari total PMDN di provinsi mining-heavy)

4. **Data 2024-2026 MISSING**
   - ❌ Hanya sampai 2023
   - ❌ Target ESDM adalah 2016-**2026**
   
   **Impact:** Missing 3 tahun terakhir (tapi bisa tolerable)

---

## 💡 Contoh Alokasi yang Bisa Dilakukan

### Scenario: Alokasi Investasi Sulteng 2022 ke Smelters

**Data BPS PMDN:**
- Sulawesi Tengah 2022: **3,758.6 Miliar Rupiah** (all sectors)
- Jumlah proyek: 1,576 proyek

**Data CGS (Smelters di Sulteng):**
- Total smelters: **35** (dari 106 nasional)
- Total capacity Sulteng: ~70 juta tonnes input (estimate)

**Data MinerbaOne (Permits di Sulteng):**
- Total permits: ~1,200 (estimate dari 8,396)
- Nickel permits: ~150

**Alokasi Method 1: Proportional by Capacity**
```
Asumsi: 40% dari PMDN Sulteng untuk mining sector
Mining PMDN 2022 = 3,758.6 × 0.4 = 1,503.4 Miliar Rp

Smelter A investment = (Smelter A capacity / Total Sulteng capacity) × 1,503.4 M
```

**Alokasi Method 2: Equal Distribution**
```
Per-smelter investment = 1,503.4 / 35 smelters = 42.9 Miliar Rp per smelter
```

**Alokasi Method 3: Proportional by Luas Lahan**
```
Smelter A investment = (Smelter A area / Total Sulteng area) × 1,503.4 M
```

---

## 🤔 Apakah Perlu Scrape Tambahan?

### Opsi 1: ✅ **TIDAK PERLU SCRAPE** (Use BPS PMDN)

**Rationale:**
- ✓ Data provinsi sudah cukup untuk **estimasi aggregate**
- ✓ Untuk analisis impact (environmental/health), granularity company-level **tidak krusial**
- ✓ Alokasi proportional by capacity **reasonable approximation**
- ✓ Effort scrape tinggi vs. added value rendah

**When to choose:**
- Jika tujuan analisis: **Regional economic impact** (provinsi-level)
- Jika acceptable: **Estimated investment** (not exact)
- Jika timeline: **Limited** (mau cepat selesai)

**Methodology:**
1. Allocate provincial PMDN to smelters proportionally by capacity
2. Document clearly: "Investment adalah alokasi proporsional, bukan actual per-company"
3. Flag as "medium confidence" data

---

### Opsi 2: ⚠️ **SCRAPE TAMBAHAN** (Get Company-Level Data)

**What to scrape:**
- BKPM NSWI portal (https://nswi.bkpm.go.id)
- Target: Company-level investment data
- Format: Per-company, per-year, with sector breakdown

**Challenges:**
1. 🔴 **Portal likely requires login** (not public API)
2. 🔴 **Data may not be downloadable** (view-only)
3. 🔴 **High complexity** (similar to BPS struggle)
4. 🔴 **May need formal request** to BKPM

**Rationale to scrape:**
- ✓ Get **actual** company-level investment (not estimated)
- ✓ Distinguish PMDN vs. PMA (foreign investment)
- ✓ Get sector breakdown (mining only)
- ✓ More accurate for financial analysis

**When to choose:**
- Jika tujuan analisis: **Company financial analysis** (ROI, profitability)
- Jika perlu: **Exact investment figures** (not estimates)
- Jika timeline: **Flexible** (ada 3-5 hari ekstra)

**Estimated Effort:**
- Reconnaissance: 2-3 jam (test portal, check API)
- Scraping development: 4-6 jam (if API exists)
- Manual fallback: **VERY HIGH** (if no API, may need formal request)

---

## 🎯 REKOMENDASI FINAL

### 🟢 **CUKUP - Gunakan BPS PMDN Data Saja**

**Alasan:**

1. **Cost-Benefit Analysis:**
   - Effort scrape BKPM: **HIGH** (portal complex, may need login)
   - Added value: **MEDIUM** (company-level detail nice-to-have, not must-have)
   - BPS PMDN approximation: **GOOD ENOUGH** for impact analysis

2. **Tujuan CELIOS:**
   - Focus: **Environmental & Health Impact**
   - Investment role: **Proxy for economic activity intensity**
   - Provinsi-level granularity: **SUFFICIENT** for correlation

3. **Data Quality Trade-off:**
   - BPS PMDN: **Verified official data** (trusted source)
   - BKPM scrape: **Uncertain accessibility** (may fail)
   - Proportional allocation: **Transparent methodology** (can be documented)

4. **Timeline:**
   - With BPS PMDN: **Ready to merge NOW** (2-3 jam)
   - With BKPM scrape: **+5-7 hari** (high risk of failure)

---

## 📋 Acceptance Criteria

### Gunakan BPS PMDN JIKA:
- ✅ Tujuan: Regional economic/environmental impact
- ✅ Acceptable: Provincial-level investment (not company-level)
- ✅ Timeline: Ingin selesai cepat (1-2 hari)
- ✅ Confidence: Medium confidence estimate OK

### Scrape BKPM JIKA:
- ❌ Tujuan: Company financial analysis / due diligence
- ❌ Require: Exact company investment figures
- ❌ Timeline: Fleksibel (bisa 1 minggu+)
- ❌ Risk tolerance: Siap handle scraping failure

---

## 💡 Proposed Workflow (Tanpa Scrape Tambahan)

**STEP 1:** Read BPS PMDN data ✅ (Already done)

**STEP 2:** Allocate to smelters
```python
# Proportional by capacity
for province in sulawesi_provinces:
    pmdn_value = bps_pmdn[province][year]
    mining_pmdn = pmdn_value * 0.4  # 40% assumption for mining
    
    for smelter in cgs_smelters[province]:
        smelter_investment = (smelter.capacity / total_capacity[province]) * mining_pmdn
```

**STEP 3:** Merge with MinerbaOne + CGS
```python
master_df['investment_idr_million'] = allocated_investment
master_df['investment_confidence'] = 'medium'
master_df['investment_source'] = 'bps_pmdn_allocated'
master_df['investment_note'] = 'Provincial PMDN allocated proportionally by capacity'
```

**STEP 4:** Document methodology clearly
```markdown
**Investment Data Methodology:**
- Source: BPS PMDN per provinsi (2016-2023)
- Allocation: Proportional by smelter capacity
- Assumption: 40% of provincial PMDN allocated to mining sector
- Confidence: MEDIUM (estimated, not actual per-company)
- Note: Does not include PMA (foreign investment)
```

---

## 🎯 JAWABAN FINAL

### ❓ Apakah BPS PMDN CUKUP untuk Nilai Investasi?

**JAWABAN:** 🟢 **YA, CUKUP** (dengan catatan)

**Reasoning:**
- ✅ Coverage provinsi & tahun: **Complete**
- ✅ Format data: **Clean & ready**
- 🟡 Granularity: **Provinsi-level** (bukan per-company, tapi **acceptable**)
- 🟡 Accuracy: **Estimated via allocation** (bukan exact, tapi **reasonable**)
- ✅ Untuk tujuan ECC impact analysis: **SUFFICIENT**

**Catatan Penting:**
1. Investment adalah **alokasi proporsional**, bukan actual per-company
2. Hanya PMDN (**domestik**), tidak termasuk PMA (foreign)
3. Asumsi 30-50% PMDN untuk sektor mining (adjustable)
4. Document methodology dengan jelas
5. Flag sebagai "**medium confidence**" data

---

### ❓ Apakah Perlu Scrape Tambahan dari BKPM?

**JAWABAN:** 🔴 **TIDAK PERLU** (not recommended)

**Reasoning:**
- 🔴 Effort scrape: **HIGH** (complex portal)
- 🔴 Success probability: **MEDIUM** (may need formal request)
- 🔴 Added value: **LIMITED** (for ECC impact analysis)
- ✅ BPS PMDN approximation: **Good enough**

**Exception:** Scrape BKPM hanya jika:
- User explicitly request exact company-level investment
- Timeline fleksibel (bisa 1 minggu+)
- Focus berubah ke financial analysis (bukan environmental)

---

*Assessment created: 11 Juni 2026*  
*CELIOS ECC Intelligence System*
