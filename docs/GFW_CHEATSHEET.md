# 📋 GFW DATA CHEATSHEET

**1-page quick reference untuk 19 dashboard cards**

---

## 🗂️ 3 FOLDER, 11 FILES

| Folder | Files | Cards Covered |
|--------|-------|---------------|
| **mega_fetch_v2** | 6 files | #1, #2, #3, #4, #10, #17 |
| **complete_fetch** | 4 files | #5, #14, #15, #18, #19 |
| **land_api_fetch** | 1 file | #6, #7, #8 |

---

## 🎯 19 CARDS → FILE LOCATION

| # | Card Name | File Location | Status |
|---|-----------|---------------|--------|
| 1 | Tree Cover Loss | `mega_fetch_v2/tree_cover_loss_*.csv` | ✅ |
| 2 | Primary Forest Loss | `mega_fetch_v2/primary_forest_loss_*.csv` | ✅ |
| 3 | Tree Cover by Category | `mega_fetch_v2/tree_cover_by_category_*.csv` | ✅ |
| 4 | Primary Forest by Category | Filter #3 by `is_primary=TRUE` | ⚠️ |
| 5 | Loss by Land Category | `complete_fetch/loss_by_category_*.csv` | ✅ |
| 6 | Primary Loss by Driver | Filter #7 by `is_primary=TRUE` | ⚠️ |
| 7 | Tree Cover Loss by Driver | `land_api_fetch/loss_by_driver_*.csv` | ✅ |
| 8 | CO2 Emissions | Column in #7: `co2_emissions_mg` | ✅ |
| 9 | Biomass Loss | N/A | ❌ |
| 10 | Loss in Protected Areas | `mega_fetch_v2/loss_in_protected_areas_*.csv` | ✅ |
| 11 | Primary Loss in Protected | Cross-ref #2 + #10 | ❌ |
| 12 | Fire Alerts | N/A | ❌ |
| 13 | GLAD Alerts | N/A | ❌ |
| 14 | Tree Cover Extent 2000 | `complete_fetch/tree_cover_extent_*.csv` | ✅ |
| 15 | Tree Cover Extent 2010 | Filter #14 by `year=2010` | ✅ |
| 16 | Current Tree Cover | Calculate: extent - loss + gain | ❌ |
| 17 | Tree Cover Gain | `mega_fetch_v2/tree_cover_gain_*.csv` | ✅ |
| 18 | Deforestation Rate | `complete_fetch/deforestation_rate_*.csv` | ✅ |
| 19 | Forest Cover Change | `complete_fetch/forest_cover_change_*.csv` | ✅ |

**Status:**
- ✅ DONE (11 cards)
- ⚠️ PARTIAL (2 cards - needs filtering)
- ❌ MISSING (6 cards)

---

## 🥇 THE GOLDEN FILE

```
land_api_fetch/loss_by_driver_sulawesi_2001_2025.csv
```

**Covers 3 cards:**
- #7: Tree Cover Loss by Driver (full dataset)
- #6: Primary Forest Loss by Driver (filter `is_primary=TRUE`)
- #8: CO2 Emissions (column `co2_emissions_mg`)

**Data:**
- 549 rows
- 2001-2023
- 5 provinces (Sulbar missing!)
- Commodity driven: 4.9M ha ← **MINING LINK!**

---

## 🔍 QUICK SEARCHES

### I need: Deforestation data
→ **Card #1:** `mega_fetch_v2/tree_cover_loss_*.csv`

### I need: PRIMARY forest loss
→ **Card #2:** `mega_fetch_v2/primary_forest_loss_*.csv`

### I need: Mining impact
→ **Card #7:** `land_api_fetch/loss_by_driver_*.csv`  
→ Filter: `driver = "Commodity driven deforestation"`

### I need: CO2 emissions
→ **Card #8:** `land_api_fetch/loss_by_driver_*.csv`  
→ Column: `co2_emissions_mg`

### I need: Protected area violations
→ **Card #10:** `mega_fetch_v2/loss_in_protected_areas_*.csv`

### I need: Deforestation rate (%)
→ **Card #18:** `complete_fetch/deforestation_rate_*.csv`

### I need: Baseline (year 2000)
→ **Card #14:** `complete_fetch/tree_cover_extent_*.csv`  
→ Filter: `year = 2000`

---

## 📊 DATA STATS

| Metric | Value |
|--------|-------|
| Total Cards | 19 |
| ✅ DONE | 11 (57.9%) |
| ⚠️ PARTIAL | 2 (10.5%) |
| ❌ MISSING | 6 (31.6%) |
| **Usable** | **13 (68.4%)** |
| Total CSV Files | 11 |
| Total Rows | ~3,000+ |
| Period | 2001-2025 |
| Provinces | 6 (5 in driver data) |

---

## 🚨 KNOWN ISSUES

1. **Sulawesi Barat missing** from driver data (#7, #6, #8)
2. Fire Alerts (#12) - SQL error
3. GLAD Alerts (#13) - Dataset 404
4. Biomass Loss (#9) - Invalid layer
5. Some null values in CO2 emissions

---

## 💡 PRO TIPS

1. **Start with the Golden File** (`loss_by_driver_*.csv`) for mining analysis
2. **Use primary_forest_loss** (#2) instead of tree_cover_loss (#1) for critical areas
3. **Cross-reference** protected areas (#10) with drivers (#7) for compliance
4. **Filter by year** to match your analysis period
5. **Check for nulls** in CO2 emissions before aggregating

---

## 🔗 RELATED DOCS

- `GFW_19_CARDS_FILE_MAPPING.md` - Detailed card descriptions
- `GFW_DATA_VISUAL_MAP.md` - Visual diagrams
- `gfw-api-documentation.md` - Full API reference
- `prd-fase1-d3tlh.md` - Project log

---

**Last Update:** 14 Juni 2026  
**Version:** 1.0  
**Status:** 68.4% complete (13/19 cards)
