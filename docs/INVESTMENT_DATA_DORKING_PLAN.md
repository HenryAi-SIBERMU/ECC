# Investment Data Collection Plan - Google Dorking Strategy

> **CELIOS ECC Intelligence System**  
> **Created:** 12 Juni 2026  
> **Target:** Investment data untuk semua tambang nikel Sulawesi (MinerbaOne + CGS)  
> **Method:** Google Dorking + Web Research

---

## 🎯 OBJECTIVE

Mengumpulkan data investasi (capex/project value) untuk **semua perusahaan tambang nikel di Sulawesi** yang terdaftar di:
- **MinerbaOne** (ESDM database - companies dengan IUP)
- **CGS Dataset** (63 smelters di Sulawesi)

**Target Output:** CSV dengan kolom:
```
company, project_name, investment_usd_million, investment_rp_triliun, year, location, province, source, source_url, notes, data_quality
```

---

## ✅ INITIAL FINDINGS (Already Found)

| Company | Investment (USD) | Year | Location | Source |
|---------|------------------|------|----------|--------|
| IMIP (Tsingshan) | $18 billion | 2022 | Morowali | Bloomberg (Luhut) |
| Merdeka Battery | $1.8 billion | 2025 | Morowali | mining.com |
| Indonesia Lithium | $545 million | - | Morowali | AidData |

**File:** `data/processed/investment_nickel_sulawesi_initial.csv`

---

## 📋 TARGET COMPANIES

### Priority 1: Listed Companies (Easiest to Find)

**IDX (Bursa Efek Indonesia):**
1. ✅ **ANTAM** (PT Aneka Tambang Tbk) - Pomalaa, Kolaka
2. ✅ **MBMA** (Merdeka Battery Materials) - Morowali (DONE)
3. **INCO** (Vale Indonesia) - Sorowako, Kolaka

**ASX (Australia):**
4. **Nickel Industries (NIC)** - Hengjaya, Ranger, Oracle (IMIP)

**TWSE (Taiwan):**
5. **Walsin Lihwa** - Walsin Nickel (Sunny Metal Industry)

**China/HK:**
6. **Tsingshan Group** (private) - IMIP multiple projects (PARTIAL DATA)
7. **Lygend Resources** - Projects in Morowali
8. **QMB New Energy** - Tsingshan subsidiary

### Priority 2: Major Private Companies

9. **Central Omega Resources** - CORII RKEF & BF
10. **Ceria Nugraha Indotama** - Merah Putih smelter
11. **Virtue Dragon Nickel Industry (VDNI)** - Cahaya Sultra Indonesia
12. **Shanghai Huadi Industry** - Huadi Nickel-Alloy
13. **Silkroad Nickel** - Multiple projects
14. **Gunbuster Nickel Industry**
15. **Indonesia Guang Ching Nickel**

### Priority 3: Smaller Operators (CGS Data)

16-63. **Remaining 48 companies** from CGS dataset (many without IUP)

---

## 🔍 GOOGLE DORKING STRATEGIES

### Strategy 1: Company Annual Reports

**Query Template:**
```
"[COMPANY NAME]" annual report [YEAR] capex investment nikel nickel Sulawesi PDF
```

**Examples:**
```
"ANTAM" OR "Aneka Tambang" annual report 2020 2021 2022 capex investasi Pomalaa
"Vale Indonesia" annual report 2020 2021 2022 capex investment nickel
"Nickel Industries" annual report 2020 2021 2022 capex IMIP Hengjaya
```

**Expected Sources:**
- Company IR websites
- IDX disclosures
- ASX announcements
- Annual reports (PDF)

### Strategy 2: Press Releases & News

**Query Template:**
```
"[COMPANY NAME]" "investasi" OR "investment" "[AMOUNT]" "miliar" OR "triliun" OR "million" OR "billion" nikel Sulawesi
```

**Examples:**
```
"ANTAM" investasi "triliun rupiah" OR "billion" Pomalaa RKEF 2020 2021 2022
"Central Omega Resources" investment "million" OR "billion" CORII smelter
"Virtue Dragon" OR "VDNI" investasi Morowali smelter
```

**Expected Sources:**
- Company press releases
- News portals (Kontan, Bisnis Indonesia, Jakarta Post)
- Mining industry news

### Strategy 3: Government Publications

**Query Template:**
```
site:go.id "investasi nikel" "[COMPANY]" OR "[LOCATION]" PDF
```

**Examples:**
```
site:esdm.go.id OR site:bkpm.go.id "investasi nikel" Morowali Kolaka filetype:pdf
site:sultengprov.go.id "investasi" "smelter" Morowali
site:sulawesitenggara.go.id "investasi pertambangan" nikel
```

**Expected Sources:**
- ESDM reports
- BKPM investment reports
- Provincial government reports

### Strategy 4: Industry Reports & Research

**Query Template:**
```
"Indonesia nickel" "investment" "[YEAR]" "[LOCATION]" "USD" OR "$" report PDF
```

**Examples:**
```
"Indonesia nickel investment" 2020 2021 2022 Sulawesi "billion" filetype:pdf
"Morowali Industrial Park" investment value USD breakdown
"nickel smelter Indonesia" capex project value Sulawesi
```

**Expected Sources:**
- Mining.com
- S&P Global
- Wood Mackenzie
- USGS reports
- Research institutions

### Strategy 5: Financial Disclosures

**Query Template:**
```
site:idx.co.id OR site:asx.com.au "[COMPANY]" financial statement capex
```

**Examples:**
```
site:idx.co.id "ANTAM" OR "MBMA" laporan keuangan capex
site:asx.com.au "Nickel Industries" financial report capex IMIP
```

### Strategy 6: Company-Specific Websites

**Direct URLs to check:**
```
https://www.antam.com/id/investor-relations
https://merdekacoppergold.com/en/investor-relations
https://nickelindustries.com/investors/
https://www.vale.com/indonesia/en/investors
```

---

## 📊 DATA COLLECTION WORKFLOW

### Phase 1: Listed Companies (Priority 1)
**Time Estimate:** 2-3 hours

For each company:
1. Search annual reports (last 5 years: 2020-2024)
2. Extract capex data from financial statements
3. Look for project-specific breakdowns
4. Check press releases for major announcements
5. Record in CSV with source URLs

**Deliverable:** CSV with 5-8 companies, high data quality

### Phase 2: Major Private Companies (Priority 2)
**Time Estimate:** 3-4 hours

For each company:
1. Google dork with company name + investment keywords
2. Check news articles for investment announcements
3. Look for government reports mentioning the company
4. Search industry reports
5. Record in CSV with data quality notes

**Deliverable:** CSV with 10-15 companies, medium-high quality

### Phase 3: Smaller Operators (Priority 3)
**Time Estimate:** 2-3 hours

For remaining companies:
1. Batch search with location (Morowali, Kolaka, etc.)
2. Use capacity as proxy if no investment data found
3. Mark as "estimated" or "no data available"
4. Aggregate industry reports for regional totals

**Deliverable:** Complete CSV with all 63 CGS companies

### Phase 4: Validation & Gap Filling
**Time Estimate:** 1-2 hours

1. Cross-reference multiple sources
2. Convert all to consistent currency (USD million)
3. Add data quality flags (HIGH/MEDIUM/LOW/ESTIMATED)
4. Fill gaps with capacity-based estimates
5. Add methodology notes

---

## 📁 OUTPUT STRUCTURE

### Primary Output File
```
data/processed/investment_nickel_sulawesi_complete.csv
```

**Columns:**
- `company` - Company name
- `project_name` - Specific project/smelter name
- `investment_usd_million` - Investment in USD million
- `investment_rp_triliun` - Investment in Rp trillion (if available)
- `year` - Year of investment/announcement
- `location` - Kabupaten/city
- `province` - Province name
- `source` - Source of data
- `source_url` - URL to source document
- `notes` - Additional context
- `data_quality` - HIGH/MEDIUM/LOW/ESTIMATED/NO_DATA

### Supporting Documentation
```
docs/INVESTMENT_DATA_SOURCES.md - List of all sources checked
docs/INVESTMENT_DATA_METHODOLOGY.md - How estimates were made
data/processed/investment_nickel_sulawesi_summary.md - Summary stats
```

---

## 🎯 SUCCESS CRITERIA

### Minimum Viable Dataset
- ✅ All Priority 1 companies (5-8) with HIGH quality data
- ✅ 50%+ of Priority 2 companies (5+ out of 10-15) with MEDIUM+ quality
- ✅ Regional totals for major locations (Morowali, Kolaka)

### Ideal Complete Dataset
- ✅ 80%+ coverage of all CGS companies (50+ out of 63)
- ✅ 60%+ with actual reported investment data (not estimates)
- ✅ Multiple sources for major companies (validation)

---

## ⚠️ CHALLENGES & MITIGATIONS

### Challenge 1: Paywalls (Bloomberg, Reuters, etc.)
**Mitigation:**
- Focus on free sources first
- Use snippets from search results
- Check company websites directly
- Look for academic/research papers

### Challenge 2: Data in Chinese
**Mitigation:**
- Use Google Translate on PDFs
- Focus on English financial disclosures
- Check Indonesian sources that cite Chinese companies

### Challenge 3: Private Companies
**Mitigation:**
- Use press releases and news
- Aggregate regional investment totals
- Estimate based on capacity if necessary
- Mark data quality appropriately

### Challenge 4: Outdated Data
**Mitigation:**
- Prioritize 2020-2024 data
- Note year of investment
- Adjust for inflation if needed
- Use most recent available

---

## 🚀 NEXT STEPS

### Immediate (Now)
1. ✅ Save initial findings to CSV (DONE)
2. ✅ Create this dorking plan document (DONE)
3. **Start Phase 1:** Listed companies dorking

### Short-term (Next 2-4 hours)
4. Complete Priority 1 companies (5-8 companies)
5. Start Priority 2 major private companies
6. Build methodology documentation

### Medium-term (Next 1-2 days)
7. Complete Priority 2 companies
8. Tackle Priority 3 smaller operators
9. Validation & gap filling
10. Final CSV compilation

---

## 📝 SEARCH QUERY CHECKLIST

### For Each Company:

- [ ] `"[COMPANY]" annual report 2020 2021 2022 2023 2024 capex`
- [ ] `"[COMPANY]" investasi nikel Sulawesi triliun miliar`
- [ ] `"[COMPANY]" investment nickel Indonesia million billion`
- [ ] `"[COMPANY]" press release investment smelter`
- [ ] `site:idx.co.id "[COMPANY]" laporan keuangan`
- [ ] `site:asx.com.au "[COMPANY]" financial report` (if ASX)
- [ ] `"[COMPANY]" "[LOCATION]" investment project value`
- [ ] `site:go.id "[COMPANY]" investasi nikel`

---

## 🔗 USEFUL RESOURCES

### Company IR Websites
- **ANTAM:** https://www.antam.com/id/investor-relations
- **Merdeka:** https://merdekacoppergold.com/en/investor-relations
- **Vale:** https://www.vale.com/indonesia/en/investors
- **Nickel Industries:** https://nickelindustries.com/investors/

### Data Portals
- **IDX:** https://www.idx.co.id/perusahaan-tercatat/laporan-keuangan-dan-tahunan/
- **ASX:** https://www.asx.com.au/
- **AnnualReports.com:** https://www.annualreports.com/

### News & Industry
- **Mining.com:** https://www.mining.com/
- **Jakarta Globe:** https://jakartaglobe.id/business
- **Kontan:** https://www.kontan.co.id/

---

**Status:** READY TO EXECUTE  
**Owner:** Agent + User  
**Timeline:** 3-5 days for complete dataset  
**Priority:** HIGH - Critical for environmental/health impact analysis

---

*Last Updated: 12 Juni 2026*  
*CELIOS ECC Intelligence System*
