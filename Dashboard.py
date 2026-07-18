import streamlit as st
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

st.set_page_config(
    page_title="Overview Temuan — CELIOS D3TLH",
    page_icon="refrensi/Celios China-Indonesia Energy Transition.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Homepage langsung redirect ke halaman Overview Temuan
st.switch_page("pages/0_Overview_Temuan.py")
