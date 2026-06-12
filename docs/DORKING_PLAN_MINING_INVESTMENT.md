# 🔍 RENCANA DORKING: DATA INVESTASI & KAPASITAS PRODUKSI TAMBANG SULAWESI

**Target:** Melengkapi data **Kapasitas Produksi** dan **Nilai Investasi** untuk perusahaan tambang/smelter nikel di Sulawesi

**Status:** 🟠 Planning Phase

**Source Data:**
- MinerbaOne: ✅ Sudah ada (jumlah izin, luas lahan, komoditas)
- CGS Nickel Smelter: ✅ Sudah ada (26 smelter dengan kapasitas)
- Target: ❌ Investasi nilai per perusahaan

---

## 📊 DATA GAP ANALYSIS

### Yang Sudah Ada ✅
| Source | Data Available |
|--------|----------------|
| MinerbaOne | Nama perusahaan, jumlah izin, luas lahan (ha), komoditas, lokasi |
| CGS Smelter | 26 smelter dengan **kapasitas produksi** (RKEF, Rotary Kiln, Pyrometallurgical) |

### Yang MISSING ❌
| Data Type | Description | Priority |
|-----------|-------------|----------|
| **Nilai Investasi** | USD/IDR per proyek/perusahaan | 🔴 HIGH |
| **Kapasitas Produksi Tambang** | Ton ore/tahun (untuk mining companies) | 🟡 MEDIUM |
| **Status Operasional** | Operasi/Konstruksi/Planned | 🟡 MEDIUM |
| **Tahun Investasi** | Kapan investasi direalisasikan | 🟢 LOW |

---

## 🎯 STRATEGI DORKING

### **A. GOOGLE DORKING - INVESTASI PERUSAHAAN**

#### 1️⃣ Pattern: Press Release & News
```
site:*.co.id OR site:*.com [NAMA_PERUSAHAAN] investasi nikel sulawesi USD
site:*.co.id OR site:*.com [NAMA_PERUSAHAAN] investment nickel smelter million
```

**Target Sites:**
- `kontan.co.id`, `bisnis.com`, `cnbcindonesia.com`, `ekonomi.bisnis.com`
- `theinsiderstories.com`, `tambang.co.id`, `minerba.esdm.go.id`

**Example Queries:**
```
site:kontan.co.id "Harita Group" investasi nikel sulawesi "US$"
site:bisnis.com "PT Vale Indonesia" investasi smelter morowali
inurl:berita nikel investasi "Kab. Morowali" OR "Kab. Konawe"
```

#### 2️⃣ Pattern: Company Reports & Filings
```
site:idx.co.id OR site:ojk.go.id [NAMA_PERUSAHAAN] investasi tambang
filetype:pdf [NAMA_PERUSAHAAN] "capital expenditure" nickel Indonesia
filetype:pdf annual report [NAMA_PERUSAHAAN] nickel investment
```

**Target:**
- Annual Reports (Laporan Tahunan)
- Prospektus IPO
- OJK Filings (untuk perusahaan publik)

#### 3️⃣ Pattern: Government Sources
```
site:bkpm.go.id OR site:esdm.go.id investasi nikel sulawesi 2020..2024
site:kemenperin.go.id smelter nikel investasi sulawesi
site:databoks.katadata.co.id investasi tambang nikel indonesia
```

#### 4️⃣ Pattern: International News (Chinese/Foreign Investment)
```
site:reuters.com OR site:bloomberg.com nickel smelter indonesia investment
"Tsingshan" OR "GEM" OR "Huayou" indonesia nickel investment million
IMIP OR IWIP morowali investment capacity production
```

---

### **B. TARGETED SCRAPING - STRUCTURED DATA**

#### 1️⃣ **BKPM NSWI Portal**
**URL:** `https://nswi.bkpm.go.id/`
- **Status:** 🔴 Requires Login/Authentication
- **Data:** Nilai realisasi investasi PMDN/PMA per perusahaan
- **Method:** Manual download atau API (jika ada)

#### 2️⃣ **MODI ESDM**
**URL:** `https://modi.esdm.go.id/`
- **Status:** 🟡 Public but pagination heavy
- **Data:** IUP details dengan metadata tambahan
- **Method:** Selenium scraping (slow but comprehensive)

#### 3️⃣ **Geoportal ESDM**
**URL:** `https://geoportal.esdm.go.id/`
- **Status:** 🟡 Map-based, requires GIS extraction
- **Data:** Spatial data izin tambang dengan metadata
- **Method:** GeoJSON/WMS layer scraping

#### 4️⃣ **Indonesia Investment Coordinating Board (BKPM) Reports**
**URL:** `https://www.bkpm.go.id/id/publikasi/detail/berita`
- **Status:** ✅ Public
- **Data:** Quarterly investment reports (aggregated by sector)
- **Method:** PDF parsing + keyword extraction

---

### **C. ALTERNATIVE DATA SOURCES**

| Source | URL | Data Type | Method |
|--------|-----|-----------|--------|
| **ANTAM Reports** | `antam.com/en/investor-relations` | Nickel production stats | PDF scraping |
| **Vale Indonesia** | `vale.com/indonesia` | Production capacity, investment | Annual report |
| **Mining Intelligence** | `mining-intelligence.com` | Mine/smelter database | Paid API |
| **S&P Global** | `spglobal.com/marketintelligence` | Mining project database | Paid subscription |
| **ASEAN Briefing** | `aseanbriefing.com` | Investment news | Web scraping |

---

## 🛠️ IMPLEMENTATION ROADMAP

### **Phase 1: Low-Hanging Fruit (1-2 hari)**
- [ ] Google dorking untuk **top 20 companies** dari MinerbaOne
- [ ] Parse CGS smelter dataset untuk map ke MinerbaOne companies
- [ ] Scrape BKPM press releases (2020-2024)
- [ ] Extract investment data dari PDF reports (Vale, ANTAM, Harita)

### **Phase 2: Structured Scraping (3-5 hari)**
- [ ] MODI ESDM scraping (detail per IUP)
- [ ] NSWI BKPM manual download (jika perlu akun)
- [ ] News aggregation (Kontan, Bisnis, CNBC)

### **Phase 3: Data Enrichment (2-3 hari)**
- [ ] Cross-reference dengan BPS PMDN data
- [ ] Fuzzy matching company names (MinerbaOne vs news)
- [ ] Quality check & validation

---

## 📋 OUTPUT SCHEMA

**Final CSV Columns:**
```
company_name, province, total_permits, nickel_permits, total_area_ha,
investment_value_usd, investment_value_idr, investment_year,
production_capacity_ton, capacity_type (ore/ferronickel/NPI),
operational_status, data_source, confidence_score, notes
```

**Confidence Score:**
- **High (90-100%):** Official company reports, BKPM filings
- **Medium (70-89%):** Credible news sources (Kontan, Bloomberg)
- **Low (50-69%):** Secondary sources, estimates

---

## ⚠️ CHALLENGES & MITIGATIONS

| Challenge | Mitigation |
|-----------|------------|
| Company name mismatch | Fuzzy string matching + manual verification |
| Investasi aggregated (not per-project) | Use permit-level data from MODI |
| Paywall sources | Focus on free/public sources first |
| Data recency | Prioritize 2020-2024 data |
| Chinese company names | Use both English/Chinese characters in search |

---

## 🚀 QUICK START DORKING QUERIES

### For Top Nickel Companies:
```bash
# Harita Group
site:*.co.id "Harita Group" OR "PT Harita Nickel" investasi sulawesi "US$" OR "USD"

# Tsingshan/IMIP
site:reuters.com OR site:bloomberg.com "Tsingshan" morowali investment "billion"

# Vale Indonesia
site:vale.com OR site:idx.co.id "Vale Indonesia" nickel investment capacity

# GEM/Rigqueza
site:*.co.id "GEM" OR "Rigqueza" nikel investasi konawe

# ANTAM
site:antam.com OR site:idx.co.id ANTAM nickel production investment

# Virtue Dragon
site:*.co.id "Virtue Dragon" OR "PT Virtue Dragon Nickel" investasi
```

---

## 📝 NOTES

1. **CGS Dataset** sudah punya kapasitas untuk **26 smelter** - ini **gold standard** untuk smelter data
2. **MinerbaOne** punya **mining permits** tapi **TIDAK punya kapasitas produksi**
3. **BPS PMDN** punya nilai investasi **tapi aggregated per sektor**, bukan per perusahaan
4. **Dorking adalah MUST** untuk per-company investment data

**Next Step:** Run Phase 1 dorking untuk top 20 companies?
