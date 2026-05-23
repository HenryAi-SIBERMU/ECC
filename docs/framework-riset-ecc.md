# Framework Riset — CELIOS ECC Dashboard
## Environmental Carrying Capacity Intelligence System (ECCIS)

> **Referensi Metodologi Utama:** Świąder et al. (2020), *fenvs-08-579838*  
> **Konteks Lokal:** 38 Provinsi Indonesia | Baseline Year: 2023  
> **Dokumen terkait:** `docs/paper-fondasi-ecc-swiader2020.md`

---

## 1. Tujuan Riset

Mengukur apakah kapasitas lingkungan hidup setiap provinsi Indonesia masih mampu  
menopang aktivitas dan konsumsi penduduknya — dinyatakan dalam tiga kondisi ekologis:

| Kondisi | Syarat | Implikasi Kebijakan |
|---------|--------|---------------------|
| **Ecological Deficit** | CF > BC | Butuh intervensi segera |
| **Ecological Reserve** | BC > CF | Kapasitas masih aman |
| **Ecological Balance** | CF / BC = 1 | Titik kritis minimum |

**Tiga narasi riset utama** (analog dengan EBT):

| # | Narasi Riset | Pertanyaan Riset |
|---|-------------|------------------|
| 1 | **Jejak Karbon Sektoral** | Sektor aktivitas manakah yang paling besar menyumbang tekanan ekologis per provinsi? |
| 2 | **Defisit Ekologis** | Seberapa besar kesenjangan antara daya dukung alam dan beban aktivitas manusia antar provinsi? |
| 3 | **Indeks Kerentanan Lingkungan (IKL)** | Provinsi mana yang paling rentan terhadap krisis daya dukung lingkungan hidup? |

---

## 2. Kerangka Metodologi (Berbasis Świąder et al. 2020)

### 2.1 Formula Inti

```
CF_total = Σ CF_komponen_i                     (7 komponen demand)

CF_per_komponen = Populasi × CF_per_kapita_i

CF_per_kapita_i = (Konsumsi_i × Faktor_Emisi_i) / (Laju_Sekuestrasi × EQF)

BC = Σ (Luas_n × YF_n × EQF_n)               (5 tipe lahan supply)

ECC_Status = CF_total - BC_total
  > 0 : Ecological Deficit
  < 0 : Ecological Reserve
  = 0 : Ecological Balance

Rasio_ECC    = CF_total / BC_total
Jumlah_Bumi  = CF_per_kapita / 1.8            (gha/kapita bumi global)
```

### 2.2 Alur Kalkulasi (Pipeline)

```
[Sumber Data] → [Scraping/API] → [Normalisasi] → [Kalkulasi CF+BC] → [CSV] → [Dashboard]

BPS WebAPI ────────────────┐
PLN Statistik ─────────────┤
Pertamina/PGN ─────────────┤
SIPSN KLHK ────────────────┤──→ prepare_data.py ──→ provinsi_ecc.csv
SAMSAT/BPS Kendaraan ──────┤                         nasional_summary.csv
KLHK Tutupan Lahan ────────┤
BNPB Risiko Banjir ────────┤
GFN Factors (konstan) ─────┘
```

---

## 3. Kebutuhan Dataset — 48 Variabel per Sumber

### Sektor 1: Ketahanan Pangan & Jejak Karbon Konsumsi Makanan

| No | Variabel | Simbol | Kategori | Sumber Indonesia | Metode Akuisisi |
|----|----------|--------|----------|-----------------|-----------------|
| 1 | Jumlah penduduk | I_N | Sosial | BPS (Sensus/Dukcapil) | **BPS WebAPI** → `subject/12` |
| 2 | Konsumsi pangan per kapita | A_F | Sosial | BPS Susenas | **BPS WebAPI** → Susenas table |
| 3 | Ekuivalen CO₂ per kg/l produk | I_CO2 | Biofisik | BRIN / Universitas (LCA) | Publikasi/Paper (hardcode) |
| 4 | EQF lahan hutan | EQF | Biofisik | Global Footprint Network | **Konstanta GFN** (hardcode) |
| 5 | Laju sekuestrasi CO₂ global | Is_CO2 | Biofisik | Global Footprint Network | **Konstanta GFN** (hardcode) |

**Formula CF_pangan:**
```
CF_food = I_N × A_F × I_CO2 / (Is_CO2 × EQF_forest)
```

---

### Sektor 2: Sanitasi & Pengelolaan Air Limbah

| No | Variabel | Simbol | Sumber | Metode |
|----|----------|--------|--------|--------|
| 6 | Jumlah penduduk | I_N | BPS | BPS WebAPI |
| 7 | Jumlah limbah tahunan per penduduk | A_S | SNI KemenPUPR | Regulasi (hardcode SNI) |
| 8 | Listrik pengolahan & pompa | A_SEL | PDAM / IPAL | Estimasi teknis (SNI) |
| 9 | Emisi CO₂ per GWh | I_ELCO2eq | PLN (Faktor Emisi Grid) | **Scrape PLN Statistik** |
| 10 | EQF + Sekuestrasi | EQF, Is | GFN | Konstanta |

**Formula CF_sewage:**
```
CF_sewage = I_N × A_S × A_SEL × I_ELCO2eq / (Is_CO2 × EQF_forest)
```

---

### Sektor 3: Pengelolaan Sampah & Emisi Tempat Pembuangan

| No | Variabel | Simbol | Sumber | Metode |
|----|----------|--------|--------|--------|
| 11 | Jumlah fraksi sampah RT | A_Gbn | SIPSN KLHK | **Scrape SIPSN** → `sipsn.menlhk.go.id` |
| 12 | Jumlah sampah campuran tahunan | - | Dinas LH / TPA | SIPSN KLHK |
| 13 | Emisi tCO₂ per ton sampah | I_GbnCO2eq | KLHK / IPCC | Faktor Emisi KLHK (hardcode) |
| 14 | EQF + Sekuestrasi | EQF, Is | GFN | Konstanta |

**Formula CF_garbage:**
```
CF_garbage = A_Gbn × I_GbnCO2eq / (Is_CO2 × EQF_forest)
```

---

### Sektor 4: Akses & Konsumsi Air Bersih

| No | Variabel | Simbol | Sumber | Metode |
|----|----------|--------|--------|--------|
| 15 | Jumlah penduduk | I_N | BPS | BPS WebAPI |
| 16 | Rata-rata penggunaan air tahunan | A_W | PDAM | **Scrape BPS** / Perpamsi |
| 17 | Listrik untuk produksi & pasokan air | A_WEL | PDAM | Estimasi SNI |
| 18 | Emisi CO₂ per GWh | I_ELCO2eq | PLN | Faktor Emisi Grid PLN |
| 19 | EQF | EQF | GFN | Konstanta |

---

### Sektor 5: Konsumsi Energi Listrik & Emisi Pembangkit

| No | Variabel | Simbol | Sumber | Metode |
|----|----------|--------|--------|--------|
| 20 | Jumlah penduduk | I_N | BPS | BPS WebAPI |
| 21 | Rata-rata penggunaan listrik tahunan | A_EL | PLN | **Scrape PLN Statistik** / ESDM |
| 22 | Emisi CO₂ per GWh | I_ELCO2eq | PLN | Faktor Emisi Grid PLN |
| 23 | EQF lahan hutan | EQF | GFN | Konstanta |
| 24 | Sekuestrasi CO₂ global | Is_CO2 | GFN | Konstanta |

**Formula CF_electricity:**
```
CF_elec = I_N × A_EL × I_ELCO2eq / (Is_CO2 × EQF_forest)
```

---

### Sektor 6: Konsumsi Gas & LPG Rumah Tangga

| No | Variabel | Simbol | Sumber | Metode |
|----|----------|--------|--------|--------|
| 25 | Jumlah penduduk | I_N | BPS | BPS WebAPI |
| 26 | Rata-rata konsumsi gas tahunan | A_G | Pertamina / PGN | **Scrape ESDM** / laporan Pertamina |
| 27 | Nilai kalor gas [GJ/m³] | I_CV | ESDM / Lemigas | Publikasi ESDM (hardcode) |
| 28 | Emisi kgCO₂ per GJ gas | I_GCO2eq | IPCC / KLHK | IPCC Tier 1 (hardcode) |
| 29 | EQF & Sekuestrasi | EQF, Is | GFN | Konstanta |

**Formula CF_gas:**
```
CF_gas = I_N × A_G × I_CV × I_GCO2eq / (Is_CO2 × EQF_forest)
```

---

### Sektor 7: Transportasi & Emisi Kendaraan Bermotor

| No | Variabel | Simbol | Sumber | Metode |
|----|----------|--------|--------|--------|
| 30 | Jumlah kendaraan terdaftar | C_N | SAMSAT / BPS | **BPS WebAPI** → Tabel Kendaraan |
| 31 | Konsumsi BBM tahunan per mobil | A_F | ESDM | Laporan ESDM / Buku Putih |
| 32 | Faktor konversi energi BBM | F_F | Pertamina | Standar IPCC (hardcode) |
| 33 | Rata-rata emisi kgCO₂ per km | I_KCO2eq | Pusjatan | Studi emisi kendaraan (hardcode) |
| 34 | EQF & Sekuestrasi | EQF, Is | GFN | Konstanta |

**Formula CF_mobility:**
```
CF_mobility = C_N × A_F × F_F × I_KCO2eq / (Is_CO2 × EQF_forest)
```

---

### Daya Pulih Ekosistem: Biokapasitas Lahan & Perairan (BC)

| No | Variabel | Simbol | Sumber | Metode |
|----|----------|--------|--------|--------|
| 35 | Luas area per tipe lahan | A_n | KLHK / BIG | **Scrape KLHK** / BIG |
| 36 | Yield Factor per tipe lahan | YF_n | GFN | Konstanta per negara |
| 37 | Equivalence Factor | EQF_n | GFN | Konstanta global |
| 38 | Rencana penggunaan lahan | RTRW | Studi Lahan / ATR BPN | Dokumen RTRW (opsional) |

**Formula BC:**
```
BC = Σ(A_n × YF_n × EQF_n)   untuk n = {hutan, lahan, padang, perikanan}
```

---

### Kawasan Perlindungan & Zonasi Ekologis

| No | Variabel | Simbol | Sumber | Metode |
|----|----------|--------|--------|--------|
| 39 | Area Lindung (P) | P | KLHK Kawasan Hutan | **API KLHK** / GIS download |
| 40 | Danau & Sungai lindung | - | PUPR / BIG | BIG Geoportal |
| 41 | Peta kesesuaian lahan pertanian (S) | S | Kementan (Agroekologi) | Kementan GIS |
| 42 | Area Risiko Banjir Q10% (F) | F | BNPB | **BNPB InaRisk API** |
| 43 | Batas wilayah spasial | - | BIG | BIG Ina-Geoportal |

---

### Kesejahteraan Sosial & Ekonomi Hijau

| No | Variabel | Simbol | Sumber | Metode |
|----|----------|--------|--------|--------|
| 44 | PDRB ADHK/ADHB per sektor | PDRB | BPS (Kab Dalam Angka) | **BPS WebAPI** |
| 45 | PDRB Hijau | PDRB_hijau | BPS / KLHK | BPS WebAPI |
| 46 | IPM & Gini Ratio | IPM, Gini | BPS | **BPS WebAPI** |
| 47 | Tenaga kerja sektor SDA | TK_SDA | BPS Sakernas | BPS WebAPI |
| 48 | Konflik lahan | Konflik | NGO / Komnas HAM | Scrape laporan (opsional) |

---

## 4. Peta Sumber Data & Metode Akuisisi

### 4.1 BPS WebAPI — Data Primer Utama

**URL Base:** `https://webapi.bps.go.id/v1/api/`  
**Auth:** API Key (gratis, daftar di webapi.bps.go.id)  
**Konfigurasi:** `.env` → `BPS_API_KEY`

| Data | Endpoint / Subject | Variabel ECC |
|------|--------------------|-------------|
| Populasi per provinsi | `subject/12` | I_N (semua komponen) |
| Konsumsi pangan (Susenas) | `subject/28` | A_F (Pangan) |
| Kendaraan bermotor | `subject/17` | C_N (Mobilitas) |
| PDRB per sektor | `subject/52` | Welfare |
| IPM | `subject/26` | Welfare |
| Gini Ratio | `subject/23` | Welfare |

```python
# Contoh fetch BPS
import requests, os
def fetch_bps(subject_id: int) -> dict:
    url = f"https://webapi.bps.go.id/v1/api/list/model/data/domain/0000/var/{subject_id}/key/{os.getenv('BPS_API_KEY')}"
    return requests.get(url, timeout=30).json()
```

---

### 4.2 PLN Statistik — Konsumsi Listrik

**Sumber:** Laporan Statistik PLN tahunan (PDF → tabel provinsi)  
**URL:** `https://web.pln.co.id/stakeholder/laporan-keuangan-dan-statistik`  
**Metode:** PDF parsing dengan `pdfplumber` atau scrape tabel HTML

| Data | Variabel ECC |
|------|-------------|
| Konsumsi listrik per provinsi (GWh) | A_EL (Listrik) |
| Faktor Emisi Grid (kg CO₂/kWh) | I_ELCO2eq |

---

### 4.3 SIPSN KLHK — Data Persampahan

**URL:** `https://sipsn.menlhk.go.id/sipsn/public/data/timbulan`  
**Metode:** Scrape tabel HTML dengan `requests` + `BeautifulSoup`  
**Data tersedia:** Timbulan sampah per kota/provinsi (ton/hari)

```python
# Contoh scrape SIPSN
from bs4 import BeautifulSoup
import requests
def fetch_sipsn_waste() -> list:
    url = "https://sipsn.menlhk.go.id/sipsn/public/data/timbulan"
    resp = requests.get(url, timeout=30)
    soup = BeautifulSoup(resp.text, "html.parser")
    # parse tabel → dict per provinsi
```

---

### 4.4 ESDM / Pertamina — Data Gas & BBM

**Sumber:** Buku Statistik ESDM (open PDF)  
**URL:** `https://www.esdm.go.id/id/statistik`  
**Data:** Konsumsi LPG per provinsi, distribusi BBM

---

### 4.5 KLHK — Tutupan Lahan & Kawasan Lindung

**Sumber:** KLHK Portal (SK Menteri Kawasan Hutan + Peta Tutupan Lahan)  
**URL:** `https://geoportal.menlhk.go.id`  
**Metode:** Download shapefile / GeoJSON → hitung luas per provinsi

---

### 4.6 GFN — Yield & Equivalence Factors (Konstanta)

Data ini **tidak perlu scraping** — hardcode sebagai konstanta tetap berdasarkan  
GFN National Footprint Accounts Indonesia (2023):

```python
# data/pipeline/constants.py
GFN_FACTORS = {
    "EQF": {
        "forest":        1.26,
        "cropland":      2.51,
        "grazing":       0.46,
        "fisheries":     0.37,
        "built_up":      2.51,
    },
    "YF_INDONESIA": {
        "forest":        0.87,
        "cropland":      0.82,
        "grazing":       0.76,
        "fisheries":     0.91,
    },
    "SEQUESTRATION_RATE_GHA_PER_TCO2": 0.2295,  # gha/tCO2
    "EARTH_BIOCAPACITY_GHA_PER_CAPITA": 1.8,
    "GRID_EMISSION_FACTOR_KG_CO2_PER_KWH": 0.760,  # PLN 2023 (Faktor Emisi Grid Indonesia)
    "LPG_EMISSION_FACTOR_KG_CO2_PER_KG": 2.983,    # IPCC Tier 1
    "PETROL_EMISSION_FACTOR_KG_CO2_PER_L": 2.313,  # IPCC Tier 1
}
```

---

## 5. Struktur Output CSV

### `data/processed/provinsi_ecc.csv` (38 baris)

```
Provinsi, populasi_2023, populasi_2022, populasi_growth,
cf_pangan, cf_limbah, cf_sampah, cf_air,
cf_listrik, cf_gas, cf_mobilitas,
cf_total, cf_total_per_kapita,
bc_hutan, bc_lahan, bc_padang, bc_perikanan,
bc_total, bc_total_per_kapita,
defisit, defisit_per_kapita, rasio_ecc, jumlah_bumi,
cf_pangan_pct, cf_listrik_pct, cf_mobilitas_pct, cf_sampah_pct,
bc_hutan_pct, bc_lahan_pct,
pdrb_2023, ipm_2023, gini_2023,
luas_kawasan_lindung_ha, luas_rawan_banjir_ha
```

### `data/processed/nasional_summary.csv` (1 baris agregat)

```
cf_total_2023, cf_total_2022, cf_total_growth,
bc_total_2023, bc_total_2022, bc_total_growth,
defisit_2023, defisit_2022, defisit_growth,
rasio_ecc_2023, jumlah_bumi_2023,
provinsi_defisit_count, provinsi_reserve_count,
cf_pangan_nasional, cf_listrik_nasional, cf_mobilitas_nasional, ...
```

---

## 6. Mapping Halaman Dashboard

| Halaman | File | Sumber Data Utama | Analisis |
|---------|------|-------------------|----------|
| **Beranda** | `Dashboard.py` | nasional_summary | KPI cards, chi-square overview |
| **Overview Nasional** | `1_Overview_Nasional.py` | nasional + provinsi | Bar chart CF vs BC, peta choropleth |
| **Jejak Karbon Sektoral** | `2_Jejak_Karbon_Sektoral.py` | provinsi (komponen CF) | Stacked bar per sektor, bubble map |
| **Defisit Ekologis** | `3_Defisit_Ekologis.py` | provinsi (CF vs BC) | Gap analysis, scatter CF×BC |
| **Indeks Kerentanan (IKL)** | `4_Indeks_Kerentanan.py` | provinsi (composite) | MinMaxScaler → IKL ranking |
| **Eksplorasi Data** | `5_Eksplorasi_Data.py` | provinsi | Filter interaktif tabel |
| **Dokumentasi Riset** | `6_Dokumentasi_Riset.py` | docs/ markdown | Render metodologi |
| **Validasi Metode** | `7_Validasi_Metode.py` | OpenAlex API | TF-IDF cosine similarity |
| **Bibliometric** | `8_Bibliometric_Discovery.py` | OpenAlex + CSE | NLP discovery |
| **Visualisasi D3** | `9_Visualisasi_Multidimensi.py` | provinsi | Parallel coordinates |
| **Infografis** | `10_Infografis.py` | provinsi + nasional | Card grid visual |
| **Infografis Summary** | `11_Infografis_Summary.py` | nasional | Summary scorecard |

---

## 7. Metodologi Analisis Per Halaman

### 7.1 Halaman 2 — Jejak Karbon Sektoral
*Analog: Desa Tambang*

- **Chi-Square Test:** Distribusi CF per komponen vs kelompok defisit/reserve  
- **Crosstab:** Komponen dominan × kategori provinsi (Jawa, Sumatera, Kalimantan, dll.)
- **Hipotesis:** H0 = tidak ada asosiasi antara sektor industri dan status ECC provinsi
- **Variabel utama:** `cf_listrik`, `cf_mobilitas`, `cf_pangan` sebagai proksi aktivitas sektoral

### 7.2 Halaman 3 — Defisit Ekologis
*Analog: Gap Potensi EBT*

- **Gap Analysis:** `defisit = cf_total - bc_total`
- **Efisiensi Ekologis:** `efisiensi = (bc_total / cf_total) × 100%`
- **Scatter Plot:** CF (x) vs BC (y), garis diagonal = balance
- **Bubble Chart:** Provinsi dengan ukuran bubble = populasi

### 7.3 Halaman 4 — Indeks Kerentanan Lingkungan (IKL)
*Analog: Ketimpangan Energi (IKE)*

**Komponen IKL (6 indikator):**
```
IKL = w1×norm(rasio_ecc) + w2×norm(defisit_per_kapita) +
      w3×norm(1/bc_per_kapita) + w4×norm(populasi_density) +
      w5×norm(1/ipm) + w6×norm(gini)

Normalisasi: MinMaxScaler → [0,1]
Bobot default: w1=0.25, w2=0.20, w3=0.20, w4=0.15, w5=0.10, w6=0.10
```

---

## 8. Roadmap Implementasi (3 Fase)

Mengikuti roadmap proyek `v1.2.0-Roadmap Environmental Carrying Capacity Intelligence System.pdf`:

### Fase 1 — 2025: Audit Regulasi & Infrastruktur Data
- Pemetaan regulasi DDDTLH (PP No. 22/2021) dan inventarisasi sumber data terbuka
- Pengumpulan data baseline: populasi, konsumsi, tutupan lahan, kawasan lindung
- Penyusunan indikator awal 48 variabel per 38 provinsi
- Output: Laporan audit regulasi + dataset baseline provinsi

### Fase 2 — 2026: Penilaian Teknis (Technical Assessment)
- Kalkulasi Carbon Footprint (CF) per sektor untuk seluruh provinsi
- Kalkulasi Biocapacity (BC) berdasarkan tutupan lahan aktual
- Identifikasi provinsi dalam kondisi defisit vs cadangan ekologis
- Penyusunan Indeks Kerentanan Lingkungan (IKL) komposit
- Output: Peta defisit ekologis nasional + dashboard interaktif

### Fase 3 — 2027: Integrasi Kebijakan & Advokasi
- Korporasi: Scorecard keberlanjutan 15 perusahaan LQ45 (PROPER KLHK + PRISMA)
- Penguatan narasi advokasi: rekomendasi kebijakan per wilayah
- Integrasi dengan dokumen RTRW dan KLHS provinsi
- Output: Policy brief, infografis publik, laporan rekomendasi kebijakan

---

## 9. Catatan Keterbatasan & Asumsi

| Keterbatasan | Penanganan |
|---|---|
| BPS API key belum tersedia | Mock data realistis → ganti dengan live data setelah key aktif |
| GFN YF/EQF berbayar untuk detail provinsi | Pakai nilai nasional Indonesia dari publikasi open-access |
| Data PLN listrik per provinsi tidak di API | Scrape PDF laporan PLN tahunan |
| PDAM data tidak terpusat | Gunakan estimasi SNI standar konsumsi air per kapita |
| Faktor emisi spesifik Indonesia | Gunakan IPCC Tier 1 + faktor emisi grid PLN (0.760 kg CO₂/kWh) |
| Data kendaraan SAMSAT tidak terpusat | BPS → tabel jumlah kendaraan bermotor per provinsi |

---

*Framework ini akan terus diperbarui seiring proses riset berlangsung.*  
*Referensi utama: Świąder et al. (2020) | Roadmap ECC v1.2.0 | Lampiran Teknis 2 (48 variabel)*  
*Dibuat: Mei 2026*
