new_veto_calc = """
# Calculate Veto
skor_veto_1 = 0.0
skor_veto_2 = 0.0
skor_veto_3 = 0.0
izin_baru = 0
perusahaan_ilegal = 0
kapasitas_pltu = 0.0

if not df_izin.empty:
    df_izin['tahun'] = pd.to_numeric(df_izin['tahun'], errors='coerce')
    df_izin['jumlah_izin'] = pd.to_numeric(df_izin['jumlah_izin'], errors='coerce').fillna(0)
    df_izin_recent = df_izin[df_izin['tahun'] >= 2014]
    izin_baru = df_izin_recent['jumlah_izin'].sum()
    skor_veto_1 = min(10.0, (izin_baru / 100) * 10) # 100 izin baru di masa krisis = 10.0

if not df_kpa_izin.empty:
    perusahaan_ilegal = len(df_kpa_izin['nama_perusahaan'].unique())
    skor_veto_2 = min(10.0, (perusahaan_ilegal / 10) * 10) # 10 perusahaan dibiarkan beroperasi ilegal = 10.0

if not df_pltu_captive.empty:
    df_pltu_captive['Capacity (MW)'] = pd.to_numeric(df_pltu_captive['Capacity (MW)'], errors='coerce').fillna(0)
    kapasitas_pltu = df_pltu_captive['Capacity (MW)'].sum()
    skor_veto_3 = min(10.0, (kapasitas_pltu / 5000) * 10) # > 5 GW PLTU Captive = 10.0 (Kenyataannya > 16 GW)

skor_akumulasi_veto = (skor_veto_1 + skor_veto_2 + skor_veto_3) / 3
"""

new_veto_hero = """
# ---------------------------------------------------------
# E. MITOS TATA KELOLA VS OBRAL IZIN (VETO KEBIJAKAN)
# ---------------------------------------------------------
colE1, colE2 = st.columns([1, 2])
with colE1:
    st.markdown(f'''
    <div style="background:#2C3E50; padding:20px; border-radius:10px; border-left:5px solid #E67E22; height:100%;">
        <h4 style="color:#FFF; margin-top:0;">Mitos D3TLH: Veto Kebijakan</h4>
        <p style="color:#BDC3C7; font-size:0.9rem;">"Penyusunan D3TLH adalah dokumen sakti (veto) yang dapat membatasi izin eksploitasi jika daya dukung lingkungan telah terlampaui."</p>
        <hr style="border-color:#34495E;">
        <h4 style="color:#E67E22;">Fakta Forensik ECC:</h4>
        <p style="color:#E0E0E0; font-size:0.9rem;">Negara mengalami kelumpuhan tata kelola (Regulatory Capture). Izin diobral massal, perusahaan ilegal dibiarkan, dan infrastruktur energi kotor diloloskan di episentrum krisis.</p>
        <div style="background-color: #1A202C; padding: 15px; border-radius: 8px; margin-top: 15px; text-align: center; border: 1px solid #E67E22;">
            <div style="font-size: 11px; color: #BDC3C7; text-transform: uppercase; letter-spacing: 1px;">Skor Kegagalan Tata Kelola</div>
            <div style="font-size: 32px; font-weight: 800; color: #E67E22; line-height: 1.2;">{skor_akumulasi_veto:.1f} <span style="font-size: 16px;">/ 10</span></div>
            <div style="font-size: 11px; color: #E67E22; margin-top: 5px; font-weight: bold;">STATUS: REGULATORY CAPTURE</div>
        </div>
        <div style="background:#D35400; color:white; padding:5px 10px; border-radius:5px; font-weight:bold; text-align:center; margin-top:15px;">
            VONIS: Kegagalan Supremasi Hukum
        </div>
    </div>
    ''', unsafe_allow_html=True)

with colE2:
    tab_v1, tab_v2, tab_v3 = st.tabs(["Fase 1: Obral Konsesi Legal", "Fase 2: Pembiaran Pelanggaran", "Fase 3: Karpet Merah Energi Kotor"])
    
    with tab_v1:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Narasi Anomali:</b> Di tengah memuncaknya status krisis daya dukung lingkungan, pemerintah secara paradoks justru menerbitkan ratusan izin eksploitasi tambang (IUP) baru. Dokumen veto tidak berfungsi.</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Obral IUP Baru (Sejak 2014)", f"{izin_baru:.0f} Izin", "Eksploitasi Meluas", delta_color="inverse")
        col2.metric("Skor Paradoks Izin", f"{skor_veto_1:.1f} / 10", "STATUS: VETO GAGAL", delta_color="inverse")
        col3.metric("Fungsi Pembatasan", "Nihil", "Hanya Formalitas", delta_color="inverse")
        st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
        
        if not df_izin.empty:
            df_izin_plot = df_izin[df_izin['tahun'] >= 2014].copy()
            fig_v1 = px.bar(df_izin_plot, x='tahun', y='jumlah_izin', title="Lonjakan Penerbitan IUP di Era Krisis Lingkungan", color_discrete_sequence=['#E67E22'])
            fig_v1.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_v1, use_container_width=True)
            with st.expander("Tampilkan Data Penerbitan Izin (Ditjen Minerba)"):
                st.dataframe(df_izin_plot, use_container_width=True)

    with tab_v2:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Narasi Anomali:</b> Bukti mutlak 'Regulatory Capture'—bahkan ketika perusahaan beroperasi ilegal, menabrak izin, tumpang tindih, atau HGU kedaluwarsa, negara tidak berani melakukan penegakan hukum dan membiarkannya.</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Perusahaan Melanggar Hukum", f"{perusahaan_ilegal} Korporat", "Hukum Tumpul", delta_color="inverse")
        col2.metric("Tindakan Tegas Negara", "0", "Pembiaran Sistematis", delta_color="inverse")
        col3.metric("Skor Impunitas", f"{skor_veto_2:.1f} / 10", "STATUS: NEGARA LUMPUH", delta_color="inverse")
        st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
        
        if not df_kpa_izin.empty:
            st.dataframe(df_kpa_izin[['nama_perusahaan', 'jenis_masalah_izin', 'lokasi']], use_container_width=True, hide_index=True)
            with st.expander("Tampilkan Detail Kasus (KPA)"):
                st.dataframe(df_kpa_izin, use_container_width=True)

    with tab_v3:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Narasi Anomali:</b> Inkonsistensi paling telanjang terhadap komitmen iklim. Di wilayah ekoregion krisis, pemerintah memberikan karpet merah pembangunan infrastruktur penyumbang emisi terbesar (PLTU Batubara Captive) khusus untuk menyuplai kawasan smelter nikel.</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Kapasitas PLTU Captive", f"{kapasitas_pltu/1000:.1f} GW", "Energi Kotor Masif", delta_color="inverse")
        col2.metric("Dampak Ekologi", "Emisi & Abu Beracun", "Mematikan", delta_color="inverse")
        col3.metric("Skor Inkonsistensi Iklim", f"{skor_veto_3:.1f} / 10", "STATUS: HYPOCRISY", delta_color="inverse")
        st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
        
        if not df_pltu_captive.empty:
            pltu_status = df_pltu_captive.groupby('Status').size().reset_index(name='jumlah')
            fig_v3 = px.pie(pltu_status, names='Status', values='jumlah', title="Proporsi Status PLTU Batubara Captive di Sulawesi", hole=0.4, color_discrete_sequence=px.colors.sequential.Oranges_r)
            fig_v3.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_v3, use_container_width=True)
            with st.expander("Tampilkan Data PLTU Captive (Global Energy Monitor)"):
                st.dataframe(df_pltu_captive[['Plant name', 'Owner', 'Status', 'Capacity (MW)']], use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)
"""
