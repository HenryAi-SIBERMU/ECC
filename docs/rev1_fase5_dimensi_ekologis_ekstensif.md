# Strategi Eksekusi: Fase 5 - Dimensi Ekologis Ekstensif (Bencana & Biodiversitas)

Dokumen ini memetakan langkah kerja (SOP) untuk memperluas metrik kerusakan lingkungan di luar polusi udara dan limbah beracun, dengan membedah **Tren Bencana Alam (Hidrometeorologi)** dan **Hilangnya Biodiversitas** di kawasan lingkar tambang se-Sulawesi.

## 🎯 Objektif Utama
Membuktikan secara empiris bahwa perluasan konsesi tambang dan *smelter* nikel tidak hanya merusak secara kimiawi (polusi udara/air), tetapi juga meruntuhkan daya dukung fisik ekosistem yang berujung pada bencana alam dan kepunahan spesies lokal.

---

## 1️⃣ Bagian A: Tren Bencana Alam (Banjir & Longsor)
Kerusakan Daerah Aliran Sungai (DAS) akibat deforestasi pembukaan tambang berimplikasi langsung terhadap hilangnya area resapan air.

### 📌 Target Data
| Variabel Data | Spesifikasi / Metrik | Sumber Utama | Sumber Alternatif (*Fallback*) |
| :--- | :--- | :--- | :--- |
| **Tren Frekuensi Kejadian** | Jumlah insiden Banjir, Banjir Bandang, Tanah Longsor di 6 Provinsi (2014-2024). | BNPB - DIBI (Data Informasi Bencana Indonesia) | BPBD Provinsi/Kabupaten, Publikasi BPS *"Provinsi X Dalam Angka"* (Seksi Bencana Alam) |
| **Dampak Kerugian Absolut** | Jumlah korban mengungsi, rumah/fasilitas hancur akibat banjir/longsor. | BNPB - DIBI (Kolom Kerugian Sosial) | *Scraping* Portal Berita (Mongabay, Antara), Laporan Observasi JATAM/Walhi |

### 🛠️ Strategi Akuisisi (Scraping)
1.  **Direct API / Portal DIBI:** Memanfaatkan REST API publik BNPB atau mengunduh langsung agregasi tabular data historis bencana level kabupaten dari portal BNPB.
2.  **Pemrosesan Crosstab (Tambang vs Non-Tambang):**
    *   Sama seperti metodologi Zoonosis, kita akan membelah dataset kabupaten menjadi 2: **Kawasan Lingkar Tambang** vs **Kawasan Kontrol (Agraris/Jasa)**.
    *   Mengukur delta lompatan jumlah insiden banjir/longsor dan jumlah kerugian absolut (warga mengungsi, fasilitas rusak) di wilayah tambang.

---

## 2️⃣ Bagian B: Penurunan Biodiversitas di Zona Deforestasi Tambang
Pembongkaran tutupan hutan primer di wilayah karst Sulawesi memicu fragmentasi habitat spesies endemik.

### 📌 Target Data
| Variabel Data | Spesifikasi / Metrik | Sumber Utama | Sumber Alternatif (*Fallback*) |
| :--- | :--- | :--- | :--- |
| **Penyusutan Ekosistem Primer** | Luas deforestasi di habitat kritis dan kawasan karst. | Laporan KLHK, BPS (Statistik Lingkungan Hidup) | Global Forest Watch (GFW), Nusantara Atlas, Peta Indikatif Penundaan Izin Baru (PIPIB) |
| **Keterancaman Spesies Endemik** | Penyusutan populasi Anoa, Babirusa, Tarsius, Macaca di lingkar tambang. | Publikasi NGO (Walhi, JATAM, Auriga Nusantara, FWI) | Laporan Kajian Ekologis Akademik, Jurnal Ilmiah (Google Scholar, ResearchGate) |
| **Status Konservasi** | Daftar spesies terancam (*endangered*) akibat tumpang tindih IUP. | IUCN Red List of Threatened Species | CITES, Daftar Satwa Dilindungi KLHK |

### 🌍 Daftar Portal & API Sumber Data Ekologis (Spatial & Raster)
Berikut adalah daftar dataset yang divalidasi dapat digunakan untuk memetakan habitat spesies (koordinat/spatial) dan titik deforestasi secara presisi guna dikorelasikan dengan wilayah konsesi IUP Tambang di Dashboard:

| # | Portal | URL | Tipe | Metode Akses | Target Data | Keterangan |
|:---:|---|---|:---:|:---:|---|---|
| 1 | **GBIF (Global Biodiversity Information Facility)** | `https://www.gbif.org` | Internasional | API / Download | **Koordinat habitat satwa endemik** (titik *occurrence* untuk Anoa, Macaca, Babirusa, Tarsius di Sulawesi). | Dataset wajib untuk memplot sebaran habitat spesies ke peta Dashboard agar bisa ditimpa (*overlay*) dengan poligon IUP. Format: GeoJSON/CSV (Lat, Long). |
| 2 | **Nusantara Atlas** | `https://map.nusantara-atlas.org` | NGO | Web Map / Trase.earth | **Laju deforestasi & *alerts*** di kawasan Sulawesi, degradasi lahan gambut. | Dikelola The TreeMap. Data spasial deforestasi bisa ditarik melalui Trase.earth atau web API. Menyediakan satelit *before-after*. |
| 3 | **MapBiomas Indonesia** | `https://plataforma.mapbiomas.org` | NGO | GEE API / Download | **Transisi tutupan lahan** (hutan primer vs area terbuka) seri waktu historis (1990-sekarang). | Menyediakan akses Google Earth Engine (GEE) dan unduhan Raster GeoTIFF. Cocok untuk visualisasi hilangnya luas hutan per kabupaten. |
| 4 | **Global Forest Watch (GFW)** | `data.globalforestwatch.org` | Internasional | REST API / Python SDK | **Hilangnya tutupan pohon (Tree cover loss)** resolusi 30m. | Memiliki API v1 dan v2. Bisa diintegrasikan langsung dengan Streamlit menggunakan SDK `gfwpy` atau REST call sederhana. |
| 5 | **KBA (Key Biodiversity Areas)** | `keybiodiversityareas.org` | Internasional | GIS Download | **Poligon kawasan habitat penting dunia.** | Memberikan file Shapefile kawasan yang tidak boleh diganggu (No-Go zones) untuk di-overlay dengan poligon tambang nikel Sulawesi. |

### 🛠️ Strategi Data Mining
1.  **Geospatial Overlap (Opsional):** Jika data spasial tersedia, menumpuk peta konsesi Izin Usaha Pertambangan (IUP) dengan peta sebaran *Key Biodiversity Areas* (KBA) di Sulawesi.
2.  **Literature Mining:** Mengekstrak *hard numbers* (angka mutlak kepunahan/penurunan spesies atau hutan lindung yang dialihfungsikan) dari publikasi-publikasi laporan resmi KLHK/NGO 3 tahun terakhir menggunakan Python *PDF Parsers* atau secara manual.

---

## 🚀 Rencana Eksekusi Sistem di Dashboard
Nantinya, kedua analisis ini akan bermuara pada **Pembaruan Page 4 (Degradasi Lingkungan)** atau pembuatan halaman baru.

1.  **Visualisasi Bencana:** Grafik tren historis (*Line Chart*) 10 tahun terakhir (2014-2024) yang mengkomparasi frekuensi banjir/longsor di kab. tambang vs non-tambang.
2.  **Narasi Jurnalistik Biodiversitas:** Pembuatan *Hero Statement* dan metrik Bento Card yang menunjukkan luas habitat satwa yang tergusur, disajikan dalam konteks ancaman kepunahan lokal demi nikel.

**Langkah Pertama yang Harus Diambil Agen Selanjutnya:**
Mulai merancang skrip *scraper* (atau pengunduh dataset manual) ke portal DIBI BNPB untuk menarik *raw data* bencana alam 10 tahun terakhir di Sulawesi.
