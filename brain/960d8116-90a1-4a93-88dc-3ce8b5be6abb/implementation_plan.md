# Rencana Implementasi: Rombak Total Page 6 (Audit Forensik D3TLH)

Tujuan dari rencana ini adalah untuk menstruktur ulang `pages/6_Audit_D3TLH.py` agar secara visual dan naratif selaras dengan strategi **Audit Forensik (Pembuktian Terbalik)** yang tertuang dalam `docs/page 6 - Strategi Counter Narrative D3TLH.md`. Halaman ini akan menjadi "Panggung Putusan" (Verdict Room) yang secara frontal membenturkan klaim AMDAL/D3TLH pemerintah dengan realitas krisis di lapangan (berdasarkan dataset yang sudah kita miliki).

## User Review Required
> [!IMPORTANT]
> Harap tinjau struktur visual dan pemetaan dataset di bawah ini. Pastikan *storytelling*-nya sudah sejalan dengan cara Anda ingin mempresentasikan kegagalan D3TLH.

## Open Questions
> [!WARNING]
> Untuk indikator "Bencana Hidrometeorologi" sebagai akibat dari deforestasi tambang, kita saat ini memiliki data hilangnya tutupan hutan (`sulawesi_gfw_hutan_primer_loss_2014_2023.csv`), tetapi data kejadian spesifik banjir bandang dari BNPB belum tersedia di folder `processed`. 
> **Pertanyaan:** Apakah kita gunakan data *Hutan Primer Loss* sebagai proksi hilangnya daya resap air (yang pasti memicu banjir), atau Anda ingin kita mengekstrak data Bencana BNPB terlebih dahulu sebelum mem-build chart ini?

## Proposed Changes

### 1. Perubahan Struktur Narasi (Executive Summary)
*   Mengganti teks Hero Statement dengan narasi keras tentang "Pembuktian Terbalik" bahwa D3TLH telah gagal mendeteksi morbiditas dan konflik.
*   Menyesuaikan *Bento Cards* agar secara spesifik memunculkan angka absolut dari "Titik Buta" AMDAL.

### 2. Tabrakan Metrik (Side-by-Side Comparison)
Kita akan membuat 3-4 seksi utama yang membenturkan Mitos (D3TLH Resmi) vs Realitas Lapangan (Data ECC).

#### A. Mitos Kapasitas Udara vs Realitas ISPA
*   **Narasi:** AMDAL mengklaim emisi debu cerobong sesuai baku mutu, tapi di bawah cerobong, paru-paru warga hancur.
*   **Data Source:** `sulawesi_kesehatan_detail_2014_2024.csv` (Kasus ISPA).
*   **Visualisasi:** *Bar Chart* atau *Area Chart* yang menunjukkan tren meroketnya kasus ISPA di sentra nikel (Sulteng/Sultra) seiring beroperasinya smelter.

#### B. Mitos Daya Tampung Air vs Realitas IKA
*   **Narasi:** D3TLH mengizinkan pembuangan limbah selama sungai/laut dianggap "mampu mengencerkan", tapi faktanya air sudah cemar berat.
*   **Data Source:** `sulawesi_ika_2016_2024.csv`.
*   **Visualisasi:** *Line Chart* yang menunjukkan tren penurunan (merosotnya) Indeks Kualitas Air di bawah standar wajar.

#### C. Mitos Analisis Dampak Sosial vs Realitas Konflik Agraria
*   **Narasi:** Amdal mengukur persetujuan sosial hanya dengan "Daftar Hadir Sosialisasi", sementara warga diusir paksa.
*   **Data Source:** `sulawesi_konflik_agraria_tanahkita.csv` dan `sulawesi_konflik_tambang_fpic.csv`.
*   **Visualisasi:** *Treemap* atau *Bar Chart* eskalasi luasan konflik dan jumlah kejadian perampasan lahan.

#### D. Anomali Tata Kelola (Regulatory Capture)
*   **Narasi:** Ketika semua indikator di atas (ISPA, IKA, Konflik) sedang merah/kritis, pemerintah justru terus menerbitkan Izin Baru. D3TLH sama sekali tidak berfungsi sebagai VETO.
*   **Data Source:** Overlay antara lonjakan metrik krisis vs `sulawesi_izin_baru_per_tahun.csv` (Tren penerbitan IUP Nikel per tahun).

### 3. File yang Dimodifikasi

#### [MODIFY] `pages/6_Audit_D3TLH.py`
Merombak total seluruh struktur Python Streamlit untuk membangun UI/UX seperti yang dideskripsikan di atas, menggantikan *placeholder* statis dengan *data loader* dinamis yang membaca file CSV dari folder `data/processed/`.

## Verification Plan
### Manual Verification
1. Menjalankan *Streamlit lokal* dan memverifikasi bahwa halaman "6. Audit D3TLH" berhasil memuat (tidak ada *error* pandas/plotly).
2. Memastikan setiap grafik *side-by-side* benar-benar menampilkan kontras antara "Klaim" dan "Fakta".
3. Memastikan teks naratif (Hero Statement dan kesimpulan) sudah terganti dengan strategi "Audit Forensik" yang disepakati.
