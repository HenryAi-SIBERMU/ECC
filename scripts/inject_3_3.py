import re

new_section_3_3 = """
# ══════════════════════════════════════════════════════════
# SUB-BAB 3.3: LINTASAN WAKTU BEBAN KESEHATAN (2014-2024)
# ══════════════════════════════════════════════════════════
st.markdown("---")
st.markdown('<h2 style="color: #ECEFF1; font-size: 24px;">3.3 Lintasan Waktu Ekologis & Ledakan Penyakit (2014-2024)</h2>', unsafe_allow_html=True)
st.markdown('<span style="background:#1565C0;color:#BBDEFB;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: Time-Series Line Chart</span>', unsafe_allow_html=True)

st.markdown(\"\"\"
Meskipun secara akumulatif kawasan Sentra Industri menanggung beban yang lebih berat, penelusuran data secara *time-series* (historis) dari 2014 hingga 2024 memberikan wawasan tambahan mengenai fluktuasi kasus penyakit dari tahun ke tahun. Anda dapat memilih indikator penyakit pada menu di bawah untuk melihat jejak ekologis secara spesifik.
\"\"\")

# Data Prep for Time Series
df_ts = df_kes.copy()
df_ts = df_ts[df_ts['nilai'] > 0] # Filter out zeros if any empty data
df_ts['Kategori'] = df_ts['provinsi'].apply(lambda x: 'Sentra Industri (Sulteng & Sultra)' if x in ['Sulawesi Tengah', 'Sulawesi Tenggara'] else 'Non-Sentra Industri (Lainnya)')

col_ts1, col_ts2 = st.columns([1, 2])
with col_ts1:
    list_indikator = df_ts['indikator'].unique().tolist()
    # Pindahkan ISPA ke pilihan pertama
    if 'Kasus ISPA/Pneumonia' in list_indikator:
        list_indikator.insert(0, list_indikator.pop(list_indikator.index('Kasus ISPA/Pneumonia')))
        
    selected_indikator = st.selectbox("Pilih Indikator Penyakit:", list_indikator)

with col_ts2:
    st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)
    st.caption(f"Menampilkan tren pertumbuhan historis untuk **{selected_indikator}** di 6 Provinsi Sulawesi.")

# Filter and aggregate
df_ts_filtered = df_ts[df_ts['indikator'] == selected_indikator]

fig_3_3 = px.line(
    df_ts_filtered,
    x='tahun',
    y='nilai',
    color='provinsi',
    markers=True,
    line_dash='Kategori',
    color_discrete_sequence=px.colors.qualitative.Set2
)

# Bold lines for Sentra Industri
for trace in fig_3_3.data:
    if trace.name in ['Sulawesi Tengah', 'Sulawesi Tenggara']:
        trace.line.width = 4
    else:
        trace.line.width = 2
        trace.opacity = 0.6

fig_3_3.update_layout(
    title=f"Tren Historis {selected_indikator} (2014-2024)",
    height=450,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    legend=dict(title="Provinsi", orientation="v", yanchor="top", y=1, xanchor="left", x=1.02),
    font=dict(color='#B0BEC5'),
    xaxis=dict(title="Tahun", showgrid=True, gridcolor='rgba(255,255,255,0.1)', dtick=1),
    yaxis=dict(title="Jumlah Kasus", showgrid=True, gridcolor='rgba(255,255,255,0.1)', zeroline=False)
)

st.plotly_chart(fig_3_3, use_container_width=True)

with st.expander(f"Lihat Data Panel: {selected_indikator} (2014-2024)", expanded=False):
    df_ts_pivot = df_ts_filtered.pivot_table(index='tahun', columns='provinsi', values='nilai').reset_index()
    st.dataframe(df_ts_pivot, use_container_width=True, hide_index=True)
    st.caption("📁 **Sumber File:** `data/processed/sulawesi_kesehatan_detail_2014_2024.csv`")

"""

with open('pages/3_Beban_Kesehatan.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Insert before Crosstab Introduction
target = "# --- Crosstab Introduction ---"
if target in content:
    new_content = content.replace(target, new_section_3_3 + "\\n" + target)
    with open('pages/3_Beban_Kesehatan.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Injeksi Section 3.3 Time Series sukses.")
else:
    print("Gagal menemukan Crosstab Introduction.")
