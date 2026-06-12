# Scrapling Tools — CELIOS ECC Data Scraper

> **Tool scraping adaptif untuk akuisisi data konflik lahan Indonesia**  
> Dibuat untuk proyek CELIOS ECC Intelligence System

---

## 📦 Isi Folder

```
scrapling/
├── README.md                    # Dokumentasi ini
├── requirements.txt             # Dependencies Python
├── config.yaml                  # Konfigurasi scraper
├── scrape_tanahkita.py         # Scraper untuk tanahkita.id
├── scraper_base.py             # Base class untuk scraper lain
├── utils/
│   ├── __init__.py
│   ├── parser.py               # HTML parsing helpers
│   └── exporter.py             # Export ke CSV/JSON/Excel
└── output/                     # Hasil scraping (gitignored)
    ├── tanahkita_konflik.csv
    └── tanahkita_konflik.json
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd tools/scrapling
pip install -r requirements.txt
```

### 2. Run Scraper

```bash
# Scrape semua 580 entries dari tanahkita.id
python scrape_tanahkita.py

# Dengan opsi kustom
python scrape_tanahkita.py --max-pages 10 --delay 1.0 --output output/test.csv
```

### 3. Output

Hasil scraping otomatis tersimpan di:
- `output/tanahkita_konflik.csv` — Format CSV untuk Excel/Pandas
- `output/tanahkita_konflik.json` — Format JSON untuk pipeline API

---

## 🛠️ Penggunaan Lanjutan

### Scrape dengan Checkpoint (Pause/Resume)

```bash
# Scraping akan otomatis menyimpan checkpoint setiap 50 entries
python scrape_tanahkita.py --checkpoint output/checkpoint.json

# Jika terinterupsi, jalankan lagi untuk melanjutkan:
python scrape_tanahkita.py --resume output/checkpoint.json
```

### Custom Configuration

Edit `config.yaml`:

```yaml
tanahkita:
  base_url: "https://tanahkita.id/data-konflik"
  delay: 0.8              # Delay antar request (detik)
  max_retries: 3          # Retry jika gagal
  timeout: 30             # Timeout per request (detik)
  rows_per_page: 100      # Coba ubah jika website support
  user_agent: "Mozilla/5.0 ..."
```

### Programmatic Usage

```python
from scrape_tanahkita import TanahKitaScraper

scraper = TanahKitaScraper(delay=1.0)
data = scraper.scrape_all()  # Returns list of dicts

# Export
scraper.export_csv("output/konflik.csv")
scraper.export_json("output/konflik.json")

# Atau langsung ke Pandas
import pandas as pd
df = pd.DataFrame(data)
df.to_excel("output/konflik.xlsx", index=False)
```

---

## 📊 Data Structure

Setiap entry konflik akan berisi:

```json
{
  "nomor": 6,
  "tahun": 2025,
  "judul": "Perambahan Kawasan Hutan Polda Riau...",
  "deskripsi": "Polda Riau memberikan kasus...",
  "lokasi": "Hutan Lindung",
  "status": "Hutan Lindung",
  "detail_url": "https://tanahkita.id/data-konflik/detail/6",
  "scraped_at": "2026-01-15T10:30:45Z"
}
```

---

## 🔧 Troubleshooting

### Error: Connection Timeout

```bash
# Tingkatkan timeout di config.yaml
timeout: 60

# Atau via CLI
python scrape_tanahkita.py --timeout 60
```

### Error: Anti-bot / Cloudflare

```bash
# Gunakan StealthyFetcher mode
python scrape_tanahkita.py --stealth
```

### Error: Rate Limited (429)

```bash
# Tingkatkan delay antar request
python scrape_tanahkita.py --delay 2.0
```

---

## 🧪 Testing

```bash
# Test scrape 1 halaman saja (10 entries)
python scrape_tanahkita.py --max-pages 1

# Test dengan verbose logging
python scrape_tanahkita.py --verbose
```

---

## 📝 Catatan Etis

- ✅ Data tanahkita.id adalah **data publik** untuk kepentingan riset
- ✅ Scraper menggunakan **rate limiting** sopan (default 0.8s delay)
- ✅ Scraper mengirim **User-Agent yang jelas** mengidentifikasi peneliti
- ⚠️ **Jangan** scrape terlalu agresif (bisa overload server mereka)
- ⚠️ **Hormati robots.txt** jika ada

---

## 🔄 Update Log

- **v1.0** (Jan 2026) — Initial release, support tanahkita.id
- **v1.1** (TBD) — Tambahkan scraper untuk SIPSN KLHK
- **v1.2** (TBD) — Tambahkan scraper untuk BPS WebAPI

---

*Dibuat untuk CELIOS ECC Intelligence System*  
*MIT License — Gunakan dengan bertanggung jawab*
