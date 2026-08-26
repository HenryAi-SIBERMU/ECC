# Asumsi dan Keputusan (Decision Log)

Dokumen ini berfungsi sebagai arsip untuk mencatat semua asumsi, keputusan desain, dan anomali logika yang sengaja dipertahankan di dalam sistem Dashboard Audit D3TLH. Tujuannya adalah agar pengembang dan analis di masa depan memahami konteks di balik perbedaan angka atau logika tertentu.

---

## 1. Veto 3 (Karpet Merah Energi Kotor / PLTU Captive)
**Tanggal Dicatat:** 22 Agustus 2026

**Konteks:** Terdapat perbedaan total kapasitas PLTU Captive antara ringkasan *Card* utama (Veto Pulau) dan penjabaran pada Tabel per Provinsi.
*   **Card Utama (10.26 GW):** Menghitung **seluruh** kapasitas PLTU yang berstatus aktif (termasuk yang berstatus *Operating*, *Construction*, *Announced*, dll). Filter yang digunakan membuang status 'Cancelled' dan 'Shelved'. 
*   **Tabel Provinsi / Skor Mesin (9.83 GW):** Hanya menghitung kapasitas PLTU yang secara eksplisit berstatus **'Operating'** (beroperasi) saja.

**Keputusan:** Perbedaan ini **DIBIARKAN / DIPERTAHANKAN**. 
**Alasan:** *Card* utama berfungsi sebagai peringatan ancaman iklim secara makro (sehingga wajar memasukkan PLTU yang sedang dibangun), sedangkan tabel provinsi digunakan untuk *scoring* dampak langsung yang sudah terjadi saat ini di lapangan (sehingga hanya menghitung yang sudah beroperasi).

---

## 2. Definisi "Sentra Industri Ekstraktif" (7 Kabupaten)
**Tanggal Dicatat:** 22 Agustus 2026

**Konteks:** Sistem melakukan perbandingan kondisi demografi dan sosial-ekonomi (krisis ruang hidup, prevalensi ISPA, dll) antara daerah "Sentra Industri Ekstraktif" versus daerah "Non-Sentra". Saat ini, daftar 7 kabupaten sentra tersebut secara teknis di-*hardcode* di dalam kode agar komputasi tidak terlalu berat.

**Keputusan (Asumsi):** Daftar 7 kabupaten sentra ini **DIPERTAHANKAN**, karena didasarkan pada asumsi empiris riil yang diolah dari dataset mentah `sulawesi_izin_raw_details.csv`.

**Alasan & Metodologi:**
Berdasarkan data mentah perizinan tambang ESDM, kita menetapkan *threshold* (batas ambang) esktrem bahwa kabupaten "Sentra" adalah wilayah yang menanggung beban izin konsesi lahan tambang (IUP) **di atas 25.000 Hektar**. 

Hasil agregasi luas konsesi menempatkan ketujuh kabupaten ini sebagai episentrum absolut eksploitasi lahan di Sulawesi (dan semuanya menjadi basis operasi kawasan industri/smelter raksasa):

1. **Morowali (Sulawesi Tengah)**
   - **Luas Konsesi (IUP):** > 73.722 Ha (bahkan mencapai > 169.000 Ha jika dihitung akumulasi lintas batas).
   - **Industri Smelter / Perusahaan Utama:** Indonesia Morowali Industrial Park (IMIP), PT Bintang Delapan, Tsingshan.
2. **Luwu Timur (Sulawesi Selatan)**
   - **Luas Konsesi (IUP):** > 27.398 Ha (mencapai > 124.000 Ha jika dihitung dengan konsesi lintas batas blok tambang).
   - **Industri Smelter / Perusahaan Utama:** PT Vale Indonesia (Sorowako).
3. **Banggai (Sulawesi Tengah)**
   - **Luas Konsesi (IUP):** 59.545 Ha.
   - **Konteks:** Daerah lingkar tambang yang terdampak langsung (termasuk hilir dari operasi industri ekstraktif dan suplai nikel/gas).
4. **Morowali Utara (Sulawesi Tengah)**
   - **Luas Konsesi (IUP):** 48.257 Ha.
   - **Industri Smelter / Perusahaan Utama:** PT Gunbuster Nickel Industry (GNI).
5. **Konawe Utara (Sulawesi Tenggara)**
   - **Luas Konsesi (IUP):** 39.561 Ha.
   - **Konteks:** Merupakan hulu pertambangan nikel masif (ratusan IUP beroperasi) yang menyuplai material ore ke pusat smelter di Konawe dan Morowali.
6. **Konawe (Sulawesi Tenggara)**
   - **Luas Konsesi (IUP):** 38.408 Ha.
   - **Industri Smelter / Perusahaan Utama:** PT Virtue Dragon Nickel Industry (VDNI) dan PT Obsidian Stainless Steel (OSS) di Morosi.
7. **Kolaka (Sulawesi Tenggara)**
   - **Luas Konsesi (IUP):** 29.415 Ha.
   - **Industri Smelter / Perusahaan Utama:** PT Vale Indonesia (Pomalaa), PT Aneka Tambang (Antam).

*(Catatan: Sebagian wilayah tambang besar dilaporkan sebagai Izin Lintas Batas "Morowali / Luwu Timur" dengan luas 93.265 Ha, yang menjustifikasi bahwa kedua kabupaten ini menanggung beban ekologis terbesar di pulau Sulawesi).*

Dengan rincian data (basis Hektar) di atas, penentuan 7 kabupaten ini bukanlah asumsi acak, melainkan batas riil *data-driven* di mana megaproyek ekstraktif secara konkret merampas luasan ruang hidup masyarakat.

---

## 3. Cacat Bawaan Data BPS SIMDASI & Metrik Boxplot (Hazen)
**Tanggal Dicatat:** 24 Agustus 2026

**Konteks 1 (Data Kosong/None):** Pada tabel data mentah di dashboard, banyak ditemukan nilai `None` (kosong) pada kolom `laju_pertumbuhan_yoy_pct`. Setelah divalidasi, ini bukan cacat kode, melainkan cacat bawaan dari *database* SIMDASI BPS yang sangat *patchy* (berlubang). 
- Wilayah Sultra (Kolaka, Konawe, dll) baru memiliki data mulai 2017, dan bolong di 2020.
- Wilayah Sulteng (Morowali, dll) memiliki data 2010, namun kosong panjang di 2011-2016, dan kosong lagi di 2021-2023.
- Karena Laju YoY membutuhkan pembanding tahun sebelumnya, melompatnya data (misal dari 2010 langsung ke 2017) membuat sistem merender hasil YoY tahun pertama pasca-gap menjadi `None` atau anomali artifisial (seperti -43.14% di Morowali 2017 akibat pemekaran).

**Keputusan 1:** Data `None` **DIBIARKAN** dan disaring menggunakan `.dropna()`. Narasi dashboard secara eksplisit diubah dari penggunaan Mean (Rata-rata) menjadi **Median (Nilai Tengah)**. 
**Alasan:** Median sangat *robust* (kebal) terhadap anomali ekstrem (seperti -43% di Morowali). Jika menggunakan Mean, rata-rata kawasan ekstraktif jatuh ke 1.95%, padahal jika satu titik anomali pemekaran dibuang, rata-rata aslinya meroket ke 3.10%. Median (1.98%) lebih jujur memotret realitas tanpa perlu repot mengimputasi data BPS yang berlubang.

**Konteks 2 (Bug Kuartil Plotly vs Pandas):** Sempat ditemukan *bug* di mana metrik Q1, Q3, dan Upper Fence di tabel (buatan Pandas) berbeda dengan visual tooltip di grafik (buatan Plotly), misalnya 2.93% vs 4.22%.
**Keputusan 2:** Kode tabel di `11_Demografi_Sosial.py` diubah untuk menggunakan *Numpy quantile* dengan `method='hazen'`.
**Alasan:** Secara matematis, kalkulator *default* Plotly (Exclusive/Linear) berkesesuaian persis dengan metode Hazen pada Numpy. Penyesuaian ini menjamin 100% konsistensi angka antara tabel statis dan visual interaktif.
