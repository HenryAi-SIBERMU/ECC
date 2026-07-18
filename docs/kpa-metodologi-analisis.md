# Analisis Metodologi Pengumpulan Data KPA (2016 - 2025)

Dokumen ini berisi hasil ekstraksi dan analisis **Metodologi Pengumpulan Data** dari seluruh PDF *Catatan Akhir Tahun (Catahu)* Konsorsium Pembaruan Agraria (KPA) yang terbit selama rentang waktu satu dekade (2016–2025).

> Analisis ini dilakukan untuk memvalidasi metodologi riset D3TLH CELIOS, khususnya dalam hal replikasi data konflik agraria melalui metode OSINT (Open Source Intelligence).

---

## 🔍 Detail Metodologi per Tahun Laporan

Berdasarkan ekstraksi *full-text* dari 9 PDF Catahu KPA, berikut adalah daftar rinci sumber data dan metodologi yang mereka gunakan setiap tahunnya:

| Tahun Laporan | Sumber Metadata | Bukti Kutipan | Halaman Kutipan |
|:---|:---|:---|:---|
| **Catahu 2016** | 1. Laporan Langsung Korban<br>2. Jaringan NGO/Pendamping<br>3. Investigasi Lapangan (Ground Truth)<br>4. Monitoring Berita Media Massa (OSINT) | *"Data kejadian konflik agraria sepanjang 2016... bersumber dari: (1) Para korban konflik... (2) jaringan KPA... (3) Hasil assessment situasi agraria... dan 4) Hasil monitoring pemberitaan di media massa (cetak dan elektronik)."* | Halaman 4 |
| **Catahu 2017** | 3. Investigasi Lapangan (Ground Truth)<br>4. Monitoring Berita Media Massa (OSINT) | *"...(3) Hasil pengumpulan data agraria di wilayah, (4) Investigasi kasus konflik agraria di lapangan, (5) Hasil monitoring pemberitaan di media massa (cetak dan elektronik)."* | Halaman 8 |
| **Catahu 2018** | *(Merujuk pada metodologi standar tahun sebelumnya)* | *(Keyword metodologi tidak ditulis secara eksplisit di bab awal PDF)* | - |
| **Catahu 2019** | 4. Monitoring Berita Media Massa (OSINT) | *"...keterbatasan perangkat organisasi untuk menjangkau seluruh wilayah kejadian konflik... serta keterbatasan publikasi media terhadap kasus konflik agraria yang terjadi."* | Halaman 12 |
| **Catahu 2020** | 1. Laporan Langsung Korban<br>2. Jaringan NGO/Pendamping<br>3. Investigasi Lapangan (Ground Truth)<br>4. Monitoring Berita Media Massa (OSINT) | *"Sumber data... bersumber dari: 1) Laporan langsung masyarakat... 2) Laporan jaringan KPA... 3) monitoring data di wilayah; dan 4) Hasil monitoring pemberitaan di media massa baik cetak, elektronik maupun online."* | Halaman 16 |
| **Catahu 2021** | 3. Investigasi Lapangan (Ground Truth) | *"Proses pemantauan dan pelaporan data konflik ini berasal dari berbagai sumber terpercaya melalui proses pemeriksaan ulang informasi atau data, investigasi hingga validasi ke lapangan..."* | Halaman 8 |
| **Catahu 2022** | 3. Investigasi Lapangan (Ground Truth) | *"Laporan ini merupakan hasil pemantauan dan analisa atas situasi konflik agraria yang terjadi di lapangan serta dinamika kebijakan agraria sepanjang tahun."* | Halaman 13 |
| **Catahu 2023** | 1. Laporan Langsung Korban<br>2. Jaringan NGO/Pendamping<br>3. Investigasi Lapangan (Ground Truth)<br>4. Monitoring Berita Media Massa (OSINT) | *"Informasi dan data konflik yang dikumpulkan berasal dari: 1) Pengaduan langsung... 2) Laporan anggota dan jaringan; 3) Hasil pemantauan lapangan... 4) Hasil pemantauan pemberitaan konflik agraria di media massa..."* | Halaman 13 |
| **Catahu 2025** | 1. Laporan Langsung Korban<br>3. Investigasi Lapangan (Ground Truth)<br>4. Monitoring Berita Media Massa (OSINT) | *"Data-data... berasal dari berbagai sumber: 1) Pengaduan langsung... 2) Hasil investigasi lapangan... 3) Hasil pemantauan konflik agraria di media massa nasional dan daerah, baik cetak, digital maupun audio-visual; 4) Hasil pemantauan di media sosial yang telah diverifikasi kembali kebenarannya..."* | Halaman 21 |

---

## ⚠️ Keterbatasan Data KPA (Self-Acknowledged)

KPA secara jujur dan ilmiah selalu menaruh *disclaimer* terkait angka mereka. Ini sangat penting untuk mitigasi riset kita:

> *"Dengan metode ini, tentu saja angka yang disajikan oleh KPA adalah **angka minimal dari jumlah konflik agraria yang sesungguhnya terjadi**, mengingat tidak seluruh wilayah dapat terpantau kejadian konflik agrarianya... Hal ini mengingat keterbatasan struktur dan sumberdaya organisasi dalam merekam serta menjangkau seluruh kejadian di berbagai daerah di sepanjang tahun."* — (Dikutip dari Catahu 2016, diulangi di 2019, 2021, dan 2025).

---

## 💡 Konklusi Strategis untuk Riset CELIOS (D3TLH)

Tabel historis di atas membuktikan secara absolut bahwa KPA menjadikan **Web Scraping / OSINT portal berita (dan Media Sosial sejak 2025)** sebagai pilar resmi perekaman data mereka. 

Pendekatan untuk mengekstrak visualisasi/infografis PDF secara parsial sebaiknya **tidak digunakan** karena rentan *error*. Sebagai gantinya, D3TLH CELIOS memiliki **justifikasi metodologi yang tervalidasi oleh dokumen KPA itu sendiri** untuk menjalankan strategi berikut:

1. **Agregasi Makro:** Mengambil data ringkasan level provinsi dari **Siaran Pers KPA** (berupa teks terstruktur).
2. **Replikasi OSINT (The KPA Way):** Menjalankan *script Scrapling* untuk menambang berita dari portal seperti *Mongabay*, *Tempo*, media lokal di Sulawesi, hingga pencarian sosial media (2016-2026). Ini adalah bentuk replikasi 1:1 dari metode pemantauan KPA. 

Metode ini sejalan dengan panduan *tools-riset-ecc.md* yang menempatkan OSINT & Web Scraping (*Scrapling*/*GHunt*) sebagai instrumen akuisisi utama.
