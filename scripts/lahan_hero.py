# ---------------------------------------------------------
# C. MITOS DAYA DUKUNG LAHAN & SOSIAL
# ---------------------------------------------------------
colC1, colC2 = st.columns([1, 2])
with colC1:
    st.markdown(f"""
<div style="background:#2C3E50; padding:20px; border-radius:10px; border-left:5px solid #FF9800; height:100%;">
<h4 style="color:#FFF; margin-top:0;">Mitos D3TLH: Daya Dukung Lahan</h4>
<p style="color:#BDC3C7; font-size:0.9rem;">"Ekspansi tambang diklaim mematuhi zona peruntukan dan tidak mengganggu fungsi jasa ekosistem lahan/sosial."</p>
<hr style="border-color:#34495E;">
<h4 style="color:#FF9800;">Fakta Forensik ECC:</h4>
<p style="color:#E0E0E0; font-size:0.9rem;">Hancurnya sabuk hijau memicu rentetan bencana, eskalasi konflik berdarah, dan monopoli izin yang tak terkendali.</p>
<div style="background-color: #1A202C; padding: 15px; border-radius: 8px; margin-top: 15px; text-align: center; border: 1px solid #FF9800;">
<div style="font-size: 11px; color: #BDC3C7; text-transform: uppercase; letter-spacing: 1px;">Akumulasi Skor Lahan & Sosial</div>
<div style="font-size: 32px; font-weight: 800; color: #FF9800; line-height: 1.2;">{(skor_akumulasi_lahan + skor_akumulasi_sosial + skor_akumulasi_veto)/3:.1f} <span style="font-size: 16px;">/ 10</span></div>
<div style="font-size: 11px; color: #FF9800; margin-top: 5px; font-weight: bold;">STATUS: KRISIS MULTI-DIMENSI</div>
</div>
<div style="background:#E67E22; color:white; padding:5px 10px; border-radius:5px; font-weight:bold; text-align:center; margin-top:15px;">
VONIS: Kegagalan Veto Kebijakan
</div>
</div>
""", unsafe_allow_html=True)

with colC2:
    tab_l1, tab_l2, tab_l3, tab_l4 = st.tabs(["Bencana Banjir & Longsor", "Deforestasi Primer", "Konflik Agraria Darat", "Monopoli Izin (IUP)"])
    
    with tab_l1:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Narasi Anomali:</b> Data BNPB membuktikan bahwa klaim 'mitigasi banjir' dalam dokumen AMDAL tambang dan smelter sama sekali tidak terbukti di lapangan. Banjir bandang terus terjadi seiring laju pembongkaran bentang alam pegunungan.</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Bencana Sulteng & Sultra", f"{bencana_sulteng_sultra:,.0f} Kejadian", "BNPB 2014-2024")
        col2.metric("Korban Terdampak", "256 Ribu Jiwa", "Estimasi Total", delta_color="inverse")
        col3.metric("Skor Bencana Lahan", f"{skor_lahan_1:.1f} / 10", "STATUS: DARURAT BENCANA", delta_color="inverse")
        st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
        
        if not df_bencana.empty:
            df_b = df_bencana.copy()
            df_b['tahun'] = pd.to_numeric(df_b['tahun'], errors='coerce')
            df_b['jumlah_kejadian'] = pd.to_numeric(df_b['jumlah_kejadian'], errors='coerce').fillna(0)
            df_b_trend = df_b.groupby(['tahun', 'provinsi'])['jumlah_kejadian'].sum().reset_index()
            fig_l1 = px.bar(df_b_trend, x='tahun', y='jumlah_kejadian', color='provinsi', 
                           title="Frekuensi Bencana Hidrometeorologi (Banjir & Longsor)",
                           color_discrete_sequence=px.colors.qualitative.Pastel)
            fig_l1.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_l1, use_container_width=True)

    with tab_l2:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Narasi Anomali:</b> Hutan primer yang berfungsi sebagai jasa penyediaan air dan penyerap karbon ditebang habis atas nama IUP. Pemerintah membiarkan sabuk hijau alam hilang begitu saja.</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Deforestasi Sulteng & Sultra", f"{deforestasi_sentra:,.0f} Ha", "2014-2023 (GFW)")
        col2.metric("Kehilangan Tutupan Pohon", f"{df_gfw['Total_Deforestasi_Ha'].sum():,.0f} Ha", "Seluruh Sulawesi", delta_color="normal")
        col3.metric("Skor Kehancuran Ekosistem", f"{skor_lahan_2:.1f} / 10", "STATUS: DARURAT DEFORESTASI", delta_color="inverse")
        st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
        
        if not df_gfw.empty:
            df_g = df_gfw.copy()
            df_g['Tahun'] = pd.to_numeric(df_g['Tahun'], errors='coerce')
            df_g['Total_Deforestasi_Ha'] = pd.to_numeric(df_g['Total_Deforestasi_Ha'], errors='coerce').fillna(0)
            df_g_trend = df_g.groupby(['Tahun', 'Provinsi'])['Total_Deforestasi_Ha'].sum().reset_index()
            fig_l2 = px.line(df_g_trend, x='Tahun', y='Total_Deforestasi_Ha', color='Provinsi', markers=True,
                           title="Laju Deforestasi Akibat Pertambangan & Sawit")
            fig_l2.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_l2, use_container_width=True)

    with tab_l3:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Narasi Anomali:</b> Jasa Budaya dalam AMDAL hanyalah mitos. Ruang hidup warga terus digusur paksa, menciptakan gelombang pengangguran baru dan represi dari aparat negara yang melindungi konsesi.</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Konflik Lahan KPA", f"{konflik_darat} Kasus", "Diluar Sektor Air")
        col2.metric("Aktor Keterlibatan Terbesar", "Perusahaan & Polisi", "Indikasi Kriminalisasi", delta_color="inverse")
        col3.metric("Skor Konflik Darat", f"{skor_sosial_1:.1f} / 10", "STATUS: DARURAT SOSIAL", delta_color="inverse")
        st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
        
        if not df_konflik.empty:
            keywords = 'air|laut|pesisir|nelayan|sungai|pulau|tailing'
            df_k = df_konflik[~df_konflik['sektor'].str.contains(keywords, case=False, na=False)].copy()
            if 'tahun' in df_k.columns:
                df_k['tahun'] = pd.to_numeric(df_k['tahun'], errors='coerce')
                df_k_trend = df_k.groupby(['tahun']).size().reset_index(name='jumlah')
                fig_l3 = px.area(df_k_trend, x='tahun', y='jumlah', title="Ledakan Konflik Perampasan Lahan Produktif", color_discrete_sequence=['#9C27B0'])
                fig_l3.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0))
                st.plotly_chart(fig_l3, use_container_width=True)

    with tab_l4:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Narasi Anomali:</b> Di saat masyarakat menanggung beban penyakit, pencemaran air, banjir, dan konflik, para pengambil kebijakan (Pemerintah Daerah & Pusat) justru terus menerbitkan ratusan ribu Hektar Izin Konsesi Baru seakan tidak ada hari esok.</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Luas IUP Baru (Sulteng & Sultra)", f"{luas_izin_sentra:,.0f} Ha", "2014-2023")
        col2.metric("Total Wilayah Dikavling", f"{df_izin['Total_Luas_Konsesi_Baru_Ha'].sum():,.0f} Ha", "Se-Sulawesi", delta_color="inverse")
        col3.metric("Skor Veto Kebijakan", f"{skor_veto_1:.1f} / 10", "STATUS: TATA KELOLA GAGAL", delta_color="inverse")
        st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
        
        if not df_izin.empty:
            df_i = df_izin.copy()
            df_i['Tahun'] = pd.to_numeric(df_i['Tahun'], errors='coerce')
            df_i['Total_Luas_Konsesi_Baru_Ha'] = pd.to_numeric(df_i['Total_Luas_Konsesi_Baru_Ha'], errors='coerce').fillna(0)
            df_i_trend = df_i.groupby(['Tahun', 'Provinsi'])['Total_Luas_Konsesi_Baru_Ha'].sum().reset_index()
            fig_l4 = px.bar(df_i_trend, x='Tahun', y='Total_Luas_Konsesi_Baru_Ha', color='Provinsi',
                           title="Laju Penerbitan Izin Konsesi Tambang Baru (Hektar)",
                           color_discrete_sequence=px.colors.qualitative.Safe)
            fig_l4.add_vline(x=2020, line_dash="dash", line_color="#FF9800", annotation_text="Pengesahan UU Minerba & Ciptaker", annotation_position="top left")
            fig_l4.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_l4, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

