new_code = """
# ---------------------------------------------------------
# C. MITOS DEFORESTASI VS BENCANA ALAM (DAYA DUKUNG LAHAN)
# ---------------------------------------------------------
colC1, colC2 = st.columns([1, 2])
with colC1:
    st.markdown(f'''
    <div style="background:#2C3E50; padding:20px; border-radius:10px; border-left:5px solid #FF9800; height:100%;">
        <h4 style="color:#FFF; margin-top:0;">Mitos D3TLH: Daya Dukung Lahan</h4>
        <p style="color:#BDC3C7; font-size:0.9rem;">"Daya dukung lahan dan tata air tanah dinilai aman secara matematis karena rasio ekoregion hutan dianggap masih mencukupi."</p>
        <hr style="border-color:#34495E;">
        <h4 style="color:#FF9800;">Fakta Forensik ECC:</h4>
        <p style="color:#E0E0E0; font-size:0.9rem;">Hancurnya sabuk hijau alam memicu rentetan bencana hidrometeorologi parah di lingkar tambang.</p>
        <div style="background-color: #1A202C; padding: 15px; border-radius: 8px; margin-top: 15px; text-align: center; border: 1px solid #FF9800;">
            <div style="font-size: 11px; color: #BDC3C7; text-transform: uppercase; letter-spacing: 1px;">Skor Kerusakan Lahan</div>
            <div style="font-size: 32px; font-weight: 800; color: #FF9800; line-height: 1.2;">{skor_akumulasi_lahan:.1f} <span style="font-size: 16px;">/ 10</span></div>
            <div style="font-size: 11px; color: #FF9800; margin-top: 5px; font-weight: bold;">STATUS: KRISIS RUANG DARAT</div>
        </div>
        <div style="background:#E67E22; color:white; padding:5px 10px; border-radius:5px; font-weight:bold; text-align:center; margin-top:15px;">
            VONIS: Kegagalan Mengukur Efek Domino Lanskap
        </div>
    </div>
    ''', unsafe_allow_html=True)

with colC2:
    tab_l1, tab_l2 = st.tabs(["Bencana Banjir & Longsor", "Deforestasi Primer"])
    
    with tab_l1:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Narasi Anomali:</b> Data BNPB membuktikan bahwa klaim 'mitigasi bencana' dalam AMDAL sama sekali tidak terbukti di lapangan.</div>", unsafe_allow_html=True)
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
            with st.expander("Tampilkan Data Mentah (BNPB)"):
                st.dataframe(df_bencana, use_container_width=True)

    with tab_l2:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Narasi Anomali:</b> Hutan primer yang berfungsi sebagai jasa penyediaan air dan penyerap karbon ditebang habis atas nama IUP.</div>", unsafe_allow_html=True)
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
            with st.expander("Tampilkan Data Mentah (Global Forest Watch)"):
                st.dataframe(df_gfw, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# D. MITOS KEDAULATAN RUANG VS KONFLIK SOSIAL (DAYA DUKUNG SOSIAL)
# ---------------------------------------------------------
colD1, colD2 = st.columns([1, 2])
with colD1:
    st.markdown(f'''
    <div style="background:#2C3E50; padding:20px; border-radius:10px; border-left:5px solid #9C27B0; height:100%;">
        <h4 style="color:#FFF; margin-top:0;">Mitos D3TLH: Daya Dukung Sosial</h4>
        <p style="color:#BDC3C7; font-size:0.9rem;">"Status kawasan dialokasikan untuk peruntukan tambang dengan klaim bahwa masyarakat telah memberikan persetujuan (FPIC) dalam sosialisasi amdal."</p>
        <hr style="border-color:#34495E;">
        <h4 style="color:#9C27B0;">Fakta Forensik ECC:</h4>
        <p style="color:#E0E0E0; font-size:0.9rem;">Eskalasi kasus konflik perampasan lahan produktif dan represi aparat membuktikan persetujuan warga dimanipulasi.</p>
        <div style="background-color: #1A202C; padding: 15px; border-radius: 8px; margin-top: 15px; text-align: center; border: 1px solid #9C27B0;">
            <div style="font-size: 11px; color: #BDC3C7; text-transform: uppercase; letter-spacing: 1px;">Skor Kerusakan Sosial</div>
            <div style="font-size: 32px; font-weight: 800; color: #9C27B0; line-height: 1.2;">{skor_akumulasi_sosial:.1f} <span style="font-size: 16px;">/ 10</span></div>
            <div style="font-size: 11px; color: #9C27B0; margin-top: 5px; font-weight: bold;">STATUS: DARURAT AGRARIA</div>
        </div>
        <div style="background:#8E44AD; color:white; padding:5px 10px; border-radius:5px; font-weight:bold; text-align:center; margin-top:15px;">
            VONIS: Ilusi Jasa Budaya & Kedaulatan Ruang
        </div>
    </div>
    ''', unsafe_allow_html=True)

with colD2:
    tab_s1, tab_s2 = st.tabs(["Ledakan Konflik Perampasan Lahan", "Kriminalisasi Aparat"])
    
    with tab_s1:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Narasi Anomali:</b> Jasa Budaya dalam AMDAL hanyalah mitos. Ruang hidup warga terus digusur paksa untuk tambang, menciptakan letusan konflik tak berkesudahan.</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Konflik Lahan", f"{konflik_darat} Kasus", "Diluar Sektor Air")
        col2.metric("Sektor Terbesar", "Tambang & Kebun", "Perampasan Ruang", delta_color="inverse")
        col3.metric("Skor Konflik Darat", f"{skor_sosial_1:.1f} / 10", "STATUS: DARURAT SOSIAL", delta_color="inverse")
        st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
        
        if not df_konflik.empty:
            keywords = 'air|laut|pesisir|nelayan|sungai|pulau|tailing'
            df_k = df_konflik[~df_konflik['sektor'].str.contains(keywords, case=False, na=False)].copy()
            if 'tahun' in df_k.columns:
                df_k['tahun'] = pd.to_numeric(df_k['tahun'], errors='coerce')
                df_k_trend = df_k.groupby(['tahun']).size().reset_index(name='jumlah')
                fig_s1 = px.area(df_k_trend, x='tahun', y='jumlah', title="Frekuensi Letusan Konflik Perampasan Lahan Produktif", color_discrete_sequence=['#9C27B0'])
                fig_s1.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0))
                st.plotly_chart(fig_s1, use_container_width=True)
                with st.expander("Tampilkan Data Mentah Konflik Agraria (KPA/TanahKita)"):
                    st.dataframe(df_k, use_container_width=True)

    with tab_s2:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Narasi Anomali:</b> Alih-alih mendapatkan pelindungan dari pemerintah, penolakan warga yang sah justru dibungkam dengan represi, kriminalisasi, penangkapan, hingga kekerasan yang menimbulkan luka dan korban jiwa.</div>", unsafe_allow_html=True)
        
        if not df_konflik.empty:
            krim_df = df_konflik[df_konflik['indikasi_kriminalisasi'] == True].copy()
            krim_df['jumlah_ditangkap'] = pd.to_numeric(krim_df['jumlah_ditangkap'], errors='coerce').fillna(0)
            krim_df['jumlah_luka'] = pd.to_numeric(krim_df['jumlah_luka'], errors='coerce').fillna(0)
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Insiden Kriminalisasi", f"{len(krim_df)} Kejadian", "Melibatkan Aparat", delta_color="inverse")
            c2.metric("Warga Ditangkap", f"{krim_df['jumlah_ditangkap'].sum():.0f} Orang", "Ditahan Bebas", delta_color="inverse")
            c3.metric("Warga Luka-luka", f"{krim_df['jumlah_luka'].sum():.0f} Orang", "Korban Represi", delta_color="inverse")
            st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
            
            if 'tahun' in krim_df.columns:
                krim_df['tahun'] = pd.to_numeric(krim_df['tahun'], errors='coerce')
                krim_trend = krim_df.groupby('tahun').size().reset_index(name='jumlah')
                fig_s2 = px.bar(krim_trend, x='tahun', y='jumlah', title="Tren Kriminalisasi & Kekerasan Terhadap Warga", color_discrete_sequence=['#E74C3C'])
                fig_s2.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0))
                st.plotly_chart(fig_s2, use_container_width=True)
                with st.expander("Tampilkan Data Indikasi Kriminalisasi"):
                    st.dataframe(krim_df[['tahun', 'judul', 'sektor', 'jumlah_ditangkap', 'jumlah_luka']], use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# E. MITOS TATA KELOLA VS OBRAL IZIN (VETO KEBIJAKAN)
# ---------------------------------------------------------
colE1, colE2 = st.columns([1, 2])
with colE1:
    st.markdown(f'''
    <div style="background:#2C3E50; padding:20px; border-radius:10px; border-left:5px solid #4CAF50; height:100%;">
        <h4 style="color:#FFF; margin-top:0;">Mitos D3TLH: Veto Kebijakan</h4>
        <p style="color:#BDC3C7; font-size:0.9rem;">"D3TLH dan Dokumen Lingkungan dianggap sebagai alat pengunci tata ruang yang akan membatasi penerbitan IUP jika daya tampung ekologis sudah kritis."</p>
        <hr style="border-color:#34495E;">
        <h4 style="color:#4CAF50;">Fakta Forensik ECC:</h4>
        <p style="color:#E0E0E0; font-size:0.9rem;">Lonjakan fantastis penerbitan IUP Nikel baru justru terjadi di saat dan di tempat indikator kesehatan & ekologi menjerit merah.</p>
        <div style="background-color: #1A202C; padding: 15px; border-radius: 8px; margin-top: 15px; text-align: center; border: 1px solid #4CAF50;">
            <div style="font-size: 11px; color: #BDC3C7; text-transform: uppercase; letter-spacing: 1px;">Skor Pelanggaran Tata Kelola</div>
            <div style="font-size: 32px; font-weight: 800; color: #4CAF50; line-height: 1.2;">{skor_akumulasi_veto:.1f} <span style="font-size: 16px;">/ 10</span></div>
            <div style="font-size: 11px; color: #4CAF50; margin-top: 5px; font-weight: bold;">STATUS: REGULATORY CAPTURE</div>
        </div>
        <div style="background:#27AE60; color:white; padding:5px 10px; border-radius:5px; font-weight:bold; text-align:center; margin-top:15px;">
            VONIS: Kegagalan Tata Kelola Negara
        </div>
    </div>
    ''', unsafe_allow_html=True)

with colE2:
    tab_v1, tab_v2 = st.tabs(["Lonjakan IUP di Tengah Krisis", "Proporsi Ruang Izin"])
    
    with tab_v1:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Narasi Anomali:</b> Di saat masyarakat menanggung beban penyakit ISPA, pencemaran laut, banjir, dan represi, Kementerian terkait justru terus melelang wilayah dan mencetak ratusan ribu Hektar Izin Konsesi Baru tanpa mengaktifkan hak Veto Keselamatan.</div>", unsafe_allow_html=True)
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
            fig_v1 = px.bar(df_i_trend, x='Tahun', y='Total_Luas_Konsesi_Baru_Ha', color='Provinsi',
                           title="Laju Obral Perizinan Konsesi Tambang Baru (Hektar)",
                           color_discrete_sequence=px.colors.qualitative.Safe)
            fig_v1.add_vline(x=2020, line_dash="dash", line_color="#FF9800", annotation_text="Pengesahan UU Minerba & Ciptaker", annotation_position="top left")
            fig_v1.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_v1, use_container_width=True)
            with st.expander("Tampilkan Data Mentah Izin Konsesi Baru (ESDM)"):
                st.dataframe(df_izin, use_container_width=True)

    with tab_v2:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Kavling Ruang Hidup:</b> Ratusan perusahaan secara de facto menguasai daratan Sulawesi, menggeser kedaulatan ruang warga negara ke tangan entitas bisnis.</div>", unsafe_allow_html=True)
        if not df_izin.empty:
            df_i_agg = df_i.groupby(['Provinsi'])['Jumlah_Izin_Baru'].sum().reset_index()
            fig_v2 = px.pie(df_i_agg, values='Jumlah_Izin_Baru', names='Provinsi', hole=0.4,
                           title="Proporsi Jumlah Penerbitan Izin Tambang Baru per Provinsi",
                           color_discrete_sequence=px.colors.qualitative.Prism)
            fig_v2.update_traces(textposition='inside', textinfo='percent+label')
            fig_v2.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_v2, use_container_width=True)

st.markdown("<br><hr style='border: 1px dashed #444;'><br>", unsafe_allow_html=True)
"""

with open('pages/6_Audit_D3TLH.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1

for i, line in enumerate(lines):
    if "# C. MITOS DEFORESTASI VS BENCANA ALAM" in line:
        start_idx = i - 1
        break

for i, line in enumerate(lines):
    if "# SECTION 4: KESIMPULAN & REKOMENDASI (VETO KESELAMATAN)" in line:
        end_idx = i - 1
        break

if start_idx != -1 and end_idx != -1:
    del lines[start_idx:end_idx]
    lines.insert(start_idx, new_code + "\n")
    with open('pages/6_Audit_D3TLH.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("Success")
else:
    print("Failed to find boundaries", start_idx, end_idx)
