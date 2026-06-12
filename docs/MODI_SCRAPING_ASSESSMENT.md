# MODI Portal Scraping Assessment — Pre-Implementation Analysis

> **CELIOS ECC Intelligence System**  
> **Created:** 10 Juni 2026  
> **Target:** https://modi.esdm.go.id/portal  
> **Status:** ⚠️ Technical Assessment — HIGH COMPLEXITY

---

## 📸 Screenshot Analysis

### Gambar 1: Listing Table (Main Page)
**URL Structure:** `https://modi.esdm.go.id/portal`

**Table Columns (8 kolom):**
1. **No** - Nomor urut (1, 2, 3...)
2. **Nama Badan Usaha** - Nama perusahaan (e.g., "3G TRUST", "AAL RIZA TAMBANG PALU")
3. **Jenis Badan Usaha** - Tipe entitas (CV, PT, dll.)
4. **Jenis Perizinan** - IUP (Izin Usaha Pertambangan), IPP, dll.
5. **Alamat** - Alamat lengkap perusahaan
6. **Aksi** - Tombol "Detail" (blue button)

**Pagination Info:**
- Text: "Menampilkan data 1 sampai 10 dari 7527 data"
- **Total entries: 7,527** ← HUGE dataset!
- **Rows per page:** 10
- **Total pages:** 753 pages
- **Pagination:** Standard numbered buttons (1, 2, 3, 4, 5, ... 753, Next)

**Key Observations:**
- ✅ Clear table structure
- ✅ Consistent column layout
- ✅ "Detail" button in every row → leads to detail page
- ⚠️ NO search/filter visible in screenshot
- ⚠️ Large dataset (753 pages!) → scraping akan lama

---

### Gambar 2: Detail Page (After clicking "Detail")
**URL Structure:** `https://modi.esdm.go.id/portal/detailPerusahaan/{ID}?jp={page}`
- Example: `/detailPerusahaan/16357?jp=1`
- `ID` = Company/entity ID (unique)
- `jp` = "Jenis Perizinan" page number (likely for sub-tables)

**Section 1: Informasi Badan Usaha** (Collapsible accordion)
- Nama Badan Usaha: "3G TRUST"
- Kode Badan Usaha: 16357
- Jenis Badan Usaha: "Perusahaan Komanditer (CV)"
- Kelurahan: -
- NPWP: 75618899+++++++
- RT/RW: - / -
- Kode Pos: -
- Alamat: Jl. ALEXANDER RT 002/001, KEL. BACANG, KEC. BUKIT INTAN, PANGKALPINANG

**Section 2: Susunan Direksi dan Komisaris** (Nested table with pagination)
- **Columns:** No, Nama Direksi, Mulai Menjabat, Akhir Menjabat, Jabatan
- **Pagination:** "Menampilkan data 1 sampai 3 dari 3 data" (small dataset per company)
- **Button:** "Cari" (search box)
- Example entries:
  1. FANDY LINGGA - Komisaris
  2. ISA MELKY ZEDECK SUHARJIMAN - Direktur
  3. IRWIN SARIONI - Direktur Utama

**Section 3: Pemegang Kepemilikan Saham** (Nested table)
- **Columns:** No, Jenis Kepemilikan, Nama, Kewarganegaraan, Asal Negara, Persentase Saham
- Example:
  1. Badan Usaha - IRWIN SARIONI - WNI - Indonesia - 30.0000000000
  2. Badan Usaha - FANDY LINGGA - WNI - Indonesia - 35.0000000000
  3. Badan Usaha - ISA MELKY ZEDECK SUHARJIMAN - WNI - Indonesia - 35.0000000000

**Section 4: Daftar Perizinan** (Most important! Nested table with pagination)
- **Columns:** No, Nomor Izin, Jenis Izin, Tahun Kedaluarsa, Golongan, Komoditas, Luas (ha), Tanggal Berlaku, Tanggal Berakhir, Status CNC, Lokasi, Kode WIUP
- **Example entry:**
  - Nomor: 02201043021400002
  - IUP
  - OPERASI PRODUKSI
  - Mineral Bukan Logam Jenis Tertentu
  - Pasir Kuarsa
  - **Luas: 123.9300000**
  - Berlaku: 30 Maret 2023
  - Berakhir: 30 Maret 2043
  - CNC
  - Lokasi: KAB. BELITUNG TIMUR
  - Kode WIUP: 211904031201941

**Search/Filter Features:**
- "Cari Nomor Izin" - Search box untuk filter izin tertentu
- Pagination per section (25 items per page default)

---

## 🔍 Technical Analysis

### A. Website Architecture

**Stack Identification:**
```javascript
// From rendered page source:
let themeMode = "system";
if (localStorage.getItem("kt_theme_mode_value")) {
  themeMode = localStorage.getItem("kt_theme_mode_value");
}
// ... theme detection code

document.documentElement.setAttribute("data-bs-theme", themeMode);
```

**Key Findings:**
- ⚠️ **100% JavaScript SPA** - No server-side rendering
- ⚠️ **Bootstrap 5** framework (data-bs-theme attribute)
- ⚠️ **Client-side state management** (localStorage usage)
- ⚠️ **Async data loading** - Content loaded via AJAX/Fetch after page load
- ⚠️ **Theme system** - MetronicKit-like admin theme (kt_theme_mode_value)

### B. URL Pattern Analysis

**Main Listing:**
```
https://modi.esdm.go.id/portal
https://modi.esdm.go.id/portal?page=2
https://modi.esdm.go.id/portal?page=753
```
(Assumed pattern based on screenshot pagination)

**Detail Page:**
```
https://modi.esdm.go.id/portal/detailPerusahaan/{company_id}
https://modi.esdm.go.id/portal/detailPerusahaan/{company_id}?jp={page}
```
- `company_id`: Integer (e.g., 16357, 12517, 477)
- `jp`: Page number for sub-tables (default = 1)

**ID Range Discovery:**
From search results, observed IDs:
- Lowest: 477 (ANUGERAH BARA INSAN)
- Highest: 15129+ (BERKAH MEKONGGA TERUS JAYA)
- Pattern: Non-sequential, gaps exist

### C. Data Loading Mechanism

**Hypothesis (needs verification):**
1. **Main page:** Fetch `/portal` → Returns blank HTML shell
2. **JavaScript execution:** Page JS makes API call to get table data
3. **Hidden API endpoint:** Likely `/api/portal/list?page=1&per_page=10`
4. **Detail data:** `/api/detailPerusahaan/{id}` or embedded in page JS

**Evidence for Hidden API:**
- Page renders empty without JavaScript (only theme code visible)
- Large dataset (7,527 entries) unlikely embedded in initial HTML
- Modern SPA architecture pattern

### D. Anti-Bot / Security Measures

**Detected:**
- ❌ No Cloudflare (different from BPS!)
- ❌ No Captcha visible in screenshots
- ⚠️ **Likely has:** Rate limiting (government site standard)
- ⚠️ **May have:** Session-based access tracking
- ✅ **Public access:** No login required (visible in screenshots)

**Risk Assessment:** 🟡 MEDIUM
- Easier than BPS (no Cloudflare)
- Harder than tanahkita (full SPA, not server-rendered)

---

## 🛠️ Scraping Strategy Options

### Option 1: XHR/API Interception (RECOMMENDED ⭐)
**Approach:** Reverse engineer hidden API endpoints

**Steps:**
1. Open MODI portal in Chrome
2. Open DevTools → Network tab → Filter: XHR/Fetch
3. Navigate pagination → Identify API calls
4. Document:
   - API base URL (e.g., `/api/portal/list`)
   - Parameters (page, per_page, filters)
   - Response schema (JSON structure)
   - Authentication (if any - likely cookies/session)
5. Replicate API calls with Python `requests`

**Pros:**
- ⚡ **FASTEST** - Direct JSON access (no HTML parsing)
- ⚡ **MOST RELIABLE** - Data structure stable
- ⚡ **LIGHTWEIGHT** - No browser automation overhead
- ⚡ **EASY TO DEBUG** - Clear request/response

**Cons:**
- 🔧 Requires reverse engineering (1-2 hours)
- ⚠️ API may be undocumented/unstable
- ⚠️ May need session/cookie management

**Success Probability:** 🟢 **HIGH (70-80%)**

**Implementation Time:** 4-6 hours (including testing)

---

### Option 2: Scrapling Browser Automation (FALLBACK)
**Approach:** Use StealthyFetcher to render JavaScript and extract data

**Steps:**
1. Use Scrapling's StealthyFetcher (like tanahkita)
2. Navigate to `/portal`
3. Wait for table to render (explicit wait for table element)
4. Extract table rows with BeautifulSoup
5. Click "Detail" button → wait → extract detail data
6. Handle pagination (click "Next" button or construct page URLs)

**Pros:**
- ✅ Works even if API is inaccessible
- ✅ Pattern already proven (tanahkita success)
- ✅ Can handle dynamic content

**Cons:**
- 🐌 **SLOW** - 753 pages × 0.5s delay = ~6 minutes just for listing
- 🐌 **VERY SLOW** - 7,527 detail pages × 1s delay = **~2 hours**
- 💾 **HIGH MEMORY** - Browser instances heavy
- ⚠️ **FRAGILE** - Breaks if layout changes
- ⚠️ **RATE LIMIT RISK** - 7K requests may trigger blocking

**Success Probability:** 🟡 **MEDIUM (60%)**

**Implementation Time:** 8-12 hours (including testing & debugging)

---

### Option 3: Hybrid Approach (PRACTICAL ⭐⭐)
**Approach:** Combine API interception + Browser automation

**Strategy:**
1. **Phase 1:** API intercept for listing (753 pages → get all company IDs)
2. **Phase 2:** API intercept for detail (if endpoint found)
3. **Fallback:** Scrapling for detail if API blocked

**Pros:**
- ⚡ Fast for listing (API)
- ✅ Reliable for detail (browser if needed)
- 🛡️ Lower risk (has fallback)

**Cons:**
- 🔧 More complex code
- ⏱️ Longer development time

**Success Probability:** 🟢 **VERY HIGH (85%)**

**Implementation Time:** 6-10 hours

---

### Option 4: Manual Download (LAST RESORT)
**Approach:** Create panduan for user to export data manually

**Feasibility Check:**
- ❌ No "Export CSV" button visible in screenshots
- ❌ 7,527 entries too large for manual copy-paste
- ❌ No bulk export feature apparent

**Conclusion:** NOT VIABLE unless MODI adds export feature

---

## 📊 Data Structure Specification

### Table 1: Main Listing (`companies`)
```python
{
    "nomor": int,                    # Sequential number in listing
    "nama_badan_usaha": str,         # Company name
    "jenis_badan_usaha": str,        # CV, PT, etc.
    "jenis_perizinan": str,          # IUP, IPP, etc.
    "alamat": str,                   # Full address
    "company_id": int,               # Extracted from detail URL
    "detail_url": str,               # Full URL to detail page
    "scraped_at": str                # ISO timestamp
}
```

**Expected Volume:** 7,527 rows

### Table 2: Company Detail (`company_details`)
```python
{
    "company_id": int,
    "nama_badan_usaha": str,
    "kode_badan_usaha": int,
    "jenis_badan_usaha": str,
    "kelurahan": str,
    "npwp": str,
    "rt_rw": str,
    "kode_pos": str,
    "alamat": str,
    "scraped_at": str
}
```

**Expected Volume:** 7,527 rows (1:1 with companies)

### Table 3: Directors (`directors`)
```python
{
    "company_id": int,               # FK to companies
    "nama_direksi": str,
    "mulai_menjabat": str,           # Date or "-"
    "akhir_menjabat": str,           # Date or "-"
    "jabatan": str,                  # Komisaris, Direktur, etc.
}
```

**Expected Volume:** ~20,000 rows (avg 2-3 directors per company)

### Table 4: Shareholders (`shareholders`)
```python
{
    "company_id": int,
    "jenis_kepemilikan": str,        # Badan Usaha, Individu
    "nama": str,
    "kewarganegaraan": str,          # WNI, WNA
    "asal_negara": str,
    "persentase_saham": float
}
```

**Expected Volume:** ~20,000 rows

### Table 5: Permits (IUP/IPP) (`permits`) ⭐ MOST IMPORTANT
```python
{
    "company_id": int,
    "nomor_izin": str,               # IUP number
    "jenis_izin": str,               # IUP, IPP, IUPK, etc.
    "tahun_kedaluarsa": str,
    "golongan": str,                 # Mineral/Coal classification
    "komoditas": str,                # Nickel, Coal, Bauxite, etc.
    "luas_ha": float,                # ⭐ Area in hectares
    "tanggal_berlaku": str,          # Start date
    "tanggal_berakhir": str,         # End date
    "status_cnc": str,               # CNC status
    "lokasi": str,                   # Province/Kabupaten
    "kode_wiup": str                 # WIUP code
}
```

**Expected Volume:** ~15,000-30,000 rows (companies can have multiple permits)

---

## ⏱️ Time Estimation

### Scenario A: API Interception Success (Best Case)
```
1. Reconnaissance (Network inspection)     : 1-2 hours
2. API documentation & testing             : 1-2 hours
3. Script development (listing + detail)   : 2-3 hours
4. Data extraction execution               : 30 minutes
   - Listing: 753 pages × 0.2s = ~2.5 min
   - Detail: 7,527 IDs × 0.3s = ~38 min
5. Data cleaning & export                  : 30 minutes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 5-7 hours (dev) + 1 hour (execution)
```

### Scenario B: Browser Automation Required (Worst Case)
```
1. Script development (Scrapling)          : 4-6 hours
2. Testing & debugging                     : 2-3 hours
3. Data extraction execution               : 3-4 hours
   - Listing: 753 pages × 1s = ~13 min
   - Detail: 7,527 pages × 1.5s = ~3 hours
4. Retry failed pages                      : 1 hour
5. Data cleaning & export                  : 1 hour
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 6-9 hours (dev) + 5-6 hours (execution)
```

### Scenario C: Hybrid (Realistic Estimate)
```
1. API + Scrapling development             : 5-7 hours
2. Execution (mixed methods)               : 1.5-2 hours
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 6.5-9 hours (total)
```

---

## 🎯 Recommendation

### ✅ **GO AHEAD** with **Hybrid Approach (Option 3)**

**Rationale:**
1. **No Cloudflare** - Much easier than BPS!
2. **Large but manageable dataset** - 7.5K entries not impossible
3. **High value data** - Includes IUP permits with luas kawasan (key metric)
4. **Multiple fallbacks** - If API fails, browser automation works
5. **Similar pattern to tanahkita** - We have proven code base

**Execution Plan:**

### Phase 1: Reconnaissance (2 hours)
- [ ] Open MODI portal in Chrome DevTools
- [ ] Inspect Network tab during:
  - [ ] Page load
  - [ ] Pagination (click page 2, 3, etc.)
  - [ ] Detail button click
  - [ ] Search/filter usage (if any)
- [ ] Document all API endpoints found
- [ ] Test API calls in Postman/Insomnia
- [ ] **Decision point:** API viable? → YES = continue, NO = switch to Scrapling

### Phase 2: Development (4-6 hours)
- [ ] Create `tools/scrapling/scripts/scrape_modi_portal.py`
- [ ] Implement listing scraper (API or browser)
- [ ] Implement detail scraper (API or browser)
- [ ] Add pagination handling (753 pages)
- [ ] Add checkpoint/resume feature
- [ ] Add progress bar (tqdm)
- [ ] Add error handling & retries

### Phase 3: Execution (1-2 hours)
- [ ] Run scraper with max_pages=5 (test)
- [ ] Verify data quality
- [ ] Run full scrape (753 pages)
- [ ] Export to CSV/JSON
- [ ] Validate data completeness

### Phase 4: Data Processing (1 hour)
- [ ] Clean & deduplicate
- [ ] Filter for Sulawesi only (if needed)
- [ ] Calculate summary statistics
- [ ] Merge with UMD dataset for validation

---

## ⚠️ Risks & Mitigation

### Risk 1: No API Found (Probability: 30%)
**Impact:** Need full browser automation (slower)
**Mitigation:** 
- Budget extra 3 hours for Scrapling implementation
- Use tanahkita pattern (already proven)
- Add aggressive caching

### Risk 2: Rate Limiting Triggered (Probability: 40%)
**Impact:** IP blocked mid-scrape
**Mitigation:**
- Increase delay to 1.5-2s per request
- Implement exponential backoff
- Save checkpoints every 100 entries
- Use rotating user agents

### Risk 3: Website Structure Changes (Probability: 10%)
**Impact:** Scraper breaks
**Mitigation:**
- Document HTML structure thoroughly
- Add schema validation
- Fail gracefully with clear error messages

### Risk 4: Incomplete Data (Probability: 50%)
**Impact:** Missing permits or details
**Mitigation:**
- Log all failed IDs
- Retry mechanism for errors
- Accept partial data (document limitations)

---

## 📝 Next Action Required

**AWAITING YOUR CONFIRMATION:**

1. **Approve Phase 1 (Reconnaissance)?**
   - Start with 2-hour investigation of API endpoints
   - Report findings before proceeding to development

2. **Data Scope Preference:**
   - **Option A:** Full national data (7,527 companies)
   - **Option B:** Sulawesi only (filter by lokasi field) → ~500-800 companies
   - **Recommendation:** Start full, filter later (easier)

3. **Time Budget:**
   - **Conservative:** 10 hours (includes buffer for issues)
   - **Aggressive:** 6 hours (assumes API success)
   - **Your preference:** _____?

4. **Execution Trigger:**
   - **Now:** Start reconnaissance immediately
   - **After review:** Wait for your feedback first
   - **Your choice:** _____?

**IF APPROVED → I WILL:**
```bash
# Step 1: Manual exploration (you can help!)
# Open https://modi.esdm.go.id/portal in Chrome
# Open DevTools (F12) → Network tab
# Click around, watch for API calls
# Screenshot any JSON responses

# Step 2: I'll analyze your findings
# And decide: API route vs. Browser route

# Step 3: Start coding
cd tools/scrapling/scripts
# Create scrape_modi_portal.py
```

---

## 📖 References for Development

**Similar Patterns:**
- `scrape_tanahkita.py` - Table scraping + pagination
- `scraper_base.py` - Base class with common methods
- `config.yaml` - Configuration template

**Key Differences from TanahKita:**
- ⚠️ JavaScript-rendered (not server-side)
- ⚠️ Nested data (detail page has multiple tables)
- ⚠️ Larger volume (7.5K vs 580 entries)
- ⚠️ Multi-level scraping (listing → detail → sub-tables)

**New Capabilities Needed:**
- API client (if endpoints found)
- Nested table parsing (directors, shareholders, permits)
- ID-based detail fetching (not URL-based pagination)
- Multi-table export (5 separate CSV files)

---

*Assessment created: 10 Juni 2026*  
*Ready for Phase 1 execution pending approval*  
*CELIOS ECC Intelligence System*
