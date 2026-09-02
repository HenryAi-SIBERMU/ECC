# BAB II: METODOLOGI ANALISIS KUALITAS LINGKUNGAN DI KAWASAN SMELTER

Dokumen laporan metodologi ini menyajikan kerangka ilmiah, formulasi matematis, prosedur pengolahan data, dan pengujian statistik yang dioperasionalkan pada **Bab 2: Kualitas Lingkungan di Kawasan Smelter**.

## 2.1. Dampak Limbah Tailing: Konsentrasi Smelter vs Indeks Kualitas Air (IKA)

> **Sumber Data Resmi & Deskripsi Visualisasi:** Data Smelter: `data/processed/sulawesi_esdm_nikel.csv`; Data IKA: `data/processed/sulawesi_ika_2016_2024.csv`; Data Limbah B3: `data/processed/sulawesi_limbah_b3_ngo_proxy.csv`; Data Pencemaran Sungai: `data/processed/sulawesi_sungai_tercemar.csv`.

#### A. Pengantar & Kerangka Narasi
Pengoperasian **778 fasilitas mega-smelter** yang didukung oleh kapasitas **9,825 MW PLTU Captive** meningkatkan intensitas emisi dan beban lingkungan di Pulau Sulawesi. Data menunjukkan konversi tutupan hutan mencapai **1,001,654 Hektar**, estimasi timbulan limbah B3/tailing sebesar **20.9 Juta Ton** per tahun, dan rata-rata IKA tahun 2024 sebesar **59.7**.

#### B. Alur Logika Metodologis Analisis Konsentrasi Smelter vs IKA
```mermaid
flowchart LR
    subgraph Data_Input["1. Input Data Dashboard"]
        A["Data Smelter ESDM<br/><i>Provinsi & jumlah fasilitas</i>"]
        B["Data IKA KLHK/BPS<br/><i>Provinsi, Tahun, Indeks Kualitas Air</i>"]
        C["Data Limbah B3 & Sungai Tercemar<br/><i>Tailing, slag, laporan pencemaran</i>"]
    end

    subgraph Visual_Processing["2. Analisis Spasial & Trendline"]
        A --> D["Agregasi jumlah smelter per provinsi"]
        B --> E["Rata-rata IKA provinsi-tahun"]
        C --> F["Validasi konteks limbah dan sungai tercemar"]
        D --> G["Peta dan trendline tekanan kualitas air"]
        E --> G
        F --> G
    end

    G --> H["Pembacaan empiris kualitas air kawasan smelter"]
```

Sebagai opsi ringkas pengganti bagan alur crosstab yang terlalu panjang, konfigurasi variabel pengujian Chi-Square disajikan pada **Tabel 2.1a** berikut:

##### Tabel 2.1a: Konfigurasi Variabel Uji Chi-Square (Sub-bab 2.1)
| Komponen Uji | Definisi Variabel (Sub-bab 2.1) |
| :--- | :--- |
| Variabel Independen (X) | Jumlah_Smelter: Total fasilitas smelter (beroperasi maupun konstruksi). |
| Variabel Dependen (Y) | Indeks Kualitas Air: Skor baku mutu air per provinsi. |
| Hipotesis Nol (H0) | Tidak ada hubungan signifikan secara statistik antara kepadatan smelter dengan Indeks Kualitas Air. |
| Decision Rule (Alpha 5%) | Jika P-Value < 0.05, maka Tolak H0 (Terbukti signifikan bahwa smelter menurunkan mutu air). |
| Threshold Kategori | Nilai Median Data Panel 2016-2024 (N=54); variabel kontinu dikonversi menjadi biner. |

#### C. Formulasi Matematis: Kalkulasi Konsentrasi Spasial & Uji Chi-Square
Parameterisasi konsentrasi spasial dan pembuktian statistik dihitung menggunakan sistem formulasi matematis berikut:

```text
S_p = Σ s_i, untuk setiap fasilitas i yang berada di provinsi p
IKĀ_{p,t} = (1 / n_{p,t}) × Σ IKA_{j,p,t}
K_x = Tinggi jika X_{p,t} ≥ M_X; K_y = Baik jika Y_{p,t} ≥ M_Y
Chi_Square (χ²) = Jumlah [ (Frekuensi_Observasi - Frekuensi_Harapan)^2 / Frekuensi_Harapan ]
Odds_Ratio (OR) = ( a * d ) / ( b * c )
```

#### D. Matriks Hasil Uji Empiris
Akumulasi pemusatan fasilitas smelter, nilai IKA, estimasi timbulan limbah B3, dan laporan sungai/pesisir tercemar pada masing-masing provinsi dapat dilihat secara empiris pada **Tabel 2.1** berikut:

##### Tabel 2.1: Rincian Empiris Konsentrasi Smelter, IKA, Limbah B3, dan Sungai Tercemar (2024)
| Provinsi | Jumlah Smelter | IKA | Limbah B3 (Ton/Tahun) | Sungai Tercemar | Daftar Sungai/Pesisir |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Sulawesi Tengah | 344 | 62.1 | 12,000,000 | 4 | Sungai Bahodopi, Sungai Laroenai, Sungai Morowali, Pesisir Fatufia |
| Sulawesi Tenggara | 262 | 65.3 | 7,700,000 | 3 | Sungai Lasolo, Sungai Lalindu, Sungai Konaweha |
| Sulawesi Selatan | 111 | 58.5 | 1,000,000 | 1 | Pesisir dan Sungai Bantaeng |
| Sulawesi Barat | 39 | 55.9 | 0 | 0 | - |
| Sulawesi Utara | 15 | 58.2 | 0 | 0 | - |
| Gorontalo | 7 | 58.1 | 0 | 0 | - |

Penerapan sistem pengujian statistik tabulasi silang pada data panel 6 provinsi selama periode 2016-2024 (total 54 observasi valid) disajikan secara ringkas pada **Tabel 2.2** berikut:

##### Tabel 2.2: Ringkasan Eksekutif Skenario Crosstab Smelter vs IKA Bab 2
| Variabel Independen (X) | Variabel Dependen (Y) | Chi-Square (χ²) | P-Value | Odds Ratio | Kesimpulan |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Kepadatan Smelter (Fasilitas) | Indeks Kualitas Air (IKA) | 2.667 | 0.102 | 0.35 | TIDAK SIGNIFIKAN |

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
        A["Data PLTU Captive<br/><i>Kapasitas (MW), Status, Provinsi</i>"]
        B["Data IKU KLHK<br/><i>Provinsi, Tahun, Indeks Kualitas Udara</i>"]
        C["Data Emisi NASA TROPOMI<br/><i>Pantauan satelit udara ambien (NO2)</i>"]
    end

    subgraph Visual_Processing["2. Analisis Spasial & Trendline"]
        A --> D["Agregasi kapasitas PLTU per provinsi"]
        B --> E["Rata-rata IKU provinsi-tahun"]
        C --> F["Validasi konteks polusi dan kepungan asap"]
        D --> G["Peta dan trendline tekanan kualitas udara"]
        E --> G
        F --> G
    end

    G --> H["Pembacaan empiris kualitas udara kawasan PLTU"]
```

Sebagai opsi ringkas pengganti bagan alur crosstab yang terlalu panjang, konfigurasi variabel pengujian Chi-Square disajikan pada **Tabel 2.2a** berikut:

##### Tabel 2.2a: Konfigurasi Variabel Uji Chi-Square (Sub-bab 2.2)
| Komponen Uji | Definisi Variabel (Sub-bab 2.2) |
| :--- | :--- |
| Variabel Independen (X) | Kapasitas PLTU (MW): Total kapasitas PLTU Captive yang beroperasi. |
| Variabel Dependen (Y) | Indeks Kualitas Udara: Skor baku mutu udara ambien per provinsi. |
| Hipotesis Nol (H0) | Tidak ada hubungan signifikan secara statistik antara kapasitas PLTU dengan Indeks Kualitas Udara. |
| Decision Rule (Alpha 5%) | Jika P-Value < 0.05, maka Tolak H0 (Terbukti signifikan bahwa emisi PLTU menurunkan kualitas udara). |
| Threshold Kategori | Nilai Median Data Panel (N=54); variabel kontinu dikonversi menjadi biner. |

#### C. Formulasi Matematis
```text
Kapasitas_PLTU_Provinsi = SUM(Kapasitas_i) GROUP BY Provinsi
Rata_Rata_IKU_Provinsi_Tahun = MEAN(IKU) GROUP BY Provinsi, Tahun
```

#### D. Matriks Hasil Uji Empiris
Akumulasi kapasitas total PLTU (Captive dan Grid) yang beroperasi, beserta kondisi mutu udara melalui pengukuran IKU dan satelit NASA TROPOMI (NO₂) dapat dilihat secara empiris pada **Tabel 2.3** berikut:

##### Tabel 2.3: Rincian Empiris Kapasitas PLTU (Captive & Grid), IKU, dan Konsentrasi NO₂ NASA (2024)
| Provinsi | Kapasitas PLTU (Captive & Grid) (MW) | IKU | NASA TROPOMI NO₂ (mol/m²) |
| :--- | :--- | :--- | :--- |
| Sulawesi Tengah | 9,365
(Captive: 9,365 | Grid: 0) | 92.9 | 6.50e-06 |
| Sulawesi Tenggara | 2,380
(Captive: 2,280 | Grid: 100) | 93.0 | 6.62e-06 |
| Sulawesi Selatan | 1,520
(Captive: 600 | Grid: 920) | 91.5 | 6.40e-06 |
| Sulawesi Utara | 220
(Captive: 0 | Grid: 220) | 93.4 | 4.09e-06 |
| Gorontalo | 100
(Captive: 0 | Grid: 100) | 93.5 | 3.76e-06 |
| Sulawesi Barat | 0
(Captive: 0 | Grid: 0) | 92.5 | 6.00e-06 |

Selain analisis polusi udara, atribusi pelepasan gas rumah kaca membedah estimasi jejak karbon dari masing-masing faktor pendorong deforestasi pada **Tabel 2.4** berikut:

##### Tabel 2.4: Rincian Empiris Deforestasi dan Emisi CO₂ per Faktor Pendorong (2014-2023)
| Faktor Pendorong Utama | Total Deforestasi (Ha) | Estimasi Emisi CO₂ (Juta Ton) |
| :--- | :--- | :--- |
| Pertambangan dan Sawit | 1,001,654.2585 | 664.4729 |
| Kehutanan Komersial | 134,637.3514 | 87.1380 |
| Pertanian Berpindah (Masyarakat) | 55,905.1723 | 38.2156 |
| Tidak Teridentifikasi | 25,737.8929 | 14.2253 |

Penerapan pengujian statistik tabulasi silang pada data panel (total 54 observasi valid) disajikan secara ringkas pada **Tabel 2.5** berikut:

##### Tabel 2.5: Ringkasan Eksekutif Skenario Crosstab Kapasitas PLTU vs IKU Bab 2
| Variabel Independen (X) | Variabel Dependen (Y) | Chi-Square (χ²) | P-Value | Odds Ratio | Kesimpulan |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Kapasitas PLTU (MW) | Indeks Kualitas Udara (IKU) | 0.000 | 1.000 | 1.18 | TIDAK SIGNIFIKAN |

#### E. Analisis Temuan Empiris: Efek Pengenceran Udara Ambien
Kegagalan pengujian statistik ini membongkar fakta krusial bahwa Indeks Kualitas Udara (IKU) level provinsi adalah metrik agregat yang mengencerkan pencemaran udara lokal di tapak industri. Kualitas udara yang buruk di sekitar PLTU tertutupi oleh wilayah yang masih bersih.

## 2.3. Eksekusi Ruang: Ekspansi Kawasan Industri vs Tekanan Ekologis (Deforestasi)

> **Sumber Data Resmi & Deskripsi Visualisasi:** Data Izin Konsesi: `data/processed/sulawesi_izin_baru_per_tahun.csv` dan `data/processed/sulawesi_kawasan_nikel_luas.csv`; Data Deforestasi: `data/processed/sulawesi_gfw_master_1_dekade_2014_2023_v3.csv`. Visualisasi dashboard menampilkan Animated Bubble Chart (Hans Rosling-style) berlapis peta choropleth deforestasi kumulatif serta pengujian Chi-Square tabulasi silang (Crosstabulation).

#### A. Pengantar & Kerangka Narasi
Pengembangan kawasan industri pemurnian nikel dan perizinan tambang berimplikasi pada alokasi ruang dan perubahan tutupan lahan. Data menunjukkan bahwa alokasi konsesi perizinan (IUP) dan Kawasan Industri mencakup total luasan **1,185,174 Hektar** di Pulau Sulawesi, dengan alokasi terbesar berada di **Sulawesi Tengah**. Sepanjang periode 2014-2023, data Global Forest Watch (GFW) merekam akumulasi kehilangan tutupan pohon sebesar **1,386,055 Hektar**, dengan akumulasi terbesar berada di Sulawesi Tengah. Sub-bab ini menguji hipotesis secara empiris: **apakah luasan ekspansi kawasan industri dan perizinan tambang berbanding lurus dengan laju deforestasi?**

#### B. Alur Logika Metodologis Analisis Ekspansi Industri vs Deforestasi
Pendekatan visualisasi dinamis Animated Bubble Chart (Hans Rosling-style) untuk memetakan eksekusi ruang secara spasio-temporal diilustrasikan pada **Bagan Alur 2.3** berikut. Adapun untuk tahapan analisis inferensial (Uji Chi-Square), alur logikanya merujuk secara penuh pada **Bagan Alur 2.1** (di sub-bab sebelumnya) dengan penyesuaian konfigurasi variabel spesifik sesuai Tabel 2.3a di bawah gambar.

##### Bagan Alur 2.3: Alur Logika Metodologis Animated Bubble Chart Ekspansi Industri vs Deforestasi
```mermaid
flowchart LR
    subgraph Data_Input["1. Input Data Dashboard"]
        A["Data Izin Konsesi Minerbaone<br/><i>Provinsi, Tahun, Luas Konsesi Baru (Ha)</i>"] --> C
        B["Data Kawasan & IUP Nikel<br/><i>Provinsi, Total Luas IUP-Kawasan (Ha)</i>"] --> C
        D["Data Deforestasi GFW 2014-2023<br/><i>Provinsi, Tahun, Total Deforestasi (Ha)</i>"] --> C
    end
    subgraph Panel_Processing["2. Pembentukan Panel 2.3"]
        C["Merge Panel Provinsi-Tahun"] --> F["CUMSUM Konsesi & Deforestasi<br/>per Provinsi (2014-2023)"]
    end
    subgraph Visual_Analysis["3. Animated Bubble Chart (Hans Rosling-style)"]
        F --> G["Choropleth<br/>Level keparahan deforestasi kumulatif"]
        F --> H["Bubble Size<br/>Skala konsesi industri kumulatif"]
        G --> I["Animasi & Slider Temporal<br/>2014-2023"]
        H --> I
    end
    I --> J["Pembacaan empiris eksekusi ruang spasio-temporal"]
```

##### Tabel 2.3a: Konfigurasi Variabel Uji Chi-Square (Sub-bab 2.3)
| Komponen Uji | Definisi Variabel (Sub-bab 2.3) |
| :--- | :--- |
| Variabel Independen (X) | Luas Ekspansi Industri (Ha) / Luas IUP & Kawasan (Ha) |
| Variabel Dependen (Y) | Kehilangan Tutupan Pohon (Ha) / Total Deforestasi Alam (Ha) |
| Hipotesis Nol (H0) | Luasan ekspansi kawasan industri dan perizinan tambang tidak berhubungan dengan laju deforestasi. |
| Hipotesis Alternatif (H1) | Alokasi izin lahan (Luas IUP & Kawasan) berkorelasi positif dengan laju deforestasi. |
| Threshold Kategori | Nilai Median Data Panel (N=60): X >= 138,148.8 Ha; Y >= 15,917.7 Ha |

#### C. Formulasi Matematis: Akumulasi Konsesi, Deforestasi, dan Uji Crosstabulation
Parameterisasi tekanan ruang dan pembuktian statistik dihitung menggunakan sistem formulasi matematis berikut:

```text
Luas_IUP_Kawasan_p = Σ ( Luas_Izin_i )   ;   untuk seluruh entitas izin i pada provinsi p
Kumulatif_Luas_Konsesi_p(T) = Σ ( Konsesi_Baru_p,t )   ;   untuk t = 2014 s.d. T
Kumulatif_Deforestasi_p(T) = Σ ( Deforestasi_p,t )   ;   untuk t = 2014 s.d. T
Kategori(x) = 'Tinggi/Parah' , jika x ≥ Median(Panel)   |   'Rendah' , jika x < Median(Panel)
χ² = Σ [ ( O_ij - E_ij )² / E_ij ]   ;   dengan E_ij = ( Total_Baris_i × Total_Kolom_j ) / N
Odds_Ratio (OR) = ( a × d ) / ( b × c )
```

#### D. Matriks Hasil Uji Empiris
Akumulasi alokasi ruang konsesi IUP-Kawasan Industri dan deforestasi kumulatif dekade 2014-2023 pada masing-masing provinsi dapat dilihat secara empiris pada **Tabel 2.6** berikut:

##### Tabel 2.6: Rincian Empiris Luas Konsesi IUP-Kawasan Industri dan Deforestasi Kumulatif per Provinsi (2014-2023)
| Provinsi | Luas IUP & Kawasan (Ha) | Konsesi Baru Kumulatif 2014-2023 (Ha) | Deforestasi Kumulatif 2014-2023 (Ha) |
| :--- | :--- | :--- | :--- |
| Sulawesi Tengah | 453,216 | 387,124 | 481,908 |
| Sulawesi Tenggara | 446,025 | 212,717 | 337,434 |
| Sulawesi Selatan | 181,469 | 123,065 | 261,147 |
| Sulawesi Utara | 94,829 | 89,170 | 74,240 |
| Gorontalo | 5,212 | 5,212 | 98,063 |
| Sulawesi Barat | 4,424 | 2,163 | 133,263 |

Penerapan pengujian statistik tabulasi silang pada data panel provinsi-tahun periode 2014-2023 (total 60 observasi valid) disajikan secara ringkas pada **Tabel 2.7** berikut:

##### Tabel 2.7: Ringkasan Eksekutif Skenario Crosstab Ekspansi Industri vs Deforestasi Bab 2
| Variabel Independen (X) | Variabel Dependen (Y) | Chi-Square (χ²) | P-Value | Odds Ratio | Kesimpulan |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Luas Ekspansi Industri (Ha) | Kehilangan Tutupan Pohon (Ha) | 35.267 | p < 0.001 | 81.0 | SIGNIFIKAN |

#### E. Analisis Temuan Empiris: Eksekusi Ruang dan Laju Deforestasi
Hasil pengujian mengonfirmasi secara SIGNIFIKAN bahwa perluasan kawasan industri dan izin pertambangan baru memiliki korelasi positif dengan tingkat deforestasi. Temuan statistik mengonfirmasi bahwa peningkatan luasan Ekspansi Industri berkorelasi signifikan dengan kenaikan tingkat Deforestasi.

## 2.4. Driver Deforestasi: Analisis Faktor Pendorong Perubahan Tutupan Hutan

> **Sumber Data Resmi & Deskripsi Visualisasi:** Data GFW Klasifikasi Driver: `data/processed/sulawesi_gfw_loss_by_driver_2014_2023_v3.csv`. Visualisasi dashboard menampilkan Normalized Stacked Area Chart (evolusi temporal komposisi driver), Bar Chart kumulatif per driver, serta kartu metrik atribusi deforestasi industri vs pertanian masyarakat.

#### A. Pengantar & Kerangka Narasi
Fokus analisis sub-bab ini adalah membedah kontribusi masing-masing sektor pendorong terhadap **1,22+ juta hektar deforestasi di Sulawesi** sepanjang dekade 2014-2023. Section ini menyajikan atribusi kuantitatif antara aktivitas industri ekstraktif komoditas (tambang/sawit) dan sektor pertanian masyarakat. Faktor-faktor penyebab deforestasi diklasifikasikan ke dalam 5 kelompok: **Industri Ekstraktif (Tambang/Sawit), Kehutanan Komersial, Pertanian Berpindah, Urbanisasi, dan Tidak Teridentifikasi**.

#### B. Alur Logika Metodologis Analisis Driver & Atribusi Emisi CO2
Kerangka atribusi kausalitas hilangnya tutupan lahan dan kuantifikasi jejak karbon dari masing-masing faktor pendorong diilustrasikan pada **Bagan Alur 2.4** berikut. Sub-bab ini murni menggunakan agregasi tabular atribusi (tanpa uji inferensial Chi-Square), dengan konfigurasi variabel analisis dirinci pada Tabel 2.4a di bawah gambar.

##### Bagan Alur 2.4: Alur Logika Metodologis Driver Analysis & Emisi CO2 Attribution
```mermaid
flowchart LR
    subgraph Data_Input["1. Input Data Dashboard"]
        A["Data GFW Klasifikasi Driver<br/><i>Provinsi, Tahun, Faktor Pendorong, Luas (Ha), Emisi CO2 (Mg)</i>"] --> C
    end
    subgraph Driver_Processing["2. Klasifikasi & Agregasi Driver"]
        C["Pemetaan Kelompok Faktor Pendorong<br/>Tambang-Sawit; Kehutanan; Pertanian; Urbanisasi; Tak Teridentifikasi"] --> F["Agregasi SUM Luas & Emisi<br/>GROUP BY Faktor Pendorong"]
        F --> G["Kuantifikasi Proporsi (%)<br/>terhadap total kumulatif deforestasi"]
    end
    subgraph Attribution_Analysis["3. Atribusi & Visualisasi"]
        G --> H["Normalized Stacked Area<br/>Evolusi temporal komposisi driver"]
        G --> I["Bar Chart Kumulatif<br/>Total deforestasi per driver"]
        G --> J["Atribusi Emisi CO2<br/>Jejak karbon per faktor pendorong"]
    end
    H --> K["Pembacaan anatomi deforestasi Sulawesi"]
    I --> K
    J --> K
```

##### Tabel 2.4a: Konfigurasi Variabel Analisis Driver & Atribusi Emisi (Sub-bab 2.4)
| Komponen Analisis | Definisi Variabel (Sub-bab 2.4) |
| :--- | :--- |
| Variabel Independen (X) | Faktor Pendorong Deforestasi (4 kelompok klasifikasi driver aktual dalam data) |
| Variabel Dependen (Y1) | Luas Deforestasi (Ha): kehilangan tutupan pohon per faktor pendorong |
| Variabel Dependen (Y2) | Emisi CO2 (Megagram): kuantitas karbon dioksida ekuivalen yang terlepas ke atmosfer |
| Periode & Cakupan Observasi | 2014-2023 pada 6 provinsi se-Sulawesi |
| Metode Atribusi | Agregasi tabular per kelompok Faktor Pendorong dengan kuantifikasi proporsi absolut (tanpa uji inferensial) |

#### C. Formulasi Matematis: Agregasi Driver, Proporsi, dan Atribusi Emisi
Kuantifikasi atribusi kausalitas dan jejak karbon dihitung menggunakan sistem formulasi matematis berikut:

```text
Total_Deforestasi_k = Σ ( Luas_Deforestasi_i )   ;   untuk seluruh observasi i dengan Faktor_Pendorong k
Total_Emisi_k = Σ ( Emisi_CO2_i )   ;   untuk seluruh observasi i dengan Faktor_Pendorong k
Persentase_Driver_k (%) = ( Total_Deforestasi_k / Total_Deforestasi_Kumulatif ) × 100
Rasio_Perbandingan = Total_Pertambangan_Sawit / Total_Pertanian_Berpindah
```

#### D. Matriks Hasil Uji Empiris
Akumulasi total deforestasi, proporsi kontribusi, dan atribusi emisi CO2 masing-masing faktor pendorong pada periode 2014-2023 dapat dilihat secara empiris pada **Tabel 2.8** berikut:

##### Tabel 2.8: Matriks Atribusi Deforestasi dan Emisi CO2 per Faktor Pendorong (Kumulatif 2014-2023)
| Faktor Pendorong | Total Deforestasi (Ha) | Proporsi (%) | Emisi CO2 (Megagram) |
| :--- | :--- | :--- | :--- |
| Pertambangan dan Sawit | 1,001,654 | 82.2% | 664,472,885 |
| Kehutanan Komersial | 134,637 | 11.1% | 87,138,022 |
| Pertanian Berpindah (Masyarakat) | 55,905 | 4.6% | 38,215,565 |
| Tidak Teridentifikasi | 25,738 | 2.1% | 14,225,278 |

#### E. Analisis Temuan Empiris: Anatomi Deforestasi Sulawesi
1. **Dominasi Sektor Pertambangan dan Sawit:** mencakup 1,001,654 Ha atau **82.2%** dari total kehilangan tutupan hutan periode 2014-2023, dengan proporsi tahunan konsisten pada rentang 78-85% setiap tahunnya.
2. **Porsi Minor Pertanian Berpindah:** 4.6% (55,905 Ha) dari total deforestasi kumulatif; deforestasi komoditas tambang dan sawit 18 kali lebih besar dibanding pertanian berpindah.
3. **Atribusi Emisi CO2:** sektor pertambangan dan sawit melepaskan 664,472,885 Megagram CO2 (82.6% dari total agregat pelepasan karbon).
4. **Implikasi Kebijakan:** pengendalian deforestasi memerlukan evaluasi tata ruang perizinan pertambangan dan pengawasan ketat terhadap pembukaan lahan komoditas di wilayah tutupan hutan.

## 2.5. Kehancuran Biodiversitas: Dampak Terhadap Habitat Satwa Endemik

> **Sumber Data Resmi & Deskripsi Visualisasi:** Data Perjumpaan GBIF: `data/raw/gbif_sulawesi_occurrences.csv`; Data Status IUCN: `data/processed/sulawesi_biodiversitas_iucn_fase5_exploded.csv`. Visualisasi dashboard menampilkan peta spasial titik occurrence GBIF dan tabel validasi ancaman IUCN Red List.

#### A. Pengantar & Kerangka Narasi
Pulau Sulawesi merupakan wilayah yang memiliki keanekaragaman hayati endemik yang khas di kawasan Wallacea. Perubahan tutupan lahan akibat ekspansi pertambangan nikel dan kawasan industri berimplikasi pada fragmentasi habitat flora dan fauna endemik. Data spasial dari **GBIF** memetakan sebanyak **269 titik koordinat keberadaan (occurrence)** dari **7 spesies endemik kunci**.

Berdasarkan **IUCN Red List**, tercatat **2 spesies Critically Endangered**, **2 spesies Endangered**, dan **3 spesies Vulnerable**. Catatan IUCN menunjukkan **4 dari 7 spesies** memiliki penanda **Mining Threat**.

#### B. Alur Logika Metodologis Spatial Mapping GBIF & Analisis IUCN Red List
Kerangka pemetaan titik koordinat perjumpaan satwa dan sintesis status konservasi internasional diilustrasikan pada **Bagan Alur 2.5** berikut. Konfigurasi variabel analisis dirinci pada Tabel 2.5a di bawah gambar.

##### Bagan Alur 2.5: Alur Logika Metodologis Spatial Mapping GBIF & Analisis IUCN Red List
```mermaid
flowchart LR
    subgraph Data_Input["1. Input Data Dashboard"]
        A["Data Perjumpaan GBIF<br/><i>Scientific Name, Latitude, Longitude, Province, Year</i>"]
        B["Data IUCN Red List<br/><i>Status, Population Trend, Mining Threat</i>"]
    end

    subgraph Spatial_Model["2. Spatial Mapping & Overlay"]
        A --> C["Pemetaan titik koordinat occurrence"]
        C --> D["Overlay dengan konteks wilayah industri dan konsesi"]
    end

    subgraph Conservation_Model["3. Analisis Status Konservasi"]
        B --> E["Klasifikasi CR, EN, VU"]
        B --> F["Identifikasi penanda Mining Threat"]
    end

    D --> G["Pembacaan keterancaman habitat satwa endemik"]
    E --> G
    F --> G
```

##### Tabel 2.5a: Konfigurasi Variabel Analisis Spatial Mapping & IUCN Red List (Sub-bab 2.5)
| Komponen Analisis | Definisi Variabel (Sub-bab 2.5) |
| :--- | :--- |
| Variabel Lokasi | Titik Koordinat (Lat, Lon): lokasi perjumpaan aktual satwa endemik. |
| Identitas Taksonomi | Scientific Name dan Common Name: identitas spesies dari GBIF/IUCN. |
| Status Konservasi | Status: level ancaman IUCN Red List (Critically Endangered, Endangered, Vulnerable). |
| Ancaman Utama | Mining Threat: penanda apakah aktivitas pertambangan tercatat sebagai ancaman spesies. |
| Cakupan Data | 269 titik GBIF, 7 spesies endemik kunci, 6 provinsi observasi. |

#### C. Formulasi Matematis: Occurrence, Status Keterancaman, dan Mining Threat
Kuantifikasi sebaran titik perjumpaan, komposisi status konservasi, dan ancaman pertambangan dihitung menggunakan sistem formulasi matematis berikut:

```text
O_s = Σ o_i, untuk setiap titik occurrence i yang memiliki spesies s
P_k (%) = ( N_k / N_total ) × 100
R_m (%) = ( N_m / N_total ) × 100
```

#### D. Matriks Hasil Uji Empiris
Rincian status konservasi, tren populasi, penanda ancaman pertambangan, dan jumlah titik occurrence GBIF per spesies disajikan pada **Tabel 2.9** berikut:

##### Tabel 2.9: Matriks Spesies Endemik, Status IUCN, Mining Threat, dan Titik Occurrence GBIF
| Scientific Name | Common Name | Status | Population Trend | Mining Threat | Titik GBIF |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Macaca nigra | Celebes Crested Macaque | Critically Endangered | Decreasing | Yes | 87 |
| Macrocephalon maleo | Maleo | Critically Endangered | Decreasing | No | 95 |
| Bubalus depressicornis | Lowland Anoa | Endangered | Decreasing | Yes | 18 |
| Bubalus quarlesi | Mountain Anoa | Endangered | Decreasing | Yes | 10 |
| Babyrousa celebensis | Sulawesi Babirusa | Vulnerable | Decreasing | Yes | 33 |
| Babyrousa babyrussa | Hairy Babirusa | Vulnerable | Decreasing | No | 14 |
| Tarsius tarsier | Spectral Tarsier | Vulnerable | Decreasing | No | 12 |

##### Tabel 2.10: Ringkasan Status Konservasi IUCN Spesies Endemik Kunci
| Status IUCN | Jumlah Spesies | Proporsi |
| :--- | :--- | :--- |
| Critically Endangered | 2 | 28.6% |
| Endangered | 2 | 28.6% |
| Vulnerable | 3 | 42.9% |

#### E. Analisis Temuan Empiris: Fragmentasi Habitat dan Ancaman Kepunahan
Pembacaan spatial mapping GBIF dan validasi IUCN Red List menunjukkan bahwa ekspansi industri ekstraktif tidak hanya menekan kualitas air, udara, dan tutupan hutan, tetapi juga mempersempit ruang hidup spesies endemik Wallacea. Titik occurrence GBIF memberikan bukti spasial keberadaan satwa, sedangkan status IUCN dan penanda Mining Threat memperkuat pembacaan bahwa tekanan pertambangan masuk dalam daftar ancaman konservasi spesies.
