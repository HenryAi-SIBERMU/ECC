# Rencana Scraping Detail TanahKita (KPA)

Sesuai permintaan, kita menggunakan pendekatan yang sama seperti saat mengekstrak detail **MinerbaOne** untuk mengambil data mendalam dari **TanahKita.id**. 

Berdasarkan investigasi pada halaman detail TanahKita, berikut temuan dan strategi pendekatannya:

## Temuan Struktur Data Detail TanahKita
Dari URL detail (contoh: `https://tanahkita.id/data/konflik/detil/S2QwbDdDLWttVEk`), data tidak tersimpan dalam API JSON (seperti MinerbaOne), melainkan disisipkan dalam tabel HTML dan paragraf teks.
Data yang bisa diekstrak secara terstruktur:
- **Luas Lahan** (contoh: "0,00 Ha" atau "1250 Ha")
- **Dampak Masyarakat** (contoh: "150 Jiwa")
- **Nilai Investasi**
- **Aktor Keterlibatan** (Pemerintah, Perusahaan, Masyarakat)
- **Narasi Kasus** (Teks panjang deskripsi kronologi)

> **Terkait Kriminalisasi Warga:** TanahKita *tidak memiliki* kolom angka khusus (terstruktur) untuk "Kriminalisasi Warga" (misal: Jumlah ditangkap, luka, dll). Informasi kriminalisasi biasanya dilebur di dalam teks **Narasi Kasus**.

## Rencana Implementasi (Strategi Hibrida)

### 1. Pembuatan Script Scraper Detail (`tools/scrapling/scripts/scrape_tanahkita_detail.py`)
Pembuatan script Python baru menggunakan `requests` dan `BeautifulSoup` yang akan:
- Membaca file `data/raw/kpa_ylbhi_tanahkita/tanahkita_konflik.csv`.
- Mengambil `detail_url` untuk setiap kasus (fokus utama pada 34 kasus di Sulawesi agar cepat, namun script akan dikembangkan agar *scalable* untuk 500+ kasus nasional).
- Memperbaiki *bug* URL bawaan scraper lama (`/data/data/konflik/` menjadi `/data/konflik/`).
- Mengunjungi setiap halaman detail dan mengekstrak: `Luas`, `Dampak Masyarakat`, dan `Narasi`.

### 2. Ekstraksi Metrik "Kriminalisasi Warga" menggunakan Regex
Karena data kriminalisasi bersembunyi di dalam teks Narasi, script akan dilengkapi dengan fungsi *Regex / Keyword Matching*.
Script akan memindai teks Narasi untuk kata kunci:
- `kriminalisasi`
- `ditangkap` / `penangkapan` / `penahanan`
- `polisi` / `aparat` / `TNI`
- `kekerasan` / `luka` / `tewas` / `intimidasi`
Jika ditemukan, kolom `indikasi_kriminalisasi` akan diset `True`, dan kalimat yang mengandung kata tersebut akan diekstrak ke kolom `bukti_teks_kriminalisasi`.

### 3. Pembaruan Master Data Konflik
Hasil scraping detail akan digabungkan (di-*merge*) kembali dengan file `tanahkita_konflik.csv` yang sudah ada, sehingga tabel final akan memiliki kolom tambahan:
`luas_ha`, `dampak_jiwa`, `narasi`, `indikasi_kriminalisasi`.

---
*Dokumen ini merupakan kerangka acuan kerja untuk penyelesaian sub-task data TanahKita (Konflik dan Kriminalisasi).*
