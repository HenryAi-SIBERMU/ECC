# Audit Laporan Per-Halaman (Page-by-Page Master Audit)

Dokumen ini menyajikan hasil audit baris demi baris dari seluruh file halaman (pages) aplikasi dasbor analitik. Seluruh teks narasi, kartu metrik dinamis, dan visualisasi yang menyajikan angka Global Forest Watch (GFW) telah diekstrak dan dibandingkan nilainya secara presisi antara **Data Lama (Sebelum V3)** vs **Data API V3 (Sekarang)**.

---

## Halaman Overview Temuan dan Ringkasan Riset

Tabel berikut menyajikan rincian perubahan data pada Halaman Overview Temuan:

| Posisi UI pada Halaman Overview Temuan | Kutipan Teks Harfiah di Layar Dasbor | Angka Lama (Sebelum V3) | Angka API V3 (Sekarang) |
| :--- | :--- | :---: | :---: |
| **1. Kartu Strip Expander 1** | Kartu Metrik Ringkasan Bab 1: `Deforestasi` | **2,107,041 Ha** | **1,001,654 Ha** |
| **2. Kartu Strip Expander 2** | Kartu Metrik Ringkasan Bab 2: `Deforestasi` | **2,107,041 Ha** | **1,001,654 Ha** |
| **3. Sub-Bab 2.4 (Card Merah)** | Header Card: **PERTAMBANGAN DAN SAWIT**<br>*"Luas Deforestasi Komoditas Sektor Industri"* | **2,107,041 Ha**<br>(87.5% dari total) | **1,001,654 Ha**<br>(72.3% dari total) |
| **4. Sub-Bab 2.4 (Card Kuning)** | Header Card: **PERTANIAN BERPINDAH**<br>*"Luas Deforestasi Akses Subsisten Masyarakat"* | **21,091 Ha**<br>(0.9% dari total) | **55,905 Ha**<br>(4.0% dari total) |
| **5. Sub-Bab 2.4 (Card Hitam/Merah)** | Header Card: **RASIO KEJAHATAN**<br>*"Industri menghancurkan hutan **{ratio} kali lebih banyak** dibanding petani kecil"* | **100x**<br>(100 kali lipat) | **18x**<br>(18 kali lipat) |
| **6. Dropdown Crosstab (1.4 & 2.2)** | Menu Dropdown: **"Total Deforestasi Alam (Hektar)"** vs **"Deforestasi Komoditas Tambang/Sawit (Hektar)"** | Opsi Pilihan Variabel Y | Opsi Pilihan Variabel Y |

---

## Bab 1: Ekspansi Industri Ekstraktif

Tabel berikut menyajikan rincian perubahan data pada Bab 1 (Ekspansi Industri Ekstraktif):

| Posisi UI pada Bab 1: Ekspansi Industri | Kutipan Teks Harfiah di Layar Dasbor | Angka Lama (Sebelum V3) | Angka API V3 (Sekarang) |
| :--- | :--- | :---: | :---: |
| **1. Bento Card KPI** | `Luas Deforestasi Komoditas` | **2,107,041 Ha** | **1,001,654 Ha** |
| **2. Hero Statement Narasi** | *"Secara bersamaan, kucuran realisasi PMDN... berbanding lurus dengan akumulasi konversi tutupan hutan sebesar **{angka} Hektar**..."* | **2,107,041 Hektar** | **1,001,654 Hektar** |
| **3. Pembedahan Ekologis (Poin 1)** | *"1. Aktor Utama Deforestasi (Donut Chart): Konversi tutupan hutan terbesar didominasi oleh Ekspansi Komoditas (Tambang & Perkebunan Monokultur) yang mencapai **{angka} Hektar** ({mha}),..."* | **4,931,210 Hektar**<br>(4.9 Mha) | **1,001,654 Hektar**<br>(1.0 Mha) |
| **4. Pembedahan Ekologis (Poin 3)** | *"3. Estimasi Emisi Karbon (Bar Chart Kanan): Konversi hutan alam untuk aktivitas komoditas melepaskan estimasi emisi sebesar **{angka} Megagrams CO2**,..."* | **3,371,872,868**<br>Megagrams CO2 | **581,089,000**<br>Megagrams CO2 |
| **5. Panel Indikator Donut Chart** | Label Teks Merah Samping Donut Chart: **Ekspansi Komoditas** | **4.9 Mha** | **1.0 Mha** |
| **6. Dropdown Crosstab (Variabel Y)** | *Parameter Perhitungan Filter:*<br>**"Batas Median Data"** | **3,114 Ha**<br>*(Tidak Tampil di UI)* | **1,387 Ha**<br>*(Tidak Tampil di UI)* |

---

## Bab 2: Kualitas Lingkungan di Kawasan Smelter

Tabel berikut menyajikan rincian perubahan data pada Bab 2 (Kualitas Lingkungan di Kawasan Smelter):

| Posisi UI pada Bab 2: Kualitas Lingkungan | Kutipan Teks Harfiah di Layar Dasbor | Angka Lama (Sebelum V3) | Angka API V3 (Sekarang) |
| :--- | :--- | :---: | :---: |
| **1. Bento Card KPI** | `Konversi Deforestasi` | **2,107,041 Ha** | **1,001,654 Ha** |
| **2. Hero Statement Narasi** | *"Data menunjukkan bahwa konversi tutupan hutan mencapai **{angka} Hektar**..."* | **2,107,041 Hektar** | **1,001,654 Hektar** |
| **3. Sub-Bab 2.4 Narasi Emisi Tambang** | *"Data menunjukkan bahwa sektor Pertambangan dan Sawit mencatatkan estimasi emisi CO₂ sebesar **{emisi} Juta Ton** dari konversi lahan seluas **{luas} Hektar**."* | **1,339.5 Juta Ton**<br>(dari 2,107,041 Ha) | **581.1 Juta Ton**<br>(dari 1,001,654 Ha) |
| **4. Sub-Bab 2.4 Narasi Porsi Emisi** | *"Tingkat emisi ini mencakup **{pct}%** dari total emisi karbon akibat hilangnya tutupan pohon..."* | **88.0%** | **72.3%** |
| **5. Sub-Bab 2.4 Narasi Emisi Petani** | *"...berbanding dengan aktivitas Pertanian Berpindah yang melepaskan emisi sebesar **{emisi} Juta Ton**."* | **13.2 Juta Ton** | **32.4 Juta Ton** |
| **6. Dropdown Crosstab (2.3)** | *Parameter Perhitungan Filter:*<br>**"Batas Median Data"** | **3,114 Ha**<br>*(Tidak Tampil di UI)* | **2,763 Ha**<br>*(Tidak Tampil di UI)* |

---

## Bab 5: Pola Penerbitan Izin Usaha Pertambangan

Tabel berikut menyajikan rincian perubahan data pada Bab 5 (Pola Penerbitan Izin Usaha Pertambangan):

| Posisi UI pada Bab 5: Pola Penerbitan Izin | Kutipan Teks Harfiah di Layar Dasbor | Angka Lama (Sebelum V3) | Angka API V3 (Sekarang) |
| :--- | :--- | :---: | :---: |
| **1. Hero Statement Narasi** | *"Selama satu dekade terakhir, total deforestasi tercatat sebesar **{angka} hektar**..."* | **2,078,652.3 Hektar** | **1,386,055.4 Hektar** |
| **2. Sub-Bab 5.2 Fakta Spasial** | *"Dalam dekade terakhir, total lebih dari **{angka} hektar** kawasan livelihood (Pertanian, Peternakan, dan Perkebunan) warga tercatat mengalami perubahan tutupan lahan..."* | **56,720 Hektar** | **41,785 Hektar** |
| **3. Sub-Bab 5.1 Dual-Axis Chart** | Kurva Batang: **Total Deforestasi (Hektar)** | **Bentuk Grafik Salah**<br>*(Bukan Angka Teks di UI)* | **Bentuk Grafik Akurat**<br>*(Bukan Angka Teks di UI)* |
| **4. Dropdown Uji Crosstab (5.4)** | Hasil Uji: **"Total Deforestasi Alam (Hektar)"** vs **"Deforestasi Komoditas"** | **TIDAK SIGNIFIKAN**<br>*(Salah data Sulteng-Sulut)* | **SIGNIFIKAN SEMUA**<br>*(Pola data akurat)* |

---

## Bab 7: Kegagalan Tata Kelola dan Bab 8: Distribusi Manfaat

Tabel berikut menyajikan rincian parameter logika di balik layar (persentil) dan perubahan threshold pada Bab 7 (Kegagalan Tata Kelola) dan Bab 8 (Distribusi Manfaat):

| Posisi UI pada Bab 7 dan Bab 8 | Parameter Logika di Balik Layar (Persentil) | Data Lama (Sebelum V3) | Data API V3 (Sekarang) |
| :--- | :--- | :---: | :---: |
| **1. Matriks Crosstab (Total Deforestasi Alam)** | **Ambang Batas "Kritis"** *(Percentile 66%)* | **> 39.633 Ha**<br>*(Threshold Terlalu Tinggi)* | **> 26.526 Ha**<br>*(Threshold Akurat)* |
| **2. Matriks Crosstab (Total Deforestasi Alam)** | **Jumlah Izin di Zona "Kritis"** *(Efek Perubahan Threshold)* | **260 Izin Baru Keluar** | **277 Izin Baru Keluar** |
| **3. Matriks Crosstab (Deforestasi Komoditas)** | **Ambang Batas "Kritis"** *(Percentile 66%)* | **> 40.041 Ha**<br>*(Threshold Terlalu Tinggi)* | **> 19.334 Ha**<br>*(Threshold Akurat)* |
| **4. Matriks Crosstab (Deforestasi Komoditas)** | **Jumlah Izin di Zona "Kritis"** *(Efek Perubahan Threshold)* | **260 Izin Baru Keluar** | **277 Izin Baru Keluar** |

---

## Halaman Infografis Ringkasan dan Fakta Kunci

Tabel berikut menyajikan rincian perubahan data pada Halaman 12 (Ringkasan Infografis) dan Halaman 13 (Fakta Kunci Infografis):

| Posisi UI pada Halaman Infografis | Kutipan Teks Harfiah di Layar Dasbor | Angka Lama (Sebelum V3) | Angka API V3 (Sekarang) |
| :--- | :--- | :---: | :---: |
| **1. Panel Kartu Ringkasan (Halaman 12)** | Label Panel: **Kehilangan Tutupan Pohon** | **2,078,652 Ha** | **1,386,055 Ha** |
| **2. Panel Kartu Ringkasan (Halaman 12)** | Label Panel: **Deforestasi (Tambang/Sawit)** | **2,107,041 Ha** | **1,001,654 Ha** |
| **3. Card Sorotan Fakta (Halaman 13)** | Card Fakta Kunci: *"Deforestasi di Kawasan Konservasi & Lindung"* | **2,078,652 Ha** | **41,785 Ha** |

---

## Sinkronisasi Dokumen Naratif (Outline 8 Juli 2026.md)

Berikut adalah daftar temuan di mana teks naratif dan angka di dalam draft dokumen laporan/outline masih menggunakan **Data Lama (Pra-V3)** dan perlu direvisi agar konsisten dengan audit API V3:

| No | Lokasi di Dokumen Outline | Kutipan / Kalimat di Outline (Data Lama) | Angka Lama di Outline | Angka Baru API V3 (Sesuai Audit) | Saran Kalimat Outline Baru |
| :---: | :--- | :--- | :---: | :---: | :--- |
| **1** | **Temuan Studi** (Baris 113) | *"2,1 Juta Hektare Hutan Dibabat Tambang dan Sawit"* | **2,1 Juta Ha** | **1.001.654 Ha**<br>*(Data 6 Provinsi, dgn Sulbar)* | *"1 Juta Hektare Hutan Dibabat Tambang dan Sawit"* |
| **2** | **Temuan Studi** (Baris 113) | *"2 Juta Hektare Hutan Hilang, 88% Didorong Tambang dan Perkebunan"* | **2 Juta Ha** (Total Loss)<br>**88%** (Porsi) | **1.094.742 Ha** (Total Deforestasi)<br>**82,4%** (Porsi Tambang & Sawit)<br>*(Data 5 Provinsi, tanpa Sulbar)* | *"1,09 Juta Hektare Total Deforestasi, 82,4% Didorong Tambang dan Sawit"* |
| **3** | **Temuan Studi** (Baris 114) | *"Angka ini 100 kali lebih besar dibanding hutan yang hilang..."* | **100 kali** | **17 kali**<br>*(Data 5 Provinsi, tanpa Sulbar)* | *"Angka ini 17 kali lebih besar dibanding hutan yang hilang..."* |
| **4** | **Temuan Studi** (Baris 117) | *"...akibat ladang berpindah, yang hanya mencapai 21.091 hektare."* | **21.091 Ha** | **52.233 Ha**<br>*(Data 5 Provinsi, tanpa Sulbar)* | *"...akibat ladang berpindah, yang hanya mencapai 52.233 hektare."* |
| **5** | **Temuan Studi** (Baris 109) | *"1.339,5 juta ton CO₂ emisi dari deforestasi tambang dan perkebunan."* | **1.339,5 Juta Ton CO₂** | **597,8 Juta Ton CO₂**<br>*(Data 5 Provinsi, tanpa Sulbar)* | *"597,8 juta ton CO₂ emisi dari deforestasi tambang dan perkebunan."* |
| **6** | **Temuan Studi** (Baris 125) | *"56,7 Ribu Hektare Ruang Hidup Warga Hilang Tanpa Pemulihan"* | **56.720 Ha** | **91.578 Ha**<br>*(Data 6 Provinsi, dgn Sulbar)* | *"91,6 Ribu Hektare Kawasan Livelihood Warga Hilang Tanpa Pemulihan"* |
| **7** | **Bab 1** (Baris 245) | *"seluas 2.107.041 hektar atau 87,9% berasal dari kedua sektor..."* | **2.107.041 Ha**<br>**87,9%** | **902.068 Ha**<br>**83,8%**<br>*(Data 5 Provinsi, tanpa Sulbar)* | *"seluas 902.068 hektar atau 83,8% berasal dari kedua sektor..."* |
| **8** | **Bab 1** (Baris 245) | *"hanya mencapai 21.091 hektar atau sekitar 0,9%..."* | **21.091 Ha**<br>**0,9%** | **52.233 Ha**<br>**4,9%**<br>*(Data 5 Provinsi, tanpa Sulbar)* | *"hanya mencapai 52.233 hektar atau sekitar 4,9%..."* |
| **9** | **Bab 1** (Baris 245) | *"...mencapai sekitar 100 kali lebih besar dibandingkan pertanian berpindah."* | **100 kali** | **17 kali**<br>*(Data 5 Provinsi, tanpa Sulbar)* | *"...mencapai sekitar 17 kali lebih besar dibandingkan pertanian berpindah."* |
| **10** | **Bab 2** (Baris 297) | *"menyumbang sekitar 1.339,5 juta ton CO₂, atau sekitar 88%..."* | **1.339,5 Jt Ton**<br>**88%** | **597,8 Jt Ton**<br>**82,9%**<br>*(Data 5 Provinsi, tanpa Sulbar)* | *"menyumbang sekitar 597,8 juta ton CO₂, atau sekitar 82,9%..."* |
| **11** | **Bab 2** (Baris 299) | *"Emisi dari kategori tersebut hanya sekitar 13,2 juta ton CO₂..."* | **13,2 Juta Ton CO₂** | **35,6 Juta Ton CO₂**<br>*(Data 5 Provinsi, tanpa Sulbar)* | *"Emisi dari kategori tersebut hanya sekitar 35,6 juta ton CO₂..."* |
| **12** | **Bab 2** (Baris 303) | *"Pulau Sulawesi kehilangan sekitar 2 juta hektar tutupan pohon."* | **2 Juta Ha** | **1.386.055 Ha**<br>*(Data 6 Provinsi, dgn Sulbar)* | *"Pulau Sulawesi kehilangan sekitar 1,38 juta hektar tutupan pohon."* |
| **13** | **Bab 2** (Baris 315) | *"kontribusi pertanian berpindah hanya sekitar 21.091 hektar, atau kurang dari 1%..."* | **21.091 Ha**<br>**<1%** | **52.233 Ha**<br>**4,9%**<br>*(Data 5 Provinsi, tanpa Sulbar)* | *"kontribusi pertanian berpindah hanya sekitar 52.233 hektar, atau sekitar 4,9%..."* |
| **14** | **Bab 2** (Baris 321, 323) | *"...hampir seratus kali lebih besar dibandingkan kehilangan hutan..."* | **100 kali** | **17 kali**<br>*(Data 5 Provinsi, tanpa Sulbar)* | *"...sekitar 17 kali lebih besar dibandingkan kehilangan hutan..."* |
| **15** | **Bab 6** (Baris 540) | *"ketika deforestasi telah mencapai 2.078.652,3 hektare..."* | **2.078.652,3 Ha** | **1.386.055,4 Ha**<br>*(Data 6 Provinsi, dgn Sulbar)* | *"ketika deforestasi telah mencapai 1.386.055,4 hektare..."* |
| **16** | **Bab 6** (Baris 556) | *"...penyusutan sekitar 56,7 ribu hektare kawasan penghidupan..."* | **56.720 Ha** | **91.578 Ha**<br>*(Data 6 Provinsi, dgn Sulbar)* | *"...penyusutan sekitar 91,6 ribu hektare kawasan penghidupan..."* |
| **17** | **Bab 6** (Baris 572) | *"luas lahan yang terdampak mencapai sekitar 56,7 ribu hektare."* | **56.720 Ha** | **91.578 Ha**<br>*(Data 6 Provinsi, dgn Sulbar)* | *"luas lahan yang terdampak mencapai sekitar 91,6 ribu hektare."* |
| **18** | **Bab 8** (Baris 674) | **Matriks Crosstab Kepatuhan D3TLH** *(Visual/Tabel)* | Ambang Kritis **>40.041 Ha**<br>**260 Izin Kritis** | Ambang Kritis **>19.334 Ha**<br>**277 Izin Baru** | *(Perbarui visual tabel matriks Crosstab dengan angka baru dan 277 izin)* |

---

## Sinkronisasi Dokumen Naratif V2 (6 Provinsi Termasuk Sulbar)

Tabel berikut menyajikan perhitungan **V2** di mana Sulawesi Barat (Sulbar) **dimasukkan** ke dalam seluruh agregat (Total Deforestasi Komoditas = 1.192.196 Ha).

| No | Lokasi di Dokumen Outline | Kutipan / Kalimat di Outline (Data Lama) | Angka Lama di Outline | Angka Baru API V3 (6 Provinsi) | Saran Kalimat Outline Baru |
| :---: | :--- | :--- | :---: | :---: | :--- |
| **1** | **Temuan Studi** (Baris 113) | *"2,1 Juta Hektare Hutan Dibabat Tambang dan Sawit"* | **2,1 Juta Ha** | **1.001.654 Ha** | *"1 Juta Hektare Hutan Dibabat Tambang dan Sawit"* |
| **2** | **Temuan Studi** (Baris 113) | *"2 Juta Hektare Hutan Hilang, 88% Didorong Tambang dan Perkebunan"* | **2 Juta Ha** (Total)<br>**88%** (Porsi) | **1.192.196 Ha** (Deforestasi Komoditas)<br>**84,0%** (Porsi Tambang & Sawit) | *"1,19 Juta Hektare Deforestasi Komoditas, 84,0% Didorong Tambang dan Sawit"* |
| **3** | **Temuan Studi** (Baris 114) | *"Angka ini 100 kali lebih besar dibanding hutan yang hilang..."* | **100 kali** | **18 kali** | *"Angka ini 18 kali lebih besar dibanding hutan yang hilang..."* |
| **4** | **Temuan Studi** (Baris 117) | *"...akibat ladang berpindah, yang hanya mencapai 21.091 hektare."* | **21.091 Ha** | **55.905 Ha** | *"...akibat ladang berpindah, yang hanya mencapai 55.905 hektare."* |
| **5** | **Temuan Studi** (Baris 109) | *"1.339,5 juta ton CO₂ emisi dari deforestasi tambang dan perkebunan."* | **1.339,5 Juta Ton CO₂** | **581,1 Juta Ton CO₂** | *"581,1 juta ton CO₂ emisi dari deforestasi tambang dan perkebunan."* |
| **6** | **Temuan Studi** (Baris 125) | *"56,7 Ribu Hektare Ruang Hidup Warga Hilang Tanpa Pemulihan"* | **56.720 Ha** | **91.578 Ha** | *"91,6 Ribu Hektare Kawasan Livelihood Warga Hilang Tanpa Pemulihan"* |
| **7** | **Bab 1** (Baris 245) | *"seluas 2.107.041 hektar atau 87,9% berasal dari kedua sektor..."* | **2.107.041 Ha**<br>**87,9%** | **1.001.654 Ha**<br>**84,0%** | *"seluas 1.001.654 hektar atau 84,0% berasal dari kedua sektor..."* |
| **8** | **Bab 1** (Baris 245) | *"hanya mencapai 21.091 hektar atau sekitar 0,9%..."* | **21.091 Ha**<br>**0,9%** | **55.905 Ha**<br>**4,7%** | *"hanya mencapai 55.905 hektar atau sekitar 4,7%..."* |
| **9** | **Bab 1** (Baris 245) | *"...mencapai sekitar 100 kali lebih besar dibandingkan pertanian berpindah."* | **100 kali** | **18 kali** | *"...mencapai sekitar 18 kali lebih besar dibandingkan pertanian berpindah."* |
| **10** | **Bab 2** (Baris 297) | *"menyumbang sekitar 1.339,5 juta ton CO₂, atau sekitar 88%..."* | **1.339,5 Jt Ton**<br>**88%** | **581,1 Jt Ton**<br>**84,1%** | *"menyumbang sekitar 581,1 juta ton CO₂, atau sekitar 84,1%..."* |
| **11** | **Bab 2** (Baris 299) | *"Emisi dari kategori tersebut hanya sekitar 13,2 juta ton CO₂..."* | **13,2 Juta Ton CO₂** | **38,2 Juta Ton CO₂** | *"Emisi dari kategori tersebut hanya sekitar 38,2 juta ton CO₂..."* |
| **12** | **Bab 2** (Baris 303) | *"Pulau Sulawesi kehilangan sekitar 2 juta hektar tutupan pohon."* | **2 Juta Ha** | **1.386.055 Ha** | *"Pulau Sulawesi kehilangan sekitar 1,38 juta hektar tutupan pohon."* |
| **13** | **Bab 2** (Baris 315) | *"kontribusi pertanian berpindah hanya sekitar 21.091 hektar, atau kurang dari 1%..."* | **21.091 Ha**<br>**<1%** | **55.905 Ha**<br>**4,7%** | *"kontribusi pertanian berpindah hanya sekitar 55.905 hektar, atau sekitar 4,7%..."* |
| **14** | **Bab 2** (Baris 321, 323) | *"...hampir seratus kali lebih besar dibandingkan kehilangan hutan..."* | **100 kali** | **18 kali** | *"...sekitar 18 kali lebih besar dibandingkan kehilangan hutan..."* |
| **15** | **Bab 6** (Baris 540) | *"ketika deforestasi telah mencapai 2.078.652,3 hektare..."* | **2.078.652,3 Ha** | **1.386.055,4 Ha** | *"ketika deforestasi telah mencapai 1.386.055,4 hektare..."* |
| **16** | **Bab 6** (Baris 556) | *"...penyusutan sekitar 56,7 ribu hektare kawasan penghidupan..."* | **56.720 Ha** | **91.578 Ha** | *"...penyusutan sekitar 91,6 ribu hektare kawasan penghidupan..."* |
| **17** | **Bab 6** (Baris 572) | *"luas lahan yang terdampak mencapai sekitar 56,7 ribu hektare."* | **56.720 Ha** | **91.578 Ha** | *"luas lahan yang terdampak mencapai sekitar 91,6 ribu hektare."* |
| **18** | **Bab 8** (Baris 674) | **Matriks Crosstab Kepatuhan D3TLH** *(Visual/Tabel)* | Ambang Kritis **>40.041 Ha**<br>**260 Izin Kritis** | Ambang Kritis **>19.334 Ha**<br>**277 Izin Baru** | *(Perbarui visual tabel matriks Crosstab dengan angka baru dan 277 izin)* |
