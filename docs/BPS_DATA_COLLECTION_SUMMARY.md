# BPS Data Collection - Summary & Panduan Lengkap

> **CELIOS ECC Intelligence System**  
> **Created:** 9 Juni 2026  
> **Status:** Ready for Manual Collection

---

## 📊 Executive Summary

Setelah investigation mendalam terhadap BPS API dan website scraping, **kesimpulan:**

### ✅ What Works
- ✅ **BPS Website accessible** - Semua URL provinsi dapat diakses
- ✅ **Data tersedia** - PAD dan Ekspor data ada di website
- ✅ **Manual download feasible** - Form interaktif berfungsi normal di browser

### ❌ What Doesn't Work
- ❌ **BPS API limited** - Banyak table metadata listed tapi data `"list-not-available"`
- ❌ **Automated scraping blocked** - **Cloudflare Turnstile** protection aktif
- ❌ **JavaScript-heavy forms** - Data dimuat asinkron, sulit di-automate

### 💡 Solution
**MANUAL DOWNLOAD + AUTOMATED PROCESSING**
1. User download manual via browser (bypass Cloudflare)
2. Script otomatis untuk cleaning + consolidation
3. Total time: ~1.5-2 jam untuk semua data

---

## 🎯 Data Target

### 1. PAD (Pendapatan Asli Daerah) - 6 Provinsi Sulawesi

| Provinsi | Kode | URL | Periode |
|----------|------|-----|---------|
| Sulawesi Utara | 7100 | [Query Builder](https://sulut.bps.go.id/id/query-builder) | 2016-2024 |
| Sulawesi Tengah | 7200 | [Query Builder](https://sulteng.bps.go.id/id/query-builder) | 2016-2024 |
| Sulawesi Selatan | 7300 | [Query Builder](https://sulsel.bps.go.id/id/query-builder) | 2016-2024 |
| Sulawesi Tenggara | 7400 | [Query Builder](https://sultra.bps.go.id/id/query-builder) | 2016-2024 |
| Gorontalo | 7500 | [Query Builder](https://gorontalo.bps.go.id/id/query-builder) | 2016-2024 |
| Sulawesi Barat | 7600 | [Query Builder](https://sulbar.bps.go.id/id/query-builder) | 2016-2024 |

**Tabel Target:**
- Realisasi Pendapatan dan Belanja Pemerintah Kabupaten/Kota
- Realisasi Pendapatan Asli Daerah (PAD)
- APBD Kabupaten/Kota

### 2. Ekspor Nasional

| Data | URL | Periode |
|------|-----|---------|
| Ekspor Nasional (HS 2 Digit) | [BPS Exim](https://www.bps.go.id/id/exim) | 2016-2024 |
| Ekspor per Pelabuhan | [BPS Exim](https://www.bps.go.id/id/exim) | 2016-2024 |
| Ekspor per Negara Tujuan | [BPS Exim](https://www.bps.go.id/id/exim) | 2016-2024 |

**Kode HS Relevan:**
- 03 - Ikan dan Udang
- 08 - Buah-buahan
- 09 - Kopi, Teh, Rempah
- 15 - Minyak Nabati
- 27 - Bahan Bakar Mineral
- 44 - Kayu dan Produk Kayu
- 72 - Besi dan Baja

---

## 📖 Panduan Download (Quick Reference)

### A. PAD Data (Per Provinsi)

**Panduan Lengkap:** `tools/scrapling/bps_eksporpad/PANDUAN_DOWNLOAD_MANUAL_PAD.md`

**Quick Steps:**
1. Buka URL query-builder provinsi
2. Tutup popup (tombol "Tutup")
3. Pilih:
   - Kategori Subjek: **Keuangan Daerah**
   - Subjek: **Keuangan Pemerintah Daerah**
   - Tabel: **Realisasi Pendapatan...**
   - Tahun: **2016-2024 (semua)**
4. Klik **"Tambah"** → **"Submit"**
5. Download CSV/Excel
6. Save as: `pad_{kode}_{provinsi}_2016-2024.csv`

**Output Folder:**
```
tools/scrapling/bps_eksporpad/downloads/
```

**Estimasi:** 45-60 menit untuk 6 provinsi

### B. Ekspor Nasional

**Panduan Lengkap:** `tools/bpsapi/output/PANDUAN_DOWNLOAD_EKSPOR_NASIONAL.md`

**Quick Steps:**
1. Buka https://www.bps.go.id/id/exim
2. Pilih:
   - Tipe: **Ekspor**
   - Agregasi: **Menurut Kode HS** (HS 2 Digit)
   - Tahun: **2016-2024**
   - Kode HS: Pilih yang relevan (lihat list di atas)
3. Klik **"Buat Tabel"**
4. Download CSV/Excel
5. Save as: `ekspor_nasional_hs2digit_2016-2024.csv`

**Output Folder:**
```
tools/bpsapi/output/ekspor/
```

**Estimasi:** 30 menit untuk 3 datasets

---

## 🛠️ Processing Scripts (Coming Next)

Setelah download selesai, data akan diproses dengan scripts:

### 1. PAD Processing
```bash
cd tools/scrapling/bps_eksporpad
python process_pad_downloads.py
```

**Tasks:**
- Clean column names
- Standardize formats
- Remove empty rows
- Consolidate 6 provinces
- Output: `pad_sulawesi_consolidated_2016-2024.csv`

### 2. Ekspor Processing
```bash
cd tools/bpsapi
python process_ekspor_downloads.py
```

**Tasks:**
- Parse HS codes
- Map sector names
- Aggregate by year
- Calculate growth rates
- Output: `ekspor_nasional_processed_2016-2024.csv`

---

## 📁 File Structure

```
4. Celios2/
├── tools/
│   ├── scrapling/
│   │   └── bps_eksporpad/
│   │       ├── PANDUAN_DOWNLOAD_MANUAL_PAD.md ✅
│   │       ├── downloads/              (User puts downloaded files here)
│   │       │   ├── pad_7100_sulawesi_utara_2016-2024.csv
│   │       │   ├── pad_7200_sulawesi_tengah_2016-2024.csv
│   │       │   ├── pad_7300_sulawesi_selatan_2016-2024.csv
│   │       │   ├── pad_7400_sulawesi_tenggara_2016-2024.csv
│   │       │   ├── pad_7500_gorontalo_2016-2024.csv
│   │       │   └── pad_7600_sulawesi_barat_2016-2024.csv
│   │       ├── process_pad_downloads.py  (To be created)
│   │       └── output/                   (Processed results)
│   │           └── pad_sulawesi_consolidated_2016-2024.csv
│   │
│   └── bpsapi/
│       ├── output/
│       │   ├── PANDUAN_DOWNLOAD_EKSPOR_NASIONAL.md ✅
│       │   └── ekspor/               (User puts downloaded files here)
│       │       ├── ekspor_nasional_hs2digit_2016-2024.csv
│       │       ├── ekspor_nasional_pelabuhan_2016-2024.csv
│       │       └── ekspor_nasional_negara_2016-2024.csv
│       ├── process_ekspor_downloads.py   (To be created)
│       └── output/                       (Processed results)
│           └── ekspor_nasional_processed_2016-2024.csv
│
└── BPS_DATA_COLLECTION_SUMMARY.md ✅ (This file)
```

---

## ⏱️ Timeline

### Phase 1: Manual Download (User Task)
- **PAD**: 45-60 minutes
- **Ekspor**: 30 minutes
- **Total**: ~1.5-2 hours

### Phase 2: Automated Processing (Script)
- **Development**: 2-3 hours (create processing scripts)
- **Execution**: 5-10 minutes (run scripts)
- **Total**: Instant once scripts ready

### Total Project Time
- **With scripts**: 2 hours (mostly manual download)
- **Without scripts**: Manual processing would take 4-6 hours

---

## 🔧 Technical Details

### Why Automated Scraping Failed

1. **Cloudflare Turnstile**
   - Anti-bot protection aktif
   - Blocked Playwright/Selenium
   - Bahkan StealthyFetcher tidak bisa bypass fully

2. **JavaScript-Heavy Forms**
   - Data dimuat async after page load
   - Form dropdown populate via AJAX
   - No direct API endpoint to call

3. **BPS API Limitations**
   - Metadata lists 30,613 tables
   - But many return `"list-not-available"`
   - PAD & Ekspor termasuk yang not accessible

### Why Manual + Processing Works

1. **Human browser** = No Cloudflare blocking
2. **Interactive form** = Works perfectly in browser
3. **Standardized output** = CSV/Excel easy to process
4. **One-time effort** = Download once, process many times

---

## ✅ Deliverables Checklist

### Documentation
- [x] PAD Download Panduan (`PANDUAN_DOWNLOAD_MANUAL_PAD.md`)
- [x] Ekspor Download Panduan (`PANDUAN_DOWNLOAD_EKSPOR_NASIONAL.md`)
- [x] Summary Document (this file)
- [ ] Processing Scripts (Next step)

### Code
- [x] Investigation tools (bps_client.py, deep_search.py)
- [x] Scraping attempts (scrape_pad_*.py, scrape_ekspor_*.py)
- [x] Documentation of limitations
- [ ] PAD processing script
- [ ] Ekspor processing script

### Data
- [ ] PAD downloads (6 files) - **USER TASK**
- [ ] Ekspor downloads (3 files) - **USER TASK**
- [ ] Processed PAD dataset - **AUTOMATED**
- [ ] Processed Ekspor dataset - **AUTOMATED**

---

## 🎯 Next Steps

### For User (You)

**Step 1: Download PAD Data**
1. Follow: `tools/scrapling/bps_eksporpad/PANDUAN_DOWNLOAD_MANUAL_PAD.md`
2. Download 6 files (one per province)
3. Place in: `tools/scrapling/bps_eksporpad/downloads/`
4. Estimated time: 45-60 minutes

**Step 2: Download Ekspor Data**
1. Follow: `tools/bpsapi/output/PANDUAN_DOWNLOAD_EKSPOR_NASIONAL.md`
2. Download 3 datasets (HS2, Pelabuhan, Negara)
3. Place in: `tools/bpsapi/output/ekspor/`
4. Estimated time: 30 minutes

**Step 3: Notify When Done**
- Tell me "downloads completed"
- I'll create processing scripts
- Run scripts to get consolidated data

### For Agent (Next)

**Step 1: Create PAD Processing Script**
- Read all 6 downloaded files
- Standardize columns
- Consolidate into single dataset
- Add province codes

**Step 2: Create Ekspor Processing Script**
- Parse HS codes and descriptions
- Aggregate by year and sector
- Calculate growth rates
- Create time series

**Step 3: Data Validation**
- Check for missing values
- Validate year ranges
- Flag outliers
- Generate summary statistics

---

## 📞 Support

**Questions during download?**
- Check troubleshooting section in panduan files
- BPS Call Center: 082373736742
- Email: bps@bps.go.id

**Technical issues?**
- Check this summary document
- Review investigation files in `tools/bpsapi/`
- Consult `DATA_AVAILABILITY_REPORT.md`

---

## 📝 Notes

### Lessons Learned
1. ✅ Always test website accessibility first
2. ✅ Check for anti-bot protection early
3. ✅ Manual + automation hybrid works best
4. ✅ Good documentation saves time

### Future Improvements
1. Monitor if BPS removes Cloudflare
2. Check for new API endpoints
3. Consider Kemenkeu DJPK as alternative source for PAD
4. Track BPS publications for historical data

---

*Document created: 9 Juni 2026*  
*Last updated: 9 Juni 2026*  
*CELIOS ECC Intelligence System*
