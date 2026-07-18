# Deforestasi Data Collection - Executive Summary

**Status:** ✅ Tools Ready for Execution  
**Created:** 14 Juni 2026  
**Priority:** Checkpoint 1 - Prioritas #4 (KLHK Deforestation)

---

## 📊 QUICK OVERVIEW

| Aspect | Details |
|--------|---------|
| **Target Data** | Laju deforestasi Sulawesi 2016-2024 |
| **Primary Source** | Global Forest Watch (GFW) API - Hansen et al. (2013) |
| **Backup Source** | SLHI PDFs (KLHK) - 11 files (2015-2025) |
| **Expected Output** | `data/processed/sulawesi_deforestasi_2016_2024.csv` |
| **Timeline** | 1-2 days (data collection + validation) |
| **Estimated Rows** | 54 rows minimum (6 provinces × 9 years) |

---

## 🎯 STRATEGY: Triple Source Approach

### PRIMARY: Global Forest Watch API ⭐⭐⭐⭐⭐
- **Credibility:** Peer-reviewed (Science journal)
- **Coverage:** 2001-2023 (covers our 2016-2024 window)
- **Resolution:** 30m satellite imagery
- **Access:** Free API, no registration required
- **Quality:** HIGH - Global standard

### BACKUP 1: SLHI PDFs ⭐⭐⭐⭐⭐
- **Credibility:** Government official (KLHK)
- **Coverage:** 2015-2025 (10+ years)
- **Status:** ✅ Files already downloaded
- **Access:** PDF extraction required
- **Quality:** MEDIUM-HIGH - Official but extraction-dependent

### BACKUP 2: SIMONTANA Portal ⭐⭐⭐⭐⭐
- **Credibility:** Government official (KLHK real-time)
- **Coverage:** Current + historical
- **Status:** ⏳ Optional - requires scraping
- **Access:** Web scraping required
- **Quality:** HIGH - Detailed government monitoring

---

## 🛠️ TOOLS CREATED

### ✅ Completed Tools:

1. **`tools/gfw/gfw_api_client.py`**
   - GFW API client class
   - Sulawesi province codes mapping
   - Rate limiting & error handling

2. **`tools/gfw/fetch_sulawesi_deforestation.py`**
   - Main execution script
   - Batch fetch for all 6 provinces
   - Output: CSV with standardized schema

3. **`tools/pdf_extraction/extract_deforestasi_slhi.py`**
   - PDF table extraction using Camelot
   - Automatic table relevance detection
   - Sulawesi data filtering

4. **`scripts/consolidate_deforestasi.py`**
   - Merge GFW + SLHI data
   - Cross-validation & quality checks
   - Interpolation untuk missing values
   - Final output generation

5. **Documentation:**
   - `docs/DEFORESTASI_DATA_STRATEGY.md` - Full strategy (4-tier sources)
   - `docs/DEFORESTASI_EXECUTION_GUIDE.md` - Step-by-step guide
   - `tools/gfw/README.md` - GFW API documentation

---

## 🚀 EXECUTION STEPS (Quick Reference)

### Step 1: GFW API (15 minutes)
```bash
python tools/gfw/fetch_sulawesi_deforestation.py
```
**Output:** `data/raw/gfw/sulawesi_deforestation_2016_2024.csv`

### Step 2: SLHI Extraction (30 minutes)
```bash
python tools/pdf_extraction/extract_deforestasi_slhi.py
```
**Output:** `data/raw/klhk_slhi/deforestasi_sulawesi_slhi_extracted.csv`

### Step 3: Consolidation (10 minutes)
```bash
python scripts/consolidate_deforestasi.py
```
**Output:** `data/processed/sulawesi_deforestasi_2016_2024.csv`

**Total Time:** ~1 hour for core data collection

---

## 📋 EXPECTED OUTPUT SCHEMA

```csv
province,year,deforestation_rate_ha,forest_cover_pct,data_source,confidence_level,deforestation_rate_ha_slhi,deforestation_discrepancy_pct,deforestation_yoy_change_pct,cumulative_deforestation_ha
Sulawesi Utara,2016,12500.5,65.3,GFW_Hansen,High,13200.0,5.6,-,12500.5
Sulawesi Utara,2017,13200.8,64.8,GFW_Hansen,High,13500.0,2.3,5.6,25701.3
...
```

**Key Columns:**
- `deforestation_rate_ha` - Annual forest loss (hectares)
- `forest_cover_pct` - Remaining forest cover (%)
- `data_source` - GFW_Hansen (primary) or SLHI (validation)
- `confidence_level` - High/Medium/Low quality indicator
- `cumulative_deforestation_ha` - Total loss since 2016

---

## ✅ SUCCESS CRITERIA

### Minimum (Phase 1 Only):
- ✅ 54 rows (6 provinces × 9 years)
- ✅ GFW data quality >80%
- ✅ No extreme outliers
- ✅ Ready untuk Checkpoint 4 analysis

### Ideal (Phase 1+2+3):
- ✅ Dual source (GFW + SLHI)
- ✅ Cross-validation correlation >0.7
- ✅ 100% data completeness
- ✅ Discrepancy <20% average

---

## 🎓 ACADEMIC CREDIBILITY

### GFW Dataset Citation:
> Hansen, M. C., Potapov, P. V., Moore, R., Hancher, M., Turubanova, S. A., Tyukavina, A., ... & Townshend, J. R. G. (2013). High-resolution global maps of 21st-century forest cover change. *Science*, 342(6160), 850-853. https://doi.org/10.1126/science.1244693

**Impact:**
- 10,000+ citations
- Used by: World Bank, FAO, UNEP, CIFOR
- Global standard for forest monitoring

### Why This Matters for CELIOS Research:
1. ✅ **Peer-reviewed credibility** - Published in top-tier journal
2. ✅ **Globally accepted methodology** - Standardized across countries
3. ✅ **Replicable** - Other researchers can verify our findings
4. ✅ **Policy-relevant** - Used by international organizations

---

## 🔗 USE CASE: Checkpoint 4 Analysis

### Integration Points:

**Crosstab 1: Jumlah Smelter vs Kualitas Air**
```python
# Already have:
# - Smelter data: data/processed/sulawesi_esdm_nikel.csv (21 smelters)
# - Water quality: data/processed/sulawesi_ika_2016_2024.csv

# Now adding:
# - Deforestation: data/processed/sulawesi_deforestasi_2016_2024.csv

# New analysis possible:
# Smelter expansion → Deforestation → Water quality degradation
```

**Crosstab 2: PLTU Captive vs Kualitas Udara**
```python
# Deforestation as additional indicator:
# Energy infrastructure → Forest clearing → Air quality impact
```

**Crosstab 3: Luas Industri vs Deforestasi** ⭐ NEW ENABLED
```python
# Direct correlation:
df_merge = pd.merge(df_mining, df_deforestation, on=['province', 'year'])
correlation = df_merge[['total_capacity_MTPA', 'deforestation_rate_ha']].corr()
# Hypothesis: Mining expansion drives deforestation
```

---

## 📈 EXPECTED FINDINGS (Hypothesis)

Based on preliminary research:

1. **Sulawesi Tengah (Morowali):**
   - Highest deforestation rate (nickel smelter hub)
   - 2016-2024: ~100,000+ hectares lost
   - Correlation: PTVI, GNI, IMIP smelter expansions

2. **Sulawesi Tenggara (Kolaka, Konawe):**
   - Second highest deforestation
   - Mining infrastructure corridors
   - Coastal forest conversion

3. **Temporal Trend:**
   - Acceleration post-2017 (nickel downstreaming policy)
   - Peak 2019-2021 (smelter construction boom)
   - Continued loss 2022-2024

4. **Policy Failure Evidence:**
   - D3TLH status: "AMAN" or "TERTEKAN"
   - Permits issued: CONTINUE despite forest loss
   - → D3TLH blind spot: Forest metrics not factored

---

## ⚠️ KNOWN LIMITATIONS

1. **Data Recency:**
   - GFW: Latest 2023 (2024 data might incomplete)
   - SLHI: 2025 report available, but extraction dependent

2. **Granularity:**
   - Province-level aggregate (kabupaten breakdown limited)
   - Cannot pinpoint specific mine sites without GIS overlay

3. **Causation:**
   - Correlation ≠ causation
   - Need additional evidence (mining permits, satellite imagery)
   - AMDAL documents for site-specific validation

4. **Data Quality:**
   - SLHI extraction accuracy depends on PDF structure
   - Manual validation recommended for key findings

**Mitigation:**
- Document all limitations transparently
- Use conservative estimates
- Cross-validate with multiple sources
- Triangulate dengan news reports, NGO studies

---

## 📞 SUPPORT & TROUBLESHOOTING

### Common Issues:

**Q: GFW API returns empty data?**  
A: Check admin codes, try alternative endpoint, review API changelog

**Q: SLHI PDF extraction fails?**  
A: Install Ghostscript, try tabula-py, fallback to manual extraction

**Q: Low correlation between GFW and SLHI?**  
A: Use GFW only (higher credibility), document SLHI as supplementary

### Getting Help:

- **Documentation:** `docs/DEFORESTASI_EXECUTION_GUIDE.md`
- **API Docs:** https://data.globalforestwatch.org/documents
- **Script Issues:** Check logs, add `logger.debug()` for verbose output

---

## ✅ NEXT ACTIONS

### Immediate (Today/Tomorrow):
1. [ ] Execute Phase 1: GFW API fetch
2. [ ] Execute Phase 2: SLHI extraction
3. [ ] Execute Phase 3: Consolidation
4. [ ] Update PRD log dengan hasil

### Short-term (This Week):
5. [ ] Integrate data ke Checkpoint 4 dashboard
6. [ ] Create visualizations (time series, provincial comparison)
7. [ ] Correlation analysis dengan mining/smelter data
8. [ ] Draft initial findings

### Medium-term (Next Week):
9. [ ] Cross-validate dengan SIMONTANA (optional)
10. [ ] Request NGO datasets (Auriga, WALHI)
11. [ ] Literature review: Similar studies di Indonesia
12. [ ] Prepare methodology section for report

---

**Status:** 🟢 READY FOR EXECUTION  
**Confidence:** HIGH (Global Forest Watch = gold standard)  
**Risk Level:** LOW (multiple backup sources available)  
**Priority:** HIGH (critical for Checkpoint 4)

---

**Prepared by:** CELIOS Research Division  
**Date:** 14 Juni 2026  
**Document:** DEFORESTASI_SUMMARY.md  
**Related:** prd-fase1-d3tlh.md (Checkpoint 1, Prioritas #4)
