__file__ = r'C:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\pages\1_Ekspansi_Industri.py'
import streamlit as st
import pandas as pd
import scipy.stats as stats
import altair as alt
import plotly.express as px
import numpy as np
import pydeck as pdk
import os
import sys

# Konfigurasi path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


st.set_page_config(
    page_title="Ekspansi Industri - CELIOS ECC",
    page_icon="refrensi/Celios China-Indonesia Energy Transition.png",
    layout="wide"
)


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
    df_pdrb = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_pdrb_sektoral_2016_2024.csv"))
    df_pdrb_kab = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_pdrb_sektoral_kabupaten_2016_2024.csv"))
    return df_izin, df_smelter, df_pltu, df_gfw, df_inv, df_pdrb, df_pdrb_kab

try:
    df_izin, df_smelter, df_pltu, df_gfw, df_inv, df_pdrb, df_pdrb_kab = load_all_data_v2()
except Exception as e:
    st.error(f"Error loading data: {e}")
    pass

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
st.markdown('<div class="org-badge">CELIOS - Center of Economic and Law Studies</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">Ekspansi Industri Ekstraktif</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Analisis spasiotemporal pertumbuhan industri ekstraktif dan pengolahan nikel serta dampaknya terhadap daya dukung dan daya tampung lingkungan di Pulau Sulawesi.</div>', unsafe_allow_html=True)

# ── Dropdown Metodologi ──
with st.expander("🔍 Metodologi", expanded=False):
    st.markdown("""
    **Alur Kausalitas (Ekonomi Politik Ekologi):** `Kebijakan Hilirisasi` → `Ekskalasi Perizinan & Investasi` → `Konsentrasi Smelter & Pembangkit Captive` → `Tekanan Ekologis (Konversi Lahan)`
    
    Kebijakan hilirisasi mendorong akselerasi perizinan dan kucuran investasi yang terkonsentrasi pada industri pengolahan padat emisi, sehingga meningkatkan beban terhadap daya dukung dan daya tampung lingkungan secara signifikan.
    
    **Variabel Tekanan / Ekspansi (X):**
    *   **Izin Usaha Pertambangan Baru:** Total IUP yang diterbitkan dalam rentang 2014-2024 (Data Minerbaone Kementerian ESDM).
    *   **Pertumbuhan Fasilitas Smelter:** Kapasitas dan jumlah unit pengolahan terintegrasi (Database CGS & Kementerian ESDM).
    *   **Kapasitas PLTU Captive:** Beban energi batu bara *off-grid* untuk fasilitas smelter (Global Energy Monitor/GEM).
    *   **Investasi PMDN:** Aliran Penanaman Modal Dalam Negeri (Kementerian Investasi/BKPM).
    
    **Variabel Dampak Ekologis (Y):**
    *   **Deforestasi Komoditas:** Luas tutupan hutan yang dikonversi untuk operasi pertambangan dan perkebunan monokultur (Global Forest Watch/GFW).
    
    **Metode Pengolahan Data:**
    Pendekatan kuantitatif deskriptif menggunakan teknik **Crosstabulation (Tabulasi Silang)** dan **Trend Analysis (Analisis Tren Time-Series)**. Seluruh raw data diagregasi berdasarkan dimensi spasial (Provinsi) dan temporal (Tahun 2014-2024) untuk memetakan anomali, pola konsentrasi perizinan, serta laju eksploitasi ruang secara presisi.
    """)

tot_investasi_triliun = tot_investasi / 1_000

# ── Hero Statement (Narasi Kritis Utama) ──
st.markdown(f"""
<div style="background-color: transparent; padding: 10px 0px; margin-bottom: 25px;">
    <h2 style="color: #FFFFFF; font-size: 1.8rem; margin-bottom: 15px; font-weight: 700;">Ekspansi Industri Ekstraktif: {tot_smelter} Unit Smelter dan Ketergantungan Energi Fosil Off-Grid di Sulawesi</h2>
    <p style="color: #CCCCCC; font-size: 1.05rem; line-height: 1.7; margin-bottom: 15px;">
        Dinamika pembangunan di Pulau Sulawesi periode 2014–2024 ditandai oleh akselerasi industri berbasis komoditas alam. Kebijakan hilirisasi nikel mendorong penerbitan <b>{int(tot_izin):,} Izin Usaha Pertambangan (IUP) baru</b> dengan total luas konsesi mencapai <b>{int(tot_luas_izin):,} Hektar</b>. Pengoperasian <b>{tot_smelter} unit fasilitas pemurnian (smelter)</b> didukung oleh kapasitas <b>{int(tot_kapasitas_pltu):,} MW PLTU Captive</b> (pembangkit listrik batu bara <i>off-grid</i>), yang meningkatkan intensitas emisi karbon pada zona-zona industri pesisir.
    </p>
    <p style="color: #CCCCCC; font-size: 1.05rem; line-height: 1.7;">
        Secara bersamaan, kucuran realisasi Penanaman Modal Dalam Negeri (PMDN) yang mencapai <b>{int(tot_investasi_triliun):,} Triliun Rupiah</b> berbanding lurus dengan akumulasi konversi tutupan hutan sebesar <b>{int(tot_deforestasi):,} Hektar</b> untuk aktivitas pertambangan dan perkebunan. Data ini mengindikasikan bahwa pertumbuhan indikator makroekonomi berjalan seiring dengan peningkatan beban terhadap daya dukung dan daya tampung lingkungan hidup.
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
            <div class="metric-value" style="color: #B71C1C;">{int(tot_izin):,} <span style="font-size:1rem;">IUP</span></div>
            <div class="metric-desc">Penambahan jumlah Izin Usaha Pertambangan (IUP) di Pulau Sulawesi dalam rentang satu dekade terakhir.</div>
        </div>
        <div class="metric-source"><b>Sumber:</b> Kementerian ESDM (Minerbaone)<br/><i>File: sulawesi_izin_baru_per_tahun.csv</i></div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Total Luas Konsesi Baru</div>
            <div class="metric-value" style="color: #C62828;">{int(tot_luas_izin):,} <span style="font-size:1rem;">Ha</span></div>
            <div class="metric-desc">Akumulasi luas daratan dan perairan pesisir yang dialokasikan untuk konsesi pertambangan sejak 2014.</div>
        </div>
        <div class="metric-source"><b>Sumber:</b> Kementerian ESDM (Minerbaone)<br/><i>File: sulawesi_izin_baru_per_tahun.csv</i></div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Kapasitas PLTU Captive Aktif</div>
            <div class="metric-value" style="color: #D32F2F;">{int(tot_kapasitas_pltu):,} <span style="font-size:1rem;">MW</span></div>
            <div class="metric-desc">Kapasitas pembangkit listrik batu bara <i>off-grid</i> yang beroperasi khusus menyokong fasilitas pemurnian nikel.</div>
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
            <div class="metric-desc">Total fasilitas pengolahan & pemurnian nikel yang terkonsentrasi di kawasan industri pesisir seperti Morowali dan Konawe.</div>
        </div>
        <div class="metric-source"><b>Sumber:</b> Database Smelter ESDM & CGS<br/><i>File: sulawesi_esdm_nikel.csv</i></div>
    </div>
    """, unsafe_allow_html=True)
with col5:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Luas Deforestasi Komoditas</div>
            <div class="metric-value" style="color: #B71C1C;">{int(tot_deforestasi):,} <span style="font-size:1rem;">Ha</span></div>
            <div class="metric-desc">Luas tutupan hutan alam yang dikonversi akibat aktivitas industri pertambangan dan perkebunan monokultur.</div>
        </div>
        <div class="metric-source"><b>Sumber:</b> Global Forest Watch (GFW)<br/><i>File: sulawesi_gfw_master_1_dekade_2014_2023.csv</i></div>
    </div>
    """, unsafe_allow_html=True)
with col6:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Investasi PMDN (2016-2024)</div>
            <div class="metric-value" style="color: #D32F2F;">{int(tot_investasi_triliun):,} <span style="font-size:1rem;">Triliun Rp</span></div>
            <div class="metric-desc">Realisasi investasi modal dalam negeri yang mengindikasikan tingginya intensitas kapital pada sektor industri ekstraktif.</div>
        </div>
        <div class="metric-source"><b>Sumber:</b> Kementerian Investasi / BKPM<br/><i>File: sulawesi_investasi_pmdn_2016_2024.csv</i></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# SUB-BAB 1.0: KONTEKS MAKRO EKONOMI (BREAKDOWN PDRB)
# ══════════════════════════════════════════════════════════
st.markdown("---")
st.subheader("1.1 Konteks Makro: Breakdown PDRB per Komoditas")

st.markdown("""
Sebelum membahas ledakan izin dan investasi ekstraktif secara spesifik, kita perlu membedah anatomi ekonomi makro Sulawesi. 
Apakah klaim "pertumbuhan ekonomi" benar-benar dinikmati oleh masyarakat luas, atau hanya dinikmati oleh segelintir sektor padat modal?
""")

st.markdown("#### 1.1.1 Dominasi Ekstraktif vs Ekonomi Akar Rumput (2016-2024)")
st.markdown("""Grafik di bawah ini menyederhanakan 17 sektor PDRB menjadi **3 klasifikasi makro advokatif** berdasarkan *Legal Supply-Chain Approach* (Metodologi CELIOS/ECC).

- 🔴 **Ekstraktif** = Kat. B (Pertambangan) + Kat. C (Industri Pengolahan/Smelter) + Kat. D (Listrik/PLTU Captive) — digabung berdasarkan mandat wajib UU Minerba Ps. 102–103 & Perpres 112/2022.
- 🟢 **Ekonomi Akar Rumput** = Kat. A (Pertanian, Kehutanan & Perikanan) — sektor terbarukan penyerap tenaga kerja lokal terbesar.
- ⚪ **Sektor Jasa & Lainnya** = 13 sektor E–U sisanya.
""")

# ── Klasifikasi Advokatif berdasarkan Metodologi CELIOS/ECC ──────────────────
# Sumber: docs/metodologi_klasifikasi_ekstraktif.md
# Kat B+C+D = Ekstraktif (Legal Supply-Chain: UU Minerba Ps.1,102-103; Perpres 112/2022 Ps.3 Ay.4)
# Kat A     = Ekonomi Akar Rumput (BPS KBLI 2020 Buku 1 Hal.21)
# E–U       = Sektor Jasa & Lainnya
EKSTRAKTIF_KODE = ['B', 'C', 'D']
EKSTRAKTIF_NAMA = [
    'Pertambangan dan Penggalian',          # Kat B — definisi langsung (Perpres 26/2010 Ps.1 Ay.2)
    'Industri Pengolahan',                   # Kat C — smelter WAJIB hukum (UU 3/2020 Ps.102-103)
    'Pengadaan Listrik dan Gas',             # Kat D — PLTU captive terintegrasi (Perpres 112/2022 Ps.3 Ay.4)
]
AKAR_RUMPUT_NAMA = ['Pertanian, Kehutanan, dan Perikanan']  # Kat A

LABEL_EKSTRAKTIF   = 'Ekstraktif'
LABEL_AKAR_RUMPUT  = 'Ekonomi Akar Rumput (Pertanian & Perikanan)'
LABEL_JASA         = 'Sektor Jasa & Lainnya'

def klasifikasi_kritis(sektor):
    """Klasifikasikan sektor PDRB ke 3 kelompok advokatif.
    Metodologi: Legal Supply-Chain Approach (docs/metodologi_klasifikasi_ekstraktif.md)
    """
    if sektor in EKSTRAKTIF_NAMA:
        return LABEL_EKSTRAKTIF
    elif sektor in AKAR_RUMPUT_NAMA:
        return LABEL_AKAR_RUMPUT
    else:
        return LABEL_JASA

df_hist_group = df_pdrb.copy()
df_hist_group['Klasifikasi'] = df_hist_group['sektor_nama'].apply(klasifikasi_kritis)
df_hist_agg = df_hist_group.groupby(['provinsi', 'tahun', 'Klasifikasi'])['nilai_miliar_rp'].sum().reset_index()
# Konversi ke Triliun Rupiah agar angka di sumbu Y lebih bersih (tidak ada 'k')
df_hist_agg['nilai_triliun_rp'] = df_hist_agg['nilai_miliar_rp'] / 1000

# Tambahkan penanda khusus untuk Sulawesi Tengah di nama provinsi agar ter-highlight
# Tambahkan penanda khusus untuk Sulawesi Tengah di nama provinsi agar ter-highlight
df_hist_agg['provinsi_label'] = df_hist_agg['provinsi'].apply(
    lambda x: f"{x.upper()} (PUSAT KONSENTRASI)" if x == "Sulawesi Tengah" else x
)

# Hitung ulang persentase berdasarkan total keseluruhan PDRB
df_total_agg = df_hist_agg.groupby(['provinsi', 'tahun'])['nilai_miliar_rp'].sum().reset_index(name='total_pdrb')
df_hist_agg = df_hist_agg.merge(df_total_agg, on=['provinsi', 'tahun'])
df_hist_agg['pct_dari_total'] = (df_hist_agg['nilai_miliar_rp'] / df_hist_agg['total_pdrb']) * 100

# Urutan kategori: Akar Rumput di bawah, Jasa di tengah, Ekstraktif di atas (stacked)
cat_order = [LABEL_EKSTRAKTIF, LABEL_JASA, LABEL_AKAR_RUMPUT]
df_hist_agg['Klasifikasi'] = pd.Categorical(df_hist_agg['Klasifikasi'], categories=cat_order, ordered=True)
df_hist_agg = df_hist_agg.sort_values(by=['provinsi', 'tahun', 'Klasifikasi'])

# VISUALISASI 1: Altair Stacked Area Chart (Historical Tren 2016-2024, Absolute Value)
color_map = {
    LABEL_EKSTRAKTIF:  '#E74C3C',  # Flat red (Alizarin)
    LABEL_JASA:        '#7F8C8D',  # Flat grey (Asbestos)
    LABEL_AKAR_RUMPUT: '#2ECC71',  # Flat green (Emerald)
}

cat_order_area = [LABEL_AKAR_RUMPUT, LABEL_JASA, LABEL_EKSTRAKTIF]

# Custom Legend HTML (Rata Kanan-Kiri & Responsif)
st.markdown(f"""
<div style="display: flex; gap: 20px; justify-content: center; margin-bottom: 25px; flex-wrap: wrap;">
    <div style="font-size: 13px;"><span style="color: {color_map[LABEL_AKAR_RUMPUT]}; font-size: 16px;">&bull;</span> {LABEL_AKAR_RUMPUT}</div>
    <div style="font-size: 13px;"><span style="color: {color_map[LABEL_JASA]}; font-size: 16px;">&bull;</span> {LABEL_JASA}</div>
    <div style="font-size: 13px;"><span style="color: {color_map[LABEL_EKSTRAKTIF]}; font-size: 16px;">&bull;</span> {LABEL_EKSTRAKTIF}</div>
</div>
""", unsafe_allow_html=True)

# Grid Layout: 3 Columns
provinces = df_hist_agg['provinsi_label'].unique()
cols = st.columns(3)

for i, prov in enumerate(provinces):
    df_prov = df_hist_agg[df_hist_agg['provinsi_label'] == prov]
    
    chart = alt.Chart(df_prov).mark_area(opacity=0.9).encode(
        x=alt.X('tahun:O', title='Tahun', axis=alt.Axis(labelAngle=0, values=[2016, 2018, 2020, 2022, 2024])),
        y=alt.Y('nilai_triliun_rp:Q', title='Nilai PDRB (Triliun Rp)', stack=True),
        color=alt.Color('Klasifikasi:N', 
                        sort=cat_order_area,
                        scale=alt.Scale(domain=cat_order_area, 
                                        range=[color_map[LABEL_AKAR_RUMPUT], color_map[LABEL_JASA], color_map[LABEL_EKSTRAKTIF]]),
                        legend=None), # Legend dinonaktifkan karena pakai HTML
        tooltip=[
            alt.Tooltip('provinsi:N', title='Provinsi'),
            alt.Tooltip('tahun:O', title='Tahun'),
            alt.Tooltip('Klasifikasi:N', title='Sektor'),
            alt.Tooltip('nilai_triliun_rp:Q', title='PDRB (Triliun Rp)', format=',.1f'),
            alt.Tooltip('pct_dari_total:Q', title='Porsi (%)', format=',.1f')
        ]
    ).properties(
        title=alt.TitleParams(text=prov, anchor='middle', fontSize=13, color='black'),
        height=220
    ).configure_view(
        stroke=None
    ).configure_axis(
        grid=True, gridColor='#333333'
    )
    
    cols[i % 3].altair_chart(chart, use_container_width=True)

st.caption("Metodologi: Legal Supply-Chain Approach — Kat B+C+D = Ekstraktif (UU Minerba Ps.102-103; Perpres 112/2022 Ps.3 Ay.4)")

st.markdown("#### 1.1.2 Pemusatan Sektor Ekstraktif di Kabupaten se-Sulawesi Tengah")
st.markdown("""
Jika dianalisis secara spasial pada tingkat kabupaten di Sulawesi Tengah, terlihat konsentrasi kegiatan industri ekstraktif. Kabupaten **Morowali** dan **Morowali Utara** mendominasi struktur PDRB provinsi melalui pengembangan kawasan industri hilirisasi dan PLTU Captive. 
Visualisasi di bawah membandingkan komposisi ketiga sektor advokatif di seluruh 13 kabupaten/kota se-Sulawesi Tengah pada tahun terbaru.
""")

df_kab_hist = df_pdrb_kab.copy()
df_kab_hist['Klasifikasi'] = df_kab_hist['sektor_nama'].apply(klasifikasi_kritis)

# Filter HANYA Sulawesi Tengah dan HANYA Tahun Terbaru
df_kab_sulteng = df_kab_hist[df_kab_hist['provinsi'] == 'Sulawesi Tengah'].copy()
latest_year_kab = df_kab_sulteng['tahun'].max()
df_kab_latest = df_kab_sulteng[df_kab_sulteng['tahun'] == latest_year_kab].copy()

df_kab_agg = df_kab_latest.groupby(['kabupaten', 'Klasifikasi'])['nilai_miliar_rp'].sum().reset_index()
df_kab_agg['nilai_triliun_rp'] = df_kab_agg['nilai_miliar_rp'] / 1000

df_kab_tot = df_kab_agg.groupby('kabupaten')['nilai_triliun_rp'].sum().reset_index(name='total')
df_kab_agg = df_kab_agg.merge(df_kab_tot, on='kabupaten')
df_kab_agg['pct'] = (df_kab_agg['nilai_triliun_rp'] / df_kab_agg['total']) * 100

# Urutkan berdasarkan total terbesar
df_kab_agg = df_kab_agg.sort_values(by=['total', 'Klasifikasi'], ascending=[True, True])

# Bikin Horizontal Stacked Bar Chart
df_kab_agg['Klasifikasi'] = pd.Categorical(df_kab_agg['Klasifikasi'], categories=cat_order_area, ordered=True)

# Tambahkan label (tanpa emoji, uppercase untuk Morowali)
df_kab_agg['kabupaten_label'] = df_kab_agg['kabupaten'].apply(
    lambda x: f"{x.upper()}" if 'Morowali' in x else x
)

# Urutkan berdasarkan total terbesar untuk urutan Y-axis Altair
sort_order = df_kab_agg.groupby('kabupaten_label')['total'].first().sort_values(ascending=False).index.tolist()

bar_kab = alt.Chart(df_kab_agg).mark_bar().encode(
    y=alt.Y('kabupaten_label:N', title=None, sort=sort_order, axis=alt.Axis(labelLimit=500, labelFontSize=11)),
    x=alt.X('nilai_triliun_rp:Q', title=f"Nilai PDRB ({latest_year_kab}) - Triliun Rp"),
    color=alt.Color('Klasifikasi:N', 
                    scale=alt.Scale(domain=cat_order_area, 
                                    range=[color_map[LABEL_AKAR_RUMPUT], color_map[LABEL_JASA], color_map[LABEL_EKSTRAKTIF]]),
                    legend=alt.Legend(title=None, orient="bottom", direction="vertical", labelLimit=1000)),
    tooltip=[
        alt.Tooltip('kabupaten:N', title='Kabupaten'),
        alt.Tooltip('Klasifikasi:N', title='Sektor'),
        alt.Tooltip('nilai_triliun_rp:Q', title='Nilai (Triliun Rp)', format=',.1f'),
        alt.Tooltip('pct:Q', title='Porsi (%)', format=',.1f')
    ]
).properties(
    height=500
).configure_view(
    stroke=None
).configure_axis(
    grid=True, gridColor='#333333'
)

st.altair_chart(bar_kab, use_container_width=True)

with st.expander("Lihat Data Mentah: Agregasi 3 Sektor Advokatif (Provinsi & Kabupaten)", expanded=False):
    col_prov, col_kab = st.columns(2)
    with col_prov:
        st.write("**Data Provinsi**")
        st.dataframe(df_hist_agg[['provinsi', 'tahun', 'Klasifikasi', 'nilai_miliar_rp', 'nilai_triliun_rp', 'pct_dari_total']], use_container_width=True, hide_index=True)
    with col_kab:
        st.write("**Data Kabupaten (Sulawesi Tengah)**")
        st.dataframe(df_kab_agg[['kabupaten', 'Klasifikasi', 'nilai_triliun_rp', 'pct']], use_container_width=True, hide_index=True)
    st.caption("📁 **Sumber File:** Data SIMDASI BPS yang diagregasi menjadi 3 Klasifikasi Utama.")


st.markdown("#### 1.1.3 Perbandingan Distribusi 17 Sektor Komoditas per Provinsi (Small Multiples, Tahun Terbaru)")
st.markdown("Visualisasi Small Multiples ini membandingkan komposisi 17 sektor komoditas secara terpisah di tiap provinsi. Sektor diurutkan dari penyumbang terbesar (atas) hingga terkecil (bawah). Skala sumbu X konsisten untuk memvalidasi perbandingan lintas provinsi.")

# VISUALISASI 2: Altair Small Multiples Horizontal Bar Chart (Current Year)
latest_year = df_pdrb['tahun'].max()
df_latest = df_pdrb[df_pdrb['tahun'] == latest_year].copy()

# Klasifikasikan 17 Sektor menjadi 3 Makro Warna
df_latest['Klasifikasi'] = df_latest['sektor_nama'].apply(klasifikasi_kritis)
df_latest['nilai_triliun_rp'] = df_latest['nilai_miliar_rp'] / 1000

# Add province totals to facet title
prov_totals = df_latest.groupby('provinsi')['nilai_miliar_rp'].sum().reset_index()
prov_totals['prov_title'] = prov_totals.apply(lambda r: f"{r['provinsi']} (Total: {r['nilai_miliar_rp']/1000:,.0f} Triliun Rp)", axis=1)

df_latest = df_latest.merge(prov_totals[['provinsi', 'prov_title']], on='provinsi')

# Shorten sector names for y-axis to fit well
df_latest['sektor_short'] = df_latest['sektor_nama'].apply(lambda x: x[:35] + '...' if len(x) > 35 else x)

# Custom Legend HTML (Sama seperti 1.1.1)
st.markdown(f"""
<div style="display: flex; gap: 20px; justify-content: center; margin-bottom: 25px; flex-wrap: wrap;">
    <div style="font-size: 13px;"><span style="color: {color_map[LABEL_AKAR_RUMPUT]}; font-size: 16px;">&bull;</span> {LABEL_AKAR_RUMPUT}</div>
    <div style="font-size: 13px;"><span style="color: {color_map[LABEL_JASA]}; font-size: 16px;">&bull;</span> {LABEL_JASA}</div>
    <div style="font-size: 13px;"><span style="color: {color_map[LABEL_EKSTRAKTIF]}; font-size: 16px;">&bull;</span> {LABEL_EKSTRAKTIF}</div>
</div>
""", unsafe_allow_html=True)

# Fixed X scale with 15% padding for text labels
max_x_val = df_latest['nilai_triliun_rp'].max() * 1.15

provinces = df_latest['prov_title'].unique()
cols_multi = st.columns(2)

for i, prov in enumerate(provinces):
    df_prov = df_latest[df_latest['prov_title'] == prov]
    
    bar_latest = alt.Chart(df_prov).mark_bar().encode(
        y=alt.Y('sektor_short:N', sort='-x', title=None, axis=alt.Axis(labels=True, ticks=False, labelOverlap=False, labelLimit=250, labelFontSize=11)),
        x=alt.X('nilai_triliun_rp:Q', title='Nilai PDRB (Triliun Rupiah)', scale=alt.Scale(domain=[0, max_x_val])),
        color=alt.Color('Klasifikasi:N', 
                        scale=alt.Scale(domain=cat_order_area, 
                                        range=[color_map[LABEL_AKAR_RUMPUT], color_map[LABEL_JASA], color_map[LABEL_EKSTRAKTIF]]),
                        legend=None),
        tooltip=[
            alt.Tooltip('sektor_nama:N', title='Sektor'),
            alt.Tooltip('Klasifikasi:N', title='Klasifikasi'),
            alt.Tooltip('nilai_triliun_rp:Q', title='Nilai (Triliun Rp)', format=',.1f'),
            alt.Tooltip('pct_dari_total:Q', title='Porsi (%)', format=',.1f')
        ]
    )

    text_latest = bar_latest.mark_text(
        align='left', baseline='middle', dx=3, color='black', fontSize=10
    ).encode(
        text=alt.Text('nilai_triliun_rp:Q', format=',.1f')
    )

    chart_latest = alt.layer(bar_latest, text_latest).properties(
        title=alt.TitleParams(text=prov, anchor='middle', fontSize=13, color='black'),
        height=380
    ).configure_view(
        stroke=None
    ).configure_axis(
        grid=True, gridColor='#333333'
    )
    
    cols_multi[i % 2].altair_chart(chart_latest, use_container_width=True)

st.markdown("""
<div style="background:#FFFFFF; padding:14px; border-radius:10px; border-left:5px solid #F44336; margin-bottom: 25px;">
    <b>Interpretasi Sektoral:</b> Analisis komoditas menunjukkan bahwa struktur PDRB Sulawesi Tengah didominasi secara signifikan oleh sektor Industri Pengolahan dan Pertambangan, berbeda dengan Sulawesi Selatan dan Gorontalo yang masih berbasis pada sektor Pertanian dan Perdagangan.
</div>
""", unsafe_allow_html=True)

with st.expander("Lihat Data Mentah: PDRB Sektoral", expanded=False):
    st.dataframe(df_pdrb, use_container_width=True, hide_index=True)
    st.caption("📁 **Sumber File:** `data/processed/sulawesi_pdrb_sektoral_2016_2024.csv` - Data dari BPS (SIMDASI).")

st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)



# ══════════════════════════════════════════════════════════
# SUB-BAB 1.2: INTENSIFIKASI RUANG (SMELTER & PLTU CAPTIVE)
# ══════════════════════════════════════════════════════════
st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
st.markdown("---")
st.subheader("1.2 Konsentrasi Kawasan Industri & PLTU Captive")
st.markdown('<span style="background:#4A148C;color:#E1BEE7;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: Analisis Spasial & Crosstab (Sentra vs Non-Sentra)</span>', unsafe_allow_html=True)
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

with st.expander("ℹ️ Metodologi: Analisis Spasial & Uji Tabulasi Silang"):
    st.markdown("""
    **Metode Analisis:** Halaman ini menggunakan pendekatan *Descriptive Spatial Analysis* dipadukan dengan Inferensial (Uji Chi-Square) untuk mengukur pemusatan infrastruktur energi (*PLTU Captive*) dan menguji hubungannya terhadap perubahan tutupan hutan secara statistik.

    1. **Analisis Profil (Chi-Square Test):** Mengukur signifikansi hubungan antara ekspansi kapasitas PLTU (X) dengan perubahan tutupan hutan (Y).
        * **Binning:** Data panel (Provinsi-Tahun) diklasifikasikan menjadi kategori "Tinggi" dan "Rendah" menggunakan ambang batas nilai Tengah (Median).
        * `H0 (Null Hypothesis): Tidak ada hubungan antara Penambahan Kapasitas PLTU Captive dan Laju Deforestasi.`
        * `Decision Rule: Jika P-Value < 0.05, maka Tolak H0 (Ada Hubungan Signifikan).`
    2. **Kalkulasi Emisi Historis (Cumulative Sum):** Merekam jejak emisi kumulatif PLTU dari tahun ke tahun.
        * `Kapasitas_Kumulatif_t = Kapasitas_Kumulatif_{t-1} + MW_t`
    3. **Pemetaan Konsentrasi Spasial (Proportional Ratio):** Mengukur distribusi lokasi fasilitas hilirisasi.
        * `Rasio Konsentrasi = (Fasilitas_Provinsi_X / Total_Fasilitas_Sulawesi) * 100%`
    4. **Variabel & Fitur Data PLTU (Global Energy Monitor):**
        * **Plant/Unit name, Owner/Parent:** Identitas dan kepemilikan.
        * **Capacity (MW), Status, Start year:** Kapasitas aktif dan tahun mulai operasi.
        * **Subnational unit (Provinsi), Local area:** Lokasi operasional.
        * **Captive industry use, captive_flag:** Penanda PLTU khusus industri.
    5. **Variabel & Fitur Data Smelter (ESDM/CGS):**
        * **nama_perusahaan, jenis_badan_usaha:** Identitas perusahaan.
        * **provinsi, komoditas, golongan:** Lokasi dan jenis tambang.
        * **total_luas_ha, nilai_investasi_usd_juta:** Luas area dan kapitalisasi modal.
        * **kapasitas_produksi_ton_tahun, status_operasional:** Output produksi dan status operasional.
    6. **Dataset & File:**
        * PLTU: `data/processed/sulawesi_pltu_captive.csv`
        * Smelter: `data/processed/sulawesi_esdm_nikel.csv`
    """)

# --- Hitung Variabel PLTU dan Smelter ---
sulawesi_provs = ['Sulawesi Utara', 'Sulawesi Selatan', 'Sulawesi Tenggara', 'Sulawesi Tengah', 'Gorontalo', 'Sulawesi Barat']
df_pltu_op_sul = df_pltu[(df_pltu['Status'].str.lower() == 'operating') & (df_pltu['Subnational unit (province, state)'].isin(sulawesi_provs))].copy()
df_pltu_op_sul['Tahun'] = pd.to_numeric(df_pltu_op_sul['Start year'], errors='coerce')

# Klasifikasi Sentra vs Non-Sentra
sentra_provs = ['Sulawesi Tengah', 'Sulawesi Tenggara']
df_pltu_op_sul['Kategori_Wilayah'] = df_pltu_op_sul['Subnational unit (province, state)'].apply(lambda x: 'Daerah Sentra Tambang' if x in sentra_provs else 'Daerah Non-Sentra')

# Agregasi Kumulatif per Kategori (Untuk Grafik Split)
df_pltu_kategori = df_pltu_op_sul.groupby(['Kategori_Wilayah', 'Tahun'])['Capacity (MW)'].sum().reset_index().sort_values(['Kategori_Wilayah', 'Tahun'])
df_pltu_kategori['Kumulatif (MW)'] = df_pltu_kategori.groupby('Kategori_Wilayah')['Capacity (MW)'].cumsum()

# Agregasi Total (Untuk Teks Narasi)
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
Intensifikasi industri pengolahan nikel di Sulawesi berpusat pada fasilitas mega-smelter. Pengoperasian **{tot_smelter} fasilitas smelter** didukung oleh kapasitas energi batu bara **{int(tot_kapasitas_pltu):,} MW dari PLTU Captive**. Berbeda dengan sistem kelistrikan umum PLN, pembangkit ini dikembangkan secara internal untuk menyokong operasi kawasan industri.

Berikut adalah **temuan konsentrasi spasial** berdasarkan data agregat:

**Pemusatan Spasial Fasilitas Smelter (Bar Chart):** Data menunjukkan bahwa **{int(persen_smelter_2prov):,}% dari total fasilitas ({sulteng_smelter} unit di Sulawesi Tengah dan {sultra_smelter} unit di Sulawesi Tenggara)** terkonsentrasi di dua provinsi tersebut. Pola ini mengonfirmasi adanya pemusatan beban ekologis dan emisi pada zona sentra pemurnian nikel.

Korelasi antara pembangunan kawasan industri dan perubahan tutupan lahan diuji menggunakan **Crosstabulation (Tabulasi Silang)** pada bagian bawah sub-bab ini.
""")

# --- Visualisasi Tambahan Advokasi: Zona Tumbal ---
# Zona Tumbal (Smelter Bar Chart dengan Persentase)
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

chart_smelter = (bars + text).properties(height=350, title=alt.TitleParams(text='Konsentrasi 78% Smelter di Sulawesi Tengah & Tenggara', color='#ECEFF1', anchor='start', fontSize=16))

st.altair_chart(chart_smelter, use_container_width=True)
st.markdown("<div style='font-size:0.85rem; color:#9E9E9E; margin-top:-10px; margin-bottom:15px; padding: 0 10px; border-left: 3px solid #F57C00;'><b>Fakta Data:</b> Sebesar 78% dari total 778 fasilitas smelter terkonsentrasi di Sulawesi Tengah & Sulawesi Tenggara, menunjukkan adanya pemusatan beban lingkungan di wilayah sentra tersebut.</div>", unsafe_allow_html=True)

with st.expander("Lihat Data Detail: Daftar Izin Smelter (PT & Lokasi)", expanded=False):
    # Pilih kolom penting
    cols_to_show = ['nama_perusahaan', 'provinsi', 'lokasi_izin', 'komoditas', 'total_luas_ha']
    # Pastikan kolom ada sebelum ditampilkan
    available_cols = [c for c in cols_to_show if c in df_smelter.columns]
    
    st.dataframe(df_smelter[available_cols], use_container_width=True, hide_index=True)
    st.caption("📁 **Sumber File:** Data mentah dari `sulawesi_esdm_nikel.csv`. Data di atas menyertakan Nama PT dan Lokasi secara detail.")

st.markdown(f"""
<div style="background:#FFFFFF; padding:14px; border-radius:10px; border-left:5px solid #D32F2F; margin-bottom: 20px;">
    <b style="color: #D32F2F;">Interpretasi Spasial Industri:</b><br><br>
    Kawasan industri pengolahan terkonsentrasi di area pesisir secara signifikan. Pertumbuhan PLTU Captive mengindikasikan tingginya ketergantungan pada energi berbasis batu bara untuk mendukung kebutuhan energi fasilitas pemurnian di Sulawesi Tengah dan Sulawesi Tenggara.
</div>
""", unsafe_allow_html=True)

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

label_x_low_2 = f"Rendah (≤{int(x_thresh_2):,})"
label_x_high_2 = f"Tinggi (>{int(x_thresh_2):,})"
label_y_low_2 = f"Rendah (<{int(y_median_2):,})"
label_y_high_2 = f"Tinggi (≥{int(y_median_2):,})"

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
    rows_2.append([f"{round(v, 1)}" for v in exps] + [f"{sum(exps):.1f}"])

tot_cnts_2 = crosstab_2.sum().tolist()
tot_exps_2 = expected_df_2.sum().tolist()
rows_2.append(tot_cnts_2 + [sum(tot_cnts_2)])
rows_2.append([f"{round(v, 1)}" for v in tot_exps_2] + [f"{sum(tot_exps_2):.1f}"])

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
    [f"{round(chi2_2, 3)}", str(dof_2), f"{round(p_2, 3)}"],
    [f"{round(g_2, 3)}", str(dof_g_2), f"{round(p_g_2, 3)}"],
    [f"{round(lbl_val_2, 3)}", "1", f"{round(p_corr_2, 3)}"],
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
            P-Value    : {round(p_2, 4)}<br>
            Chi-Square : {round(chi2_2, 3)}<br>
            df         : {dof_2}
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"**Odds Ratio (Risk Estimate):** `{round(or_2, 3)}`")

with cr2:
    if is_sig_2:
        interp_txt_2 = f"Bukti empiris menegaskan bahwa kehadiran dan penambahan kapasitas PLTU Captive secara spasial-temporal di Sulawesi **signifikan memicu ekskalasi deforestasi** (OR: {round(or_2, 3)}). Kompleks PLTU tidak hanya mengunci emisi kotor, tetapi infrastruktur pendukungnya membongkar fungsi kawasan penyangga."
    else:
        interp_txt_2 = f"Meski data tahunan agregat menunjukkan tidak signifikan (kemungkinan karena konsentrasi PLTU hanya terjadi di segelintir tahun dan lokasi seperti Morowali), hal ini **bukan berarti PLTU ramah lingkungan**. Sebaliknya, efek rusak dari sebuah PLTU bersifat permanen dan lintas-batas (spillover) yang mencemari wilayah di luar lokasi spesifik pendiriannya."
    
    st.markdown(f"""
    <div style="background:#FFFFFF; padding:14px; border-radius:10px; border-left:5px solid {ord_col_2}; height: 100%;">
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
        
        lbl_x_h = f"Tinggi (>{int(thresh_x):,})"
        lbl_x_l = f"Rendah (≤{int(thresh_x):,})"
        lbl_y_h = f"Tinggi (≥{int(med_y):,})"
        lbl_y_l = f"Rendah (<{int(med_y):,})"
        
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
            "Chi-Square": f"{round(c2_val, 3)}",
            "P-Value": f"{round(pv_val, 3)}",
            "Odds Ratio": f"{round(or_v, 2)}",
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
# SUB-BAB 1.3: TREN IZIN & CROSSTABULATION
# ══════════════════════════════════════════════════════════
st.markdown("---")
st.subheader("1.3 Tren Pertumbuhan Izin Tambang Baru & Uji Signifikansi")
with st.expander("ℹ️ Metodologi: Analisis Tren & Uji Tabulasi Silang"):
    st.markdown("""
    **Metode Analisis:** Halaman ini menggunakan pendekatan statistik *Time-Series* dan Inferensial (Uji Chi-Square) untuk menguji hipotesis bahwa ekspansi izin tambang berbanding lurus dengan laju deforestasi.

    1. **Analisis Profil (Chi-Square Test):** Mengukur signifikansi hubungan antara tekanan ekspansi (X) dengan perubahan tutupan hutan (Y).
        * **Binning:** Data panel (Provinsi-Tahun) diklasifikasikan menjadi kategori "Tinggi" dan "Rendah" menggunakan ambang batas nilai Tengah (Median).
        * `H0 (Null Hypothesis): Tidak ada hubungan antara Ekspansi Perizinan dan Laju Deforestasi.`
        * `Decision Rule: Jika P-Value < 0.05, maka Tolak H0 (Ada Hubungan Signifikan).`
    2. **Formula Analisis Tren (Time-Series):** Mengukur agregasi jumlah izin baru dan tren persentase lonjakan (*Year-on-Year*).
        * `Regresi Komparatif = (IUP_t - IUP_{t-1}) / IUP_{t-1} * 100%`
    3. **Variabel & Fitur Data:**
        * **Provinsi:** Nama provinsi lokasi izin.
        * **Tahun:** Tahun penerbitan izin.
        * **Jumlah_Izin_Baru:** Total izin baru yang terbit di tahun tersebut.
        * **Total_Luas_Konsesi_Baru_Ha:** Luas konsesi (Hektar).
        * **Sumber:** Metadata sumber data Minerbaone.
    4. **Dataset & File:** Dataset primer dari Minerbaone (Kementerian ESDM).
        * `data/processed/sulawesi_izin_baru_per_tahun.csv`
    """)

# --- Pindahkan agregasi ke atas markdown ---
df_izin_agg = df_izin.groupby(['Tahun', 'Provinsi'])['Jumlah_Izin_Baru'].sum().reset_index()
df_izin_total = df_izin_agg.groupby('Tahun')['Jumlah_Izin_Baru'].sum().reset_index()

val_izin_2014 = df_izin_total[df_izin_total['Tahun'] == 2014]['Jumlah_Izin_Baru'].values[0] if 2014 in df_izin_total['Tahun'].values else 0
val_izin_2022 = df_izin_total[df_izin_total['Tahun'] == 2022]['Jumlah_Izin_Baru'].values[0] if 2022 in df_izin_total['Tahun'].values else 0
val_izin_2023 = df_izin_total[df_izin_total['Tahun'] == 2023]['Jumlah_Izin_Baru'].values[0] if 2023 in df_izin_total['Tahun'].values else 0
val_izin_2024 = df_izin_total[df_izin_total['Tahun'] == 2024]['Jumlah_Izin_Baru'].values[0] if 2024 in df_izin_total['Tahun'].values else 0

st.markdown(f"""
Pola perizinan pertambangan di Pulau Sulawesi selama satu dekade terakhir menunjukkan peningkatan alokasi ruang yang signifikan. Berdasarkan data agregat *Minerbaone*, tercatat **{int(tot_izin):,} Izin Usaha Pertambangan (IUP) baru** sepanjang 2014-2024, dengan total luas konsesi mencapai **{int(tot_luas_izin):,} Hektar**.

Berdasarkan analisis tren time-series pada grafik **"Penerbitan Izin Tambang"** di bawah, penerbitan izin pada periode awal (2014) tercatat sebanyak **{int(val_izin_2014):,} IUP**. Peningkatan signifikan terjadi pada periode 2022–2024, di mana penerbitan meningkat dari **{int(val_izin_2022):,} IUP di tahun 2022** menjadi **{int(val_izin_2023):,} IUP pada 2023**, dan mencapai **{int(val_izin_2024):,} IUP baru pada 2024**.

Anotasi pada grafik mencatat kenaikan sebesar **246% pada periode 2022–2024**. Data ini mengindikasikan perlunya evaluasi terhadap instrumen pengendalian perizinan dan tata ruang. Distribusi perizinan tertinggi berada di Sulawesi Tengah dan Sulawesi Tenggara, yang selaras dengan kawasan pengembangan industri pemurnian nikel.

Uji **Crosstabulation** pada bagian bawah mengukur hubungan antara laju penerbitan perizinan dan indikator deforestasi di wilayah tersebut.
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
    annotation_text = f"↑ {int(pct_increase):,}% Kenaikan (2022-2024)"
except IndexError:
    annotation_text = "Peningkatan Signifikan"

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
    title='Tren Penerbitan Izin Tambang Sulawesi (2014-2024)'
).configure_axis(
    grid=True,
    gridOpacity=0.1
)

st.altair_chart(chart_izin, use_container_width=True)

st.markdown("""
<div style="background:#FFFFFF; padding:14px; border-radius:10px; border-left:5px solid #FF5722; margin-bottom: 25px;">
    <b>Interpretasi Sektoral:</b> Peningkatan penerbitan IUP di kawasan timur Sulawesi berbanding lurus dengan perluasan area konversi hutan. Pola perizinan ini menunjukkan pentingnya penerapan instrumen tata ruang dan evaluasi lingkungan secara ketat.
</div>
""", unsafe_allow_html=True)

with st.expander("Lihat Data Mentah: Agregat Izin Minerbaone", expanded=False):
    st.dataframe(df_izin_agg, use_container_width=True, hide_index=True)
    st.caption("📁 **Sumber File:** `data/processed/sulawesi_izin_baru_per_tahun.csv` - Agregat penerbitan izin tambang baru per provinsi di Sulawesi.")

# --- Crosstab Introduction ---
st.markdown("#### Pembuktian Statistik: Intensitas Ekspansi vs Deforestasi")
st.markdown("""
Hipotesis utama narasi ini adalah bahwa **lonjakan ekspansi ekstraktif** berbanding lurus dengan **kebangkrutan ekologis** (deforestasi). 
Untuk mengujinya secara statistik di tengah keterbatasan jumlah provinsi di Sulawesi (N=6), tabel crosstab dan uji Chi-Square di bawah menggunakan unit observasi **Provinsi-Tahun** (6 provinsi x 10 tahun = 60 sampel panel). 
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

label_x_low = f"Rendah (<{int(x_median):,})"
label_x_high = f"Tinggi (≥{int(x_median):,})"
label_y_low = f"Rendah (<{int(y_median):,})"
label_y_high = f"Tinggi (≥{int(y_median):,})"

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
st.caption("Tabel-tabel di bawah ini adalah *output* statistik formal yang menyajikan bukti statistik formal: Case Processing → Crosstabulation → Chi-Square Tests → Ringkasan Hipotesis.")

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
    rows.append([f"{round(v, 1)}" for v in exps] + [f"{sum(exps):.1f}"])

total_counts = crosstab.sum().tolist()
total_exps = expected_df.sum().tolist()
rows.append(total_counts + [sum(total_counts)])
rows.append([f"{round(v, 1)}" for v in total_exps] + [f"{sum(total_exps):.1f}"])

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
    [f"{round(chi2, 3)}", str(dof), f"{round(p, 3)}"],
    [f"{round(g, 3)}", str(dof), f"{round(p_g, 3)}"],
    [f"{round(lbl_val, 3)}", "1", f"{round(p_corr, 3)}"],
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
            P-Value    : {round(p, 4)}<br>
            Chi-Square : {round(chi2, 3)}<br>
            df         : {dof}
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"**Odds Ratio (Risk Estimate):** `{round(odds_ratio, 3)}`")

with col_res2:
    if is_significant:
        interp_text = f"Temuan ini sangat krusial: lonjakan intensitas {x_options[x_col]} terbukti **berkorelasi kuat dan signifikan** dengan peningkatan {y_options[y_col]} (OR: {round(odds_ratio, 3)}). Ini adalah konfirmasi empiris bahwa narasi hilirisasi dan investasi ekstraktif bukanlah pertumbuhan tanpa korban-ekspansi spasial mereka mutlak mengorbankan luasan hutan di tingkat tapak."
    else:
        interp_text = f"Secara agregat, hubungan antara {x_options[x_col]} dan {y_options[y_col]} **tidak signifikan** secara statistik (P ≥ 0.05). Ini mengindikasikan bahwa deforestasi terjadi sangat masif di seluruh panel waktu dan ruang secara merata. Krisis tata kelola dan deforestasi telah menyebar ke seluruh wilayah, sehingga lonjakan izin di tahun tertentu tidak lagi menjadi prediktor tunggal atas kebangkrutan ekologis yang sudah sistemik."
    
    st.markdown(f"""
    <div style="background:#FFFFFF; padding:14px; border-radius:10px; border-left:5px solid {order_color}; height: 100%;">
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
        
        lbl_x_h = f"Tinggi (≥{int(med_x):,})"
        lbl_x_l = f"Rendah (<{int(med_x):,})"
        lbl_y_h = f"Tinggi (≥{int(med_y):,})"
        lbl_y_l = f"Rendah (<{int(med_y):,})"
        
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
            "Chi-Square": f"{round(c2_val, 3)}",
            "P-Value": f"{round(pv_val, 3)}",
            "Odds Ratio": f"{round(or_v, 2)}",
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
Menariknya, jika ada skenario yang menunjukkan <i>TIDAK SIGNIFIKAN</i> (khususnya pada deforestasi komoditas spesifik), ini tidak berarti industri ekstraktif ramah lingkungan. Sebaliknya, ini menjadi indikasi mengerikan bahwa <b>kehancuran ekologis telah menyebar tak terkendali (spillover effect)</b>-di mana kerusakan hutan akibat operasi tambang menjalar jauh melampaui batas konsesi resmi komoditasnya hingga merusak total lanskap alam secara merata.\
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
# SUB-BAB 1.4: REALISASI INVESTASI VS BEBAN LAHAN
# ══════════════════════════════════════════════════════════
st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
st.markdown("---")
st.subheader("1.4 Analisis Realisasi Investasi PMDN dan Dampak Terhadap Tutupan Hutan")
st.markdown('<span style="background:#4A148C;color:#E1BEE7;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: Analisis Spasial, Dual-Axis Split & Uji Chi-Square</span>', unsafe_allow_html=True)
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

with st.expander("ℹ️ Metodologi: Analisis Spasial & Uji Chi-Square (Crosstab)"):
    st.markdown("""
    **Metode Analisis:** Sub-bab ini menggunakan pendekatan *Descriptive Spatial Analysis* dan inferensi statistik melalui Uji Chi-Square (Crosstabulation) untuk menguji korelasi antara kucuran modal PMDN dengan tingkat perubahan tutupan hutan secara spasial.

    1. **Uji Tabulasi Silang (Chi-Square Test of Independence):** Mengukur signifikansi hubungan antara arus masuk investasi (X) dengan tingkat perubahan tutupan hutan (Y).
        * **Binning Kategori:** Variabel kontinu dikonversi menjadi data kategorikal (Biner) menggunakan nilai tengah (Median). 'Tinggi' > Median, 'Rendah' <= Median.
        * `H0 (Null Hypothesis): Tidak ada hubungan signifikan secara statistik antara tingginya arus modal PMDN dengan laju deforestasi.`
        * `Decision Rule (Alpha 5%): Jika P-Value < 0.05, maka Tolak H0 (Terbukti secara empiris bahwa kucuran investasi berkorelasi dengan perubahan tutupan hutan).`
    2. **Kalkulasi Dual-Axis (Trend Comparison):** Membandingkan secara visual tren investasi (Bar Chart) terhadap fluktuasi laju deforestasi komoditas (Line Chart) menggunakan skala ganda (Dual-Axis) terpisah per kategori wilayah.
        * `Tahun_t (Investasi) vs Tahun_t (Deforestasi)`
    3. **Variabel & Fitur Data Investasi (BKPM):**
        * **Tahun, Provinsi:** Dimensi waktu dan lokasi.
        * **nilai (Juta Rupiah):** Realisasi Investasi Penanaman Modal Dalam Negeri (PMDN).
    4. **Variabel & Fitur Data Deforestasi (GFW):**
        * **Provinsi, Tahun:** Dimensi spasial dan temporal deforestasi.
        * **Total_Deforestasi_Ha:** Angka agregat seluruh jenis kerusakan tutupan lahan.
        * **Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha:** Deforestasi khusus komoditas ekstraktif.
    5. **Dataset & File:**
        * Investasi: `data/processed/sulawesi_investasi_pmdn_2016_2024.csv`
        * Deforestasi: `data/processed/sulawesi_gfw_master_1_dekade_2014_2023.csv`
    """)

# --- Variabel Time Series Investasi & Deforestasi (Split Sentra vs Non-Sentra) ---
sentra_provs = ['Sulawesi Tengah', 'Sulawesi Tenggara']

# Grouping GFW by Kategori
df_gfw_kat = df_gfw.copy()
df_gfw_kat['Kategori_Wilayah'] = df_gfw_kat['Provinsi'].apply(lambda x: 'Sentra Tambang' if x in sentra_provs else 'Non-Sentra')
df_gfw_kategori = df_gfw_kat.groupby(['Kategori_Wilayah', 'Tahun'])['Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha'].sum().reset_index()

# Grouping Izin Tambang Baru by Kategori
df_izin_kat = df_izin.copy()
df_izin_kat['Kategori_Wilayah'] = df_izin_kat['Provinsi'].apply(lambda x: 'Sentra Tambang' if x in sentra_provs else 'Non-Sentra')
df_izin_kategori = df_izin_kat.groupby(['Kategori_Wilayah', 'Tahun'])['Total_Luas_Konsesi_Baru_Ha'].sum().reset_index()

df_viz_1_3 = pd.merge(df_gfw_kategori, df_izin_kategori, on=['Kategori_Wilayah', 'Tahun'], how='inner')

# Agregat Total Untuk Narasi
df_gfw_agg = df_gfw.groupby('Tahun')['Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha'].sum().reset_index()
df_izin_agg = df_izin_kat.groupby('Tahun')['Total_Luas_Konsesi_Baru_Ha'].sum().reset_index()

val_izin_2016 = df_izin_agg[df_izin_agg['Tahun'] == 2016]['Total_Luas_Konsesi_Baru_Ha'].values[0] if 2016 in df_izin_agg['Tahun'].values else 0
val_izin_2023 = df_izin_agg[df_izin_agg['Tahun'] == 2023]['Total_Luas_Konsesi_Baru_Ha'].values[0] if 2023 in df_izin_agg['Tahun'].values else 0
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
    
    # Relabel jujur: BPS tidak menyediakan data PAD level provinsi untuk Sulawesi Tenggara.
    # Yang tersedia hanyalah pendapatan Pemerintah Desa (Kab. Buton), bukan PAD provinsi.
    # Beri label eksplisit agar tidak menyesatkan pembaca.
    mask_sultra = df_pad_combined['Provinsi'] == 'Sulawesi Tenggara'
    df_pad_combined.loc[mask_sultra, 'Jenis_Pendapatan'] = 'PAD Kab. Buton (BPS: no data provinsi)'
    
    # Buang baris bernilai sangat kecil (< 0.05 Miliar / 50 juta Rp).
    # Kotak bernilai puluhan juta ditampilkan sebagai "0.0 M Rp" oleh format :,.1f → menyesatkan.
    # Threshold 0.05 Miliar = 50 juta agar hanya komponen signifikan yang tampil.
    df_pad_combined = df_pad_combined[df_pad_combined['Nilai_Miliar_Rp'] > 0.05].reset_index(drop=True)
    
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

    # Hitung share 4 komponen PAD murni (Pajak Daerah, Retribusi, Hasil BUMD, Lain-lain PAD)
    # secara dinamis dari data. Kecualikan transfer pusat (Dana Alokasi, Bagi Hasil, dll) dan
    # baris "Total/agregat" yang bukan komponen PAD, agar persentase di narasi tidak drift.
    pad_komponen = ['Pajak Daerah', 'Retribusi Daerah', 'Hasil BUMD', 'Lain-lain PAD Yang Sah']
    df_pad_murni = df_pad_combined[df_pad_combined['Jenis_Pendapatan'].isin(pad_komponen)]
    total_pad_murni = df_pad_murni['Nilai_Miliar_Rp'].sum()

    def _share_pad(komponen):
        v = df_pad_murni.loc[df_pad_murni['Jenis_Pendapatan'] == komponen, 'Nilai_Miliar_Rp'].sum()
        return (v / total_pad_murni * 100) if total_pad_murni > 0 else 0.0

    pct_pajak_daerah = _share_pad('Pajak Daerah')
    pct_retribusi = _share_pad('Retribusi Daerah')
    pct_hasil_bumd = _share_pad('Hasil BUMD')
    pct_lain_pad = _share_pad('Lain-lain PAD Yang Sah')
    
    # Count provinces with breakdown
    num_prov_breakdown = len(provinsi_with_breakdown)
    total_prov = len(df_pad_prov)
    
    has_pad_data = True
except Exception as e:
    has_pad_data = False
    st.warning(f"Data PAD tidak ditemukan: {e}")


st.markdown("<br>", unsafe_allow_html=True)

st.markdown(f"""
Grafik di bawah ini memetakan dinamika penerbitan konsesi tambang baru dan dampaknya terhadap tutupan hutan. Pada tahun 2016, luas konsesi tambang baru yang diterbitkan di Sulawesi mencakup **{int(val_izin_2016):,} Hektar**, dan meningkat signifikan hingga mencapai **{int(val_izin_2023):,} Hektar** pada tahun 2023. Pada periode yang sama, angka deforestasi komoditas mencatatkan luasan sebesar **{int(val_def_2023):,} Hektar**.

Data ini mengindikasikan bahwa akselerasi penerbitan konsesi berbanding lurus dengan laju konversi hutan alam (akumulasi deforestasi sebesar **{int(tot_deforestasi):,} Hektar**). Hal ini menegaskan pentingnya pertimbangan daya dukung ekologis dalam setiap kebijakan alokasi konsesi pertambangan.
""")

col_chart_s, col_chart_n = st.columns(2)
max_y_izin = df_viz_1_3['Total_Luas_Konsesi_Baru_Ha'].max() * 1.1

with col_chart_s:
    st.markdown("<h5 style='color:#ECEFF1; text-align:center;'>Daerah Sentra Tambang</h5>", unsafe_allow_html=True)
    df_s = df_viz_1_3[df_viz_1_3['Kategori_Wilayah'] == 'Sentra Tambang']
    chart_s = alt.Chart(df_s).mark_bar(opacity=0.8, color='#F57C00').encode(
        x=alt.X('Tahun:O', title='', axis=alt.Axis(labelAngle=-45, labelColor='#B0BEC5')),
        y=alt.Y('Total_Luas_Konsesi_Baru_Ha:Q', scale=alt.Scale(domain=[0, max_y_izin]), title='Luas Konsesi Baru (Ha)', axis=alt.Axis(gridOpacity=0.05, labelColor='#B0BEC5', titleColor='#B0BEC5')),
        tooltip=['Tahun', alt.Tooltip('Total_Luas_Konsesi_Baru_Ha', format=',.0f', title='Konsesi Baru (Ha)')]
    ).properties(height=350)
    st.altair_chart(chart_s, use_container_width=True)

with col_chart_n:
    st.markdown("<h5 style='color:#ECEFF1; text-align:center;'>Daerah Non-Sentra</h5>", unsafe_allow_html=True)
    df_n = df_viz_1_3[df_viz_1_3['Kategori_Wilayah'] == 'Non-Sentra']
    chart_n = alt.Chart(df_n).mark_bar(opacity=0.8, color='#90A4AE').encode(
        x=alt.X('Tahun:O', title='', axis=alt.Axis(labelAngle=-45, labelColor='#B0BEC5')),
        y=alt.Y('Total_Luas_Konsesi_Baru_Ha:Q', scale=alt.Scale(domain=[0, max_y_izin]), title='Luas Konsesi Baru (Ha)', axis=alt.Axis(gridOpacity=0.05, labelColor='#B0BEC5', titleColor='#B0BEC5')),
        tooltip=['Tahun', alt.Tooltip('Total_Luas_Konsesi_Baru_Ha', format=',.0f', title='Konsesi Baru (Ha)')]
    ).properties(height=350)
    st.altair_chart(chart_n, use_container_width=True)

st.markdown(f"""
<div style="background:#FFFFFF; padding:14px; border-radius:10px; border-left:5px solid #D32F2F; margin-bottom: 20px;">
    <b>Interpretasi Spasial:</b> Perbandingan grafik batang di atas menunjukkan bahwa tingkat alokasi konsesi di Daerah Sentra Tambang (Morowali & Konawe) jauh lebih tinggi dibanding wilayah non-sentra, yang berdampak langsung pada konsentrasi perubahan tutupan hutan.
</div>
""", unsafe_allow_html=True)

with st.expander("Lihat Data Mentah: Ekspansi Konsesi vs Deforestasi", expanded=False):
    df_table_1_3 = df_viz_1_3.copy()
    df_table_1_3 = df_table_1_3.rename(columns={
        'Tahun': 'Tahun',
        'Kategori_Wilayah': 'Kategori Wilayah',
        'Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha': 'Deforestasi Komoditas (Ha)',
        'Total_Luas_Konsesi_Baru_Ha': 'Luas Konsesi Tambang Baru (Ha)'
    })
    
    st.dataframe(df_table_1_3, use_container_width=True, hide_index=True)
    st.caption("📁 **Sumber File:** `sulawesi_izin_baru_per_tahun.csv` & `sulawesi_gfw_master_1_dekade_2014_2023.csv` - Data Kementerian ESDM (Izin) dan GFW.")


# Memuat data tambahan untuk 3 Dashboard Cards GFW
try:
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path_driver = os.path.join(base_dir, 'data', 'raw', 'klhk_gfw', 'land_api_fetch', 'loss_by_driver_sulawesi_2001_2025.csv')
    path_primary = os.path.join(base_dir, 'data', 'raw', 'klhk_gfw', 'mega_fetch_v2', 'primary_forest_loss_sulawesi_2001_2025.csv')
    
    df_driver_gfw = pd.read_csv(path_driver)
    df_primary_gfw = pd.read_csv(path_primary)
    
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
    ).properties(height=350, title=alt.TitleParams(text="Perubahan Tutupan Hutan Primer", color='#ECEFF1'))

    # 3. Bar Chart (Emisi CO2 Komoditas)
    df_co2 = df_driver_gfw[df_driver_gfw['driver'] == 'Commodity driven deforestation']
    df_co2_agg = df_co2.groupby('year')['co2_emissions_mg'].sum().reset_index()
    chart_co2 = alt.Chart(df_co2_agg).mark_bar(color='#5D4037').encode(
        x=alt.X('year:O', title='Tahun', axis=alt.Axis(labelAngle=-45, labelColor='#B0BEC5', titleColor='#B0BEC5')),
        y=alt.Y('co2_emissions_mg:Q', title='Emisi CO2 (Megagrams)', axis=alt.Axis(labelColor='#B0BEC5', titleColor='#B0BEC5', gridOpacity=0.05)),
        tooltip=['year', alt.Tooltip('co2_emissions_mg', format=',.0f')]
    ).properties(height=350, title=alt.TitleParams(text="Estimasi Emisi Karbon Komoditas", color='#ECEFF1'))

    st.markdown("---")
    st.markdown("#### Pembedahan Ekologis: Aktor, Dampak, dan Emisi")
    
    tot_primary_loss = df_primary_agg['area__ha'].sum()
    tot_co2_emissions = df_co2_agg['co2_emissions_mg'].sum()
    
    st.markdown(f"""
Berdasarkan data Global Forest Watch (GFW), analisis penyebab deforestasi di Sulawesi mengonfirmasi faktor-faktor berikut:

**1. Aktor Utama Deforestasi (Donut Chart):** Konversi tutupan hutan terbesar didominasi oleh **Ekspansi Komoditas (Tambang & Perkebunan Monokultur)** yang mencapai **{int(area_komoditas):,} Hektar** ({komoditas_str}), mengindikasikan bahwa pembukaan lahan didorong oleh aktivitas sektor industri skala besar.

**2. Perubahan Tutupan Hutan Primer (Bar Chart Tengah):** Akumulasi konversi lahan mencakup **{int(tot_primary_loss):,} Hektar Hutan Primer**, yang memiliki peranan kunci dalam menjaga keanekaragaman hayati dan penyimpan cadangan karbon alami.

**3. Estimasi Emisi Karbon (Bar Chart Kanan):** Konversi hutan alam untuk aktivitas komoditas melepaskan estimasi emisi sebesar **{int(tot_co2_emissions):,} Megagrams CO2**, yang menjadi catatan penting dalam inventarisasi emisi sektor berbasis lahan.
""")
    
    col_v1, col_v2, col_v3 = st.columns(3)
    
    with col_v1:
        st.markdown("<b style='color:#ECEFF1;'>Aktor Utama Deforestasi</b>", unsafe_allow_html=True)
        col_leg, col_chart = st.columns([1.2, 1])
        with col_leg:
            st.markdown(f"""
            <div style="font-family: sans-serif; line-height: 1.2; margin-top: 15%;">
                <div style="margin-bottom: 12px;">
                    <span style="color: #D32F2F; font-size: 0.8rem;">&bull;</span> <span style="color: #B0BEC5; font-size: 0.85rem;">Ekspansi Komoditas</span><br>
                    <strong style="color: #D32F2F; font-size: 1.5rem;">{komoditas_str}</strong>
                </div>
                <div style="margin-bottom: 12px;">
                    <span style="color: #4CAF50; font-size: 0.8rem;">&bull;</span> <span style="color: #B0BEC5; font-size: 0.85rem;">Kehutanan (Logging)</span><br>
                    <strong style="color: #4CAF50; font-size: 1.2rem;">{forestry_str}</strong>
                </div>
                <div>
                    <span style="color: #FFC107; font-size: 0.8rem;">&bull;</span> <span style="color: #B0BEC5; font-size: 0.85rem;">Pertanian Berpindah</span><br>
                    <strong style="color: #FFC107; font-size: 1.2rem;">{shifting_str}</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_chart:
            st.altair_chart(chart_donut, use_container_width=True)
        st.caption("Investasi komoditas (merah) mendominasi porsi penyebab konversi hutan di Sulawesi.")
    with col_v2:
        st.altair_chart(chart_primary, use_container_width=True)
        st.caption("Perubahan tutupan mencakup area Hutan Primer.")
    with col_v3:
        st.altair_chart(chart_co2, use_container_width=True)
        st.caption("Estimasi pelepasan emisi CO2 akibat konversi lahan berbasis komoditas.")
        
except Exception as e:
    st.warning(f"Tidak dapat memuat visualisasi tambahan: {e}")


with st.expander("Lihat Data Mentah: Deforestasi GFW", expanded=False):
    st.dataframe(df_gfw, use_container_width=True, hide_index=True)

# --- Crosstab 1.4: Investasi PMDN vs Deforestasi ---
st.markdown("#### Pembuktian Statistik: Arus Investasi PMDN vs Deforestasi")
st.markdown("""
Menggunakan tabel crosstab untuk menguji korelasi spasial-temporal antara arus masuk Investasi PMDN dengan tingkat kerusakan hutan (Deforestasi) pada level panel **Provinsi-Tahun**. Variabel *Investasi* akan dipecah berdasarkan nilai tengah (median) menjadi 'Tinggi' dan 'Rendah', begitu pula dengan variabel *Deforestasi*.
""")

# Data Preparation untuk Panel 1.4
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

# Calculation (Binning for 1.4)
x_median_3 = df_panel_1_3[x_col_3].median()
x_thresh_3 = x_median_3 if x_median_3 > 0 else 0
y_median_3 = df_panel_1_3[y_col_3].median()

label_x_low_3 = f"Rendah (≤{int(x_thresh_3):,})"
label_x_high_3 = f"Tinggi (>{int(x_thresh_3):,})"
label_y_low_3 = f"Rendah (<{int(y_median_3):,})"
label_y_high_3 = f"Tinggi (≥{int(y_median_3):,})"

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

# A. Case Processing Summary 1.4
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

# B. Crosstabulation 1.4
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
    rows_3.append([f"{round(v, 1)}" for v in exps] + [f"{sum(exps):.1f}"])

tot_cnts_3 = crosstab_3.sum().tolist()
tot_exps_3 = expected_df_3.sum().tolist()
rows_3.append(tot_cnts_3 + [sum(tot_cnts_3)])
rows_3.append([f"{round(v, 1)}" for v in tot_exps_3] + [f"{sum(tot_exps_3):.1f}"])

m_idx_3 = pd.MultiIndex.from_tuples(row_idx_3, names=[x_options_3[x_col_3], ""])
st.table(pd.DataFrame(rows_3, index=m_idx_3, columns=cats_y_3 + ["Total"]))

# C. Chi-Square Tests 1.4
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
    [f"{round(chi2_3, 3)}", str(dof_3), f"{round(p_3, 3)}"],
    [f"{round(g_3, 3)}", str(dof_g_3), f"{round(p_g_3, 3)}"],
    [f"{round(lbl_val_3, 3)}", "1", f"{round(p_corr_3, 3)}"],
    [str(valid_cases_3), "", ""]
]
st.table(pd.DataFrame(chi_data_3, index=["Pearson Chi-Square", "Likelihood Ratio", "Linear-by-Linear Association", "N of Valid Cases"], columns=["Value", "df", "Asymp. Sig. (2-sided)"]))

# D. Hypothesis & Risk Summary 1.4
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
            P-Value    : {round(p_3, 4)}<br>
            Chi-Square : {round(chi2_3, 3)}<br>
            df         : {dof_3}
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"**Odds Ratio (Risk Estimate):** `{round(or_3, 3)}`")

with cr2_3:
    if is_sig_3:
        interp_txt_3 = f"Terdapat bukti statistik yang sah bahwa arus masuk modal (Investasi PMDN) secara langsung dan sistematis mendorong ekskalasi deforestasi di wilayah Sulawesi (OR: {round(or_3, 3)}). Investasi ini bukanlah katalisator ekonomi hijau, melainkan injeksi modal untuk ekstraksi lahan."
    else:
        interp_txt_3 = f"Secara statistik agregat mungkin belum terlihat korelasi linier di tahun yang persis sama. Hal ini menyingkap anomali bahwa investasi bernilai triliunan kerap ditahan untuk birokrasi awal, sementara pembabatan hutan fisiknya baru meledak secara sporadis di tahun-tahun berikutnya (<i>lagging effect</i>)."
    
    st.markdown(f"""
    <div style="background:#FFFFFF; padding:14px; border-radius:10px; border-left:5px solid {ord_col_3}; height: 100%;">
        <b>Interpretasi Kausalitas:</b><br><br>
        {interp_txt_3}
    </div>
    """, unsafe_allow_html=True)

# --- E. Executive Summary of All Combinations 1.4 ---
st.markdown("---")
st.markdown("### Ringkasan Eksekutif Seluruh Skenario Crosstab")
st.markdown("Tabel di bawah ini merangkum hasil pengujian statistik (Chi-Square) untuk semua kemungkinan kombinasi indikator antara Realisasi Investasi PMDN dan Dampak Ekologis pada panel data.")

summary_data_3 = []
for k_x, v_x in x_options_3.items():
    for k_y, v_y in y_options_3.items():
        med_x = df_panel_1_3[k_x].median()
        thresh_x = med_x if med_x > 0 else 0
        med_y = df_panel_1_3[k_y].median()
        
        lbl_x_h = f"Tinggi (>{int(thresh_x):,})"
        lbl_x_l = f"Rendah (≤{int(thresh_x):,})"
        lbl_y_h = f"Tinggi (≥{int(med_y):,})"
        lbl_y_l = f"Rendah (<{int(med_y):,})"
        
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
            "Chi-Square": f"{round(c2_val, 3)}",
            "P-Value": f"{round(pv_val, 3)}",
            "Odds Ratio": f"{round(or_v, 2)}",
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

# ═════════════════════════════════════════════════════════════
# 1.5 PELABUHAN EKSPOR NIKEL
st.markdown("<br><hr style='border: 1px dashed #333;'><br>", unsafe_allow_html=True)
st.subheader("1.5 Pelabuhan Ekspor: Ke Mana Nikel Sulawesi Dikirim?")

st.markdown('<span style="background:#4A148C;color:#E1BEE7;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: Open Source Intelligence (OSINT)</span>', unsafe_allow_html=True)
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

with st.expander("ℹ️ Metodologi: Open Source Intelligence (OSINT)"):
    st.markdown("""
    **Metode Analisis:** Kurasi & Validasi Silang (OSINT) dengan mencocokkan data citra satelit, dokumen lingkungan, dan laporan kargo.
    """)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
Ekspansi nikel di Sulawesi tidak berhenti pada izin dan pabrik smelter. Di setiap lokasi industri nikel besar, berdiri **pelabuhan atau dermaga** yang menghubungkan pabrik langsung ke kapal-kapal pengangkut menuju China dan pasar global. Dari 6 lokasi utama yang ditelusuri, **seluruhnya terbukti memiliki** pelabuhan atau dermaga ekspor, dan **4 dari 6** mendapat label Proyek Strategis Nasional (PSN) dari pemerintah.
""")

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

import pandas as pd
import os

@st.cache_data
def load_logistik_simpul():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    return pd.read_csv(os.path.join(base_dir, 'data', 'processed', 'sulawesi_logistik_simpul_nikel.csv'))

df_logistik = load_logistik_simpul()

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div style="background-color: #FFFFFF; padding: 20px; border-radius: 10px; border: 1px solid #333;">
        <div style="color: #A0AEC0; font-size: 0.85rem; font-weight: 600; margin-bottom: 10px; text-transform: uppercase; text-align: center;">Pelabuhan Nikel Terkonfirmasi</div>
        <div style="color: #48BB78; font-size: 2.5rem; font-weight: bold; text-align: center; margin-bottom: 15px;">6</div>
        <div style="color: #A0AEC0; font-size: 0.85rem; margin-bottom: 20px; text-align: left;">Seluruh lokasi industri nikel besar di Sulawesi terbukti memiliki pelabuhan atau dermaga ekspor.</div>
        <div style="color: #718096; font-size: 0.75rem; border-top: 1px solid #333; padding-top: 10px;">Sumber: Situs perusahaan, dokumen pemerintah, media (25 sumber)<br>File: sulawesi_logistik_simpul_nikel.csv</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div style="background-color: #FFFFFF; padding: 20px; border-radius: 10px; border: 1px solid #333;">
        <div style="color: #A0AEC0; font-size: 0.85rem; font-weight: 600; margin-bottom: 10px; text-transform: uppercase; text-align: center;">Berlabel Proyek Strategis Nasional</div>
        <div style="color: #ECC94B; font-size: 2.5rem; font-weight: bold; text-align: center; margin-bottom: 15px;">4 <span style="font-size: 1.2rem; color: #718096;">/ 6</span></div>
        <div style="color: #A0AEC0; font-size: 0.85rem; margin-bottom: 20px; text-align: left;">Label PSN mempercepat perizinan dan memudahkan pembebasan lahan warga sekitar.</div>
        <div style="color: #718096; font-size: 0.75rem; border-top: 1px solid #333; padding-top: 10px;">Sumber: KPPIP, Perpres 58/2017, Perpres 12/2025</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div style="background-color: #FFFFFF; padding: 20px; border-radius: 10px; border: 1px solid #333;">
        <div style="color: #A0AEC0; font-size: 0.85rem; font-weight: 600; margin-bottom: 10px; text-transform: uppercase; text-align: center;">Pelabuhan Terbesar</div>
        <div style="color: #63B3ED; font-size: 2.5rem; font-weight: bold; text-align: center; margin-bottom: 15px;">50.000 <span style="font-size: 1.2rem; color: #718096;">ton</span></div>
        <div style="color: #A0AEC0; font-size: 0.85rem; margin-bottom: 20px; text-align: left;">GNI Petasia memiliki pelabuhan yang mampu menampung kapal pengangkut berkapasitas hingga 50.000 ton.</div>
        <div style="color: #718096; font-size: 0.75rem; border-top: 1px solid #333; padding-top: 10px;">Sumber: gunbusternickelindustry.com</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

with st.expander("Lihat Data Mentah: Fasilitas Pelabuhan Ekspor (Card 1)"):
    st.dataframe(df_logistik[['node_label', 'port_facility', 'export_channel']], use_container_width=True, hide_index=True)
    st.caption("📁 **Sumber File:** `data/processed/sulawesi_logistik_simpul_nikel.csv` - Ekstraksi data OSINT fasilitas pelabuhan.")

with st.expander("Lihat Data Mentah: Status PSN (Card 2)"):
    st.dataframe(df_logistik[['node_label', 'psn_status', 'psn_detail']], use_container_width=True, hide_index=True)
    st.caption("📁 **Sumber File:** `data/processed/sulawesi_logistik_simpul_nikel.csv` - Ekstraksi data status Proyek Strategis Nasional.")

with st.expander("Lihat Data Mentah: Detail Kapasitas Pelabuhan (Card 3)"):
    st.dataframe(df_logistik[['node_label', 'port_detail']], use_container_width=True, hide_index=True)
    st.caption("📁 **Sumber File:** `data/processed/sulawesi_logistik_simpul_nikel.csv` - Ekstraksi spesifikasi teknis dan kapasitas pelabuhan.")

st.markdown("<br><hr style='border: 1px dashed #333;'><br>", unsafe_allow_html=True)
st.subheader("1.6 Peta Jalur Distribusi Logistik Nikel Sulawesi")

st.markdown('<span style="background:#4A148C;color:#E1BEE7;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: Spatial Logistic Mapping (Analisis Spasial Ekstraktif)</span>', unsafe_allow_html=True)
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

with st.expander("ℹ️ Metodologi: Pemetaan Spasial Rantai Pasok Maritim"):
    st.markdown("""
    **Metode Analisis:** Pemetaan Kausalitas (Spasial) untuk membedah asimetri penguasaan ruang antara origin (sumber ekstraksi) dan destination (pusat industrialisasi). Garis diplot menggunakan rute untuk merepresentasikan jarak tempuh kapal logistik di permukaan bumi.
    """)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

import plotly.graph_objects as go
import math

def generate_curve(lon1, lat1, lon2, lat2, offset=0.1, n_points=50):
    # Titik tengah
    mid_lon = (lon1 + lon2) / 2
    mid_lat = (lat1 + lat2) / 2
    
    # Jarak
    dx = lon2 - lon1
    dy = lat2 - lat1
    dist = math.sqrt(dx**2 + dy**2)
    
    # Vektor tegak lurus
    px = -dy / dist
    py = dx / dist
    
    ctrl_lon = mid_lon + px * dist * offset
    ctrl_lat = mid_lat + py * dist * offset
    
    # Bezier curve
    lons, lats = [], []
    for i in range(n_points + 1):
        t = i / n_points
        lon = (1-t)**2 * lon1 + 2*(1-t)*t * ctrl_lon + t**2 * lon2
        lat = (1-t)**2 * lat1 + 2*(1-t)*t * ctrl_lat + t**2 * lat2
        lons.append(lon)
        lats.append(lat)
    return lons, lats

# MAP_ROUTES: Nama, Lon Origin, Lat Origin, Lon Dest, Lat Dest, Color, Curve Offset
MAP_ROUTES = [
    ("IMIP",         122.15, -2.82, 113.8, 22.8,  "rgb(230, 25, 25)",  -0.12),
    ("GNI",          121.32, -1.91, 113.8, 22.8,  "rgb(255, 140, 0)",  -0.04),
    ("VDNI",         122.42, -3.83, 113.8, 22.8,  "rgb(0, 112, 220)",   0.04),
    ("OSS",          122.48, -3.80, 113.8, 22.8,  "rgb(0, 190, 220)",   0.12),
    ("ANTAM",        121.60, -4.18, 135.0, 35.0,  "rgb(0, 180, 80)",   -0.08),
    ("PT Vale",      121.34, -2.56, 135.0, 35.0,  "rgb(180, 0, 200)",   0.08),
]

fig_map = go.Figure()

# Base map layout (Peta di-width-kan maksimal dengan rasio ekstrim agar full screen)
fig_map.update_geos(
    projection_type="equirectangular",
    showcountries=True, countrycolor="#B0BEC5",
    showcoastlines=True, coastlinecolor="#B0BEC5",
    showland=True, landcolor="#FFFFFF",
    showocean=True, oceancolor="#EAF6FF",
    lonaxis_range=[40, 170], # 130 derajat lebar
    lataxis_range=[-15, 35], # 50 derajat tinggi
    bgcolor='white'
)

hover_details = {
    "IMIP": "<b>IMIP (Morowali)</b><br>Pelabuhan: Seaport + Jetties Bulk Carrier<br>Komoditas: NPI/Feronikel",
    "GNI": "<b>GNI (Morowali Utara)</b><br>Pelabuhan: 2x50.000 DWT Vessel<br>Komoditas: NPI",
    "VDNI": "<b>VDNI (Konawe)</b><br>Pelabuhan: Kapasitas 50.000 Ton<br>Komoditas: Feronikel & Stainless Steel",
    "OSS": "<b>OSS (Konawe)</b><br>Pelabuhan: Berbagi Jetty Porara<br>Komoditas: Stainless Steel",
    "ANTAM": "<b>ANTAM (Kolaka)</b><br>Pelabuhan: Jetty 12.000 DWT, Conveyor 4km<br>Komoditas: Feronikel",
    "PT Vale": "<b>PT Vale (Luwu Timur)</b><br>Pelabuhan: Pelabuhan Balantang Malili<br>Komoditas: Nickel in Matte"
}

# Add curved lines for routes
for name, lon1, lat1, lon2, lat2, color, offset in MAP_ROUTES:
    curve_lons, curve_lats = generate_curve(lon1, lat1, lon2, lat2, offset=offset)
    dest_name = "Jepang/Korea" if "Jepang" in name or "Korea" in name or lat2 > 30 else "China"
    detail = hover_details.get(name, "")
    hover_text = [f"{detail}<br>Rute Logistik: ➔ {dest_name}"] * len(curve_lons)
    
    fig_map.add_trace(
        go.Scattergeo(
            lon=curve_lons,
            lat=curve_lats,
            mode='lines',
            line=dict(width=2.5, color=color),
            name=name,
            text=hover_text,
            hoverinfo='text'
        )
    )

# Add Origin points (Tanpa text label agar tidak tumpang tindih)
for name, lon1, lat1, lon2, lat2, color, offset in MAP_ROUTES:
    detail = hover_details.get(name, "")
    hover_text = f"{detail}"
    
    fig_map.add_trace(
        go.Scattergeo(
            lon=[lon1],
            lat=[lat1],
            mode='markers',
            marker=dict(size=6, color=color, line=dict(width=1, color='black')),
            name=name,
            text=[hover_text],
            hoverinfo='text',
            showlegend=False
        )
    )

# Add Destination Points
fig_map.add_trace(
    go.Scattergeo(
        lon=[113.8, 135.0],
        lat=[22.8, 35.0],
        mode='markers+text',
        marker=dict(size=8, color="#555"),
        text=["China (Pasar Utama)", "Jepang/Korea"],
        textposition="top left",
        textfont=dict(color="#111", size=11, family="Arial Black"),
        showlegend=False,
        hoverinfo='none'
    )
)

fig_map.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0},
    paper_bgcolor='white',
    plot_bgcolor='white',
    height=450,
    legend=dict(
        orientation="h",
        yanchor="bottom", y=-0.1,
        xanchor="center", x=0.5,
        font=dict(color="#ECEFF1", size=12)
    )
)

st.plotly_chart(fig_map, use_container_width=True, config={'displayModeBar': False})

# Red Box Ketergantungan
st.markdown("""
<div style="background:#FFFFFF; padding:20px; border-radius:10px; border-left:5px solid #D32F2F; margin-top: 20px;">
    <b style="color:#FF5252; font-size:1.1em;">Anatomi Rantai Pasok Logistik Maritim</b><br><br>
    Peta rute logistik maritim mengilustrasikan alur distribusi produk olahan nikel dari kawasan industri di Sulawesi:
    <ul style="margin-top: 10px; line-height: 1.6;">
        <li><b>Orientasi Ekspor:</b> Kawasan industri utama (IMIP, GNI, VDNI/OSS) yang berstatus Proyek Strategis Nasional (PSN) mengalirkan produk olahan (NPI, Feronikel, Matte) ke sentra-sentra industri manufaktur di pasar internasional.</li>
        <li><b>Integrasi Rantai Pasok:</b> Mayoritas rute pengapalan terhubung langsung dengan pelabuhan ekspor tujuan, yang mengindikasikan posisi kawasan pemurnian di Sulawesi sebagai pemasok bahan baku setengah jadi pada rantai pasok global.</li>
        <li><b>Dinamika Rute Maritim:</b> Peta rute mencerminkan diversifikasi pasar ekspor, di mana beberapa fasilitas terhubung dengan pasar Asia Timur (Jepang dan Korea Selatan), sementara fasilitas baru terintegrasi dengan jaringan logistik utama kawasan Asia.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
with st.expander("Lihat Data Mentah: Jalur Distribusi Logistik Nikel Sulawesi", expanded=False):
    df_logistik_map = pd.DataFrame(MAP_ROUTES, columns=["Nama Smelter", "Lon Origin", "Lat Origin", "Lon Dest", "Lat Dest", "Color", "Offset"])
    st.dataframe(df_logistik_map[["Nama Smelter", "Lon Origin", "Lat Origin", "Lon Dest", "Lat Dest"]], use_container_width=True, hide_index=True)
    st.caption("ℹ️ **Sumber File:** data/processed/sulawesi_logistik_simpul_nikel.csv - Pemetaan koordinat smelter dan pelabuhan tujuan akhir (agregasi spasial).")
