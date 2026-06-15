# Data Processed - Final Datasets

**Last Updated:** 2026-06-15

Folder ini hanya berisi **dataset final** yang siap digunakan untuk dashboard dan analisis. Semua file intermediate/per-tahun/per-provinsi sudah dipindahkan ke `data/raw/`.

---

## 📁 Struktur File

### 🌏 NASIONAL (3 files)

| File | Deskripsi | Periode | Rows | Provinsi |
|:---|:---|:---:|---:|:---:|
| `nasional_ika_2015_2024.csv` | Indeks Kualitas Air Nasional | 2015-2024 | 10 | Nasional |
| `nasional_kesehatan_2014_2024.csv` | Fasilitas Kesehatan Nasional | 2014-2024 | ~34,000 | 34 provinsi |
| `nasional_limbah_b3_2020_2024.csv` | Limbah B3 per Sektor | 2020-2024 | 5 | Nasional |

### 🗺️ SULAWESI (7 files)

| File | Deskripsi | Periode | Rows | Provinsi |
|:---|:---|:---:|---:|:---:|
| `sulawesi_iku_2015_2024.csv` | **Indeks Kualitas Udara (IKU)** | 2015-2024 | 54 | 6 Sulawesi |
| `sulawesi_ika_2016_2024.csv` | Indeks Kualitas Air (IKA) | 2016-2024 | 54 | 6 Sulawesi |
| `sulawesi_esdm_nikel.csv` | Data ESDM Nikel | 2020-2024 | ~50 | 6 Sulawesi |
| `sulawesi_faskes_agregat.csv` | Fasilitas Kesehatan Agregat | 2014-2024 | 66 | 6 Sulawesi |
| `sulawesi_investasi_nikel.csv` | Investasi Sektor Nikel | 2016-2026 | ~30 | 6 Sulawesi |
| `sulawesi_limbah_b3.csv` | Limbah B3 (NGO Proxy) | 2020-2024 | 5 | Nasional (proxy) |
| `sulawesi_konflik_lahan.csv` | Konflik Lahan (Tanahkita) | 2024 | ~40 | 6 Sulawesi |

---

## 📋 Naming Convention

**Format:** `{kategori}_{variabel}_{periode}.csv`

- **Kategori:** `nasional` atau `sulawesi`
- **Variabel:** `iku`, `ika`, `kesehatan`, `limbah_b3`, dll.
- **Periode:** `2015_2024`, `2016_2024`, dll.

**Contoh:**
- ✅ `sulawesi_iku_2015_2024.csv` - Clear, consistent
- ❌ `iku_sulawesi_2019_2024_final.csv` - Old format (moved to raw)

---

## 🗂️ File Mapping (Old → New)

### Renamed Files
| Old Name | New Name | Status |
|:---|:---|:---:|
| `iku_sulawesi_2015_2024_merged.csv` | `sulawesi_iku_2015_2024.csv` | ✅ Renamed |
| `semua_sulawesi_ika_1_dekade_2016_2024.csv` | `sulawesi_ika_2016_2024.csv` | ✅ Renamed |
| `esdm_sulawesi_.csv` | `sulawesi_esdm_nikel.csv` | ✅ Renamed |
| `faskes_sulawesi_agg.csv` | `sulawesi_faskes_agregat.csv` | ✅ Renamed |
| `investment_nickel_sulawesi_initial.csv` | `sulawesi_investasi_nikel.csv` | ✅ Renamed |
| `sulawesi_limbah_b3_ngo_proxy.csv` | `sulawesi_limbah_b3.csv` | ✅ Renamed |
| `tanahkita_konflik_lengkap.csv` | `sulawesi_konflik_lahan.csv` | ✅ Renamed |
| `kemenkes_bersih_all.csv` | `nasional_kesehatan_2014_2024.csv` | ✅ Renamed |
| `nasional_ika_1_dekade_2015_2024.csv` | `nasional_ika_2015_2024.csv` | ✅ Renamed |
| `nasional_limbah_b3_per_sektor_2020_2024.csv` | `nasional_limbah_b3_2020_2024.csv` | ✅ Renamed |

### Moved to Raw
| File | New Location | Reason |
|:---|:---|:---|
| `iku_2015_2018_clean.csv` | `data/raw/intermediate_iku/` | Intermediate |
| `iku_2015_2018_raw.csv` | `data/raw/intermediate_iku/` | Intermediate |
| `iku_2023_page227_table1.csv` | `data/raw/intermediate_iku/` | PDF extract |
| `iku_2024_page128_table1.csv` | `data/raw/intermediate_iku/` | PDF extract |
| `iku_2024_page327_table1.csv` | `data/raw/intermediate_iku/` | PDF extract |
| `iku_2025_page122_table1.csv` | `data/raw/intermediate_iku/` | PDF extract |
| `iku_2025_page319_table1.csv` | `data/raw/intermediate_iku/` | PDF extract |
| `iku_sulawesi_2019_2024_clean.csv` | `data/raw/intermediate_iku/` | Intermediate |
| `iku_sulawesi_2019_2024_final.csv` | `data/raw/intermediate_iku/` | Old final |
| `iku_sulawesi_extracted_slhi.csv` | `data/raw/intermediate_iku/` | Extracted raw |
| `kemenkes_bersih_2014_id.csv` → `2024.csv` | `data/raw/intermediate_kemenkes/` | Per-year (11 files) |
| `bps_kesehatan_provinsi_2014_2024.csv` | `data/raw/intermediate_other/` | Provincial detail |
| `sulut_ika_1_dekade_2016_2024.csv` | `data/raw/intermediate_other/` | Single province |

---

## 🎯 Usage Guidelines

### For Dashboard Development
✅ **USE:** Files in `data/processed/` only  
❌ **DON'T USE:** Files in `data/raw/` (for reproducibility/audit only)

### For Adding New Data
1. Process raw data with scripts in `scripts/`
2. Save intermediate steps to `data/raw/intermediate_*/`
3. Save final cleaned dataset to `data/processed/` with proper naming

### For Data Updates
1. Keep old final file as backup in `data/raw/archive/`
2. Replace with new version in `data/processed/`
3. Update this README with change log

---

## 📊 Column Standards

All final datasets follow these standards:

### Common Columns
- **Tahun** (integer): 2014-2024
- **Provinsi** (string): Official BPS province names
- **Sumber** (string): Data source attribution

### IKU/IKA Columns
- **IKU/IKA** (float): Index value (0-100)
- Range: 70-100 (typical for Sulawesi)
- Categories: 0-50 (Tidak Sehat), 51-70 (Sedang), 71-85 (Baik), 86-100 (Sangat Baik)

### Encoding
- **CSV Format:** UTF-8 with BOM
- **Delimiter:** Comma (`,`)
- **Quote:** Double quotes (`"`) when needed

---

## 📝 Change Log

### 2026-06-14 - Major Reorganization
- ✅ Moved 23 intermediate files to `data/raw/`
- ✅ Renamed 10 final files for consistency
- ✅ Established `{kategori}_{variabel}_{periode}.csv` naming convention
- ✅ Reduced processed folder from 33 files → 10 final datasets

### Previous
- 2026-06-13: IKU 2015-2024 collection completed
- 2026-06-12: IKA, Kesehatan, ESDM data processing
- 2026-06-10: Initial data collection

---

## 🔗 Related Documentation

- `docs/IKU_COLLECTION_FINAL_REPORT.md` - IKU data collection report
- `docs/IKU_DATA_COLLECTION_SUMMARY.md` - IKU methodology
- `docs/DATA_AVAILABILITY_REPORT.md` - Overall data assessment
- `scripts/README.md` - Data processing scripts

---

**Status:** ✅ Clean, organized, production-ready  
**Maintainer:** CELIOS ECC Intelligence System  
**Last Audit:** 2026-06-14
