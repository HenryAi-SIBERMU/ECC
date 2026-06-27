# Pedoman Desain UI/UX & Struktur Dashboard (Adaptasi CELIOS 5 - LEUI)

Dokumen ini disusun ulang secara komprehensif berdasarkan struktur tingkat tinggi dari proyek referensi `Celios5-LEUI` (khususnya halaman `3_H1_Inconsistency_Risk.py`). Pedoman ini bersifat **mengikat dan wajib diterapkan** pada seluruh rancangan visualisasi *Page 1* dan seterusnya pada proyek Studi D3TLH.

---

## 1. Aturan Emas: Pure Data-Driven (NO MOCK DATA)
Seluruh narasi, perhitungan persentase (*growth*, rasio, proporsi), dan status (AWAS/AMAN) **WAJIB** dikalkulasi langsung secara dinamis dari file CSV mentah (folder `data/processed/`). 
*   **Dilarang keras** melakukan *hardcode* angka statistik pada teks narasi. 
*   Gunakan variabel Python (contoh: `{top5_share:.1f}%`, `{total_smelter:,}`) yang diinjeksi ke dalam teks narasi menggunakan `f-string` atau `.format()`.

---

## 2. Struktur Bab & Sub-Bab (Hierarki H1, H2, H3)
Setiap halaman tidak boleh sekadar meletakkan grafik secara acak. Halaman harus dibagi menjadi *layer* pemikiran yang terstruktur:
*   **Separator Header Utama:** Menggunakan garis putus-putus atau blok pemisah (contoh: `# ════════════ LAYER X: VARIABEL PENYEBAB ════════════`).
*   **Penomoran Sub-Bab:** Wajib konsisten. 
    *   `st.subheader("1. Fakta Penyebab: Ekspansi Industri dan Izin")`
    *   `st.subheader("1.1 Tren Pertumbuhan Izin Tambang Baru (Crosstab 1)")`
    *   `st.subheader("1.2 Agresivitas Ekspansi Smelter vs Luas Lahan (Crosstab 2)")`
*   **Struktur Crosstab:** Setiap matriks *Crosstab* dari *outline* riset (misal: Jumlah Izin vs Tahun) harus mewakili satu Sub-Bab tersendiri.

---

## 3. Tag Metode (Method Tag)
Tepat di bawah setiap judul Sub-Bab, **wajib** mencantumkan *Tag Metode* berupa blok `HTML <span>` kecil dengan latar belakang warna khusus untuk menjelaskan *proxy* atau variabel metode yang digunakan.
*   **Contoh:** 
    ```python
    st.markdown('<span style="background:#5C2B6A;color:#E1BEE7;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: Crosstabulation Pertumbuhan Izin per Provinsi (Variabel X1)</span>', unsafe_allow_html=True)
    ```

---

## 4. Narasi Storytelling, Advokasi, dan Kritis
Proyek Celios sangat mengedepankan narasi riset advokasi. Grafik tidak boleh dibiarkan berbicara sendiri.
*   **Judul Halaman (Main Title):** **Dilarang** menggunakan awalan penomoran seperti "Page 1:" atau "Page 2:" di dalam UI. Langsung gunakan judul substantifnya (contoh: "Ekspansi Industri Ekstraktif").
*   **Struktur Header Eksekutif:** Di bagian atas setiap halaman analisis penting, wajib menggunakan urutan **Dropdown Metodologi**, **Hero Statement**, lalu **Bento Cards**.
    1.  **Dropdown Metodologi (`st.expander`):** Tepat di bawah sub-judul, wajib diletakkan `st.expander("🔍 Metodologi")` yang menguraikan kerangka kerja halaman tersebut.
        *   *Isi Metodologi:* Harus mencakup penjelasan **Alur Kausalitas** (contoh: `A → B → C`), pemetaan **Variabel (X)** (faktor penyebab/tekanan), **Variabel (Y)** (dampak/hasil), serta **Metode Pengolahan Data** (contoh: *Crosstabulation*, *Trend Analysis*).
    2.  **Hero Statement (Paragraf Narasi Kritis Utama):** Ini adalah teks pengantar (tanpa kotak aksen/warna terang, cukup *background* transparan) yang **WAJIB diletakkan tepat di bawah Tag Metode atau Dropdown Metodologi (sebelum pemilih/dropdown data dan sebelum grafik)**. Paragraf ini **WAJIB** dibangun sebagai sebuah *storytelling* jurnalistik-kritis yang panjang (minimal 250 kata) dan *data-driven*. Narasi ini harus mengekstrak angka mutlak dari agregasi awal (menggunakan Python `f-strings`), menyebut langsung total kasus/kerusakan secara eksplisit, dan menarik kesimpulan kausalitas yang membantah narasi arus utama (misalnya "Membantah Hilirisasi Hijau").
    3.  **Bento Cards (Grid Kartu Metrik Agregat):** Letakkan tepat di bawah Hero Statement dalam bentuk grid (contoh: 2 baris x 3 kolom).
        *   *Kewajiban Bento Cards:* **Setiap kartu WAJIB memiliki deskripsi naratif** yang menjelaskan konteks/arti angka tersebut di dalam kartunya.
        *   *Atribusi Sumber File:* **WAJIB mencantumkan institusi sumber beserta nama file CSV aslinya** di sudut bawah setiap kartu (contoh: `Sumber: Kementerian ESDM (Minerbaone) <br/> File: sulawesi_izin_baru.csv`). **DILARANG keras menggunakan icon emoji** (seperti 📁). Semua angka wajib murni *data-driven* tanpa *hardcode*.
*   **Kotak Interpretasi/Pembedahan Realitas Ekologis (Card di Bawah Grafik):** Di bawah setiap visualisasi (grafik) atau tabel eksekutif, sediakan ringkasan narasi spesifik mengenai grafik tersebut.
    *   *Standar Ketajaman Narasi:* Berbeda dengan versi pedoman sebelumnya, kotak ini **TIDAK PERLU** berisi narasi panjang 250 kata. Kotak Interpretasi Ekologis di bawah grafik cukup berisi **1-2 paragraf pendek** yang merangkum dinamika spesifik data yang sedang ditampilkan (misal: membandingkan angka variabel yang dipilih melalui dropdown).
    *   *Praktik Wajib:* Jika ingin menggunakan kotak antarmuka bergaya kartu peringatan namun **TANPA IKON** (agar terlihat lebih bersih/minimalis dari bawaan `st.error`), Anda **WAJIB** menggunakan elemen kustom HTML (`<div>`) dengan `unsafe_allow_html=True`.
    *   *Peringatan Rendering (Sangat Penting):* Saat teks diletakkan di dalam `<div>`, Streamlit tidak akan mem- *parsing* sintaks Markdown. Oleh karena itu, Anda **DILARANG KERAS** menggunakan Markdown seperti `**tebal**`. Gunakan secara murni tag HTML seperti `<b>tebal</b>`, `<i>miring</i>`, dan `<br>` untuk spasi paragraf. Jika tidak mematuhi ini, sintaks bintang akan bocor ke tampilan UI.

---

## 5. Dropdown Sumber Tabel Setiap Visualisasi (Data Transparency)
Sebagai bentuk transparansi *data-driven*, tepat di bawah **SETIAP** analisis visual (baik itu Peta, Bar Chart, Area Chart, Scatter Plot, maupun Uji SPSS), **wajib** disediakan tombol *dropdown/expander* yang berisi tabel data mentah (*dataframe*) pembentuk visualisasi tersebut secara berdampingan.
*   **Format Wajib:**
    ```python
    with st.expander("Lihat Data Mentah: [Nama Tabel Data]", expanded=False):
        st.dataframe(df_nama_data, use_container_width=True, hide_index=True)
        st.caption("📁 **Sumber File:** `data/processed/nama_file.csv` - [Keterangan singkat isi data]")
    ```
*   Sumber file (`📁 Sumber:`) juga boleh dipasang di bawah paragraf narasi pengantar dengan ukuran teks `<small>`.

---

## 6. Gaya Desain Visualisasi (Altair / Plotly)
*   **Judul Grafik Internal Wajib (Internal Chart Title):** Setiap pembuatan grafik (Altair/Plotly) **WAJIB** menyertakan judul langsung di dalam konfigurasi grafiknya (misal: menggunakan `title=alt.TitleParams(text="...", color='#ECEFF1', anchor='start')` pada Altair atau `title=...` pada Plotly). Dilarang hanya mengandalkan `st.markdown` sebagai judul di atas grafik, agar ketika grafik diekspor/diunduh, konteks dan judul tetap terbawa utuh.
*   **Konsistensi Tema Halaman (Header & Badge):** Seluruh halaman aplikasi (Hero Section) **WAJIB** menggunakan palet warna hijau khas CELIOS secara konsisten untuk judul dan *badge*. **DILARANG** menggunakan warna biru atau tema lain untuk header agar identitas *brand* terjaga.
    *   `.org-badge`: `linear-gradient(135deg, #1B5E20, #2E7D32);`
    *   `.main-title`: `linear-gradient(135deg, #43A047, #66BB6A, #81C784);`
*   **Tema Utama:** Gelap Premium (*Dark Mode*). Hindari tampilan *default* bawaan yang terlalu mencolok.
*   **Anotasi (Callouts):** Sangat disarankan menambahkan anotasi teks/tanda panah langsung di dalam grafik untuk menunjuk "Puncak Lonjakan" atau "Titik Anomali". **DILARANG** menggunakan teks interpretasi statis yang emosional. **WAJIB** menggunakan kalkulasi data dinamis yang murni empiris, contoh: menghitung persentase lonjakan langsung dari DataFrame (`↑ 235% Kenaikan (2022-2024)`).
*   **Palet Warna (Minimalist Professional Flat):** **DILARANG KERAS** menggunakan warna pelangi (*rainbow*) atau warna cerah yang terlalu *vibrant/bright*. Gaya visualisasi harus berwibawa menyerupai laporan jurnal *Think-Tank* internasional atau *dashboard* intelijen korporat:
    *   Gunakan warna *flat/muted* (redup namun tegas).
    *   **Data Baseline/Konteks/Lainnya:** Gunakan gradasi *Slate Grey* atau *Blue Grey* (contoh: `#37474F`, `#546E7A`, `#78909C`, `#90A4AE`).
    *   **Data Kritis/Bahaya (Highlight Utama):** Gunakan *Muted Red* (contoh: `#D32F2F`) atau *Muted Orange* (contoh: `#F57C00`) secara spesifik untuk menyorot anomali, kerusakan lingkungan, atau monopoli ruang (zona tumbal).
*   **Elemen Kosmetik UI Chart:** Disarankan untuk menyamarkan garis *grid* (atur *gridOpacity* di angka 0.1 atau 0.05) agar latar belakang grafik terlihat bersih (*clean*). Warnai teks *axis* maupun *legend* dengan abu-abu netral (contoh: `#B0BEC5` atau `#ECEFF1`).
*   **Time-Series Area Chart (Gaya OWID):** Untuk menyoroti tren kenaikan kumulatif atau eksponensial dari waktu ke waktu, gunakan *Stacked Area Chart* dengan *range slider* di bawahnya (meniru gaya *Our World in Data*). Pada sumbu X yang memuat data Tahun, resolusi harus dijaga agar tidak berdempetan (`dtick=2`) dan **WAJIB** menghilangkan format pemisah ribuan menggunakan format resolusi `tickformat='d'` (Plotly) atau yang setara pada Altair agar "2,020" tampil menjadi "2020".

## 7. Analisis Statistik (SPSS Style Crosstab)
Jika riset membutuhkan pengujian hipotesis bivariat (seperti Chi-Square Test), UI wajib dirender menyerupai layar *output* perangkat lunak statistik standar (SPSS/Stata):
*   **Case Processing Summary:** Menampilkan hitungan N (Valid/Missing).
*   **Crosstabulation Table:** Matriks baris/kolom bertingkat (`Count` dan `Expected Count`) dengan Multi-Index DataFrame.
*   **Chi-Square Tests Table:** Menampilkan Nilai *Pearson Chi-Square*, *Likelihood Ratio*, dan `P-Value` (Asymp. Sig).
*   **Dynamic Hypothesis Card:** Menyediakan *Card UI* bersyarat. Jika P-Value < 0.05, warna border hijau menyala. Jika P-Value ≥ 0.05, warna border merah menyala. **Narasi interpretasi WAJIB responsif** terhadap perubahan ini.

---
**Kesimpulan Implementasi untuk Page 1:**
Saat *coding* Page 1 (Ekspansi Industri), tiap sub-bab akan diawali dengan judul yang mengalir (tanpa mencantumkan label nama kode kaku seperti "(Crosstab 1)" di *subheader*), *Tag Metode*, diikuti narasi kritis (*Data-driven* Python `f-strings`), grafik dengan anotasi, matriks Crosstabulation SPSS (jika relevan), blok Interpretasi, dan ditutup dengan `st.expander` berisi data CSV murni (seperti `sulawesi_izin_baru_per_tahun.csv` dan `sulawesi_esdm_nikel.csv`).
