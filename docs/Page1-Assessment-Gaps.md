# Asesmen Kesiapan Dataset - Page 1 (Ekspansi Industri & Intensifikasi Pemanfaatan Ruang)

**Tanggal Asesmen:** 14 Juni 2026
**Fokus:** Membaca pola pertumbuhan industri pengolahan alam (tambang, nikel, semen) di Pulau Sulawesi sebagai sumber tekanan utama terhadap daya dukung lingkungan.
**Tujuan Akhir:** Menyiapkan Crosstab untuk Page 1 (Jumlah Izin vs Tahun, Jumlah Smelter vs Luas Lahan, Investasi vs Ekspansi Industri).

---

## ✅ 1. DATA YANG SUDAH SIAP (CLEAN)

Dataset utama berikut sudah tersedia di dalam folder `data/processed/` dan siap digunakan untuk merakit Page 1:

1. **Jumlah Smelter & Kapasitas Produksi**
   - **File:** `sulawesi_esdm_nikel.csv`
   - **Status:** Sangat Solid. Berisi *merging* data 21 smelter di Sulawesi (sumber CGS) beserta detail profil perusahaan dari Minerbaone.

2. **Data Tren Investasi (PMDN & Asing)**
   - **File:** `sulawesi_investasi_pmdn_2016_2024.csv` & `sulawesi_investasi_nikel.csv`
   - **Status:** Siap. Bisa langsung digunakan untuk visualisasi "Tren Investasi vs Ekspansi Industri".

3. **Luas Lahan / Intensifikasi Ruang (Proxy Ekologis)**
   - **File:** `sulawesi_gfw_master_1_dekade_2014_2023.csv`
   - **Status:** Siap. Kolom `Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha` berfungsi sebagai proksi terbaik yang menunjukkan *real impact* dari intensifikasi pemanfaatan ruang akibat ekspansi tambang.

---

## ⚠️ 2. GAPS & KEKURANGAN DATA (BUTUH TINDAKAN)

Terdapat beberapa komponen penting yang diwajibkan oleh *outline* riset, namun wujud file `clean` (*processed*)-nya belum tersedia:

### A. Data PLTU Captive Belum Ada di Folder Processed
- **Konteks:** Pertumbuhan PLTU *Captive* (off-grid) adalah salah satu ciri khas kawasan industri nikel di Sulawesi.
- **Kondisi Saat Ini:** File *raw data* dari GEM (*Global Energy Monitor*) dilaporkan sudah diunduh (berada di `data/raw/ESDM/`), tetapi belum di-*clean* dan belum dipisahkan khusus untuk region Sulawesi.
- **Action Required:** Membaca dataset GEM, mem-filter PLTU Captive di Sulawesi, dan menyimpannya menjadi `data/processed/sulawesi_pltu_captive.csv`.

### B. Timeline Izin per Tahun Belum Rapi
- **Konteks:** Outline mensyaratkan adanya grafik *crosstab* antara **Jumlah Izin Baru vs Tahun**. 
- **Kondisi Saat Ini:** Profil perusahaan/smelter sudah ada, tapi belum dipastikan apakah kita memiliki kolom "Tahun Terbit IUP/Izin Smelter" atau "Tahun Mulai Operasi" yang *clean* dan bisa di-*plot* sebagai *timeline*.
- **Action Required:** Membedah file `sulawesi_esdm_nikel.csv` atau `minerbaone_permits.csv` di folder `raw` untuk merapikan kolom Tahun Izin/Operasi.

### C. Luas Kawasan Industri (Agregat)
- **Konteks:** Beberapa izin terkonsentrasi di dalam satu kawasan mega-industri (seperti IMIP di Morowali atau VDNI di Konawe).
- **Kondisi Saat Ini:** Data masih tersebar per nama perusahaan/smelter. Belum ada rekap khusus yang menyatakan "Luas IMIP X Hektar, Luas VDNI Y Hektar".
- **Action Required:** Mencari atau mengagregasi data estimasi luasan kawasan industri dari file profil smelter yang ada, atau menggunakan data AMDAL yang sudah di-*scrape*.

---

## 🚀 3. REKOMENDASI NEXT ACTION

Sebelum tim mulai merakit *dashboard* atau kode visualisasi untuk Page 1, agen harus mengeksekusi dua langkah teknis ini:
1. **[Scripting]** Buat script python untuk mengekstrak dan membersihkan data PLTU Captive (dari GEM dataset) menjadi file processed.
2. **[Scripting]** Buat script verifikasi/cleaning untuk mengekstrak "Tahun Terbit Izin" dari master data ESDM agar grafik *timeline* bisa dibuat dengan akurat.
