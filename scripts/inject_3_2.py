import pandas as pd
import re

with open('pages/3_Beban_Kesehatan.py', 'r', encoding='utf-8') as f:
    content = f.read()

# We need to replace Section 3.2 Placeholder
# From '# Section 3.2 Placeholder' to the end of the file.

pattern = re.compile(r'# Section 3.2 Placeholder.*', re.DOTALL)
match = pattern.search(content)

new_section_3_2 = """# ══════════════════════════════════════════════════════════
# SUB-BAB 3.2: KESENJANGAN FASILITAS KESEHATAN
# ══════════════════════════════════════════════════════════
st.markdown("---")
st.markdown('<h2 style="color: #ECEFF1; font-size: 24px;">3.2 Kesenjangan Fasilitas Kesehatan di Kawasan Ekstraktif</h2>', unsafe_allow_html=True)
st.markdown('<span style="background:#5C2B6A;color:#E1BEE7;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: Dumbbell Plot / Disparity Analysis (Data 2022)</span>', unsafe_allow_html=True)

# Data Prep Chart
sentra = ['Sulawesi Tengah', 'Sulawesi Tenggara']
df_faskes_copy = df_faskes.copy()
df_faskes_copy = df_faskes_copy[~df_faskes_copy['provinsi'].str.contains('Indonesia', na=False)]
df_faskes_copy['Kategori'] = df_faskes_copy['provinsi'].apply(lambda x: 'Sentra Industri' if x in sentra else 'Non-Sentra Industri')

# Filter tahun 2022 karena memiliki data Rumah Sakit & Puskesmas terlengkap
df_2022 = df_faskes_copy[df_faskes_copy['tahun'] == 2022]
df_gap = df_2022.groupby(['Kategori', 'jenis'])['jumlah'].mean().reset_index()

# Pivot for Dumbbell Plot
df_pivot = df_gap.pivot(index='jenis', columns='Kategori', values='jumlah').reset_index()
df_pivot.columns.name = None

import plotly.graph_objects as go

fig_3_2 = go.Figure()

# Add lines connecting the dots
for i, row in df_pivot.iterrows():
    fig_3_2.add_trace(go.Scatter(
        x=[row['Sentra Industri'], row['Non-Sentra Industri']],
        y=[row['jenis'], row['jenis']],
        mode='lines',
        line=dict(color='rgba(255, 255, 255, 0.3)', width=4),
        showlegend=False,
        hoverinfo='skip'
    ))

# Add markers for Sentra Industri
fig_3_2.add_trace(go.Scatter(
    x=df_pivot['Sentra Industri'],
    y=df_pivot['jenis'],
    mode='markers+text',
    name='Sentra Industri (Sulteng & Sultra)',
    marker=dict(color='#E53935', size=20, line=dict(color='#B71C1C', width=2)),
    text=df_pivot['Sentra Industri'].apply(lambda x: f"{x:.0f}"),
    textposition='bottom center',
    textfont=dict(color='#E53935', size=14, weight='bold'),
    hovertemplate="Kategori: Sentra Industri<br>Rata-rata: %{x:.1f} Faskes<extra></extra>"
))

# Add markers for Non-Sentra Industri
fig_3_2.add_trace(go.Scatter(
    x=df_pivot['Non-Sentra Industri'],
    y=df_pivot['jenis'],
    mode='markers+text',
    name='Non-Sentra Industri (Lainnya)',
    marker=dict(color='#546E7A', size=20, line=dict(color='#37474F', width=2)),
    text=df_pivot['Non-Sentra Industri'].apply(lambda x: f"{x:.0f}"),
    textposition='top center',
    textfont=dict(color='#546E7A', size=14, weight='bold'),
    hovertemplate="Kategori: Non-Sentra Industri<br>Rata-rata: %{x:.1f} Faskes<extra></extra>"
))

fig_3_2.update_layout(
    title="Ketimpangan Jumlah Fasilitas Kesehatan (Rata-rata per Provinsi, 2022)",
    height=400,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    font=dict(color='#B0BEC5'),
    xaxis=dict(title="Rata-Rata Jumlah Fasilitas", showgrid=True, gridcolor='rgba(255,255,255,0.1)', zeroline=False),
    yaxis=dict(title="", showgrid=False, zeroline=False)
)

st.markdown("<br>", unsafe_allow_html=True)

rs_sentra = df_pivot.loc[df_pivot['jenis'] == 'Rumah Sakit', 'Sentra Industri'].values[0]
rs_non = df_pivot.loc[df_pivot['jenis'] == 'Rumah Sakit', 'Non-Sentra Industri'].values[0]

st.markdown(f\"\"\"
Mitos bahwa masuknya investasi smelter akan membawa *trickle-down effect* (efek tetesan ke bawah) berupa perbaikan infrastruktur publik, **terbantahkan secara absolut oleh data**. Melalui *Dumbbell Plot* di bawah, kita bisa mengukur secara presisi disparitas ketersediaan Fasilitas Kesehatan antara provinsi yang dieksploitasi dengan provinsi yang tidak.

Saat rata-rata kasus ISPA dan Diare di Sentra Industri menembus dua kali lipat lebih tinggi, infrastruktur penunjang kehidupan mereka justru jauh tertinggal. Rata-rata Rumah Sakit di Sentra Industri hanya berjumlah **{rs_sentra:.0f} unit** per provinsi, tertinggal jauh dari wilayah Non-Sentra yang mencapai **{rs_non:.0f} unit**. Defisit fasilitas kesehatan di tengah ledakan populasi dan epidemi infeksi pernapasan ini adalah bentuk kekerasan struktural: negara dan korporasi mengekspor polusi, namun absen dalam menyediakan infrastruktur pertahanan hidup.
\"\"\")

st.plotly_chart(fig_3_2, use_container_width=True)

with st.expander("Lihat Data Mentah: Ketimpangan Faskes 2022", expanded=False):
    st.dataframe(df_pivot, use_container_width=True, hide_index=True)
    st.caption("📁 **Sumber File:** `data/processed/sulawesi_faskes_agregat.csv`")
"""

if match:
    new_content = content[:match.start()] + new_section_3_2
    with open('pages/3_Beban_Kesehatan.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Injeksi Section 3.2 sukses.")
else:
    print("Gagal regex.")
