"""
extract_chapter_7.py
100% faithful extraction of pages/7_Kegagalan_Tata_Kelola.py → chapter_7.md
"""
import os, sys, re
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA = ROOT / "data" / "processed"
VIS  = HERE / "visuals_bab7"
VIS.mkdir(exist_ok=True)

def save_plotly(fig, path, w=1000, h=500):
    fig.write_image(str(path), width=w, height=h, scale=2)

# ─── DATA LOAD ───────────────────────────────────────────────────────────────
df_izin = pd.read_csv(DATA / "sulawesi_izin_baru_per_tahun.csv") if (DATA / "sulawesi_izin_baru_per_tahun.csv").exists() else pd.DataFrame()
df_gfw  = pd.read_csv(DATA / "sulawesi_gfw_master_1_dekade_2014_2023.csv") if (DATA / "sulawesi_gfw_master_1_dekade_2014_2023.csv").exists() else pd.DataFrame()
df_konflik_hukum = pd.read_csv(DATA / "sulawesi_konflik_hukum.csv") if (DATA / "sulawesi_konflik_hukum.csv").exists() else pd.DataFrame()
df_pltu_captive  = pd.read_csv(DATA / "sulawesi_pltu_captive.csv") if (DATA / "sulawesi_pltu_captive.csv").exists() else pd.DataFrame()
df_raw_details   = pd.read_csv(DATA / "sulawesi_izin_raw_details.csv") if (DATA / "sulawesi_izin_raw_details.csv").exists() else pd.DataFrame()

df_panel = pd.merge(df_gfw, df_izin, on=['Provinsi', 'Tahun'], how='left').fillna({'Jumlah_Izin_Baru': 0, 'Total_Luas_Konsesi_Baru_Ha': 0})

# ─── SECTION 7.1 CALCULATION ─────────────────────────────────────────────────
indikator_d3tlh = "Total_Deforestasi_Ha"
tertekan_threshold = df_panel[indikator_d3tlh].quantile(0.33)
kritis_threshold   = df_panel[indikator_d3tlh].quantile(0.66)

def classify_d3tlh(val):
    if val <= tertekan_threshold:
        return "Aman"
    elif val <= kritis_threshold:
        return "Tertekan"
    else:
        return "Kritis"

df_panel['Status_D3TLH'] = df_panel[indikator_d3tlh].apply(classify_d3tlh)

agg_df = df_panel.groupby('Status_D3TLH').agg({
    'Jumlah_Izin_Baru': 'sum',
    'Total_Luas_Konsesi_Baru_Ha': 'sum',
    indikator_d3tlh: ['min', 'max']
}).reset_index()

agg_df.columns = ['Status_D3TLH', 'Total_IUP', 'Total_Luas_Ha', 'Min_Def', 'Max_Def']
order_map = {"Aman": 1, "Tertekan": 2, "Kritis": 3}
agg_df['Order'] = agg_df['Status_D3TLH'].map(order_map)
agg_df = agg_df.sort_values('Order')

total_iup_kritis = 0
table_rows_md = []
table_rows_md.append("| Status Daya Dukung | Kondisi Kerusakan Hutan | Seharusnya (Menurut Aturan) | Kenyataan di Lapangan | Kesimpulan Tata Kelola |")
table_rows_md.append("|---|---|---|---|---|")

for idx, row in agg_df.iterrows():
    status = row['Status_D3TLH']
    if status == "Kritis":
        total_iup_kritis = row['Total_IUP']
        
    range_str = f"Hilang {row['Min_Def']:,.0f} - {row['Max_Def']:,.0f} Ha"
    iup_str = f"{int(row['Total_IUP'])} Izin Baru Keluar"
    
    if status == "Aman":
        kondisi = f"Ringan ({range_str})"
        aturan = "Wajar diterbitkan izin"
        kenyataan = iup_str
        kesimpulan = "Normal (Sesuai Aturan)"
    elif status == "Tertekan":
        kondisi = f"Sedang ({range_str})"
        aturan = "Izin mulai direm/dibatasi"
        kenyataan = iup_str
        kesimpulan = "Anomali (Lampu Kuning)"
    else: # Kritis
        kondisi = f"Sangat Parah ({range_str})"
        aturan = "**Moratorium / Izin Dilarang!**"
        kenyataan = f"**{iup_str}** (Termasuk luasan {row['Total_Luas_Ha']:,.0f} Ha)"
        kesimpulan = "**BUKTI PELANGGARAN FATAL**"
    
    table_rows_md.append(f"| **{status}** | {kondisi} | {aturan} | {kenyataan} | {kesimpulan} |")

table_crosstab_md = "\n".join(table_rows_md)

# Detailed Kritis Table
df_kritis_panel = df_panel[(df_panel['Status_D3TLH'] == 'Kritis') & (df_panel['Jumlah_Izin_Baru'] > 0)]
kritis_pairs = set(zip(df_kritis_panel['Provinsi'], df_kritis_panel['Tahun']))
df_kritis_raw = df_raw_details[df_raw_details.apply(lambda row: (row['Provinsi'], row['Tahun']) in kritis_pairs, axis=1)].copy()

if not df_kritis_raw.empty:
    df_show_raw = df_kritis_raw[['nama_badan_usaha', 'nomor_izin', 'tahap_kegiatan', 'komoditas', 'Provinsi', 'lokasi_perizinan', 'Tahun', 'luas_ha']].copy()
    deforestasi_map = df_kritis_panel.set_index(['Provinsi', 'Tahun'])[indikator_d3tlh].to_dict()
    df_show_raw['deforestasi'] = df_show_raw.apply(lambda row: deforestasi_map.get((row['Provinsi'], row['Tahun']), 0), axis=1)
    df_show_raw['Status Lingkungan'] = 'KRITIS (Deforestasi Ekstrem)'
    df_show_raw = df_show_raw[['nama_badan_usaha', 'nomor_izin', 'tahap_kegiatan', 'komoditas', 'Provinsi', 'lokasi_perizinan', 'Tahun', 'Status Lingkungan', 'deforestasi', 'luas_ha']].sort_values(by=['Tahun', 'Provinsi'], ascending=[False, True])
    df_show_raw.columns = ['Nama Perusahaan (IUP)', 'Nomor SK Izin', 'Tahap Kegiatan', 'Komoditas', 'Provinsi', 'Lokasi Kabupaten/Kota', 'Tahun Terbit Izin', 'Kondisi Saat Izin Terbit', 'Kehilangan Hutan Provinsi Tersebut (Ha)', 'Luas Konsesi Izin Baru (Ha)']

# ─── SECTION 7.2 VISUALS ─────────────────────────────────────────────────────
print("Rendering 7.2 Chart ...")
total_konflik_hukum = len(df_konflik_hukum)
sektor_counts = df_konflik_hukum['Sektor'].value_counts().reset_index()
sektor_counts.columns = ['Sektor (Penyebab)', 'Jumlah Kasus']

if 'Tahun' in df_konflik_hukum.columns and df_konflik_hukum['Tahun'].notna().any():
    df_timeline = df_konflik_hukum.dropna(subset=['Tahun']).copy()
    df_timeline['Tahun'] = df_timeline['Tahun'].astype(int)
    df_timeline = df_timeline[df_timeline['Tahun'] >= 2014]
    timeline_counts = df_timeline.groupby(['Tahun', 'Provinsi']).size().reset_index(name='Jumlah Kasus')
    red_shades = ['#67000d', '#a50f15', '#cb181d', '#ef3b2c', '#fb6a4a', '#fc9272']
    fig_konflik_hukum = px.bar(timeline_counts, x='Tahun', y='Jumlah Kasus', color='Provinsi', title="Timeline Letusan Konflik Agraria (10 Tahun Terakhir)", color_discrete_sequence=red_shades)
    fig_konflik_hukum.update_xaxes(dtick=1)
else:
    prov_counts = df_konflik_hukum['Provinsi'].value_counts().reset_index()
    prov_counts.columns = ['Provinsi', 'Jumlah Kasus']
    fig_konflik_hukum = px.bar(prov_counts, x='Jumlah Kasus', y='Provinsi', orientation='h', title="Sebaran Wilayah Konflik (Hingga 2024)", color='Jumlah Kasus', color_continuous_scale='Reds')

fig_konflik_hukum.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(color='#333'), margin=dict(l=0, r=0, t=40, b=0))
save_plotly(fig_konflik_hukum, VIS / "chart_7_2_konflik_hukum.png", w=900, h=450)

# ─── SECTION 7.3 VISUALS ─────────────────────────────────────────────────────
print("Rendering 7.3 Chart ...")
total_pltu_unit = len(df_pltu_captive)
total_mw = df_pltu_captive['Capacity (MW)'].sum()

df_pltu_captive['Provinsi'] = df_pltu_captive['Subnational unit (province, state)']
df_pltu_captive['Tahun'] = df_pltu_captive['Start year'].fillna(2025).astype(int)
df_timeline_pltu = df_pltu_captive[df_pltu_captive['Tahun'] <= 2024].groupby(['Provinsi', 'Tahun'])['Capacity (MW)'].sum().reset_index()
df_pivot = df_timeline_pltu.pivot(index='Tahun', columns='Provinsi', values='Capacity (MW)').fillna(0)
all_years = list(range(df_pivot.index.min(), 2025))
df_pivot = df_pivot.reindex(all_years, fill_value=0)
df_cum = df_pivot.cumsum().reset_index()
df_melt = df_cum.melt(id_vars='Tahun', value_name='Capacity (MW)')

fig_pltu_timeline = px.line(df_melt, x='Tahun', y='Capacity (MW)', color='Provinsi', markers=True, title="Timeline Pertumbuhan Kapasitas PLTU Captive (Hingga 2024)", color_discrete_sequence=px.colors.qualitative.Set1)
fig_pltu_timeline.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(color='#333'), margin=dict(l=0, r=0, t=40, b=0), height=450)
save_plotly(fig_pltu_timeline, VIS / "chart_7_3_pltu_captive_timeline.png", w=900, h=450)

# ─── BUILD MARKDOWN ──────────────────────────────────────────────────────────
print("Writing 100% faithful chapter_7.md ...")

md = f"""# Bab 7: Kegagalan Tata Kelola: D3TLH Dalam Sistem Perizinan

**CELIOS — Center of Economic and Law Studies**

*Evaluasi instrumen perlindungan ekologis dan implementasinya dalam sistem perizinan.*

---

## Ringkasan Tata Kelola
| Indikator | Kondisi Aktual | Deskripsi |
|---|---|---|
| **Fungsi Pembatas Daya Dukung** | **Penerbitan Izin Lanjut** | Data menunjukkan perlunya penguatan fungsi D3TLH sebagai instrumen pengaman. Penerbitan izin baru masih berlangsung di kawasan yang tercatat mengalami tekanan lingkungan tinggi. |
| **Pengawasan & Penegakan Hukum** | **Tantangan Sanksi** | Evaluasi menunjukkan tantangan dalam penegakan sanksi administratif dan pengawasan perizinan bagi entitas yang beroperasi tidak sesuai ketentuan. |

---

## Metodologi Pendekatan & Pertanyaan Kritis

**Membaca Hubungan Antara Hasil D3TLH dan Keputusan Perizinan Aktual**

Analisis di halaman ini menggunakan **Matriks Analisis Crosstab** untuk menjawab 3 pertanyaan fundamental:
1. **Apakah D3TLH digunakan sebagai dasar keputusan?**
2. **Apakah D3TLH bersifat mengikat atau hanya rekomendasi?**
3. **Apakah D3TLH dapat diabaikan secara prosedural?**

*Kerangka Pengujian:* Menyilangkan Data Fase Status Ekologis (Aman / Tertekan / Kritis) dengan Data Empiris Keputusan Izin yang benar-benar diterbitkan negara.

---

Dokumen tata ruang dan Daya Dukung Daya Tampung Lingkungan Hidup (D3TLH) dirancang sebagai instrumen pengendalian investasi agar tidak melampaui kapasitas daya dukung lingkungan. Penelusuran *timeline* penerbitan izin di Sulawesi mengindikasikan perlunya penguatan efektivitas instrumen ini dalam proses perizinan usaha pertambangan dan infrastruktur pendukungnya.

---

## 7.1 Pembuktian Empiris: Status Ekologis vs Penerbitan Izin

**Metode: Spatial Overlay & Crosstabulation (ESDM x GFW)**

### Metodologi: Evaluasi Kepatuhan D3TLH Berdasarkan Data Historis

**Metode Analisis:** Sub-bab ini menggunakan agregasi berbasis aturan (*Rule-based Categorization*) untuk membedah ketidaksesuaian antara status kerusakan lingkungan dengan keputusan administratif perizinan.

1. **Model Evaluasi Pelanggaran (*Compliance Modeling*):**
    * **Kategorisasi Status (Binning):** Nilai kerusakan lingkungan absolut dibagi ke dalam tiga kelas menggunakan distribusi *percentile*: Aman (≤33%), Tertekan (33-66%), dan Kritis (>66%).
    * **Kuantifikasi Pelanggaran D3TLH:** Mengidentifikasi secara kuantitatif apakah pemerintah tetap mengobral Izin Usaha Pertambangan (IUP) baru pada wilayah-wilayah yang secara empiris terbukti telah berada di fase 'Kritis'.
2. **Kalkulasi/Formula Pengolahan:**
    * `Ambang_Kritis = Percentile(Deforestasi, 0.66)`
    * `Total_Izin_Ilegal_Ekologis = SUM(IUP_Baru) WHERE Status_D3TLH = 'Kritis'`
3. **Variabel & Fitur Data:**
    * **Variabel Konteks Lingkungan:** `Total_Deforestasi_Ha` atau `Deforestasi_Driver_Komoditas...` (sebagai basis status wilayah)
    * **Variabel Keputusan Aktor:** `Jumlah_Izin_Baru` dan `Total_Luas_Konsesi_Baru_Ha`
4. **Dataset & File:**
    * `data/processed/sulawesi_izin_baru_per_tahun.csv` dan `sulawesi_gfw_master_1_dekade_2014_2023.csv`

---

Daya Tampung dan Daya Dukung Lingkungan Hidup (D3TLH) dirancang sebagai instrumen pencegahan dan pengatur batas pengaman ekologis (*ecological safeguard*). Secara umum, penerbitan izin baru sepatutnya mempertimbangkan indikator daya dukung lingkungan guna mengantisipasi degradasi ekosistem.

Penyandingan data deforestasi tahunan dari *Global Forest Watch* (GFW) dan data perizinan pertambangan dari *Minerba One Data Indonesia* (MODI) Kementerian ESDM menunjukkan bahwa penerbitan izin usaha pertambangan baru tetap tercatat pada kurun waktu ketika perubahan tutupan hutan meningkat. Hal ini terlihat pada tren di wilayah Sulawesi Tengah dan Tenggara periode 2014-2023.

Kondisi ini menggarisbawahi pentingnya penguatan fungsi dokumen AMDAL, D3TLH, dan KLHS agar menjadi pertimbangan utama yang mengikat dalam pengambilan keputusan perizinan, demi menjaga keberlanjutan lingkungan dan kehidupan masyarakat sekitar.

Matriks Statistik di bawah ini menyajikan perbandingan indikator status ekologis dan penerbitan izin.

### Konklusi Analisis Kepatuhan D3TLH Berdasarkan Data Historis

Tabel pembuktian di bawah ini mengukur akumulasi penerbitan izin pada rentang waktu ketika wilayah berstatus Aman, Tertekan, hingga Kritis secara aktual. Apabila pada status Kritis izin masih diterbitkan, hal tersebut secara matematis mendiskualifikasi D3TLH sebagai instrumen perlindungan lingkungan.

{table_crosstab_md}

> **Temuan Target:**
> - **Fungsi pembatas D3TLH perlu ditingkatkan** (Terdapat **{int(total_iup_kritis)}** Izin Baru yang terbit pada periode berstatus deforestasi tinggi).
> - **Diperlukan penguatan integrasi data lingkungan dalam keputusan perizinan**.

**Metodologi Pembuktian (100% Data-Driven)**

Daftar di bawah ini adalah **Tabel Irisan (Intersection)** yang menyatukan Data Satelit (GFW) dan Data Perizinan (ESDM Minerba One).
Sistem secara otomatis melacak dan menarik nama-nama perusahaan yang SK IUP-nya ditandatangani persis pada Tahun dan Provinsi yang sedang berstatus Kritis akibat deforestasi.

#### Tabel Irisan: Daftar Izin IUP Baru yang Diterbitkan di Tengah Situasi Kritis

*(Tabel dapat dilihat pada versi interaktif web).*

---

## 7.2 Tabrakan Hukum: Impunitas dan Pembiaran Operasi Ilegal

**Impunitas Korporasi dan Pembiaran Konflik Struktural di Sektor Ekstraktif**

**Metode: Thematic Coding & Analisis Kasus (LSM / KPA / Tanah Kita)**

### Metodologi: Pemetaan Impunitas Korporasi

**Metode Analisis:** Sub-bab ini menggunakan agregasi pelaporan berbasis insiden (*Incident-based Reporting Aggregation*) untuk mengukur tingkat pembiaran penegakan hukum (impunitas).

1. **Model Penelusuran Anomali Hukum:**
    * **Kasus Rekam Jejak:** Menyaring dan mengklasifikasikan database konflik sengketa lahan, pelanggaran HAM, dan kasus operasi ilegal tanpa izin di level tapak.
    * **Pemetaan Pembiaran (*State Omission*):** Menghitung total volume agregat di mana korporasi yang terbukti bermasalah secara hukum tetap dipertahankan keberadaan operasinya oleh aparatur negara.
2. **Kalkulasi/Formula Pengolahan:**
    * `Total_Kasus_Impunitas = COUNT(Judul_Kasus)`
    * `Volume_Pembiaran_Sektoral = SUM(Kasus) GROUP BY Sektor`
3. **Variabel & Fitur Data:**
    * **Atribut Laporan:** `Provinsi`, `Sektor`, `Judul_Kasus`, `Deskripsi_Singkat`
4. **Dataset & File:**
    * `data/processed/sulawesi_konflik_hukum.csv`

---

Konsep Daya Tampung dan Daya Dukung Lingkungan Hidup (D3TLH) mengukur kapasitas daya tahan ekosistem serta daya dukung sosial masyarakat di sekitar kawasan industri. Kompilasi laporan masyarakat sipil dan organisasi terkait mencatat adanya sengketa tanah dan dinamika sosial dalam ekspansi industri ekstraktif.

Hal ini menunjukkan pentingnya kepatuhan perizinan dan penerapan sanksi administratif secara konsisten. Pengawasan terhadap batas wilayah perizinan (HGU/IUP) serta pelaksanaan konsultasi publik (FPIC) menjadi aspek penting dalam tata kelola pertanahan dan lingkungan.

Penguatan koordinasi antar-instansi serta penyelesaian sengketa tenurial secara adil menjadi langkah krusial untuk memastikan kepastian hukum dan perlindungan hak masyarakat di wilayah sekitar industri.

| Indikator Evaluasi | Nilai | Keterangan |
|---|---|---|
| **Total Kasus Tercatat** | **{total_konflik_hukum} Kasus** | Dinamika Konflik di Sulawesi (KPA/LSM) |

![Timeline Letusan Konflik Agraria](visuals_bab7/chart_7_2_konflik_hukum.png)

---

## 7.3 Inkonsistensi Iklim: Karpet Merah PLTU Captive

**Paradoks Hilirisasi Hijau dan Karpet Merah untuk PLTU Batubara Captive**

**Metode: Penyaringan Agregat Dataset Eksternal (Global Coal Plant Tracker GEM)**

### Metodologi: Agregasi Beban Karbon PLTU Captive

**Metode Analisis:** Sub-bab ini menggunakan inventarisasi agregat kuantitatif (*Quantitative Inventory Aggregation*) dari database global PLTU batubara independen (*captive*).

1. **Model Ekstraksi Kapasitas Fosil:**
    * **Isolasi Regional:** Melakukan pemfilteran data inventaris energi kotor (PLTU) yang berlokasi secara presisi di kawasan industri strategis pulau Sulawesi.
    * **Kuantifikasi Kontradiksi Karbon:** Menghitung total jumlah *unit* pembangkit dan agregat luaran listrik kotor (dalam satuan Megawatt) yang dibangun secara masif demi menopang pabrik pemurnian nikel, yang notabene dipromosikan sebagai proyek energi ramah lingkungan.
2. **Kalkulasi/Formula Pengolahan:**
    * `Total_Beban_Karbon = SUM(Capacity_MW) GROUP BY Provinsi`
    * `Total_Infrastruktur_Kotor = COUNT(Unit_PLTU)`
3. **Variabel & Fitur Data:**
    * **Spesifikasi Pembangkit:** `Capacity (MW)`, `Start year`, `Provinsi (Subnational unit)`
4. **Dataset & File:**
    * `data/processed/sulawesi_pltu_captive.csv`

---

Komitmen transisi energi global dan pengembangan rantai pasok industri nikel memegang peranan strategis. Di saat yang sama, pemenuhan kebutuhan energi untuk fasilitas pengolahan nikel (*smelter*) di Sulawesi masih didominasi oleh Pembangkit Listrik Tenaga Uap (PLTU) Batubara *Captive*.

Data dari *Global Coal Plant Tracker* (GEM) mencatat keberadaan unit PLTU *Captive* yang beroperasi maupun direncanakan di kawasan industri Sulawesi Tengah dan Sulawesi Tenggara. Pemanfaatan energi berbasis batu bara pada industri ini menghasilkan tantangan tersendiri bagi pengelolaan emisi gas rumah kaca dan kualitas udara ambien.

Kondisi ini menunjukkan perlunya strategi percepatan transisi energi bersih di sektor industri ekstraktif guna menyelaraskan target hilirisasi dengan komitmen penurunan emisi nasional.

| Indikator PLTU Captive | Nilai | Keterangan |
|---|---|---|
| **Total Unit PLTU Captive** | **{total_pltu_unit} Unit** | Beroperasi/Dibangun/Direncanakan Khusus Kawasan Sulawesi |
| **Total Kapasitas Pembangkitan Kotor** | **{total_mw:,.0f} MW** | Pembangkit Fosil Penopang Smelter |

![Timeline Pertumbuhan Kapasitas PLTU Captive](visuals_bab7/chart_7_3_pltu_captive_timeline.png)
"""

out_path = HERE / "chapter_7.md"
out_path.write_text(md, encoding="utf-8")
print(f"Done! 100% faithful chapter_7.md saved to {out_path}")
