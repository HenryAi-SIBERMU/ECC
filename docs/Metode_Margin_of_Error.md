# Panduan Lengkap: Validitas Data & Batasan Riset (Data Limitations)

## 1. Pendahuluan
Dokumen ini disusun sebagai panduan standar dalam menjelaskan konsep metodologi, penanganan masalah data, dan justifikasi validitas untuk proyek riset Celios2. Panduan ini dirancang agar tim dapat menjawab pertanyaan-pertanyaan metodologis dari *stakeholder* atau audiens dengan argumen statistik dan data science yang solid.

---

## 2. Mengapa "Margin of Error" (MoE) Tidak Berlaku di Riset Ini?
Seringkali muncul pertanyaan mengenai besaran **Margin of Error (MoE)** dari data yang digunakan. Namun, perlu dipahami bahwa **rumus statistik Margin of Error HANYA berlaku untuk riset yang menggunakan *Probability Sampling* (seperti survei kuesioner ke sebagian responden secara acak).**

Riset Celios2 menganalisis data menggunakan:
1. **Data Sensus / Administratif:** (Misal: PDRB BPS, Ekspor BPS, Izin Tambang ESDM, Data Faskes). Ini adalah data absolut seluruh populasi (tidak di-*sampling*).
2. **Data Satelit / Geospasial:** (Misal: GFW Deforestasi, NASA NO2). Data ini merekam seluruh permukaan bumi (Sulawesi), bukan mengambil sampel sebagian wilayah acak.
3. **Data Insiden / Rekam Kasus:** (Misal: Konflik Agraria, Zoonosis, Bencana). Ini adalah rekapitulasi jumlah kasus faktual di lapangan.

### Argumen Defensif (Golden Standard)
Jika ditanya mengenai Margin of Error dari riset ini, ini adalah standar jawaban yang sangat sah secara akademik:
> *"Riset ini menggunakan metode analisis data sekunder berskala besar (Big Data), sensus administratif, dan penginderaan jauh (satelit), BUKAN survei probability sampling. Karena kami menganalisis seluruh populasi data yang terekam secara resmi, **konsep statistik Margin of Error dari sampling tidak berlaku (MoE = 0%)**. Adapun batasan validitas pada riset ini terletak pada ketersediaan data resmi instansi (Missing Values) dan potensi kasus tak terlapor di lapangan (Under-reporting), bukan dari bias pengambilan sampel."*

---

## 3. Penanganan Data Bolong (*Missing Data* / *Gapped Time-Series*)
Dalam analisis data sekunder historis (contoh: rentang 10 tahun ke belakang), sangat wajar ditemukan *Missing Values* (ketiadaan data pada tahun tertentu). Dalam data science, kondisi ini dikenal sebagai **Gapped Time Series** atau **Sparse Data**. 

Keberadaan data yang berlubang/bolong adalah hal yang **sangat sah dan merupakan realitas wajar** di dunia akademik maupun riset industri. Namun, data tidak boleh dibiarkan kosong (NaN) begitu saja saat divisualisasikan karena akan merusak garis tren grafik.

### Solusi Teknis (Teknik Imputasi)
Untuk menambal *gap* tersebut, riset ini menggunakan *Golden Standard* dalam Data Science yang disebut **Data Imputation (Imputasi Data)**. Berikut adalah metode yang digunakan:

1. **Linear Interpolation (Interpolasi Linear) - *Standar Emas Demografi***
   - **Konteks:** Standar emas dari BPS dan Bank Dunia untuk data demografi.
   - **Logika:** Menarik garis lurus (nilai tengah) di antara dua data historis yang tersedia. Asumsinya, variabel seperti demografi populasi berubah secara linier konstan dan tidak melompat drastis secara tiba-tiba.
   - **Contoh:** Jika data populasi 2018 = 100 ribu dan 2020 = 120 ribu, maka kekosongan data di tahun 2019 (NaN) akan diisi dengan estimasi interplasi sebesar 110 ribu.

2. **Forward Fill / LOCF (Last Observation Carried Forward)**
   - **Konteks:** Digunakan jika data di tahun-tahun ujung yang paling baru (misal 2023 atau 2024) belum dirilis oleh pemerintah atau instansi terkait.
   - **Logika:** Mengasumsikan kondisi terakhir masih bertahan stabil / belum ada perubahan yang terdata secara resmi. 
   - **Contoh:** Meng-*copy* nilai riil dari rilis tahun 2022 untuk mengisi kekosongan data di tahun 2023.

3. **KNN Imputation / MICE (Advanced Machine Learning)**
   - **Konteks:** Standar lanjut yang biasa dipakai untuk *publish* jurnal akademik level Q1 (Internasional).
   - **Logika:** Daripada menebak menggunakan garis lurus, pendekatan ini menggunakan algoritma *Machine Learning* untuk memprediksi angka yang hilang berdasarkan pola dari variabel-variabel lain di dataset.
   - **Catatan:** Untuk cakupan laporan riset Celios, metode ini dianggap *overkill* dan pendekatan poin 1 dan 2 (Interpolasi & LOCF) sudah sangat valid secara saintifik.

### Kalimat *Disclaimer* untuk Laporan Metodologi
Untuk menjaga integritas ilmiah riset dan transparansi data, sangat direkomendasikan untuk mencantumkan *disclaimer* teknis ini pada bagian metodologi laporan:

> *"Dalam proses pengolahan data demografi dan *time-series* untuk rentang periode pengamatan 2014-2024, ditemukan beberapa *missing values* (ketiadaan data) pada tahun-tahun tertentu bersumber dari basis data resmi pemerintah. Untuk menjaga kontinuitas kelengkapan tren *time-series*, tahapan Data Pre-Processing pada riset ini menggunakan teknik **Linear Interpolation** dan **Forward Fill** untuk mengestimasi nilai pada periode tahun yang kosong. Pendekatan ini merupakan standar prosedur umum dan valid dalam pengolahan data statistik sekunder."*
