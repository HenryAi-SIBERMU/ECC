import streamlit as st
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from src.components.sidebar import render_sidebar

st.set_page_config(
    page_title="CELIOS — ECC Intelligence System",
    page_icon="refrensi/Celios China-Indonesia Energy Transition.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }

.main-title {
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(135deg, #2E7D32, #66BB6A, #A5D6A7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.2;
    margin-bottom: 0;
}
.sub-title {
    font-size: 1rem;
    color: #9E9E9E;
    font-weight: 300;
    margin-top: 0.3rem;
    margin-bottom: 2rem;
}
.info-card {
    background: #1A1F2B;
    border: 1px solid #2E7D3230;
    border-left: 3px solid #2E7D32;
    border-radius: 8px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
}
.info-card h4 { color: #66BB6A; margin: 0 0 0.4rem 0; font-size: 0.95rem; }
.info-card p  { color: #BDBDBD; margin: 0; font-size: 0.85rem; line-height: 1.5; }
</style>
""", unsafe_allow_html=True)

render_sidebar()

st.markdown('<div class="main-title">Environmental Carrying Capacity</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">CELIOS Intelligence System — Dashboard Riset Daya Dukung Lingkungan Hidup Indonesia</div>', unsafe_allow_html=True)

st.warning("Sistem ini sedang dalam tahap pengembangan aktif. Data yang ditampilkan masih berupa simulasi. Fitur analisis penuh akan tersedia secara bertahap.")

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""<div class="info-card">
    <h4>Narasi 1 — Jejak Karbon Sektoral</h4>
    <p>Sektor aktivitas manakah yang paling besar menyumbang tekanan ekologis per provinsi?</p>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown("""<div class="info-card">
    <h4>Narasi 2 — Defisit Ekologis</h4>
    <p>Seberapa besar kesenjangan antara daya dukung alam dan beban aktivitas manusia antar provinsi?</p>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown("""<div class="info-card">
    <h4>Narasi 3 — Indeks Kerentanan</h4>
    <p>Provinsi mana yang paling rentan terhadap krisis daya dukung lingkungan hidup?</p>
    </div>""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
**Metodologi:** Diadaptasi dari Świąder et al. (2020) · **Cakupan:** 38 Provinsi Indonesia · **Baseline:** 2023  
**Sumber data:** BPS WebAPI · PLN Statistik · SIPSN KLHK · ESDM · KLHK GIS · BNPB InaRisk · GFN
""")
