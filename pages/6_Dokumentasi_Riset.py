import streamlit as st
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.components.sidebar import render_sidebar

st.set_page_config(page_title="Dokumentasi Riset - CELIOS ECC", page_icon="refrensi/Celios China-Indonesia Energy Transition.png", layout="wide")
render_sidebar()

st.title("Dokumentasi Riset")
st.caption("Framework, metodologi, dan kebutuhan dataset proyek CELIOS ECC Intelligence System")

st.markdown("---")

DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")

md_files = sorted([
    f for f in os.listdir(DOCS_DIR)
    if f.endswith(".md") and not f.startswith("_")
]) if os.path.exists(DOCS_DIR) else []

if not md_files:
    st.error("Tidak ada dokumen ditemukan di folder docs/")
else:
    label_map = {
        "framework-riset-ecc.md":          "Framework Riset ECC",
        "prd-ecc-dashboard.md":            "Product Requirements Document (PRD)",
        "paper-fondasi-ecc-swiader2020.md":"Paper Fondasi  Swiader et al. (2020)",
        "estimasi-halaman-publikasi-ecc.md":"Estimasi Halaman Publikasi",
    }
    options = {label_map.get(f, f): f for f in md_files}

    selected_label = st.selectbox("Pilih dokumen:", list(options.keys()))
    selected_file = options[selected_label]
    file_path = os.path.join(DOCS_DIR, selected_file)

    st.markdown("---")

    with open(file_path, "r", encoding="utf-8") as f:
        st.markdown(f.read())

    with open(file_path, "rb") as f:
        st.download_button(
            label="Unduh dokumen ini",
            data=f,
            file_name=selected_file,
            mime="text/markdown",
        )