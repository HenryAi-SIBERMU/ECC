# ✅ INSTRUKSI DOWNLOAD DATA BPS - Ready to Use

> **CELIOS ECC Intelligence System**  
> **Status:** All tools & panduan ready  
> **Estimasi waktu:** 1.5-2 jam (mostly manual download)

---

## 🎯 Target Data

### 1. PAD Sulawesi (6 Provinsi)
- **Periode:** 2016-2024
- **Coverage:** Sulawesi Utara, Tengah, Selatan, Tenggara, Gorontalo, Barat
- **Format:** CSV/Excel per provinsi
- **Estimasi:** 45-60 menit

### 2. Ekspor Nasional
- **Periode:** 2016-2024
- **Coverage:** HS 2 Digit, Per Pelabuhan, Per Negara
- **Format:** CSV/Excel
- **Estimasi:** 30 menit

---

## 📖 Step-by-Step

### STEP 1: Download PAD Data

**Panduan Lengkap:**
```
tools/scrapling/bps_eksporpad/PANDUAN_DOWNLOAD_MANUAL_PAD.md
```

**Quick Summary:**
1. Buka URL per provinsi (6 URL di panduan)
2. Pilih:
   - Kategori: Keuangan Daerah
   - Subjek: Keuangan Pemerintah Daerah
   - Tabel: Realisasi Pendapatan...
   - Tahun: 2016-2024 (semua)
3. Download CSV
4. Save ke: `tools/scrapling/bps_eksporpad/downloads/`
5. Naming: `pad_7300_sulawesi_selatan_2016-2024.csv`

**URLs:**
- Sulut: https://sulut.bps.go.id/id/query-builder
- Sulteng: https://sulteng.bps.go.id/id/query-builder
- Sulsel: https://sulsel.bps.go.id/id/query-builder
- Sultra: https://sultra.bps.go.id/id/query-builder
- Gorontalo: https://gorontalo.bps.go.id/id/query-builder
- Sulbar: https://sulbar.bps.go.id/id/query-builder

### STEP 2: Download Ekspor Data

**Panduan Lengkap:**
```
tools/bpsapi/output/PANDUAN_DOWNLOAD_EKSPOR_NASIONAL.md
```

**Quick Summary:**
1. Buka: https://www.bps.go.id/id/exim
2. Pilih:
   - Tipe: Ekspor
   - Agregasi: Menurut Kode HS (HS 2 Digit)
   - Tahun: 2016-2024
   - Kode HS: 03, 08, 09, 15, 27, 44, 72 (relevant sectors)
3. Download CSV
4. Save ke: `tools/bpsapi/output/ekspor/`
5. Naming: `ekspor_nasional_hs2digit_2016-2024.csv`

**Repeat untuk 3 agregasi:**
- HS 2 Digit
- Per Pelabuhan
- Per Negara

### STEP 3: Process Data (Otomatis)

**PAD Processing:**
```bash
cd tools/scrapling/bps_eksporpad
python process_pad_downloads.py
```

**Ekspor Processing:**
```bash
cd tools/bpsapi
python process_ekspor_downloads.py
```

**Output:**
- `tools/scrapling/bps_eksporpad/output/pad_sulawesi_consolidated_*.csv`
- `tools/bpsapi/output/ekspor_nasional_processed_*.csv`

---

## 📁 File Locations

### Input (You Download)
```
tools/
├── scrapling/bps_eksporpad/downloads/
│   ├── pad_7100_sulawesi_utara_2016-2024.csv      ⬅️ You create
│   ├── pad_7200_sulawesi_tengah_2016-2024.csv     ⬅️ You create
│   ├── pad_7300_sulawesi_selatan_2016-2024.csv    ⬅️ You create
│   ├── pad_7400_sulawesi_tenggara_2016-2024.csv   ⬅️ You create
│   ├── pad_7500_gorontalo_2016-2024.csv           ⬅️ You create
│   └── pad_7600_sulawesi_barat_2016-2024.csv      ⬅️ You create
│
└── bpsapi/output/ekspor/
    ├── ekspor_nasional_hs2digit_2016-2024.csv     ⬅️ You create
    ├── ekspor_nasional_pelabuhan_2016-2024.csv    ⬅️ You create
    └── ekspor_nasional_negara_2016-2024.csv       ⬅️ You create
```

### Output (Script Creates)
```
tools/
├── scrapling/bps_eksporpad/output/
│   └── pad_sulawesi_consolidated_*.csv            ⬅️ Script creates
│
└── bpsapi/output/
    └── ekspor_nasional_processed_*.csv            ⬅️ Script creates
```

---

## ✅ Checklist

### PAD Downloads (6 files)
```
☐ Sulawesi Utara (7100)
☐ Sulawesi Tengah (7200)
☐ Sulawesi Selatan (7300)
☐ Sulawesi Tenggara (7400)
☐ Gorontalo (7500)
☐ Sulawesi Barat (7600)
```

### Ekspor Downloads (3 files)
```
☐ Ekspor HS 2 Digit
☐ Ekspor Per Pelabuhan
☐ Ekspor Per Negara
```

### Processing
```
☐ Run PAD processing script
☐ Run Ekspor processing script
☐ Verify output files
☐ Check data quality
```

---

## 🆘 Troubleshooting

### ❌ Form tidak muncul
- Refresh page (F5)
- Clear cache (Ctrl+Shift+Del)
- Try different browser

### ❌ Data tidak lengkap
- Normal - not all years available
- Download what's available
- Note missing years

### ❌ File corrupt
- Re-download with different format (CSV ↔ Excel)
- Check file size (should be > 1 KB)

### ❌ Processing script error
- Check file naming matches pattern
- Verify files in correct folder
- Check file encoding (UTF-8 or ANSI)

---

## 📊 Expected Results

### PAD Dataset
- **Rows:** ~1,000-5,000 (depends on granularity)
- **Columns:** ~15-30
- **Years:** 2016-2024 (where available)
- **Provinces:** 6
- **Format:** Consolidated CSV

### Ekspor Dataset
- **Rows:** ~500-2,000 per agregasi
- **Columns:** ~10-20
- **Years:** 2016-2024
- **Coverage:** National
- **Format:** Processed CSV with sectors

---

## 🎯 Next Steps After Download

1. ✅ **Verify all files downloaded** (9 total)
2. ✅ **Check file sizes** (should be reasonable, not 0 KB)
3. ✅ **Run processing scripts**
4. ✅ **Review consolidated datasets**
5. ✅ **Start ECC model integration**

---

## 📚 Documentation Reference

| Document | Purpose | Location |
|----------|---------|----------|
| **Main Summary** | Overview & strategy | `tools/BPS_DATA_COLLECTION_SUMMARY.md` |
| **PAD Panduan** | Step-by-step PAD | `tools/scrapling/bps_eksporpad/PANDUAN_DOWNLOAD_MANUAL_PAD.md` |
| **Ekspor Panduan** | Step-by-step Ekspor | `tools/bpsapi/output/PANDUAN_DOWNLOAD_EKSPOR_NASIONAL.md` |
| **PAD README** | Quick reference | `tools/scrapling/bps_eksporpad/README.md` |
| **Investigation** | Technical details | `tools/bpsapi/DATA_AVAILABILITY_REPORT.md` |

---

## ⏱️ Timeline Summary

| Phase | Task | Time |
|-------|------|------|
| 1 | Download PAD (6 provinces) | 45-60 min |
| 2 | Download Ekspor (3 datasets) | 30 min |
| 3 | Run processing scripts | 5-10 min |
| **Total** | **Complete workflow** | **~2 hours** |

---

## 💡 Tips for Efficiency

1. **Open multiple tabs** - Download 2-3 provinces parallel
2. **Use keyboard shortcuts** - Tab + Space for navigation
3. **Screenshot each step** - Documentation for reference
4. **Note any anomalies** - Missing years, weird values
5. **Verify before processing** - Check all 9 files present

---

## ✅ You're Ready!

**Everything is prepared:**
- ✅ Comprehensive guides created
- ✅ Processing scripts ready
- ✅ Folder structure set up
- ✅ Documentation complete

**Start with:** `PANDUAN_DOWNLOAD_MANUAL_PAD.md`

**Questions?** Check troubleshooting sections in panduan files

---

*Created: 9 Juni 2026*  
*CELIOS ECC Intelligence System*  
*Ready for execution* 🚀
