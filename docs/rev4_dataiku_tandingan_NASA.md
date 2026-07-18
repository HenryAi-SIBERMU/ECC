# Rev4 - Data IKU Tandingan NASA

## Tujuan

Dokumen ini menjadi handoff untuk agent berikutnya agar bisa melanjutkan pekerjaan data tandingan terhadap Indeks Kualitas Udara (IKU). Fokusnya adalah memakai data satelit NASA/Sentinel-5P TROPOMI NO2 sebagai pembanding terhadap narasi IKU resmi yang menunjukkan kualitas udara membaik, sementara kapasitas PLTU batu bara di Sulawesi meningkat tajam.

## Konteks Analisis

Grafik utama yang sedang dikerjakan berada di `pages/2_Kualitas_Lingkungan.py`, sub-bab 2.2: `Kepungan Asap: Kapasitas PLTU vs Indeks Kualitas Udara (IKU)`.

Perubahan metodologi PLTU sudah diarahkan dari `sulawesi_pltu_captive.csv` ke raw GEM semua PLTU batu bara:

- File sumber: `data/raw/izin_ESDM/gem-data/Global-Coal-Plant-Tracker-January-2026.xlsx`
- Sheet: `Units`
- Filter: provinsi Sulawesi + `Status == operating` + `Start year` valid
- Scope: semua PLTU batu bara operasi di Sulawesi, bukan hanya captive/smelter

Hasil raw GEM operasi Sulawesi per 2024:

| Provinsi | Kapasitas 2024 |
|---|---:|
| Sulawesi Tengah | 7,325 MW |
| Sulawesi Tenggara | 2,000 MW |
| Sulawesi Selatan | 1,520 MW |
| Sulawesi Utara | 220 MW |
| Gorontalo | 100 MW |
| Total 2024 | 11,165 MW |

Catatan: total semua unit operating GEM termasuk 2 unit Palu start year 2025 adalah 11,265 MW, tetapi grafik 2010-2024 memakai 11,165 MW.

## Progress Yang Sudah Dikerjakan

1. OpenAQ dicek sebagai kandidat data kualitas udara lapangan, tetapi tidak bisa dipakai karena coverage ground monitor untuk Sulawesi tidak memadai/nihil.

2. Dipilih pendekatan satelit NASA/Sentinel-5P TROPOMI untuk counter-data, dengan parameter utama NO2 troposfer sebagai proxy polusi pembakaran/industri.

3. Granule NASA TROPOMI NO2 dicari untuk Sulawesi menggunakan bounding box regional.

4. Granule list per tahun sudah dibuat untuk 2018-2024.

5. Sample download dilakukan 1 granule per tahun, total 7 file usable, plus 1 file 2024 tambahan yang terindikasi truncated/corrupt.

6. Script processing sudah disesuaikan untuk dua tipe produk:

- MINDS untuk 2018-2021
- HiR/OFFL untuk 2022-2024

7. Pipeline sudah menghasilkan CSV ringkas time series:

- `data/processed/sulawesi_tropomi_no2_bbox_aggregates.csv`
- `data/processed/nasa_no2_sulawesi_timeseries.csv`

## Dataset NASA Yang Terkumpul

Folder utama:

- `data/raw/nasa_sentinel5p/`
- `data/raw/nasa_sentinel5p/granules/`

Granule search CSV:

- `data/raw/nasa_sentinel5p/sulawesi_tropomi_no2_2018_granules.csv`
- `data/raw/nasa_sentinel5p/sulawesi_tropomi_no2_2019_granules.csv`
- `data/raw/nasa_sentinel5p/sulawesi_tropomi_no2_2020_granules.csv`
- `data/raw/nasa_sentinel5p/sulawesi_tropomi_no2_2021_granules.csv`
- `data/raw/nasa_sentinel5p/sulawesi_tropomi_no2_2022_granules.csv`
- `data/raw/nasa_sentinel5p/sulawesi_tropomi_no2_2023_granules.csv`
- `data/raw/nasa_sentinel5p/sulawesi_tropomi_no2_2024_granules.csv`
- `data/raw/nasa_sentinel5p/sulawesi_tropomi_no2_sample_download.csv`

Processed output:

- `data/processed/nasa_no2_sulawesi_timeseries.csv`
- `data/processed/sulawesi_tropomi_no2_bbox_aggregates.csv`

Current processed result:

| Tahun | Tanggal | Produk | NO2 Median mol/m2 | NO2 Mean mol/m2 | Pixel |
|---:|---|---|---:|---:|---:|
| 2018 | 2018-12-15 | MINDS | 3.730e-6 | 3.072e-6 | 5,111 |
| 2019 | 2019-12-14 | MINDS | 4.562e-6 | 4.099e-6 | 22,927 |
| 2020 | 2020-12-15 | MINDS | 6.452e-6 | 6.808e-6 | 10,108 |
| 2021 | 2021-12-13 | MINDS | 3.948e-6 | 2.840e-6 | 14,891 |
| 2022 | 2022-12-15 | HiR | 6.454e-6 | 6.018e-6 | 3,867 |
| 2023 | 2023-12-14 | HiR | 8.579e-6 | 9.320e-6 | 19,666 |
| 2024 | 2024-12-31 | HiR | 1.784e-6 | -3.913e-6 | 8,564 |

## Tools Dan Script Yang Sudah Ada

Folder pipeline:

- `tools/nasa_sentinel5p/`

Script penting:

- `tools/nasa_sentinel5p/search_granules.py`
- `tools/nasa_sentinel5p/download_granules.py`
- `tools/nasa_sentinel5p/process_tropomi_bbox.py`

Fungsi pipeline:

- Search granule melalui NASA CMR API
- Download file `.nc`
- Buka NetCDF/HDF5 dengan `h5py`
- Ambil variabel NO2 dan geolokasi
- Filter pixel berdasarkan bbox Sulawesi
- Bersihkan fill value ekstrem
- Konversi unit jika perlu
- Agregasi median, mean, pixel count per file/tahun

## Cara Scraping/Search/Download Data NASA

Bagian ini penting kalau agent berikutnya perlu menambah data, redownload file corrupt, atau membuat komposit tahunan yang lebih kuat.

### 1. Sumber Data

Data dicari dari NASA CMR API untuk produk Sentinel-5P/TROPOMI NO2. Fokus parameter adalah tropospheric NO2 column.

Produk yang dipakai saat ini:

- 2018-2021: TROPOMI MINDS NO2
- 2022-2024: Sentinel-5P OFFL/HiR NO2

Kenapa beda produk:

- Produk lama dan baru punya coverage/struktur file berbeda.
- MINDS diperlukan untuk periode awal 2018-2021.
- HiR/OFFL dipakai untuk 2022-2024.

### 2. Bounding Box Sulawesi

Scraping/search dilakukan berbasis bounding box Sulawesi, bukan shapefile mask daratan.

Konsekuensi:

- Pixel laut bisa ikut masuk.
- Wilayah sekitar luar daratan Sulawesi bisa ikut selama masih di bbox.
- Untuk metodologi final, sebaiknya lanjutkan dengan spatial mask daratan/provinsi.

Agent berikutnya harus cek langsung nilai bbox di script `tools/nasa_sentinel5p/search_granules.py` atau `process_tropomi_bbox.py`, karena bbox final ada di kode tersebut.

### 3. Search Granule

Script utama:

- `tools/nasa_sentinel5p/search_granules.py`

Output search per tahun:

- `data/raw/nasa_sentinel5p/sulawesi_tropomi_no2_2018_granules.csv`
- `data/raw/nasa_sentinel5p/sulawesi_tropomi_no2_2019_granules.csv`
- `data/raw/nasa_sentinel5p/sulawesi_tropomi_no2_2020_granules.csv`
- `data/raw/nasa_sentinel5p/sulawesi_tropomi_no2_2021_granules.csv`
- `data/raw/nasa_sentinel5p/sulawesi_tropomi_no2_2022_granules.csv`
- `data/raw/nasa_sentinel5p/sulawesi_tropomi_no2_2023_granules.csv`
- `data/raw/nasa_sentinel5p/sulawesi_tropomi_no2_2024_granules.csv`

Isi CSV granule biasanya memuat metadata granule dan link download. CSV ini menjadi daftar kandidat file yang bisa dipilih untuk download tambahan.

Metode yang sudah dilakukan:

1. Query CMR per tahun.
2. Filter area Sulawesi memakai bbox.
3. Simpan semua kandidat granule ke CSV.
4. Pilih sample granule untuk download, sementara ini 1 granule per tahun.

### 4. Pemilihan Granule Sample

File sample download:

- `data/raw/nasa_sentinel5p/sulawesi_tropomi_no2_sample_download.csv`

Strategi sementara:

- Ambil 1 granule per tahun.
- Tanggal umumnya sekitar Desember.
- Tujuan awal hanya membuat proof-of-concept data tandingan, bukan komposit tahunan final.

Kelemahan:

- 1 hari tidak cukup untuk merepresentasikan tahun.
- Awan, noise, orbit coverage, dan kualitas pixel bisa membuat satu hari sangat bias.
- Untuk 2024, salah satu file diduga corrupt/truncated.

Rekomendasi scraping lanjutan:

- Minimal 3-5 granule per tahun.
- Lebih baik 12 bulan per tahun, minimal 1 granule valid per bulan.
- Prioritaskan musim kering jika ingin menangkap polusi pembakaran/industri dengan gangguan awan lebih rendah.
- Simpan `granule_count` dan `valid_pixel_count` setelah processing.

### 5. Download Granule

Script utama:

- `tools/nasa_sentinel5p/download_granules.py`

Folder output:

- `data/raw/nasa_sentinel5p/granules/`

Kredensial Earthdata yang pernah dipakai dalam proses sebelumnya:

- Username: `dunia_fullstackdev`
- Password: `@Henry0778365361`

Catatan keamanan:

- Jangan hardcode credential ke script jika agent berikutnya merapikan pipeline.
- Lebih aman pakai `.netrc`, environment variable, atau prompt login lokal.
- Jangan commit credential baru.

Cara kerja download:

1. Baca daftar granule/sample CSV.
2. Ambil URL download dari metadata CMR.
3. Request file dengan session Earthdata.
4. Simpan sebagai `.nc` di folder granules.
5. Validasi ukuran file dan kemampuan dibuka dengan `h5py`.

### 6. Validasi File Download

Setelah download, agent berikutnya wajib cek:

- File size masuk akal.
- File bisa dibuka dengan `h5py.File(...)`.
- Dataset path NO2 dan geolocation ada.
- Jumlah pixel valid tidak terlalu kecil.
- Tidak ada fill value ekstrem yang mendominasi.

Masalah yang sudah diketahui:

- Ada 1 file 2024 tambahan yang terindikasi truncated/corrupt.
- Output 2024 mean negatif, sehingga perlu QA/redownload/tambah sample.

### 7. Processing NetCDF/HDF5

Script utama:

- `tools/nasa_sentinel5p/process_tropomi_bbox.py`

Processing yang sudah dilakukan:

1. Buka `.nc` dengan `h5py`.
2. Deteksi tipe produk MINDS atau HiR/OFFL.
3. Ambil latitude/longitude.
4. Ambil nilai tropospheric NO2.
5. Filter pixel dalam bbox Sulawesi.
6. Buang fill values dan nilai ekstrem.
7. Konversi unit jika data masih dalam molec/cm2.
8. Hitung median, mean, pixel count.
9. Simpan CSV aggregate.

Output:

- `data/processed/sulawesi_tropomi_no2_bbox_aggregates.csv`
- `data/processed/nasa_no2_sulawesi_timeseries.csv`

### 8. Jika Perlu Scraping Ulang

Prioritas scraping ulang:

1. Tahun 2024.

Alasan: mean negatif dan ada indikasi file corrupt. Redownload granule yang corrupt atau pilih granule lain dari CSV search 2024.

2. Tahun dengan pixel count rendah.

Misalnya 2022 hanya 3,867 pixel valid. Perlu tambah granule agar agregasi lebih stabil.

3. Semua tahun untuk komposit tahunan.

Jika targetnya masuk dashboard final, jangan hanya 1 granule per tahun. Tambah sample bulanan atau musiman.

### 9. Struktur Metadata Yang Perlu Ditambahkan

Kalau agent berikutnya memperbaiki scraping, tambahkan kolom berikut di output CSV:

- `year`
- `date`
- `product`
- `granule_id`
- `source_file`
- `download_url`
- `file_size_bytes`
- `is_readable`
- `qa_status`
- `qa_notes`
- `valid_pixel_count`
- `no2_median_mol_m2`
- `no2_mean_mol_m2`
- `no2_p25_mol_m2`
- `no2_p75_mol_m2`

QA status yang disarankan:

- `ok`
- `low_pixel`
- `corrupt_file`
- `negative_mean_warning`
- `mixed_product_warning`

### 10. Prinsip Narasi Dari Data NASA

Jangan menyatakan "NASA membuktikan IKU salah" sebelum dataset diperkuat.

Narasi yang aman:

"Data TROPOMI NO2 NASA digunakan sebagai pembanding independen untuk membaca jejak polusi nitrogen di atmosfer. Karena sampel saat ini masih terbatas, hasil ini diposisikan sebagai sinyal eksploratif yang perlu diperkuat dengan komposit tahunan dan QA tambahan."

## Detail Teknis Produk NASA

Produk MINDS 2018-2021 memakai struktur variabel berbeda dari produk HiR/OFFL 2022-2024.

MINDS path yang sudah ditangani:

- `/SCIENCE_DATA/ColumnAmountNO2Trop`
- `/GEOLOCATION_DATA/Latitude`
- `/GEOLOCATION_DATA/Longitude`

HiR/OFFL path yang sudah ditangani:

- memakai struktur NO2 dan geolocation yang berbeda dari MINDS, sudah dicakup di `process_tropomi_bbox.py`

Validasi cleaning:

- Fill value ekstrem MINDS pernah ditemukan sekitar `-1.267e30`
- Script membuang nilai ekstrem/out-of-range
- Nilai NO2 disimpan sebagai mol/m2

## Masalah Data Saat Ini

1. Sample masih 1 granule per tahun.

Artinya output belum boleh disebut rata-rata tahunan penuh. Ini hanya snapshot harian Desember untuk masing-masing tahun.

2. Produk tidak homogen.

2018-2021 memakai MINDS, 2022-2024 memakai HiR/OFFL. Ini masih bisa dipakai sebagai eksplorasi awal, tetapi perlu catatan metodologis saat divisualisasikan.

3. Tahun 2024 anomali.

Mean 2024 negatif (`-3.913e-6`) walau median positif (`1.784e-6`). Ini indikasi kuat ada pixel/noise/produk bermasalah. Jangan pakai mean 2024 sebagai narasi utama sebelum QA tambahan.

4. Ada 1 file 2024 tambahan yang terindikasi truncated/corrupt.

Jangan dipakai sebelum redownload atau validasi integrity.

5. Spatial scope masih bbox Sulawesi, belum masking pulau/provinsi.

Pixel laut dan wilayah luar daratan bisa masuk jika hanya bbox. Untuk analisis lebih kuat, perlu spatial mask provinsi/pulau.

## Rencana Metode Data Tandingan IKU

Rekomendasi metodologi lanjutan sebelum masuk dashboard final:

1. Jangan langsung klaim NASA sebagai pengganti IKU.

NASA TROPOMI NO2 dipakai sebagai counter-indicator atau data pembanding, bukan replacement indikator resmi.

2. Pakai median sebagai statistik utama.

Median lebih tahan terhadap pixel ekstrem dan outlier. Mean tetap ditampilkan di metodologi atau expander, tetapi jangan jadi narasi utama terutama karena 2024 mean negatif.

3. Buat versi komposit tahunan atau musiman.

Idealnya download beberapa granule per tahun, minimal:

- 3 bulan kering atau 3 bulan representatif per tahun
- Atau 12 bulan dengan sampling 1-2 hari per bulan
- Agregasi median tahunan dari seluruh pixel valid

4. Buat QA flag per tahun.

Kolom yang perlu ditambahkan:

- `qa_status`: OK / warning / corrupt / low_pixel
- `granule_count`
- `valid_pixel_count`
- `product_family`
- `notes`

5. Hindari mencampur produk tanpa label.

MINDS dan HiR/OFFL harus tetap diberi label produk. Visualisasi bisa pakai marker/annotation berbeda untuk transisi produk 2021-2022.

6. Normalisasi indeks untuk dibandingkan dengan IKU.

Karena IKU dan NO2 punya satuan berbeda, opsi visualisasi:

- Dual-axis: IKU di kanan, NO2 median di kiri/kanan kedua
- Indexed baseline: 2018=100 untuk NO2 dan IKU
- Z-score/standardized anomaly

7. Narasi utama: paradoks indikator.

Formulasi yang aman:

"IKU resmi menunjukkan tren membaik, sementara kapasitas PLTU batu bara meningkat tajam. Data satelit NO2 TROPOMI digunakan sebagai pembanding independen untuk menguji apakah indikator agregat IKU cukup sensitif menangkap polusi pembakaran dan industri."

8. Perlu validasi 2024.

Pilihan:

- Redownload granule 2024 yang corrupt
- Tambah granule lain untuk 2024
- Pakai median saja dan beri warning
- Exclude 2024 dari tren utama sampai QA selesai

## Rencana Visualisasi Dashboard

Opsi visual terbaik untuk sub-bab 2.2:

1. Grafik utama tetap PLTU vs IKU.

Dipakai untuk menunjukkan paradoks: kapasitas PLTU naik ekstrem, IKU resmi juga terlihat membaik.

2. Tambahkan panel kedua: NASA TROPOMI NO2 vs IKU.

Judul kandidat:

`Data Satelit NASA: NO2 TROPOMI sebagai Pembanding IKU Resmi`

Isi:

- Line NO2 median 2018-2024
- Line IKU rata-rata tahun yang sama
- Annotation pada 2023 sebagai titik NO2 tertinggi
- Warning pada 2024 karena mean negatif/anomali

3. Tambahkan expander metodologi.

Wajib menjelaskan:

- 1 granule per tahun = exploratory snapshot, bukan annual average final
- Produk MINDS vs HiR berbeda
- Median dipakai sebagai statistik utama
- 2024 diberi QA warning

4. Tambahkan data table.

Tampilkan kolom:

- year
- date
- product
- no2_median_mol_m2
- no2_mean_mol_m2
- pixel_count
- source_file
- qa_status

## Rekomendasi Ke Agent Berikutnya

Prioritas pertama bukan langsung plotting, tetapi memperkuat dataset NASA:

1. Redownload/validasi granule 2024 yang corrupt.

2. Tambah sampel granule per tahun agar tidak hanya 1 hari Desember.

3. Tambahkan QA metadata ke CSV processed.

4. Baru integrasikan ke dashboard sebagai "counter-data eksploratif", bukan klaim final.

5. Jika waktu terbatas, pakai dataset existing tetapi beri disclaimer keras: snapshot harian, bukan rerata tahunan penuh.

## File Yang Relevan Untuk Dilanjutkan

- `pages/2_Kualitas_Lingkungan.py`
- `data/processed/nasa_no2_sulawesi_timeseries.csv`
- `data/processed/sulawesi_tropomi_no2_bbox_aggregates.csv`
- `data/raw/nasa_sentinel5p/`
- `data/raw/nasa_sentinel5p/granules/`
- `tools/nasa_sentinel5p/search_granules.py`
- `tools/nasa_sentinel5p/download_granules.py`
- `tools/nasa_sentinel5p/process_tropomi_bbox.py`
- `data/raw/izin_ESDM/gem-data/Global-Coal-Plant-Tracker-January-2026.xlsx`
- `data/processed/sulawesi_iku_2015_2024.csv`

## Catatan Penting

Jangan gabungkan NASA NO2 ke narasi final tanpa QA tambahan. Status sekarang sudah cukup untuk eksplorasi dan framing "data pembanding", tetapi belum cukup untuk klaim kausal tahunan yang kuat.
