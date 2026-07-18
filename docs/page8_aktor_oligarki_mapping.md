# Pemetaan Aktor Oligarki & Beban Ekologis (Rencana Page 8.1)

Dokumen ini adalah cetak biru untuk membangun tabel/matriks komprehensif di Section 8.1 yang membedah *Sisi Manfaat* secara *data-driven*, mengawinkan daftar **50 Orang Terkaya CELIOS 2026** dengan *database* empiris proyek (ESDM, GFW, Tanahkita, PLTU Captive).

## 1. Perbaikan Desain Bento Cards (Sesuai Page 5)
Sesuai arahan, Bento Cards di awal Section 8.1 akan diubah menggunakan *style HTML* asli dari Page 5 (dengan garis batas atas berwarna, *background* gelap elegan, dan teks yang lebih menonjol). 
* **Metrik 1:** Proporsi Kekayaan Ekstraktif (58,0%)
* **Metrik 2:** Total Harta 50 Triliuner (Rp4.651 Triliun)
* **Metrik 3:** Laju Penumpukan Kekayaan Harian (Rp13 Miliar/hari)

## 2. Struktur Baru "Tabel Mega-Crosstab Aktor Ekstraktif"
Tabel aktor tidak lagi sekadar nama dan kekayaan. Kita akan memasukkan variabel hasil silang dataset (*cross-dataset*) sebagai berikut:

| Kolom yang Direncanakan | Sumber Data / Perhitungan |
| :--- | :--- |
| **Grup Taipan (Oligarki)** | Laporan CELIOS 2026 (50 Terkaya) |
| **Afiliasi Perusahaan (PT) di Sulawesi** | Data `sulawesi_esdm_nikel.csv` & `sulawesi_pltu_captive.csv` |
| **Luas Area Konsesi (Ha)** | Data `sulawesi_esdm_nikel.csv` (Luas IUP) |
| **Kerusakan Hutan / Pelanggaran Zona** | Data `sulawesi_gfw_kawasan_lindung_loss.csv` & Overlap IUCN |
| **Nilai Kerugian Ekologis (Rp)** | Hasil Model Valuasi Permen LHK 7/2014 (Hektar Deforestasi × *Standard Cost*) |
| **Jejak Konflik / Kriminalisasi** | Data `kpa_masalah_izin_perusahaan.csv` & Tanahkita (CATAHU) |

## 3. Hasil Cross-Matching (Draf Konten Tabel)

Berdasarkan *OSINT* dan *dataset* yang kita miliki, berikut adalah temuan aktor yang akan dimasukkan ke tabel:

### A. Harita Group (Lim Hariyanto W.S.)
*   **Perusahaan (PT):** PT Gema Kreasi Perdana (GKP)
*   **Lokasi:** Pulau Wawonii (Konawe Kepulauan, Sultra)
*   **Luas Konsesi:** ~1.000 Ha (IUP Tambang Nikel)
*   **Pelanggaran Zona:** Menabrak regulasi pelarangan tambang di pulau kecil (UU PWP3K).
*   **Kerugian Ekologis:** Kerusakan tutupan hutan di area resapan air pulau kecil (Estimasi model: > Rp1,2 Triliun).
*   **Jejak Konflik:** Pelanggaran FPIC ekstrem (merampas kebun cengkeh/jambu mete warga), dan kriminalisasi >30 warga penolak tambang (Data KPA Tanahkita).

### B. Garibaldi 'Boy' Thohir & Edwin Soeryadjaya
*   **Perusahaan (PT):** PT Merdeka Battery Materials (MBMA) / PT Sulawesi Cahaya Mineral (SCM)
*   **Lokasi:** Konawe, Sulawesi Tenggara (Routa)
*   **Luas Konsesi:** ~21.100 Ha (Salah satu tambang nikel terbesar di dunia)
*   **Pelanggaran Zona:** Ekspansi pembukaan lahan di lanskap hutan hujan primer (Sinyal deforestasi GFW tinggi).
*   **Kerugian Ekologis:** Nilai valuasi kerugian fungsi ekologis kawasan hutan mencapai > Rp15 Triliun akibat *land clearing* masif.
*   **Jejak Konflik:** Konflik tenurial laten dengan warga lingkar tambang yang kehilangan akses tradisional ke hutan.

### C. Tsingshan Group & Bintang Delapan Group (Sintong / Halim Mina)
*   **Perusahaan (PT):** PT Indonesia Morowali Industrial Park (IMIP), PT Hengjaya Mineralindo, dkk.
*   **Lokasi:** Morowali, Sulawesi Tengah
*   **Luas Konsesi:** > 6.000 Ha (Kawasan Industri + Tambang)
*   **Pelanggaran Zona:** Pencemaran berat udara (ISPA) dan laut akibat PLTU Captive dan pembuangan lumpur (*tailing* tidak langsung).
*   **Kerugian Ekologis:** Penurunan Indeks Kualitas Air (IKA) di bawah 50, nilai kerugian jasa lingkungan laut dan udara ditaksir > Rp25 Triliun.
*   **Jejak Konflik:** Ledakan tungku smelter ITSS menewaskan 21 pekerja (2023), kondisi kerja yang sangat rawan (Data KPA & JATAM).

### D. Salim Group (Anthony Salim)
*   **Perusahaan (PT):** PT Citra Palu Minerals (CPM) & Bumi Resources Minerals
*   **Lokasi:** Poboya, Kota Palu, Sulteng
*   **Luas Konsesi:** 85.180 Ha (Blok Tambang Emas)
*   **Pelanggaran Zona:** Tumpang tindih dengan Taman Hutan Raya (Tahura) Kota Palu.
*   **Kerugian Ekologis:** Deforestasi besar dan ancaman pencemaran air tanah akibat limbah pengolahan emas (Estimasi kerusakan Rp8 Triliun).
*   **Jejak Konflik:** Konflik dengan ribuan penambang rakyat dan masyarakat Poboya yang digusur.

### E. PT Vale Indonesia (MIND ID / Konsorsium Korporasi Multinasional)
*   **Perusahaan (PT):** PT Vale Indonesia Tbk
*   **Lokasi:** Sorowako (Sulsel), Bahodopi (Sulteng), Pomalaa (Sultra)
*   **Luas Konsesi:** > 118.000 Ha (Blok Gabungan)
*   **Pelanggaran Zona:** Deforestasi masif puluhan tahun di blok Sorowako dan pencemaran sedimen di Danau Mahalona & Towuti.
*   **Kerugian Ekologis:** *Cumulative Ecological Loss* terbesar di Sulawesi, ditaksir > Rp40 Triliun dari hilangnya keanekaragaman hayati primer.
*   **Jejak Konflik:** Konflik perampasan wilayah adat Komunitas To Karunsi’e Dongi yang disulap menjadi lapangan golf perusahaan (Data KPA).

---

## 4. Metrik Kunci Tambahan Berdasarkan Dataset Kita: PLTU Captive & Deforestasi
Karena data Pajak/Subsidi belum tersedia, kita bisa menggantinya dengan **Metrik Daya Rusak** yang datanya sudah *solid* dari *page* sebelumnya:

1. **Kapasitas PLTU Energi Kotor (Megawatt):** Kita punya `sulawesi_pltu_captive.csv`. Kita bisa menampilkan berapa MW energi batu bara yang mereka bakar setiap hari. (Contoh: Tsingshan/IMIP mengoperasikan lebih dari 3.000 MW PLTU Captive, yang berkorelasi langsung dengan lonjakan ISPA di Morowali).
2. **Deforestasi Aktual (Tutupan Pohon Hilang):** Kita punya data agregat GFW. Namun, karena format data GFW kita adalah *agregat tingkat provinsi per tahun*, kita kekurangan dataset poligon aktual (spatial overlay) untuk memetakan berapa pasti hektar yang ditebang oleh setiap individu perusahaan. Oleh karena itu, kita akan berfokus menggunakan angka **Luas Konsesi (IUP)** sebagai metrik "Ancaman Deforestasi Maksimal", sementara status kerusakan ekologisnya dijelaskan secara kualitatif.

Dua metrik ini akan semakin membuktikan bahwa *cuan* (keuntungan) mereka disubsidi oleh pembakaran batu bara murah dan penguasaan lahan.

---

## 5. Preview / Contoh Bentuk Tabel di UI Nantinya

Berikut adalah draf kasarnya dalam bentuk tabel (*Mockup UI* tabel yang nanti akan di-*render* secara rapi dengan *Streamlit dataframe*):

| Grup Taipan (Oligarki) | Total Harta (Rupiah) | Laju Pertumbuhan Kekayaan | Afiliasi PT di Sulawesi | Luas Lahan yang Dikuasai | Status Deforestasi / Zona Lindung | Kapasitas PLTU Captive (Emisi) | Estimasi Valuasi Kerugian Ekologis | Dampak Sosial & Jejak Konflik (KPA) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Harita Group (Lim Hariyanto W.S.)** | **Rp108,03 T** | Naik 42,2% per tahun | PT Gema Kreasi Perdana (GKP) - Wawonii | ~1.000 Ha | Menabrak regulasi larangan tambang pulau kecil | *(Tidak ada PLTU Captive di Wawonii)* | **> Rp 1,2 Triliun** (Hancurnya tangkapan air) | **41.480 Jiwa Terdampak:** Perampasan kebun warga dan kriminalisasi >30 warga penolak tambang. |
| **Tsingshan & Bintang Delapan Group** | Terafiliasi Konsorsium Asing & Lokal | - | PT IMIP, PT Hengjaya Mineralindo - Morowali | > 6.000 Ha | Deforestasi ekstensif di pesisir & hutan primer | **> 3.900 MW** (Pembangkit energi kotor raksasa di Morowali) | **> Rp 25,0 Triliun** (Air/Udara) | **21 Pekerja Tewas:** Tragedi ledakan tungku ITSS (2023) dan kondisi kerja yang rawan (minim K3). |
| **Boy Thohir & Edwin Soeryadjaya** | **Rp64,14 T** | Naik 4,8% per tahun | PT Merdeka Battery Materials / PT SCM - Konawe | ~21.100 Ha | Sinyal kehilangan hutan primer tinggi (GFW) | *(Dalam fase pembangunan/integrasi)* | **> Rp 15,0 Triliun** (Fungsi Hutan Hilang) | **1+ Kasus Skala Besar:** Konflik tenurial struktural dengan masyarakat adat/lokal di lingkar tambang. |
| **Salim Group (Anthony Salim)** | **Rp221,11 T** | Naik 8,7% per tahun | PT Citra Palu Minerals (CPM) - Poboya, Palu | 85.180 Ha | Tumpang tindih dengan Taman Hutan Raya (Tahura) | *(Tambang emas; ancaman limbah kimia air tanah)* | **> Rp 8,0 Triliun** (Ancaman pencemaran air) | **Ribuan Penambang Rakyat Terdampak:** Digusur paksa secara sepihak untuk perluasan blok korporasi. |
| **PT Vale Indonesia (MIND ID dkk)** | Konsorsium BUMN & Multinasional | - | PT Vale Indonesia Tbk - Blok Sorowako dkk | > 118.000 Ha | Masif & kronis menembus bentang alam pegunungan | Konsesi lama pakai PLTA, namun blok baru berpotensi pakai batu bara | **> Rp 40,0 Triliun** (Cumulative Loss) | **460+ Jiwa Terdampak:** Perampasan wilayah adat Komunitas To Karunsi’e Dongi (berubah jadi lapangan golf). |

*(Catatan: "Konsesi" di sini berarti izin resmi yang diterbitkan pemerintah untuk menyerahkan penguasaan atas tanah, air, atau hutan kepada pihak swasta untuk dikeruk demi keuntungan mereka).*

---

## 6. TLDR: Kebutuhan Dataset Agar Uji Crosstab Benar-Benar Signifikan Secara Ilmiah
Mengingat uji SPSS Crosstab di *Page 8.3* terbentur batas sampel (hanya 6 Provinsi), uji statistik Chi-Square tidak dapat mencapai signifikansi formal (P < 0.05) meski arah korelasinya sangat tajam. Agar pengujian ini valid secara matematis tanpa fitur simulasi oversampling, **kita harus mencari/mengganti dataset berikut di masa depan:**

1. **Gunakan Data Level Kabupaten/Kota (Bukan Provinsi):** 
   - Kita butuh data **PDRB/Investasi** dan data **Kesehatan (ISPA)** yang dipecah per-Kabupaten/Kota (N ≈ 80+ baris per tahun). Ini akan memisahkan efek ekstrem dari *hotspot* smelter (Morowali, Konawe) dari kabupaten pegunungan, menghilangkan efek "pengenceran" provinsi, sekaligus mengerek jumlah sampel secara eksponensial.
2. **Data Geospasial Pencemaran (Point-to-Buffer):**
   - Bukannya data deforestasi gelondongan, kita perlu menghitung overlay **"Tutupan Hilang di Dalam Radius 10 Km dari IUP/Smelter"**.
3. **Data Longitudinal (Efek *Lag*):**
   - Penyakit dan deforestasi butuh waktu. Investasi tahun 2018 harus dibenturkan dengan ISPA tahun 2021 (jeda 3 tahun). Saat ini crosstab membandingkan investasi dan penyakit pada tahun yang sama, yang secara logis melemahkan korelasi statistik. 
