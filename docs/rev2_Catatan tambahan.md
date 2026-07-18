# Catatan Tambahan (Revisi 2)

### Transkrip Diskusi Asli:
> **A:** Halo Hen, sama ini mumpung ingat.
> 
> **B:** Jadi ada beberapa cross step atau analisis
> 
> **A:** data yang itu penting untuk dipilah agar dia punya hasil yang lebih kritis. Misalkan di part beban kesehatan, soal korelasi langsung penurunan IKA versus lonjakan diare. Nah itu kayaknya ada nggak tau nih ini sementara nih ya ini usulannya itu di split antara yang merah sama yang abu-abu itu jadi korelasinya dibuat dua biar
> 
> **B:** terlihat disparitasnya misalkan trennya itu catatan satu
> 
> **A:** catatan kedua kayaknya coba dibuat pembanding antara
> 
> **B:** daerah sentra industri dengan non centra misalkan
> 
> **A:** untuk kasus ISPA itu kan sehingga kita benar-benar bisa melihat misalkan di tren historis kasus ISPA pneumonia di tabel beban kesehatan
> 
> **B:** itu jumlah kasus kalau misalkan atau tolonglah
> 
> **A:** dicek semua chart-chart tabel yang bagian-bagian lain
> 
> **B:** yang kita buat klasifikasi lah dari seluruh
> 
> **A:** provinsi di Sulawesi itu kita buat klasifikasi. Kalau daerah sentra itu gimana? Daerah non-sentra itu gimana? Sehingga tidak diindeks semua. Gimana ya maksudnya?
> 
> **B:** Biar nggak diindeksasi semua, tapi kita split, sehingga kita bisa memberi perbandingan dari daerah
> 
> **A:** yang sentra dan non-sentra.
> 
> **B:** Terus catatan lagi begini, apakah kamu memperhatikan potensi double accounting terhadap data yang diolah?
> 
> **A:** Kan kamu tuh ngambil beberapa data itu kan dari beberapa report tuh. Ada report KPA, ada report AR, ada report lembaga A, B, C, D misalkan. sangat potensial kan data ABCD yang diambil KPA yang diambil ini samplingnya

---

### Rangkuman Ekstraksi Poin:

1. **Beban Kesehatan (Korelasi)**
   - Pisah (split) korelasi IKA vs Lonjakan Diare menjadi dua garis pembanding (merah vs abu-abu) agar disparitas trennya terlihat lebih jelas dan kritis.

2. **Sentra vs Non-Sentra Industri**
   - Buat klasifikasi pembagian "Daerah Sentra Industri" dan "Daerah Non-Sentra".
   - Terapkan pemilahan (split) ini di berbagai chart (khususnya tren historis kasus ISPA/Pneumonia di tabel beban kesehatan) agar perbandingan dampak ekstraktifnya terindeks dengan jelas, bukan digabung secara provinsial.

3. **Potensi *Double Accounting***
   - Waspadai perhitungan ganda (*double accounting*) saat menggabungkan laporan dari multi-sumber (KPA, Annual Report, NGO A, B, C, D).
   - Pastikan bahwa sampling data yang diambil tidak mencatat kasus atau *event* berulang yang sama dari lembaga yang berbeda.

---

## 🎯 Roadmap Eksekusi Revisi 2 (Penajaman Analisis)

Berdasarkan catatan di atas, berikut adalah *action items* yang dipecah ke dalam 3 fase eksekusi krusial:

### Fase 1: Pemisahan (*Split*) Korelasi Ekologis & Kesehatan
* ⏳ **STATUS:** **PENDING**
* **Log Eksekusi:** Belum dimulai.
* 🎯 **TARGET:** Mempertegas visualisasi *causality* antara rusaknya IKA dan lonjakan penyakit.
* 📋 **TUGAS:** 
    *   Mengubah *scatter plot/line chart* korelasi IKA vs Diare di `pages/3_Beban_Kesehatan.py` menjadi sistem dua *cluster* (Garis Merah untuk daerah IKA buruk, Garis Abu-abu untuk IKA baik).
    *   Memastikan UI/UX Streamlit bisa secara dinamis menyorot perbandingan tajam antar dua kelompok ini.

### Fase 2: Klasifikasi "Daerah Sentra" vs "Non-Sentra"
* ⏳ **STATUS:** **PENDING**
* **Log Eksekusi:** Belum dimulai.
* 🎯 **TARGET:** Membuktikan secara empiris bahwa wilayah episentrum tambang menanggung beban ISPA/Pneumonia tertinggi.
* 📋 **TUGAS:** 
    *   Menyusun kamus/daftar kabupaten/kota mana saja di Sulawesi & Malut yang masuk kategori "Sentra Industri/Ekstraktif" (misal: Morowali, Halmahera, Konawe).
    *   Mengaplikasikan fungsi *grouping* (Sentra vs Non-Sentra) pada pembacaan *dataset* ISPA.
    *   Membuat grafik *line/bar chart* perbandingan tren ISPA antara Sentra vs Non-Sentra.

### Fase 3: Algoritma Mitigasi *Double Accounting*
* ⏳ **STATUS:** **PENDING**
* **Log Eksekusi:** Belum dimulai.
* 🎯 **TARGET:** Menjaga integritas dan keabsahan angka konflik dari tuduhan manipulasi/duplikasi.
* 📋 **TUGAS:** 
    *   Merumuskan algoritma *deduplication* di Pandas berbasis kunci unik gabungan (`[Tahun + Kabupaten + Sektor Terlibat]`).
    *   Membersihkan *dataset* agregat (Master Data Konflik & Kriminalisasi) dari baris-baris identik yang dilaporkan oleh lembaga berbeda sebelum di-render ke Dashboard.

### Fase 4: Halaman *Overview* Temuan (TL;DR)
* ⏳ **STATUS:** **PENDING**
* **Log Eksekusi:** Belum dimulai.
* 🎯 **TARGET:** Memberikan rangkuman komprehensif bagi pembaca eksekutif (TL;DR) mengenai inti sari seluruh riset.
* 📋 **TUGAS:** 
    *   Membuat satu halaman baru khusus ("Overview Temuan").
    *   Menyusun ringkasan singkat (TL;DR) untuk semua *page*, bab, dan sub-bab yang ada di dashboard ke dalam halaman tersebut agar mudah dibaca sekilas.

### Fase 5: *Dropdown* Metodologi & Dataset di Setiap Sub-Bab
* ⏳ **STATUS:** **PENDING**
* **Log Eksekusi:** Belum dimulai.
* 🎯 **TARGET:** Meningkatkan transparansi riset dengan menjelaskan metodologi dan sumber data yang spesifik untuk tiap visualisasi/analisis.
* 📋 **TUGAS:** 
    *   Mengubah *tag* metode (yang biasanya berupa *badge* biru/hijau) di setiap sub-bab menjadi elemen *dropdown* (seperti `st.expander` atau pop-over).
    *   Mengisi *dropdown* tersebut dengan deskripsi detail mengenai metode apa yang digunakan dan dataset/sumber data apa saja yang dipakai.
