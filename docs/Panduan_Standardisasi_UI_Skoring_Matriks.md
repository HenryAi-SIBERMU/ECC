# Panduan Standardisasi UI & Skoring Matriks D3TLH (ECC Dashboard)

Dokumen ini berisi *log* penyelarasan (*fine-tuning*) dan panduan *blueprint* pengembangan yang telah disepakati dari pengerjaan "Matriks Daya Tampung Udara". Panduan ini **Wajib** digunakan sebagai standar (*template*) untuk membangun matriks-matriks selanjutnya (Daya Tampung Air, Lahan/Kebencanaan, Kedaulatan Ruang, dll).

## 1. Arsitektur Layout Utama (Split 1:2)
Setiap halaman/bagian matriks harus dipisah menggunakan sistem rasio kolom 1:2.
*   **Kolom Kiri (colA1 - Lebar 1x)**: Khusus untuk "Kartu Vonis Eksekutif" atau "Mitos vs Fakta". Menggunakan latar gelap (`#2C3E50`), garis tepi merah (`#E74C3C`), dan secara eksklusif memuat **Akumulasi Skor Kerusakan** (angka tunggal raksasa).
*   **Kolom Kanan (colA2 - Lebar 2x)**: Khusus untuk penjabaran analitik mendalam menggunakan komponen navigasi **4 Tab Interaktif** (`st.tabs`).

## 2. Sistem Skoring Universal (Skala 0-10) & Model Matematis
Setiap data empiris, sebesar apapun satuannya (Juta Ton, Ribuan Megawatt), **wajib** dikonversi dan dinormalisasi menjadi Indeks Skala 0 hingga 10 menggunakan model statistik (misal: *Min-Max Normalization, Carrying Capacity Index, IRR/Relative Risk*).
*   **Dynamic Thresholding (Normalisasi Batas Atas)**: Jangan menggunakan batas mentok (*ceiling*) yang terlalu kecil. Jika data empiris sangat ekstrem (misal 25x lipat dari ambang batas), gunakan pembagi (denominator) yang logis (misal dibagi 30) agar skor tidak selalu *hardcode* mentok di 10.0. Tujuannya agar metrik menampilkan angka dinamis (misal: 8.1, 9.4).

## 3. Komponen Tab: Sistem 3 Metrik
Setiap Tab **tidak boleh** hanya menyajikan grafik kosong. Di atas grafik, harus selalu didahului oleh penjabaran angka cepat (`st.columns(3)`):
*   **Metrik 1 (Kiri)**: Data Absolut Penyebab (Misal: Total Timbulan B3, Kapasitas MW).
*   **Metrik 2 (Tengah)**: Data Komparator / Dampak Langsung (Misal: Jumlah Kasus ISPA, Total Hutan Hilang).
*   **Metrik 3 (Kanan)**: **Skor Matematis (0-10)** dengan label peringatan keras di bawahnya (`delta_color="inverse"`), misal: "STATUS: DARURAT MEDIS".

## 4. Penggunaan "Narasi Anomali" Tipis (Micro-Copy)
Hindari penggunaan *banner alert* yang tebal dan memakan ruang (seperti `st.error` atau `st.warning`) untuk teks yang panjang.
*   Gunakan HTML *micro-copy* tipis berwarna abu-abu terang sebagai narasi pembuka/pembuat *framing* saintifik di atas grafik.
*   *Template Code*: `<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Narasi Anomali:</b> [Teks penjelasan kegagalan/kebohongan data dokumen D3TLH]</div>`

## 5. Aggregasi "Vonis" / Akumulasi Skor Kerusakan
Metrik terpenting dari seluruh halaman.
*   **Metode**: Rata-rata dari keempat Tab (atau *Simple Additive Weighting* berbobot sama 25%).
*   **Lokasi**: Ditempatkan di dalam Kolom Kiri (Kartu Mitos vs Fakta).
*   **Visual**: Teks berukuran 32px, dicetak sangat tebal (Font weight: 800), merah (`#E74C3C`), di dalam kotak pembatas *dark mode* murni (`#1A202C`). **Dilarang** menggunakan icon emoji (seperti 🚨) untuk menjaga kesan dasbor forensik intelijen yang kaku, ilmiah, dan presisi.

---
**Catatan Implementasi:**
Setiap kali membuka/membangun Matriks baru (Air, Lahan, Sosial), programmer/AI **wajib** membaca panduan ini dan melakukan replikasi logika UI/UX serta *data flow* matematika yang serupa.
