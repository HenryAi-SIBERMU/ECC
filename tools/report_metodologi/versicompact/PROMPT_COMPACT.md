# PANDUAN EKSEKUSI & INSTRUKSI PROMPT GENERASI METODOLOGI COMPACT (BAB 2 – BAB 9)
**Center of Economic and Law Studies (CELIOS) — Riset D3TLH Sulawesi**

Dokumen ini adalah **Prompt Master & Protokol Instruksi** untuk agen AI berikutnya. Dokumen ini memastikan bahwa generasi laporan metodologi versi compact untuk bab-bab selanjutnya (**Bab 2 hingga Bab 9**) menghasilkan kualitas dan spesifikasi yang **100% konsisten** dengan keberhasilan final **Bab 1 Compact**.

---

## 1. Template Prompt Singkat untuk Pengguna (Tinggal Copy-Paste)

Saat sesi baru dimulai, pengguna cukup menyalin prompt berikut:

```markdown
Tolong kerjakan Laporan Metodologi Versi Compact untuk [Sebutkan Bab Target, misal: Bab 2].
Sebelum mulai, wajib baca dan ikuti:
1. tools/report_metodologi/versicompact/PROMPT_COMPACT.md (Panduan & Protokol Eksekusi)
2. tools/report_metodologi/versicompact/RULES_DOKUMENTASI_COMPACT.md (Aturan Baku Format & Layout)
3. Contoh sukses Bab 1 di tools/report_metodologi/versicompact/bab_1/ (Skrip, DOCX 2 lembar, dan MD)
4. Dokumen root non-compact bab target di tools/report_metodologi/bab_[X]/

Pastikan dokumen Word (DOCX) hasil akhir berukuran maksimal 2-4 lembar, tanpa icon/emoji, tanpa blok improvisasi (no humanisasi/caveats), dan penomoran sub-bab persis sesuai root non-compact.
```

---

## 2. File Rujukan Wajib yang Harus Dibaca Agen

Sebelum menulis kode atau membuat file untuk bab target (`Bab X`), agen **WAJIB** membaca file-file berikut:

| No | Komponen Acuan | Path File | Fungsi & Peran |
| :---: | :--- | :--- | :--- |
| 1 | **Aturan Baku Compact** | `tools/report_metodologi/versicompact/RULES_DOKUMENTASI_COMPACT.md` | Aturan baku layout ultra-dense, font 8.5 pt, margin 1.2 cm, no icon, no improv. |
| 2 | **Contoh Skrip Generator Sukses** | `tools/report_metodologi/versicompact/bab_1/generate_bab1_compact.py` | Template skrip python-docx padat yang menghasilkan Word tepat 2 lembar. |
| 3 | **Contoh Markdown Sukses** | `tools/report_metodologi/versicompact/bab_1/Metodologi_Bab1_Ekspansi_Industri_Compact.md` | Standar kepadatan naskah Markdown. |
| 4 | **Dokumen Root Bab Target (Full)** | `tools/report_metodologi/bab_{X}/Metodologi_Bab{X}_....md` | Sumber data primer tunggal (semua narasi, rumus, dan angka diambil dari sini). |

---

## 3. 5 Aturan Emas yang Tidak Boleh Dilanggar (*Non-Negotiable Rules*)

1. **Target Panjang Halaman (Page Budget): MAKSIMAL 2 HINGGA 4 LEMBAR**
   - Dokumen Word (DOCX) yang dihasilkan **TIDAK BOLEH LEBIH DARI 4 HALAMAN**.
   - Idealnya tepat **2 hingga 3 halaman** seperti Bab 1.
   - Wajib diverifikasi dengan menjalankan pengujian halaman Word COM di terminal.
2. **Kesesuaian Header & Judul Root:**
   - Judul dokumen `# BAB {X}: METODOLOGI ANALISIS ...` harus sama persis dengan dokumen root non-compact.
   - Penomoran sub-bab wajib langsung (`X.1`, `X.2`, `X.3`, dst.), **TIDAK BOLEH** memakai kata `"Poin"`.
3. **Nol Improvisasi (Strict Content Fidelity):**
   - **DILARANG** menambahkan narasi buatan sendiri atau opini di luar dokumen root.
   - **DILARANG** membuat kotak `SKALA HUMANISASI (REALITAS SOSIAL)` atau `CATATAN KETERBATASAN DATA (CAVEATS)` buatan.
   - **DILARANG** menggunakan metafora yang tidak ada di naskah root (cangkir kopi, lapangan bola, upah detik buruh, dsb.).
4. **Nol Icon / Emoji (No Icon Policy):**
   - Hapus total seluruh icon atau emoji grafis (`⚠️`, `🔎`, `✅`, `❌`, dsb.).
5. **Sintesis Tabel Padat:**
   - Gabungkan skenario tabel inferensial statistik (Chi-Square, p-value, Odds Ratio) ke dalam **1 tabel sintesis panel** berstandar SPSS.
   - Batasi total tabel dalam satu bab hanya berkisar antara **4 hingga 6 tabel kunci**.

---

## 4. Protokol Eksekusi Langkah-demi-Langkah (Untuk Agen AI)

Ketika diminta mengerjakan Bab berikutnya (misal: Bab 2), ikuti langkah berikut:

### Langkah 1: Pelajari Dokumen Root Bab Target
Buka dan baca dokumen non-compact di `tools/report_metodologi/bab_{X}/`:
- Catat judul bab lengkap dan paragraf pengantar.
- Petakan seluruh sub-bab (`X.1`, `X.2`, `X.3`, dst.).
- Identifikasi seluruh formulasi matematis dan tabel temuan data empiris.

### Langkah 2: Buat Folder Khusus Bab di Versicompact
Buat direktori baru:
```powershell
New-Item -ItemType Directory -Force -Path "tools/report_metodologi/versicompact/bab_{X}"
```

### Langkah 3: Susun Skrip Generator `generate_bab{X}_compact.py`
Tulis skrip Python dengan mengadopsi arsitektur dari `versicompact/bab_1/generate_bab1_compact.py`:
- **Margin Halaman:**
  ```python
  for section in doc.sections:
      section.top_margin = Cm(1.2)
      section.bottom_margin = Cm(1.2)
      section.left_margin = Cm(1.2)
      section.right_margin = Cm(1.2)
  ```
- **Tipografi:**
  - Normal Body: `Calibri 8.5 pt`, line spacing `1.05`, space after `2 pt`.
  - Heading 1: `10.5 pt bold` (warna `#1B5E20`, border bottom `#1B5E20` sz 8).
  - Heading 2: `9.5 pt bold` (warna `#1B5E20`, border bottom `#2E7D32` sz 4).
  - Heading 3: `8.5 pt bold` (warna `#2E7D32`).
  - Tabel: `Calibri 7.0–7.5 pt`, cell margin rapat (top/bottom `20-30 dxa`, left/right `50 dxa`).
  - Formulasi: `Consolas 7.5 pt` horizontal 1–2 baris dengan latar `#EDF7EE`.
- **Lokasi Simpan Ganda (Dual Save):**
  - Simpan di: `tools/report_metodologi/versicompact/bab_{X}/Metodologi_Bab{X}_..._Compact.docx`
  - Salin ke: `tools/report_metodologi/bab_{X}/Metodologi_Bab{X}_..._Compact.docx`
  - Dan buat naskah Markdown `.md` di kedua lokasi yang sama.

### Langkah 4: Eksekusi Generator
Jalankan skrip di terminal:
```powershell
python "tools/report_metodologi/versicompact/bab_{X}/generate_bab{X}_compact.py"
```

### Langkah 5: Verifikasi Jumlah Halaman Word (Wajib!)
Jalankan skrip verifikasi statistik halaman Word COM:
```powershell
python -c "
import win32com.client as win32
word = win32.Dispatch('Word.Application')
word.Visible = False
doc = word.Documents.Open(r'C:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\tools\report_metodologi\versicompact\bab_{X}\Metodologi_Bab{X}_..._Compact.docx')
pages = doc.ComputeStatistics(2)
print('Page count:', pages)
doc.Close()
word.Quit()
"
```
- **Kriteria Kelulusan:** Nilai `Page count` **HARUS berada di antara 2 hingga 4 lembar**.
- Jika `Page count > 4`: Lakukan pengetatan cell padding tabel, padatkan teks deskripsi, atau sintesiskan baris tabel hingga mencapai target 2–4 lembar.

### Langkah 6: Git Commit
Lakukan commit ke Git:
```powershell
git add "tools/report_metodologi/versicompact/bab_{X}" "tools/report_metodologi/bab_{X}/Metodologi_Bab{X}_..._Compact.*"
git commit -m "feat: generate Bab {X} compact methodology (ultra-dense layout, exactly X pages)"
```

---

## 5. Ringkasan Status Pengerjaan Seluruh Bab

| Bab | Topik Metodologi | Status Versi Compact | Jumlah Halaman Word |
| :---: | :--- | :---: | :---: |
| **Bab 1** | Ekspansi Industri Ekstraktif & Infrastruktur Penunjang | **SELESAI (Standard Acuan)** | **Tepat 2 Lembar** |
| **Bab 2** | Beban Kualitas Lingkungan Hidup (IKU, IKA, Tailing, Deforestasi, Biodiversitas) | Menunggu Pengerjaan | Target: 2–4 Lembar |
| **Bab 3** | Beban Kesehatan & Kerugian Ekonomi Lingkungan | Menunggu Pengerjaan | Target: 2–4 Lembar |
| **Bab 4** | Ketimpangan Ekonomi & Polarisasi Kesejahteraan | Menunggu Pengerjaan | Target: 2–4 Lembar |
| **Bab 5** | Pola Penerbitan Izin & Tata Kelola Ruang Tambang | Menunggu Pengerjaan | Target: 2–4 Lembar |
| **Bab 6** | Audit Daya Dukung & Daya Tampung Lingkungan Hidup (D3TLH) | Menunggu Pengerjaan | Target: 2–4 Lembar |
| **Bab 7** | Kegagalan Tata Kelola & Kebijakan Transisi Energi | Menunggu Pengerjaan | Target: 2–4 Lembar |
| **Bab 8** | Distribusi Manfaat Ekonomi vs Eksternalitas Lingkungan | Menunggu Pengerjaan | Target: 2–4 Lembar |
| **Bab 9** | Demografi Sosial & Kerentanan Masyarakat Adat / Pesisir | Menunggu Pengerjaan | Target: 2–4 Lembar |
