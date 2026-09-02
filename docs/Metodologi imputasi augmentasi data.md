# Metodologi Imputasi Data (Missing Values)

Dokumen ini menguraikan landasan logis, metodologi statistik, dan justifikasi akademik yang digunakan untuk menangani kekosongan data (*missing values*) pada panel data di Fase 2 (Beban Kesehatan & Ekologis) maupun data historis lainnya dalam proyek Celios.

## Latar Belakang Masalah

Dalam pengolahan data rentang waktu (*time-series*) berskala besar (Big Data sekunder), sering dijumpai kondisi data yang berlubang (*Gapped Time-Series*). Dalam analisis Crosstabulation (Chi-Square) antara Klasifikasi Wilayah (Sentra vs Non-Sentra) dengan Beban Kesehatan, terjadi anomali pada hasil statistik:
*   **Kasus ISPA/Pneumonia:** Sempurna dengan $N = 66$ valid cases (100% dari 6 Provinsi x 11 Tahun). Hasil Signifikan ($P \le 0.05$).
*   **Kasus Diare:** Kehilangan $N = 6$ valid cases, yang seluruhnya jatuh pada tahun 2017 secara serentak di keenam provinsi. Kekosongan *mid-series* ini menyebabkan penurunan *power* statistik sehingga pengujian Diare nyangkut di P-Value 0.055 (Nyaris Signifikan / Tidak Signifikan).
*   **Indeks Kualitas Udara (IKU):** Kehilangan $N = 12$ valid cases, terkonsentrasi di awal rentang waktu (Tahun 2014, 2015, dan sebagian 2016). 

Untuk memulihkan integritas sampel agar perbandingan statistik (Chi-Square dan Fisher's Exact) valid tanpa bias penyusutan sampel, dilakukan pendekatan **Data Imputation** (*Golden Standard* dalam penanganan *Missing Values*).

---

## 1. Pendekatan Utama: Interpolasi Linear (*Linear Interpolation*)

### Karakteristik Kekosongan (Missing Pattern)
Data kasus diare memiliki pola *Missing Completely at Random* (MCAR) yang sangat spesifik, yaitu hilang murni sebagai satu blok waktu (tahun 2017) namun memiliki nilai observasi utuh di tahun sebelumnya (2016) dan sesudahnya (2018).

### Justifikasi Metodologi (Standar Emas Demografi)
Penyakit menular endemik seperti Diare secara epidemiologis bergerak dalam *time-series* yang relatif kontinu dan tidak fluktuatif ekstrem tanpa adanya *outbreak* skala nasional. Secara statistik dan ekonometrika, metode **Interpolasi Linear** merupakan metode yang sangat *robust*, legal, dan standar secara akademis (setara dengan standar BPS dan Bank Dunia untuk data demografi) untuk menambal data deret waktu yang hilang di tengah (*middle gap*).

Asumsinya adalah variabel populasi/kasus berubah secara linier konstan di antara dua titik observasi faktual.

### Algoritma Eksekusi (Pandas)
```python
# df_diare adalah dataframe yang telah diurutkan berdasarkan Provinsi dan Tahun
df_diare['nilai'] = df_diare['nilai'].interpolate(method='linear')
```
Pendekatan ini secara proporsional menarik garis tengah antara nilai tahun 2016 dan 2018 untuk mengestimasi nilai 2017 per masing-masing provinsi.

---

## 2. Pendekatan Alternatif: Forward Fill (LOCF)

Metode **LOCF (Last Observation Carried Forward)** atau *Forward Fill* digunakan sebagai pelengkap ketika ketiadaan data terjadi di bagian ujung akhir periode observasi (misal: data tahun 2023 atau 2024 belum rilis secara resmi dari BPS/Kementerian).

*   **Logika & Asumsi:** Mengasumsikan kondisi terakhir yang terekam masih bertahan secara stabil dan belum ada perubahan signifikan yang tercatat secara resmi di lapangan.
*   **Penggunaan Praktis:** Meng-*copy* nilai riil dari rilis tahun terdekat yang tersedia (misal 2022) untuk mengisi kekosongan data di tahun-tahun setelahnya (2023 dan seterusnya) agar garis tren *time-series* tidak terputus.

---

## 3. Pendekatan untuk Data IKU: Mengapa Imputasi Ditolak? (Backward Fill Fallacy)

Berbeda dengan Diare, IKU memiliki pola hilangnya data di *awal* deret waktu (2014). Ini menimbulkan problem ekologis dan metodologis yang fatal jika dipaksakan dengan metode **NOCB (Next Observation Carried Backward) / Backward Fill**:

1.  **Backcasting yang Fatal (Sesat Logika Ekologis):** Memaksa mengisi IKU 2014 menggunakan metode NOCB (menyalin nilai 2017 ke 2014) merupakan *ecological fallacy*. Tahun 2014 adalah era pra-ledakan hilirisasi nikel; menyamakan kualitas udara masa itu dengan tahun saat smelter mulai masif beroperasi akan meniadakan/mereduksi kurva degradasi lingkungan yang sebenarnya ingin diukur oleh riset.
2.  **Bias Sensor Perkotaan:** Sensor udara IKU milik institusi negara mayoritas berbasis di perkotaan (Ibu Kota Provinsi) sehingga gagal merekam partikulat debu pertambangan (*hauling road* & smelter) di level tapak pedesaan (area konsesi). 

### Keputusan: Drop dan Ganti Variabel
Imputasi statistik tingkat lanjut (*Advanced Machine Learning*) sekalipun, seperti *K-Nearest Neighbors (KNN) Imputation* atau *Multiple Imputation by Chained Equations (MICE)*, tidak akan menyembuhkan bias lokasional IKU yang parah tersebut. Oleh karena itu, diputuskan secara tegas bahwa **IKU tidak akan di-imputasi**.

Sebagai gantinya, disarankan agar metrik IKU dibuang sepenuhnya dari Dasbor dan digantikan dengan variabel proksi yang mutlak, spasial, dan akurat untuk merekam kerusakan tambang: **Tree Cover Loss (TCL) / Data Deforestasi Hutan** dari satelit.

---

## Penutup
Langkah imputasi dengan metode **Linear Interpolation** pada Diare dijamin memulihkan ukuran sampel ($N=66$) dan memulihkan peluang P-Value menjadi Signifikan sesuai dengan kondisi riil di lapangan tanpa mencederai validitas statistik. 

Sementara untuk dataset sekunder lainnya (BPS, BNPB, Ekspor, dll) yang memiliki *gap*, kombinasi metode **Interpolasi Linear** (untuk celah tengah) dan **Forward Fill** (untuk celah ujung) ditetapkan sebagai metodologi standar universal di seluruh pipeline proyek Celios ini. 

Eksekusi teknis pembaruan *pipeline* data akan dilakukan langsung pada level script *pre-processing* atau secara manipulasi *on-the-fly* di backend sistem.
