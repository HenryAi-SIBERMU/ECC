# BPS PAD Data Collection - Sulawesi

> **Status:** Ready for manual download  
> **Cloudflare protection:** ✅ Detected and documented

---

## Quick Start

### 1. Download Data (Manual)
Follow: **[PANDUAN_DOWNLOAD_MANUAL_PAD.md](PANDUAN_DOWNLOAD_MANUAL_PAD.md)**

**Time:** ~45-60 minutes for 6 provinces

### 2. Save Files
Place downloaded CSV files in:
```
downloads/
├── pad_7100_sulawesi_utara_2016-2024.csv
├── pad_7200_sulawesi_tengah_2016-2024.csv
├── pad_7300_sulawesi_selatan_2016-2024.csv
├── pad_7400_sulawesi_tenggara_2016-2024.csv
├── pad_7500_gorontalo_2016-2024.csv
└── pad_7600_sulawesi_barat_2016-2024.csv
```

### 3. Process Data (Automated)
```bash
python process_pad_downloads.py
```
**Output:** `output/pad_sulawesi_consolidated_2016-2024.csv`

---

## Files in This Folder

| File | Purpose | Status |
|------|---------|--------|
| `PANDUAN_DOWNLOAD_MANUAL_PAD.md` | Complete download guide | ✅ Ready |
| `scrape_pad_browser.py` | Browser automation attempt | ❌ Blocked by Cloudflare |
| `scrape_pad_interactive.py` | Playwright automation | ❌ Blocked by Cloudflare |
| `scrape_pad_stealth.py` | Stealth mode test | ⚠️ Partial success |
| `process_pad_downloads.py` | Processing script | 🔜 To be created |
| `downloads/` | User-downloaded files | 📁 Empty (waiting) |
| `output/` | Processed results | 📁 Empty (waiting) |

---

## Why Manual Download?

**Problem:** BPS website uses **Cloudflare Turnstile** protection
- ❌ Blocks automated browsers (Playwright, Selenium)
- ❌ Detects StealthyFetcher
- ❌ JavaScript forms load async (hard to automate)

**Solution:** Manual download via normal browser
- ✅ No Cloudflare blocking
- ✅ Forms work perfectly
- ✅ One-time effort (~1 hour)
- ✅ Automated processing after download

---

## Investigation Summary

**Tools Tested:**
1. `DynamicFetcher` (Scrapling) - ❌ 403 errors
2. `StealthyFetcher` (Scrapling) - ⚠️ Bypassed CF but forms didn't load
3. `Playwright` direct - ❌ Detected by Cloudflare
4. `BPS WebAPI` - ❌ PAD data not accessible

**Conclusion:** Manual download most reliable

---

## Next Steps

1. ✅ Read `PANDUAN_DOWNLOAD_MANUAL_PAD.md`
2. ⏳ Download 6 PAD files (~1 hour)
3. 📁 Place files in `downloads/`
4. 🔜 Wait for `process_pad_downloads.py` script
5. ▶️ Run processing script
6. ✅ Get consolidated dataset

---

## Related Files

- **Main Summary:** `../../BPS_DATA_COLLECTION_SUMMARY.md`
- **Ekspor Guide:** `../../bpsapi/output/PANDUAN_DOWNLOAD_EKSPOR_NASIONAL.md`
- **API Investigation:** `../../bpsapi/DATA_AVAILABILITY_REPORT.md`

---

*Created: 9 Juni 2026 | CELIOS ECC Intelligence System*
