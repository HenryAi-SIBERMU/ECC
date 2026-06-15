import streamlit as st
import os, sys
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.components.sidebar import render_sidebar

st.set_page_config(page_title="CELIOS ECC - Audit D3TLH", layout="wide")
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
# DATA PREPARATION (PLACEHOLDERS UNTUK BENTO CARDS)
# ---------------------------------------------------------
# TODO: Ganti dengan data aktual setelah pipeline ETL D3TLH selesai.
# Untuk sementara, kita gunakan angka representatif yang mencerminkan urgensi isu (berdasarkan studi literatur).

total_kasus_ispa = 450000  # Angka ilustrasi kumulatif penderita ISPA di lingkar tambang
penurunan_ika = 25         # Persentase rata-rata penurunan Indeks Kualitas Air
jumlah_bencana = 320       # Kejadian bencana hidrometeorologi (banjir/longsor) di area konsesi

# ---------------------------------------------------------
# HERO SECTION (EXECUTIVE SUMMARY)
# ---------------------------------------------------------
st.markdown('<div class="org-badge">CELIOS — Center of Economic and Law Studies</div>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">Audit Metodologi D3TLH: Blind Spots & Dampak yang Hilang</h1>', unsafe_allow_html=True)

# Bento Cards Executive Summary (Sesuai arahan PRD: D3TLH Mengabaikan Sosial)
st.markdown("<br>", unsafe_allow_html=True)
c1, c2 = st.columns(2)

with c1:
    st.markdown("""
    <div style="background:#1A1A1A; padding: 20px; border-radius: 10px; border-top: 4px solid #E74C3C; height: 100%; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
        <div style="font-size:0.8rem; color:#E74C3C; font-weight:bold; letter-spacing:1px; margin-bottom:10px;">TITIK BUTA METODOLOGIS</div>
        <div style="color: #fff; font-size: 1.3rem; font-weight:bold; margin-bottom:12px; line-height:1.3;">D3TLH Mengabaikan Dimensi Sosial-Kesehatan</div>
        <div style="color:#B0BEC5; font-size:0.9rem; line-height:1.5;">
            Instrumen <b>Daya Dukung dan Daya Tampung Lingkungan Hidup (D3TLH)</b> yang digunakan saat ini terbukti cacat metodologis. Dokumen ini didesain hanya untuk menghitung kapasitas daya tampung fisik (seperti debu dan air), namun <b>secara sistematis menghilangkan metrik penderitaan manusia</b>—seperti lonjakan kasus ISPA (Infeksi Saluran Pernapasan Akut) dan hilangnya ruang hidup komunal.
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div style="background:#1A1A1A; padding: 20px; border-radius: 10px; border-top: 4px solid #F39C12; height: 100%; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
        <div style="font-size:0.8rem; color:#F39C12; font-weight:bold; letter-spacing:1px; margin-bottom:10px;">KRISIS HIDROMETEOROLOGI</div>
        <div style="color: #fff; font-size: 1.3rem; font-weight:bold; margin-bottom:12px; line-height:1.3;">Ilusi Batas Aman Lingkungan</div>
        <div style="color:#B0BEC5; font-size:0.9rem; line-height:1.5;">
            Batas ambang polusi yang diklaim 'masih aman' dalam dokumen D3TLH berbanding terbalik dengan realitas lapangan. Ribuan hektar wilayah resapan air yang telah dirusak berimplikasi langsung pada lonjakan frekuensi banjir bandang dan tanah longsor mematikan, yang dampaknya <b>ditanggung sepenuhnya oleh masyarakat lokal, bukan korporasi</b>.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<p class="sub-title">Membongkar kesenjangan antara dokumen lingkungan (D3TLH) yang hanya mengukur indikator pro-investasi versus data riil penderitaan ekologis dan krisis kesehatan masyarakat.</p>', unsafe_allow_html=True)

with st.expander("Metodologi Audit D3TLH", expanded=False):
    st.markdown("""
    **Kerangka Logis (Audit Metodologis):**
    Bagian ini dirancang untuk membuktikan hipotesis bahwa dokumen D3TLH mengalami *'blind spots'* yang disengaja.
    
    1. **Kritik Metrik Fisik vs Sosial:** Membandingkan perhitungan emisi statis dalam AMDAL dengan data ledakan penyakit pernapasan (ISPA) dari Kementerian Kesehatan.
    2. **Kritik Perubahan Lanskap:** Membandingkan batas deforestasi wajar dalam D3TLH dengan data peningkatan drastis bencana banjir dan tanah longsor akibat hilangnya hutan primer (data BNPB/Walhi).
    3. **Pendekatan Metodologis:** *Spatial Overlay* dan *Time-Series Comparison* antara indikator lingkungan pemerintah vs metrik penderitaan sosial masyarakat adat/lokal.
    
    **Tujuan:**
    Memperlihatkan bahwa selama dokumen lingkungan (AMDAL & D3TLH) tidak memasukkan variabel kerugian sosial-ekonomi masyarakat dan ancaman krisis kesehatan, maka dokumen tersebut hanyalah ilusi ilmiah untuk melegalkan pengrusakan alam atas nama investasi.
    """)

# Hero Statement
st.markdown("""
Selama ini, retorika pertumbuhan ekonomi dan hilirisasi selalu berlindung di balik klaim bahwa investasi telah "mematuhi daya dukung lingkungan". Namun, audit silang terhadap data kesehatan masyarakat dan kebencanaan membuka kedok kebohongan instrumen Daya Dukung dan Daya Tampung Lingkungan Hidup (D3TLH). Dokumen ini didesain secara sengaja sebagai instrumen "rabun dekat" yang hanya menghitung kapasitas fisik wilayah dalam menoleransi polusi industri, sambil menutup mata sepenuhnya dari realitas sosiologis di baliknya. Ketika D3TLH menyatakan sebuah wilayah masih sanggup menampung pabrik smelter baru, di saat yang sama Puskesmas lokal mencatat ledakan ribuan penderita ISPA dan desa-desa lingkar tambang diterjang banjir bandang berlumpur. Kegagalan memasukkan variabel kerentanan manusia dan risiko bencana struktural ini menjadikan D3TLH sekadar fiksi administratif yang membiarkan masyarakat lingkar tambang menanggung ongkos kematian dan penderitaan secara perlahan.
""")

st.markdown("<br>", unsafe_allow_html=True)

# Bento Cards Metrics (Placeholders for now)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">BIAYA KESEHATAN TERSEMBUNYI</div>
            <div class="metric-value" style="color: #E53935;">ISPA Melonjak</div>
            <div class="metric-desc">Peningkatan tajam infeksi saluran pernapasan akut di wilayah lingkar smelter yang <b>tidak pernah dihitung</b> sebagai biaya kerugian (externality cost) dalam D3TLH.</div>
        </div>
        <div class="metric-source">Sumber: Data Dinas Kesehatan (Proses Integrasi)<br>Indikator: Kasus ISPA Morowali & Konawe</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">ILUSI DAYA TAMPUNG AIR</div>
            <div class="metric-value" style="color: #FFB74D;">IKA Turun Tajam</div>
            <div class="metric-desc">Indeks Kualitas Air (IKA) di sentra tambang terus anjlok ke level cemaran berat akibat pembuangan tailing laut dan lumpur nikel yang menutupi terumbu karang.</div>
        </div>
        <div class="metric-source">Sumber: SLHI KLHK<br>Indikator: Indeks Kualitas Air Sultra & Sulteng</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">BENCANA HIDROMETEOROLOGI</div>
            <div class="metric-value" style="color: #4DB6AC;">Banjir Lumpur</div>
            <div class="metric-desc">Hilangnya daya serap air (hutan primer) di hulu konsesi nikel memicu rentetan banjir lumpur. D3TLH abai memprediksi efek domino bencana lanskap ini.</div>
        </div>
        <div class="metric-source">Sumber: Data BNPB/BPBD (Proses Integrasi)<br>Indikator: Frekuensi Banjir & Longsor</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><hr style='border: 1px dashed #333;'><br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# FALLBACK SECTION (UNTUK BAGIAN BERIKUTNYA)
# ---------------------------------------------------------

st.subheader("6.1 Membandingkan Metrik Fisik vs Dampak Nyata")
st.info("Visualisasi data kesehatan (Kemenkes) vs Tingkat Polusi Udara/ISPU sedang dalam tahap kompilasi dan pembersihan data. Komponen chart akan ditambahkan pada *sprint* berikutnya.")

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("6.2 Dampak Menghilangnya Kawasan Resapan Air")
st.info("Peta spasial overlay antara perluasan konsesi tambang, hilangnya daya resap air (tutupan hutan), dan titik kejadian banjir bandang (Data BNPB) akan diintegrasikan di sini.")

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("6.3 Kesimpulan Audit: Revisi Menyeluruh D3TLH")
st.markdown("""
<div style="background:#1E1E1E; padding:15px 20px; border-radius:8px; border-left:4px solid #66BB6A; margin-top: 10px; margin-bottom: 25px;">
    <span style="color: #E0E0E0; font-size: 0.95rem;">
        <b style="color:#66BB6A;">Rekomendasi Kebijakan:</b> Pemerintah Republik Indonesia mutlak perlu merombak metodologi penyusunan AMDAL dan D3TLH. Instrumen ini <b>harus secara mandat (mandatory) memasukkan valuasi ekonomi kerugian kesehatan (Health Impact Assessment) masyarakat dan risiko bencana turunan</b>, bukan hanya sebatas menghitung ambang batas partikel kimia secara terisolasi. Selama celah metodologis ini dibiarkan, D3TLH akan terus menjadi alat stempel perampasan ruang atas nama investasi yang legal namun tidak bermoral.
    </span>
</div>
""", unsafe_allow_html=True)
