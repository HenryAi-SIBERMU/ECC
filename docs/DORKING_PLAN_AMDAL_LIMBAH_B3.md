# Rencana Dorking & Investigasi: Metadata Mikro Limbah B3 Tambang/Smelter

Dokumen ini adalah cetak biru (*blueprint*) investigasi OSINT (*Open-Source Intelligence*) dan *Google Dorking* untuk mengakali *Data Vacuum* (ketertutupan data) terkait volume dan komposisi Limbah B3 dari fasilitas pengolahan nikel dan mineral lainnya di Indonesia, khususnya regional Sulawesi dan Maluku.

Mengingat portal pemerintah (SIRAJA dan Amdalnet KLHK) bersifat tertutup/terenkripsi, strategi ini fokus pada pengepungan data dari portal internasional, dokumen AMDAL yang bocor, serta laporan teknis LSM/Akademisi.

---

## 1. Target Data (Metadata Mikro)
Data yang dicari memiliki tingkat resolusi fasilitias/pabrik (bukan agregat nasional):
1. **Identitas Fasilitas:** Nama Perusahaan / Smelter, Lokasi (Koordinat/Kawasan).
2. **Kapasitas Limbah:** Volume limbah padat (Slag/Tailing) per tahun.
3. **Kapasitas Cair:** Debit pelepasan efluen cair (juta m³).
4. **Metode Penyimpanan:** *Deep Sea Tailings Placement* (DSTP), *Dry-Stack Tailings*, atau Bendungan Tailing Konvensional.
5. **Kategori Bahaya:** Kandungan logam berat spesifik (Cr6+, Pb, dsb).

---

## 2. Strategi Dorking Level 1: Dokumen Lingkungan (AMDAL & RKL-RPL)

Setiap perusahaan wajib menyusun Analisis Mengenai Dampak Lingkungan (AMDAL) dan Rencana Pengelolaan Lingkungan (RKL-RPL). Meskipun tidak dipublikasikan resmi, dokumen ini kerap "bocor" (diunggah tidak sengaja oleh pemda, konsultan, atau mahasiswa).

### 2.1 Keyword Pencarian (Google Dorks)
Kopi-paste *query* ini ke mesin pencari Google:
*   `"RKL-RPL" OR "AMDAL" AND "tailing" OR "slag" "Indonesia" filetype:pdf`
*   `site:go.id "RKL-RPL" "pengelolaan limbah B3" "smelter"`
*   `"izin lingkungan" "limbah B3" "tailing" "IMIP" OR "VDNI" filetype:pdf`
*   `"Executive Summary" AMDAL smelter nikel filetype:pdf`

**Tanda Sukses:** Menemukan tabel matriks RKL-RPL yang menunjukkan "Sumber Dampak", "Tolok Ukur", dan "Besaran Dampak" (tonase).

---

## 3. Strategi Dorking Level 2: Spesifik Teknologi Limbah (HPAL & DSTP)

Berfokus pada metode pembuangan limbah teknologi tingkat lanjut (seperti HPAL untuk baterai EV) yang sering memicu resistensi NGO dan sorotan internasional.

### 3.1 Keyword Pencarian (Google Dorks)
*   `"dry-stack tailings" "Indonesia" "nickel" filetype:pdf`
*   `"Tailings Storage Facility" OR "TSF" "Morowali" OR "Konawe" OR "Obi" filetype:pdf`
*   `"Deep Sea Tailings Placement" OR DSTP "Indonesia" "Ramu" OR "Obi" filetype:pdf`
*   `"slurry" "limbah" "nikel" "ton per tahun" filetype:pdf`

**Tanda Sukses:** Menemukan kajian spesifik tentang kapasitas bendungan tailing atau jalur pipa pembuangan laut, biasanya berbahasa Inggris atau riset kolaborasi.

---

## 4. Strategi Level 3: Portal Data Internasional & Komersial

Mengakses pangkalan data intelijen global yang melacak jejak ESG (*Environmental, Social, and Governance*) dari perusahaan-perusahaan multinasional yang beroperasi di Indonesia.

### 4.1 Database Terbuka (Public/UN)
*   **Target:** [Global Tailings Portal (GRID-Arendal)](https://tailing.grida.no/)
*   **Deskripsi:** Database PBB yang melacak fasilitas penyimpanan tailing di seluruh dunia.
*   **Metode:** Mencari negara "Indonesia" langsung di portal mereka atau menggunakan Dork: `"Global Tailings Portal" Indonesia nickel`

### 4.2 Database Komersial/Berbayar (Opsi Tingkat Lanjut)
Apabila diperlukan analisis mendalam untuk mengukur biaya pemulihan ekologis secara moneter, platform ini menyediakan data level-pabrik:
1. **S&P Global Market Intelligence:** Dork: `"S&P Global Market Intelligence" "tailings" Indonesia` (Biasanya dalam modul *Mine Economics*).
2. **Wood Mackenzie:** Dork: `"Wood Mackenzie" "nickel cost curve" tailings Indonesia` (Menyediakan intelijen komoditas dan estimasi biaya pengelolaan limbah).
3. **Benchmark Mineral Intelligence:** Dork: `"Benchmark Mineral Intelligence" ESG nickel tailings Indonesia` (Melacak jejak karbon dan praktik tailing pada rantai pasok EV).

---

## 4. Strategi Level 4: Dorking Spesifik Perusahaan (Data ESDM)

Untuk mendapatkan data dengan resolusi tingkat fasilitas, kita dapat menggunakan daftar nama perusahaan penambang/pemurni nikel dari database resmi Kementerian ESDM.

### 4.1 Keyword Pencarian (*Targeted Company Dorking*)
Gunakan nama PT spesifik (berdasarkan filter "Top 50" perusahaan dengan konsesi terbesar) untuk menjebak dokumen AMDAL spesifik:
*   `"[NAMA PERUSAHAAN DARI CSV ESDM]" "AMDAL" OR "RKL-RPL" "limbah" OR "tailing" filetype:pdf`
*   *Contoh:* `"CITRA LAMPIA MANDIRI" "AMDAL" OR "RKL-RPL" "limbah" OR "tailing" filetype:pdf`

**Tanda Sukses:** Menemukan *executive summary* RKL-RPL spesifik milik PT terkait, yang merincikan koordinat fasilitas pengolahan (*tailing dam*) dan volume limbah ton/tahun. Karena sifatnya sangat presisi, pencarian ini bisa diotomatisasi secara terbatas (mempertimbangkan batas kuota API Google CSE).

---

## 5. Tata Cara Eksekusi

1. **Jalankan Dorking:** Eksekusi keyword di atas satu per satu.
2. **Koleksi PDF:** Unduh semua dokumen PDF yang relevan ke dalam folder `data/raw/klhk_ngo_reports` atau `data/raw/amdal_leaks`.
3. **Deep Parsing Otomatis:** Setelah PDF terkumpul, jalankan *script* Python `parse_ngo_user_files.py` milik agen AI untuk secara otomatis men- *scan* dan mengekstrak tabel/kalimat yang mengandung variabel tonase (contoh: "12 juta ton", "Tailing", "Slag").
4. **Update CSV:** Masukkan angka hasil ekstraksi ke dalam `sulawesi_limbah_b3_ngo_proxy.csv`.

*Dokumen ini dibuat pada Juni 2026 sebagai navigasi operasional tim periset CELIOS.*
