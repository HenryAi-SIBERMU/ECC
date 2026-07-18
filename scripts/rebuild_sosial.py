new_sosial_calc = """
# Calculate Sosial
skor_sosial_1 = 0.0
skor_sosial_2 = 0.0
skor_sosial_3 = 0.0
konflik_darat = 0
luas_ha_dirampas = 0
jiwa_terdampak = 0
insiden_krim = 0
warga_ditangkap = 0
kasus_fpic = 0

if not df_konflik.empty:
    keywords = 'air|laut|pesisir|nelayan|sungai|pulau|tailing'
    df_konflik_darat = df_konflik[~df_konflik['sektor'].str.contains(keywords, case=False, na=False)].copy()
    konflik_darat = len(df_konflik_darat)
    
    df_konflik_darat['luas_ha'] = pd.to_numeric(df_konflik_darat['luas_ha'], errors='coerce').fillna(0)
    df_konflik_darat['dampak_masyarakat_jiwa'] = pd.to_numeric(df_konflik_darat['dampak_masyarakat_jiwa'], errors='coerce').fillna(0)
    
    luas_ha_dirampas = df_konflik_darat['luas_ha'].sum()
    jiwa_terdampak = df_konflik_darat['dampak_masyarakat_jiwa'].sum()
    
    # Skoring
    skor_sosial_2 = min(10.0, (jiwa_terdampak / 100_000) * 10) # Sangat krisis karena >> 100k
    
    # Kriminalisasi
    krim_df = df_konflik_darat[df_konflik_darat['indikasi_kriminalisasi'] == True].copy()
    krim_df['jumlah_ditangkap'] = pd.to_numeric(krim_df['jumlah_ditangkap'], errors='coerce').fillna(0)
    insiden_krim = len(krim_df)
    warga_ditangkap = krim_df['jumlah_ditangkap'].sum()
    skor_sosial_3 = min(10.0, (insiden_krim / 50) * 10) # 50 insiden aparat sdh krisis absolut

if not df_konflik_fpic.empty:
    kasus_fpic = len(df_konflik_fpic)
    skor_sosial_1 = min(10.0, (kasus_fpic / 5) * 10) # Hanya butuh 5 kasus investigasi utk membuktikan pola

skor_akumulasi_sosial = (skor_sosial_1 + skor_sosial_2 + skor_sosial_3) / 3
"""

new_sosial_hero = """
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
        <p style="color:#E0E0E0; font-size:0.9rem;">Alur penindasan terbukti jelas: Persetujuan dimanipulasi, ruang hidup jutaan hektar dirampas, dan penolakan dibungkam dengan bui.</p>
        <div style="background-color: #1A202C; padding: 15px; border-radius: 8px; margin-top: 15px; text-align: center; border: 1px solid #9C27B0;">
            <div style="font-size: 11px; color: #BDC3C7; text-transform: uppercase; letter-spacing: 1px;">Skor Kerusakan Sosial</div>
            <div style="font-size: 32px; font-weight: 800; color: #9C27B0; line-height: 1.2;">{skor_akumulasi_sosial:.1f} <span style="font-size: 16px;">/ 10</span></div>
            <div style="font-size: 11px; color: #9C27B0; margin-top: 5px; font-weight: bold;">STATUS: KRISIS KEMANUSIAAN</div>
        </div>
        <div style="background:#8E44AD; color:white; padding:5px 10px; border-radius:5px; font-weight:bold; text-align:center; margin-top:15px;">
            VONIS: Ilusi Kedaulatan Ruang Warga
        </div>
    </div>
    ''', unsafe_allow_html=True)

with colD2:
    tab_s1, tab_s2, tab_s3 = st.tabs(["Fase 1: Manipulasi Persetujuan", "Fase 2: Perampasan Ruang Hidup", "Fase 3: Kriminalisasi Warga"])
    
    with tab_s1:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Narasi Anomali:</b> 'Persetujuan Warga' hanyalah stempel karet. Data investigasi Konsorsium Pembaruan Agraria membuktikan perusahaan memanipulasi persetujuan (FPIC) sejak fase sosialisasi AMDAL.</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Kasus Manipulasi FPIC", f"{kasus_fpic} Investigasi", "Sulawesi (KPA)")
        col2.metric("Status Dokumen", "Persetujuan Palsu", "Modus Perusahaan", delta_color="inverse")
        col3.metric("Skor Penipuan Publik", f"{skor_sosial_1:.1f} / 10", "STATUS: AMDAL BODONG", delta_color="inverse")
        st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
        
        if not df_konflik_fpic.empty:
            df_fpic_view = df_konflik_fpic[['tahun', 'nama_perusahaan', 'indikasi_fpic', 'judul']].copy()
            # Replace True/False strings if any, format to make it readable
            df_fpic_view['indikasi_fpic'] = df_fpic_view['indikasi_fpic'].replace({'True': 'Terbukti Melanggar', 'False': 'Investigasi Berjalan'})
            st.dataframe(df_fpic_view, use_container_width=True, hide_index=True)
            with st.expander("Tampilkan Data Mentah FPIC (KPA/TanahKita)"):
                st.dataframe(df_konflik_fpic, use_container_width=True)

    with tab_s2:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Narasi Anomali:</b> Setelah izin keluar lewat manipulasi, perampasan paksa terjadi. Ruang hidup warga menyusut drastis, memicu letusan konflik yang berdampak pada ratusan ribu korban jiwa.</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Lahan Dirampas", f"{luas_ha_dirampas/1000000:.1f} Juta Ha", f"{konflik_darat} Kasus Konflik", delta_color="inverse")
        col2.metric("Korban Terdampak", f"{jiwa_terdampak:,.0f} Jiwa", "Warga Kehilangan Tanah", delta_color="inverse")
        col3.metric("Skor Genosida Ruang", f"{skor_sosial_2:.1f} / 10", "STATUS: KRISIS AGRARIA", delta_color="inverse")
        st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
        
        if not df_konflik.empty:
            df_k_darat = df_konflik[~df_konflik['sektor'].str.contains('air|laut|pesisir|nelayan|sungai|pulau|tailing', case=False, na=False)].copy()
            if 'tahun' in df_k_darat.columns:
                df_k_darat['tahun'] = pd.to_numeric(df_k_darat['tahun'], errors='coerce')
                df_k_trend = df_k_darat.groupby(['tahun']).size().reset_index(name='jumlah')
                fig_s1 = px.area(df_k_trend, x='tahun', y='jumlah', title="Frekuensi Letusan Konflik Perampasan Lahan Tahunan", color_discrete_sequence=['#9C27B0'])
                fig_s1.add_hline(y=10, line_dash="dash", line_color="#E74C3C", annotation_text="Batas Darurat Nasional (10 Konflik/Thn)", annotation_position="top left")
                fig_s1.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0))
                st.plotly_chart(fig_s1, use_container_width=True)

    with tab_s3:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Narasi Anomali:</b> Di fase akhir, ketika warga melakukan penolakan yang sah atas perampasan, negara tidak hadir melindungi, melainkan mengirim aparat untuk memenjarakan mereka.</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Insiden Kriminalisasi", f"{insiden_krim} Kejadian", "Melibatkan Aparat", delta_color="inverse")
        col2.metric("Warga Dipenjara", f"{warga_ditangkap:.0f} Orang", "Ditahan Paksa", delta_color="inverse")
        col3.metric("Skor Represi", f"{skor_sosial_3:.1f} / 10", "STATUS: KEKERASAN NEGARA", delta_color="inverse")
        st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
        
        if not df_konflik.empty:
            krim_df = df_k_darat[df_k_darat['indikasi_kriminalisasi'] == True].copy()
            krim_df['jumlah_ditangkap'] = pd.to_numeric(krim_df['jumlah_ditangkap'], errors='coerce').fillna(0)
            if 'tahun' in krim_df.columns:
                krim_df['tahun'] = pd.to_numeric(krim_df['tahun'], errors='coerce')
                krim_trend = krim_df.groupby('tahun').size().reset_index(name='jumlah')
                fig_s2 = px.bar(krim_trend, x='tahun', y='jumlah', title="Tren Insiden Kriminalisasi & Kekerasan Terhadap Warga", color_discrete_sequence=['#E74C3C'])
                fig_s2.add_hline(y=5, line_dash="dash", line_color="#F1C40F", annotation_text="Batas Toleransi Demokrasi", annotation_position="top left")
                fig_s2.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0))
                st.plotly_chart(fig_s2, use_container_width=True)
                with st.expander("Tampilkan Data Indikasi Kriminalisasi"):
                    st.dataframe(krim_df[['tahun', 'judul', 'sektor', 'jumlah_ditangkap', 'jumlah_luka']], use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)
"""

import sys

with open('pages/6_Audit_D3TLH.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 1. Modify the calculation for Sosial
calc_start = -1
calc_end = -1
for i, line in enumerate(lines):
    if "skor_sosial_1 = 0" in line and "konflik_darat = 0" in lines[i+1]:
        calc_start = i
        break

for i in range(calc_start, len(lines)):
    if "luas_izin_sentra = 0" in lines[i]:
        calc_end = i - 1
        break

if calc_start != -1 and calc_end != -1:
    del lines[calc_start:calc_end]
    lines.insert(calc_start, new_sosial_calc + "\\n")
else:
    print("Failed to find sosial calc section", calc_start, calc_end)

# Re-read lines since array length changed
lines_str = "".join(lines)

# 2. Modify the Hero Section
hero_start_idx = lines_str.find("# ---------------------------------------------------------\\n# D. MITOS KEDAULATAN RUANG VS KONFLIK SOSIAL (DAYA DUKUNG SOSIAL)")
if hero_start_idx == -1:
    print("Failed to find hero section start")
    sys.exit(1)

hero_end_idx = lines_str.find("# ---------------------------------------------------------\\n# E. MITOS TATA KELOLA VS OBRAL IZIN (VETO KEBIJAKAN)")
if hero_end_idx == -1:
    # try alternative finding
    hero_end_idx = lines_str.find("# ---------------------------------------------------------\n# E. MITOS TATA KELOLA VS OBRAL IZIN")
    if hero_end_idx == -1:
        print("Failed to find hero section end")
        sys.exit(1)

new_lines_str = lines_str[:hero_start_idx] + new_sosial_hero + "\n" + lines_str[hero_end_idx:]

with open('pages/6_Audit_D3TLH.py', 'w', encoding='utf-8') as f:
    f.write(new_lines_str)
print("Successfully modified pages/6_Audit_D3TLH.py")
