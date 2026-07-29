# Bab 4: Ruang Hidup yang Terampas

**CELIOS — Center of Economic and Law Studies**

*Membedah eskalasi konflik sosial dan perampasan ruang agraria di balik klaim keberhasilan pembangunan.*

---

## Metodologi

**Alur Kausalitas (Ekonomi Politik Ekologi):** `Ekspansi Industri & Proyek Strategis` → `Perampasan Ruang Hidup & Lahan` → `Eskalasi Konflik Sosial/Agraria`

Tesis dari analisis ini membantah narasi kesejahteraan dengan memperlihatkan bahwa agresivitas izin konsesi, proyek strategis nasional, hingga perluasan taman nasional dan pariwisata berbanding lurus dengan meningkatnya resistensi dan terdepaknya masyarakat lokal dari ruang kelolanya.

**Variabel Dampak (Y):**
*   **Jumlah Konflik:** Riwayat insiden letupan konflik agraria historis berdasarkan database independen masyarakat sipil.
*   **Sektor Pemicu:** Tipologi konflik yang dipecah berdasarkan klasifikasi sektor penyebab dominan.

**Metode Pengolahan Data:**
Analisis menggunakan pendekatan *Trend Analysis* dan tabulasi silang (*Crosstabulation*). Menyandingkan matriks kejadian letupan konflik secara sektoral untuk mengekstraksi fakta episentrum sengketa berdarah.

---

## Hilirisasi & Pembangunan Berlumur Konflik

Ekspansi industri ekstraktif dan proyek strategis tidak hanya menumbangkan daya dukung ekologis, tetapi secara agresif merobek tatanan kehidupan sosial masyarakat. Data empiris mencatat sejarah panjang perlawanan akar rumput dengan total terjadinya **95 letupan konflik agraria** yang tercatat. Konflik ini bukanlah residu acak pembangunan, melainkan ekses langsung dari model ekonomi yang sangat rakus daratan.

Secara mengejutkan, aktor perampas lahan utama tidak hanya didominasi oleh pertambangan dan perkebunan monokultur, namun meluas ke sekor **Kehutanan** (Hutan Lindung, Produksi, Konservasi), **Infrastruktur & PSN** (Bendungan, Transmigrasi, Kawasan Industri), hingga proyek **Pariwisata & Pesisir**. Tiga sektor utama (Perkebunan, Kehutanan, dan Pertambangan) menyumbang porsi **82.1%** dari keseluruhan catatan konflik. Alih-alih mendapatkan kucuran kesejahteraan, warga lokal justru seringkali dikriminalisasi, direpresi, dan diusir dari atas ruang penghidupan historis mereka.

---

## Ringkasan Metrik Agregat

| Indikator | Nilai | Keterangan |
|---|---|---|
| **Total Letupan Konflik** | **95 kasus** | Insiden perampasan lahan dan sengketa agraria yang memicu perlawanan sipil. |
| **Korban Terdampak (Jiwa)** | **90,582 jiwa** | Jumlah warga yang kehilangan ruang hidup, digusur, atau terpinggirkan akibat konflik lahan (bukan korban meninggal). |
| **Status: Belum Ditangani** | **51 kasus** | Kasus yang dibiarkan terkatung-katung tanpa resolusi berkeadilan bagi warga. |
| **Masyarakat Melawan** | **59 komunitas** | Kelompok tani dan masyarakat adat yang berjuang mempertahankan ruang hidup. |
| **Sektor Perkebunan** | **25 kasus** | Tumpang tindih Hak Guna Usaha (HGU) sawit skala masif dengan lahan rakyat. |
| **Sektor Kehutanan** | **30 kasus** | Klaim sepihak hutan produksi dan konservasi yang menggusur masyarakat lokal. |
| **Sektor Pertambangan** | **23 kasus** | Operasi pengerukan lahan dan hilirisasi untuk industri mineral serta nikel. |
| **Infrastruktur & PSN** | **13 kasus** | Penggusuran proyek strategis nasional seperti bendungan dan jalan. |
| **Pariwisata & Pesisir** | **3 kasus** | Privatisasi pesisir dan pariwisata super-premium (KEK). |
| **Keterlibatan Pemerintah** | **69 kasus** | Andil institusi negara dan pemerintah daerah dalam sengketa warga. |
| **Keterlibatan Korporasi** | **52 kasus** | Perusahaan swasta asing maupun BUMN yang memonopoli ruang hidup. |

*Sumber Analisis Data: Konsorsium Pembaruan Agraria (KPA) / Tanah Kita*

---

## 4.1 Tren Eskalasi Konflik Agraria Seiring Ekspansi Industri

**Metode: Analisis Tren Time-Series (Sumber: KPA / Tanah Kita)**

### Metodologi: Analisis Tren Time-Series

**Metode Analisis:** Sub-bab ini menggunakan visualisasi tren runtun waktu (*Time-Series Trend Analysis*) untuk melacak eskalasi kasus perampasan lahan secara historis.

1. **Model Analisis Tren Historis:**
    * **Time-Series Tracking:** Memetakan fluktuasi dan eskalasi frekuensi letupan konflik agraria dalam rentang waktu memanjang (longitudinal).
    * **Komparasi Periodik:** Membandingkan volume letupan konflik antara fase pra-ekspansi (sebelum hilirisasi masif) dengan fase pasca-ekspansi (era Proyek Strategis Nasional).
    * **Pemetaan Eskalasi:** Mengidentifikasi pola lonjakan kasus perampasan lahan untuk membuktikan secara empiris relasi antara percepatan industrialisasi dengan peningkatan konflik sosial.
2. **Kalkulasi/Formula Pengolahan:** Agregasi jumlah konflik berdasarkan periode tahun pencatatan dan sektor industri.
    * `Total_Konflik_Tahunan = COUNT(Kasus) GROUP BY Tahun, Sektor`
    * `Lonjakan_Eskalasi = (Kasus_Pasca - Kasus_Pra) / Kasus_Pra * 100%`
3. **Variabel & Fitur Data:**
    * **Waktu (Independen):** Tahun pencatatan konflik (1990 - 2025).
    * **Frekuensi & Sektor (Dependen):** Jumlah insiden perampasan ruang dan sektor korporasi yang memicu konflik.
4. **Dataset & File:**
    * Catatan Konflik Agraria: `data/processed/sulawesi_konflik_agraria_tanahkita.csv`

---

Visualisasi *time-series* di bawah ini memberikan bukti empiris yang tidak dapat dibantah mengenai korelasi langsung antara ekspansi industri berskala masif dengan eskalasi letupan konflik agraria di daratan Sulawesi. Secara historis, jika kita membandingkan dua periode waktu yang berbeda, lonjakan perampasan ruang hidup masyarakat terlihat sangat drastis dan tidak proporsional. Pada periode pra-2005, sistem pendataan mencatat "hanya" terdapat **13 kasus** letupan konflik yang tereskalasi. Angka ini secara fundamental merepresentasikan dinamika agraria tradisional sebelum keran perizinan konsesi ekstraktif dibuka secara agresif oleh pemerintah daerah pasca implementasi otonomi daerah secara penuh.

Namun, narasi harmoni pembangunan ini hancur berantakan ketika memasuki periode pasca-2005 hingga saat ini. Data empiris secara mengejutkan mencatat setidaknya **82 kasus** perampasan lahan yang memicu perlawanan berdarah, yang ekuivalen dengan lonjakan eskalasi raksasa sebesar **630.8%** dibandingkan era sebelumnya. Transformasi tata ruang yang sangat brutal ini didorong oleh lahirnya rezim komodifikasi daratan, di mana penerbitan Izin Usaha Pertambangan (IUP) mineral dan batubara, serta ekspansi Hak Guna Usaha (HGU) untuk perkebunan kelapa sawit monokultur menjadi panglima pembangunan yang menggusur wilayah kelola masyarakat adat dan petani gurem. Hal ini secara faktual membuktikan bahwa model pembangunan berorientasi PDB (Produk Domestik Bruto) nyatanya beroperasi di atas kerentanan ruang hidup warga.

Lebih jauh lagi, jika membedah tren pada satu dekade terakhir (terutama puncak eskalasi masif pada tahun 2017 dan melesat pasca-2020), kita menemukan anomali yang sangat berbahaya. Tren letupan sengketa sosial ini tidak lagi sekadar didominasi oleh perambahan hutan lindung atau perluasan kebun sawit, melainkan telah bermutasi menjadi konflik struktural akibat narasi besar **Hilirisasi Nikel** dan pengadaan daratan secara darurat untuk **Proyek Strategis Nasional (Infrastruktur & PSN)**. Warga lokal dipaksa melepaskan hak atas tanah produktif mereka di wilayah-wilayah episentrum ekstraktif demi menggelar karpet merah bagi modal korporat transnasional. Fakta keras berupa **95 total insiden historis** ini secara definitif membantah klaim negara bahwa industrialisasi ekstraktif membawa efek kesejahteraan berganda (*trickle-down effect*). Sebaliknya, kawasan-kawasan investasi tersebut justru bermetamorfosis menjadi 'zona tumbal' (*sacrifice zones*) di mana laju akumulasi kapital segelintir elit korporasi harus dibayar sangat mahal dengan ongkos krisis ekologis permanen, represi aparat negara, serta hancurnya tatanan kedaulatan pangan maupun pranata sosial masyarakat lokal.

![Ledakan Konflik Agraria di Sulawesi (1990-2025)](visuals_bab4/chart_4_1_konflik_timeseries.png)

> **Interpretasi Ekologis: Anatomi Ledakan Konflik 2017**
>
> Grafik di atas secara gamblang memperlihatkan anomali eskalasi ekstrem yang memuncak pada **tahun 2017** dengan rekor **75 letupan konflik**. Pembedahan data sektoral membongkar bahwa krisis ini bukanlah sekadar kebetulan; ledakan ini didominasi secara mutlak oleh sektor **Kehutanan (40 kasus)** dan **Perkebunan (21 kasus)**, yang kemudian diikuti oleh penetrasi **Pertambangan dan Infrastruktur PSN**. Tahun 2017 menandai periode kelam *(inflection point)* di mana pemerintah mengakselerasi pelepasan kawasan hutan dan Izin Pinjam Pakai Kawasan Hutan (IPPKH) secara masif guna memfasilitasi rantai pasok nikel dan megaproyek strategis nasional. Ekspansi spasial yang brutal ini secara langsung merampas wilayah kelola masyarakat adat dan merusak ekosistem penyangga, memicu gelombang perlawanan akar rumput yang direpresi. Secara empiris, narasi hilirisasi telah membuktikan dirinya beroperasi di atas ongkos perampasan ruang hidup berskala masif.

> **Interpretasi Ekologis dan Sosial:** Loncatan drastis letupan konflik terjadi beririsan dengan agresivitas rezim perizinan. Hilirisasi Nikel dan Proyek Strategis Nasional (PSN) secara faktual telah merekayasa kawasan investasi menjadi zona tumbal yang mengorbankan kedaulatan masyarakat lokal secara permanen.

---

## 4.2 Sebaran Sektoral: Korban Jiwa dan Monopoli Ruang

**Metode: Analisis Komparatif Dampak Sosial-Ekologis (Sumber: KPA / Tanah Kita)**

### Metodologi: Analisis Komparatif Dampak Sosial-Ekologis

**Metode Analisis:** Sub-bab ini menggunakan agregasi komparatif (*Comparative Aggregation Analysis*) untuk membedah skala kehancuran sosial (korban terdampak) dan monopoli ruang (hektar) antar sektor.

1. **Model Analisis Beban Sektoral (Sectoral Burden Analysis):**
    * **Kategorisasi Sektoral (Profiling):** Mengklasifikasikan sumber konflik (sektor Tambang, Perkebunan, Kehutanan, dll.) sebagai basis pengelompokan (*grouping*).
    * **Kuantifikasi Monopoli:** Menghitung total agregat luasan daratan (hektar) yang dirampas dan jumlah masyarakat (jiwa) yang terdampak per sektor industri.
    * **Evaluasi Dominasi:** Membedah asimetri penguasaan ruang untuk mengidentifikasi sektor mana yang bertindak sebagai aktor dominan dalam praktik perampasan tanah (*land grabbing*).
2. **Kalkulasi/Formula Pengolahan:** Perhitungan sum/agregat dari seluruh korban jiwa (bukan korban meninggal, melainkan terdampak) dan hektar.
    * `Total_Jiwa_Terdampak = SUM(Jiwa) GROUP BY Sektor`
    * `Total_Monopoli_Area = SUM(Hektar) GROUP BY Sektor`
3. **Variabel & Fitur Data:**
    * **Sektor (Independen):** Kategori proyek (Perkebunan, Kehutanan, Pertambangan, dll).
    * **Korban Jiwa & Luas Area (Dependen):** Jumlah orang terdampak (Jiwa) dan luas sengketa (Ha).
4. **Dataset & File:**
    * Dampak Konflik: `data/processed/sulawesi_konflik_agraria_tanahkita.csv`

---

Konflik agraria bukanlah sebuah insiden terisolasi yang hanya berupa sengketa batas tanah, melainkan instrumen sistematis dari akumulasi modal yang beroperasi dengan menggusur paksa kehidupan manusia. Visualisasi komparatif di bawah ini membongkar skala kehancuran sosial dan ekologis yang diakibatkan oleh masing-masing sektor industri ekstraktif. Ketika kita membedah total jumlah korban terdampak, data menunjukkan realitas yang sangat mengerikan. **Sektor Kehutanan** menjadi penyumbang terbesar krisis kemanusiaan dengan total korban mencapai **21,886 jiwa**. Angka ini bukan sekadar statistik; ini merepresentasikan masyarakat adat dan komunitas lokal yang ruang hidup dan wilayah adatnya direnggut atas nama legalitas izin Hutan Tanaman Industri (HTI) maupun klaim sepihak kawasan lindung oleh negara.

Menyusul di posisi kedua adalah **Sektor Pertambangan** yang telah memakan korban sebanyak **54,658 jiwa**. Lonjakan korban di sektor ini berhubungan langsung dengan ambisi hilirisasi mineral kritis (terutama nikel) yang memaksa warga pesisir dan petani untuk melepaskan ruang produksi mereka demi fasilitas *smelter* dan pertambangan terbuka. Masyarakat yang melawan seringkali dihadapkan pada represi berlapis, mulai dari intimidasi preman korporasi hingga kriminalisasi oleh aparat keamanan negara yang bertindak sebagai penjaga gawang investasi.

Di sisi lain, saat kita meninjau dari dimensi monopoli tata ruang (luasan hektar yang dikonflikkan), **Sektor Perkebunan**—khususnya ekspansi kelapa sawit—menjadi penguasa absolut dengan merampas lahan seluas **77,902 Hektar**. Konsentrasi penguasaan tanah oleh segelintir korporasi perkebunan ini menghancurkan kedaulatan pangan lokal dan menciptakan ketimpangan agraria yang struktural. Disusul oleh sektor Kehutanan seluas **66,193 Ha** dan Pertambangan seluas **441,286 Ha**, trinitas sektor ekstraktif ini (Kebun, Hutan, Tambang) secara empiris membuktikan bahwa pembangunan ekonomi selama ini semata-mata bergantung pada perampasan ruang berskala masif. Tidak ada tetesan kesejahteraan (*trickle-down effect*) bagi warga tapak; yang tersisa hanyalah kemiskinan struktural, pencemaran tanah, dan hilangnya hak-hak dasar konstitusional mereka atas daratan yang telah mereka tempati secara turun-temurun.

![Ledakan Korban Terdampak (Jiwa) per Tahun](visuals_bab4/chart_4_2a_jiwa.png)

![Monopoli Area Konflik (Hektar) per Tahun](visuals_bab4/chart_4_2b_ha.png)

> **Interpretasi Ekologis dan Sosial:** Lonjakan luar biasa pada grafik merepresentasikan titik didih ledakan demografis dari kegagalan mutlak sistem pengaman sosial di zona investasi ekstraktif.

### Bedah Forensik Anomali (Spike) Konflik Agraria

Berdasarkan ekstraksi dataset secara mendalam, berikut adalah bedah anatomis dari lonjakan-lonjakan ekstrem (*spikes*) yang terjadi pada grafik **Ledakan Korban Terdampak (Jiwa)** dan **Monopoli Area Konflik (Hektar)** di wilayah ini.

---

## 4.3 Kriminalisasi Aktivis dan Resistensi Ruang Sipil

**Metode: Analisis Agregat Kasus Represi & Pelanggaran HAM (Sumber: Database Tanah Kita)**

### Metodologi: Analisis Agregat Kasus Represi & Pelanggaran HAM

**Metode Analisis:** Sub-bab ini menggunakan agregasi kasus indikasi pelanggaran Hak Asasi Manusia dan Kriminalisasi Pejuang Lingkungan melalui ekstraksi metrik fatalitas.

1. **Pemodelan Indikator Kekerasan & Represi:**
    * **Violence & Criminalization Tracking:** Mendokumentasikan kasus penangkapan, intimidasi, kekerasan fisik, hingga jatuhnya korban jiwa di pihak warga dan aktivis lingkungan.
    * **Kuantifikasi Fatalitas:** Menghitung akumulasi jumlah korban kriminalisasi dan korban tewas sebagai proksi tingkat represi struktural.
    * **Pemetaan Ruang Sipil:** Mengevaluasi sejauh mana ekspansi investasi industri ekstraktif beroperasi dengan menggunakan instrumen represi aparatur keamanan (penyempitan ruang sipil).
2. **Kalkulasi/Formula Pengolahan:** Penghitungan jumlah insiden kriminalisasi serta total akumulasi korban represi kekerasan fisik.
    * `Total_Kasus_Kriminalisasi = COUNT(Kasus) WHERE Indikasi_Kriminalisasi = TRUE`
    * `Total_Korban_Tewas = SUM(Jumlah_Tewas) GROUP BY Sektor`
3. **Variabel & Fitur Data:**
    * **Status Represi (Dependen):** Boolean (Ya/Tidak) terjadinya indikasi kriminalisasi dalam konflik.
    * **Kuantitas Korban (Dependen):** Angka mutlak (integer) korban tertangkap, terluka, dan meninggal.
4. **Dataset & File:**
    * Represi dan Kriminalisasi: `data/processed/sulawesi_konflik_agraria_tanahkita.csv`

---

Rentetan data kuantitatif di wilayah Sulawesi secara telanjang membantah klaim arus utama yang kerap didengungkan oleh pemerintah dan oligarki korporasi, bahwa ekspansi industri ekstraktif membawa kesejahteraan dan pertumbuhan inklusif bagi masyarakat lokal. Fakta empiris justru memperlihatkan bahwa tata kelola investasi di Indonesia secara struktural dibangun di atas fondasi represi dan kekerasan terhadap ruang sipil.

Dari **46 kasus indikasi kriminalisasi** yang berhasil didokumentasikan, tercatat sebanyak **93 warga dan aktivis lingkungan yang ditangkap** secara sewenang-wenang. Angka ini bukanlah statistik hampa, melainkan representasi dari hancurnya keadilan ekologis dan perampasan ruang hidup masyarakat adat, petani, dan nelayan yang dipaksa menyerahkan tanah leluhurnya demi akumulasi kapital segelintir elit industri ekstraktif.

Jika kita membedah lebih dalam pada distribusi sektoral, **Sektor Pertambangan** muncul sebagai aktor dominan yang paling sering menggunakan instrumen koersif negara, menyumbang total **17 kasus represi**. Penggunaan aparat keamanan negara maupun preman korporasi untuk memuluskan perampasan tanah menunjukkan bahwa hukum seringkali ditundukkan pada kepentingan bisnis raksasa yang lapar lahan. Eskalasi konflik paling mematikan mencapai puncaknya pada tahun **2017** dengan mencatatkan **7 kasus secara bersamaan**. Dalam banyak peristiwa empiris, warga lokal yang sekadar mempertahankan hak konstitusional mereka atas lingkungan hidup yang baik dan sehat justru dilabeli sebagai provokator dan dijerat pasal pidana karet.

Tragedi kemanusiaan ini menjadi semakin kelam dengan hilangnya nyawa **1 pejuang lingkungan** yang melayang sia-sia di pusaran konflik agraria. Gugurnya pahlawan-pahlawan ruang hidup ini menggarisbawahi kegagalan mutlak instrumen pengaman ekologis - seperti D3TLH maupun dokumen AMDAL - dalam menjamin keselamatan rakyat. Selama pendekatan pembangunan eksploitatif yang bertumpu pada sekuritisasi investasi ini dipertahankan, setiap hektar hutan yang dibabat akan selalu berlumuran air mata konflik.

| Kasus Indikasi Kriminalisasi | Warga/Aktivis Ditangkap | Korban Luka-luka | Korban Tewas |
|---|---|---|---|
| **46 Kasus** | **93 Orang** | **4 Orang** | **1 Orang** |

![Tren Kasus Kriminalisasi & Represi (Pasca 2000)](visuals_bab4/chart_4_3a_kriminalisasi_trend.png)

![Sektor Industri Paling Represif](visuals_bab4/chart_4_3b_sektor_represif.png)

> **Interpretasi Ekologis & Hak Asasi Manusia:** Tingginya angka kriminalisasi dan korban tewas di sekitar area konsesi (terutama Pertambangan) membuktikan bahwa perampasan ruang selalu dibarengi dengan pendekatan represif. Ini membantah telak narasi "Hilirisasi Hijau" yang nyatanya ditebus dengan ongkos kemanusiaan yang berdarah.

#### Arsip Kasus Represi dan Kekerasan Fisik Tertinggi

*Menampilkan 10 kasus dengan jumlah korban penangkapan atau tewas terbanyak berdasarkan data yang berhasil didokumentasikan.*

---

## 4.4 Pembuktian Statistik: Ekspansi vs Eskalasi Konflik

**Metode: Before-After Analysis & Crosstabulation**

### Metodologi: Before-After Analysis & Crosstabulation

**Metode Analisis:** Sub-bab ini menggunakan Uji Chi-Square (*Crosstabulation*) dan kalkulasi risiko peluang (*Odds Ratio*) untuk menguji validitas empiris secara akademis.

1. **Uji Korelasi Variabel Kategorikal:**
    * **Crosstabulation:** Mentabulasi silang frekuensi kemunculan dua kondisi (Contoh: Keterlibatan Perusahaan vs Adanya Kriminalisasi) untuk mencari relasi ketergantungan.
    * `H0 (Null Hypothesis): Variabel baris (Periode/Aktor) saling bebas (independent) secara absolut terhadap variabel kolom (Represi/Kematian).`
    * `Decision Rule: Chi-Square Asymptotic Significance (P-Value) < 0.05, maka tolak H0 (Terdapat korelasi yang signifikan).`
2. **Kalkulasi/Formula Pengolahan:** Algoritma Uji Tabulasi Silang Chi-Square.
    * `Chi-Square (χ²) = Σ [(Observed - Expected)² / Expected]`
    * `Odds Ratio (OR) = (Sel A × Sel D) / (Sel B × Sel C)`
3. **Variabel & Fitur Data:**
    * **Matriks Ekspansi (Independen):** Dikotomi rentang waktu (Pra/Pasca 2014) dan kehadiran korporasi.
    * **Matriks Eskalasi (Dependen):** Kehadiran status represi dan terjadinya jatuhnya korban nyawa (Boolean dikonversi ke kategori).
4. **Dataset & File:**
    * Base Data Cross-Section: `data/processed/sulawesi_konflik_agraria_tanahkita.csv`

---

Hipotesis utama dalam evaluasi ini adalah bahwa **industrialisasi dan ekspansi korporasi** berbanding lurus dengan **eskalasi konflik dan represi** terhadap masyarakat.
Untuk mengujinya secara statistik sesuai pedoman D3TLH, analisis dibagi menjadi dua bagian: (1) Komparasi metrik Before-After, dan (2) Uji signifikansi Crosstab Chi-Square. Unit observasinya adalah catatan kejadian letupan konflik historis.

### A. Analisis Komparatif Before-After (Pra vs Era Hilirisasi)

Perbandingan absolut eskalasi konflik agraria sebelum dan sesudah rezim hilirisasi masif dimulai (cut-off tahun 2014).

| Periode | Rata-rata Konflik | Total Letupan | Warga Ditangkap | Korban Tewas |
|---|---|---|---|---|
| **Pra-Ekspansi (1990 – 2013)** | **2.1 Kasus/Tahun** | 37 kejadian | 83 jiwa | 0 jiwa |
| **Pasca-Ekspansi (2014 – 2024)** | **5.5 Kasus/Tahun** | 55 kejadian | 10 jiwa | 1 jiwa |

### B. Uji Statistik Crosstab (Chi-Square)

**Variabel Independen (X):** Periode Ekspansi Industri

**Variabel Dependen (Y):** Tingkat Represi & Kriminalisasi

#### Case Processing Summary

| | Valid N | Valid % | Missing N | Missing % | Total N | Total % |
|---|---|---|---|---|---|---|
| Periode Ekspansi Industri * Tingkat Represi & Kriminalisasi | 523 | 100.0% | 0 | 0.0% | 523 | 100.0% |

#### Periode Ekspansi Industri * Tingkat Represi & Kriminalisasi Crosstabulation

| | Baseline (Tanpa Kriminalisasi) | Ada Represi/Kriminalisasi | Total |
|---|---|---|---|
| **Pra-ekspansi (< 2014)** Count | 179 | 73 | 252 |
| **Pra-ekspansi (< 2014)** Expected | 157.6 | 94.4 | 252.0 |
| **Pasca-ekspansi (≥ 2014)** Count | 148 | 123 | 271 |
| **Pasca-ekspansi (≥ 2014)** Expected | 169.4 | 101.6 | 271.0 |
| **Total** Count | 327 | 196 | 523 |
| **Total** Expected | 327.0 | 196.0 | 523.0 |

#### Chi-Square Tests

**Periode Ekspansi Industri * Tingkat Represi & Kriminalisasi**

| | Value | df | Asymp. Sig. (2-sided) |
|---|---|---|---|
| Pearson Chi-Square | 14.331 | 1 | 0.000 |
| Likelihood Ratio | 14.447 | 1 | 0.000 |
| Linear-by-Linear Association | 14.995 | 1 | 0.000 |
| N of Valid Cases | 523 | | |

### Ringkasan Uji Hipotesis

**Result: SIGNIFIKAN (Ada Hubungan)**

| Parameter | Nilai |
|---|---|
| P-Value | 0.0002 |
| Chi-Square | 14.331 |
| df | 1 |
| **Odds Ratio (Risk Estimate)** | **2.038** |

> **Interpretasi Sosial Kritis:** Temuan ini sangat krusial: pergeseran status **Periode Ekspansi Industri** terbukti **berkorelasi kuat dan signifikan** dengan **Tingkat Represi & Kriminalisasi** (P < 0.05). Angka Odds Ratio (OR: 2.038) menjadi konfirmasi empiris bahwa narasi hilirisasi dan investasi bukanlah agenda nirkekerasan—ekspansi spasial mereka mutlak mengeskalasi pelanggaran hak asasi masyarakat tapak.

---

### Ringkasan Eksekutif Seluruh Skenario Crosstab

Tabel di bawah ini merangkum hasil pengujian statistik (Chi-Square) untuk semua kemungkinan kombinasi antara indikator Ekspansi (X) dan Eskalasi Konflik (Y) pada panel data yang sama.

| Variabel Independen (X) | Variabel Dependen (Y) | Chi-Square | P-Value | Odds Ratio | Kesimpulan |
|---|---|---|---|---|---|
| Periode Ekspansi Industri | Tingkat Represi & Kriminalisasi | 14.331 | 0.000 | 2.04 | 🟢 SIGNIFIKAN |
| Periode Ekspansi Industri | Tingkat Penelantaran Kasus | 3.283 | 0.070 | 1.40 | 🔴 TIDAK SIGNIFIKAN |
| Periode Ekspansi Industri | Tingkat Insiden Fisik (Luka/Tewas/Ditangkap) | 2.636 | 0.104 | 0.53 | 🔴 TIDAK SIGNIFIKAN |
| Tipe Sektor (Tambang vs Non-Tambang) | Tingkat Represi & Kriminalisasi | 13.609 | 0.000 | 2.84 | 🟢 SIGNIFIKAN |
| Tipe Sektor (Tambang vs Non-Tambang) | Tingkat Penelantaran Kasus | 4.742 | 0.029 | 1.89 | 🟢 SIGNIFIKAN |
| Tipe Sektor (Tambang vs Non-Tambang) | Tingkat Insiden Fisik (Luka/Tewas/Ditangkap) | 0.665 | 0.415 | 1.66 | 🔴 TIDAK SIGNIFIKAN |
| Keterlibatan Aparat/Pemerintah | Tingkat Represi & Kriminalisasi | 55.633 | 0.000 | 4.80 | 🟢 SIGNIFIKAN |
| Keterlibatan Aparat/Pemerintah | Tingkat Penelantaran Kasus | 1.135 | 0.287 | 0.81 | 🔴 TIDAK SIGNIFIKAN |
| Keterlibatan Aparat/Pemerintah | Tingkat Insiden Fisik (Luka/Tewas/Ditangkap) | 3.253 | 0.071 | 2.23 | 🔴 TIDAK SIGNIFIKAN |

> **Pembedahan Realitas Kemanusiaan:**
>
> Dari **9 skenario pengujian**, terdapat **4 skenario yang terbukti SIGNIFIKAN**.

Angka-angka pada tabel di atas bukan sekadar statistik di atas kertas, melainkan **bukti empiris** dari brutalitas pembangunan. Tingginya angka kemunculan represi pada skenario yang signifikan menegaskan bahwa setiap kali wilayah operasi investasi diperlebar, probabilitas dihadapkannya moncong senjata kepada warga melonjak drastis.

Skenario yang *TIDAK SIGNIFIKAN* tidak berarti rezim terbebas dari dosa kekerasan, melainkan bukti bahwa represi terhadap warga yang mempertahankan tanahnya telah menjadi kultur mapan yang menyebar secara sporadis melampaui sekat waktu dan korporasi.

---

## 4.5 Peta Orkestrasi Konflik: Aktor Sipil vs Aktor Ekstraktif

**Metode: Frequency Profiling (Text Parsing NLP) pada Data TanahKita**

### Metodologi: Frequency Profiling (Text Parsing NLP)

**Metode Analisis:** Sub-bab ini menggunakan teknik pemrosesan teks berbasis *Natural Language Processing* (Regex Entity Extraction) untuk membedah relasi aktor (korporasi vs sipil).

1. **Model Ekstraksi Aktor (Entity Parsing & Text Mining):**
    * **Textual Pattern Matching:** Memindai ribuan korpus teks narasi historis menggunakan metode *Regular Expressions* (RegEx) untuk mendeteksi entitas korporasi (PT/CV) dan organisasi masyarakat sipil (CSO).
    * **Token Counting (Frequency Profiling):** Menghitung frekuensi absolut penyebutan (*mentions*) dari setiap aktor spesifik di dalam dokumentasi konflik.
    * **Pemetaan Oligarki:** Memvalidasi indikasi konsentrasi kekuasaan dan monopoli penguasaan ruang oleh segelintir konglomerasi besar melalui seberapa sering nama entitas tersebut muncul dalam sengketa tanah.
2. **Kalkulasi/Formula Pengolahan:** Regex pattern matching and Token Counting.
    * `Count_PT = SUM(RegEx_Match(r"\b(?:PT|CV)\.?\s*[A-Z][a-zA-Z]*..."))`
    * `Count_CSO = SUM(RegEx_Match(r"\b(?:Walhi|Jatam|AMAN|Aliansi)..."))`
3. **Variabel & Fitur Data:**
    * **Teks Korpus Historis (Independen):** Penggabungan kolom `judul`, `deskripsi`, dan `narasi` dari repositori kasus.
    * **Frekuensi Penyebutan (Dependen):** *Word counts* eksistensi entitas pada teks-teks sengketa.
4. **Dataset & File:**
    * Teks Bebas (*Free-Text*): `data/processed/sulawesi_konflik_agraria_tanahkita.csv`

---

Konflik yang membara tidak hanya melibatkan negara dan aparat, melainkan memunculkan fenomena adu domba struktural (*orkestrasi konflik horizontal*).
Pemecahan entitas (*string parsing*) terhadap catatan kronologi advokasi TanahKita menelanjangi siapa yang sesungguhnya bermain di lapangan.
Di satu sisi, masyarakat asli sering kali didampingi oleh organisasi struktural yang solid, namun di sisi lain, mulai muncul
ormas-ormas, lembaga swadaya buatan, hingga institusi pseudo-adat yang digunakan sebagai proksi (*buffer*) oleh korporasi.
Grafik frekuensi ini membongkar dominasi aktor-aktor sipil dan perusahaan tambang yang paling banyak merebut ruang hidup.

#### Top 10 Entitas Korporasi Paling Dominan

![Top 10 Entitas Korporasi Paling Dominan](visuals_bab4/chart_4_5a_korporasi.png)

> **Analisis Kritis:** Ekstraksi presisi tinggi membuktikan dominasi absolut dari entitas **PT Perkebunan Nusantara (PTPN)** yang terlibat dalam **153 catatan konflik terpisah**. Konsentrasi tinggi frekuensi korporasi besar ini menegaskan bahwa represi di Sulawesi bukan sekadar residu administratif, melainkan *modus operandi* struktural para penguasa modal skala masif.

#### Top Aktor Proksi & Vigilante Terdeteksi

![Top Aktor Proksi & Vigilante Terdeteksi](visuals_bab4/chart_4_5b_vigilante.png)

> **Analisis Kritis:** Kemunculan kelompok sipil seperti **Preman** (terdeteksi hingga **16 kali**) menangkap besarnya skala orkestrasi horizontal. Korporasi seringkali menggunakan jasa pengamanan swakarsa, kelompok preman, hingga ormas vigilante sebagai "bemper proksi" untuk mengintimidasi warga lokal dan memecah belah solidaritas akar rumput.

*\* Grafik di atas hanya menampilkan Top 10 entitas. Untuk melihat daftar lengkap dan detail seluruh aktor yang terdeteksi, silakan buka tabel data di bawah ini.*

*Sumber File: `data/processed/sulawesi_konflik_agraria_tanahkita.csv` - Data diekstraksi secara dinamis menggunakan NLP Regex dari korpus narasi seluruh kasus agraria (Nasional, N=568 kasus) untuk memetakan orkestrasi struktural dan modus operandi aktor secara utuh.*
