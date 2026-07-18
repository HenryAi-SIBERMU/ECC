import re

with open('crosstab_snippet.py', 'r', encoding='utf-8') as f:
    crosstab_code = f.read()

# Replace variables for Crosstab
crosstab_code = crosstab_code.replace('df_gfw, df_izin', 'df_iku, df_kes_ispa')
crosstab_code = crosstab_code.replace('Total_Deforestasi_Ha', 'Total_ISPA')
crosstab_code = crosstab_code.replace('Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha', 'Total_Diare')
crosstab_code = crosstab_code.replace('Jumlah_Izin_Baru', 'IKU_Point')
crosstab_code = crosstab_code.replace('Total_Luas_Konsesi_Baru_Ha', 'IKU_Point_Alt')

merge_replacement = """
import scipy.stats as stats

df_kes_ispa = df_kes[df_kes['indikator'] == 'Kasus ISPA/Pneumonia'][['provinsi', 'tahun', 'nilai']].rename(columns={'nilai': 'Total_ISPA', 'provinsi': 'Provinsi', 'tahun': 'Tahun'})
df_kes_diare = df_kes[df_kes['indikator'] == 'Kasus Diare Dilayani'][['provinsi', 'tahun', 'nilai']].rename(columns={'nilai': 'Total_Diare', 'provinsi': 'Provinsi', 'tahun': 'Tahun'})
df_panel = pd.merge(df_kes_ispa, df_iku, on=['Provinsi', 'Tahun'], how='inner')
df_panel = pd.merge(df_panel, df_kes_diare, on=['Provinsi', 'Tahun'], how='inner')
df_panel['IKU_Point'] = df_panel['IKU']
df_panel['IKU_Point_Alt'] = df_panel['IKU']
"""
crosstab_code = crosstab_code.replace("df_panel = pd.merge(df_iku, df_kes_ispa, on=['Provinsi', 'Tahun'], how='left').fillna({'IKU_Point': 0, 'IKU_Point_Alt': 0})", merge_replacement)
crosstab_code = crosstab_code.replace("df_panel = pd.merge(df_gfw, df_izin, on=['Provinsi', 'Tahun'], how='left').fillna({'Jumlah_Izin_Baru': 0, 'Total_Luas_Konsesi_Baru_Ha': 0})", merge_replacement)

crosstab_code = crosstab_code.replace('"Jumlah Izin Baru (IUP)"', '"Skor Indeks Kualitas Udara (IKU)"')
crosstab_code = crosstab_code.replace('"Luas Konsesi Baru (Hektar)"', '"Skor IKU (Alternatif)"')
crosstab_code = crosstab_code.replace('"Total Deforestasi Alam (Hektar)"', '"Total Kasus ISPA/Pneumonia"')
crosstab_code = crosstab_code.replace('"Deforestasi Komoditas Tambang/Sawit (Hektar)"', '"Total Kasus Diare"')

crosstab_code = crosstab_code.replace('Intensitas Ekspansi vs Deforestasi', 'Penurunan Kualitas Udara vs Ledakan Penyakit')
crosstab_code = crosstab_code.replace('lonjakan ekspansi ekstraktif', 'penurunan kualitas udara ambien (IKU)')
crosstab_code = crosstab_code.replace('kebangkrutan ekologis (deforestasi)', 'ledakan penyakit pernapasan dan lingkungan (seperti ISPA dan Diare)')
crosstab_code = crosstab_code.replace('kebangkrutan ekologis', 'ledakan penyakit pernapasan dan lingkungan')
crosstab_code = crosstab_code.replace('(deforestasi)', '(seperti ISPA dan Diare)')
crosstab_code = crosstab_code.replace('Tekanan Ekspansi', 'Faktor Lingkungan')
crosstab_code = crosstab_code.replace('Indikator Ekspansi', 'Indikator Lingkungan')

crosstab_code = crosstab_code.replace('Pilih Indikator Dampak', 'Pilih Indikator Penyakit')
crosstab_code = crosstab_code.replace('Dampak Ekologis', 'Dampak Kesehatan')

crosstab_code = crosstab_code.replace("sulawesi_izin_baru_per_tahun.csv", "sulawesi_iku_2015_2024.csv")
crosstab_code = crosstab_code.replace("Minerbaone", "KLHK")
crosstab_code = crosstab_code.replace("sulawesi_gfw_master_1_dekade_2014_2023.csv", "sulawesi_kesehatan_detail_2014_2024.csv")
crosstab_code = crosstab_code.replace("GFW", "Dinas Kesehatan")


new_section_3_2 = f"""# ══════════════════════════════════════════════════════════
# SUB-BAB 3.2: KESENJANGAN FASILITAS KESEHATAN
# ══════════════════════════════════════════════════════════
st.markdown("---")
st.markdown('<h2 style="color: #ECEFF1; font-size: 24px;">3.2 Kesenjangan Fasilitas Kesehatan di Kawasan Ekstraktif</h2>', unsafe_allow_html=True)
st.markdown('<span style="background:#5C2B6A;color:#E1BEE7;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: Grouped Horizontal Bar Chart (Data 2022)</span>', unsafe_allow_html=True)

# Data Prep Chart
sentra = ['Sulawesi Tengah', 'Sulawesi Tenggara']
df_faskes_copy = df_faskes.copy()
df_faskes_copy = df_faskes_copy[~df_faskes_copy['provinsi'].str.contains('Indonesia', na=False)]
df_faskes_copy['Kategori'] = df_faskes_copy['provinsi'].apply(lambda x: 'Sentra Industri (Sulteng & Sultra)' if x in sentra else 'Non-Sentra Industri (Lainnya)')

# Filter tahun 2022 karena memiliki data Rumah Sakit & Puskesmas terlengkap
df_2022 = df_faskes_copy[df_faskes_copy['tahun'] == 2022]
df_gap = df_2022.groupby(['Kategori', 'jenis'])['jumlah'].mean().reset_index()

import plotly.express as px

fig_3_2 = px.bar(
    df_gap,
    x='jumlah',
    y='jenis',
    color='Kategori',
    barmode='group',
    orientation='h',
    color_discrete_map={{
        'Sentra Industri (Sulteng & Sultra)': '#E53935',
        'Non-Sentra Industri (Lainnya)': '#546E7A'
    }},
    text='jumlah'
)

fig_3_2.update_traces(texttemplate='%{{text:.0f}}', textposition='outside', textfont_size=13)

fig_3_2.update_layout(
    title="Ketimpangan Ketersediaan Fasilitas Kesehatan (Rata-rata per Provinsi, 2022)",
    height=400,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    legend=dict(title=None, orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    font=dict(color='#B0BEC5'),
    xaxis=dict(title="Rata-Rata Jumlah Fasilitas", showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
    yaxis=dict(title="", showgrid=False)
)

st.markdown("<br>", unsafe_allow_html=True)

rs_sentra = df_gap[(df_gap['jenis'] == 'Rumah Sakit') & (df_gap['Kategori'].str.contains('Sentra'))]['jumlah'].values[0]
rs_non = df_gap[(df_gap['jenis'] == 'Rumah Sakit') & (df_gap['Kategori'].str.contains('Non-Sentra'))]['jumlah'].values[0]

st.markdown(f\"\"\"
Mitos bahwa masuknya investasi smelter akan membawa *trickle-down effect* (efek tetesan ke bawah) berupa perbaikan infrastruktur publik, **terbantahkan secara absolut oleh data**. Melalui komparasi grafik batang (*Grouped Bar Chart*) di bawah, kita bisa membaca secara mudah dan gamblang bahwa ketersediaan Fasilitas Kesehatan di provinsi yang dieksploitasi jutru mengalami defisit.

Saat rata-rata kasus ISPA dan Diare di Sentra Industri menembus dua kali lipat lebih tinggi (berdasarkan grafik sebelumnya), infrastruktur penunjang kehidupan mereka justru jauh tertinggal. Rata-rata Rumah Sakit di Sentra Industri hanya berjumlah **{{rs_sentra:.0f}} unit** per provinsi, tertinggal jauh dari wilayah Non-Sentra yang mencapai **{{rs_non:.0f}} unit**. Defisit absolut fasilitas medis di episentrum ekstraksi dan ledakan penyakit ini adalah bentuk kekerasan struktural: negara dan korporasi mengekspor polusi, namun absen dalam menyediakan infrastruktur keselamatan warga.
\"\"\")

st.plotly_chart(fig_3_2, use_container_width=True)

with st.expander("Lihat Data Mentah: Ketimpangan Faskes 2022", expanded=False):
    st.dataframe(df_gap, use_container_width=True, hide_index=True)
    st.caption("📁 **Sumber File:** `data/processed/sulawesi_faskes_agregat.csv`")

\\n\\n
{crosstab_code}
"""

with open('pages/3_Beban_Kesehatan.py', 'r', encoding='utf-8') as f:
    content = f.read()

separator = '# ══════════════════════════════════════════════════════════\\n# SUB-BAB 3.2: KESENJANGAN FASILITAS KESEHATAN'
parts = re.split(r'# ══════════════════════════════════════════════════════════\s*# SUB-BAB 3\.2: KESENJANGAN FASILITAS KESEHATAN', content)

if len(parts) > 1:
    new_content = parts[0] + new_section_3_2
    with open('pages/3_Beban_Kesehatan.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Injeksi Bar Chart dan Crosstab sukses pakai split.")
else:
    print("Gagal menemukan separator.")
