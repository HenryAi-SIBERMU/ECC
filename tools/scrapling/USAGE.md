# Usage Guide — TanahKita Scraper

> **Panduan lengkap menggunakan scraper tanahkita.id**  
> CELIOS ECC Intelligence System

---

## 📋 Prerequisites

```bash
# 1. Install Python 3.8+
python --version

# 2. Install dependencies
cd tools/scrapling
pip install -r requirements.txt
```

---

## 🚀 Basic Usage

### Scrape Semua Data (580 entries)

```bash
python scrape_tanahkita.py
```

Output:
- `output/tanahkita_konflik.csv`
- `output/tanahkita_konflik.json`

Waktu estimasi: **~2-3 menit** untuk 580 entries (58 halaman @ 10 per page)

---

## 🎯 Advanced Usage

### 1. Test Scrape (1 halaman saja)

```bash
python scrape_tanahkita.py --max-pages 1
```

Akan scrape 10 entries pertama untuk testing.

---

### 2. Custom Output Path

```bash
python scrape_tanahkita.py --output data/konflik_lahan.csv
```

---

### 3. Adjust Rate Limiting

```bash
# Lebih cepat (risky, bisa kena rate limit)
python scrape_tanahkita.py --delay 0.3

# Lebih sopan (slower tapi aman)
python scrape_tanahkita.py --delay 2.0
```

---

### 4. Pause & Resume

```bash
# Scrape dengan checkpoint
python scrape_tanahkita.py --checkpoint output/checkpoint.json

# Jika terinterupsi (Ctrl+C), lanjutkan dengan:
python scrape_tanahkita.py --resume output/checkpoint.json
```

Checkpoint otomatis tersimpan setiap **50 entries**.

---

### 5. Verbose Logging

```bash
python scrape_tanahkita.py --verbose
```

Akan show debug info setiap request.

---

## 📊 Data Structure

Setiap entry konflik berisi:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `nomor` | int | Nomor urut | `6` |
| `tahun` | int | Tahun kejadian | `2025` |
| `judul` | string | Judul konflik | `"Perambahan Kawasan Hutan..."` |
| `deskripsi` | string | Deskripsi singkat | `"Polda Riau memberikan..."` |
| `lokasi` | string | Lokasi konflik | `"Hutan Lindung"` |
| `status` | string | Status badge | `"Hutan Lindung"` |
| `detail_url` | string | URL detail (jika ada) | `"https://tanahkita.id/..."` |
| `scraped_at` | string (ISO) | Timestamp scraping | `"2026-01-15T10:30:45Z"` |

---

## 🔧 Programmatic Usage

### Python Script

```python
from scrape_tanahkita import TanahKitaScraper

# Create scraper
scraper = TanahKitaScraper(
    delay=0.8,
    max_pages=None,  # Scrape all
    verbose=False
)

# Scrape
data = scraper.scrape_all()

# Get data as list of dicts
print(f"Scraped {len(data)} entries")

# Export
scraper.export_csv("output/konflik.csv")
scraper.export_json("output/konflik.json")
```

### Pandas Integration

```python
import pandas as pd
from scrape_tanahkita import TanahKitaScraper

scraper = TanahKitaScraper()
data = scraper.scrape_all()

# Convert to DataFrame
df = pd.DataFrame(data)

# Analyze
print(df.info())
print(df.describe())

# Filter by year
df_2024 = df[df['tahun'] == 2024]

# Export to Excel
df.to_excel("output/analisis_konflik.xlsx", index=False)
```

---

## 📈 Performance Tuning

### Rows Per Page

Default: 10 rows/page → butuh 58 requests untuk 580 entries.

**Optimasi:** Coba ubah `rows_per_page` di `config.yaml`:

```yaml
tanahkita:
  rows_per_page: 50  # Atau 100
```

Jika website support, ini akan reduce total requests:
- 50 rows/page → 12 requests
- 100 rows/page → 6 requests

**Test dulu** dengan `--max-pages 1` untuk pastikan website support!

---

## 🐛 Troubleshooting

### Error: "No table found on page X"

**Penyebab:** Website berubah struktur atau pagination salah.

**Solusi:**
1. Buka browser, kunjungi halaman tsb manual
2. Inspect element table
3. Update selector di `scrape_tanahkita.py` jika perlu

---

### Error: Connection Timeout

**Penyebab:** Network lambat atau server sibuk.

**Solusi:**
```bash
# Tingkatkan timeout di config.yaml
timeout: 60

# Atau via CLI (future feature)
python scrape_tanahkita.py --timeout 60
```

---

### Error: 429 Too Many Requests

**Penyebab:** Scrape terlalu cepat, kena rate limit.

**Solusi:**
```bash
# Tingkatkan delay
python scrape_tanahkita.py --delay 2.0
```

---

### Data Incomplete / Missing Fields

**Penyebab:** HTML structure berbeda dari expected.

**Solusi:**
1. Run dengan `--verbose` untuk debug
2. Check raw HTML: tambahkan `save_html: true` di config
3. Update parsing logic di `_parse_table_row()`

---

## 📦 Output Format Examples

### CSV Format

```csv
nomor,tahun,judul,deskripsi,lokasi,status,detail_url,scraped_at
6,2025,Perambahan Kawasan Hutan...,Polda Riau memberikan...,Hutan Lindung,Hutan Lindung,https://tanahkita.id/...,2026-01-15T10:30:45Z
```

### JSON Format

```json
[
  {
    "nomor": 6,
    "tahun": 2025,
    "judul": "Perambahan Kawasan Hutan...",
    "deskripsi": "Polda Riau memberikan...",
    "lokasi": "Hutan Lindung",
    "status": "Hutan Lindung",
    "detail_url": "https://tanahkita.id/...",
    "scraped_at": "2026-01-15T10:30:45Z"
  }
]
```

---

## 🔐 Ethical Scraping

### Best Practices

✅ **DO:**
- Use reasonable delays (default 0.8s)
- Respect rate limits
- Scrape during off-peak hours
- Provide informative User-Agent
- Cache results (jangan scrape ulang tanpa perlu)

❌ **DON'T:**
- Scrape aggressively (no delay)
- Run parallel scrapers
- Scrape private/auth-required data
- Violate ToS

### User-Agent

Default User-Agent diset di `config.yaml`:

```yaml
user_agent: "CELIOS-ECC-Research/1.0 (Academic Research; Contact: research@celios.edu)"
```

Ini memberi identifikasi jelas bahwa scraping untuk riset akademik.

---

## 📝 Next Steps

Setelah scraping selesai:

1. **Data Cleaning**
   - Check missing values
   - Normalize text (lowercase, trim)
   - Extract structured info dari deskripsi

2. **EDA (Exploratory Data Analysis)**
   - Distribusi per tahun
   - Top lokasi konflik
   - Analisis status

3. **Integration ke ECC System**
   - Import ke database
   - Link dengan data BPS/KLHK lain
   - Visualisasi spatial

---

*Panduan ini akan diupdate seiring development.*  
*CELIOS ECC Intelligence System — Januar 2026*
