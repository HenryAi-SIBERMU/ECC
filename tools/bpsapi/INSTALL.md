# Installation Guide — BPS API Tool

> **Setup BPS API client untuk CELIOS ECC**

---

## 🔧 Prerequisites

- Python 3.8+
- Internet connection
- BPS API Key: `06fd644648629502353deaed29fc6383`

---

## 📦 Installation Steps

### 1. Navigate to Tool Directory

```bash
cd tools\bpsapi
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows (PowerShell/CMD):**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

Setelah activated, prompt akan berubah:
```
(venv) PS C:\...\tools\bpsapi>
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

**Packages yang akan di-install:**
- requests — HTTP client
- pandas — Data manipulation
- openpyxl — Excel support
- pyyaml — Config parsing
- python-dotenv — Environment variables
- tqdm — Progress bars
- pydantic — Data validation

**Estimasi waktu:** ~30-60 detik

---

## ✅ Verify Installation

### Test 1: Check Python & Packages

```bash
python --version
python -c "import requests, pandas, yaml; print('✅ All packages installed')"
```

### Test 2: Test BPS API Connection

```bash
python bps_client.py
```

Expected output:
```
================================================================================
BPS API Client - Connection Test
================================================================================

1. Testing connection...
   ✅ Connection successful!

2. Listing subjects...
   Found XX subjects
   1. Subject Name (ID: xxx)
   ...

3. Listing domains...
   Found XX domains
   - Sulawesi Utara (Code: 71)
   - Sulawesi Tengah (Code: 72)
   ...

================================================================================
✅ All tests passed! Client is ready.
================================================================================
```

---

## 🚀 Quick Start

### Fetch Ekspor Data

```bash
python fetch_ekspor.py --tahun-awal 2016 --tahun-akhir 2026
```

### Fetch PAD Data

```bash
python fetch_pad_sulawesi.py --tahun-awal 2016 --tahun-akhir 2026
```

### Fetch All Data (Recommended)

```bash
python fetch_all.py --tahun-awal 2016 --tahun-akhir 2026
```

---

## 📁 Expected Output

Setelah run, data akan tersimpan di:

```
output/
├── ekspor_sulawesi_2016_2026.csv
├── ekspor_sulawesi_2016_2026.json
├── pad_sulawesi_2016_2026.csv
└── pad_sulawesi_2016_2026.json
```

---

## 🐛 Troubleshooting

### Error: "python not found"

**Solusi:**
```bash
# Try python3 instead
python3 -m venv venv
```

### Error: "Module not found"

**Solusi:**
```bash
# Make sure venv is activated
venv\Scripts\activate

# Re-install dependencies
pip install -r requirements.txt
```

### Error: "Invalid API Key"

**Solusi:**
Check your `config.yaml` file has the correct API key:
```yaml
bps:
  api_key: "06fd644648629502353deaed29fc6383"
```

### Error: "Rate Limit Exceeded"

**Solusi:**
Increase delay in `config.yaml`:
```yaml
bps:
  rate_limit: 2.0  # Increase to 2 seconds
```

---

## 🔄 Deactivate Virtual Environment

When done, deactivate:

```bash
deactivate
```

---

## 📝 Next Steps

1. ✅ Verify API connection works
2. ✅ Test fetch ekspor/PAD data
3. ✅ Explore BPS API subjects/domains
4. ✅ Customize fetch scripts for specific indicators
5. ✅ Integrate dengan CELIOS ECC pipeline

---

*Setup guide untuk CELIOS ECC Intelligence System*  
*Juni 2026*
