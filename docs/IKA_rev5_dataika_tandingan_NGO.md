# Alternatif Data Indeks Kualitas Air (IKA) - Sumber Non-Pemerintah (NGO & Akademis)

## Konteks Masalah
Berdasarkan investigasi terhadap data resmi BPS (SIMDASI), ditemukan fakta bahwa **BPS Sulawesi Tengah berhenti mempublikasikan data "Akses Air Minum Layak" tingkat kabupaten sejak tahun 2019**. Ketiadaan data (Black Hole) ini tepat terjadi sebelum periode ekspansi masif smelter nikel di Morowali dan Morowali Utara. 

Karena absennya data runtun waktu (*time-series*) resmi dari pemerintah, kita tidak dapat melakukan uji statistik kausalitas (regresi) yang valid. Oleh karena itu, kita menggunakan **Ground Truth Data** dari laporan investigasi NGO dan penelitian akademis sebagai data tandingan (Counter-Data) pembuktian pencemaran air.

## Tabel Sumber Data Tandingan IKA (Pencemaran Air)

Semua *raw file* PDF dari sumber di bawah ini telah berhasil diunduh dan diarsipkan secara lokal di dalam repositori:
`data/raw/ika_ngo/` beserta *metadata* masternya di `metadata_ika_ngo.json`.

| No | Judul Dokumen / Laporan | Penerbit (NGO/Institusi) | Tahun Terbit | Parameter Pencemaran Terukur | Lokasi Spesifik | Deskripsi & Temuan Utama | File Lokal |
|:---|:---|:---|:---|:---|:---|:---|:---|
| **1** | **Tailing yang Difilter di Indonesia** | Earthworks | 2026 | Kromium Heksavalen (Cr6+) | Sungai Bahodopi (Kawasan IMIP) | Mendokumentasikan insiden jebolnya fasilitas *tailing* PT Huayue Nickel Cobalt (PT HYNC) pada Maret 2025. Hasil lab menunjukkan kadar Cr6+ yang bocor langsung ke aliran Sungai Bahodopi. | `Earthworks_Tailing_Filtered_IMIP_2026.pdf` |
| **2** | **Kebijakan, Risiko, dan Pencegahan Dampak Pertambangan Nikel pada Laut di Indonesia** | AEER (Aksi Ekologi & Emansipasi Rakyat) | 2025 | Kromium Heksavalen (Cr6+) | Pesisir & Perairan Kawasan IMIP | Laporan pemantauan kualitas lingkungan di perairan sekitar kawasan industri Morowali. Membuktikan adanya jejak Cr6+ yang merupakan logam berat karsinogenik. | `AEER_Risiko_Laut_IMIP_Cr6.pdf` |
| **3** | **Policy Paper: Sulawesi Lumbung Polusi** | WALHI Sulawesi Selatan | 2024 | TSS (Total Suspended Solids) & Cr6+ | Sungai & Laut Morowali | Membedah mekanisme polusi: limpasan air hujan dari *stockpile* bijih nikel dan pembuangan air limbah langsung ke laut tanpa *treatment* menyebabkan nilai TSS melampaui baku mutu parah (laut merah bata). | `WALHI_Sulsel_Lumbung_Polusi.pdf` |
| **4** | **Analisis Kualitas Air Limpasan Tambang Nikel di Morowali** | Universitas Gadjah Mada (UGM) | 2023 | Indeks Pencemaran Air (Multivariabel) | Desa Matarape, Kab. Morowali | Penelitian tesis akademis yang melakukan pengujian lab langsung pada air limpasan (*runoff*) di lingkar tambang laterit. Menyimpulkan status air permukaan adalah **"Tercemar Berat"**. | `Tesis_UGM_Matarape_Morowali.pdf` |

## Limitasi & Rekomendasi Eksekusi
- **Limitasi:** Data ini berbentuk laporan cetak (PDF), bukan API atau dataset terstruktur (CSV). NGO mengumpulkan data melalui metode sampling fisik manual, sehingga tidak menghasilkan data runtun waktu yang masif.
- **Rekomendasi Visualisasi Dashboard:** 
  1. Buat infografis di Streamlit yang memaparkan narasi "Black Hole Data BPS" vs "Realita Bukti Lab NGO".
  2. Ekstrak (*parsing*) angka ukur Cr6+ dan TSS dari dalam teks PDF di atas, lalu konversikan menjadi tabel bar-chart statis di dalam *dashboard* sebagai peringatan bahaya klinis.
  3. Hubungkan tingginya kadar Cr6+ dengan lonjakan kasus Diare dan ISPA dari data Kemenkes, menggunakan logika toksikologi medis sederhana (pencemaran sumber air minum masyarakat lokal).

## Syarat Eksekusi Regresi yang Valid Secara Statistik

Mengingat regresi OLS di tingkat provinsi (n=6) **terbukti gagal dan tidak signifikan**, maka jika ke depannya riset ini ingin membuktikan kausalitas secara empiris (angka), ketiga syarat mutlak berikut harus dipenuhi:

1. **Turun ke Level Kabupaten/Kecamatan (Penambahan N):** 
   Secara matematis, menguji kausalitas statistik hanya dengan observasi provinsi (N=6) terlalu lemah (underpowered). Data Diare dan Kualitas Air wajib ditarik di level Kabupaten (N=81) atau Kecamatan agar variasi datanya cukup besar untuk dideteksi oleh OLS tanpa bias oleh anomali agregat provinsi berpenduduk besar.
2. **Gunakan Regresi Multivariat (Tambah Variabel Kontrol):**
   Penyakit Diare dipengaruhi oleh banyak faktor. Melakukan regresi bivariat (`Diare ~ IKA`) rentan mengalami bias (*Omitted Variable Bias*). Model regresi wajib memasukkan variabel kontrol esensial: `Diare ~ IKA + Curah Hujan + Akses Sanitasi/Toilet + Kepadatan Penduduk + Fasilitas Kesehatan`. 
3. **Ganti Variabel Independen (X) - Jangan Pakai IKA KLHK:**
   Indeks Kualitas Air (IKA) dari KLHK merupakan indeks agregat (*gado-gado*) dari seluruh sungai di sebuah provinsi, padahal yang tercemar nikel hanyalah area sungai pesisir spesifik. Sebaiknya ganti proksi variabel independen (X) menggunakan **Data Satelit TSS (Kekeruhan Air)** khusus di muara sungai pesisir tambang, atau langsung menggunakan data **Kapasitas Smelter (MW)** per kabupaten.

## Alternatif Pengukuran Spasial (Web API / Remote Sensing)

Selain data fisik (uji lab) dari NGO, **kekeruhan air (*Total Suspended Solids* / TSS)** yang diakibatkan oleh limpasan sedimen tambang nikel sebenarnya dapat diukur secara terstruktur dari luar angkasa. 

Berikut adalah *dataset* / API web yang dapat digunakan sebagai proksi pengukuran kualitas air secara spasial:

| No | Platform / Sumber | Deskripsi Dataset | Tipe Data & Akses | Keterbatasan (Limitasi) |
|:---|:---|:---|:---|:---|
| **1** | **Google Earth Engine (GEE)** | Koleksi citra **Sentinel-2 MSI**. Algoritma rasio *band* optik (Merah & Inframerah Dekat) terbukti akurat untuk mengkalkulasi TSS (kekeruhan) perairan. Ini ekuivalen dengan *Global Forest Watch*, namun untuk air. | *Remote Sensing API* (Python/JS) | Bukan *dataset* instan. Membutuhkan algoritma pengolahan spasial untuk mengubah piksel citra menjadi angka TSS numerik. |
| **2** | **Copernicus Global Land Service** | Dataset **Lake Water Quality** yang melacak tingkat kekeruhan (*turbidity*) secara periodik. | API (NetCDF / TIFF) | Resolusi terbatas; umumnya hanya menargetkan danau besar, kurang mendetail untuk hilir sungai sempit di lingkar tambang. |
| **3** | **KLHK (Sistem ONLIMO)** | *Online Monitoring Kualitas Air* secara *real-time* dari stasiun *telemetry* sungai milik pemerintah. | *Dashboard Web* | Akses API mentah (JSON/CSV) **ditutup untuk publik**. Hanya visualisasi *dashboard* atau agregat provinsi (IKA tahunan) yang dirilis. |
| **4** | **UNEP GEMS / Water** | *Global Environment Monitoring System for Water* dari PBB. Berisi *database* pengujian air permukaan global. | Portal Web Terbuka | Stasiun pemantauan di wilayah timur Indonesia (terutama Morowali) sangat minim atau tidak di-*update* secara *real-time*. |

> **Catatan Teknis:** Untuk parameter racun kimiawi berat seperti Kromium (Cr6+) mutlak membutuhkan *sample* fisik (PDF NGO). Namun untuk parameter **Kekeruhan (TSS)**, API **Google Earth Engine** adalah satu-satunya instrumen data terstruktur paling mutakhir yang bisa menandingi ketiadaan data statistik BPS.
