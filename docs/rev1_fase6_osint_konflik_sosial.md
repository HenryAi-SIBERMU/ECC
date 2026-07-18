# Rencana Eksekusi Revisi Fase 6: OSINT Konflik Sosial & Peta Aktor

## Latar Belakang & Tujuan
Sesuai arahan pada `rev1_Catatan dan Masukan olah data Henry.md` (Fase 6), tujuan dari fase ini adalah untuk membongkar **Dimensi Konflik Sosial** akibat ekspansi *smelter* dan kawasan industri tambang. 
Fokus utamanya adalah memetakan dua hal:
1. **Intensitas Konflik & Kriminalisasi Warga:** Mengekstrak data riil perampasan ruang hidup dari *database* Konsorsium Pembaruan Agraria (KPA) / **TanahKita.id**.
2. **Peta Orkestrasi Konflik Horizontal:** Mendeteksi kemunculan ormas atau lembaga adat "tandingan" yang tiba-tiba muncul untuk memberikan dukungan politik (seolah-olah dukungan publik) terhadap aktivitas tambang, guna membungkam resistensi murni masyarakat adat/lokal.

---

## Strategi Eksekusi

### 1. Integrasi Data Kriminalisasi TanahKita.id
*Update: Dataset TanahKita ternyata sudah tersedia dan komplit.* Kita akan langsung menggunakan data dari `data/processed/sulawesi_konflik_agraria_tanahkita.csv`.
*   **Status Data:** Dataset telah memuat kolom `luas_ha`, `dampak_masyarakat_jiwa`, `narasi`, dan kolom `indikasi_kriminalisasi` (True/False) hasil ekstraksi teks.
*   **Tindakan Selanjutnya:** Fokus utama pada data ini hanyalah pemfilteran khusus wilayah lingkar tambang nikel (mengiris data dengan letak IUP/Smelter) dan menampilkannya sebagai *Bento Cards* dan tabel *Crosstab* di Dashboard.

### 2. Peta Aktor & Orkestrasi Konflik (Data-Driven TanahKita)
*Update: Sesuai temuan terbaru, kita **TIDAK PERLU** melakukan OSINT Web Scraping.* Dataset `sulawesi_konflik_agraria_tanahkita.csv` ternyata sudah memiliki kolom *Profiling Aktor* yang sangat terperinci, yaitu:
*   `keterlibatan_pemerintah` (Contoh: Kementerian ESDM, Kepolisian, Pemda).
*   `keterlibatan_perusahaan` (Contoh: PT Antam, PT IMIP).
*   `keterlibatan_masyarakat` (Contoh: Jatam, Walhi, Ormas Lokal, Lembaga Adat).

*   **Metode Eksekusi:**
    1.  Membaca dataset menggunakan Pandas.
    2.  Melakukan *string splitting* (pemisahan karakter `|`) pada kolom `keterlibatan_masyarakat` dan `keterlibatan_pemerintah` untuk mengekstrak entitas independen.
    3.  Menghitung frekuensi (*value counts*) kemunculan aktor-aktor negara dan non-negara (LSM/Ormas/Lembaga Adat) dalam kasus perampasan lahan.
    4.  Membangun matriks relasi (Peta Aktor) untuk divisualisasikan di Dashboard.

### 3. Integrasi & Visualisasi UI di Dashboard (Page 4)
*   **Lokasi Page:** `pages/4_Konflik_Sosial.py` (Akan dieksekusi selanjutnya).
*   **Visualisasi Utama:** 
    *   *Bento Cards* untuk Total Kasus Konflik, Total Luas Lahan Dirampas, dan Total Insiden Kriminalisasi.
    *   *Bar Chart / Network Graph* Profiling Aktor yang terlibat.
    *   *Hero Statement* yang kuat mengenai eskalasi konflik horisontal dan perampasan ruang.

### 3. Integrasi & Visualisasi UI di Dashboard
*   **Lokasi Page:** Kemungkinan akan diletakkan di **Page 4 (Konflik Sosial & Demografi)** atau jika terlalu besar, dibuat *page* khusus.
*   **Visualisasi:** 
    *   *Bento Cards* untuk Total Kasus Konflik, Total Luas Lahan Dirampas, dan Total Kasus Kriminalisasi.
    *   Tabel Matriks Profiling Aktor: Membandingkan Aktor Pro-Tambang (Ormas/Lembaga Bentukan) vs Aktor Anti-Tambang (Petani, Nelayan, Warga Asli).
    *   *Hero Statement* yang kuat mengenai "Orkestrasi Konflik Horizontal".

---
## Kebutuhan & Blocker Saat Ini
Sebelum penulisan skrip scraper TanahKita dan OSINT dimulai, apakah strategi pencarian *keyword* untuk pemetaan aktor ini sudah sesuai dengan narasi yang ingin ditekankan? Atau ada tambahan portal berita alternatif (*Watchdog*) yang harus diutamakan?
