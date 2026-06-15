import streamlit as st
import os, sys

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

.content-box {
    background: #1A1F2B;
    border: 1px solid #333;
    border-radius: 10px;
    padding: 30px;
    margin-bottom: 25px;
}
.content-box h2 {
    color: #EF5350;
    margin-top: 0;
    font-size: 1.8rem;
    border-bottom: 1px solid #444;
    padding-bottom: 15px;
    margin-bottom: 20px;
}
.content-box h3 {
    color: #FFCDD2;
    font-size: 1.3rem;
    margin-top: 25px;
}
.content-box p, .content-box li {
    color: #E0E0E0;
    font-size: 1.05rem;
    line-height: 1.7;
    text-align: justify;
}
.highlight-text {
    color: #EF5350;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# ── Header Halaman ──
st.markdown('<div class="org-badge">CELIOS — Center of Economic and Law Studies</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">Audit Forensik Metodologi D3TLH & AMDAL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Fase 1: Evaluasi Kebijakan Ekstraktif - Pembuktian Terbalik</div>', unsafe_allow_html=True)

# =====================================================================
# SECTION 1: FILOSOFI AUDIT FORENSIK
# =====================================================================
st.markdown("""
<div class="content-box">
<h2>1. Filosofi Audit Forensik (Sistem Alarm Rakyat)</h2>
<p>
AMDAL dan D3TLH pemerintah mengklaim bersifat "prediktif"—menilai batasan daya dukung alam <i>sebelum</i> izin diberikan. Namun, data lapangan membuktikan bahwa dokumen-dokumen tersebut secara sistematis cacat dan gagal melindungi ruang hidup masyarakat.
</p>
<p><b>Standpoint Riset ECC:</b><br>
Kita melakukan <b>Pembuktian Terbalik</b>. Kita tidak perlu berdebat soal rumus "daya dukung spasial" milik konsultan korporasi. Fakta empiris bahwa <span class="highlight-text">kasus ISPA meroket, banjir bandang rutin terjadi, konflik berdarah bereskalasi, dan izin terus diobral secara anomali</span> adalah <b>Bukti Mutlak (Definitive Proof)</b> bahwa daya dukung ekologis dan sosial wilayah tersebut <b>SUDAH JEBOL</b>.
</p>
<p>
Halaman ini merangkum semua indikator krisis menjadi sebuah palu godam untuk memvonis bahwa sistem AMDAL/D3TLH saat ini sekadar "stempel birokrasi" yang buta terhadap penderitaan manusia.
</p>
</div>
""", unsafe_allow_html=True)

# =====================================================================
# SECTION 2: FAKTA METODOLOGI PEMERINTAH & BLIND SPOTS
# =====================================================================
st.markdown("""
<div class="content-box">
<h2>2. Fakta: Metodologi Resmi D3TLH Pemerintah (Jasa Ekosistem)</h2>
<p>
Berdasarkan dokumen pedoman teknis D3TLH (seperti Permen LH 17/2009 dan panduan KLHK), pemerintah saat ini menyusun D3TLH dengan pendekatan murni spasial/bio-fisik yang disebut <b>Jasa Ekosistem (Ecosystem Services)</b>.
</p>
<p>Indikator resmi yang digunakan dibagi menjadi 4 kategori:</p>
<ul>
<li><b>Jasa Penyediaan (Provisioning):</b> Kapasitas lahan menyediakan pangan, air bersih, dll.</li>
<li><b>Jasa Pengaturan (Regulating):</b> Kapasitas tata air, mitigasi iklim, mitigasi banjir, pemurnian udara.</li>
<li><b>Jasa Pendukung (Supporting):</b> Siklus hara, pembentukan tanah.</li>
<li><b>Jasa Budaya (Cultural):</b> Estetika alam, rekreasi.</li>
</ul>

<h3>Letak Cacat Metodologi (Blind Spots):</h3>
<p>Rumus utama yang dipakai pemerintah untuk menghitung indeks di atas hanyalah: <b>Peta Ekoregion + Peta Tutupan Lahan (Land Cover)</b>.</p>
<ul>
<li><b>Abaikan Nyawa & Morbiditas:</b> Menghitung kapasitas udara dari peta vegetasi, namun <b>TIDAK PERNAH</b> menghitung rekam medis warga (ISPA) yang paru-parunya rusak akibat debu smelter.</li>
<li><b>Abaikan Kedaulatan Ruang:</b> Mengukur kapasitas pertanian, tapi abai terhadap perampasan lahan yang memicu konflik sosial berdarah.</li>
<li><b>Bukan Veto Kebijakan:</b> Saat D3TLH menyatakan daya dukung turun, instrumen ini tidak dipakai untuk "menyetop" penerbitan IUP (Izin Usaha Pertambangan) baru.</li>
</ul>
</div>
""", unsafe_allow_html=True)

# =====================================================================
# DATA LOADING
# =====================================================================
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "processed")

@st.cache_data
def load_data():
    df_kes = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_kesehatan_detail_2014_2024.csv")) if os.path.exists(os.path.join(DATA_DIR, "sulawesi_kesehatan_detail_2014_2024.csv")) else pd.DataFrame()
    df_ika = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_ika_2016_2024.csv")) if os.path.exists(os.path.join(DATA_DIR, "sulawesi_ika_2016_2024.csv")) else pd.DataFrame()
    df_bencana = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_bencana_bnpb_2014_2024.csv")) if os.path.exists(os.path.join(DATA_DIR, "sulawesi_bencana_bnpb_2014_2024.csv")) else pd.DataFrame()
    df_konflik = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_konflik_agraria_tanahkita.csv")) if os.path.exists(os.path.join(DATA_DIR, "sulawesi_konflik_agraria_tanahkita.csv")) else pd.DataFrame()
    return df_kes, df_ika, df_bencana, df_konflik

df_kes, df_ika, df_bencana, df_konflik = load_data()

# =====================================================================
# SECTION 3: MATRIKS PEMBUKTIAN TERBALIK
# =====================================================================
st.markdown("""
<div class="content-box">
    <h2>3. Matriks Pembuktian Terbalik: D3TLH vs Fakta Lapangan</h2>
    <p>
        Di sinilah seluruh temuan riset kita diintegrasikan untuk "menelanjangi" cacat bawaan D3TLH. Di bawah ini adalah benturan langsung antara <b>Mitos (Klaim Dokumen Resmi)</b> versus <b>Realitas Lapangan (Bukti Forensik)</b>.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# A. MITOS KUALITAS UDARA VS ISPA
# ---------------------------------------------------------
colA1, colA2 = st.columns([1, 2])
with colA1:
    st.markdown("""
    <div style="background:#2C3E50; padding:20px; border-radius:10px; border-left:5px solid #E74C3C; height:100%;">
        <h4 style="color:#FFF; margin-top:0;">Mitos D3TLH: Daya Tampung Udara</h4>
        <p style="color:#BDC3C7; font-size:0.9rem;">"Daya tampung udara (berdasarkan peta tutupan lahan) diklaim masih luas dan mampu menyerap emisi."</p>
        <hr style="border-color:#34495E;">
        <h4 style="color:#E74C3C;">Fakta Forensik ECC:</h4>
        <p style="color:#E0E0E0; font-size:0.9rem;">Lonjakan drastis persentase Kasus ISPA dan penyakit saluran pernapasan di lingkar tambang.</p>
        <div style="background:#C0392B; color:white; padding:5px 10px; border-radius:5px; font-weight:bold; text-align:center; margin-top:15px;">
            VONIS: Kegagalan Deteksi Morbiditas Akumulatif
        </div>
    </div>
    """, unsafe_allow_html=True)

with colA2:
    if not df_kes.empty:
        df_ispa = df_kes[df_kes['indikator'].str.contains('ISPA', case=False, na=False)]
        df_ispa_plot = df_ispa.groupby(['tahun', 'provinsi'])['nilai'].sum().reset_index()
        fig1 = px.line(df_ispa_plot, x='tahun', y='nilai', color='provinsi', markers=True,
                       title="Eskalasi Pasien ISPA di Sentra Nikel Sulawesi",
                       color_discrete_sequence=['#E74C3C', '#F39C12', '#3498DB'])
        fig1.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig1, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# B. MITOS KAPASITAS AIR VS IKA
# ---------------------------------------------------------
colB1, colB2 = st.columns([1, 2])
with colB1:
    st.markdown("""
    <div style="background:#2C3E50; padding:20px; border-radius:10px; border-left:5px solid #3498DB; height:100%;">
        <h4 style="color:#FFF; margin-top:0;">Mitos D3TLH: Daya Tampung Air</h4>
        <p style="color:#BDC3C7; font-size:0.9rem;">"Pembuangan tailing diizinkan selama beban cemaran sungai/laut masih secara teori mampu mengencerkan."</p>
        <hr style="border-color:#34495E;">
        <h4 style="color:#3498DB;">Fakta Forensik ECC:</h4>
        <p style="color:#E0E0E0; font-size:0.9rem;">Penurunan drastis Indeks Kualitas Air (IKA BPS) dan hancurnya wilayah tangkap nelayan pesisir.</p>
        <div style="background:#2980B9; color:white; padding:5px 10px; border-radius:5px; font-weight:bold; text-align:center; margin-top:15px;">
            VONIS: Kegagalan Prediksi Kerusakan Terumbu Karang & Livelihood
        </div>
    </div>
    """, unsafe_allow_html=True)

with colB2:
    if not df_ika.empty:
        df_ika_long = df_ika.rename(columns={'Indeks Kualitas Air': 'Nilai IKA'})
        # Filter Provinsi terkait tambang (Sulteng & Sultra) untuk fokus visual
        df_ika_long = df_ika_long[df_ika_long['Provinsi'].isin(['Sulawesi Tengah', 'Sulawesi Tenggara'])]
        fig2 = px.line(df_ika_long, x='Tahun', y='Nilai IKA', color='Provinsi', markers=True,
                       title="Runtuhnya Indeks Kualitas Air (IKA) - BPS",
                       color_discrete_sequence=['#3498DB', '#E74C3C'])
        fig2.add_hline(y=50, line_dash="dot", annotation_text="Batas Kritis Cemar", annotation_position="bottom right", line_color="#E74C3C")
        fig2.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig2, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# C. MITOS DEFORESTASI VS BENCANA ALAM
# ---------------------------------------------------------
colC1, colC2 = st.columns([1, 2])
with colC1:
    st.markdown("""
    <div style="background:#2C3E50; padding:20px; border-radius:10px; border-left:5px solid #F39C12; height:100%;">
        <h4 style="color:#FFF; margin-top:0;">Mitos D3TLH: Daya Dukung Lahan</h4>
        <p style="color:#BDC3C7; font-size:0.9rem;">"Daya dukung tata air tanah dinilai aman karena rasio ekoregion hutan dianggap masih mencukupi secara hitungan spasial provinsi."</p>
        <hr style="border-color:#34495E;">
        <h4 style="color:#F39C12;">Fakta Forensik ECC:</h4>
        <p style="color:#E0E0E0; font-size:0.9rem;">Lonjakan frekuensi kejadian Banjir Bandang dan Tanah Longsor di daerah hilir tambang akibat hilangnya daya resap air lokal.</p>
        <div style="background:#D35400; color:white; padding:5px 10px; border-radius:5px; font-weight:bold; text-align:center; margin-top:15px;">
            VONIS: Kegagalan Mengukur Efek Domino Lanskap
        </div>
    </div>
    """, unsafe_allow_html=True)

with colC2:
    if not df_bencana.empty:
        fig3 = px.bar(df_bencana, x='tahun', y='jumlah_kejadian', color='jenis_bencana', facet_col='provinsi',
                      title="Lonjakan Bencana Hidrometeorologi di Sentra Nikel (Data BNPB)",
                      color_discrete_map={"Banjir": "#3498DB", "Tanah Longsor": "#8D6E63"})
        fig3.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig3, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# D. MITOS KEDAULATAN RUANG VS KONFLIK AGRARIA
# ---------------------------------------------------------
colD1, colD2 = st.columns([1, 2])
with colD1:
    st.markdown("""
    <div style="background:#2C3E50; padding:20px; border-radius:10px; border-left:5px solid #8E44AD; height:100%;">
        <h4 style="color:#FFF; margin-top:0;">Mitos D3TLH: Daya Dukung Sosial</h4>
        <p style="color:#BDC3C7; font-size:0.9rem;">"Status kawasan dialokasikan untuk peruntukan tambang dengan klaim bahwa masyarakat telah memberikan persetujuan (FPIC) dalam sosialisasi amdal."</p>
        <hr style="border-color:#34495E;">
        <h4 style="color:#8E44AD;">Fakta Forensik ECC:</h4>
        <p style="color:#E0E0E0; font-size:0.9rem;">Eskalasi kasus konflik perampasan lahan produktif dan represi aparat, membuktikan persetujuan warga dimanipulasi.</p>
        <div style="background:#8E44AD; color:white; padding:5px 10px; border-radius:5px; font-weight:bold; text-align:center; margin-top:15px;">
            VONIS: Ilusi Jasa Budaya & Kedaulatan Ruang
        </div>
    </div>
    """, unsafe_allow_html=True)

with colD2:
    if not df_konflik.empty:
        # Group by Sektor and create a bar/treemap
        df_konflik_grouped = df_konflik.groupby('Sektor')['Luas Lahan (Ha)'].sum().reset_index()
        fig4 = px.pie(df_konflik_grouped, values='Luas Lahan (Ha)', names='Sektor', hole=0.4,
                      title="Total Luasan Lahan Konflik Agraria di Sulawesi Berdasarkan Sektor",
                      color_discrete_sequence=px.colors.sequential.Purples_r)
        fig4.update_traces(textposition='inside', textinfo='percent+label')
        fig4.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig4, use_container_width=True)

st.markdown("<br><hr style='border: 1px dashed #444;'><br>", unsafe_allow_html=True)

# =====================================================================
# SECTION 4: KESIMPULAN & REKOMENDASI (VETO KESELAMATAN)
# =====================================================================
st.markdown("""
<div class="content-box" style="border: 1px solid #E53935; border-left: 8px solid #E53935; background: linear-gradient(135deg, #2E1515, #1A1F2B);">
    <h2 style="color: #EF5350; border-bottom:none;">4. Putusan Forensik: D3TLH Sebagai "Veto Keselamatan"</h2>
    <p>
        Penyajian benturan data secara langsung di atas menggugurkan seluruh fondasi hitungan <b>Ecosystem Services</b> yang dipakai pemerintah. Dokumen lingkungan yang diterbitkan hanyalah fabrikasi angka spasial yang menutupi kebangkrutan ekologi secara *de facto*.
    </p>
    <p>
        Oleh karena itu, <b>Riset Fase 1 ECC mengeluarkan putusan rekomendasi kebijakan radikal:</b>
    </p>
    <ul>
        <li><b>D3TLH Tidak Boleh Sekadar Dokumen Tata Ruang:</b> D3TLH harus diubah menjadi <b>Hak Veto Absolut</b>. Jika indikator kesehatan turun (ISPA naik) dan IKA anjlok, seluruh penerbitan IUP baru di ekoregion tersebut harus dihentikan secara otomatis tanpa kompromi.</li>
        <li><b>Kewajiban Valuasi Morbiditas:</b> Pendekatan teknis wajib diubah. Dokumen lingkungan tidak boleh hanya menghitung 'baku mutu cerobong', tetapi wajib menghitung <b>Valuasi Ekonomi Kerugian Kesehatan Warga (Health Impact Assessment)</b> sebagai beban utang korporasi.</li>
    </ul>
    <p style="color: #FFCDD2; font-weight:bold; margin-top:20px;">
        Dashboard forensik ini menjadi fondasi masuk akal mengapa kita membutuhkan "ECC Monitoring System" (Riset Fase 2) untuk mengawal keselamatan ruang hidup secara real-time.
    </p>
</div>
""", unsafe_allow_html=True)

