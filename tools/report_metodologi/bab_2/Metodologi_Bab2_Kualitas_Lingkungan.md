# BAB II: METODOLOGI ANALISIS KUALITAS LINGKUNGAN DI KAWASAN SMELTER

Dokumen laporan metodologi ini menyajikan kerangka ilmiah, formulasi matematis, prosedur pengolahan data, dan pengujian statistik yang dioperasionalkan pada **Bab 2: Kualitas Lingkungan di Kawasan Smelter**.

## 2.1. Dampak Limbah Tailing: Konsentrasi Smelter vs Indeks Kualitas Air (IKA)

> **Sumber Data Resmi & Deskripsi Visualisasi:** Data Smelter: `data/processed/sulawesi_esdm_nikel.csv`; Data IKA: `data/processed/sulawesi_ika_2016_2024.csv`; Data Limbah B3: `data/processed/sulawesi_limbah_b3_ngo_proxy.csv`; Data Pencemaran Sungai: `data/processed/sulawesi_sungai_tercemar.csv`.

#### A. Pengantar & Kerangka Narasi
Pengoperasian **778 fasilitas mega-smelter** yang didukung oleh kapasitas **9,825 MW PLTU Captive** meningkatkan intensitas emisi dan beban lingkungan di Pulau Sulawesi. Data menunjukkan konversi tutupan hutan mencapai **1,001,654 Hektar**, estimasi timbulan limbah B3/tailing sebesar **20.9 Juta Ton** per tahun, dan rata-rata IKA tahun 2023 sebesar **58.8**.

#### B. Alur Logika Metodologis Analisis Konsentrasi Smelter vs IKA
```mermaid
flowchart LR
    subgraph Data_Input["1. Input Data Dashboard"]
        A["Data Smelter ESDM<br/><i>Provinsi, jumlah fasilitas, status operasional</i>"] --> C
        B["Data IKA KLHK/BPS<br/><i>Provinsi, Tahun, Indeks Kualitas Air</i>"] --> C
        D["Data Limbah B3 NGO & Sungai Tercemar<br/><i>Tailing, slag, kasus pencemaran</i>"] --> E
    end

    subgraph Panel_Processing["2. Pembentukan Panel 2.1"]
        C["Agregasi Jumlah Smelter per Provinsi"] --> F["Merge dengan IKA Provinsi-Tahun"]
        F --> G["Panel Data: Provinsi x Tahun"]
        E --> H["Validasi spasial peta limbah dan sungai tercemar"]
    end

    subgraph Statistical_Test["3. Crosstabulation & Trendline"]
        G --> I["Binning Median<br/>Smelter Tinggi/Rendah; IKA Kritis/Baik"]
        I --> J["Uji Chi-Square Pearson"]
        J --> K["Odds Ratio<br/>Risiko IKA kritis pada kelompok smelter tinggi"]
    end

    H --> L["Pembacaan empiris kualitas air kawasan smelter"]
    K --> L
```

#### C. Formulasi Matematis: Kalkulasi Konsentrasi Spasial & Uji Chi-Square
Parameterisasi konsentrasi spasial dan pembuktian statistik dihitung menggunakan sistem formulasi matematis berikut:

```text
Jumlah_Smelter_Provinsi = COUNT(Smelter_i) GROUP BY Provinsi
Rata_Rata_IKA_Provinsi_Tahun = MEAN(IKA_Provinsi_Tahun)
Kategori = IF(Nilai >= Median(Seluruh Panel), 'Tinggi/Baik', 'Rendah/Kritis')
Chi_Square (χ²) = Jumlah [ (Frekuensi_Observasi - Frekuensi_Harapan)^2 / Frekuensi_Harapan ]
Odds_Ratio (OR) = ( a * d ) / ( b * c )
```

#### D. Matriks Hasil Uji Empiris
Akumulasi pemusatan fasilitas smelter, nilai IKA, estimasi timbulan limbah B3, dan laporan sungai/pesisir tercemar pada masing-masing provinsi dapat dilihat secara empiris pada **Tabel 2.1** berikut:

##### Tabel 2.1: Rincian Empiris Konsentrasi Smelter, IKA, Limbah B3, dan Sungai Tercemar (2023)
| Provinsi | Jumlah Smelter | IKA | Limbah B3 (Ton/Tahun) | Sungai Tercemar | Daftar Sungai/Pesisir |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Sulawesi Tengah | 344 | 63.6 | 12,000,000 | 4 | Sungai Bahodopi, Sungai Laroenai, Sungai Morowali, Pesisir Fatufia |
| Sulawesi Tenggara | 262 | 61.3 | 7,700,000 | 3 | Sungai Lasolo, Sungai Lalindu, Sungai Konaweha |
| Sulawesi Selatan | 111 | 58.0 | 1,000,000 | 1 | Pesisir dan Sungai Bantaeng |
| Sulawesi Barat | 39 | 58.8 | 0 | 0 | - |
| Sulawesi Utara | 15 | 52.1 | 0 | 0 | - |
| Gorontalo | 7 | 58.7 | 0 | 0 | - |

Penerapan sistem pengujian statistik tabulasi silang pada data panel 6 provinsi selama periode 2016-2023 (total 48 observasi valid) disajikan secara ringkas pada **Tabel 2.2** berikut:

##### Tabel 2.2: Ringkasan Eksekutif Skenario Crosstab Smelter vs IKA Bab 2
| Variabel Independen (X) | Variabel Dependen (Y) | Chi-Square (χ²) | P-Value | Odds Ratio | Kesimpulan |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Kepadatan Smelter (Fasilitas) | Indeks Kualitas Air (IKA) | 2.083 | p = 0.1489 | 0.4 | TIDAK SIGNIFIKAN |

#### E. Analisis Temuan Empiris: Pencemaran Air dan Efek Pengenceran Data Agregat
Kegagalan statistik mendeteksi signifikansi membongkar fakta krusial: Indeks Kualitas Air (IKA) provinsi adalah metrik agregat yang mengencerkan tekanan ekologis di tapak. Pencemaran tailing fatal di area tambang dapat tertutupi oleh data sungai-sungai lain di luar lingkar industri.

## 2.2. Kepungan Asap: Kapasitas PLTU vs Indeks Kualitas Udara (IKU)

> **Sumber Data Resmi & Deskripsi Visualisasi:** Data PLTU Captive: `data/processed/sulawesi_pltu_captive.csv`; Data IKU: `data/processed/sulawesi_iku_2015_2024.csv`. Visualisasi dashboard menampilkan trendline IKU dan pengujian Chi-Square tabulasi silang (Crosstabulation).

#### A. Pengantar & Kerangka Narasi
Keberadaan **9,825 MW PLTU Captive** di kawasan hilirisasi secara langsung berkontribusi pada pencemaran udara. Sub-bab ini menguji hipotesis apakah kapasitas terpasang PLTU Captive memiliki hubungan yang signifikan dengan penurunan Indeks Kualitas Udara (IKU).

#### B. Alur Logika Metodologis Analisis Kapasitas PLTU vs IKU
```mermaid
flowchart LR
    subgraph Data_Input["1. Input Data Dashboard"]
        A["Data PLTU Captive<br/><i>Kapasitas (MW), Status, Provinsi</i>"] --> C
        B["Data IKU KLHK<br/><i>Provinsi, Tahun, IKU</i>"] --> C
    end
    subgraph Panel_Processing["2. Pembentukan Panel 2.2"]
        C["Agregasi Kapasitas PLTU per Provinsi"] --> F["Merge dengan IKU Provinsi-Tahun"]
        F --> G["Panel Data: Provinsi x Tahun"]
    end
    subgraph Statistical_Test["3. Crosstabulation & Analisis"]
        G --> I["Binning Median<br/>PLTU Tinggi/Rendah; IKU Kritis/Baik"]
        I --> J["Uji Chi-Square Pearson"]
        J --> K["Odds Ratio<br/>Risiko IKU kritis pada kelompok PLTU tinggi"]
    end
    K --> L["Pembacaan empiris kualitas udara ambien"]
```

#### C. Formulasi Matematis
```text
Kapasitas_PLTU_Provinsi = SUM(Kapasitas_i) GROUP BY Provinsi
Rata_Rata_IKU_Provinsi_Tahun = MEAN(IKU) GROUP BY Provinsi, Tahun
```

#### D. Matriks Hasil Uji Empiris
Penerapan pengujian statistik tabulasi silang pada data panel (total 54 observasi valid) disajikan secara ringkas pada **Tabel 2.3** berikut:

##### Tabel 2.3: Ringkasan Eksekutif Skenario Crosstab Kapasitas PLTU vs IKU Bab 2
| Variabel Independen (X) | Variabel Dependen (Y) | Chi-Square (χ²) | P-Value | Odds Ratio | Kesimpulan |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Kapasitas PLTU Captive (MW) | Indeks Kualitas Udara (IKU) | 0.000 | p = 1.0000 | Infinite | TIDAK SIGNIFIKAN |

#### E. Analisis Temuan Empiris: Efek Pengenceran Udara Ambien
Kegagalan pengujian statistik ini membongkar fakta krusial bahwa Indeks Kualitas Udara (IKU) level provinsi adalah metrik agregat yang mengencerkan pencemaran udara lokal di tapak industri. Kualitas udara yang buruk di sekitar PLTU tertutupi oleh wilayah yang masih bersih.
