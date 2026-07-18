# Gold Standard Google Dorking Strategy - SLHI 2014-2016

## 🎯 Target
Menemukan publikasi SLHI (Status Lingkungan Hidup Indonesia) atau data IKU tahun 2014-2016 menggunakan teknik dorking advanced.

---

## 📋 Keyword Variations (Lebih Luas)

### Primary Keywords
- "Status Lingkungan Hidup Indonesia"
- "SLHI"
- "Statistik Lingkungan Hidup"
- "Indeks Kualitas Lingkungan Hidup"
- "IKLH"

### Secondary Keywords (Data Specific)
- "indeks kualitas udara"
- "IKU"
- "kualitas udara"
- "PM2.5"
- "PM10"
- "polusi udara"
- "pencemaran udara"

### Document Type Variations
- "publikasi"
- "buku"
- "laporan"
- "statistik"
- "data"
- "ringkasan"

---

## 🔧 Advanced Google Operators

### 1. File Type Operators
```
filetype:pdf
filetype:xlsx
filetype:xls
filetype:csv
filetype:doc
filetype:docx
```

### 2. Site-Specific Operators
```
site:bps.go.id
site:*.bps.go.id (wildcard untuk subdomain)
site:archive.bps.go.id
site:menlhk.go.id
site:kemenlh.go.id
site:ppid.menlhk.go.id (portal PPID)
site:sipsn.menlhk.go.id
site:data.go.id
site:satu-data.go.id
```

### 3. URL Pattern Operators
```
inurl:publikasi
inurl:download
inurl:pdf
inurl:file
inurl:doc
inurl:2014
inurl:2015
inurl:2016
inurl:slhi
inurl:lingkungan
```

### 4. Title Operators
```
intitle:"SLHI"
intitle:"lingkungan hidup"
intitle:"statistik"
intitle:2014
intitle:2015
intitle:2016
```

### 5. Exact Match & Wildcards
```
"Status Lingkungan Hidup Indonesia 2014"
"SLHI * 2014" (wildcard)
"statistik lingkungan hidup" 2014..2016 (range)
```

---

## 🎲 Query Combinations (100+ Variations)

### Tier 1: Exact Document Match
```
1. "Status Lingkungan Hidup Indonesia 2014" filetype:pdf
2. "Status Lingkungan Hidup Indonesia 2015" filetype:pdf
3. "Status Lingkungan Hidup Indonesia 2016" filetype:pdf
4. "SLHI 2014" filetype:pdf site:bps.go.id
5. "SLHI 2015" filetype:pdf site:bps.go.id
6. "SLHI 2016" filetype:pdf site:bps.go.id
7. intitle:"SLHI 2014" filetype:pdf
8. intitle:"SLHI 2015" filetype:pdf
9. intitle:"SLHI 2016" filetype:pdf
```

### Tier 2: Publication Pattern
```
10. inurl:publikasi "lingkungan hidup" 2014 filetype:pdf
11. inurl:publikasi "lingkungan hidup" 2015 filetype:pdf
12. inurl:publikasi "lingkungan hidup" 2016 filetype:pdf
13. site:bps.go.id inurl:pdf "lingkungan hidup" 2014
14. site:bps.go.id inurl:pdf "lingkungan hidup" 2015
15. site:bps.go.id inurl:pdf "lingkungan hidup" 2016
16. "statistik lingkungan hidup indonesia" 2014 -2017 -2018
17. "statistik lingkungan hidup indonesia" 2015 -2017 -2018
18. "statistik lingkungan hidup indonesia" 2016 -2017 -2018
```

### Tier 3: BPS Subdomain Sweep
```
19. site:*.bps.go.id "SLHI" 2014
20. site:*.bps.go.id "SLHI" 2015
21. site:*.bps.go.id "SLHI" 2016
22. site:*.bps.go.id "lingkungan hidup" 2014 filetype:pdf
23. site:*.bps.go.id "lingkungan hidup" 2015 filetype:pdf
24. site:*.bps.go.id "lingkungan hidup" 2016 filetype:pdf
```

### Tier 4: Archive.org Time Machine
```
25. site:web.archive.org "bps.go.id" "SLHI 2014"
26. site:web.archive.org "bps.go.id" "SLHI 2015"
27. site:web.archive.org "bps.go.id" "SLHI 2016"
28. site:web.archive.org "menlhk.go.id" "lingkungan hidup" 2014
29. site:web.archive.org "menlhk.go.id" "lingkungan hidup" 2015
30. site:web.archive.org "menlhk.go.id" "lingkungan hidup" 2016
```

### Tier 5: KLHK/KemenLH Domains
```
31. site:menlhk.go.id "SLHI" 2014 filetype:pdf
32. site:menlhk.go.id "SLHI" 2015 filetype:pdf
33. site:menlhk.go.id "SLHI" 2016 filetype:pdf
34. site:kemenlh.go.id "SLHI" 2014 filetype:pdf
35. site:kemenlh.go.id "SLHI" 2015 filetype:pdf
36. site:kemenlh.go.id "SLHI" 2016 filetype:pdf
37. site:ppid.menlhk.go.id "lingkungan hidup" 2014..2016
```

### Tier 6: Data Portal Indonesia
```
38. site:data.go.id "lingkungan hidup" 2014 filetype:csv
39. site:data.go.id "lingkungan hidup" 2015 filetype:csv
40. site:data.go.id "lingkungan hidup" 2016 filetype:csv
41. site:satu-data.go.id "IKLH" 2014..2016
42. site:satu-data.go.id "kualitas udara" 2014..2016
```

### Tier 7: Third-Party Hosts (Issuu, Scribd, ResearchGate)
```
43. site:issuu.com "lingkungan hidup indonesia" 2014
44. site:issuu.com "lingkungan hidup indonesia" 2015
45. site:issuu.com "lingkungan hidup indonesia" 2016
46. site:scribd.com "SLHI" 2014
47. site:scribd.com "SLHI" 2015
48. site:scribd.com "SLHI" 2016
49. site:researchgate.net "status lingkungan hidup" indonesia 2014
50. site:researchgate.net "status lingkungan hidup" indonesia 2015
51. site:researchgate.net "status lingkungan hidup" indonesia 2016
```

### Tier 8: Academic & Repository
```
52. site:.ac.id "SLHI" 2014 filetype:pdf
53. site:.ac.id "SLHI" 2015 filetype:pdf
54. site:.ac.id "SLHI" 2016 filetype:pdf
55. inurl:repository "lingkungan hidup" indonesia 2014
56. inurl:repository "lingkungan hidup" indonesia 2015
57. inurl:repository "lingkungan hidup" indonesia 2016
58. inurl:eprints "statistik lingkungan" 2014..2016
```

### Tier 9: Specific Data (IKU Focus)
```
59. "indeks kualitas udara" indonesia 2014 filetype:pdf
60. "indeks kualitas udara" indonesia 2015 filetype:pdf
61. "indeks kualitas udara" indonesia 2016 filetype:pdf
62. "IKU" "sulawesi" 2014 site:bps.go.id
63. "IKU" "sulawesi" 2015 site:bps.go.id
64. "IKU" "sulawesi" 2016 site:bps.go.id
65. "kualitas udara" "sulawesi" 2014..2016 filetype:xlsx
```

### Tier 10: Provincial BPS
```
66. site:sulutprov.bps.go.id "lingkungan" 2014..2016
67. site:sultengprov.bps.go.id "lingkungan" 2014..2016
68. site:sulsel.bps.go.id "lingkungan" 2014..2016
69. site:sultraprov.bps.go.id "lingkungan" 2014..2016
70. site:sulbarprov.bps.go.id "lingkungan" 2014..2016
71. site:gorontaloprov.bps.go.id "lingkungan" 2014..2016
```

---

## 🚀 Execution Plan

### Method 1: Google CSE API (RECOMMENDED)
**Kenapa CSE?**
- Bisa scrape hasil lebih banyak (100+ results per query)
- Bisa filter by date range
- Bisa programmatic access
- Rate limit lebih generous

**Setup:**
1. Create Google CSE: https://programmablesearchengine.google.com/
2. Get API Key: https://console.cloud.google.com/apis/credentials
3. Batch execute 70+ queries
4. Parse results & download PDFs

### Method 2: Serpapi (Alternatif)
- API untuk scrape Google hasil
- Bypass CAPTCHA
- Rate limit tinggi

### Method 3: Manual Hybrid
- Execute top 20 queries manual
- Document hasil
- Focus on high-probability sources

---

## 📊 Expected Success Rate

| Tier | Queries | Expected Hit Rate | Priority |
|:---|---:|---:|:---|
| Tier 1 (Exact) | 9 | 40-60% | 🔥 HIGH |
| Tier 2 (Publication) | 9 | 30-50% | 🔥 HIGH |
| Tier 3 (BPS Subdomain) | 6 | 20-40% | 🟡 MEDIUM |
| Tier 4 (Archive.org) | 6 | 30-50% | 🟡 MEDIUM |
| Tier 5 (KLHK) | 7 | 10-30% | 🟡 MEDIUM |
| Tier 6 (Data Portal) | 5 | 10-20% | 🟢 LOW |
| Tier 7 (3rd Party) | 9 | 40-60% | 🔥 HIGH |
| Tier 8 (Academic) | 7 | 20-40% | 🟡 MEDIUM |
| Tier 9 (IKU Specific) | 7 | 30-50% | 🟡 MEDIUM |
| Tier 10 (Provincial) | 6 | 10-30% | 🟢 LOW |

**Overall Expected:** 60-80% chance menemukan minimal 1 SLHI dari 2014-2016.

---

## 🛠️ Tools Needed

1. **Google CSE API** - Primary search engine
2. **Serpapi** - Backup scraper
3. **Archive.org Wayback API** - Time machine access
4. **wget/curl** - Batch download PDFs
5. **pdfplumber** - Extract tables from found PDFs

---

## ✅ Success Criteria

- [ ] Found SLHI 2014 PDF (or equivalent data)
- [ ] Found SLHI 2015 PDF (or equivalent data)
- [ ] Found SLHI 2016 PDF (or equivalent data)
- [ ] Extracted IKU data for 6 Sulawesi provinces
- [ ] Validated data quality
- [ ] Merged with existing 2019-2024 dataset

---

**NEXT STEP:** Setup Google CSE API atau execute Tier 1-2 manually dulu?
