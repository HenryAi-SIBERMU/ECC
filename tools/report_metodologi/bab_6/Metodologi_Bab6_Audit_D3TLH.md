# BAB VI: Audit Forensik Metodologi D3TLH (Model Skoring Kerusakan Ekologis)

**CELIOS - Center of Economic and Law Studies | Laporan Riset Metodologi D3TLH**

Dokumen laporan metodologi ini menyajikan kerangka ilmiah, prosedur pengolahan data, model formulasi matematis, dan pembacaan empiris yang dioperasionalkan pada **Bab 6: Audit Forensik Metodologi D3TLH (Fase 1: Evaluasi Kebijakan Ekstraktif - Pembuktian Terbalik)** dalam studi Daya Dukung dan Daya Tampung Lingkungan Hidup (D3TLH) Sulawesi.

## 6.1 Algoritma Skoring Bioregion Pulau: Matriks Daya Tampung Udara

> **Sumber Data Resmi & Deskripsi Visualisasi:** Data PLTU Captive: `data/processed/sulawesi_pltu_captive.csv` (Global Energy Monitor 2023); Sensor Satelit NASA TROPOMI NO2: `data/processed/gee_nasa_no2_sulawesi_provinsi.csv`; Morbiditas ISPA: `data/processed/sulawesi_kesehatan_detail_2014_2024.csv` (Kemenkes RI); Neraca Limbah B3: `data/processed/sulawesi_limbah_b3.csv` (KLHK Laporan Kinerja 2022); Emisi CO2: `data/processed/sulawesi_gfw_master_1_dekade_2014_2023_v3.csv` (Global Forest Watch 2014-2023).

#### A. Pengantar & Kerangka Narasi
Berdasarkan pedoman teknis D3TLH resmi pemerintah (Permen LH 17/2009 dan regulasi KLHK), perhitungan daya dukung dan daya tampung lingkungan selama ini disusun murni menggunakan pendekatan bio-fisik spasial **Jasa Ekosistem (Ecosystem Services)** berbasis permodelan tutupan lahan dan peta ekoregion. Dalam kategori Jasa Pengaturan, kapasitas udara dinilai semata-mata dari luasan tutupan vegetasi hutan tanpa mengintegrasikan beban pencemaran cerobong PLTU captive batubara, konsentrasi gas NO2 atmosferik dari satelit, maupun rekam medis morbiditas ISPA warga tapak industri nikel.

#### B. Alur Logika Metodologis Skoring Bioregion Pulau (Matriks Udara)
```mermaid
flowchart LR
    subgraph S1["1. Data Empiris Input"]
        A1["Kapasitas PLTU Captive<br/><i>GEM 2023 (MW)</i>"]
        A2["Satelit NASA TROPOMI<br/><i>NO2 Troposferik (mol/m²)</i>"]
        A3["Morbiditas ISPA Kemenkes<br/><i>Incidence Rate Ratio (IRR)</i>"]
        A4["Neraca Limbah B3 KLHK<br/><i>Timbulan Tonase & Proporsi</i>"]
        A5["Deforestasi & Emisi GFW<br/><i>Juta Ton CO2e Hutan Primer</i>"]
    end
    subgraph S2["2. Ambang Batas Regulasi"]
        B1["PLTU: >5.000 MW (GEM)<br/>NO2: >6.0e-6 mol/m²"]
        B2["ISPA IRR > 2.0x<br/><i>(WHO EHC 6)</i>"]
        B3["B3: >5.0% Beban Nasional<br/><i>(LQ / Environmental Injustice)</i>"]
        B4["CO2: >150 Jt Ton<br/><i>(SK MenLHK 168/2022)</i>"]
    end
    subgraph S3["3. Kalkulasi 4 Sub-Metrik"]
        C1["Udara 1: Skor PLTU + NO2<br/><i>Skor 0 - 10</i>"]
        C2["Udara 2: Anomali ISPA<br/><i>Skor 0 - 10</i>"]
        C3["Udara 3: Over-Capacity B3<br/><i>Skor 0 - 10</i>"]
        C4["Udara 4: Defisit Ekosistem CO2<br/><i>Skor 0 - 10</i>"]
    end
    subgraph S4["4. Agregasi & Vonis D3TLH"]
        D1["Simple Additive Weighting<br/><i>Bobot Equal 25% per Pilar</i>"]
        D2["Skor Kontinu WSM (0 - 10)<br/>& Skala Likert Diskret (1 - 5)"]
        D3["Status: DARURAT UDARA<br/><i>Daya Tampung Jebol</i>"]
    end
    A1 & A2 --> B1 --> C1
    A3 --> B2 --> C2
    A4 --> B3 --> C3
    A5 --> B4 --> C4
    C1 & C2 & C3 & C4 --> D1 --> D2 --> D3
```

#### C. Formulasi Matematis: Normalisasi, Thresholding, dan Agregasi SAW
```text
Skor_PLTU = min(5.0, (9,825 / 5000.0) * 5.0) = 5.00
Skor_NO2 = min(5.0, max(0.0, (5.56e-06 - 4.0e-6) / (6.0e-6 - 4.0e-6)) * 5.0) = 3.91
Skor_Udara1 = min(10.0, 5.00 + 3.91) = 8.91
Skor_Udara2 = min(10.0, max(0.0, (3.50 - 1.0) * 10.0)) = 10.00
Skor_Udara3 = min(10.0, (7.93 / 5.0) * 10.0) = 10.00
Skor_Udara4 = min(10.0, (804.05 / 150.0) * 10.0) = 10.00
Skor_Akumulasi_Udara = (8.91 + 10.00 + 10.00 + 10.00) / 4.0 = 9.73 / 10.0
Skor_Likert (Versi 3) = 9.73 / 2.0 = 4.86 -> 5.0 / 5.0 (DARURAT UDARA)
```

#### D. Matriks Hasil Uji Empiris
##### Tabel 6.1: Evaluasi Kuantitatif 4 Sub-Metrik Daya Tampung Udara Bioregion Pulau Sulawesi
| Kode | Indikator Empiris | Nilai Aktual | Ambang Batas Kritis | Formula Substitusi | Skor WSM (0-10) | Skor Likert (1-5) | Status Ekologis |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Udara 1a | Kapasitas PLTU Captive Beroperasi | 9,825.0 MW | > 5.000 MW (GEM 2023) | min(5.0, (9,825/5000)*5) | 5.00 / 5.0 | 2.50 / 2.5 | Kritis Ekstrem |
| Udara 1b | Konsentrasi Gas NO2 Satelit TROPOMI | 5.56e-06 mol/m² | > 6.0e-6 mol/m² (Baseline) | min(5.0, (NO2-4e-6)/(2e-6)*5) | 3.91 / 5.0 | 1.95 / 2.5 | Melampaui Baku Mutu |
| Udara 1 | Sub-Metrik Gabungan Ancaman Udara | Kombinasi PLTU + NO2 | Maksimal Skor 10.0 | min(10.0, 5.00 + 3.91) | 8.91 / 10.0 | 4.45 / 5.0 | Darurat Polusi |
| Udara 2 | Rasio Anomali ISPA (Morbiditas) | 3.50x lipat (IRR) | > 2.0x lipat (WHO EHC 6) | min(10.0, (3.50-1)*10) | 10.00 / 10.0 | 5.00 / 5.0 | KLB Morbiditas |
| Udara 3 | Proporsi Timbulan Limbah B3 | 7.93% dari Nasional | > 5.0% Beban Nasional (KLHK) | min(10.0, (7.93/5)*10) | 10.00 / 10.0 | 5.00 / 5.0 | Overcapacity Asimetris |
| Udara 4 | Defisit Ekosistem Emisi Karbon | 804.05 Juta Ton CO2e | > 150 Jt Ton (Target NDC FOLU) | min(10.0, (804.1/150)*10) | 10.00 / 10.0 | 5.00 / 5.0 | Target FOLU Kolaps |
| TOTAL | Akumulasi Skor Matriks Udara | Rata-rata 4 Pilar SAW | Threshold Kritis >= 4.0 / 6.0 | Σ(Skor 1..4) / 4 | 9.73 / 10.0 | 4.86 / 5.0 | DARURAT UDARA |

##### Tabel 6.2: Dasar Regulasi, Dokumen Legal, dan Landasan Ilmiah Ambang Batas Matriks Udara
| Parameter | Regulasi / Rujukan Ilmiah | Kutipan Dokumen Resmi / Verbatim | Pasal / Hal. | Status Audit |
| :--- | :--- | :--- | :--- | :--- |
| PLTU Captive (Udara 1a) | Global Energy Monitor (GEM 2023) | Operating captive power capacity has increased nearly eightfold from 2013 to 2023, from 1.4 gigawatts (GW) to 10.8 GW. | Key Findings Hal. 4 | VERIFIED |
| Polusi NO2 (Udara 1b) | PP No. 22/2021 & Copernicus AMT 2020 | Baku Mutu Udara Ambien NO2 24h = 65 µg/m³; TROPOMI reported in SI units (µmol/m²); Ambang batas Polusi Berat Tiongkok = 66,0e-6 mol/m². | Lampiran VII Hal. 129 & AMT Hal. 1316 | VERIFIED (BMUA) |
| ISPA Morbiditas (Udara 2) | WHO Environmental Health Criteria (EHC 6) | The relative risk is the ratio between the risk in the exposed population and the risk in the unexposed population (IRR > 2.0 mengonfirmasi paparan industri dominan). | WHO EHC 6, Hal. 13 | DEFENSIBLE |
| Limbah B3 (Udara 3) | Laporan Kinerja (LKj) KLHK 2022 | Total limbah B3 nasional = 427 juta ton. Penduduk Sulteng hanya 1,1% nasional, threshold >5% merefleksikan beban per kapita 5x lipat rata-rata nasional. | LKj KLHK 2022, Hal. 10 | DEFENSIBLE |
| Emisi CO2 (Udara 4) | SK MenLHK No.SK.168/MENLHK/PKTL/PLA.1/2/2022 | Sasaran implementasi FOLU Net Sink 2030 adalah tingkat emisi gas rumah kaca sebesar -140 juta ton CO2e. Emisi >150 juta ton menggagalkan komitmen NDC. | Bab I.3, Hal. 5-6 | VERIFIED |

#### E. Analisis Temuan Empiris: Pembuktian Terbalik Kolapsnya Daya Tampung Udara
1. **Kapasitas Pembakaran Batubara Ekstrem:** Operasional PLTU captive batubara di kawasan industri nikel Sulawesi telah menembus angka **9,825.0 MW**, melampaui ambang batas konsentrasi spasial 5.000 MW (GEM 2023).
2. **Anomali Satelit TROPOMI dan Baku Mutu Udara Ambien:** Konsentrasi rata-rata NO2 tahunan pulau mencapai **5.56e-06 mol/m²** (di Morowali mencapai 8.8e-5 mol/m²), melampaui baku mutu PP 22/2021 dan standar polusi berat internasional (6.6e-5 mol/m²).
3. **Krisis Morbiditas dan Ketidakadilan Beban B3:** Rasio insidensi ISPA warga di wilayah sentra industri tercatat **3.50x lipat** lebih tinggi daripada wilayah non-sentra (KLB Medis WHO). Sulawesi juga menanggung **7.93%** timbulan limbah B3 nasional (33,840,141 Ton/Tahun), memvalidasi overcapacity ekologis per kapita 5x lipat kewajaran nasional.
4. **Vonis Kegagalan Iklim:** Pelepasan karbon **804.05 Juta Ton CO2e** menghancurkan target penyerapan FOLU Net Sink 2030 (-140 Juta Ton CO2e). Dengan Skor Akumulasi **9.73 / 10.0 (Likert: 5.0 / 5.0)**, daya tampung beban udara Bioregion Pulau Sulawesi resmi dinyatakan dalam status **DARURAT UDARA (OVERCAPACITY)**.

## 6.2 Algoritma Skoring Bioregion Pulau: Matriks Daya Tampung Air

> **Sumber Data Resmi & Deskripsi Visualisasi:** Data IKA Resmi: `data/processed/sulawesi_ika_2016_2024.csv` (BPS & KLHK); Uji Toksisitas Cr6+: `data/processed/ika_ngo_cr6_gabungan.csv` (Laboratorium Independen / AEER / WALHI); Morbiditas Diare: `data/processed/sulawesi_kesehatan_detail_2014_2024.csv` (Kemenkes RI); Konflik Pesisir: `data/processed/sulawesi_konflik_agraria_tanahkita_v2.csv` (KPA CATAHU & TanahKita.id); Timbulan Tailing/Sludge: `data/processed/sulawesi_limbah_b3.csv` & Dokumen AMDAL PT HPI (IMIP).

#### A. Pengantar & Kerangka Narasi
Dalam metodologi D3TLH resmi pemerintah, daya tampung air dianalisis sebatas ketersediaan kuantitas hidrologis permukaan melalui rasio ketersediaan debit air vs kebutuhan domestik. Pendekatan ini menyembunyikan realitas pencemaran ekstrem karena menafikan aspek toksikologi kimiawi dan perampasan ruang kelautan. Melalui prinsip **Composite Worst-Case**, metodologi audit forensik ini menetapkan bahwa temuan konsentrasi logam berat karsinogenik Kromium Heksavalen (Cr6+) di muara tapak industri secara sah menganulir klaim rata-rata IKA, sekaligus mengintegrasikan anomali morbiditas diare, penggusuran nelayan tradisional, dan ancaman tailing laut (DSTP).

#### B. Alur Logika Metodologis Skoring Bioregion Pulau (Matriks Air)
```mermaid
flowchart LR
    subgraph S1["1. Data Empiris Input"]
        A1["Indeks Kualitas Air BPS<br/><i>IKA Pemantauan Resmi</i>"]
        A2["Uji Lab Toksisitas Cr6+<br/><i>Kromium Heksavalen (mg/L)</i>"]
        A3["Morbiditas Diare Kemenkes<br/><i>Incidence Rate Ratio (IRR)</i>"]
        A4["Konflik Pesisir TanahKita<br/><i>Perampasan Wilayah Tangkap</i>"]
        A5["Timbulan Tailing / Sludge<br/><i>Estimasi Tonase per Tahun</i>"]
    end
    subgraph S2["2. Ambang Batas Regulasi"]
        B1["IKA < 70 (PermenLHK 27/2021)<br/>Cr6+ > 0.05 mg/L (PP 22/2021)"]
        B2["Diare IRR > 2.0x<br/><i>(WHO EHC 6 + Kemenkes)</i>"]
        B3["Konflik Pesisir: >= 15 Kasus<br/><i>(4.8x Anomali KPA CATAHU)</i>"]
        B4["Tailing: > 25 Jt Ton/Thn<br/><i>(AMDAL PT HPI - AEER 2020)</i>"]
    end
    subgraph S3["3. Kalkulasi 4 Sub-Metrik"]
        C1["Air 1: Composite Worst-Case<br/><i>max(Makro IKA, Mikro Cr6+)</i>"]
        C2["Air 2: Anomali Diare<br/><i>Skor 0 - 10</i>"]
        C3["Air 3: Darurat Pesisir<br/><i>Skor 0 - 10</i>"]
        C4["Air 4: Beban Tailing DSTP<br/><i>Skor 0 - 10</i>"]
    end
    subgraph S4["4. Agregasi & Vonis D3TLH"]
        D1["Simple Additive Weighting<br/><i>Bobot Equal 25% per Pilar</i>"]
        D2["Skor Kontinu WSM (0 - 10)<br/>& Skala Likert Diskret (1 - 5)"]
        D3["Status: DARURAT AIR<br/><i>Daya Tampung Air Jebol</i>"]
    end
    A1 & A2 --> B1 --> C1
    A3 --> B2 --> C2
    A4 --> B3 --> C3
    A5 --> B4 --> C4
    C1 & C2 & C3 & C4 --> D1 --> D2 --> D3
```

#### C. Formulasi Matematis: Composite Worst-Case, IRR Diare, dan Ambang Batas AMDAL
```text
Skor_Makro_Air = min(10.0, max(0.0, (90.0 - 62.07) / 20.0) * 10.0) = 10.00
Skor_Mikro_Air = min(10.0, (1.00 / 0.05) * 10.0) = 10.00
Skor_Air_1 = max(10.00, 10.00) = 10.00
Skor_Air_2 = round(min(10.0, max(0.0, (1.38 - 1.0) * 10.0)) / 2.0) * 2.0 = 4.00
Skor_Air_3 = min(10.0, (15 / 15.0) * 10.0) = 10.00
Skor_Air_4 = min(10.0, (33.84 / 25.0) * 10.0) = 10.00
Skor_Akumulasi_Air = (10.00 + 4.00 + 10.00 + 10.00) / 4.0 = 8.50 / 10.0
Skor_Likert (Versi 3) = 8.50 / 2.0 = 4.25 -> 4.5 / 5.0 (DARURAT AIR)
```

#### D. Matriks Hasil Uji Empiris
##### Tabel 6.3: Evaluasi Kuantitatif 4 Sub-Metrik Daya Tampung Air Bioregion Pulau Sulawesi
| Kode | Indikator Empiris | Nilai Aktual | Ambang Batas Kritis | Formula Substitusi | Skor WSM (0-10) | Skor Likert (1-5) | Status Ekologis |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Air 1a | Indeks Kualitas Air (Makro IKA) | 62.07 | IKA < 70.0 (Batas Baik PermenLHK 27/2021) | min(10.0, (90-62.07)/20*10) | 10.00 / 10.0 | 5.00 / 5.0 | Kualitas Sedang/Kritis |
| Air 1b | Toksisitas Logam Berat Cr6+ (Mikro) | 1.00 mg/L | > 0.05 mg/L (PP 22/2021 Lamp. VI) | min(10.0, (1.00/0.05)*10) | 10.00 / 10.0 | 5.00 / 5.0 | Karsinogenik Ekstrem (20x) |
| Air 1 | Sub-Metrik Gabungan Kualitas Air | Composite Worst-Case | Override Mikro atas Makro | max(10.00, 10.00) | 10.00 / 10.0 | 5.00 / 5.0 | Darurat Toksisitas |
| Air 2 | Morbiditas Penyakit Diare | 1.38x lipat (IRR) | > 2.0x lipat (WHO EHC 6 + Kemenkes) | round(min(10.0, (1.38-1)*10)/2)*2 | 4.00 / 10.0 | 2.00 / 5.0 | Waspada Morbiditas |
| Air 3 | Konflik Pesisir & Nelayan | 15 Kasus | >= 15 Kasus (4.8x Anomali KPA CATAHU) | min(10.0, (15/15)*10) | 10.00 / 10.0 | 5.00 / 5.0 | Darurat Agraria Pesisir |
| Air 4 | Ancaman Tailing DSTP Kawasan | 33.84 Jt Ton/Thn | > 25 Jt Ton/Thn (AMDAL HPI-IMIP) | min(10.0, (33.84/25)*10) | 10.00 / 10.0 | 5.00 / 5.0 | Overcapacity AMDAL |
| TOTAL | Akumulasi Skor Matriks Air | Rata-rata 4 Pilar SAW | Threshold Kritis >= 4.0 / 6.0 | Σ(Skor 1..4) / 4 | 8.50 / 10.0 | 4.25 / 5.0 | DARURAT AIR |

##### Tabel 6.4: Dasar Regulasi, Dokumen Legal, dan Landasan Ilmiah Ambang Batas Matriks Air
| Parameter | Regulasi / Rujukan Ilmiah | Kutipan Dokumen Resmi / Verbatim | Pasal / Hal. | Status Audit |
| :--- | :--- | :--- | :--- | :--- |
| IKA & Toksisitas Cr6+ (Air 1) | PermenLHK No. 27/2021 & PP No. 22/2021 | Kategori Indeks Kualitas Air Kurang (25 ≤ x < 50) dan Baku Mutu Air Kelas II: Kromium Heksavalen (Cr6+) = 0.05 mg/L. | Hal. 35 & Lampiran VI Hal. 120 | VERIFIED |
| Diare Morbiditas (Air 2) | Profil Kesehatan Indonesia 2023 & WHO EHC 6 | Prevalensi diare semua umur 2%; relative risk dihitung dari insidensi per 1.000 penduduk terpapar vs kontrol (IRR > 2.0 batas KLB). | Hal. 220 & Hal. 13 | VERIFIED |
| Konflik Pesisir (Air 3) | KPA Annual Report CATAHU 2022 & 2023 | Letusan konflik agraria pesisir & pulau kecil; 2 provinsi sentra menanggung 15 kasus (4.8x lipat kuota proporsional 3.1 kasus dari 53 kasus nasional). | Hal. 12-15 & Hal. 22 | DEFENSIBLE |
| Tailing DSTP (Air 4) | Dokumen AMDAL Kawasan IMIP (PT HPI) & AEER 2020 | Di Morowali, Hua Pioneer membuang tailing melalui pipa sejauh 4 km di kedalaman 250 m dengan laju pembuangan sekitar 25 juta ton pertahun. | Laporan AEER 2020, Hal. 36 (Footnote 87) | VERIFIED |

#### E. Analisis Temuan Empiris: Pembuktian Terbalik Kolapsnya Ekosistem Perairan
1. **Override Toksisitas Karsinogenik atas IKA:** Meskipun rerata IKA resmi berada pada angka 62.07 (skor makro 10.0/10), temuan uji laboratorium independen mengonfirmasi bahwa konsentrasi Kromium Heksavalen (Cr6+) di muara sungai lingkar tambang mencapai **1.00 mg/L** (20x lipat baku mutu PP 22/2021).
2. **Morbiditas Diare dan Pencemaran Akuifer:** Insidensi penyakit diare di kawasan sentra tercatat **1.38x lipat** dibanding wilayah kontrol (Skor Likert 2.0/5.0), mencerminkan intrusi sedimentasi lumpur dan asam tambang.
3. **Perampasan Ruang Tangkap Nelayan:** Letusan **15 kasus** konflik perairan dan pulau kecil (4,8x lipat kuota proporsional nasional KPA) mengindikasikan penggusuran terstruktur terhadap nelayan tradisional.
4. **Overcapacity Tailing DSTP:** Timbulan sludge/tailing mencapai **33.84 Juta Ton/Tahun**, melampaui batas kapasitas desain AMDAL PT HPI di Morowali (25 Juta Ton/Tahun). Dengan Skor Akumulasi **8.50 / 10.0 (Likert: 4.5 / 5.0)**, daya tampung ekosistem air Bioregion Pulau Sulawesi resmi dinyatakan dalam status **DARURAT AIR (OVERCAPACITY)**.
