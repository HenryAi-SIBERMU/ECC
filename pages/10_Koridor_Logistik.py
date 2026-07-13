import streamlit as st
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.components.sidebar import render_sidebar

st.set_page_config(page_title="CELIOS ECC - Koridor Logistik", layout="wide")
render_sidebar()

# ── Styles ──
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
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 1px;
    margin-bottom: 1rem;
    box-shadow: 0 4px 15px rgba(27, 94, 32, 0.3);
}
</style>
""", unsafe_allow_html=True)

# ── Header Halaman ──
st.markdown('<div class="org-badge">CELIOS — Center of Economic and Law Studies</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">Koridor Logistik Nikel</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Pemetaan Jalur Distribusi Logistik Nikel Sulawesi</div>', unsafe_allow_html=True)
st.markdown("---")

st.markdown("""
<div style="background:#1E1E1E; padding:25px; border-radius:10px; border-left:5px solid #3498DB; margin-top: 20px; text-align: center;">
    <h3 style="color: #3498DB; margin-bottom: 15px;">Peta Jalur Distribusi Telah Dipindahkan</h3>
    <p style="color: #E0E0E0; font-size: 1.1rem; line-height: 1.6; margin-bottom: 25px;">
        Visualisasi komprehensif mengenai <b>Peta Jalur Distribusi Logistik Nikel Sulawesi</b> (peta <i>supply chain</i> maritim dari titik tambang/pelabuhan ke negara tujuan) kini telah diintegrasikan langsung ke dalam <b>Bab 1. Peta Konsesi & Lanskap Ekstraktif</b> untuk menjaga kontinuitas alur baca laporan.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("Lihat Peta Logistik (Menuju Bab 1) ➡️", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Peta_Konsesi.py")

