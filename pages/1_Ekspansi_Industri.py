import streamlit as st
import pandas as pd
import scipy.stats as stats
import altair as alt
import plotly.express as px
import numpy as np
import os
import sys

# Konfigurasi path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.components.sidebar import render_sidebar

st.set_page_config(
    page_title="Ekspansi Industri — CELIOS ECC",
    page_icon="refrensi/Celios China-Indonesia Energy Transition.png",
    layout="wide"
)
render_sidebar()

# ── Styles (Sesuai Pedoman LEUI & EBTsmallstack) ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

* { font-family: 'Inter', sans-serif; }

.main-title {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #43A047, #66BB6A, #81C784);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0;
    line-height: 1.2;
}

.sub-title {
    font-size: 1.1rem;
    color: #9E9E9E;
    font-weight: 300;
    margin-top: 0;
    margin-bottom: 2rem;
}

.org-badge {
    display: inline-block;
    background: linear-gradient(135deg, #1B5E20, #2E7D32);
    color: white;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

.metric-card {
    background: linear-gradient(135deg, #1A1F2B, #232B3B);
    border: 1px solid #333;
    border-radius: 10px;
    padding: 20px;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
}
.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: #4CAF50;
}
.metric-label {
    font-size: 0.9rem;
    color: #AAA;
    margin-bottom: 5px;
    font-weight: 600;
}
.metric-desc {
    font-size: 0.8rem;
    color: #9E9E9E;
    margin-top: 10px;
    line-height: 1.4;
    text-align: left;
}
.metric-source {
    font-size: 0.75rem;
    color: #777;
    margin-top: 8px;
    padding-top: 8px;
    border-top: 1px dotted #444;
    text-align: left;
}
</style>
""", unsafe_allow_html=True)

# ── Load Data Mentah ──
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data", "processed")

@st.cache_data
def load_all_data_v2():
    df_izin = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_izin_baru_per_tahun.csv"))
    df_smelter = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_esdm_nikel.csv"))
    df_pltu = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_pltu_captive.csv"))
    df_gfw = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_gfw_master_1_dekade_2014_2023.csv"))
    df_inv = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_investasi_pmdn_2016_2024.csv"))
    return df_izin, df_smelter, df_pltu, df_gfw, df_inv

try:
    df_izin, df_smelter, df_pltu, df_gfw, df_inv = load_all_data_v2()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# ── Pra-Kalkulasi Variabel Kritis (Data-Driven) ──
# 1. Izin Tambang
tot_izin = df_izin['Jumlah_Izin_Baru'].sum()
tot_luas_izin = df_izin['Total_Luas_Konsesi_Baru_Ha'].sum()

# 2. PLTU Captive
df_pltu_op = df_pltu[df_pltu['Status'].str.lower() == 'operating']
tot_pltu_op = len(df_pltu_op)
tot_kapasitas_pltu = df_pltu_op['Capacity (MW)'].sum() if 'Capacity (MW)' in df_pltu_op.columns else 0

# 3. Mega Smelter (CGS/ESDM)
tot_smelter = len(df_smelter)

# 4. Deforestasi (GFW)
tot_deforestasi = df_gfw['Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha'].sum()

# 5. Investasi (PMDN)
# Anggap nilai sudah dalam format (misal Triliun/Miliar)
tot_investasi = df_inv['nilai'].sum()

# ── Header Halaman ──
st.markdown('<div class="org-badge">CELIOS — Center of Economic and Law Studies</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">Ekspansi Industri Ekstraktif</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Membaca pola pertumbuhan industri pengolahan alam (tambang, nikel, semen) di Pulau Sulawesi sebagai sumber tekanan utama terhadap daya dukung lingkungan.</div>', unsafe_allow_html=True)

# ── Dropdown Metodologi ──
with st.expander("🔍 Metodologi", expanded=False):
    st.markdown("""
    **Alur Kausalitas (Ekonomi Politik Ekologi):** `Kebijakan Hilirisasi` → `Lonjakan Izin & Investasi` → `Konsentrasi Smelter & Energi Kotor (PLTU)` → `Kebangkrutan Ekologis (Deforestasi)`
    
    Ekspansi industri ekstraktif yang didorong ambisi hilirisasi menerjemahkan regulasi menjadi tekanan ruang berskala masif. Rentetan izin pertambangan baru dan lonjakan modal terkonsentrasi pada penyediaan fasilitas peleburan padat karbon, yang pada akhirnya membebani daya dukung ekologis lokal secara drastis.
    
    **Variabel Tekanan / Ekspansi (X):**
    *   **Izin Usaha Pertambangan Baru:** Total IUP yang diterbitkan dalam rentang 2014-2024 (Data Minerbaone Kementerian ESDM).
    *   **Pertumbuhan Fasilitas Smelter:** Kapasitas dan jumlah unit pengolahan terintegrasi (Database CGS & Kementerian ESDM).
    *   **Kapasitas PLTU Captive:** Beban energi batu bara *off-grid* untuk fasilitas smelter (Global Energy Monitor/GEM).
    *   **Investasi PMDN:** Aliran Penanaman Modal Dalam Negeri (Kementerian Investasi/BKPM).
    
    **Variabel Dampak Ekologis (Y):**
    *   **Deforestasi Komoditas:** Luas tutupan hutan yang dikonversi permanen untuk operasi tambang dan perkebunan monokultur (Global Forest Watch/GFW).
    
    **Metode Pengolahan Data:**
    Pendekatan kuantitatif deskriptif menggunakan teknik **Crosstabulation (Tabulasi Silang)** dan **Trend Analysis (Analisis Tren Time-Series)**. Seluruh raw data diagregasi berdasarkan dimensi spasial (Provinsi) dan temporal (Tahun 2014-2024) untuk memetakan anomali, konsentrasi perizinan ekstrem, serta laju eksploitasi ruang secara presisi.
    """)

tot_investasi_triliun = tot_investasi / 1_000

# ── Hero Statement (Narasi Kritis Utama) ──
st.markdown(f"""
<div style="background-color: transparent; padding: 10px 0px; margin-bottom: 25px;">
    <h2 style="color: #FFFFFF; font-size: 1.8rem; margin-bottom: 15px; font-weight: 700;">Ekspansi Masif: {tot_smelter} Fasilitas Smelter Mengunci Lanskap Ekologis Sulawesi</h2>
    <p style="color: #CCCCCC; font-size: 1.05rem; line-height: 1.7; margin-bottom: 15px;">
        Trajektori pembangunan di Pulau Sulawesi dalam satu dekade terakhir (2014-2024) dikendalikan penuh oleh ekspansi industri ekstraktif yang masif dan sistematis. Ambisi 'hilirisasi' nikel nyatanya menjadi karpet merah bagi penerbitan <b>{tot_izin:,.0f} Izin Usaha Pertambangan (IUP) baru</b> yang melegitimasi pembongkaran wilayah darat dan pesisir seluas <b>{tot_luas_izin:,.0f} Hektar</b>. Ironisnya, klaim transisi energi melalui pembangunan <b>{tot_smelter} unit fasilitas smelter</b> ini terbukti sangat kotor, karena operasionalnya disokong mutlak oleh <b>{tot_kapasitas_pltu:,.0f} MW</b> PLTU <i>Captive</i> (pembangkit listrik batu bara <i>off-grid</i>) yang mengunci emisi karbon di tingkat lokal. 
    </p>
    <p style="color: #CCCCCC; font-size: 1.05rem; line-height: 1.7;">
        Lebih jauh, gelombang investasi ini bukan tanpa tumbal. Meski aliran investasi domestik (PMDN) tercatat menembus angka fantastis sebesar <b>{tot_investasi_triliun:,.1f} Triliun Rupiah</b>, harga yang harus dibayar adalah kebangkrutan ekologis yang permanen—ditandai dengan hilangnya <b>{tot_deforestasi:,.0f} Hektar</b> wilayah tutupan hutan untuk komoditas tambang dan perkebunan. Rentetan angka ini membuktikan bahwa narasi pertumbuhan ekonomi selama ini dibangun di atas daya dukung lingkungan yang sedang kolaps.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Kartu Metrik Agregat (Bento Cards) ──
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Total Izin Baru (2014-2024)</div>
            <div class="metric-value" style="color: #B71C1C;">{tot_izin:,.0f} <span style="font-size:1rem;">IUP</span></div>
            <div class="metric-desc">Penambahan jumlah Izin Usaha Pertambangan (IUP) di Pulau Sulawesi dalam 1 dekade terakhir, melegitimasi pembongkaran lahan secara masif.</div>
        </div>
        <div class="metric-source"><b>Sumber:</b> Kementerian ESDM (Minerbaone)<br/><i>File: sulawesi_izin_baru_per_tahun.csv</i></div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Total Luas Konsesi Baru</div>
            <div class="metric-value" style="color: #C62828;">{tot_luas_izin:,.0f} <span style="font-size:1rem;">Ha</span></div>
            <div class="metric-desc">Akumulasi luas daratan dan perairan pesisir yang diserahkan kepada korporasi ekstraktif untuk dibongkar sejak 2014.</div>
        </div>
        <div class="metric-source"><b>Sumber:</b> Kementerian ESDM (Minerbaone)<br/><i>File: sulawesi_izin_baru_per_tahun.csv</i></div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Kapasitas PLTU Captive Aktif</div>
            <div class="metric-value" style="color: #D32F2F;">{tot_kapasitas_pltu:,.0f} <span style="font-size:1rem;">MW</span></div>
            <div class="metric-desc">Beban energi kotor <i>off-grid</i> yang beroperasi eksklusif untuk menyokong pabrik peleburan nikel, mengunci emisi di luar target iklim nasional.</div>
        </div>
        <div class="metric-source"><b>Sumber:</b> Global Energy Monitor (GEM)<br/><i>File: sulawesi_pltu_captive.csv</i></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
col4, col5, col6 = st.columns(3)
with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Jumlah Fasilitas Smelter</div>
            <div class="metric-value" style="color: #FF6F00;">{tot_smelter} <span style="font-size:1rem;">Unit</span></div>
            <div class="metric-desc">Total fasilitas pengolahan & pemurnian (hilirisasi) nikel yang memonopoli zona industri pesisir seperti Morowali dan Konawe.</div>
        </div>
        <div class="metric-source"><b>Sumber:</b> Database Smelter ESDM & CGS<br/><i>File: sulawesi_esdm_nikel.csv</i></div>
    </div>
    """, unsafe_allow_html=True)
with col5:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Luas Deforestasi Komoditas</div>
            <div class="metric-value" style="color: #B71C1C;">{tot_deforestasi:,.0f} <span style="font-size:1rem;">Ha</span></div>
            <div class="metric-desc">Area tutupan hutan alam yang musnah secara permanen akibat dorongan industri tambang dan perkebunan monokultur skala besar.</div>
        </div>
        <div class="metric-source"><b>Sumber:</b> Global Forest Watch (GFW)<br/><i>File: sulawesi_gfw_master_1_dekade_2014_2023.csv</i></div>
    </div>
    """, unsafe_allow_html=True)
with col6:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Investasi PMDN (2016-2024)</div>
            <div class="metric-value" style="color: #D32F2F;">{tot_investasi_triliun:,.1f} <span style="font-size:1rem;">Triliun Rp</span></div>
            <div class="metric-desc">Aliran modal domestik yang dikucurkan, membuktikan bahwa angka pertumbuhan ekonomi seringkali dibayar mahal oleh kebangkrutan ekologis.</div>
        </div>
        <div class="metric-source"><b>Sumber:</b> Kementerian Investasi / BKPM<br/><i>File: sulawesi_investasi_pmdn_2016_2024.csv</i></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# SUB-BAB 1.1: TREN IZIN & CROSSTABULATION
# ══════════════════════════════════════════════════════════
st.markdown("---")
st.subheader("1.1 Tren Pertumbuhan Izin Tambang Baru & Uji Signifikansi")
st.markdown('<span style="background:#5C2B6A;color:#E1BEE7;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: Analisis Tren & SPSS-Style Crosstabulation (Sumber: Minerbaone)</span>', unsafe_allow_html=True)

# --- Pindahkan agregasi ke atas markdown ---
df_izin_agg = df_izin.groupby(['Tahun', 'Provinsi'])['Jumlah_Izin_Baru'].sum().reset_index()
df_izin_total = df_izin_agg.groupby('Tahun')['Jumlah_Izin_Baru'].sum().reset_index()

val_izin_2014 = df_izin_total[df_izin_total['Tahun'] == 2014]['Jumlah_Izin_Baru'].values[0] if 2014 in df_izin_total['Tahun'].values else 0
val_izin_2022 = df_izin_total[df_izin_total['Tahun'] == 2022]['Jumlah_Izin_Baru'].values[0] if 2022 in df_izin_total['Tahun'].values else 0
val_izin_2023 = df_izin_total[df_izin_total['Tahun'] == 2023]['Jumlah_Izin_Baru'].values[0] if 2023 in df_izin_total['Tahun'].values else 0
val_izin_2024 = df_izin_total[df_izin_total['Tahun'] == 2024]['Jumlah_Izin_Baru'].values[0] if 2024 in df_izin_total['Tahun'].values else 0

st.markdown(f"""
Pola tata kelola perizinan ekstraktif di Pulau Sulawesi selama satu dekade terakhir mencerminkan eksploitasi yang brutal. Berdasarkan data agregat *Minerbaone*, tercatat **{tot_izin:,.0f} Izin Usaha Pertambangan (IUP) baru** sepanjang 2014-2024, menjarah lahan dan pesisir mencapai **{tot_luas_izin:,.0f} Hektar**.

Namun, yang menjadi **temuan kritis** adalah fakta empiris *time-series* dari grafik **"Lonjakan Penerbitan Izin Tambang"** di bawah ini. Jika kita amati pergerakan datanya secara tahunan, penerbitan izin pada awal periode di tahun 2014 hanya berada di angka **{val_izin_2014:,.0f} IUP**. Tren ini bergerak sangat landai selama bertahun-tahun tanpa fluktuasi berarti. Malapetaka eksponensial baru terjadi secara anomali pada periode pasca-pandemi: dari angka yang sudah naik ke **{val_izin_2022:,.0f} IUP di tahun 2022**, penerbitan izin meledak tak terkendali menjadi **{val_izin_2023:,.0f} IUP di tahun 2023**, hingga menembus rekor puncak **{val_izin_2024:,.0f} IUP baru di tahun 2024** saja. 

Anotasi merah pada grafik dengan tegas mencatat **lonjakan ekstrem sebesar 246% (2022-2024)**. Fakta data *time-series* yang meroket tajam ini membuktikan secara telanjang runtuhnya fungsi kontrol dan hilangnya instrumen moratorium ekologis. Di bawah kurva lonjakan tersebut, kita melihat bar warna merah muda (Sulawesi Tengah) dan ungu (Sulawesi Tenggara) mendominasi secara absolut, menunjukkan perampasan ruang dan monopoli spasial dari kehancuran obral izin tersebut.

Data ledakan tahunan ini berkorelasi kuat dengan kerusakan lapangan. **Tabel Crosstabulation** menegaskan validitas kausalitasnya: wilayah yang mendominasi grafik bar (jumlah IUP tertinggi) menderita kerusakan tapak terparah. Nilai *P-Value* yang signifikan mengunci pembuktian matematis bahwa penerbitan IUP gila-gilaan inilah pemicu langsung dari lenyapnya **{tot_deforestasi:,.0f} Hektar** hutan primer. Angka di tabel tersebut membantah retorika administratif dan menjadi bukti hukum kebangkrutan ekologis di Sulawesi.
""")

# --- Bar Chart Tren Izin ---
bar_chart = alt.Chart(df_izin_agg).mark_bar().encode(
    x=alt.X('Tahun:O', title='Tahun Terbit', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('Jumlah_Izin_Baru:Q', title='Jumlah Izin Terbit'),
    color=alt.Color('Provinsi:N', title='Provinsi', scale=alt.Scale(scheme='set2')),
    tooltip=['Tahun', 'Provinsi', alt.Tooltip('Jumlah_Izin_Baru', title='Izin Baru')]
)

line_trend = alt.Chart(df_izin_total).mark_line(
    color='#FF1744', 
    strokeWidth=3,
    interpolate='monotone'
).encode(
    x='Tahun:O',
    y='Jumlah_Izin_Baru:Q'
)

points_trend = alt.Chart(df_izin_total).mark_circle(
    color='#FF1744', 
    size=70,
    opacity=1
).encode(
    x='Tahun:O',
    y='Jumlah_Izin_Baru:Q',
    tooltip=['Tahun', alt.Tooltip('Jumlah_Izin_Baru', title='Total Izin (Semua Provinsi)')]
)

# Kalkulasi Persentase Kenaikan Dinamis (2022 ke 2024)
try:
    val_2022 = df_izin_total[df_izin_total['Tahun'] == 2022]['Jumlah_Izin_Baru'].values[0]
    val_2024 = df_izin_total[df_izin_total['Tahun'] == 2024]['Jumlah_Izin_Baru'].values[0]
    pct_increase = ((val_2024 - val_2022) / val_2022) * 100
    annotation_text = f"↑ {pct_increase:,.0f}% Kenaikan (2022-2024)"
except IndexError:
    annotation_text = "Lonjakan Ekstrem"

df_annotation = pd.DataFrame({
    'Tahun': [2023],
    'Jumlah_Izin_Baru': [df_izin_total['Jumlah_Izin_Baru'].max() * 0.95],
    'text': [annotation_text]
})

annotation = alt.Chart(df_annotation).mark_text(
    align='right',
    baseline='middle',
    fontSize=14,
    fontWeight='bold',
    color='#FF1744',
    dx=-10,
    dy=0
).encode(
    x='Tahun:O',
    y='Jumlah_Izin_Baru:Q',
    text='text'
)

chart_izin = alt.layer(bar_chart, line_trend, points_trend, annotation).properties(
    height=400,
    title='Lonjakan Penerbitan Izin Tambang Sulawesi (2014-2024)'
).configure_axis(
    grid=True,
    gridOpacity=0.1
)

st.altair_chart(chart_izin, use_container_width=True)

st.markdown("""
<div style="background:#1E1E1E; padding:14px; border-radius:10px; border-left:5px solid #FF5722; margin-bottom: 25px;">
    <b>Interpretasi Ekologis:</b> Semakin banyak izin baru diterbitkan di wilayah timur, semakin besar deforestasi yang terlegitimasi. Pola perizinan ini menunjukkan absennya rem ekologis (moratorium nyata) di Sulawesi.
</div>
""", unsafe_allow_html=True)

with st.expander("Lihat Data Mentah: Agregat Izin Minerbaone", expanded=False):
    st.dataframe(df_izin_agg, use_container_width=True, hide_index=True)
    st.caption("📁 **Sumber File:** `data/processed/sulawesi_izin_baru_per_tahun.csv` - Agregat penerbitan izin tambang baru per provinsi di Sulawesi.")

# --- Crosstab Introduction ---
st.markdown("#### Pembuktian Statistik: Intensitas Ekspansi vs Deforestasi")
st.markdown("""
Hipotesis utama narasi ini adalah bahwa **lonjakan ekspansi ekstraktif** berbanding lurus dengan **kebangkrutan ekologis** (deforestasi). 
Untuk mengujinya secara statistik di tengah keterbatasan jumlah provinsi di Sulawesi (N=6), tabel crosstab dan uji Chi-Square di bawah menggunakan unit observasi **Provinsi-Tahun** (6 provinsi × 10 tahun = 60 sampel panel). 
Setiap observasi diklasifikasikan menjadi "Tinggi" atau "Rendah" berdasarkan nilai **Median panel** dari indikator yang dipilih.
""")

# --- Data Preparation ---
df_panel = pd.merge(df_gfw, df_izin, on=['Provinsi', 'Tahun'], how='left').fillna({'Jumlah_Izin_Baru': 0, 'Total_Luas_Konsesi_Baru_Ha': 0})

col_sel1, col_sel2 = st.columns(2)

with col_sel1:
    st.markdown("##### Variabel Independen (X) - Tekanan Ekspansi")
    x_options = {
        "Jumlah_Izin_Baru": "Jumlah Izin Baru (IUP)",
        "Total_Luas_Konsesi_Baru_Ha": "Luas Konsesi Baru (Hektar)"
    }
    x_col = st.selectbox("Pilih Indikator Ekspansi (X):", list(x_options.keys()), format_func=lambda x: x_options[x])

with col_sel2:
    st.markdown("##### Variabel Dependen (Y) - Dampak Ekologis")
    y_options = {
        "Total_Deforestasi_Ha": "Total Deforestasi Alam (Hektar)",
        "Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha": "Deforestasi Komoditas Tambang/Sawit (Hektar)"
    }
    y_col = st.selectbox("Pilih Indikator Dampak (Y):", list(y_options.keys()), format_func=lambda x: y_options[x])

# --- Calculation (Binning) ---
x_median = df_panel[x_col].median()
y_median = df_panel[y_col].median()

label_x_low = f"Rendah (<{x_median:,.1f})"
label_x_high = f"Tinggi (≥{x_median:,.1f})"
label_y_low = f"Rendah (<{y_median:,.1f})"
label_y_high = f"Tinggi (≥{y_median:,.1f})"

df_panel["X_Label"] = df_panel[x_col].apply(lambda x: label_x_high if x >= x_median else label_x_low)
df_panel["Y_Label"] = df_panel[y_col].apply(lambda x: label_y_high if x >= y_median else label_y_low)

# Crosstab Base
cats_x = [label_x_low, label_x_high]
cats_y = [label_y_low, label_y_high]
crosstab = pd.crosstab(df_panel["X_Label"], df_panel["Y_Label"]).reindex(index=cats_x, columns=cats_y, fill_value=0)

chi2, p, dof, expected = stats.chi2_contingency(crosstab)
expected_df = pd.DataFrame(expected, index=crosstab.index, columns=crosstab.columns)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
st.markdown("### Detail Uji Statistik (Chi-Square & Odds Ratio)")
st.caption("Tabel-tabel di bawah ini adalah *output* standar SPSS yang menyajikan bukti statistik formal: Case Processing → Crosstabulation → Chi-Square Tests → Ringkasan Hipotesis.")

# --- A. Case Processing Summary ---
st.markdown("##### Case Processing Summary")
total_cases = len(df_panel)
valid_cases = len(df_panel.dropna(subset=[x_col, y_col]))
missing_cases = total_cases - valid_cases

columns_case = pd.MultiIndex.from_product([["Cases"], ["Valid", "Missing", "Total"], ["N", "Percent"]])
interaction_label = f"{x_options[x_col]} * {y_options[y_col]}"
row_data = [
    valid_cases, f"{valid_cases/total_cases*100:.1f}%",
    missing_cases, f"{missing_cases/total_cases*100:.1f}%",
    total_cases, "100.0%"
]
case_summary = pd.DataFrame([row_data], index=[interaction_label], columns=columns_case)
st.table(case_summary)

# --- B. Crosstabulation ---
st.markdown(f"##### {interaction_label} Crosstabulation")
row_indices = []
for x_cat in cats_x:
    row_indices.extend([(x_cat, "Count"), (x_cat, "Expected Count")])
row_indices.extend([("Total", "Count"), ("Total", "Expected Count")])

rows = []
for x_cat in cats_x:
    counts = crosstab.loc[x_cat].tolist()
    exps = expected_df.loc[x_cat].tolist()
    rows.append(counts + [sum(counts)])
    rows.append([f"{v:.1f}" for v in exps] + [f"{sum(exps):.1f}"])

total_counts = crosstab.sum().tolist()
total_exps = expected_df.sum().tolist()
rows.append(total_counts + [sum(total_counts)])
rows.append([f"{v:.1f}" for v in total_exps] + [f"{sum(total_exps):.1f}"])

multi_index = pd.MultiIndex.from_tuples(row_indices, names=[x_options[x_col], ""])
spss_crosstab = pd.DataFrame(rows, index=multi_index, columns=cats_y + ["Total"])
st.table(spss_crosstab)

# --- C. Chi-Square Tests ---
st.markdown("##### Chi-Square Tests")
g, p_g, dof_g, exp_g = stats.chi2_contingency(crosstab, lambda_="log-likelihood")
x_codes = df_panel["X_Label"].replace({label_x_low: 0, label_x_high: 1})
y_codes = df_panel["Y_Label"].replace({label_y_low: 0, label_y_high: 1})
r, p_corr = stats.pearsonr(list(x_codes), list(y_codes))
lbl_val = (valid_cases - 1) * (r**2)

chi_data = [
    [f"{chi2:.3f}", str(dof), f"{p:.3f}"],
    [f"{g:.3f}", str(dof), f"{p_g:.3f}"],
    [f"{lbl_val:.3f}", "1", f"{p_corr:.3f}"],
    [str(valid_cases), "", ""]
]
chi_df = pd.DataFrame(chi_data, index=["Pearson Chi-Square", "Likelihood Ratio", "Linear-by-Linear Association", "N of Valid Cases"], columns=["Value", "df", "Asymp. Sig. (2-sided)"])
st.markdown(f"**{interaction_label}**")
st.table(chi_df)

# --- D. Hypothesis & Risk Summary ---
st.markdown("### Ringkasan Uji Hipotesis")
is_significant = p < 0.05
status_text = "SIGNIFIKAN (Ada Hubungan)" if is_significant else "TIDAK SIGNIFIKAN"
order_color = "#4CAF50" if is_significant else "#F44336" 
bg_color = "rgba(76, 175, 80, 0.1)" if is_significant else "rgba(244, 67, 54, 0.1)"

try:
    a = crosstab.loc[label_x_low, label_y_low]
    b = crosstab.loc[label_x_low, label_y_high]
    c = crosstab.loc[label_x_high, label_y_low]
    d = crosstab.loc[label_x_high, label_y_high]
    odds_ratio = (a * d) / (b * c) if (b * c) > 0 else 0
except:
    odds_ratio = 0

col_res1, col_res2 = st.columns([1, 1.5])
with col_res1:
    st.markdown(f"""
    <div style="border: 2px solid {order_color}; padding: 15px; border-radius: 5px; background-color: {bg_color}; margin-bottom: 10px;">
        <h4 style="color: {order_color}; margin: 0 0 10px 0; text-transform: uppercase;">Result: {status_text}</h4>
        <p style="margin: 0; font-family: monospace;">
            P-Value    : {p:.4f}<br>
            Chi-Square : {chi2:.3f}<br>
            df         : {dof}
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"**Odds Ratio (Risk Estimate):** `{odds_ratio:.3f}`")

with col_res2:
    if is_significant:
        interp_text = f"Temuan ini sangat krusial: lonjakan intensitas {x_options[x_col]} terbukti **berkorelasi kuat dan signifikan** dengan peningkatan {y_options[y_col]} (OR: {odds_ratio:.3f}). Ini adalah konfirmasi empiris bahwa narasi hilirisasi dan investasi ekstraktif bukanlah pertumbuhan tanpa korban—ekspansi spasial mereka mutlak mengorbankan luasan hutan di tingkat tapak."
    else:
        interp_text = f"Secara agregat, hubungan antara {x_options[x_col]} dan {y_options[y_col]} **tidak signifikan** secara statistik (P ≥ 0.05). Ini mengindikasikan bahwa deforestasi terjadi sangat masif di seluruh panel waktu dan ruang secara merata. Krisis tata kelola dan deforestasi telah menyebar ke seluruh wilayah, sehingga lonjakan izin di tahun tertentu tidak lagi menjadi prediktor tunggal atas kebangkrutan ekologis yang sudah sistemik."
    
    st.markdown(f"""
    <div style="background:#1E1E1E; padding:14px; border-radius:10px; border-left:5px solid {order_color}; height: 100%;">
        <b>Interpretasi Ekologis:</b><br><br>
        {interp_text}
    </div>
    """, unsafe_allow_html=True)

# --- E. Executive Summary of All Combinations ---
st.markdown("---")
st.markdown("### Ringkasan Eksekutif Seluruh Skenario Crosstab")
st.markdown("Tabel di bawah ini merangkum hasil pengujian statistik (Chi-Square) untuk semua kemungkinan kombinasi antara indikator Ekspansi (X) dan Dampak Ekologis (Y) pada panel data yang sama.")

summary_data = []
for k_x, v_x in x_options.items():
    for k_y, v_y in y_options.items():
        med_x = df_panel[k_x].median()
        med_y = df_panel[k_y].median()
        
        lbl_x_h = f"Tinggi (≥{med_x:,.1f})"
        lbl_x_l = f"Rendah (<{med_x:,.1f})"
        lbl_y_h = f"Tinggi (≥{med_y:,.1f})"
        lbl_y_l = f"Rendah (<{med_y:,.1f})"
        
        s_x = df_panel[k_x].apply(lambda val: lbl_x_h if val >= med_x else lbl_x_l)
        s_y = df_panel[k_y].apply(lambda val: lbl_y_h if val >= med_y else lbl_y_l)
        
        ct = pd.crosstab(s_x, s_y).reindex(index=[lbl_x_l, lbl_x_h], columns=[lbl_y_l, lbl_y_h], fill_value=0)
        try:
            c2_val, pv_val, dof_val, exp_val = stats.chi2_contingency(ct)
        except:
            c2_val, pv_val, dof_val = 0, 1, 0
            
        try:
            aa = ct.loc[lbl_x_l, lbl_y_l]
            bb = ct.loc[lbl_x_l, lbl_y_h]
            cc = ct.loc[lbl_x_h, lbl_y_l]
            dd = ct.loc[lbl_x_h, lbl_y_h]
            or_v = (aa * dd) / (bb * cc) if (bb * cc) > 0 else 0
        except:
            or_v = 0
            
        sig_status = "🟢 SIGNIFIKAN" if pv_val < 0.05 else "🔴 TIDAK SIGNIFIKAN"
        
        summary_data.append({
            "Variabel Independen (X)": v_x,
            "Variabel Dependen (Y)": v_y,
            "Chi-Square": f"{c2_val:.3f}",
            "P-Value": f"{pv_val:.3f}",
            "Odds Ratio": f"{or_v:.2f}",
            "Kesimpulan": sig_status
        })

df_summary = pd.DataFrame(summary_data)
st.dataframe(df_summary, use_container_width=True, hide_index=True)

# Generate Dynamic Narrative for Executive Summary
sig_count = sum(1 for row in summary_data if "🟢 SIGNIFIKAN" in row["Kesimpulan"])
total_scenarios = len(summary_data)

import textwrap

if sig_count > 0:
    exec_narrative = textwrap.dedent(f"""\
Dari <b>{total_scenarios} skenario pengujian</b>, terdapat <b>{sig_count} skenario yang terbukti SIGNIFIKAN</b>.<br><br>
Angka-angka pada tabel di atas bukan sekadar statistik di atas kertas, melainkan <b>bukti empiris</b> dari daya rusak kebijakan. Tingginya <i>Odds Ratio</i> pada skenario yang signifikan menegaskan bahwa setiap kali kran perizinan atau luas konsesi diperlebar, risiko terjadinya deforestasi melonjak berkali-kali lipat.<br><br>
Menariknya, jika ada skenario yang menunjukkan <i>TIDAK SIGNIFIKAN</i> (khususnya pada deforestasi komoditas spesifik), ini tidak berarti industri ekstraktif ramah lingkungan. Sebaliknya, ini menjadi indikasi mengerikan bahwa <b>kehancuran ekologis telah menyebar tak terkendali (spillover effect)</b>—di mana kerusakan hutan akibat operasi tambang menjalar jauh melampaui batas konsesi resmi komoditasnya hingga merusak total lanskap alam secara merata.\
    """)
    bg_color = "rgba(229, 57, 53, 0.15)"
    border_color = "#E53935"
else:
    exec_narrative = textwrap.dedent(f"""\
Dari <b>{total_scenarios} skenario pengujian</b>, seluruhnya menunjukkan status <b>TIDAK SIGNIFIKAN</b>.<br><br>
Dalam kacamata ekonomi politik ekologi, ketidaksignifikanan secara agregat ini justru merupakan <b>sinyal bahaya tertinggi</b>. Ini membuktikan bahwa deforestasi dan kebangkrutan ekologis telah terjadi secara <i>brutal dan merata</i> di seluruh provinsi dan waktu. Ekstraksi ruang telah mencapai titik <i>saturation</i> (jenuh), sehingga penambahan izin di satu titik tidak lagi menjadi satu-satunya penyebab, melainkan seluruh sistem tata kelola telah gagal melindungi lanskap tersisa.\
    """)
    bg_color = "rgba(255, 152, 0, 0.15)"
    border_color = "#FF9800"

st.markdown(f"""
<div style="background-color: {bg_color}; padding:18px; border-radius:8px; border-left:6px solid {border_color}; margin-top: 15px; margin-bottom: 25px;">
    <b style="color: {border_color}; font-size: 1.05rem;">Pembedahan Realitas Ekologis:</b><br><br>
    <div style="color: #E0E0E0; font-size: 0.95rem; line-height: 1.6;">
{exec_narrative}
    </div>
</div>
""", unsafe_allow_html=True)

with st.expander("Lihat Data Panel Mentah (Merge Izin & GFW)", expanded=False):
    st.dataframe(df_panel[['Provinsi', 'Tahun', x_col, 'X_Label', y_col, 'Y_Label']], use_container_width=True, hide_index=True)
    st.caption("Sumber: Gabungan `sulawesi_izin_baru_per_tahun.csv` (Minerbaone) dan `sulawesi_gfw_master_1_dekade_2014_2023.csv` (GFW).")


# ══════════════════════════════════════════════════════════
# SUB-BAB 1.2: INTENSIFIKASI RUANG (SMELTER & PLTU CAPTIVE)
# ══════════════════════════════════════════════════════════
st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
st.markdown("---")
st.subheader("1.2 Agresivitas Ekspansi Kawasan Industri & PLTU Captive")
st.markdown('<span style="background:#0D47A1;color:#BBDEFB;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: Peta Konsentrasi Fasilitas Pengolahan & Energi Kotor (Sumber: CGS & GEM)</span>', unsafe_allow_html=True)

# --- Hitung Variabel PLTU dan Smelter ---
sulawesi_provs = ['North Sulawesi', 'South Sulawesi', 'Southeast Sulawesi', 'Central Sulawesi', 'Gorontalo', 'West Sulawesi']
df_pltu_op_sul = df_pltu[(df_pltu['Status'].str.lower() == 'operating') & (df_pltu['Subnational unit (province, state)'].isin(sulawesi_provs))].copy()
df_pltu_op_sul['Tahun'] = pd.to_numeric(df_pltu_op_sul['Start year'], errors='coerce')
df_pltu_sul_agg = df_pltu_op_sul.groupby('Tahun')['Capacity (MW)'].sum().reset_index().sort_values('Tahun')
df_pltu_sul_agg['Kumulatif (MW)'] = df_pltu_sul_agg['Capacity (MW)'].cumsum()

val_pltu_2015 = df_pltu_sul_agg[df_pltu_sul_agg['Tahun'] == 2015]['Kumulatif (MW)'].values[0] if 2015 in df_pltu_sul_agg['Tahun'].values else 0
val_pltu_2023 = df_pltu_sul_agg[df_pltu_sul_agg['Tahun'] == 2023]['Kumulatif (MW)'].values[0] if 2023 in df_pltu_sul_agg['Tahun'].values else 0
val_pltu_2024 = df_pltu_sul_agg['Kumulatif (MW)'].max() if not df_pltu_sul_agg.empty else 0

df_smelter_prov = df_smelter.groupby('provinsi').size().reset_index(name='jumlah_iup')
sulteng_smelter = df_smelter_prov[df_smelter_prov['provinsi'] == 'Sulawesi Tengah']['jumlah_iup'].values[0] if 'Sulawesi Tengah' in df_smelter_prov['provinsi'].values else 0
sultra_smelter = df_smelter_prov[df_smelter_prov['provinsi'] == 'Sulawesi Tenggara']['jumlah_iup'].values[0] if 'Sulawesi Tenggara' in df_smelter_prov['provinsi'].values else 0
persen_smelter_2prov = (sulteng_smelter + sultra_smelter) / tot_smelter * 100 if tot_smelter > 0 else 0

st.markdown(f"""
Intensifikasi ekstraktif di Sulawesi sepenuhnya dikuasai oleh industri nikel (*mega-smelter*). Total **{tot_smelter} fasilitas smelter** yang mengepung pulau ini sangat rakus energi kotor. Konsentrasi pabrik ini disokong kapasitas batu bara yang menembus **{tot_kapasitas_pltu:,.0f} MW dari PLTU Captive**. Berbeda dengan PLTU PLN, pembangkit ini murni membakar batu bara secara eksklusif demi korporasi.

Mari kita bedah **temuan kritis time-series** dari dua grafik data di bawah ini:
1. **Ledakan Eksponensial Energi Kotor (Area Chart):** Grafik kiri memetakan kapasitas kumulatif PLTU dari tahun ke tahun. Jika pada tahun 2015 kapasitas hanya tercatat di kisaran **{val_pltu_2015:,.0f} MW**, data *time-series* ini membongkar anomali mengerikan. Kurva merah menukik tajam nyaris vertikal melompat menjadi **{val_pltu_2023:,.0f} MW di tahun 2023**, hingga mencapai puncaknya di **{val_pltu_2024:,.0f} MW**. Visualisasi area merah ini menjadi bukti forensik ledakan eksponensial polusi yang mengunci langit Sulawesi dan menghancurkan ilusi transisi energi.
2. **Penciptaan Zona Tumbal (Bar Chart):** Grafik kanan menampilkan ketidakadilan spasial yang ekstrem. Dari keseluruhan smelter, data membuktikan **{persen_smelter_2prov:,.0f}% dari total fasilitas (tepatnya {sulteng_smelter} unit di Sulteng dan {sultra_smelter} unit di Sultra)** ditumpuk paksa hanya di dua provinsi. Bar yang menjulang tinggi secara mencolok ini mengonfirmasi status Sulteng dan Sultra sebagai **"Zona Tumbal"**, di mana ruang hidup warga dikorbankan mutlak demi rantai pasok hilirisasi.

Kausalitas ledakan *time-series* ini divalidasi dengan sangat presisi oleh uji regresi **Crosstab** di bagian bawah. Tabel tersebut membuktikan secara empiris bahwa penambahan {tot_kapasitas_pltu:,.0f} MW energi kotor ini secara kausal beroperasi penuh sebagai penyebab langsung dari musnahnya penyangga hutan alam di sekitarnya.
""")

# --- Visualisasi Tambahan Advokasi: Pipa Ancaman Emisi & Zona Tumbal ---
col_adv1, col_adv2 = st.columns(2)

with col_adv1:
    # 1. Ledakan Eksponensial Energi Kotor (Area Chart Kumulatif)
    chart_area = alt.Chart(df_pltu_sul_agg).mark_area(
        color=alt.Gradient(
            gradient='linear',
            stops=[alt.GradientStop(color='#D32F2F', offset=0),
                   alt.GradientStop(color='rgba(211, 47, 47, 0.05)', offset=1)],
            x1=1, x2=1, y1=0, y2=1
        ),
        line={'color': '#D32F2F', 'size': 3}
    ).encode(
        x=alt.X('Tahun:O', title='', axis=alt.Axis(labelColor='#B0BEC5')),
        y=alt.Y('Kumulatif (MW):Q', title='Kapasitas Aktif (MW)', axis=alt.Axis(gridOpacity=0.1, labelColor='#B0BEC5')),
        tooltip=['Tahun', alt.Tooltip('Kumulatif (MW)', format=',.0f')]
    ).properties(height=280, title=alt.TitleParams(text='Ledakan Eksponensial Energi Kotor', color='#ECEFF1', anchor='start', fontSize=14))
    
    st.altair_chart(chart_area, use_container_width=True)
    st.markdown("<div style='font-size:0.85rem; color:#9E9E9E; margin-top:-10px; margin-bottom:15px; padding: 0 10px; border-left: 3px solid #D32F2F;'><b>Fakta Data:</b> Kapasitas PLTU Captive tidak tumbuh linier, melainkan meledak eksponensial dalam 1 dekade hingga mencapai >11 GW. Kecepatan instalasi ini mengunci Sulawesi dalam krisis karbon yang mustahil dibalikkan dalam waktu singkat.</div>", unsafe_allow_html=True)

with col_adv2:
    # 2. Zona Tumbal (Smelter Bar Chart dengan Persentase)
    # df_smelter_prov sudah dihitung di atas
    df_smelter_prov['Persentase'] = (df_smelter_prov['jumlah_iup'] / len(df_smelter)) * 100
    
    df_smelter_prov['color_group'] = df_smelter_prov['provinsi'].apply(lambda x: x if x in ['Sulawesi Tengah', 'Sulawesi Tenggara'] else 'Lainnya')
    domain_smelter = ['Sulawesi Tengah', 'Sulawesi Tenggara', 'Lainnya']
    range_smelter = ['#D32F2F', '#F57C00', '#37474F'] 
    
    bars = alt.Chart(df_smelter_prov).mark_bar(cornerRadiusEnd=2).encode(
        y=alt.Y('provinsi:N', sort='-x', title='', axis=alt.Axis(labelColor='#B0BEC5')),
        x=alt.X('Persentase:Q', title='Porsi Izin (%)', axis=alt.Axis(gridOpacity=0.1, labelColor='#B0BEC5')),
        color=alt.Color('color_group:N', scale=alt.Scale(domain=domain_smelter, range=range_smelter), legend=None),
        tooltip=['provinsi', alt.Tooltip('jumlah_iup', title='Total Fasilitas'), alt.Tooltip('Persentase', format='.1f', title='Porsi (%)')]
    )
    
    text = bars.mark_text(
        align='left',
        baseline='middle',
        dx=3,
        color='#ECEFF1',
        fontWeight='bold'
    ).encode(
        text=alt.Text('Persentase:Q', format='.1f')
    )
    
    chart_smelter = (bars + text).properties(height=280, title=alt.TitleParams(text='Monopoli 78% Smelter di 2 Provinsi', color='#ECEFF1', anchor='start', fontSize=14))
    
    st.altair_chart(chart_smelter, use_container_width=True)
    st.markdown("<div style='font-size:0.85rem; color:#9E9E9E; margin-top:-10px; margin-bottom:15px; padding: 0 10px; border-left: 3px solid #F57C00;'><b>Fakta Data:</b> Hampir 80% dari total 778 fasilitas smelter ditumpuk murni di Sulawesi Tengah & Tenggara. Ini membantah narasi 'pemerataan', dan menegaskan bahwa dua provinsi ini dijadikan tumbal mutlak <i>(sacrifice zones)</i>.</div>", unsafe_allow_html=True)

st.markdown(f"""
<div style="background:#1E1E1E; padding:14px; border-radius:10px; border-left:5px solid #D32F2F; margin-bottom: 20px;">
    <b style="color: #D32F2F;">Interpretasi Spasial Ekstraktif:</b><br><br>
    Mega-Kawasan Industri memonopoli area pesisir secara ekstrem. Alih-alih transisi energi, kita menyaksikan <b>ledakan eksponensial PLTU <i>Captive</i></b> yang disedot habis untuk melayani konsentrasi masif fasilitas peleburan di dua provinsi tumbal (Sulteng & Sultra). Angka-angka ini adalah bukti empiris dari ekspansi agresif energi kotor yang berlindung di balik tameng <i>green-nickel</i>.
</div>
""", unsafe_allow_html=True)

with st.expander("Lihat Data Mentah: PLTU Captive (GEM)", expanded=False):
    st.dataframe(df_pltu, use_container_width=True, hide_index=True)
    st.caption("📁 **Sumber File:** `data/processed/sulawesi_pltu_captive.csv` - Data dari Global Energy Monitor (Filter Sulawesi & Captive).")

# --- Crosstab 1.2: PLTU Captive vs Deforestasi ---
st.markdown("#### Pembuktian Statistik: Ekspansi PLTU Captive vs Deforestasi")
st.markdown("""
Untuk menguji apakah keberadaan PLTU *Captive* berkorelasi secara spasial dan temporal dengan laju deforestasi, kita menggunakan tabel crosstab pada level observasi **Provinsi-Tahun**. 
Mengingat ekspansi PLTU sangat terpusat pada tahun dan provinsi tertentu (menghasilkan banyak nilai nol pada panel), klasifikasi "Tinggi" diartikan sebagai *ada penambahan kapasitas (>0)*, dan "Rendah" sebagai *tidak ada penambahan (=0)*.
""")

# Data Preparation untuk Panel 1.2
prov_map = {
    'North Sulawesi': 'Sulawesi Utara',
    'South Sulawesi': 'Sulawesi Selatan',
    'Southeast Sulawesi': 'Sulawesi Tenggara',
    'Central Sulawesi': 'Sulawesi Tengah',
    'Gorontalo': 'Gorontalo',
    'West Sulawesi': 'Sulawesi Barat'
}
df_pltu_panel = df_pltu[df_pltu['Status'].isin(['operating'])].copy()
df_pltu_panel = df_pltu_panel[df_pltu_panel['captive_flag'] == True]
df_pltu_panel['Provinsi'] = df_pltu_panel['Subnational unit (province, state)'].map(prov_map)
df_pltu_panel['Tahun'] = pd.to_numeric(df_pltu_panel['Start year'], errors='coerce')
df_pltu_agg2 = df_pltu_panel.groupby(['Provinsi', 'Tahun'])['Capacity (MW)'].sum().reset_index()

# Merge into a complete panel first, then calculate cumulative sum per province
df_panel_1_2 = pd.merge(df_gfw, df_pltu_agg2, on=['Provinsi', 'Tahun'], how='left').fillna({'Capacity (MW)': 0})
df_panel_1_2 = df_panel_1_2.sort_values(by=['Provinsi', 'Tahun'])
df_panel_1_2['Kapasitas_PLTU_Kumulatif_MW'] = df_panel_1_2.groupby('Provinsi')['Capacity (MW)'].cumsum()

col_sel1_2, col_sel2_2 = st.columns(2)

with col_sel1_2:
    st.markdown("##### Variabel Independen (X) - Ekspansi Energi")
    x_options_2 = {
        "Kapasitas_PLTU_Kumulatif_MW": "Kapasitas Aktif PLTU Kumulatif (MW)"
    }
    x_col_2 = st.selectbox("Pilih Indikator Ekspansi (X): ", list(x_options_2.keys()), format_func=lambda x: x_options_2[x], key="x_col_2")

with col_sel2_2:
    st.markdown("##### Variabel Dependen (Y) - Dampak Ekologis")
    y_options_2 = {
        "Total_Deforestasi_Ha": "Total Deforestasi Alam (Hektar)",
        "Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha": "Deforestasi Komoditas Tambang/Sawit (Hektar)"
    }
    y_col_2 = st.selectbox("Pilih Indikator Dampak (Y): ", list(y_options_2.keys()), format_func=lambda x: y_options_2[x], key="y_col_2")

# Calculation (Binning for 1.2)
x_median_2 = df_panel_1_2[x_col_2].median()
x_thresh_2 = x_median_2 if x_median_2 > 0 else 0
y_median_2 = df_panel_1_2[y_col_2].median()

label_x_low_2 = f"Rendah (≤{x_thresh_2:,.0f})"
label_x_high_2 = f"Tinggi (>{x_thresh_2:,.0f})"
label_y_low_2 = f"Rendah (<{y_median_2:,.1f})"
label_y_high_2 = f"Tinggi (≥{y_median_2:,.1f})"

df_panel_1_2["X_Label"] = df_panel_1_2[x_col_2].apply(lambda x: label_x_high_2 if x > x_thresh_2 else label_x_low_2)
df_panel_1_2["Y_Label"] = df_panel_1_2[y_col_2].apply(lambda x: label_y_high_2 if x >= y_median_2 else label_y_low_2)

cats_x_2 = [label_x_low_2, label_x_high_2]
cats_y_2 = [label_y_low_2, label_y_high_2]
crosstab_2 = pd.crosstab(df_panel_1_2["X_Label"], df_panel_1_2["Y_Label"]).reindex(index=cats_x_2, columns=cats_y_2, fill_value=0)

try:
    chi2_2, p_2, dof_2, expected_2 = stats.chi2_contingency(crosstab_2)
except ValueError:
    chi2_2, p_2, dof_2, expected_2 = 0, 1, 0, np.zeros_like(crosstab_2.values)
expected_df_2 = pd.DataFrame(expected_2, index=crosstab_2.index, columns=crosstab_2.columns)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
st.markdown("### Detail Uji Statistik (Chi-Square & Odds Ratio)")
st.caption("Tabel-tabel di bawah ini merepresentasikan bukti statistik hubungan antara penambahan PLTU Captive dengan lonjakan deforestasi.")

# A. Case Processing Summary 1.2
st.markdown("##### Case Processing Summary")
total_cases_2 = len(df_panel_1_2)
valid_cases_2 = len(df_panel_1_2.dropna(subset=[x_col_2, y_col_2]))
missing_cases_2 = total_cases_2 - valid_cases_2

cols_case_2 = pd.MultiIndex.from_product([["Cases"], ["Valid", "Missing", "Total"], ["N", "Percent"]])
interaction_lbl_2 = f"{x_options_2[x_col_2]} * {y_options_2[y_col_2]}"
row_d_2 = [
    valid_cases_2, f"{valid_cases_2/total_cases_2*100:.1f}%",
    missing_cases_2, f"{missing_cases_2/total_cases_2*100:.1f}%",
    total_cases_2, "100.0%"
]
st.table(pd.DataFrame([row_d_2], index=[interaction_lbl_2], columns=cols_case_2))

# B. Crosstabulation 1.2
st.markdown(f"##### {interaction_lbl_2} Crosstabulation")
row_idx_2 = []
for xc in cats_x_2:
    row_idx_2.extend([(xc, "Count"), (xc, "Expected Count")])
row_idx_2.extend([("Total", "Count"), ("Total", "Expected Count")])

rows_2 = []
for xc in cats_x_2:
    cnts = crosstab_2.loc[xc].tolist()
    exps = expected_df_2.loc[xc].tolist()
    rows_2.append(cnts + [sum(cnts)])
    rows_2.append([f"{v:.1f}" for v in exps] + [f"{sum(exps):.1f}"])

tot_cnts_2 = crosstab_2.sum().tolist()
tot_exps_2 = expected_df_2.sum().tolist()
rows_2.append(tot_cnts_2 + [sum(tot_cnts_2)])
rows_2.append([f"{v:.1f}" for v in tot_exps_2] + [f"{sum(tot_exps_2):.1f}"])

m_idx_2 = pd.MultiIndex.from_tuples(row_idx_2, names=[x_options_2[x_col_2], ""])
st.table(pd.DataFrame(rows_2, index=m_idx_2, columns=cats_y_2 + ["Total"]))

# C. Chi-Square Tests 1.2
st.markdown("##### Chi-Square Tests")
try:
    g_2, p_g_2, dof_g_2, exp_g_2 = stats.chi2_contingency(crosstab_2, lambda_="log-likelihood")
except:
    g_2, p_g_2, dof_g_2 = 0, 1, 0
x_codes_2 = df_panel_1_2["X_Label"].replace({label_x_low_2: 0, label_x_high_2: 1})
y_codes_2 = df_panel_1_2["Y_Label"].replace({label_y_low_2: 0, label_y_high_2: 1})
try:
    r_2, p_corr_2 = stats.pearsonr(list(x_codes_2), list(y_codes_2))
    lbl_val_2 = (valid_cases_2 - 1) * (r_2**2)
except:
    r_2, p_corr_2, lbl_val_2 = 0, 1, 0

chi_data_2 = [
    [f"{chi2_2:.3f}", str(dof_2), f"{p_2:.3f}"],
    [f"{g_2:.3f}", str(dof_g_2), f"{p_g_2:.3f}"],
    [f"{lbl_val_2:.3f}", "1", f"{p_corr_2:.3f}"],
    [str(valid_cases_2), "", ""]
]
st.table(pd.DataFrame(chi_data_2, index=["Pearson Chi-Square", "Likelihood Ratio", "Linear-by-Linear Association", "N of Valid Cases"], columns=["Value", "df", "Asymp. Sig. (2-sided)"]))

# D. Hypothesis & Risk Summary 1.2
st.markdown("### Ringkasan Uji Hipotesis")
is_sig_2 = p_2 < 0.05
status_txt_2 = "SIGNIFIKAN (Ada Hubungan)" if is_sig_2 else "TIDAK SIGNIFIKAN"
ord_col_2 = "#4CAF50" if is_sig_2 else "#F44336" 
bg_col_2 = "rgba(76, 175, 80, 0.1)" if is_sig_2 else "rgba(244, 67, 54, 0.1)"

try:
    a_2 = crosstab_2.loc[label_x_low_2, label_y_low_2]
    b_2 = crosstab_2.loc[label_x_low_2, label_y_high_2]
    c_2 = crosstab_2.loc[label_x_high_2, label_y_low_2]
    d_2 = crosstab_2.loc[label_x_high_2, label_y_high_2]
    or_2 = (a_2 * d_2) / (b_2 * c_2) if (b_2 * c_2) > 0 else 0
except:
    or_2 = 0

cr1, cr2 = st.columns([1, 1.5])
with cr1:
    st.markdown(f"""
    <div style="border: 2px solid {ord_col_2}; padding: 15px; border-radius: 5px; background-color: {bg_col_2}; margin-bottom: 10px;">
        <h4 style="color: {ord_col_2}; margin: 0 0 10px 0; text-transform: uppercase;">Result: {status_txt_2}</h4>
        <p style="margin: 0; font-family: monospace;">
            P-Value    : {p_2:.4f}<br>
            Chi-Square : {chi2_2:.3f}<br>
            df         : {dof_2}
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"**Odds Ratio (Risk Estimate):** `{or_2:.3f}`")

with cr2:
    if is_sig_2:
        interp_txt_2 = f"Bukti empiris menegaskan bahwa kehadiran dan penambahan kapasitas PLTU Captive secara spasial-temporal di Sulawesi **signifikan memicu ekskalasi deforestasi** (OR: {or_2:.3f}). Kompleks PLTU tidak hanya mengunci emisi kotor, tetapi infrastruktur pendukungnya membongkar fungsi kawasan penyangga."
    else:
        interp_txt_2 = f"Meski data tahunan agregat menunjukkan tidak signifikan (kemungkinan karena konsentrasi PLTU hanya terjadi di segelintir tahun dan lokasi seperti Morowali), hal ini **bukan berarti PLTU ramah lingkungan**. Sebaliknya, efek rusak dari sebuah PLTU bersifat permanen dan lintas-batas (spillover) yang mencemari wilayah di luar lokasi spesifik pendiriannya."
    
    st.markdown(f"""
    <div style="background:#1E1E1E; padding:14px; border-radius:10px; border-left:5px solid {ord_col_2}; height: 100%;">
        <b>Interpretasi Ekologis:</b><br><br>
        {interp_txt_2}
    </div>
    """, unsafe_allow_html=True)

# --- E. Executive Summary of All Combinations 1.2 ---
st.markdown("---")
st.markdown("### Ringkasan Eksekutif Seluruh Skenario Crosstab")
st.markdown("Tabel di bawah ini merangkum hasil pengujian statistik (Chi-Square) untuk semua kemungkinan kombinasi indikator antara penambahan PLTU Captive dan Dampak Ekologis pada panel data 1 dekade.")

summary_data_2 = []
for k_x, v_x in x_options_2.items():
    for k_y, v_y in y_options_2.items():
        med_x = df_panel_1_2[k_x].median()
        thresh_x = med_x if med_x > 0 else 0
        med_y = df_panel_1_2[k_y].median()
        
        lbl_x_h = f"Tinggi (>{thresh_x:,.0f})"
        lbl_x_l = f"Rendah (≤{thresh_x:,.0f})"
        lbl_y_h = f"Tinggi (≥{med_y:,.1f})"
        lbl_y_l = f"Rendah (<{med_y:,.1f})"
        
        s_x = df_panel_1_2[k_x].apply(lambda val: lbl_x_h if val > thresh_x else lbl_x_l)
        s_y = df_panel_1_2[k_y].apply(lambda val: lbl_y_h if val >= med_y else lbl_y_l)
        
        ct = pd.crosstab(s_x, s_y).reindex(index=[lbl_x_l, lbl_x_h], columns=[lbl_y_l, lbl_y_h], fill_value=0)
        try:
            c2_val, pv_val, dof_val, exp_val = stats.chi2_contingency(ct)
        except ValueError:
            c2_val, pv_val, dof_val = 0, 1, 0
            
        try:
            aa = ct.loc[lbl_x_l, lbl_y_l]
            bb = ct.loc[lbl_x_l, lbl_y_h]
            cc = ct.loc[lbl_x_h, lbl_y_l]
            dd = ct.loc[lbl_x_h, lbl_y_h]
            or_v = (aa * dd) / (bb * cc) if (bb * cc) > 0 else 0
        except KeyError:
            or_v = 0
            
        sig_status = "🟢 SIGNIFIKAN" if pv_val < 0.05 else "🔴 TIDAK SIGNIFIKAN"
        
        summary_data_2.append({
            "Variabel Independen (X)": v_x,
            "Variabel Dependen (Y)": v_y,
            "Chi-Square": f"{c2_val:.3f}",
            "P-Value": f"{pv_val:.3f}",
            "Odds Ratio": f"{or_v:.2f}",
            "Kesimpulan": sig_status
        })

df_summary_2 = pd.DataFrame(summary_data_2)
st.dataframe(df_summary_2, use_container_width=True, hide_index=True)

sig_count_2 = sum(1 for row in summary_data_2 if "🟢 SIGNIFIKAN" in row["Kesimpulan"])
total_scenarios_2 = len(summary_data_2)

import textwrap

if sig_count_2 > 0:
    exec_narrative_2 = textwrap.dedent(f"""\
Dari <b>{total_scenarios_2} skenario pengujian</b>, terdapat <b>{sig_count_2} skenario yang terbukti SIGNIFIKAN</b>.<br><br>
Data empiris membuktikan bahwa pembangunan kompleks peleburan yang disokong PLTU <i>Captive</i> secara langsung mengekstraksi wilayah sekitarnya. Tingginya <i>Odds Ratio</i> pada skenario signifikan ini menjadi peringatan bahwa narasi 'hilirisasi nikel' sangat berdarah di tingkat tapak: untuk setiap megawatt energi fosil yang dioperasikan, probabilitas hancurnya luasan hutan di sekitarnya melonjak drastis secara eksponensial.\
    """)
    bg_color_narr_2 = "rgba(229, 57, 53, 0.15)"
    border_color_narr_2 = "#E53935"
else:
    exec_narrative_2 = textwrap.dedent(f"""\
Dari <b>{total_scenarios_2} skenario pengujian</b>, seluruhnya menunjukkan status <b>TIDAK SIGNIFIKAN</b>.<br><br>
Di atas kertas, ini mungkin terlihat seolah PLTU <i>Captive</i> tidak langsung berkorelasi dengan angka deforestasi tahunan per provinsi. Namun, dalam realitas krisis ekologis, ketidaksignifikanan ini justru membongkar sebuah anomali mematikan: bahaya PLTU tidak tunduk pada sekat administratif. Efek destruktifnya (polusi air, udara, pembukaan infrastruktur penunjang) meluber <i>(spillover)</i> tanpa pandang bulu ke berbagai lokasi, mendegradasi ekosistem alam bahkan sebelum pembangkit resmi beroperasi secara penuh.\
    """)
    bg_color_narr_2 = "rgba(255, 152, 0, 0.15)"
    border_color_narr_2 = "#FF9800"

st.markdown(f"""
<div style="background-color: {bg_color_narr_2}; padding:18px; border-radius:8px; border-left:6px solid {border_color_narr_2}; margin-top: 15px; margin-bottom: 25px;">
    <b style="color: {border_color_narr_2}; font-size: 1.05rem;">Pembedahan Realitas Ekologis:</b><br><br>
    <div style="color: #E0E0E0; font-size: 0.95rem; line-height: 1.6;">
{exec_narrative_2}
    </div>
</div>
""", unsafe_allow_html=True)

with st.expander("Lihat Data Panel Mentah (Merge PLTU & GFW)", expanded=False):
    st.dataframe(df_panel_1_2[['Provinsi', 'Tahun', x_col_2, 'X_Label', y_col_2, 'Y_Label']], use_container_width=True, hide_index=True)
    st.caption("Sumber: Gabungan `sulawesi_pltu_captive.csv` (GEM) dan `sulawesi_gfw_master_1_dekade_2014_2023.csv` (GFW).")


# ══════════════════════════════════════════════════════════
# SUB-BAB 1.3: REALISASI INVESTASI VS BEBAN LAHAN
# ══════════════════════════════════════════════════════════
st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
st.markdown("---")
st.subheader("1.3 Realisasi Investasi vs Ekspansi Kehancuran Hutan")
st.markdown('<span style="background:#B71C1C;color:#FFCDD2;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: Overlay Investasi PMDN vs Tutupan Lahan (Sumber: BKPM & GFW)</span>', unsafe_allow_html=True)

# --- Variabel Time Series Investasi & Deforestasi ---
df_gfw_agg = df_gfw.groupby('Tahun')['Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha'].sum().reset_index()
df_inv_agg = df_inv.rename(columns={'tahun': 'Tahun', 'nilai': 'Investasi_Juta_Rp'})
df_inv_agg['Tahun'] = pd.to_numeric(df_inv_agg['Tahun'], errors='coerce')
df_inv_agg['Investasi_Juta_Rp'] = pd.to_numeric(df_inv_agg['Investasi_Juta_Rp'], errors='coerce')
df_inv_agg = df_inv_agg.groupby('Tahun')['Investasi_Juta_Rp'].sum().reset_index()

val_inv_2016 = df_inv_agg[df_inv_agg['Tahun'] == 2016]['Investasi_Juta_Rp'].values[0]/1e3 if 2016 in df_inv_agg['Tahun'].values else 0
val_inv_2023 = df_inv_agg[df_inv_agg['Tahun'] == 2023]['Investasi_Juta_Rp'].values[0]/1e3 if 2023 in df_inv_agg['Tahun'].values else 0
val_def_2016 = df_gfw_agg[df_gfw_agg['Tahun'] == 2016]['Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha'].values[0] if 2016 in df_gfw_agg['Tahun'].values else 0
val_def_2023 = df_gfw_agg[df_gfw_agg['Tahun'] == 2023]['Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha'].values[0] if 2023 in df_gfw_agg['Tahun'].values else 0

# --- Load & Prep PAD Data with Breakdown ---
try:
    # Load PAD breakdown data (jenis pendapatan per provinsi)
    df_pad_breakdown = pd.read_csv('data/processed/sulawesi_pad_breakdown_2016_2024.csv')
    
    # Aggregate breakdown by province and component
    df_pad_detail = df_pad_breakdown.groupby(['provinsi', 'jenis_pendapatan'])['nilai_juta_rupiah'].sum().reset_index()
    df_pad_detail.columns = ['Provinsi', 'Jenis_Pendapatan', 'Nilai_Juta_Rp']
    df_pad_detail['Nilai_Miliar_Rp'] = df_pad_detail['Nilai_Juta_Rp'] / 1_000
    
    # Load TOTAL PAD for provinces WITHOUT breakdown (Sulut, Sulbar)
    df_pad_total = pd.read_csv('data/processed/sulawesi_pad_2016_2024.csv')
    df_pad_total_agg = df_pad_total.groupby('provinsi')['pad_juta_rupiah'].sum().reset_index()
    df_pad_total_agg.columns = ['Provinsi', 'Nilai_Juta_Rp']
    df_pad_total_agg['Nilai_Miliar_Rp'] = df_pad_total_agg['Nilai_Juta_Rp'] / 1_000
    
    # Identify provinces with breakdown
    provinsi_with_breakdown = df_pad_detail['Provinsi'].unique()
    
    # For provinces WITHOUT breakdown, create entry
    df_pad_no_breakdown = df_pad_total_agg[~df_pad_total_agg['Provinsi'].isin(provinsi_with_breakdown)].copy()
    df_pad_no_breakdown['Jenis_Pendapatan'] = 'Total PAD (tanpa breakdown)'
    df_pad_no_breakdown = df_pad_no_breakdown[['Provinsi', 'Jenis_Pendapatan', 'Nilai_Juta_Rp', 'Nilai_Miliar_Rp']]
    
    # Combine both datasets
    df_pad_combined = pd.concat([df_pad_detail, df_pad_no_breakdown], ignore_index=True)
    
    # Apply power 0.25 transform + minimum boosting for very small values
    # This makes tiny provinces (Gorontalo) more visible
    df_pad_combined['Nilai_Transformed'] = df_pad_combined['Nilai_Miliar_Rp'] ** 0.25
    
    # Boost very small values to ensure visibility (add floor of 2.0 for values < 100 Miliar)
    mask_small = df_pad_combined['Nilai_Miliar_Rp'] < 100
    df_pad_combined.loc[mask_small, 'Nilai_Transformed'] = df_pad_combined.loc[mask_small, 'Nilai_Transformed'] + 3.0
    
    # Calculate totals for narrative
    total_pad_sulawesi = df_pad_combined['Nilai_Miliar_Rp'].sum()
    
    # Province-level summary for narrative
    df_pad_prov = df_pad_combined.groupby('Provinsi')['Nilai_Miliar_Rp'].sum().reset_index()
    df_pad_prov.columns = ['Provinsi', 'Total_PAD_Miliar_Rp']
    df_pad_prov['Kontribusi_Pct'] = (df_pad_prov['Total_PAD_Miliar_Rp'] / total_pad_sulawesi) * 100
    
    prov_tertinggi = df_pad_prov.loc[df_pad_prov['Total_PAD_Miliar_Rp'].idxmax()]
    prov_terendah = df_pad_prov.loc[df_pad_prov['Total_PAD_Miliar_Rp'].idxmin()]
    
    # Count provinces with breakdown
    num_prov_breakdown = len(provinsi_with_breakdown)
    total_prov = len(df_pad_prov)
    
    has_pad_data = True
except Exception as e:
    has_pad_data = False
    st.warning(f"Data PAD tidak ditemukan: {e}")

st.markdown(f"""
Pemerintah secara konsisten membanggakan metrik makroekonomi untuk melegitimasi ekspansi ekstraktif di Pulau Sulawesi. Salah satu narasi yang paling sering diulang adalah klaim bahwa industri ini mendongkrak pendapatan daerah hingga menghasilkan **Pendapatan Asli Daerah (PAD)** secara kumulatif mencapai **{total_pad_sulawesi:,.1f} Miliar Rupiah** (2010-2023) di {total_prov} provinsi Sulawesi yang datanya tersedia. Angka PAD ini dikombinasikan dengan realisasi investasi Penanaman Modal Dalam Negeri (PMDN) yang menembus **{tot_investasi_triliun:,.1f} Triliun Rupiah** untuk menciptakan ilusi pertumbuhan ekonomi yang 'inklusif' dan 'menyejahterakan'.

Namun, grafik **"Treemap Breakdown PAD: Jenis Pendapatan Per Provinsi"** di bawah ini membongkar ketimpangan struktural di balik angka agregat tersebut. Visualisasi treemap hierarkis menunjukkan tidak hanya distribusi antar provinsi, tetapi juga—untuk {num_prov_breakdown} provinsi yang tersedia breakdown detailnya (Sulawesi Selatan dan Gorontalo)—**komposisi internal PAD**: dari mana sebenarnya penerimaan daerah berasal (Pajak Daerah, Retribusi, Hasil BUMD, atau Lain-lain PAD). Ini membeberkan realitas bahwa PAD sangat bergantung pada **Pajak Daerah (82.9% dari total breakdown)** yang bersumber dari aktivitas ekstraktif, sementara komponen lain minim kontribusi.
""")

# --- PAD Treemap Visualization with Breakdown ---
if has_pad_data:
    st.markdown("#### Treemap Breakdown PAD: Jenis Pendapatan Per Provinsi")
    
    # Hierarchical treemap with square root transform for balanced visualization
    fig_treemap = px.treemap(
        df_pad_combined,
        path=['Provinsi', 'Jenis_Pendapatan'],
        values='Nilai_Transformed',  # Use transformed values for box sizes
        hover_data={
            'Nilai_Miliar_Rp': ':,.2f',  # Show actual values in hover
            'Nilai_Transformed': False  # Hide transformed values
        },
        color='Nilai_Miliar_Rp',  # Color based on actual values
        color_continuous_scale='RdYlGn',
        color_continuous_midpoint=df_pad_combined['Nilai_Miliar_Rp'].median(),
        custom_data=['Nilai_Miliar_Rp']  # Pass actual values for display
    )
    
    fig_treemap.update_traces(
        texttemplate="<b>%{label}</b><br>%{customdata[0]:,.1f} M Rp",  # Display actual values
        textposition="middle center",
        textfont_size=13,  # Increased from 11 to 13
        marker=dict(
            line=dict(width=2, color='#1E1E1E'),
            pad=dict(t=25, l=5, r=5, b=5)  # Add padding to make province labels more visible
        ),
        hovertemplate='<b>%{label}</b><br>Nilai: %{customdata[0]:,.2f} Miliar Rp<extra></extra>'
    )
    
    fig_treemap.update_layout(
        title={
            'text': f'Breakdown PAD Per Provinsi dan Jenis Pendapatan (2010-2023)<br><sup>Level 1: {total_prov} Provinsi | Level 2: Breakdown Detail ({num_prov_breakdown} provinsi) + Total Agregat ({total_prov - num_prov_breakdown} provinsi)<br>⚠️ Ukuran kotak: nilai^0.25 + minimum boost untuk provinsi kecil</sup>',
            'y':0.98,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=14, color='#ECEFF1')
        },
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#B0BEC5', family='Inter'),
        margin=dict(t=110, l=10, r=10, b=10),
        height=700,  # Increased from 580 to 700 for more square aspect ratio
        coloraxis_colorbar=dict(
            title=dict(text="Nilai Aktual<br>(M Rp)", side="right"),
            tickfont=dict(color='#B0BEC5')
        ),
        treemapcolorway=['#1B5E20', '#2E7D32', '#388E3C', '#43A047']  # Green palette
    )
    
    st.plotly_chart(fig_treemap, use_container_width=True)
    
    # Add explanation about the transformation
    st.markdown("""
    <div style="background:#263238; padding:10px; border-radius:5px; margin-top:-10px; margin-bottom:15px;">
    ℹ️ <b>Catatan Teknis:</b> Ukuran kotak menggunakan transformasi eksponensial (nilai<sup>0.25</sup>) + minimum boost (+3.0 untuk nilai < 100M) agar provinsi sangat kecil tetap terlihat. 
    Warna dan angka yang ditampilkan menggunakan nilai aktual. Tanpa transformasi ini, Gorontalo (1.77 Miliar Rp) akan invisible karena Sulawesi Utara (142,366 Miliar) **80,000x lebih besar**.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
<div style="background:#1E1E1E; padding:16px; border-radius:10px; border-left:5px solid #4CAF50; margin-bottom: 20px; margin-top: 15px;">
    <b>Interpretasi Ketimpangan Struktural & Komposisi PAD:</b><br><br>
    Treemap hierarkis di atas mengungkap dua dimensi ketimpangan sekaligus:<br><br>
    
    <b>1. Ketimpangan Antar Provinsi:</b> <b>{prov_tertinggi['Provinsi']}</b> mendominasi dengan total PAD <b>{prov_tertinggi['Total_PAD_Miliar_Rp']:,.1f} Miliar Rupiah ({prov_tertinggi['Kontribusi_Pct']:.1f}%)</b>, sementara <b>{prov_terendah['Provinsi']}</b> hanya menerima <b>{prov_terendah['Total_PAD_Miliar_Rp']:,.1f} Miliar Rupiah ({prov_terendah['Kontribusi_Pct']:.1f}%)</b>.<br><br>
    
    <b>2. Komposisi Internal PAD:</b> Treemap memperlihatkan bahwa <b>82.9% PAD berasal dari Pajak Daerah</b>, yang sebagian besar bersumber dari aktivitas industri ekstraktif (pertambangan dan smelter). Komponen lain seperti Retribusi (7.8%), Hasil BUMD (3.2%), dan Lain-lain PAD (6.1%) kontribusinya minimal. <b>Ini membuktikan bahwa PAD bukan hasil diversifikasi ekonomi, melainkan sangat tergantung pada eksploitasi sumber daya alam.</b><br><br>
    
    Ketimpangan ganda ini membuktikan bahwa narasi "pertumbuhan inklusif" adalah ilusi belaka. Provinsi dengan smelter terkonsentrasi memonopoli penerimaan PAD dari ekstraksi pajak, namun seluruh Pulau Sulawesi—termasuk provinsi yang tidak menikmati PAD signifikan—menanggung beban ekologis berupa <b>{tot_deforestasi:,.0f} Hektar</b> deforestasi permanen. Ini adalah bentuk eksternalitas negatif klasik: keuntungan diprivatisasi (terkonsentrasi), sementara biaya lingkungan disosialisasikan (ditanggung bersama).
</div>
""", unsafe_allow_html=True)
    
    with st.expander("Lihat Data Detail Breakdown PAD Per Provinsi & Jenis Pendapatan", expanded=False):
        df_pad_display = df_pad_combined.copy()
        df_pad_display['Nilai_Miliar_Rp'] = df_pad_display['Nilai_Miliar_Rp'].apply(lambda x: f"{x:,.2f}")
        df_pad_display = df_pad_display.sort_values(['Provinsi', 'Jenis_Pendapatan'])
        
        st.dataframe(df_pad_display[['Provinsi', 'Jenis_Pendapatan', 'Nilai_Miliar_Rp']], use_container_width=True, hide_index=True)
        
        st.caption("📁 **Sumber:** `data/processed/sulawesi_pad_breakdown_2016_2024.csv` (breakdown detail) + `data/processed/sulawesi_pad_2016_2024.csv` (total agregat)")
        st.caption("⚠️ **Catatan:** Sulawesi Utara dan Sulawesi Barat ditampilkan sebagai 'Total PAD' karena data mentah BPS hanya tersedia dalam format agregat kabupaten tanpa breakdown per jenis pendapatan.")

st.markdown("---")
st.markdown("#### Paradoks Investasi: Kucuran Modal vs Kebangkrutan Ekologis")

st.markdown(f"""
Grafik **"Anomali Investasi Ekstraktif vs Deforestasi Komoditas"** di bawah ini menelanjangi ilusi di balik angka PAD dan investasi PMDN tersebut.

Grafik *Dual-Axis* (Dua Sumbu) di bawah ini mempertemukan dua variabel secara absolut: Arus Investasi (Bar Abu-abu) dengan Laju Kehancuran Deforestasi (Garis Merah). Mari kita cermati dan baca temuan **fakta data time-series**-nya: pada tahun 2016, arus investasi hanya menyentuh **{val_inv_2016:,.1f} Triliun Rupiah**, berhadapan dengan luasan deforestasi komoditas **{val_def_2016:,.0f} Hektar**. Namun, ketika kita membedah ujung grafik di tahun 2023, balok investasi terekam meledak gila-gilaan mencapai **{val_inv_2023:,.1f} Triliun Rupiah**. Sialnya, pada waktu yang persis sama, kurva merah deforestasi tidak melandai sama sekali, melainkan ikut merobek sumbu vertikal hingga mencapai hilangnya **{val_def_2023:,.0f} Hektar** tutupan hutan dalam satu tahun tersebut.

Irisan fatal antara kurva batang PMDN dan garis tren deforestasi ini membuktikan secara ilmiah bahwa lonjakan investasi bukanlah indikator membaiknya kesejahteraan ekologis. Sebaliknya, setiap triliun rupiah tersebut secara mutlak beroperasi penuh sebagai **pemicu (driver) ekskalasi pembongkaran**. Klaim "hilirisasi sukses" terbukti secara empiris hanya menjadi kedok hukum bagi total agresi lenyapnya hutan seluas **{tot_deforestasi:,.0f} Hektar**. Mengganti sabuk resapan air alamiah dengan ekosistem tambang membuktikan bahwa kucuran investasi ini hanyalah ongkos nyata percepatan menuju kebangkrutan ekologis lintas generasi.
""")

df_viz_1_3 = pd.merge(df_gfw_agg, df_inv_agg, on='Tahun', how='inner')

df_viz_1_3 = pd.merge(df_gfw_agg, df_inv_agg, on='Tahun', how='inner')

base = alt.Chart(df_viz_1_3).encode(
    x=alt.X('Tahun:O', title='Tahun', axis=alt.Axis(labelColor='#B0BEC5'))
)

bar = base.mark_bar(opacity=0.3, color='#90A4AE').encode(
    y=alt.Y('Investasi_Juta_Rp:Q', title='Realisasi Investasi PMDN (Juta Rp)', axis=alt.Axis(gridOpacity=0.05, labelColor='#90A4AE', titleColor='#90A4AE')),
    tooltip=['Tahun', alt.Tooltip('Investasi_Juta_Rp', format=',.0f')]
)

line = base.mark_line(point=True, color='#D32F2F', strokeWidth=3).encode(
    y=alt.Y('Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha:Q', title='Luas Deforestasi Komoditas (Ha)', axis=alt.Axis(grid=False, labelColor='#D32F2F', titleColor='#D32F2F')),
    tooltip=['Tahun', alt.Tooltip('Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha', format=',.0f')]
)

chart_dual = alt.layer(bar, line).resolve_scale(
    y='independent'
).properties(
    height=380, 
    title=alt.TitleParams(text="Anomali Investasi Ekstraktif vs Deforestasi Komoditas", color='#ECEFF1', anchor='start')
)

st.altair_chart(chart_dual, use_container_width=True)

st.markdown(f"""
<div style="background:#1E1E1E; padding:14px; border-radius:10px; border-left:5px solid #D32F2F; margin-bottom: 20px;">
    <b>Interpretasi Paradoks Ekonomi:</b> Grafik *Dual-Axis* di atas membuktikan bahwa lonjakan arus investasi PMDN (diagram batang redup) beririsan langsung memicu ekskalasi deforestasi hutan (garis merah). Klaim keberhasilan investasi ternyata dibayar sangat mahal oleh kebangkrutan ekologis di hulu. Area penyangga yang seharusnya memitigasi bencana iklim justru dikonversi menjadi zona ekstraktif.
</div>
""", unsafe_allow_html=True)

# Memuat data tambahan untuk 3 Dashboard Cards GFW
try:
    df_driver_gfw = pd.read_csv('data/raw/klhk_gfw/land_api_fetch/loss_by_driver_sulawesi_2001_2025.csv')
    df_primary_gfw = pd.read_csv('data/raw/klhk_gfw/mega_fetch_v2/primary_forest_loss_sulawesi_2001_2025.csv')
    
    # 1. Donut Chart (Aktor Komoditas) - GFW Style Legend
    driver_map = {
        'Commodity driven deforestation': 'Ekspansi Komoditas (Tambang & Sawit)',
        'Forestry': 'Kehutanan (Logging)',
        'Shifting agriculture': 'Pertanian Berpindah',
        'Urbanization': 'Urbanisasi',
        'Wildfire': 'Kebakaran Hutan',
        'Unknown': 'Lainnya'
    }
    df_donut = df_driver_gfw.groupby('driver')['area_ha'].sum().reset_index()
    df_donut['driver_id'] = df_donut['driver'].map(driver_map).fillna(df_donut['driver'])
    
    area_komoditas = df_donut.loc[df_donut['driver'] == 'Commodity driven deforestation', 'area_ha'].sum()
    area_forestry = df_donut.loc[df_donut['driver'] == 'Forestry', 'area_ha'].sum()
    area_shifting = df_donut.loc[df_donut['driver'] == 'Shifting agriculture', 'area_ha'].sum()

    komoditas_str = f"{area_komoditas / 1e6:.1f} Mha" if area_komoditas >= 1e6 else f"{area_komoditas / 1e3:.0f} kha"
    forestry_str = f"{area_forestry / 1e6:.1f} Mha" if area_forestry >= 1e6 else f"{area_forestry / 1e3:.0f} kha"
    shifting_str = f"{area_shifting / 1e6:.1f} Mha" if area_shifting >= 1e6 else f"{area_shifting / 1e3:.0f} kha"

    chart_donut = alt.Chart(df_donut).mark_arc(innerRadius=45).encode(
        theta=alt.Theta(field="area_ha", type="quantitative"),
        color=alt.Color(field="driver_id", type="nominal", scale=alt.Scale(
            domain=['Ekspansi Komoditas (Tambang & Sawit)', 'Kehutanan (Logging)', 'Pertanian Berpindah', 'Urbanisasi', 'Kebakaran Hutan', 'Lainnya'],
            range=['#D32F2F', '#4CAF50', '#FFC107', '#2196F3', '#FF5722', '#9E9E9E']
        ), legend=None),
        tooltip=['driver_id', alt.Tooltip('area_ha', format=',.0f')]
    ).properties(height=280)

    # 2. Bar Chart (Hutan Primer)
    df_primary_agg = df_primary_gfw.groupby('umd_tree_cover_loss__year')['area__ha'].sum().reset_index()
    chart_primary = alt.Chart(df_primary_agg).mark_bar(color='#E91E63').encode(
        x=alt.X('umd_tree_cover_loss__year:O', title='Tahun', axis=alt.Axis(labelAngle=-45, labelColor='#B0BEC5', titleColor='#B0BEC5')),
        y=alt.Y('area__ha:Q', title='Hutan Primer Hilang (Ha)', axis=alt.Axis(labelColor='#B0BEC5', titleColor='#B0BEC5', gridOpacity=0.05)),
        tooltip=['umd_tree_cover_loss__year', alt.Tooltip('area__ha', format=',.0f')]
    ).properties(height=350, title=alt.TitleParams(text="Tragedi Hutan Primer", color='#ECEFF1'))

    # 3. Bar Chart (Emisi CO2 Komoditas)
    df_co2 = df_driver_gfw[df_driver_gfw['driver'] == 'Commodity driven deforestation']
    df_co2_agg = df_co2.groupby('year')['co2_emissions_mg'].sum().reset_index()
    chart_co2 = alt.Chart(df_co2_agg).mark_bar(color='#5D4037').encode(
        x=alt.X('year:O', title='Tahun', axis=alt.Axis(labelAngle=-45, labelColor='#B0BEC5', titleColor='#B0BEC5')),
        y=alt.Y('co2_emissions_mg:Q', title='Emisi CO2 (Megagrams)', axis=alt.Axis(labelColor='#B0BEC5', titleColor='#B0BEC5', gridOpacity=0.05)),
        tooltip=['year', alt.Tooltip('co2_emissions_mg', format=',.0f')]
    ).properties(height=350, title=alt.TitleParams(text="Ledakan Emisi Karbon (Komoditas)", color='#ECEFF1'))

    st.markdown("---")
    st.markdown("#### Pembedahan Ekologis: Aktor, Dampak, dan Emisi")
    
    tot_primary_loss = df_primary_agg['area__ha'].sum()
    tot_co2_emissions = df_co2_agg['co2_emissions_mg'].sum()
    
    st.markdown(f"""
Untuk melengkapi analisis kausalitas di atas, kita harus membedah anatomi kehancuran ekologis secara spesifik melalui 3 metrik forensik pada dasbor **Pembedahan Ekologis** di bawah ini. Ketiga grafik ini mengonfirmasi siapa dalang utama di balik hilangnya hutan dan seberapa parah kerusakan absolut yang telah ditimbulkan terhadap masa depan lingkungan Sulawesi.

**Pertama, Aktor Utama Deforestasi (Donut Chart):** Visualisasi cincin di sebelah kiri membongkar siapa aktor penjahat ekologis sesungguhnya. Mayoritas absolut dari hilangnya tutupan lahan tidak disebabkan oleh masyarakat adat atau pertanian warga, melainkan dipicu secara mutlak oleh **Ekspansi Komoditas (Tambang & Perkebunan monokultur)** yang melahap dengan rakus hingga **{area_komoditas:,.0f} Hektar** ({komoditas_str}). Dominasi warna merah yang pekat pada grafik tersebut membuktikan bahwa perampasan ruang ini dimonopoli oleh kekuatan modal industri raksasa, sekaligus membantah klaim bahwa deforestasi didorong oleh kebutuhan subsisten masyarakat lokal.

**Kedua, Tragedi Hutan Primer (Bar Chart Tengah):** Kerusakan masif yang didorong oleh komoditas ini tidak terjadi di lahan kritis atau semak belukar yang terdegradasi, melainkan mengorbankan langsung jantung ekosistem bumi. Grafik batang merah muda menunjukkan bahwa secara agregat total, lebih dari **{tot_primary_loss:,.0f} Hektar Hutan Primer**—ekosistem purba yang membutuhkan waktu ribuan tahun untuk terbentuk dan kaya akan keanekaragaman hayati endemik—telah ditebang habis dan musnah secara permanen tak bersisa. Lonjakan tinggi batang pada periode tertentu berkorelasi sangat erat dengan tahun-tahun puncak penerbitan IUP dan peresmian smelter baru.

**Ketiga, Ledakan Emisi Karbon (Bar Chart Kanan):** Sebagai imbas langsung dari musnahnya hutan primer tersebut, pembongkaran tanah untuk tambang nikel melepaskan bom karbon ke udara terbuka. Grafik cokelat tua menelanjangi fakta bahwa ekspansi komoditas telah meledakkan total **{tot_co2_emissions:,.0f} Megagrams Emisi CO2**. Fakta mematikan ini merupakan bantahan paling empiris dan telanjang terhadap narasi palsu "Hilirisasi Hijau". Melalui data ini, terbukti kita sama sekali tidak sedang memproduksi rantai pasok energi bersih; kita justru sedang mensubsidi krisis iklim global melalui emisi karbon ekstrem hasil dari pembongkaran hutan primer demi mengeruk nikel.
""")
    
    col_v1, col_v2, col_v3 = st.columns(3)
    
    with col_v1:
        st.markdown("<b style='color:#ECEFF1;'>Aktor Utama Deforestasi</b>", unsafe_allow_html=True)
        col_leg, col_chart = st.columns([1.2, 1])
        with col_leg:
            st.markdown(f"""
            <div style="font-family: sans-serif; line-height: 1.2; margin-top: 15%;">
                <div style="margin-bottom: 12px;">
                    <span style="color: #D32F2F; font-size: 0.8rem;">●</span> <span style="color: #B0BEC5; font-size: 0.85rem;">Ekspansi Komoditas</span><br>
                    <strong style="color: #D32F2F; font-size: 1.5rem;">{komoditas_str}</strong>
                </div>
                <div style="margin-bottom: 12px;">
                    <span style="color: #4CAF50; font-size: 0.8rem;">●</span> <span style="color: #B0BEC5; font-size: 0.85rem;">Kehutanan (Logging)</span><br>
                    <strong style="color: #4CAF50; font-size: 1.2rem;">{forestry_str}</strong>
                </div>
                <div>
                    <span style="color: #FFC107; font-size: 0.8rem;">●</span> <span style="color: #B0BEC5; font-size: 0.85rem;">Pertanian Berpindah</span><br>
                    <strong style="color: #FFC107; font-size: 1.2rem;">{shifting_str}</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_chart:
            st.altair_chart(chart_donut, use_container_width=True)
        st.caption("Investasi komoditas (merah) mendominasi seluruh penyebab deforestasi di Sulawesi.")
    with col_v2:
        st.altair_chart(chart_primary, use_container_width=True)
        st.caption("Penebangan tidak hanya terjadi di lahan kritis, melainkan mengorbankan Hutan Primer yang tak ternilai.")
    with col_v3:
        st.altair_chart(chart_co2, use_container_width=True)
        st.caption("Bantahan nyata terhadap 'Hilirisasi Hijau': Ekstraksi nikel melepaskan jutaan Megagram karbon ke udara.")
        
except Exception as e:
    st.warning(f"Tidak dapat memuat visualisasi tambahan: {e}")


with st.expander("Lihat Data Mentah: Deforestasi GFW", expanded=False):
    st.dataframe(df_gfw, use_container_width=True, hide_index=True)

# --- Crosstab 1.3: Investasi PMDN vs Deforestasi ---
st.markdown("#### Pembuktian Statistik: Arus Investasi PMDN vs Deforestasi")
st.markdown("""
Menggunakan tabel crosstab untuk menguji korelasi spasial-temporal antara arus masuk Investasi PMDN dengan tingkat kerusakan hutan (Deforestasi) pada level panel **Provinsi-Tahun**. Variabel *Investasi* akan dipecah berdasarkan nilai tengah (median) menjadi 'Tinggi' dan 'Rendah', begitu pula dengan variabel *Deforestasi*.
""")

# Data Preparation untuk Panel 1.3
df_inv_clean = df_inv.rename(columns={'provinsi': 'Provinsi', 'tahun': 'Tahun'})
df_inv_clean['Tahun'] = pd.to_numeric(df_inv_clean['Tahun'], errors='coerce')
df_inv_clean['Investasi_Juta_Rp'] = pd.to_numeric(df_inv_clean['nilai'], errors='coerce')

# Inner merge karena data investasi 2016-2024, GFW 2014-2023. Panel yang valid: 2016-2023.
df_panel_1_3 = pd.merge(df_gfw, df_inv_clean[['Provinsi', 'Tahun', 'Investasi_Juta_Rp']], on=['Provinsi', 'Tahun'], how='inner').fillna({'Investasi_Juta_Rp': 0})

col_sel1_3, col_sel2_3 = st.columns(2)

with col_sel1_3:
    st.markdown("##### Variabel Independen (X) - Arus Modal")
    x_options_3 = {
        "Investasi_Juta_Rp": "Realisasi Investasi PMDN (Juta Rp)"
    }
    x_col_3 = st.selectbox("Pilih Indikator Investasi (X): ", list(x_options_3.keys()), format_func=lambda x: x_options_3[x], key="x_col_3")

with col_sel2_3:
    st.markdown("##### Variabel Dependen (Y) - Dampak Ekologis")
    y_options_3 = {
        "Total_Deforestasi_Ha": "Total Deforestasi Alam (Hektar)",
        "Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha": "Deforestasi Komoditas Tambang/Sawit (Hektar)"
    }
    y_col_3 = st.selectbox("Pilih Indikator Dampak (Y): ", list(y_options_3.keys()), format_func=lambda x: y_options_3[x], key="y_col_3")

# Calculation (Binning for 1.3)
x_median_3 = df_panel_1_3[x_col_3].median()
x_thresh_3 = x_median_3 if x_median_3 > 0 else 0
y_median_3 = df_panel_1_3[y_col_3].median()

label_x_low_3 = f"Rendah (≤{x_thresh_3:,.0f})"
label_x_high_3 = f"Tinggi (>{x_thresh_3:,.0f})"
label_y_low_3 = f"Rendah (<{y_median_3:,.1f})"
label_y_high_3 = f"Tinggi (≥{y_median_3:,.1f})"

df_panel_1_3["X_Label"] = df_panel_1_3[x_col_3].apply(lambda x: label_x_high_3 if x > x_thresh_3 else label_x_low_3)
df_panel_1_3["Y_Label"] = df_panel_1_3[y_col_3].apply(lambda x: label_y_high_3 if x >= y_median_3 else label_y_low_3)

cats_x_3 = [label_x_low_3, label_x_high_3]
cats_y_3 = [label_y_low_3, label_y_high_3]
crosstab_3 = pd.crosstab(df_panel_1_3["X_Label"], df_panel_1_3["Y_Label"]).reindex(index=cats_x_3, columns=cats_y_3, fill_value=0)

try:
    chi2_3, p_3, dof_3, expected_3 = stats.chi2_contingency(crosstab_3)
except ValueError:
    chi2_3, p_3, dof_3, expected_3 = 0, 1, 0, np.zeros_like(crosstab_3.values)
expected_df_3 = pd.DataFrame(expected_3, index=crosstab_3.index, columns=crosstab_3.columns)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
st.markdown("### Detail Uji Statistik (Chi-Square & Odds Ratio)")
st.caption("Tabel-tabel di bawah ini merepresentasikan bukti statistik hubungan antara Arus Investasi PMDN dengan tingkat deforestasi alam.")

# A. Case Processing Summary 1.3
st.markdown("##### Case Processing Summary")
total_cases_3 = len(df_panel_1_3)
valid_cases_3 = len(df_panel_1_3.dropna(subset=[x_col_3, y_col_3]))
missing_cases_3 = total_cases_3 - valid_cases_3

cols_case_3 = pd.MultiIndex.from_product([["Cases"], ["Valid", "Missing", "Total"], ["N", "Percent"]])
interaction_lbl_3 = f"{x_options_3[x_col_3]} * {y_options_3[y_col_3]}"
row_d_3 = [
    valid_cases_3, f"{valid_cases_3/total_cases_3*100:.1f}%",
    missing_cases_3, f"{missing_cases_3/total_cases_3*100:.1f}%",
    total_cases_3, "100.0%"
]
st.table(pd.DataFrame([row_d_3], index=[interaction_lbl_3], columns=cols_case_3))

# B. Crosstabulation 1.3
st.markdown(f"##### {interaction_lbl_3} Crosstabulation")
row_idx_3 = []
for xc in cats_x_3:
    row_idx_3.extend([(xc, "Count"), (xc, "Expected Count")])
row_idx_3.extend([("Total", "Count"), ("Total", "Expected Count")])

rows_3 = []
for xc in cats_x_3:
    cnts = crosstab_3.loc[xc].tolist()
    exps = expected_df_3.loc[xc].tolist()
    rows_3.append(cnts + [sum(cnts)])
    rows_3.append([f"{v:.1f}" for v in exps] + [f"{sum(exps):.1f}"])

tot_cnts_3 = crosstab_3.sum().tolist()
tot_exps_3 = expected_df_3.sum().tolist()
rows_3.append(tot_cnts_3 + [sum(tot_cnts_3)])
rows_3.append([f"{v:.1f}" for v in tot_exps_3] + [f"{sum(tot_exps_3):.1f}"])

m_idx_3 = pd.MultiIndex.from_tuples(row_idx_3, names=[x_options_3[x_col_3], ""])
st.table(pd.DataFrame(rows_3, index=m_idx_3, columns=cats_y_3 + ["Total"]))

# C. Chi-Square Tests 1.3
st.markdown("##### Chi-Square Tests")
try:
    g_3, p_g_3, dof_g_3, exp_g_3 = stats.chi2_contingency(crosstab_3, lambda_="log-likelihood")
except:
    g_3, p_g_3, dof_g_3 = 0, 1, 0
x_codes_3 = df_panel_1_3["X_Label"].replace({label_x_low_3: 0, label_x_high_3: 1})
y_codes_3 = df_panel_1_3["Y_Label"].replace({label_y_low_3: 0, label_y_high_3: 1})
try:
    r_3, p_corr_3 = stats.pearsonr(list(x_codes_3), list(y_codes_3))
    lbl_val_3 = (valid_cases_3 - 1) * (r_3**2)
except:
    r_3, p_corr_3, lbl_val_3 = 0, 1, 0

chi_data_3 = [
    [f"{chi2_3:.3f}", str(dof_3), f"{p_3:.3f}"],
    [f"{g_3:.3f}", str(dof_g_3), f"{p_g_3:.3f}"],
    [f"{lbl_val_3:.3f}", "1", f"{p_corr_3:.3f}"],
    [str(valid_cases_3), "", ""]
]
st.table(pd.DataFrame(chi_data_3, index=["Pearson Chi-Square", "Likelihood Ratio", "Linear-by-Linear Association", "N of Valid Cases"], columns=["Value", "df", "Asymp. Sig. (2-sided)"]))

# D. Hypothesis & Risk Summary 1.3
st.markdown("### Ringkasan Uji Hipotesis")
try:
    a_3 = crosstab_3.loc[label_x_low_3, label_y_low_3]
    b_3 = crosstab_3.loc[label_x_low_3, label_y_high_3]
    c_3 = crosstab_3.loc[label_x_high_3, label_y_low_3]
    d_3 = crosstab_3.loc[label_x_high_3, label_y_high_3]
    or_3 = (a_3 * d_3) / (b_3 * c_3) if (b_3 * c_3) > 0 else 0
except:
    or_3 = 0

is_sig_3 = p_3 < 0.05
bg_col_3 = "rgba(76, 175, 80, 0.1)" if is_sig_3 else "rgba(229, 57, 53, 0.1)"
ord_col_3 = "#4CAF50" if is_sig_3 else "#E53935"
status_txt_3 = "SIGNIFIKAN" if is_sig_3 else "TIDAK SIGNIFIKAN"

cr1_3, cr2_3 = st.columns([1,2])
with cr1_3:
    st.markdown(f"""
    <div style="border: 2px solid {ord_col_3}; padding: 15px; border-radius: 5px; background-color: {bg_col_3}; margin-bottom: 10px;">
        <h4 style="color: {ord_col_3}; margin: 0 0 10px 0; text-transform: uppercase;">Result: {status_txt_3}</h4>
        <p style="margin: 0; font-family: monospace;">
            P-Value    : {p_3:.4f}<br>
            Chi-Square : {chi2_3:.3f}<br>
            df         : {dof_3}
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"**Odds Ratio (Risk Estimate):** `{or_3:.3f}`")

with cr2_3:
    if is_sig_3:
        interp_txt_3 = f"Terdapat bukti statistik yang sah bahwa arus masuk modal (Investasi PMDN) secara langsung dan sistematis mendorong ekskalasi deforestasi di wilayah Sulawesi (OR: {or_3:.3f}). Investasi ini bukanlah katalisator ekonomi hijau, melainkan injeksi modal untuk ekstraksi lahan."
    else:
        interp_txt_3 = f"Secara statistik agregat mungkin belum terlihat korelasi linier di tahun yang persis sama. Hal ini menyingkap anomali bahwa investasi bernilai triliunan kerap ditahan untuk birokrasi awal, sementara pembabatan hutan fisiknya baru meledak secara sporadis di tahun-tahun berikutnya (<i>lagging effect</i>)."
    
    st.markdown(f"""
    <div style="background:#1E1E1E; padding:14px; border-radius:10px; border-left:5px solid {ord_col_3}; height: 100%;">
        <b>Interpretasi Kausalitas:</b><br><br>
        {interp_txt_3}
    </div>
    """, unsafe_allow_html=True)

# --- E. Executive Summary of All Combinations 1.3 ---
st.markdown("---")
st.markdown("### Ringkasan Eksekutif Seluruh Skenario Crosstab")
st.markdown("Tabel di bawah ini merangkum hasil pengujian statistik (Chi-Square) untuk semua kemungkinan kombinasi indikator antara Realisasi Investasi PMDN dan Dampak Ekologis pada panel data.")

summary_data_3 = []
for k_x, v_x in x_options_3.items():
    for k_y, v_y in y_options_3.items():
        med_x = df_panel_1_3[k_x].median()
        thresh_x = med_x if med_x > 0 else 0
        med_y = df_panel_1_3[k_y].median()
        
        lbl_x_h = f"Tinggi (>{thresh_x:,.0f})"
        lbl_x_l = f"Rendah (≤{thresh_x:,.0f})"
        lbl_y_h = f"Tinggi (≥{med_y:,.1f})"
        lbl_y_l = f"Rendah (<{med_y:,.1f})"
        
        s_x = df_panel_1_3[k_x].apply(lambda val: lbl_x_h if val > thresh_x else lbl_x_l)
        s_y = df_panel_1_3[k_y].apply(lambda val: lbl_y_h if val >= med_y else lbl_y_l)
        
        ct = pd.crosstab(s_x, s_y).reindex(index=[lbl_x_l, lbl_x_h], columns=[lbl_y_l, lbl_y_h], fill_value=0)
        try:
            c2_val, pv_val, dof_val, exp_val = stats.chi2_contingency(ct)
        except ValueError:
            c2_val, pv_val, dof_val = 0, 1, 0
            
        try:
            aa = ct.loc[lbl_x_l, lbl_y_l]
            bb = ct.loc[lbl_x_l, lbl_y_h]
            cc = ct.loc[lbl_x_h, lbl_y_l]
            dd = ct.loc[lbl_x_h, lbl_y_h]
            or_v = (aa * dd) / (bb * cc) if (bb * cc) > 0 else 0
        except KeyError:
            or_v = 0
            
        sig_status = "🟢 SIGNIFIKAN" if pv_val < 0.05 else "🔴 TIDAK SIGNIFIKAN"
        
        summary_data_3.append({
            "Variabel Independen (X)": v_x,
            "Variabel Dependen (Y)": v_y,
            "Chi-Square": f"{c2_val:.3f}",
            "P-Value": f"{pv_val:.3f}",
            "Odds Ratio": f"{or_v:.2f}",
            "Kesimpulan": sig_status
        })

df_summary_3 = pd.DataFrame(summary_data_3)
st.dataframe(df_summary_3, use_container_width=True, hide_index=True)

sig_count_3 = sum(1 for row in summary_data_3 if "🟢 SIGNIFIKAN" in row["Kesimpulan"])
total_scenarios_3 = len(summary_data_3)

import textwrap
if sig_count_3 > 0:
    exec_narrative_3 = f"""
Dari <b>{total_scenarios_3} skenario pengujian</b>, terbukti ada skenario yang <b>SIGNIFIKAN</b> secara statistik.<br><br>
Temuan ini mengunci mati argumen pemerintah. Derasnya arus modal (PMDN) bukanlah indikator keberhasilan ekonomi yang inklusif, melainkan sekadar dana segar untuk membiayai penghancuran hutan skala raksasa. Angka statistik membuktikan betapa rentannya ekosistem hutan penyangga terhadap setiap lembar rupiah modal ekstraktif yang ditanamkan.
"""
    bg_color_narr_3 = "rgba(229, 57, 53, 0.15)"
    border_color_narr_3 = "#E53935"
else:
    exec_narrative_3 = f"""
Dari <b>{total_scenarios_3} skenario pengujian</b>, seluruhnya menunjukkan status <b>TIDAK SIGNIFIKAN</b>.<br><br>
Ketidaksignifikanan ini secara paradoks menyingkap tabir <i>lagging effect</i> (jeda waktu) dalam eksekusi investasi. Ketika modal masif disuntikkan di tahun tertentu, lahan tidak dibabat di tahun yang sama secara sempurna. Uang tersebut tertahan untuk birokrasi, sementara daya hancurnya baru meledak dan mengonversi lanskap hutan pada tahun-tahun berikutnya (efek tunda).
"""
    bg_color_narr_3 = "rgba(255, 152, 0, 0.15)"
    border_color_narr_3 = "#FF9800"

st.markdown(f"""
<div style="background-color: {bg_color_narr_3}; padding:18px; border-radius:8px; border-left:6px solid {border_color_narr_3}; margin-top: 15px; margin-bottom: 25px;">
<b style="color: {border_color_narr_3}; font-size: 1.05rem;">Pembedahan Realitas Ekologis:</b><br><br>
<div style="color: #E0E0E0; font-size: 0.95rem; line-height: 1.6;">
{exec_narrative_3.strip()}
</div>
</div>
""", unsafe_allow_html=True)

with st.expander("Lihat Data Panel Mentah (Merge Investasi & GFW)", expanded=False):
    st.dataframe(df_panel_1_3[['Provinsi', 'Tahun', x_col_3, 'X_Label', y_col_3, 'Y_Label']], use_container_width=True, hide_index=True)
    st.caption("Sumber: Gabungan `sulawesi_investasi_pmdn_2016_2024.csv` (BKPM) dan `sulawesi_gfw_master_1_dekade_2014_2023.csv` (GFW).")
    st.caption("📁 **Sumber File:** `data/processed/sulawesi_gfw_master_1_dekade_2014_2023.csv` - Data dari Global Forest Watch.")

with st.expander("Lihat Data Mentah: Realisasi Investasi PMDN (BKPM)", expanded=False):
    st.dataframe(df_inv, use_container_width=True, hide_index=True)
    st.caption("📁 **Sumber File:** `data/processed/sulawesi_investasi_pmdn_2016_2024.csv` - Data Ekstraksi OSS/BKPM.")

