# Panduan Standardisasi Komprehensif Matriks D3TLH (ECC Dashboard)

Dokumen ini adalah **Blueprint Wajib** yang merangkum *seluruh* proses *fine-tuning* yang telah kita lakukan saat membangun "Matriks Daya Tampung Udara". Panduan ini harus direplikasi secara presisi saat menyusun Matriks Daya Tampung Air, Daya Dukung Lahan (Kebencanaan), dan Sosial/Kedaulatan Ruang.

## 1. Tata Letak (Layout) & Navigasi
*   **Sistem Split Kolom 1:2**: Layar dibagi menjadi 2. Kolom kiri khusus untuk Kartu "Mitos vs Fakta" dan *Vonis Akumulasi Skor*. Kolom kanan khusus untuk analisis mendalam.
*   **Wajib Menggunakan Tab (`st.tabs`)**: Jangan menumpuk grafik secara vertikal memanjang ke bawah. Semua sajian data harus dikemas ke dalam 4 (atau lebih) Tab interaktif agar rapi dan fokus.

## 2. MAKSIMALKAN GRAFIK, FAKTA, DAN DATA DARI SEMUA PAGE & DATASET
Ini adalah prinsip paling krusial dalam menyusun matriks:
*   **Gunakan Semua yang Kita Punya**: Jangan pernah membiarkan data menganggur. Eksploitasi *semua* dataset yang telah kita kumpulkan (Kesehatan, IKA, IKU, Deforestasi, Limbah B3, Titik Izin IUP/Smelter, dll).
*   **Daur Ulang (Re-Use) Grafik dari Page Lain**: Jika di halaman 1, 2, 3, 4, atau 5 sudah pernah dibuat sebuah grafik/peta yang relevan, **tarik dan gunakan kembali (re-use)** grafik tersebut ke dalam Tab Matriks. Jangan membuang waktu membuat grafik baru dari nol jika asetnya sudah ada.
*   **Visualisasikan Semua Fakta**: Jika suatu dataset tidak cocok dijadikan grafik linier/bar, maka wajib diubah menjadi **Fakta Data Teks/Angka Metrik**. Tidak boleh ada data yang luput dari paparan argumen.

## 3. Komponen di Dalam Setiap Tab
Setiap Tab harus memiliki struktur urut dari atas ke bawah sebagai berikut:
1.  **Statement/Narasi Tipis di Atas Grafik**: Selalu letakkan kalimat pengantar/narasi anomali (menggunakan HTML *micro-copy* tipis warna abu-abu) sebelum menampilkan grafik. Jangan gunakan `st.error` / *alert box* yang memakan ruang.
2.  **3 Kolom Metrik (Angka Cepat)**: Gunakan `st.columns(3)` untuk memaparkan: (1) Data Fakta Absolut, (2) Data Pembanding/Dampak, (3) Skor Metrik Numerik (0-10) dengan status kritis di bawahnya.
3.  **Grafik Interaktif (Plotly)**: Visualisasi utama yang telah diberi injeksi anomali (lihat poin 4).

## 4. Injeksi Kritis pada Grafik (Anotasi & Threshold)
Grafik standar tidak cukup. Setiap grafik *wajib* disuntik dengan elemen analitik investigatif:
*   **Garis Threshold (Batas Kritis)**: Tambahkan garis batas horizontal (`add_hline`) atau vertikal (`add_vline`) yang mencolok (misalnya garis putus-putus merah). Contoh: Garis "Kapasitas Toleransi Ambruk" di angka 5 Juta Ton, atau garis "Eskalasi Pabrik Nikel" di tahun 2015.
*   **Notasi/Anotasi Kritis**: Berikan teks notasi (`add_annotation`) langsung menempel di dalam grafik untuk menunjuk anomali tertentu. Buat visualnya agar publik awam langsung paham di mana letak kejanggalan/bahayanya tanpa harus berpikir keras.

## 5. Sistem Skoring & Model Matematis (Skala 0-10)
*   **Vonis Angka, Bukan Teks Panjang**: Ubah peringatan bahaya menjadi Skor Skala 0-10. Tampilkan metrik ini sejajar dengan angka data aslinya.
*   **Model Matematis Dinamis**: Jangan *hardcode* nilai agar mentok di 10.0. Gunakan normalisasi (*Dynamic Thresholding*, rasio IRR, *Carrying Capacity Index*) dengan batas atas (denominator) yang wajar sehingga skor bisa tampil dinamis (misal: 8.1, 9.4).
*   **Akumulasi Skor Kerusakan (Kartu Kiri)**: Satukan semua skor dari tiap Tab menggunakan rata-rata (*Simple Additive Weighting*). Tampilkan angka akumulasi (misal `9.8 / 10`) secara mencolok, *bold*, tebal di dalam kartu Mitos vs Fakta, **tanpa** menggunakan icon emoji (🚨) agar terkesan serius dan forensik.
