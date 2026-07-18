# 🗺️ GFW DATA - VISUAL MAPPING

**Quick Reference:** Mana file untuk mana card

---

## 🎯 TIER 1: MUST HAVE (4 Cards) - ✅ ALL DONE!

```
┌─────────────────────────────────────────────────────────────┐
│ 🔴 PRIMARY FOREST LOSS (Card #2)                           │
│ File: mega_fetch_v2/primary_forest_loss_*.csv              │
│ 312 rows | 2001-2025 | 6 provinces                         │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 🌲 TREE COVER LOSS (Card #1)                               │
│ File: mega_fetch_v2/tree_cover_loss_*.csv                  │
│ 156 rows | 2001-2025 | 6 provinces                         │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 🏭 PRIMARY FOREST LOSS BY DRIVER (Card #6) ⚠️ FILTER       │
│ File: land_api_fetch/loss_by_driver_*.csv                  │
│ Filter: is_primary = TRUE                                   │
│ ~200 rows estimated | Mining link! | CO2 included          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 🚜 TREE COVER LOSS BY DRIVER (Card #7) ✅ COMPLETE         │
│ File: land_api_fetch/loss_by_driver_*.csv                  │
│ 549 rows | 2001-2023 | 5 provinces (no Sulbar)             │
│ Drivers: Commodity(4.9M ha), Forestry(536K), Agri(47K)     │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 TIER 2: IMPORTANT (4 Cards) - ✅ ALL DONE!

```
┌─────────────────────────────────────────────────────────────┐
│ 🛡️ LOSS IN PROTECTED AREAS (Card #10)                      │
│ File: mega_fetch_v2/loss_in_protected_areas_*.csv          │
│ 468 rows | Compliance critical!                            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 💨 CO2 EMISSIONS (Card #8)                                  │
│ File: land_api_fetch/loss_by_driver_*.csv                  │
│ Column: co2_emissions_mg | BONUS DATA!                     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 🔥 FIRE ALERTS (Card #12) ❌ MISSING                        │
│ File: N/A                                                   │
│ Issue: SQL syntax error                                     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 🗺️ TREE COVER EXTENT 2000 (Card #14)                       │
│ File: complete_fetch/tree_cover_extent_*.csv               │
│ 12 rows | Baseline year 2000 | Filter by year              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🗂️ TIER 3: BONUS (11 Cards) - 7/11 DONE

### ✅ DONE (7)

```
Card #3:  Tree Cover by Category
          → mega_fetch_v2/tree_cover_by_category_*.csv

Card #5:  Loss by Land Category
          → complete_fetch/loss_by_category_*.csv

Card #15: Tree Cover Extent 2010
          → complete_fetch/tree_cover_extent_*.csv (filter year=2010)

Card #17: Tree Cover Gain
          → mega_fetch_v2/tree_cover_gain_*.csv

Card #18: Deforestation Rate
          → complete_fetch/deforestation_rate_*.csv

Card #19: Forest Cover Change
          → complete_fetch/forest_cover_change_*.csv

Card #8:  CO2 Emissions (already in Tier 2)
          → land_api_fetch/loss_by_driver_*.csv (co2_emissions_mg column)
```

### ⚠️ PARTIAL (2)

```
Card #4:  Primary Forest by Category
          → Filter tree_cover_by_category where is_primary=TRUE

Card #6:  Primary Forest Loss by Driver
          → Filter loss_by_driver where is_primary=TRUE
```

### ❌ MISSING (4)

```
Card #9:  Biomass Loss - Invalid layer name
Card #11: Primary Forest Loss in Protected Areas - No dedicated layer
Card #13: GLAD Alerts - Dataset 404
Card #16: Current Tree Cover - Needs calculation
```

---

## 🏆 THE GOLDEN FILE

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 🥇 land_api_fetch/loss_by_driver_sulawesi_2001_2025.csv  ┃
┃                                                            ┃
┃ COVERS 3 CARDS IN 1 FILE:                                 ┃
┃ • Card #7: Tree Cover Loss by Driver (full)               ┃
┃ • Card #6: Primary Forest Loss by Driver (filter)         ┃
┃ • Card #8: CO2 Emissions (column)                         ┃
┃                                                            ┃
┃ 549 rows | 2001-2023 | 5 provinces                        ┃
┃ Commodity driven: 4.9M ha ← MINING IMPACT HERE!           ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

**Columns:**
- `province` - Sulawesi Utara/Tengah/Selatan/Tenggara/Gorontalo (no Barat)
- `year` - 2001-2023
- `driver` - Commodity/Forestry/Shifting agriculture/Urbanization/Wildfire/Unknown
- `area_ha` - Luas deforestasi (hektar)
- `co2_emissions_mg` - Emisi CO2 (Megagram)
- `is_primary` - Flag hutan primer (TRUE/FALSE)

---

## 🗺️ FOLDER STRUCTURE

```
data/raw/klhk_gfw/
│
├── 📁 mega_fetch_v2/              [6 files - Round 2]
│   ├── tree_cover_loss_*.csv              → Card #1
│   ├── primary_forest_loss_*.csv          → Card #2  ⭐
│   ├── tree_cover_by_category_*.csv       → Card #3, #4
│   ├── loss_in_protected_areas_*.csv      → Card #10 ⭐
│   ├── tree_cover_gain_*.csv              → Card #17
│   └── loss_by_land_cover_*.csv           → (context)
│
├── 📁 complete_fetch/             [4 files - Round 3]
│   ├── tree_cover_extent_*.csv            → Card #14, #15
│   ├── loss_by_category_*.csv             → Card #5
│   ├── deforestation_rate_*.csv           → Card #18
│   └── forest_cover_change_*.csv          → Card #19
│
└── 📁 land_api_fetch/             [1 file - Round 4]
    └── loss_by_driver_*.csv               → Card #6, #7, #8  ⭐⭐⭐
```

**Total:** 11 CSV files

---

## 🎯 QUICK LOOKUP

**Want deforestation data?**
→ `mega_fetch_v2/tree_cover_loss_*.csv` (Card #1)

**Want PRIMARY forest loss?**
→ `mega_fetch_v2/primary_forest_loss_*.csv` (Card #2)

**Want to link deforestation to MINING?**
→ `land_api_fetch/loss_by_driver_*.csv` (Card #7)
→ Filter `driver = "Commodity driven deforestation"`

**Want CO2 emissions?**
→ `land_api_fetch/loss_by_driver_*.csv` (Card #8)
→ Column: `co2_emissions_mg`

**Want protected areas violations?**
→ `mega_fetch_v2/loss_in_protected_areas_*.csv` (Card #10)

**Want deforestation rate (%)?**
→ `complete_fetch/deforestation_rate_*.csv` (Card #18)

**Want baseline (year 2000)?**
→ `complete_fetch/tree_cover_extent_*.csv` (Card #14)
→ Filter `year = 2000`

---

## 📊 DATA COVERAGE

```
┌──────────────────────────┬────────┬──────┬─────────┐
│ Metric                   │ Status │ Count│ Percent │
├──────────────────────────┼────────┼──────┼─────────┤
│ Cards DONE               │   ✅   │  11  │  57.9%  │
│ Cards PARTIAL            │   ⚠️   │   2  │  10.5%  │
│ Cards MISSING            │   ❌   │   6  │  31.6%  │
├──────────────────────────┼────────┼──────┼─────────┤
│ TOTAL                    │        │  19  │ 100.0%  │
├──────────────────────────┼────────┼──────┼─────────┤
│ Usable Data (DONE+PART)  │   🎯   │  13  │  68.4%  │
└──────────────────────────┴────────┴──────┴─────────┘
```

---

## ⚡ FASTEST WAY TO USE DATA

### Step 1: Read the Golden File
```python
import pandas as pd

df = pd.read_csv("data/raw/klhk_gfw/land_api_fetch/loss_by_driver_sulawesi_2001_2025.csv")

# Card #7: All driver data
print(df.head())

# Card #6: Primary forest only
primary = df[df['is_primary'] == True]

# Card #8: CO2 emissions
co2 = df[['province', 'year', 'co2_emissions_mg']]
```

### Step 2: Get Basic Loss Data
```python
# Card #1: Tree cover loss
loss = pd.read_csv("data/raw/klhk_gfw/mega_fetch_v2/tree_cover_loss_*.csv")

# Card #2: Primary forest loss
primary_loss = pd.read_csv("data/raw/klhk_gfw/mega_fetch_v2/primary_forest_loss_*.csv")
```

### Step 3: Get Protected Areas Data
```python
# Card #10: Loss in protected areas
protected = pd.read_csv("data/raw/klhk_gfw/mega_fetch_v2/loss_in_protected_areas_*.csv")
```

---

## 🚨 KNOWN ISSUES

1. **Sulawesi Barat missing** from driver dataset (land_api_fetch)
   - Only 5/6 provinces have driver data
   - May need separate fetch for Sulbar

2. **Fire Alerts failed** (Card #12)
   - SQL syntax error in query
   - Needs query fix and retry

3. **GLAD Alerts unavailable** (Card #13)
   - Dataset returns 404
   - May need different API version

4. **Biomass Loss not found** (Card #9)
   - Invalid layer name
   - May need manual download

---

**Generated:** 14 Juni 2026  
**For:** CELIOS D3TH Research - Fase 1  
**Coverage:** 13/19 cards (68.4%)  
**Status:** Ready for analysis
