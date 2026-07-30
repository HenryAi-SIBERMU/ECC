"""
extract_chapter_6.py
100% faithful extraction of pages/6_Audit_D3TLH.py → chapter_6.md
"""
import os, sys, re
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import scipy.stats as stats
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA = ROOT / "data" / "processed"
VIS  = HERE / "visuals_bab6"
VIS.mkdir(exist_ok=True)

def save_plotly(fig, path, w=1000, h=500):
    fig.write_image(str(path), width=w, height=h, scale=2)

# ─── DATA LOAD ───────────────────────────────────────────────────────────────
df_kes = pd.read_csv(DATA / "sulawesi_kesehatan_detail_2014_2024.csv") if (DATA / "sulawesi_kesehatan_detail_2014_2024.csv").exists() else pd.DataFrame()
df_ika = pd.read_csv(DATA / "sulawesi_ika_2016_2024.csv") if (DATA / "sulawesi_ika_2016_2024.csv").exists() else pd.DataFrame()
df_bencana = pd.read_csv(DATA / "sulawesi_bencana_bnpb_2014_2024.csv") if (DATA / "sulawesi_bencana_bnpb_2014_2024.csv").exists() else pd.DataFrame()
df_konflik = pd.read_csv(DATA / "sulawesi_konflik_agraria_tanahkita.csv") if (DATA / "sulawesi_konflik_agraria_tanahkita.csv").exists() else pd.DataFrame()
df_izin = pd.read_csv(DATA / "sulawesi_izin_baru_per_tahun.csv") if (DATA / "sulawesi_izin_baru_per_tahun.csv").exists() else pd.DataFrame()
df_iku = pd.read_csv(DATA / "sulawesi_iku_2015_2024.csv") if (DATA / "sulawesi_iku_2015_2024.csv").exists() else pd.DataFrame()
df_b3 = pd.read_csv(DATA / "sulawesi_limbah_b3.csv") if (DATA / "sulawesi_limbah_b3.csv").exists() else pd.DataFrame()
df_pltu_op = pd.read_csv(DATA / "sulawesi_pltu_captive.csv") if (DATA / "sulawesi_pltu_captive.csv").exists() else pd.DataFrame()
df_gfw = pd.read_csv(DATA / "sulawesi_gfw_master_1_dekade_2014_2023.csv") if (DATA / "sulawesi_gfw_master_1_dekade_2014_2023.csv").exists() else pd.DataFrame()
df_gfw_lindung = pd.read_csv(DATA / "sulawesi_gfw_kawasan_lindung_loss_2014_2023.csv") if (DATA / "sulawesi_gfw_kawasan_lindung_loss_2014_2023.csv").exists() else pd.DataFrame()
df_gfw_driver = pd.read_csv(DATA / "sulawesi_gfw_loss_by_driver_2014_2023.csv") if (DATA / "sulawesi_gfw_loss_by_driver_2014_2023.csv").exists() else pd.DataFrame()
df_konflik_fpic = pd.read_csv(DATA / "sulawesi_konflik_tambang_fpic.csv") if (DATA / "sulawesi_konflik_tambang_fpic.csv").exists() else pd.DataFrame()
df_kpa_izin = pd.read_csv(DATA / "kpa_masalah_izin_perusahaan.csv") if (DATA / "kpa_masalah_izin_perusahaan.csv").exists() else pd.DataFrame()
df_pltu_captive = pd.read_csv(DATA / "sulawesi_pltu_captive.csv") if (DATA / "sulawesi_pltu_captive.csv").exists() else pd.DataFrame()
df_kawasan_nikel = pd.read_csv(DATA / "sulawesi_kawasan_nikel_luas_per_provinsi.csv") if (DATA / "sulawesi_kawasan_nikel_luas_per_provinsi.csv").exists() else pd.DataFrame()
df_faskes = pd.read_csv(DATA / "sulawesi_faskes_agregat.csv") if (DATA / "sulawesi_faskes_agregat.csv").exists() else pd.DataFrame()
df_nasa = pd.read_csv(DATA / "gee_nasa_no2_sulawesi_monthly_raw.csv") if (DATA / "gee_nasa_no2_sulawesi_monthly_raw.csv").exists() else pd.DataFrame()

# ─── CALCULATIONS FOR SCORES ───────────────────────────────────────────────
# Udara
kapasitas_terkini = 0
no2_terkini = 4.0e-6
if not df_pltu_op.empty:
    kapasitas_terkini = df_pltu_op[(df_pltu_op['Status'].str.lower() == 'operating')]['Capacity (MW)'].sum()
if not df_nasa.empty:
    df_nasa_annual = df_nasa.groupby('Tahun')['Rata_Rata_NO2'].mean().reset_index()
    if not df_nasa_annual.empty:
        no2_terkini = df_nasa_annual.loc[df_nasa_annual['Tahun'].idxmax(), 'Rata_Rata_NO2']
skor_1 = min(10.0, (kapasitas_terkini / 10000) * 5 + max(0, (no2_terkini - 4.0e-6) / (7.0e-6 - 4.0e-6)) * 5)

skor_2 = 0; rasio_anomali = 0; kasus_sentra = 0
if not df_kes.empty:
    df_ts_pre = df_kes[df_kes['indikator'].str.contains('ISPA', case=False, na=False)]
    kasus_sentra = df_ts_pre[df_ts_pre['provinsi'].isin(['Sulawesi Tengah', 'Sulawesi Tenggara'])]['nilai'].sum()
    kasus_non_sentra = df_ts_pre[~df_ts_pre['provinsi'].isin(['Sulawesi Tengah', 'Sulawesi Tenggara'])]['nilai'].sum()
    rasio_anomali = (kasus_sentra / 2) / (kasus_non_sentra / 4) if kasus_non_sentra > 0 else 0
    skor_2 = min(10.0, max(0.0, (rasio_anomali - 1) * 10.0))

skor_3 = 0; skor_overcapacity = 0; total_b3_sulteng = 0
if not df_b3.empty:
    df_b3['Estimasi Timbulan (Ton/Tahun)'] = pd.to_numeric(df_b3['Estimasi Timbulan (Ton/Tahun)'], errors='coerce').fillna(0)
    total_b3_sulteng = df_b3[df_b3['Provinsi'] == 'Sulawesi Tengah']['Estimasi Timbulan (Ton/Tahun)'].sum()
    skor_overcapacity = total_b3_sulteng / 1_000_000
    skor_3 = min(10.0, (skor_overcapacity / 30.0) * 10)

skor_4 = 0; total_emisi_co2 = 0
if not df_gfw.empty:
    df_gfw['Total_Emisi_CO2_Megagram'] = pd.to_numeric(df_gfw['Total_Emisi_CO2_Megagram'], errors='coerce').fillna(0)
    total_emisi_co2 = df_gfw['Total_Emisi_CO2_Megagram'].sum() / 1_000_000
    skor_4 = min(10.0, (total_emisi_co2 / 150.0) * 10)

skor_akumulasi_udara = (skor_1 + skor_2 + skor_3 + skor_4) / 4

# Air
ika_terkini = 50; ika_sulteng = 50
if not df_ika.empty:
    df_ika_avg = df_ika.groupby('Tahun')['Indeks Kualitas Air'].mean().reset_index()
    if 2024 in df_ika_avg['Tahun'].values:
        ika_terkini = df_ika_avg[df_ika_avg['Tahun'] == 2024]['Indeks Kualitas Air'].values[0]
    df_sulteng = df_ika[df_ika['Provinsi'] == 'Sulawesi Tengah']
    if not df_sulteng.empty and 2024 in df_sulteng['Tahun'].values:
        ika_sulteng = df_sulteng[df_sulteng['Tahun'] == 2024]['Indeks Kualitas Air'].values[0]
skor_air_1 = min(10.0, max(0, (80 - ika_sulteng) / 30) * 10)

skor_air_2 = 0; kasus_diare_sentra = 0; kasus_diare_non = 0; rasio_diare = 0
if not df_kes.empty:
    df_diare = df_kes[df_kes['indikator'].str.contains('Diare', case=False, na=False)]
    kasus_diare_sentra = df_diare[df_diare['provinsi'].isin(['Sulawesi Tengah', 'Sulawesi Tenggara'])]['nilai'].sum()
    kasus_diare_non = df_diare[~df_diare['provinsi'].isin(['Sulawesi Tengah', 'Sulawesi Tenggara'])]['nilai'].sum()
    ir_sentra = (kasus_diare_sentra / 5_700_000) * 1000
    ir_non = (kasus_diare_non / 14_200_000) * 1000 if kasus_diare_non > 0 else 1
    rasio_diare = ir_sentra / ir_non if ir_non > 0 else 0
    skor_air_2 = min(10.0, max(0.0, (rasio_diare - 1) * 10.0))

skor_air_3 = 0; jumlah_konflik_air = 0; luas_konflik_air = 0
df_konflik_air = pd.DataFrame()
if not df_konflik.empty:
    keywords = 'air|laut|pesisir|nelayan|sungai|pulau|tailing'
    df_konflik_air = df_konflik[df_konflik['sektor'].str.contains(keywords, case=False, na=False) | 
                                df_konflik['judul'].str.contains(keywords, case=False, na=False) | 
                                df_konflik['deskripsi'].str.contains(keywords, case=False, na=False)]
    jumlah_konflik_air = len(df_konflik_air)
    if 'luas_ha' in df_konflik_air.columns:
        luas_konflik_air = pd.to_numeric(df_konflik_air['luas_ha'], errors='coerce').sum()
    skor_air_3 = min(10.0, (jumlah_konflik_air / 15.0) * 10)

skor_air_4 = 0; total_tailing_sulteng = 0
if not df_b3.empty:
    total_tailing_sulteng = df_b3[df_b3['Provinsi'] == 'Sulawesi Tengah']['Estimasi Timbulan (Ton/Tahun)'].sum()
    skor_air_4 = min(10.0, (total_tailing_sulteng / 25_000_000) * 10)

skor_akumulasi_air = (skor_air_1 + skor_air_2 + skor_air_3 + skor_air_4) / 4

# Lahan
skor_lahan_1 = 0; bencana_sulteng_sultra = 0
if not df_bencana.empty:
    df_bencana_sentra = df_bencana[df_bencana['provinsi'].isin(['Sulawesi Tengah', 'Sulawesi Tenggara'])].copy()
    df_bencana_sentra['jumlah_kejadian'] = pd.to_numeric(df_bencana_sentra['jumlah_kejadian'], errors='coerce').fillna(0)
    bencana_sulteng_sultra = df_bencana_sentra['jumlah_kejadian'].sum()
    skor_lahan_1 = min(10.0, (bencana_sulteng_sultra / 877) * 10)

skor_lahan_2 = 0; deforestasi_sentra = 0
if not df_gfw.empty:
    df_gfw_sentra = df_gfw[df_gfw['Provinsi'].isin(['Sulawesi Tengah', 'Sulawesi Tenggara'])].copy()
    df_gfw_sentra['Total_Deforestasi_Ha'] = pd.to_numeric(df_gfw_sentra['Total_Deforestasi_Ha'], errors='coerce').fillna(0)
    deforestasi_sentra = df_gfw_sentra['Total_Deforestasi_Ha'].sum()
    skor_lahan_2 = min(10.0, (deforestasi_sentra / 638_000) * 10)

skor_lahan_3 = 0; lindung_hilang = 0
if not df_gfw_lindung.empty:
    df_l = df_gfw_lindung[df_gfw_lindung['Provinsi'].isin(['Sulawesi Tengah', 'Sulawesi Tenggara'])].copy()
    df_l['Luas_Hilang_Kawasan_Lindung_Ha'] = pd.to_numeric(df_l['Luas_Hilang_Kawasan_Lindung_Ha'], errors='coerce').fillna(0)
    lindung_hilang = df_l['Luas_Hilang_Kawasan_Lindung_Ha'].sum()
    skor_lahan_3 = min(10.0, (lindung_hilang / 638_000) * 10)

skor_lahan_4 = 0; tambang_driver_ha = 0
if not df_gfw_driver.empty:
    df_d = df_gfw_driver[df_gfw_driver['Provinsi'].isin(['Sulawesi Tengah', 'Sulawesi Tenggara'])].copy()
    df_d['Luas_Deforestasi_Ha'] = pd.to_numeric(df_d['Luas_Deforestasi_Ha'], errors='coerce').fillna(0)
    tambang_driver = df_d[df_d['Faktor_Pendorong'] == 'Deforestasi Komoditas (Tambang/Sawit)']
    tambang_driver_ha = tambang_driver['Luas_Deforestasi_Ha'].sum()
    skor_lahan_4 = min(10.0, (tambang_driver_ha / 500_000) * 10)

skor_akumulasi_lahan = (skor_lahan_1 + skor_lahan_2 + skor_lahan_3 + skor_lahan_4) / 4

# Sosial
skor_sosial_1 = 0; skor_sosial_2 = 0; skor_sosial_3 = 0; konflik_darat = 0; luas_ha_dirampas = 0
jiwa_terdampak = 0; insiden_krim = 0; warga_ditangkap = 0; kasus_fpic = 0

if not df_konflik.empty:
    keywords = 'air|laut|pesisir|nelayan|sungai|pulau|tailing'
    df_konflik_darat = df_konflik[~df_konflik['sektor'].str.contains(keywords, case=False, na=False)].copy()
    konflik_darat = len(df_konflik_darat)
    df_konflik_darat['luas_ha'] = pd.to_numeric(df_konflik_darat['luas_ha'], errors='coerce').fillna(0)
    df_konflik_darat['dampak_masyarakat_jiwa'] = pd.to_numeric(df_konflik_darat['dampak_masyarakat_jiwa'], errors='coerce').fillna(0)
    luas_ha_dirampas = df_konflik_darat['luas_ha'].sum()
    jiwa_terdampak = df_konflik_darat['dampak_masyarakat_jiwa'].sum()
    skor_sosial_2 = min(10.0, (jiwa_terdampak / 100_000) * 10)
    
    krim_df = df_konflik_darat[df_konflik_darat['indikasi_kriminalisasi'] == True].copy()
    krim_df['jumlah_ditangkap'] = pd.to_numeric(krim_df['jumlah_ditangkap'], errors='coerce').fillna(0)
    insiden_krim = len(krim_df)
    warga_ditangkap = krim_df['jumlah_ditangkap'].sum()
    skor_sosial_3 = min(10.0, (insiden_krim / 50) * 10)

if not df_konflik_fpic.empty:
    kasus_fpic = len(df_konflik_fpic)
    skor_sosial_1 = min(10.0, (kasus_fpic / 12) * 10)

spa_aktual_pct = 42.5; target_rpjmn = 80.0
gap_spa = max(0.0, target_rpjmn - spa_aktual_pct)
skor_sosial_4 = min(10.0, (gap_spa / target_rpjmn) * 10)

skor_akumulasi_sosial = (skor_sosial_1 + skor_sosial_2 + skor_sosial_3 + skor_sosial_4) / 4

# Veto
skor_veto_1 = 0; skor_veto_2 = 0; skor_veto_3 = 0
izin_baru = 0; perusahaan_ilegal = 0; kapasitas_pltu = 0.0

if not df_izin.empty:
    df_izin['Tahun'] = pd.to_numeric(df_izin['Tahun'], errors='coerce')
    df_izin['Jumlah_Izin_Baru'] = pd.to_numeric(df_izin['Jumlah_Izin_Baru'], errors='coerce').fillna(0)
    df_izin_recent = df_izin[df_izin['Tahun'] >= 2014]
    izin_baru = df_izin_recent['Jumlah_Izin_Baru'].sum()
    skor_veto_1 = min(10.0, (izin_baru / 100) * 10)

if not df_kpa_izin.empty:
    perusahaan_ilegal = len(df_kpa_izin['nama_perusahaan'].unique())
    skor_veto_2 = min(10.0, (perusahaan_ilegal / 10) * 10)

if not df_pltu_captive.empty:
    df_pltu_captive['Capacity (MW)'] = pd.to_numeric(df_pltu_captive['Capacity (MW)'], errors='coerce').fillna(0)
    kapasitas_pltu = df_pltu_captive['Capacity (MW)'].sum()
    skor_veto_3 = min(10.0, (kapasitas_pltu / 5000) * 10)

skor_akumulasi_veto = (skor_veto_1 + skor_veto_2 + skor_veto_3) / 3

# ─── GENERATE VISUALS ───────────────────────────────────────────────────────
print("Rendering Bab 6 Charts ...")

# 1. Combo PLTU vs NO2 NASA
if not df_pltu_op.empty and not df_nasa.empty:
    years = list(range(2010, 2025))
    prov_map = {'Central Sulawesi':'Sulawesi Tengah', 'South East Sulawesi':'Sulawesi Tenggara', 'South Sulawesi':'Sulawesi Selatan', 'North Sulawesi':'Sulawesi Utara', 'West Sulawesi':'Sulawesi Barat', 'Gorontalo':'Gorontalo'}
    df_pltu_op_tab = df_pltu_op.copy()
    df_pltu_op_tab['Provinsi'] = df_pltu_op_tab['Subnational unit (province, state)'].replace(prov_map)
    df_pltu_op_tab = df_pltu_op_tab[(df_pltu_op_tab['Status'].str.lower() == 'operating') & df_pltu_op_tab['Start year'].notna()]
    grid_pltu = pd.DataFrame([
        {'Provinsi': 'Gorontalo', 'Capacity (MW)': 100, 'Start year': 2010},
        {'Provinsi': 'Sulawesi Utara', 'Capacity (MW)': 220, 'Start year': 2010},
        {'Provinsi': 'Sulawesi Selatan', 'Capacity (MW)': 920, 'Start year': 2010},
        {'Provinsi': 'Sulawesi Tenggara', 'Capacity (MW)': 100, 'Start year': 2010}
    ])
    df_pltu_op_tab = pd.concat([df_pltu_op_tab, grid_pltu], ignore_index=True)
    panel_data_pltu = []
    for y in years:
        for prov in prov_map.values():
            cap = df_pltu_op_tab[(df_pltu_op_tab['Provinsi'] == prov) & (df_pltu_op_tab['Start year'] <= y)]['Capacity (MW)'].sum()
            panel_data_pltu.append({'Tahun': y, 'Provinsi': prov, 'Kapasitas_PLTU_MW': cap})
    df_pltu_trend = pd.DataFrame(panel_data_pltu)
    df_nasa_annual = df_nasa.groupby('Tahun')['Rata_Rata_NO2'].mean().reset_index()
    df_nasa_annual.rename(columns={'Tahun': 'year', 'Rata_Rata_NO2': 'median'}, inplace=True)
    
    fig_nasa_combined = make_subplots(specs=[[{"secondary_y": True}]])
    pltu_colors = {'Gorontalo':'#757575', 'Sulawesi Utara':'#8D6E63', 'Sulawesi Selatan':'#FBC02D', 'Sulawesi Tenggara':'#F57C00', 'Sulawesi Tengah':'#D32F2F'}
    for prov, color in pltu_colors.items():
        d_trend = df_pltu_trend[df_pltu_trend['Provinsi'] == prov]
        if not d_trend.empty:
            fig_nasa_combined.add_trace(go.Scatter(x=d_trend['Tahun'], y=d_trend['Kapasitas_PLTU_MW'], name=prov, mode='lines', stackgroup='one', line=dict(width=1, color=color), fillcolor=color), secondary_y=False)
    fig_nasa_combined.add_trace(go.Scatter(x=df_nasa_annual['year'], y=df_nasa_annual['median'], name="Rata-rata NO2 Tahunan", mode='lines+markers', line=dict(color='#D32F2F', width=3), marker=dict(size=8)), secondary_y=True)
    fig_nasa_combined.update_layout(title="Semua PLTU Batubara vs Polusi NO2 (Data Satelit NASA)", plot_bgcolor="white", paper_bgcolor="white", font=dict(color="#333"), margin=dict(l=0, r=0, t=40, b=0))
    save_plotly(fig_nasa_combined, VIS / "chart_6_1a_pltu_no2.png")

# 2. ISPA Line Chart
if not df_kes.empty:
    df_ts_filtered = df_kes[df_kes['indikator'].str.contains('ISPA', case=False, na=False)].copy()
    populasi_bps = {"Sulawesi Selatan": 9070000, "Sulawesi Tengah": 2985000, "Sulawesi Tenggara": 2624000, "Sulawesi Utara": 2621000, "Sulawesi Barat": 1419000, "Gorontalo": 1171000}
    df_ts_filtered["populasi"] = df_ts_filtered["provinsi"].map(populasi_bps)
    df_ts_filtered["rate_per_10k"] = (df_ts_filtered["nilai"] / df_ts_filtered["populasi"]) * 10000
    color_map_prov = {"Sulawesi Tengah": "#EF5350", "Sulawesi Tenggara": "#D32F2F", "Gorontalo": "#42A5F5", "Sulawesi Barat": "#1E88E5", "Sulawesi Selatan": "#1565C0", "Sulawesi Utara": "#90CAF9"}
    fig_ispa = px.line(df_ts_filtered, x="tahun", y="rate_per_10k", color="provinsi", markers=True, color_discrete_map=color_map_prov, title="Insiden ISPA per 10.000 Penduduk")
    fig_ispa.update_layout(plot_bgcolor="white", paper_bgcolor="white", font=dict(color="#333"), margin=dict(l=0, r=0, t=40, b=0))
    save_plotly(fig_ispa, VIS / "chart_6_1b_ispa_trend.png")

# 3. B3 Bar Chart
if not df_b3.empty:
    df_b3_prov = df_b3.groupby('Provinsi')['Estimasi Timbulan (Ton/Tahun)'].sum().reset_index()
    fig_b3 = px.bar(df_b3_prov, x='Estimasi Timbulan (Ton/Tahun)', y='Provinsi', orientation='h', text='Estimasi Timbulan (Ton/Tahun)', color='Estimasi Timbulan (Ton/Tahun)', color_continuous_scale='Reds', title="Beban Timbulan B3 per Provinsi")
    fig_b3.update_layout(plot_bgcolor="white", paper_bgcolor="white", font=dict(color="#333"), margin=dict(l=0, r=0, t=40, b=0))
    save_plotly(fig_b3, VIS / "chart_6_1c_b3_beban.png")

# 4. CO2 Deforestasi Emisi Area Chart
if not df_gfw.empty:
    df_emisi_trend = df_gfw.groupby(['Tahun', 'Provinsi'])['Total_Emisi_CO2_Megagram'].sum().reset_index()
    fig_emisi = px.area(df_emisi_trend, x='Tahun', y='Total_Emisi_CO2_Megagram', color='Provinsi', title="Tren Emisi Karbon Akibat Deforestasi (2014-2023)")
    fig_emisi.update_layout(plot_bgcolor="white", paper_bgcolor="white", font=dict(color="#333"), margin=dict(l=0, r=0, t=40, b=0))
    save_plotly(fig_emisi, VIS / "chart_6_1d_co2_emisi.png")

# 5. Air IKA Line Chart
if not df_ika.empty:
    df_ika_long = df_ika.rename(columns={'Indeks Kualitas Air': 'Nilai IKA'})
    fig_ika = px.line(df_ika_long, x='Tahun', y='Nilai IKA', color='Provinsi', markers=True, color_discrete_map=color_map_prov, title="Indeks Kualitas Air (IKA)")
    fig_ika.update_layout(plot_bgcolor="white", paper_bgcolor="white", font=dict(color="#333"), margin=dict(l=0, r=0, t=40, b=0))
    save_plotly(fig_ika, VIS / "chart_6_2a_ika_line.png")

# 6. Diare Area Chart
if not df_kes.empty:
    df_diare_trend = df_diare.copy()
    df_diare_trend['Kategori'] = df_diare_trend['provinsi'].apply(lambda x: 'Sentra Tambang' if x in ['Sulawesi Tengah', 'Sulawesi Tenggara'] else 'Non-Sentra')
    df_d_agg = df_diare_trend.groupby(['tahun', 'Kategori'])['nilai'].sum().reset_index()
    fig_diare = px.area(df_d_agg, x='tahun', y='nilai', color='Kategori', title="Kasus Diare (Sentra Tambang vs Non-Sentra)")
    fig_diare.update_layout(plot_bgcolor="white", paper_bgcolor="white", font=dict(color="#333"), margin=dict(l=0, r=0, t=40, b=0))
    save_plotly(fig_diare, VIS / "chart_6_2b_diare_area.png")

# 7. Konflik Nelayan Bar Chart
if not df_konflik_air.empty and 'tahun' in df_konflik_air.columns:
    df_k_trend = df_konflik_air.groupby('tahun').size().reset_index(name='Jumlah')
    df_k_trend = df_k_trend[df_k_trend['tahun'] >= 2020]
    fig_nelayan = px.bar(df_k_trend, x='tahun', y='Jumlah', title="Frekuensi Letusan Konflik Pesisir & Nelayan (5 Tahun Terakhir)")
    fig_nelayan.update_layout(plot_bgcolor="white", paper_bgcolor="white", font=dict(color="#333"), margin=dict(l=0, r=0, t=40, b=0))
    save_plotly(fig_nelayan, VIS / "chart_6_2c_konflik_nelayan.png")

# 8. Tailing Treemap
if not df_b3.empty:
    fig_tailing = px.treemap(df_b3, path=['Provinsi', 'Kawasan/Perusahaan'], values='Estimasi Timbulan (Ton/Tahun)', color='Estimasi Timbulan (Ton/Tahun)', color_continuous_scale='Blues', title="Proporsi Beban Limbah Tailing & B3 ke Ekosistem Air")
    fig_tailing.update_layout(plot_bgcolor="white", paper_bgcolor="white", font=dict(color="#333"), margin=dict(l=0, r=0, t=40, b=0))
    save_plotly(fig_tailing, VIS / "chart_6_2d_tailing_treemap.png")

# 9. Bencana BNPB Bar Chart
if not df_bencana.empty:
    df_b = df_bencana.copy()
    df_b['tahun'] = pd.to_numeric(df_b['tahun'], errors='coerce')
    df_b['jumlah_kejadian'] = pd.to_numeric(df_b['jumlah_kejadian'], errors='coerce').fillna(0)
    df_b_trend = df_b.groupby(['tahun', 'provinsi'])['jumlah_kejadian'].sum().reset_index()
    fig_bencana = px.bar(df_b_trend, x='tahun', y='jumlah_kejadian', color='provinsi', title="Frekuensi Bencana Hidrometeorologi (Banjir & Longsor)")
    fig_bencana.update_layout(plot_bgcolor="white", paper_bgcolor="white", font=dict(color="#333"), margin=dict(l=0, r=0, t=40, b=0))
    save_plotly(fig_bencana, VIS / "chart_6_3a_bencana_bnpb.png")

# 10. Deforestasi GFW Line Chart
if not df_gfw.empty:
    df_g = df_gfw.copy()
    df_g['Tahun'] = pd.to_numeric(df_g['Tahun'], errors='coerce')
    df_g['Total_Deforestasi_Ha'] = pd.to_numeric(df_g['Total_Deforestasi_Ha'], errors='coerce').fillna(0)
    df_g_trend = df_g.groupby(['Tahun', 'Provinsi'])['Total_Deforestasi_Ha'].sum().reset_index()
    fig_gfw_line = px.line(df_g_trend, x='Tahun', y='Total_Deforestasi_Ha', color='Provinsi', markers=True, title="Laju Deforestasi Akibat Pertambangan & Sawit")
    fig_gfw_line.update_layout(plot_bgcolor="white", paper_bgcolor="white", font=dict(color="#333"), margin=dict(l=0, r=0, t=40, b=0))
    save_plotly(fig_gfw_line, VIS / "chart_6_3b_deforestasi_gfw.png")

# 11. Kawasan Lindung GFW Area Chart
if not df_gfw_lindung.empty:
    df_gl = df_gfw_lindung.copy()
    df_gl['Tahun'] = pd.to_numeric(df_gl['Tahun'], errors='coerce')
    df_gl['Luas_Hilang_Kawasan_Lindung_Ha'] = pd.to_numeric(df_gl['Luas_Hilang_Kawasan_Lindung_Ha'], errors='coerce').fillna(0)
    df_gl_trend = df_gl.groupby(['Tahun', 'Provinsi'])['Luas_Hilang_Kawasan_Lindung_Ha'].sum().reset_index()
    fig_lindung = px.area(df_gl_trend, x='Tahun', y='Luas_Hilang_Kawasan_Lindung_Ha', color='Provinsi', title="Deforestasi di Kawasan Lindung (Protected Areas)")
    fig_lindung.update_layout(plot_bgcolor="white", paper_bgcolor="white", font=dict(color="#333"), margin=dict(l=0, r=0, t=40, b=0))
    save_plotly(fig_lindung, VIS / "chart_6_3c_kawasan_lindung.png")

# 12. Drivers Deforestation Pie Chart
if not df_gfw_driver.empty:
    df_gd = df_gfw_driver.copy()
    df_gd['Luas_Deforestasi_Ha'] = pd.to_numeric(df_gd['Luas_Deforestasi_Ha'], errors='coerce').fillna(0)
    df_gd_agg = df_gd.groupby('Faktor_Pendorong')['Luas_Deforestasi_Ha'].sum().reset_index()
    fig_drivers = px.pie(df_gd_agg, values='Luas_Deforestasi_Ha', names='Faktor_Pendorong', hole=0.3, title="Penyebab Utama Kehilangan Hutan (Drivers of Deforestation)")
    fig_drivers.update_layout(plot_bgcolor="white", paper_bgcolor="white", font=dict(color="#333"), margin=dict(l=0, r=0, t=40, b=0))
    save_plotly(fig_drivers, VIS / "chart_6_3d_drivers_pie.png")

# 13. Timeline Konflik vs Masalah Izin
if not df_konflik_fpic.empty and not df_kpa_izin.empty:
    df_ktl = df_konflik_fpic.copy()
    df_ktl['kategori'] = 'Konflik Pertambangan'
    df_ktl = df_ktl.rename(columns={'tahun': 'Tahun'})
    df_mtl = df_kpa_izin[df_kpa_izin['lokasi'].str.contains('Sulawesi', case=False, na=False)].copy()
    df_mtl['kategori'] = 'Masalah Izin (KPA)'
    df_mtl['Tahun'] = df_mtl['tahun_laporan'].astype(int)
    df_combtl = pd.concat([df_ktl[['Tahun', 'kategori']], df_mtl[['Tahun', 'kategori']]], ignore_index=True)
    df_combtl = df_combtl[df_combtl['Tahun'] >= 2000]
    df_tl_agg2 = df_combtl.groupby(['Tahun', 'kategori']).size().reset_index(name='Jumlah')
    fig_fpic_tl = px.bar(df_tl_agg2, x='Tahun', y='Jumlah', color='kategori', barmode='group', title='Timeline Historis: Konflik Pertambangan & Masalah Izin')
    fig_fpic_tl.update_layout(plot_bgcolor="white", paper_bgcolor="white", font=dict(color="#333"), margin=dict(l=0, r=0, t=40, b=0))
    save_plotly(fig_fpic_tl, VIS / "chart_6_4a_fpic_timeline.png")

# 14. Perampasan Lahan Area Chart
if not df_konflik.empty:
    df_kd = df_konflik[~df_konflik['sektor'].str.contains('air|laut|pesisir|nelayan|sungai|pulau|tailing', case=False, na=False)].copy()
    if 'tahun' in df_kd.columns:
        df_kd['tahun'] = pd.to_numeric(df_kd['tahun'], errors='coerce')
        df_kd_trend = df_kd.groupby(['tahun']).size().reset_index(name='jumlah')
        fig_perampasan = px.area(df_kd_trend, x='tahun', y='jumlah', title="Frekuensi Letusan Konflik Perampasan Lahan Tahunan")
        fig_perampasan.update_layout(plot_bgcolor="white", paper_bgcolor="white", font=dict(color="#333"), margin=dict(l=0, r=0, t=40, b=0))
        save_plotly(fig_perampasan, VIS / "chart_6_4b_perampasan_lahan.png")

# 15. Kriminalisasi Bar Chart
if not df_konflik.empty:
    krim_df = df_kd[df_kd['indikasi_kriminalisasi'] == True].copy()
    if 'tahun' in krim_df.columns:
        krim_df['tahun'] = pd.to_numeric(krim_df['tahun'], errors='coerce')
        krim_trend = krim_df.groupby('tahun').size().reset_index(name='jumlah')
        fig_krim_bar = px.bar(krim_trend, x='tahun', y='jumlah', title="Tren Insiden Kriminalisasi & Kekerasan Terhadap Warga")
        fig_krim_bar.update_layout(plot_bgcolor="white", paper_bgcolor="white", font=dict(color="#333"), margin=dict(l=0, r=0, t=40, b=0))
        save_plotly(fig_krim_bar, VIS / "chart_6_4c_kriminalisasi.png")

# 16. Faskes Line Chart
if not df_faskes.empty:
    df_f_plot = df_faskes[df_faskes['provinsi'].isin(['Sulawesi Tengah', 'Sulawesi Tenggara'])].copy()
    df_f_plot['jumlah'] = pd.to_numeric(df_f_plot['jumlah'], errors='coerce').fillna(0)
    df_f_plot['tahun'] = pd.to_numeric(df_f_plot['tahun'], errors='coerce')
    df_f_agg = df_f_plot.groupby(['tahun', 'provinsi'])['jumlah'].sum().reset_index()
    fig_faskes = px.line(df_f_agg, x='tahun', y='jumlah', color='provinsi', markers=True, title="Tren Jumlah Fisik Faskes (2014-2024)")
    fig_faskes.update_layout(plot_bgcolor="white", paper_bgcolor="white", font=dict(color="#333"), margin=dict(l=0, r=0, t=40, b=0))
    save_plotly(fig_faskes, VIS / "chart_6_4d_faskes_line.png")

# 17. IUP Baru Bar Chart
if not df_izin.empty:
    df_izin_plot = df_izin[df_izin['Tahun'] >= 2014].copy()
    fig_iup_baru = px.bar(df_izin_plot, x='Tahun', y='Jumlah_Izin_Baru', title="Lonjakan Penerbitan IUP di Era Krisis Lingkungan")
    fig_iup_baru.update_layout(plot_bgcolor="white", paper_bgcolor="white", font=dict(color="#333"), margin=dict(l=0, r=0, t=40, b=0))
    save_plotly(fig_iup_baru, VIS / "chart_6_5a_iup_baru.png")

# 18. Modus Pelanggaran Horizontal Bar
if not df_kpa_izin.empty:
    df_kpa_ex = df_kpa_izin.copy()
    df_kpa_ex['jenis_masalah_izin'] = df_kpa_ex['jenis_masalah_izin'].str.split('; ')
    df_kpa_ex = df_kpa_ex.explode('jenis_masalah_izin')
    masalah_counts = df_kpa_ex['jenis_masalah_izin'].value_counts().reset_index()
    masalah_counts.columns = ['Jenis Pelanggaran', 'Jumlah Korporat']
    fig_modus = px.bar(masalah_counts, x='Jumlah Korporat', y='Jenis Pelanggaran', orientation='h', title="Distribusi Modus Pelanggaran Izin Korporat")
    fig_modus.update_layout(plot_bgcolor="white", paper_bgcolor="white", font=dict(color="#333"), margin=dict(l=0, r=0, t=40, b=0))
    save_plotly(fig_modus, VIS / "chart_6_5b_modus_pelanggaran.png")

# 19. PLTU Status Pie Chart
if not df_pltu_captive.empty:
    pltu_status = df_pltu_captive.groupby('Status').size().reset_index(name='jumlah')
    fig_pltu_pie = px.pie(pltu_status, names='Status', values='jumlah', title="Proporsi Status PLTU Batubara Captive di Sulawesi", hole=0.4)
    fig_pltu_pie.update_layout(plot_bgcolor="white", paper_bgcolor="white", font=dict(color="#333"), margin=dict(l=0, r=0, t=40, b=0))
    save_plotly(fig_pltu_pie, VIS / "chart_6_5c_pltu_status_pie.png")

# ─── BUILD MARKDOWN ──────────────────────────────────────────────────────────
print("Writing 100% faithful chapter_6.md ...")

md = f"""# Bab 6: Audit Forensik Metodologi D3TLH

**CELIOS — Center of Economic and Law Studies**

*Fase 1: Evaluasi Kebijakan Ekstraktif - Pembuktian Terbalik*

---

> **Kesimpulan Eksekutif**
>
> Evaluasi empiris mengindikasikan perlunya perbaikan substansial dalam integrasi dokumen D3TLH dan AMDAL. Instrumen pengelolaan lingkungan perlu diperkuat agar mampu memetakan dampak akumulatif dan berfungsi sebagai pertimbangan yang lebih efektif dalam pengendalian perizinan investasi.

---

## Ringkasan Audit Kritis D3TLH

| Dimensi Audit | Skor Kerusakan | Status Vonis | Indikator Utama |
|---|---|---|---|
| **DAYA TAMPUNG UDARA** | **{skor_akumulasi_udara:.1f} / 10** | STATUS: EVALUASI KUALITAS UDARA - Analisis data menunjukkan korelasi antara aktivitas industri dan tren penyakit saluran pernapasan. | NOTE: Perlu pengawasan lebih ketat terhadap emisi industri \| Kapasitas PLTU: {kapasitas_terkini:,.0f} MW / NO2 NASA: {no2_terkini:.2e} / Rasio ISPA: {rasio_anomali:.1f}x |
| **DAYA TAMPUNG AIR** | **{skor_akumulasi_air:.1f} / 10** | STATUS: EVALUASI KUALITAS AIR - Pemantauan Indeks Kualitas Air dan prevalensi penyakit berbasis air sebagai indikator lingkungan. | NOTE: Pentingnya penguatan standar pemantauan limbah \| IKA Sulteng: {ika_sulteng:.1f} / Kasus Diare: {kasus_diare_sentra:,.0f} / Konflik Air: {jumlah_konflik_air} |
| **DAYA DUKUNG LAHAN** | **{skor_akumulasi_lahan:.1f} / 10** | STATUS: EVALUASI TATA GUNA LAHAN - Pemetaan dampak tutupan lahan terhadap risiko bencana hidrometeorologi. | NOTE: Perlu peninjauan tata ruang berbasis mitigasi bencana \| Bencana: {bencana_sulteng_sultra:,.0f} Kejadian / Deforestasi: {deforestasi_sentra:,.0f} Ha |
| **DAYA DUKUNG SOSIAL** | **{skor_akumulasi_sosial:.1f} / 10** | STATUS: EVALUASI SOSIAL AGRARIA - Pemantauan sengketa lahan dan dampaknya terhadap kesejahteraan masyarakat lokal. | NOTE: Pentingnya pendekatan dialogis dalam kebijakan agraria \| Konflik Lahan: {konflik_darat} Kasus TanahKita |
| **VETO KEBIJAKAN** | **{skor_akumulasi_veto:.1f} / 10** | STATUS: EVALUASI PERIZINAN - Peninjauan pemberian izin operasional industri dibandingkan dengan kapasitas ekologi. | NOTE: Penyelarasan izin dengan daya dukung lingkungan \| {izin_baru:,.0f} Izin Baru & {kapasitas_pltu/1000:,.1f} GW PLTU Captive Diloloskan |

---

## 1. Kerangka Analisis Evaluasi D3TLH

AMDAL dan D3TLH dirancang bersifat prediktif untuk menilai batasan daya dukung lingkungan sebelum izin diterbitkan. Evaluasi empiris diperlukan untuk menilai efektivitas instrumen ini dalam meredam dampak lingkungan dan sosial di lapangan.

**Standpoint Riset ECC:** 
Pendekatan riset menggunakan **Evaluasi Berbasis Bukti Empiris**. Analisis menyandingkan indikator daya dukung spasial dengan indikator empiris seperti tren kesehatan masyarakat, kejadian bencana hidrometeorologi, dan dinamika sengketa lahan guna mengukur sejauh mana daya dukung ekologis dan sosial telah tertekan.

Halaman ini merangkum indikator-indikator tersebut untuk memberikan rekomendasi perbaikan tata kelola lingkungan dan sistem perizinan.

---

## 2. Fakta: Metodologi Resmi D3TLH Pemerintah (Jasa Ekosistem)

Berdasarkan dokumen pedoman teknis D3TLH (seperti Permen LH 17/2009 dan panduan KLHK), pemerintah saat ini menyusun D3TLH dengan pendekatan murni spasial/bio-fisik yang disebut **Jasa Ekosistem (Ecosystem Services)**.

Indikator resmi yang digunakan dibagi menjadi 4 kategori:
*   **Jasa Penyediaan (Provisioning):** Kapasitas lahan menyediakan pangan, air bersih, dll.
*   **Jasa Pengaturan (Regulating):** Kapasitas tata air, mitigasi iklim, mitigasi banjir, pemurnian udara.
*   **Jasa Pendukung (Supporting):** Siklus hara, pembentukan tanah.
*   **Jasa Budaya (Cultural):** Estetika alam, rekreasi.

### Letak Cacat Metodologi (Blind Spots):

Rumus utama yang dipakai pemerintah untuk menghitung indeks di atas hanyalah: **Peta Ekoregion + Peta Tutupan Lahan (Land Cover)**.

*   **Abaikan Nyawa & Morbiditas:** Menghitung kapasitas udara dari peta vegetasi, namun **TIDAK PERNAH** menghitung rekam medis warga (ISPA) yang paru-parunya rusak akibat debu smelter.
*   **Abaikan Kedaulatan Ruang:** Mengukur kapasitas pertanian, tapi abai terhadap perampasan lahan yang memicu konflik sosial berdarah.
*   **Bukan Veto Kebijakan:** Saat D3TLH menyatakan daya dukung turun, instrumen ini tidak dipakai untuk "menyetop" penerbitan IUP (Izin Usaha Pertambangan) baru.

---

## 3. Matriks Pembuktian Terbalik: D3TLH vs Fakta Lapangan

Di sinilah seluruh temuan riset kita diintegrasikan untuk "menelanjangi" cacat bawaan D3TLH. Di bawah ini adalah benturan langsung antara **Mitos (Klaim Dokumen Resmi)** versus **Realitas Lapangan (Bukti Forensik)**.

---

### A. Audit D3TLH: Daya Tampung Udara

> **Klaim Mitos:** *"Daya tampung udara (berdasarkan peta tutupan lahan) dianalisis sebagai indikator kapasitas pemulihan emisi."*
>
> **Fakta Empiris:** Data menunjukkan tren penyakit saluran pernapasan di sekitar kawasan industri.
> **Akumulasi Skor Kerusakan:** **{skor_akumulasi_udara:.1f} / 10** — *STATUS: PERLU PENGAWASAN \| ANALISIS: Pemantauan Morbiditas Akumulatif*

#### 1. Korelasi PLTU & Kualitas Udara
Pemerintah sebelumnya mengklaim IKU 'Masih Aman'. Namun pantauan independen Satelit TROPOMI NASA mengungkap realitas lain: konsentrasi gas beracun NO2 meledak meroket sejajar dengan ekspansi PLTU captive. **Threshold Kritis NASA: NO2 > 6.0e-6 mol/m²**.

![PLTU vs NO2 NASA](visuals_bab6/chart_6_1a_pltu_no2.png)

#### 2. Dampak Kasus ISPA/Pneumonia
Dokumen daya dukung mengabaikan lonjakan tajam pasien ISPA di RSUD Morowali dan Kendari. Grafik membuktikan bahwa tren ISPA di provinsi non-tambang relatif stabil, namun meroket secara paralel dengan asap di provinsi sentra nikel.

![Insiden ISPA per 10.000 Penduduk](visuals_bab6/chart_6_1b_ispa_trend.png)

#### 3. Fakta Beban Limbah & Emisi
Data perizinan D3TLH fokus pada syarat emisi cerobong di atas kertas, tetapi mengabaikan gunung-gunung debu slag (fly ash) di darat yang bebas tertiup angin memapari puluhan desa setiap harinya. **Threshold Kritis: 30 Juta Ton/Tahun** = 7% dari total neraca B3 nasional 427 juta ton dari 1 provinsi (anomali 2,4x proporsional). Sumber: *KLHK LKj 2022, IKK Pengelolaan Limbah B3, Hal. 47*.

![Beban Timbulan B3 per Provinsi](visuals_bab6/chart_6_1c_b3_beban.png)

#### 4. Hilangnya Paru-Paru Udara (Emisi CO2)
Audit resmi pemerintah hanya menghitung 'emisi yang keluar dari corong pabrik', tetapi dengan sengaja mengaburkan 'emisi dari jutaan pohon yang mati' akibat ekspansi lahan tambang itu sendiri. **Threshold Kritis: 150 Juta Ton CO2e** = melampaui target NDC FOLU Net Sink 2030 (-140 juta ton CO2e). Sumber: *SK MenLHK No.SK.168/MENLHK/PKTL/PLA.1/2/2022, Bag. III, Hal. 5*.

![Emisi CO2 Akibat Deforestasi](visuals_bab6/chart_6_1d_co2_emisi.png)

---

### B. Audit D3TLH: Daya Tampung Air

> **Klaim Mitos:** *"Daya tampung air diukur berdasarkan rasio pengenceran alami dan neraca kualitas air."*
>
> **Fakta Empiris:** Indeks Kualitas Air dan prevalensi penyakit saluran pencernaan menunjukkan perlunya pengawasan kualitas air.
> **Akumulasi Skor Kerusakan:** **{skor_akumulasi_air:.1f} / 10** — *STATUS: PERLU PENGAWASAN \| ANALISIS: Pemantauan Toksisitas dan Sanitasi*

#### 1. Kualitas Air (IKA)
Klaim sungai/laut mampu mengencerkan limbah berbanding terbalik dengan hancurnya Indeks Kualitas Air BPS hingga menyentuh batas cemar kotor.

![Indeks Kualitas Air](visuals_bab6/chart_6_2a_ika_line.png)

#### 2. Morbiditas Diare
AMDAL gagal menghitung dampak kontaminasi logam berat ke air tanah yang dikonsumsi warga, dibuktikan dengan ledakan pasien Diare di lingkar tambang. **Threshold Kritis: Incidence Rate Ratio (IRR) > 2.0** (Risiko 2x lipat dari populasi rata-rata). Sumber: *Kemenkes Profil Kesehatan 2023, Hal. 112*.

![Kasus Diare](visuals_bab6/chart_6_2b_diare_area.png)

#### 3. Konflik Nelayan & Pesisir
Ekosistem tangkap nelayan dihancurkan oleh limbah tailing dan privatisasi pesisir untuk Smelter, memicu lonjakan konflik agraria laut.

![Konflik Nelayan & Pesisir](visuals_bab6/chart_6_2c_konflik_nelayan.png)

#### 4. Beban Tailing (Treemap B3)
Resiko kebocoran Tailings Dam (Bendungan Tailing) atau Deep Sea Tailing Placement (DSTP) yang ditutupi oleh klaim 'mitigasi teknologi'. **Threshold Kritis: 25 Juta Ton/Tahun** (Batas Kapasitas AMDAL Gabungan Kawasan IMIP & OSS). Sumber: *Dokumen AMDAL KLHK, PPID*.

![Proporsi Beban Limbah Tailing & B3](visuals_bab6/chart_6_2d_tailing_treemap.png)

---

### C. Audit D3TLH: Daya Dukung Lahan

> **Klaim Mitos:** *"Daya dukung lahan dianalisis berdasarkan kecukupan tutupan hutan dan batas fungsi kawasan."*
>
> **Fakta Empiris:** Perubahan tutupan lahan berpotensi memengaruhi laju bencana hidrometeorologi di kawasan industri.
> **Skor Kerusakan Lahan:** **{skor_akumulasi_lahan:.1f} / 10** — *STATUS: PERLU PENGAWASAN \| ANALISIS: Evaluasi Pengelolaan Lanskap*

#### 1. Bencana Banjir & Longsor (BNPB)
Data BNPB membuktikan bahwa klaim 'mitigasi bencana' dalam AMDAL sama sekali tidak terbukti di lapangan.

![Bencana Hidrometeorologi](visuals_bab6/chart_6_3a_bencana_bnpb.png)

#### 2. Deforestasi Primer (GFW)
Hutan primer yang berfungsi sebagai jasa penyediaan air dan penyerap karbon ditebang habis atas nama IUP.

![Laju Deforestasi Pertambangan & Sawit](visuals_bab6/chart_6_3b_deforestasi_gfw.png)

#### 3. Pelanggaran Kawasan Lindung
Temuan **paling mematikan**: Data GFW membuktikan bahwa **100% dari setiap Ha deforestasi** yang terjadi di Sulteng dan Sultra selama 10 tahun (2014–2023) terjadi di dalam **Kawasan Lindung / Protected Areas (IUCN)**. Tidak ada satu pun hektar yang dibabat di luar batas kawasan yang seharusnya tidak boleh disentuh.

![Deforestasi Kawasan Lindung](visuals_bab6/chart_6_3c_kawasan_lindung.png)

#### 4. Aktor Deforestasi
Data atribusi GFW mematahkan alibi 'ladang berpindah'. Pertambangan dan Sawit adalah aktor dominan penghancur hutan. ⚠️ *Catatan: Data GFW untuk Sulteng absen/kosong, angka setengah juta hektar ini MURNI dari Sulawesi Tenggara saja.*

![Drivers of Deforestation](visuals_bab6/chart_6_3d_drivers_pie.png)

---

### D. Audit D3TLH: Daya Dukung Sosial

> **Klaim Mitos:** *"Status kawasan dialokasikan untuk peruntukan industri dengan pelaksanaan konsultasi publik."*
>
> **Fakta Empiris:** Pentingnya transparansi dan pelibatan masyarakat lokal dalam penataan ruang dan perizinan.
> **Skor Kerusakan Sosial:** **{skor_akumulasi_sosial:.1f} / 10** — *STATUS: PERLU PENGAWASAN \| ANALISIS: Pelibatan Masyarakat Lokal*

#### 1. Manipulasi Persetujuan FPIC
'Persetujuan Warga' hanyalah stempel karet. Data investigasi Konsorsium Pembaruan Agraria membuktikan perusahaan memanipulasi persetujuan (FPIC) sejak fase sosialisasi AMDAL.

![Timeline Konflik Tambang vs Masalah Izin](visuals_bab6/chart_6_4a_fpic_timeline.png)

#### 2. Perampasan Ruang Hidup
Setelah izin keluar lewat manipulasi, perampasan paksa terjadi. Ruang hidup warga menyusut drastis, memicu letusan konflik yang berdampak pada ratusan ribu korban jiwa.

![Frekuensi Letusan Konflik Perampasan Lahan](visuals_bab6/chart_6_4b_perampasan_lahan.png)

#### 3. Kriminalisasi Warga
Di fase akhir, ketika warga melakukan penolakan yang sah atas perampasan, negara tidak hadir melindungi, melainkan mengirim aparat untuk memenjarakan mereka.

![Insiden Kriminalisasi & Kekerasan](visuals_bab6/chart_6_4c_kriminalisasi.png)

#### 4. Defisit Layanan Dasar (Faskes)
Di tengah ekspor nikel sentra Sulawesi yang meledak ratusan kali lipat, kualitas layanan dasar hancur. Mayoritas Puskesmas gagal memenuhi standar minimal **Sarana, Prasarana, dan Alat Kesehatan (SPA)**. Klaim AMDAL tentang 'peningkatan kesejahteraan' adalah fiksi belaka.

![Tren Jumlah Fisik Faskes](visuals_bab6/chart_6_4d_faskes_line.png)

---

### E. Audit D3TLH: Veto Kebijakan

> **Klaim Mitos:** *"Penyusunan D3TLH dirancang sebagai pertimbangan dalam membatasi izin eksploitasi."*
>
> **Fakta Empiris:** Evaluasi menunjukkan pentingnya penguatan kepatuhan hukum dan efektivitas instrumen pengendalian perizinan.
> **Skor Kegagalan Tata Kelola:** **{skor_akumulasi_veto:.1f} / 10** — *STATUS: PERLU REFORMASI \| ANALISIS: Penguatan Pengawasan Kebijakan*

#### 1. Obral Konsesi Legal
Di tengah memuncaknya status krisis daya dukung lingkungan, pemerintah secara paradoks justru menerbitkan ratusan izin eksploitasi tambang (IUP) baru. Dokumen veto tidak berfungsi.

![Lonjakan Penerbitan IUP Baru](visuals_bab6/chart_6_5a_iup_baru.png)

#### 2. Pembiaran Pelanggaran Korporat
Bukti mutlak 'Regulatory Capture'—bahkan ketika perusahaan beroperasi ilegal, menabrak izin, tumpang tindih, atau HGU kedaluwarsa, negara tidak berani melakukan penegakan hukum dan membiarkannya.

![Distribusi Modus Pelanggaran Izin Korporat](visuals_bab6/chart_6_5b_modus_pelanggaran.png)

#### 3. Karpet Merah Energi Kotor (PLTU Captive)
Inkonsistensi paling telanjang terhadap komitmen iklim. Di wilayah ekoregion krisis, pemerintah memberikan karpet merah pembangunan infrastruktur penyumbang emisi terbesar (PLTU Batubara Captive) khusus untuk menyuplai kawasan smelter nikel.

![Proporsi Status PLTU Captive](visuals_bab6/chart_6_5c_pltu_status_pie.png)
"""

out_path = HERE / "chapter_6.md"
out_path.write_text(md, encoding="utf-8")
print(f"Done! 100% faithful chapter_6.md saved to {out_path}")
