# Installation Guide — Scrapling Tool

> **Setup virtual environment dan dependencies**  
> CELIOS ECC Intelligence System

---

## 🔧 Setup (Windows)

### 1. Buat Virtual Environment

```bash
cd tools\scrapling
python -m venv venv
```

Virtual environment sudah dibuat di folder `venv/`.

---

### 2. Activate Virtual Environment

**Option A: Manual**
```bash
venv\Scripts\activate
```

**Option B: Quick Activation**
```bash
activate.bat
```

Setelah activated, prompt akan berubah jadi:
```
(venv) PS C:\...\tools\scrapling>
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Ini akan install:
- `scrapling` — Web scraping framework
- `beautifulsoup4` & `lxml` — HTML parsing
- `requests` — HTTP client
- `pandas` & `openpyxl` — Data handling & Excel export
- `pyyaml` — Config file parsing
- `tqdm` — Progress bar

**Estimasi waktu:** ~30-60 detik

---

### 4. Verify Installation

```bash
python -c "import scrapling; print('Scrapling version:', scrapling.__version__)"
```

Expected output:
```
Scrapling version: 0.4.8
```

---

## 🚀 Quick Test

Test scraper dengan 1 halaman:

```bash
python scrape_tanahkita.py --max-pages 1 --verbose
```

Jika berhasil, akan muncul:
```
✅ Success! Scraped 10 entries
📁 Output: output\tanahkita_konflik.csv
```

---

## 🔄 Deactivate Virtual Environment

Setelah selesai, deactivate dengan:

```bash
deactivate
```

---

## 📦 Struktur Venv

```
venv/
├── Scripts/
│   ├── activate.bat       # Activation script
│   ├── python.exe         # Python isolated
│   └── pip.exe            # Pip isolated
├── Lib/
│   └── site-packages/     # Installed packages
└── pyvenv.cfg             # Config
```

**Note:** Folder `venv/` sudah di-gitignore, tidak akan ke-commit.

---

## 🐛 Troubleshooting

### Error: "python not found"

**Solusi:**
```bash
# Check Python installation
python --version

# Atau gunakan python3
python3 -m venv venv
```

---

### Error: "activate.bat is not recognized"

**Solusi:**
```bash
# Gunakan full path
venv\Scripts\activate.bat

# Atau cd dulu
cd tools\scrapling
venv\Scripts\activate
```

---

### Error: pip install gagal

**Solusi:**
```bash
# Upgrade pip dulu
python -m pip install --upgrade pip

# Lalu install requirements
pip install -r requirements.txt
```

---

### Warning: "pip is out of date"

**Solusi:**
```bash
python -m pip install --upgrade pip
```

---

## 🔐 Dependencies Security

Semua packages di `requirements.txt` adalah:
- ✅ Open source & widely used
- ✅ Maintained actively
- ✅ No known critical vulnerabilities

**Lock versions** untuk reproducibility:
```bash
pip freeze > requirements-lock.txt
```

---

*Setup guide untuk CELIOS ECC Intelligence System*  
*Last updated: Januari 2026*
