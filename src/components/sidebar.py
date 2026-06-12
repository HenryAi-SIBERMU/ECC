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

        st.markdown("""
        <div style="text-align:center; padding: 6px 0 2px 0;">
            <div style="font-size:0.85rem; font-weight:700; color:#66BB6A; letter-spacing:0.03em;">ECC Intelligence System</div>
            <div style="font-size:0.7rem; color:#9E9E9E; margin-top:2px;">Daya Dukung Lingkungan Hidup Indonesia</div>
        </div>
        """, unsafe_allow_html=True)

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
        st.page_link("pages/0_Progress_Riset.py",           label=_("Progress Riset & Data"))

        st.markdown('<div class="sidebar-label">D3TLH Sulawesi (Fase 1)</div>', unsafe_allow_html=True)
        st.page_link("pages/1_Ekspansi_Industri.py",        label=_("Ekspansi Industri"))
        st.page_link("pages/2_Kualitas_Lingkungan.py",      label=_("Kualitas Lingkungan"))
        st.page_link("pages/3_Beban_Kesehatan.py",          label=_("Beban Kesehatan"))
        st.page_link("pages/4_Konflik_Sosial.py",           label=_("Konflik Sosial"))
        st.page_link("pages/5_Pola_Penerbitan_Izin.py",     label=_("Pola Penerbitan Izin"))
        st.page_link("pages/6_Audit_D3TLH.py",              label=_("Audit D3TLH"))
        st.page_link("pages/7_Kegagalan_Tata_Kelola.py",    label=_("Kegagalan Tata Kelola"))
        st.page_link("pages/8_Distribusi_Manfaat.py",       label=_("Distribusi Manfaat"))

        st.markdown('<div class="sidebar-label">Resources</div>', unsafe_allow_html=True)
        st.page_link("pages/9_Dokumentasi_Riset.py",        label=_("Dokumentasi Riset"))

        st.markdown("---")
        st.caption("CELIOS · ECC Intelligence System · 2026")
