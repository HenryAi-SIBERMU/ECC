# Metodologi Imputasi Data (Missing Values)

Dokumen ini menguraikan landasan logis, metodologi statistik, dan justifikasi akademik yang digunakan untuk menangani kekosongan data (*missing values*) pada panel data di Fase 2 (Beban Kesehatan & Ekologis) dalam proyek Celios.

## Latar Belakang Masalah

Dalam analisis Crosstabulation (Chi-Square) antara Klasifikasi Wilayah (Sentra vs Non-Sentra) dengan Beban Kesehatan, terjadi anomali pada hasil statistik:
*   **Kasus ISPA/Pneumonia:** Sempurna dengan $N = 66$ valid cases (100% dari 6 Provinsi x 11 Tahun). Hasil Signifikan ($P \le 0.05$).
*   **Kasus Diare:** Kehilangan $N = 6$ valid cases, yang seluruhnya jatuh pada tahun 2017 secara serentak di keenam provinsi. Kekosongan *mid-series* ini menyebabkan penurunan *power* statistik sehingga pengujian Diare nyangkut di P-Value 0.055 (Nyaris Signifikan / Tidak Signifikan).
*   **Indeks Kualitas Udara (IKU):** Kehilangan $N = 12$ valid cases, terkonsentrasi di awal rentang waktu (Tahun 2014, 2015, dan sebagian 2016). 

Untuk memulihkan integritas sampel agar perbandingan statistik (Chi-Square dan Fisher's Exact) valid tanpa bias penyusutan sampel, dilakukan pendekatan **Data Imputation**.

---

## 1. Pendekatan untuk Data Diare: Interpolasi Linear (*Linear Interpolation*)

### Karakteristik Kekosongan (Missing Pattern)
Data kasus diare memiliki pola *Missing Completely at Random* (MCAR) yang sangat spesifik, yaitu hilang murni sebagai satu blok waktu (tahun 2017) namun memiliki nilai observasi utuh di tahun sebelumnya (2016) dan sesudahnya (2018).

### Justifikasi Metodologi
Penyakit menular endemik seperti Diare secara epidemiologis bergerak dalam *time-series* yang relatif kontinu dan tidak fluktuatif ekstrem tanpa adanya *outbreak* skala nasional. 
Secara statistik dan ekonometrika, metode **Interpolasi Linear** merupakan metode yang sangat *robust*, legal, dan standar secara akademis untuk menambal data deret waktu yang hilang di tengah (*middle gap*).

### Algoritma Eksekusi (Pandas)
```python
# df_diare adalah dataframe yang telah diurutkan berdasarkan Provinsi dan Tahun
df_diare['nilai'] = df_diare['nilai'].interpolate(method='linear')
```
Pendekatan ini secara proporsional menarik garis tengah antara nilai tahun 2016 dan 2018 untuk mengestimasi nilai 2017 per masing-masing provinsi.

---

## 2. Pendekatan untuk Data IKU: Mengapa Imputasi Ditolak?

Berbeda dengan Diare, IKU memiliki pola hilangnya data di *awal* deret waktu (2014). Ini menimbulkan problem ekologis dan metodologis:

1.  **Backcasting yang Fatal:** Melakukan *Linear Interpolation* tidak dimungkinkan karena hilangnya titik referensi awal. Memaksa mengisi IKU 2014 menggunakan metode *Next Observation Carried Backward* (NOCB) (menyalin nilai 2017 ke 2014) merupakan sesat logika (fallacy) secara ekologis. Tahun 2014 adalah era pra-ledakan hilirisasi nikel; menyamakan kualitas udara masa itu dengan tahun saat smelter mulai masif beroperasi akan meniadakan/mereduksi kurva degradasi lingkungan.
2.  **Bias Sensor Perkotaan:** Sensor udara IKU milik institusi negara mayoritas berbasis di perkotaan (Ibu Kota Provinsi) sehingga gagal merekam partikulat debu pertambangan (*hauling road* & smelter) di level tapak pedesaan (area konsesi). 

### Keputusan: Drop dan Ganti Variabel
Imputasi statistik canggih sekalipun seperti *Multiple Imputation by Chained Equations* (MICE) tidak akan menyembuhkan bias lokasional IKU. Oleh karena itu, diputuskan bahwa **IKU tidak akan di-imputasi**.

Sebagai gantinya, disarankan agar metrik IKU dibuang sepenuhnya dari Dasbor dan digantikan dengan variabel proksi yang mutlak, spasial, dan akurat untuk merekam kerusakan tambang: **Tree Cover Loss (TCL) / Data Deforestasi Hutan** dari satelit (contoh: Global Forest Watch).

---

## Penutup
Langkah imputasi pada Diare dijamin memulihkan ukuran sampel ($N=66$) dan memulihkan peluang P-Value menjadi Signifikan sesuai dengan kondisi riil di lapangan. Eksekusi teknis pembaruan *pipeline* data Diare akan dilakukan langsung pada level script *pre-processing* atau secara manipulasi *on-the-fly* di backend Streamlit.
