# ROADMAP REVISI LANJUTAN (D3TLH)
*Dokumen ini merupakan hasil restrukturisasi dari catatan revisi asli agar lebih mudah dilacak progresnya (To-Do List).*

## Konteks Utama
- [ ] Tambahkan narasi dasar justifikasi: **"Kenapa studi kasus dipilih di skala Pulau Sulawesi?"**

---

## Bab 1: Makro Ekonomi
- [ ] **1.1 Breakdown PDRB:** Pastikan grafik mem-breakdown PDRB secara eksplisit per komoditas.
- [x] **1.2 Grafik PDRB vs Energi:** Ubah menjadi grafik batang saja. Grafik ledakan energi kotor/PLTU **digeser ke bagian Polusi Udara (Bab 2)**.
- [ ] **1.3 Treemap PAD & Investasi:** 
  - Hapus grafik *Treemap Breakdown PAD (Jenis Pendapatan Per Provinsi)*.
  - Grafik *Paradoks Investasi*: Tampilkan **grafik batang lonjakan kucuran modal saja**, HAPUS overlay/gabungan dengan grafik deforestasi.
- [x] **1.4 Peta Distribusi:** Ubah visualisasi menjadi **Peta Jalur Distribusi**.

---

## Bab 2: Kualitas Lingkungan
- [x] **2.1 Peta Choropleth (Smelter vs IKA):** Periksa kembali datanya (*re-check*), karena secara visual terlihat tidak berkorelasi.
- [x] **2.2 Grafik Tambahan (Kecil):** Jelaskan maksud dari grafik kecil di bawah, atau hapus/rombak jika visualisasinya membingungkan. (Dirombak sesuai gambar)
- [ ] **2.3 Polusi Udara:** (Aman / Sisipkan grafik ledakan energi dari 1.2 dan Emisi dari 2.4 ke sini).
- [x] **2.4 Deforestasi:**
  - Pada grafik evolusi temporal, ubah terminologi *"industri ekstraktif (tambang...)"* menjadi **"pertambangan dan sawit"**.
  - Bagian **"Emisi CO₂ per Driver"** dipindah/digeser naik ke bagian Polusi Udara.
- [ ] **2.5 Ancaman Biodiversitas:** (Aman).

---

## Bab 3: Beban Kesehatan
- [ ] **Judul Bab:** Ubah dari "Membayar" menjadi **"Hilirisasi yang Dibayar dengan Nyawa"**.
- [ ] **3.1 & 3.2:** Balik urutan penempatan seksinya.
- [ ] **3.3 Penyakit:** *Take-out* (hapus) data Kusta. Berikan opsi visualisasi data alternatif.
- [ ] **3.4 Peta Penyakit:** (Aman).
- [ ] **3.5 Korelasi Penyakit:** Ganti visualisasi (sebelumnya scatter plot IKA vs Diare) menjadi opsi lain, *preferably* menggunakan **grafik batang**.
- [ ] **3.6 Limbah B3:** Tambahkan 2 provinsi lainnya di bar chart meskipun angkanya kecil/tidak signifikan.
- [ ] **3.7 Zoonosis:** 
  - Tambahkan data/grafik **Malaria** (mirip gaya 3.3). 
  - Pastikan urutan 3.3 dan 3.7 disandingkan/diurutkan dengan baik.
  - Tarik bagian **11.4** (dari Bab 11) naik ke bagian Zoonosis ini.

---

## Bab 4: Konflik Sosial
- [ ] **4.1 Eskalasi Konflik:** Tambahkan analisis/narasi mengenai faktor pemicu ledakan konflik di tahun **2017**.
- [ ] **4.2 Monopoli Area:** (Sementara aman, perlu *re-check*).
- [ ] **4.3 Kriminalisasi (Tugas Saleh):** Pastikan dan validasi bagaimana skema "penempelan" status PSN pada pertambangan nikel terjadi di lapangan.
- [ ] **4.4 Pembuktian Statistik:** (Aman).
- [ ] **4.5 Peta Orkestrasi (NLP):**
  - **Aktor Korporasi:** Cek entitas bisnis PTPN vs PTPN Unit 14 (digabung jika sama).
  - **Aktor Sipil (Grafik Kanan):** Perjelas ormas yang dimaksud: apakah ormas *vigilante* (seperti GRIB Jaya, PP) atau ormas kebudayaan yang mencurigakan (*sus*).

---

## Bab 5: Pola Penerbitan Izin
- [ ] **5.1 Time-lag Deforestasi:** Uji coba menggeser maju angka deforestasi 1 tahun (Asumsi: IUP keluar 2016 -> *land clearing* 2017). Jika korelasi positif/match, perkuat justifikasinya dengan studi kasus.
- [ ] **5.2 Variabel Wilayah:** Ganti variabel "Taman Nasional" dan "Cagar Alam" menjadi wilayah **Livelihood** (zona pertanian, peternakan, perkebunan warga). Harus dibedakan dengan perkebunan monokultur skala besar.
- [ ] **5.3 Timeline Historis:** Potong grafik *Timeline Historis: Konflik & Izin* agar hanya dimulai dari **tahun 2000** ke atas (sebelumnya 1968-2025).

---

## Bab 8 & Bab 11 (Topik Lain-lain)
- [ ] **8.1 Tabel Top 10 Penguasa:** Tambahkan penjelasan/metodologi dasar asumsi perhitungan pada kolom **"Estimasi Rugi Ekologis"**.
- [ ] **8.2 Grafik ISPA (Duplicate):** Hapus grafik ISPA di bagian ini (karena berulang).
- [ ] **Bab Koridor Logistik Nikel:** **HAPUS / Take-out** dari *report* D3TLH. Jika tetap dipertahankan, cukup buat peta *supply chain* sederhana (dari tambang mana ke *port* mana).
- [ ] **Bab 11 (Demografi & Struktur Sosial):**
  - **11.1:** Hapus grafik (tidak terbaca & sudah direpresentasikan di 11.2).
  - **11.2:** (Aman).
  - **11.3 Komposisi PDRB:** Gabungkan variabel "Industri Pengolahan" dan "Pertambangan". Tambahkan variabel baru: **"Perikanan Tangkap"**.
  - **11.3 Indeks Agrikultur vs Industri:** Ubah warna *chart* agar lebih kontras.
  - **11.4:** (Sudah dipindah ke Bab 3 Zoonosis).


<br>
<br>

---

# DRAFT ASLI (RAW TEXT)
*Catatan orisinil dari user untuk referensi jika ada konteks yang terlewat.*

```text
Dasar kenapa studi kasus dipilih di skala Pulau Sulawesi
1.1 breakdown per komoditas
1.2 disajikan yang grafik batang aja. grafik ledakan energi kotor digeser ke polusi udara
1.3 Treemap Breakdown PAD: Jenis Pendapatan Per Provinsi hapus aja dulu
	Paradoks Investasi: Kucuran Modal vs Kebangkrutan Ekologis → cuman grafik batang lonjakan kucuran modal aja, grafik nggak usah di-overlay sama deforestasi
1.4 dibikin peta jalur distribusi

2.1 Peta Cloropleth Konsentrasi Smelter vs Indeks Kualitas Air (IKA) kindly rechecking, nggak korelatif
2.2 Dijelaskan grafik kecil di bawah makdusnya apa. Visualisasinya membingungkan
2.3 aman
2.4 di grafik evolusi temporal, terma ‘industri ekstraktif (tambang….)’ diganti jadi ‘pertambangan dan sawit
Emisi CO₂ per Driver — Kontribusi terhadap Krisis Iklim → bagian ini digeser naik ke bagian udara
2.5 aman

Judul Bab III ‘Hilirisasi yang Membayar dengan Nyawa’ Membayar → Dibayar
3.1 dan 3.2 dibalik urutannya
3.3 kusta ditake-out aja. Terus kasih opsi visualisasi data
3.4 aman
3.5 opsi visualisasi data lainnya. preferably pake grafik batang
3.6 grafik ‘beban limbah b3 per provinsi’ ditambah 2 provinsi lainnya meskipun gambaran bar-nya nggak signifikan
3.7 +data malaria kayak di 3.3 (3.3 dan 3.7 ini diurutkan)

4.1 data eskalasi th 2017 perlu dianalisis apa faktornya
4.2 sementara aman. kindly recheck
4.3 Tugas Saleh: make sure apakah pertambangan nikel skema ‘penempelan’ PSN-nya gimana
4.4 aman
4.5 PTPN vs PTPN unit 14 dicek entitas bisnisnya. Grafik kanan → ormas yang dimaksud adalah vigilante group kek GRIB Jaya, PP, dll atau ormas kebudayaan yang sus

5.1 ((Memungkinkan nggak)) kalau angka deforestasi itu digeser maju ke depan satu tahun. Asumsinya kalo IUP keluar 2016, mulai deforestasi/land clearing 2017. Kalo ternyata mach (berkorelasi positif) bisa diperkuat justifikasinya dengan studi kasus
5.2 ganti variabel TN dan cagar alam jadi livelihood (zona pertanian, peternakan, perkebunan warga, bedakan dengan perkebunan monokultur skala besar)
5.3 Grafik ‘Timeline Historis: Konflik Pertambangan & Masalah Izin (1968-2025)’ dipotong dari tahun 2000 aja

BAB 6 dan 7 setelah settling 1-5

8.1 Di tabel “Top 10 Penguasa Tahta Ekstraktif vs Kerugian Publik” bagian kolom estimasi rugi ekologis dijelaskan dasar asumsi/perhitungannya
8.2 kenapa ada grafik ISPA lagi????

BAB KORIDOR LOGISTIK NIKEL. Ini tuh nggak usah untuk report D3TLH
Harusnya sih dari tambang mana yang menyuplai ke port. terus dari port disupply ke mana

BAB DEMOGRAFI DAN STRUKTUR SOSIAL
11.1 itu grafiknuya nggak terbaca untuk menarik kesimpulan. saran kami di-take out aja karena udah direpresentasikan di 11.2 utk menggambarkan pola kepadatan di daerah industri ekstraktif
11.2 aman
11.3 grafik ‘komposisi PDRB sektor kunci’ untuk variabel ‘industri pengolahan’ dan ‘pertambangan’ dijadikan satu. ditambah variabel ‘perikanan tangkap’
grafik ‘agriculture to industry index’ warna chart yang lebih kontras
11.4  bagian ini ditarik naik ke bagian zoonosis
```
