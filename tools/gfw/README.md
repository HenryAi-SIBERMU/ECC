# Global Forest Watch (GFW) API Tools

Tools untuk mengakses data deforestasi dari Global Forest Watch API.

## 📋 Overview

Global Forest Watch menyediakan dataset global forest cover change berbasis satelit dengan resolusi 30m. Data bersumber dari Hansen et al. (2013) yang dipublikasikan di Science journal.

**Data Source:** Hansen, M. C., et al. (2013). High-resolution global maps of 21st-century forest cover change. *Science*, 342(6160), 850-853.

**Coverage:** 2001-2023 (updated annually)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install requests pandas
```

### 2. Run Data Fetch

```bash
python tools/gfw/fetch_sulawesi_deforestation.py
```

**Output:** `data/raw/gfw/sulawesi_deforestation_2016_2024.csv`

## 📊 Expected Output Schema

```csv
province,province_en,admin1_code,bps_code,year,tree_cover_loss_ha,tree_cover_pct,data_source,confidence_level,extraction_date
Sulawesi Utara,North Sulawesi,IDN.31,71,2016,12500.5,65.3,GFW_Hansen,High,2026-06-14
Sulawesi Tengah,Central Sulawesi,IDN.29,72,2016,15300.2,58.7,GFW_Hansen,High,2026-06-14
...
```

## 🔧 API Configuration

### API Key (Optional)

GFW public datasets tidak memerlukan API key. Namun untuk rate limits lebih tinggi atau akses advanced features:

1. Register di: https://data.globalforestwatch.org
2. Generate API key
3. Set environment variable:
   ```bash
   export GFW_API_KEY="your_key_here"
   ```

### Admin Codes

Kode admin untuk provinsi Sulawesi:

| Province | Admin Code | BPS Code |
|----------|-----------|----------|
| Sulawesi Utara | IDN.31 | 71 |
| Sulawesi Tengah | IDN.29 | 72 |
| Sulawesi Selatan | IDN.30 | 73 |
| Sulawesi Tenggara | IDN.32 | 74 |
| Gorontalo | IDN.11 | 75 |
| Sulawesi Barat | IDN.33 | 76 |

## 📖 API Documentation

### GFW API v1 Endpoints

**Base URL:** `https://production-api.globalforestwatch.org`

#### UMD Loss/Gain
```
GET /v1/umd-loss-gain
Parameters:
  - iso: Country code (e.g., IDN)
  - admin1: Province code (e.g., 30 for Sulsel)
  - admin2: Regency code (optional)
  - thresh: Tree cover threshold % (default: 30)
  - period: Date range (e.g., 2016-01-01,2024-12-31)
```

#### GLAD Alerts
```
GET /v1/glad-alerts
Parameters:
  - iso: Country code
  - admin1: Province code
  - dateRange: Date range for alerts
```

### Alternative: GFW Data API v2/v3

**Base URL:** `https://data-api.globalforestwatch.org`

More advanced features, better untuk custom geometry analysis.

## 🛠️ Troubleshooting

### Issue: No data returned

**Cause:** Admin codes might need adjustment.

**Solution:** 
1. Check GFW country/admin boundaries: https://www.globalforestwatch.org
2. Verify admin codes dengan GFW metadata API
3. Try different admin code formats (numeric vs full code)

### Issue: Rate limiting

**Cause:** Too many API calls.

**Solution:**
- Add delays between calls (implemented in `gfw_api_client.py`)
- Register for API key untuk higher limits
- Use bulk download features jika tersedia

### Issue: Response structure changed

**Cause:** GFW API updates.

**Solution:**
- Print raw response: `print(json.dumps(response, indent=2))`
- Check API changelog: https://data.globalforestwatch.org/documents
- Adjust parsing logic in `gfw_api_client.py`

## 📚 References

- GFW Website: https://www.globalforestwatch.org
- API Docs: https://data.globalforestwatch.org/documents
- Hansen Dataset: https://earthenginepartners.appspot.com/science-2013-global-forest
- GitHub: https://github.com/wri/gfw-api

## 🔄 Next Steps

After fetching GFW data:

1. **Validate:** Check output CSV untuk completeness
2. **Cross-reference:** Compare dengan SLHI data (`tools/pdf_extraction/extract_deforestasi_slhi.py`)
3. **Consolidate:** Run `scripts/consolidate_deforestasi.py` untuk merge sources
4. **Analysis:** Use for Checkpoint 4 - Environmental Quality Dashboard

---

**Created:** 14 Juni 2026  
**Author:** CELIOS Research Division  
**Status:** ✅ Ready for execution
