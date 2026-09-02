# BAB II: METODOLOGI ANALISIS KUALITAS LINGKUNGAN DI KAWASAN SMELTER

Dokumen laporan metodologi ini menyajikan kerangka ilmiah, formulasi matematis, prosedur pengolahan data, dan pengujian statistik yang dioperasionalkan pada **Bab 2: Kualitas Lingkungan di Kawasan Smelter** dalam studi Daya Dukung dan Daya Tampung Lingkungan Hidup (D3TLH) Sulawesi periode 2014–2024.

---

## 2.1. Dampak Limbah Tailing: Konsentrasi Smelter vs Indeks Kualitas Air (IKA)

Pengoperasian **778 fasilitas mega-smelter** yang didukung oleh kapasitas **9.825 MW PLTU Captive** meningkatkan intensitas emisi dan beban lingkungan di Pulau Sulawesi. Konversi tutupan hutan mencapai **1.001.654 Hektar**, estimasi timbulan limbah B3/tailing sebesar **20,9 Juta Ton per tahun**, dan rata-rata Indeks Kualitas Air (IKA) tahun 2024 sebesar **59,7**.

> **Sumber Data:** Data Smelter: `sulawesi_esdm_nikel.csv`; Data IKA: `sulawesi_ika_2016_2024.csv`; Data Limbah B3: `sulawesi_limbah_b3_ngo_proxy.csv`; Data Sungai Tercemar: `sulawesi_sungai_tercemar.csv`.

##### Tabel 2.1: Rincian Empiris Konsentrasi Smelter, IKA, Limbah B3, dan Sungai Tercemar per Provinsi (2024)
| Provinsi | Smelter (Unit) | Skor IKA | Limbah B3 (Ton/Thn) | Sungai Tercemar | Daftar Sungai / Pesisir Terdampak |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Sulawesi Tengah** | 344 | 62.1 | 12,000,000 | 4 | Sungai Bahodopi, Laroenai, Morowali, Pesisir Fatufia |
| **Sulawesi Tenggara** | 262 | 65.3 | 7,700,000 | 3 | Sungai Lasolo, Sungai Lalindu, Sungai Konaweha |
| **Sulawesi Selatan** | 111 | 58.5 | 1,000,000 | 1 | Pesisir dan Sungai Bantaeng |
| **Sulawesi Barat** | 39 | 55.9 | 0 | 0 | Tidak teridentifikasi pembuangan tailing smelter |
| **Sulawesi Utara** | 15 | 58.2 | 0 | 0 | Tidak teridentifikasi pembuangan tailing smelter |
| **Gorontalo** | 7 | 58.1 | 0 | 0 | Tidak teridentifikasi pembuangan tailing smelter |

**Formulasi Matematis (Konsentrasi Smelter & Beban Limbah B3 Tailing):**
```text
S_p = Σ s_i  |  IKĀ_{p,t} = ( 1 / n_{p,t} ) * Σ IKA_{j,p,t}
χ² = Σ [ ( O_ij - E_ij )² / E_ij ]  |  Odds_Ratio (OR) = ( a * d ) / ( b * c )
```
**Persamaan Substitusi:**
```text
Smelter_Sulteng_Sultra = 344 unit + 262 unit = 606 unit (77,89% total se-Sulawesi)
Estimasi_Limbah_B3_Tailing = 12.000.000 Ton/Thn (Sulteng) + 7.700.000 Ton/Thn (Sultra) = 19.700.000 Ton/Thn (94,26% total limbah B3)
```
*Hasil uji Chi-Square dan Odds Ratio data panel disajikan pada Tabel 2.4. Kegagalan signifikansi statistik membuktikan Aggregate Dilution Bias (pencemaran fatal sungai industri Bahodopi & Lasolo terencerkan oleh stasiun pemantau sungai non-industri).*

---

## 2.2. Kepungan Asap: Kapasitas PLTU vs Indeks Kualitas Udara (IKU)

Sebanyak **9.825 MW PLTU Captive batu bara off-grid** beroperasi di kawasan hilirisasi nikel menyumbang polusi udara ambien dan gas buang NO₂.

> **Sumber Data:** Data PLTU: `sulawesi_pltu_captive.csv`; Data IKU: `sulawesi_iku_2015_2024.csv`; Pantauan Emisi: Satelit NASA TROPOMI (NO2).

##### Tabel 2.2: Rincian Empiris Kapasitas PLTU (Captive & Grid), IKU, dan Konsentrasi NO₂ NASA (2024)
| Provinsi | Kapasitas PLTU Captive (MW) | PLTU Grid PLN (MW) | Total Daya (MW) | Skor IKU | NASA TROPOMI NO₂ (mol/m²) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Sulawesi Tengah** | 9,365 | 0 | 9,365 | 92.9 | 6.50e-06 |
| **Sulawesi Tenggara** | 2,280 | 100 | 2,380 | 93.0 | 6.62e-06 |
| **Sulawesi Selatan** | 600 | 920 | 1,520 | 91.5 | 6.40e-06 |
| **Sulawesi Utara** | 0 | 220 | 220 | 93.4 | 4.09e-06 |
| **Gorontalo** | 0 | 100 | 100 | 93.5 | 3.76e-06 |
| **Sulawesi Barat** | 0 | 0 | 0 | 92.5 | 6.00e-06 |

**Formulasi Matematis (Kapasitas Energi PLTU & Parameter Kualitas Udara):**
```text
Kapasitas_PLTU_Provinsi = Σ Kapasitas_i  |  Rata_Rata_IKU = MEAN( IKU_Provinsi, Tahun )
χ² = Σ [ ( O - E )² / E ]  |  Odds_Ratio (OR) = ( a * d ) / ( b * c )
```
**Persamaan Substitusi:**
```text
Total_PLTU_Captive = 9.365 MW (Sulteng) + 2.280 MW (Sultra) + 600 MW (Sulsel) = 12.245 MW terpasang
```
*Hasil pengujian statistik tabulasi silang dirinci pada Tabel 2.4. Ketidaksignifikanan membuktikan Efek Pengenceran Udara Ambien karena sensor IKU tersebar merata di hutan berudara bersih.*

---

## 2.3. Eksekusi Ruang: Ekspansi Kawasan Industri vs Tekanan Ekologis (Deforestasi)

Alokasi konsesi IUP dan Kawasan Industri mencakup **1.185.174 Hektar** di Sulawesi. Sepanjang dekade 2014–2023, data Global Forest Watch (GFW) merekam akumulasi kehilangan tutupan pohon sebesar **1.386.055 Hektar** (terbesar di Sulawesi Tengah dan Tenggara).

##### Tabel 2.3: Rincian Empiris Luas Konsesi IUP-Kawasan Industri dan Deforestasi Kumulatif (2014–2023)
| Provinsi | Luas IUP & Kawasan (Ha) | Konsesi Baru Kumulatif (Ha) | Deforestasi Kumulatif 1 Dekade (Ha) |
| :--- | :---: | :---: | :---: |
| **Sulawesi Tengah** | 453,216 | 387,124 | 481,908 |
| **Sulawesi Tenggara** | 446,025 | 212,717 | 337,434 |
| **Sulawesi Selatan** | 181,469 | 123,065 | 261,147 |
| **Sulawesi Utara** | 94,829 | 89,170 | 74,240 |
| **Gorontalo** | 5,212 | 5,212 | 98,063 |
| **Sulawesi Barat** | 4,424 | 2,163 | 133,263 |

##### Tabel 2.4: Ringkasan Hasil Uji Independensi Chi-Square (χ²) dan Odds Ratio (OR) Data Panel Bab 2 (N=54 s.d. 60)
| Faktor Tekanan Lingkungan (X) | Indikator Dampak (Y) | Chi-Square (χ²) | P-Value | Odds Ratio | Kesimpulan Ilmiah |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Kepadatan Smelter (Fasilitas)** | Indeks Kualitas Air (IKA) | 2.667 | 0.102 | 0.35x | TIDAK SIGNIFIKAN (Pengenceran Agregat) |
| **Kapasitas PLTU (MW)** | Indeks Kualitas Udara (IKU) | 0.000 | 1.000 | 1.18x | TIDAK SIGNIFIKAN (Pengenceran Ambien) |
| **Luas Ekspansi Industri (Ha)** | Kehilangan Tutupan Pohon (Ha) | 35.267 | p < 0.001 | 81.0x | SIGNIFIKAN (Risiko Deforestasi 81x Lipat) |

**Formulasi Matematis (Eksekusi Ruang & Konsentrasi Deforestasi Sentra):**
```text
Luas_IUP_Kawasan_p = Σ ( Luas_Izin_i )  |  Kumulatif_Deforestasi_p(T) = Σ ( Deforestasi_p,t )
χ² = Σ [ ( O_ij - E_ij )² / E_ij ]  |  Odds_Ratio (OR) = ( a * d ) / ( b * c )
```
**Persamaan Substitusi:**
```text
Konsesi_Sulteng_Sultra = 453.216 Ha (Sulteng) + 446.025 Ha (Sultra) = 899.241 Hektar (75,87% konsesi se-Sulawesi)
Deforestasi_Sulteng_Sultra = 481.908 Ha (Sulteng) + 337.434 Ha (Sultra) = 819.342 Hektar (59,11% deforestasi se-Sulawesi)
```
*Uji Chi-Square membuktikan secara sangat signifikan (χ² = 35.267, p < 0.001, OR = 81.0x) bahwa wilayah konsesi industri nikel menghadapi risiko deforestasi 81 kali lipat lebih tinggi (lihat Tabel 2.4).*

---

## 2.4. Driver Deforestasi: Analisis Faktor Pendorong Perubahan Tutupan Hutan

Atribusi kausalitas membedah kontribusi faktor pendorong terhadap **1,22+ juta hektar deforestasi di Sulawesi** (GFW 2014–2023) antara industri komoditas ekstraktif skala besar vs pertanian berpindah masyarakat.

##### Tabel 2.5: Matriks Atribusi Deforestasi dan Pelepasan Emisi CO₂ per Faktor Pendorong (Kumulatif 2014–2023)
| Faktor Pendorong Deforestasi | Total Deforestasi (Ha) | Proporsi (%) | Estimasi Emisi Karbon CO₂ (Mg) | Proporsi Emisi (%) |
| :--- | :---: | :---: | :---: | :---: |
| **Pertambangan dan Sawit (Ekstraktif)** | 1,001,654 | 82.2% | 664,472,885 | 82.6% |
| **Kehutanan Komersial (Logging)** | 134,637 | 11.1% | 87,138,022 | 10.8% |
| **Pertanian Berpindah (Masyarakat)** | 55,905 | 4.6% | 38,215,565 | 4.8% |
| **Tidak Teridentifikasi / Lainnya** | 25,738 | 2.1% | 14,225,278 | 1.8% |
| **Total Agregat Sulawesi** | **1,217,934** | **100.0%** | **804,051,750** | **100.0%** |

**Formulasi Matematis (Atribusi Deforestasi Komoditas & Pelepasan Karbon):**
```text
Proporsi_Driver_k (%) = ( Total_Deforestasi_k / Total_Deforestasi_Kumulatif ) * 100
Rasio_Kerusakan = Total_Deforestasi_Tambang_Sawit / Total_Deforestasi_Pertanian_Rakyat
```
**Persamaan Substitusi:**
```text
Proporsi_Tambang_Sawit = ( 1.001.654 Ha / 1.217.934 Ha ) * 100% = 82,24% (Emisi: 664.472.885 Mg CO2 / 82,64%)
Proporsi_Pertanian_Rakyat = ( 55.905 Ha / 1.217.934 Ha ) * 100% = 4,59% (Emisi: 38.215.565 Mg CO2 / 4,75%)
Rasio_Kerusakan = 1.001.654 Ha / 55.905 Ha = 17,92 Kali Lipat Lebih Masif
```
*Fakta empiris membantah tudingan deforestasi akibat perladangan rakyat: industri tambang & sawit merusak hutan 18 kali lipat lebih masif.*

---

## 2.5. Kehancuran Biodiversitas: Dampak Terhadap Habitat Satwa Endemik

Ekspansi pertambangan nikel dan kawasan industri mengancam keanekaragaman hayati kawasan biogeografi Wallacea. Data spasial **GBIF** memetakan **269 titik koordinat perjumpaan (*occurrence*)** dari 7 spesies endemik kunci. Validasi **IUCN Red List** menunjukkan seluruh spesies mengalami tren penurunan populasi (*Decreasing*) dan **4 dari 7 spesies terkonfirmasi menghadapi Mining Threat**.

##### Tabel 2.6: Matriks Spesies Endemik Wallacea, Status IUCN, Penanda Mining Threat, dan Titik GBIF
| Nama Ilmiah (Scientific Name) | Nama Umum (Common Name) | Status IUCN | Tren Populasi | Mining Threat | Titik GBIF |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Macaca nigra** | Celebes Crested Macaque | Critically Endangered | Decreasing | Yes | 87 |
| **Macrocephalon maleo** | Maleo | Critically Endangered | Decreasing | No | 95 |
| **Bubalus depressicornis** | Lowland Anoa | Endangered | Decreasing | Yes | 18 |
| **Bubalus quarlesi** | Mountain Anoa | Endangered | Decreasing | Yes | 10 |
| **Babyrousa celebensis** | Sulawesi Babirusa | Vulnerable | Decreasing | Yes | 33 |
| **Babyrousa babyrussa** | Hairy Babirusa | Vulnerable | Decreasing | No | 14 |
| **Tarsius tarsier** | Spectral Tarsier | Vulnerable | Decreasing | No | 12 |

**Formulasi Matematis (Keterancaman Spesies Wallacea & Penanda Mining Threat):**
```text
O_s = Σ o_i  |  Proporsi_Kritis (%) = ( N_CR_EN / N_total ) * 100  |  Rasio_Mining (%) = ( N_Mining / N_total ) * 100
```
**Persamaan Substitusi:**
```text
Titik_Occurrence_GBIF = 269 Titik Terverifikasi (Maleo 95, Macaca 87, Babirusa 47, Anoa 28, Tarsius 12)
Status_Konservasi_Kritis = [ ( 2 CR + 2 EN ) / 7 Spesies ] * 100% = 57,14% Sangat Terancam Punah
Penanda_Mining_Threat = [ 4 Spesies / 7 Spesies ] * 100% = 57,14% Beririsan Langsung dengan Konsesi IUP Nikel
```
*Spesies Anoa dan Babirusa terbukti secara empiris menghadapi ancaman kepunahan langsung akibat fragmentasi habitat konsesi pertambangan.*
