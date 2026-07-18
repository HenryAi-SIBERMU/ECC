# 🌲 GFW DEFORESTATION DATA - SULAWESI

**Collection Date:** 14 Juni 2026  
**Coverage:** 2001-2025  
**Geographic Scope:** 6 Sulawesi provinces  
**API Source:** Global Forest Watch Data API v3

---

## 📊 DATA OVERVIEW

| Metric | Value |
|--------|-------|
| Total CSV Files | 11 |
| Dashboard Cards Covered | 13/19 (68.4%) |
| Total Data Rows | ~3,000+ |
| Time Period | 2001-2025 |
| Provinces | 6 (Sulawesi Utara, Tengah, Selatan, Tenggara, Gorontalo, Barat) |

---

## 🗂️ FOLDER STRUCTURE

```
klhk_gfw/
├── mega_fetch_v2/          [Round 2: Zonal Analysis - 6 files]
│   ├── tree_cover_loss_*.csv
│   ├── primary_forest_loss_*.csv
│   ├── tree_cover_by_category_*.csv
│   ├── loss_in_protected_areas_*.csv
│   ├── tree_cover_gain_*.csv
│   └── loss_by_land_cover_*.csv
│
├── complete_fetch/         [Round 3: SQL Query - 4 files]
│   ├── tree_cover_extent_*.csv
│   ├── loss_by_category_*.csv
│   ├── deforestation_rate_*.csv
│   └── forest_cover_change_*.csv
│
└── land_api_fetch/         [Round 4: Beta Land API - 1 file]
    └── loss_by_driver_*.csv     ← CRITICAL! Contains driver + CO2 data
```

---

## 🥇 THE GOLDEN FILE

**`land_api_fetch/loss_by_driver_sulawesi_2001_2025.csv`**

This single file contains data for **3 dashboard cards**:
- Card #7: Tree Cover Loss by Driver (full dataset)
- Card #6: Primary Forest Loss by Driver (filter `is_primary=TRUE`)
- Card #8: CO2 Emissions (column `co2_emissions_mg`)

**Key Data:**
- 549 rows
- 2001-2023
- 5 provinces (Sulawesi Barat missing!)
- Commodity-driven deforestation: **4.9M ha** ← Links to mining activity!

---

## 📋 QUICK FILE REFERENCE

### mega_fetch_v2/ (6 files)

| File | Rows | Cards | Description |
|------|------|-------|-------------|
| `tree_cover_loss_*.csv` | 156 | #1 | Total tree cover loss per year |
| `primary_forest_loss_*.csv` | 312 | #2 | Primary forest loss per year |
| `tree_cover_by_category_*.csv` | 54 | #3, #4 | Tree cover by land category |
| `loss_in_protected_areas_*.csv` | 468 | #10 | Loss in protected areas |
| `tree_cover_gain_*.csv` | 12 | #17 | Tree cover gain 2000-2020 |
| `loss_by_land_cover_*.csv` | 741 | - | Loss by land cover type |

### complete_fetch/ (4 files)

| File | Rows | Cards | Description |
|------|------|-------|-------------|
| `tree_cover_extent_*.csv` | 12 | #14, #15 | Tree cover extent 2000 & 2010 |
| `loss_by_category_*.csv` | 1,331 | #5 | Loss by land category |
| `deforestation_rate_*.csv` | 150 | #18 | Deforestation rate (%) |
| `forest_cover_change_*.csv` | 150 | #19 | Net forest cover change |

### land_api_fetch/ (1 file)

| File | Rows | Cards | Description |
|------|------|-------|-------------|
| `loss_by_driver_*.csv` | 549 | #6, #7, #8 | Loss by driver + CO2 emissions |

---

## 🎯 COMMON QUERIES

### Q: Where's the mining impact data?
**A:** `land_api_fetch/loss_by_driver_*.csv`  
Filter: `driver = "Commodity driven deforestation"`  
Result: 4.9M ha deforestation linked to commodity sector (mining + plantations)

### Q: Where's the primary forest data?
**A:** `mega_fetch_v2/primary_forest_loss_*.csv`  
312 rows covering 2001-2025 for all 6 provinces

### Q: Where's the CO2 emissions data?
**A:** `land_api_fetch/loss_by_driver_*.csv`  
Column: `co2_emissions_mg`

### Q: Where's the protected area violations?
**A:** `mega_fetch_v2/loss_in_protected_areas_*.csv`  
468 rows showing deforestation inside protected areas

### Q: Where's the baseline (year 2000)?
**A:** `complete_fetch/tree_cover_extent_*.csv`  
Filter: `year = 2000`

---

## 🚨 KNOWN ISSUES

1. **Sulawesi Barat missing** from driver dataset
   - Only 5/6 provinces in `loss_by_driver_*.csv`
   - May need separate API call

2. **Missing Cards:**
   - Card #9: Biomass Loss (API layer invalid)
   - Card #11: Primary Loss in Protected Areas (no dedicated endpoint)
   - Card #12: Fire Alerts (SQL error)
   - Card #13: GLAD Alerts (dataset 404)
   - Card #16: Current Tree Cover (needs calculation)

3. **Data Quality:**
   - Some null values in CO2 emissions
   - Year ranges vary by dataset
   - Some provinces have incomplete data for certain years

---

## 📖 USAGE EXAMPLE

```python
import pandas as pd

# Load the golden file
driver_data = pd.read_csv("land_api_fetch/loss_by_driver_sulawesi_2001_2025.csv")

# Get mining impact (commodity-driven deforestation)
mining = driver_data[driver_data['driver'] == 'Commodity driven deforestation']
print(f"Mining-related deforestation: {mining['area_ha'].sum():,.0f} ha")

# Get CO2 emissions
total_co2 = driver_data['co2_emissions_mg'].sum()
print(f"Total CO2 emissions: {total_co2:,.0f} Mg")

# Get primary forest loss
primary = driver_data[driver_data['is_primary'] == True]
print(f"Primary forest loss: {primary['area_ha'].sum():,.0f} ha")
```

---

## 🔗 DOCUMENTATION

- **Full Card Mapping:** `docs/GFW_19_CARDS_FILE_MAPPING.md`
- **Visual Map:** `docs/GFW_DATA_VISUAL_MAP.md`
- **Cheatsheet:** `docs/GFW_CHEATSHEET.md`
- **API Reference:** `docs/gfw-api-documentation.md`
- **Loading Script:** `tools/gfw/load_gfw_data_example.py`

---

## 📞 DATA COLLECTION SCRIPTS

| Script | Purpose | Status |
|--------|---------|--------|
| `fetch_all_gfw_data.py` | Round 1 - Discovery | Deprecated |
| `fetch_all_gfw_data_v2.py` | Round 2 - Zonal Analysis | ✅ Success (6 files) |
| `fetch_complete_gfw_data.py` | Round 3 - SQL Query | ✅ Success (4 files) |
| `fetch_drivers_via_land_api.py` | Round 4 - Beta Land API | ✅ Success (1 file) |

All scripts located in: `tools/gfw/`

---

## 🔐 API CREDENTIALS

API Key stored in: `.env.gfw`  
Valid until: 14 Juni 2027  
Base URL: `https://data-api.globalforestwatch.org`

---

**Last Updated:** 14 Juni 2026  
**For Project:** CELIOS D3TLH Research - Fase 1  
**Status:** 68.4% complete (13/19 dashboard cards)
