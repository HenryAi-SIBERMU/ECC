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

render_sidebar()

st.title("Halaman dalam Pengembangan")
st.info("Data untuk modul ini sedang dalam proses akuisisi/cleaning.")
