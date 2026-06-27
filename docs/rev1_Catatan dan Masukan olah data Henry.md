# Catatan dan Masukan olah data Henry

1. **Pertanyaan penelitian**
   - P3 pertanyaan tambahan/lanjutan: dan bagaimana mengukurnya?
   - P4 tekanan sosio-ekologis (tambahin sosio untuk menunjukkan)
   - P5 mengukur potensi dampak
   - P6 apa kebuntuan tata kelola
   - P7 usul bukan biaya ekologis tapi beban ekologis

3. **Rencana temuan studi**
   - Kesehatan: tren peningkatan penyakit (perlu diperluas, karena bisa lebih bervariasi, misal yang disebabkan oleh zoonosis)
   - Sosial: tambah data migrasi, dan perubahan pola ruang desa-kota
   - <span style="color:red">Pertanyaan:</span> Perubahan pola atau jenis pekerjaan masuk di mana?

4.1 **Ekspansi industrii…**
   - Jika dibayangkan butuh jalur transportasi baru dalam perkembangn industri, apakah memungkinkan dicari? Misal ada proyeksi penambahan jalur kereta yang menghubungkan KEK. Sementara hasil dugaan awal, KEK dijadikan legitimasi pembukaan tambang baru. Atau soal lokasi port dan apa fungsinya? Ada beberapa port yang juga diduga dijadikan sandar pasokan bahan baku ilegal
   - <span style="color:red">Pertanyaan:</span> apakah penambahan smelter misal, itu udah masuk kategori nikel?

4.2 **Penurunan kualitas lingkungan**
   - Tren bencana
   - Tren penurunan biodiversitas

4.3 **Beban kesehatan dan dampak sosial**
   - Mungkin migrasi yang ada di atas masuk sini, atau tetap di atas?
   - Penyankit bisa lebih diperluas selain soal penyakit pernapasasn? Atau setidaknya cek kalau ada tren yang menjadi anomali. Tapi ini juga melihat spesifik kawasan tertentu apakah dia zona karst, smelter atau semacamnya

4.4 **Konflik sosial**
   - Jika memungkinkan apakah ada data peningkatan data ormas baru? Bisa masuk melalui scraping portal berita. Misal nih yaa [Lembaga Adat Suku Pagu dukung aktivitas tambang di Halmahera - ANTARA News Ambon, Maluku](https://ambon.antaranews.com)
   - Rekomendasi link konflik agraria [https://www.tanahkita.id/home](https://www.tanahkita.id/home)

---

## 🎯 Roadmap Eksekusi Revisi (Fase Penambahan Data)

Berdasarkan catatan di atas, berikut adalah *action items* yang dipecah ke dalam 6 fase eksekusi untuk melengkapi riset:

### Fase 1: Penyelarasan Kerangka Teori (PRD Update)
* 🎯 **STATUS:** **SELESAI**
* **[23 Juni 2026] Log Eksekusi:**
  - ✅ **ACTION TAKEN:**
    - Mengganti istilah "Biaya Ekologis" menjadi "Beban Ekologis (sebelumnya Biaya Ekologis)" secara menyeluruh di dokumen kerangka dan *UI Dashboard* (`pages/8_Distribusi_Manfaat.py`).
    - Mengintegrasikan variabel "Tekanan Sosio-Ekologis", "Potensi Dampak", dan indikator "Kebuntuan Tata Kelola" ke dalam pertanyaan riset di dokumen PRD utama.
* 🎯 **TARGET:** Mengubah kerangka berpikir dan terminologi dasar di dokumen riset.
* 📋 **TUGAS:** 
    *   Mengganti istilah "Biaya Ekologis" menjadi **"Beban Ekologis"** di seluruh dokumen dan UI *dashboard*.
    *   Mengintegrasikan variabel "Tekanan Sosio-Ekologis" dan indikator "Kebuntuan Tata Kelola" ke dalam *outline* riset.

### Fase 2: Ekstraksi Data Kesehatan Spesifik (Zoonosis & Anomali Karst)
* 🎯 **STATUS:** **SELESAI**
* **[26 Juni 2026] Log Eksekusi:**
  - ✅ **ACTION TAKEN:**
    - Pemrosesan data Zoonosis (DBD, Malaria, Filariasis, Rabies) dari sumber dinas kesehatan ke dalam `zoonosis_kab_kota_2015_2024.csv`.
    - Mengintegrasikan analisis "Anomali Zoonosis" ke dalam `pages/3_Beban_Kesehatan.py` (Bagian 3.6).
    - Menerapkan *crosstabulation* yang membandingkan rata-rata kasus penyakit antara wilayah Lingkar Tambang/Smelter (Morowali, Morowali Utara, Banggai) vs Wilayah Kontrol (Agraris).
    - Membangun *Hero Statement* berbasis *data-driven* yang membeberkan narasi kritis mengenai hancurnya daya dukung ekologis akibat *smelter*.
* 🎯 **TARGET:** Memperluas metrik penyakit di luar ISPA (Pernapasan).
* 📋 **TUGAS:** 
    *   *Scraping* data BPS/Kemenkes terkait tren penyakit **Zoonosis** (Malaria, DBD, dll) di 6 provinsi Sulawesi.
    *   Pemetaan *Crosstab* khusus: Korelasi anomali penyakit dengan proksimitas wilayah tambang/smelter dan zona karst.

### Fase 3: Pelacakan Infrastruktur Logistik (Pelabuhan & Rel Kereta)
* ⏳ **STATUS:** **PENDING**
* **Log Eksekusi:** Belum dimulai.
* 🎯 **TARGET:** Membuktikan KEK sebagai legitimasi ekspansi tambang.
* 📋 **TUGAS:** 
    *   *Data Mining* daftar pembangunan Pelabuhan (*Port*) khusus tambang/smelter beserta fungsinya (mencari celah pasokan ilegal).
    *   *OSINT Tracking* proyek strategis nasional terkait jalur kereta api penghubung KEK di Sulawesi.
    *   *Validasi:* Memastikan penambahan infrastruktur *smelter* memang masuk dalam klasifikasi nikel.

### Fase 4: Analisis Demografi, Sosial, & Ketenagakerjaan
* ⏳ **STATUS:** **PENDING**
* **Log Eksekusi:** Belum dimulai.
* 🎯 **TARGET:** Mengukur pergeseran struktur sosial di lingkar tambang.
* 📋 **TUGAS:** 
    *   Ekstraksi data **Migrasi Penduduk** (BPS) antar kabupaten/provinsi (Dampak *Smelter*).
    *   Pengambilan data **Perubahan Pola Ruang** (Desa ke Kota) / Urbanisasi.
    *   *Mapping* Perubahan Jenis Pekerjaan (Peralihan dari sektor agraris ke industri).

### Fase 5: Dimensi Ekologis Ekstensif (Bencana & Biodiversitas)
* ⏳ **STATUS:** **PENDING**
* **Log Eksekusi:** Belum dimulai.
* 🎯 **TARGET:** Menambah bukti empiris penurunan kualitas lingkungan di luar emisi dan limbah.
* 📋 **TUGAS:** 
    *   *Scraping* data BNPB (DIBI) untuk mendapatkan **Tren Bencana Alam** (banjir/longsor) di Sulawesi dalam 1 dekade terakhir.
    *   *Data Mining* laporan KLHK/NGO terkait tren hilangnya/penurunan **Biodiversitas** di kawasan hutan primer yang dibongkar.

### Fase 6: OSINT Konflik Sosial & Peta Aktor (Ormas)
* ⏳ **STATUS:** **PENDING**
* **Log Eksekusi:** Belum dimulai.
* 🎯 **TARGET:** Memetakan resistensi vs dukungan masyarakat buatan (orkestrasi konflik horizontal).
* 📋 **TUGAS:** 
    *   *Web Scraping* portal berita (Antara, Mongabay, dll) menggunakan *keyword* spesifik untuk melacak **tren kemunculan Ormas/Lembaga Adat baru** yang membela aktivitas tambang (Contoh kasus: Halmahera/Sulawesi).
    *   Ekstraksi dan integrasi penuh *database* konflik agraria dari **tanahkita.id** ke dalam Master Dataset Konflik.
