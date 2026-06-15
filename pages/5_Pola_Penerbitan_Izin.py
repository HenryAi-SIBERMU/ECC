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
st.markdown('<div class="org-badge">Modul Kajian 4.5</div>', unsafe_allow_html=True)
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
st.markdown('<span style="background:#5C2B6A;color:#E1BEE7;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: Dual-Axis Time-Series Overlay (Plotly)</span>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

from plotly.subplots import make_subplots

# Data Prep for Timeline Mapping
df_izin_agg = df_izin.groupby('Tahun')['Jumlah_Izin_Baru'].sum().reset_index()
df_gfw_agg = df_gfw.groupby('Tahun')['Total_Deforestasi_Ha'].sum().reset_index()

# Merge and pad missing years up to 2024
df_timeline = pd.merge(df_izin_agg, df_gfw_agg, on='Tahun', how='outer').fillna(0).sort_values('Tahun')

# Plotly Dual-Axis Chart
fig_timeline = make_subplots(specs=[[{"secondary_y": True}]])
fig_timeline.add_trace(
    go.Bar(x=df_timeline['Tahun'], y=df_timeline['Jumlah_Izin_Baru'], name="Total Izin Baru (Kiri)", marker_color='#F57C00', opacity=0.85),
    secondary_y=False,
)
fig_timeline.add_trace(
    go.Scatter(x=df_timeline['Tahun'], y=df_timeline['Total_Deforestasi_Ha'], name="Deforestasi Alam (Kanan)", line=dict(color='#E53935', width=4), mode='lines+markers', marker=dict(size=8, color='#B71C1C')),
    secondary_y=True,
)
fig_timeline.update_layout(
    title="Sinkronisasi Absolut: Obral Izin vs Kehancuran Ekologis (2014-2024)",
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
    legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5),
    margin=dict(l=0, r=0, t=80, b=40),
    hovermode="x unified"
)
fig_timeline.update_xaxes(showgrid=False, tickmode='linear', dtick=1, title_text="Tahun")
fig_timeline.update_yaxes(title_text="Jumlah Penerbitan Izin (IUP)", showgrid=True, gridcolor='rgba(255,255,255,0.1)', secondary_y=False)
fig_timeline.update_yaxes(title_text="Laju Deforestasi (Hektar)", showgrid=False, secondary_y=True)

st.plotly_chart(fig_timeline, use_container_width=True)

# Interpretation Box
st.markdown("""
<div style="background:#1E1E1E; padding:20px; border-radius:10px; border-left:5px solid #FF5722; margin-bottom: 25px;">
    <b style="color:#FF5722; font-size:1.1rem;">Pembedahan Realitas Ekologis (Governance Failure):</b><br><br>
    <div style="color: #E0E0E0; font-size: 0.95rem; line-height: 1.6;">
    Data deret waktu (<i>time-series</i>) di atas menyajikan kronik forensik yang memalukan bagi tata kelola lingkungan hidup di semenanjung Sulawesi. Kurva merah menyala yang merepresentasikan luasan deforestasi berfluktuasi secara masif, dengan rekor kehancuran menembus <b>333 ribu hektar</b> pada tahun 2015 dan kembali melonjak drastis di atas <b>255 ribu hektar</b> pada tahun 2023. Secara logika keberlanjutan dan muruah instrumen D3TLH, momentum di mana daya dukung ekologis sedang ambruk seharusnya memicu mekanisme moratorium perizinan secara otomatis.<br><br>
    Namun, batang-batang oranye yang menunjukkan jumlah obral izin usaha pertambangan (IUP) baru justru mengkhianati logika penyelamatan tersebut. Alih-alih mengerem laju ekspansi saat hutan Sulawesi sedang kritis berdarah-darah, negara justru <b>mempercepat laju perizinan secara membabi buta</b>. Puncak pengabaian ini terjadi pada rentang 2022 hingga 2024, di mana grafik batang oranye meroket secara eksponensial tak terkendali. Tepat ketika grafik merah (deforestasi) kembali menanjak ekstrem di tahun 2023, pemerintah justru mengesahkan <b>149 izin tambang baru</b>, dan melanjutkannya dengan rekor gila <b>194 izin baru di tahun 2024</b>.<br><br>
    Ketidakpedulian absolut antara kondisi krisis ruang hidup (sumbu Y kanan) dengan ambisi perampasan ruang konsesi (sumbu Y kiri) ini merupakan bukti empiris yang tidak terbantahkan: instrumen daya dukung lingkungan (D3TLH) telah sepenuhnya mati, lumpuh, dan dibajak secara formal oleh syahwat ekspansi hilirisasi oligarki ekstraktif.
    </div>
</div>
""", unsafe_allow_html=True)

with st.expander("Lihat Data Mentah: Sinkronisasi Waktu", expanded=False):
    st.dataframe(df_timeline, use_container_width=True, hide_index=True)
    st.caption("📁 **Sumber File:** Agregasi dari `sulawesi_izin_baru_per_tahun.csv` (Minerbaone) & `sulawesi_gfw_master_1_dekade_2014_2023.csv` (GFW). Catatan: Data GFW 2024 bernilai 0 karena jeda rilis tahunan dari satelit penginderaan.")

st.markdown("---")

st.subheader("5.2 Kegagalan Tata Kelola: Izin Terbit di Zona Darurat Ekologis")
st.info("⚠️ Placeholder: Crosstab Analysis (SPSS Style) untuk membuktikan signifikansi pengabaian kondisi ekologis terhadap keputusan penerbitan izin.")

st.markdown("<br><br>", unsafe_allow_html=True)
