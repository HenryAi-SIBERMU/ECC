new_lahan_script = """
# Calculate Lahan 3 & 4
skor_lahan_3 = 0.0
skor_lahan_4 = 0.0
lindung_hilang = 0
tambang_driver_ha = 0

if not df_gfw_lindung.empty:
    df_l = df_gfw_lindung[df_gfw_lindung['Provinsi'].isin(['Sulawesi Tengah', 'Sulawesi Tenggara'])].copy()
    df_l['Luas_Hilang_Kawasan_Lindung_Ha'] = pd.to_numeric(df_l['Luas_Hilang_Kawasan_Lindung_Ha'], errors='coerce').fillna(0)
    lindung_hilang = df_l['Luas_Hilang_Kawasan_Lindung_Ha'].sum()
    skor_lahan_3 = min(10.0, (lindung_hilang / 100_000) * 10) # Sangat ketat karena ini kawasan lindung

if not df_gfw_driver.empty:
    df_d = df_gfw_driver[df_gfw_driver['Provinsi'].isin(['Sulawesi Tengah', 'Sulawesi Tenggara'])].copy()
    df_d['Luas_Deforestasi_Ha'] = pd.to_numeric(df_d['Luas_Deforestasi_Ha'], errors='coerce').fillna(0)
    tambang_driver = df_d[df_d['Faktor_Pendorong'] == 'Deforestasi Komoditas (Tambang/Sawit)']
    tambang_driver_ha = tambang_driver['Luas_Deforestasi_Ha'].sum()
    skor_lahan_4 = min(10.0, (tambang_driver_ha / 250_000) * 10)

skor_akumulasi_lahan = (skor_lahan_1 + skor_lahan_2 + skor_lahan_3 + skor_lahan_4) / 4
"""

new_hero_script = """
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
        <p style="color:#E0E0E0; font-size:0.9rem;">Hancurnya sabuk hijau alam memicu rentetan bencana hidrometeorologi parah di lingkar tambang, menabrak batas fungsi kawasan lindung.</p>
        <div style="background-color: #1A202C; padding: 15px; border-radius: 8px; margin-top: 15px; text-align: center; border: 1px solid #FF9800;">
            <div style="font-size: 11px; color: #BDC3C7; text-transform: uppercase; letter-spacing: 1px;">Skor Kerusakan Lahan</div>
            <div style="font-size: 32px; font-weight: 800; color: #FF9800; line-height: 1.2;">{skor_akumulasi_lahan:.1f} <span style="font-size: 16px;">/ 10</span></div>
            <div style="font-size: 11px; color: #FF9800; margin-top: 5px; font-weight: bold;">STATUS: KRISIS RUANG DARAT</div>
        </div>
        <div style="background:#E67E22; color:white; padding:5px 10px; border-radius:5px; font-weight:bold; text-align:center; margin-top:15px;">
            VONIS: Kegagalan Menjaga Fungsi Lanskap
        </div>
    </div>
    ''', unsafe_allow_html=True)

with colC2:
    tab_l1, tab_l2, tab_l3, tab_l4 = st.tabs(["Bencana Banjir & Longsor", "Deforestasi Primer", "Pelanggaran Kawasan Lindung", "Aktor Deforestasi"])
    
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
            fig_l1.add_hline(y=50, line_dash="dash", line_color="#E74C3C", annotation_text="Batas Darurat Bencana (50/Tahun)", annotation_position="top left")
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
            fig_l2.add_hline(y=25000, line_dash="dash", line_color="#E74C3C", annotation_text="Batas Kritis Tahunan (25.000 Ha)", annotation_position="bottom right")
            fig_l2.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_l2, use_container_width=True)
            with st.expander("Tampilkan Data Mentah (Global Forest Watch)"):
                st.dataframe(df_gfw, use_container_width=True)

    with tab_l3:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Narasi Anomali:</b> Sangat mematikan! Dari 1,14 Juta Ha deforestasi di Sentra Nikel, hampir seluruhnya identik dengan perambahan <b>Kawasan Lindung / Protected Areas (IUCN)</b>. Ini adalah pelanggaran D3TLH paling fundamental.</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Kawasan Lindung Hilang", f"{lindung_hilang:,.0f} Ha", "Sulteng & Sultra")
        col2.metric("Total Kerusakan Sulawesi", f"{df_gfw_lindung['Luas_Hilang_Kawasan_Lindung_Ha'].astype(float).sum():,.0f} Ha", "Protected Areas", delta_color="inverse")
        col3.metric("Skor Pelanggaran Zonasi", f"{skor_lahan_3:.1f} / 10", "STATUS: ZONASI DITABRAK", delta_color="inverse")
        st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
        
        if not df_gfw_lindung.empty:
            df_gl = df_gfw_lindung.copy()
            df_gl['Tahun'] = pd.to_numeric(df_gl['Tahun'], errors='coerce')
            df_gl['Luas_Hilang_Kawasan_Lindung_Ha'] = pd.to_numeric(df_gl['Luas_Hilang_Kawasan_Lindung_Ha'], errors='coerce').fillna(0)
            df_gl_trend = df_gl.groupby(['Tahun', 'Provinsi'])['Luas_Hilang_Kawasan_Lindung_Ha'].sum().reset_index()
            fig_l3 = px.area(df_gl_trend, x='Tahun', y='Luas_Hilang_Kawasan_Lindung_Ha', color='Provinsi',
                           title="Tren Perambahan Deforestasi di Kawasan Lindung (Protected Areas)")
            fig_l3.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_l3, use_container_width=True)
            with st.expander("Tampilkan Data Mentah Kawasan Lindung (GFW)"):
                st.dataframe(df_gfw_lindung, use_container_width=True)

    with tab_l4:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Narasi Anomali:</b> Data mematahkan mitos bahwa perambahan dilakukan oleh warga lokal. Penyebab (Driver) utama deforestasi ini dikendalikan oleh <b>Ekstraksi Komoditas</b> (Izin Tambang & Perkebunan Skala Besar).</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Deforestasi Komoditas", f"{tambang_driver_ha:,.0f} Ha", "Sulteng & Sultra")
        col2.metric("Aktor Pendorong Utama", "Tambang & Sawit", "Bukan Pertanian Warga", delta_color="normal")
        col3.metric("Skor Dominasi Ekstraktif", f"{skor_lahan_4:.1f} / 10", "STATUS: MONOPOLI KONSESI", delta_color="inverse")
        st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
        
        if not df_gfw_driver.empty:
            df_gd = df_gfw_driver.copy()
            df_gd['Luas_Deforestasi_Ha'] = pd.to_numeric(df_gd['Luas_Deforestasi_Ha'], errors='coerce').fillna(0)
            df_gd_agg = df_gd.groupby('Faktor_Pendorong')['Luas_Deforestasi_Ha'].sum().reset_index()
            fig_l4 = px.pie(df_gd_agg, values='Luas_Deforestasi_Ha', names='Faktor_Pendorong', hole=0.3,
                           title="Penyebab Utama Kehilangan Hutan (Drivers of Deforestation)",
                           color_discrete_sequence=px.colors.qualitative.Bold)
            fig_l4.update_traces(textposition='inside', textinfo='percent+label')
            fig_l4.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_l4, use_container_width=True)
            with st.expander("Tampilkan Data Mentah Drivers (GFW)"):
                st.dataframe(df_gfw_driver, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)
"""

import sys

with open('pages/6_Audit_D3TLH.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 1. Modify the calculation for Lahan
calc_start = -1
calc_end = -1
for i, line in enumerate(lines):
    if "skor_akumulasi_lahan = (skor_lahan_1 + skor_lahan_2) / 2" in line:
        calc_start = i
        calc_end = i + 1
        break

if calc_start != -1:
    lines[calc_start] = new_lahan_script + "\\n"

# 2. Modify the Hero Section
hero_start = -1
hero_end = -1
for i, line in enumerate(lines):
    if "# C. MITOS DEFORESTASI VS BENCANA ALAM" in line:
        hero_start = i - 1
        break

for i, line in enumerate(lines):
    if "# D. MITOS KEDAULATAN RUANG VS KONFLIK SOSIAL" in line:
        hero_end = i - 1
        break

if hero_start != -1 and hero_end != -1:
    del lines[hero_start:hero_end]
    lines.insert(hero_start, new_hero_script + "\\n")
else:
    print("Failed to find hero section")
    sys.exit(1)

with open('pages/6_Audit_D3TLH.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Successfully modified pages/6_Audit_D3TLH.py")
