import streamlit as st
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.components.sidebar import render_sidebar
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import scipy.stats as stats
import textwrap

st.set_page_config(page_title="CELIOS ECC", layout="wide")
render_sidebar()

# ── Styles (Sesuai Pedoman UI/UX CELIOS) ──
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

# ---------------------------------------------------------
# DATA PREPARATION (PURE DATA-DRIVEN)
# ---------------------------------------------------------
@st.cache_data
def load_izin_data():
    return pd.read_csv('data/processed/sulawesi_izin_baru_per_tahun.csv')

@st.cache_data
def load_gfw_data():
    return pd.read_csv('data/processed/sulawesi_gfw_master_1_dekade_2014_2023.csv')

df_izin = load_izin_data()
df_gfw = load_gfw_data()

# Kalkulasi Metrik Agregat
total_izin = int(df_izin['Jumlah_Izin_Baru'].sum())
total_luas_konsesi = float(df_izin['Total_Luas_Konsesi_Baru_Ha'].sum())
total_deforestasi = float(df_gfw['Total_Deforestasi_Ha'].sum())

# Metrik tahun puncak penerbitan izin
df_izin_thn = df_izin.groupby('Tahun')['Jumlah_Izin_Baru'].sum().reset_index()
tahun_puncak = int(df_izin_thn.loc[df_izin_thn['Jumlah_Izin_Baru'].idxmax(), 'Tahun']) if not df_izin_thn.empty else 0
izin_puncak = int(df_izin_thn['Jumlah_Izin_Baru'].max()) if not df_izin_thn.empty else 0

# Kalkulasi Metrik Agregat Baru (Bento Cards - Insight Kritis)
df_panel_bento = pd.merge(df_gfw, df_izin, on=['Provinsi', 'Tahun'], how='left').fillna({'Jumlah_Izin_Baru': 0})
med_def = df_panel_bento['Total_Deforestasi_Ha'].median()
df_panel_bento['is_kritis'] = df_panel_bento['Total_Deforestasi_Ha'] > med_def

izin_kritis = int(df_panel_bento[df_panel_bento['is_kritis']]['Jumlah_Izin_Baru'].sum())
izin_total = int(df_panel_bento['Jumlah_Izin_Baru'].sum())
pct_kritis = (izin_kritis / izin_total * 100) if izin_total > 0 else 0

kritis_prov = df_panel_bento[df_panel_bento['is_kritis']].groupby('Provinsi')['Jumlah_Izin_Baru'].sum().reset_index()
top_prov_kritis = kritis_prov.loc[kritis_prov['Jumlah_Izin_Baru'].idxmax()]
nama_prov_kritis = top_prov_kritis['Provinsi']
jumlah_prov_kritis = int(top_prov_kritis['Jumlah_Izin_Baru'])

izin_pra_2020 = int(df_izin[df_izin['Tahun'] < 2020]['Jumlah_Izin_Baru'].sum())
izin_pasca_2020 = int(df_izin[df_izin['Tahun'] >= 2020]['Jumlah_Izin_Baru'].sum())
rasio_akselerasi = (izin_pasca_2020 / izin_pra_2020) if izin_pra_2020 > 0 else 0

# ---------------------------------------------------------
# HERO SECTION (EXECUTIVE SUMMARY)
# ---------------------------------------------------------
st.markdown('<div class="org-badge">CELIOS — Center of Economic and Law Studies</div>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">Pola Penerbitan Izin di Zona Kritis Ekologis</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Evaluasi terhadap kegagalan instrumen tata kelola lingkungan dalam meredam perizinan tambang di wilayah yang telah melampaui daya dukung ekologis.</p>', unsafe_allow_html=True)

with st.expander("🔍 Metodologi Pendekatan", expanded=False):
    st.markdown("""
    **Kerangka Logis (Alur Kausalitas):**
    Bagian ini dirancang untuk menjawab sub-pertanyaan kritis dalam studi D3TLH: *"Apakah izin baru tetap diterbitkan ketika tekanan ekologis sudah tinggi?"*
    
    1. **Variabel Dependen (Y):** Jumlah penerbitan izin tambang baru per tahun.
    2. **Variabel Konteks (X):** Status kritis ekologis (diukur dari laju deforestasi dan kerusakan eksisting).
    3. **Pendekatan Metodologis:** *Timeline Mapping* dan *Crosstabulation* untuk melihat tumpang tindih (*overlay*) temporal antara memburuknya kualitas lingkungan dengan grafik penerbitan izin.
    
    **Tujuan:**
    Membuktikan secara empiris terjadinya kegagalan tata kelola (governance failure) di mana instrumen Daya Dukung dan Daya Tampung Lingkungan Hidup (D3TLH) tidak bersifat mengikat (non-mandatory) dan mudah diabaikan demi melancarkan investasi.
    """)

# Hero Statement
st.markdown(f"""
Secara institusional, dokumen tata ruang dan instrumen lingkungan hidup semestinya beroperasi sebagai 'rem darurat' negara untuk menolak izin investasi baru di bentang alam yang sudah melampaui kapasitas pemulihannya. Namun, penelusuran data spasial dan waktu di semenanjung Sulawesi membongkar skandal tata kelola yang memilukan. Selama satu dekade terakhir, saat total deforestasi telah merobek **{total_deforestasi:,.1f} hektar** tutupan hutan tersisa, negara justru terus mengobral **{total_izin:,} izin tambang baru** yang merampas tambahan **{total_luas_konsesi:,.1f} hektar** ruang daratan. Ironisnya, puncak penerbitan izin tertinggi meledak pada tahun **{tahun_puncak}** ({izin_puncak} izin), tepat pada momentum di mana berbagai wilayah telah memancarkan sinyal darurat polusi dan kebangkrutan ekologis. Ini membuktikan bahwa D3TLH telah dilumpuhkan menjadi sekadar ornamen administratif semata yang tunduk pada syahwat oligarki ekstraktif.
""")

st.markdown("<br>", unsafe_allow_html=True)

# Bento Cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">TINGKAT PENGABAIAN EKOLOGIS</div>
            <div class="metric-value" style="color: #E53935;">{pct_kritis:.1f}% <span style="font-size:1rem;color:#777;">({izin_kritis} IUP)</span></div>
            <div class="metric-desc">Mayoritas mutlak izin baru justru diobral secara sengaja pada tahun-tahun di mana laju deforestasi provinsi tersebut sedang berada di zona kritis (di atas rata-rata).</div>
        </div>
        <div class="metric-source">Sumber: Data Panel (ESDM & GFW)<br>File: sulawesi_izin_baru_per_tahun.csv</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">ZONA BEBAS REM DARURAT</div>
            <div class="metric-value" style="color: #FFB74D;">{nama_prov_kritis} <span style="font-size:1rem;color:#777;">({jumlah_prov_kritis} IUP)</span></div>
            <div class="metric-desc">Provinsi dengan rekor penerbitan izin tertinggi tepat pada saat daya dukung lingkungan (tutupan hutan) mereka sedang hancur lebur tanpa mitigasi.</div>
        </div>
        <div class="metric-source">Sumber: Data Panel (ESDM & GFW)<br>File: sulawesi_izin_baru_per_tahun.csv</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">AKSELERASI IZIN PASCA-2020</div>
            <div class="metric-value" style="color: #4DB6AC;">{rasio_akselerasi:.1f}x <span style="font-size:1rem;color:#777;">Lipat</span></div>
            <div class="metric-desc">Ledakan drastis penerbitan izin baru di era pasca-2020 dibandingkan periode sebelumnya, mengonfirmasi jebol dan diabaikannya instrumen D3TLH.</div>
        </div>
        <div class="metric-source">Sumber: Kementerian ESDM (Minerbaone)<br>File: sulawesi_izin_baru_per_tahun.csv</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><hr style='border: 1px dashed #333;'><br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# PLACEHOLDERS
# ---------------------------------------------------------

st.subheader("5.1 Fakta Penyebab: Sinkronisasi Waktu (Timeline Mapping)")
st.markdown('<span style="background:#5C2B6A;color:#E1BEE7;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: Gantt Chart Timeline (Plotly Express)</span>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

import plotly.graph_objects as go

# Data Prep for Time-Series Dual-Axis Line Chart
df_izin_thn = df_izin.groupby('Tahun')['Jumlah_Izin_Baru'].sum().reset_index()
df_gfw_thn = df_gfw.groupby('Tahun')['Total_Deforestasi_Ha'].sum().reset_index()
df_timeline = pd.merge(df_gfw_thn, df_izin_thn, on='Tahun', how='outer').fillna(0).sort_values('Tahun')
df_timeline = df_timeline[df_timeline['Tahun'] <= 2023] # Filter out 2024 karena data GFW mentok di 2023

from plotly.subplots import make_subplots

st.markdown("""
Visualisasi di bawah ini menelanjangi kegagalan fungsi instrumen daya dukung lingkungan (D3TLH). Batang merah merepresentasikan luas deforestasi yang seharusnya menjadi "rem darurat" bagi pemerintah. Namun, perhatikan garis kuning yang merepresentasikan penerbitan izin tambang baru.

Alih-alih menurun saat deforestasi memburuk, kurva izin (garis kuning) justru ikut melesat tajam dan mencapai puncaknya bertepatan dengan tingginya kerusakan hutan (batang merah). Ini menandakan bahwa instrumen tata ruang justru hanya menjadi stempel legalisasi untuk mengobral Izin Tambang Baru (IUP) di tengah darurat lingkungan.
""")

# Render Combo Chart (Bar + Line) Dual Axis
fig_timeline = make_subplots(specs=[[{'secondary_y': True}]])

# 1. Bar Chart: Deforestasi (Sumbu Y Kiri)
fig_timeline.add_trace(
    go.Bar(
        x=df_timeline['Tahun'], 
        y=df_timeline['Total_Deforestasi_Ha'], 
        name='Total Deforestasi (Hektar)', 
        marker_color='rgba(231, 76, 60, 0.7)', # Merah transparan
        marker_line_color='#C0392B',
        marker_line_width=1.5,
        hovertemplate="<b>Tahun %{x}</b><br>Deforestasi: %{y:,.0f} Ha<extra></extra>"
    ),
    secondary_y=False,
)

# 2. Line Chart: Izin Baru (Sumbu Y Kanan)
fig_timeline.add_trace(
    go.Scatter(
        x=df_timeline['Tahun'], 
        y=df_timeline['Jumlah_Izin_Baru'], 
        name='Total Penerbitan Izin (IUP)', 
        mode='lines+markers+text',
        text=df_timeline['Jumlah_Izin_Baru'].astype(int).astype(str),
        textposition='top center',
        textfont=dict(color='#F1C40F', size=12, weight='bold'),
        line=dict(color='#F1C40F', width=3),
        marker=dict(symbol='circle', size=10, color='#F1C40F', line=dict(color='#1E1E1E', width=2)),
        hovertemplate="<b>Tahun %{x}</b><br>Izin Baru: %{y} IUP<extra></extra>"
    ),
    secondary_y=True,
)

fig_timeline.update_layout(
    title='Tren Eskalasi Bersamaan: Kerusakan Hutan (Batang) vs Penerbitan Izin (Garis)',
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    hovermode='x unified',
    height=500,
    margin=dict(l=0, r=20, t=60, b=40),
    xaxis=dict(
        tickformat="%Y",
        dtick="M12",
        showgrid=False,
    ),
    legend=dict(
        orientation="h", 
        yanchor="bottom", 
        y=1.05, 
        xanchor="center", 
        x=0.5,
        title=""
    )
)

fig_timeline.update_yaxes(title_text='Deforestasi (Hektar)', secondary_y=False, showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='#E74C3C')
fig_timeline.update_yaxes(title_text='Jumlah Izin Baru (IUP)', secondary_y=True, showgrid=False, color='#F1C40F')

st.plotly_chart(fig_timeline, use_container_width=True)

# Interpretation Box Ringkas (Sesuai gaya Page 4)
st.markdown("""
<div style="background:#1E1E1E; padding:15px 20px; border-radius:8px; border-left:4px solid #F57C00; margin-top: 10px; margin-bottom: 25px;">
    <span style="color: #E0E0E0; font-size: 0.95rem;">
        <b style="color:#F57C00;">Interpretasi Governance Failure:</b> Alih-alih membunyikan "rem darurat", data tren historis mengonfirmasi bahwa instrumen D3TLH hanya berakhir sebagai formalitas administratif yang secara sistematis diabaikan demi memfasilitasi ekspansi oligarki ekstraktif.
    </span>
</div>
""", unsafe_allow_html=True)

with st.expander("Lihat Data Mentah: Agregasi Waktu Historis", expanded=False):
    # Format data untuk tabel
    df_tabel = df_timeline.copy()
    df_tabel['Tahun'] = df_tabel['Tahun'].astype(int).astype(str)
    df_tabel['Total_Deforestasi_Ha'] = df_tabel['Total_Deforestasi_Ha'].apply(lambda x: f"{x:,.0f}")
    df_tabel['Jumlah_Izin_Baru'] = df_tabel['Jumlah_Izin_Baru'].astype(int)
    
    st.dataframe(df_tabel, use_container_width=True, hide_index=True)
    st.caption("📁 **Sumber File:** Agregasi dari `sulawesi_izin_baru_per_tahun.csv` (Minerbaone) & `sulawesi_gfw_master_1_dekade_2014_2023.csv` (GFW).")

st.markdown("---")

st.subheader("5.2 Kegagalan Tata Kelola: Izin Terbit di Zona Darurat Ekologis")
st.info("⚠️ Placeholder: Crosstab Analysis (SPSS Style) untuk membuktikan signifikansi pengabaian kondisi ekologis terhadap keputusan penerbitan izin.")

st.markdown("<br><br>", unsafe_allow_html=True)
