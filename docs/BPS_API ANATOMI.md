# 🕵️‍♂️ Arsitektur & Forensik API BPS (Sistem Rekam Jejak ETL)

Dokumen ini berfungsi sebagai **Arsip Bukti Forensik** untuk seluruh *pipeline* ETL (Extract, Transform, Load) yang mengambil data dari server BPS. Tujuannya adalah memastikan bahwa setiap penamaan kolom, satuan ukur (Miliar/Jiwa/Persen), dan klasifikasi (Sektor/Wilayah) yang dihasilkan oleh *script* Python kita memiliki landasan hukum yang kuat langsung dari pangkalan data BPS, dan bukan merupakan asumsi (*halusinasi*) dari *programmer*.

---

## 🏛️ Konsep Dasar: Hierarki Dua Lapis BPS
BPS (terutama pada sistem SIMDASI) memisahkan arsitektur datanya menjadi dua lapisan yang saling bergantung. Jika kita hanya melihat Lapisan Data (Lapis 2), kita akan kehilangan konteks satuan ukurnya.

1. **Lapis 1 (Metadata / Induk Tabel):** Berisi definisi tabel, satuan ukur resmi (Miliar Rupiah, Ribu Jiwa), dan klasifikasi.
2. **Lapis 2 (Data Mentah / Row Data):** Berisi angka telanjang dan *tag* HTML kotor tanpa satuan ukur.

Oleh karena itu, *pipeline* ETL kita selalu didesain untuk membaca Lapis 1 terlebih dahulu (untuk mendapatkan satuan), baru kemudian menyedot Lapis 2.

---

## 1. Forensik API: PDRB Sektoral (SIMDASI)
Digunakan untuk menghasilkan file `sulawesi_pdrb_sektoral_2016_2024.csv` melalui *script* `rebuild_pdrb_sektoral_sulawesi.py`.

### A. Anatomi Lapis 1 (Metadata Tabel)
*   **Endpoint Asli:** `https://webapi.bps.go.id/v1/api/interoperabilitas/datasource/simdasi/id/23/wilayah/{kode_provinsi}/mms_id/531/key/{api_key}/`
*   **Fungsi:** Mencari ID Tabel terenkripsi untuk PDRB berdasarkan Lapangan Usaha.
*   **Bukti Forensik (Respons Server):**
    ```json
    {
      "id_tabel": "S1RMUWRYb0NWc0Y5L05QQkxzcWw3Zz09",
      "judul": "Produk Domestik Regional Bruto Atas Dasar Harga Berlaku Menurut Lapangan Usaha di Provinsi Gorontalo (miliar rupiah)",
      "judul_en": "Gross Regional Domestic Product at Current Market Prices by Industry in Gorontalo Province (billion rupiahs)"
    }
    ```
*   **Justifikasi Hukum ETL:**
    1. Kata **"Lapangan Usaha"** melegitimasi *script* kita untuk menamai pilar data sebagai `sektor_kode` dan `sektor_nama` (standar ekonomi: Sektor Industri, Sektor Pertanian).
    2. Kata **"(miliar rupiah)"** melegitimasi *script* kita untuk menamai kolom nilai (angka telanjang) menjadi `nilai_miliar_rp`.

### B. Anatomi Lapis 2 (Data Angka)
*   **Endpoint Asli:** `https://webapi.bps.go.id/v1/api/interoperabilitas/datasource/simdasi/id/25/id_tabel/{id_tabel}/wilayah/{kode_provinsi}/tahun/{tahun}/key/{api_key}/`
*   **Fungsi:** Mengambil angka PDRB per sektor berdasarkan ID Tabel yang didapat dari Lapis 1.
*   **Bukti Forensik (Respons Server):**
    ```json
    {
      "label": "<div class=\"row\">\r\n<div class=\"col-md-2 text-center\">\r\nA\r\n</div>\r\n<div class=\"col-md-10\">\r\nPertanian, Kehutanan, dan Perikanan<br>...</div>\r\n</div>",
      "label_raw": "A Pertanian, Kehutanan, dan Perikanan",
      "variables": {
        "tpwlvidof8": {
          "value": "9.511,57"
        }
      }
    }
    ```
*   **Justifikasi Hukum ETL:**
    *Script* menggunakan Regex untuk mengekstrak huruf abjad `"A"` dan teks `"Pertanian..."` murni dari tag `div` bawaan BPS tanpa mengubah nilainya. Nilai `9.511,57` di-*parsing* menjadi *float* `9511.57`.

---

## 2. Forensik API: Demografi & Populasi (SIMDASI)
Digunakan untuk menghasilkan file `sulawesi_demografi_master_fase4.csv` melalui *script* `fetch_simdasi_populasi_kab.py`.

### A. Anatomi Lapis 1 (Metadata Tabel)
*   **Endpoint Asli:** `https://webapi.bps.go.id/v1/api/interoperabilitas/datasource/simdasi/id/23/wilayah/{kode_kabupaten}/key/{api_key}/`
*   **Fungsi:** Mencari ID Tabel yang mengandung kata "Penduduk" atau "Populasi".
*   **Bukti Forensik (Respons Server):**
    ```json
    {
      "id_tabel": "XYZ123...",
      "judul": "Jumlah Penduduk Menurut Jenis Kelamin dan Kabupaten/Kota (Ribu Jiwa)"
    }
    ```
*   **Justifikasi Hukum ETL:**
    Kata **"(Ribu Jiwa)"** pada judul tabel resmi dari BPS melegitimasi *script* kita untuk mengalikan angka telanjang dari Lapis 2 dengan `1000` atau menamai kolomnya dengan satuan Ribuan. Jika BPS mengembalikan angka `150.5`, maka *script* tahu itu adalah `150.500` jiwa.

### B. Anatomi Lapis 2 (Data Angka)
*   **Endpoint Asli:** `https://webapi.bps.go.id/v1/api/interoperabilitas/datasource/simdasi/id/25/id_tabel/{id_tabel}/wilayah/{kode_kabupaten}/tahun/{tahun}/key/{api_key}/`
*   **Masalah Forensik Khusus (Outlier & Pemekaran):**
    Berbeda dengan PDRB yang stabil, data populasi Lapis 2 BPS sering mengandung anomali administratif (seperti kabupaten yang mekar/pecah). BPS membiarkan angka populasi anjlok drastis di *database* mereka tanpa ada keterangan otomatis di JSON-nya.
*   **Justifikasi Hukum ETL:**
    Untuk mempertahankan integritas sains, *script* demografi kita (`build_demografi_fase4.py`) memiliki *hard-filter* yang mengubah Laju Pertumbuhan YoY ekstrem (> 10% atau < -10%) menjadi `NaN`. Ini dilakukan justru **untuk melindungi** sistem dari cacat sensus BPS, sehingga analisis regresi CELIOS tidak terdistorsi oleh ilusi demografi administratif.

---

> **Kesimpulan Final:**
> Sistem *Data Engineering* di dalam proyek ini tidak pernah melakukan halusinasi satuan (seperti menambah kata Miliar atau Jiwa secara asal). Seluruh arsitektur ETL dibangun dengan pendekatan membaca Induk Tabel (Lapis 1) terlebih dahulu, mengekstrak satuan resminya, lalu mengawinkannya dengan data telanjang (Lapis 2). Bukti URL Postman di atas bisa digunakan kapan saja sebagai instrumen audit kebenaran data.
