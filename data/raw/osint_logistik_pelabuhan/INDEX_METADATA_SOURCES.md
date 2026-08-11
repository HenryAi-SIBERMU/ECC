# INDEX METADATA SUMBER RAW - Pelabuhan Ekspor Nikel Sulawesi

## Overview
Folder ini berisi **METADATA SUMBER ASLI (RAW)** dari proses dorking OSINT untuk 3 Dataset Cards section 1.5 Dashboard.

Ini BUKAN data processed/clean, tapi **dokumentasi lengkap sumber-sumber mentah** yang digunakan untuk membangun dataset final `sulawesi_logistik_simpul_nikel.csv`.

---

## Struktur File Metadata

### 1. `sources_card1_25_sumber.json`
**Untuk:** Card 1 - Fasilitas Pelabuhan Ekspor

**Isi:**
- 25 sumber OSINT (website perusahaan, media, dokumen pemerintah, satellite imagery, vessel tracking)
- Setiap sumber memiliki:
  - URL lengkap + archived URL
  - Tanggal akses
  - Key information extracted
  - Reliability score
  - Screenshot/PDF reference

**Kategori Sumber:**
- Website Perusahaan: 5 sumber (IMIP, GNI, Vale, ANTAM, VDNI)
- Media Investigasi: 9 sumber (Katadata, Mongabay, Tempo, Kompas, JATAM, Bloomberg, Gecko Project, dll)
- Dokumen Pemerintah: 3 sumber (AMDAL, UKL-UPL, Kemenhub)
- Satellite Imagery: 2 sumber (Google Earth Pro, Sentinel Hub)
- Vessel Tracking: 2 sumber (Marine Traffic, Vessel Finder)
- Laporan Keuangan: 2 sumber (ANTAM Annual Report, Vale Sustainability Report)
- Media Lokal: 2 sumber (Radar Sultra, Tribun Sultra)
- Investigasi Lapangan: 1 sumber (DuniaHub Field Research)

**File Size:** ~12 KB (JSON structured)

---

### 2. `sources_card2_perpres_kppip.json`
**Untuk:** Card 2 - Status Proyek Strategis Nasional (PSN)

**Isi:**
- 3 dokumen resmi pemerintah (Perpres 58/2017, Perpres 12/2025, KPPIP Buku PSN 2022)
- Metadata lengkap:
  - Nomor dokumen resmi
  - Tanggal terbit
  - URL download (peraturan.go.id, jdih.setneg.go.id, kppip.go.id)
  - Archived URL
  - Pasal/section relevan
  - Confirmed PSN projects per dokumen
  - Download instructions
  - Local copy reference

**Hasil Validasi:**
- ✅ IMIP: Terkonfirmasi (3 dokumen)
- ✅ VDNI: Terkonfirmasi (2 dokumen)
- ✅ OSS: Terkonfirmasi (2 dokumen, bagian dari IKN)
- ✅ ANTAM: Terkonfirmasi (1 dokumen + Vale PDF reference)
- ❌ GNI: Tidak ditemukan
- ❌ Vale: Tidak ditemukan

**File Size:** ~10 KB (JSON structured)

---

### 3. `sources_card3_gni_website.json`
**Untuk:** Card 3 - Detail Kapasitas Pelabuhan

**Isi:**
- 6 sumber detail teknis (GNI website, IMIP website, ANTAM annual report, Vale sustainability report, VDNI UKL-UPL, Kompas article)
- Data extracted:
  - Port capacity (DWT, berth length, draft depth)
  - Infrastructure (roads, conveyor, airport, stockpile)
  - Operational details (loading time, export destinations, cargo types)
  - Screenshots saved location
  - PDF/HTML archived location

**Highlights:**
- 🏆 **Largest Port:** GNI (50,000 DWT vessel)
- ⚡ **Fastest Unloading:** ANTAM (1,000 ton/hour)
- ✈️ **Unique:** IMIP airport 1,800m
- 🔗 **Shared Facility:** OSS-VDNI model

**File Size:** ~15 KB (JSON structured)

---

## Total Raw Sources Documented

| Category | Count | Reliability |
|----------|-------|-------------|
| **Website Perusahaan** | 5 | Very High |
| **Dokumen Pemerintah Resmi** | 6 | Very High |
| **Laporan Keuangan Korporat** | 2 | Very High |
| **Media Investigasi Nasional** | 7 | High |
| **Media Internasional** | 2 | High |
| **Media Lokal** | 2 | Medium |
| **Satellite Imagery** | 2 | Very High |
| **Vessel Tracking** | 2 | High |
| **Akademik** | 1 | High |
| **Investigasi Lapangan** | 1 | High |
| **TOTAL** | **34 sources** | **Average: High** |

---

## Data Processing Pipeline

```
RAW SOURCES (34 sumber)
    ↓
EXTRACTION (Manual + Automated scraping)
    ↓
CROSS-VALIDATION (Min 3 sources per claim)
    ↓
VERIFICATION (Satellite + Vessel tracking)
    ↓
COMPILATION (Excel/CSV structured)
    ↓
CLEANING (Standardize format, remove duplicates)
    ↓
PROCESSED DATASET
data/processed/sulawesi_logistik_simpul_nikel.csv
```

---

## How to Use This Metadata

### For Data Validation
1. Check `sources_card1_25_sumber.json` untuk validasi claim tentang fasilitas pelabuhan
2. Cross-reference dengan `sources_card2_perpres_kppip.json` untuk status PSN
3. Verify technical specs di `sources_card3_gni_website.json`

### For Citation
Gunakan ID sumber + URL untuk citation:
```
Source ID 2 (GNI): gunbusternickelindustry.com/port-facilities
Accessed: 2024-11-20
Data: "GNI pelabuhan 50.000 DWT vessel"
```

### For Reproducibility
1. Download dokumen dari URL yang listed
2. Follow download instructions di masing-masing JSON
3. Compare dengan local copy di folder ini
4. Verify dengan archived URL jika link mati

---

## Files That Should Exist (But Not Included in Repo)

Karena ukuran besar, file-file berikut TIDAK di-commit ke repo, tapi harus di-download manual:

### PDF Documents
```
data/raw/osint_logistik_pelabuhan/
├── Perpres_58_2017.pdf (2.1 MB)
├── Perpres_12_2025.pdf (3.8 MB)
├── KPPIP_Buku_PSN_2022.pdf (45.7 MB)
├── ANTAM_Annual_Report_2023.pdf (8.5 MB)
├── Vale_Indonesia_Sustainability_Report_2023.pdf (12.3 MB)
├── VDNI_UKL_UPL_2017.pdf (4.2 MB)
├── IMIP_AMDAL_2022.pdf (6.8 MB)
└── GNI_Port_Infrastructure_Brochure.pdf (2.1 MB)
```

### HTML Archives
```
data/raw/osint_logistik_pelabuhan/html/
├── GNI_facilities_page.html
├── IMIP_infrastructure_page.html
├── Kompas_OSS_VDNI_article.html
└── ... (other archived HTML pages)
```

### Screenshots
```
data/raw/osint_logistik_pelabuhan/screenshots/
├── GNI_port_overview.png
├── GNI_capacity_specs.png
├── IMIP_seaport_facilities.png
├── IMIP_airport_runway.png
├── Kompas_OSS_VDNI_shared_port.png
└── ... (other screenshots)
```

**Total Size (if all downloaded):** ~90 MB

---

## Download Instructions

### 1. Perpres Documents
```bash
# Perpres 58/2017
wget https://peraturan.go.id/id/perpres-no-58-tahun-2017 -O Perpres_58_2017.pdf

# Perpres 12/2025
wget https://jdih.setneg.go.id/viewpdfperaturan/id/PERPRES_12_2025.pdf -O Perpres_12_2025.pdf
```

### 2. KPPIP Book
```bash
# KPPIP Buku PSN 2022 (45.7 MB - large file!)
wget https://kppip.go.id/publikasi/buku-psn-2022/download -O KPPIP_Buku_PSN_2022.pdf
```

### 3. Corporate Reports
```bash
# ANTAM
wget https://antam.com/sites/default/files/laporan-tahunan/Annual_Report_ANTAM_2023.pdf

# Vale
wget https://vale.com/documents/Vale_Indonesia_Sustainability_Report_2023.pdf
```

### 4. Website Archives (Automated)
```bash
# Install HTTrack
sudo apt-get install httrack  # Linux
brew install httrack          # Mac

# Archive GNI website
httrack https://gunbusternickelindustry.com -O html/GNI +*.gunbusternickelindustry.com/*

# Archive IMIP website
httrack https://imip.co.id -O html/IMIP +*.imip.co.id/*
```

### 5. Screenshots (Manual)
- Buka browser
- Akses URL yang listed di JSON
- Screenshot dengan `Ctrl+Shift+S` (Windows) atau `Cmd+Shift+4` (Mac)
- Save ke folder `screenshots/`

---

## Data Quality Assurance

### Validation Checklist
- [x] All URLs tested and accessible (or archived)
- [x] Cross-validation: Min 3 sources per major claim
- [x] Satellite imagery confirms port existence
- [x] Vessel tracking confirms operational status
- [x] Government docs verify PSN status
- [x] Corporate reports provide technical specs

### Reliability Scoring
- **Very High:** Government docs, corporate audited reports, satellite imagery
- **High:** Reputable media (Katadata, Kompas, Bloomberg), company websites
- **Medium:** Local media (triangulated with other sources)
- **Low:** Single-source claims (flagged for further verification)

### Known Limitations
1. **GNI Website:** Kadang down, rely on Wayback Machine
2. **SIPPN KLHK:** Butuh akun untuk download AMDAL/UKL-UPL
3. **Marine Traffic:** Free tier limited, upgrade for detailed vessel data
4. **Vessel Size:** Beberapa specs estimated (tidak disclosed publicly)
5. **Annual Throughput:** Perusahaan tidak disclose actual volumes, hanya capacity

---

## Updates & Maintenance

### Last Updated
- **Card 1 Sources:** 2024-12-15
- **Card 2 Sources:** 2025-02-01 (Perpres 12/2025 baru keluar)
- **Card 3 Sources:** 2024-11-20

### Update Schedule
- **Quarterly:** Check website updates (GNI, IMIP, Vale, ANTAM)
- **Annually:** Download latest annual reports (ANTAM, Vale)
- **Ad-hoc:** Monitor Perpres updates (jdih.setneg.go.id)
- **Monthly:** Verify vessel tracking data (Marine Traffic)

### Changelog
```
2025-02-01: Added Perpres 12/2025 to Card 2 sources
2024-12-15: Updated IMIP website data extraction
2024-11-20: Initial metadata compilation completed
2024-10-10: Started OSINT collection for 3 cards
```

---

## Contact & Support

**Data Questions:** research@duniahub.org  
**Broken Links:** Report di GitHub Issues  
**Source Contributions:** Pull requests welcome!

---

## License & Attribution

Metadata ini tersedia untuk **penelitian, advokasi, dan jurnalisme publik**.

**Attribution Required:**
```
DuniaHub Research Team (2025). "Raw Source Metadata: Pelabuhan Ekspor Nikel Sulawesi."
Dataset version 1.0. Available at: data/raw/osint_logistik_pelabuhan/
```

**Redistribution:**
- ✅ Allowed: Research, journalism, advocacy
- ✅ Allowed: Non-commercial educational use
- ❌ Not allowed: Commercial use without permission
- ❌ Not allowed: Removal of attribution

---

**Generated:** 2025-08-03  
**Status:** ✅ Complete - Ready for Use  
**Version:** 1.0
