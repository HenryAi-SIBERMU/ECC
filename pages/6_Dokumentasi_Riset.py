import streamlit as st
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.components.sidebar import render_sidebar

st.set_page_config(page_title="Dokumentasi Riset - CELIOS ECC", page_icon="refrensi/Celios China-Indonesia Energy Transition.png", layout="wide")
render_sidebar()

st.title("Dokumentasi Riset")
st.caption("Framework, metodologi, dan kebutuhan dataset proyek CELIOS ECC Intelligence System")
st.warning("Halaman ini sedang dalam pengembangan. Fitur pemilihan dokumen dan unduhan akan tersedia pada Fase 8.")

st.markdown("---")

DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")
FRAMEWORK_FILE = os.path.join(DOCS_DIR, "framework-riset-ecc.md")

if os.path.exists(FRAMEWORK_FILE):
    with open(FRAMEWORK_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    st.markdown(content)
else:
    st.error(f"File tidak ditemukan: {FRAMEWORK_FILE}")