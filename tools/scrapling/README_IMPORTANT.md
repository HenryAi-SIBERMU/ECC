# ⚠️ PENTING — URL Verification Needed

## Status Tool

✅ **Virtual environment**: Setup complete  
✅ **Dependencies**: Installed (scrapling 0.4.9, pandas, bs4, dll.)  
✅ **Scraper code**: Ready  
⚠️ **Target URL**: **PERLU VERIFIKASI**

---

## Masalah

URL `https://tanahkita.id/data-konflik` dari screenshot **returns 404 Not Found**.

Kemungkinan penyebab:
1. Website berubah struktur
2. Perlu authentikasi/login dulu
3. URL berbeda dari yang terlihat di screenshot
4. Data di-load via JavaScript (bukan HTML statis)

---

## Next Steps

### Option 1: Manual URL Verification (RECOMMENDED)

1. **Buka browser**, kunjungi website tanahkita.id
2. **Navigate** ke halaman data konflik yang ada tabelnya
3. **Copy exact URL** dari address bar
4. **Update** `config.yaml`:
   ```yaml
   tanahkita:
     base_url: "URL_YANG_BENAR"
   ```
5. **Re-run test**:
   ```bash
   python scrape_tanahkita.py --max-pages 1 --verbose
   ```

---

### Option 2: Inspect dengan Browser DevTools

1. Buka halaman dengan tabel konflik
2. Open DevTools (F12)
3. Go to **Network tab**
4. Refresh page
5. Cari request yang return data tabel:
   - **Jika HTML** → copy URL-nya
   - **Jika JSON/API** → lebih bagus! Copy API endpoint-nya

**Jika API endpoint:**
```yaml
tanahkita:
  api_endpoint: "https://tanahkita.id/api/konflik?page=1&limit=100"
  is_api: true  # Flag untuk logic berbeda
```

Scraper perlu dimodifikasi untuk handle JSON response.

---

### Option 3: Use DynamicFetcher (JavaScript-heavy site)

Jika data di-load via JavaScript (lazy load), perlu browser automation:

```bash
# Install playwright
pip install "scrapling[fetchers]"
scrapling install  # Download browser
```

Update scraper menggunakan `DynamicFetcher` instead of `Fetcher`.

---

## Testing URLs Found

Dari homepage inspection, ada link ke:
- `/data/wilayah_kelola/` — Data wilayah kelola per provinsi
- Tapi **bukan** data konflik

**Kemungkinan**:
- Data konflik ada di navigation menu yang tidak ter-scrape
- Atau di subdomain/path berbeda

---

## Workaround: Generic Table Scraper

Jika Anda bisa berikan **correct URL**, scraper sudah siap.

**Atau**, saya bisa buat **generic table scraper** yang:
1. Input: URL apapun dengan table HTML
2. Output: Scrape semua table dalam format CSV/JSON
3. Anda tinggal jalankan dengan URL yang benar

---

## Tools Sudah Siap

```
tools/scrapling/
├── ✅ venv/                    # Virtual environment
├── ✅ scraper_base.py          # Base class
├── ✅ scrape_tanahkita.py      # Main scraper
├── ✅ utils/                   # Helpers
├── ✅ inspect_site.py          # URL inspector
└── ⚠️  config.yaml             # NEED CORRECT URL
```

Semua dependency sudah installed, tinggal fix URL saja.

---

## Action Items

**Untuk melanjutkan, Anda perlu:**

1. ✅ Confirm exact URL dari browser (manual check)
2. ⏭️ Update `config.yaml` dengan URL yang benar
3. ⏭️ Test scraper dengan `--max-pages 1`
4. ⏭️ Jika berhasil, full scrape 580 entries

**Atau**, share screenshot yang lebih jelas (termasuk address bar penuh) dan saya akan adjust scraper accordingly.

---

*Tools ready, waiting for correct URL verification.*  
*CELIOS ECC Intelligence System — Juni 2026*
