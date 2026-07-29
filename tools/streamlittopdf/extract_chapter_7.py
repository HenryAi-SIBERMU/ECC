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

*Evaluasi terhadap kelumpuhan supremasi hukum di mana instrumen perlindungan ekologis direduksi menjadi stempel administratif.*

---

## Metodologi Pendekatan & Pertanyaan Kritis

**Membaca Hubungan Antara Hasil D3TLH dan Keputusan Perizinan Aktual**

Analisis di halaman ini menggunakan **Matriks Analisis Crosstab** untuk menjawab 3 pertanyaan fundamental:
1. **Apakah D3TLH digunakan sebagai dasar keputusan?**
2. **Apakah D3TLH bersifat mengikat atau hanya rekomendasi?**
3. **Apakah D3TLH dapat diabaikan secara prosedural?**

*Kerangka Pengujian:* Menyilangkan Data Fase Status Ekologis (Aman / Tertekan / Kritis) dengan Data Empiris Keputusan Izin yang benar-benar diterbitkan negara.

---

Secara hukum, dokumen tata ruang dan Daya Dukung Daya Tampung Lingkungan Hidup (D3TLH) dirancang sebagai **veto absolut** negara—sebuah instrumen yang memiliki otoritas untuk menolak izin investasi baru manakala beban lingkungan hidup di suatu ekoregion telah melampaui kapasitas pemulihannya. Namun, matriks forensik yang membedah *timeline* penerbitan izin di semenanjung Sulawesi membongkar skandal **Regulatory Capture**. Negara, melalui aparatus perizinannya, terbukti mendelegitimasi instrumen penyelamatannya sendiri. Dokumen AMDAL dan D3TLH diposisikan bukan sebagai garis merah hukum (*redline*), melainkan sekadar ornamen pelengkap persyaratan untuk merestui perluasan tambang dan pembangunan masif PLTU captive.

---

## Temuan Kunci Tata Kelola

| Indikator | Status / Nilai | Keterangan |
|---|---|---|
| **Skor Tata Kelola (Veto)** | **9.8 / 10** | Tingkat keparahan kegagalan fungsi D3TLH sebagai pembatas. **Vonis: Regulatory Capture.** (Indeks Komposit CELIOS) |
| **Otoritas D3TLH** | **Nihil** | Instrumen lingkungan terbukti tidak mengikat dan gagal membatasi laju obral perizinan secara nyata di lapangan. |
| **Status Penegakan Hukum** | **Pembiaran** | Masifnya temuan perusahaan beroperasi secara ilegal tanpa dikenakan sanksi pencabutan izin operasi (Impunitas massal). |

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

Dalih "sudah sesuai aturan" sering kali digunakan oleh pemerintah daerah maupun pusat untuk membenarkan penerbitan Izin Usaha Pertambangan (IUP) yang masif di Pulau Sulawesi. Namun, jika Daya Tampung dan Daya Dukung Lingkungan Hidup (D3TLH) benar-benar dijadikan sebagai instrumen pencegahan dan batas pengaman ekologis (*ecological safeguard*), maka secara logika hukum dan sains, laju penerbitan izin baru wajib dihentikan seketika saat sebuah wilayah telah menunjukkan gejala kerusakan ekstrem, seperti deforestasi besar-besaran. Kenyataannya, data spasial menunjukkan sebuah anomali fatal: grafik penerbitan izin justru melonjak eksponensial tepat di tahun-tahun ketika hilangnya tutupan pohon sekunder dan primer mencapai titik kritis.

Kami menyilangkan data deforestasi tahunan dari *Global Forest Watch* (GFW) dengan riwayat penerbitan izin pertambangan dari *Minerba One Data Indonesia* (MODI) Kementerian ESDM. Hasil irisan tersebut memperlihatkan pola *business-as-usual* yang sangat agresif. Sebagai contoh, ketika jutaan hektar hutan di Sulawesi Tengah dan Tenggara ditebang secara brutal pada periode 2014 hingga 2023 untuk membuka jalan bagi kawasan industri (smelter) dan infrastruktur pendukungnya, pemerintah secara bersamaan terus mencetak ratusan Izin Usaha Pertambangan baru di provinsi-provinsi yang sama, tanpa mempertimbangkan bahwa kapasitas hidrologis dan daya dukung lanskap di wilayah tersebut sudah ambruk total.

Fakta bahwa perizinan konsesi tetap mengalir deras di zona-zona merah ini membuktikan kegagalan tata kelola yang sistemik. D3TLH, Analisis Mengenai Dampak Lingkungan (AMDAL), maupun instrumen Kajian Lingkungan Hidup Strategis (KLHS) telah direduksi menjadi sekadar stempel administratif formalitas belaka. Alih-alih menjadi rem darurat bagi kerusakan, dokumen-dokumen lingkungan tersebut ditundukkan oleh tekanan investasi dan target pertumbuhan produksi nikel nasional. Kegagalan otoritas dalam menggunakan data riil kerusakan lapangan sebagai dasar penghentian operasi atau moratorium izin ini pada akhirnya mempercepat laju krisis ekologis yang kini harus ditanggung sepenuhnya oleh masyarakat pesisir, petani, dan nelayan yang kehilangan ruang hidup mereka. Kehancuran ini bukan lagi kecelakaan, melainkan hasil dari kebijakan pembiaran (*state-sponsored ecocide*).

Matriks Statistik di bawah ini digunakan untuk membuktikan secara kuantitatif jejak kelumpuhan tata kelola (*Governance Failure*) tersebut.

### Konklusi Analisis Kepatuhan D3TLH Berdasarkan Data Historis

Tabel pembuktian di bawah ini mengukur akumulasi penerbitan izin pada rentang waktu ketika wilayah berstatus Aman, Tertekan, hingga Kritis secara aktual. Apabila pada status Kritis izin masih diterbitkan, hal tersebut secara matematis mendiskualifikasi D3TLH sebagai instrumen perlindungan lingkungan.

{table_crosstab_md}

> **Temuan Target:**
> - **Daya dukung tidak menjadi pembatas nyata** (Terdapat **{int(total_iup_kritis)} Izin Baru** yang tetap sengaja diterbitkan ketika lingkungan sudah terkonfirmasi berada di fase Kritis).
> - **Keputusan perizinan tetap dominan secara politis** meski D3TLH menunjukkan kondisi kritis (Bukti *Regulatory Capture* mutlak).

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

Konsep Daya Tampung dan Daya Dukung Lingkungan Hidup (D3TLH) secara esensial tidak hanya mengukur batas fisik daya tahan ekosistem darat, air, dan udara, tetapi juga mengukur sejauh mana ruang hidup sosial masyarakat mampu menoleransi masuknya investasi skala raksasa. Namun, realitas di lapangan menunjukkan bahwa ambang batas sosial ini telah dilanggar secara brutal dan sistematis. Berdasarkan kompilasi data laporan masyarakat sipil, Jaringan Advokasi, serta Konsorsium Pembaruan Agraria (KPA), kami menemukan bahwa ekspansi industri ekstraktif di Sulawesi—mulai dari pertambangan nikel, perkebunan monokultur, hingga pembangunan kawasan industri strategis nasional (PSN)—selalu beriringan dengan letusan konflik agraria yang memakan korban di pihak masyarakat akar rumput.

Pembiaran atas pelanggaran hukum (impunitas) terlihat sangat telanjang. Perusahaan-perusahaan yang terbukti merebut lahan tanpa persetujuan bebas, diinformasikan di awal, dan tanpa paksaan atau *Free, Prior and Informed Consent* (FPIC) dari masyarakat adat maupun penduduk lokal, tetap dibiarkan beroperasi dengan leluasa. Dalam berbagai kasus, korporasi tambang maupun perkebunan yang status izin (HGU/IUP)-nya tumpang tindih dengan tanah ulayat, atau bahkan beroperasi di luar konsesi yang sah, tidak pernah mendapatkan sanksi administratif berupa pencabutan izin. Aparat penegak hukum justru kerap digunakan sebagai instrumen represi untuk membungkam protest warga, mengkriminalisasi petani yang mempertahankan kebunnya, serta menyingkirkan masyarakat yang bermukim di sekitar area lingkar tambang.

Absennya sanksi tegas dari Kementerian Lingkungan Hidup, Kementerian ESDM, maupun aparat hukum mencerminkan adanya perlindungan politik yang kuat terhadap operasi bisnis kotor ini. Konflik tenurial yang terjadi di Morowali, Konawe, hingga Wawonii membuktikan bahwa instrumen hukum yang seharusnya melindungi rakyat telah dibajak demi memfasilitasi akumulasi modal. Pembiaran ini menciptakan tabrakan hukum di mana regulasi perlindungan lingkungan hidup dan hak asasi manusia kalah secara sistemik oleh undang-undang sektoral pro-investasi seperti UU Cipta Kerja dan UU Minerba revisi terbaru. Kegagalan menegakkan hukum ini pada akhirnya mengonfirmasi bahwa negara secara sadar menoleransi kekerasan struktural dan kerusakan lingkungan sebagai harga yang wajar demi pencapaian target industri hilirisasi, mengubah wilayah-wilayah krisis tersebut menjadi zona pengorbanan (*sacrifice zones*).

| Indikator Impunitas | Nilai | Keterangan |
|---|---|---|
| **Total Kasus Konflik/Pelanggaran Dibiarkan** | **{total_konflik_hukum} Kasus** | Bukti Impunitas Hukum di Sulawesi (KPA/LSM) |

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

Di panggung negosiasi iklim internasional, pemerintah secara retoris selalu mempromosikan komitmen Indonesia dalam transisi energi menuju target *Net Zero Emission* serta mengkampanyekan keberhasilan program "Hilirisasi Hijau" untuk mendukung rantai pasok kendaraan listrik (EV) global. Namun, ironi terbesar dan paling memalukan dari narasi transisi energi tersebut terbentang sangat nyata di pulau Sulawesi. Demi memenuhi kebutuhan listrik raksasa untuk operasional pabrik pemurnian (*smelter*) nikel, pemerintah memberikan karpet merah perizinan untuk pembangunan puluhan Pembangkit Listrik Tenaga Uap (PLTU) Batubara *Captive*. Pembangkit-pembangkit kotor ini dibangun secara mandiri di dalam kawasan industri dan berdiri di luar sistem jaringan (grid) PLN nasional, sehingga keberadaannya sering kali luput dari skema pembatasan emisi atau target penghentian batubara (*coal phase-out*).

Ekstraksi data terbaru dari *Global Coal Plant Tracker* (GEM) membongkar skalanya yang masif dan mengerikan. Kami menemukan bahwa terdapat puluhan unit PLTU *Captive*—baik yang sudah beroperasi secara aktif, sedang dalam tahap konstruksi, maupun yang telah mendapatkan izin (*permitted/announced*)—yang tersebar di sentra-sentra industri di Sulawesi Tengah, Sulawesi Tenggara, dan provinsi lainnya. Total kapasitas kotor pembangkitan dari puluhan PLTU batubara ini mencapai belasan ribu Megawatt. Ini berarti, proses pengolahan material nikel yang diklaim sebagai bahan baku energi bersih masa depan (baterai kendaraan listrik) justru diproduksi dengan membakar jutaan metrik ton batu bara setiap tahunnya, menyemburkan polutan mematikan seperti SO2, NOx, dan PM2.5 langsung ke ruang udara pemukiman warga sekitar.

Inkonsistensi kebijakan ini jelas menunjukkan kegagalan tata kelola iklim yang paling telanjang. Transisi energi dalam konteks hilirisasi nikel di Indonesia tidak lebih dari sekadar *greenwashing*, di mana perlindungan daya dukung udara dikorbankan demi profitabilitas ekonomi. Emisi Gas Rumah Kaca (GRK) dari Sulawesi justru meledak secara dramatis berkat kehadiran PLTU *Captive* ini. Dengan terus memberikan izin baru bagi pembangkit listrik berbahan bakar fosil terburuk di bumi ini, pemerintah tidak hanya mengkhianati komitmen penurunan emisinya sendiri, tetapi juga menjerumuskan masyarakat lokal ke dalam kondisi kerentanan kesehatan pernapasan akut yang tak terpulihkan.

| Indikator PLTU Captive | Nilai | Keterangan |
|---|---|---|
| **Total Unit PLTU Captive** | **{total_pltu_unit} Unit** | Beroperasi/Dibangun/Direncanakan Khusus Kawasan Sulawesi |
| **Total Kapasitas Pembangkitan Kotor** | **{total_mw:,.0f} MW** | Pembangkit Fosil Penopang Smelter |

![Timeline Pertumbuhan Kapasitas PLTU Captive](visuals_bab7/chart_7_3_pltu_captive_timeline.png)
"""

out_path = HERE / "chapter_7.md"
out_path.write_text(md, encoding="utf-8")
print(f"Done! 100% faithful chapter_7.md saved to {out_path}")
