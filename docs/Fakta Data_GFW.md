# Fakta Data: Global Forest Watch (GFW) Versi 3

Dokumen ini memetakan seluruh kolom metrik dari dataset GFW versi 3, baik dari file **Processed** (hasil olahan/agregasi 2014-2023) maupun file **RAW** (mentah tarikan dari API 2001-2025), yang digunakan dalam *dashboard* Celios. Penjelasan dibagi menjadi dua sudut pandang: **Bahasa Teknis** (untuk akurasi akademik/metodologi) dan **Bahasa Bayi** (untuk audiens awam/media).

---

## 1. Dataset PROCESSED: Master Data 1 Dekade (2014-2023)
**Nama File:** `sulawesi_gfw_master_1_dekade_2014_2023_v3.csv`
**Deskripsi:** File agregasi matang. Berisi gabungan semua tipe deforestasi per provinsi per tahun.

| Nama Kolom di CSV | Penjelasan Teknis (Metodologi) | Penjelasan Bahasa Bayi (Awam) |
| :--- | :--- | :--- |
| `Total_Deforestasi_Ha` | Total area *Tree Cover Loss* (kanopi >5m, >30% kerapatan) tanpa memandang jenis tutupan lahannya. | **Total Pohon Tumbang:** Luas seluruh pohon yang ditebang atau mati, baik itu hutan asli, kebun sawit, maupun hutan karet. |
| `Deforestasi_Hutan_Primer_Ha` | *Tree Cover Loss* yang beririsan (intersect) dengan *Hansen Regional Primary Forest mask*. | **Kehilangan Hutan Perawan:** Luas hutan asli warisan alam (belum pernah ditebang) yang musnah. Ini metrik kerusakan terpenting! |
| `Deforestasi_Kawasan_Lindung_Ha` | *Tree Cover Loss* yang terjadi di dalam poligon batas *World Database on Protected Areas* (WDPA) IUCN. | **Pelanggaran Hutan Lindung:** Luas pohon yang ditebang secara ilegal di dalam area konservasi (taman nasional/cagar alam). |
| `Laju_Deforestasi_Ha` | Perubahan angka deforestasi secara rata-rata atau absolut dibandingkan tahun sebelumnya. | **Kecepatan Kerusakan:** Kecepatan seberapa cepat hutan ditebang dari waktu ke waktu (ibarat *speedometer* perusakan hutan). |
| `Baseline_Tutupan_Hutan_2000_Ha` | Area *Tree Cover Extent* (luas tutupan kanopi) pada tahun awal pengukuran satelit (tahun 2000). | **Modal Awal Hutan:** Luas total hutan yang dimiliki Sulawesi di masa lalu sebelum maraknya tambang. |
| `Total_Emisi_CO2_Megagram` | Gross *Carbon Dioxide* (CO2) *Emissions* yang dilepaskan ke atmosfer akibat hilangnya biomasa. | **Asap Karbon Lepas:** Jumlah gas rumah kaca (polusi) yang menguap ke udara karena pohon pembawa oksigen ditebang/dibakar. |
| `Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha` | Filter deforestasi khusus kategori *Commodity Driven*. | Area hutan yang digusur tambang/sawit raksasa. |
| `Deforestasi_Driver_Kehutanan_Ha` | Filter deforestasi khusus kategori *Forestry*. | Area panen industri kayu (HTI). |
| `Deforestasi_Driver_Pertanian_Berpindah_Ha` | Filter deforestasi khusus kategori *Shifting Agriculture*. | Area pembukaan lahan oleh petani warga. |
| `Deforestasi_Driver_Urbanisasi_Ha` | Filter deforestasi khusus kategori *Urbanization*. | Area yang dibeton/diaspal jadi perkotaan. |

---

## 2. Dataset PROCESSED: Faktor Pendorong & Spesifik (2014-2023)
Deretan file ini adalah pecahan dari Master Data, yang difilter spesifik untuk 1 dekade terakhir.

### 2.1. `sulawesi_gfw_loss_by_driver_2014_2023_v3.csv`
| Kolom | Penjelasan Teknis | Penjelasan Bahasa Bayi |
| :--- | :--- | :--- |
| `Faktor_Pendorong` | Hasil prediksi Machine Learning TSC (*Commodity driven, Shifting agriculture*, dll) atas penyebab deforestasi. | Kategori yang menjawab "Hutan ini ditebang buat apa?". |
| `Luas_Deforestasi_Ha` | Total *loss* berdasarkan faktor pendorongnya. | Luas area yang dihancurkan. |
| `Emisi_CO2_Megagram` | Estimasi gross emisi karbon dioksida. | Jumlah polusi gas buang (asap karbon). |
| `Hutan_Primer` | Apakah kejadian deforestasi ini terjadi di dalam poligon hutan primer (True/False). | Penanda apakah tebangan itu merusak hutan perawan. |

### 2.2. `sulawesi_gfw_hutan_primer_loss_2014_2023_v3.csv`
| Kolom | Penjelasan Teknis | Penjelasan Bahasa Bayi |
| :--- | :--- | :--- |
| `is__umd_regional_primary_forest_2001`| Bendera (True) penanda ekosistem hutan primer 2001. | Bukti kuat bahwa yang ditebang adalah hutan perawan. |
| `Luas_Hilang_Hutan_Primer_Ha` | *Tree Cover Loss* yang khusus terjadi di atas hutan primer. | Luas habitat asli yang dihancurkan. |

### 2.3. `sulawesi_gfw_kawasan_lindung_loss_2014_2023_v3.csv`
| Kolom | Penjelasan Teknis | Penjelasan Bahasa Bayi |
| :--- | :--- | :--- |
| `wdpa_protected_areas__iucn_cat` | Kategori kawasan konservasi berdasarkan IUCN. | Label status larangan suatu wilayah hutan. |
| `Luas_Hilang_Kawasan_Lindung_Ha` | *Tree Cover Loss* yang khusus terjadi di dalam kawasan lindung/konservasi. | Luas perambahan hutan terlarang (kriminalitas lingkungan). |

---

## 3. Dataset RAW: Tarikan Asli API (Rentang Penuh 2001-2025)
**Deskripsi:** Ini adalah 7 file mentah dari API GFW yang menjadi bahan baku (*raw material*) sebelum diproses menjadi data 1 dekade di atas.

### 3.1. `loss_by_driver_sulawesi_2001_2025_v3.csv` (RAW Faktor Pendorong)
*Lokasi: `data/raw/klhk_gfw/land_api_fetch/`*
| Nama Kolom API | Penjelasan Teknis | Penjelasan Bahasa Bayi |
| :--- | :--- | :--- |
| `driver` | Klasifikasi penyebab deforestasi dari algoritma TSC. | Penyebab utama (Tambang, Kebakaran, dll). |
| `area_ha` | Luas area yang terdampak faktor tersebut. | Hektar yang hancur. |
| `co2_emissions_mg` | Emisi gas karbon dioksida. | Polusi asap yang terlepas. |
| `is_primary` | Bendera boolean irisan hutan primer. | Apakah itu hutan perawan? (Ya/Tidak) |

*(Di bawah ini berlokasi di `data/raw/klhk_gfw/mega_fetch_v3/`)*

### 3.2. `tree_cover_loss_sulawesi_v3.csv` (Total Kehilangan Tajuk Pohon)
| Nama Kolom API | Penjelasan Teknis | Penjelasan Bahasa Bayi |
| :--- | :--- | :--- |
| `tree_cover_loss_ha` | Total area kanopi pohon yang hilang secara bruto. | Total hektar luas tebangan kasar. |

### 3.3. `loss_by_land_cover_sulawesi_v3.csv` (Kehilangan Berdasarkan Jenis Lahan)
| Nama Kolom API | Penjelasan Teknis | Penjelasan Bahasa Bayi |
| :--- | :--- | :--- |
| `esa_land_cover_2015__class` | Kategori lahan berdasarkan satelit ESA 2015. | Label tanahnya sebelum ditebang (Hutan, Semak, Kota). |
| `area__ha` | Luas area kehilangan di kategori tersebut. | Luas area yang ditebang. |

### 3.4. `primary_forest_loss_sulawesi_v3.csv` (Khusus Hutan Primer)
| Nama Kolom API | Penjelasan Teknis | Penjelasan Bahasa Bayi |
| :--- | :--- | :--- |
| `is__umd_regional_primary_forest_2001`| Bendera (True) penanda ekosistem hutan primer 2001. | Tanda bukti bahwa area yang ditebang itu hutan perawan. |
| `area__ha` | Luas hutan primer yang hilang. | Luas hutan perawan yang dihancurkan. |

### 3.5. `loss_in_protected_areas_sulawesi_v3.csv` (Khusus Kawasan Lindung)
| Nama Kolom API | Penjelasan Teknis | Penjelasan Bahasa Bayi |
| :--- | :--- | :--- |
| `wdpa_protected_areas__iucn_cat` | Status level konservasi wilayah (Standar IUCN). | Status larangan wilayah (Taman Nasional, Suaka, dll). |
| `area__ha` | Luas area konservasi yang hilang. | Luas area cagar alam yang digunduli. |

### 3.6. `tree_cover_by_category_sulawesi_v3.csv` (Sisa Persediaan Pohon Berdiri)
| Nama Kolom API | Penjelasan Teknis | Penjelasan Bahasa Bayi |
| :--- | :--- | :--- |
| `category_type` | Jenis pengelompokan API (*protected_area* / *plantation*). | Filter data (hutan lindung atau kebun manusia). |
| `gfw_plantations__type` | Klasifikasi jenis perkebunan. | Info kebunnya (Kelapa sawit atau Kayu industri). |
| `area__ha` | Luas area tutupan tajuk pohon yang masih berdiri (Tahun 2000). | Luas wilayah yang menghijau / belum ditebang. |

### 3.7. `tree_cover_gain_sulawesi_v3.csv` (Penghijauan Kembali)
| Nama Kolom API | Penjelasan Teknis | Penjelasan Bahasa Bayi |
| :--- | :--- | :--- |
| `is__umd_tree_cover_gain` | Flag (True) lahan dengan pertambahan tajuk pohon. | Area yang tumbuh kembali (Reboisasi). |
| `area__ha` | Luas area yang mengalami *gain*. | Luas area yang kembali rimbun. |
