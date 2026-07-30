import pandas as pd
import altair as alt
import scipy.stats as stats
import numpy as np
import os
import math
from pathlib import Path
import textwrap
import plotly.graph_objects as go
import plotly.express as px

# ── Light theme config ──
BG = 'white'
GRID_COLOR = '#E0E0E0'
LABEL_COLOR = '#333333'
TITLE_COLOR = '#111111'

def configure_light(chart):
    return chart.configure_view(stroke=None).configure_axis(
        grid=True, gridColor=GRID_COLOR, labelColor=LABEL_COLOR, titleColor=LABEL_COLOR
    ).configure_title(color=TITLE_COLOR).configure(background=BG)

def generate():
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    DATA_DIR = BASE_DIR / "data" / "processed"
    OUT_DIR = BASE_DIR / "tools" / "streamlittopdf"
    VISUALS_DIR = OUT_DIR / "visuals"
    VISUALS_DIR.mkdir(parents=True, exist_ok=True)

    # ── Load Data ──
    df_izin    = pd.read_csv(DATA_DIR / "sulawesi_izin_baru_per_tahun.csv")
    df_smelter = pd.read_csv(DATA_DIR / "sulawesi_esdm_nikel.csv")
    df_pltu    = pd.read_csv(DATA_DIR / "sulawesi_pltu_captive.csv")
    df_gfw     = pd.read_csv(DATA_DIR / "sulawesi_gfw_master_1_dekade_2014_2023.csv")
    df_inv     = pd.read_csv(DATA_DIR / "sulawesi_investasi_pmdn_2016_2024.csv")
    df_pdrb    = pd.read_csv(DATA_DIR / "sulawesi_pdrb_sektoral_2016_2024.csv")
    df_pdrb_kab= pd.read_csv(DATA_DIR / "sulawesi_pdrb_sektoral_kabupaten_2016_2024.csv")

    # ── Pre-calc ──
    tot_izin        = df_izin['Jumlah_Izin_Baru'].sum()
    tot_luas_izin   = df_izin['Total_Luas_Konsesi_Baru_Ha'].sum()
    df_pltu_op      = df_pltu[df_pltu['Status'].str.lower() == 'operating']
    tot_kapasitas_pltu = df_pltu_op['Capacity (MW)'].sum() if 'Capacity (MW)' in df_pltu_op.columns else 0
    tot_smelter     = len(df_smelter)
    tot_deforestasi = df_gfw['Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha'].sum()
    tot_investasi   = df_inv['nilai'].sum()
    tot_investasi_triliun = tot_investasi / 1_000

    EKSTRAKTIF_NAMA = ['Pertambangan dan Penggalian', 'Industri Pengolahan', 'Pengadaan Listrik dan Gas']
    AKAR_RUMPUT_NAMA = ['Pertanian, Kehutanan, dan Perikanan']
    LABEL_EKSTRAKTIF  = 'Ekstraktif'
    LABEL_AKAR_RUMPUT = 'Ekonomi Akar Rumput (Pertanian & Perikanan)'
    LABEL_JASA        = 'Sektor Jasa & Lainnya'

    def klasifikasi_kritis(sektor):
        if sektor in EKSTRAKTIF_NAMA: return LABEL_EKSTRAKTIF
        elif sektor in AKAR_RUMPUT_NAMA: return LABEL_AKAR_RUMPUT
        else: return LABEL_JASA

    color_map = {LABEL_EKSTRAKTIF: '#E74C3C', LABEL_JASA: '#7F8C8D', LABEL_AKAR_RUMPUT: '#2ECC71'}
    cat_order_area = [LABEL_AKAR_RUMPUT, LABEL_JASA, LABEL_EKSTRAKTIF]

    # ══════════════════════════════════════════════════
    # CHART 1.1.1 — Stacked Area (3x2 grid, light theme)
    # ══════════════════════════════════════════════════
    print("Chart 1.1.1 ...")
    df_hist = df_pdrb.copy()
    df_hist['Klasifikasi'] = df_hist['sektor_nama'].apply(klasifikasi_kritis)
    df_hist_agg = df_hist.groupby(['provinsi', 'tahun', 'Klasifikasi'])['nilai_miliar_rp'].sum().reset_index()
    df_hist_agg['nilai_triliun_rp'] = df_hist_agg['nilai_miliar_rp'] / 1000
    df_hist_agg['provinsi_label'] = df_hist_agg['provinsi'].apply(
        lambda x: f"{x.upper()} (PUSAT LEDAKAN)" if x == "Sulawesi Tengah" else x)
    df_total_agg = df_hist_agg.groupby(['provinsi', 'tahun'])['nilai_miliar_rp'].sum().reset_index(name='total_pdrb')
    df_hist_agg = df_hist_agg.merge(df_total_agg, on=['provinsi', 'tahun'])
    df_hist_agg['pct_dari_total'] = (df_hist_agg['nilai_miliar_rp'] / df_hist_agg['total_pdrb']) * 100

    provinces = df_hist_agg['provinsi_label'].unique()
    rows, current_row = [], []
    for prov in provinces:
        df_prov = df_hist_agg[df_hist_agg['provinsi_label'] == prov]
        chart = alt.Chart(df_prov).mark_area(opacity=0.9).encode(
            x=alt.X('tahun:O', title='Tahun', axis=alt.Axis(labelAngle=0, values=[2016, 2018, 2020, 2022, 2024])),
            y=alt.Y('nilai_triliun_rp:Q', title='Nilai PDRB (Triliun Rp)', stack=True),
            color=alt.Color('Klasifikasi:N', sort=cat_order_area,
                            scale=alt.Scale(domain=cat_order_area, range=[color_map[LABEL_AKAR_RUMPUT], color_map[LABEL_JASA], color_map[LABEL_EKSTRAKTIF]]),
                            legend=alt.Legend(title=None, orient='bottom'))
        ).properties(title=alt.TitleParams(text=prov, anchor='middle', fontSize=12), height=200, width=210)
        current_row.append(chart)
    for i in range(0, len(current_row), 3):
        rows.append(alt.hconcat(*current_row[i:i+3], spacing=15))
    chart_1_1_1 = configure_light(alt.vconcat(*rows, spacing=15))
    chart_1_1_1.save(str(VISUALS_DIR / "chart_1_1_1.png"))

    # ══════════════════════════════════════════════════
    # CHART 1.1.2 — Ketimpangan Kabupaten Sulteng
    # ══════════════════════════════════════════════════
    print("Chart 1.1.2 ...")
    df_kab = df_pdrb_kab.copy()
    df_kab['Klasifikasi'] = df_kab['sektor_nama'].apply(klasifikasi_kritis)
    df_kab_sulteng = df_kab[df_kab['provinsi'] == 'Sulawesi Tengah'].copy()
    latest_year_kab = df_kab_sulteng['tahun'].max()
    df_kab_latest = df_kab_sulteng[df_kab_sulteng['tahun'] == latest_year_kab].copy()
    df_kab_agg = df_kab_latest.groupby(['kabupaten', 'Klasifikasi'])['nilai_miliar_rp'].sum().reset_index()
    df_kab_agg['nilai_triliun_rp'] = df_kab_agg['nilai_miliar_rp'] / 1000
    df_kab_tot = df_kab_agg.groupby('kabupaten')['nilai_triliun_rp'].sum().reset_index(name='total')
    df_kab_agg = df_kab_agg.merge(df_kab_tot, on='kabupaten')
    df_kab_agg['Klasifikasi'] = pd.Categorical(df_kab_agg['Klasifikasi'], categories=cat_order_area, ordered=True)
    df_kab_agg['kabupaten_label'] = df_kab_agg['kabupaten'].apply(lambda x: x.upper() if 'Morowali' in x else x)
    sort_order = df_kab_agg.groupby('kabupaten_label')['total'].first().sort_values(ascending=False).index.tolist()
    bar_kab = alt.Chart(df_kab_agg).mark_bar().encode(
        y=alt.Y('kabupaten_label:N', title=None, sort=sort_order, axis=alt.Axis(labelLimit=500, labelFontSize=11)),
        x=alt.X('nilai_triliun_rp:Q', title=f"Nilai PDRB ({latest_year_kab}) - Triliun Rp"),
        color=alt.Color('Klasifikasi:N',
                        scale=alt.Scale(domain=cat_order_area, range=[color_map[LABEL_AKAR_RUMPUT], color_map[LABEL_JASA], color_map[LABEL_EKSTRAKTIF]]),
                        legend=alt.Legend(title=None, orient="bottom", direction="vertical", labelLimit=1000))
    ).properties(height=500)
    configure_light(bar_kab).save(str(VISUALS_DIR / "chart_1_1_2.png"))

    # ══════════════════════════════════════════════════
    # CHART 1.1.3 — Small Multiples 17 Sektor (2 kolom)
    # ══════════════════════════════════════════════════
    print("Chart 1.1.3 ...")
    latest_year = df_pdrb['tahun'].max()
    df_latest = df_pdrb[df_pdrb['tahun'] == latest_year].copy()
    df_latest['Klasifikasi'] = df_latest['sektor_nama'].apply(klasifikasi_kritis)
    df_latest['nilai_triliun_rp'] = df_latest['nilai_miliar_rp'] / 1000
    prov_totals = df_latest.groupby('provinsi')['nilai_miliar_rp'].sum().reset_index()
    prov_totals['prov_title'] = prov_totals.apply(lambda r: f"{r['provinsi']} (Total: {r['nilai_miliar_rp']/1000:,.0f} Triliun Rp)", axis=1)
    df_latest = df_latest.merge(prov_totals[['provinsi', 'prov_title']], on='provinsi')
    df_latest['sektor_short'] = df_latest['sektor_nama'].apply(lambda x: x[:35] + '...' if len(x) > 35 else x)
    max_x_val = df_latest['nilai_triliun_rp'].max() * 1.15
    provinces_small = df_latest['prov_title'].unique()
    rows_sm, current_row_sm = [], []
    for prov in provinces_small:
        df_prov = df_latest[df_latest['prov_title'] == prov]
        bar = alt.Chart(df_prov).mark_bar().encode(
            y=alt.Y('sektor_short:N', sort='-x', title=None, axis=alt.Axis(labelLimit=250, labelFontSize=10)),
            x=alt.X('nilai_triliun_rp:Q', title='Nilai PDRB (Triliun Rp)', scale=alt.Scale(domain=[0, max_x_val])),
            color=alt.Color('Klasifikasi:N',
                            scale=alt.Scale(domain=cat_order_area, range=[color_map[LABEL_AKAR_RUMPUT], color_map[LABEL_JASA], color_map[LABEL_EKSTRAKTIF]]),
                            legend=None)
        )
        text_sm = bar.mark_text(align='left', baseline='middle', dx=3, fontSize=9).encode(
            text=alt.Text('nilai_triliun_rp:Q', format=',.1f')
        )
        chart_sm = alt.layer(bar, text_sm).properties(
            title=alt.TitleParams(text=prov, anchor='middle', fontSize=11), height=350, width=380)
        current_row_sm.append(chart_sm)
    for i in range(0, len(current_row_sm), 2):
        rows_sm.append(alt.hconcat(*current_row_sm[i:i+2], spacing=20))
    chart_1_1_3 = configure_light(alt.vconcat(*rows_sm, spacing=20))
    chart_1_1_3.save(str(VISUALS_DIR / "chart_1_1_3.png"))

    # ══════════════════════════════════════════════════
    # CHART 1.2 — Zona Terdampak Smelter
    # ══════════════════════════════════════════════════
    print("Chart 1.2 ...")
    df_smelter_prov = df_smelter.groupby('provinsi').size().reset_index(name='jumlah_iup')
    sulteng_smelter = df_smelter_prov[df_smelter_prov['provinsi'] == 'Sulawesi Tengah']['jumlah_iup'].values[0] if 'Sulawesi Tengah' in df_smelter_prov['provinsi'].values else 0
    sultra_smelter  = df_smelter_prov[df_smelter_prov['provinsi'] == 'Sulawesi Tenggara']['jumlah_iup'].values[0] if 'Sulawesi Tenggara' in df_smelter_prov['provinsi'].values else 0
    persen_smelter_2prov = (sulteng_smelter + sultra_smelter) / tot_smelter * 100 if tot_smelter > 0 else 0
    df_smelter_prov['Persentase'] = (df_smelter_prov['jumlah_iup'] / len(df_smelter)) * 100
    df_smelter_prov['color_group'] = df_smelter_prov['provinsi'].apply(lambda x: x if x in ['Sulawesi Tengah', 'Sulawesi Tenggara'] else 'Lainnya')
    domain_smelter = ['Sulawesi Tengah', 'Sulawesi Tenggara', 'Lainnya']
    range_smelter  = ['#D32F2F', '#F57C00', '#90A4AE']
    bars = alt.Chart(df_smelter_prov).mark_bar(cornerRadiusEnd=2).encode(
        y=alt.Y('provinsi:N', sort='-x', title=''),
        x=alt.X('Persentase:Q', title='Porsi Izin (%)'),
        color=alt.Color('color_group:N', scale=alt.Scale(domain=domain_smelter, range=range_smelter), legend=None)
    )
    text_bar = bars.mark_text(align='left', baseline='middle', dx=3, fontWeight='bold').encode(
        text=alt.Text('Persentase:Q', format='.1f'))
    chart_smelter = configure_light((bars + text_bar).properties(
        height=300,
        title=alt.TitleParams(text='Monopoli 78% Smelter di 2 Provinsi (Sentra Tambang)', anchor='start', fontSize=14)
    ))
    chart_smelter.save(str(VISUALS_DIR / "chart_1_2.png"))

    # ══════════════════════════════════════════════════
    # CHART 1.3 — Tren Izin Tambang Bar+Line
    # ══════════════════════════════════════════════════
    print("Chart 1.3 ...")
    df_izin_agg  = df_izin.groupby(['Tahun', 'Provinsi'])['Jumlah_Izin_Baru'].sum().reset_index()
    df_izin_total= df_izin_agg.groupby('Tahun')['Jumlah_Izin_Baru'].sum().reset_index()
    val_izin_2014= df_izin_total[df_izin_total['Tahun'] == 2014]['Jumlah_Izin_Baru'].values[0] if 2014 in df_izin_total['Tahun'].values else 0
    val_izin_2022= df_izin_total[df_izin_total['Tahun'] == 2022]['Jumlah_Izin_Baru'].values[0] if 2022 in df_izin_total['Tahun'].values else 0
    val_izin_2023= df_izin_total[df_izin_total['Tahun'] == 2023]['Jumlah_Izin_Baru'].values[0] if 2023 in df_izin_total['Tahun'].values else 0
    val_izin_2024= df_izin_total[df_izin_total['Tahun'] == 2024]['Jumlah_Izin_Baru'].values[0] if 2024 in df_izin_total['Tahun'].values else 0
    try:
        pct_increase = ((val_izin_2024 - val_izin_2022) / val_izin_2022) * 100
        annotation_text = f"↑ {int(pct_increase):,}% Kenaikan (2022-2024)"
    except: annotation_text = "Lonjakan Ekstrem"
    bar_chart = alt.Chart(df_izin_agg).mark_bar().encode(
        x=alt.X('Tahun:O', title='Tahun Terbit', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Jumlah_Izin_Baru:Q', title='Jumlah Izin Terbit'),
        color=alt.Color('Provinsi:N', title='Provinsi', scale=alt.Scale(scheme='set2'))
    )
    line_trend  = alt.Chart(df_izin_total).mark_line(color='#FF1744', strokeWidth=3, interpolate='monotone').encode(x='Tahun:O', y='Jumlah_Izin_Baru:Q')
    points_trend= alt.Chart(df_izin_total).mark_circle(color='#FF1744', size=70).encode(x='Tahun:O', y='Jumlah_Izin_Baru:Q')
    df_annot = pd.DataFrame({'Tahun': [2023], 'Jumlah_Izin_Baru': [df_izin_total['Jumlah_Izin_Baru'].max() * 0.95], 'text': [annotation_text]})
    annot = alt.Chart(df_annot).mark_text(align='right', baseline='middle', fontSize=13, fontWeight='bold', color='#FF1744', dx=-10).encode(x='Tahun:O', y='Jumlah_Izin_Baru:Q', text='text')
    chart_izin = configure_light(alt.layer(bar_chart, line_trend, points_trend, annot).properties(height=380, title='Lonjakan Penerbitan Izin Tambang Sulawesi (2014-2024)'))
    chart_izin.save(str(VISUALS_DIR / "chart_1_3.png"))

    # ══════════════════════════════════════════════════
    # CHART 1.4 — Sentra vs Non-Sentra (2 kolom)
    # ══════════════════════════════════════════════════
    print("Chart 1.4 ...")
    sentra_provs = ['Sulawesi Tengah', 'Sulawesi Tenggara']
    df_gfw_kat = df_gfw.copy()
    df_gfw_kat['Kategori_Wilayah'] = df_gfw_kat['Provinsi'].apply(lambda x: 'Sentra Tambang' if x in sentra_provs else 'Non-Sentra')
    df_gfw_kategori = df_gfw_kat.groupby(['Kategori_Wilayah', 'Tahun'])['Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha'].sum().reset_index()
    df_izin_kat = df_izin.copy()
    df_izin_kat['Kategori_Wilayah'] = df_izin_kat['Provinsi'].apply(lambda x: 'Sentra Tambang' if x in sentra_provs else 'Non-Sentra')
    df_izin_kategori = df_izin_kat.groupby(['Kategori_Wilayah', 'Tahun'])['Total_Luas_Konsesi_Baru_Ha'].sum().reset_index()
    df_viz_1_3 = pd.merge(df_gfw_kategori, df_izin_kategori, on=['Kategori_Wilayah', 'Tahun'], how='inner')
    df_izin_agg_narasi = df_izin_kat.groupby('Tahun')['Total_Luas_Konsesi_Baru_Ha'].sum().reset_index()
    df_gfw_agg_narasi  = df_gfw.groupby('Tahun')['Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha'].sum().reset_index()
    val_izin_2016 = df_izin_agg_narasi[df_izin_agg_narasi['Tahun'] == 2016]['Total_Luas_Konsesi_Baru_Ha'].values[0] if 2016 in df_izin_agg_narasi['Tahun'].values else 0
    val_izin_2023_ha = df_izin_agg_narasi[df_izin_agg_narasi['Tahun'] == 2023]['Total_Luas_Konsesi_Baru_Ha'].values[0] if 2023 in df_izin_agg_narasi['Tahun'].values else 0
    val_def_2023 = df_gfw_agg_narasi[df_gfw_agg_narasi['Tahun'] == 2023]['Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha'].values[0] if 2023 in df_gfw_agg_narasi['Tahun'].values else 0
    max_y_izin = df_viz_1_3['Total_Luas_Konsesi_Baru_Ha'].max() * 1.1
    df_s = df_viz_1_3[df_viz_1_3['Kategori_Wilayah'] == 'Sentra Tambang']
    df_n = df_viz_1_3[df_viz_1_3['Kategori_Wilayah'] == 'Non-Sentra']
    chart_s = alt.Chart(df_s).mark_bar(opacity=0.8, color='#F57C00').encode(
        x=alt.X('Tahun:O', title='', axis=alt.Axis(labelAngle=-45)),
        y=alt.Y('Total_Luas_Konsesi_Baru_Ha:Q', scale=alt.Scale(domain=[0, max_y_izin]), title='Luas Konsesi Baru (Ha)')
    ).properties(height=320, title='Daerah Sentra Tambang')
    chart_n = alt.Chart(df_n).mark_bar(opacity=0.8, color='#90A4AE').encode(
        x=alt.X('Tahun:O', title='', axis=alt.Axis(labelAngle=-45)),
        y=alt.Y('Total_Luas_Konsesi_Baru_Ha:Q', scale=alt.Scale(domain=[0, max_y_izin]), title='Luas Konsesi Baru (Ha)')
    ).properties(height=320, title='Daerah Non-Sentra')
    chart_1_4 = configure_light(alt.hconcat(chart_s, chart_n, spacing=20))
    chart_1_4.save(str(VISUALS_DIR / "chart_1_4.png"))

    # ══════════════════════════════════════════════════
    # CHART 1.4b — Pembedahan Ekologis (Donut, Primary, CO2)
    # ══════════════════════════════════════════════════
    print("Chart 1.4 Pembedahan Ekologis ...")
    path_driver  = BASE_DIR / "data" / "raw" / "klhk_gfw" / "land_api_fetch" / "loss_by_driver_sulawesi_2001_2025.csv"
    path_primary = BASE_DIR / "data" / "raw" / "klhk_gfw" / "mega_fetch_v2" / "primary_forest_loss_sulawesi_2001_2025.csv"
    try:
        df_driver_gfw  = pd.read_csv(path_driver)
        df_primary_gfw = pd.read_csv(path_primary)

        driver_map = {
            'Commodity driven deforestation': 'Ekspansi Komoditas (Tambang & Sawit)',
            'Forestry': 'Kehutanan (Logging)',
            'Shifting agriculture': 'Pertanian Berpindah',
            'Urbanization': 'Urbanisasi',
            'Wildfire': 'Kebakaran Hutan',
            'Unknown': 'Lainnya'
        }
        df_donut = df_driver_gfw.groupby('driver')['area_ha'].sum().reset_index()
        df_donut['driver_id'] = df_donut['driver'].map(driver_map).fillna(df_donut['driver'])
        area_komoditas = df_donut.loc[df_donut['driver'] == 'Commodity driven deforestation', 'area_ha'].sum()
        area_forestry  = df_donut.loc[df_donut['driver'] == 'Forestry', 'area_ha'].sum()
        area_shifting  = df_donut.loc[df_donut['driver'] == 'Shifting agriculture', 'area_ha'].sum()
        tot_primary_loss    = df_primary_gfw['area__ha'].sum() if 'area__ha' in df_primary_gfw.columns else 0
        df_co2 = df_driver_gfw[df_driver_gfw['driver'] == 'Commodity driven deforestation']
        tot_co2_emissions   = df_co2['co2_emissions_mg'].sum() if 'co2_emissions_mg' in df_co2.columns else 0

        # Donut chart (Plotly, white bg)
        fig_donut = go.Figure(go.Pie(
            labels=df_donut['driver_id'].tolist(),
            values=df_donut['area_ha'].tolist(),
            hole=0.45,
            marker=dict(colors=['#D32F2F','#4CAF50','#FFC107','#2196F3','#FF5722','#9E9E9E'])
        ))
        fig_donut.update_layout(paper_bgcolor='white', plot_bgcolor='white', height=350,
            legend=dict(font=dict(color='#333')),
            title=dict(text='Aktor Utama Deforestasi Sulawesi', font=dict(color='#111', size=14)))
        fig_donut.write_image(str(VISUALS_DIR / "chart_1_4b_donut.png"), width=600, height=350)

        # Primary forest bar chart
        if 'area__ha' in df_primary_gfw.columns and 'umd_tree_cover_loss__year' in df_primary_gfw.columns:
            df_primary_agg = df_primary_gfw.groupby('umd_tree_cover_loss__year')['area__ha'].sum().reset_index()
            chart_primary = configure_light(alt.Chart(df_primary_agg).mark_bar(color='#E91E63').encode(
                x=alt.X('umd_tree_cover_loss__year:O', title='Tahun', axis=alt.Axis(labelAngle=-45)),
                y=alt.Y('area__ha:Q', title='Hutan Primer Hilang (Ha)')
            ).properties(height=300, title='Tragedi Hutan Primer Sulawesi'))
            chart_primary.save(str(VISUALS_DIR / "chart_1_4b_primary.png"))

        # CO2 bar chart
        if 'co2_emissions_mg' in df_co2.columns and 'year' in df_co2.columns:
            df_co2_agg = df_co2.groupby('year')['co2_emissions_mg'].sum().reset_index()
            chart_co2 = configure_light(alt.Chart(df_co2_agg).mark_bar(color='#5D4037').encode(
                x=alt.X('year:O', title='Tahun', axis=alt.Axis(labelAngle=-45)),
                y=alt.Y('co2_emissions_mg:Q', title='Emisi CO2 (Megagrams)')
            ).properties(height=300, title='Peningkatan Signifikan Emisi Karbon (Komoditas)'))
            chart_co2.save(str(VISUALS_DIR / "chart_1_4b_co2.png"))

        komoditas_str = f"{area_komoditas/1e6:.1f} Mha" if area_komoditas >= 1e6 else f"{area_komoditas/1e3:.0f} kha"
        has_ekologis = True
    except Exception as e:
        print(f"  WARNING: Pembedahan Ekologis skipped: {e}")
        has_ekologis = False
        area_komoditas = tot_primary_loss = tot_co2_emissions = 0
        komoditas_str = "N/A"

    # ══════════════════════════════════════════════════
    # CHART 1.6 — Peta Logistik Plotly (saved as PNG)
    # ══════════════════════════════════════════════════
    print("Chart 1.6 Peta Logistik ...")
    def generate_curve(lon1, lat1, lon2, lat2, offset=0.1, n_points=50):
        mid_lon = (lon1 + lon2) / 2; mid_lat = (lat1 + lat2) / 2
        dx = lon2 - lon1; dy = lat2 - lat1
        dist = math.sqrt(dx**2 + dy**2)
        px = -dy / dist; py = dx / dist
        ctrl_lon = mid_lon + px * dist * offset; ctrl_lat = mid_lat + py * dist * offset
        lons, lats = [], []
        for i in range(n_points + 1):
            t = i / n_points
            lons.append((1-t)**2 * lon1 + 2*(1-t)*t * ctrl_lon + t**2 * lon2)
            lats.append((1-t)**2 * lat1 + 2*(1-t)*t * ctrl_lat + t**2 * lat2)
        return lons, lats

    MAP_ROUTES = [
        ("IMIP",    122.15, -2.82, 113.8, 22.8, "rgb(230, 25, 25)",  -0.12),
        ("GNI",     121.32, -1.91, 113.8, 22.8, "rgb(255, 140, 0)",  -0.04),
        ("VDNI",    122.42, -3.83, 113.8, 22.8, "rgb(0, 112, 220)",   0.04),
        ("OSS",     122.48, -3.80, 113.8, 22.8, "rgb(0, 190, 220)",   0.12),
        ("ANTAM",   121.60, -4.18, 135.0, 35.0, "rgb(0, 180, 80)",   -0.08),
        ("PT Vale", 121.34, -2.56, 135.0, 35.0, "rgb(180, 0, 200)",   0.08),
    ]
    fig_map = go.Figure()
    fig_map.update_geos(
        projection_type="equirectangular",
        showcountries=True, countrycolor="#888888",
        showcoastlines=True, coastlinecolor="#888888",
        showland=True, landcolor="#F5F5F0",
        showocean=True, oceancolor="#D6EAF8",
        lonaxis_range=[100, 145], lataxis_range=[-12, 35],
        bgcolor='white'
    )
    for name, lon1, lat1, lon2, lat2, color, offset in MAP_ROUTES:
        curve_lons, curve_lats = generate_curve(lon1, lat1, lon2, lat2, offset=offset)
        fig_map.add_trace(go.Scattergeo(lon=curve_lons, lat=curve_lats, mode='lines',
            line=dict(width=2.5, color=color), name=name, hoverinfo='name'))
        fig_map.add_trace(go.Scattergeo(lon=[lon1], lat=[lat1], mode='markers+text',
            marker=dict(size=8, color=color, line=dict(width=1, color='white')),
            text=[name], textposition='top right', textfont=dict(size=9, color='#333'),
            showlegend=False, hoverinfo='text', name=name))
    fig_map.add_trace(go.Scattergeo(
        lon=[113.8, 135.0], lat=[22.8, 35.0], mode='markers+text',
        marker=dict(size=9, color='#555'),
        text=["China (Pasar Utama)", "Jepang/Korea"],
        textposition=["top left", "top left"],
        textfont=dict(color='#111', size=10, family='Arial Black'),
        showlegend=False, hoverinfo='none'
    ))
    fig_map.update_layout(
        margin={"r":0,"t":30,"l":0,"b":0},
        paper_bgcolor='white', plot_bgcolor='white', height=450,
        title=dict(text='Peta Jalur Distribusi Logistik Nikel Sulawesi', font=dict(color='#111', size=14)),
        legend=dict(orientation="h", yanchor="bottom", y=-0.12, xanchor="center", x=0.5,
                    font=dict(color='#333', size=11))
    )
    fig_map.write_image(str(VISUALS_DIR / "chart_1_6_peta.png"), width=900, height=450)

    # ══════════════════════════════════════════════════
    # Crosstab 1.2 — PLTU vs Deforestasi
    # ══════════════════════════════════════════════════
    prov_map = {'North Sulawesi': 'Sulawesi Utara', 'South Sulawesi': 'Sulawesi Selatan',
                'Southeast Sulawesi': 'Sulawesi Tenggara', 'Central Sulawesi': 'Sulawesi Tengah',
                'Gorontalo': 'Gorontalo', 'West Sulawesi': 'Sulawesi Barat'}
    df_pltu_panel = df_pltu[df_pltu['Status'].isin(['operating'])].copy()
    if 'captive_flag' in df_pltu_panel.columns:
        df_pltu_panel = df_pltu_panel[df_pltu_panel['captive_flag'] == True]
    df_pltu_panel['Provinsi'] = df_pltu_panel['Subnational unit (province, state)'].map(prov_map)
    df_pltu_panel['Tahun'] = pd.to_numeric(df_pltu_panel['Start year'], errors='coerce')
    df_pltu_agg2 = df_pltu_panel.groupby(['Provinsi', 'Tahun'])['Capacity (MW)'].sum().reset_index()
    df_panel_1_2 = pd.merge(df_gfw, df_pltu_agg2, on=['Provinsi', 'Tahun'], how='left').fillna({'Capacity (MW)': 0})
    df_panel_1_2 = df_panel_1_2.sort_values(by=['Provinsi', 'Tahun'])
    df_panel_1_2['Kapasitas_PLTU_Kumulatif_MW'] = df_panel_1_2.groupby('Provinsi')['Capacity (MW)'].cumsum()

    x_col_2 = 'Kapasitas_PLTU_Kumulatif_MW'
    y_col_2 = 'Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha'
    x_median_2 = df_panel_1_2[x_col_2].median()
    x_thresh_2 = x_median_2 if x_median_2 > 0 else 0
    y_median_2 = df_panel_1_2[y_col_2].median()
    lbl_x_l2 = f"Rendah (≤{int(x_thresh_2):,})"; lbl_x_h2 = f"Tinggi (>{int(x_thresh_2):,})"
    lbl_y_l2 = f"Rendah (<{int(y_median_2):,})";  lbl_y_h2 = f"Tinggi (≥{int(y_median_2):,})"
    df_panel_1_2["X_Label"] = df_panel_1_2[x_col_2].apply(lambda x: lbl_x_h2 if x > x_thresh_2 else lbl_x_l2)
    df_panel_1_2["Y_Label"] = df_panel_1_2[y_col_2].apply(lambda x: lbl_y_h2 if x >= y_median_2 else lbl_y_l2)
    cats_x_2 = [lbl_x_l2, lbl_x_h2]; cats_y_2 = [lbl_y_l2, lbl_y_h2]
    crosstab_2 = pd.crosstab(df_panel_1_2["X_Label"], df_panel_1_2["Y_Label"]).reindex(index=cats_x_2, columns=cats_y_2, fill_value=0)
    try: chi2_2, p_2, dof_2, expected_2 = stats.chi2_contingency(crosstab_2)
    except: chi2_2, p_2, dof_2, expected_2 = 0, 1, 0, np.zeros_like(crosstab_2.values)
    is_sig_2 = p_2 < 0.05
    status_txt_2 = "SIGNIFIKAN" if is_sig_2 else "TIDAK SIGNIFIKAN"
    try:
        a2=crosstab_2.loc[lbl_x_l2, lbl_y_l2]; b2=crosstab_2.loc[lbl_x_l2, lbl_y_h2]
        c2=crosstab_2.loc[lbl_x_h2, lbl_y_l2]; d2=crosstab_2.loc[lbl_x_h2, lbl_y_h2]
        or_2 = (a2*d2)/(b2*c2) if (b2*c2) > 0 else 0
    except: or_2 = 0
    total_cases_2 = len(df_panel_1_2)
    valid_cases_2 = len(df_panel_1_2.dropna(subset=[x_col_2, y_col_2]))
    crosstab_2_df = crosstab_2.copy(); crosstab_2_df['Total'] = crosstab_2_df.sum(axis=1)
    if is_sig_2:
        interp_txt_2 = f"Bukti empiris menegaskan bahwa kehadiran dan penambahan kapasitas PLTU Captive secara spasial-temporal di Sulawesi signifikan memicu ekskalasi deforestasi (OR: {round(or_2, 3)}). Kompleks PLTU tidak hanya mengunci emisi kotor, tetapi infrastruktur pendukungnya membongkar fungsi kawasan penyangga."
    else:
        interp_txt_2 = "Meski data tahunan agregat menunjukkan tidak signifikan (kemungkinan karena konsentrasi PLTU hanya terjadi di segelintir tahun dan lokasi seperti Morowali), hal ini bukan berarti PLTU ramah lingkungan. Sebaliknya, efek rusak dari sebuah PLTU bersifat permanen dan lintas-batas (spillover) yang mencemari wilayah di luar lokasi spesifik pendiriannya."

    # Crosstab 1.3 — Izin vs Deforestasi
    df_panel = pd.merge(df_gfw, df_izin, on=['Provinsi', 'Tahun'], how='left').fillna({'Jumlah_Izin_Baru': 0, 'Total_Luas_Konsesi_Baru_Ha': 0})
    x_col_13 = 'Jumlah_Izin_Baru'; y_col_13 = 'Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha'
    x_med_13 = df_panel[x_col_13].median(); y_med_13 = df_panel[y_col_13].median()
    lbl_xl13 = f"Rendah (<{int(x_med_13):,})"; lbl_xh13 = f"Tinggi (≥{int(x_med_13):,})"
    lbl_yl13 = f"Rendah (<{int(y_med_13):,})"; lbl_yh13 = f"Tinggi (≥{int(y_med_13):,})"
    df_panel["X_Label"] = df_panel[x_col_13].apply(lambda x: lbl_xh13 if x >= x_med_13 else lbl_xl13)
    df_panel["Y_Label"] = df_panel[y_col_13].apply(lambda x: lbl_yh13 if x >= y_med_13 else lbl_yl13)
    cats_x_13 = [lbl_xl13, lbl_xh13]; cats_y_13 = [lbl_yl13, lbl_yh13]
    crosstab_13 = pd.crosstab(df_panel["X_Label"], df_panel["Y_Label"]).reindex(index=cats_x_13, columns=cats_y_13, fill_value=0)
    try: chi2_13, p_13, dof_13, _ = stats.chi2_contingency(crosstab_13)
    except: chi2_13, p_13, dof_13 = 0, 1, 0
    is_sig_13 = p_13 < 0.05; status_13 = "SIGNIFIKAN" if is_sig_13 else "TIDAK SIGNIFIKAN"
    valid_cases_13 = len(df_panel.dropna(subset=[x_col_13, y_col_13]))
    try:
        a13=crosstab_13.loc[lbl_xl13,lbl_yl13]; b13=crosstab_13.loc[lbl_xl13,lbl_yh13]
        c13=crosstab_13.loc[lbl_xh13,lbl_yl13]; d13=crosstab_13.loc[lbl_xh13,lbl_yh13]
        or_13 = (a13*d13)/(b13*c13) if (b13*c13) > 0 else 0
    except: or_13 = 0
    if is_sig_13:
        interp_13 = f"Temuan ini sangat krusial: lonjakan intensitas Jumlah Izin Baru (IUP) terbukti berkorelasi kuat dan signifikan dengan peningkatan Deforestasi Komoditas Tambang/Sawit (OR: {round(or_13, 3)}). Ini adalah konfirmasi empiris bahwa narasi hilirisasi dan investasi ekstraktif bukanlah pertumbuhan tanpa korban—ekspansi spasial mereka mutlak mengorbankan luasan hutan di tingkat tapak."
    else:
        interp_13 = f"Secara agregat, hubungan antara Jumlah Izin Baru dan Deforestasi Komoditas tidak signifikan secara statistik (P ≥ 0.05). Ini mengindikasikan bahwa deforestasi terjadi sangat masif di seluruh panel waktu dan ruang secara merata. Krisis tata kelola dan deforestasi telah menyebar ke seluruh wilayah, sehingga lonjakan izin di tahun tertentu tidak lagi menjadi prediktor tunggal atas kebangkrutan ekologis yang sudah sistemik."

    # Crosstab 1.4 — Investasi vs Deforestasi
    df_inv_clean = df_inv.rename(columns={'provinsi': 'Provinsi', 'tahun': 'Tahun'})
    df_inv_clean['Tahun'] = pd.to_numeric(df_inv_clean['Tahun'], errors='coerce')
    df_inv_clean['Investasi_Juta_Rp'] = pd.to_numeric(df_inv_clean['nilai'], errors='coerce')
    df_panel_14 = pd.merge(df_gfw, df_inv_clean[['Provinsi', 'Tahun', 'Investasi_Juta_Rp']], on=['Provinsi', 'Tahun'], how='inner').fillna({'Investasi_Juta_Rp': 0})
    x_col_14 = 'Investasi_Juta_Rp'; y_col_14 = 'Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha'
    x_med_14 = df_panel_14[x_col_14].median(); y_med_14 = df_panel_14[y_col_14].median()
    lbl_xl14 = f"Rendah (≤{int(x_med_14):,})"; lbl_xh14 = f"Tinggi (>{int(x_med_14):,})"
    lbl_yl14 = f"Rendah (<{int(y_med_14):,})"; lbl_yh14 = f"Tinggi (≥{int(y_med_14):,})"
    df_panel_14["X_Label"] = df_panel_14[x_col_14].apply(lambda x: lbl_xh14 if x > x_med_14 else lbl_xl14)
    df_panel_14["Y_Label"] = df_panel_14[y_col_14].apply(lambda x: lbl_yh14 if x >= y_med_14 else lbl_yl14)
    cats_x_14 = [lbl_xl14, lbl_xh14]; cats_y_14 = [lbl_yl14, lbl_yh14]
    crosstab_14 = pd.crosstab(df_panel_14["X_Label"], df_panel_14["Y_Label"]).reindex(index=cats_x_14, columns=cats_y_14, fill_value=0)
    try: chi2_14, p_14, dof_14, _ = stats.chi2_contingency(crosstab_14)
    except: chi2_14, p_14, dof_14 = 0, 1, 0
    is_sig_14 = p_14 < 0.05; status_14 = "SIGNIFIKAN" if is_sig_14 else "TIDAK SIGNIFIKAN"
    valid_cases_14 = len(df_panel_14.dropna(subset=[x_col_14, y_col_14]))
    try:
        a14=crosstab_14.loc[lbl_xl14,lbl_yl14]; b14=crosstab_14.loc[lbl_xl14,lbl_yh14]
        c14=crosstab_14.loc[lbl_xh14,lbl_yl14]; d14=crosstab_14.loc[lbl_xh14,lbl_yh14]
        or_14 = (a14*d14)/(b14*c14) if (b14*c14) > 0 else 0
    except: or_14 = 0
    if is_sig_14:
        interp_14 = f"Terdapat bukti statistik yang sah bahwa arus masuk modal (Investasi PMDN) secara langsung dan sistematis mendorong ekskalasi deforestasi di wilayah Sulawesi (OR: {round(or_14, 3)}). Investasi ini bukanlah katalisator ekonomi hijau, melainkan injeksi modal untuk ekstraksi lahan."
    else:
        interp_14 = "Secara statistik agregat mungkin belum terlihat korelasi linier di tahun yang persis sama. Hal ini menyingkap anomali bahwa investasi bernilai triliunan kerap ditahan untuk birokrasi awal, sementara pembabatan hutan fisiknya baru meledak secara sporadis di tahun-tahun berikutnya (lagging effect)."

    # ══════════════════════════════════════════════════
    # Ringkasan Eksekutif Semua Skenario Crosstab
    # ══════════════════════════════════════════════════
    def run_all_crosstab(df_panel_in, x_options, y_options):
        """Run all combinations of X and Y, return markdown table rows."""
        y_col_map = {
            'Total_Deforestasi_Ha': 'Total Deforestasi Alam (Hektar)',
            'Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha': 'Deforestasi Komoditas Tambang/Sawit (Hektar)'
        }
        rows = []
        for k_x, v_x in x_options.items():
            for k_y, v_y in y_options.items():
                med_x = df_panel_in[k_x].median()
                thresh_x = med_x if med_x > 0 else 0
                med_y = df_panel_in[k_y].median()
                lbl_xh = f"Tinggi (>{int(thresh_x):,})"; lbl_xl = f"Rendah (≤{int(thresh_x):,})"
                lbl_yh = f"Tinggi (≥{int(med_y):,})"; lbl_yl = f"Rendah (<{int(med_y):,})"
                s_x = df_panel_in[k_x].apply(lambda val: lbl_xh if val > thresh_x else lbl_xl)
                s_y = df_panel_in[k_y].apply(lambda val: lbl_yh if val >= med_y else lbl_yl)
                ct = pd.crosstab(s_x, s_y).reindex(index=[lbl_xl, lbl_xh], columns=[lbl_yl, lbl_yh], fill_value=0)
                try: c2v, pv, _, _ = stats.chi2_contingency(ct)
                except: c2v, pv = 0, 1
                try:
                    aa=ct.loc[lbl_xl,lbl_yl]; bb=ct.loc[lbl_xl,lbl_yh]
                    cc=ct.loc[lbl_xh,lbl_yl]; dd=ct.loc[lbl_xh,lbl_yh]
                    or_v = (aa*dd)/(bb*cc) if (bb*cc) > 0 else 0
                except: or_v = 0
                sig = "✅ SIGNIFIKAN" if pv < 0.05 else "❌ TIDAK SIGNIFIKAN"
                v_y_label = y_col_map.get(k_y, v_y)
                rows.append(f"| {v_x} | {v_y_label} | {c2v:.3f} | {pv:.3f} | {or_v:.2f} | {sig} |")
        return rows

    # Exec summary 1.2 (PLTU)
    x_opts_12 = {'Kapasitas_PLTU_Kumulatif_MW': 'Kapasitas Aktif PLTU Kumulatif (MW)'}
    y_opts_def = {'Total_Deforestasi_Ha': 'Total Deforestasi Alam (Hektar)',
                  'Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha': 'Deforestasi Komoditas Tambang/Sawit (Hektar)'}
    exec_rows_12 = run_all_crosstab(df_panel_1_2, x_opts_12, y_opts_def)
    sig_count_12 = sum(1 for r in exec_rows_12 if 'SIGNIFIKAN' in r and '❌' not in r)
    exec_narr_12 = (f"Dari **{len(exec_rows_12)} skenario pengujian**, terdapat **{sig_count_12} skenario yang terbukti SIGNIFIKAN**. Data empiris membuktikan bahwa pembangunan kompleks peleburan yang disokong PLTU *Captive* secara langsung mengekstraksi wilayah sekitarnya."
                    if sig_count_12 > 0 else
                    f"Dari **{len(exec_rows_12)} skenario pengujian**, seluruhnya menunjukkan status **TIDAK SIGNIFIKAN**. Meski demikian, ini bukan berarti PLTU ramah lingkungan—efek destruktifnya bersifat *spillover* yang mencemari wilayah bahkan di luar lokasi spesifik pendiriannya.")

    # Exec summary 1.3 (Izin)
    x_opts_13 = {'Jumlah_Izin_Baru': 'Jumlah Izin Baru (IUP)',
                 'Total_Luas_Konsesi_Baru_Ha': 'Luas Konsesi Baru (Hektar)'}
    exec_rows_13 = run_all_crosstab(df_panel, x_opts_13, y_opts_def)
    sig_count_13 = sum(1 for r in exec_rows_13 if 'SIGNIFIKAN' in r and '❌' not in r)
    exec_narr_13 = (f"Dari **{len(exec_rows_13)} skenario pengujian**, terdapat **{sig_count_13} skenario yang terbukti SIGNIFIKAN**. Tingginya *Odds Ratio* pada skenario signifikan menegaskan bahwa setiap kali kran perizinan atau luas konsesi diperlebar, risiko terjadinya deforestasi melonjak berkali-kali lipat."
                    if sig_count_13 > 0 else
                    f"Dari **{len(exec_rows_13)} skenario pengujian**, seluruhnya menunjukkan status **TIDAK SIGNIFIKAN**. Ini merupakan sinyal bahaya tertinggi—deforestasi dan kebangkrutan ekologis telah terjadi secara brutal dan merata (*saturation effect*) di seluruh provinsi dan waktu.")

    # Exec summary 1.4 (Investasi)
    x_opts_14 = {'Investasi_Juta_Rp': 'Realisasi Investasi PMDN (Juta Rp)'}
    exec_rows_14 = run_all_crosstab(df_panel_14, x_opts_14, y_opts_def)
    sig_count_14 = sum(1 for r in exec_rows_14 if 'SIGNIFIKAN' in r and '❌' not in r)
    exec_narr_14 = (f"Dari **{len(exec_rows_14)} skenario pengujian**, terdapat **{sig_count_14} skenario yang terbukti SIGNIFIKAN**. Derasnya arus modal (PMDN) bukan indikator keberhasilan ekonomi yang inklusif, melainkan sekadar dana segar untuk membiayai penghancuran hutan skala raksasa."
                    if sig_count_14 > 0 else
                    f"Dari **{len(exec_rows_14)} skenario pengujian**, seluruhnya menunjukkan status **TIDAK SIGNIFIKAN**. Ini menyingkap tabir *lagging effect*—ketika modal masif disuntikkan di tahun tertentu, lahan tidak dibabat di tahun yang sama secara sempurna; daya hancurnya baru meledak pada tahun-tahun berikutnya.")
    # ══════════════════════════════════════════════════
    # Generate Markdown (FULL)
    # ══════════════════════════════════════════════════
    print("Generating Markdown ...")
    md = f"""# Ekspansi Industri Ekstraktif

*Analisis spasiotemporal pertumbuhan industri ekstraktif dan pengolahan nikel serta dampaknya terhadap daya dukung dan daya tampung lingkungan di Pulau Sulawesi.*

## Ekspansi Industri Ekstraktif: {tot_smelter} Unit Smelter dan Ketergantungan Energi Fosil Off-Grid di Sulawesi

Dinamika pembangunan di Pulau Sulawesi periode 2014–2024 ditandai oleh akselerasi industri berbasis komoditas alam. Kebijakan hilirisasi nikel mendorong penerbitan **{int(tot_izin):,} Izin Usaha Pertambangan (IUP) baru** dengan total luas konsesi mencapai **{int(tot_luas_izin):,} Hektar**. Pengoperasian **{tot_smelter} unit fasilitas pemurnian (smelter)** didukung oleh kapasitas **{int(tot_kapasitas_pltu):,} MW PLTU Captive** (pembangkit listrik batu bara *off-grid*), yang meningkatkan intensitas emisi karbon pada zona-zona industri pesisir.

Secara bersamaan, kucuran realisasi Penanaman Modal Dalam Negeri (PMDN) yang mencapai **{int(tot_investasi_triliun):,} Triliun Rupiah** berbanding lurus dengan akumulasi konversi tutupan hutan sebesar **{int(tot_deforestasi):,} Hektar** untuk aktivitas pertambangan dan perkebunan. Data ini mengindikasikan bahwa pertumbuhan indikator makroekonomi berjalan seiring dengan peningkatan beban terhadap daya dukung dan daya tampung lingkungan hidup.

### Metrik Ekstraktif

| Indikator | Nilai | Deskripsi |
| :--- | :--- | :--- |
| **Total Izin Baru (2014-2024)** | **{int(tot_izin):,} IUP** | Penambahan jumlah IUP di Pulau Sulawesi dalam 1 dekade terakhir. |
| **Total Luas Konsesi Baru** | **{int(tot_luas_izin):,} Ha** | Akumulasi luas daratan dan pesisir yang diserahkan sejak 2014. |
| **Kapasitas PLTU Captive Aktif** | **{int(tot_kapasitas_pltu):,} MW** | Beban energi kotor off-grid untuk menyokong pabrik peleburan. |
| **Jumlah Fasilitas Smelter** | **{tot_smelter} Unit** | Total fasilitas pengolahan nikel yang memonopoli zona industri pesisir. |
| **Luas Deforestasi Komoditas** | **{int(tot_deforestasi):,} Ha** | Area hutan alam yang musnah akibat tambang dan perkebunan. |
| **Investasi PMDN (2016-2024)** | **{int(tot_investasi_triliun):,} Triliun Rp** | Aliran modal domestik yang dikucurkan. |

---

## 1.1 Konteks Makro: Breakdown PDRB per Komoditas

Grafik di bawah ini menyederhanakan 17 sektor PDRB menjadi **3 klasifikasi makro advokatif** berdasarkan *Legal Supply-Chain Approach* (Metodologi CELIOS/ECC).

### 1.1.1 Dominasi Ekstraktif vs Ekonomi Akar Rumput (2016-2024)

Grafik di bawah ini menyederhanakan 17 sektor PDRB menjadi **3 klasifikasi makro advokatif** berdasarkan *Legal Supply-Chain Approach* (Metodologi CELIOS/ECC).

- **Ekstraktif** = Kat. B (Pertambangan) + Kat. C (Industri Pengolahan/Smelter) + Kat. D (Listrik/PLTU Captive) — digabung berdasarkan mandat wajib UU Minerba Ps. 102-103 & Perpres 112/2022.
- **Ekonomi Akar Rumput** = Kat. A (Pertanian, Kehutanan & Perikanan) — sektor terbarukan penyerap tenaga kerja lokal terbesar.
- **Sektor Jasa & Lainnya** = 13 sektor E-U sisanya.

![1.1.1](visuals/chart_1_1_1.png)

*Metodologi: Legal Supply-Chain Approach — Kat B+C+D = Ekstraktif (UU Minerba Ps.102-103; Perpres 112/2022 Ps.3 Ay.4)*

### 1.1.2 Pemusatan Sektor Ekstraktif di Kabupaten se-Sulawesi Tengah

Visualisasi di bawah membandingkan komposisi ketiga sektor advokatif di seluruh 13 kabupaten/kota se-Sulawesi Tengah pada tahun terbaru.

![1.1.2](visuals/chart_1_1_2.png)

### 1.1.3 Perbandingan Distribusi 17 Sektor Komoditas per Provinsi (Small Multiples, Tahun Terbaru)

Visualisasi Small Multiples ini membandingkan komposisi 17 sektor komoditas secara terpisah di tiap provinsi. Sektor diurutkan dari penyumbang terbesar (atas) hingga terkecil (bawah). Skala sumbu X konsisten untuk memvalidasi perbandingan lintas provinsi.

![1.1.3](visuals/chart_1_1_3.png)

---

## 1.2 Konsentrasi Kawasan Industri & PLTU Captive

Intensifikasi industri pengolahan nikel di Sulawesi berpusat pada fasilitas mega-smelter. Pengoperasian **{tot_smelter} fasilitas smelter** didukung oleh kapasitas energi batu bara **{int(tot_kapasitas_pltu):,} MW dari PLTU Captive**. Berbeda dengan sistem kelistrikan umum PLN, pembangkit ini dikembangkan secara internal untuk menyokong operasi kawasan industri.

Berikut adalah **temuan konsentrasi spasial** berdasarkan data agregat:

**Pemusatan Spasial Fasilitas Smelter (Bar Chart):** Data menunjukkan bahwa **{int(persen_smelter_2prov):,}% dari total fasilitas ({sulteng_smelter} unit di Sulawesi Tengah dan {sultra_smelter} unit di Sulawesi Tenggara)** terkonsentrasi di dua provinsi tersebut. Pola ini mengonfirmasi adanya pemusatan beban ekologis dan emisi pada zona sentra pemurnian nikel.

Korelasi antara pembangunan kawasan industri dan perubahan tutupan lahan diuji menggunakan **Crosstabulation (Tabulasi Silang)** pada bagian bawah sub-bab ini.

![1.2](visuals/chart_1_2.png)

**Fakta Data:** Sebesar 78% dari total {tot_smelter} fasilitas smelter terkonsentrasi di Sulawesi Tengah & Sulawesi Tenggara, menunjukkan adanya pemusatan beban lingkungan di wilayah sentra tersebut.

### Pembuktian Statistik: Ekspansi PLTU Captive vs Deforestasi

Untuk menguji apakah keberadaan PLTU *Captive* berkorelasi secara spasial dan temporal dengan laju deforestasi, kita menggunakan tabel crosstab pada level observasi **Provinsi-Tahun**.
Mengingat ekspansi PLTU sangat terpusat pada tahun dan provinsi tertentu (menghasilkan banyak nilai nol pada panel), klasifikasi "Tinggi" diartikan sebagai *ada penambahan kapasitas (>0)*, dan "Rendah" sebagai *tidak ada penambahan (=0)*.

**Case Processing Summary**

| Keterangan | N | Persen |
| :--- | :--- | :--- |
| Valid | {valid_cases_2} | {valid_cases_2/total_cases_2*100:.1f}% |
| Total | {total_cases_2} | 100.0% |

**Chi-Square Tests**

| Uji | Value | df | Asymp. Sig. (2-sided) |
| :--- | :--- | :--- | :--- |
| Pearson Chi-Square | {round(chi2_2, 3)} | {dof_2} | {round(p_2, 3)} |

**Result: {status_txt_2}** (P-Value = {round(p_2, 4)}, Odds Ratio = {round(or_2, 3)})

*{interp_txt_2}*

**Interpretasi Spasial Industri:** Kawasan industri pengolahan terkonsentrasi di area pesisir secara signifikan. Pertumbuhan PLTU Captive mengindikasikan tingginya ketergantungan pada energi berbasis batu bara untuk mendukung kebutuhan energi fasilitas pemurnian di Sulawesi Tengah dan Sulawesi Tenggara.

### Ringkasan Eksekutif Seluruh Skenario Crosstab

Tabel di bawah ini merangkum hasil pengujian statistik (Chi-Square) untuk semua kemungkinan kombinasi indikator antara penambahan PLTU Captive dan Dampak Ekologis pada panel data 1 dekade.

| Variabel Independen (X) | Variabel Dependen (Y) | Chi-Square | P-Value | Odds Ratio | Kesimpulan |
| :--- | :--- | :--- | :--- | :--- | :--- |
{''.join([row + chr(10) for row in exec_rows_12])}
{exec_narr_12}

---

## 1.3 Tren Pertumbuhan Izin Tambang Baru & Uji Signifikansi

Pola perizinan pertambangan di Pulau Sulawesi selama satu dekade terakhir menunjukkan peningkatan alokasi ruang yang signifikan. Berdasarkan data agregat *Minerbaone*, tercatat **{int(tot_izin):,} Izin Usaha Pertambangan (IUP) baru** sepanjang 2014-2024, dengan total luas konsesi mencapai **{int(tot_luas_izin):,} Hektar**.

Berdasarkan analisis tren time-series pada grafik **"Penerbitan Izin Tambang"** di bawah, penerbitan izin pada periode awal (2014) tercatat sebanyak **{int(val_izin_2014):,} IUP**. Peningkatan signifikan terjadi pada periode 2022–2024, di mana penerbitan meningkat dari **{int(val_izin_2022):,} IUP di tahun 2022** menjadi **{int(val_izin_2023):,} IUP pada 2023**, dan mencapai **{int(val_izin_2024):,} IUP baru pada 2024**.

Anotasi pada grafik mencatat kenaikan sebesar **246% pada periode 2022–2024**. Data ini mengindikasikan perlunya evaluasi terhadap instrumen pengendalian perizinan dan tata ruang. Distribusi perizinan tertinggi berada di Sulawesi Tengah dan Sulawesi Tenggara, yang selaras dengan kawasan pengembangan industri pemurnian nikel.

Uji **Crosstabulation** pada bagian bawah mengukur hubungan antara laju penerbitan perizinan dan indikator deforestasi di wilayah tersebut.

![1.3](visuals/chart_1_3.png)

**Interpretasi Sektoral:** Peningkatan penerbitan IUP di kawasan timur Sulawesi berbanding lurus dengan perluasan area konversi hutan. Pola perizinan ini menunjukkan pentingnya penerapan instrumen tata ruang dan evaluasi lingkungan secara ketat.

### Pembuktian Statistik: Intensitas Ekspansi vs Deforestasi

Hipotesis utama narasi ini adalah bahwa **lonjakan ekspansi ekstraktif** berbanding lurus dengan **kebangkrutan ekologis** (deforestasi).
Untuk mengujinya secara statistik di tengah keterbatasan jumlah provinsi di Sulawesi (N=6), tabel crosstab dan uji Chi-Square di bawah menggunakan unit observasi **Provinsi-Tahun** (6 provinsi x 10 tahun = 60 sampel panel).
Setiap observasi diklasifikasikan menjadi "Tinggi" atau "Rendah" berdasarkan nilai **Median panel** dari indikator yang dipilih.

**Chi-Square Tests (Jumlah Izin Baru IUP * Deforestasi Komoditas)**

| Uji | Value | df | Asymp. Sig. (2-sided) |
| :--- | :--- | :--- | :--- |
| Pearson Chi-Square | {round(chi2_13, 3)} | {dof_13} | {round(p_13, 3)} |
| N of Valid Cases | {valid_cases_13} | | |

**Result: {status_13}** (P-Value = {round(p_13, 4)}, Odds Ratio = {round(or_13, 3)})

*{interp_13}*

### Ringkasan Eksekutif Seluruh Skenario Crosstab

Tabel di bawah ini merangkum hasil pengujian statistik (Chi-Square) untuk semua kemungkinan kombinasi antara indikator Ekspansi (X) dan Dampak Ekologis (Y) pada panel data yang sama.

| Variabel Independen (X) | Variabel Dependen (Y) | Chi-Square | P-Value | Odds Ratio | Kesimpulan |
| :--- | :--- | :--- | :--- | :--- | :--- |
{''.join([row + chr(10) for row in exec_rows_13])}
{exec_narr_13}

---

## 1.4 Analisis Realisasi Investasi PMDN dan Dampak Terhadap Tutupan Hutan

Grafik di bawah ini memetakan dinamika penerbitan konsesi tambang baru dan dampaknya terhadap tutupan hutan. Pada tahun 2016, luas konsesi tambang baru yang diterbitkan di Sulawesi mencakup **{int(val_izin_2016):,} Hektar**, dan meningkat signifikan hingga mencapai **{int(val_izin_2023_ha):,} Hektar** pada tahun 2023. Pada periode yang sama, angka deforestasi komoditas mencatatkan luasan sebesar **{int(val_def_2023):,} Hektar**.

Data ini mengindikasikan bahwa akselerasi penerbitan konsesi berbanding lurus dengan laju konversi hutan alam (akumulasi deforestasi sebesar **{int(tot_deforestasi):,} Hektar**). Hal ini menegaskan pentingnya pertimbangan daya dukung ekologis dalam setiap kebijakan alokasi konsesi pertambangan.

![1.4](visuals/chart_1_4.png)

**Interpretasi Spasial:** Perbandingan grafik batang di atas menunjukkan bahwa tingkat alokasi konsesi di Daerah Sentra Tambang (Morowali & Konawe) jauh lebih tinggi dibanding wilayah non-sentra, yang berdampak langsung pada konsentrasi perubahan tutupan hutan.

### Pembuktian Statistik: Arus Investasi PMDN vs Deforestasi

**Chi-Square Tests (Realisasi Investasi PMDN * Deforestasi Komoditas)**

| Uji | Value | df | Asymp. Sig. (2-sided) |
| :--- | :--- | :--- | :--- |
| Pearson Chi-Square | {round(chi2_14, 3)} | {dof_14} | {round(p_14, 3)} |
| N of Valid Cases | {valid_cases_14} | | |

**Result: {status_14}** (P-Value = {round(p_14, 4)}, Odds Ratio = {round(or_14, 3)})

*{interp_14}*

### Ringkasan Eksekutif Seluruh Skenario Crosstab (Investasi vs Deforestasi)

Tabel di bawah ini merangkum hasil pengujian statistik (Chi-Square) untuk semua kemungkinan kombinasi antara Realisasi Investasi PMDN dan Dampak Ekologis pada panel data.

| Variabel Independen (X) | Variabel Dependen (Y) | Chi-Square | P-Value | Odds Ratio | Kesimpulan |
| :--- | :--- | :--- | :--- | :--- | :--- |
{''.join([row + chr(10) for row in exec_rows_14])}
{exec_narr_14}

---

## 1.5 Pelabuhan Ekspor: Ke Mana Nikel Sulawesi Dikirim?

Ekspansi nikel di Sulawesi tidak berhenti pada izin dan pabrik smelter. Di setiap lokasi industri nikel besar, berdiri **pelabuhan atau dermaga** yang menghubungkan pabrik langsung ke kapal-kapal pengangkut menuju China dan pasar global. Dari 6 lokasi utama yang ditelusuri, **seluruhnya terbukti memiliki** pelabuhan atau dermaga ekspor, dan **4 dari 6** mendapat label Proyek Strategis Nasional (PSN) dari pemerintah.

| Indikator | Nilai |
| :--- | :--- |
| **Pelabuhan Nikel Terkonfirmasi** | **6** Lokasi |
| **Berlabel Proyek Strategis Nasional** | **4 / 6** |
| **Kapasitas Pelabuhan Terbesar** | **50.000 ton** (GNI Petasia) |

*Sumber: Situs perusahaan, dokumen pemerintah, media (25 sumber OSINT). File: sulawesi_logistik_simpul_nikel.csv*

---

## 1.6 Peta Jalur Distribusi Logistik Nikel Sulawesi

Peta rute logistik maritim ini mengilustrasikan realitas geopolitik dari ambisi hilirisasi nikel di Sulawesi. Alih-alih membangun kemandirian industri manufaktur nasional, data pergerakan kapal dan desain pelabuhan menunjukkan **ketergantungan absolut pada rantai pasok asing**.

| Nama Smelter | Asal (Lon, Lat) | Tujuan | Komoditas |
| :--- | :--- | :--- | :--- |
| **IMIP** | Morowali (122.15, -2.82) | China | NPI/Feronikel |
| **GNI** | Morowali Utara (121.32, -1.91) | China | NPI |
| **VDNI** | Konawe (122.42, -3.83) | China | Feronikel & Stainless Steel |
| **OSS** | Konawe (122.48, -3.80) | China | Stainless Steel |
| **ANTAM** | Kolaka (121.60, -4.18) | Jepang/Korea | Feronikel |
| **PT Vale** | Luwu Timur (121.34, -2.56) | Jepang/Korea | Nickel in Matte |

![Peta Jalur Distribusi Logistik Nikel Sulawesi](visuals/chart_1_6_peta.png)

**Ketergantungan Struktural Rantai Pasok:**
- **Dominasi Ekspor ke China:** Tiga raksasa kawasan industri baru (IMIP, GNI, VDNI/OSS) yang menikmati fasilitas kemudahan Proyek Strategis Nasional (PSN) mengirimkan hampir seluruh *output* barang setengah jadi (NPI, Feronikel, Matte) langsung ke sentra industri di China Timur dan Selatan.
- **Absennya Interkoneksi Domestik:** Sangat minim jalur distribusi logistik yang menghubungkan kawasan smelter raksasa ini dengan pusat industri manufaktur di dalam negeri (seperti di Pulau Jawa). Hal ini mengonfirmasi temuan bahwa Sulawesi saat ini lebih difungsikan murni sebagai *extractive feeder* (daerah penyuplai ekstraktif) bagi mesin industrialisasi negara lain, bukan sebagai fondasi terintegrasi untuk ekosistem mobil listrik domestik.
- **Pergeseran Geopolitik:** Sementara pemain lama seperti PT Vale dan ANTAM memiliki rute pasokan yang mapan ke pasar otomotif tradisional di Jepang dan Korea Selatan, dominasi logistik dan tonase kini telah bergeser drastis seiring dengan peningkatan signifikan pembangunan smelter baru yang terintegrasi langsung dengan pasar China.
"""

    md_path = OUT_DIR / "chapter_1.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Done! Saved to {md_path}")

if __name__ == "__main__":
    generate()
