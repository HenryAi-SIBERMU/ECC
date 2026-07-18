# BPS API Client — CELIOS ECC Data Pipeline

> **API client untuk mengakses data BPS (Badan Pusat Statistik) Indonesia**  
> Fokus: Ekspor per Sektor, PAD Kabupaten/Kota Sulawesi 2016-2026

---

## 📦 Overview

Tool ini mengakses **BPS Web API** untuk mendapatkan:
- **Nilai Ekspor per Sektor** (ekonomi regional)
- **PAD per Kabupaten/Kota** (Pendapatan Asli Daerah) fokus Sulawesi
- **Indikator ekonomi lainnya** yang relevan untuk analisis ECC

**Target data**: ±300 baris × 10 tahun (2016-2026)

---

## 🔑 API Key

API Key BPS Anda: `06fd644648629502353deaed29fc6383`

> ⚠️ **JANGAN commit API key ke git!** Sudah ada di `.gitignore`

---

## 🚀 Quick Start

### 1. Setup Virtual Environment

```bash
cd tools/bpsapi
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure API Key

Edit `config.yaml` atau set environment variable:

```bash
set BPS_API_KEY=06fd644648629502353deaed29fc6383
```

### 3. Run Data Fetch

```bash
# Fetch ekspor data
python fetch_ekspor.py --tahun-awal 2016 --tahun-akhir 2026

# Fetch PAD Sulawesi
python fetch_pad_sulawesi.py --tahun-awal 2016 --tahun-akhir 2026

# Fetch all
python fetch_all.py
```

---

## 📊 Data Structure

### Ekspor per Sektor

```python
{
    "tahun": 2023,
    "provinsi": "Sulawesi Selatan",
    "kode_provinsi": "73",
    "sektor": "Pertanian",
    "nilai_ekspor_usd": 1250000000,
    "nilai_ekspor_idr": 18750000000000,
    "perubahan_yoy": 5.2,
    "scraped_at": "2026-06-09T..."
}
```

### PAD per Kabupaten/Kota

```python
{
    "tahun": 2023,
    "provinsi": "Sulawesi Selatan",
    "kabupaten_kota": "Kota Makassar",
    "kode_wilayah": "7371",
    "pad_total": 2500000000000,
    "pajak_daerah": 1800000000000,
    "retribusi_daerah": 400000000000,
    "lain_lain_pad": 300000000000,
    "scraped_at": "2026-06-09T..."
}
```

---

## 🛠️ Features

### ✅ Implemented

- [x] BPS API authentication
- [x] Province/regency code mapping
- [x] Time series data extraction (2016-2026)
- [x] Multi-format export (CSV, JSON, Excel)
- [x] Rate limiting & retry logic
- [x] Data validation & cleaning
- [x] Progress bar & logging

### 🔄 Planned

- [ ] Caching mechanism
- [ ] Incremental updates
- [ ] Data quality checks
- [ ] Integration dengan tools lain (Scrapling, PageIndex)

---

## 📂 Folder Structure

```
bpsapi/
├── README.md                   # Documentation
├── requirements.txt            # Dependencies
├── config.yaml                 # Configuration (gitignored)
├── .env.example                # Environment template
├── .gitignore
├── bps_client.py              # Core API client
├── fetch_ekspor.py            # Ekspor data fetcher
├── fetch_pad_sulawesi.py      # PAD Sulawesi fetcher
├── fetch_all.py               # Batch fetcher
├── utils/
│   ├── __init__.py
│   ├── province_codes.py      # Kode wilayah BPS
│   ├── validators.py          # Data validation
│   └── exporters.py           # Export utilities
├── output/                     # Output data (gitignored)
│   ├── ekspor_2016_2026.csv
│   ├── pad_sulawesi_2016_2026.csv
│   └── metadata.json
└── tests/
    └── test_bps_client.py
```

---

## 🔧 Configuration

### config.yaml

```yaml
bps:
  api_key: "${BPS_API_KEY}"  # From environment
  base_url: "https://webapi.bps.go.id/v1/api"
  timeout: 30
  max_retries: 3
  rate_limit: 1.0  # seconds between requests
  
  # Target regions for Sulawesi
  sulawesi_provinces:
    - code: "71"
      name: "Sulawesi Utara"
    - code: "72"
      name: "Sulawesi Tengah"
    - code: "73"
      name: "Sulawesi Selatan"
    - code: "74"
      name: "Sulawesi Tenggara"
    - code: "75"
      name: "Gorontalo"
    - code: "76"
      name: "Sulawesi Barat"
  
  # Data indicators
  indicators:
    ekspor:
      subject: "ekspor"
      variables: ["nilai_usd", "nilai_idr", "pertumbuhan"]
    pad:
      subject: "pad"
      variables: ["pajak", "retribusi", "lain_lain"]

# Output settings
output:
  dir: "output"
  formats: ["csv", "json", "xlsx"]
  encoding: "utf-8-sig"
```

---

## 📖 BPS API Endpoints

### Base URL
```
https://webapi.bps.go.id/v1/api
```

### Key Endpoints

| Endpoint | Description |
|----------|-------------|
| `/list` | List available datasets |
| `/subject` | Browse by subject/tema |
| `/domain` | Browse by domain/provinsi |
| `/data` | Get actual data |
| `/pressrelease` | Latest press releases |

### Example Request

```bash
curl -X GET "https://webapi.bps.go.id/v1/api/list" \
  -H "key: 06fd644648629502353deaed29fc6383"
```

---

## 🧪 Testing

```bash
# Test API connection
python -c "from bps_client import BPSClient; client = BPSClient(); print(client.test_connection())"

# Test specific endpoint
python tests/test_bps_client.py
```

---

## 📝 Usage Examples

### Python Script

```python
from bps_client import BPSClient

# Initialize client
client = BPSClient(api_key="06fd644648629502353deaed29fc6383")

# Fetch ekspor data
ekspor_data = client.fetch_ekspor_by_province(
    province_code="73",  # Sulsel
    tahun_awal=2016,
    tahun_akhir=2026
)

# Fetch PAD data
pad_data = client.fetch_pad_sulawesi(
    tahun_awal=2016,
    tahun_akhir=2026
)

# Export
client.export_to_csv(ekspor_data, "output/ekspor_sulsel.csv")
client.export_to_json(pad_data, "output/pad_sulawesi.json")
```

---

## 🚨 Troubleshooting

### Error: "Invalid API Key"

```bash
# Check your API key
echo %BPS_API_KEY%

# Re-set it
set BPS_API_KEY=06fd644648629502353deaed29fc6383
```

### Error: "Rate Limit Exceeded"

Increase delay in `config.yaml`:

```yaml
bps:
  rate_limit: 2.0  # Increase to 2 seconds
```

### Error: "No data returned"

Check:
1. Province/regency codes are correct
2. Time range is valid
3. Indicator subject exists

---

## 🔗 Resources

- **BPS Web API Docs**: https://webapi.bps.go.id/documentation
- **BPS Main Site**: https://bps.go.id
- **Sulawesi Statistics**: https://sulsel.bps.go.id

---

## 📄 License

MIT License - Use responsibly and respect BPS ToS

---

*Dibuat untuk CELIOS ECC Intelligence System*  
*Juni 2026*
