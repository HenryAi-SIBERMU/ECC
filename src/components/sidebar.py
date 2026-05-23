"""Shared sidebar component — imported by every page for consistent branding & navigation."""
import streamlit as st
import os
from src.utils.i18n import init_lang, set_lang, _

def render_sidebar():
    """Render CELIOS logo, language toggle, and ECCIS navigation in sidebar."""
    _dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(_dir, "..", "..", "refrensi", "Celios China-Indonesia Energy Transition.png")
    logo_path = os.path.normpath(logo_path)

    with st.sidebar:
        st.markdown("""
        <style>
        [data-testid="stSidebarNav"] { display: none !important; }
        .sidebar-label {
            font-size: 0.7rem;
            font-weight: 600;
            letter-spacing: 0.08em;
            color: #66BB6A;
            text-transform: uppercase;
            padding: 10px 0 4px 0;
        }
        </style>
        """, unsafe_allow_html=True)

        if os.path.exists(logo_path):
            st.image(logo_path, use_container_width=True)
        else:
            st.caption("CELIOS — ECC Intelligence System")

        st.markdown("---")

        init_lang()
        lang_options = {"id": "ID", "en": "EN"}
        current_lang = st.session_state.get("lang", "id")
        current_idx = list(lang_options.keys()).index(current_lang)

        def switch_lang():
            set_lang(st.session_state.lang_radio)

        st.radio(
            "Bahasa / Language",
            options=lang_options.keys(),
            format_func=lambda x: lang_options[x],
            index=current_idx,
            key="lang_radio",
            on_change=switch_lang,
            horizontal=True,
            label_visibility="collapsed",
        )
        st.markdown("---")

        st.page_link("Dashboard.py", label=_("Beranda"))

        st.markdown('<div class="sidebar-label">Analisis</div>', unsafe_allow_html=True)
        st.page_link("pages/1_Overview_Nasional.py",         label=_("Overview Nasional"))
        st.page_link("pages/2_Jejak_Karbon_Sektoral.py",    label=_("Jejak Karbon Sektoral"))
        st.page_link("pages/3_Defisit_Ekologis.py",         label=_("Defisit Ekologis"))
        st.page_link("pages/4_Indeks_Kerentanan.py",        label=_("Indeks Kerentanan"))
        st.page_link("pages/9_Visualisasi_Multidimensi.py", label=_("Visualisasi Multidimensi"))

        st.markdown('<div class="sidebar-label">Resources</div>', unsafe_allow_html=True)
        st.page_link("pages/5_Eksplorasi_Data.py",          label=_("Eksplorasi Data"))
        st.page_link("pages/6_Dokumentasi_Riset.py",        label=_("Dokumentasi Riset"))
        st.page_link("pages/7_Validasi_Metode.py",          label=_("Validasi Metode"))
        st.page_link("pages/8_Bibliometric_Discovery.py",   label=_("Bibliometric Discovery"))
        st.page_link("pages/10_Infografis.py",              label=_("Infografis"))

        st.markdown("---")
        st.caption("CELIOS · ECC Intelligence System · 2026")
