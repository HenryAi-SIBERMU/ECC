"""Shared sidebar component — imported by every page for consistent branding & navigation."""

import os

import streamlit as st

from src.utils.i18n import _, init_lang, set_lang


def render_sidebar():
    """Render CELIOS logo, language toggle, and ECCIS navigation in sidebar."""
    _dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(
        _dir, "..", "..", "refrensi", "Celios China-Indonesia Energy Transition.png"
    )
    logo_path = os.path.normpath(logo_path)

    with st.sidebar:
        st.markdown(
            """
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
        """,
            unsafe_allow_html=True,
        )

        if os.path.exists(logo_path):
            st.image(logo_path, use_container_width=True)

        st.markdown(
            """
        <div style="text-align:center; padding: 6px 0 2px 0;">
            <div style="font-size:0.85rem; font-weight:700; color:#66BB6A; letter-spacing:0.03em;">ECC Intelligence System</div>
            <div style="font-size:0.7rem; color:#9E9E9E; margin-top:2px;">Daya Dukung Lingkungan Hidup Indonesia</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

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

        st.page_link("pages/00_Daftar_Isi.py", label=_("Daftar Isi"))
        st.page_link("Dashboard.py", label=_("Overview Temuan"))
        # st.page_link("pages/0_Progress_Riset.py",           label=_("Progress Riset & Data"))

        st.markdown(
            '<div class="sidebar-label">D3TLH Sulawesi (Fase 1)</div>',
            unsafe_allow_html=True,
        )
        st.page_link("pages/1_Ekspansi_Industri.py", label=_("Ekspansi Industri"))
        st.page_link("pages/2_Kualitas_Lingkungan.py", label=_("Kualitas Lingkungan"))
        st.page_link("pages/3_Beban_Kesehatan.py", label=_("Beban Kesehatan"))
        st.page_link("pages/4_Konflik_Sosial.py", label=_("Konflik Sosial"))
        st.page_link("pages/5_Pola_Penerbitan_Izin.py", label=_("Pola Penerbitan Izin"))
        st.page_link("pages/6_Audit_D3TLH.py", label=_("Audit D3TLH"))
        st.page_link(
            "pages/7_Kegagalan_Tata_Kelola.py", label=_("Kegagalan Tata Kelola")
        )
        st.page_link("pages/8_Distribusi_Manfaat.py", label=_("Distribusi Manfaat"))
        # st.page_link("pages/10_Koridor_Logistik.py", label=_("Koridor Logistik Nikel"))
        st.page_link(
            "pages/11_Demografi_Sosial.py", label=_("Demografi & Struktur Sosial")
        )

        st.markdown(
            '<div class="sidebar-label">Resources</div>', unsafe_allow_html=True
        )
        st.page_link("pages/9_Dokumentasi_Riset.py", label=_("Dokumentasi Riset"))
        st.page_link("pages/12_Infografis_Summary.py", label=_("Infografis Summary"))
        st.page_link("pages/13_Infografis_Fakta.py", label=_("Infografis Fakta"))
        st.page_link("pages/14_Lampiran.py", label=_("Lampiran"))

        st.markdown("---")
        st.caption("CELIOS · ECC Intelligence System · 2026")

        # Injeksi Javascript Auto-Scroller untuk mengatasi bug native Streamlit
        import streamlit.components.v1 as components
        components.html("""
        <script>
            // Cegah duplikasi event listener
            if (!window.parent.window._customScrollListenerAttached) {
                window.parent.window._customScrollListenerAttached = true;
                const scroll_to_hash = function() {
                    const hash = window.parent.location.hash;
                    if (hash) {
                        const id = hash.substring(1);
                        const el = window.parent.document.getElementById(id);
                        if (el) {
                            el.scrollIntoView({behavior: "smooth", block: "start"});
                        }
                    }
                };
                
                // Pantau perubahan hash URL secara real-time
                window.parent.addEventListener('hashchange', function() {
                    setTimeout(scroll_to_hash, 300);
                    setTimeout(scroll_to_hash, 1000); // Fallback
                });
            }
            
            // Eksekusi paksa pada saat halaman pertama kali dimuat
            setTimeout(function() {
                const hash = window.parent.location.hash;
                if (hash) {
                    const id = hash.substring(1);
                    const el = window.parent.document.getElementById(id);
                    if (el) {
                        el.scrollIntoView({behavior: "smooth", block: "start"});
                    }
                }
            }, 800);
            
            setTimeout(function() {
                const hash = window.parent.location.hash;
                if (hash) {
                    const id = hash.substring(1);
                    const el = window.parent.document.getElementById(id);
                    if (el) {
                        el.scrollIntoView({behavior: "smooth", block: "start"});
                    }
                }
            }, 1500); // Ekstra Fallback jika data rendering berat
        </script>
        """, height=0, width=0)
