import streamlit as st
import os, sys
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.components.sidebar import render_sidebar

st.set_page_config(page_title="CELIOS ECC - Audit Forensik D3TLH", layout="wide")
render_sidebar()

# ── Styles (Sesuai Pedoman UI/UX CELIOS) ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

* { font-family: 'Inter', sans-serif; }

.main-title {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #E53935, #EF5350, #FFCDD2);
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
    background: linear-gradient(135deg, #B71C1C, #D32F2F);
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
.verdict-box {
    background: #1E1E1E;
    padding: 20px;
    border-radius: 8px;
    border-left: 5px solid #F44336;
    margin-bottom: 30px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 1. LOAD DATASETS
# ---------------------------------------------------------
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "processed")

@st.cache_data
def load_data():
    # 1. ISPA (Kesehatan)
    df_kesehatan = pd.DataFrame()
    path_kes = os.path.join(DATA_DIR, "sulawesi_kesehatan_detail_2014_2024.csv")
    if os.path.exists(path_kes):
        df_kesehatan = pd.read_csv(path_kes)
        
    # 2. IKA (Kualitas Air)
    df_ika = pd.DataFrame()
    path_ika = os.path.join(DATA_DIR, "sulawesi_ika_2016_2024.csv")
    if os.path.exists(path_ika):
        df_ika = pd.read_csv(path_ika)
        
    # 3. Bencana (BNPB)
    df_bencana = pd.DataFrame()
    path_bencana = os.path.join(DATA_DIR, "sulawesi_bencana_bnpb_2014_2024.csv")
    if os.path.exists(path_bencana):
        df_bencana = pd.read_csv(path_bencana)
        
    # 4. Konflik Agraria
    df_konflik = pd.DataFrame()
    path_konflik = os.path.join(DATA_DIR, "sulawesi_konflik_agraria_tanahkita.csv")
    if os.path.exists(path_konflik):
        df_konflik = pd.read_csv(path_konflik)
        
    return df_kesehatan, df_ika, df_bencana, df_konflik

df_kes, df_ika, df_bencana, df_konflik = load_data()

# ---------------------------------------------------------
# 2. CALCULATE AGGREGATES FOR BENTO CARDS
# ---------------------------------------------------------
tot_ispa = 0
if not df_kes.empty:
    df_ispa = df_kes[df_kes['indikator'].str.contains('ISPA', case=False, na=False)]
    tot_ispa = df_ispa['jumlah_kasus'].sum()

penurunan_ika_str = "N/A"
if not df_ika.empty:
    df_ika_filtered = df_ika[df_ika['Provinsi'].isin(['SULAWESI TENGAH', 'SULAWESI TENGGARA'])]
    if not df_ika_filtered.empty:
        # Rata-rata 2016 vs rata-rata 2024
        rata_2016 = df_ika_filtered['2016'].mean()
        rata_2024 = df_ika_filtered['2024'].mean()
        penurunan = rata_2016 - rata_2024
        penurunan_ika_str = f"{penurunan:.1f} Poin"

tot_bencana = 0
tot_korban = 0
if not df_bencana.empty:
    tot_bencana = df_bencana['jumlah_kejadian'].sum()
    tot_korban = df_bencana['korban_terdampak'].sum()

tot_konflik = 0
if not df_konflik.empty:
    tot_konflik = len(df_konflik)

# ── Header Halaman ──
st.markdown('<div class="org-badge">CELIOS — Center of Economic and Law Studies</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">Audit Forensik D3TLH: Mitos vs Realitas Lapangan</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Membongkar kesenjangan antara klaim ambang batas aman dalam AMDAL/D3TLH pemerintah versus data empiris penderitaan rakyat di lingkar tambang.</div>', unsafe_allow_html=True)

# ── Executive Summary (Verdict Box) ──
st.markdown("""
<div class="verdict-box">
    <h3 style="color: #EF5350; margin-top: 0;">Bukti Terbalik (Ex-Post Evaluation)</h3>
    <p style="color: #E0E0E0; font-size: 1.05rem; line-height: 1.6; margin-bottom: 0;">
        AMDAL dan D3TLH pemerintah diklaim sebagai alat "prediktif" pelindung lingkungan, dengan metodologi spasial "Jasa Ekosistem" yang buta terhadap nyawa manusia. Halaman ini adalah <b>Panggung Putusan</b> yang menggunakan data historis lintas sektoral (Kesehatan, Kebencanaan, Kualitas Air) sebagai bukti absolut bahwa daya dukung ekologis di sentra nikel <b>telah lama hancur</b>.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Bento Cards ──
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Ledakan Pasien ISPA</div>
            <div class="metric-value" style="color: #F44336;">{int(tot_ispa):,}</div>
            <div class="metric-desc">Total kasus ISPA tercatat. Fakta kegagalan perhitungan kualitas udara AMDAL.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Kehancuran Ekosistem Air</div>
            <div class="metric-value" style="color: #FF5252;">{penurunan_ika_str}</div>
            <div class="metric-desc">Rata-rata penurunan Indeks Kualitas Air di Sulteng & Sultra (2016-2024).</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Bencana Ekologis BNPB</div>
            <div class="metric-value" style="color: #FF9800;">{int(tot_bencana):,}</div>
            <div class="metric-desc">Kejadian banjir & longsor (2014-2023) dengan {int(tot_korban):,} korban jiwa/mengungsi.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Konflik Agraria & Lahan</div>
            <div class="metric-value" style="color: #00BCD4;">{tot_konflik} Kasus</div>
            <div class="metric-desc">Bukti nihilnya persetujuan warga (FPIC) yang dimanipulasi dalam sosialisasi AMDAL.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><hr style='border: 1px dashed #333;'><br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. SIDE-BY-SIDE FORENSIC COMPARISON
# ---------------------------------------------------------

# --- A. Kualitas Udara vs ISPA ---
st.markdown("### A. Mitos Baku Mutu Udara vs Realitas Ledakan ISPA")
st.markdown("<p style='color:#AAA;'>D3TLH dan AMDAL mengklaim polusi cerobong asap 'sesuai baku mutu teknis', namun grafik kunjungan Puskesmas membuktikan bahwa paru-paru warga menanggung beban yang tidak pernah dihitung.</p>", unsafe_allow_html=True)

if not df_kes.empty:
    df_ispa_plot = df_ispa.groupby(['tahun', 'provinsi'])['jumlah_kasus'].sum().reset_index()
    fig1 = px.line(df_ispa_plot, x='tahun', y='jumlah_kasus', color='provinsi', markers=True,
                   title="Eskalasi Kasus ISPA Tahunan di Sentra Nikel Sulawesi",
                   color_discrete_sequence=['#F44336', '#FF9800', '#2196F3', '#4CAF50', '#9C27B0'])
    fig1.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.warning("Data Kesehatan ISPA tidak tersedia.")

st.markdown("<br>", unsafe_allow_html=True)

# --- B. Mitos Daya Tampung Air vs Realitas IKA ---
st.markdown("### B. Mitos Daya Tampung Perairan vs Runtuhnya Indeks Kualitas Air")
st.markdown("<p style='color:#AAA;'>Dokumen lingkungan menjustifikasi izin pembuangan tailing ke sungai dan laut dengan dalih 'laut mampu mengencerkan limbah'. Data BPS menunjukkan bahwa sungai dan pesisir Sulawesi makin beracun setiap tahunnya.</p>", unsafe_allow_html=True)

if not df_ika.empty:
    df_ika_long = df_ika.melt(id_vars=['Provinsi'], var_name='Tahun', value_name='Nilai IKA')
    # Filter only numbers for Tahun
    df_ika_long = df_ika_long[df_ika_long['Tahun'].str.match(r'^\d{4}$')]
    fig2 = px.line(df_ika_long, x='Tahun', y='Nilai IKA', color='Provinsi', markers=True,
                   title="Tren Penurunan Indeks Kualitas Air (IKA) Berdasarkan Data BPS",
                   color_discrete_sequence=px.colors.qualitative.Pastel)
    fig2.add_hline(y=50, line_dash="dot", annotation_text="Batas Kritis", annotation_position="bottom right", line_color="red")
    fig2.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("Data IKA tidak tersedia.")

st.markdown("<br>", unsafe_allow_html=True)

# --- C. Mitos Deforestasi Wajar vs Bencana Banjir Bandang ---
st.markdown("### C. Izin Buka Kawasan Hutan vs Bencana Hidrometeorologi")
st.markdown("<p style='color:#AAA;'>AMDAL melegalkan penebangan hutan primer dengan syarat reklamasi yang tak pernah terwujud. Akibatnya, daya resap air hancur seketika, memicu ledakan frekuensi banjir bandang lumpur dan tanah longsor ke pemukiman hilir.</p>", unsafe_allow_html=True)

if not df_bencana.empty:
    fig3 = px.bar(df_bencana, x='tahun', y='jumlah_kejadian', color='jenis_bencana', facet_col='provinsi',
                  title="Lonjakan Frekuensi Banjir & Tanah Longsor (Data BNPB)",
                  color_discrete_map={"Banjir": "#2196F3", "Tanah Longsor": "#8D6E63"})
    fig3.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.warning("Data Bencana BNPB tidak tersedia.")

st.markdown("<br>", unsafe_allow_html=True)

# --- D. Kesimpulan Kebijakan (The Call to Action) ---
st.markdown("""
<div style="background: linear-gradient(135deg, #2E1515, #1E1E1E); padding:25px; border-radius:10px; border: 1px solid #444; border-left: 6px solid #E53935;">
    <h3 style="color: #E53935; margin-top: 0;">KESIMPULAN: D3TLH Sebagai Rem Darurat</h3>
    <p style="color: #E0E0E0; font-size: 1.05rem; line-height: 1.6;">
        Penyajian data kontras di atas menggugurkan klaim sepihak perusahaan pertambangan. Oleh karena itu, <b>Instrumen D3TLH dan AMDAL harus dirombak ulang secara radikal</b>. 
    </p>
    <ul style="color: #E0E0E0; font-size: 1rem; line-height: 1.6;">
        <li><b>Wajib Health Impact Assessment (HIA):</b> Dokumen perizinan harus menghitung valuasi ekonomi kerugian kesehatan (Biaya Pengobatan ISPA).</li>
        <li><b>Kekuatan VETO:</b> D3TLH tidak boleh lagi sekadar menjadi "arahan tata ruang" yang lunak. Jika Indeks Kesehatan dan Kualitas Air anjlok, D3TLH harus memiliki kekuatan mengikat untuk menyetop Izin Usaha baru.</li>
    </ul>
    <p style="color: #E0E0E0; font-size: 1.05rem; line-height: 1.6; font-weight:bold; margin-bottom:0;">
        Riset Fase 1 ini membuktikan kebangkrutan tata kelola saat ini, yang akan dijawab oleh <i>ECC Monitoring Dashboard</i> pada Riset Fase 2.
    </p>
</div>
""", unsafe_allow_html=True)
