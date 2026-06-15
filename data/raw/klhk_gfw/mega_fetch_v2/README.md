# GFW API Mega Fetch V2 - Dataset Catalog
## Comprehensive Forest Data Collection for Sulawesi (2001-2025)

**Execution Date:** 14 Juni 2026  
**Data Source:** [Global Forest Watch DATA API v2](https://data-api.globalforestwatch.org)  
**Method:** Zonal Statistics Analysis via Geostore IDs  
**Coverage:** 6 Provinsi Sulawesi  
**API Key:** `21899f40-1f6d-4ff9-93e1-c10d04513984` (valid until 14 Juni 2027)

---

## 📊 Datasets Collected (6 Files)

### 1. **Tree Cover Loss (2001-2025)**
- **File:** `tree_cover_loss_sulawesi_2001_2025.csv`
- **Rows:** 156 (6 provinsi × 26 tahun)
- **Columns:** `year`, `tree_cover_loss_ha`, `province`
- **Total Loss:** 97.8 juta hektar (2001-2025)
- **API Layer:** `umd_tree_cover_loss__year`
- **Description:** Annual tree cover loss in hectares per province

**Sample Data:**
```
year,tree_cover_loss_ha,province
2001.0,4140.57938,Sulawesi Utara
2002.0,7110.936409999999,Sulawesi Utara
2003.0,2617.6355,Sulawesi Utara
```

---

### 2. **Primary Forest Loss (2001-2025)**
- **File:** `primary_forest_loss_sulawesi_2001_2025.csv`
- **Rows:** 312 (6 provinsi × 26 tahun × 2 categories)
- **Columns:** `umd_tree_cover_loss__year`, `is__umd_regional_primary_forest_2001`, `area__ha`, `province`, `year`
- **API Layers:** `umd_tree_cover_loss__year`, `is__umd_regional_primary_forest_2001`
- **Description:** Tree cover loss breakdown by primary forest status (true/false)
- **Key Insight:** Allows differentiation between primary forest loss vs secondary forest loss

**Sample Data:**
```
umd_tree_cover_loss__year,is__umd_regional_primary_forest_2001,area__ha,province,year
2001,false,3385.48053,Sulawesi Utara,2001.0
2001,true,755.09888,Sulawesi Utara,2001.0
```

---

### 3. **Tree Cover by Category**
- **File:** `tree_cover_by_category_sulawesi_2001_2025.csv`
- **Rows:** 54
- **Columns:** varies by category type
- **API Layers:** `wdpa_protected_areas__iucn_cat`, `gfw_plantations__type`
- **Description:** Tree cover area breakdown by land use category
- **Categories Covered:**
  - WDPA Protected Areas (IUCN categories: Ia, Ib, II, III, IV, V, VI, Not Applicable, Not Assigned, Not Reported)
  - GFW Plantation Types (Oil Palm, Wood Fiber, Other)

**Sample Data:**
```
wdpa_protected_areas__iucn_cat,area__ha,category_type,province
II,2169.8557,wdpa_protected_areas__iucn_cat,Sulawesi Utara
```

---

### 4. **Loss in Protected Areas (2001-2025)**
- **File:** `loss_in_protected_areas_sulawesi_2001_2025.csv`
- **Rows:** 468
- **Columns:** `umd_tree_cover_loss__year`, `wdpa_protected_areas__iucn_cat`, `area__ha`, `province`, `year`
- **API Layers:** `umd_tree_cover_loss__year`, `wdpa_protected_areas__iucn_cat`
- **Description:** Annual tree cover loss within protected areas by IUCN category
- **Key Insight:** Critical for analyzing effectiveness of protected area management

**Sample Data:**
```
umd_tree_cover_loss__year,wdpa_protected_areas__iucn_cat,area__ha,province,year
2001,II,143.5884,Sulawesi Utara,2001.0
2001,Not Applicable,3951.56117,Sulawesi Utara,2001.0
```

---

### 5. **Tree Cover Gain**
- **File:** `tree_cover_gain_sulawesi_2001_2025.csv`
- **Rows:** 12 (6 provinsi × 2 categories: gain vs no-gain)
- **Columns:** `is__umd_tree_cover_gain`, `area__ha`, `province`
- **Total Gain:** 232,000 hektar (across 6 provinces)
- **API Layer:** `is__umd_tree_cover_gain`
- **Description:** Total tree cover gain (2000-2012 period) per province

**Sample Data:**
```
is__umd_tree_cover_gain,area__ha,province
false,22362665.03536,Sulawesi Utara
true,3636.43141,Sulawesi Utara
```

**Provincial Gain Breakdown:**
- Sulawesi Tengah: **72,133 ha** (highest)
- Sulawesi Selatan: **67,615 ha**
- Sulawesi Tenggara: **47,691 ha**
- Sulawesi Barat: **29,971 ha**
- Gorontalo: **6,931 ha**
- Sulawesi Utara: **3,636 ha** (lowest)

---

### 6. **Loss by Land Cover Type (2001-2025)**
- **File:** `loss_by_land_cover_sulawesi_2001_2025.csv`
- **Rows:** 741
- **Columns:** `umd_tree_cover_loss__year`, `esa_land_cover_2015__class`, `area__ha`, `province`, `year`
- **API Layers:** `umd_tree_cover_loss__year`, `esa_land_cover_2015__class`
- **Description:** Tree cover loss by ESA land cover classification
- **Land Cover Classes:** 20+ types (Tree cover, Shrubland, Grassland, Cropland, Urban, Wetland, etc.)

**Sample Data:**
```
umd_tree_cover_loss__year,esa_land_cover_2015__class,area__ha,province,year
2001,Tree cover,3985.66894,Sulawesi Utara,2001.0
2001,Shrubland,154.91035,Sulawesi Utara,2001.0
```

---

## 🔧 Technical Details

### Geostore IDs Used
```json
{
  "Sulawesi Utara": "89b35f128c9cfe7685e1738c89a0a730",
  "Sulawesi Tengah": "fce1e175169936334347ae17207381a0",
  "Sulawesi Selatan": "abc6fc008f433d3dbdc65861bdcc8a87",
  "Sulawesi Tenggara": "fe2e396191a0e8b6e70aa03dd225d7f7",
  "Gorontalo": "db937e7121c426140dd91072c14bbdaf",
  "Sulawesi Barat": "77f83070a9b4111e24a7cfdea73a5adb"
}
```

### API Endpoint Used
```
GET https://data-api.globalforestwatch.org/analysis/zonal/{geostore_id}
```

### Query Parameters Pattern
```
?sum=area__ha
&group_by=umd_tree_cover_loss__year
&geostore_origin=gfw
```

### Rate Limiting
- 1 second delay between queries
- Total execution time: ~5 minutes for 6 provinces

---

## ❌ Failed Dataset Attempts

### 7. **Tree Cover Density** (FAILED)
- **Target Layers:** `umd_tree_cover_density_2000__30`, `umd_tree_cover_density_2010__30`
- **Error:** `Layer umd_tree_cover_density_2000__30 is invalid` (422 status)
- **Reason:** Density layers tidak tersedia untuk zonal analysis endpoint
- **Alternative:** Data dapat diakses via tile-based query (bukan zonal)

### Other Invalid Layers Discovered:
- `whrc_aboveground_co2_emissions__Mg` - CO2 emissions layer invalid
- `tsc_tree_cover_loss_drivers__type` - Tree cover loss drivers invalid
- `is__gfw_mining`, `is__gfw_oil_palm` - Mining/oil palm layers invalid

---

## 📈 Data Quality & Coverage

### Temporal Coverage
- **Start Year:** 2001
- **End Year:** 2025
- **Total Years:** 25 years (extends beyond original target of 2016-2024!)

### Spatial Coverage
- **6 Provinces:** Complete coverage of Sulawesi region
- **Analysis Unit:** Province-level aggregation via geostores

### Data Completeness
- **Tree Cover Loss:** ✅ Complete (156/156 expected rows)
- **Primary Forest Loss:** ✅ Complete (312/312 expected rows)
- **Protected Areas Loss:** ✅ Complete (468 rows)
- **Tree Cover Gain:** ✅ Complete (12/12 expected rows)
- **Land Cover Loss:** ✅ Complete (741 rows)
- **Category Breakdown:** ✅ Complete (54 rows)

---

## 🔗 Data Source Attribution

**Citation:**
> Hansen, M. C., P. V. Potapov, R. Moore, M. Hancher, S. A. Turubanova, A. Tyukavina, D. Thau, S. V. Stehman, S. J. Goetz, T. R. Loveland, A. Kommareddy, A. Egorov, L. Chini, C. O. Justice, and J. R. G. Townshend. 2013. "High-Resolution Global Maps of 21st-Century Forest Cover Change." Science 342 (15 November): 850–53.

**Data Access:**
- Global Forest Watch DATA API: https://data-api.globalforestwatch.org
- Interactive Dashboard: https://www.globalforestwatch.org
- Data Download Portal: https://data.globalforestwatch.org

**License:** Open Data (CC BY 4.0)

---

## 🔄 Next Steps

1. **Cross-Validation:** Compare GFW data dengan SLHI PDF extraction
2. **Consolidation:** Merge GFW + SLHI untuk dataset final
3. **Processing:** Generate `data/processed/sulawesi_deforestation_2001_2025_consolidated.csv`
4. **Dashboard Integration:** Integrate deforestation data ke Checkpoint 4 visualizations

---

## 📁 Related Files

- **Scripts:** `tools/gfw/fetch_all_gfw_data_v2.py`
- **Geostore Mapping:** `data/raw/klhk_gfw/sulawesi_geostore_mapping.json`
- **API Key Config:** `.env.gfw`
- **Documentation:** `docs/prd-fase1-d3tlh.md` (entry: 14 Juni 2026)

---

**Generated:** 14 Juni 2026  
**Script Version:** fetch_all_gfw_data_v2.py  
**Success Rate:** 6/7 datasets (86%)  
**Total Data Points:** 1,743 rows
