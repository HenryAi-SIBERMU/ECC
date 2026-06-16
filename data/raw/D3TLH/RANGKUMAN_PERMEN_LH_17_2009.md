# RANGKUMAN REGULASI & PEDOMAN D3TLH PEMERINTAH
*(Sumber: Permen LH No. 17 Tahun 2009 & Buku Pedoman D3TLH KLHK)*

Dokumen ini adalah ekstraksi manual dari kerangka hukum dan panduan teknis pemerintah terkait penentuan Daya Dukung dan Daya Tampung Lingkungan Hidup (D3TLH), karena situs resmi JDIH KLHK dan repositori pemerintah kerap mengalami *timeout* saat diunduh secara *headless*.

---

## 1. Landasan Hukum Utama
Regulasi primer yang mengatur D3TLH di Indonesia adalah **Peraturan Menteri Negara Lingkungan Hidup Nomor 17 Tahun 2009** tentang Pedoman Penentuan Daya Dukung Lingkungan Hidup dalam Penataan Ruang Wilayah. Aturan ini kemudian disempurnakan dengan PP 22/2021 dan Buku Pedoman Jasa Ekosistem KLHK.

## 2. Definisi Resmi Pemerintah
Dalam regulasi tersebut, Daya Dukung Lingkungan Hidup didefinisikan sebagai:
> *"Kemampuan lingkungan hidup untuk mendukung perikehidupan manusia dan makhluk hidup lain."*

Sedangkan Daya Tampung Lingkungan Hidup adalah:
> *"Kemampuan lingkungan hidup untuk menyerap zat, energi, dan/atau komponen lain yang masuk atau dimasukkan ke dalamnya."*

## 3. Metodologi Perhitungan (The "Blind Spot")
Berdasarkan pedoman resmi KLHK, tata cara penentuan D3TLH pada tingkat provinsi/kabupaten menggunakan basis **Jasa Ekosistem (*Ecosystem Services*)**. 

Pemerintah melakukan perhitungan dengan rumus spasial (GIS) berbasis:
1.  **Peta Ekoregion:** Peta karakteristik lanskap, batuan, dan tanah.
2.  **Peta Tutupan Lahan (*Land Cover*):** Peta yang menunjukkan apakah suatu area adalah hutan primer, sekunder, kebun, pemukiman, atau lahan terbuka.

Kedua peta di atas di-*overlay* (ditumpuk) untuk menghasilkan **Indeks Jasa Ekosistem** yang berskala 1 (Sangat Rendah) hingga 5 (Sangat Tinggi).

### Kategori Jasa Ekosistem yang Dihitung:
*   **Provisioning (Penyediaan):** Pangan, air bersih, bahan bakar, materi genetik.
*   **Regulating (Pengaturan):** Tata air, mitigasi iklim, mitigasi banjir, pemurnian udara.
*   **Supporting (Pendukung):** Siklus hara, pembentukan tanah.
*   **Cultural (Budaya):** Estetika alam, rekreasi.

## 4. Analisis Kritis: Mengapa Regulasi Ini Menyesatkan?
Berdasarkan rumusan resmi di atas, terlihat jelas mengapa D3TLH pemerintah gagal mendeteksi krisis di lapangan:

1.  **Hanya Berbasis Spasial Benda Mati:** Rumus pemerintah berasumsi bahwa "selama peta satelit masih hijau (ada tutupan lahan), maka kapasitas pemurnian udara masih bagus". Padahal, di bawah warna hijau peta tersebut, warga sedang terpapar debu tebal smelter.
2.  **Ketiadaan Metrik Sosiologi:** Tidak ada satu pun pasal dalam Permen LH 17/2009 yang mewajibkan perhitungan jumlah letupan konflik agraria akibat alih fungsi lahan.
3.  **Ketiadaan Metrik Epidemiologi:** Pedoman KLHK tidak mewajibkan integrasi data rekam medis Puskesmas (ISPA, penyakit kulit) ke dalam penentuan batas daya dukung.
4.  **Bukan Rem Darurat (Veto):** Dokumen D3TLH pemerintah sebagian besar berakhir menjadi "Peta Arahan" dalam Rencana Tata Ruang Wilayah (RTRW), namun hampir tidak pernah memiliki kekuatan absolut (VETO) untuk mencabut IUP (Izin Usaha Pertambangan) meskipun wilayah tersebut secara ekologis sudah berstatus "Kritis".

---
*Dokumen ini diletakkan di `data/raw/D3TLH` sebagai landasan teoritis bagi pipeline data di Fase 1 (Audit D3TLH).*
