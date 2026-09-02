# BAB I: METODOLOGI ANALISIS EKSPANSI INDUSTRI EKSTRAKTIF DAN INFRASTRUKTUR PENUNJANG DI PULAU SULAWESI

Dokumen laporan metodologi ini menyajikan kerangka ilmiah, landasan regulasi, formulasi matematis, prosedur analisis statistik, serta metodologi pembuktian berbasis data terbuka yang dioperasionalkan pada **Bab 1: Ekspansi Industri Ekstraktif** dalam studi Daya Dukung dan Daya Tampung Lingkungan Hidup (D3TLH) Sulawesi periode 2014–2024.

---

## 1.1 Konteks Makro: Breakdown PDRB per Komoditas

### 1.1.1 Konteks Makro: Dominasi Ekstraktif vs Ekonomi Akar Rumput
Struktur Produk Domestik Regional Bruto (PDRB) enam provinsi Sulawesi (2016–2024) dianalisis menggunakan *Stacked Area Chart* untuk menguji pergeseran sektor produktif lokal ke industri ekstraktif padat modal melalui pendekatan *Legal Supply-Chain* (KBLI 2020).

> **Sumber Data:** BPS Provinsi se-Sulawesi (SIMDASI Subject 52 PDRB ADHB 2016–2024 diolah CELIOS).

##### Tabel 1.1: Reklasifikasi Sektoral PDRB KBLI 2020 Berdasarkan Pendekatan Rantai Pasok Hukum (Legal Supply-Chain)
| Kategori BPS | Sektor Lapangan Usaha | Klasifikasi | Dasar Regulasi & Mandat Hukum | Intisari Ketentuan Hukum |
| :--- | :--- | :---: | :--- | :--- |
| **Kategori B** | Pertambangan dan Penggalian | Ekstraktif | Perpres No. 26/2010 | Pasal 1 Ayat (2) pengambilan komoditas tambang. |
| **Kategori C** | Industri Pengolahan (Smelter Logam) | Ekstraktif | UU No. 3/2020 & PP 96/2021 | Pasal 102–103 kewajiban hilirisasi smelter terintegrasi tambang. |
| **Kategori D** | Pengadaan Listrik & Gas (PLTU Captive) | Ekstraktif | Perpres No. 112/2022 | Pasal 3 Ayat (4) huruf b pengecualian PLTU off-grid khusus smelter. |
| **Kategori A** | Pertanian, Kehutanan, Perikanan | Akar Rumput | KBLI 2020 BPS | Pemanfaatan sumber daya hayati terbarukan & tenaga kerja lokal. |
| **Kategori E–U** | 13 Sektor Jasa & Konstruksi | Jasa & Lainnya | Klasifikasi Standar BPS | Sektor sekunder dan tersier penunjang perekonomian daerah. |

**Formulasi Matematis (Agregasi Rantai Pasok Hukum & Pangsa PDRB):**
```text
Sektor Ekstraktif = PDRB Pertambangan (Kat. B) + PDRB Industri Pengolahan/Smelter (Kat. C) + PDRB Listrik/PLTU (Kat. D)
Total PDRB = Sektor Ekstraktif + Sektor Akar Rumput (Kat. A) + Sektor Jasa & Lainnya (Kat. E s.d. U)
Pangsa Ekstraktif (%) = ( Sektor Ekstraktif ÷ Total PDRB ) × 100%
Laju Pertumbuhan (%) = ( ( Nilai Tahun Ini - Nilai Tahun Sebelumnya ) ÷ Nilai Tahun Sebelumnya ) × 100%
```
**Persamaan Substitusi:**
```text
Sektor Ekstraktif Sulteng 2024 = Rp28.450 M (Tambang) + Rp173.864 M (Smelter) + Rp8.200 M (Listrik) = Rp210.513,75 Miliar (Rp210,51 Triliun)
Pangsa Ekstraktif 2024 = ( Rp210.513,75 Miliar ÷ Rp376.950,31 Miliar ) × 100% = 55,85%
Laju Pertumbuhan = ( ( Rp210,51 T - Rp28,45 T ) ÷ Rp28,45 T ) × 100% = +639,93% (Meroket 7,40 Kali Lipat)
```
*Di Sulawesi Tengah, klaster ekstraktif menguasai 55,85% total PDRB 2024, sedangkan pertanian rakyat anjlok di bawah 18%.*

---

### 1.1.2 Pemusatan Sektor Ekstraktif di Kabupaten se-Sulawesi Tengah
Dekomposisi spasial membongkar *Aggregate Illusion Bias*. Kabupaten **Morowali** menghasilkan PDRB Rp 347,72 Triliun dengan sektor ekstraktif mencapai **Rp 157,17 Triliun (45,20%)**, melampaui gabungan total PDRB dari delapan kabupaten lainnya di Sulawesi Tengah.

##### Tabel 1.2: Matriks Polarisasi Sektoral PDRB Kabupaten di Sulawesi Tengah (Tahun 2024)
| Kabupaten / Tipologi | Akar Rumput (T Rp) | Ekstraktif (T Rp) | Jasa (T Rp) | Total PDRB (T Rp) | Porsi Akar (%) | Porsi Eks (%) | Basis Utama Ekonomi |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Morowali (Sentra Smelter)** | 2.70 | 157.17 | 187.85 | **347.72** | 0.8% | 45.2% | Hilirisasi Nikel (Smelter & PLTU) |
| **Morowali Utara (Sentra Smelter)** | 5.17 | 19.22 | 36.08 | **60.47** | 8.5% | 31.8% | Hilirisasi Nikel (Smelter GNI) |
| **Banggai (Sentra Migas/Tambang)** | 8.85 | 20.63 | 51.99 | **81.47** | 10.9% | 25.3% | Migas, Tambang & Perdagangan |
| **Kota Palu (Pusat Jasa/Pemerintahan)** | 1.24 | 4.56 | 60.03 | **65.84** | 1.9% | 6.9% | Jasa & Perdagangan |
| **9 Kab. Non-Sentra Lainnya (Rata-rata)** | 4.86 | 1.13 | 18.59 | **24.58** | 21.3% | 4.3% | Pertanian Rakyat & Perikanan |

**Formulasi Matematis (Disparitas Spasial & Rasio Kesenjangan Morowali):**
```text
Sektor Ekstraktif Kabupaten = PDRB Pertambangan + PDRB Industri Pengolahan + PDRB Listrik (level kabupaten)
Porsi Sektor (%) = ( Nilai Sektor Kabupaten ÷ Total PDRB Kabupaten ) × 100%
Rasio Kesenjangan = Sektor Ekstraktif Morowali ÷ Sektor Pertanian Rakyat Morowali
```
**Persamaan Substitusi:**
```text
Sektor Ekstraktif Morowali = Rp29,20 T (Tambang) + Rp127,96 T (Smelter) = Rp157,17 Triliun (Porsi: 45,20%)
Sektor Pertanian Rakyat Morowali = Rp2,70 Triliun (Porsi: 0,78%)
Rasio Kesenjangan Morowali = Rp157,17 Triliun ÷ Rp2,70 Triliun = 58,21 Kali Lipat
Komparasi Wilayah: Sektor ekstraktif Morowali (Rp157,17 T) > Gabungan 8 Kabupaten Non-Sentra Sulteng (Rp115,22 T)
```
*Sektor pangan dan pertanian rakyat Morowali hanya tersisa 0,78% dari total kapasitas ekonomi daerah.*

---

### 1.1.3 Perbandingan Distribusi 17 Sektor Komoditas per Provinsi (Small Multiples, Tahun Terbaru)
Analisis komparatif Small Multiples membuktikan polarisasi regional: Sulawesi Tengah (44,1% smelter, 11,8% tambang) dan Sulawesi Tenggara (22,4% pertanian, 20,9% tambang) terpolarisasi ekstraktif, sementara empat provinsi lainnya (Sulsel, Sulut, Sulbar, Gorontalo) bertumpu pada pertanian dan jasa perdagangan (20,5% s.d. 38,2%).

---

## 1.2 Konsentrasi Kawasan Industri & PLTU Captive

Operasi **778 unit smelter** di Sulawesi ditopang oleh **9.825 MW PLTU Captive batu bara off-grid** (ESDM & GEM). Uji tabulasi silang SPSS (N=60) mengonfirmasi pemusatan energi fosil berkorelasi erat dengan eskalasi deforestasi tapak industri.

**Formulasi Matematis (Konsentrasi Spasial Energi PLTU Captive):**
```text
Porsi Konsentrasi (%) = ( Kapasitas PLTU Wilayah Sentra ÷ Total Kapasitas se-Sulawesi ) × 100%
Chi-Square (χ²) = Jumlah dari [ ( Frekuensi Observasi - Frekuensi Harapan )² ÷ Frekuensi Harapan ]  |  Odds Ratio (OR) = ( a × d ) ÷ ( b × c )
```
**Persamaan Substitusi:**
```text
Konsentrasi Morowali + Konawe = ( 8.750 MW ÷ 9.825 MW ) × 100% = 89,06% Daya Terkunci
```
*Hasil pengujian statistik tabulasi silang (Chi-Square & Odds Ratio) dirinci secara komprehensif pada Tabel 1.4, dengan konfigurasi variabel uji pada Tabel 1.3.*

---

## 1.3 Tren Pertumbuhan Izin Tambang Baru & Uji Signifikansi Statistik

Pangkalan data Minerbaone mencatat penerbitan **574 Izin Usaha Pertambangan (IUP) baru** sepanjang 2014–2024 seluas **819.452 Hektar**, dengan lonjakan penerbitan mencapai **246% pada periode 2022–2024**. Uji inferensial Chi-Square membuktikan laju perizinan berhubungan positif signifikan dengan deforestasi alam dan komoditas.

**Formulasi Matematis (Laju Pertumbuhan Izin & Alih Fungsi Ruang):**
```text
Pertumbuhan Izin (%) = ( ( Izin Tahun Ini - Izin Tahun Sebelumnya ) ÷ Izin Tahun Sebelumnya ) × 100%
Laju Alih Ruang Harian = Total Luas Konsesi 10 Tahun ÷ 3.650 Hari
Chi-Square (χ²) = Jumlah dari [ ( Frekuensi Observasi - Frekuensi Harapan )² ÷ Frekuensi Harapan ]  |  Odds Ratio (OR) = ( a × d ) ÷ ( b × c )
```
**Persamaan Substitusi:**
```text
Lonjakan IUP 2022–2024 = ( ( 194 izin - 56 izin ) ÷ 56 izin ) × 100% = +246,43%
Laju Alih Ruang = 819.452,54 Ha ÷ 3.650 Hari = 224,51 Hektar/Hari (Setara 314 Lapangan Bola/Hari)
```
*Hasil pengujian statistik tabulasi silang (Chi-Square & Odds Ratio) dirinci secara komprehensif pada Tabel 1.4, dengan konfigurasi variabel uji pada Tabel 1.3.*

---

## 1.4 Analisis Realisasi Investasi PMDN dan Dampak Terhadap Tutupan Hutan

Realisasi Penanaman Modal Dalam Negeri (PMDN) sebesar **Rp 218 Triliun** (BKPM 2016–2024) berbanding lurus dengan **1.001.654 Hektar** kehilangan tutupan hutan komoditas (GFW). Pembedahan data GFW Driver Classification (2001–2025) membuktikan sektor ekstraktif menyumbang **48,4% (1.890.659 Ha)** dari total 3.904.079 Ha kehilangan hutan primer Sulawesi (emisi: 1,28 Miliar Mg CO2), sedangkan perladangan rakyat hanya 2,9% (115.404 Ha).

**Formulasi Matematis (Konsentrasi Modal PMDN & Atribusi Deforestasi Komoditas):**
```text
Konsentrasi PMDN (%) = ( PMDN 3 Provinsi Sentra ÷ Total PMDN Sulawesi ) × 100%
Rasio Kerusakan = Deforestasi Komoditas (Tambang/Sawit) ÷ Deforestasi Pertanian Rakyat
Chi-Square (χ²) = Jumlah dari [ ( Frekuensi Observasi - Frekuensi Harapan )² ÷ Frekuensi Harapan ]  |  Odds Ratio (OR) = ( a × d ) ÷ ( b × c )
```
**Persamaan Substitusi:**
```text
Konsentrasi PMDN = ( Rp194,89 Triliun ÷ Rp218,98 Triliun ) × 100% = 89,00% Tertumpuk di Sulteng, Sultra, Sulsel
Rasio Kerusakan = 1.001.654 Ha (Tambang/Sawit) ÷ 55.905 Ha (Pertanian Rakyat) = 17,92 Kali Lipat Lebih Masif
```
*Hasil pengujian statistik tabulasi silang (Chi-Square & Odds Ratio) dirinci secara komprehensif pada Tabel 1.4, dengan konfigurasi variabel uji pada Tabel 1.3.*

##### Tabel 1.3: Konfigurasi Variabel Uji Tabulasi Silang (Crosstab) Bab 1 — Skenario Sub-bab 1.2, 1.3, dan 1.4
| Komponen Uji | 1.2 PLTU Captive vs Deforestasi | 1.3 Izin Tambang vs Deforestasi | 1.4 Investasi PMDN vs Deforestasi |
| :--- | :--- | :--- | :--- |
| **Variabel Independen (X)** | Kapasitas PLTU Captive (MW) | Frekuensi IUP Baru (Unit) / Luas Konsesi Baru (Ha) | Realisasi Investasi PMDN (Juta Rp) |
| **Variabel Dependen (Y)** | Deforestasi Komoditas (Ha) | Deforestasi Komoditas (Ha) / Total Deforestasi Alam (Ha) | Total Deforestasi Alam (Ha) / Deforestasi Komoditas (Ha) |
| **Hipotesis Alternatif (H1)** | Ekspansi PLTU Captive berkorelasi positif dengan lonjakan deforestasi komoditas | Tingginya penerbitan izin / luas konsesi berhubungan positif dengan laju deforestasi | Tingginya realisasi investasi PMDN berhubungan positif dengan laju deforestasi |
| **Decision Rule (Alpha 5%)** | Tolak H0 jika P-Value < 0.05 | Tolak H0 jika P-Value < 0.05 | Tolak H0 jika P-Value < 0.05 |
| **Threshold Kategori (Median Panel)** | X > 0 MW (PLTU aktif); Y ≥ 10,961.8 Ha (N=60) | X ≥ 2.0 izin; Y ≥ 10,961.8 Ha (N=60) | X > 3,146.4 Juta Rp; Y ≥ 10,451.7 Ha (N=48) |
| **Orientasi Odds Ratio** | a = PLTU Tinggi & Deforestasi Tinggi (risiko lonjakan deforestasi) | a = Izin Tinggi & Deforestasi Tinggi (risiko deforestasi tinggi) | a = Investasi Tinggi & Deforestasi Tinggi (risiko deforestasi tinggi) |

##### Tabel 1.4: Ringkasan Hasil Uji Independensi Chi-Square (χ²) dan Odds Ratio (OR) Data Panel Bab 1 (N=60)
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

##### Tabel 1.5: Inventarisasi Enam Simpul Pelabuhan dan Terminal Khusus Ekspor Nikel di Pulau Sulawesi
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

Pemodelan spasial alur pelayaran kargo nikel dari 6 pelabuhan muat Sulawesi menuju negara tujuan utama (Tiongkok, Jepang, Korea Selatan) dikonstruksi menggunakan kurva parametrik Bézier untuk merepresentasikan jarak tempuh aktual di permukaan bumi.

**Formulasi Matematis (Kurva Parametrik Bézier Alur Pelayaran Maritim):**
```text
Titik Kurva Pelayaran = ( 1 - t )² × Pelabuhan Asal + 2 × ( 1 - t ) × t × Titik Kontrol + t² × Pelabuhan Tujuan ,  t bergerak dari 0 ke 1
```
**Persamaan Substitusi:**
```text
Kapasitas Kapal Maksimum = 52.378 DWT (Setara ~5.200 Truk Tronton per Pengapalan)
Orientasi Logistik: Lebih dari 78% kargo bertolak langsung ke pelabuhan Tiongkok (Ningbo, Qingdao) dan Jepang (Chiba)
```
*Pelabuhan Asal: koordinat pelabuhan muat Sulawesi; Titik Kontrol: jangkar lengkung di perairan internasional; Pelabuhan Tujuan: pelabuhan bongkar negara tujuan.*

---

## 1.7 Matriks Indikator dan Sumber Data Resmi Bab 1

##### Tabel 1.6: Matriks Indikator dan Sumber Data Primer Resmi Bab 1
| No | Nama Indikator | Kategori Analisis | Satuan | Cakupan | Institusi Sumber Data Primer Resmi |
| :---: | :--- | :--- | :---: | :---: | :--- |
| 1 | IUP Tambang Baru | Tekanan Ekstraktif | Unit | 2014-2024 | Kementerian ESDM — MODI (Minerbaone) |
| 2 | Luas Konsesi Baru | Tekanan Ekstraktif | Hektar | 2014-2024 | Kementerian ESDM — MODI (Minerbaone) |
| 3 | PLTU Captive | Energi Fosil Khusus | MW | 2014-2024 | Global Energy Monitor (GEM) |
| 4 | Smelter Nikel | Fasilitas Industri | Unit | 2014-2024 | Kementerian ESDM & Center for Global Sustainability |
| 5 | Investasi PMDN | Arus Modal | Triliun Rp | 2016-2024 | Kementerian Investasi / BKPM & BPS |
| 6 | PDRB Provinsi Sektoral | Ekonomi Makro | Triliun Rp | 2016-2024 | BPS Provinsi se-Sulawesi (Subject 52) |
| 7 | PDRB Kabupaten Sentra | Ekonomi Daerah | Triliun Rp | 2016-2024 | BPS Kabupaten se-Sulawesi Tengah |
| 8 | Deforestasi Komoditas | Dampak Ekologis | Hektar | 2014-2023 | Global Forest Watch (University of Maryland) |
| 9 | Pelabuhan & Terminal Khusus | Logistik Maritim | DWT / Titik | 2014-2024 | KNKT, Perpres PSN, Laporan Korporasi |

---

## 1.8 Bagan Alur Kerangka Kerja Riset Bab 1

##### Tabel 1.7: Matriks Tahapan dan Alur Kerangka Kerja Riset Bab 1
| Fase Riset | Fokus Metodologis | Bahan & Sumber Data Primer | Keluaran Analisis |
| :--- | :--- | :--- | :--- |
| **Fase I: Pengumpulan Data** | Kurasi data resmi lintas K/L | Publikasi BPS, Minerbaone, BKPM, GEM, GFW | Basis Data Tabular Panel Provinsi (2014–2024) |
| **Fase II: Reklasifikasi Hukum** | Penyusunan rantai pasok hukum | UU 3/2020, PP 96/2021, Perpres 112/2022 | 3 Klaster Makro (Ekstraktif, Akar Rumput, Jasa) |
| **Fase III: Pengujian Statistik** | Uji signifikansi & rasio risiko | Tabel Kontinjensi, Chi-Square, Odds Ratio | Kausalitas Signifikan Tekanan vs Deforestasi (N=60) |
| **Fase IV: Pemetaan Rantai Pasok** | Triangulasi logistik & rute kapal | KNKT, Perpres PSN, Kurva Parametrik Bézier | Peta Alur Rantai Pasok Ekspor & Konsentrasi Maritim |
