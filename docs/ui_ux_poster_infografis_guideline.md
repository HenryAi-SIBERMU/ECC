# UI/UX Poster Infografis Guideline (CELIOS D3TLH)

Dokumen ini adalah **pedoman teknis absolut dan paling mendetail** untuk rancang bangun UI/UX pada halaman Infografis (Poster/Summary) di platform CELIOS D3TLH. Dokumen ini mendiktekan seluruh logika perhitungan, format data, pewarnaan CSS, struktur grid HTML, dan injeksi *f-strings* tanpa diringkas sama sekali, berdasarkan standar emas yang telah diselesaikan di Seksi 1.

> [!IMPORTANT]
> **REFERENSI KODE ABSOLUT (SOURCE OF TRUTH)**
> Dokumen ini dirancang untuk di- *reuse* pada proyek-proyek selanjutnya sebagai *Context Memory*. Seluruh panduan di bawah ini secara spesifik mengacu pada arsitektur yang telah dibangun di dalam file master:
> **File:** `12_Infografis_Summary.py`
> **Folder Lokasi:** `client/4. Celios2/pages/`
> Pastikan untuk selalu merujuk ke file tersebut saat mengimplementasikan pedoman ini.

---

## 1. GOLDEN RULES (ATURAN MUTLAK)
1. **Dinamis 100% (No Hardcode):** Dilarang keras mengetik manual angka apa pun untuk metrik (contoh: tidak boleh `st.write("14.000 Ha")`). Semua angka harus ditarik dari dataset CSV yang terletak di dalam folder `client/4. Celios2/data/processed/` dan `client/4. Celios2/data/raw/` menggunakan Pandas (`df.sum()`, `len(df)`).
2. **Eksekusi Baseline Wajib Ekstraksi Data Historis:** Jika tahun awal (baseline 2014) terkesan tidak ada, Anda WAJIB membedah kolom `Tahun` atau mengekstrak data historis dari dataset untuk menciptakan baseline empiris (misal `len(df[df['Tahun'] <= 2014])`). Jangan gunakan nilai 0 yang mematikan kalkulasi Delta. Delta WAJIB berupa persentase murni (contoh: `▲ +342%`), bukan sekadar lencana teks (*badges* kata-kata sifat seperti "Dominasi").
3. **Ekstraksi Brutal (Tanpa Batas Baris):** Buang jauh-jauh aturan desain "8 baris ideal". Semakin banyak matriks kerusakan yang bisa diekstrak dari CSV, semakin kuat narasi poster. Seksi 1 pada file `client/4. Celios2/pages/12_Infografis_Summary.py` terbukti mampu memuat 10 metrik indikator sekaligus.
4. **Data-Driven Insights:** Kolom *Recommendation/Insight* tidak boleh memuat opini kualitatif pasif. WAJIB menggunakan sintaks *f-strings* yang menyuntikkan selisih nilai murni atau persentase delta hasil kalkulasi.
5. **Tipografi Mengintimidasi:** **Dilarang menggunakan teks miring (*italic*)** untuk *insight* maupun indikator. Pengaturan ini telah dihapus dari kelas CSS `.cell-insight` di file `client/4. Celios2/pages/12_Infografis_Summary.py`. Semua teks harus tegak dan tegas. Angka metrik menggunakan bobot maksimal (`font-weight: 700/800`).

---

## 2. ARSITEKTUR LOGIKA DATA & KALKULASI PANDAS

Semua kalkulasi dilakukan secara pra-render sebelum menyentuh komponen UI. Berikut adalah referensi absolut cara kita membedah dataset di Seksi 1, seperti yang tertulis di dalam file `client/4. Celios2/pages/12_Infografis_Summary.py`:

### A. Pola Pencarian Baseline vs Terkini (Contoh: Izin IUP)
Dataset rujukan: `client/4. Celios2/data/processed/sulawesi_izin_baru_per_tahun.csv`
```python
iup_2014 = df_izin[df_izin['Tahun'] == 2014]['Jumlah_Izin_Baru'].sum()
iup_terkini = df_izin['Jumlah_Izin_Baru'].sum()
delta_iup = ((iup_terkini - iup_2014) / iup_2014) * 100
```

### B. Pola Filter Multi-Kondisi (Contoh: Hutan Primer)
Dataset rujukan: `client/4. Celios2/data/raw/klhk_gfw/mega_fetch_v2/primary_forest_loss_sulawesi_2001_2025.csv`
```python
prim_2014 = df_prim[(df_prim['year'] == 2014) & (df_prim['is__umd_regional_primary_forest_2001'] == True)]['area__ha'].sum()
prim_terkini = df_prim[df_prim['is__umd_regional_primary_forest_2001'] == True]['area__ha'].sum()
delta_prim = ((prim_terkini - prim_2014) / prim_2014) * 100
```

### C. Pola Kalkulasi Delta Persentase Absolut (Wajib)
Dataset rujukan: `client/4. Celios2/data/processed/sulawesi_konflik_tambang_fpic.csv`
```python
# WAJIB mencari nilai awal/historis agar Delta Persentase terbentuk nyata.
fpic_2014 = len(df_fpic[df_fpic['tahun'] <= 2014]) 
fpic_terkini = len(df_fpic)
delta_fpic = f"▲ +{((fpic_terkini - fpic_2014) / fpic_2014 * 100):,.0f}%" # Wajib berbentuk persentase f-string
```

---

## 3. FORMATTING F-STRINGS UNTUK DATA-DRIVEN INSIGHTS

Setiap baris indikator harus menyuntikkan narasi berbasis angka. Angka besar harus dibagi menjadi unit baca yang manusiawi (Ribu, Juta, Triliun, Megaton). Aturan ini diimplementasikan secara statis di file `client/4. Celios2/pages/12_Infografis_Summary.py`.

*   **Format Absolut Jutaan:** `{val/1_000_000:,.1f} juta`
*   **Format Absolut Ribuan (Decimal):** `{val:,.0f}`

**Referensi Nyata Seksi 1 dari `client/4. Celios2/pages/12_Infografis_Summary.py`:**
```python
insight_iup = f"Penambahan {iup_terkini - iup_2014:,.0f} IUP baru ({delta_iup:,.0f}%) merepresentasikan percepatan ekspansi ekstraktif di luar kapasitas daya dukung."
insight_luas = f"Monopoli lahan seluas {luas_terkini/1_000:,.0f} Ribu Ha (naik {delta_luas:,.0f}%) secara legal mencaplok ruang hidup komunal dan pesisir."
insight_def = f"Laju deforestasi meroket {delta_def:,.0f}%, menyapu {def_terkini/1_000_000:,.1f} juta Ha tutupan lahan yang berbanding lurus dengan konsesi."
insight_smelter = f"Konsentrasi {smelter_terkini} unit fasilitas pengolahan mengunci wilayah pesisir menjadi zona degradasi ekologis absolut."
insight_pltu = f"Suplai {pltu_terkini:,.0f} MW energi kotor (naik {delta_pltu:,.0f}%) mensabotase target dekarbonisasi nasional demi operasi smelter."
insight_inv = f"Aliran modal domestik sebesar {inv_terkini/1000:,.1f} Triliun Rp terbukti mensubsidi deforestasi tanpa keadilan ekonomi lokal."
insight_pad = f"Ledakan PAD {delta_pad:,.0f}% menjadi ilusi; APBD disandera volatilitas sektor tambang dengan beban eksternalitas negatif permanen."
insight_prim = f"Pembabatan {prim_terkini/1_000_000:,.1f} juta Ha hutan primer mengindikasikan lenyapnya ekosistem purba dan resapan air secara ireversibel."
insight_co2 = f"Pelepasan {co2_terkini/1_000_000:,.1f} megaton karbon mengeliminasi efektivitas klaim transisi energi hijau dari hilirisasi nikel."
insight_log = f"Fragmentasi ruang oleh {log_terkini} simpul logistik pesisir mematikan daya dukung maritim dan wilayah tangkap nelayan tradisional."
```

---

## 4. KONSTRUKSI KOMPONEN PYTHON (DASHBOARD VIEW)

Fungsi `render_infographic_row` diatur dengan *signature* argumen yang kaku. Perhatikan urutan argumen dari file `client/4. Celios2/pages/12_Infografis_Summary.py`:

```python
def render_infographic_row(
    icon, key_indicator, title, unit, 
    label_start, val_start, 
    label_end, val_end, 
    delta_pct, recommendation, 
    color_theme="default", reverse_delta=False
):
```

Ketika memanggil, **jangan pernah** menggunakan label seperti `"Baseline 2014"` atau `"Terkini"`. Selalu gunakan parameter waktu numerik `"Tahun 2014"` dan `"Tahun 2024"` (atau penamaan kuantitatif lain seperti "Pra-2020", "Pasca-2020") untuk argumen `label_start` dan `label_end`!

---

## 5. CSS & HTML LENGKAP UNTUK VERSI CETAK (POSTER V2)

Versi cetak meniadakan Streamlit UI sepenuhnya dan digantikan oleh *raw HTML injection*. 

### A. Kerangka Dasar Grid HTML (Wajib Dipertahankan)
```html
<div class="table-container" style="margin-bottom: 20px;">
    <!-- KEPALA TABEL GRID (Wajib konsisten namanya!) -->
    <div class="col-header">
        <div>Indikator Perizinan</div>
        <div class="ch-center">Data 2014</div>
        <div class="ch-center">Data 2024</div>
        <div class="ch-center">Delta</div>
        <div>Temuan & Implikasi</div>
    </div>
    
    <!-- GRID KONTEN SEKSI -->
    <div class="section-grid">
        <div class="sidebar-cell bg-s1">
            <span style="font-size:18pt; font-weight:900;">01</span>
            <span style="font-size:6pt; writing-mode:vertical-rl; transform:rotate(180deg); margin-top:10px; letter-spacing:1px;">EKSPANSI INDUSTRI</span>
        </div>
        <div class="data-area tint-s1">
            <!-- CONTOH 1 BARIS DATA-ROW -->
            <div class="data-row">
                <!-- KOLOM 1: INDIKATOR -->
                <div class="cell-indicator">Total Ekspansi IUP<br/><span class="unit">Obral Konsesi</span></div>
                
                <!-- KOLOM 2: DATA 2014 -->
                <div class="cell-val v-gray">
                    <span class="material-symbols-outlined">description</span>
                    <span class="num">{izin_2014:,.0f}</span>
                </div>
                
                <!-- KOLOM 3: DATA 2024 -->
                <div class="cell-val v-red">
                    <span class="material-symbols-outlined">description</span>
                    <span class="num">{izin_terkini:,.0f}</span>
                </div>
                
                <!-- KOLOM 4: DELTA (Wajib persen) -->
                <div style="text-align:center;">
                    <span class="badge badge-bad">▲ +{delta_izin:.1f}%</span>
                </div>
                
                <!-- KOLOM 5: INSIGHT -->
                <div class="cell-insight">{insight_izin_tot}</div>
            </div>
        </div>
    </div>
</div>
```

### B. Pedoman CSS Kritis
Pastikan deklarasi CSS di *top-level* halaman (blok `<style>` di Streamlit) menampung semua pernak-pernik tipografi ini secara absolut tanpa pengurangan.

```css
/* Struktur Grid Bawaan */
.table-container { width: 100%; border-collapse: collapse; }
.section-grid { display: flex; border: 1px solid #ddd; }

/* Lebar Kolom Konsisten 5-Kolom (2:1:1:0.8:3) */
.col-header { display: grid; grid-template-columns: 2fr 1fr 1fr 0.8fr 3fr; padding: 2mm; background: rgba(0,0,0,0.02); font-weight: 800; font-size: 6pt; color: #333; text-transform: uppercase; border-bottom: 1px solid #eee; }
.data-row { display: grid; grid-template-columns: 2fr 1fr 1fr 0.8fr 3fr; border-bottom: 1px solid #f0f0f0; align-items: center; padding: 1.5mm 2mm; }

/* Styling Sel Data (Wajib Font-Style Tegak untuk Insight) */
.cell-indicator { font-size: 7.5pt; font-weight: 700; line-height: 1.2; }
.cell-indicator .unit { font-size: 5.5pt; font-weight: 400; color: #888; }
.cell-insight { font-size: 6.5pt; color: #555; line-height: 1.3; } /* <-- DILARANG MENAMBAH FONT-STYLE ITALIC DI SINI */

.cell-val { display: flex; align-items: center; gap: 4px; }
.cell-val span.num { font-size: 7pt; font-weight: 700; font-family: 'Courier New', Courier, monospace; }
.v-gray { color: #888; }
.v-gray .material-symbols-outlined { color: #bbb; }
.v-red { color: #C62828; }
.v-red .material-symbols-outlined { color: #EF5350; }

/* Sistem Lencana (Badges) */
.badge { display: inline-block; padding: 0.5mm 2mm; border-radius: 3px; font-size: 6pt; font-weight: 800; white-space: nowrap; }
.badge-up { background: rgba(76, 175, 80, 0.15); color: #2E7D32; } /* Positif */
.badge-down { background: rgba(244, 67, 54, 0.15); color: #C62828; } /* Negatif Normal */
.badge-bad { background: rgba(244, 67, 54, 0.15); color: #C62828; } /* Merah Khusus (Misal ISPA naik = buruk) */
.badge-neutral { background: rgba(158, 158, 158, 0.15); color: #757575; } /* Abu-abu untuk String Text */

/* Pengatur Warna Tema Seksi 1 (Ungu) */
.bg-s1 { background: #5E35B1; color: white; }
.tint-s1 { background: #fdfcff; }
```

**Setiap meracik baris data untuk seksi-seksi berikutnya, HARAM HUKUMNYA menyimpang dari formula f-strings, HTML `.data-row`, maupun manipulasi *baseline* seperti yang tercantum di atas! Seluruh konfigurasi mengacu secara definitif pada struktur file `client/4. Celios2/pages/12_Infografis_Summary.py`.**
