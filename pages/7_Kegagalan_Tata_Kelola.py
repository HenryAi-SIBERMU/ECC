import streamlit as st
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.components.sidebar import render_sidebar

st.set_page_config(page_title="CELIOS ECC - Tata Kelola", layout="wide")
render_sidebar()

# ── Styles (Sesuai Pedoman UI/UX CELIOS & Page 5) ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

* { font-family: 'Inter', sans-serif; }

.main-title {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #E67E22, #F39C12, #D35400);
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
    background: linear-gradient(135deg, #D35400, #E67E22);
    color: white;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

.temuan-card {
    background-color: #2C0B0E; border: 1px solid #E74C3C;
    padding: 20px; border-radius: 8px; margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# HERO SECTION
# ---------------------------------------------------------
st.markdown('<div class="org-badge">CELIOS — Center of Economic and Law Studies</div>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">Matriks Veto: Kegagalan Tata Kelola D3TLH</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Menyingkap tabir "Regulatory Capture" di mana instrumen Daya Dukung dan Daya Tampung Lingkungan Hidup (D3TLH) secara sistematis dilumpuhkan dan diabaikan demi melayani obral izin ekstraktif.</p>', unsafe_allow_html=True)

with st.expander("Metodologi Pendekatan (Framework D3TLH)", expanded=False):
    st.markdown("""
    Bagian ini menguji **Sub-Bab 4.7 Kegagalan Tata Kelola D3TLH** dari kerangka riset.
    
    Fokus pembuktian empiris untuk menjawab 3 Pertanyaan Kritis:
    1. **Apakah D3TLH digunakan sebagai dasar keputusan perizinan?**
    2. **Apakah D3TLH bersifat mengikat atau hanya rekomendasi formalitas?**
    3. **Apakah instrumen D3TLH dapat diabaikan begitu saja secara prosedural?**
    
    *Crosstab Matriks yang Digunakan:* Status Daya Dukung Lingkungan (Aman/Tertekan/Kritis) diuji silang terhadap Keputusan Izin Aktual (Izin Keluar / Ditolak).
    """)

st.markdown("<br><hr style='border: 1px dashed #333;'><br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# ARSITEKTUR UTAMA (SPLIT 1:2 SESUAI PANDUAN UI MATRIKS)
# ---------------------------------------------------------
col_kiri, col_kanan = st.columns([1, 2])

# KOLOM KIRI (1 Part): KARTU VONIS & AKUMULASI SKOR
with col_kiri:
    st.markdown("""
    <div style="background:#2C3E50; padding:20px; border-radius:10px; border-left:5px solid #E67E22; height:100%;">
        <h4 style="color:#FFF; margin-top:0;">Mitos Veto Kebijakan</h4>
        <p style="color:#BDC3C7; font-size:0.9rem;">"D3TLH adalah dokumen sakti (veto) yang dapat merem atau menolak izin eksploitasi industri ekstraktif jika daya dukung alam terlampaui."</p>
        <hr style="border-color:#34495E;">
        <h4 style="color:#E67E22;">Fakta Forensik:</h4>
        <p style="color:#E0E0E0; font-size:0.9rem;">
            Negara mengalami kelumpuhan tata kelola (Regulatory Capture). Izin terus diobral secara masif, dan perusahaan dibiarkan melanggar aturan bahkan di saat alam berteriak krisis.
        </p>
        
        <!-- PLACEHOLDER SKOR AKUMULASI (Standard Matriks UI) -->
        <div style="background-color: #1A202C; padding: 15px; border-radius: 8px; margin-top: 15px; text-align: center; border: 1px solid #E67E22;">
            <div style="font-size: 11px; color: #BDC3C7; text-transform: uppercase; letter-spacing: 1px;">Skor Kegagalan Tata Kelola</div>
            <div style="font-size: 32px; font-weight: 800; color: #E67E22; line-height: 1.2;">[X.X] <span style="font-size: 16px;">/ 10</span></div>
        </div>
        
        <div style="background:#D35400; color:white; padding:5px 10px; border-radius:5px; font-weight:bold; text-align:center; margin-top:15px; text-transform: uppercase;">
            VONIS: Regulatory Capture
        </div>
        
        <!-- JAWABAN 3 PERTANYAAN KRITIS -->
        <div style="margin-top: 25px; font-size: 0.85rem; color: #BDC3C7; line-height: 1.6;">
            <b>Kesimpulan Framework:</b><br>
            • D3TLH Digunakan? <span style="color:#E74C3C; font-weight:bold;">TIDAK</span><br>
            • Bersifat Mengikat? <span style="color:#E74C3C; font-weight:bold;">TIDAK</span><br>
            • Dapat Diabaikan? <span style="color:#E74C3C; font-weight:bold;">YA</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# KOLOM KANAN (2 Parts): 4 TAB INTERAKTIF
with col_kanan:
    tab1, tab2, tab3, tab4 = st.tabs([
        "Paradoks Izin", 
        "Matriks Crosstab", 
        "Impunitas Hukum", 
        "Hipokrisi Iklim"
    ])
    
    with tab1:
        st.info("🚧 PLACEHOLDER: Narasi Anomali, 3 Metrik Kolom, dan Grafik Combo Bar/Line dengan Garis Batas Kritis.")
        
    with tab2:
        st.info("🚧 PLACEHOLDER: Tabel Visual Status Daya Dukung (Aman/Tertekan/Kritis) vs Keputusan Izin (Izin Keluar).")
        
    with tab3:
        st.info("🚧 PLACEHOLDER: Narasi Anomali, 3 Metrik Kolom, dan Tabel Korporasi Bermasalah (KPA).")
        
    with tab4:
        st.info("🚧 PLACEHOLDER: Narasi Anomali, 3 Metrik Kolom, dan Chart PLTU Captive.")


# ---------------------------------------------------------
# TEMUAN UTAMA (BOTTOM SECTION)
# ---------------------------------------------------------
st.markdown("""
<div class='temuan-card'>
    <h3 style='color: #E74C3C; margin-top: 0;'>🎯 TEMUAN YANG DIUNGKAP</h3>
    <ul style='color: #E0E0E0; font-size: 1.15rem; line-height: 1.6;'>
        <li><b>Daya dukung tidak menjadi pembatas nyata.</b></li>
        <li><b>Keputusan perizinan tetap dominan secara politik meski D3TLH menunjukkan kondisi kritis.</b></li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

