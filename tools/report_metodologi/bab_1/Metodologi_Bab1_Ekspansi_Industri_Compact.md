# BAB I: METODOLOGI ANALISIS EKSPANSI INDUSTRI EKSTRAKTIF DAN INFRASTRUKTUR PENUNJANG DI PULAU SULAWESI

Dokumen laporan metodologi ini menyajikan kerangka ilmiah, landasan regulasi, formulasi matematis, prosedur analisis statistik, serta metodologi pembuktian berbasis data terbuka yang dioperasionalkan pada **Bab 1: Ekspansi Industri Ekstraktif** dalam studi Daya Dukung dan Daya Tampung Lingkungan Hidup (D3TLH) Sulawesi periode 2014–2024.

---

## 1.1 Konteks Makro: Breakdown PDRB per Komoditas

### 1.1.1 Konteks Makro: Dominasi Ekstraktif vs Ekonomi Akar Rumput
Bagian ini menganalisis struktur Produk Domestik Regional Bruto (PDRB) pada enam provinsi di Pulau Sulawesi sepanjang periode 2016–2024 menggunakan visualisasi grafik area bertumpuk (*Stacked Area Chart*). Analisis ini ditujukan untuk menguji secara empiris apakah percepatan pertumbuhan ekonomi daerah benar-benar bersumber dari sektor produktif masyarakat lokal atau didominasi oleh industri ekstraktif padat modal yang mengalihkan pemanfaatan ruang dan sumber daya alam. Di **Sulawesi Tengah (sebagai pusat hilirisasi)**, ekspansi industri ekstraktif menguasai **55.8% dari total PDRB provinsi pada tahun 2024** (melonjak dari Rp28,45 T pada 2016 menjadi Rp210,51 T pada 2024).

> **Sumber Data:** BPS Provinsi se-Sulawesi (SIMDASI Subject 52 PDRB ADHB 2016–2024 diolah CELIOS).

##### Tabel 1.1: Reklasifikasi Sektoral PDRB KBLI 2020 Berdasarkan Pendekatan Rantai Pasok Hukum (Legal Supply-Chain)
| Kategori BPS | Sektor Lapangan Usaha | Klasifikasi Analisis | Dasar Regulasi & Mandat Hukum | Intisari Ketentuan Hukum |
| :--- | :--- | :---: | :--- | :--- |
| **Kategori B** | Pertambangan dan Penggalian | Ekstraktif | Perpres No. 26/2010 | Ketentuan Pasal 1 Ayat (2) mengenai pengambilan komoditas tambang. |
| **Kategori C** | Industri Pengolahan (Smelter Logam) | Ekstraktif | UU No. 3/2020 & PP 96/2021 | Pasal 102–103 kewajiban hilirisasi smelter terintegrasi pertambangan. |
| **Kategori D** | Pengadaan Listrik & Gas (PLTU Captive) | Ekstraktif | Perpres No. 112/2022 | Pasal 3 Ayat (4) huruf b pengecualian PLTU off-grid khusus smelter. |
| **Kategori A** | Pertanian, Kehutanan, Perikanan | Akar Rumput | KBLI 2020 BPS | Sektor pemanfaatan sumber daya hayati terbarukan & tenaga kerja lokal. |
| **Kategori E–U** | 13 Sektor Jasa & Konstruksi | Jasa & Lainnya | Klasifikasi Standar BPS | Sektor sekunder dan tersier penunjang perekonomian daerah. |

**Formulasi Agregasi Legal Supply-Chain:**
```text
Sektor_Ekstraktif = PDRB(Kat.B) + PDRB(Kat.C) + PDRB(Kat.D)
Total_PDRB = Sektor_Ekstraktif + Sektor_Akar_Rumput(Kat.A) + Sektor_Jasa(Kat.E s.d. U)
Pangsa_Ekstraktif (%) = ( Sektor_Ekstraktif / Total_PDRB ) * 100
```

---

### 1.1.2 Pemusatan Sektor Ekstraktif di Kabupaten se-Sulawesi Tengah
Dekomposisi spasial tingkat kabupaten membuktikan terjadinya *Aggregate Illusion Bias*. Kabupaten **Morowali** mendominasi dengan nilai sektor ekstraktif sebesar **Rp 157.17 Triliun (45.2% dari total PDRB Rp 347.72 Triliun)**, melampaui gabungan total PDRB dari delapan kabupaten lainnya. Bersama Morowali Utara (Rp 19.22 T ekstraktif), kedua daerah mengunci output hilirisasi, sementara 8 kabupaten lainnya memiliki porsi ekstraktif <11% dan bergantung pada pertanian rakyat berproduktivitas rendah.

##### Tabel 1.2: Matriks Polarisasi Sektoral PDRB Kabupaten di Sulawesi Tengah (Tahun 2024)
| Kabupaten / Tipologi | Akar Rumput (T Rp) | Ekstraktif (T Rp) | Jasa (T Rp) | Total PDRB (T Rp) | Porsi Akar (%) | Porsi Eks (%) | Basis Utama Ekonomi |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Morowali (Sentra Smelter)** | 2.70 | 157.17 | 187.85 | **347.72** | 0.8% | 45.2% | Hilirisasi Nikel (Smelter & PLTU) |
| **Morowali Utara (Sentra Smelter)** | 5.17 | 19.22 | 36.08 | **60.47** | 8.5% | 31.8% | Hilirisasi Nikel (Smelter GNI) |
| **Banggai (Sentra Migas/Tambang)** | 8.85 | 20.63 | 51.99 | **81.47** | 10.9% | 25.3% | Migas, Tambang & Perdagangan |
| **Kota Palu (Pusat Jasa/Pemerintahan)** | 1.24 | 4.56 | 60.03 | **65.84** | 1.9% | 6.9% | Jasa & Perdagangan |
| **9 Kab. Non-Sentra Lainnya (Rata-rata)** | 4.86 | 1.13 | 18.59 | **24.58** | 21.3% | 4.3% | Pertanian Rakyat & Perikanan |

---

### 1.1.3 Perbandingan Distribusi 17 Sektor Komoditas per Provinsi (Small Multiples, Tahun Terbaru)
Analisis komparatif *Small Multiples* terhadap 17 sektor KBLI 2020 (BPS 2024) membuktikan dualisme regional: Sulawesi Tengah (44.1% smelter, 11.8% tambang) dan Sulawesi Tenggara (22.4% pertanian, 20.9% tambang) terpolarisasi pada sektor ekstraktif, sedangkan Sulawesi Selatan (21.8%), Sulawesi Utara (20.5%), Sulawesi Barat (38.2%), dan Gorontalo (36.4%) tetap bertumpu pada Sektor Pertanian dan Jasa Perdagangan.

---

## 1.2 Konsentrasi Kawasan Industri & PLTU Captive

Pengoperasian **778 fasilitas smelter** di Sulawesi didukung oleh kapasitas energi fosil **9,825 MW PLTU Captive batu bara off-grid** (ESDM & GEM). Uji tabulasi silang panel (Crosstab SPSS, N=60) membuktikan keterkaitan signifikan antara keberadaan PLTU captive dengan eskalasi kehilangan tutupan hutan di tapak industri.

**Formulasi Chi-Square & Odds Ratio:**
```text
χ² = Σ [ (O - E)² / E ]  |  E_ij = (R_i * C_j) / N  |  OR = (a * d) / (b * c)
```

---

## 1.3 Tren Pertumbuhan Izin Tambang Baru & Uji Signifikansi Statistik

Data Minerbaone mencatat penerbitan **574 Izin Usaha Pertambangan (IUP) baru** sepanjang 2014–2024 seluas **819,452 Hektar**, dengan lonjakan sebesar **246% pada periode 2022–2024**. Uji inferensial Chi-Square membuktikan peningkatan frekuensi dan luas konsesi izin berkorelasi positif sangat kuat terhadap eskalasi deforestasi alam dan komoditas (p < 0.0001).

---

## 1.4 Analisis Realisasi Investasi PMDN dan Dampak Terhadap Tutupan Hutan

Realisasi Penanaman Modal Dalam Negeri (PMDN) sebesar **Rp 218 Triliun** (BKPM 2016–2024) berbanding lurus dengan **1,001,654 Hektar** kehilangan tutupan hutan komoditas (GFW). Pembedahan data GFW Driver Classification (2001–2025) membuktikan sektor komoditas ekstraktif menyumbang **48.4% (1,890,659 Ha)** dari 3,904,079 Ha kehilangan hutan primer Sulawesi (emisi: 1,28 Miliar Mg CO2), sedangkan perladangan rakyat hanya 2.9% (115,404 Ha). Uji crosstab mengonfirmasi **Efek Jeda Waktu (Time-Lagging Effect)**: modal yang masuk hari ini tertahan birokrasi dan baru berdampak pada deforestasi fisik 1 hingga 2 tahun berikutnya.

##### Tabel 1.3: Ringkasan Hasil Uji Independensi Chi-Square (χ²) dan Odds Ratio (OR) Data Panel Bab 1 (N=60)
| Faktor Tekanan Industri (X) | Indikator Dampak Lingkungan (Y) | Chi-Square (χ²) | P-Value | Odds Ratio | df | Kesimpulan Ilmiah |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Kapasitas PLTU Captive (MW)** | Deforestasi Komoditas (≥10,961 Ha) | 18.049 | p < 0.0001 | 18.00x | 1 | SIGNIFIKAN (Risiko 18x Lipat) |
| **Jumlah IUP Tambang Baru (Unit)** | Total Deforestasi Alam (Ha) | 17.239 | p < 0.0001 | 13.75x | 1 | SIGNIFIKAN (Risiko 13.7x Lipat) |
| **Jumlah IUP Tambang Baru (Unit)** | Deforestasi Komoditas (Ha) | 21.818 | p < 0.0001 | 21.36x | 1 | SIGNIFIKAN (Risiko 21.4x Lipat) |
| **Luas Konsesi Tambang Baru (Ha)** | Deforestasi Komoditas (Ha) | 19.267 | p < 0.0001 | 16.00x | 1 | SIGNIFIKAN (Risiko 16.0x Lipat) |
| **Realisasi Investasi PMDN (Juta Rp)** | Deforestasi Komoditas (Ha) | 2.083 | p = 0.1489 | 2.80x | 1 | TIDAK SIGNIFIKAN (Efek Time-Lag) |

---

## 1.5 Pelabuhan Ekspor & Peta Jalur Distribusi Logistik Nikel Sulawesi

Eksploitasi nikel terhubung langsung ke pasar global melalui 6 simpul pelabuhan samudera dan terminal khusus utama di pesisir Sulawesi yang diverifikasi melalui triangulasi Laporan KNKT, Regulasi PSN (Perpres No. 109/2020), dan laporan emiten.

##### Tabel 1.4: Inventarisasi Enam Simpul Pelabuhan dan Terminal Khusus Ekspor Nikel di Pulau Sulawesi
| Kawasan Industri | Wilayah Administrasi | Fasilitas Pelabuhan / Terminal | Status Regulasi | Kapasitas Kapal | Tujuan Utama Ekspor |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **IMIP Morowali** | Morowali, Sulteng | Pelabuhan Samudera & Dermaga Curah | PSN (Perpres 109/2020) | Hingga 52.378 DWT | Pasar Global (Tiongkok) |
| **GNI Morowali Utara** | Morowali Utara, Sulteng | Terminal Khusus Pesisir Tomori | Izin Industri Mandiri | Hingga 30.000 DWT | Pasar Global (Tiongkok) |
| **VDNI Konawe** | Konawe, Sultra | Dermaga Khusus Curah & Kargo | PSN (Perpres 109/2020) | Hingga 50.000 DWT | Pasar Global (Tiongkok) |
| **OSS Konawe** | Konawe, Sultra | Dermaga Terintegrasi Konawe | PSN (Perpres 109/2020) | Hingga 50.000 DWT | Pasar Global (Tiongkok) |
| **Pomalaa (ANTAM)** | Kolaka, Sultra | Dermaga Pomalaa & Konveyor | Kawasan BUMN Industri | Hingga 12.000 DWT | Jepang & Korsel |
| **Sorowako (Vale)** | Luwu Timur, Sulsel | Pelabuhan Balantang Malili | Kontrak Karya Tambang | Hingga 15.000 DWT | Jepang & Skandinavia |

---

## 1.6 Peta Jalur Distribusi Logistik Nikel Sulawesi

Pemodelan spasial alur pelayaran kargo nikel dari 6 pelabuhan muat Sulawesi menuju negara tujuan utama (Tiongkok, Jepang, Korea Selatan) dikonstruksi menggunakan kurva parametrik Bézier untuk merepresentasikan jarak tempuh aktual di permukaan bumi:
```text
Kurva(t) = (1 - t)² * P_Asal + 2*(1 - t)*t * P_Kontrol + t² * P_Tujuan , t in [0, 1]
```

---

## 1.7 Matriks Indikator dan Sumber Data Resmi Bab 1

##### Tabel 1.5: Matriks Indikator dan Sumber Data Primer Resmi Bab 1
| No | Nama Indikator | Kategori Analisis | Satuan | Cakupan | Institusi Sumber Data Primer | Dataset File |
| :---: | :--- | :--- | :---: | :---: | :--- | :--- |
| 1 | IUP Tambang Baru | Tekanan Ekstraktif | Unit | 2014-2024 | ESDM MODI (Minerbaone) | `sulawesi_izin_baru_per_tahun.csv` |
| 2 | Luas Konsesi Baru | Tekanan Ekstraktif | Hektar | 2014-2024 | ESDM MODI (Minerbaone) | `sulawesi_kawasan_nikel_luas.csv` |
| 3 | PLTU Captive | Energi Fosil Khusus | MW | 2014-2024 | Global Energy Monitor (GEM) | `sulawesi_pltu_captive.csv` |
| 4 | Smelter Nikel | Fasilitas Industri | Unit | 2014-2024 | ESDM & CGS | `sulawesi_esdm_nikel.csv` |
| 5 | Investasi PMDN | Arus Modal | Triliun Rp | 2016-2024 | BKPM & BPS | `sulawesi_investasi_pmdn_2016_2024.csv` |
| 6 | PDRB Provinsi Sektoral | Ekonomi Makro | Triliun Rp | 2016-2024 | BPS Provinsi (Subject 52) | `sulawesi_pdrb_sektoral_2016_2024.csv` |
| 7 | PDRB Kabupaten Sentra | Ekonomi Daerah | Triliun Rp | 2016-2024 | BPS Kabupaten se-Sulteng | `sulawesi_pdrb_sektoral_kabupaten_2016_2024.csv` |
| 8 | Deforestasi Komoditas | Dampak Ekologis | Hektar | 2014-2023 | Global Forest Watch (GFW API) | `sulawesi_gfw_master_1_dekade_2014_2023_v3.csv` |
| 9 | Pelabuhan Ekspor | Logistik Maritim | DWT | 2014-2024 | KNKT, Perpres PSN, Korporasi | `sulawesi_logistik_simpul_nikel.csv` |

---

## 1.8 Bagan Alur Kerangka Kerja Riset Bab 1

##### Tabel 1.6: Matriks Tahapan dan Alur Kerangka Kerja Riset Bab 1
| Fase Riset | Fokus Metodologis | Bahan & Sumber Data Primer | Keluaran Analisis |
| :--- | :--- | :--- | :--- |
| **Fase I: Pengumpulan Data** | Kurasi data resmi lintas K/L | Publikasi BPS, Minerbaone, BKPM, GEM, GFW | Basis Data Tabular Panel Provinsi (2014–2024) |
| **Fase II: Reklasifikasi Hukum** | Penyusunan rantai pasok hukum | UU 3/2020, PP 96/2021, Perpres 112/2022 | 3 Klaster Makro (Ekstraktif, Akar Rumput, Jasa) |
| **Fase III: Pengujian Statistik** | Uji signifikansi & rasio risiko | Tabel Kontinjensi, Chi-Square, Odds Ratio | Kausalitas Signifikan Tekanan vs Deforestasi (N=60) |
| **Fase IV: Pemetaan Rantai Pasok** | Triangulasi logistik & rute kapal | KNKT, Perpres PSN, Kurva Parametrik Bézier | Peta Alur Rantai Pasok Ekspor & Konsentrasi Maritim |
