# Tools Pendukung Proyek — CELIOS ECC Intelligence System

> **Dokumen ini adalah referensi living document** yang mendaftar tool-tool open source yang direkomendasikan untuk digunakan atau dipelajari selama proyek berlangsung.  
> Diperbarui seiring proyek berkembang.  
> **Dibuat:** Juni 2026 | **Status:** Aktif digunakan / Dipelajari

---

## Kategori Tool

1. [📑 Document Intelligence — PageIndex](#1-pageindex--document-intelligence-tanpa-chunking)
2. [🕷️ Web Scraping Adaptif — Scrapling](#2-scrapling--web-scraping-adaptif-anti-bot)
3. [🔍 OSINT & Recon Arsenal](#3-awesome-osint-arsenal--toolkit-osint-lengkap)
4. [🕵️ Google OSINT — GHunt](#4-ghunt--osint-berbasis-google)

---

## 1. PageIndex — Document Intelligence Tanpa Chunking

**GitHub:** https://github.com/VectifyAI/PageIndex  
**Stars:** ⭐ 32.5k | **License:** MIT  
**Bahasa:** Python

### Apa itu PageIndex?

PageIndex adalah sistem RAG (**Retrieval-Augmented Generation**) berbasis **penalaran (reasoning-based)**, bukan vektor similarity. Terinspirasi dari AlphaGo, ia membangun **indeks pohon hierarkis** dari dokumen panjang dan menggunakan LLM untuk bernalar melalui tree tersebut — persis seperti cara manusia membaca dan menavigasi dokumen kompleks.

> **Kunci:** No Vector DB. No Chunking. Tidak ada potongan teks buatan. Dokumen dibaca utuh dalam struktur alaminya.

### Cara Kerja

```
Dokumen PDF/MD → Bangun "Table of Contents" sebagai Tree Index
                ↓
     LLM melakukan Tree Search (reasoning)
                ↓
         Retrieval relevan + traceable
```

### Fitur Utama

| Fitur | Keterangan |
|-------|------------|
| **No Chunking** | Dokumen diorganisir dalam seksi alami, bukan potongan buatan |
| **No Vector DB** | Retrieval berbasis struktur dokumen + reasoning LLM |
| **Explainable** | Setiap hasil retrieval bisa ditelusuri hingga halaman & seksi asal |
| **Context-Aware** | Retrieval mempertimbangkan konteks percakapan penuh |
| **Multi-LLM** | Support via LiteLLM: OpenAI, Anthropic, Gemini, dll. |
| **MCP Server** | Bisa diintegrasikan langsung ke Claude/Cursor sebagai tool |

### Performa

Pada benchmark **FinanceBench** (analisis dokumen keuangan panjang):
- PageIndex: **98.7% akurasi**
- Vector RAG tradisional: jauh di bawah

### Relevansi untuk Proyek ECC

| Use Case | Penerapan |
|----------|-----------|
| **Baca paper Świąder et al. (2020)** | Parse PDF panjang tanpa kehilangan konteks metodologi |
| **Baca laporan PLN, ESDM, KLHK** | Dokumen PDF tebal dengan tabel kompleks → retrieval akurat |
| **Baca dokumen RTRW provinsi** | Navigasi dokumen perencanaan tata ruang ratusan halaman |
| **Bibliometric Discovery** | Ekstrak informasi dari banyak paper sekaligus |

### Quick Start

```bash
pip install -r requirements.txt
# Set API key di .env
python3 run_pageindex.py --pdf_path /path/to/laporan-pln-2023.pdf
```

### Deployment Options

- **Self-host** (open source) — bisa jalan lokal
- **Cloud API** — untuk dokumen dengan OCR kompleks
- **MCP Server** — integrasi langsung ke AI assistant

---

## 2. Scrapling — Web Scraping Adaptif & Anti-Bot

**GitHub:** https://github.com/D4Vinci/Scrapling  
**Stars:** ⭐ 59.3k | **License:** BSD-3-Clause  
**Bahasa:** Python | **Versi terbaru:** v0.4.8 (Mei 2026)

### Apa itu Scrapling?

Scrapling adalah framework web scraping Python yang **adaptif** — ia bisa belajar dari perubahan website dan **otomatis menemukan kembali elemen** yang bergeser. Dilengkapi dengan kemampuan bypass anti-bot (Cloudflare Turnstile, dll.) out of the box.

> **Satu library untuk semua kebutuhan**: dari single HTTP request hingga full-scale crawl dengan concurrency, pause/resume, dan proxy rotation.

### Fitur Utama

| Fitur | Keterangan |
|-------|------------|
| **StealthyFetcher** | Bypass Cloudflare Turnstile dan anti-bot lainnya |
| **Adaptive Element Tracking** | Otomatis temukan elemen setelah website berubah tampilan |
| **Spider Framework** | Scrapy-like API untuk full crawl dengan concurrency |
| **Pause & Resume** | Checkpoint-based crawl — bisa dihentikan dan dilanjutkan |
| **Session Management** | Cookie & state persistence lintas request |
| **Proxy Rotation** | Built-in ProxyRotator dengan strategi cyclic atau custom |
| **MCP Server** | Digunakan langsung oleh AI assistant (Claude/Cursor) |
| **CLI Tool** | Scrape URL langsung dari terminal tanpa nulis kode |
| **Async Support** | Full async untuk semua fetcher |

### Fetcher Options

```python
from scrapling.fetchers import Fetcher, StealthyFetcher, DynamicFetcher

# HTTP biasa (cepat)
page = Fetcher.get('https://webapi.bps.go.id/...')

# Stealth mode (bypass anti-bot)
page = StealthyFetcher.fetch('https://sipsn.menlhk.go.id/...', headless=True)

# Full browser automation (JavaScript heavy)
page = DynamicFetcher.fetch('https://geoportal.menlhk.go.id/...')
```

### Relevansi untuk Proyek ECC

| Sumber Data ECC | Fetcher yang Cocok |
|----------------|--------------------|
| **BPS WebAPI** | `Fetcher` (API REST biasa) |
| **SIPSN KLHK** | `StealthyFetcher` atau `Fetcher` + BeautifulSoup |
| **PLN Statistik** | `Fetcher` → download PDF, atau `DynamicFetcher` jika JS-heavy |
| **ESDM / Pertamina** | `Fetcher` untuk halaman statis |
| **Geoportal KLHK** | `DynamicFetcher` (peta interaktif GIS) |
| **BNPB InaRisk** | `DynamicFetcher` |

### Instalasi

```bash
pip install scrapling
pip install "scrapling[fetchers]"  # untuk fetcher dengan browser
scrapling install                  # download browser dependencies
```

---

## 3. Awesome OSINT Arsenal — Toolkit OSINT Lengkap

**GitHub:** https://github.com/rawfilejson/awesome-osint-arsenal  
**Stars:** ⭐ 494 | **License:** —  
**Bahasa:** Shell (installer scripts)

### Apa itu Awesome OSINT Arsenal?

Koleksi kurasi **100+ tools OSINT dan recon** untuk Kali Linux, dilengkapi **one-command installer**. Mencakup berbagai kategori: SOCMINT, GEOINT, network recon, dark web, forensics, dan lainnya.

### Struktur Tool

| Script | Kategori Tools |
|--------|---------------|
| `osint.sh` | OSINT tools utama |
| `redteam.sh` | Red team & penetration testing |
| `blueteam.sh` | Blue team & defensive tools |
| `forensics.sh` | Digital forensics |
| `hardware.sh` | Hardware recon |
| `extras.sh` | Tools tambahan |
| `termux.sh` | Mobile (Android/Termux) |

### Kategori Tools

- **SOCMINT** — Social media intelligence (Instagram, Twitter, LinkedIn)
- **GEOINT** — Geospatial intelligence, koordinat, satelit
- **Network Recon** — Scan port, identifikasi infrastruktur
- **Dark Web** — Monitoring forum, leak database
- **Forensics** — Analisis metadata, file recovery
- **Government Data** — Public records, data pemerintah

### Relevansi untuk Proyek ECC

| Use Case | Tools yang Relevan |
|----------|--------------------|
| **Verifikasi data pemerintah** | Government data tools, public records |
| **Monitoring laporan lingkungan** | Web scraping + SOCMINT untuk NGO/media |
| **Geospatial analysis** | GEOINT tools untuk validasi koordinat provinsi |
| **Audit sumber data** | Network recon untuk verifikasi endpoint API |

> ⚠️ **Catatan Etis:** Gunakan hanya untuk riset legal dan data publik. Seluruh akuisisi data ECC harus mematuhi ToS sumber masing-masing.

---

## 4. GHunt — OSINT Berbasis Google

**GitHub:** https://github.com/mxrch/GHunt  
**Stars:** ⭐ 19k | **License:** AGPL-3.0  
**Bahasa:** Python | **Versi terbaru:** v2.2.0

### Apa itu GHunt?

GHunt adalah **offensive Google framework** untuk OSINT — mengekstrak informasi yang terhubung dengan akun Google (Gmail, Google Maps, Google Drive, dll.) secara legal untuk keperluan investigasi.

> **Online version:** https://osint.industries

### Modul yang Tersedia

| Modul | Fungsi |
|-------|--------|
| `email` | Ekstrak informasi dari alamat Gmail |
| `gaia` | Informasi dari Google Gaia ID |
| `drive` | Metadata file/folder Google Drive publik |
| `geolocate` | Geolocate berdasarkan BSSID WiFi |
| `spiderdal` | Temukan aset via Digital Assets Links |

### Instalasi

```bash
pip install pipx
pipx ensurepath
pipx install ghunt
ghunt login
```

### Export JSON

```bash
ghunt email <email> --json output.json
```

### Relevansi untuk Proyek ECC

| Use Case | Penerapan |
|----------|-----------|
| **Verifikasi kontak sumber data** | Cek kredibilitas narasumber atau instansi |
| **Research discovery** | Temukan akun peneliti lingkungan Indonesia |
| **Geolocate data lapangan** | Validasi koordinat lapangan via BSSID |

> ⚠️ **Disclaimer:** Gunakan hanya untuk tujuan riset, investigasi legal, dan data publik. Hormati privasi individu.

---

## Ringkasan Penggunaan di Proyek ECC

| Tool | Fase Proyek | Kegunaan Utama |
|------|-------------|----------------|
| **PageIndex** | Semua fase | Baca & ekstrak dokumen PDF panjang (paper, laporan, regulasi) |
| **Scrapling** | Fase 12 (Data Pipeline) | Scrape data nyata dari BPS, SIPSN, PLN, ESDM, KLHK |
| **OSINT Arsenal** | Research support | Verifikasi sumber data, monitoring laporan lingkungan |
| **GHunt** | Research support | OSINT peneliti, verifikasi narasumber |

---

## Catatan Pengembangan

- [ ] PageIndex — Uji coba dengan paper Świąder et al. PDF
- [ ] Scrapling — Proof-of-concept scrape endpoint BPS WebAPI
- [ ] Scrapling — Test `StealthyFetcher` untuk SIPSN KLHK
- [ ] OSINT Arsenal — Review tools yang relevan untuk data pemerintah Indonesia
- [ ] GHunt — Pelajari batasan ToS untuk penggunaan riset

---

*Dokumen ini akan diperbarui seiring proyek berkembang dan tool baru ditemukan.*  
*Dibuat: Juni 2026 | CELIOS ECC Intelligence System*
