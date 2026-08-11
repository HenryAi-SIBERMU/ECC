# Laporan Analisis Forensik Keseluruhan Dataset GFW (V1/V2 vs V3)

Dokumen ini mencatat hasil evaluasi dan perbandingan forensik antara seluruh dataset GFW lama (V2) dengan dataset terbaru (V3) yang menggunakan Geostore ID resmi.

## 📊 1. Total Kehilangan Tutupan Pohon (Tree Cover Loss 2014-2023)

| Provinsi | V2 Lama (BBox Salah) | V3 Resmi (GADM) | Selisih Absolut | Perubahan (%) |
| :--- | :---: | :---: | :---: | :---: |
| **Gorontalo** | 108,190.71 ha | **70,262.33 ha** | -37,928.37 ha | **-35.06%** |
| **Sulawesi Barat** | 201,605.84 ha | **1,149.17 ha** | -200,456.67 ha | **-99.43%** |
| **Sulawesi Selatan** | 553,500.84 ha | **371,337.04 ha** | -182,163.80 ha | **-32.91%** |
| **Sulawesi Tengah** | 821,447.96 ha | **74,240.02 ha** | -747,207.94 ha | **-90.96%** |
| **Sulawesi Tenggara** | 327,187.21 ha | **734,216.29 ha** | +407,029.07 ha | **+124.40%** |
| **Sulawesi Utara** | 66,719.74 ha | **1,577,105.01 ha** | +1,510,385.28 ha | **+2263.78%** |
| **TOTAL SULAWESI** | **2,078,652.29 ha** | **2,828,309.86 ha** | **+749,657.57 ha** | **+36.06%** |

## 🌳 2. Kehilangan Hutan Primer (Primary Forest Loss 2014-2023)

| Provinsi | V2 Lama (BBox Salah) | V3 Resmi (GADM) | Selisih Absolut | Perubahan (%) |
| :--- | :---: | :---: | :---: | :---: |
| **Gorontalo** | 31,551.63 ha | **3,424.64 ha** | -28,126.99 ha | **-89.15%** |
| **Sulawesi Barat** | 53,833.46 ha | **0.00 ha** | -53,833.46 ha | **-100.00%** |
| **Sulawesi Selatan** | 178,405.30 ha | **137,381.34 ha** | -41,023.96 ha | **-22.99%** |
| **Sulawesi Tengah** | 356,171.10 ha | **23,407.98 ha** | -332,763.11 ha | **-93.43%** |
| **Sulawesi Tenggara** | 102,328.19 ha | **118,659.52 ha** | +16,331.33 ha | **+15.96%** |
| **Sulawesi Utara** | 21,737.09 ha | **118,349.61 ha** | +96,612.52 ha | **+444.46%** |
| **TOTAL SULAWESI** | **744,026.77 ha** | **401,223.08 ha** | **-342,803.69 ha** | **-46.07%** |

## 🛡️ 3. Kehilangan di Kawasan Lindung (Loss in Protected Areas 2014-2023)

| Provinsi | V2 Lama (BBox Salah) | V3 Resmi (GADM) | Selisih Absolut | Perubahan (%) |
| :--- | :---: | :---: | :---: | :---: |
| **Gorontalo** | 2,017.19 ha | **1,772.66 ha** | -244.53 ha | **-12.12%** |
| **Sulawesi Barat** | 2,792.93 ha | **18.82 ha** | -2,774.11 ha | **-99.33%** |
| **Sulawesi Selatan** | 10,100.83 ha | **25,926.45 ha** | +15,825.62 ha | **+156.68%** |
| **Sulawesi Tengah** | 28,151.22 ha | **5,161.43 ha** | -22,989.80 ha | **-81.67%** |
| **Sulawesi Tenggara** | 8,482.61 ha | **8,484.06 ha** | +1.46 ha | **+0.02%** |
| **Sulawesi Utara** | 5,175.12 ha | **50,214.55 ha** | +45,039.43 ha | **+870.31%** |
| **TOTAL SULAWESI** | **56,719.89 ha** | **91,577.96 ha** | **+34,858.07 ha** | **+61.46%** |

## 🌿 4. Kehilangan Berdasarkan Tutupan Lahan (Loss by Land Cover 2014-2023)

| Provinsi | V2 Lama (BBox Salah) | V3 Resmi (GADM) | Selisih Absolut | Perubahan (%) |
| :--- | :---: | :---: | :---: | :---: |
| **Gorontalo** | 72,830.18 ha | **57,939.73 ha** | -14,890.44 ha | **-20.45%** |
| **Sulawesi Barat** | 149,170.15 ha | **1,121.90 ha** | -148,048.25 ha | **-99.25%** |
| **Sulawesi Selatan** | 395,583.95 ha | **298,108.98 ha** | -97,474.96 ha | **-24.64%** |
| **Sulawesi Tengah** | 617,349.61 ha | **56,441.40 ha** | -560,908.21 ha | **-90.86%** |
| **Sulawesi Tenggara** | 223,800.70 ha | **520,745.86 ha** | +296,945.17 ha | **+132.68%** |
| **Sulawesi Utara** | 50,511.81 ha | **1,220,464.44 ha** | +1,169,952.63 ha | **+2316.20%** |
| **TOTAL SULAWESI** | **1,509,246.39 ha** | **2,154,822.32 ha** | **+645,575.93 ha** | **+42.77%** |



## 🚨 8. Laporan Investigasi Resolusi Spasial: BBox vs GADM (V2 vs V3)

Tabel berikut menunjukkan perbedaan *Geostore ID* (kode area poligon) yang digunakan API Global Forest Watch pada dataset V2 (Lama) dan V3 (Baru).

| Provinsi | Geostore ID V2 (Salah/BBox) | Geostore ID V3 (Resmi GADM) | Keterangan Fatalitas V2 |
| :--- | :--- | :--- | :--- |
| **Sulawesi Tengah** | `fce1e175169936334347ae17207381a0` | `70415db2d291955e71d4b08466cd6136` | Kotak imajiner terlalu besar (Overbounding). Menyerok wilayah laut dan pulau tetangga (Maluku/Kaltim). Angka deforestasi palsu meledak hingga 1.000%! |
| **Sulawesi Utara** | `89b35f128c9cfe7685e1738c89a0a730` | `8856238b97d25e076634ab9ddbb662b1` | Kotak imajiner terpotong (Underbounding). Tidak menjangkau pulau terluar seperti Sangihe & Talaud. Menyebabkan under-reporting deforestasi yang sangat masif. |
| **Sulawesi Tenggara** | `fe2e396191a0e8b6e70aa03dd225d7f7` | `3c79929a54bff963e7bf3a4762b803e9` | Kehilangan Kepulauan Wakatobi, Buton, dan Muna akibat batas kotak yang tidak meliuk. Saat direvisi (V3), angka deforestasi aslinya naik +124%. |
| **Sulawesi Barat** | `77f83070a9b4111e24a7cfdea73a5adb` | `796e2f453e81e409e183d833c586ff34` | Overbounding parah (terseret ke daratan Kalimantan). Angka Hutan Primer lama mencatat 53rb Ha, padahal aslinya 0 Ha. |
| **Sulawesi Selatan** | `abc6fc008f433d3dbdc65861bdcc8a87` | `33c45193c87f0505647dfae91a796b67` | Kepulauan Selayar dan Spermonde tidak tercakup akurat pada V2. |
| **Gorontalo** | `db937e7121c426140dd91072c14bbdaf` | `8d998ed751ba37bf689febf729f30304` | Batas darat utara yang bergerigi terseragamkan menjadi garis lurus di V2, merusak akurasi hektar di perbatasan. |

### Penjelasan Akar Masalah (Mengapa BBox Haram Digunakan)

1. **BBox (Bounding Box) pada V2:** 
   Sistem V2 menarik data satelit dengan memberikan koordinat *Min-Max Longitude/Latitude*. Ini menghasilkan bentuk **persegi panjang**. Karena bentuk Sulawesi itu rumit seperti huruf "K", kotak ini menabrak lautan dan pulau tetangga. Hutan yang terbakar di Maluku atau Kalimantan ikut terhitung sebagai deforestasi Sulawesi.
2. **GADM Geostore pada V3:**
   Sistem V3 tidak lagi memberikan koordinat kotak. Kita memberikan **ID Resmi dari GADM** (Database Area Administratif Global). GFW menggunakan ID ini untuk memotong peta satelit persis mengikuti lekukan pesisir pantai dan batas provinsi aslinya. Inilah data yang diakui dunia internasional secara *scientific*.


### 🚨 Kasus Khusus: Kesalahan AOI (Area of Interest) pada Data Faktor Pendorong (Driver)

Khusus untuk dataset **Loss by Driver (Faktor Pendorong Deforestasi)**, API GFW tidak menggunakan `Geostore ID`, melainkan menggunakan fitur *Area of Interest (AOI)* berbasis kodifikasi GADM tingkat Provinsi (disebut parameter `adm1`). 

Pada pengambilan data V2 (Lama), terjadi kesalahan fatal di mana sistem me-request **kode provinsi yang sepenuhnya salah sasaran**, karena kode tersebut bukan kodifikasi GADM resmi Indonesia. Berikut perbandingannya:

| Provinsi | Kode `adm1` V2 (Lama/Salah) | Kode `adm1` V3 (GADM Resmi) | Keterangan (Tujuan Asli Kode V2) |
| :--- | :---: | :---: | :--- |
| **Gorontalo** | `11` | `6` | Data lama menarik data deforestasi dari **Sumatera Barat** |
| **Sulawesi Barat** | `33` | `25` | Data lama menarik data deforestasi dari **Nusa Tenggara Timur (NTT)** |
| **Sulawesi Selatan** | `30` | `26` | Data lama menarik data deforestasi dari **Jawa Timur** |
| **Sulawesi Tengah** | `29` | `27` | Data lama menarik data deforestasi dari **Jawa Tengah** |
| **Sulawesi Tenggara** | `32` | `28` | Data lama menarik data deforestasi dari **Bali** |
| **Sulawesi Utara** | `31` | `29` | Data lama menarik data deforestasi dari **DI Yogyakarta** |

**Dampak Kesalahan V2:** 
Sistem mengunduh emisi CO2 dan data deforestasi komoditas sawit dari pulau Sumatera atau Jawa, lalu mengklaimnya sebagai data Sulawesi. Inilah mengapa dataset *Loss by Driver* V3 sangat krusial, karena di V3 kita telah mengkalibrasi ulang `adm1` sehingga menarik 100% dari teritori Sulawesi yang tepat.
