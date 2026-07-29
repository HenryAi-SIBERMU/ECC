"""
extract_chapter_5.py
100% faithful extraction of pages/5_Pola_Penerbitan_Izin.py → chapter_5.md
"""
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import scipy.stats as stats
import textwrap
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA = ROOT / "data" / "processed"
VIS  = HERE / "visuals_bab5"
VIS.mkdir(exist_ok=True)

def save_plotly(fig, path, w=1000, h=500):
    fig.write_image(str(path), width=w, height=h, scale=2)

# ─── DATA LOAD ───────────────────────────────────────────────────────────────
df_izin = pd.read_csv(DATA / "sulawesi_izin_baru_per_tahun.csv")
df_gfw  = pd.read_csv(DATA / "sulawesi_gfw_master_1_dekade_2014_2023.csv")
df_kawasan = pd.read_csv(DATA / "sulawesi_gfw_kawasan_lindung_loss_2014_2023.csv")
df_konflik_fpic = pd.read_csv(DATA / "sulawesi_konflik_tambang_fpic.csv")
df_masalah = pd.read_csv(DATA / "kpa_masalah_izin_perusahaan.csv")

# ─── METRIC CALCULATIONS ─────────────────────────────────────────────────────
total_izin         = int(df_izin['Jumlah_Izin_Baru'].sum())
total_luas_konsesi = float(df_izin['Total_Luas_Konsesi_Baru_Ha'].sum())
total_deforestasi  = float(df_gfw['Total_Deforestasi_Ha'].sum())

df_izin_thn   = df_izin.groupby('Tahun')['Jumlah_Izin_Baru'].sum().reset_index()
tahun_puncak  = int(df_izin_thn.loc[df_izin_thn['Jumlah_Izin_Baru'].idxmax(), 'Tahun']) if not df_izin_thn.empty else 0
izin_puncak   = int(df_izin_thn['Jumlah_Izin_Baru'].max()) if not df_izin_thn.empty else 0

df_panel_bento = pd.merge(df_gfw, df_izin, on=['Provinsi','Tahun'], how='left').fillna({'Jumlah_Izin_Baru': 0})
med_def = df_panel_bento['Total_Deforestasi_Ha'].median()
df_panel_bento['is_kritis'] = df_panel_bento['Total_Deforestasi_Ha'] > med_def
izin_kritis   = int(df_panel_bento[df_panel_bento['is_kritis']]['Jumlah_Izin_Baru'].sum())
izin_total    = int(df_panel_bento['Jumlah_Izin_Baru'].sum())
pct_kritis    = (izin_kritis / izin_total * 100) if izin_total > 0 else 0

kritis_prov   = df_panel_bento[df_panel_bento['is_kritis']].groupby('Provinsi')['Jumlah_Izin_Baru'].sum().reset_index()
top_prov_kritis = kritis_prov.loc[kritis_prov['Jumlah_Izin_Baru'].idxmax()]
nama_prov_kritis   = top_prov_kritis['Provinsi']
jumlah_prov_kritis = int(top_prov_kritis['Jumlah_Izin_Baru'])

izin_pra_2020  = int(df_izin[df_izin['Tahun'] < 2020]['Jumlah_Izin_Baru'].sum())
izin_pasca_2020= int(df_izin[df_izin['Tahun'] >= 2020]['Jumlah_Izin_Baru'].sum())
rasio_akselerasi = (izin_pasca_2020 / izin_pra_2020) if izin_pra_2020 > 0 else 0

# FPIC metrics
total_konflik_fpic   = len(df_konflik_fpic)
konflik_fpic_count   = int(df_konflik_fpic['indikasi_fpic'].sum())
total_masalah_izin   = len(df_masalah)
perusahaan_masalah_sulawesi = df_masalah[df_masalah['lokasi'].str.contains('Sulawesi', case=False, na=False)]['nama_perusahaan'].nunique()

# ─── CHART 5.1: DUAL AXIS TIMELINE ─────────────────────────────────────────
print("Rendering 5.1 Dual-Axis Timeline Chart ...")
df_izin_thn2 = df_izin.groupby('Tahun')[['Jumlah_Izin_Baru','Total_Luas_Konsesi_Baru_Ha']].sum().reset_index()
df_gfw_thn   = df_gfw.groupby('Tahun')['Total_Deforestasi_Ha'].sum().reset_index()
df_timeline  = pd.merge(df_gfw_thn, df_izin_thn2, on='Tahun', how='outer').fillna(0).sort_values('Tahun')
df_timeline  = df_timeline[df_timeline['Tahun'] <= 2023]
df_timeline['Total_Deforestasi_Ha_Plotted'] = df_timeline['Total_Deforestasi_Ha']

fig_timeline = make_subplots(specs=[[{'secondary_y': True}]])
fig_timeline.add_trace(
    go.Bar(x=df_timeline['Tahun'], y=df_timeline['Total_Deforestasi_Ha_Plotted'],
           name='Total Deforestasi (Hektar)', marker_color='rgba(231,76,60,0.7)',
           marker_line_color='#C0392B', marker_line_width=1.5,
           text=df_timeline['Total_Deforestasi_Ha_Plotted'].apply(lambda x: f"{int(x):,} Ha"),
           textposition='auto', textfont=dict(color='#333', size=10)),
    secondary_y=False,
)
fig_timeline.add_trace(
    go.Scatter(x=df_timeline['Tahun'], y=df_timeline['Total_Luas_Konsesi_Baru_Ha'],
               name='Area Konsesi IUP (Hektar)', mode='lines+markers+text',
               text=[f"{int(luas/1000)}k ({int(iup)} IUP)" if luas > 0 else "0"
                     for luas, iup in zip(df_timeline['Total_Luas_Konsesi_Baru_Ha'], df_timeline['Jumlah_Izin_Baru'])],
               textposition='top center', textfont=dict(color='#B8860B', size=10, weight='bold'),
               line=dict(color='#DAA520', width=3),
               marker=dict(symbol='circle', size=10, color='#DAA520', line=dict(color='white', width=2))),
    secondary_y=True,
)
fig_timeline.update_layout(
    plot_bgcolor='white', paper_bgcolor='white', font=dict(color='#333'),
    hovermode='x unified', height=500, margin=dict(l=0, r=20, t=50, b=40),
    xaxis=dict(tickformat="%Y", dtick="M12", showgrid=False),
    legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5, title="")
)
fig_timeline.add_vrect(x0=2013.5, x1=2018.5, fillcolor="rgba(149,165,166,0.1)", layer="below", line_width=0,
    annotation_text="<b>Era Ekspansi<br>Sawit & HPH</b>", annotation_position="top left",
    annotation_font_color="#666")
fig_timeline.add_vrect(x0=2018.5, x1=2023.5, fillcolor="rgba(231,76,60,0.05)", layer="below", line_width=0,
    annotation_text="<b>Era Hilirisasi<br>Nikel (Krisis)</b>", annotation_position="top left",
    annotation_font_color="#C0392B")
fig_timeline.update_yaxes(title_text='Deforestasi (Hektar)', secondary_y=False,
    showgrid=True, gridcolor='rgba(0,0,0,0.08)', color='#C0392B')
fig_timeline.update_yaxes(title_text='Area Konsesi (Hektar)', secondary_y=True,
    showgrid=False, color='#B8860B')
save_plotly(fig_timeline, VIS / "chart_5_1_timeline_dual.png", w=1100, h=500)

# ─── CHART 5.2: KAWASAN LIVELIHOOD ─────────────────────────────────────────
print("Rendering 5.2 Kawasan Livelihood Chart ...")
try:
    df_kaw = df_kawasan.copy()
    df_kaw = df_kaw[(df_kaw['wdpa_protected_areas__iucn_cat'].astype(str) != '0') & (df_kaw['Tahun'] <= 2023)]
    df_pivot_chart = pd.pivot_table(df_kaw, values='Luas_Hilang_Kawasan_Lindung_Ha',
                                     index='Tahun', columns='wdpa_protected_areas__iucn_cat',
                                     aggfunc='sum', fill_value=0).reset_index()
    if 1 in df_pivot_chart.columns:
        df_pivot_chart[1] = df_pivot_chart[1].cumsum()
    if 2 in df_pivot_chart.columns:
        df_pivot_chart[2] = df_pivot_chart[2].cumsum()
    df_pivot_chart['Total'] = df_pivot_chart.get(1, 0) + df_pivot_chart.get(2, 0)

    fig_kawasan = go.Figure()
    if 1 in df_pivot_chart.columns:
        fig_kawasan.add_trace(go.Bar(x=df_pivot_chart['Tahun'], y=df_pivot_chart[1],
            name='Zona Pertanian & Peternakan', marker_color='#E74C3C',
            text=[f"{v/1000:,.1f}k" if v > 0 else "" for v in df_pivot_chart[1]],
            textposition='outside', textfont=dict(color='#C0392B', size=10)))
    if 2 in df_pivot_chart.columns:
        fig_kawasan.add_trace(go.Bar(x=df_pivot_chart['Tahun'], y=df_pivot_chart[2],
            name='Perkebunan Warga', marker_color='#F39C12',
            text=[f"{v/1000:,.1f}k" if v > 0 else "" for v in df_pivot_chart[2]],
            textposition='outside', textfont=dict(color='#C0392B', size=10)))
    fig_kawasan.add_trace(go.Scatter(x=df_pivot_chart['Tahun'], y=df_pivot_chart['Total'],
        name='Total Kehancuran Kumulatif', mode='lines+markers+text',
        text=[f"Total: {v/1000:,.1f}k" for v in df_pivot_chart['Total']],
        textposition='top center', textfont=dict(color='#333', size=10, weight='bold'),
        line=dict(color='#333', width=2, dash='dot'), marker=dict(size=7, color='#333')))
    fig_kawasan.update_layout(barmode='stack', plot_bgcolor='white', paper_bgcolor='white',
        font=dict(color='#333'),
        xaxis=dict(title='Tahun', tickmode='linear', dtick=1, showgrid=False),
        yaxis=dict(title='Luas Area Hancur (Hektar)', showgrid=True, gridcolor='rgba(0,0,0,0.08)'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=550, margin=dict(l=0, r=0, t=50, b=0))
    save_plotly(fig_kawasan, VIS / "chart_5_2_kawasan_livelihood.png", w=1000, h=550)
    kawasan_ok = True
except Exception as e:
    print(f"  Kawasan chart failed: {e}")
    kawasan_ok = False

# ─── CHART 5.3a: TIMELINE KONFLIK & MASALAH IZIN ──────────────────────────
print("Rendering 5.3 Charts ...")
df_konflik_tl = df_konflik_fpic.copy()
df_konflik_tl['kategori'] = 'Konflik Pertambangan'
df_konflik_tl = df_konflik_tl.rename(columns={'tahun':'Tahun','judul':'Keterangan'})
df_konflik_tl['Keterangan'] = df_konflik_tl['Keterangan'].str[:80] + '...'

df_masalah_tl = df_masalah[df_masalah['lokasi'].str.contains('Sulawesi', case=False, na=False)].copy()
df_masalah_tl['kategori'] = 'Masalah Izin (KPA)'
df_masalah_tl['Tahun'] = df_masalah_tl['tahun_laporan'].astype(int)
df_masalah_tl['Keterangan'] = df_masalah_tl['nama_perusahaan'] + ' - ' + df_masalah_tl['jenis_masalah_izin']

df_combined_tl = pd.concat([
    df_konflik_tl[['Tahun','kategori','Keterangan']],
    df_masalah_tl[['Tahun','kategori','Keterangan']]
], ignore_index=True).sort_values('Tahun')
df_combined_tl = df_combined_tl[df_combined_tl['Tahun'] >= 2000]
df_tl_agg = df_combined_tl.groupby(['Tahun','kategori']).size().reset_index(name='Jumlah')

fig_tl_konflik = px.bar(df_tl_agg, x='Tahun', y='Jumlah', color='kategori', barmode='group',
    color_discrete_map={'Konflik Pertambangan':'#E74C3C','Masalah Izin (KPA)':'#F39C12'},
    title='Distribusi Temporal: Konflik Pertambangan vs Masalah Izin Perusahaan',
    labels={'Jumlah':'Jumlah Kasus','Tahun':'Tahun'}, text='Jumlah')
fig_tl_konflik.update_traces(textposition='outside', textfont_size=10)
fig_tl_konflik.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(color='#333'),
    height=450, hovermode='x unified',
    xaxis=dict(tickmode='linear', tick0=1968, dtick=5, showgrid=False),
    yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.08)'),
    legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5, title=""))
save_plotly(fig_tl_konflik, VIS / "chart_5_3a_timeline_konflik.png", w=900, h=450)

# ─── CHART 5.3b: JENIS MASALAH IZIN ────────────────────────────────────────
masalah_list = []
for _, row in df_masalah.iterrows():
    masalah_str = str(row['jenis_masalah_izin'])
    for m in masalah_str.split(';'):
        masalah_list.append({'Jenis Masalah': m.strip(), 'Tahun': row['tahun_laporan'], 'Perusahaan': row['nama_perusahaan']})
df_masalah_breakdown = pd.DataFrame(masalah_list)
df_masalah_count = df_masalah_breakdown.groupby('Jenis Masalah').size().reset_index(name='Jumlah Kasus').sort_values('Jumlah Kasus', ascending=True)

fig_masalah = px.bar(df_masalah_count, x='Jumlah Kasus', y='Jenis Masalah', orientation='h',
    title='Jenis Masalah Izin yang Paling Sering Terjadi (KPA CATAHU 2016-2025)',
    text='Jumlah Kasus', color='Jumlah Kasus', color_continuous_scale='Reds')
fig_masalah.update_traces(textposition='outside', textfont_size=11)
fig_masalah.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(color='#333'),
    height=400, showlegend=False,
    xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.08)'),
    yaxis=dict(showgrid=False))
save_plotly(fig_masalah, VIS / "chart_5_3b_masalah_izin.png", w=900, h=400)

# ─── CROSSTAB 5.4 ───────────────────────────────────────────────────────────
print("Computing Crosstabs 5.4 ...")
df_panel = pd.merge(df_gfw, df_izin, on=['Provinsi','Tahun'], how='left').fillna({'Jumlah_Izin_Baru':0,'Total_Luas_Konsesi_Baru_Ha':0})

x_options = {
    "Jumlah_Izin_Baru": "Jumlah Izin Baru (IUP)",
    "Total_Luas_Konsesi_Baru_Ha": "Luas Konsesi Baru (Hektar)"
}
y_options = {
    "Total_Deforestasi_Ha": "Total Deforestasi Alam (Hektar)",
    "Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha": "Deforestasi Komoditas Tambang/Sawit (Hektar)"
}

# Default: Jumlah_Izin_Baru vs Total_Deforestasi_Ha
x_col_def = "Jumlah_Izin_Baru"
y_col_def = "Total_Deforestasi_Ha"
x_med_def = df_panel[x_col_def].median()
y_med_def = df_panel[y_col_def].median()
lx_low = f"Rendah (<{x_med_def:,.1f})"
lx_high= f"Tinggi (≥{x_med_def:,.1f})"
ly_low = f"Rendah (<{y_med_def:,.1f})"
ly_high= f"Tinggi (≥{y_med_def:,.1f})"
df_panel["X_Label"] = df_panel[x_col_def].apply(lambda v: lx_high if v >= x_med_def else lx_low)
df_panel["Y_Label"] = df_panel[y_col_def].apply(lambda v: ly_high if v >= y_med_def else ly_low)
cats_x = [lx_low, lx_high]; cats_y = [ly_low, ly_high]
crosstab_def = pd.crosstab(df_panel["X_Label"], df_panel["Y_Label"]).reindex(index=cats_x, columns=cats_y, fill_value=0)
chi2_def, p_def, dof_def, exp_def = stats.chi2_contingency(crosstab_def)
exp_df_def = pd.DataFrame(exp_def, index=cats_x, columns=cats_y)
try:
    a = crosstab_def.loc[lx_low, ly_low]; b = crosstab_def.loc[lx_low, ly_high]
    c = crosstab_def.loc[lx_high, ly_low]; d = crosstab_def.loc[lx_high, ly_high]
    or_def = (a*d)/(b*c) if (b*c) > 0 else 0
except: or_def = 0

g_def, p_g_def, _, _ = stats.chi2_contingency(crosstab_def, lambda_="log-likelihood")
x_codes_def = df_panel["X_Label"].replace({lx_low:0, lx_high:1})
y_codes_def = df_panel["Y_Label"].replace({ly_low:0, ly_high:1})
try: r_def, p_corr_def = stats.pearsonr(list(x_codes_def), list(y_codes_def)); lbl_val_def = (len(df_panel)-1)*(r_def**2)
except: r_def, p_corr_def, lbl_val_def = 0, 1, 0

total_cases_def = len(df_panel)
valid_cases_def = len(df_panel.dropna(subset=[x_col_def, y_col_def]))
missing_cases_def = total_cases_def - valid_cases_def
interaction_lbl_def = f"{x_options[x_col_def]} * {y_options[y_col_def]}"
is_significant_def = p_def < 0.05
status_text_def = "SIGNIFIKAN (Ada Hubungan)" if is_significant_def else "TIDAK SIGNIFIKAN"

if is_significant_def:
    interp_text_def = (f"Temuan ini sangat krusial: lonjakan intensitas **{x_options[x_col_def]}** terbukti **berkorelasi kuat dan signifikan** "
        f"dengan peningkatan **{y_options[y_col_def]}** (OR: {or_def:.3f}). Ini adalah konfirmasi empiris bahwa narasi hilirisasi dan investasi "
        "ekstraktif bukanlah pertumbuhan tanpa korban—ekspansi spasial mereka mutlak mengorbankan luasan hutan di tingkat tapak.")
else:
    interp_text_def = (f"Secara agregat, hubungan antara **{x_options[x_col_def]}** dan **{y_options[y_col_def]}** **tidak signifikan** secara "
        "statistik (P ≥ 0.05). Ini mengindikasikan bahwa deforestasi terjadi sangat masif di seluruh panel waktu dan ruang secara merata. "
        "Krisis tata kelola dan deforestasi telah menyebar ke seluruh wilayah, sehingga lonjakan izin di tahun tertentu tidak lagi menjadi "
        "prediktor tunggal atas kebangkrutan ekologis yang sudah sistemik.")

# Executive Summary All Combinations
summary_data = []
for k_x, v_x in x_options.items():
    for k_y, v_y in y_options.items():
        med_x = df_panel[k_x].median()
        med_y = df_panel[k_y].median()
        lx_h = f"Tinggi (≥{med_x:,.1f})"; lx_l = f"Rendah (<{med_x:,.1f})"
        ly_h = f"Tinggi (≥{med_y:,.1f})"; ly_l = f"Rendah (<{med_y:,.1f})"
        s_x = df_panel[k_x].apply(lambda v: lx_h if v >= med_x else lx_l)
        s_y = df_panel[k_y].apply(lambda v: ly_h if v >= med_y else ly_l)
        ct = pd.crosstab(s_x, s_y).reindex(index=[lx_l, lx_h], columns=[ly_l, ly_h], fill_value=0)
        try: c2v, pv, dofv, _ = stats.chi2_contingency(ct)
        except: c2v, pv, dofv = 0, 1, 0
        try:
            aa = ct.loc[lx_l, ly_l]; bb = ct.loc[lx_l, ly_h]
            cc = ct.loc[lx_h, ly_l]; dd = ct.loc[lx_h, ly_h]
            orv = (aa*dd)/(bb*cc) if (bb*cc) > 0 else 0
        except: orv = 0
        sig = "🟢 SIGNIFIKAN" if pv < 0.05 else "🔴 TIDAK SIGNIFIKAN"
        summary_data.append({"Variabel Independen (X)": v_x, "Variabel Dependen (Y)": v_y,
            "Chi-Square": f"{c2v:.3f}", "P-Value": f"{pv:.3f}", "Odds Ratio": f"{orv:.2f}", "Kesimpulan": sig})

sig_count = sum(1 for r in summary_data if "🟢 SIGNIFIKAN" in r["Kesimpulan"])
total_scenarios = len(summary_data)

if sig_count > 0:
    exec_narrative = (
        f"Dari **{total_scenarios} skenario pengujian**, terdapat **{sig_count} skenario yang terbukti SIGNIFIKAN**.\n\n"
        "Angka-angka pada tabel di atas bukan sekadar statistik di atas kertas, melainkan **bukti empiris** dari daya rusak kebijakan. "
        "Tingginya *Odds Ratio* pada skenario yang signifikan menegaskan bahwa setiap kali kran perizinan atau luas konsesi diperlebar, "
        "risiko terjadinya deforestasi melonjak berkali-kali lipat.\n\n"
        "Menariknya, jika ada skenario yang menunjukkan *TIDAK SIGNIFIKAN* (khususnya pada deforestasi komoditas spesifik), ini tidak berarti "
        "industri ekstraktif ramah lingkungan. Sebaliknya, ini menjadi indikasi mengerikan bahwa **kehancuran ekologis telah menyebar tak "
        "terkendali (spillover effect)**—di mana kerusakan hutan akibat operasi tambang menjalar jauh melampaui batas konsesi resmi "
        "komoditasnya hingga merusak total lanskap alam secara merata."
    )
else:
    exec_narrative = (
        f"Dari **{total_scenarios} skenario pengujian**, seluruhnya menunjukkan status **TIDAK SIGNIFIKAN**.\n\n"
        "Dalam kacamata ekonomi politik ekologi, ketidaksignifikanan secara agregat ini justru merupakan **sinyal bahaya tertinggi**. "
        "Ini membuktikan bahwa deforestasi dan kebangkrutan ekologis telah terjadi secara *brutal dan merata* di seluruh provinsi dan waktu. "
        "Ekstraksi ruang telah mencapai titik *saturation* (jenuh), sehingga penambahan izin di satu titik tidak lagi menjadi satu-satunya "
        "penyebab, melainkan seluruh sistem tata kelola telah gagal melindungi lanskap tersisa."
    )

# ─── FORMAT CROSSTAB MD ──────────────────────────────────────────────────────
def fmt_ct_md(ct, exp_df, cx, cy):
    header = "| | " + " | ".join(cy) + " | Total |"
    sep    = "|---|" + "|".join(["---"]*len(cy)) + "|---|"
    rows   = [header, sep]
    for x_cat in cx:
        counts = ct.loc[x_cat].tolist()
        exps   = exp_df.loc[x_cat].tolist()
        rows.append(f"| **{x_cat}** Count | " + " | ".join(str(v) for v in counts) + f" | {sum(counts)} |")
        rows.append(f"| **{x_cat}** Expected | " + " | ".join(f"{v:.1f}" for v in exps) + f" | {sum(exps):.1f} |")
    tc = ct.sum().tolist(); te = exp_df.sum().tolist()
    rows.append("| **Total** Count | " + " | ".join(str(v) for v in tc) + f" | {sum(tc)} |")
    rows.append("| **Total** Expected | " + " | ".join(f"{v:.1f}" for v in te) + f" | {sum(te):.1f} |")
    return "\n".join(rows)

crosstab_md = fmt_ct_md(crosstab_def, exp_df_def, cats_x, cats_y)

exec_header = "| Variabel Independen (X) | Variabel Dependen (Y) | Chi-Square | P-Value | Odds Ratio | Kesimpulan |"
exec_sep    = "|---|---|---|---|---|---|"
exec_rows   = [exec_header, exec_sep]
for row in summary_data:
    exec_rows.append(f"| {row['Variabel Independen (X)']} | {row['Variabel Dependen (Y)']} | {row['Chi-Square']} | {row['P-Value']} | {row['Odds Ratio']} | {row['Kesimpulan']} |")
exec_table_md = "\n".join(exec_rows)

# FPIC violations list
df_fpic_v = df_konflik_fpic[df_konflik_fpic['indikasi_fpic'] == True].copy()
df_fpic_v['Perusahaan'] = df_fpic_v['nama_perusahaan'].str.split(';').str[0].str.strip()
df_fpic_v = df_fpic_v[['tahun','Perusahaan','provinsi','lokasi','judul','detail_url']].sort_values('tahun', ascending=False)
fpic_rows = []
for _, row in df_fpic_v.iterrows():
    fpic_rows.append(f"**{row['tahun']}** — {row['Perusahaan']} ({row['provinsi']})\n\n"
                     f"> **Judul Konflik:** {row['judul']}\n>\n"
                     f"> **Komoditas:** {row['lokasi']}\n>\n"
                     f"> **Provinsi:** {row['provinsi']}\n>\n"
                     f"> **Sumber:** [Tanahkita.id]({row['detail_url']})\n")
fpic_md = "\n---\n\n".join(fpic_rows)

# ─── WRITE MARKDOWN ──────────────────────────────────────────────────────────
print("Writing 100% faithful chapter_5.md ...")
md = f"""# Bab 5: Pola Penerbitan Izin di Zona Kritis Ekologis

**CELIOS — Center of Economic and Law Studies**

---

## Fakta Kritis D3TLH

### FAKTA CRI, MIGHTY EARTH, TANAHKITA.ID — Mayoritas IUP Tanpa FPIC

Laporan Climate Rights International, Mighty Earth, dan Business-Human Rights Resource Centre mendokumentasikan banyak IUP tambang nikel di Sulawesi terbit **tanpa *Free, Prior, and Informed Consent* (FPIC)** dari masyarakat adat. Dokumen AMDAL kerap disusun **tanpa konsultasi bermakna** dan pelibatan masyarakat yang ruang hidupnya dirampas.

### DATA BPS (SLHI) — Krisis Kualitas Air (IKA) di Bawah 55

Indeks Kualitas Air (IKA) di sentra nikel seperti Sultra dan Sulteng konsisten terpuruk di level cemaran berat (46-55). Sedimentasi lumpur tambang laut menghancurkan terumbu karang dan mengusir wilayah tangkap nelayan sejauh puluhan mil.

---

*Evaluasi terhadap kegagalan instrumen tata kelola lingkungan dalam meredam perizinan tambang di wilayah yang telah melampaui daya dukung ekologis.*

### Metodologi Pendekatan

**Kerangka Logis (Alur Kausalitas):**
Bagian ini dirancang untuk menjawab sub-pertanyaan kritis dalam studi D3TLH: *"Apakah izin baru tetap diterbitkan ketika tekanan ekologis sudah tinggi?"*

1. **Variabel Dependen (Y):** Jumlah penerbitan izin tambang baru per tahun.
2. **Variabel Konteks (X):** Status kritis ekologis (diukur dari laju deforestasi dan kerusakan eksisting).
3. **Pendekatan Metodologis:** *Timeline Mapping* dan *Crosstabulation* untuk melihat tumpang tindih (*overlay*) temporal antara memburuknya kualitas lingkungan dengan grafik penerbitan izin.

**Tujuan:**
Membuktikan secara empiris terjadinya kegagalan tata kelola (governance failure) di mana instrumen Daya Dukung dan Daya Tampung Lingkungan Hidup (D3TLH) tidak bersifat mengikat (non-mandatory) dan mudah diabaikan demi melancarkan investasi.

---

Secara institusional, dokumen tata ruang dan instrumen lingkungan hidup semestinya beroperasi sebagai 'rem darurat' negara untuk menolak izin investasi baru di bentang alam yang sudah melampaui kapasitas pemulihannya. Namun, penelusuran data spasial dan waktu di semenanjung Sulawesi membongkar skandal tata kelola yang memilukan. Selama satu dekade terakhir, saat total deforestasi telah merobek **{total_deforestasi:,.1f} hektar** tutupan hutan tersisa, negara justru terus mengobral **{total_izin:,} izin tambang baru** yang merampas tambahan **{total_luas_konsesi:,.1f} hektar** ruang daratan. Ironisnya, puncak penerbitan izin tertinggi meledak pada tahun **{tahun_puncak}** ({izin_puncak} izin), tepat pada momentum di mana berbagai wilayah telah memancarkan sinyal darurat polusi dan kebangkrutan ekologis. Ini membuktikan bahwa D3TLH telah dilumpuhkan menjadi sekadar ornamen administratif semata yang tunduk pada syahwat oligarki ekstraktif.

---

## Ringkasan Metrik Agregat

| Indikator | Nilai | Keterangan |
|---|---|---|
| **Tingkat Pengabaian Ekologis** | **{pct_kritis:.1f}% ({izin_kritis} IUP)** | Mayoritas mutlak izin baru justru diobral secara sengaja pada tahun-tahun di mana laju deforestasi provinsi tersebut sedang berada di zona kritis (di atas rata-rata). Sumber: Data Panel (ESDM & GFW) |
| **Zona Bebas Rem Darurat** | **{nama_prov_kritis} ({jumlah_prov_kritis} IUP)** | Provinsi dengan rekor penerbitan izin tertinggi tepat pada saat daya dukung lingkungan (tutupan hutan) mereka sedang hancur lebur tanpa mitigasi. Sumber: Data Panel (ESDM & GFW) |
| **Akselerasi Izin Pasca-2020** | **{rasio_akselerasi:.1f}x Lipat** | Ledakan drastis penerbitan izin baru di era pasca-2020 dibandingkan periode sebelumnya, mengonfirmasi jebol dan diabaikannya instrumen D3TLH. Sumber: Kementerian ESDM (Minerbaone) |

---

## 5.1 Fakta Penyebab: Sinkronisasi Waktu (Timeline Mapping)

**Metode: Gantt Chart Timeline (Plotly Express)**

### Metodologi: Sinkronisasi Waktu (Timeline Mapping)

**Metode Analisis:** Sub-bab ini menggunakan visualisasi deret waktu bersilang (*Dual-Axis Combo Chart*) untuk mendeteksi korelasi visual temporal.

1. **Model Komparasi Temporal:**
    * **Time-Series Tracking:** Mengkomparasikan secara bersamaan akumulasi hilangnya luasan hutan (deforestasi) dengan laju obral perizinan pertambangan baru dari tahun 2014-2023.
    * **Pemetaan Anomali (*Governance Failure*):** Melacak secara empiris apakah instrumen 'rem darurat' ekologis bekerja. Jika kurva perizinan terus melesat naik tepat di tahun saat grafik deforestasi menembus batas krisis, maka terjadi pengabaian tata ruang yang disengaja.
2. **Kalkulasi/Formula Pengolahan:**
    * `Total_Deforestasi_Tahunan = SUM(Luas_Hilang_Ha) GROUP BY Tahun`
    * `Total_IUP_Baru = COUNT(Izin) GROUP BY Tahun`
3. **Variabel & Fitur Data:**
    * **X-Axis (Waktu):** `Tahun` (2014-2023)
    * **Y-Axis Kiri (Dampak Ekologis):** `Total_Deforestasi_Ha`
    * **Y-Axis Kanan (Keputusan Aktor):** `Jumlah_Izin_Baru`
4. **Dataset & File:**
    * `data/processed/sulawesi_izin_baru_per_tahun.csv` (Minerbaone)
    * `data/processed/sulawesi_gfw_master_1_dekade_2014_2023.csv` (GFW)

---

Visualisasi *Dual-Axis Combo Chart* di bawah ini memberikan penelanjangan empiris mengenai pergeseran aktor perusak hutan dan kegagalan sistemik dari instrumen Daya Dukung dan Daya Tampung Lingkungan Hidup (D3TLH). Jika kita membedah tren historisnya, terdapat dua fase krisis ekologis yang berbeda. Pada **Fase 2014-2018 (Zona Kiri)**, tingginya angka deforestasi mayoritas digerakkan oleh ekspansi perkebunan kelapa sawit dan Hak Pengusahaan Hutan (HPH). Pada periode ini, kurva konsesi tambang mineral masih tergolong landai dan belum menjadi aktor utama. Namun, konstelasi ini berubah drastis memasuki fase berikutnya.

Memasuki **Era Hilirisasi Nikel Pasca-2019 (Zona Kanan)**, industri tambang mengambil alih estafet sebagai mesin utama deforestasi. Kurva kuning (Area Konsesi IUP Baru) melesat tajam dan bergerak secara sinkron dengan skala kerusakan ekosistem. Anomali paling fatal terjadi pasca-2020: lonjakan luas konsesi tambang mencapai rekor tertingginya tepat pada momentum ketika grafik deforestasi kembali memerah parah. Secara matematis, ratusan ribu hektar tanah yang diserahkan melalui konsesi IUP baru ini berkorelasi mutlak dengan hilangnya tutupan pohon (*Hektar vs Hektar*). Fenomena ini bukanlah kebetulan statistik, melainkan mengonfirmasi tesis *governance failure*, di mana instrumen tata ruang tidak lagi berfungsi sebagai "rem darurat".

Dokumen AMDAL dan analisis daya dukung lingkungan (D3TLH) telah direduksi nilainya menjadi sekadar ornamen administratif belaka; hanya berfungsi sebagai stempel legalisasi prosedural untuk memfasilitasi kelancaran invasi spasial oligarki tambang. Negara, melalui aparatus birokrasinya, secara sadar dan sistematis mengabaikan sinyal darurat dari alam. Akibat pembiaran struktural ini, wilayah-wilayah penyangga kehidupan di semenanjung Sulawesi kini secara nyata dikorbankan menjadi zona tumbal (*sacrifice zones*) demi ilusi pertumbuhan rasio PDB nasional, yang pada akhirnya harus dibayar sangat mahal dengan ongkos kebangkrutan ekologis permanen.

#### Tren Eskalasi Bersamaan: Kerusakan Hutan (Batang) vs Penerbitan Izin (Garis)

![Tren Eskalasi Bersamaan: Deforestasi vs Penerbitan Izin (2014-2023)](visuals_bab5/chart_5_1_timeline_dual.png)

> **Interpretasi Governance Failure:** Alih-alih membunyikan "rem darurat", data tren historis mengonfirmasi bahwa instrumen D3TLH hanya berakhir sebagai formalitas administratif yang secara sistematis diabaikan demi memfasilitasi ekspansi oligarki ekstraktif.

---

## 5.2 Fakta Spasial: Tabrakan Tata Ruang di Kawasan Konservasi

**Metode: Overlay Area Kawasan Lindung (GFW)**

### Metodologi: Analisis Spasial Tabrakan Tata Ruang

**Metode Analisis:** Sub-bab ini menggunakan agregasi spasial bertingkat (*Stacked Bar Chart*) untuk mendokumentasikan skala kehancuran mutlak pada wilayah yang diharamkan untuk ditambang.

1. **Model Analisis Deforestasi Livelihood:**
    * **Geospatial Overlay:** Melakukan isolasi data *tree cover loss* (GFW) yang secara spesifik bertumpukan/beririsan dengan poligon Kawasan Livelihood (Zona Pertanian, Peternakan) dan Perkebunan Warga.
    * **Kuantifikasi Kerusakan Kumulatif:** Mengkalkulasi kehancuran agregat kawasan penyangga ekosistem esensial selama satu dekade terakhir akibat penetrasi aktivitas tambang.
2. **Kalkulasi/Formula Pengolahan:**
    * `Luas_Hancur_Perkebunan_Warga = SUM(Loss_Ha) WHERE Cat = '2'`
    * `Luas_Hancur_Pertanian_Peternakan = SUM(Loss_Ha) WHERE Cat = '1'`
    * `Total_Kumulatif_Hancur(t) = Total_Kumulatif_Hancur(t-1) + Luas_Hancur(t)`
3. **Variabel & Fitur Data:**
    * **Kategorisasi Spasial (X):** `Tahun`, Kategori Livelihood
    * **Besaran Destruksi (Y):** `Luas_Hilang_Kawasan_Livelihood_Ha`
4. **Dataset & File:**
    * `data/processed/sulawesi_gfw_kawasan_lindung_loss_2014_2023.csv`

---

Dataset spasial menunjukkan obral IUP tambang tidak mempedulikan batas tata ruang. Jutaan hektar kawasan penyangga kehidupan (Hutan Produksi, Kawasan Lindung, dan Area Resapan Air) secara sistematis dirusak dan dihilangkan fungsi ekologisnya demi memuluskan ekspansi ekstraksi nikel.

#### Akumulasi Kehancuran Total: Livelihood Warga (Pertanian, Peternakan, Perkebunan) 2014-2023

![Akumulasi Kehancuran Total Kawasan Livelihood 2014-2023](visuals_bab5/chart_5_2_kawasan_livelihood.png)

> **Fakta Lapangan:** Dalam dekade terakhir, total lebih dari **56 ribu hektar** kawasan livelihood (Pertanian, Peternakan, dan Perkebunan) warga yang seharusnya menjadi ruang hidup masyarakat sekitar telah dihancurkan oleh ekspansi industri ekstraktif.

---

## 5.3 Realitas Lapangan: Izin Bermasalah, FPIC Diabaikan, Masyarakat Dikorbankan

**Metode: Cross-Dataset Integration (KPA CATAHU + Tanahkita + CRI/Mighty Earth Reports)**

### Metodologi: Ekstraksi Data Konflik Agraria & Pelanggaran HAM

**Metode Analisis:** Sub-bab ini menggunakan triangulasi data kualitatif-kuantitatif dengan mendemonstrasikan integrasi *database* konflik agraria (*Multi-source Database Profiling*).

1. **Pemodelan Indikator Pelanggaran FPIC:**
    * **Cross-Referencing:** Memadukan repositori konflik terbuka (KPA & Tanahkita.id) dengan laporan independen lembaga HAM global (CRI, Mighty Earth, BHRRC) untuk membongkar anomali perizinan (*non-compliance*).
    * **Kuantifikasi Kriminalisasi:** Menghitung jumlah perampasan lahan tanpa persetujuan warga (Pelanggaran *Free, Prior, Informed Consent*/FPIC), tumpang tindih HGU, dan letupan represi bersenjata.
2. **Kalkulasi/Formula Pengolahan:**
    * `Total_Pelanggaran_FPIC = COUNT(Kasus) WHERE indikasi_fpic = True`
    * `Rekam_Jejak_Oligarki = COUNT(Jenis_Masalah_Izin) GROUP BY nama_perusahaan`
3. **Variabel & Fitur Data:**
    * **Kategori Entitas:** `nama_perusahaan`, `provinsi`, `jenis_masalah_izin`, `indikasi_fpic`
    * **Besaran Kasus:** `luas_ha`, Frekuensi kemunculan konflik.
4. **Dataset & File:**
    * `data/processed/sulawesi_konflik_tambang_fpic.csv`
    * `data/processed/kpa_masalah_izin_perusahaan.csv`

---

Di balik lautan angka statistik penerbitan IUP, tersembunyi realitas mengerikan: **mayoritas izin tambang nikel di Sulawesi terbit tanpa *Free, Prior, and Informed Consent* (FPIC) dari masyarakat adat**. Laporan terbaru dari **Climate Rights International (2024-2025)**, **Mighty Earth (2024)**, dan **Business & Human Rights Resource Centre** mendokumentasikan pola sistematis di mana perusahaan tambang nikel secara ilegal membabat hutan lindung dan hutan produksi di seluruh Indonesia, termasuk Sulawesi, tanpa konsultasi bermakna dengan masyarakat lokal. Dokumen AMDAL dan analisis daya dukung (D3TLH) disusun sebagai **formalitas prosedural belaka**—sekadar stempel legalisasi untuk memfasilitasi investasi raksasa tanpa pelibatan komunitas yang ruang hidupnya dirampas.

Penelusuran mendalam terhadap **database Konsorsium Pembaruan Agraria (KPA) CATAHU 2016-2025** dan **Tanahkita.id** mengungkap fakta mengejutkan: dari **21 kasus masalah izin perusahaan** yang teridentifikasi dalam 9 laporan tahunan KPA, **mayoritas melibatkan perusahaan tambang dengan HGU kadaluarsa, operasi ilegal tanpa izin kehutanan, dan tumpang tindih klaim lahan**. Di Sulawesi sendiri, tercatat **12 konflik pertambangan** dengan **4 kasus pelanggaran FPIC eksplisit** yang melibatkan penembakan warga, kriminalisasi aktivis, dan penggusuran paksa lahan adat.

Yang paling mengkhawatirkan: perusahaan-perusahaan dengan rekam jejak konflik agraria dan pelanggaran HAM ini **terus beroperasi hingga hari ini**, bahkan beberapa di antaranya menjadi bagian dari Proyek Strategis Nasional (PSN) yang dilindungi negara. Ini membuktikan bahwa sistem perizinan tambang di Indonesia bukan hanya gagal melindungi lingkungan, tetapi juga **secara sistematis mengorbankan hak-hak masyarakat adat dan lokal demi kepentingan oligarki ekstraktif**.

### Metrik Kunci

| Indikator | Nilai | Keterangan |
|---|---|---|
| **Konflik Pertambangan Sulawesi** | **{total_konflik_fpic} Kasus** | Total konflik pertambangan terdokumentasi di Sulawesi (1968-2023) dengan **{konflik_fpic_count} kasus pelanggaran FPIC eksplisit** yang melibatkan kekerasan, kriminalisasi, dan penggusuran paksa. Sumber: Tanahkita.id (KPA/YLBHI) |
| **Perusahaan Izin Bermasalah** | **{total_masalah_izin} Kasus** | Kasus masalah izin perusahaan yang teridentifikasi dalam CATAHU KPA (2016-2025): HGU kadaluarsa, operasi ilegal, IUP bermasalah, dan tumpang tindih klaim lahan. Sumber: KPA CATAHU 2016-2025 |
| **Perusahaan Bermasalah di Sulawesi** | **{perusahaan_masalah_sulawesi} Perusahaan** | Perusahaan unik yang disebutkan dalam laporan KPA dengan lokasi operasi di Sulawesi, mayoritas terlibat dalam kasus tumpang tindih lahan dan HGU kadaluarsa. Sumber: KPA CATAHU 2016-2025 |

#### Timeline Historis: Konflik Pertambangan & Masalah Izin (2000-2025)

![Distribusi Temporal: Konflik Pertambangan vs Masalah Izin Perusahaan](visuals_bab5/chart_5_3a_timeline_konflik.png)

> **Temuan Kunci:** Lonjakan konflik pertambangan terjadi pada periode 2011-2023, bersamaan dengan boom nikel di Sulawesi. Laporan KPA menunjukkan pola sistematis: mayoritas konflik melibatkan perusahaan dengan HGU kadaluarsa, operasi ilegal, dan pengabaian FPIC. Era pasca-2020 menunjukkan intensifikasi masalah izin, mengonfirmasi jebolnya instrumen tata kelola lingkungan.

#### Breakdown Jenis Masalah Izin Perusahaan

![Jenis Masalah Izin yang Paling Sering Terjadi (KPA CATAHU 2016-2025)](visuals_bab5/chart_5_3b_masalah_izin.png)

> **Pola Pelanggaran Dominan:** Tumpang tindih klaim lahan (17 kasus) dan HGU kadaluarsa (10 kasus) menjadi masalah terbanyak. Ini membuktikan lemahnya koordinasi antar-kementerian dan diabaikannya status legal lahan dalam proses penerbitan IUP baru. Operasi ilegal (3 kasus) dan IUP bermasalah (2 kasus) menunjukkan pengawasan yang sangat lemah dari otoritas berwenang.

#### Perusahaan dengan Pelanggaran FPIC Eksplisit

{fpic_md}

> **Kasus Terburuk:** PT Gema Kreasi Perdana (GKP) di Pulau Wawonii beroperasi dengan IPPKH kadaluarsa, mengkriminalisasi puluhan warga penolak, dan menghancurkan lahan pertanian yang dikelola 30 tahun oleh 37,000+ jiwa. PT Sumber Energi Jaya di Minahasa Selatan menembaki warga pada 4 Juni 2012. PT Vale Indonesia mengubah lahan adat To Karunsi'e menjadi lapangan golf. Ini bukan kecelakaan—ini desain sistemik.

### Referensi Utama & Verifikasi Independen

**Laporan Organisasi Internasional:**
- **Climate Rights International (2024-2025):** "Indonesia: Nickel Industry Harming Human Rights and the Environment" — Dokumentasi pelanggaran hak asasi dan lingkungan di industri nikel Indonesia. cri.org/indonesia
- **Mighty Earth (2024):** "From Forests to Electric Vehicles" — Temuan: perusahaan tambang nikel secara ilegal membabat hutan lindung dan produksi, **tanpa menggunakan FPIC untuk konsultasi dengan komunitas lokal di Kabaena**. mightyearth.org
- **Business & Human Rights Resource Centre (2024):** "Indonesia: Nickel mining levels forests without FPIC" — Dokumentasi dampak kesehatan, lingkungan, dan ekonomi yang merugikan masyarakat lokal. business-humanrights.org
- **EJAtlas:** "Islanders resisting nickel mining permits, Wawonii, Southeast Sulawesi" — "Meskipun konsesi mencakup area pemukiman dan tanah leluhur, **penduduk tidak dilibatkan dalam proses pengambilan keputusan**." ejatlas.org
- **Mongabay (2025):** "Nickel boom on an Indonesian island brings toxic seas, lost incomes" — "Komunitas yang terdampak melaporkan **perampasan lahan tanpa konsultasi atau kompensasi yang layak, partisipasi publik yang terbatas, dan kriminalisasi terhadap protes**, semuanya melanggar hak-hak masyarakat adat dan hukum nasional." mongabay.com

**Database Nasional:**
- **Konsorsium Pembaruan Agraria (KPA):** Catatan Akhir Tahun (CATAHU) 2016-2025 — 9 laporan tahunan komprehensif tentang konflik agraria dan masalah perizinan di Indonesia.
- **Tanahkita.id:** Database konflik agraria YLBHI/KPA — 568 kasus konflik nasional, 12 kasus pertambangan Sulawesi terekam.

---

## 5.4 Pembuktian Empiris: Uji Statistik Korelasi Penerbitan Izin & Deforestasi

**Metode: Crosstabulation & Pearson Chi-Square Test**

### Metodologi: Uji Korelasi Penerbitan Izin & Ekstraksi Ekologis

**Metode Analisis:** Sub-bab ini menggunakan pengujian statistik inferensial (*Crosstabulation & Chi-Square Test*) untuk membuktikan secara matematis apakah besaran jumlah perizinan baru menjadi prediktor kuat terhadap tingkat kerusakan deforestasi.

1. **Uji Signifikansi Statistik (Chi-Square):**
    * **Binning (Kategorisasi Data):** Data numerik berkelanjutan (Jumlah Izin & Luas Deforestasi) dikategorikan menjadi 2 level (Tinggi & Rendah) menggunakan ambang batas Median dari distribusi panel. `Nilai > Median = Tinggi`, `Nilai <= Median = Rendah`.
    * `H0 (Null Hypothesis): Tidak ada hubungan yang signifikan (independen) antara klasifikasi tingginya jumlah penerbitan IUP baru dengan klasifikasi tingginya luasan deforestasi pada suatu provinsi di tahun tertentu.`
    * `Decision Rule: Tolak H0 jika nilai Asymptotic Significance (P-Value) pada uji Pearson Chi-Square < 0.05 (Alpha 5%).`
2. **Kalkulasi/Formula Pengolahan:**
    * `Chi-Square (χ²) = Σ [ (O_i - E_i)² / E_i ]`
    * `Odds Ratio = (Peluang Deforestasi Tinggi pada Izin Tinggi) / (Peluang Deforestasi Tinggi pada Izin Rendah)`
3. **Variabel & Fitur Data:**
    * **Variabel Independen (X):** `Jumlah_Izin_Baru` atau `Total_Luas_Konsesi_Baru_Ha` (Interaktif Dropdown).
    * **Variabel Dependen (Y):** `Total_Deforestasi_Ha` atau `Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha` (Interaktif Dropdown).
4. **Dataset & File:**
    * Panel Join dari: `sulawesi_izin_baru_per_tahun.csv` dan `sulawesi_gfw_master_1_dekade_2014_2023.csv`

---

### Detail Uji Statistik (Chi-Square & Odds Ratio)

*Tabel-tabel di bawah ini adalah output statistik formal yang menyajikan bukti statistik formal: Case Processing → Crosstabulation → Chi-Square Tests → Ringkasan Hipotesis.*

**Variabel Independen (X):** {x_options[x_col_def]}

**Variabel Dependen (Y):** {y_options[y_col_def]}

#### Case Processing Summary

| | Valid N | Valid % | Missing N | Missing % | Total N | Total % |
|---|---|---|---|---|---|---|
| {interaction_lbl_def} | {valid_cases_def} | {valid_cases_def/total_cases_def*100:.1f}% | {missing_cases_def} | {missing_cases_def/total_cases_def*100:.1f}% | {total_cases_def} | 100.0% |

#### {interaction_lbl_def} Crosstabulation

{crosstab_md}

#### Chi-Square Tests

**{interaction_lbl_def}**

| | Value | df | Asymp. Sig. (2-sided) |
|---|---|---|---|
| Pearson Chi-Square | {chi2_def:.3f} | {dof_def} | {p_def:.3f} |
| Likelihood Ratio | {g_def:.3f} | {dof_def} | {p_g_def:.3f} |
| Linear-by-Linear Association | {lbl_val_def:.3f} | 1 | {p_corr_def:.3f} |
| N of Valid Cases | {valid_cases_def} | | |

### Ringkasan Uji Hipotesis

**Result: {status_text_def}**

| Parameter | Nilai |
|---|---|
| P-Value | {p_def:.4f} |
| Chi-Square | {chi2_def:.3f} |
| df | {dof_def} |
| **Odds Ratio (Risk Estimate)** | **{or_def:.3f}** |

> **Interpretasi Ekologis:** {interp_text_def}

---

### Ringkasan Eksekutif Seluruh Skenario Crosstab

Tabel di bawah ini merangkum hasil pengujian statistik (Chi-Square) untuk semua kemungkinan kombinasi antara indikator Ekspansi (X) dan Dampak Ekologis (Y) pada panel data yang sama.

{exec_table_md}

> **Pembedahan Realitas Ekologis:**
>
> {exec_narrative}
"""

out_path = HERE / "chapter_5.md"
out_path.write_text(md, encoding="utf-8")
print(f"Done! 100% faithful chapter_5.md saved to {out_path}")
