# Ringkasan: Treemap PAD Tidak Berubah di Browser

> **Status: BELUM SELESAI.** Kode sudah benar & tersimpan (terverifikasi via syntax check + replikasi data-prep), tetapi **treemap di browser user tetap tidak berubah** walau kode sudah diedit. Masalah ada di runtime/render, BUKAN di logika kode. Agen berikutnya wajib memecahkan ini dulu sebelum mengubah apapun lagi.

---

## 1. Yang SUDAH dikerjakan & terverifikasi

### 1a. Edit di `pages/1_Ekspansi_Industri.py` (semua sudah tersimpan, `ast.parse` = `SYNTAX OK`)

| Lokasi | Perubahan | Tujuan |
|---|---|---|
| `:992-996` | Relabel Sultra: `Jenis_Pendapatan` → `'PAD Kab. Buton (BPS: no data provinsi)'` | Jujur: data Sultra = pendapatan Pemerintah Desa Kab. Buton, BUKAN PAD provinsi (BPS tak menyediakan data level provinsi untuk Sultra) |
| `:998-1000` | Filter `df_pad_combined = df_pad_combined[df_pad_combined['Nilai_Miliar_Rp'] > 0]` | Buang 1 baris bernilai 0 (komponen PAD Sulsel yang realisasinya nol di BPS) supaya tidak muncul kotak `0.0 M Rp` |
| `:1018-1035` (data-prep) + `:1033` (narrative) + `:1104` (insight box) | Hitung 4 persentase komponen PAD **dinamis** dari data (`pct_pajak_daerah`, `pct_retribusi`, `pct_hasil_bumd`, `pct_lain_pad`) dan ganti literal hardcoded `82.9%` / `7.8%` / `3.2%` / `6.1%` | Hilangkan angka statis yang bisa drift bila data berubah |
| Narasi + judul chart | `(2010-2023)` → `(2015-2024)` | Rentang tahun sesuai data aktual |

### 1b. Bukti kode benar (replikasi standalone logika data-prep)

Dijalankan terpisah meniru persis blok `:966-1035`:

```
Pajak Daerah  : 82.9%  (hardcoded was 82.9%)   <- match
Retribusi    : 7.8%  (hardcoded was 7.8%)     <- match
Hasil BUMD   : 3.2%  (hardcoded was 3.2%)     <- match
Lain-lain PAD: 6.1%  (hardcoded was 6.1%)     <- match
Total PAD murni: 7116.1 Miliar
```

- Baris treemap: 27 → 26 (1 baris nol dibuang)
- Sultra: label `Total Pendapatan` → `PAD Kab. Buton (BPS: no data provinsi)`, nilai 304.97 Miliar tetap tampil
- Sisa baris bernilai 0: **0** (semua bersih)

### 1c. Konfigurasi runtime yang ditemukan

- File `1_Ekspansi_Industri.py` last-modified **05:25:35**
- Streamlit start **05:42:50** (PID 32536, port 8501) → server load kode setelah edit, jadi kode baru sudah di server
- `.streamlit/config.toml`: `[runner] fastReruns = true`, **`runOnSave` TIDAK diset** → default `false` → Streamlit tidak auto-rerun saat file berubah; hanya muncul prompt "Source file changed → Rerun?"
- Loading PAD (`:968`) **TIDAK** di dalam `@st.cache_data` → bukan masalah cache Streamlit. Dua `@st.cache_data` hanya load dataset lain (izin/smelter/pltu/gfw/inv/logistik)

---

## 2. Masalah TERBUKA (wajib dikerjakan agen berikutnya)

> **User melaporkan treemap "belum berubah" WALAU kode sudah benar & server sudah load kode baru. Aku sudah suruh user tekan R / Ctrl+Shift+R tapi user tetap melaporkan tidak berubah.** Akar masalah belum ditemukan.

### Hipotesis yang belum dibantah & belum diuji (CEK URUT INI)

1. **User belum benar-benar trigger rerun.** `runOnSave=false` → Streamlit cuma tunjuk prompt; bila user tidak klik "Rerun" atau tekan R, render lama dipertahankan. **Tanya langsung: apakah prompt "Rerun?" muncul di pojok kanan atas? Sudah diklik?**
2. **Browser cache.** Plotly treemap bisa ter-cache agresif. Coba hard-refresh `Ctrl+Shift+R` / buka tab incognito / buka URL dengan `?embed=true` baru.
3. **Port/session salah.** Mungkin user lihat browser di port lain (bukan 8501) atau tab lama yang stuck. Verifikasi: `Get-NetTCPConnection -State Listen | ? LocalPort -in 8501,8502,8503`.
4. **Perubahan terlalu halus untuk diliat mata.** Aku akui: hanya 1 label kotak berubah + 1 kotak nol hilang (invisible). Struktur treemap (5 provinsi, layout) praktis identik. **User mungkin menganggap "tidak berubah" karena layout besar tak beda**, padahal label Sultra sudah berubah. Minta user klik kotak Sulawesi Tenggara dan baca labelnya.
5. **Bila semua di atas sudah dicek & tetap tidak berubah**: kemungkinan ada `__pycache__` Streamlit yang hold module lama. Kill PID 32536, hapus `__pycache__`, restart `python -m streamlit run Dashboard.py` lalu buka fresh.

### Cara verifikasi cepat perubahan BENAR-BENAR live

Setelah rerun, kotak **Sulawesi Tenggara** harus berlabel:
`PAD Kab. Buton (BPS: no data provinsi)`
(bukan `Total Pendapatan`). Kalau masih `Total Pendapatan` → kode lama yang jalan, bukan kode baru.

---

## 3. Keputusan konteks data (tetap berlaku, jangan diubah sembarangan)

- **Sultra = data salah level administratif**: `data/raw/bps_pad/padsultra.csv` adalah keuangan Pemerintah Desa Kab. Buton, BUKAN PAD provinsi Sultra. Diputuskan: **dipertahankan di treemap tapi dilabel jujur**, BUKAN dihapus (agar tidak menyesatkan, tanpa kehilangan konteks).
- **8 baris nol di CSV** = realisasi nol yang sah di sumber BPS (BPS bedakan `0` = realisasi nol vs `-` = tidak relevan). Diputuskan: **dibuang dari tampilan treemap** (filter `> 0`) tapi tetap ada di tabel data detail (`:1110` expander) demi transparansi.
- **CSV tidak diubah** (data lineage dijaga); fix dilakukan page-level di `1_Ekspansi_Industri.py` saja.

---

## 4. Konteks file (untuk agen berikutnya)

- **File utama:** `pages/1_Ekspansi_Industri.py` (1589 baris). Blok data-prep & treemap `:965-1079`; insight box `:1097-1108`; tabel detail `:1110`.
- **Data PAD breakdown:** `data/processed/sulawesi_pad_breakdown_2016_2024.csv` (125 baris, 3 provinsi: Gorontalo 2015-2019 juta Rp, Sulsel 2016-2021 ribu Rp, Sultra 2022-2024 = Kab. Buton)
- **Data PAD total (tanpa breakdown):** `data/processed/sulawesi_pad_2016_2024.csv` (Sulut, Sulbar)
- **Raw BPS:** `data/raw/bps_pad/{padsulsel,padsultra,padgorontalo}.csv`
- **Entry point Streamlit:** `Dashboard.py` → `python -m streamlit run Dashboard.py`
- **Konfig:** `.streamlit/config.toml` (theme gelap, `runOnSave` default false)

---

## 5. Saran tindakan agen berikutnya (urutan prioritas)

1. **JANGAN ubah kode dulu.** Kode sudah benar. Ubah kode = bikin makin rumit.
2. Konfirmasi dulu apakah user benar-benar sudah rerun (prompt "Rerun?" diklik / tekan R).
3. Cek label kotak Sulawesi Tenggara = `PAD Kab. Buton (BPS: no data provinsi)`? Kalau ya → perubahan SUDAH live, user salah persepsi layout. Kalau masih `Total Pendapatan` → kode lama yang jalan → lanjut langkah 4.
4. Kill & restart Streamlit bersih: hapus `__pycache__`, `Get-Process python | Stop-Process`, `python -m streamlit run Dashboard.py`, buka tab incognito.
5. Bila tetap gagal: aktifkan `runOnSave = true` di `.streamlit/config.toml` `[server]` supaya auto-rerun, lalu simpan file (trigger rerun paksa).
6. **Bonus opsional (bukan prioritas):** persentase dinamis sudah diimplementasi; tidak ada hardcoded `82.9/7.8/3.2/6.1` tersisa (sudah diverifikasi via `findstr`).
