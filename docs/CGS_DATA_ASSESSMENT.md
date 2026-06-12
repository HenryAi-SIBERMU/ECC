# CGS Dataset Assessment: Sumber Data untuk Kapasitas & Investasi

> **CELIOS ECC Intelligence System**  
> **Created:** 11 Juni 2026  
> **File:** CGS_Nickel_Smelter_Dataset_V1.xlsx

---

## ✅ HASIL ANALISIS: CGS Dataset SANGAT BAGUS!

### 📊 Data yang Tersedia di CGS:

| Data Type | Column Name | Coverage | Quality |
|-----------|-------------|----------|---------|
| **✅ Kapasitas Input** | Input Capacity (Tonnes) | 79/106 (74.5%) | 🟢 Excellent |
| **✅ Kapasitas Output** | Output Capacity (Tonnes) | 92/106 (86.8%) | 🟢 Excellent |
| **✅ Ni Equivalent** | Ni metal equivalent (tonnes) | 47/106 (44.3%) | 🟡 Good |
| **✅ Company Name** | Smelter Name | 106/106 (100%) | 🟢 Perfect |
| **✅ Location** | Province | 106/106 (100%) | 🟢 Perfect |
| **✅ Coordinates** | Latitude, Longitude | 106/106 (100%) | 🟢 Perfect |
| **🟡 Investment** | Investor Notes | 39/106 (36.8%) | 🟠 Limited |

---

## 🎯 Data KAPASITAS PRODUKSI: ✅ TERSEDIA

### 1. **Input Capacity (Tonnes)** - Ore Input
- **Coverage:** 74.5% (79 dari 106 smelters)
- **Range:** 70,000 - 21,600,000 tonnes/year
- **Average:** 3,378,265 tonnes/year
- **Format:** Numeric, siap pakai

**Contoh Data:**
- Adhikara Cipta Mulia: **2,401,920 tonnes/year**
- ANTAM Pomalaa RKEF: **1,450,000 tonnes/year**
- ANTAM Feni Haltim RKEF: **1,219,945 tonnes/year**

### 2. **Output Capacity (Tonnes)** - Product Output
- **Coverage:** 86.8% (92 dari 106 smelters)
- **Range:** 3,200 - 2,500,000 tonnes/year
- **Average:** 296,803 tonnes/year
- **Format:** Numeric, siap pakai

**Output Products:**
- FeNi (Ferronickel)
- MHP (Mixed Hydroxide Precipitate)
- NPI (Nickel Pig Iron)

**Contoh Data:**
- Adhikara Cipta Mulia: **76,500 tonnes MHP/year**
- ANTAM Pomalaa RKEF: **90,000 tonnes FeNi/year**
- ANTAM Feni Haltim RKEF: **64,655 tonnes FeNi/year**

### 3. **Ni Metal Equivalent (Tonnes)** - Pure Nickel
- **Coverage:** 44.3% (47 dari 106 smelters)
- **Range:** 800 - 185,000 tonnes/year
- **Average:** 43,300 tonnes Ni/year
- **Format:** Numeric, siap pakai

**Contoh Data:**
- Adhikara Cipta Mulia: **30,400 tonnes Ni/year**
- ANTAM Pomalaa RKEF: **27,000 tonnes Ni/year**
- ANTAM Feni Haltim RKEF: **13,500 tonnes Ni/year**

---

## 💰 Data NILAI INVESTASI: 🟡 TERBATAS

### **Investor Notes Column**
- **Coverage:** 36.8% (39 dari 106 smelters)
- **Format:** Text/narrative (NOT numeric)
- **Content:** Company ownership, investor names, deal notes

**Contoh Data:**
- "ANTAM"
- "Consortium CBL (CATL, Brunp, Lygend)"
- "Nickel Mines bought out Shanghai Decent... for US$527.6 million"

**⚠️ MASALAH:**
- ❌ Tidak ada kolom investasi dalam format USD/IDR yang siap pakai
- ❌ Hanya sebagian punya nilai investasi (embedded in text)
- ❌ Perlu parsing manual untuk extract angka investasi

**💡 REKOMENDASI untuk Investasi:**
1. **Opsi A:** Parse "Investor Notes" column (effort tinggi, hasil terbatas)
2. **Opsi B:** Gunakan **BPS PMDN data** yang sudah didownload (96 rows)
3. **Opsi C:** Request data investasi formal ke BKPM

---

## 🏝️ Coverage SULAWESI: 🟢 EXCELLENT

### Total Smelters di Sulawesi: **63 dari 106** (59.4%)

| Province | Smelters | Sample Capacity (Input) |
|----------|----------|------------------------|
| **Central Sulawesi** | 35 | 2.4M - 1.8M tonnes/year |
| **South East Sulawesi** | 20 | 2.4M - 1.4M tonnes/year |
| **South Sulawesi** | 8 | Data available |
| **TOTAL SULAWESI** | **63** | Majority covered |

**Contoh Smelters Sulawesi:**
- Adhikara Cipta Mulia (South East): 2,401,920 tonnes input
- ANTAM Pomalaa (South East): 1,450,000 tonnes input
- Ang And Fang Brother (South East): 1,866,510 tonnes input
- Anugrah Tambang Sejahtera (South East): 1,440,000 tonnes input
- Artha Mining Industry (Central): 2,000,000 tonnes input

---

## 🔗 Matching dengan MinerbaOne: FEASIBLE

### Kolom untuk Matching:

| CGS Column | MinerbaOne Column | Match Method |
|------------|-------------------|--------------|
| **Smelter Name** | `nama` (from details.csv) | Fuzzy string matching |
| **Province** | `lokasi_perizinan` | Exact or contains |
| **Regency** | `lokasi_perizinan` | Extract kabupaten |

**Contoh Matching:**
```
CGS: "ANTAM Pomalaa RKEF" 
  Province: "South East Sulawesi"
  Regency: "Kolaka Regency"
  
MinerbaOne: "PT Aneka Tambang (Persero) Tbk"
  Lokasi: "KAB. KOLAKA, SULAWESI TENGGARA"
  Komoditas: "Nikel"
  
→ MATCH! Add capacity: 1,450,000 tonnes input / 90,000 tonnes output
```

---

## 📋 REKOMENDASI FINAL

### ✅ Gunakan CGS Dataset untuk KAPASITAS PRODUKSI

**Langkah-langkah:**
1. ✅ Extract CGS data (DONE - file: `output/cgs_dataset_extracted.csv`)
2. ⏳ Match CGS smelters dengan MinerbaOne permits
   - By company name (fuzzy matching)
   - By location (province + regency)
3. ⏳ Add capacity columns ke MinerbaOne data:
   - `capacity_input_tonnes`
   - `capacity_output_tonnes`
   - `ni_metal_equivalent_tonnes`
4. ⏳ Flag confidence level:
   - `high`: Exact name + location match
   - `medium`: Fuzzy name match only
   - `low`: Location match only

**Estimasi Coverage setelah Merge:**
- MinerbaOne nickel permits: **399** 
- CGS nickel smelters: **106**
- Expected match rate: **70-80%** (75-85 smelters)
- Coverage untuk analisis: **SUFFICIENT**

---

### 🟡 Untuk NILAI INVESTASI: Gunakan BPS PMDN

**Alasan:**
- ❌ CGS data investasi terbatas (36.8%) dan format text
- ✅ BPS PMDN data sudah ada (96 rows, per provinsi)
- ✅ Bisa alokasi investasi ke smelter proporsional by capacity

**Langkah-langkah:**
1. ✅ Read BPS PMDN data (already downloaded)
2. ⏳ Filter untuk sektor Mining & Quarrying
3. ⏳ Allocate provinsi investment ke individual smelters
4. ⏳ Proportional by capacity:
   ```
   Smelter Investment = (Smelter Capacity / Total Provincial Capacity) × Provincial Investment
   ```

---

## 🎯 KESIMPULAN

### Untuk Pertanyaan: "Kapasitas dan Investasi diambil dari mana?"

**JAWABAN:**

1. **✅ KAPASITAS PRODUKSI** → **Gunakan CGS Dataset**
   - Coverage: 74-87% excellent
   - Format: Numeric, siap pakai
   - Match dengan MinerbaOne by name + location
   - **RECOMMENDED: YES**

2. **🟡 NILAI INVESTASI** → **Gunakan BPS PMDN Data**
   - CGS terbatas (36.8%, format text)
   - BPS PMDN lebih complete (per provinsi)
   - Allocate proportional by capacity
   - **RECOMMENDED: Use BPS, not CGS**

---

## 📊 Expected Final Dataset

```csv
company_name,permit_number,province,commodity,area_ha,capacity_input_tonnes,capacity_output_tonnes,ni_equivalent_tonnes,investment_usd,data_source
PT Aneka Tambang,IUP-xxx,Sulawesi Tenggara,Nikel,1975.00,1450000,90000,27000,150000000,minerbaone+cgs+bps
PT Adhikara Cipta,IUP-yyy,Sulawesi Tenggara,Nikel,2000.00,2401920,76500,30400,200000000,minerbaone+cgs+bps
```

**Columns from:**
- MinerbaOne: company, permit, province, commodity, area
- CGS: capacity_input, capacity_output, ni_equivalent
- BPS PMDN: investment (allocated)

---

*Assessment created: 11 Juni 2026*  
*CELIOS ECC Intelligence System*
