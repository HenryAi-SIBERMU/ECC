# Audit Forensik D3TLH: UI Pulau vs Algoritma Provinsi

Dokumen ini merangkum hasil investigasi dan komparasi nyata antara **Logika UI Pulau (Matriks Pembuktian Terbalik)** versus **Logika Algoritma Z-Score (Tabel Provinsi)** beserta bukti angka hasil *render* aktual.

## TLDR Forensik Pilar Udara

| Indikator | Metode Level Pulau (UI Card) | Metode Level Provinsi (Tabel Algoritma) | Hasil Aktual | Vonis (Mana yang Benar?) |
| :--- | :--- | :--- | :--- | :--- |
| **Udara 1 (PLTU & NO2)** | Mengambil *sum* kapasitas PLTU *captive*, grafiknya di-*inject* manual (hardcoded) *grid* Sultra dkk. | Dinamis membaca dari file `sulawesi_pltu_captive.csv` yang difilter per provinsi. | **UI**: Hardcoded Grid.<br>**Algo**: Dinamis per provinsi. | **Provinsi Lebih Valid**. |
| **Udara 2 (ISPA)** | Mendefinisikan 'Sentra' HANYA Sulteng+Sultra. Rata-rata IRR dihitung asal (Kasus / 2 vs Kasus / 4). | Menghitung Incidence Rate (kasus/10.000 jiwa BPS). | **UI**: 1.94x (Salah Rumus).<br>**Algo**: 3.50x (Max IRR Sulteng). | **Provinsi Sangat Benar.** |
| **Udara 3 (Limbah B3)** | Hanya menarik data "Sulawesi Tengah" lalu membaginya seolah itu mewakili seluruh Sulawesi. | Menjumlahkan limbah B3 per provinsi. | **UI**: 25.3 Juta Ton (Hanya Sulteng).<br>**Algo**: 32.8 Juta Ton (Seluruh Sulawesi). | **Provinsi Benar.** |
| **Udara 4 (Emisi CO2)** | Menjumlahkan seluruh emisi CO2 di tabel GFW. | Menjumlahkan emisi per wilayah secara spesifik. | **UI**: 804.1 Juta Ton.<br>**Algo**: 804.1 Juta Ton. | **Keduanya Sinkron.** |

## TLDR Forensik Pilar Air

| Indikator | Metode Level Pulau (UI Card) | Metode Level Provinsi (Tabel Algoritma) | Hasil Aktual (Bukti Render) | Vonis (Mana yang Benar?) |
| :--- | :--- | :--- | :--- | :--- |
| **Air 1 (IKA)** | Dihardcode eksplisit: `df_ika[Provinsi == 'Sulawesi Tengah']`. | Menghitung rata-rata IKA dari ke-6 provinsi secara dinamis. | **UI**: IKA = 62.07 (Data Sulteng).<br>**Algo**: IKA = 59.68 (Avg se-Sulawesi). | **Provinsi Lebih Valid**. |
| **Air 2 (Morbiditas Diare)** | Hardcode 'Sentra' (Sulteng+Sultra) & Hardcode populasi manual `2985000+2624000`. | Menghitung *Incidence Rate* dinamis per provinsi membandingkan populasi. | **UI**: IRR = 1.38x.<br>**Algo**: Max IRR = 1.52x. | **Provinsi Sangat Benar.** |
| **Air 3 (Konflik Air/Pesisir)** | Mengambil *length* dari seluruh file tanpa filter provinsi (`len(df_konflik_air)`). | Menggunakan filter text `.str.contains(prov_keyword)` pada kolom `lokasi` dan `judul`. | **UI**: 44 Kasus.<br>**Algo Tabel**: Total hanya 8 Kasus (karena filter string cacat). | 🔴 **UI KALI INI BENAR!**<br>Tabel backend sangat cacat karena jika `lokasi` tertulis "Sulteng", filter `str.contains("Tengah")` akan gagal, menyebabkan 36 kasus tidak terhitung! |
| **Air 4 (Beban Tailing DSTP)** | Dihardcode murni hanya melihat data limbah di `Sulawesi Tengah` sama persis dengan Udara 3. | Mengagregasi B3 per provinsi sesuai iterasi. | **UI**: 25.3 Jt Ton.<br>**Algo**: 32.8 Jt Ton. | **Provinsi Benar.** |

## Rekomendasi Eksekusi Pilar Air
1. **Air 1, Air 2, Air 4 (UI Pulau):** UI Card Pulau harus di-*refactor* total menggunakan variabel loop dari algoritma backend, persis seperti yang kita lakukan di Udara 1, 2, dan 3.
2. **Air 3 (Tabel Backend):** Tabel algoritma provinsi *harus diperbaiki*. Filter string `prov_keyword` yang naif membuat puluhan kasus tidak terhitung. Kita butuh filter mapping regex yang lebih toleran (misal: "Tengah|Sulteng", "Tenggara|Sultra", dll) agar tabel backend bisa menampilkan total 44 kasus jika dijumlahkan.

## TLDR Forensik Pilar Lahan

## TLDR Forensik Pilar Lahan

| Indikator | Metode Level Pulau (UI Card) | Metode Level Provinsi (Tabel Algoritma) | Hasil Aktual (Bukti Render) | Vonis (Mana yang Benar?) |
| :--- | :--- | :--- | :--- | :--- |
| **Lahan 1 (Bencana Alam)** | Menjumlahkan *seluruh* kejadian bencana (6 provinsi), tapi variabel & teks UI dikunci dengan string/label "Sulteng & Sultra". | Menghitung total bencana spesifik per provinsi. | **UI**: 1.609 Kejadian (Total Sulawesi tapi diklaim Sulteng).<br>**Algo**: Dinamis per provinsi. | **Provinsi Benar.** (UI salah pelabelan string). |
| **Lahan 2 (Deforestasi Primer)** | Menjumlahkan total deforestasi GFW dari seluruh provinsi, tapi diklaim dalam string UI sebagai "Sulteng & Sultra". | Menjumlahkan deforestasi spesifik per provinsi. | **UI**: Menampilkan agregat Sulawesi.<br>**Algo**: Dinamis per provinsi. | **Provinsi Benar.** (UI salah pelabelan string). |
| **Lahan 3 (Kawasan Lindung)** | Menjumlahkan pelanggaran kawasan lindung dari seluruh provinsi, tapi diklaim sebagai `lindung_sulteng`. | Menghitung luasan hilang spesifik per provinsi. | **UI**: Menampilkan agregat Sulawesi.<br>**Algo**: Dinamis per provinsi. | **Provinsi Benar.** (UI salah pelabelan string). |
| **Lahan 4 (Aktor Deforestasi)** | Menjumlahkan deforestasi tambang dari seluruh provinsi, tapi diklaim sebagai `deforestasi_tambang_sulteng`. | Menghitung deforestasi komoditas tambang spesifik per provinsi. | **UI**: Menampilkan agregat Sulawesi.<br>**Algo**: Dinamis per provinsi. | **Provinsi Benar.** (UI salah pelabelan string). |
| **Lahan 5 (Kepadatan Spasial)** | Telah direfactor. Menghitung (Total IUP Aktif / Luas Daratan) = Rasio Kepadatan. | Menghitung (Total IUP Aktif / Luas Daratan). Keduanya sudah seragam. | **UI**: ~6.2%.<br>**Algo**: ~6.2%. | **Keduanya Sinkron (Sudah Diperbaiki).** |

## TLDR Forensik Pilar Sosial

| Indikator | Metode Level Pulau (UI Card) | Metode Level Provinsi (Tabel Algoritma) | Hasil Aktual (Bukti Render) | Vonis (Mana yang Benar?) |
| :--- | :--- | :--- | :--- | :--- |
| **Sosial 1 (FPIC)** | Mengambil *length* dari seluruh dataset FPIC (semua tahun) tanpa filter. | Memfilter ketat `tahun >= 2014` (Era 1 Dekade Terakhir) & filter provinsi. | **UI**: 6 Kasus.<br>**Algo**: 3 Kasus (Jika diakumulasi nasional). | **Provinsi Benar.** (Analisis difokuskan pada 1 dekade terakhir, UI gagal memfilter tahun). |
| **Sosial 2 (Jiwa Terdampak)** | Menjumlahkan seluruh baris data dari segala tahun tanpa filter. | Memfilter `tahun >= 2014` dan sudah menggunakan kolom AI `provinsi_ner`. | **UI**: 70.471 Jiwa.<br>**Algo**: 54.310 Jiwa. | **Provinsi Sangat Benar.** (Algoritma berhasil memfilter 1 dekade terakhir dan memetakan string lokasi rumit dengan NER. UI salah karena tidak memfilter tahun). |
| **Sosial 3 (Kriminalisasi)** | Menjumlahkan seluruh insiden (semua tahun) dari dataset. | Memfilter `tahun >= 2014` dan sudah menggunakan kolom AI `provinsi_ner`. | **UI**: 38 Insiden.<br>**Algo**: 21 Insiden. | **Provinsi Sangat Benar.** (Sama seperti Sosial 2, UI salah karena tidak memfilter tahun). |
| **Sosial 4 (Faskes)** | Di-*hardcode* manual `spa_aktual_pct = 42.5`. Logika lama: Gap Target SPA 80%. | Mengubah drastis konsep menjadi dinamis: Rasio Pasien (ISPA+Diare) berbanding Jumlah Faskes. | **UI**: 42.5% (Hardcode statis).<br>**Algo**: Dinamis menghitung beban pasien di faskes per provinsi. | 🔴 **DISONANSI KOGNITIF.** UI dan Algo mengukur indikator yang sama sekali berbeda secara fundamental. Algo Provinsi lebih *data-driven* dan realistis. |

## Rekomendasi Eksekusi Pilar Sosial
1. **Sosial 1, 2, 3 (UI Pulau):** Harus direfactor untuk mengimplementasikan filter `tahun >= 2014` (jendela 1 dekade terakhir) agar selaras dengan tabel backend.
3. **Sosial 4 (Faskes):** Rombak total! Hapus UI statis SPA 80% yang di-*hardcode*, dan migrasikan UI Lahan 4 untuk menampilkan metrik Rasio Pasien (Beban Faskes) sesuai yang diimplementasikan di Backend Provinsi, karena ini jauh lebih *insightful* untuk D3TLH.
