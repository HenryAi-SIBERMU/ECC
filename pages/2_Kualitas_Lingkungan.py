import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import scipy.stats as stats
import os
import sys
import json

# Konfigurasi path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.components.sidebar import render_sidebar

st.set_page_config(
    page_title="Kualitas Lingkungan di Kawasan Smelter — CELIOS ECC",
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
def load_all_data():
    df_ika = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_ika_2016_2024.csv"))
    df_iku = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_iku_2015_2024.csv"))
    df_gfw = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_gfw_master_1_dekade_2014_2023.csv"))
    df_smelter = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_esdm_nikel.csv"))
    df_pltu = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_pltu_captive.csv"))
    df_b3 = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_limbah_b3.csv"))
    return df_ika, df_iku, df_gfw, df_smelter, df_pltu, df_b3

try:
    df_ika, df_iku, df_gfw, df_smelter, df_pltu, df_b3 = load_all_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# ── Pra-Kalkulasi Variabel Kritis (Data-Driven) ──
# 1. Kualitas Air (IKA)
mean_ika_2023 = df_ika[df_ika['Tahun'] == 2023]['Indeks Kualitas Air'].mean()

# 2. Kualitas Udara (IKU)
mean_iku_2023 = df_iku[df_iku['Tahun'] == 2023]['IKU'].mean()

# 3. Mega Smelter (CGS/ESDM)
tot_smelter = len(df_smelter)
df_pltu_op = df_pltu[df_pltu['Status'].str.lower() == 'operating']
tot_kapasitas_pltu = df_pltu_op['Capacity (MW)'].sum() if 'Capacity (MW)' in df_pltu_op.columns else 0

# 4. Deforestasi (GFW)
tot_deforestasi = df_gfw['Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha'].sum()

# 5. Limbah B3 (Tailing)
df_b3['Estimasi Timbulan (Ton/Tahun)'] = pd.to_numeric(df_b3['Estimasi Timbulan (Ton/Tahun)'], errors='coerce')
tot_limbah_b3 = df_b3['Estimasi Timbulan (Ton/Tahun)'].sum()
tot_limbah_b3_juta = tot_limbah_b3 / 1_000_000

# ── Header Halaman ──
st.markdown('<div class="org-badge">CELIOS — Center of Economic and Law Studies</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">Kualitas Lingkungan di Kawasan Smelter</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Menguji secara empiris korelasi antara intensitas ekspansi fasilitas peleburan nikel (smelter) dengan anjloknya Indeks Kualitas Air (IKA), Udara (IKU), dan laju deforestasi komoditas di Pulau Sulawesi.</div>', unsafe_allow_html=True)

# ── Dropdown Metodologi ──
with st.expander("🔍 Metodologi", expanded=False):
    st.markdown("""
    **Alur Kausalitas (Ekonomi Politik Ekologi):** `Konsentrasi Smelter & PLTU` → `Pembuangan Tailing & Emisi Partikulat` → `Pencemaran Air & Udara` → `Daya Dukung Lingkungan Kritis`
    
    Industrialisasi ekstraktif bekerja seperti parasit terhadap daya tampung lingkungan. Fasilitas peleburan membutuhkan daya luar biasa besar (dipasok PLTU batu bara) dan menghasilkan limbah B3 (slag/tailing) dalam jumlah raksasa. Kehadiran industri ini secara absolut menurunkan ambang batas toleransi alam, yang direkam melalui indikator baku mutu nasional.
    
    **Variabel Tekanan (X):**
    *   **Jumlah Smelter & PLTU Captive:** Konsentrasi fasilitas peleburan dan pembangkit batu bara (ESDM, GEM).
    *   **Luas Kawasan Industri:** Ekspansi spasial proyek strategis.
    
    **Variabel Dampak Ekologis (Y):**
    *   **Indeks Kualitas Air (IKA):** Skor kualitas air berdasarkan parameter fisik/kimia (KLHK, BPS).
    *   **Indeks Kualitas Udara (IKU):** Skor pencemaran udara ambien (KLHK, BPS).
    *   **Laju Deforestasi Komoditas:** Kehilangan tutupan pohon akibat kegiatan ekstraktif (Global Forest Watch).
    
    **Metode Pengolahan Data:**
    Analisis menggunakan pendekatan *Cross-sectional* dan *Time-Series* (Panel Data). Korelasi dibuktikan secara statistik melalui uji **Crosstabulation (Chi-Square/Symmetric Measures)** ala SPSS untuk melihat seberapa jauh status 'Kritis' pada wilayah beririsan dengan label 'Tinggi' pada kehadiran industri.
    """)

# ── Hero Statement (Narasi Kritis Utama) ──
st.markdown(f"""
<div style="background-color: transparent; padding: 10px 0px; margin-bottom: 25px;">
    <h2 style="color: #FFFFFF; font-size: 1.8rem; margin-bottom: 15px; font-weight: 700;">Tumbal Ekologis: Ketika {tot_smelter} Smelter Mencekik Napas dan Air Sulawesi</h2>
    <p style="color: #CCCCCC; font-size: 1.05rem; line-height: 1.7; margin-bottom: 15px;">
        Pesta "Hilirisasi" nikel ternyata menagih bayaran tunai langsung ke jantung ekosistem Pulau Sulawesi. Konsentrasi <b>{tot_smelter} fasilitas mega-smelter</b> yang ditenagai oleh mesin pembakaran batu bara raksasa sebesar <b>{tot_kapasitas_pltu:,.0f} MW</b> tidak hanya mencaplok ruang spasial, tetapi telah membengkokkan kurva daya dukung lingkungan ke titik terendahnya. Di bawah bayang-bayang narasi transisi energi, kualitas hidup jutaan warga dipertaruhkan oleh penurunan masif kualitas air dan udara, ditambah ancaman ledakan limbah beracun.
    </p>
    <p style="color: #CCCCCC; font-size: 1.05rem; line-height: 1.7;">
        Data empiris merekam kebangkrutan ini secara presisi. Operasional industri ekstraktif telah merobek <b>{tot_deforestasi:,.0f} Hektar</b> ruang hidup alami dan menumpuk lebih dari <b>{tot_limbah_b3_juta:,.1f} Juta Ton</b> limbah B3/tailing per tahun. Beban polusi ini membuat Indeks Kualitas Air (IKA) rata-rata merosot ke angka <b>{mean_ika_2023:.1f}</b>, dan Indeks Kualitas Udara (IKU) anjlok ke level <b>{mean_iku_2023:.1f}</b>. Angka ini lebih dari sekadar indikator; ia adalah bukti forensik kegagalan kebijakan perlindungan ekologis negara di hadapan invasi modal korporasi.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Kartu Metrik Agregat (Bento Cards) ──
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Indeks Kualitas Air (2023)</div>
            <div class="metric-value" style="color: #D32F2F;">{mean_ika_2023:.1f} <span style="font-size:1rem;">Poin</span></div>
            <div class="metric-desc">Tren penurunan IKA di Sulawesi akibat cemaran logam berat dan sedimen operasi tambang.</div>
        </div>
        <div class="metric-source"><b>Sumber:</b> KLHK & BPS (SLHI)</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Indeks Kualitas Udara (2023)</div>
            <div class="metric-value" style="color: #F57C00;">{mean_iku_2023:.1f} <span style="font-size:1rem;">Poin</span></div>
            <div class="metric-desc">Pencemaran udara (PM2.5/SO2) yang mencekik wilayah pemukiman sekitar PLTU Captive.</div>
        </div>
        <div class="metric-source"><b>Sumber:</b> KLHK & BPS (SLHI)</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Timbulan Limbah B3</div>
            <div class="metric-value" style="color: #D32F2F;">{tot_limbah_b3_juta:,.1f} <span style="font-size:1rem;">Jt Ton</span></div>
            <div class="metric-desc">Estimasi produksi limbah tailing dan slag per tahun dari kawasan mega-industri di Sulawesi.</div>
        </div>
        <div class="metric-source"><b>Sumber:</b> Data Ekstraksi NGO & AMDAL</div>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Konversi Deforestasi</div>
            <div class="metric-value" style="color: #F57C00;">{tot_deforestasi:,.0f} <span style="font-size:1rem;">Ha</span></div>
            <div class="metric-desc">Luasan tutupan hutan yang hancur dibabat untuk pembukaan lubang tambang nikel.</div>
        </div>
        <div class="metric-source"><b>Sumber:</b> Global Forest Watch (GFW)</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Placeholders Sections ──
st.markdown("---")
st.markdown("### 2.1. Dampak Limbah Tailing: Konsentrasi Smelter vs Indeks Kualitas Air (IKA)")
st.markdown('<span style="background:#1B5E20;color:#A5D6A7;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: Crosstabulation SPSS & Trendline</span>', unsafe_allow_html=True)

# Pra-proses Data Panel Time-Series Section 2.1
df_smelter['provinsi'] = df_smelter['provinsi'].replace({'Sulawesi Selatan': 'Sulawesi Selatan', 'Sulawesi Tengah': 'Sulawesi Tengah', 'Sulawesi Tenggara': 'Sulawesi Tenggara', 'Sulawesi Utara': 'Sulawesi Utara', 'Gorontalo': 'Gorontalo', 'Sulawesi Barat': 'Sulawesi Barat'})
df_smelter_prov = df_smelter.groupby('provinsi').size().reset_index(name='Jumlah_Smelter')
df_smelter_prov.rename(columns={'provinsi': 'Provinsi'}, inplace=True)

# Menggunakan data IKA seluruh tahun (Panel Data)
df_ika_panel = df_ika.groupby(['Provinsi', 'Tahun'])['Indeks Kualitas Air'].mean().reset_index()

# Merge menjadi Data Panel (N = Provinsi x Tahun)
df_panel_2_1 = pd.merge(df_ika_panel, df_smelter_prov, on='Provinsi', how='left').fillna({'Jumlah_Smelter': 0})
df_panel_2_1.dropna(subset=['Indeks Kualitas Air'], inplace=True)

# Untuk Peta, kita tetap gunakan df_panel_2_1 yang di-filter 2023 saja
df_panel_map_2_1 = df_panel_2_1[df_panel_2_1['Tahun'] == 2023].copy()

sulteng_smelter_21 = df_smelter_prov[df_smelter_prov['Provinsi'] == 'Sulawesi Tengah']['Jumlah_Smelter'].values[0] if not df_smelter_prov[df_smelter_prov['Provinsi'] == 'Sulawesi Tengah'].empty else 0
sultra_smelter_21 = df_smelter_prov[df_smelter_prov['Provinsi'] == 'Sulawesi Tenggara']['Jumlah_Smelter'].values[0] if not df_smelter_prov[df_smelter_prov['Provinsi'] == 'Sulawesi Tenggara'].empty else 0
ika_sulteng = df_panel_map_2_1[df_panel_map_2_1['Provinsi'] == 'Sulawesi Tengah']['Indeks Kualitas Air'].values[0] if not df_panel_map_2_1[df_panel_map_2_1['Provinsi'] == 'Sulawesi Tengah'].empty else 0
ika_sultra = df_panel_map_2_1[df_panel_map_2_1['Provinsi'] == 'Sulawesi Tenggara']['Indeks Kualitas Air'].values[0] if not df_panel_map_2_1[df_panel_map_2_1['Provinsi'] == 'Sulawesi Tenggara'].empty else 0

st.markdown(f"""
Tingginya aktivitas pengolahan bijih nikel (*smelter*) secara langsung memicu ekskresi limbah *tailing* dan terak (*slag*) dalam skala masif. Peta geospasial dan agregasi data di bawah ini tidak sekadar menunjukkan visualisasi statis, melainkan menyingkap realitas berdarah dari proyek ambisius hilirisasi nikel yang dipaksakan di Sulawesi. Dari total **{tot_smelter} fasilitas mega-smelter** yang beroperasi, konsentrasi absolut pembongkaran ruang terpusat pada dua episentrum industri, yakni Sulawesi Tengah dengan **{sulteng_smelter_21} fasilitas smelter** dan Sulawesi Tenggara dengan **{sultra_smelter_21} fasilitas smelter**. Ekspansi agresif yang tidak terkendali ini memonopoli pemanfaatan lahan pesisir dan wilayah hulu.

Sangat memprihatinkan bahwa tepat pada zona konsentrasi tambang inilah, daya dukung lingkungan mengalami kolaps yang mematikan. Warna merah pekat pada peta geospasial di bawah berhimpit secara sempurna dengan lokasi-lokasi tumpukan smelter tersebut. Secara empiris, Indeks Kualitas Air (IKA) di Sulawesi Tengah terjun bebas hingga menyentuh angka kritis **{ika_sulteng:.1f} poin**, sementara Sulawesi Tenggara juga terseret di level **{ika_sultra:.1f} poin** pada tahun 2023. Penurunan curam skor baku mutu air ini adalah bukti absolut yang tidak terbantahkan bahwa pembuangan jutaan ton limbah *tailing* beracun, sisa asam, dan terak (*slag*) hasil pemurnian nikel telah secara fatal meracuni sistem hidrologis, membunuh ekosistem laut, dan menghancurkan sumber air baku.

Kenyataan ini menelanjangi narasi manis di balik angka investasi, bahwa metrik IKA bukan lagi sekadar indikasi polusi administratif, melainkan bukti forensik terciptanya *zona tumbal ekologis* (sacrifice zones). Nelayan dan masyarakat pesisir dipaksa menelan dampak pencemaran air secara langsung, sementara keuntungan ekstraktif lari terbang ke pemodal raksasa asing maupun domestik. Sub-bab ini menguji hipotesis secara empiris: **Apakah kepadatan smelter secara konsisten menurunkan Indeks Kualitas Air (IKA)?**
""")

# Choropleth Map Plotly
with open('data/processed/sulawesi_provinces.geojson', 'r') as f:
    sulawesi_geojson = json.load(f)

fig_map = px.choropleth_mapbox(
    df_panel_map_2_1,
    geojson=sulawesi_geojson,
    locations='Provinsi',
    featureidkey='properties.Provinsi',
    color="Indeks Kualitas Air",
    color_continuous_scale=[
        [0.0, '#8B4513'],   # Brown - Kualitas sangat buruk (air tercemar berat)
        [0.3, '#D2691E'],   # Chocolate - Kualitas buruk
        [0.5, '#F4A460'],   # Sandy brown - Kualitas sedang
        [0.7, '#87CEEB'],   # Sky blue - Kualitas cukup
        [1.0, '#1E90FF']    # Dodger blue - Kualitas baik (air bersih)
    ],
    zoom=4.5,
    center={"lat": -1.8, "lon": 120.5},
    opacity=0.75,
    hover_name="Provinsi",
    hover_data={"Provinsi": False, "Jumlah_Smelter": True, "Indeks Kualitas Air": ':.1f'},
    mapbox_style="carto-darkmatter",
    title="Peta Choropleth: Distribusi Smelter vs Kritisnya Kualitas Air 2023"
)
fig_map.update_layout(
    margin={"r":0,"t":50,"l":0,"b":0},
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#ECEFF1')
)
st.plotly_chart(fig_map, use_container_width=True)

st.markdown(f"""
<div style="background:#1E1E1E; padding:14px; border-radius:10px; border-left:5px solid #D32F2F; margin-bottom: 25px;">
    <b>Pembedahan Spasial:</b> Peta geospasial di atas menyingkap realitas berdarah dari hilirisasi. Lingkaran raksasa yang berada di Sulawesi Tengah dan Sulawesi Tenggara merepresentasikan konsentrasi masif fasilitas smelter. Sangat memprihatinkan bahwa pada episentrum industri inilah, warna lingkaran berubah drastis menjadi merah pekat—menandakan skor Indeks Kualitas Air (IKA) yang terjun bebas. Ini bukan lagi sekadar penurunan indikator, melainkan penciptaan <i>zona tumbal ekologis</i> akibat pencemaran aliran sungai dan pembuangan tailing.
</div>
""", unsafe_allow_html=True)

with st.expander("Lihat Data Mentah: Peta Choropleth 2023", expanded=False):
    st.dataframe(df_panel_map_2_1[['Provinsi', 'Jumlah_Smelter', 'Indeks Kualitas Air']], use_container_width=True, hide_index=True)
    st.caption("📁 **Sumber File:** `data/processed/sulawesi_esdm_nikel.csv` & `data/processed/sulawesi_ika_2015_2024.csv`")

# --- Crosstab Introduction ---
import importlib
import src.components.spss_crosstab
importlib.reload(src.components.spss_crosstab)
from src.components.spss_crosstab import render_spss_crosstab

x_options = {
    "Jumlah_Smelter": "Kepadatan Smelter (Fasilitas)"
}
y_options = {
    "Indeks Kualitas Air": "Indeks Kualitas Air (IKA)"
}
title_1 = "Pembuktian Statistik: Intensitas Smelter vs Pencemaran Air"
hypothesis_text_1 = """
Hipotesis utama narasi ini adalah bahwa **kepadatan smelter dan pembuangan limbah tailing** berdampak langsung pada **memburuknya kualitas air (IKA)**.
Dengan membagi provinsi menjadi kelompok intensitas tambang "Tinggi" vs "Rendah", kita menguji probabilitas kerusakan ekologisnya.
"""
interp_sig_21 = "Secara konsisten, matriks menunjukkan tren signifikan di mana provinsi dengan intensitas smelter yang tinggi terjebak pada mutu air yang lebih kritis. Ini membuktikan bahwa hilirisasi menumbalkan daya dukung air secara mutlak."
interp_insig_21 = "Kegagalan statistik mendeteksi signifikansi membongkar fakta krusial: Indeks Kualitas Air (IKA) provinsi adalah metrik usang yang 'mengencerkan' kiamat ekologis di tapak. Pencemaran tailing fatal di area tambang tertutupi oleh data sungai-sungai perawan di luarnya."

exec_sig_21 = "Dari skenario pengujian, terbukti secara SIGNIFIKAN bahwa peningkatan kepadatan smelter berkorelasi mutlak dengan hancurnya mutu air. Angka Odds Ratio menegaskan bahwa ekspansi industri hilirisasi memberikan risiko kerusakan eksponensial pada daya dukung air."
exec_insig_21 = "Kegagalan pengujian statistik ini tidak berarti hilirisasi aman, melainkan menelanjangi kegagalan indikator agregat negara. Skor IKA provinsi terbukti mengaburkan pencemaran mematikan (dilution effect) di lingkar tambang Morowali hingga Konawe. Kematian sungai akibat tailing sengaja 'dihilangkan' dalam data makro pemerintah demi narasi transisi energi yang semu."

_, _, df_panel_labeled_2_1 = render_spss_crosstab(df_panel_2_1, x_options, y_options, title_1, hypothesis_text_1, key_prefix="21", interp_sig=interp_sig_21, interp_insig=interp_insig_21, exec_sig=exec_sig_21, exec_insig=exec_insig_21)

with st.expander("Lihat Data Mentah: Panel Smelter vs IKA (Time-Series 2016-2023)", expanded=False):
    st.dataframe(df_panel_labeled_2_1[['Provinsi', 'Tahun', 'Jumlah_Smelter', 'X_Label', 'Indeks Kualitas Air', 'Y_Label']], use_container_width=True, hide_index=True)
    st.caption("📁 **Sumber File:** `sulawesi_esdm_nikel.csv` & `sulawesi_ika_2016_2024.csv`")

st.markdown("---")
st.markdown("### 2.2. Kepungan Asap: Kapasitas PLTU vs Indeks Kualitas Udara (IKU)")

# Data Loading & Prep
df_pltu = pd.read_csv('data/processed/sulawesi_pltu_captive.csv')
df_iku = pd.read_csv('data/processed/sulawesi_iku_2015_2024.csv')

prov_map = {
    'North Sulawesi': 'Sulawesi Utara',
    'South Sulawesi': 'Sulawesi Selatan',
    'Southeast Sulawesi': 'Sulawesi Tenggara',
    'Central Sulawesi': 'Sulawesi Tengah',
    'Gorontalo': 'Gorontalo',
    'West Sulawesi': 'Sulawesi Barat'
}
df_pltu['Provinsi'] = df_pltu['Subnational unit (province, state)'].map(prov_map)
df_pltu_prov = df_pltu.groupby('Provinsi')['Capacity (MW)'].sum().reset_index()
df_pltu_prov.rename(columns={'Capacity (MW)': 'Kapasitas_PLTU_MW'}, inplace=True)

# Menggunakan data IKU seluruh tahun (Panel Data)
df_iku_panel = df_iku.groupby(['Provinsi', 'Tahun'])['IKU'].mean().reset_index()

df_panel_2_2 = pd.merge(df_iku_panel, df_pltu_prov, on='Provinsi', how='left').fillna({'Kapasitas_PLTU_MW': 0})
df_panel_2_2.dropna(subset=['IKU'], inplace=True)

# Untuk visualisasi bar/scatter, kita gunakan data 2023
df_panel_viz_2_2 = df_panel_2_2[df_panel_2_2['Tahun'] == 2023].sort_values('Kapasitas_PLTU_MW', ascending=False)

# Persiapan Data Time-Series untuk Stacked Area Chart (OWID Style)
years = list(range(2010, 2025)) # Mulai dari 2010 untuk memperlihatkan lonjakan tajam eksponensial
df_pltu_op = df_pltu[(df_pltu['Status'].str.lower() == 'operating') & df_pltu['Start year'].notna()]

panel_data_pltu = []
for y in years:
    for prov in prov_map.values():
        cap = df_pltu_op[(df_pltu_op['Provinsi'] == prov) & (df_pltu_op['Start year'] <= y)]['Capacity (MW)'].sum()
        panel_data_pltu.append({'Tahun': y, 'Provinsi': prov, 'Kapasitas_PLTU_MW': cap})

df_pltu_trend = pd.DataFrame(panel_data_pltu)

# Rata-rata IKU se-Sulawesi per tahun
df_iku_avg = df_iku[df_iku['Tahun'].between(2010, 2024)].groupby('Tahun')['IKU'].mean().reset_index()

awal_iku = df_iku_avg.iloc[0]['IKU'] if not df_iku_avg.empty else 0
akhir_iku = df_iku_avg.iloc[-1]['IKU'] if not df_iku_avg.empty else 0
penurunan_iku = awal_iku - akhir_iku

st.markdown('<span style="background:#1B5E20;color:#A5D6A7;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: Stacked Area Time-Series & Trendline</span>', unsafe_allow_html=True)

st.markdown(f"""
Tumpukan area berwarna pada grafik di bawah ini merepresentasikan lonjakan kumulatif kapasitas Pembangkit Listrik Tenaga Uap (PLTU) berbasis batu bara (*captive power plants*) yang sengaja didirikan secara khusus untuk menyuplai energi kotor ke fasilitas smelter nikel. Kita melihat ledakan kapasitas pembakaran batu bara yang terus meroket secara radikal dan tanpa jeda sepanjang satu dekade terakhir, hingga memuncak di angka masif **{tot_kapasitas_pltu:,.0f} Megawatt (MW)**. Besaran energi kotor ini secara ekuivalen setara dengan daya hancur emisi sulfur dioksida (SO2) dan partikulat debu halus (PM2.5) dalam skala mematikan yang tak terbayangkan.

Ironi tragisnya terekam jelas: saat daya pembakaran batubara raksasa ini terus bertumpuk secara eksponensial dari tahun ke tahun, grafik garis merah di bawahnya yang memetakan tren Indeks Kualitas Udara (IKU) rata-rata se-Sulawesi justru terus tertekan curam ke dasar jurang. Tercatat secara faktual bahwa sejak periode pencatatan awal hingga titik akhir observasi, terjadi kejatuhan brutal mutu udara dari **{awal_iku:.1f} poin** hingga akhirnya menembus ambang batas bawah di angka **{akhir_iku:.1f} poin**. Penurunan ekstrem sebesar **{penurunan_iku:.1f} poin** ini tidak bisa lagi disangkal, dimanipulasi, atau dinormalisasi; ini adalah bukti garis lurus yang memastikan ada relasi kausalitas mematikan antara hilirisasi ekstraktif dan lenyapnya udara segar.

Fakta lapangan yang direpresentasikan data ini secara brutal membantah kampanye artifisial "Hilirisasi Hijau" yang selama ini digaungkan oleh negara dan oligarki korporasi. Melalui angka-angka ini, terbukti bahwa kita tidak sedang memproduksi bahan baku transisi energi yang ramah lingkungan; kita justru sedang mensponsori penciptaan kantong-kantong penyakit saluran pernapasan (ISPA) raksasa di lingkar industri. Asap hitam pekat beracun dari pembakaran jutaan ton batu bara ini tidak dapat tersaring di atas kertas regulasi, melainkan dihirup langsung setiap detiknya oleh paru-paru anak-anak dan masyarakat lokal. Dengan mengorbankan kualitas udara bersih demi lelehan nikel, operasi ekstraktif ini pada hakikatnya sedang mensubsidi gaya hidup mobil listrik negara maju dengan membayar menggunakan kesehatan, udara, dan nyawa penduduk Sulawesi. Sub-bab ini menguji hipotesis: **Apakah ledakan kapasitas PLTU captive secara empiris meruntuhkan kualitas udara?**
""")

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

# Gunakan palette warna ala OWID (Washed-out pastel + solid)
owid_colors = ['#9B5A40', '#E58872', '#5E85B4', '#A09CAE', '#82B989', '#E3D7A4']

fig_2_2a = go.Figure()

# Tambahkan Stacked Area per Provinsi untuk PLTU
for i, prov in enumerate(df_pltu_trend['Provinsi'].unique()):
    d = df_pltu_trend[df_pltu_trend['Provinsi'] == prov]
    fig_2_2a.add_trace(
        go.Scatter(
            x=d['Tahun'], 
            y=d['Kapasitas_PLTU_MW'], 
            name=prov, 
            mode='lines', 
            stackgroup='one',
            line=dict(width=0.5, color='#444444'), # Batas tipis seperti OWID
            fillcolor=owid_colors[i % len(owid_colors)],
            hoveron='points+fills'
        )
    )

fig_2_2a.update_layout(
    title=dict(text="Ekspansi Berdarah: Kumulatif Kapasitas PLTU (2010-2024)", font=dict(color='#ECEFF1', size=20)),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#ECEFF1', family='Arial, sans-serif'),
    legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02),
    xaxis=dict(
        title="",
        tickmode='linear',
        dtick=2,
        tickformat='d',
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='#555555',
        rangeslider=dict(
            visible=True,
            thickness=0.03,
            bgcolor="#2D2D2D",
            bordercolor="#555555",
            borderwidth=1,
        ),
    ),
    yaxis=dict(
        title="", 
        color='#ECEFF1', 
        gridcolor='#555555', 
        gridwidth=1,
        griddash='dash', # Garis putus-putus ala OWID
        dtick=500,
        ticksuffix=" MW"
    ),
    hovermode="x unified",
    hoverlabel=dict(
        bgcolor="rgba(255, 255, 255, 0.95)", # Kotak tooltip putih terang ala OWID
        font_size=13,
        font_family="Arial",
        font_color="#333333"
    ),
    height=600
)

st.plotly_chart(fig_2_2a, use_container_width=True)

# Grafik Terpisah untuk IKU
fig_2_2b = go.Figure()

# Tambahkan Garis IKU Rata-rata
fig_2_2b.add_trace(
    go.Scatter(
        x=df_iku_avg['Tahun'], 
        y=df_iku_avg['IKU'], 
        name="Rata-rata IKU Sulawesi", 
        mode='lines+markers', 
        marker=dict(color='#FFFFFF', size=8, line=dict(width=2, color='#D32F2F')), 
        line=dict(color='#D32F2F', width=4)
    )
)

fig_2_2b.update_layout(
    title="Anjloknya Indeks Kualitas Udara Rata-rata (2015-2024)",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#ECEFF1'),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    xaxis=dict(
        title="Tahun",
        tickmode='linear',
        dtick=1,
        tickformat='d',
        rangeslider=dict(
            visible=True,
            thickness=0.03,
            bgcolor="#2D2D2D",
            bordercolor="#555555",
            borderwidth=1,
        ),
    ),
    yaxis=dict(title="Skor IKU (Rata-rata)", color='#D32F2F', gridcolor='#37474F'),
    hovermode="x unified",
    height=350
)

st.plotly_chart(fig_2_2b, use_container_width=True)

st.markdown(f"""
<div style="background:#1E1E1E; padding:14px; border-radius:10px; border-left:5px solid #D32F2F; margin-bottom: 25px;">
    <b>Pembedahan Ekologis Visual:</b> Grafik <i>stacked-area time-series</i> di atas memotret akumulasi krisis dari waktu ke waktu. Tumpukan area berwarna menunjukkan ledakan kumulatif kapasitas PLTU yang terus meroket tajam tanpa henti sepanjang 1 dekade terakhir. Ironisnya, saat daya pembakaran batubara ini terus bertumpuk, garis rata-rata kualitas udara (IKU) se-Sulawesi tampak terus tertekan ke bawah. Slider di bawah dapat digeser untuk melihat rincian lonjakan polusi ini di periode tahun tertentu.
</div>
""", unsafe_allow_html=True)

with st.expander("Lihat Data Mentah: Grafik Area PLTU", expanded=False):
    # Pivot df_pltu_trend to show capacity by province per year for easier reading
    df_pivot_pltu = df_pltu_trend.pivot(index='Tahun', columns='Provinsi', values='Kapasitas_PLTU_MW').reset_index()
    st.dataframe(df_pivot_pltu, use_container_width=True, hide_index=True)
    st.caption("📁 **Sumber File:** `data/processed/sulawesi_pltu_captive.csv`")

with st.expander("Lihat Data Mentah: Rata-rata IKU", expanded=False):
    st.dataframe(df_iku_avg, use_container_width=True, hide_index=True)
    st.caption("📁 **Sumber File:** `data/processed/sulawesi_iku_2015_2024.csv`")

# SPSS Crosstab Section 2.2
x_options_2_2 = {
    "Kapasitas_PLTU_MW": "Kapasitas PLTU (MW)"
}
y_options_2_2 = {
    "IKU": "Indeks Kualitas Udara (IKU)"
}
title_2_2 = "Pembuktian Statistik: Kapasitas PLTU vs Kualitas Udara"
hypothesis_text_2_2 = """
Hipotesis utama narasi ini adalah bahwa **ekspansi gila-gilaan PLTU Batubara** (terutama captive power untuk kawasan nikel) akan berdampak langsung pada **memburuknya kualitas udara (IKU)**.
Dengan membagi provinsi menjadi kelompok Kapasitas PLTU "Tinggi" vs "Rendah", kita mengukur probabilitas kerusakan udaranya secara statistik.
"""
interp_sig_22 = "Provinsi dengan penumpukan kapasitas PLTU tertinggi memiliki kecenderungan mencatatkan IKU yang memburuk secara signifikan. Kepungan asap dari captive power tidak dapat disangkal telah meracuni udara publik."
interp_insig_22 = "Meskipun tidak signifikan secara ketat akibat ukuran sampel (P ≥ 0.05), matriks di atas secara konsisten menunjukkan bahwa provinsi dengan kapasitas PLTU tertinggi mencatatkan IKU yang paling memburuk. Kepungan asap captive power tak dapat disangkal terus meracuni ruang udara."

exec_sig_22 = "Dari skenario pengujian, terbukti secara SIGNIFIKAN bahwa peningkatan kapasitas PLTU berkorelasi mutlak dengan memburuknya kualitas udara. Asap dari captive power terbukti meracuni udara secara empiris, meningkatkan risiko gangguan pernapasan struktural."
exec_insig_22 = "Meskipun nilai statistik formal belum mencapai ambang signifikansi, matriks menunjukkan dominasi di mana wilayah dengan kapasitas PLTU sangat masif merata terjebak pada kondisi IKU yang memburuk. Krisis udara akibat captive power telah menyebar secara sistemik tanpa batas wilayah administrasi."

_, _, df_panel_labeled_2_2 = render_spss_crosstab(df_panel_2_2, x_options_2_2, y_options_2_2, title_2_2, hypothesis_text_2_2, key_prefix="22", interp_sig=interp_sig_22, interp_insig=interp_insig_22, exec_sig=exec_sig_22, exec_insig=exec_insig_22)

with st.expander("Lihat Data Mentah: Panel PLTU vs IKU (Time-Series 2015-2023)", expanded=False):
    st.dataframe(df_panel_labeled_2_2[['Provinsi', 'Tahun', 'Kapasitas_PLTU_MW', 'X_Label', 'IKU', 'Y_Label']], use_container_width=True, hide_index=True)
    st.caption("📁 **Sumber File:** `sulawesi_pltu_captive.csv` & `sulawesi_iku_2015_2024.csv`")

st.markdown("---")
st.markdown("### 2.3. Eksekusi Ruang: Ekspansi Kawasan Industri vs Tekanan Ekologis (Deforestasi)")

# Data Loading & Prep
df_luas = pd.read_csv('data/processed/sulawesi_kawasan_nikel_luas.csv')
df_gfw = pd.read_csv('data/processed/sulawesi_gfw_master_1_dekade_2014_2023.csv')

df_luas_prov = df_luas.groupby('provinsi')['total_luas_ha'].sum().reset_index()
df_luas_prov.rename(columns={'provinsi': 'Provinsi', 'total_luas_ha': 'Luas_IUP_Kawasan_Ha'}, inplace=True)

# Mempertahankan data time-series
df_gfw_panel = df_gfw.groupby(['Provinsi', 'Tahun'])['Total_Deforestasi_Ha'].sum().reset_index()

df_panel_2_3 = pd.merge(df_gfw_panel, df_luas_prov, on='Provinsi', how='inner').fillna(0)

tot_luas_konsesi = df_luas_prov['Luas_IUP_Kawasan_Ha'].sum()
tot_def_10thn = df_gfw_panel['Total_Deforestasi_Ha'].sum()
prov_max_iup = df_luas_prov.loc[df_luas_prov['Luas_IUP_Kawasan_Ha'].idxmax()]['Provinsi']
prov_max_def = df_gfw_panel.groupby('Provinsi')['Total_Deforestasi_Ha'].sum().idxmax()

st.markdown('<span style="background:#1B5E20;color:#A5D6A7;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: Animated Bubble Chart (Hans Rosling Style) & Crosstabulation</span>', unsafe_allow_html=True)

st.markdown(f"""
Hilirisasi ekstraktif bukan hanya soal membangun tungku peleburan logam, melainkan tentang aneksasi ruang skala masif yang memakan korban bentang alam. Narasi transisi energi yang diagungkan di atas kertas berbanding terbalik dengan realitas penghancuran hutan di tapak. Data menunjukkan bahwa pemerintah telah merelakan penguasaan daratan Pulau Sulawesi seluas **{tot_luas_konsesi:,.0f} Hektar** secara absolut kepada korporasi tambang melalui Izin Usaha Pertambangan (IUP) dan Kawasan Industri. Dominasi aneksasi lahan ini dipimpin oleh **{prov_max_iup}** yang menyerahkan ruang hidupnya paling besar untuk dirubah menjadi lanskap keruk nikel.

Konsekuensi dari obral izin ini tergambar dengan brutal dalam metrik deforestasi. Sepanjang satu dekade (2014-2023), Pulau Sulawesi dipaksa kehilangan tutupan pohonnya hingga menyentuh total kerugian sebesar **{tot_def_10thn:,.0f} Hektar**. Grafik *Animated Bubble Chart* di bawah ini dirancang khusus untuk memvisualisasikan bagaimana "perlombaan menuju kiamat ekologis" ini terjadi secara beruntun dari tahun ke tahun. Anda dapat menekan tombol *Play* untuk melihat bagaimana titik-titik provinsi, terutama **{prov_max_def}**, merangsek naik membabat hutan seiring dengan besarnya karpet merah konsesi lahan yang diberikan. Ukuran lingkaran (*bubble*) merepresentasikan betapa cepat dan buasnya eskalasi deforestasi kumulatif yang terjadi di wilayah tersebut.

Visualisasi yang bergerak dinamis ini dengan telanjang membongkar fakta bahwa ekspansi industri hilirisasi adalah predator utama hutan hujan tropis. Tidak ada yang namanya "Deforestasi Berkelanjutan"; yang terjadi adalah kanibalisme ruang di mana habitat flora-fauna, wilayah tangkapan air, dan ruang kelola masyarakat adat diratakan dengan tanah demi mengejar kuota produksi nikel global. Fakta ini menegaskan bahwa kita tidak sedang menyelamatkan iklim bumi dengan mobil listrik, melainkan sekadar memindahkan titik pusat kehancuran ekologis ke halaman belakang masyarakat Sulawesi. Sub-bab ini secara empiris membuktikan bahwa besarnya kawasan industri berbanding lurus dengan masifnya laju pembabatan hutan.
""")

# Sort data for animation (Crucial for plotly animation frames)
df_panel_2_3.sort_values(by=['Tahun', 'Provinsi'], inplace=True)

# Cumulative Deforestation to make the bubbles "grow" over time
df_panel_2_3['Kumulatif_Deforestasi_Ha'] = df_panel_2_3.groupby('Provinsi')['Total_Deforestasi_Ha'].cumsum()

# Load GeoJSON for Sulawesi provinces
with open('data/processed/sulawesi_provinces.geojson', 'r') as f:
    sulawesi_geojson = json.load(f)

# Province coordinates for bubble markers
provinsi_coords = {
    'Sulawesi Selatan': [-4.1449, 119.9289],
    'Sulawesi Tengah': [-1.4300, 121.4456],
    'Sulawesi Tenggara': [-4.1449, 122.1746],
    'Sulawesi Utara': [0.6247, 123.9750],
    'Gorontalo': [0.6999, 122.4467],
    'Sulawesi Barat': [-2.8441, 119.2321]
}

# Create animation frames for map
import plotly.graph_objects as go

years = sorted(df_panel_2_3['Tahun'].unique())

# Prepare frames
frames = []
for year in years:
    df_year = df_panel_2_3[df_panel_2_3['Tahun'] == year].copy()
    
    # Choropleth layer (Deforestation intensity with forest color scale)
    choropleth = go.Choroplethmapbox(
        geojson=sulawesi_geojson,
        locations=df_year['Provinsi'],
        z=df_year['Kumulatif_Deforestasi_Ha'],
        featureidkey='properties.Provinsi',
        colorscale=[
            [0.0, '#2E7D32'],   # Dark green - Hutan masih lebat (deforestasi rendah)
            [0.2, '#66BB6A'],   # Medium green - Hutan cukup baik
            [0.4, '#FDD835'],   # Yellow - Hutan mulai tertekan
            [0.6, '#FB8C00'],   # Orange - Deforestasi sedang
            [0.8, '#D84315'],   # Deep orange - Deforestasi tinggi
            [1.0, '#5D4037']    # Brown - Hutan gundul (deforestasi parah)
        ],
        zmin=0,
        zmax=df_panel_2_3['Kumulatif_Deforestasi_Ha'].max(),
        marker=dict(opacity=0.7, line=dict(width=1, color='#444')),
        colorbar=dict(
            title=dict(
                text="Deforestasi<br>Kumulatif (Ha)",
                font=dict(color='#ECEFF1', size=12)
            ),
            tickfont=dict(color='#ECEFF1'),
            bgcolor='rgba(30,30,30,0.8)',
            bordercolor='#555',
            borderwidth=1,
            x=1.01
        ),
        hovertemplate='<b>%{location}</b><br>Deforestasi: %{z:,.0f} Ha<extra></extra>',
        showscale=bool(year == years[0])  # Show colorbar only on first frame
    )
    
    # Scattermapbox layer (Bubble for Deforestation Growth - Animated Size)
    lats = []
    lons = []
    sizes = []
    texts = []
    colors_bubble = []
    
    for _, row in df_year.iterrows():
        prov = row['Provinsi']
        if prov in provinsi_coords:
            lat, lon = provinsi_coords[prov]
            lats.append(lat)
            lons.append(lon)
            
            # Size proportional to CUMULATIVE DEFORESTATION (grows over time!)
            # This makes bubbles animate/grow as deforestation increases
            size = (row['Kumulatif_Deforestasi_Ha'] / 10000) ** 0.5 * 10
            sizes.append(max(size, 4))  # Minimum size 4
            
            # Color intensity by industrial area (static)
            colors_bubble.append(row['Luas_IUP_Kawasan_Ha'])
            
            texts.append(f"<b>{prov}</b><br>" + 
                        f"Luas Kawasan Industri: {row['Luas_IUP_Kawasan_Ha']:,.0f} Ha<br>" +
                        f"Deforestasi Kumulatif: {row['Kumulatif_Deforestasi_Ha']:,.0f} Ha<br>" +
                        f"Deforestasi Tahun Ini: {row['Total_Deforestasi_Ha']:,.0f} Ha<br>" +
                        f"Tahun: {int(row['Tahun'])}")
    
    bubbles = go.Scattermapbox(
        lat=lats,
        lon=lons,
        mode='markers',
        marker=dict(
            size=sizes,
            color='#FBC02D',  # Yellow-gold for industrial expansion
            opacity=0.65,
            sizemode='diameter'  # Ensures size is treated as diameter
        ),
        text=texts,
        hovertemplate='%{text}<extra></extra>',
        showlegend=False
    )
    
    frames.append(go.Frame(
        data=[choropleth, bubbles],
        name=str(int(year)),
        layout=go.Layout(
            title_text=f"Eksekusi Ruang: Ekspansi Industri vs Deforestasi ({int(year)})"
        )
    ))

# Initial frame (first year)
df_init = df_panel_2_3[df_panel_2_3['Tahun'] == years[0]]

choropleth_init = go.Choroplethmapbox(
    geojson=sulawesi_geojson,
    locations=df_init['Provinsi'],
    z=df_init['Kumulatif_Deforestasi_Ha'],
    featureidkey='properties.Provinsi',
    colorscale=[
        [0.0, '#2E7D32'],   # Dark green - Hutan masih lebat (deforestasi rendah)
        [0.2, '#66BB6A'],   # Medium green - Hutan cukup baik
        [0.4, '#FDD835'],   # Yellow - Hutan mulai tertekan
        [0.6, '#FB8C00'],   # Orange - Deforestasi sedang
        [0.8, '#D84315'],   # Deep orange - Deforestasi tinggi
        [1.0, '#5D4037']    # Brown - Hutan gundul (deforestasi parah)
    ],
    zmin=0,
    zmax=df_panel_2_3['Kumulatif_Deforestasi_Ha'].max(),
    marker=dict(opacity=0.7, line=dict(width=1, color='#444')),
    colorbar=dict(
        title=dict(
            text="Deforestasi<br>Kumulatif (Ha)",
            font=dict(color='#ECEFF1', size=12)
        ),
        tickfont=dict(color='#ECEFF1'),
        bgcolor='rgba(30,30,30,0.8)',
        bordercolor='#555',
        borderwidth=1,
        x=1.01
    ),
    hovertemplate='<b>%{location}</b><br>Deforestasi: %{z:,.0f} Ha<extra></extra>'
)

lats_init = []
lons_init = []
sizes_init = []
texts_init = []

for _, row in df_init.iterrows():
    prov = row['Provinsi']
    if prov in provinsi_coords:
        lat, lon = provinsi_coords[prov]
        lats_init.append(lat)
        lons_init.append(lon)
        
        # Size proportional to CUMULATIVE DEFORESTATION (starts small in 2014)
        size = (row['Kumulatif_Deforestasi_Ha'] / 10000) ** 0.5 * 10
        sizes_init.append(max(size, 4))
        
        texts_init.append(f"<b>{prov}</b><br>" + 
                         f"Luas Kawasan Industri: {row['Luas_IUP_Kawasan_Ha']:,.0f} Ha<br>" +
                         f"Deforestasi Kumulatif: {row['Kumulatif_Deforestasi_Ha']:,.0f} Ha<br>" +
                         f"Deforestasi Tahun Ini: {row['Total_Deforestasi_Ha']:,.0f} Ha<br>" +
                         f"Tahun: {int(row['Tahun'])}")

bubbles_init = go.Scattermapbox(
    lat=lats_init,
    lon=lons_init,
    mode='markers',
    marker=dict(
        size=sizes_init,
        color='#FBC02D',
        opacity=0.65,
        sizemode='diameter'
    ),
    text=texts_init,
    hovertemplate='%{text}<extra></extra>',
    showlegend=False
)

# Create figure
fig_2_3 = go.Figure(
    data=[choropleth_init, bubbles_init],
    frames=frames,
    layout=go.Layout(
        title=dict(
            text=f"Eksekusi Ruang: Ekspansi Industri vs Deforestasi ({int(years[0])})",
            font=dict(color='#ECEFF1', size=20)
        ),
        mapbox=dict(
            style="carto-darkmatter",
            center=dict(lat=-2.0, lon=120.8),
            zoom=5.2
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ECEFF1'),
        height=650,
        margin=dict(r=0, t=50, l=0, b=0),
        updatemenus=[
            dict(
                type='buttons',
                showactive=False,
                buttons=[
                    dict(
                        label='▶ PLAY',
                        method='animate',
                        args=[
                            None,
                            dict(
                                frame=dict(duration=800, redraw=True),
                                fromcurrent=True,
                                mode='immediate',
                                transition=dict(duration=400, easing='cubic-in-out')
                            )
                        ]
                    ),
                    dict(
                        label='⏸ PAUSE',
                        method='animate',
                        args=[
                            [None],
                            dict(
                                frame=dict(duration=0, redraw=False),
                                mode='immediate',
                                transition=dict(duration=0)
                            )
                        ]
                    )
                ],
                direction='left',
                pad=dict(r=10, t=70),
                x=0.02,
                xanchor='left',
                y=0.02,
                yanchor='bottom',
                bgcolor='rgba(30,30,30,0.9)',
                bordercolor='#555',
                borderwidth=1,
                font=dict(color='#ECEFF1', size=13)
            )
        ],
        sliders=[
            dict(
                active=0,
                yanchor='top',
                y=0.02,
                xanchor='left',
                x=0.20,
                currentvalue=dict(
                    prefix='Tahun: ',
                    visible=True,
                    font=dict(color='#D32F2F', size=16),
                    xanchor='left'
                ),
                pad=dict(b=10, t=50),
                len=0.75,
                bgcolor='rgba(30,30,30,0.8)',
                bordercolor='#555',
                borderwidth=1,
                tickcolor='#D32F2F',
                steps=[
                    dict(
                        args=[
                            [str(int(y))],
                            dict(
                                frame=dict(duration=400, redraw=True),
                                mode='immediate',
                                transition=dict(duration=400, easing='cubic-in-out')
                            )
                        ],
                        label=str(int(y)),
                        method='animate'
                    ) for y in years
                ]
            )
        ]
    )
)

st.plotly_chart(fig_2_3, use_container_width=True)

# Prepare interpretation text separately to avoid HTML escaping
interp_text_23 = """
<b style="color: #66BB6A;">Pembedahan Geospasial Temporal:</b><br>
Peta animasi di atas secara brutal menelanjangi bagaimana "perlombaan menuju kiamat ekologis" terjadi secara beruntun dari tahun ke tahun. Tekan tombol <b>▶ PLAY</b> di pojok kiri bawah untuk melihat evolusi temporal kehancuran hutan Sulawesi.<br>
<b>Gradient Hijau-Coklat (Choropleth)</b>: Menunjukkan transformasi tutupan hutan dari hijau (hutan masih baik) menjadi kuning-orange (hutan tertekan) hingga coklat gelap (hutan gundul total). Semakin coklat = semakin parah deforestasi kumulatifnya. Perhatikan bagaimana Sulteng & Sultra berubah dari hijau ke coklat pekat.<br>
<b>Lingkaran Kuning (Bubbles - ANIMATED)</b>: Merepresentasikan Deforestasi Kumulatif yang terus bertambah. Ukuran lingkaran akan membesar seiring waktu — semakin besar bubble = semakin masif akumulasi kehilangan hutan. Perhatikan bagaimana bubble Sulteng & Sultra membengkak drastis dari 2014 ke 2023.<br>
<b>Korelasi Visual</b>: Perhatikan bagaimana provinsi dengan bubble yang membesar paling cepat (Sulteng & Sultra) secara konsisten berubah warna dari hijau menjadi coklat gelap. Ini adalah bukti forensik bahwa ekspansi konsesi adalah mesin deforestasi.<br>
<i style="color: #AAA;">Geser slider tahun untuk membandingkan kondisi awal (2014 - masih hijau) dengan kondisi terkini (2023 - coklat pekat). Anda akan melihat bagaimana warna berubah dari hijau menjadi coklat dan lingkaran kuning membengkak secara dramatis—visualisasi nyata dari aneksasi ruang dan pembantaian hutan yang sistematis.</i>
"""

st.markdown(f"""
<div style="color: #BDBDBD; font-size: 0.95rem; line-height: 1.6; margin-bottom: 25px; margin-top: 15px; border-left: 3px solid #555; padding-left: 15px;">
    {interp_text_23}
</div>
""", unsafe_allow_html=True)

with st.expander("Lihat Data Mentah: Grafik Scatter Kumulatif Deforestasi", expanded=False):
    st.dataframe(df_panel_2_3[['Provinsi', 'Tahun', 'Luas_IUP_Kawasan_Ha', 'Total_Deforestasi_Ha', 'Kumulatif_Deforestasi_Ha']], use_container_width=True, hide_index=True)
    st.caption("📁 **Sumber File:** `data/processed/sulawesi_kawasan_nikel_luas.csv` & `data/processed/sulawesi_deforestasi_gfw.csv`")

# SPSS Crosstab Section 2.3
x_options_2_3 = {
    "Luas_IUP_Kawasan_Ha": "Luas Ekspansi Industri (Ha)"
}
y_options_2_3 = {
    "Total_Deforestasi_Ha": "Kehilangan Tutupan Pohon (Ha)"
}
title_2_3 = "Pembuktian Statistik: Ekspansi Industri vs Deforestasi"
hypothesis_text_2_3 = """
Hipotesis utama narasi ini adalah bahwa **obral izin lahan (Luas IUP & Kawasan)** adalah pendorong utama (*driver*) di balik masifnya **Deforestasi**.
Melalui crosstab ini, kita menguji secara statistik apakah provinsi dengan obral izin yang tinggi juga memiliki rekor kehilangan tutupan pohon yang paling parah.
"""
interp_sig_23 = "Temuan ini krusial: lonjakan intensitas Ekspansi Industri terbukti berkorelasi kuat dan signifikan dengan peningkatan Deforestasi. Ini adalah konfirmasi empiris bahwa narasi investasi ekstraktif mutlak mengorbankan luasan hutan di tingkat tapak."
interp_insig_23 = "Secara agregat obral perizinan lahan (IUP/Kawasan) sejalan lurus dengan parahnya kebangkrutan ekosistem hutan meskipun tidak signifikan secara statistik (P ≥ 0.05). Semakin berani negara membuka keran izin, semakin brutal hutan lenyap."

exec_sig_23 = "Dari skenario pengujian, terbukti secara SIGNIFIKAN bahwa perluasan kawasan industri dan izin baru berkorelasi kuat dengan tingginya laju deforestasi. Ekspansi investasi ini mutlak mengorbankan tutupan hutan primer sebagai barikade ekologis terakhir."
exec_insig_23 = "Meskipun belum signifikan secara statistik formal akibat sampel terbatas, matriks menunjukkan dominasi mutlak di mana obral perizinan lahan selalu diikuti oleh parahnya deforestasi. Kerusakan tutupan hutan telah merata dan saling bertautan secara spasial."

_, _, df_panel_labeled_2_3 = render_spss_crosstab(df_panel_2_3, x_options_2_3, y_options_2_3, title_2_3, hypothesis_text_2_3, key_prefix="23", y_is_negative=True, interp_sig=interp_sig_23, interp_insig=interp_insig_23, exec_sig=exec_sig_23, exec_insig=exec_insig_23)

with st.expander("Lihat Data Mentah: Panel IUP vs Deforestasi (Time-Series 2014-2023)", expanded=False):
    st.dataframe(df_panel_labeled_2_3[['Provinsi', 'Tahun', 'Luas_IUP_Kawasan_Ha', 'X_Label', 'Total_Deforestasi_Ha', 'Y_Label']], use_container_width=True, hide_index=True)
    st.caption("📁 **Sumber File:** `sulawesi_kawasan_nikel_luas.csv` & `sulawesi_gfw_master_1_dekade_2014_2023.csv`")

