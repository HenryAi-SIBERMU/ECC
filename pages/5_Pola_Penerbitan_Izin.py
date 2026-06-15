import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import scipy.stats as stats
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.components.sidebar import render_sidebar

st.set_page_config(page_title="CELIOS ECC - Pola Perizinan", layout="wide", initial_sidebar_state="expanded")
render_sidebar()

# Custom CSS for UI Guidelines
st.markdown("""
<style>
    .metric-card {
        background: #1E1E1E;
        padding: 20px;
        border-radius: 10px;
        border-top: 4px solid #5C2B6A;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .metric-title {
        color: #9E9E9E;
        font-size: 1rem;
        margin-bottom: 5px;
    }
    .metric-value {
        color: #FFF;
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0;
    }
    .kritis-text { color: #E53935; font-weight: bold; }
    .tertekan-text { color: #FFB300; font-weight: bold; }
    .normal-text { color: #43A047; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("5. Anomali Tata Kelola: Izin Baru di Tengah Krisis Ekologis")
st.markdown("""
<div style="background:#1E1E1E; padding:15px; border-left:5px solid #FFC107; border-radius:5px; margin-bottom:20px;">
    <strong>Fokus Analisis (D3TLH Section 4.5)</strong><br>
    Halaman ini menguji hipotesis tata kelola: <i>"Apakah negara tetap menerbitkan izin konsesi baru meskipun indikator tekanan ekologis (Daya Dukung Lingkungan) di tahun sebelumnya sudah menunjukkan status Tertekan atau Kritis?"</i>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 1. DATA PREPARATION & MERGING
# -------------------------------------------------------------
@st.cache_data
def load_and_merge_data():
    base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'processed')
    
    # Load all 4 datasets
    df_izin = pd.read_csv(os.path.join(base_dir, 'sulawesi_izin_baru_per_tahun.csv'))
    df_defor = pd.read_csv(os.path.join(base_dir, 'sulawesi_gfw_master_1_dekade_2014_2023.csv'))
    df_ika = pd.read_csv(os.path.join(base_dir, 'sulawesi_ika_2016_2024.csv'))
    df_iku = pd.read_csv(os.path.join(base_dir, 'sulawesi_iku_2015_2024.csv'))
    
    # Standardize types and strings
    df_izin['Tahun'] = df_izin['Tahun'].astype(int)
    df_defor['Tahun'] = df_defor['Tahun'].astype(int)
    df_ika['Tahun'] = df_ika['Tahun'].astype(int)
    df_iku['Tahun'] = df_iku['Tahun'].astype(int)
    
    for df in [df_izin, df_defor, df_ika, df_iku]:
        df['Provinsi'] = df['Provinsi'].str.strip().str.title()
        
    df_defor = df_defor.rename(columns={'Total_Deforestasi_Ha': 'Deforestasi_Ha'})
    df_ika = df_ika.rename(columns={'Indeks Kualitas Air': 'IKA'})
    
    # Merge master based on Provinsi and Tahun
    df_master = df_izin.merge(df_defor[['Provinsi', 'Tahun', 'Deforestasi_Ha']], on=['Provinsi', 'Tahun'], how='outer')
    df_master = df_master.merge(df_ika[['Provinsi', 'Tahun', 'IKA']], on=['Provinsi', 'Tahun'], how='outer')
    df_master = df_master.merge(df_iku[['Provinsi', 'Tahun', 'IKU']], on=['Provinsi', 'Tahun'], how='outer')
    
    df_master = df_master[df_master['Tahun'].between(2015, 2023)].copy()
    df_master['Jumlah_Izin_Baru'] = df_master['Jumlah_Izin_Baru'].fillna(0)
    
    # Shift environment metrics to T-1 (Previous Year)
    # This aligns the logic: "If environment was critical in 2018, how many permits were issued in 2019?"
    df_env = df_master[['Provinsi', 'Tahun', 'Deforestasi_Ha', 'IKA', 'IKU']].copy()
    df_env['Tahun'] = df_env['Tahun'] + 1
    df_env = df_env.rename(columns={'Deforestasi_Ha': 'Defor_prev', 'IKA': 'IKA_prev', 'IKU': 'IKU_prev'})
    
    df_merged = df_master[['Provinsi', 'Tahun', 'Jumlah_Izin_Baru']].merge(df_env, on=['Provinsi', 'Tahun'], how='left')
    df_merged = df_merged.dropna(subset=['Defor_prev']).copy()
    
    def classify_status(row):
        # Klasifikasi KLHK: Sangat Kurang (<50), Kurang (50-70), Cukup/Baik (>70)
        # Fallback to Deforestation if IKA/IKU is NaN
        if pd.notna(row['IKA_prev']):
            if row['IKA_prev'] < 50: return 'Kritis'
            elif row['IKA_prev'] < 70: return 'Tertekan'
            else: return 'Aman / Normal'
        elif pd.notna(row['IKU_prev']):
            if row['IKU_prev'] < 50: return 'Kritis'
            elif row['IKU_prev'] < 70: return 'Tertekan'
            else: return 'Aman / Normal'
        else:
            # Fallback based on Deforestation quantiles
            if row['Defor_prev'] > 50000: return 'Kritis'
            elif row['Defor_prev'] > 20000: return 'Tertekan'
            else: return 'Aman / Normal'
            
    df_merged['Status_Ekologis_T_1'] = df_merged.apply(classify_status, axis=1)
    df_merged['Ada_Izin_Baru'] = df_merged['Jumlah_Izin_Baru'].apply(lambda x: 'Ya (Diterbitkan)' if x > 0 else 'Tidak Diterbitkan')
    
    return df_merged, df_master

df_analisis, df_raw = load_and_merge_data()

# Summary Metrics
total_izin_kritis = df_analisis[df_analisis['Status_Ekologis_T_1'] == 'Kritis']['Jumlah_Izin_Baru'].sum()
total_izin_tertekan = df_analisis[df_analisis['Status_Ekologis_T_1'] == 'Tertekan']['Jumlah_Izin_Baru'].sum()
total_izin_aman = df_analisis[df_analisis['Status_Ekologis_T_1'] == 'Aman / Normal']['Jumlah_Izin_Baru'].sum()

st.markdown("#### A. Ringkasan Eksekutif Penerbitan Izin")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="metric-card" style="border-top-color: #E53935;">
        <div class="metric-title">Izin Terbit di Zona Kritis (< 50 IKA)</div>
        <div class="metric-value" style="color: #E53935;">{int(total_izin_kritis)} <span style="font-size:1rem; color:#AAA;">Izin</span></div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-card" style="border-top-color: #FFB300;">
        <div class="metric-title">Izin Terbit di Zona Tertekan (50-70 IKA)</div>
        <div class="metric-value" style="color: #FFB300;">{int(total_izin_tertekan)} <span style="font-size:1rem; color:#AAA;">Izin</span></div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="metric-card" style="border-top-color: #43A047;">
        <div class="metric-title">Izin Terbit di Zona Aman (> 70 IKA)</div>
        <div class="metric-value" style="color: #43A047;">{int(total_izin_aman)} <span style="font-size:1rem; color:#AAA;">Izin</span></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------------------------------------
# 2. TIMELINE OVERLAY VISUALIZATION
# -------------------------------------------------------------
st.markdown("#### B. Pemetaan Waktu: Tekanan Ekologis vs Penerbitan Izin")
st.write("Grafik di bawah membandingkan tren Indeks Kualitas Air (garis merah) sebagai proksi daya dukung lingkungan melawan jumlah penerbitan izin baru (batang ungu). Seharusnya, ketika IKA turun mendekati batas kritis, penerbitan izin ikut ditekan (Moratorium).")

# Prepare agg data for chart
df_chart = df_raw.groupby('Tahun').agg({
    'Jumlah_Izin_Baru': 'sum',
    'IKA': 'mean',
    'Deforestasi_Ha': 'sum'
}).reset_index()

fig_timeline = go.Figure()

# Bar Chart for Permits
fig_timeline.add_trace(
    go.Bar(
        x=df_chart['Tahun'],
        y=df_chart['Jumlah_Izin_Baru'],
        name="Jumlah Izin Baru",
        marker_color='#5C2B6A',
        opacity=0.8,
        yaxis='y1'
    )
)

# Line Chart for IKA
fig_timeline.add_trace(
    go.Scatter(
        x=df_chart['Tahun'],
        y=df_chart['IKA'],
        name="Rata-rata IKA (Lingkungan)",
        mode='lines+markers',
        line=dict(color='#FF5252', width=3),
        marker=dict(size=8, symbol='circle'),
        yaxis='y2'
    )
)

# Layout setup for Dual Axis
fig_timeline.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    hovermode='x unified',
    margin=dict(l=40, r=40, t=40, b=40),
    xaxis=dict(title='Tahun', showgrid=False, dtick=1),
    yaxis=dict(
        title='Jumlah Izin Baru Diterbitkan',
        showgrid=True,
        gridcolor='rgba(255,255,255,0.1)'
    ),
    yaxis2=dict(
        title='Indeks Kualitas Air (0-100)',
        overlaying='y',
        side='right',
        range=[40, 100],
        showgrid=False
    ),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig_timeline, use_container_width=True)

with st.expander("Lihat Data Mentah Komparasi", expanded=False):
    st.dataframe(df_analisis, use_container_width=True, hide_index=True)


# -------------------------------------------------------------
# 3. UJI STATISTIK CROSSTAB & CHI-SQUARE
# -------------------------------------------------------------
st.markdown("---")
st.markdown("#### C. Pembuktian Statistik (Crosstab & Chi-Square)")
st.markdown('<span style="background:#1E88E5;color:#E3F2FD;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: SPSS-Style Crosstabulation</span>', unsafe_allow_html=True)
st.markdown("Tabel silang ini menyandingkan **Status Ekologis Tahun Sebelumnya (T-1)** dengan Keputusan **Penerbitan Izin di Tahun Berjalan (T)**.")

crosstab_result = pd.crosstab(df_analisis['Status_Ekologis_T_1'], df_analisis['Ada_Izin_Baru'])
crosstab_pct = pd.crosstab(df_analisis['Status_Ekologis_T_1'], df_analisis['Ada_Izin_Baru'], normalize='index') * 100

st.write("**Tabel Crosstab: Status Ekologis T-1 vs Keputusan Izin T**")
st.dataframe(crosstab_result, use_container_width=True)

# Chi-Square Calculation
chi2, p_val, dof, expected = stats.chi2_contingency(crosstab_result)

st.markdown(f"""
<div style="background:#2C2C2C; padding:15px; border-radius:5px; border-left:4px solid #1E88E5; font-family: monospace; font-size: 0.9rem;">
    <b>Pearson Chi-Square Test</b><br>
    Chi-Square Value : {chi2:.4f}<br>
    P-Value          : {p_val:.4f}<br>
    Degrees of Freedom: {dof}
</div>
""", unsafe_allow_html=True)

if p_val < 0.05:
    st.success(f"**Interpretasi**: Secara statistik (p < 0.05), terdapat korelasi signifikan antara status lingkungan dengan penerbitan izin. Namun, melihat distribusinya, korelasi ini justru menunjukkan bahwa izin **tetap diterbitkan** bahkan saat status tertekan/kritis.")
else:
    st.warning(f"**Interpretasi**: Secara statistik (p = {p_val:.4f} > 0.05), tidak ada hubungan yang signifikan antara status lingkungan dan keputusan izin. **Artinya, instrumen D3TLH (Status Lingkungan) diabaikan sepenuhnya dalam proses pengambilan keputusan izin baru.** Negara menerbitkan izin secara independen tanpa mempedulikan daya dukung lingkungan.")

st.markdown("""
<br>
<div style="background:#1E1E1E; padding:14px; border-radius:10px; border-left:5px solid #E53935; margin-top: 10px;">
    <b>Kesimpulan Sub-Bab 4.5:</b> Fakta bahwa ratusan izin baru terus diterbitkan di wilayah yang Indeks Kualitas Lingkungannya berstatus <i>Tertekan</i> dan <i>Kritis</i> adalah bukti kegagalan tata kelola (Governance Failure). D3TLH tereduksi hanya menjadi dokumen administratif pemanis yang tidak memiliki kekuatan <i>veto</i> ekologis.
</div>
""", unsafe_allow_html=True)
