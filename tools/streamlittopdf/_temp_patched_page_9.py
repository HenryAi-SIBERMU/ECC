__file__ = r'C:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\pages\9_Dokumentasi_Riset.py'
import streamlit as st
import os, sys, re

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


st.set_page_config(
    page_title="Framework Riset D3TLH — CELIOS",
    page_icon="refrensi/Celios China-Indonesia Energy Transition.png",
    layout="wide"
)


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
FRAMEWORK_PATH = os.path.join(BASE_DIR, "docs", "framework-fase1-d3tlh.md")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }
.doc-title {
    font-size: 1.8rem; font-weight: 800;
    color: #ECEFF1;
    margin-bottom: 0;
}
.doc-subtitle {
    font-size: 0.9rem; color: #78909C;
    margin-top: 0.2rem; margin-bottom: 1.5rem;
}
blockquote {
    border-left: 3px solid #43A047 !important;
    background: #1A2F1C;
    padding: 0.6rem 1rem;
    border-radius: 0 6px 6px 0;
    color: #A5D6A7;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="doc-title">Framework Riset — D3TLH Sulawesi</div>', unsafe_allow_html=True)
st.markdown('<div class="doc-subtitle">CELIOS Research Division · Evaluasi Daya Dukung dan Daya Tampung Lingkungan Hidup · Fase 1</div>', unsafe_allow_html=True)
st.markdown("---")

# ─── BACA DAN BERSIHKAN DARI EMOJI ─────────────────────────────────────────
def strip_emoji(text: str) -> str:
    """Hapus karakter emoji dan simbol non-ASCII luar Latin."""
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map
        u"\U0001F1E0-\U0001F1FF"  # flags
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642"
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"
        u"\u3030"
        "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub("", text)

if os.path.exists(FRAMEWORK_PATH):
    with open(FRAMEWORK_PATH, "r", encoding="utf-8") as f:
        raw = f.read()
    clean = strip_emoji(raw)
    st.markdown(clean)

    with open(FRAMEWORK_PATH, "rb") as f:
        st.download_button(
            label="Unduh Framework (Markdown)",
            data=f,
            file_name="framework-fase1-d3tlh.md",
            mime="text/markdown",
        )
else:
    st.error(f"File framework tidak ditemukan: {FRAMEWORK_PATH}")