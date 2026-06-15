# Rencana Ekstraksi Portal Open Data Regional Sulawesi (Satu Data)

Dokumen ini merinci rencana teknis (*Implementation Plan*) untuk mengekstraksi data Kualitas Air (IKA), Kualitas Udara (IKU/PM2.5), dan variabel lingkungan hidup lainnya langsung dari "hulu" yaitu **Portal Open Data (Satu Data)** yang dikelola oleh masing-masing pemerintah provinsi di wilayah Sulawesi.

Pendekatan ini dipilih untuk mem-*bypass* hambatan akses (*login wall*) pada portal nasional KemenLH (SITALA & SIPSN), serta mengatasi keterbatasan data tahun lama pada API BPS.

## Pemetaan Portal & Mesin Scraping

Setiap provinsi menggunakan platform *Satu Data* yang berbeda-beda. Berikut adalah tabel kompilasi alamat portal dan metode ekstraksi yang akan kita gunakan:

| Provinsi | URL Portal Open Data | Software/Mesin | Metode Ekstraksi (Scraping) |
| :--- | :--- | :--- | :--- |
| **Sulawesi Utara** | `opendata.sulutprov.go.id` | CKAN | Menggunakan API standar CKAN (`/api/3/action/package_search`). Sangat mudah diotomatisasi. |
| **Sulawesi Barat** | `opendata.sulbarprov.go.id` | Custom / DKAN | Menggunakan API *custom* atau *HTML Parsing* (BeautifulSoup). |
| **Sulawesi Selatan** | `satudata.sulselprov.go.id` | Custom Web | *HTML Parsing* (BeautifulSoup / LXML). Mencari elemen tabel atau link `.csv`/`.xlsx`. |
| **Sulawesi Tengah** | `satudata.sultengprov.go.id` | Custom Web | *HTML Parsing* (BeautifulSoup / LXML). |
| **Sulawesi Tenggara** | `simdata.sultraprov.go.id` | SIMDATA (Custom) | *HTML Parsing* (BeautifulSoup / LXML). |
| **Gorontalo** | `data.gorontaloprov.go.id` | CKAN / Custom | Cek ketersediaan API, jika gagal gunakan *HTML Parsing*. |

## Rencana Eksekusi (Tahapan)

1. **Fase 1: Ekstraksi API CKAN (Sulawesi Utara & API-based)**
   - Fokus: Scraping 23 dataset "Kualitas Air" yang sudah terkonfirmasi ada di Sulut.
   - Script: `scripts/scrape_opendata_api.py` (Menarik JSON *metadata* dan *download URL* file CSV/XLSX-nya).
   - *Output*: Folder `data/raw/sulut_kualitas_air/`.

2. **Fase 2: Ekstraksi HTML (Sulsel, Sulteng, Sultra, Sulbar)**
   - Fokus: Mencari halaman pencarian (*Search Page*) pada masing-masing portal dengan *keyword* "Kualitas Air" dan "Udara".
   - Script: `scripts/scrape_opendata_html.py` menggunakan `requests` dan `BeautifulSoup`.
   - Proses: Menyimulasikan HTTP GET ke URL *search*, menemukan tag `<a>` untuk dataset, lalu mengunduh lampirannya.

3. **Fase 3: Konsolidasi & Pembersihan (Data Wrangling)**
   - Menggabungkan data IKA/IKU dari ke-6 provinsi menjadi satu tabel master (*Master Table*) `kualitas_lingkungan_sulawesi.csv` yang terstandardisasi per kabupaten/kota.

## Open Questions

> [!IMPORTANT]
> 1. Karena Sulut sudah terkonfirmasi memiliki 23 dataset via API, apakah kita eksekusi Sulut terlebih dahulu sebagai *Proof of Concept* (PoC)?
> 2. Data *raw* yang diunduh (biasanya berupa puluhan file `.csv` atau `.xlsx`) akan saya simpan di dalam direktori `data/raw/opendata_provinsi/`. Apakah lokasi ini sesuai dengan struktur proyek Mas?
