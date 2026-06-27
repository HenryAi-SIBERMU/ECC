# Rev1: Scraping/Crawl Data Profil Kesehatan Provinsi

**Tanggal:** 26 Juni 2026  
**Target Folder:** `data/raw/profil kesehatan provinsi_kemenkes/`  
**Target Provinsi:** Sulsel, Sultra, Sulbar, Gorontalo, Sulteng, Sulut  
**Target Tahun:** 2018-2024 (atau data terakhir yang tersedia)

---

## 🔥 UPDATE OSINT ROUND 2 (27 Juni 2026)

**Pendekatan:** Validasi ulang semua asumsi docs lama via Internet Archive (Wayback) CDX API + cross-check metadata publik Scribd. Hasil: 2 dari 5 dokumen "tertahan Scribd" **ternyata tersedia gratis** di cache Wayback, dan mapping link Scribd docs lama punya **kesalahan label tahun**.

### ✅ Didapatkan (download resmi, valid, gratis)

| # | Dokumen | Sumber Sebenarnya | Hasil Validasi |
|---|---------|-------------------|----------------|
| 1 | **Profil_Kesehatan_Sulsel_2020.pdf** | Wayback Machine snapshot `20240519090112if_` dari `apidinkes.sulselprov.go.id/repo/dinkes-PROFIL_2020_FINISH1.pdf` | ✅ 3,606,061 bytes (3.5 MB), `%PDF-1.7`, **295 halaman**, cover: "KATA SAMBUTAN KEPALA DINAS KESEHATAN PROVINSI SULAWESI SELATAN" |
| 2 | **Profil_Kesehatan_Sulsel_2021.pdf** | Wayback Machine snapshot `20240602234329if_` dari `apidinkes.sulselprov.go.id/repo/dinkes-PROFIL_20211.pdf` | ✅ 13,215,996 bytes (12.6 MB), `%PDF-1.4`, **333 halaman** |

**Koreksi root cause:** Docs lama menyatakan "Wayback tidak pernah cache file 2019+" — **SALAH**. Wayback meng-cache file 2020 dan 2021 pada April–Juni 2024 (lihat digest `6PWZU5LAJX5IZEMTWWM5IRCQYKTHBGFD` dan `FMZK7AM4CPZUYJR4DJZIJY5EZQ7MPQAY`). Bug adalah query CDX docs lama tidak pakai filter `statuscode:200` + `mimetype:application/pdf`, sehingga snapshot valid tidak terlihat.

### ⚠️ Tetap hanya di Scribd (metadata publik tersimpan di `_scribd_metadata/`)

| # | Dokumen | Scribd ID | Halaman | Catatan |
|---|---------|-----------|---------|---------|
| 3 | Profil Kesehatan Sulsel 2022 | 723843377 | **338** | Link docs LAMA benar; ini Profil Kesehatan Tahun 2022 asli |
| 4 | Profil Kesehatan Sulsel 2023 | 863344834 | **266** | ⚠️ Docs LAMA salah label sebagai "Sulsel 2022 versi 2". Judul asli Scribd: "Dinkes Profil **2023** Lengkap Compressed 2" → ini adalah **Sulsel 2023** |
| 5 | Profil Kesehatan Sultra 2021 | 651042131 | **296** | Link docs LAMA benar |

### ❌ Link docs LAMA yang SALAH / bukan Profil Kesehatan

| Scribd ID | Label docs lama | **Kenyataan** |
|-----------|-----------------|---------------|
| 744330313 | "Sulsel 2023" | ❌ **BUKAN Profil Kesehatan.** Judul asli: "draft Daftar_Informasi_Publik_Dinkes sulsel_2024", hanya **4 halaman**. Ini dokumen BIP/DIP (Daftar Informasi Publik), bukan Profil Kesehatan. Link ini harus dihapus dari dokumen referensi. |

### Status target dokumen yang diminta user (5 link Scribd)

| Link yang diminta | Status real |
|-------------------|-------------|
| Sulsel 2020 → 544140512 | ✅ Lebih baik ambil dari Wayback (sudah didapat) — link Scribd tidak lagi relevan |
| Sulsel 2021 → 625619811 | ✅ Lebih baik ambil dari Wayback (sudah didapat) |
| Sulsel 2022 → 723843377 | ⚠️ Tetap di Scribd (338 hal), butuh akun untuk download PDF |
| Sulsel 2023 → 744330313 | ❌ **Link SALAH** — ini DIP 4 hal, bukan Profil Kesehatan. Ganti ke 863344834 |
| Sultra 2021 → 651042131 | ⚠️ Tetap di Scribd (296 hal), butuh akun |

### Kesimpulan

- **2/5 dokumen berhasil diambil gratis** lewat re-query Wayback Machine yang benar (docs lama keliru menyimpulkan sumber ini mati).
- **3/5 dokumen** memang hanya tersedia di Scribd; tidak ada mirror publik gratis di Wayback, Internet Archive, Google Scholar, repository Kemenkes, SimData, atau portal Dinkes mana pun yang dapat dijangkau.
- **1 link user (Sulsel 2023) salah ketik di list** — bukan Profil Kesehatan; versi asli Sulsel 2023 ada di Scribd ID 863344834.

---

## Status Akhir (sebelum OSINT Round 2)

| Provinsi | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 |
|----------|------|------|------|------|------|------|------|------|------|------|
| **Gorontalo** | - | - | ⚠️ RAR | ⚠️ RAR | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Sulteng** | - | - | - | - | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Sulsel** | ✅ | ✅ | ✅ | ✅ | ❌ | [📄 Scribd](#link-scribd) | [📄 Scribd](#link-scribd) | [📄 Scribd](#link-scribd) | [📄 Scribd](#link-scribd) | ❌ |
| **Sulut** | - | - | - | - | - | - | - | - | ⚠️* | - |
| **Sultra** | - | - | - | - | ❌ | ❌ | [📄 Scribd](#link-scribd) | ❌ | ❌ | ❌ |
| **Sulbar** | - | - | - | - | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

**Keterangan:**
- ✅ = Berhasil download PDF
- ⚠️ = Ada tapi bukan PDF utuh (RAR / jenis beda)
- ⚠️* = BPS Statistik Kesehatan (bukan Profil Kesehatan Dinkes)
- [📄 Scribd](#link-scribd) = Tersedia di Scribd (butuh subscription $11.99/bulan untuk download)
- ❌ = Gagal total (tidak ada di sumber manapun)
- `-` = Tidak perlu (di luar range tahun target)

---

## File yang Sudah Ada di Folder

### PDF Profil Kesehatan (19 file)

| # | Filename | Size | Provinsi | Tahun | Sumber |
|---|----------|------|----------|-------|--------|
| 1 | Profil_Kesehatan_Gorontalo_2019.pdf | 4.66 MB | Gorontalo | 2019 | Google Drive |
| 2 | Profil_Kesehatan_Gorontalo_2020.pdf | 5.33 MB | Gorontalo | 2020 | Google Drive |
| 3 | Profil_Kesehatan_Gorontalo_2021.pdf | 7.53 MB | Gorontalo | 2021 | PPK Kemendagri |
| 4 | Profil_Kesehatan_Gorontalo_2022.pdf | 5.96 MB | Gorontalo | 2022 | PPK Kemendagri |
| 5 | Profil_Kesehatan_Gorontalo_2023.pdf | 3.46 MB | Gorontalo | 2023 | Google Drive |
| 6 | Profil_Kesehatan_Gorontalo_2024.pdf | 5.29 MB | Gorontalo | 2024 | Google Drive |
| 7 | Profil_Kesehatan_Sulsel_2015.pdf | 7.15 MB | Sulsel | 2015 | Wayback Machine |
| 8 | Profil_Kesehatan_Sulsel_2016.pdf | 2.19 MB | Sulsel | 2016 | Wayback Machine |
| 9 | Profil_Kesehatan_Sulsel_2017.pdf | 2.25 MB | Sulsel | 2017 | Wayback Machine |
| 10 | Profil_Kesehatan_Sulsel_2018.pdf | 2.28 MB | Sulsel | 2018 | Wayback Machine |
| 11 | Profil_Kesehatan_Sulteng_2019.pdf | 14.17 MB | Sulteng | 2019 | Sudah ada |
| 12 | Profil_Kesehatan_Sulteng_2020.pdf | 17.16 MB | Sulteng | 2020 | Sudah ada |
| 13 | Profil_Kesehatan_Sulteng_2021.pdf | 15.64 MB | Sulteng | 2021 | Sudah ada |
| 14 | Profil_Kesehatan_Sulteng_2022.pdf | 9.92 MB | Sulteng | 2022 | Sudah ada |
| 15 | Profil_Kesehatan_Sulteng_2023.pdf | 15.14 MB | Sulteng | 2023 | Sudah ada |
| 16 | Profil_Kesehatan_Sulteng_2024.pdf | 11.03 MB | Sulteng | 2024 | Sudah ada |
| 17 | Statistik_Kesehatan_Sulut_2023.pdf | 3.23 MB | Sulut | 2023 | BPS (jenis beda) |

### RAR (2 file - perlu diekstrak/merged)

| # | Filename | Size | Provinsi | Tahun | Sumber |
|---|----------|------|----------|-------|--------|
| 18 | Gorontalo_2017.rar | 4.04 MB | Gorontalo | 2017 | dinkes.gorontaloprov.go.id |
| 19 | Gorontalo_2018.rar | 16.23 MB | Gorontalo | 2018 | dinkes.gorontaloprov.go.id |

### File Lainnya (perlu dibersihkan)

| # | Filename | Size | Keterangan |
|---|----------|------|------------|
| - | extracted_gorontalo/ | - | Folder hasil ekstrak RAR 2017 |
| - | extracted_Gorontalo_2018/ | - | Folder hasil ekstrak RAR 2018 |
| - | sample_parsing_2019.txt | 4.7 KB | File sementara parsing data |
| - | sample_parsing_2022_rabies_filariasis.txt | 8.2 KB | File sementara parsing data |

**Total: 19 file PDF + 2 RAR + 4 file lain = 25 item, ~130 MB (PDF+RAR saja)**

---

## Status per Provinsi

### 1. Gorontalo ✅ SELESAI

| Tahun | Status | Sumber | File |
|-------|--------|--------|------|
| 2017 | ⚠️ RAR | dinkes.gorontaloprov.go.id | Gorontalo_2017.rar (4.04 MB) |
| 2018 | ⚠️ RAR | dinkes.gorontaloprov.go.id | Gorontalo_2018.rar (16.23 MB) |
| 2019 | ✅ PDF | Google Drive | Profil_Kesehatan_Gorontalo_2019.pdf |
| 2020 | ✅ PDF | Google Drive | Profil_Kesehatan_Gorontalo_2020.pdf |
| 2021 | ✅ PDF | PPK Kemendagri | Profil_Kesehatan_Gorontalo_2021.pdf |
| 2022 | ✅ PDF | PPK Kemendagri | Profil_Kesehatan_Gorontalo_2022.pdf |
| 2023 | ✅ PDF | Google Drive | Profil_Kesehatan_Gorontalo_2023.pdf |
| 2024 | ✅ PDF | Google Drive | Profil_Kesehatan_Gorontalo_2024.pdf |

**Catatan:**
- RAR 2017 berisi: Cover.pdf, KATA PENGANTAR.pdf, NARASI.pdf, LAMPIRAN.xls (bukan 1 PDF utuh)
- RAR 2018 berisi: file terpisah juga (perlu dicek isi extracted_Gorontalo_2018/)
- Google Drive timeout untuk 2021-2022, fallback ke PPK Kemendagri

### 2. Sulteng ✅ SELESAI

| Tahun | Status | Sumber |
|-------|--------|--------|
| 2019-2024 | ✅ PDF | Sudah ada di folder |

### 3. Sulsel ⚠️ SEBAGIAN

| Tahun | Status | Sumber | Keterangan |
|-------|--------|--------|------------|
| 2015 | ✅ PDF | Wayback Machine | Bonus (di luar target) |
| 2016 | ✅ PDF | Wayback Machine | Bonus (di luar target) |
| 2017 | ✅ PDF | Wayback Machine | Bonus (di luar target) |
| 2018 | ✅ PDF | Wayback Machine | Bonus (di luar target) |
| 2019 | ❌ | - | Tidak ditemukan dimanapun |
| 2020 | 📄 Scribd | Scribd | Butuh subscription |
| 2021 | 📄 Scribd | Scribd | Butuh subscription |
| 2022 | 📄 Scribd | Scribd | Butuh subscription |
| 2023 | 📄 Scribd | Scribd | Butuh subscription |
| 2024 | ❌ | - | Tidak ditemukan dimanapun |

**Root Cause:**
- `apidinkes.sulselprov.go.id` DNS tidak resolve dari mesin lokal
- Wayback Machine tidak pernah cache file 2019+ (CDX API return 0 snapshots)
- URL pattern lama: `https://apidinkes.sulselprov.go.id/repo/dinkes-PK-[YEAR].pdf`
- URL pattern 2020: `dinkes-PROFIL_2020_FINISH1.pdf`
- URL pattern 2021: `dinkes-PROFIL_20211.pdf`

### 4. Sulut ❌ BELUM SELESAI

| Tahun | Status | Sumber | Keterangan |
|-------|--------|--------|------------|
| 2023 | ⚠️* | BPS | Statistik Kesehatan (bukan Profil Kesehatan) |
| Lainnya | ❌ | - | Tidak ditemukan |

**Root Cause:**
- Dinkes Sulut punya halaman "Profil Kesehatan Download" tapi kosong
- BPS hanya punya "Statistik Kesehatan" (jenis publikasi berbeda)

### 5. Sultra ❌ BELUM SELESAI

| Tahun | Status | Sumber | Keterangan |
|-------|--------|--------|------------|
| 2019 | ❌ | - | Tidak ditemukan dimanapun |
| 2020 | ❌ | - | Tidak ditemukan dimanapun |
| 2021 | 📄 Scribd | Scribd | Butuh subscription |
| 2022 | ❌ | - | Tidak ditemukan dimanapun |
| 2023 | ❌ | - | Tidak ditemukan dimanapun |
| 2024 | ❌ | - | Tidak ditemukan dimanapun |

**Root Cause:**
- `dinkes.sultraprov.go.id` return HTTP 500 terus
- Tidak ada mirror/backup
- Tidak ada cached version di Wayback/Google Cache
- PPID Provinsi tidak punya dokumen ini
- SimData Sultra (`simdata.sultraprov.go.id`) accessible tapi tidak ada download link

### 6. Sulbar ❌ BELUM SELESAI

| Tahun | Status | Sumber | Keterangan |
|-------|--------|--------|------------|
| 2019-2024 | ❌ | - | Tidak ditemukan dimanapun |

**Root Cause:**
- `dinkes.sulbarprov.go.id` semua subdomain reject SSL/TLS handshake
- Kemungkinan TLS version mismatch dari Windows 10
- Tidak ada cached version di manapun
- PPID Provinsi (`e-ppid.sulbarprov.go.id`) DNS tidak resolve
- BPS Sulbar 403 Forbidden

---

## Metode yang Sudah Dicoba

| # | Metode | Hasil | Keterangan |
|---|--------|-------|------------|
| 1 | Direct download dinkes.*.go.id | ❌ | DNS mati / SSL error / 500 |
| 2 | Wayback Machine | ⚠️ | Hanya berhasil untuk Sulsel 2015-2018 |
| 3 | PPK Kemendagri | ⚠️ | Hanya ada Gorontalo 2021-2022 |
| 4 | Google Drive search | ⚠️ | Hanya ada Gorontalo 2019, 2020, 2023, 2024 |
| 5 | BPS (bps.go.id) | ⚠️ | Publikasi "Dalam Angka" / "Statistik Kesehatan", bukan Profil Kesehatan |
| 6 | PPID Provinsi | ❌ | Tidak ada Profil Kesehatan di dokumen |
| 7 | Satu Data (data.go.id) | ❌ | Tidak ada dataset Profil Kesehatan |
| 8 | Satusehat Kemkes | ❌ | Hanya data nasional, bukan provinsi |
| 9 | Google Dorking | ⚠️ | Tidak menemukan URL download gratis |
| 10 | Scribd | ⚠️ | File ada tapi berbayar ($11.99/bulan) |
| 11 | Academia.edu | ❌ | Hanya Sulsel lama (2005-2009) |
| 12 | portaldinkesv2.teknologi40.com | ❌ | Connection closed / timeout |
| 13 | mirror/alternatif dinkes | ❌ | Tidak ada yang aktif |
| 14 | SimData Provinsi | ❌ | Tidak ada Profil Kesehatan |
| 15 | GitHub/Code Repository | ❌ | Tidak ada repo yang relevan |

---

## Link Scribd (Butuh Subscription)

| # | Provinsi | Tahun | Link | Halaman | Status |
|---|----------|-------|------|---------|--------|
| 1 | Sulsel | 2020 | https://id.scribd.com/document/544140512/Profil-2020-Finish1 | - | Tersedia |
| 2 | Sulsel | 2021 | https://id.scribd.com/document/625619811/Dinkes-PROFIL-20211 | - | Tersedia |
| 3 | Sulsel | 2022 | https://id.scribd.com/document/723843377/Profil-Kesehatan-Tahun-2022 | 338 | Tersedia |
| 4 | Sulsel | 2022 | https://id.scribd.com/document/863344834/Dinkes-Profil-2023-Lengkap-Compressed-2 | 266 | Tersedia |
| 5 | Sulsel | 2023 | https://id.scribd.com/document/744330313/draft-Daftar-Informasi-Publik-Dinkes-sulsel-2024 | - | Tersedia |
| 6 | Sultra | 2021 | https://www.scribd.com/document/651042131/profil-kesehatan-sultra-2021 | - | Tersedia |

**Catatan:**
- Sulsel 2022 punya 2 versi di Scribd (perlu dicek mana yang benar)
- Scribd free trial 7 hari tersedia, bisa cancel sebelum charge $11.99
- Sulsel 2019 & 2024, Sultra 2019-2020 & 2022-2024, Sulbar SEMUA TAHUN = **tidak ditemukan di Scribd manapun**

---

## Google Drive IDs (Gorontalo)

| Tahun | Google Drive ID | Status |
|-------|-----------------|--------|
| 2019 | 1dLpI1JjBTIAdzpiS65l7m5s0pPSSrJd6 | ✅ Downloaded |
| 2020 | 1lIgcOmcscL1wF3ZluWrfHT0I3fZG0KDS | ✅ Downloaded |
| 2023 | 15ZAv7RML1gM9OhSifJX6aW-_SVJavmIl | ✅ Downloaded |
| 2024 | 1K2BuvSEvxBVop272Wc79p5890yi00Fkv | ✅ Downloaded |

---

## PPK Kemendagri Links (Gorontalo)

| Tahun | URL | Status |
|-------|-----|--------|
| 2021 | https://ppid.kemendagri.go.id/storage/dokumen/hueF2kGNFAlSXe5Ua74AUfSfp0QJTketairvgNUl.pdf | ✅ Downloaded |
| 2022 | https://ppid.kemendagri.go.id/storage/dokumen/cuM4GUKKQOO91rXjCrMt4eVciObtpd6AgwI0emdt.pdf | ✅ Downloaded |

---

## Ringkasan Teknis

### Kenapa Gagal per Provinsi

| Provinsi | Root Cause | Solusi |
|----------|-----------|--------|
| **Sulsel 2019-2024** | `apidinkes.sulselprov.go.id` DNS tidak resolve. Wayback tidak cache. | Scribd (2020-2023) / Hubungi Dinkes (2019, 2024) |
| **Sultra 2019-2024** | `dinkes.sultraprov.go.id` HTTP 500. Tidak ada mirror/cache. | Scribd (2021) / Hubungi Dinkes (semua tahun) |
| **Sulbar 2019-2024** | SSL/TLS handshake rejection. DNS tidak resolve untuk PPID. | Hubungi Dinkes langsung |
| **Sulut** | Dinkes kosong. BPS hanya "Statistik Kesehatan". | Hubungi Dinkes / Gunakan BPS sebagai alternatif |

### PowerShell Command untuk Download

```powershell
# Contoh download dari Google Drive
$url = "https://drive.google.com/uc?export=download&id=FILE_ID"
Invoke-WebRequest -Uri $url -OutFile "output.pdf" -Headers @{"User-Agent"="Mozilla/5.0"}

# Contoh download dari PPK Kemendagri
$url = "https://ppid.kemendagri.go.id/storage/dokumen/FILE_ID.pdf"
Invoke-WebRequest -Uri $url -OutFile "output.pdf" -Headers @{"User-Agent"="Mozilla/5.0"}

# Contoh extract RAR
& "C:\Program Files\WinRAR\UnRAR.exe" x -o+ "input.rar" "output_folder\"
```

---

## Rekomendasi

### Prioritas 1: Download dari Scribd (6 file)
1. **Sulsel 2022** - Link tersedia, 338 halaman
2. **Sulsel 2023** - Link tersedia
3. **Sulsel 2020-2021** - Link tersedia
4. **Sultra 2021** - Link tersedia
5. **Action:** Daftar Scribd free trial 7 hari, download semua, lalu cancel

### Prioritas 2: Hubungi Dinas Kesehatan (13 file gap)
1. **Sulsel 2019 & 2024** - Email: dinkes@sulselprov.go.id
2. **Sultra 2019-2020 & 2022-2024** - Email: dinkes@sultraprov.go.id
3. **Sulbar 2019-2024** - Email: dinkes@sulbarprov.go.id
4. **Sulut selain 2023** - Email: dinkes@sulutprov.go.id

### Prioritas 3: Cleanup & Merge
1. **Gorontalo 2017-2018** - Merge isi RAR ke PDF utuh (atau keep sebagai 2 file)
2. **Hapus file sampah:** extracted_gorontalo/, extracted_Gorontalo_2018/, sample_parsing_*.txt

### Prioritas 4: Validasi
1. Cek magic bytes `%PDF` untuk semua file .pdf
2. Cek ukuran minimum > 100 KB
3. Buka sample untuk pastikan tidak corrupt

---

## Statistik Akhir

| Metrik | Nilai |
|--------|-------|
| Total provinsi target | 6 |
| Provinsi selesai | 2 (Gorontalo, Sulteng) |
| Provinsi parsial | 2 (Sulsel, Sulut) |
| Provinsi belum mulai | 2 (Sultra, Sulbar) |
| Total file PDF | 19 |
| Total file RAR | 2 |
| File di Scribd (belum didownload) | 6 |
| File tidak ditemukan dimanapun | 13 |
| Metode sudah dicoba | 15 |
| Sumber berhasil | Wayback, Google Drive, PPK Kemendagri, BPS |
