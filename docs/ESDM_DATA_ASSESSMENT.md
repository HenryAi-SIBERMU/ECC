# Assessment: Data ESDM/BKPM (Izin Tambang, Smelter, Investasi)

> **CELIOS ECC Intelligence System**  
> **Created:** 10 Juni 2026  
> **Status:** Technical Assessment — Pre-Implementation  
> **Difficulty:** 🟠 Sulit (High Complexity)

---

## 📊 Executive Summary

Setelah investigasi mendalam terhadap sumber data ESDM/BKPM untuk izin tambang, smelter, dan investasi, **kesimpulan:**

### ✅ What We Found
- ✅ **MODI (Minerba One Data Indonesia)** - Portal resmi ESDM untuk data minerba
- ✅ **SIMBARA** - Sistem terintegrasi untuk tracking minerba (launched 2022, expanded 2024)
- ✅ **Geoportal ESDM** - Data spasial tambang dan smelter
- ✅ **NSWI BKPM** - Data investasi (National Single Window for Investment)
- ✅ **Alternative Sources** - UMD Nickel Smelter Dataset, Global Energy Monitor

### ❌ Major Challenges
- ❌ **No Public API** - MODI/SIMBARA tidak menyediakan REST API publik
- ❌ **JavaScript-Heavy Portals** - Full SPA (Single Page Application) dengan async data loading
- ❌ **Government Access Only** - SIMBARA hanya untuk inter-ministry (Kemenkeu, ESDM, dll)
- ❌ **Data Fragmentation** - Data tersebar di MODI (izin), SIMBARA (tracking), Geoportal (spasial)
- ❌ **Limited Historical Data** - SIMBARA baru 2022, MODI data historis unclear

### 💡 Recommended Strategy
**HYBRID APPROACH: Scraping + Manual + Alternative Sources**

---

## 🎯 Data Target Detail

### 1. Jumlah Izin Tambang/Smelter
**Sumber Primer:** MODI (https://modi.esdm.go.id)
- **Portal:** `/portal` - Company listing
- **Smelter:** `/smelter` - Smelter-specific data
- **IUP Database:** Integrated mining permit database

**Data Points:**
- Nama perusahaan
- Nomor IUP (Izin Usaha Pertambangan)
- Jenis komoditas (nickel, coal, bauxite, tin, copper)
- Tahun penerbitan izin
- Status operasi (aktif/non-aktif)
- Lokasi (provinsi, kabupaten)

### 2. Kapasitas Produksi
**Sumber Primer:** MODI + SIMBARA
- **Kapasitas:** Ton/tahun per smelter
- **Realisasi Produksi:** Actual output (dari SIMBARA)
- **PLTU Captive:** Power generation capacity (GW)

**Data Points:**
- Kapasitas terpasang (nameplate capacity)
- Utilisasi (%)
- Produksi aktual (ton/tahun)

### 3. Nilai Investasi
**Sumber Primer:** BKPM NSWI
- **PMDN:** Investasi domestik (BPS API sudah berhasil)
- **PMA:** Foreign direct investment
- **Sektor:** Mining & quarrying, manufacturing (metal processing)

**Data Points:**
- Nilai investasi (USD/IDR)
- Breakdown per provinsi
- Breakdown per sub-sektor (nickel, coal, copper, dll)

### 4. Luas Kawasan Industri
**Sumber Primer:** Geoportal ESDM + BIG/KLHK One Map
- **Wilayah Izin Usaha Pertambangan (WIUP)**
- **Kawasan Industri Pengolahan (smelter parks)**
- **Footprint deforestasi**

**Data Points:**
- Luas lahan (hektar)
- Koordinat geografis (polygon/shapefile)
- Perubahan tutupan lahan 2016-2026

---

## 🔍 Portal Analysis

### A. MODI (Minerba One Data Indonesia)

**URL:** https://modi.esdm.go.id

#### Structure Analysis
```
MODI Portal Architecture:
├── /portal              → Company/IUP listing (main database)
├── /smelter             → Smelter-specific data
├── /produksi-batubara   → Coal production data
├── /detail Perusahaan   → Individual company pages
└── [Hidden API endpoints to discover]
```

#### Technical Stack
- **Framework:** Modern JavaScript SPA (likely Vue.js or React)
- **Data Loading:** Asynchronous (AJAX/Fetch API)
- **Authentication:** Session-based (cookies)
- **Anti-Bot:** Unclear, likely rate limiting

#### Data Accessibility
- ⚠️ **Portal listing accessible** - Company names and basic info visible
- ⚠️ **Detail pages require navigation** - Deep linking possible
- ❌ **No direct API** - Must scrape HTML or intercept XHR
- ⚠️ **Pagination** - Likely thousands of entries

#### Scraping Strategy
**Option 1: Browser Automation (Playwright/Scrapling)**
- Pros: Can handle JavaScript rendering
- Cons: Slow, high resource usage, may be rate-limited
- Method: Navigate → Wait for data → Extract JSON from page

**Option 2: XHR Interception**
- Pros: Fast, direct access to JSON
- Cons: Requires reverse engineering API endpoints
- Method: Inspect Network tab → Find API calls → Replicate with requests

**Option 3: HTML Parsing (Fallback)**
- Pros: Works if JavaScript fails
- Cons: Fragile (breaks if layout changes)
- Method: BeautifulSoup / lxml parsing

### B. SIMBARA

**URL:** Not publicly accessible (government internal system)

#### What We Know
- Launched: March 2022 (coal), expanded July 2024 (nickel, tin)
- Purpose: Inter-ministry tracking system (Kemenkeu, ESDM, customs)
- Data: Production, sales, exports, tax compliance
- Access: **Government agencies only**

#### Implications for Research
- ❌ **Cannot access directly**
- ✅ **Aggregate data may appear in:** Ministry reports, BPS publications, press releases
- ✅ **Workaround:** Parse PDF reports mentioning SIMBARA data

### C. Geoportal ESDM

**URL:** https://geoportal.esdm.go.id

#### Structure Analysis
- **Type:** ArcGIS-based geospatial portal
- **Data:** WMS/WFS services (Web Map Service / Web Feature Service)
- **Layers:** Mining concessions, smelter locations, geological maps

#### Technical Access
```
Potential ArcGIS REST API endpoints (standard):
- /arcgis/rest/services/              → Service listing
- /MapServer/                          → Map layers
- /FeatureServer/                      → Feature data (queryable)
- /query?where=1=1&outFields=*&f=json  → Export all features
```

#### Data Availability
- ✅ **Spatial data downloadable** - Shapefiles/GeoJSON
- ✅ **REST API likely available** - Standard ArcGIS patterns
- ⚠️ **May require authentication** - Check access restrictions
- ✅ **Historical comparison possible** - If time-series layers exist

#### Scraping Strategy
**Option 1: ArcGIS REST API (Preferred)**
- Pros: Direct JSON access, structured data, fast
- Cons: May require API key or authentication
- Method: Query FeatureServer endpoints with spatial filters

**Option 2: WFS Download**
- Pros: Standard OGC protocol, shapefile export
- Cons: Large file sizes, requires GIS processing
- Method: QGIS/Python OGR library

### D. BKPM NSWI

**URL:** https://nswi.bkpm.go.id

#### Structure Analysis
- **Type:** Investment licensing portal (OSS 2.0 integration)
- **Data:** Investment permits, company registrations
- **Access:** Public dashboard vs. restricted data

#### Data Accessibility
- ✅ **Aggregate statistics available** - Total investment by sector/region
- ❌ **Company-level data restricted** - Requires business login
- ✅ **BPS API already successful** - PMDN data obtained (96 rows)
- ⚠️ **PMA data unclear** - May need manual download

---

## 📋 Alternative Data Sources

### 1. University of Maryland Nickel Smelter Dataset
**URL:** https://dgi.umd.edu (CGS - Center for Global Sustainability)

**What It Contains:**
- Comprehensive list of nickel smelters in Indonesia
- Operational status, capacity, location
- Ownership structure, investment amounts
- Published: 2024 (most recent)

**Accessibility:** ✅ Public research dataset, likely downloadable

**Strategy:** Download CSV/Excel → Merge with MODI data for validation

### 2. Global Energy Monitor (GEM)
**Portal:** https://www.gem.wiki

**What It Contains:**
- Coal Mine Tracker
- Smelter tracking (some coverage)
- Power plant database (captive PLTU)

**Accessibility:** ✅ Public wiki, API available

**Strategy:** Query API → Cross-reference with MODI

### 3. APNI (Asosiasi Penambang Nikel Indonesia)
**URL:** https://www.apni.or.id

**What It Contains:**
- Member companies (nickel miners/smelters)
- Industry statistics
- HPM Calculator (nickel pricing)

**Accessibility:** ✅ Public website, some data tables

**Strategy:** Scrape member directory → Match with MODI IUPs

### 4. Academic Publications & Reports
**Sources:**
- RMI (Rocky Mountain Institute) - "Advancing Clean Metals" report
- IEA (International Energy Agency) - SIMBARA policy analysis
- Reuters/Kompas - News articles with data points

**Strategy:** PDF parsing → Extract tabular data

---

## 🛠️ Recommended Implementation Strategy

### Phase 1: Low-Hanging Fruit (1-2 Days)
**Target:** Get baseline data from easiest sources

1. **Download UMD Nickel Smelter Dataset**
   - Method: Web search → Download CSV
   - Tool: Manual download or requests
   - Output: `data/raw/umd_nickel_smelters_indonesia_2024.csv`
   
2. **Query GEM Wiki API**
   - Method: API client (Python requests)
   - Tool: `tools/gem_api_client.py`
   - Output: `data/raw/gem_coal_mines_indonesia.csv`

3. **Scrape APNI Member Directory**
   - Method: Scrapling (simple HTML parsing)
   - Tool: `tools/scrapling/scrape_apni.py`
   - Output: `data/raw/apni_members_nickel.csv`

**Estimasi:** 4-6 jam development + 30 menit eksekusi

### Phase 2: Geoportal ESDM API (2-3 Days)
**Target:** Extract spatial data and smelter locations

1. **Discover ArcGIS REST Endpoints**
   - Method: Manual exploration (browser → inspect network)
   - Tool: Postman / Insomnia (API testing)
   - Document: All available FeatureServer layers

2. **Query Smelter/Mining Concession Layers**
   - Method: Python ArcGIS REST API client
   - Tool: `tools/geoportal/arcgis_client.py`
   - Output: `data/raw/geoportal_smelters_*.geojson`

3. **Process Spatial Data**
   - Method: GeoPandas / Shapely
   - Calculate: Luas kawasan, provinsi, jarak ke pemukiman
   - Output: `data/processed/smelter_locations_sulawesi.csv`

**Estimasi:** 8-12 jam (including API reverse engineering)

### Phase 3: MODI Portal Scraping (3-5 Days)
**Target:** Extract IUP database and company details

**Sub-Phase 3A: Reconnaissance**
1. Manual exploration of MODI portal structure
2. Identify XHR/Fetch API calls (Chrome DevTools)
3. Document API endpoints, parameters, response schemas
4. Test rate limits and anti-bot measures

**Sub-Phase 3B: Implementation**
1. **If API endpoints found:** Build API client
   - Tool: `tools/modi/modi_api_client.py`
   - Method: Direct JSON requests (fast)
   
2. **If API blocked:** Use Scrapling StealthyFetcher
   - Tool: `tools/modi/scrape_modi_portal.py`
   - Method: Browser automation with stealth
   
3. **Fallback:** Manual download strategy (if all fails)
   - Create: `docs/PANDUAN_DOWNLOAD_MANUAL_MODI.md`
   - User task: Download CSV exports per region

**Output:**
- `data/raw/modi_iup_database_*.csv` (paginated downloads)
- `data/raw/modi_smelter_details_*.csv`
- `data/raw/modi_companies_sulawesi.csv`

**Estimasi:** 16-24 jam (high complexity, may fail)

**Risk Assessment:** 🔴 HIGH RISK
- May encounter Cloudflare/anti-bot (like BPS)
- May require manual download fallback
- Data structure may be complex/nested

### Phase 4: Data Consolidation (1-2 Days)
**Target:** Merge all sources into master dataset

1. **Merge & Deduplicate**
   - UMD + GEM + APNI + Geoportal + MODI
   - Match by: Company name, location, capacity
   - Resolve conflicts (take most recent/reliable source)

2. **Enrich with BPS Investment Data**
   - Already obtained: PMDN per provinsi (96 rows)
   - Allocate investment to specific smelters (proportional to capacity)

3. **Calculate Derived Metrics**
   - Luas kawasan per provinsi (sum)
   - Jumlah izin baru per tahun (count)
   - Growth rate (% change YoY)

**Output:** `data/processed/d3tlh_industri_master_2016_2026.csv`

**Estimasi:** 6-8 jam

---

## 📊 Expected Data Structure

```csv
company_name,iup_number,commodity,province,kabupaten,latitude,longitude,capacity_ton_year,operational_status,year_issued,investment_usd,luas_kawasan_ha,pltu_captive_mw,source
PT Smelter A,IUP-123456,Nickel,Sulawesi Selatan,Luwu Timur,-2.5,121.3,2000000,Operational,2018,500000000,250,150,MODI+UMD
PT Smelter B,IUP-789012,Nickel,Sulawesi Tengah,Morowali,-2.8,121.8,3000000,Operational,2017,800000000,400,300,MODI+Geoportal
```

**Estimated Rows:** 200-500 (all smelters + major mines in Sulawesi)

---

## ⚠️ Risks & Mitigation

### Risk 1: MODI Portal Inaccessible
**Probability:** 🟡 Medium (40%)
**Impact:** 🔴 High (primary data source)

**Mitigation:**
1. Use alternative sources (UMD, GEM) as baseline
2. Create manual download guide (like BPS)
3. Request formal data access from ESDM (official letter from CELIOS)

### Risk 2: Geoportal API Restricted
**Probability:** 🟡 Medium (30%)
**Impact:** 🟡 Medium (spatial data nice-to-have)

**Mitigation:**
1. Manual download via QGIS (WMS/WFS clients)
2. Use satellite imagery analysis (alternative approach)
3. Use published maps from ESDM reports (PDF georeferencing)

### Risk 3: Data Incomplete for 2016-2026
**Probability:** 🟢 High (70%) - Expected
**Impact:** 🟡 Medium (affects time-series analysis)

**Mitigation:**
1. Accept missing years (document limitations)
2. Interpolate missing values (with clear methodology note)
3. Focus on 2018-2024 (when MODI became operational)

### Risk 4: Time Consumption Exceeds Estimate
**Probability:** 🟢 High (60%)
**Impact:** 🟡 Medium (delays Checkpoint 1)

**Mitigation:**
1. Set hard deadline: 5 working days max
2. Switch to manual download if automation fails after Day 3
3. Prioritize Sulawesi data only (skip other provinces)

---

## 📝 Recommendation: GO / NO-GO Decision

### ✅ GO AHEAD - Recommended Approach

**Reason:**
1. Multiple alternative sources available (not dependent on single portal)
2. Geoportal likely has REST API (standard ArcGIS)
3. UMD dataset provides excellent baseline (2024 data)
4. Even with partial data, better than no data
5. Manual download fallback exists

**Execution Plan:**
- **Week 1:** Phase 1 + Phase 2 (low-hanging fruit + Geoportal)
- **Week 2:** Phase 3 (MODI portal - high risk)
- **Week 3:** Phase 4 (consolidation) + Checkpoint 2

**Success Criteria:**
- Minimum: 100+ smelters/mines with basic info (name, location, capacity)
- Target: 300+ entries with full metadata (investment, year issued, status)
- Stretch: Complete MODI IUP database for Sulawesi (all permits 2016-2026)

---

## 🎯 Next Action

**PENDING USER APPROVAL:**
1. **Approve strategy?** Hybrid scraping + manual + alternative sources
2. **Set priority:** Full Sulawesi coverage vs. National sample?
3. **Time budget:** How many days allocated for ESDM data?
4. **Fallback trigger:** When to switch from automation to manual?

**IF APPROVED → START PHASE 1:**
```bash
# Step 1: Setup tools
mkdir -p tools/esdm
mkdir -p tools/geoportal
mkdir -p data/raw/esdm
mkdir -p data/raw/geoportal

# Step 2: Download UMD dataset (manual or script)
# Step 3: Query GEM Wiki API
# Step 4: Scrape APNI directory
# Step 5: Explore Geoportal endpoints
```

---

*Assessment created: 10 Juni 2026*  
*Last updated: 10 Juni 2026*  
*CELIOS ECC Intelligence System*
