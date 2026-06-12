# Dokumentasi Paper Fondasi ECC
## Świąder et al. (2020) — Environmental Carrying Capacity Assessment

---

**Judul Lengkap:**  
*Environmental Carrying Capacity Assessment—the Policy Instrument and Tool for Sustainable Spatial Management*

**Sumber:**  
Frontiers in Environmental Science | Vol. 8 | Article 579838 | November 2020  
DOI: `10.3389/fenvs.2020.579838`

**Penulis:**  
Małgorzata Świąder (MS), Szymon Szewrański (SS), Jan K. Kazak (JK)  
Wrocław University of Environmental and Life Sciences, Poland

---

## 1. Latar Belakang & Relevansi

Paper ini menjadi **fondasi metodologis utama** proyek *Environmental Carrying Capacity Intelligence System (ECCIS)* CELIOS. Paper ini membangun framework ilmiah untuk mengukur apakah kapasitas lingkungan suatu wilayah masih mampu menopang aktivitas penduduknya.

**Konteks global yang melatarbelakangi:**
- Aktivitas manusia telah mengubah lingkungan "pada skala planet dan dengan kecepatan yang melampaui batas historis" (DellaSala, 2018)
- Saat ini dunia membutuhkan **1.69 bumi** untuk menopang kebutuhan populasi global (Global Footprint Network, 2019)
- Pertumbuhan urban dan urban sprawl memperparah tekanan ekologis pada kawasan peri-urban dan rural

**Area studi paper:**  
Kota Wrocław + zona suburban (11 municipality), Lower Silesia, Polandia  
→ *Analog dalam proyek CELIOS: 38 Provinsi Indonesia*

---

## 2. Konsep Inti: Tiga Pilar ECC

### 2.1 Ecological Footprint (EF)
Total permintaan manusia terhadap alam, dinyatakan dalam **global hectare (gha)**.  
Unit gha memungkinkan perbandingan lintas wilayah dan lintas waktu karena sudah dinormalisasi ke standar produktivitas bumi global.

### 2.2 Carbon Footprint (CF)
Pendekatan **bottom-up** per komponen aktivitas manusia. CF dihitung dengan mengonversi konsumsi/emisi tiap komponen ke dalam unit gha melalui:
1. Konversi ke CO₂ atau CO₂eq
2. Pembagian dengan laju sekuestrasi karbon global (`gha/tCO₂`)
3. Perkalian dengan Equivalence Factor (EQF)

### 2.3 Biocapacity (BC)
Kemampuan alam untuk meregenerasi sumber daya dan menyerap limbah, dihitung dari tutupan lahan menggunakan standar **Global Footprint Network (GFN)**.

---

## 3. Formula Matematika

### Formula 1 — CF Total Per Komponen (Planned Land Use)

```
CF_TiSi = P_Si × CF_i
```

| Simbol | Keterangan | Satuan |
|--------|------------|--------|
| `CF_TiSi` | CF total komponen `i` pada skenario `i` | gha |
| `P_Si` | Jumlah populasi pada skenario `i` | jiwa |
| `CF_i` | CF per kapita komponen `i` | gha/kapita |

**CF per kapita** dihitung dari:
```
CF_i_per_kapita = (konsumsi_per_kapita × faktor_emisi) / (laju_sekuestrasi × EQF)
```

### Formula 2 — Biocapacity (BC)

```
BC = Σ (A_n × YF_n × EQF_n)
```

| Simbol | Keterangan | Satuan |
|--------|------------|--------|
| `BC` | Total Biocapacity | gha |
| `A_n` | Luas tipe lahan ke-`n` | ha |
| `YF_n` | Yield Factor tipe lahan ke-`n` | - (dimensionless) |
| `EQF_n` | Equivalence Factor tipe lahan ke-`n` | - (dimensionless) |

### Formula 3 — Konsumsi Pangan Tertimbang (Weighted Average)

Dikarenakan ketiadaan data konsumsi di level munisipalitas, paper ini menggunakan data rata-rata wilayah (Lower Silesia) yang dibobot berdasarkan ukuran lokalitas (kelas populasi kota/desa).

```
A_Fi = (W_Ln × A_FiLn) + (W_V × A_FnV)
```

| Simbol | Keterangan | Satuan |
|--------|------------|--------|
| `A_Fi` | Konsumsi produk makanan ke-`i` yang disesuaikan (adjusted) | kg/kapita |
| `W_Ln` | Bobot proporsi penduduk di kota (Town/City) | persentase |
| `A_FiLn` | Konsumsi rata-rata produk `i` di kota | kg/kapita |
| `W_V` | Bobot proporsi penduduk di pedesaan (Village) | persentase |
| `A_FnV` | Konsumsi rata-rata produk `i` di pedesaan | kg/kapita |

### Formula 4 — Bobot Populasi Per Kelas Lokalitas

```
W_Ln = I_In / (I_In + I_IV)
```

| Simbol | Keterangan |
|--------|------------|
| `W_Ln` | Bobot kelas kota ke-`n` |
| `I_In` | Jumlah penduduk di kota kelas `n` |
| `I_IV` | Total penduduk di seluruh kota (Towns) dan desa (Villages) di munisipalitas tersebut |

Pendekatan ini sangat krusial untuk CELIOS karena di Indonesia, data konsumsi BPS (Susenas) seringkali hanya akurat di level provinsi/kabupaten, sehingga untuk level yang lebih mikro (kecamatan/desa) memerlukan pembobotan rasio urban-rural seperti ini.

---

## 4. Status ECC — Tiga Kondisi Ekologis

| Kondisi | Syarat | Interpretasi |
|---------|--------|--------------|
| **Ecological Deficit** | EF > BC (atau CF > BC) | Lahan yang tersedia tidak cukup untuk menyerap dampak aktivitas manusia |
| **Ecological Reserve** | BC > EF (atau BC > CF) | Kapasitas alam masih melebihi permintaan |
| **Ecological Balance** | EF / BC = 1 | Titik keseimbangan minimum — kondisi paling rentan |

> "If EF or CF is higher than BC, it represents the state of the environment called an ecological deficit. It reflects insufficient physical area needed to sustain emission related to needs satisfied by the population."

---

## 5. Komponen Carbon Footprint (Bottom-Up, 7 Komponen)

Paper ini mendefinisikan **7 komponen CF** yang dihitung secara terpisah (bottom-up):

| No. | Komponen | Kode | Keterangan |
|-----|----------|------|------------|
| 1 | **Konsumsi Pangan (Food)** | CF_food | Konsumsi pangan per kapita × intensitas karbon per kg produk |
| 2 | **Limbah Cair (Sewage)** | CF_sewage | Volume limbah cair × energi pengolahan |
| 3 | **Persampahan (Garbage)** | CF_garbage | Volume sampah padat × faktor emisi TPA (metana) |
| 4 | **Penggunaan Air (Water Use)** | CF_water | Konsumsi air bersih × energi pengolahan |
| 5 | **Listrik (Electricity)** | CF_elec | Konsumsi listrik (kWh) × faktor emisi grid |
| 6 | **Gas (Gas Supply)** | CF_gas | Konsumsi LPG/gas kota × faktor emisi |
| 7 | **Mobilitas (Car Use)** | CF_mobility | Jumlah kendaraan × konsumsi BBM × jarak × faktor emisi |

> "CF of food consumption, CF of sewage/liquid waste generation, CF of garbage/solid waste generation, CF of water use, CF of electricity use, CF of gas supply; CF of car use."

**Komponen dengan dampak tertinggi** (temuan paper untuk Wrocław):  
Electricity use → komponen penyumbang CF terbesar.

---

## 6. Komponen Biocapacity (5 Tipe Lahan GFN)

Berdasarkan **National Footprint Accounts (NFA)** standar Global Footprint Network:

| No. | Tipe Lahan | Keterangan |
|-----|------------|------------|
| 1 | **Infrastructure** | Lahan terbangun (permukiman, jalan, industri) |
| 2 | **Forestland** | Hutan produksi dan penyerap karbon |
| 3 | **Grazing land** | Padang penggembalaan |
| 4 | **Croplands** | Lahan pertanian |
| 5 | **Inland fishing grounds** | Perairan darat (sungai, danau, waduk) |

> Untuk wilayah pesisir ditambahkan: **Marine fishing grounds**

Setiap tipe lahan memiliki **Yield Factor (YF)** dan **Equivalence Factor (EQF)** yang berbeda — dikeluarkan oleh GFN setiap tahun dalam publikasi *National Footprint Accounts*.

---

## 7. Zona Lingkungan (Environmental Zones)

Framework ini menambahkan layer **zona pembatas** yang dikurangi dari BC potensial. Langkah ini diotomatisasi menggunakan perangkat lunak **CommunityViz** (ekstensi ArcGIS) untuk menghitung indikator berbasis keruangan.

### Excluded Zones (Zona Terbatas Mutlak)
- **Kawasan Lindung (Protected Areas)** → Tidak boleh dieksploitasi untuk permukiman manusia demi menjaga layanan ekosistem dan keanekaragaman hayati.

### Restricted Zones (Zona Terbatas Bersyarat)
- **Good-quality soils** → Cadangan tanah subur yang disiapkan untuk *urban agriculture* (pertanian perkotaan). Ini penting untuk ketahanan pangan lokal.
- **Flood-risk areas** → Kawasan rawan banjir (berdasarkan probabilitas banjir historis Q 10%).

**Kode Identifikasi Zona (dalam paper):**

| Kode | Isi | Deskripsi Ekologis |
|------|-----|--------------------|
| `P` | Protected areas | Area konservasi alam (Natura 2000, dll) |
| `O` | Good-quality soils | Lahan pertanian produktif yang dilindungi dari konversi perumahan |
| `F` | Flood-risk areas | Area yang dihindari karena risiko bencana |
| `POO` | Protected + Good soils | Kombinasi perlindungan biodiversitas & ketahanan pangan |
| `PSF` | Protected + Good soils + Flood risk | Zona paling ketat (mengurangi ekspansi urban paling drastis) |

---

## 8. Skenario Perencanaan (4 Skenario)

Paper membangun **4 skenario alternatif** untuk mengevaluasi kebijakan tata ruang:

| Skenario | Kode | Zona yang Dikecualikan |
|----------|------|------------------------|
| **Base Scenario** | P | Hanya penggunaan lahan saat ini |
| **Scenario 1** | PO | + Protected areas |
| **Scenario 2** | PS | + Protected + Good soils |
| **Scenario 3** | PF | + Protected + Flood-risk |
| **Scenario 4** | PSF | + Protected + Good soils + Flood-risk (terlengkap) |

**Temuan kunci skenario (Berdasarkan Ekstraksi PageIndex GPT-5.1):**
- Perlindungan **Good-quality soils** (tanah pertanian) memiliki efek paling drastis dalam mencegah lonjakan CF dibanding pembatasan perlindungan alam atau banjir.
- Skenario PSF memberikan penurunan area permukiman terencana tertinggi yang berkorelasi dengan penurunan ekspansi CF masa depan, khususnya di wilayah dominan pertanian (Zórawina −62.18%, Kobierzyce −34%).
- Bahkan perubahan kecil pada BC (< +0.01%) akibat perlindungan zona-zona ini memberikan dampak nyata pada pengurangan total defisit ekologis.

---

## 9. Alat & Data yang Digunakan

Paper ini sangat menekankan pentingnya integrasi resolusi tinggi seperti *Digital Elevation Models (DEMs)* dan LiDAR dalam pemodelan lingkungan.

| Komponen | Sumber Data (Polandia) | Analog Indonesia untuk CELIOS |
|----------|------------------------|-------------------------------|
| **Populasi** | GUS (Badan Statistik Nasional) | **BPS Indonesia (Sensus/Susenas)** |
| **Konsumsi Pangan** | Data pengeluaran rumah tangga regional | **Susenas BPS (Modul Konsumsi)** |
| **Limbah Cair** | MPWiK Wrocław (PDAM/Sanitasi lokal) | **Dinas LHK / PDAM / BPS** |
| **Sampah Padat** | Laporan tahunan TPA munisipalitas | **SIPSN KLHK** |
| **Listrik** | Laporan agregat penyedia listrik | **Statistik PLN** |
| **Gas** | Data distribusi operator jaringan gas | **Pertamina / PGN / BPH Migas** |
| **Mobilitas** | Database registrasi kendaraan lokal | **Korlantas Polri / BPS Transportasi** |
| **Tutupan Lahan** | CLC 2018 (Corine Land Cover - Copernicus) | **Peta Penutupan Lahan KLHK / BIG** |
| **Kawasan Lindung**| Jaringan Natura 2000 Eropa | **SK Kawasan Konservasi KLHK** |
| **Rawan Banjir** | Państwowe Gospodarstwo Wodne (Otoritas Air) | **Peta Risiko Bencana BNPB / Inarisk** |
| **YF & EQF** | Global Footprint Network (GFN) NFA | **GFN NFA — Data per negara** |

**Analisis Spasial & Otomasi:**  
Pemrosesan dilakukan di **ArcGIS** menggunakan ekstensi **CommunityViz** dengan modul *Calculation Variables (CV)*. Modul ini memungkinkan pengguna untuk mendefinisikan persamaan secara dinamis dan mengotomatisasi kalkulasi serta visualisasi perubahan tata guna lahan tanpa memerlukan software tambahan.  
→ *Analog CELIOS: Kita akan menggunakan Python (Geopandas/Rasterio) dikombinasikan dengan Streamlit + Plotly/DeckGL.*

---

## 10. Temuan Utama (Wrocław Case Study)

| Metrik | Nilai |
|--------|-------|
| Populasi *Current* -> *Planned* | **807.503 jiwa** -> **1.392.297 jiwa** |
| Radius Ekologis (Spatial extent) | **107,8 km** melebar ke **141,4 km** |
| CF total Wrocław + suburban | **3.652.211 gha** (naik 72% di Base Scenario) |
| CF per kapita | **4,523 gha/kapita** |
| Komposisi CF Terbesar | **Listrik (66,6%)**, **Mobilitas (16,8%)**, **Pangan (6,4%)** |
| "Earths needed" (study area) | **2,77 bumi** |
| "Earths needed" (rata-rata Polandia) | 2,72 bumi |
| Area hutan dibutuhkan untuk menyerap CF | ~2 juta ha (≈ luas Lower Silesia) |

**Defisit Ekologis Tambahan** jika semua rencana tata ruang (Base Scenario) diimplementasikan secara penuh:
Kenaikan total CF mencapai **6.275.076 gha** (+72%). Menariknya, meskipun persentase pertumbuhan CF kota Wrocław lebih kecil dibanding wilayah sub-urbannya (hanya tumbuh 55%), namun karena populasi asalnya sangat padat, kota Wrocław menyumbang **75% dari total defisit ekologis** seluruh regional tersebut.

---

## 11. Kontribusi Ilmiah Paper

1. **Framework ECC terintegrasi** yang menggabungkan CF (demand) + BC (supply) + Environmental Zones
2. **Pendekatan bottom-up** yang memungkinkan kalkulasi di level lokal tanpa harus menunggu data nasional
3. **Scenario modeling** untuk mendukung pengambilan kebijakan tata ruang berbasis bukti
4. **Replicability** — metodologi eksplisit dinyatakan dapat diterapkan di zona suburban lain dengan penyesuaian variabel lokal

> "The proposed approach would allow to add or delete variables in order to reflect local socio-environmental conditions."

---

## 12. Limitasi yang Diakui Paper

- Data spasial (peta) tidak selalu tersedia dalam format digital → butuh vektorisasi manual
- Data konsumsi lokal sering tidak ada → harus menggunakan rata-rata regional/nasional (dengan pembobotan populasi)
- Analisis membutuhkan keahlian tinggi dari analis GIS
- Asumsi: kebiasaan hidup populasi tidak berubah (lifestyle statis)

---

## 13. Implikasi Langsung untuk Proyek CELIOS ECC

### Mapping Metodologi → Implementasi Indonesia

```
Paper (Wrocław)                    CELIOS ECC (38 Provinsi Indonesia)
─────────────────────────────────────────────────────────────────────
11 municipality          →         38 provinsi
CLC 2018 (Copernicus)    →         Peta tutupan lahan KLHK + BIG
GUS (statistik nasional) →         BPS WebAPI + Susenas
Natura 2000              →         SK Kawasan Konservasi KLHK
Flood Q10%               →         Peta Risiko Banjir BNPB
GFN YF & EQF Polandia    →         GFN NFA Indonesia (perlu akses)
ArcGIS CV                →         Python + Altair/Plotly + Streamlit
4 skenario tata ruang    →         3 skenario: Baseline / +Lindung / +Bencana
```

### Kolom Data CSV yang Diperlukan (berdasarkan metodologi paper)

```python
# provinsi_ecc.csv — 38 baris
columns = [
    "Provinsi",
    # Carbon Footprint per komponen (gha/kapita)
    "cf_pangan_per_kapita", "cf_limbah_per_kapita", "cf_sampah_per_kapita",
    "cf_air_per_kapita", "cf_listrik_per_kapita", "cf_gas_per_kapita",
    "cf_mobilitas_per_kapita",
    # CF total
    "cf_total_per_kapita",   # = Σ semua komponen
    "cf_total_gha",          # = cf_total_per_kapita × populasi
    # Biocapacity per tipe lahan (gha)
    "bc_hutan", "bc_lahan_pertanian", "bc_padang",
    "bc_perikanan_darat", "bc_perikanan_laut",
    "bc_total",              # = Σ(A_n × YF_n × EQF_n)
    "bc_per_kapita",
    # Status ECC
    "defisit_gha",           # = cf_total_gha - bc_total (+: defisit, -: reserve)
    "defisit_per_kapita",
    "rasio_ecc",             # = cf_total / bc_total (>1: defisit)
    "jumlah_bumi",           # = cf_total_per_kapita / 1.8 (biocapacity per kapita bumi)
    # Populasi
    "populasi_2023", "populasi_2022",
    # Luas lahan per tipe (ha) — input BC
    "luas_hutan_ha", "luas_lahan_ha", "luas_padang_ha",
    "luas_perikanan_darat_ha", "luas_perikanan_laut_ha",
    # Zona terbatas (ha)
    "luas_kawasan_lindung_ha", "luas_rawan_banjir_ha",
    "luas_lahan_pertanian_strategis_ha",
]
```

### Faktor GFN yang Dibutuhkan (Indonesia)

| Parameter | Nilai Indonesia (estimasi GFN 2023) | Sumber |
|-----------|-------------------------------------|--------|
| YF Forestland | ~0.87 | GFN NFA Indonesia |
| YF Cropland | ~0.82 | GFN NFA Indonesia |
| YF Grazing | ~0.76 | GFN NFA Indonesia |
| YF Fisheries | ~0.91 | GFN NFA Indonesia |
| EQF Forest | ~1.26 | GFN (global standard) |
| EQF Cropland | ~2.51 | GFN (global standard) |
| EQF Grazing | ~0.46 | GFN (global standard) |
| EQF Fisheries | ~0.37 | GFN (global standard) |
| EQF Built-up | ~2.51 | GFN (global standard) |

> ⚠️ Nilai di atas adalah estimasi. Nilai resmi per negara tersedia di GFN National Footprint Accounts (berbayar). Nilai open-access tersedia untuk level nasional di publikasi GFN.

---

## 14. Kutipan Kunci untuk Referensi

> "The ecological limits assessed with carrying capacity as the benchmark allowed to quantify the human impact and the level that could be sustained by the environment."

> "To be sustainable, mankind's activity must respect the ecological limitations of planet Earth."

> "The application of such solutions allows national, regional and local economies to adapt to climate change and protect various sectors of the national economy."

> "This research could be applicable in other suburban zones with the same or different land-use and socio-demographic dynamics. The approach could be changed according to land-use conditions of a given area."

---

## 15. Referensi Terkait dalam Folder Proyek

| File | Relevansi |
|------|-----------|
| `Ref-Luar/fenvs-08-579838.pdf` | **Paper ini sendiri** (fondasi utama) |
| `Ref-Luar/ijerph-20-02370.pdf` | Kemungkinan terkait environmental health / EF urban |
| `Ref-Luar/sustainability-14-04416-v2.pdf` | Kemungkinan terkait sustainability assessment |
| `Ref-indo/sustainability-15-05791.pdf` | **Penting:** kemungkinan berisi GFN factors untuk Indonesia |
| `Ref-indo/Subekti_2018_IOP_Conf.pdf` | Daya dukung lingkungan konteks Indonesia (2018) |
| `data/ECC_Lampiran_Teknis_2_dataset mining.xlsx` | Spesifikasi 48 variabel yang sudah disesuaikan dengan framework paper ini |

---

*Dokumen ini dibuat berdasarkan pembacaan penuh paper Świąder et al. (2020), fenvs-08-579838.*  
*Dibuat untuk keperluan internal riset CELIOS Environmental Intelligence System.*  
*Last updated: Mei 2026*
