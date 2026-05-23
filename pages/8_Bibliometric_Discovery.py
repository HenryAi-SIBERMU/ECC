import streamlit as st
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.components.sidebar import render_sidebar
st.set_page_config(page_title="Bibliometric Discovery - CELIOS ECC", page_icon="refrensi/Celios China-Indonesia Energy Transition.png", layout="wide")
render_sidebar()

st.title("Bibliometric Discovery")
st.caption("Peta lanskap ilmiah riset ECC di Indonesia dan Asia Tenggara")
st.warning("Halaman ini sedang dalam pengembangan. Konten analisis akan tersedia pada Fase 9.")