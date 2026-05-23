import streamlit as st
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.components.sidebar import render_sidebar
st.set_page_config(page_title="Validasi Metode - CELIOS ECC", page_icon="refrensi/Celios China-Indonesia Energy Transition.png", layout="wide")
render_sidebar()

st.title("Validasi Metode")
st.caption("Validasi metodologi ECC melalui literatur ilmiah (OpenAlex API)")
st.warning("Halaman ini sedang dalam pengembangan. Konten analisis akan tersedia pada Fase 9.")