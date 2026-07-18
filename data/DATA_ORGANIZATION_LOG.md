# Data Organization Log

**Date:** 2026-06-14  
**Task:** Clean up `data/processed/` folder  
**Status:** ✅ COMPLETED

---

## 📊 Summary

**Goal:** Hanya simpan 2 kategori di `data/processed/`: **Nasional** dan **Sulawesi** (final datasets only)

### Before
- **Total files:** 33 files
- **Issues:** 
  - Intermediate files mixed with final
  - Inconsistent naming (iku_sulawesi vs sulawesi_iku)
  - Per-year files (kemenkes_2014.csv - 2024.csv)
  - Provincial detail files (sulut_ika, bps_kesehatan_provinsi)

### After
- **Total files:** 10 files (3 nasional + 7 sulawesi)
- **Improvements:**
  - ✅ All intermediate files moved to `data/raw/`
  - ✅ Consistent naming: `{kategori}_{variabel}_{periode}.csv`
  - ✅ Clean separation: final vs intermediate
  - ✅ Clear README documentation

---

## 📁 Final Structure

### `data/processed/` (10 files)

**NASIONAL (3):**
1. `nasional_ika_2015_2024.csv`
2. `nasional_kesehatan_2014_2024.csv`
3. `nasional_limbah_b3_2020_2024.csv`

**SULAWESI (7):**
1. `sulawesi_iku_2015_2024.csv` ⭐ (newly completed)
2. `sulawesi_ika_2016_2024.csv`
3. `sulawesi_esdm_nikel.csv`
4. `sulawesi_faskes_agregat.csv`
5. `sulawesi_investasi_nikel.csv`
6. `sulawesi_limbah_b3.csv`
7. `sulawesi_konflik_lahan.csv`

### `data/raw/intermediate_*` (23 files moved)

**intermediate_iku/ (10 files):**
- IKU extraction steps (2015-2018 raw/clean)
- PDF table extracts (page-level)
- Old final versions (2019-2024)

**intermediate_kemenkes/ (11 files):**
- Per-year files: kemenkes_bersih_2014.csv → 2024.csv

**intermediate_other/ (2 files):**
- Provincial detail: bps_kesehatan_provinsi_2014_2024.csv
- Single province: sulut_ika_1_dekade_2016_2024.csv

---

## 🔄 File Mapping

### Renamed (Consistency)
| Old | New | Reason |
|:---|:---|:---|
| `iku_sulawesi_2015_2024_merged.csv` | `sulawesi_iku_2015_2024.csv` | Category-first naming |
| `semua_sulawesi_ika_1_dekade_2016_2024.csv` | `sulawesi_ika_2016_2024.csv` | Simplify name |
| `esdm_sulawesi_.csv` | `sulawesi_esdm_nikel.csv` | Remove trailing underscore |
| `faskes_sulawesi_agg.csv` | `sulawesi_faskes_agregat.csv` | Bahasa Indonesia |
| `investment_nickel_sulawesi_initial.csv` | `sulawesi_investasi_nikel.csv` | Bahasa Indonesia |
| `sulawesi_limbah_b3_ngo_proxy.csv` | `sulawesi_limbah_b3.csv` | Remove "proxy" suffix |
| `tanahkita_konflik_lengkap.csv` | `sulawesi_konflik_lahan.csv` | Category-first naming |
| `kemenkes_bersih_all.csv` | `nasional_kesehatan_2014_2024.csv` | Descriptive name |
| `nasional_ika_1_dekade_2015_2024.csv` | `nasional_ika_2015_2024.csv` | Remove redundant "1_dekade" |
| `nasional_limbah_b3_per_sektor_2020_2024.csv` | `nasional_limbah_b3_2020_2024.csv` | Simplify |

### Moved (Intermediate → Raw)
- 10 IKU intermediate files → `data/raw/intermediate_iku/`
- 11 Kemenkes per-year files → `data/raw/intermediate_kemenkes/`
- 2 provincial detail files → `data/raw/intermediate_other/`

---

## 📋 Naming Convention (New Standard)

**Format:** `{kategori}_{variabel}_{periode}.csv`

| Component | Options | Example |
|:---|:---|:---|
| **kategori** | `nasional`, `sulawesi` | `sulawesi` |
| **variabel** | `iku`, `ika`, `kesehatan`, `esdm`, `investasi`, `limbah_b3`, `konflik` | `iku` |
| **periode** | `YYYY_YYYY` (start_end year) | `2015_2024` |

**Full Example:** `sulawesi_iku_2015_2024.csv`

**Rules:**
- ✅ Category first (nasional/sulawesi)
- ✅ Lowercase with underscores
- ✅ Bahasa Indonesia preferred for variabel
- ✅ Period format: `YYYY_YYYY` (not "1_dekade")
- ❌ No trailing underscores (`esdm_sulawesi_.csv` ❌)
- ❌ No version suffixes in final (`_final`, `_initial`, `_v2`)

---

## ✅ Benefits

### For Development
1. **Faster file discovery** - Only 10 files instead of 33
2. **Clear intent** - File name tells everything (category, variable, period)
3. **No confusion** - Final vs intermediate clearly separated

### For Dashboard
1. **Simple imports** - `sulawesi_iku_2015_2024.csv` is obvious
2. **No filtering needed** - All files in processed are ready to use
3. **Consistent structure** - Same naming pattern across all datasets

### For Maintenance
1. **Reproducibility** - Intermediate steps preserved in raw/
2. **Audit trail** - Can trace back to extraction source
3. **Easy updates** - Replace final file, keep old in raw/archive/

---

## 🔗 Related Files

- `data/processed/README.md` - Complete documentation of final datasets
- `data/raw/intermediate_iku/README.md` - Documentation of IKU extraction steps (to be created)
- `docs/IKU_COLLECTION_FINAL_REPORT.md` - IKU data collection report

---

## 📝 Next Steps

1. ✅ Update scripts that reference old file names
2. ✅ Update documentation with new file names
3. 🔄 Test dashboard imports with new names
4. 📝 Create README in each intermediate_* folder
5. 🗄️ Create data/raw/archive/ for old versions

---

**Completed by:** CELIOS ECC Intelligence System  
**Date:** 2026-06-14  
**Files reorganized:** 33 → 10 (processed), 23 moved to raw
