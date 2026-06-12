import streamlit as st
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.components.sidebar import render_sidebar

st.set_page_config(page_title="CELIOS ECC", layout="wide")
render_sidebar()

st.title("Halaman dalam Pengembangan")
st.info("Data untuk modul ini sedang dalam proses akuisisi/cleaning.")
