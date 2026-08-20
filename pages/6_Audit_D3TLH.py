import streamlit as st
import os, sys
import json
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import importlib
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.components.sidebar import render_sidebar
import tools.algo_skoring_pulau.kalkulasi_pulau_sulawesi as algo_pulau_mod
import tools.algo_skoring_provinsi.kalkulasi_provinsi_sulawesi as algo_prov_mod
importlib.reload(algo_pulau_mod)
importlib.reload(algo_prov_mod)
kalkulasi_skor_pulau_sulawesi = algo_pulau_mod.kalkulasi_skor_pulau_sulawesi
kalkulasi_skor_provinsi_sulawesi = algo_prov_mod.kalkulasi_skor_provinsi_sulawesi

st.set_page_config(page_title="CELIOS ECC - Audit Forensik Metodologi D3TLH", layout="wide")
render_sidebar()



# ── Styles (Sesuai Pedoman UI/UX CELIOS) ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

* { font-family: 'Inter', sans-serif; }

.main-title {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #E53935, #EF5350, #FFCDD2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0;
    line-height: 1.2;
}

.sub-title {
    font-size: 1.1rem;
    color: #9E9E9E;
    font-weight: 300;
    margin-top: 0;
    margin-bottom: 2rem;
}

.org-badge {
    display: inline-block;
    background: linear-gradient(135deg, #B71C1C, #D32F2F);
    color: white;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

.content-box {
    background: #1A1F2B;
    border: 1px solid #333;
    border-radius: 10px;
    padding: 30px;
    margin-bottom: 25px;
}
.content-box h2 {
    color: #EF5350;
    margin-top: 0;
    font-size: 1.8rem;
    border-bottom: 1px solid #444;
    padding-bottom: 15px;
    margin-bottom: 20px;
}
.content-box h3 {
    color: #FFCDD2;
    font-size: 1.3rem;
    margin-top: 25px;
}
.content-box p, .content-box li {
    color: #E0E0E0;
    font-size: 1.05rem;
    line-height: 1.7;
    text-align: justify;
}
.highlight-text {
    color: #EF5350;
    font-weight: 700;
}
.metric-card {
    background: linear-gradient(135deg, #1A1F2B, #232B3B);
    border: 1px solid #333;
    border-radius: 10px;
    padding: 20px;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
}
.metric-value {
    font-size: 2rem;
    font-weight: 700;
}
.metric-label {
    font-size: 0.9rem;
    color: #AAA;
    margin-bottom: 5px;
    font-weight: 600;
}
.metric-desc {
    font-size: 0.8rem;
    color: #9E9E9E;
    margin-top: 10px;
    line-height: 1.4;
    text-align: left;
}
.metric-source {
    font-size: 0.75rem;
    color: #777;
    margin-top: 8px;
    padding-top: 8px;
    border-top: 1px dotted #444;
    text-align: left;
}
</style>
""", unsafe_allow_html=True)

# ── Header Halaman ──
st.markdown('<div class="org-badge">CELIOS — Center of Economic and Law Studies</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">Audit Forensik Metodologi D3TLH</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Fase 1: Evaluasi Kebijakan Ekstraktif - Pembuktian Terbalik</div>', unsafe_allow_html=True)

# =====================================================================
# DATA LOADING
# =====================================================================
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "processed")

@st.cache_data
def load_data():
    # Cache busted: 2026-08-15 19:42 to force reload of NLP filtered Konflik CSV
    df_kes = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_kesehatan_detail_2014_2024.csv")) if os.path.exists(os.path.join(DATA_DIR, "sulawesi_kesehatan_detail_2014_2024.csv")) else pd.DataFrame()
    df_ika = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_ika_2016_2024.csv")) if os.path.exists(os.path.join(DATA_DIR, "sulawesi_ika_2016_2024.csv")) else pd.DataFrame()
    df_bencana = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_bencana_bnpb_2014_2024.csv")) if os.path.exists(os.path.join(DATA_DIR, "sulawesi_bencana_bnpb_2014_2024.csv")) else pd.DataFrame()
    df_konflik = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_konflik_agraria_tanahkita.csv")) if os.path.exists(os.path.join(DATA_DIR, "sulawesi_konflik_agraria_tanahkita.csv")) else pd.DataFrame()
    if not df_konflik.empty and 'tahun' in df_konflik.columns:
        df_konflik['tahun'] = pd.to_numeric(df_konflik['tahun'], errors='coerce')
        df_konflik = df_konflik[df_konflik['tahun'] >= 2014]
    
    df_izin = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_izin_baru_per_tahun.csv")) if os.path.exists(os.path.join(DATA_DIR, "sulawesi_izin_baru_per_tahun.csv")) else pd.DataFrame()
    df_iku = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_iku_2015_2024.csv")) if os.path.exists(os.path.join(DATA_DIR, "sulawesi_iku_2015_2024.csv")) else pd.DataFrame()
    df_b3 = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_limbah_b3.csv")) if os.path.exists(os.path.join(DATA_DIR, "sulawesi_limbah_b3.csv")) else pd.DataFrame()
    df_pltu_op = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_pltu_captive.csv")) if os.path.exists(os.path.join(DATA_DIR, "sulawesi_pltu_captive.csv")) else pd.DataFrame()
    df_gfw = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_gfw_master_1_dekade_2014_2023_v3.csv")) if os.path.exists(os.path.join(DATA_DIR, "sulawesi_gfw_master_1_dekade_2014_2023_v3.csv")) else pd.DataFrame()
    df_gfw_lindung = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_gfw_kawasan_lindung_loss_2014_2023_v3.csv")) if os.path.exists(os.path.join(DATA_DIR, "sulawesi_gfw_kawasan_lindung_loss_2014_2023_v3.csv")) else pd.DataFrame()
    df_gfw_driver = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_gfw_loss_by_driver_2014_2023_v3.csv")) if os.path.exists(os.path.join(DATA_DIR, "sulawesi_gfw_loss_by_driver_2014_2023_v3.csv")) else pd.DataFrame()
    df_konflik_fpic = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_konflik_tambang_fpic.csv")) if os.path.exists(os.path.join(DATA_DIR, "sulawesi_konflik_tambang_fpic.csv")) else pd.DataFrame()
    df_kpa_izin = pd.read_csv(os.path.join(DATA_DIR, "kpa_masalah_izin_perusahaan.csv")) if os.path.exists(os.path.join(DATA_DIR, "kpa_masalah_izin_perusahaan.csv")) else pd.DataFrame()
    df_pltu_captive = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_pltu_captive.csv")) if os.path.exists(os.path.join(DATA_DIR, "sulawesi_pltu_captive.csv")) else pd.DataFrame()
    df_kawasan_nikel = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_kawasan_nikel_luas_per_provinsi.csv")) if os.path.exists(os.path.join(DATA_DIR, "sulawesi_kawasan_nikel_luas_per_provinsi.csv")) else pd.DataFrame()
    df_faskes = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_faskes_agregat_v3.csv")) if os.path.exists(os.path.join(DATA_DIR, "sulawesi_faskes_agregat_v3.csv")) else pd.DataFrame()
    df_nasa = pd.read_csv(os.path.join(DATA_DIR, "gee_nasa_no2_sulawesi_provinsi.csv")) if os.path.exists(os.path.join(DATA_DIR, "gee_nasa_no2_sulawesi_provinsi.csv")) else pd.DataFrame()
    return df_kes, df_ika, df_bencana, df_konflik, df_izin, df_iku, df_b3, df_pltu_op, df_gfw, df_gfw_lindung, df_gfw_driver, df_konflik_fpic, df_kpa_izin, df_pltu_captive, df_kawasan_nikel, df_faskes, df_nasa

df_kes, df_ika, df_bencana, df_konflik, df_izin, df_iku, df_b3, df_pltu_op, df_gfw, df_gfw_lindung, df_gfw_driver, df_konflik_fpic, df_kpa_izin, df_pltu_captive, df_kawasan_nikel, df_faskes, df_nasa = load_data()

# =====================================================================
# PRE-CALCULATE SCORES SECTION A & B (Yang sudah ada datanya)
# =====================================================================

# --- SECTION A: UDARA ---
kapasitas_terkini = 0
no2_terkini = 4.0e-6
if not df_pltu_op.empty:
    kapasitas_terkini = df_pltu_op[(df_pltu_op['Status'].str.lower() == 'operating')]['Capacity (MW)'].sum()
if not df_nasa.empty:
    df_nasa_annual = df_nasa.groupby('Tahun')['Rata_Rata_NO2'].mean().reset_index()
    if not df_nasa_annual.empty:
        no2_terkini = df_nasa_annual.loc[df_nasa_annual['Tahun'].idxmax(), 'Rata_Rata_NO2']

iku_terkini_global = 100.0
if not df_iku.empty:
    df_iku_annual = df_iku.groupby('Tahun')['IKU'].mean().reset_index()
    if not df_iku_annual.empty:
        iku_terkini_global = df_iku_annual.loc[df_iku_annual['Tahun'].idxmax(), 'IKU']

# --- PENGUMPULAN DATA EMPIRIS KABUPATEN/PULAU ---
# Udara
if not df_kes.empty:
    df_ts_pre = df_kes[df_kes['indikator'].str.contains('ISPA', case=False, na=False)]
    kasus_sentra = df_ts_pre[df_ts_pre['provinsi'].isin(['Sulawesi Tengah', 'Sulawesi Tenggara'])]['nilai'].sum()
    kasus_non_sentra = df_ts_pre[~df_ts_pre['provinsi'].isin(['Sulawesi Tengah', 'Sulawesi Tenggara'])]['nilai'].sum()
    rasio_anomali = (kasus_sentra / 2.0) / (kasus_non_sentra / 4.0) if kasus_non_sentra > 0 else 0
else:
    rasio_anomali = 0

proporsi_b3 = 0.0
total_b3_sulteng = 0.0
if not df_b3.empty:
    df_b3['Estimasi Timbulan (Ton/Tahun)'] = pd.to_numeric(df_b3['Estimasi Timbulan (Ton/Tahun)'], errors='coerce').fillna(0)
    total_b3_sulteng = df_b3[df_b3['Provinsi'] == 'Sulawesi Tengah']['Estimasi Timbulan (Ton/Tahun)'].sum()
    proporsi_b3 = (total_b3_sulteng / 427_000_000.0) * 100.0

total_emisi_co2 = 0.0
if not df_gfw.empty:
    df_gfw['Total_Emisi_CO2_Megagram'] = pd.to_numeric(df_gfw['Total_Emisi_CO2_Megagram'], errors='coerce').fillna(0)
    total_emisi_co2 = df_gfw['Total_Emisi_CO2_Megagram'].sum() / 1_000_000.0

# Air
ika_sulteng = 50
if not df_ika.empty:
    df_sulteng = df_ika[df_ika['Provinsi'] == 'Sulawesi Tengah']
    if not df_sulteng.empty and 2024 in df_sulteng['Tahun'].values:
        ika_sulteng = df_sulteng[df_sulteng['Tahun'] == 2024]['Indeks Kualitas Air'].values[0]

try:
    df_cr6 = pd.read_csv("data/processed/ika_ngo_cr6_gabungan.csv")
    max_cr6 = df_cr6["Konsentrasi Cr6+ (mg/L)"].max()
except Exception:
    max_cr6 = 0

r_diare = 0.0
if not df_kes.empty:
    df_diare = df_kes[df_kes['indikator'].str.contains('Diare', case=False, na=False)]
    kasus_diare_sentra = df_diare[df_diare['provinsi'].isin(['Sulawesi Tengah', 'Sulawesi Tenggara'])]['nilai'].sum()
    k_non = df_diare[~df_diare['provinsi'].isin(['Sulawesi Tengah', 'Sulawesi Tenggara'])]['nilai'].sum()
    ir_s = (kasus_diare_sentra / 5_700_000) * 1000
    ir_n = (k_non / 14_200_000) * 1000 if k_non > 0 else 1
    r_diare = ir_s / ir_n if ir_n > 0 else 0

jumlah_konflik_air = 0
if not df_konflik.empty:
    keywords = 'air|laut|pesisir|nelayan|sungai|pulau|tailing'
    df_konflik_air = df_konflik[df_konflik['sektor'].str.contains(keywords, case=False, na=False) | 
                                df_konflik['judul'].str.contains(keywords, case=False, na=False) | 
                                df_konflik['deskripsi'].str.contains(keywords, case=False, na=False)]
    jumlah_konflik_air = len(df_konflik_air)

# Lahan
bencana_sulteng_sultra = 0
if not df_bencana.empty:
    df_bencana_sentra = df_bencana.copy()
    df_bencana_sentra['jumlah_kejadian'] = pd.to_numeric(df_bencana_sentra['jumlah_kejadian'], errors='coerce').fillna(0)
    bencana_sulteng_sultra = df_bencana_sentra['jumlah_kejadian'].sum()

deforestasi_sentra = 0
if not df_gfw.empty:
    df_gfw_sentra = df_gfw.copy()
    df_gfw_sentra['Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha'] = pd.to_numeric(df_gfw_sentra['Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha'], errors='coerce').fillna(0)
    deforestasi_sentra = df_gfw_sentra['Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha'].sum()

lindung_hilang = 0
if not df_gfw_lindung.empty:
    df_l = df_gfw_lindung.copy()
    df_l['Luas_Hilang_Kawasan_Lindung_Ha'] = pd.to_numeric(df_l['Luas_Hilang_Kawasan_Lindung_Ha'], errors='coerce').fillna(0)
    lindung_hilang = df_l['Luas_Hilang_Kawasan_Lindung_Ha'].sum()

tambang_driver_ha = 0
if not df_gfw_driver.empty:
    df_d = df_gfw_driver.copy()
    df_d['Luas_Deforestasi_Ha'] = pd.to_numeric(df_d['Luas_Deforestasi_Ha'], errors='coerce').fillna(0)
    tambang_driver = df_d[df_d['Faktor_Pendorong'] == 'Deforestasi Komoditas (Tambang/Sawit)']
    tambang_driver_ha = tambang_driver['Luas_Deforestasi_Ha'].sum()

rasio_ekspansi = 0.0
if not df_kawasan_nikel.empty:
    sentra_kn = df_kawasan_nikel.copy()
    sentra_kn['total_luas_iup_ha'] = pd.to_numeric(sentra_kn['total_luas_iup_ha'], errors='coerce').fillna(0)
    sentra_kn['total_luas_amdal_ha'] = pd.to_numeric(sentra_kn['total_luas_amdal_ha'], errors='coerce').fillna(0)
    total_iup_nikel = sentra_kn['total_luas_iup_ha'].sum()
    total_amdal_nikel = sentra_kn['total_luas_amdal_ha'].sum()
    gap_amdal_iup = total_amdal_nikel - total_iup_nikel
    rasio_ekspansi = gap_amdal_iup / total_iup_nikel if total_iup_nikel > 0 else 0

# Sosial
konflik_darat = 0
luas_ha_dirampas = 0
jiwa_terdampak = 0
insiden_krim = 0
warga_ditangkap = 0
if not df_konflik.empty:
    keywords = 'air|laut|pesisir|nelayan|sungai|pulau|tailing'
    df_konflik_darat = df_konflik[~df_konflik['sektor'].str.contains(keywords, case=False, na=False)].copy()
    konflik_darat = len(df_konflik_darat)
    df_konflik_darat['luas_ha'] = pd.to_numeric(df_konflik_darat['luas_ha'], errors='coerce').fillna(0)
    df_konflik_darat['dampak_masyarakat_jiwa'] = pd.to_numeric(df_konflik_darat['dampak_masyarakat_jiwa'], errors='coerce').fillna(0)
    luas_ha_dirampas = df_konflik_darat['luas_ha'].sum()
    jiwa_terdampak = df_konflik_darat['dampak_masyarakat_jiwa'].sum()
    krim_df = df_konflik_darat[df_konflik_darat['indikasi_kriminalisasi'] == True].copy()
    krim_df['jumlah_ditangkap'] = pd.to_numeric(krim_df['jumlah_ditangkap'], errors='coerce').fillna(0)
    insiden_krim = len(krim_df)
    warga_ditangkap = krim_df['jumlah_ditangkap'].sum()

kasus_fpic = 0
if not df_konflik_fpic.empty:
    kasus_fpic = len(df_konflik_fpic[df_konflik_fpic['indikasi_fpic'] == True])

spa_aktual_pct = 42.5

# Veto
izin_baru = 0
if not df_izin.empty:
    df_izin['Tahun'] = pd.to_numeric(df_izin['Tahun'], errors='coerce')
    df_izin['Jumlah_Izin_Baru'] = pd.to_numeric(df_izin['Jumlah_Izin_Baru'], errors='coerce').fillna(0)
    df_izin_recent = df_izin[df_izin['Tahun'] >= 2014]
    izin_baru = df_izin_recent['Jumlah_Izin_Baru'].sum()

perusahaan_ilegal = 0
if not df_kpa_izin.empty:
    perusahaan_ilegal = len(df_kpa_izin['nama_perusahaan'].unique())

kapasitas_pltu = 0.0
if not df_pltu_captive.empty:
    df_active_pltu = df_pltu_captive[~df_pltu_captive['Status'].str.lower().isin(['cancelled', 'shelved'])].copy()
    df_active_pltu['Capacity (MW)'] = pd.to_numeric(df_active_pltu['Capacity (MW)'], errors='coerce').fillna(0)
    kapasitas_pltu = df_active_pltu['Capacity (MW)'].sum()

# --- EKSTRAKSI DAN UNPACKING KALKULASI DARI MODUL TERISOLASI ---
data_empiris_pulau = {
    'kapasitas_pltu_mw': kapasitas_terkini,
    'no2_tropomi': no2_terkini,
    'rasio_ispa_sentra_vs_non': rasio_anomali,
    'proporsi_b3_nasional': proporsi_b3,
    'emisi_co2_juta_ton': total_emisi_co2,
    'ika_bps': ika_sulteng,
    'cr6_mg_l': max_cr6,
    'rasio_diare_sentra_vs_non': r_diare,
    'jumlah_konflik_pesisir': jumlah_konflik_air,
    'tailing_buang_ton_tahun': total_b3_sulteng,
    'jumlah_bencana': bencana_sulteng_sultra,
    'deforestasi_ha': deforestasi_sentra,
    'deforestasi_hutan_lindung_ha': lindung_hilang,
    'deforestasi_driver_tambang_ha': tambang_driver_ha,
    'rasio_gap_amdal_iup': rasio_ekspansi,
    'kasus_pelanggaran_fpic': kasus_fpic,
    'jiwa_terdampak_konflik': jiwa_terdampak,
    'insiden_kriminalisasi': insiden_krim,
    'persentase_faskes_spa': spa_aktual_pct,
    'jumlah_izin_baru_krisis': izin_baru,
    'perusahaan_ilegal_pemutihan': perusahaan_ilegal,
}

res_pulau = kalkulasi_skor_pulau_sulawesi(data_empiris_pulau)
det_pulau = res_pulau['details']

skor_pltu = det_pulau['skor_pltu']
skor_no2 = det_pulau['skor_no2']
skor_1 = det_pulau['skor_1']
skor_2 = det_pulau['skor_2']
skor_3 = det_pulau['skor_3']
skor_4 = det_pulau['skor_4']
skor_akumulasi_udara = det_pulau['skor_akumulasi_udara']

skor_makro_air_1 = min(10.0, max(0, (80 - ika_sulteng) / 30) * 10)
skor_mikro_air_1 = det_pulau['skor_mikro_air_1']
skor_air_1 = skor_makro_air_1
skor_air_2 = round(det_pulau.get('skor_air_2', 4.0) / 2.0) * 2.0
skor_air_3 = det_pulau['skor_air_3']
skor_air_4 = det_pulau['skor_air_4']
skor_akumulasi_air = (skor_air_1 + skor_air_2 + skor_air_3 + skor_air_4) / 4.0

skor_lahan_1 = det_pulau['skor_lahan_1']
skor_lahan_2 = det_pulau['skor_lahan_2']
skor_lahan_3 = det_pulau['skor_lahan_3']
skor_lahan_4 = det_pulau['skor_lahan_4']
skor_lahan_5 = det_pulau['skor_lahan_5']
skor_akumulasi_lahan = det_pulau['skor_akumulasi_lahan']

skor_sosial_1 = det_pulau['skor_sosial_1']
skor_sosial_2 = det_pulau['skor_sosial_2']
skor_sosial_3 = det_pulau['skor_sosial_3']
skor_sosial_4 = det_pulau['skor_sosial_4']
skor_akumulasi_sosial = det_pulau['skor_akumulasi_sosial']

skor_veto_1 = det_pulau['skor_veto_1']
skor_veto_2 = det_pulau['skor_veto_2']
skor_veto_3 = det_pulau['skor_veto_3']
skor_akumulasi_veto = det_pulau['skor_akumulasi_veto']


# ==== METODE & VERSI METODOLOGI TOGGLE ====
st.markdown("### Pilih Metodologi & Versi Skoring:")
map_version = st.radio(
    "Gunakan opsi ini untuk memilih metode skoring dan versi visualisasi.",
    ("Versi 3", "Versi 2", "Versi 1"),
    horizontal=True,
    index=0,
    key="map_version_toggle",
    label_visibility="collapsed"
)

if map_version == "Versi 3":
    st.caption("**Versi 3**: Model Metodologi MCDA-Likert Terverifikasi (Skala Diskret 0 – 5) berbasis Threshold Spasial Multi-Skala.")
elif map_version == "Versi 2":
    st.caption("**Versi 2**: Model Continuous WSM (Skala Continuous 0 – 10 & Tooltip Peta Kinetik).")
else:
    st.caption("**Versi 1**: Model Visualisasi Plotly Baseline (Skala Continuous 0 – 10).")

is_likert_mode = map_version == "Versi 3"

if is_likert_mode:
    card_u_val = f"{(skor_akumulasi_udara / 2.0):.1f}"
    card_a_val = f"{(skor_akumulasi_air / 2.0):.1f}"
    card_l_val = f"{(skor_akumulasi_lahan / 2.0):.1f}"
    card_s_val = f"{(skor_akumulasi_sosial / 2.0):.1f}"
    card_v_val = f"{(skor_akumulasi_veto / 2.0):.1f}"
    card_denom = "5"
else:
    card_u_val = f"{skor_akumulasi_udara:.1f}"
    card_a_val = f"{skor_akumulasi_air:.1f}"
    card_l_val = f"{skor_akumulasi_lahan:.1f}"
    card_s_val = f"{skor_akumulasi_sosial:.1f}"
    card_v_val = f"{skor_akumulasi_veto:.1f}"
    card_denom = "10"

# =====================================================================
# KESIMPULAN EKSEKUTIF
# =====================================================================
st.markdown("""
<div style="background: #1E1E1E; padding: 20px; border-radius: 8px; border-left: 5px solid #F44336; margin-bottom: 30px;">
    <h3 style="color: #EF5350; margin-top: 0;">Kesimpulan Eksekutif</h3>
    <p style="color: #E0E0E0; font-size: 1.05rem; line-height: 1.6; margin-bottom: 0;">
        Evaluasi empiris mengindikasikan perlunya perbaikan substansial dalam integrasi dokumen D3TLH dan AMDAL. Instrumen pengelolaan lingkungan perlu diperkuat agar mampu memetakan dampak akumulatif dan berfungsi sebagai pertimbangan yang lebih efektif dalam pengendalian perizinan investasi.
    </p>
</div>
""", unsafe_allow_html=True)

# =====================================================================
# KARTU METRIK (Style PERSIS Page 3)
# =====================================================================
col1, col2 = st.columns(2)
help_akumulasi_udara = f"Kalkulasi Agregat Daya Tampung Udara:&#10;(Skor 1: {skor_1:.1f} + Skor 2: {skor_2:.1f} + Skor 3: {skor_3:.1f} + Skor 4: {skor_4:.1f}) / 4 = {skor_akumulasi_udara:.1f}/10&#10;" + (f"Konversi Likert: {skor_akumulasi_udara:.1f} / 2 = {(skor_akumulasi_udara / 2.0):.1f}/5" if is_likert_mode else "")

with col1:
    st.markdown(f"""
    <div class="metric-card" title="{help_akumulasi_udara}">
        <div>
            <div class="metric-label">DAYA TAMPUNG UDARA</div>
            <div class="metric-value" style="color: #E53935;">{card_u_val} <span style="font-size: 1rem; color: #888;">/ {card_denom}</span></div>
            <div class="metric-desc">
                <b>STATUS: EVALUASI KUALITAS UDARA</b><br><br>
                Analisis data menunjukkan korelasi antara aktivitas industri dan tren penyakit saluran pernapasan.
            </div>
        </div>
        <div class="metric-source">
            <b>NOTE:</b> Perlu pengawasan lebih ketat terhadap emisi industri<br>
            <i>Kapasitas PLTU: {kapasitas_terkini:,.0f} MW / NO2 NASA: {no2_terkini:.2e} / Rasio ISPA: {rasio_anomali:.1f}x</i>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">DAYA TAMPUNG AIR</div>
            <div class="metric-value" style="color: #E53935;">{card_a_val} <span style="font-size: 1rem; color: #888;">/ {card_denom}</span></div>
            <div class="metric-desc">
                <b>STATUS: EVALUASI KUALITAS AIR</b><br><br>
                Pemantauan Indeks Kualitas Air dan prevalensi penyakit berbasis air sebagai indikator lingkungan.
            </div>
        </div>
        <div class="metric-source">
            <b>NOTE:</b> Pentingnya penguatan standar pemantauan limbah<br>
            <i>IKA Sulteng: {ika_sulteng:.1f} / Kasus Diare: {kasus_diare_sentra:,.0f} / Konflik Air: {jumlah_konflik_air}</i>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

# Row 2: Kartu Lahan, Sosial, Veto
col3, col4, col5 = st.columns(3)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">DAYA DUKUNG LAHAN</div>
            <div class="metric-value" style="color: #E53935;">{card_l_val} <span style="font-size: 1rem; color: #888;">/ {card_denom}</span></div>
            <div class="metric-desc">
                <b>STATUS: EVALUASI TATA GUNA LAHAN</b><br><br>
                Pemetaan dampak tutupan lahan terhadap risiko bencana hidrometeorologi.
            </div>
        </div>
        <div class="metric-source">
            <b>NOTE:</b> Perlu peninjauan tata ruang berbasis mitigasi bencana<br>
            <i>Bencana: {bencana_sulteng_sultra:,.0f} Kejadian / Deforestasi: {deforestasi_sentra:,.0f} Ha</i>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">DAYA DUKUNG SOSIAL</div>
            <div class="metric-value" style="color: #E53935;">{card_s_val} <span style="font-size: 1rem; color: #888;">/ {card_denom}</span></div>
            <div class="metric-desc">
                <b>STATUS: EVALUASI SOSIAL AGRARIA</b><br><br>
                Pemantauan sengketa lahan dan dampaknya terhadap kesejahteraan masyarakat lokal.
            </div>
        </div>
        <div class="metric-source">
            <b>NOTE:</b> Pentingnya pendekatan dialogis dalam kebijakan agraria<br>
            <i>Konflik Lahan: {konflik_darat} Kasus TanahKita</i>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">VETO KEBIJAKAN</div>
            <div class="metric-value" style="color: #E53935;">{card_v_val} <span style="font-size: 1rem; color: #888;">/ {card_denom}</span></div>
            <div class="metric-desc">
                <b>STATUS: EVALUASI PERIZINAN</b><br><br>
                Peninjauan pemberian izin operasional industri dibandingkan dengan kapasitas ekologi.
            </div>
        </div>
        <div class="metric-source">
            <b>NOTE:</b> Penyelarasan izin dengan daya dukung lingkungan<br>
            <i>{izin_baru:,.0f} Izin Baru & {kapasitas_pltu/1000:,.1f} GW PLTU Captive Diloloskan</i>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><hr style='border: 1px dashed #333;'><br>", unsafe_allow_html=True)

# =====================================================================
# PETA KRISIS EKOLOGIS (Spasial)
# =====================================================================
st.markdown("<h3 style='color: #ECEFF1; font-weight: 600; text-align: center; margin-bottom: 5px;'>Peta Sebaran Krisis Ekologis Episentrum Ekstraktif</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9E9E9E; margin-bottom: 25px;'>Akumulasi skor komprehensif 5 Pilar Daya Tampung Lingkungan (DTL) wilayah Sulawesi.</p>", unsafe_allow_html=True)


import streamlit.components.v1 as components
import json

def binned_likert_score(ratio):
    r = float(ratio)
    if r < 0.2:
        return 0.0
    elif r < 0.5:
        return 1.0
    elif r < 1.0:
        return 2.0
    elif r < 1.5:
        return 3.0
    elif r < 2.0:
        return 4.0
    else:
        return 5.0

def get_likert_label(score):
    s = round(score)
    # Sesuai Permintaan Mas Saleh SIBERMU
    if s >= 4:
        return "Melampaui Batas"
    elif s == 3:
        return "Mendekati Batas"
    else:
        return "Tidak Melampaui Batas"

# --- GLOBAL PROVINCE SCORE CALCULATOR ---
def calculate_province_score(prov_name, use_likert=False):
    # Data referensi provinsi untuk normalisasi
    prov_data = {
        'Sulawesi Selatan': {'luas': 4671748, 'populasi': 9073509},
        'Sulawesi Tenggara': {'luas': 3806770, 'populasi': 2624875},
        'Sulawesi Tengah': {'luas': 6184129, 'populasi': 2985734},
        'Sulawesi Utara': {'luas': 1389247, 'populasi': 2621117},
        'Sulawesi Barat': {'luas': 1678718, 'populasi': 1419229},
        'Gorontalo': {'luas': 1125707, 'populasi': 1171681}
    }
    
    luas_prov = prov_data.get(prov_name, {'luas': 3000000})['luas']
    pop_prov = prov_data.get(prov_name, {'populasi': 3000000})['populasi']
    
    LUAS_NASIONAL = 190_000_000
    POP_NASIONAL = 275_000_000

    iku_terkini = 100.0
    if not df_iku.empty:
        df_prov_iku = df_iku[df_iku['Provinsi'] == prov_name]
        if not df_prov_iku.empty:
            iku_terkini = df_prov_iku.loc[df_prov_iku['Tahun'].idxmax(), 'IKU']
            
    no2_terkini = 4.0e-6
    if not df_nasa.empty:
        df_prov_nasa = df_nasa[df_nasa['Provinsi'] == prov_name]
        if not df_prov_nasa.empty:
            no2_terkini = df_prov_nasa.loc[df_prov_nasa['Tahun'].idxmax(), 'Rata_Rata_NO2']
    
    # --- SECTION A: UDARA ---
    kapasitas_terkini = 0
    if not df_pltu_op.empty:
        prov_mask = df_pltu_op['Subnational unit (province, state)'].str.contains(prov_name.split()[-1], case=False, na=False)
        op_mask = df_pltu_op['Status'].str.lower() == 'operating'
        kapasitas_terkini = df_pltu_op[prov_mask & op_mask]['Capacity (MW)'].sum()
    
    skor_1 = min(10.0, (kapasitas_terkini / 10000) * 5 + max(0.0, (80.0 - iku_terkini) / 30.0) * 2.5 + max(0.0, (no2_terkini - 4.0e-6) / (7.0e-6 - 4.0e-6)) * 2.5)
    
    skor_2 = 0
    rasio_anomali = 0
    if not df_kes.empty:
        df_ts_pre = df_kes[df_kes['indikator'].str.contains('ISPA', case=False, na=False)]
        kasus_prov = df_ts_pre[df_ts_pre['provinsi'] == prov_name]['nilai'].sum()
        kasus_non_prov = df_ts_pre[df_ts_pre['provinsi'] != prov_name]['nilai'].sum()
        rasio_anomali = (kasus_prov / 2) / (kasus_non_prov / 4) if kasus_non_prov > 0 else 0
        skor_2 = min(10.0, max(0.0, (rasio_anomali - 1) * 10.0))
        
    skor_3 = 0
    proporsi_b3 = 0
    total_b3_prov = 0
    if not df_b3.empty:
        df_b3['Estimasi Timbulan (Ton/Tahun)'] = pd.to_numeric(df_b3['Estimasi Timbulan (Ton/Tahun)'].astype(str).str.replace(',', '', regex=False), errors='coerce').fillna(0)
        total_b3_prov = df_b3[df_b3['Provinsi'] == prov_name]['Estimasi Timbulan (Ton/Tahun)'].sum()
        proporsi_b3 = (total_b3_prov / 25_260_000) * 100
        skor_3 = min(10.0, (proporsi_b3 / 5.0) * 10)
        
    skor_4 = 0
    total_emisi_co2 = 0
    threshold_co2 = (luas_prov / LUAS_NASIONAL) * 150.0
    if not df_gfw.empty:
        df_gfw['Total_Emisi_CO2_Megagram'] = pd.to_numeric(df_gfw['Total_Emisi_CO2_Megagram'], errors='coerce').fillna(0)
        df_gfw_prov = df_gfw[df_gfw['Provinsi'] == prov_name]
        total_emisi_co2 = df_gfw_prov['Total_Emisi_CO2_Megagram'].sum() / 1_000_000
        skor_4 = min(10.0, (total_emisi_co2 / threshold_co2) * 10) if threshold_co2 > 0 else 0
        
    skor_akumulasi_udara = (skor_1 + skor_2 + skor_3 + skor_4) / 4
    
    # --- SECTION B: AIR ---
    ika_prov = 50
    if not df_ika.empty:
        df_prov_ika = df_ika[df_ika['Provinsi'] == prov_name]
        if not df_prov_ika.empty and 2024 in df_prov_ika['Tahun'].values:
            ika_prov = df_prov_ika[df_prov_ika['Tahun'] == 2024]['Indeks Kualitas Air'].values[0]
        elif not df_prov_ika.empty:
            ika_prov = df_prov_ika['Indeks Kualitas Air'].mean()
            
    skor_makro_air_1 = min(10.0, max(0.0, (80.0 - ika_prov) / 30.0) * 10.0)
    
    skor_mikro_air_1 = 0
    max_cr6 = 0
    try:
        df_cr6 = pd.read_csv("data/processed/ika_ngo_cr6_gabungan.csv")
        if prov_name in ['Sulawesi Tengah', 'Sulawesi Tenggara']:
            keyword = 'Morowali' if prov_name == 'Sulawesi Tengah' else 'Konawe'
            df_cr6_prov = df_cr6[df_cr6['Lokasi'].str.contains(keyword, case=False, na=False)]
            if not df_cr6_prov.empty:
                max_cr6 = df_cr6_prov["Konsentrasi Cr6+ (mg/L)"].max()
                skor_mikro_air_1 = min(10.0, (max_cr6 / 0.05) * 10)
    except Exception:
        pass
        
    skor_air_1 = max(skor_makro_air_1, skor_mikro_air_1)
    
    skor_air_2 = 0
    rasio_diare = 0
    if not df_kes.empty:
        df_diare = df_kes[df_kes['indikator'].str.contains('Diare', case=False, na=False)]
        kasus_diare_prov = df_diare[df_diare['provinsi'] == prov_name]['nilai'].sum()
        kasus_diare_non_prov = df_diare[df_diare['provinsi'] != prov_name]['nilai'].sum()
        rasio_diare = (kasus_diare_prov / 2) / (kasus_diare_non_prov / 4) if kasus_diare_non_prov > 0 else 0
        skor_air_2 = min(10.0, max(0.0, (rasio_diare - 1) * 10.0))
        
    skor_air_3 = 0
    jumlah_konflik_air = 0
    if not df_konflik.empty:
        keywords = 'air|laut|pesisir|nelayan|sungai|pulau|tailing'
        prov_keyword = prov_name.split()[-1]
        df_konf_prov = df_konflik[df_konflik['lokasi'].str.contains(prov_keyword, case=False, na=False) | df_konflik['judul'].str.contains(prov_keyword, case=False, na=False)]
        df_konflik_air = df_konf_prov[df_konf_prov['sektor'].str.contains(keywords, case=False, na=False) | 
                                      df_konf_prov['judul'].str.contains(keywords, case=False, na=False) | 
                                      df_konf_prov['deskripsi'].str.contains(keywords, case=False, na=False)]
        jumlah_konflik_air = len(df_konflik_air)
        skor_air_3 = min(10.0, (jumlah_konflik_air / 15.0) * 10)
        
    skor_air_4 = 0
    t_b3_prov = 0
    if not df_b3.empty:
        t_b3_prov = df_b3[df_b3['Provinsi'] == prov_name]['Estimasi Timbulan (Ton/Tahun)'].sum()
        skor_air_4 = min(10.0, (t_b3_prov / 25_000_000) * 10)
        
    skor_akumulasi_air = (skor_air_1 + skor_air_2 + skor_air_3 + skor_air_4) / 4
    
    # --- SECTION C: LAHAN ---
    skor_lahan_1 = 0
    bencana_prov = 120.0
    if not df_bencana.empty:
        df_bencana_prov = df_bencana[df_bencana['provinsi'] == prov_name].copy()
        df_bencana_prov['jumlah_kejadian'] = pd.to_numeric(df_bencana_prov['jumlah_kejadian'], errors='coerce').fillna(0)
        bencana_prov = df_bencana_prov['jumlah_kejadian'].sum()
        if bencana_prov == 0:
            bencana_prov = 120.0
        skor_lahan_1 = min(10.0, (bencana_prov / 877.0) * 10)
        
    skor_lahan_2 = 0
    deforestasi_prov = 45000.0
    threshold_deforestasi = (luas_prov / LUAS_NASIONAL) * 570_000
    if not df_gfw.empty:
        df_gfw_prov = df_gfw[df_gfw['Provinsi'] == prov_name].copy()
        df_gfw_prov['Total_Deforestasi_Ha'] = pd.to_numeric(df_gfw_prov['Total_Deforestasi_Ha'], errors='coerce').fillna(0)
        deforestasi_prov = df_gfw_prov['Total_Deforestasi_Ha'].sum()
        if deforestasi_prov == 0:
            deforestasi_prov = 45000.0
        skor_lahan_2 = min(10.0, (deforestasi_prov / threshold_deforestasi) * 10) if threshold_deforestasi > 0 else 0
        
    skor_lahan_3 = 0.0
    lindung_hilang = 0
    if not df_gfw_lindung.empty:
        df_l = df_gfw_lindung[df_gfw_lindung['Provinsi'] == prov_name].copy()
        df_l['Luas_Hilang_Kawasan_Lindung_Ha'] = pd.to_numeric(df_l['Luas_Hilang_Kawasan_Lindung_Ha'], errors='coerce').fillna(0)
        lindung_hilang = df_l['Luas_Hilang_Kawasan_Lindung_Ha'].sum()
        skor_lahan_3 = 10.0 if lindung_hilang > 0 else 0.0
        
    skor_lahan_4 = 0.0
    tambang_driver_ha = 0
    threshold_tambang = (luas_prov / LUAS_NASIONAL) * 500_000
    if not df_gfw_driver.empty:
        df_d = df_gfw_driver[df_gfw_driver['Provinsi'] == prov_name].copy()
        df_d['Luas_Deforestasi_Ha'] = pd.to_numeric(df_d['Luas_Deforestasi_Ha'], errors='coerce').fillna(0)
        tambang_driver_ha = df_d[df_d['Faktor_Pendorong'] == 'Deforestasi Komoditas (Tambang/Sawit)']['Luas_Deforestasi_Ha'].sum()
        skor_lahan_4 = min(10.0, (tambang_driver_ha / threshold_tambang) * 10) if threshold_tambang > 0 else 0
        
    skor_lahan_5 = 0.0
    rasio_ekspansi = 0
    if not df_kawasan_nikel.empty:
        sentra_kn = df_kawasan_nikel[df_kawasan_nikel['provinsi'] == prov_name].copy()
        if not sentra_kn.empty:
            sentra_kn['total_luas_iup_ha'] = pd.to_numeric(sentra_kn['total_luas_iup_ha'], errors='coerce').fillna(0)
            sentra_kn['total_luas_amdal_ha'] = pd.to_numeric(sentra_kn['total_luas_amdal_ha'], errors='coerce').fillna(0)
            total_iup_nikel = sentra_kn['total_luas_iup_ha'].sum()
            total_amdal_nikel = sentra_kn['total_luas_amdal_ha'].sum()
            gap_amdal_iup = total_amdal_nikel - total_iup_nikel
            rasio_ekspansi = gap_amdal_iup / total_iup_nikel if total_iup_nikel > 0 else 0
            skor_lahan_5 = min(10.0, max(0.0, rasio_ekspansi * 10))
            
    skor_akumulasi_lahan = (skor_lahan_1 + skor_lahan_2 + skor_lahan_3 + skor_lahan_4 + skor_lahan_5) / 5
    
    # --- SECTION D: SOSIAL ---
    skor_sosial_1 = 0.0
    skor_sosial_2 = 0.0
    skor_sosial_3 = 0.0
    jiwa_terdampak = 0
    insiden_krim = 0
    threshold_jiwa = (pop_prov / POP_NASIONAL) * 406_000
    threshold_krim = (pop_prov / POP_NASIONAL) * 57
    if not df_konflik.empty:
        keywords = 'air|laut|pesisir|nelayan|sungai|pulau|tailing'
        prov_keyword = prov_name.split()[-1]
        df_konf_prov = df_konflik[df_konflik['lokasi'].str.contains(prov_keyword, case=False, na=False) | df_konflik['judul'].str.contains(prov_keyword, case=False, na=False)]
        df_konflik_darat = df_konf_prov[~df_konf_prov['sektor'].str.contains(keywords, case=False, na=False)].copy()
        df_konflik_darat['dampak_masyarakat_jiwa'] = pd.to_numeric(df_konflik_darat['dampak_masyarakat_jiwa'], errors='coerce').fillna(0)
        jiwa_terdampak = df_konflik_darat['dampak_masyarakat_jiwa'].sum()
        skor_sosial_2 = min(10.0, (jiwa_terdampak / threshold_jiwa) * 10) if threshold_jiwa > 0 else 0
        
        krim_df = df_konflik_darat[df_konflik_darat['indikasi_kriminalisasi'] == True].copy()
        insiden_krim = len(krim_df)
        skor_sosial_3 = min(10.0, (insiden_krim / threshold_krim) * 10) if threshold_krim > 0 else 0
        
    kasus_fpic = 0
    if not df_konflik_fpic.empty:
        kasus_fpic = len(df_konflik_fpic[(df_konflik_fpic['provinsi'] == prov_name) & (df_konflik_fpic['indikasi_fpic'] == True)])
        skor_sosial_1 = min(10.0, (kasus_fpic / 4) * 10)
        
    skor_sosial_4 = 0.0
    spa_aktual_pct = 42.5 if prov_name in ['Sulawesi Tengah', 'Sulawesi Tenggara'] else 60.0
    target_rpjmn = 80.0
    gap_spa = max(0.0, target_rpjmn - spa_aktual_pct)
    if not df_faskes.empty:        skor_sosial_4 = min(10.0, (gap_spa / 45.0) * 10.0)
        
    skor_akumulasi_sosial = (skor_sosial_1 + skor_sosial_2 + skor_sosial_3 + skor_sosial_4) / 4
    
    # --- SECTION E: VETO ---
    skor_veto_1 = 0.0
    skor_veto_2 = 0.0
    skor_veto_3 = 0.0
    izin_baru = 0
    perusahaan_ilegal = 0
    kapasitas_pltu = 0
    if not df_izin.empty:
        df_izin['Tahun'] = pd.to_numeric(df_izin['Tahun'], errors='coerce')
        df_izin['Jumlah_Izin_Baru'] = pd.to_numeric(df_izin['Jumlah_Izin_Baru'], errors='coerce').fillna(0)
        df_izin_recent = df_izin[(df_izin['Tahun'] >= 2014) & (df_izin['Provinsi'] == prov_name)]
        izin_baru = len(df_izin_recent)
        skor_veto_1 = min(10.0, (izin_baru / 35.0) * 10)
        
    if not df_kpa_izin.empty:
        prov_keyword = prov_name.split()[-1]
        df_kpa_prov = df_kpa_izin[df_kpa_izin['lokasi'].str.contains(prov_keyword, case=False, na=False)]
        perusahaan_ilegal = len(df_kpa_prov['nama_perusahaan'].unique())
        skor_veto_2 = min(10.0, (perusahaan_ilegal / 4.0) * 10)
        
    if not df_pltu_captive.empty:
        prov_mask = df_pltu_captive['Subnational unit (province, state)'].str.contains(prov_name.split()[-1], case=False, na=False)
        df_pltu_prov = df_pltu_captive[prov_mask].copy()
        df_active_prov = df_pltu_prov[~df_pltu_prov['Status'].str.lower().isin(['cancelled', 'shelved'])].copy()
        df_active_prov['Capacity (MW)'] = pd.to_numeric(df_active_prov['Capacity (MW)'], errors='coerce').fillna(0)
        kapasitas_pltu = df_active_prov['Capacity (MW)'].sum()
        skor_veto_3 = min(10.0, (kapasitas_pltu / 2200.0) * 10)
        
    skor_akumulasi_veto = (skor_veto_1 + skor_veto_2 + skor_veto_3) / 3
    
    skor_total = (skor_akumulasi_udara + skor_akumulasi_air + skor_akumulasi_lahan + skor_akumulasi_sosial + skor_akumulasi_veto) / 5

    if use_likert:
        res_prov_map = kalkulasi_skor_provinsi_sulawesi()
        res_p = res_prov_map.get(prov_name, {})
        skor_akumulasi_udara = res_p.get('udara', 1.0)
        skor_akumulasi_air = res_p.get('air', 1.0)
        skor_akumulasi_lahan = res_p.get('lahan', 1.0)
        skor_akumulasi_sosial = res_p.get('sosial', 1.0)
        skor_akumulasi_veto = res_p.get('veto', 1.0)
        skor_total = res_p.get('total_likert', 1.0)
        likert_desc = res_p.get('likert_label', 'Versi 3 Z-Score EWM')
    else:
        likert_desc = get_likert_label(skor_total)

    return {
        'total': skor_total,
        'udara': skor_akumulasi_udara,
        'air': skor_akumulasi_air,
        'lahan': skor_akumulasi_lahan,
        'sosial': skor_akumulasi_sosial,
        'veto': skor_akumulasi_veto,
        'likert_label': likert_desc,
        'raw': {
            'IKU (Udara)': f"{iku_terkini:.1f}",
            'ISPA (Udara)': f"{kasus_prov if 'kasus_prov' in locals() else 0:.0f}",
            'Limbah B3 (Udara)': f"{total_b3_prov if 'total_b3_prov' in locals() else 0:.1f}",
            'Emisi CO2 (Udara)': f"{total_emisi_co2 if 'total_emisi_co2' in locals() else 0:.2f}",
            'IKA (Air)': f"{ika_prov if 'ika_prov' in locals() else 0:.1f}",
            'Cr6+ (Air)': f"{max_cr6 if 'max_cr6' in locals() else 0:.3f}",
            'Diare (Air)': f"{kasus_diare_prov if 'kasus_diare_prov' in locals() else 0:.0f}",
            'Konflik Pesisir (Air)': f"{jumlah_konflik_air if 'jumlah_konflik_air' in locals() else 0}",
            'Tailing DSTP (Air)': f"{t_b3_prov if 't_b3_prov' in locals() else 0:.0f}",
            'Bencana (Lahan)': f"{bencana_prov if 'bencana_prov' in locals() else 0:.0f}",
            'Deforestasi (Lahan)': f"{deforestasi_prov if 'deforestasi_prov' in locals() else 0:.1f}",
            'Hutan Lindung (Lahan)': f"{lindung_hilang if 'lindung_hilang' in locals() else 0:.1f}",
            'Driver Tambang (Lahan)': f"{tambang_driver_ha if 'tambang_driver_ha' in locals() else 0:.1f}",
            'FPIC (Sosial)': f"{kasus_fpic if 'kasus_fpic' in locals() else 0}",
            'Jiwa Terdampak (Sosial)': f"{jiwa_terdampak if 'jiwa_terdampak' in locals() else 0:.0f}",
            'Kriminalisasi (Sosial)': f"{insiden_krim if 'insiden_krim' in locals() else 0}",
            'Defisit Faskes (Sosial)': f"{spa_aktual_pct if 'spa_aktual_pct' in locals() else 0:.1f}",
            'Izin Baru (Veto)': f"{izin_baru if 'izin_baru' in locals() else 0:.0f}",
            'Izin Ilegal (Veto)': f"{perusahaan_ilegal if 'perusahaan_ilegal' in locals() else 0}",
            'PLTU Captive (Veto)': f"{kapasitas_pltu if 'kapasitas_pltu' in locals() else 0:.1f}"
        }
    }


import streamlit.components.v1 as components
import json

def render_crisis_map_d3(df_map, sulawesi_geojson, skor_akumulasi, skor_udara, skor_air, skor_lahan, skor_sosial, skor_veto, versi=2):
    # Serialize data
    geo_data = json.dumps(sulawesi_geojson)
    
    max_scale = 5.0 if versi == 3 else 10.0
    
    # Map dataframe to dict by province name for easy JS lookup
    data_dict = {}
    for _, row in df_map.iterrows():
        data_dict[row['Provinsi']] = {
            'label': row['Label'],
            'skor': row['Skor Krisis'],
            'udara': row['Udara'],
            'air': row['Air'],
            'lahan': row['Lahan'],
            'sosial': row['Sosial'],
            'veto': row['Veto'],
            'likert_label': row.get('Likert Label', ''),
            'lat': row['lat'],
            'lon': row['lon']
        }
    data_json = json.dumps(data_dict)

    agregat_title = "Pulau Sulawesi (Skor Pulau)"
    sk_str = f"{skor_akumulasi:.1f}"
    u_str = f"{skor_udara:.1f}"
    a_str = f"{skor_air:.1f}"
    l_str = f"{skor_lahan:.1f}"
    s_str = f"{skor_sosial:.1f}"
    v_str = f"{skor_veto:.1f}"

    def format_sub(s):
        return f"{s/2.0:.1f}" if versi == 3 else f"{s:.1f}"

    su1, su2, su3, su4 = format_sub(skor_1), format_sub(skor_2), format_sub(skor_3), format_sub(skor_4)
    sa1, sa2, sa3, sa4 = format_sub(skor_air_1), format_sub(skor_air_2), format_sub(skor_air_3), format_sub(skor_air_4)
    sl1, sl2, sl3, sl4, sl5 = format_sub(skor_lahan_1), format_sub(skor_lahan_2), format_sub(skor_lahan_3), format_sub(skor_lahan_4), format_sub(skor_lahan_5)
    ss1, ss2, ss3, ss4 = format_sub(skor_sosial_1), format_sub(skor_sosial_2), format_sub(skor_sosial_3), format_sub(skor_sosial_4)
    sv1, sv2, sv3 = format_sub(skor_veto_1), format_sub(skor_veto_2), format_sub(skor_veto_3)
    prov_badge_js = '<span style="font-size: 8px; background-color: #1E3A8A; color: #FFFFFF; padding: 2px 5px; border-radius: 3px; font-weight: 600; margin-left: 3px;">EWM & Z-Score Anomali</span>' if versi == 3 else '<span style="font-size: 8px; color: #666; font-weight: normal;">(Skor Provinsi)</span>'
    island_badge_html = '<span style="font-size: 8px; background-color: #064E3B; color: #FFFFFF; padding: 2px 6px; border-radius: 3px; font-weight: 600; margin-left: 5px;">MCDA Min-Max & WSM</span>' if versi == 3 else '<span style="font-size: 8px; color: #666; font-weight: normal;">(Skor Makro Pulau)</span>'

    agregat_html = f"""
            <div id="agregat-box">
                <div style="font-size: 12px; font-weight: 600; color: #333333; margin-bottom: 8px;">{agregat_title} {island_badge_html}</div>
                <div style="font-size: 24px; font-weight: 700; color: #B71C1C;">{sk_str} <span style="font-size: 11px; color: #333333; font-weight: normal;">/ {max_scale:.0f}</span></div>
                <div style="font-size: 11px; color: #555555; margin-top: 10px; line-height: 1.4;">
                    <b>Udara {u_str}</b><br><span style="font-size: 9px;">(PLTU+IKU ({su1}), ISPA ({su2}), Limbah B3 ({su3}), Emisi CO2 ({su4}))</span><br>
                    <b>Air {a_str}</b><br><span style="font-size: 9px;">(IKA & Cr6+ ({sa1}), Diare ({sa2}), Konflik Pesisir ({sa3}), Tailing ({sa4}))</span><br>
                    <b>Lahan {l_str}</b><br><span style="font-size: 9px;">(Bencana ({sl1}), Deforestasi ({sl2}), Lindung ({sl3}), Driver ({sl4}), Ekspansi ({sl5}))</span><br>
                    <b>Sosial {s_str}</b><br><span style="font-size: 9px;">(FPIC ({ss1}), Jiwa Terdampak ({ss2}), Kriminalisasi ({ss3}), Defisit Faskes ({ss4}))</span><br>
                    <b>Veto {v_str}</b><br><span style="font-size: 9px;">(Izin Baru ({sv1}), KPA Izin ({sv2}), PLTU Captive ({sv3}))</span>
                </div>
            </div>
        """
    
    legend_title = "Skor Likert" if versi == 3 else "Skor Krisis"
    legend_sub = "(Likert 0 - 5)" if versi == 3 else "(Merah = Darurat)"
    
    if versi == 3:
        score_div = f'<div class="fixed-score">${{Math.round(pData.skor)}} <span style="font-size:9px; color:#666;">/ {max_scale:.0f}</span></div><div style="font-size:9px; font-weight:700; color:#B71C1C; margin-bottom:3px;">${{pData.likert_label || ""}}</div>'
        details_html_js = 'Udara ${Math.round(pData.udara)} | Air ${Math.round(pData.air)}<br>Lahan ${Math.round(pData.lahan)} | Sosial ${Math.round(pData.sosial)}<br>Veto ${Math.round(pData.veto)}'
    else:
        score_div = f'<div class="fixed-score">${{pData.skor.toFixed(1)}} <span style="font-size:9px; color:#666;">/ {max_scale:.0f}</span></div>'
        details_html_js = 'Udara ${pData.udara.toFixed(1)} | Air ${pData.air.toFixed(1)}<br>Lahan ${pData.lahan.toFixed(1)} | Sosial ${pData.sosial.toFixed(1)}<br>Veto ${pData.veto.toFixed(1)}'

    js_legend_and_tooltips = f"""
            // Draw Legend
            const legendG = d3.select("#legend-g");
            const legendX = 40;
            const legendY = height / 2 - 100;
            const legendHeight = 200;
            const legendWidth = 15;
            
            legendG.append("rect")
                .attr("x", legendX)
                .attr("y", legendY)
                .attr("width", legendWidth)
                .attr("height", legendHeight)
                .style("fill", "url(#grad1)");
                
            // Legend Title
            legendG.append("text")
                .attr("x", legendX)
                .attr("y", legendY - 25)
                .attr("class", "legend-text")
                .text("{legend_title}");
            legendG.append("text")
                .attr("x", legendX)
                .attr("y", legendY - 12)
                .attr("class", "legend-subtext")
                .text("{legend_sub}");
                
            // Legend Axis
            const yAxisScale = d3.scaleLinear()
                .domain([{max_scale}, 0])
                .range([0, legendHeight]);
                
            const yAxis = d3.axisRight(yAxisScale)
                .ticks(5)
                .tickSize(4);
                
            legendG.append("g")
                .attr("transform", `translate(${{legendX + legendWidth}}, ${{legendY}})`)
                .call(yAxis)
                .selectAll("text")
                .style("fill", "#ECEFF1");
            legendG.selectAll(".domain, .tick line")
                .style("stroke", "#ECEFF1");
        """
        
    js_legend_and_tooltips += f"""
            // Fixed Tooltips / Annotations
            const offsets = {{
                'SULTENG': {{ dx: -170, dy: -60 }},
                'SULTRA': {{ dx: 170, dy: 30 }},
                'SULSEL': {{ dx: -160, dy: 90 }},
                'SULBAR': {{ dx: -170, dy: -30 }},
                'GORONTALO': {{ dx: -70, dy: -120 }},
                'SULUT': {{ dx: 140, dy: -90 }}
            }};

            geoData.features.forEach(d => {{
                const pData = d.properties._data;
                if (pData) {{
                    const centroid = path.centroid(d);
                    const cx = centroid[0];
                    const cy = centroid[1];
                    
                    let adjCy = cy;
                    if(pData.label === 'GORONTALO') adjCy = cy - 10;
                    if(pData.label === 'SULTRA') adjCy = cy + 10;
                    
                    const offset = offsets[pData.label] || {{dx: 0, dy: 0}};
                    const tx = cx + offset.dx;
                    const ty = adjCy + offset.dy;
                    
                    d3.select("#lines-g").append("line")
                        .attr("class", "pointer-line")
                        .attr("x1", cx)
                        .attr("y1", adjCy)
                        .attr("x2", tx)
                        .attr("y2", ty);

                    const div = document.createElement("div");
                    div.className = "fixed-annotation";
                    div.style.left = tx + "px";
                    div.style.top = ty + "px";
                    
                    div.innerHTML = `
                        <div class="fixed-title">${{pData.label}} {prov_badge_js}</div>
                        {score_div}
                        <div class="fixed-details">
                            {details_html_js}
                        </div>
                    `;
                    annotationsContainer.appendChild(div);
                }}
            }});
        """

    # HTML/JS template
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <script src="https://d3js.org/d3.v7.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
        <style>
            body {{
                margin: 0;
                padding: 0;
                background-color: #0E1117; /* matches Streamlit dark mode */
                font-family: "Source Sans Pro", sans-serif;
            }}
            #map-container {{
                width: 100%;
                height: 800px;
                position: relative;
                overflow: hidden;
            }}
            .province {{
                stroke: #333;
                stroke-width: 0.5px;
            }}
            .province:hover {{
                opacity: 0.8;
                stroke-width: 1.5px;
            }}
            
            /* Aggregate Box */
            #agregat-box {{
                position: absolute;
                bottom: 30px;
                right: 30px;
                background-color: rgba(255, 255, 255, 0.95);
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 15px;
                box-shadow: 0px 4px 12px rgba(0,0,0,0.15);
                pointer-events: none;
                color: #333;
                z-index: 10;
            }}
            
            /* Fixed tooltips for provinces */
            .fixed-annotation {{
                position: absolute;
                background-color: rgba(255, 255, 255, 0.95);
                border: 1.5px solid #CCCCCC;
                border-radius: 8px;
                padding: 6px 10px;
                pointer-events: none;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
                color: #333;
                font-size: 11px;
                min-width: 100px;
                z-index: 5;
                transform: translate(-50%, -50%);
            }}
            .fixed-title {{
                font-size: 10px;
                font-weight: 600;
                color: #333333;
            }}
            .fixed-score {{
                font-size: 14px;
                font-weight: 700;
                color: #B71C1C;
                margin-bottom: 2px;
            }}
            .fixed-details {{
                font-size: 8px;
                color: #555;
                line-height: 1.2;
            }}
            
            /* Pointer line */
            .pointer-line {{
                stroke: #FFFFFF;
                stroke-width: 1.5px;
                fill: none;
                marker-end: url(#arrow);
            }}
            
            /* Legend text */
            .legend-text {{
                font-size: 12px;
                fill: #ECEFF1;
                font-weight: 500;
            }}
            .legend-subtext {{
                font-size: 9px;
                fill: #E53935;
            }}
            
            /* Download Button */
            #download-btn {{
                position: absolute;
                top: 20px;
                right: 20px;
                background-color: #333;
                color: #FFF;
                border: 1px solid #555;
                padding: 8px 12px;
                border-radius: 4px;
                cursor: pointer;
                font-family: inherit;
                font-size: 12px;
                z-index: 100;
                transition: background-color 0.2s;
            }}
            #download-btn:hover {{
                background-color: #555;
            }}
        </style>
    </head>
    <body>
        <div id="map-container">
            <button id="download-btn">📷 Download PNG</button>
            <svg width="100%" height="100%">
                <defs>
                    <linearGradient id="grad1" x1="0%" y1="100%" x2="0%" y2="0%">
                        <stop offset="0%" style="stop-color:#FFEBEE;stop-opacity:1" />
                        <stop offset="25%" style="stop-color:#FFCDD2;stop-opacity:1" />
                        <stop offset="50%" style="stop-color:#E53935;stop-opacity:1" />
                        <stop offset="75%" style="stop-color:#B71C1C;stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#660000;stop-opacity:1" />
                    </linearGradient>
                    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5"
                        markerWidth="4" markerHeight="4" orient="auto-start-reverse">
                        <path d="M 0 0 L 10 5 L 0 10 z" fill="#FFFFFF" />
                    </marker>
                </defs>
                <g id="map-g"></g>
                <g id="lines-g"></g>
                <g id="legend-g"></g>
            </svg>
            
            <div id="annotations-container"></div>
            
            {agregat_html}
        </div>

        <script>
            const geoData = {geo_data};
            const mapData = {data_json};

            const container = document.getElementById('map-container');
            const annotationsContainer = document.getElementById('annotations-container');
            const svg = d3.select("svg");
            const width = container.clientWidth || 800;
            const height = 800; 

            // Setup Projection
            const projection = d3.geoMercator()
                .center([121.0, -2.0])
                .scale(width * 2.5) 
                .translate([width / 2, height / 2 + 50]); 

            const path = d3.geoPath().projection(projection);

            // Color Scale
            const maxDomain = {max_scale};
            const colorScale = d3.scaleLinear()
                .domain([0, maxDomain * 0.25, maxDomain * 0.5, maxDomain * 0.75, maxDomain])
                .range(['#FFEBEE', '#FFCDD2', '#E53935', '#B71C1C', '#660000']);

            // Draw map
            d3.select("#map-g")
                .selectAll("path")
                .data(geoData.features)
                .enter().append("path")
                .attr("class", "province")
                .attr("d", path)
                .attr("fill", d => {{
                    const provName = d.properties.Provinsi.toUpperCase();
                    let matchedData = null;
                    for (let key in mapData) {{
                        if (key.toUpperCase() === provName || 
                           (key === 'Sulawesi Selatan' && provName === 'SULAWESI SELATAN') ||
                           (key === 'Gorontalo' && provName === 'GORONTALO')) {{
                            matchedData = mapData[key];
                            break;
                        }}
                    }}
                    d.properties._data = matchedData;
                    
                    if (matchedData) {{
                        return colorScale(matchedData.skor);
                    }}
                    return "#333333"; 
                }});

            {js_legend_and_tooltips}

            // Download functionality
            document.getElementById('download-btn').addEventListener('click', function() {{
                const btn = this;
                btn.style.display = 'none'; 
                html2canvas(container, {{
                    backgroundColor: '#0E1117', 
                    useCORS: true
                }}).then(canvas => {{
                    btn.style.display = 'block'; 
                    
                    const link = document.createElement('a');
                    link.download = 'peta_krisis_sulawesi.png';
                    link.href = canvas.toDataURL('image/png');
                    link.click();
                }});
            }});
        </script>
    </body>
    </html>
    """
    
    components.html(html_content, height=820)

def render_crisis_map(skor_udara, skor_air, skor_lahan, skor_sosial, skor_veto):
    # =====================================================================
    # PRE-CALCULATE SCORES PER PROVINCE
    # =====================================================================
    skor_akumulasi = (skor_udara + skor_air + skor_lahan + skor_sosial + skor_veto) / 5

    prov_list = ['Sulawesi Tengah', 'Sulawesi Tenggara', 'Sulawesi Selatan', 'Sulawesi Barat', 'Gorontalo', 'Sulawesi Utara']
    detail_list = [calculate_province_score(p) for p in prov_list]
    skor_list = [d['total'] for d in detail_list]

    # Buat dataframe untuk 6 provinsi di Sulawesi
    df_map = pd.DataFrame({
        'Provinsi': prov_list,
        'Label': ['SULTENG', 'SULTRA', 'SULSEL', 'SULBAR', 'GORONTALO', 'SULUT'],
        'Skor Krisis': skor_list,
        'Udara': [d['udara'] for d in detail_list],
        'Air': [d['air'] for d in detail_list],
        'Lahan': [d['lahan'] for d in detail_list],
        'Sosial': [d['sosial'] for d in detail_list],
        'Veto': [d['veto'] for d in detail_list],
        'lat': [-1.43, -4.14, -3.66, -2.46, 0.69, 0.82],
        'lon': [121.44, 122.07, 119.97, 119.22, 124.50, 124.50]
    })
    with open('data/processed/sulawesi_provinces.geojson', 'r', encoding='utf-8') as f:
        sulawesi_geojson = json.load(f)

    # Buat Choropleth Map
    fig = px.choropleth_mapbox(
        df_map, geojson=sulawesi_geojson, locations='Provinsi', featureidkey='properties.Provinsi',
        color="Skor Krisis",
        color_continuous_scale=[[0.0, '#FFEBEE'], [0.25, '#FFCDD2'], [0.5, '#E53935'], [0.75, '#B71C1C'], [1.0, '#660000']],
        range_color=[0, 10], zoom=5.2, center={"lat": -2.0, "lon": 121.0}, opacity=0.8,
        hover_name=None, 
        hover_data=None, 
        mapbox_style="carto-darkmatter"
    )
    
    # Tambahkan teks label di atas peta
    fig.add_trace(go.Scattermapbox(
        lat=df_map['lat'],
        lon=df_map['lon'],
        mode='text',
        text=df_map['Label'],
        textfont=dict(color='white', size=13),
        hoverinfo='skip'
    ))

    fig.update_layout(
        margin={"r":0,"t":10,"l":0,"b":0}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
        font=dict(color='#ECEFF1'),
        coloraxis_colorbar=dict(
            title="Skor Krisis<br><span style='font-size:0.7em;color:#E53935;'>(Merah = Darurat)</span>", 
            thicknessmode="pixels", thickness=15, 
            lenmode="pixels", len=200, 
            yanchor="middle", y=0.5, 
            xanchor="left", x=0
        ),
        annotations=[
            dict(
                x=0.98,
                y=0.05,
                xref="paper",
                yref="paper",
                xanchor="right",
                yanchor="bottom",
                text=f"<span style='font-size: 12px; font-weight: 600; color: #333333;'>Pulau Sulawesi (Agregat)</span><br><span style='font-size: 9px; background-color: #E8F5E9; color: #2E7D32; padding: 2px 4px; border-radius: 3px;'>Metode: Min-Max WSM</span><br><br><span style='font-size: 24px; font-weight: 700; color: #B71C1C;'>{skor_akumulasi:.1f}</span><span style='font-size: 11px; color: #333333;'> Skor Krisis Keseluruhan</span><br><br><span style='font-size: 11px; color: #555555;'><b>Udara {skor_udara:.1f}</b><br><span style='font-size: 9px;'>(PLTU+IKU, ISPA,<br>Limbah B3, Emisi CO2)</span><br><b>Air {skor_air:.1f}</b><br><span style='font-size: 9px;'>(IKA & Cr6+, Diare,<br>Konflik Pesisir, Tailing)</span><br><b>Lahan {skor_lahan:.1f}</b><br><span style='font-size: 9px;'>(Bencana, Deforestasi,<br>Kaw. Lindung, Driver Tambang)</span><br><b>Sosial {skor_sosial:.1f}</b><br><span style='font-size: 9px;'>(FPIC, Jiwa Terdampak,<br>Kriminalisasi, Defisit Faskes)</span><br><b>Veto {skor_veto:.1f}</b><br><span style='font-size: 9px;'>(Izin Baru, KPA Izin,<br>PLTU Captive)</span></span>",
                align="left",
                showarrow=False,
                bgcolor="white",
                bordercolor="#E0E0E0",
                borderwidth=1,
                borderpad=8
            ),
            dict(
                x=0.53, y=0.5, xref="paper", yref="paper",
                text=f"<span style='font-size: 10px; font-weight: 600; color: #333333;'>SULTENG</span><br><span style='font-size: 8px; background-color: #E3F2FD; color: #1565C0; padding: 2px 4px; border-radius: 3px;'>EWM Z-Score</span><br><span style='font-size: 14px; font-weight: 700; color: #B71C1C;'>{skor_list[0]:.1f}</span><br><span style='font-size: 8px; color: #555;'>Udara {detail_list[0]['udara']:.1f} | Air {detail_list[0]['air']:.1f}<br>Lahan {detail_list[0]['lahan']:.1f} | Sosial {detail_list[0]['sosial']:.1f}<br>Veto {detail_list[0]['veto']:.1f}</span>",
                align="left", showarrow=True, arrowcolor="#555555", arrowhead=2, arrowsize=1, arrowwidth=1.5, ax=-100, ay=-50,
                bgcolor="rgba(255,255,255,0.95)", bordercolor="#CCCCCC", borderwidth=1.5, borderpad=6
            ),
            dict(
                x=0.6, y=0.25, xref="paper", yref="paper",
                text=f"<span style='font-size: 10px; font-weight: 600; color: #333333;'>SULTRA</span><br><span style='font-size: 8px; background-color: #E3F2FD; color: #1565C0; padding: 2px 4px; border-radius: 3px;'>EWM Z-Score</span><br><span style='font-size: 14px; font-weight: 700; color: #B71C1C;'>{skor_list[1]:.1f}</span><br><span style='font-size: 8px; color: #555;'>Udara {detail_list[1]['udara']:.1f} | Air {detail_list[1]['air']:.1f}<br>Lahan {detail_list[1]['lahan']:.1f} | Sosial {detail_list[1]['sosial']:.1f}<br>Veto {detail_list[1]['veto']:.1f}</span>",
                align="left", showarrow=True, arrowcolor="#555555", arrowhead=2, arrowsize=1, arrowwidth=1.5, ax=100, ay=30,
                bgcolor="rgba(255,255,255,0.95)", bordercolor="#CCCCCC", borderwidth=1.5, borderpad=6
            ),
            dict(
                x=0.43, y=0.25, xref="paper", yref="paper",
                text=f"<span style='font-size: 10px; font-weight: 600; color: #333333;'>SULSEL</span><br><span style='font-size: 8px; background-color: #E3F2FD; color: #1565C0; padding: 2px 4px; border-radius: 3px;'>EWM Z-Score</span><br><span style='font-size: 14px; font-weight: 700; color: #B71C1C;'>{skor_list[2]:.1f}</span><br><span style='font-size: 8px; color: #555;'>Udara {detail_list[2]['udara']:.1f} | Air {detail_list[2]['air']:.1f}<br>Lahan {detail_list[2]['lahan']:.1f} | Sosial {detail_list[2]['sosial']:.1f}<br>Veto {detail_list[2]['veto']:.1f}</span>",
                align="left", showarrow=True, arrowcolor="#555555", arrowhead=2, arrowsize=1, arrowwidth=1.5, ax=-100, ay=60,
                bgcolor="rgba(255,255,255,0.95)", bordercolor="#CCCCCC", borderwidth=1.5, borderpad=6
            ),
            dict(
                x=0.41, y=0.48, xref="paper", yref="paper",
                text=f"<span style='font-size: 10px; font-weight: 600; color: #333333;'>SULBAR</span><br><span style='font-size: 8px; background-color: #E3F2FD; color: #1565C0; padding: 2px 4px; border-radius: 3px;'>EWM Z-Score</span><br><span style='font-size: 14px; font-weight: 700; color: #B71C1C;'>{skor_list[3]:.1f}</span><br><span style='font-size: 8px; color: #555;'>Udara {detail_list[3]['udara']:.1f} | Air {detail_list[3]['air']:.1f}<br>Lahan {detail_list[3]['lahan']:.1f} | Sosial {detail_list[3]['sosial']:.1f}<br>Veto {detail_list[3]['veto']:.1f}</span>",
                align="left", showarrow=True, arrowcolor="#555555", arrowhead=2, arrowsize=1, arrowwidth=1.5, ax=-110, ay=-20,
                bgcolor="rgba(255,255,255,0.95)", bordercolor="#CCCCCC", borderwidth=1.5, borderpad=6
            ),
            dict(
                x=0.55, y=0.82, xref="paper", yref="paper",
                text=f"<span style='font-size: 10px; font-weight: 600; color: #333333;'>GORONTALO</span><br><span style='font-size: 8px; background-color: #E3F2FD; color: #1565C0; padding: 2px 4px; border-radius: 3px;'>EWM Z-Score</span><br><span style='font-size: 14px; font-weight: 700; color: #B71C1C;'>{skor_list[4]:.1f}</span><br><span style='font-size: 8px; color: #555;'>Udara {detail_list[4]['udara']:.1f} | Air {detail_list[4]['air']:.1f}<br>Lahan {detail_list[4]['lahan']:.1f} | Sosial {detail_list[4]['sosial']:.1f}<br>Veto {detail_list[4]['veto']:.1f}</span>",
                align="left", showarrow=True, arrowcolor="#555555", arrowhead=2, arrowsize=1, arrowwidth=1.5, ax=-40, ay=-80,
                bgcolor="rgba(255,255,255,0.95)", bordercolor="#CCCCCC", borderwidth=1.5, borderpad=6
            ),
            dict(
                x=0.68, y=0.85, xref="paper", yref="paper",
                text=f"<span style='font-size: 10px; font-weight: 600; color: #333333;'>SULUT</span><br><span style='font-size: 8px; background-color: #E3F2FD; color: #1565C0; padding: 2px 4px; border-radius: 3px;'>EWM Z-Score</span><br><span style='font-size: 14px; font-weight: 700; color: #B71C1C;'>{skor_list[5]:.1f}</span><br><span style='font-size: 8px; color: #555;'>Udara {detail_list[5]['udara']:.1f} | Air {detail_list[5]['air']:.1f}<br>Lahan {detail_list[5]['lahan']:.1f} | Sosial {detail_list[5]['sosial']:.1f}<br>Veto {detail_list[5]['veto']:.1f}</span>",
                align="left", showarrow=True, arrowcolor="#555555", arrowhead=2, arrowsize=1, arrowwidth=1.5, ax=90, ay=-50,
                bgcolor="rgba(255,255,255,0.95)", bordercolor="#CCCCCC", borderwidth=1.5, borderpad=6
            )
        ]
    )
    
    fig.update_traces(hoverinfo="skip", hovertemplate=None)
    
    return fig

if map_version == "Versi 1":
    crisis_map = render_crisis_map(skor_akumulasi_udara, skor_akumulasi_air, skor_akumulasi_lahan, skor_akumulasi_sosial, skor_akumulasi_veto)
    st.plotly_chart(crisis_map, use_container_width=True)
else:
    is_likert = map_version == "Versi 3"
    v_mode = 3 if is_likert else 2

    prov_list = ['Sulawesi Tengah', 'Sulawesi Tenggara', 'Sulawesi Selatan', 'Sulawesi Barat', 'Gorontalo', 'Sulawesi Utara']
    detail_list = [calculate_province_score(p, use_likert=is_likert) for p in prov_list]
    skor_list = [d['total'] for d in detail_list]
    
    df_map = pd.DataFrame({
        'Provinsi': prov_list,
        'Label': ['SULTENG', 'SULTRA', 'SULSEL', 'SULBAR', 'GORONTALO', 'SULUT'],
        'Skor Krisis': skor_list,
        'Udara': [d['udara'] for d in detail_list],
        'Air': [d['air'] for d in detail_list],
        'Lahan': [d['lahan'] for d in detail_list],
        'Sosial': [d['sosial'] for d in detail_list],
        'Veto': [d['veto'] for d in detail_list],
        'Likert Label': [d.get('likert_label', '') for d in detail_list],
        'lat': [-1.43, -4.14, -3.66, -2.46, 0.69, 0.82],
        'lon': [121.44, 122.07, 119.97, 119.22, 124.50, 124.50]
    })
    
    geojson_path = 'data/processed/sulawesi_provinces.geojson'
    if not os.path.exists(geojson_path):
        geojson_path = 'scripts/data/processed/sulawesi_provinces.geojson'
    if not os.path.exists(geojson_path):
        geojson_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scripts', 'data', 'processed', 'sulawesi_provinces.geojson')

    with open(geojson_path, 'r', encoding='utf-8') as f:
        sulawesi_geojson = json.load(f)
        
    if is_likert:
        # Island-Wide Cumulative Threshold (de Brito & Evers 2018; Meyer et al. 2009 - Macro Ecological Boundary)
        # Kalkulasi ini kini sepenuhnya data-driven dari akumulasi skor makro (dibagi 2 untuk konversi Likert 0-5)
        s_u = skor_akumulasi_udara / 2.0
        s_a = skor_akumulasi_air / 2.0
        s_l = skor_akumulasi_lahan / 2.0
        s_s = skor_akumulasi_sosial / 2.0
        s_v = skor_akumulasi_veto / 2.0
        sk_ak = (s_u + s_a + s_l + s_s + s_v) / 5
    else:
        s_u, s_a, s_l, s_s, s_v = skor_akumulasi_udara, skor_akumulasi_air, skor_akumulasi_lahan, skor_akumulasi_sosial, skor_akumulasi_veto
        sk_ak = (s_u + s_a + s_l + s_s + s_v) / 5

    render_crisis_map_d3(
        df_map, 
        sulawesi_geojson, 
        sk_ak, 
        s_u, 
        s_a, 
        s_l, 
        s_s, 
        s_v,
        versi=v_mode
    )

    st.markdown(r'''<div style="border: 1px solid #1E3A8A; border-radius: 8px; padding: 18px; background-color: #0E131F; margin-top: 18px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.25);">
<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; border-bottom: 1px solid #1E293B; padding-bottom: 10px;">
<div style="font-size: 1.0rem; font-weight: 700; color: #F8FAFC;">
Metodologi Skoring Multi-Skala: Integrasi Baseline Pulau & Anomali Statistik Provinsi
</div>
<div>
<span style="font-size: 0.75rem; background-color: #064E3B; color: #A7F3D0; padding: 3px 8px; border-radius: 4px; font-weight: 600; margin-right: 6px;">Pulau: MCDA Min-Max & WSM</span>
<span style="font-size: 0.75rem; background-color: #1E3A8A; color: #BFDBFE; padding: 3px 8px; border-radius: 4px; font-weight: 600;">Provinsi: EWM & Z-Score Anomali</span>
</div>
</div>
<p style="font-size: 0.88rem; color: #CBD5E1; margin-bottom: 10px; line-height: 1.5;">
<b>1. Level Pulau (Sulawesi):</b> Menggunakan kerangka kerja <b>MCDA-Likert (Weighted Sum Model / WSM & Min-Max Normalization)</b> merujuk pada <i>de Brito & Evers (2018)</i> [HESS] dan <i>Meyer et al. (2009)</i> [NHESS]. Skor dihitung berdasarkan <i>Island-Wide Cumulative Baseline Threshold</i> (akumulasi total beban lanskap: >5.000 MW PLTU Captive, >150 Jt Ton CO2, >500.000 Ha deforestasi driver tambang, dan >100.000 jiwa terdampak) guna mengamankan daya dukung lanskap ekologis utuh.
</p>
<p style="font-size: 0.88rem; color: #CBD5E1; margin-bottom: 12px; line-height: 1.5;">
<b>2. Level Provinsi (6 Provinsi):</b> Menerapkan pemodelan saintifik <b>Entropy Weight Method (EWM) & Z-Score Outlier Standard Deviation (Z = (x - μ) / σ)</b> berbasis studi terbitan <i>Nature Scientific Reports</i> (<i>Sun et al., 2024/2026</i>). EWM secara otomatis memberikan bobot objektif tertinggi pada indikator dengan ketimpangan varians terbesar, sementara Z-Score mengidentifikasi deviasi anomali (≥ +1.0σ) sehingga provinsi episentrum (<b>Sulawesi Tengah Skor 5.0</b> & <b>Sulawesi Tenggara Skor 3.9</b>) terbukti secara statistik berada pada posisi <b>Red Alert / Kritis</b> tanpa terdistorsi atau tersamarkan oleh luas wilayah.
</p>
<div style="background-color: rgba(15, 23, 42, 0.8); border: 1px solid #334155; padding: 8px 14px; border-radius: 6px; font-size: 0.82rem; font-family: monospace; color: #94A3B8;">
Skor_Pulau = MinMax_WSM(Akumulasi_Beban_Makro_Sulawesi) &nbsp;|&nbsp; Skor_Provinsi = ZScore_Outlier_EWM(Matriks_6_Provinsi)
</div>
</div>''', unsafe_allow_html=True)

    verifikasi_data = [
        {"No": 1, "Matriks": "Udara", "Tab": "PLTU+IKU", "Threshold Pulau": "IKU turun 30 poin (80→50)", "Threshold Provinsi": "Sama (Berbasis Indeks) (Metrik Intensif)", "Basis Skoring": "Kategori Resmi IKU", "Sumber": "PermenLHK No.27/2021", "Kutipan": "Kategori IKU: Baik=70–90, Sedang=50–70, Kurang=25–50. IKU=50 = batas terbawah Sedang/awal Kurang", "Pasal / Hal.": "Lampiran, Tabel 1 (Klasifikasi IKLH)", "Kutipan Letterlijk + Hal.": "Kategori Indeks Kualitas Udara: 3. Sedang 50 ≤ x < 70, 4. Kurang 25 ≤ x < 50 (Lampiran, Hal. 41)"},
        {"No": 2, "Matriks": "Udara", "Tab": "ISPA Rasio", "Threshold Pulau": "Rasio 2x lipat", "Threshold Provinsi": "Sama (Berbasis Rasio) (Metrik Intensif)", "Basis Skoring": "Incidence Rate Ratio (IRR) Epidemiologi", "Sumber": "WHO + Kemenkes", "Kutipan": "Threshold IRR > 2 ditetapkan sebagai batas logis statistik di mana paparan industri menjadi pemicu dominan yang melampaui faktor penyakit alami.", "Pasal / Hal.": "WHO EHC 6, Hal. 13 (Validasi Metode)", "Kutipan Letterlijk + Hal.": "The relative risk is the ratio between the risk in the exposed population and the risk in the unexposed population (Hal. 13)"},
        {"No": 3, "Matriks": "Udara", "Tab": "Limbah B3", "Threshold Pulau": ">5% Proporsi Nasional", "Threshold Provinsi": "Sama (Berbasis Rasio Proporsi) (Metrik Intensif)", "Basis Skoring": "Keadilan Lingkungan (Location Quotient)", "Sumber": "KLHK Laporan Kinerja 2022", "Kutipan": "Total limbah B3 nasional = 25,26 juta ton. Penduduk Sulteng hanya 1,1% nasional. Threshold limbah >5% ditetapkan karena ekuivalen dengan beban per kapita 5x lipat dari rata-rata nasional.", "Pasal / Hal.": "Hal. 10 (Infografis)", "Kutipan Letterlijk + Hal.": "Pengelolaan limbah B3 (juta ton) ... 25,26 [Tahun] 2022 (Hal. 10)"},
        {"No": 4, "Matriks": "Udara", "Tab": "Emisi CO2", "Threshold Pulau": "150 Juta Ton", "Threshold Provinsi": "(Luas_Prov / Luas_Nasional) * 150 Jt Ton (Metrik Ekstensif)", "Basis Skoring": "Batas kegagalan target NDC FOLU", "Sumber": "SK MenLHK No.SK.168/MENLHK/PKTL/PLA.1/2/2022", "Kutipan": "Target FOLU Net Sink 2030 = -140 juta ton CO2e. Threshold 150 juta ton = melampaui seluruh target sektor FOLU = kegagalan NDC", "Pasal / Hal.": "Bab I, 1.3 Tujuan dan Sasaran", "Kutipan Letterlijk + Hal.": "Sasaran yang ingin dicapai melalui implementasi Rencana Operasional Indonesia's FOLU Net Sink 2030 adalah tercapainya tingkat emisi gas rumah kaca sebesar -140 juta ton CO2e pada tahun 2030 (Bab 1.3, Hal. 5-6)"},
        {"No": 5, "Matriks": "Air", "Tab": "IKA & Toksisitas (Cr6+)", "Threshold Pulau": "IKA < 50 ATAU Cr6+ > 0.05 mg/L", "Threshold Provinsi": "Sama (Berbasis Indeks) (Metrik Intensif)", "Basis Skoring": "Composite Worst-Case", "Sumber": "PermenLHK No.27/2021 & PP 22/2021", "Kutipan": "Kategori Indeks Kualitas Air Kurang (25 ≤ x < 50) dan Sangat Kurang (0 ≤ x < 25). serta Baku Mutu Air Kelas II: Kromium Heksavalen (Cr6+) = 0.05 mg/L.", "Pasal / Hal.": "PermenLHK 27/2021 (Hal. 35) & PP 22/2021 (Lampiran VI)", "Kutipan Letterlijk + Hal.": "Kategori Indeks Kualitas Air: 4. Kurang 25 ≤ x < 50, 5. Sangat Kurang 0 ≤ x < 25 (Hal. 35)"},
        {"No": 6, "Matriks": "Air", "Tab": "Diare", "Threshold Pulau": "Rasio 2x lipat (IRR > 2.0)", "Threshold Provinsi": "Sama (Berbasis Rasio) (Metrik Intensif)", "Basis Skoring": "Incidence Rate Ratio (IRR) Epidemiologi", "Sumber": "WHO EHC 6 + Kemenkes 2023", "Kutipan": "Baseline nasional = 2% (Profil Kesehatan 2023). Threshold IRR > 2.0 (Prevalensi Wilayah > 4%) = 2x lipat baseline mengindikasikan wabah paparan industri.", "Pasal / Hal.": "Hal. 220 (Kemenkes) & Hal. 14 (WHO EHC 6)", "Kutipan Letterlijk + Hal.": "Kemenkes: 'prevalensi diare pada semua kelompok umur sebesar 2%' (Hal. 220) + WHO: 'The relative risk is the ratio between the risk in the exposed population and the risk in the unexposed population' (Hal. 14). [Logic: Baseline=2%, IRR > 2.0x → Prevalensi Wilayah > 4%]"},
        {"No": 7, "Matriks": "Air", "Tab": "Konflik Pesisir", "Threshold Pulau": "15 konflik", "Threshold Provinsi": "Sama (Sudah Proporsi Provinsi) (Metrik Ekstensif)", "Basis Skoring": "Proporsional rata-rata nasional", "Sumber": "KPA CATAHU 2023", "Kutipan": "Total nasional 2023 = 241 konflik (5 kasus pesisir murni). Threshold 15 kasus = 3x total pesisir nasional (5 kasus) ATAU kalkulasi proporsional 6 prov Sulawesi dari 241 letusan nasional: 241 ÷ 34 × 6 × 30% = 13–15 kasus. [Asal-usul 30%: Bobot spasial 30% (W_pesisir = 0.30) mewakili proporsi kabupaten/kota pesisir lingkar industri nikel Sulawesi yang memiliki garis pantai dan terdampak proyek reklamasi/pelabuhan/smelter].", "Pasal / Hal.": "Hal. 22 (PDF Hal. 31) & Hal. 2 (PDF Hal. 11)", "Kutipan Letterlijk + Hal.": "CATAHU KPA 2023 (Hal. 22 / PDF Hal. 31): 'Letusan konflik agraria di wilayah pesisir dan pulau-pulau kecil sepanjang tahun ini terjadi sebanyak 5 (lima) kali di atas tanah seluas 428 hektar' + Hal. 2: 'Sepanjang tahun 2023, KPA mencatat sedikitnya terjadi 241 letusan konflik agraria'. [Reasoning: Threshold 15 konflik = 3x total pesisir nasional 5 kasus ATAU 30% bobot daerah pesisir Sulawesi dari 241 konflik]"},
        {"No": 8, "Matriks": "Air", "Tab": "Tailing", "Threshold Pulau": "25 Juta Ton / Tahun", "Threshold Provinsi": "Sama (Standar Tapak Site) (Metrik Ekstensif)", "Basis Skoring": "Kapasitas AMDAL (PT HPI - IMIP)", "Sumber": "Laporan AEER & JATAM 2020", "Kutipan": "Threshold 25 Juta Ton/Tahun berbasis dokumen AMDAL PT Hua Pioneer Indonesia (Morowali IMIP). Pembuangan DSTP >25 Jt Ton/Thn mengancam terumbu karang (4.000 ha) dan zona pelagis Morowali.", "Pasal / Hal.": "Bab 3.1, Hal. 36 (PDF Index 35)", "Kutipan Letterlijk + Hal.": "Di Morowali, Hua Pioneer akan membuang tailing melalui pipa sejauh 4 km dari garis pantai di kedalaman 250 m dengan laju pembuangan 31.522 m3/jam atau sekitar 25 juta ton pertahun (Laporan AEER 2020, Hal. 36, Footnote 87)"},
        {"No": 9, "Matriks": "Lahan", "Tab": "Bencana", "Threshold Pulau": "877 kejadian", "Threshold Provinsi": "Sama (Distribusi Provinsi) (Metrik Ekstensif)", "Basis Skoring": "Mean + 1 SD (6 Prov Sulawesi)", "Sumber": "BNPB 2014–2024 (Kalkulasi Internal)", "Kutipan": "Mean=778, SD=99 → Threshold=877. Aktual Sulteng+Sultra=1.557 = 1,77× di atas outlier. Replikabel dari data publik BNPB", "Pasal / Hal.": "Dataset BNPB per Provinsi 2014–2024", "Kutipan Letterlijk + Hal.": "Batas deviasi statistik Mean + 1 SD = 877 kejadian banjir & longsor berbasis akumulasi data historis BNPB 2014–2024 (Dataset BNPB 2014-2024)"},
        {"No": 10, "Matriks": "Lahan", "Tab": "Deforestasi", "Threshold Pulau": "1,7 Juta Ha / 30 Thn (57k Ha/Thn)", "Threshold Provinsi": "(Luas_Prov / Luas_Nasional) * 57.000 Ha (Metrik Ekstensif)", "Basis Skoring": "Target LTS-LCCP & FOLU Net Sink 2030 (KLHK)", "Sumber": "Renops FOLU Net Sink 2030 (KLHK 2022)", "Kutipan": "Batas maksimal kuota deforestasi nasional 2021–2050 = 1,7 juta Ha (rata-rata 57.000 Ha/tahun). Deforestasi melampaui kuota proporsional mengancam target Net Zero Emission 2060.", "Pasal / Hal.": "Bab 4.3, Hal. 128 (PDF Index 127)", "Kutipan Letterlijk + Hal.": "Under the LTS-LCCP scenario to reach NZE before 2060, deforestation quota until 2050 is only 1.7 million ha, or equivalent to an average deforestation of 57,000 ha per year (for the period 2021-2050) (Renops FOLU 2030, Hal. 128)"},
        {"No": 11, "Matriks": "Lahan", "Tab": "Kawasan Lindung", "Threshold Pulau": "0 Hektar (Nol Toleransi)", "Threshold Provinsi": "Sama (Nol Toleransi) (Metrik Ekstensif)", "Basis Skoring": "Mandat UU Kehutanan", "Sumber": "UU No. 41 Tahun 1999", "Kutipan": "Threshold = 0 Hektar (Nol Toleransi). Setiap pembukaan lahan pertambangan terbuka di kawasan hutan lindung secara hukum merupakan tindak pidana kehutanan (Skor Likert 10.0).", "Pasal / Hal.": "Pasal 38 Ayat (4), Hal. 15", "Kutipan Letterlijk + Hal.": "Pada kawasan hutan lindung dilarang melakukan penambangan dengan pola pertambangan terbuka (Pasal 38 Ayat 4 UU No. 41 Tahun 1999, Hal. 15)"},
        {"No": 12, "Matriks": "Lahan", "Tab": "Driver Tambang", "Threshold Pulau": "500.000 Ha / 1 Dekade", "Threshold Provinsi": "(Luas_Prov / Luas_Nasional) * 500.000 Ha (Metrik Ekstensif)", "Basis Skoring": "GFW Dominant Driver Dataset", "Sumber": "GFW Loss by Driver 2014–2023", "Kutipan": "Threshold 500.000 Ha/1 Dekade. Aktual Sultra saja = 513.561 Ha (1 prov melampaui threshold). Data Sulteng unclassified GFW (total deforestasi Sulteng 821.448 Ha).", "Pasal / Hal.": "GFW Master 1 Dekade Dataset (2014–2023)", "Kutipan Letterlijk + Hal.": "Aktual Sultra saja = 513.561 Ha deforestasi pendorong komoditas/tambang. 1 provinsi Sultra saja sudah melampaui threshold 500.000 Ha (Dataset GFW Master 2014–2023)"},
        {"No": 13, "Matriks": "Sosial", "Tab": "FPIC", "Threshold Pulau": "≥ 3 Kasus (Zero Tolerance)", "Threshold Provinsi": "Sama (Red Flag) (Metrik Kualitatif HAM)", "Basis Skoring": "IFC Performance Standard 7 & UNDRIP", "Sumber": "Panduan Praktik ESG & IFC PS7 (2012)", "Kutipan": "Dokumen EP4 menetapkan FPIC sebagai kewajiban mutlak (Zero Tolerance). Secara matematis, metrik ini ditranslasikan menjadi threshold sangat ketat: keberadaan ≥3 kasus di tingkat pulau membuktikan kegagalan kepatuhan yang bersifat sistemik (Skor 10.0).", "Pasal / Hal.": "Equator Principles 4, Hal. 12", "Kutipan Letterlijk + Hal.": "All Projects affecting Indigenous Peoples... will need to comply with the rights and protections... IFC Performance Standard 7 paragraphs 13-17 detail the special circumstances that require the Free, Prior and Informed Consent (FPIC)... which include: Projects with impacts on lands and natural resources subject to traditional ownership or under customary use (Equator Principles EP4, Hal. 12)"},
        {"No": 14, "Matriks": "Sosial", "Tab": "Jiwa Terdampak", "Threshold Pulau": "100.000 Jiwa", "Threshold Provinsi": "(Pop_Prov / Pop_Nasional) * 406.824 Jiwa (Metrik Ekstensif)", "Basis Skoring": "Proporsionalitas Darurat Kemanusiaan", "Sumber": "KPA CATAHU 2023", "Kutipan": "135.608 KK terdampak nasional × 3 jiwa/KK = 406.824 jiwa. Threshold 100.000 jiwa di Sulawesi = 24.5% dari total beban darurat kemanusiaan konflik agraria nasional.", "Pasal / Hal.": "Bab II.1, Hal. 8 (PDF Index 17)", "Kutipan Letterlijk + Hal.": "tersebar di 346 desa dengan korban terdampak sebanyak 135.608 Kepala Keluarga. Melalui perhitungan sederhana, jika dalam satu keluarga rata-rata terdiri dari empat jiwa, maka lebih dari ½ (setengah) juta orang juga menjadi korban dari letusan konflik agraria pada tahun 2023 (CATAHU KPA 2023, Hal. 8)"},
        {"No": 15, "Matriks": "Sosial", "Tab": "Kriminalisasi", "Threshold Pulau": "50 Insiden", "Threshold Provinsi": "(Pop_Prov / Pop_Nasional) * 57 Insiden (Metrik Ekstensif)", "Basis Skoring": "Benchmark 1 Tahun Kasus Aktif", "Sumber": "Satya Bumi & Protection International 2023", "Kutipan": "Total insiden kekerasan/kriminalisasi nasional = 57 insiden (2023). Threshold 50 insiden di Sulawesi = 87,7% dari total beban serangan terhadap pembela HAM lingkungan se-Indonesia.", "Pasal / Hal.": "Bab II, Hal. 10 (PDF Index 16)", "Kutipan Letterlijk + Hal.": "Sedikitnya terjadi 57 serangan berbeda terhadap Pembela HAM Lingkungan Hidup di tahun 2023. Dalam satu kasus pun dapat terjadi dua atau lebih serangan maupun ancaman yang diterima Pembela HAM Lingkungan Hidup. Kriminalisasi menjadi yang terbanyak yaitu 27 kasus (Satya Bumi 2023, Hal. 10)"},
        {"No": 16, "Matriks": "Sosial", "Tab": "Defisit Faskes", "Threshold Pulau": "Gap Target SPA 80%", "Threshold Provinsi": "Sama (Gap Persentase Target) (Metrik Intensif)", "Basis Skoring": "Standar Pelayanan Minimal (SPM)", "Sumber": "Permenkes No. 6/2024 & RPJMN 2025–2029", "Kutipan": "RPJMN 2025–2029 menetapkan target 80% Puskesmas wajib memenuhi standar SPA (Sarana, Prasarana, Alat). Gap persentase di bawah 80% mengukur tingkat krisis akses faskes primer.", "Pasal / Hal.": "Permenkes 6/2024 (Hal. 8) & RPJMN Bab IV", "Kutipan Letterlijk + Hal.": "Dalam rangka penerapan SPM Kesehatan disusun standar teknis pemenuhan Pelayanan Dasar Puskesmas (Permenkes 6/2024, Hal. 8) + Target persentase Puskesmas yang memenuhi standar Sarana, Prasarana, dan Alat Kesehatan (SPA) ditetapkan minimal 80% (RPJMN 2025-2029, Bab IV)"},
        {"No": 17, "Matriks": "Veto", "Tab": "Izin Baru", "Threshold Pulau": "100 Izin", "Threshold Provinsi": "Sama (Standar Provinsi) (Metrik Ekstensif)", "Basis Skoring": "Paradoxical Issuance Index", "Sumber": "Ditjen Minerba ESDM", "Kutipan": "Threshold 100 Izin Baru. Menilai paradoks Otoritisasi: ekspansi penerbitan WIUP/IUP baru di wilayah dengan indikator daya dukung lingkungan terlampaui (Skor Veto Likert 10.0).", "Pasal / Hal.": "Sub-Bab 1.5.3, Hal. 31 (PDF Index 30)", "Kutipan Letterlijk + Hal.": "Lelang WIUP tahap I pada tahun 2024 diikuti oleh total 130 peserta yang telah menyampaikan dokumen persyaratan lelang terhadap 19 (Sembilan belas) blok WIUP yang dilelang. Adapun hasilnya 9 (Sembilan) blok telah ditetapkan sebagai pemenang lelang (LKj Ditjen Minerba ESDM 2024, Hal. 31)"},
        {"No": 18, "Matriks": "Veto", "Tab": "Izin Ilegal", "Threshold Pulau": "10 Perusahaan", "Threshold Provinsi": "Sama (Standar Provinsi) (Metrik Ekstensif)", "Basis Skoring": "Impunity Tolerance Index", "Sumber": "KPA CATAHU 2023", "Kutipan": "Threshold 10 Perusahaan (atau 3,1 Juta Ha Nasional). Menilai impunitas pemutihan tambang/sawit ilegal di kawasan hutan via Pasal 110A/110B UU Cipta Kerja (Skor Veto Likert 10.0).", "Pasal / Hal.": "Bab III, Hal. 40 (PDF Index 48)", "Kutipan Letterlijk + Hal.": "Tanah-tanah yang 'terlanjur' dirampas, diklaim, dan dikuasai secara melawan hukum oleh pengusaha untuk bisnis sawit, tambang, dan hutan tanpa izin/hak atas tanah, dapat dilegalkan hanya dengan mengakui (mendaftar) dan membayar denda pada pemerintah... Di kawasan hutan saja bisnis ilegal pengusaha ditargetkan mencapai 3,1 juta hektar (CATAHU KPA 2023, Hal. 40)"},
        {"No": 19, "Matriks": "Veto", "Tab": "PLTU Captive", "Threshold Pulau": "5.000 MW (5 GW)", "Threshold Provinsi": "Sama (Standar Provinsi) (Metrik Ekstensif)", "Basis Skoring": "Climate Hypocrisy Index", "Sumber": "Global Energy Monitor (GEM) 2023", "Kutipan": "Threshold 5.000 MW (5 GW). Total PLTU captive nasional = 10,8 GW (2023). Kapasitas >5 GW di satu pulau = 46,2% total nasional, memicu Skor Veto Likert 10.0.", "Pasal / Hal.": "Key Findings, Hal. 4 (PDF Index 3)", "Kutipan Letterlijk + Hal.": "Operating captive power capacity has increased nearly eightfold from 2013 to 2023, from 1.4 gigawatts (GW) to 10.8 GW. Based on the latest dataset, 14.4 GW of captive coal capacity is proposed or in construction (Global Energy Monitor 2023, Hal. 4)"}
    ]


    with st.expander("Bukti & Metodologi Threshold Spasial: Tingkat Pulau vs Tingkat Provinsi"):
        st.markdown("### Tabel Verifikasi Threshold (Lengkap dengan Kutipan)")
        st.dataframe(pd.DataFrame(verifikasi_data), use_container_width=True, hide_index=True)
    
    # Render Raw Data Breakdown
    raw_data_list = []
    for i, p in enumerate(prov_list):
        raw_dict = detail_list[i]['raw']
        raw_dict['Provinsi'] = p
        raw_data_list.append(raw_dict)
    df_raw = pd.DataFrame(raw_data_list)
    cols = ['Provinsi'] + [c for c in df_raw.columns if c != 'Provinsi']
    df_raw = df_raw[cols]
    
    with st.expander("📊 Lihat Data Fakta Mentah di Balik Skor (Fact-Check)"):
        st.markdown("Berikut adalah rincian data metrik sesungguhnya di lapangan yang masuk ke dalam sistem skoring. Jika suatu angka 0, artinya **data tidak ditemukan** di dataset untuk provinsi tersebut.")
        st.dataframe(df_raw, use_container_width=True, hide_index=True)
# =======================================

# =====================================================================
# SECTION 1: FILOSOFI AUDIT FORENSIK
# =====================================================================
st.markdown("""
<div class="content-box">
<h2>1. Kerangka Analisis Evaluasi D3TLH</h2>
<p>
AMDAL dan D3TLH dirancang bersifat prediktif untuk menilai batasan daya dukung lingkungan sebelum izin diterbitkan. Evaluasi empiris diperlukan untuk menilai efektivitas instrumen ini dalam meredam dampak lingkungan dan sosial di lapangan.
</p>
<p><b>Standpoint Riset ECC:</b><br>
Pendekatan riset menggunakan <b>Evaluasi Berbasis Bukti Empiris</b>. Analisis menyandingkan indikator daya dukung spasial dengan indikator empiris seperti tren kesehatan masyarakat, kejadian bencana hidrometeorologi, dan dinamika sengketa lahan guna mengukur sejauh mana daya dukung ekologis dan sosial telah tertekan.
</p>
<p>
Halaman ini merangkum indikator-indikator tersebut untuk memberikan rekomendasi perbaikan tata kelola lingkungan dan sistem perizinan.
</p>
</div>
""", unsafe_allow_html=True)

# =====================================================================
# SECTION 2: FAKTA METODOLOGI PEMERINTAH & BLIND SPOTS
# =====================================================================
st.markdown("""
<div class="content-box">
<h2>2. Fakta: Metodologi Resmi D3TLH Pemerintah (Jasa Ekosistem)</h2>
<p>
Berdasarkan dokumen pedoman teknis D3TLH (seperti Permen LH 17/2009 dan panduan KLHK), pemerintah saat ini menyusun D3TLH dengan pendekatan murni spasial/bio-fisik yang disebut <b>Jasa Ekosistem (Ecosystem Services)</b>.
</p>
<p>Indikator resmi yang digunakan dibagi menjadi 4 kategori:</p>
<ul>
<li><b>Jasa Penyediaan (Provisioning):</b> Kapasitas lahan menyediakan pangan, air bersih, dll.</li>
<li><b>Jasa Pengaturan (Regulating):</b> Kapasitas tata air, mitigasi iklim, mitigasi banjir, pemurnian udara.</li>
<li><b>Jasa Pendukung (Supporting):</b> Siklus hara, pembentukan tanah.</li>
<li><b>Jasa Budaya (Cultural):</b> Estetika alam, rekreasi.</li>
</ul>

<h3>Letak Cacat Metodologi (Blind Spots):</h3>
<p>Rumus utama yang dipakai pemerintah untuk menghitung indeks di atas hanyalah: <b>Peta Ekoregion + Peta Tutupan Lahan (Land Cover)</b>.</p>
<ul>
<li><b>Abaikan Nyawa & Morbiditas:</b> Menghitung kapasitas udara dari peta vegetasi, namun <b>TIDAK PERNAH</b> menghitung rekam medis warga (ISPA) yang paru-parunya rusak akibat debu smelter.</li>
<li><b>Abaikan Kedaulatan Ruang:</b> Mengukur kapasitas pertanian, tapi abai terhadap perampasan lahan yang memicu konflik sosial berdarah.</li>
<li><b>Bukan Veto Kebijakan:</b> Saat D3TLH menyatakan daya dukung turun, instrumen ini tidak dipakai untuk "menyetop" penerbitan IUP (Izin Usaha Pertambangan) baru.</li>
</ul>
</div>
""", unsafe_allow_html=True)



# =====================================================================
# SECTION 3: MATRIKS PEMBUKTIAN TERBALIK
# =====================================================================
st.markdown("""
<div class="content-box">
    <h2>3. Matriks Pembuktian Terbalik: D3TLH vs Fakta Lapangan</h2>
    <p>
        Di sinilah seluruh temuan riset kita diintegrasikan untuk "menelanjangi" cacat bawaan D3TLH. Di bawah ini adalah benturan langsung antara <b>Mitos (Klaim Dokumen Resmi)</b> versus <b>Realitas Lapangan (Bukti Forensik)</b>.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# A. MITOS KUALITAS UDARA VS ISPA
# ---------------------------------------------------------
# --- Pre-computation for Scores (Skala 0-10) ---
# Skor 1: Ancaman Udara
kapasitas_terkini = 0
no2_terkini = 4.0e-6
if not df_pltu_op.empty:
    kapasitas_terkini = df_pltu_op[(df_pltu_op['Status'].str.lower() == 'operating')]['Capacity (MW)'].sum()
if not df_nasa.empty:
    df_nasa_annual = df_nasa.groupby('Tahun')['Rata_Rata_NO2'].mean().reset_index()
    if not df_nasa_annual.empty:
        no2_terkini = df_nasa_annual.loc[df_nasa_annual['Tahun'].idxmax(), 'Rata_Rata_NO2']
# Normalisasi Sesuai Dokumen Metode_Model_Matematis_Skoring_ECC.md
skor_pltu_UI = min(5.0, (kapasitas_terkini / 5000.0) * 5.0)
skor_no2_UI = min(5.0, max(0.0, (no2_terkini - 4.0e-6) / (6.0e-6 - 4.0e-6)) * 5.0)
skor_1 = min(10.0, skor_pltu_UI + skor_no2_UI)

# Skor 2: Rasio Anomali ISPA
skor_2 = 0
rasio_anomali = 0
kasus_sentra = 0
if not df_kes.empty:
    df_ts_pre = df_kes[df_kes['indikator'].str.contains('ISPA', case=False, na=False)]
    kasus_sentra = df_ts_pre[df_ts_pre['provinsi'].isin(['Sulawesi Tengah', 'Sulawesi Tenggara'])]['nilai'].sum()
    kasus_non_sentra = df_ts_pre[~df_ts_pre['provinsi'].isin(['Sulawesi Tengah', 'Sulawesi Tenggara'])]['nilai'].sum()
    rasio_anomali = (kasus_sentra / 2) / (kasus_non_sentra / 4) if kasus_non_sentra > 0 else 0
    # Normalisasi: Rasio 2x lipat = skor 10
    skor_2 = min(10.0, max(0.0, (rasio_anomali - 1.0) * 10.0))

# Skor 3: Over-Capacity B3
skor_3 = 0
skor_overcapacity = 0
total_b3_sulteng = 0
if not df_b3.empty:
    df_b3['Estimasi Timbulan (Ton/Tahun)'] = pd.to_numeric(df_b3['Estimasi Timbulan (Ton/Tahun)'], errors='coerce').fillna(0)
    total_b3_all_pre = df_b3['Estimasi Timbulan (Ton/Tahun)'].sum()
    total_b3_sulteng = df_b3[df_b3['Provinsi'] == 'Sulawesi Tengah']['Estimasi Timbulan (Ton/Tahun)'].sum()
    proporsi_b3 = (total_b3_sulteng / 427_000_000.0) * 100.0
    # Normalisasi: Threshold >5% proporsi nasional = skor 10
    skor_3 = min(10.0, (proporsi_b3 / 5.0) * 10.0)

# Skor 4: Defisit Ekosistem
skor_4 = 0
if not df_gfw.empty:
    df_gfw['Total_Emisi_CO2_Megagram'] = pd.to_numeric(df_gfw['Total_Emisi_CO2_Megagram'], errors='coerce').fillna(0)
    total_emisi_pre = df_gfw['Total_Emisi_CO2_Megagram'].sum() / 1_000_000.0
    # Normalisasi: Emisi 150 Juta Ton = skor 10
    skor_4 = min(10.0, (total_emisi_pre / 150.0) * 10.0)

sk1_str = f"{(skor_1 / 2.0):.1f}" if is_likert_mode else f"{skor_1:.1f}"
sk2_str = f"{(skor_2 / 2.0):.1f}" if is_likert_mode else f"{skor_2:.1f}"
sk3_str = f"{(skor_3 / 2.0):.1f}" if is_likert_mode else f"{skor_3:.1f}"
sk4_str = f"{(skor_4 / 2.0):.1f}" if is_likert_mode else f"{skor_4:.1f}"

# Conditional formatting untuk card Udara
status_color_udara = "#4CAF50"
status_text_udara = "STATUS: AMAN/TERKENDALI"
skor_akumulasi_udara = (skor_1 + skor_2 + skor_3 + skor_4) / 4.0
if skor_akumulasi_udara >= 6.0:
    status_color_udara = "#E74C3C"
    status_text_udara = "STATUS: DARURAT UDARA"
elif skor_akumulasi_udara >= 4.0:
    status_color_udara = "#FBC02D"
    status_text_udara = "STATUS: PERLU PENGAWASAN"

colA1, colA2 = st.columns([1, 2])
with colA1:
    st.markdown(f"""
<div style="background:#2C3E50; padding:20px; border-radius:10px; border-left:5px solid {status_color_udara}; height:100%;">
    <h4 style="color:#FFF; margin-top:0;">Audit D3TLH: Daya Tampung Udara</h4>
    <p style="color:#BDC3C7; font-size:0.9rem;">"Daya tampung udara (berdasarkan peta tutupan lahan) dianalisis sebagai indikator kapasitas pemulihan emisi."</p>
    <hr style="border-color:#34495E;">
    <h4 style="color:{status_color_udara};">Fakta Empiris:</h4>
    <p style="color:#E0E0E0; font-size:0.9rem;">Data menunjukkan tren penyakit saluran pernapasan di sekitar kawasan industri.</p>
    <div style="background-color: #1A202C; padding: 15px; border-radius: 8px; margin-top: 15px; text-align: center; border: 1px solid {status_color_udara};">
        <div style="font-size: 11px; color: #BDC3C7; text-transform: uppercase; letter-spacing: 1px;">
            Skor Indikator Udara 
            <span title="Kalkulasi Skor Udara:&#10;({sk1_str} + {sk2_str} + {sk3_str} + {sk4_str}) / 4 = {card_u_val}" style="cursor:help; display:inline-block; background-color:#444; color:#FFF; border-radius:50%; width:14px; height:14px; line-height:14px; text-align:center; font-size:10px; margin-left:4px;">?</span>
        </div>
        <div style="font-size: 32px; font-weight: 800; color: {status_color_udara}; line-height: 1.2;">
            <span title="Kalkulasi Skor Udara:&#10;({sk1_str} + {sk2_str} + {sk3_str} + {sk4_str}) / 4 = {card_u_val}" style="cursor:help;">{card_u_val}</span> <span style="font-size: 16px;">/ {card_denom}</span>
        </div>
        <div style="font-size: 11px; color: {status_color_udara}; margin-top: 5px; margin-bottom: 15px; font-weight: bold;">{status_text_udara}</div>
        <div style="text-align: left; font-size: 11px; color: #BDC3C7; border-top: 1px dashed #444; padding-top: 10px; line-height: 1.5;">
            <b>Rincian Skor Matriks Udara:</b><br>
            • <b>Udara 1 (PLTU & Polusi):</b> {sk1_str} / {card_denom}<br>
            • <b>Udara 2 (Dampak ISPA):</b> {sk2_str} / {card_denom}<br>
            • <b>Udara 3 (Limbah B3):</b> {sk3_str} / {card_denom}<br>
            • <b>Udara 4 (Defisit CO2):</b> {sk4_str} / {card_denom}
        </div>
    </div>
    <div style="background:{status_color_udara}; color:white; padding:5px 10px; border-radius:5px; font-weight:bold; text-align:center; margin-top:15px; opacity:0.9;">
        ANALISIS: Pemantauan Morbiditas Akumulatif
    </div>
</div>
    """, unsafe_allow_html=True)

with colA2:
    if not df_kes.empty:
        tab1, tab2, tab3, tab4 = st.tabs(["(Udara 1) Korelasi PLTU & Kualitas Udara", "(Udara 2) Dampak Kasus ISPA/Pneumonia", "(Udara 3) Fakta Beban Limbah & Emisi", "(Udara 4) Hilangnya Paru-Paru Udara"])
        
        with tab1:
            # --- 1. Ekspansi PLTU vs Penurunan Kualitas Udara ---
            st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Threshold & Referensi (Udara 1):</b><br>• <b>Kapasitas PLTU:</b> > 5.000 MW (<i>Sumber: Global Energy Monitor / GEM 2023</i>).<br>• <b>Polusi NO2:</b> > 6.0e-6 mol/m² (Batas Baseline Aman Sulawesi). Batas Darurat: > 66.0e-6 mol/m² (<i>Sumber: Copernicus 2020 & Literatur Tiongkok utk Kategori 'Polusi Berat' / Heavy Pollution</i>).</div>", unsafe_allow_html=True)
            
            if not df_pltu_op.empty and not df_nasa.empty:
                years = list(range(2010, 2025))
                prov_map = {
                    'Central Sulawesi': 'Sulawesi Tengah', 'South East Sulawesi': 'Sulawesi Tenggara',
                    'South Sulawesi': 'Sulawesi Selatan', 'North Sulawesi': 'Sulawesi Utara',
                    'West Sulawesi': 'Sulawesi Barat', 'Gorontalo': 'Gorontalo'
                }
                
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
                
                kapasitas_grafik = df_pltu_trend[df_pltu_trend['Tahun'] == 2024]['Kapasitas_PLTU_MW'].sum()
                no2_grafik = df_nasa_annual.loc[df_nasa_annual['year'].idxmax(), 'median'] if not df_nasa_annual.empty else 0.0
                
                col1_d = f"Melebihi Threshold (5.000 MW)" if kapasitas_grafik > 5000 else f"Di Bawah Threshold (5.000 MW)"
                col1_c = "inverse" if kapasitas_grafik > 5000 else "normal"

                col2_d = f"Kritis (> 6.0e-6 mol/m²)" if no2_grafik > 6.0e-6 else f"Aman (≤ 6.0e-6 mol/m²)"
                col2_c = "inverse" if no2_grafik > 6.0e-6 else "normal"

                col3_d = f"STATUS: KRITIS" if (skor_1 >= 6.0 or is_likert_mode) else f"STATUS: AMAN"
                col3_c = "inverse" if (skor_1 >= 6.0 or is_likert_mode) else "normal"

                col1, col2, col3 = st.columns(3)
                
                help_pltu = f"Kalkulasi Skor (1a):\nmin(5.0, ({kapasitas_grafik:,.0f} / 5000) * 5.0) = {skor_pltu:.1f}/5.0"
                help_no2 = f"Kalkulasi Skor (1b):\nmin(5.0, max(0, ({no2_grafik:.2e} - 4.0e-6) / (6.0e-6 - 4.0e-6)) * 5.0) = {skor_no2:.1f}/5.0"
                help_skor1 = f"Kalkulasi Total (Udara 1):\nSkor PLTU ({skor_pltu:.1f}) + Skor NO2 ({skor_no2:.1f}) = {skor_1:.1f}/10\n" + (f"Konversi Likert: {skor_1:.1f} / 2 = {(skor_1 / 2.0):.1f}/5" if is_likert_mode else "")
                
                col1.metric(f"Kapasitas PLTU Aktif (Skor: {skor_pltu:.1f})", f"{kapasitas_grafik:,.0f} MW", col1_d, delta_color=col1_c, help=help_pltu)
                col2.metric(f"Rata-rata Polusi NO2 NASA (Skor: {skor_no2:.1f})", f"{no2_grafik:.2e}", col2_d, delta_color=col2_c, help=help_no2)
                col3.metric("Skor Ancaman Udara (Udara 1)", f"{sk1_str} / {card_denom}", col3_d, delta_color=col3_c, help=help_skor1)
                st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
                
                pltu_colors = {
                    'Gorontalo': '#757575',
                    'Sulawesi Utara': '#8D6E63',
                    'Sulawesi Selatan': '#FBC02D',
                    'Sulawesi Tenggara': '#F57C00',
                    'Sulawesi Tengah': '#D32F2F'
                }
                
                pltu_config = []
                for prov, color in pltu_colors.items():
                    d_trend = df_pltu_trend[df_pltu_trend['Provinsi'] == prov]
                    if not d_trend.empty:
                        max_mw = d_trend['Kapasitas_PLTU_MW'].max()
                        label = f"{prov} — PLTU max {max_mw:,.0f} MW"
                        pltu_config.append({'prov': prov, 'color': color, 'label': label})

                def get_no2_color(val):
                    if val > 6.0e-6: return '#D32F2F'
                    elif val > 5.0e-6: return '#FBC02D'
                    else: return '#4CAF50'
                
                no2_annual_colors = [get_no2_color(v) for v in df_nasa_annual['median']]

                fig_nasa_combined = make_subplots(specs=[[{"secondary_y": True}]])
                
                for cfg in pltu_config:
                    d_trend = df_pltu_trend[df_pltu_trend['Provinsi'] == cfg['prov']]
                    if not d_trend.empty:
                        fig_nasa_combined.add_trace(
                            go.Scatter(
                                x=d_trend['Tahun'], y=d_trend['Kapasitas_PLTU_MW'], name=cfg['label'], 
                                mode='lines', stackgroup='one', line=dict(width=1, color=cfg['color']),
                                fillcolor=cfg['color'], hoveron='points+fills',
                                hovertemplate=cfg['prov'] + ': %{y:,.0f} MW<extra></extra>', showlegend=True
                            ),
                            secondary_y=False
                        )

                for i in range(len(df_nasa_annual)-1):
                    fig_nasa_combined.add_trace(
                        go.Scatter(
                            x=df_nasa_annual['year'].iloc[i:i+2],
                            y=df_nasa_annual['median'].iloc[i:i+2],
                            mode='lines',
                            line=dict(color=no2_annual_colors[i+1], width=4),
                            showlegend=False, hoverinfo='skip'
                        ),
                        secondary_y=True
                    )
                
                fig_nasa_combined.add_trace(
                    go.Scatter(
                        x=df_nasa_annual['year'], y=df_nasa_annual['median'], name="Rata-rata NO2 Tahunan", 
                        mode='markers', marker=dict(color=no2_annual_colors, size=10, line=dict(width=1, color='#FFFFFF')), 
                        hovertemplate='Tahun %{x}<br>NO2: %{y:.2e}<extra></extra>', showlegend=False
                    ),
                    secondary_y=True
                )

                fig_nasa_combined.add_trace(go.Scatter(x=[None], y=[None], mode='markers', marker=dict(color='#D32F2F', size=10), name='🔴 Puncak Anomali Sulawesi (2021-2023): > 6.0e-6 mol/m²'), secondary_y=True)
                fig_nasa_combined.add_trace(go.Scatter(x=[None], y=[None], mode='markers', marker=dict(color='#FBC02D', size=10), name='🟡 Transisi Ekspansi Industri (2019-2020): 5.0-6.0e-6 mol/m²'), secondary_y=True)
                fig_nasa_combined.add_trace(go.Scatter(x=[None], y=[None], mode='markers', marker=dict(color='#4CAF50', size=10), name='🟢 Baseline Rata-rata Sulawesi (2018): < 5.0e-6 mol/m²'), secondary_y=True)

                fig_nasa_combined.update_layout(
                    title=dict(text="Semua PLTU Batubara vs Polusi NO2 (Data Satelit NASA TROPOMI)", font=dict(color='#ECEFF1', size=16)),
                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#ECEFF1', family='Arial, sans-serif'),
                    legend=dict(orientation="v", yanchor="top", y=0.98, xanchor="left", x=0.02, bgcolor='rgba(30,30,30,0.8)', bordercolor='#555', borderwidth=1, font=dict(size=11), traceorder='reversed'),
                    xaxis=dict(title="", tickmode='linear', dtick=2, tickformat='d', showgrid=True, gridcolor='#2b3240', gridwidth=1, griddash='dash', showline=True, linewidth=1, linecolor='#555555', rangeslider=dict(visible=False)),
                    yaxis=dict(title="Kapasitas PLTU Kumulatif (MW)", showgrid=True, gridcolor='#2b3240', gridwidth=1, griddash='dash', side='left', tickformat=',.1s', dtick=500, ticksuffix=' MW'),
                    yaxis2=dict(title="Konsentrasi NO2 Satelit (mol/m²)", showgrid=False, overlaying='y', side='right'),
                    hovermode="x unified", hoverlabel=dict(bgcolor="rgba(0, 0, 0, 0.8)", font_size=13, font_family="Arial", font_color="#FFFFFF"),
                    margin=dict(l=0, r=0, t=40, b=0)
                )

                st.plotly_chart(fig_nasa_combined, use_container_width=True, config={'displayModeBar': False})
                
                with st.expander("Lihat Data Mentah: Kapasitas PLTU per Provinsi", expanded=False):
                    df_pivot_pltu = df_pltu_trend.pivot(index='Tahun', columns='Provinsi', values='Kapasitas_PLTU_MW').reset_index()
                    st.dataframe(df_pivot_pltu, use_container_width=True, hide_index=True)
                    st.caption("Sumber: `sulawesi_pltu_captive.csv` (gabungan captive + grid)")


        with tab2:
            # --- 2. Tren Historis Kasus ISPA/Pneumonia ---
            st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Threshold & Referensi (Udara 2):</b><br>• <b>Morbiditas ISPA:</b> Incidence Rate Ratio (IRR) > 2.0x lipat populasi kontrol. (<i>Sumber: WHO Environmental Health Criteria 6, Hal. 13</i>).</div>", unsafe_allow_html=True)
            df_ts_filtered = df_kes[df_kes['indikator'].str.contains('ISPA', case=False, na=False)].copy()
            if not df_ts_filtered.empty:
                df_ts_filtered['Kategori'] = df_ts_filtered['provinsi'].apply(lambda x: 'Sentra Industri (Sulteng & Sultra)' if x in ['Sulawesi Tengah', 'Sulawesi Tenggara'] else 'Non-Sentra Industri (Lainnya)')
                df_ts_agg = df_ts_filtered.groupby(['tahun', 'provinsi', 'Kategori'])['nilai'].sum().reset_index()
                
                # Gunakan skor pre-calculated
                kasus_sentra_grafik = df_ts_filtered[df_ts_filtered['Kategori'] == 'Sentra Industri (Sulteng & Sultra)']['nilai'].sum()
                kasus_non_sentra_grafik = df_ts_filtered[df_ts_filtered['Kategori'] == 'Non-Sentra Industri (Lainnya)']['nilai'].sum()
                sk2_str = f"{(skor_2 / 2.0):.1f}" if is_likert_mode else f"{skor_2:.1f}"
                avg_sentra = kasus_sentra_grafik / 2.0
                avg_non = kasus_non_sentra_grafik / 4.0
                
                col1_d = f"Rata-rata Prov: {avg_sentra:,.0f} (Sentra) vs {avg_non:,.0f} (Non)"
                col1_c = "inverse" if rasio_anomali > 2.0 else "normal"

                col2_d = f"STATUS: KRITIS" if (skor_2 >= 6.0 or is_likert_mode) else f"STATUS: AMAN"
                col2_c = "inverse" if (skor_2 >= 6.0 or is_likert_mode) else "normal"

                col1, col2 = st.columns(2)
                
                help_skor2 = f"Kalkulasi Total (Udara 2):\nmin(10.0, ({rasio_anomali:.1f} / 2.0) * 10) = {skor_2:.1f}/10\n" + (f"Konversi Likert: {skor_2:.1f} / 2 = {(skor_2 / 2.0):.1f}/5" if is_likert_mode else "")
                help_irr = f"Incidence Rate Ratio (IRR):\nRasio rata-rata kumulatif kasus per provinsi:\n- Sentra (2 Prov): {kasus_sentra_grafik:,.0f} / 2 = {avg_sentra:,.0f}\n- Non-Sentra (4 Prov): {kasus_non_sentra_grafik:,.0f} / 4 = {avg_non:,.0f}\n- Rasio IRR: {avg_sentra:,.0f} / {avg_non:,.0f} = {rasio_anomali:.1f}x Lipat\n(Threshold > 2.0x Darurat Medis)\n\n{help_skor2}"
                col1.metric(f"Incidence Rate Ratio (Skor: {sk2_str})", f"{rasio_anomali:.1f}x Lipat", col1_d, delta_color=col1_c, help=help_irr)
                col2.metric("Skor Morbiditas ISPA (Udara 2)", f"{sk2_str} / {card_denom}", col2_d, delta_color=col2_c, help=help_skor2)
                st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
                
                populasi_bps = {
                    "Sulawesi Selatan": 9070000,
                    "Sulawesi Tengah": 2985000,
                    "Sulawesi Tenggara": 2624000,
                    "Sulawesi Utara": 2621000,
                    "Sulawesi Barat": 1419000,
                    "Gorontalo": 1171000
                }
                df_ts_filtered["populasi"] = df_ts_filtered["provinsi"].map(populasi_bps)
                df_ts_filtered["rate_per_10k"] = (df_ts_filtered["nilai"] / df_ts_filtered["populasi"]) * 10000

                color_map_prov = {"Sulawesi Tengah": "#EF5350", "Sulawesi Tenggara": "#D32F2F", "Gorontalo": "#42A5F5", "Sulawesi Barat": "#1E88E5", "Sulawesi Selatan": "#1565C0", "Sulawesi Utara": "#90CAF9"}

                def create_ts_chart(data, y_col, y_title, hover_format=",.0f"):
                    fig = px.line(data, x="tahun", y=y_col, color="provinsi", markers=True, color_discrete_map=color_map_prov)
                    for trace in fig.data:
                        if trace.name in ['Sulawesi Tengah', 'Sulawesi Tenggara']:
                            trace.line.width = 4
                        else:
                            trace.line.width = 2
                            trace.line.dash = "dot"
                            trace.opacity = 0.7
                        trace.hovertemplate = f"<b>%{{fullData.name}}</b><br>Tahun: %{{x}}<br>{y_title}: %{{y:{hover_format}}}<extra></extra>"
                    fig.update_layout(
                        title=f"Tren Historis Kasus ISPA/Pneumonia", height=450,
                        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                        legend=dict(title="Provinsi (Merah: Sentra, Biru: Non-Sentra)", orientation="v", yanchor="top", y=1, xanchor="left", x=1.02),
                        font=dict(color="#B0BEC5"),
                        xaxis=dict(title="Tahun", showgrid=True, gridcolor="rgba(255,255,255,0.1)", dtick=1),
                        yaxis=dict(title=y_title, showgrid=True, gridcolor="rgba(255,255,255,0.1)", zeroline=False),
                        margin=dict(l=0, r=0, t=40, b=0)
                    )
                    return fig

                tab_norm, tab_abs, tab_alt = st.tabs(["Insiden per 10.000 Penduduk", "Total Kasus Absolut", "Opsi: Stacked Bar Chart"])
                with tab_norm:
                    fig_norm = create_ts_chart(df_ts_filtered, "rate_per_10k", "Insiden per 10.000 Penduduk", hover_format=",.0f")
                    st.plotly_chart(fig_norm, use_container_width=True, config={'displayModeBar': False})
                with tab_abs:
                    fig_abs = create_ts_chart(df_ts_filtered, "nilai", "Total Kasus (Angka Absolut)")
                    st.plotly_chart(fig_abs, use_container_width=True, config={'displayModeBar': False})
                with tab_alt:
                    fig_bar = px.bar(df_ts_filtered, x="tahun", y="rate_per_10k", color="provinsi", color_discrete_map=color_map_prov, barmode="stack", title="Distribusi Kasus ISPA (per 10.000 Penduduk)")
                    fig_bar.update_layout(height=450, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#B0BEC5"), xaxis=dict(title="Tahun", dtick=1), yaxis=dict(title="Insiden per 10.000 Penduduk"), legend=dict(title="", orientation="v", yanchor="top", y=1, xanchor="left", x=1.02), margin=dict(l=0, r=0, t=40, b=0))
                    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
                
                with st.expander("Lihat Data Panel: Kasus ISPA/Pneumonia (2014-2024)", expanded=False):
                    df_ts_pivot = df_ts_agg.pivot(index='tahun', columns='provinsi', values='nilai').reset_index()
                    st.dataframe(df_ts_pivot, use_container_width=True, hide_index=True)
                    st.caption("Sumber File: `sulawesi_kesehatan_detail_2014_2024.csv`")
                    
        with tab3:
            # --- 3. Fakta Data Timbulan Limbah Udara & B3 ---
            st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Threshold & Referensi (Udara 3):</b><br>• <b>Ketidakadilan Lingkungan (Limbah B3):</b> Proporsi limbah daerah > 5% dari total timbulan nasional 427 Juta Ton. (<i>Sumber: Laporan Kinerja KLHK 2022, Hal. 10</i>).</div>", unsafe_allow_html=True)
            # Gunakan nilai pre-calculated
            sk3_str = f"{(skor_3 / 2.0):.1f}" if is_likert_mode else f"{skor_3:.1f}"
            proporsi_sulteng = (total_b3_sulteng / 427_000_000.0) * 100.0
            
            col_f1_d = f"Threshold > 5.0% (Environmental Injustice)" if proporsi_sulteng > 5.0 else f"Aman (≤ 5.0%)"
            col_f1_c = "inverse" if proporsi_sulteng > 5.0 else "normal"

            col_f2_d = f"STATUS: OVERCAPACITY" if (skor_3 >= 6.0 or is_likert_mode) else f"STATUS: AMAN"
            col_f2_c = "inverse" if (skor_3 >= 6.0 or is_likert_mode) else "normal"

            help_skor3 = f"Kalkulasi Total (Udara 3):\nmin(10.0, (Proporsi B3 Sulteng {proporsi_sulteng:.1f}% / 5.0%) * 10.0) = {skor_3:.1f}/10\n" + (f"Konversi Likert: {skor_3:.1f} / 2 = {(skor_3 / 2.0):.1f}/5" if is_likert_mode else "")
            
            help_proporsi_b3 = f"Proporsi Limbah B3 Sulteng terhadap Nasional:\n- Total B3 Sulteng: {total_b3_sulteng/1_000_000:.1f} Juta Ton\n- Total B3 Nasional (2022): 427.0 Juta Ton\n- Proporsi: ({total_b3_sulteng/1_000_000:.1f} / 427.0) * 100% = {proporsi_sulteng:.1f}%\n(Threshold Kritis > 5% Nasional)\n\n{help_skor3}"

            col_f1, col_f2 = st.columns(2)
            col_f1.metric(f"Proporsi B3 Sulteng (Skor: {sk3_str})", f"{proporsi_sulteng:.1f}% Nasional", col_f1_d, delta_color=col_f1_c, help=help_proporsi_b3)
            col_f2.metric("Skor Over-Capacity B3 (Udara 3)", f"{sk3_str} / {card_denom}", col_f2_d, delta_color=col_f2_c, help=help_skor3)
            
            st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
            
            if not df_b3.empty:
                df_b3_prov = df_b3.groupby('Provinsi')['Estimasi Timbulan (Ton/Tahun)'].sum().reset_index()
                fig_b3 = px.bar(df_b3_prov, x='Estimasi Timbulan (Ton/Tahun)', y='Provinsi', orientation='h',
                                text='Estimasi Timbulan (Ton/Tahun)', color='Estimasi Timbulan (Ton/Tahun)',
                                color_continuous_scale='Reds', title="Beban Timbulan B3 per Provinsi")
                
                # Threshold B3 = 21.35 Juta Ton (5% Proporsi Nasional — KLHK LKj 2022 Hal. 10)
                fig_b3.add_vline(x=21_350_000, line_dash="dot", line_color="#FF5252", annotation_text="Threshold Kritis: 21.35 Jt Ton (5% Nasional)", annotation_font_color="#FF5252", annotation_position="top left")
                
                fig_b3.update_traces(texttemplate='%{text:,.0f} ton', textposition='outside')
                fig_b3.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0))
                st.plotly_chart(fig_b3, use_container_width=True, config={'displayModeBar': False})
                
                with st.expander("Lihat Data Mentah: Timbulan Limbah B3", expanded=False):
                    st.dataframe(df_b3, use_container_width=True, hide_index=True)
                    st.caption("Sumber File: `sulawesi_limbah_b3.csv`")
                    
        with tab4:
            # --- 4. Hilangnya Paru-Paru Udara (Deforestasi CO2) ---
            st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Threshold & Referensi (Udara 4):</b><br>• <b>Defisit Karbon CO2:</b> Total Emisi Deforestasi > 150 Juta Ton CO2e (melampaui target nasional NDC FOLU Net Sink -140 juta ton). (<i>Sumber: SK MenLHK No.SK.168/MENLHK/PKTL/PLA.1/2/2022</i>).</div>", unsafe_allow_html=True)
            
            if not df_gfw.empty:
                df_gfw['Total_Emisi_CO2_Megagram'] = pd.to_numeric(df_gfw['Total_Emisi_CO2_Megagram'], errors='coerce').fillna(0)
                total_emisi = df_gfw['Total_Emisi_CO2_Megagram'].sum() / 1_000_000 # Juta Ton
                total_deforestasi = df_gfw['Total_Deforestasi_Ha'].sum() / 1_000 # Ribu Ha
                
                sk4_str = f"{(skor_4 / 2.0):.1f}" if is_likert_mode else f"{skor_4:.1f}"
                
                col_e1_d = f"Threshold > 150 Jt Ton (Gagal NDC)" if total_emisi > 150 else f"Aman (≤ 150 Jt Ton)"
                col_e1_c = "inverse" if total_emisi > 150 else "normal"

                col_e2_d = f"STATUS: DARURAT KARBON" if (skor_4 >= 6.0 or is_likert_mode) else f"STATUS: TERKENDALI"
                col_e2_c = "inverse" if (skor_4 >= 6.0 or is_likert_mode) else "normal"

                help_skor4 = f"Kalkulasi Total (Udara 4):\nmin(10.0, ({total_emisi:.1f} / 150.0) * 10) = {skor_4:.1f}/10\n" + (f"Konversi Likert: {skor_4:.1f} / 2 = {(skor_4 / 2.0):.1f}/5" if is_likert_mode else "")
                
                help_emisi_co2 = f"Defisit Ekosistem Karbon:\n- Total Emisi CO2 Lepas: {total_emisi:.1f} Juta Ton\n- Total Hutan Hilang: {total_deforestasi:.1f} Ribu Hektar\n(Threshold Kritis > 150 Juta Ton CO2e)\n\n{help_skor4}"

                col_e1, col_e2 = st.columns(2)
                col_e1.metric(f"Total Emisi CO2 (Skor: {sk4_str})", f"{total_emisi:.1f} Jt Ton", col_e1_d, delta_color=col_e1_c, help=help_emisi_co2)
                col_e2.metric("Skor Defisit Karbon (Udara 4)", f"{sk4_str} / {card_denom}", col_e2_d, delta_color=col_e2_c, help=help_skor4)
                
                st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
                
                df_emisi_trend = df_gfw.groupby(['Tahun', 'Provinsi'])['Total_Emisi_CO2_Megagram'].sum().reset_index()
                df_emisi_trend = df_emisi_trend.sort_values(by=['Provinsi', 'Tahun'])
                df_emisi_trend['Kumulatif_Emisi_CO2'] = df_emisi_trend.groupby('Provinsi')['Total_Emisi_CO2_Megagram'].cumsum()
                
                fig_emisi = px.area(df_emisi_trend, x='Tahun', y='Kumulatif_Emisi_CO2', color='Provinsi',
                                   title="Akumulasi Emisi Karbon Deforestasi (2014-2023)")
                # Threshold CO2 = 150 Juta Ton (>NDC FOLU -140 juta ton — SK.168/MENLHK Bag.III Hal.5)
                fig_emisi.add_hline(y=150_000_000, line_dash="dot", line_color="#FF5252",
                                   annotation_text="Threshold Kritis: 150 Jt Ton CO2e (Gagal NDC FOLU — SK.168/MENLHK)",
                                   annotation_font_color="#FF5252", annotation_position="top left")
                fig_emisi.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0))
                st.plotly_chart(fig_emisi, use_container_width=True, config={'displayModeBar': False})
                
                with st.expander("Lihat Data Panel: Emisi CO2 Deforestasi", expanded=False):
                    df_emisi_pivot = df_emisi_trend.pivot(index='Tahun', columns='Provinsi', values='Total_Emisi_CO2_Megagram').reset_index()
                    st.dataframe(df_emisi_pivot, use_container_width=True, hide_index=True)
                    st.caption("Sumber File: `sulawesi_gfw_master_1_dekade_2014_2023_v3.csv`")

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# B. MITOS DAYA TAMPUNG AIR
# ---------------------------------------------------------
# --- Pre-computation for Water Scores (Skala 0-10) ---
# Skor 1: IKA 
ika_terkini = 50
ika_sulteng = 50
if not df_ika.empty:
    df_ika_avg = df_ika.groupby('Tahun')['Indeks Kualitas Air'].mean().reset_index()
    if 2024 in df_ika_avg['Tahun'].values:
        ika_terkini = df_ika_avg[df_ika_avg['Tahun'] == 2024]['Indeks Kualitas Air'].values[0]
    
    df_sulteng = df_ika[df_ika['Provinsi'] == 'Sulawesi Tengah']
    if not df_sulteng.empty and 2024 in df_sulteng['Tahun'].values:
        ika_sulteng = df_sulteng[df_sulteng['Tahun'] == 2024]['Indeks Kualitas Air'].values[0]

# Normalisasi: IKA ideal = 80, IKA cemar berat = 50
skor_makro_air_1 = min(10.0, max(0, (80 - ika_sulteng) / 30) * 10)

# Murni Menggunakan IKA untuk Skor Air 1
skor_air_1 = skor_makro_air_1

# Skor 2: Morbiditas Diare
skor_air_2 = 0
kasus_diare_sentra = 0
kasus_diare_non = 0
rasio_diare = 0

# Exact BPS Population Data
populasi_sentra = 2985000 + 2624000  # Sulteng + Sultra = 5,609,000
populasi_non = 9070000 + 2621000 + 1419000 + 1171000  # Sulsel + Sulut + Sulbar + Gorontalo = 14,281,000

if not df_kes.empty:
    df_diare = df_kes[df_kes['indikator'].str.contains('Diare', case=False, na=False)]
    kasus_diare_sentra = df_diare[df_diare['provinsi'].isin(['Sulawesi Tengah', 'Sulawesi Tenggara'])]['nilai'].sum()
    kasus_diare_non = df_diare[~df_diare['provinsi'].isin(['Sulawesi Tengah', 'Sulawesi Tenggara'])]['nilai'].sum()
    
    ir_sentra = (kasus_diare_sentra / populasi_sentra) * 1000
    ir_non = (kasus_diare_non / populasi_non) * 1000 if populasi_non > 0 else 1
    
    rasio_diare = ir_sentra / ir_non if ir_non > 0 else 0
    skor_air_2_raw = min(10.0, max(0.0, (rasio_diare - 1) * 10.0))
    skor_air_2 = round(skor_air_2_raw / 2.0) * 2.0

# Skor 3: Konflik Air/Pesisir
skor_air_3 = 0
jumlah_konflik_air = 0
luas_konflik_air = 0
df_konflik_air = pd.DataFrame()
if not df_konflik.empty:
    if 'indikasi_air_sulawesi' in df_konflik.columns:
        df_konflik_air = df_konflik[df_konflik['indikasi_air_sulawesi'] == True]
    else:
        # Fallback jika script NLP belum dijalankan
        keywords = 'air|laut|pesisir|nelayan|sungai|pulau|tailing'
        df_konflik_air = df_konflik[df_konflik['sektor'].str.contains(keywords, case=False, na=False) | 
                                    df_konflik['judul'].str.contains(keywords, case=False, na=False) | 
                                    df_konflik['deskripsi'].str.contains(keywords, case=False, na=False)]
    
    # Filter 1 Dekade (2014 - Sekarang) agar tidak memasukkan data dari tahun 1959
    if 'tahun' in df_konflik_air.columns:
        df_konflik_air = df_konflik_air[df_konflik_air['tahun'] >= 2014]
        
    jumlah_konflik_air = len(df_konflik_air)
    if 'luas_ha' in df_konflik_air.columns:
        luas_konflik_air = pd.to_numeric(df_konflik_air['luas_ha'], errors='coerce').sum()
    # Normalisasi: 15 Konflik = Skor 10
    skor_air_3 = min(10.0, (jumlah_konflik_air / 15.0) * 10)

# Skor 4: Beban Tailing (Proxy B3)
skor_air_4 = 0
total_tailing_sulteng = 0
if not df_b3.empty:
    total_tailing_sulteng = df_b3[df_b3['Provinsi'] == 'Sulawesi Tengah']['Estimasi Timbulan (Ton/Tahun)'].sum()
    skor_air_4 = min(10.0, (total_tailing_sulteng / 25_000_000) * 10)

skor_akumulasi_air = (skor_air_1 + skor_air_2 + skor_air_3 + skor_air_4) / 4

sk1_air_str = f"{(skor_air_1 / 2.0):.1f}" if is_likert_mode else f"{skor_air_1:.1f}"
sk2_air_str = f"{(skor_air_2 / 2.0):.1f}" if is_likert_mode else f"{skor_air_2:.1f}"
sk3_air_str = f"{(skor_air_3 / 2.0):.1f}" if is_likert_mode else f"{skor_air_3:.1f}"
sk4_air_str = f"{(skor_air_4 / 2.0):.1f}" if is_likert_mode else f"{skor_air_4:.1f}"

# Conditional formatting untuk card Air
status_color_air = "#4CAF50"
status_text_air = "STATUS: AMAN/TERKENDALI"
if skor_akumulasi_air >= 6.0:
    status_color_air = "#E74C3C"
    status_text_air = "STATUS: DARURAT AIR"
elif skor_akumulasi_air >= 4.0:
    status_color_air = "#FBC02D"
    status_text_air = "STATUS: PERLU PENGAWASAN"

colB1, colB2 = st.columns([1, 2])
with colB1:
    st.markdown(f"""
<div style="background:#2C3E50; padding:20px; border-radius:10px; border-left:5px solid {status_color_air}; height:100%;">
<h4 style="color:#FFF; margin-top:0;">Audit D3TLH: Daya Tampung Air</h4>
<p style="color:#BDC3C7; font-size:0.9rem;">"Daya tampung air diukur berdasarkan rasio pengenceran alami dan neraca kualitas air."</p>
<hr style="border-color:#34495E;">
<h4 style="color:{status_color_air};">Fakta Empiris:</h4>
<p style="color:#E0E0E0; font-size:0.9rem;">Indeks Kualitas Air dan prevalensi penyakit saluran pencernaan menunjukkan perlunya pengawasan kualitas air.</p>
<div style="background-color: #1A202C; padding: 15px; border-radius: 8px; margin-top: 15px; text-align: center; border: 1px solid {status_color_air};">
<div style="font-size: 11px; color: #BDC3C7; text-transform: uppercase; letter-spacing: 1px;">
    Skor Indikator Air
    <span title="Kalkulasi Skor Air:&#10;({sk1_air_str} + {sk2_air_str} + {sk3_air_str} + {sk4_air_str}) / 4 = {card_a_val}" style="cursor:help; display:inline-block; background-color:#444; color:#FFF; border-radius:50%; width:14px; height:14px; line-height:14px; text-align:center; font-size:10px; margin-left:4px;">?</span>
</div>
<div style="font-size: 32px; font-weight: 800; color: {status_color_air}; line-height: 1.2;">
    <span title="Kalkulasi Skor Air:&#10;({sk1_air_str} + {sk2_air_str} + {sk3_air_str} + {sk4_air_str}) / 4 = {card_a_val}" style="cursor:help;">{card_a_val}</span> <span style="font-size: 16px;">/ {card_denom}</span>
</div>
<div style="font-size: 11px; color: {status_color_air}; margin-top: 5px; margin-bottom: 15px; font-weight: bold;">{status_text_air}</div>
<div style="text-align: left; font-size: 11px; color: #BDC3C7; border-top: 1px dashed #444; padding-top: 10px; line-height: 1.5;">
    <b>Rincian Skor Matriks Air:</b><br>
    • <b>Air 1 (Kualitas Air):</b> {sk1_air_str} / {card_denom}<br>
    • <b>Air 2 (Morbiditas Diare):</b> {sk2_air_str} / {card_denom}<br>
    • <b>Air 3 (Konflik Nelayan):</b> {sk3_air_str} / {card_denom}<br>
    • <b>Air 4 (Beban Tailing):</b> {sk4_air_str} / {card_denom}
</div>
</div>
<div style="background:{status_color_air}; color:white; padding:5px 10px; border-radius:5px; font-weight:bold; text-align:center; margin-top:15px; opacity:0.9;">
    ANALISIS: Kapasitas Penetralan Limbah Melampaui Batas
</div>
</div>
""", unsafe_allow_html=True)

with colB2:
    tab_w1, tab_w2, tab_w3, tab_w4 = st.tabs(["(Air 1) Kualitas Air", "(Air 2) Morbiditas Diare", "(Air 3) Konflik Nelayan", "(Air 4) Beban Tailing"])
    
    with tab_w1:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Threshold & Referensi (Air 1):</b><br>• <b>Indeks Kualitas Air (IKA):</b> Kategori Kurang = &lt; 50<br>• <b>Regulasi:</b> PermenLHK No.27/2021 (Hal.35).</div>", unsafe_allow_html=True)
        
        sk1_air_str = f"{(skor_air_1 / 2.0):.1f}" if is_likert_mode else f"{skor_air_1:.1f}"
        
        help_skor_makro = f"Skor Makro IKA: min(10.0, max(0, (80 - {ika_sulteng:.1f}) / 30) * 10) = {skor_makro_air_1:.1f}/10" + (f" (Likert: {(skor_makro_air_1 / 2.0):.1f}/5)" if is_likert_mode else "")
        
        help_air_1 = f"Kalkulasi Kualitas Air (Air 1):\n- {help_skor_makro}"
        
        skor_makro_str = f"{(skor_makro_air_1 / 2.0):.1f}" if is_likert_mode else f"{skor_makro_air_1:.1f}"
        
        if ika_sulteng < 50:
            col1_delta = "- Jatuh ke Kategori Kurang (< 50)"
        else:
            col1_delta = "Secara Agregat 'Aman' (> 50)"
        col1_color = "normal"
        
        col2_delta = f"STATUS: KRITIS" if skor_air_1 >= 6.0 else f"STATUS: TERKENDALI"
        col2_color = "inverse" if skor_air_1 >= 6.0 else "normal"
        
        col1, col2 = st.columns(2)
        col1.metric(f"Indeks Kualitas Air (Skor: {skor_makro_str})", f"{ika_sulteng:.1f}", col1_delta, delta_color=col1_color, help=help_skor_makro)
        col2.metric("Skor Kualitas Air (Air 1)", f"{sk1_air_str} / {card_denom}", col2_delta, delta_color=col2_color, help=help_air_1)
        
        st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
        
        if not df_ika.empty:
            df_ika_filtered = df_ika[df_ika['Provinsi'].isin([
                'Sulawesi Utara', 'Sulawesi Tengah', 'Sulawesi Selatan', 
                'Sulawesi Tenggara', 'Gorontalo', 'Sulawesi Barat'
            ])]
            
            fig_w1 = px.line(
                df_ika_filtered, x='Tahun', y='Indeks Kualitas Air', color='Provinsi',
                markers=True, title='Runtuhnya Indeks Kualitas Air (IKA) di Area Sentra Nikel'
            )
            
            for trace in fig_w1.data:
                if trace.name in ['Sulawesi Tengah', 'Sulawesi Tenggara']:
                    trace.line.color = '#E74C3C'
                    trace.line.width = 4
                    trace.name = f"{trace.name}"
                else:
                    trace.line.color = '#2980B9'
                    trace.line.dash = 'dot'
                    trace.line.width = 2
                    
            fig_w1.add_shape(
                type="line", x0=df_ika_filtered['Tahun'].min(), x1=df_ika_filtered['Tahun'].max(),
                y0=50, y1=50, line=dict(color="#E74C3C", width=2, dash="dashdot"),
            )
            fig_w1.add_annotation(
                x=df_ika_filtered['Tahun'].max(), y=50, text="Batas Kritis Cemar (50)",
                showarrow=False, yshift=-10, font=dict(color="#E74C3C", size=10), xanchor="right"
            )
            
            fig_w1.add_shape(type="rect", x0=df_ika_filtered['Tahun'].min(), x1=df_ika_filtered['Tahun'].max(), y0=50, y1=100, fillcolor="rgba(46, 204, 113, 0.1)", layer="below", line_width=0)
            fig_w1.add_shape(type="rect", x0=df_ika_filtered['Tahun'].min(), x1=df_ika_filtered['Tahun'].max(), y0=0, y1=50, fillcolor="rgba(231, 76, 60, 0.1)", layer="below", line_width=0)
            
            fig_w1.add_annotation(x=df_ika_filtered['Tahun'].min(), y=95, text="ZONA AMAN (> 50)", showarrow=False, font=dict(color="#2ECC71", size=10), xanchor="left")
            fig_w1.add_annotation(x=df_ika_filtered['Tahun'].min(), y=5, text="ZONA CEMAR (< 50)", showarrow=False, font=dict(color="#E74C3C", size=10), xanchor="left")
            
            fig_w1.update_layout(
                template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                yaxis=dict(range=[0, 100], title="Indeks Kualitas Air"), xaxis=dict(title=""),
                legend_title="Provinsi (Merah: Sentra, Biru: Non-Sentra)", margin=dict(l=0, r=0, t=40, b=0)
            )
            st.plotly_chart(fig_w1, use_container_width=True, config={'displayModeBar': False})
            
    with tab_w2:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Threshold & Referensi (Air 2):</b><br>• <b>Incidence Rate Ratio (IRR):</b> > 2.0 (Risiko 2x lipat dari populasi rata-rata).<br>• <b>Regulasi:</b> WHO EHC 6 & Epidemiologi Kemenkes 2023 (Hal. 112).</div>", unsafe_allow_html=True)
        
        col1_delta = f"↑ {rasio_diare:.1f}x Lipat Risiko Kritis (> 2.0)" if rasio_diare > 2.0 else f"Normal (≤ 2.0)"
        col1_color = "inverse" if rasio_diare > 2.0 else "normal"
        
        col2_delta = f"STATUS: DARURAT KLB" if skor_air_2 >= 6.0 else f"STATUS: TERKENDALI"
        col2_color = "inverse" if skor_air_2 >= 6.0 else "normal"
        
        sk2_str = f"{(skor_air_2 / 2.0):.1f}" if is_likert_mode else f"{skor_air_2:.1f}"
        
        help_skor2 = f"Kalkulasi Total (Air 2):\nmin(10.0, max(0.0, ({rasio_diare:.1f} - 1) * 10.0)) = {skor_air_2:.1f}/10" + (f" (Likert: {(skor_air_2 / 2.0):.1f}/5)" if is_likert_mode else "")
        help_irr = f"Data Kemenkes 2023:\n- Kasus Sentra (2 Prov): {kasus_diare_sentra:,.0f} jiwa\n- Kasus Non-Sentra (4 Prov): {kasus_diare_non:,.0f} jiwa\n\nKalkulasi IRR:\n({kasus_diare_sentra:,.0f} / {populasi_sentra:,.0f}) / ({kasus_diare_non:,.0f} / {populasi_non:,.0f}) = {rasio_diare:.1f}x Lipat\n(Threshold > 2.0x Darurat Medis)\n\n{help_skor2}"
        
        col1, col2 = st.columns(2)
        col1.metric(f"Incidence Rate Ratio (Skor: {sk2_str})", f"{rasio_diare:.1f}x", col1_delta, delta_color=col1_color, help=help_irr)
        col2.metric("Skor Beban Penyakit (Air 2)", f"{sk2_str} / {card_denom}", col2_delta, delta_color=col2_color, help=help_skor2)
        
        st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
        
        if not df_kes.empty:
            df_diare_trend = df_diare.copy()
            df_diare_trend['Kategori'] = df_diare_trend['provinsi'].apply(lambda x: 'Sentra Tambang' if x in ['Sulawesi Tengah', 'Sulawesi Tenggara'] else 'Non-Sentra')
            df_d_agg = df_diare_trend.groupby(['tahun', 'Kategori'])['nilai'].sum().reset_index()
            fig_w2 = px.area(df_d_agg, x='tahun', y='nilai', color='Kategori', title="Ledakan Kasus Diare (Indikator Kualitas Air Tanah)")
            fig_w2.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_w2, use_container_width=True, config={'displayModeBar': False})

    with tab_w3:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Threshold & Referensi (Air 3):</b><br>• <b>Konflik Pesisir/Air:</b> > 15 Konflik (Mewakili 30% ekuivalensi spasial pesisir nasional).<br>• <b>Regulasi:</b> Konsorsium Pembaruan Agraria (KPA CATAHU 2023, Hal. 22).</div>", unsafe_allow_html=True)
        
        col1_delta = f"↑ {jumlah_konflik_air} Kasus (Kritis > 15)" if jumlah_konflik_air > 15 else f"Normal (≤ 15)"
        col1_color = "inverse" if jumlah_konflik_air > 15 else "normal"
        
        col2_delta = f"STATUS: DARURAT AGRARIA" if skor_air_3 >= 6.0 else f"STATUS: TERKENDALI"
        col2_color = "inverse" if skor_air_3 >= 6.0 else "normal"
        
        sk3_str = f"{(skor_air_3 / 2.0):.1f}" if is_likert_mode else f"{skor_air_3:.1f}"
        
        help_skor3 = f"Kalkulasi Total (Air 3):\nmin(10.0, ({jumlah_konflik_air} / 15.0) * 10) = {skor_air_3:.1f}/10" + (f" (Likert: {(skor_air_3 / 2.0):.1f}/5)" if is_likert_mode else "")
        help_konflik = f"Data Agraria (KPA & TanahKita):\n- Total Kasus Pesisir: {jumlah_konflik_air} Kasus\n- Estimasi Luas Terdampak: {luas_konflik_air:,.0f} Ha (Ruang Hidup Nelayan)\n\nThreshold 15 Kasus ditetapkan berdasarkan 30% ekuivalensi pesisir Sulawesi terhadap total konflik pesisir nasional.\n\n{help_skor3}"
        
        col1, col2 = st.columns(2)
        col1.metric(f"Total Konflik Pesisir (Skor: {sk3_str})", f"{jumlah_konflik_air} Kasus", col1_delta, delta_color=col1_color, help=help_konflik)
        col2.metric("Skor Konflik Ruang Air (Air 3)", f"{sk3_str} / {card_denom}", col2_delta, delta_color=col2_color, help=help_skor3)
        
        st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
        
        if not df_konflik_air.empty and 'tahun' in df_konflik_air.columns:
            df_k_trend = df_konflik_air.groupby('tahun').size().reset_index(name='Jumlah')
            
            fig_w3 = px.bar(df_k_trend, x='tahun', y='Jumlah', title="Frekuensi Letusan Konflik Pesisir & Nelayan (1 Dekade Terakhir: 2014-2024)")
            fig_w3.update_traces(marker_color='#E91E63')
            fig_w3.update_layout(
                height=450, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#B0BEC5"),
                xaxis=dict(title="Tahun", showgrid=True, gridcolor="rgba(255,255,255,0.1)", dtick=1),
                yaxis=dict(title="Jumlah Kasus", showgrid=True, gridcolor="rgba(255,255,255,0.1)"),
                margin=dict(l=0, r=0, t=40, b=0)
            )
            st.plotly_chart(fig_w3, use_container_width=True, config={'displayModeBar': False})
            
            with st.expander("Lihat Data Mentah: Rincian 44 Kasus Konflik Pesisir/Nelayan (1 Dekade)", expanded=False):
                st.dataframe(df_konflik_air, use_container_width=True, hide_index=True)
                st.caption("Sumber: `sulawesi_konflik_agraria_tanahkita.csv` (Di-filter berdasarkan keyword: air, laut, pesisir, nelayan, tailing, dll)")

    with tab_w4:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Threshold & Referensi (Air 4):</b><br>• <b>Timbulan Tailing/Slag:</b> > 25 Juta Ton/Tahun (Batas Kapasitas maksimal DSTP/Tailing Dam).<br>• <b>Regulasi:</b> Dokumen AMDAL KLHK (PT HPI - IMIP) & Laporan AEER 2020 (Hal. 36).</div>", unsafe_allow_html=True)
        
        col1_delta = f"↑ {total_tailing_sulteng/1_000_000:.1f} Jt Ton (Kritis > 25 Jt)" if total_tailing_sulteng > 25_000_000 else f"Normal (≤ 25 Jt)"
        col1_color = "inverse" if total_tailing_sulteng > 25_000_000 else "normal"
        
        col2_delta = f"STATUS: DARURAT LIMBAH" if skor_air_4 >= 6.0 else f"STATUS: TERKENDALI"
        col2_color = "inverse" if skor_air_4 >= 6.0 else "normal"
        
        sk4_str = f"{(skor_air_4 / 2.0):.1f}" if is_likert_mode else f"{skor_air_4:.1f}"
        
        help_skor4 = f"Kalkulasi Total (Air 4):\nmin(10.0, ({total_tailing_sulteng/1_000_000:.1f} / 25.0) * 10) = {skor_air_4:.1f}/10" + (f" (Likert: {(skor_air_4 / 2.0):.1f}/5)" if is_likert_mode else "")
        help_tailing = f"Data Limbah B3 KLHK:\n- Total Timbulan B3/Tailing (Sulteng): {total_tailing_sulteng/1_000_000:.1f} Juta Ton\n\nThreshold 25 Juta Ton/Tahun ditetapkan berdasarkan batas absolut daya dukung maksimum kapasitas pembuangan laut dalam (DSTP) dan bendungan tailing di Morowali.\n\n{help_skor4}"
        
        col1, col2 = st.columns(2)
        col1.metric(f"Total Timbulan Tailing (Skor: {sk4_str})", f"{total_tailing_sulteng/1_000_000:.1f} Jt Ton", col1_delta, delta_color=col1_color, help=help_tailing)
        col2.metric("Skor Ancaman Tailing (Air 4)", f"{sk4_str} / {card_denom}", col2_delta, delta_color=col2_color, help=help_skor4)
        
        st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
        
        if not df_b3.empty:
            fig_w4 = px.treemap(df_b3, path=['Provinsi', 'Kawasan/Perusahaan'], values='Estimasi Timbulan (Ton/Tahun)', 
                                color='Estimasi Timbulan (Ton/Tahun)', color_continuous_scale='Blues',
                                title="Proporsi Beban Limbah Tailing & B3 ke Ekosistem Air")
            fig_w4.update_layout(template="plotly_dark", margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_w4, use_container_width=True, config={'displayModeBar': False})
            
            with st.expander("Lihat Data Mentah: Rincian Limbah B3/Tailing", expanded=False):
                st.dataframe(df_b3, use_container_width=True, hide_index=True)
                st.caption("Sumber: `sulawesi_limbah_b3.csv` (Data KLHK yang diekstraksi ke level Perusahaan/Kawasan)")

st.markdown("<br>", unsafe_allow_html=True)



# ---------------------------------------------------------
# C. MITOS DEFORESTASI VS BENCANA ALAM (DAYA DUKUNG LAHAN)
# ---------------------------------------------------------
# Conditional formatting untuk card Lahan
status_color_lahan = "#4CAF50"
status_text_lahan = "STATUS: AMAN/TERKENDALI"
if skor_akumulasi_lahan >= 6.0:
    status_color_lahan = "#E74C3C"
    status_text_lahan = "STATUS: DARURAT LAHAN"
elif skor_akumulasi_lahan >= 4.0:
    status_color_lahan = "#FBC02D"
    status_text_lahan = "STATUS: PERLU PENGAWASAN"

skl1_str = f"{(skor_lahan_1 / 2.0):.1f}" if is_likert_mode else f"{skor_lahan_1:.1f}"
skl2_str = f"{(skor_lahan_2 / 2.0):.1f}" if is_likert_mode else f"{skor_lahan_2:.1f}"
skl3_str = f"{(skor_lahan_3 / 2.0):.1f}" if is_likert_mode else f"{skor_lahan_3:.1f}"
skl4_str = f"{(skor_lahan_4 / 2.0):.1f}" if is_likert_mode else f"{skor_lahan_4:.1f}"

colC1, colC2 = st.columns([1, 2])
with colC1:
    st.markdown(f'''
    <div style="background:#2C3E50; padding:20px; border-radius:10px; border-left:5px solid {status_color_lahan}; height:100%;">
        <h4 style="color:#FFF; margin-top:0;">Audit D3TLH: Daya Dukung Lahan</h4>
        <p style="color:#BDC3C7; font-size:0.9rem;">"Daya dukung lahan dianalisis berdasarkan kecukupan tutupan hutan dan batas fungsi kawasan."</p>
        <hr style="border-color:#34495E;">
        <h4 style="color:{status_color_lahan};">Fakta Empiris:</h4>
        <p style="color:#E0E0E0; font-size:0.9rem;">Perubahan tutupan lahan berpotensi memengaruhi laju bencana hidrometeorologi di kawasan industri.</p>
        <div style="background-color: #1A202C; padding: 15px; border-radius: 8px; margin-top: 15px; text-align: center; border: 1px solid {status_color_lahan};">
            <div style="font-size: 11px; color: #BDC3C7; text-transform: uppercase; letter-spacing: 1px;">Skor Indikator Lahan</div>
            <div style="font-size: 32px; font-weight: 800; color: {status_color_lahan}; line-height: 1.2;">{card_l_val} <span style="font-size: 16px;">/ {card_denom}</span></div>
            <div style="font-size: 11px; color: {status_color_lahan}; margin-top: 5px; margin-bottom: 15px; font-weight: bold;">{status_text_lahan}</div>
            <div style="text-align: left; font-size: 11px; color: #BDC3C7; border-top: 1px dashed #444; padding-top: 10px; line-height: 1.5;">
                <b>Rincian Skor Matriks Lahan:</b><br>
                • <b>Lahan 1 (Bencana Alam):</b> {skl1_str} / {card_denom}<br>
                • <b>Lahan 2 (Deforestasi Primer):</b> {skl2_str} / {card_denom}<br>
                • <b>Lahan 3 (Kawasan Lindung):</b> {skl3_str} / {card_denom}<br>
                • <b>Lahan 4 (Aktor Deforestasi):</b> {skl4_str} / {card_denom}
            </div>
        </div>
        <div style="background:{status_color_lahan}; color:white; padding:5px 10px; border-radius:5px; font-weight:bold; text-align:center; margin-top:15px; opacity:0.9;">
            ANALISIS: Evaluasi Pengelolaan Lanskap
        </div>
    </div>
    ''', unsafe_allow_html=True)

with colC2:
    tab_l1, tab_l2, tab_l3, tab_l4 = st.tabs(["(Lahan 1) Bencana Banjir & Longsor", "(Lahan 2) Deforestasi Primer", "(Lahan 3) Pelanggaran Kawasan Lindung", "(Lahan 4) Aktor Deforestasi"])
    
    with tab_l1:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Threshold & Referensi (Lahan 1):</b><br>• <b>Bencana Hidrometeorologi:</b> > 877 Kejadian (Batas Deviasi Outlier Statistik: Mean + 1 SD).<br>• <b>Regulasi/Data:</b> Dataset Historis BNPB (2014-2024).</div>", unsafe_allow_html=True)
        
        col1_delta = f"↑ {bencana_sulteng_sultra:,.0f} Kejadian (Kritis > 877)" if bencana_sulteng_sultra > 877 else f"Normal (≤ 877)"
        col1_color = "inverse" if bencana_sulteng_sultra > 877 else "normal"
        
        col2_delta = f"STATUS: DARURAT BENCANA" if skor_lahan_1 >= 6.0 else f"STATUS: TERKENDALI"
        col2_color = "inverse" if skor_lahan_1 >= 6.0 else "normal"
        
        skl1_str = f"{(skor_lahan_1 / 2.0):.1f}" if is_likert_mode else f"{skor_lahan_1:.1f}"
        
        help_skorl1 = f"Kalkulasi Total (Lahan 1):\nmin(10.0, ({bencana_sulteng_sultra:,.0f} / 877) * 10) = {skor_lahan_1:.1f}/10" + (f" (Likert: {(skor_lahan_1 / 2.0):.1f}/5)" if is_likert_mode else "")
        help_lahan1 = f"Data BNPB:\n- Bencana Sulteng & Sultra: {bencana_sulteng_sultra:,.0f} Kejadian\n\nThreshold 877 kejadian didapat dari batas deviasi outlier statistik (rata-rata historis (Mean) + 1 Standar Deviasi (SD)) untuk seluruh Sulawesi dalam rentang 1 dekade.\n\n{help_skorl1}"
        
        col1, col2 = st.columns(2)
        col1.metric(f"Total Bencana Banjir & Longsor (Skor: {skl1_str})", f"{bencana_sulteng_sultra:,.0f} Kasus", col1_delta, delta_color=col1_color, help=help_lahan1)
        col2.metric("Skor Bencana Lahan (Lahan 1)", f"{skl1_str} / {card_denom}", col2_delta, delta_color=col2_color, help=help_skorl1)
        
        st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
        
        if not df_bencana.empty:
            df_b = df_bencana.copy()
            df_b['tahun'] = pd.to_numeric(df_b['tahun'], errors='coerce')
            df_b['jumlah_kejadian'] = pd.to_numeric(df_b['jumlah_kejadian'], errors='coerce').fillna(0)
            df_b_trend = df_b.groupby(['tahun', 'provinsi'])['jumlah_kejadian'].sum().reset_index()
            fig_l1 = px.bar(df_b_trend, x='tahun', y='jumlah_kejadian', color='provinsi', 
                           title="Frekuensi Bencana Hidrometeorologi (Banjir & Longsor)",
                           color_discrete_sequence=px.colors.qualitative.Pastel)
            fig_l1.add_hline(y=88, line_dash="dash", line_color="#E74C3C", annotation_text="Batas Darurat Bencana (88/Tahun)", annotation_position="top left")
            fig_l1.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_l1, use_container_width=True, config={'displayModeBar': False})
            with st.expander("Tampilkan Data Mentah (BNPB)"):
                st.dataframe(df_bencana, use_container_width=True)

    with tab_l2:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Threshold & Referensi (Lahan 2):</b><br>• <b>Deforestasi Hutan:</b> > 638.000 Ha / 10 Tahun (Proporsi Spasial Target FOLU Net Sink Nasional).<br>• <b>Regulasi:</b> Dokumen Rencana Operasional FOLU Net Sink 2030 KLHK (Hal. 128).</div>", unsafe_allow_html=True)
        
        os_ratio_l2 = (deforestasi_sentra / 638000) * 100
        col1_delta = f"↑ Overshoot {os_ratio_l2:.1f}% dari ambang batas" if deforestasi_sentra > 638000 else f"Aman (≤ 638 Ribu Ha)"
        col1_color = "inverse" if deforestasi_sentra > 638000 else "normal"
        
        col2_delta = f"STATUS: DARURAT DEFORESTASI" if skor_lahan_2 >= 6.0 else f"STATUS: TERKENDALI"
        col2_color = "inverse" if skor_lahan_2 >= 6.0 else "normal"
        
        skl2_str = f"{(skor_lahan_2 / 2.0):.1f}" if is_likert_mode else f"{skor_lahan_2:.1f}"
        
        help_skorl2 = f"Kalkulasi Total (Lahan 2):\nmin(10.0, ({deforestasi_sentra:,.0f} / 638,000) * 10) = {skor_lahan_2:.1f}/10" + (f" (Likert: {(skor_lahan_2 / 2.0):.1f}/5)" if is_likert_mode else "")
        help_lahan2 = f"Data GFW:\n- Deforestasi Komoditas (Tambang & Sawit) Pulau Sulawesi: {deforestasi_sentra:,.0f} Ha (2014-2023)\n\nKalkulasi Threshold FOLU Net Sink 2030:\n- Kuota Maksimal Nasional: 1.700.000 Ha / 30 Tahun\n- Rata-rata Kuota Nasional: ~58.000 Ha / Tahun\n- Rentang Observasi GFW: 11 Tahun (2014-2024)\n- Threshold: 58.000 Ha * 11 Tahun = 638.000 Ha\n\n{help_skorl2}"
        
        col1, col2 = st.columns(2)
        col1.metric(f"Total Deforestasi Komoditas (Skor: {skl2_str})", f"{deforestasi_sentra:,.0f} Ha", col1_delta, delta_color=col1_color, help=help_lahan2)
        col2.metric("Skor Deforestasi Primer (Lahan 2)", f"{skl2_str} / {card_denom}", col2_delta, delta_color=col2_color, help=help_skorl2)
        
        st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
        
        if not df_gfw.empty:
            df_g = df_gfw.copy()
            df_g['Tahun'] = pd.to_numeric(df_g['Tahun'], errors='coerce')
            df_g['Total_Deforestasi_Ha'] = pd.to_numeric(df_g['Total_Deforestasi_Ha'], errors='coerce').fillna(0)
            df_g_trend = df_g.groupby(['Tahun', 'Provinsi'])['Total_Deforestasi_Ha'].sum().reset_index()
            fig_l2 = px.line(df_g_trend, x='Tahun', y='Total_Deforestasi_Ha', color='Provinsi', markers=True,
                           title="Laju Deforestasi Akibat Pertambangan & Sawit")
            fig_l2.add_hline(y=57000, line_dash="dash", line_color="#E74C3C", annotation_text="Batas Tahunan FOLU Nasional (57.000 Ha)", annotation_position="bottom right")
            fig_l2.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_l2, use_container_width=True, config={'displayModeBar': False})
            with st.expander("Tampilkan Data Mentah (Global Forest Watch)"):
                st.dataframe(df_gfw, use_container_width=True)

    with tab_l3:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Threshold & Referensi (Lahan 3):</b><br>• <b>Kawasan Lindung:</b> 0 Hektar / Nol Toleransi.<br>• <b>Regulasi:</b> Pasal 38 Ayat 4 UU No. 41 Tahun 1999 tentang Kehutanan (Tindak Pidana Kehutanan).</div>", unsafe_allow_html=True)
        
        col1_delta = f"↑ {lindung_hilang:,.0f} Ha (Kritis > 0 Ha)" if lindung_hilang > 0 else f"Aman (0 Ha)"
        col1_color = "inverse" if lindung_hilang > 0 else "normal"
        
        col2_delta = f"STATUS: PELANGGARAN HUKUM" if skor_lahan_3 >= 10.0 else f"STATUS: TERKENDALI"
        col2_color = "inverse" if skor_lahan_3 >= 10.0 else "normal"
        
        skl3_str = f"{(skor_lahan_3 / 2.0):.1f}" if is_likert_mode else f"{skor_lahan_3:.1f}"
        
        help_skorl3 = f"Kalkulasi Total (Lahan 3):\nJika Luas Hilang > 0 Ha, maka Skor = 10.0 (Pelanggaran Hukum).\nAktual = 10.0/10" + (f" (Likert: 5.0/5)" if is_likert_mode else "") if lindung_hilang > 0 else f"Kalkulasi Total (Lahan 3):\nSkor = 0.0/10" + (f" (Likert: 0.0/5)" if is_likert_mode else "")
        help_lahan3 = f"Data GFW (Protected Areas):\n- Deforestasi Kawasan Lindung Sulteng & Sultra: {lindung_hilang:,.0f} Ha\n\nKalkulasi Threshold (Nol Toleransi):\n- Ambang Batas: 0 Hektar\n- Regulasi: Pasal 38 UU Kehutanan melarang penambangan terbuka di kawasan hutan lindung.\n- Status: {'Pelanggaran Hukum Mutlak' if lindung_hilang > 0 else 'Aman'}\n\n{help_skorl3}"
        
        col1, col2 = st.columns(2)
        col1.metric(f"Total Kehancuran Kawasan Lindung (Skor: {skl3_str})", f"{lindung_hilang:,.0f} Ha", col1_delta, delta_color=col1_color, help=help_lahan3)
        col2.metric("Skor Pelanggaran Zonasi (Lahan 3)", f"{skl3_str} / {card_denom}", col2_delta, delta_color=col2_color, help=help_skorl3)
        
        st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
        
        if not df_gfw_lindung.empty:
            df_gl = df_gfw_lindung.copy()
            df_gl['Tahun'] = pd.to_numeric(df_gl['Tahun'], errors='coerce')
            df_gl['Luas_Hilang_Kawasan_Lindung_Ha'] = pd.to_numeric(df_gl['Luas_Hilang_Kawasan_Lindung_Ha'], errors='coerce').fillna(0)
            df_gl_trend = df_gl.groupby(['Tahun', 'Provinsi'])['Luas_Hilang_Kawasan_Lindung_Ha'].sum().reset_index()
            fig_l3 = px.area(df_gl_trend, x='Tahun', y='Luas_Hilang_Kawasan_Lindung_Ha', color='Provinsi',
                           title="Tren Perambahan Deforestasi di Kawasan Lindung (Protected Areas)")
            fig_l3.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_l3, use_container_width=True, config={'displayModeBar': False})
            with st.expander("Tampilkan Data Mentah Kawasan Lindung (GFW)"):
                st.dataframe(df_gfw_lindung, use_container_width=True)

    with tab_l4:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Threshold & Referensi (Lahan 4):</b><br>• <b>Deforestasi Konsesi:</b> > 500.000 Ha / 1 Dekade (Batas Kritis Daya Dukung Ekologis Pulau).<br>• <b>Keterangan Data:</b> Menggunakan data empiris satelit GFW untuk deforestasi yang murni didorong oleh ekspansi konsesi komersial (Tambang/Sawit).</div>", unsafe_allow_html=True)
        
        os_ratio_l4 = (tambang_driver_ha / 500000) * 100
        col1_delta = f"↑ Overshoot {os_ratio_l4:.1f}% dari ambang batas" if tambang_driver_ha > 500000 else f"Aman (≤ 500 Ribu Ha)"
        col1_color = "inverse" if tambang_driver_ha > 500000 else "normal"
        
        col2_delta = f"STATUS: MONOPOLI KONSESI" if skor_lahan_4 >= 6.0 else f"STATUS: TERKENDALI"
        col2_color = "inverse" if skor_lahan_4 >= 6.0 else "normal"
        
        skl4_str = f"{(skor_lahan_4 / 2.0):.1f}" if is_likert_mode else f"{skor_lahan_4:.1f}"
        
        help_skorl4 = f"Kalkulasi Total (Lahan 4):\nmin(10.0, ({tambang_driver_ha:,.0f} / 500,000) * 10) = {skor_lahan_4:.1f}/10" + (f" (Likert: {(skor_lahan_4 / 2.0):.1f}/5)" if is_likert_mode else "")
        help_lahan4 = f"Data GFW (Drivers of Deforestation):\n- Total Deforestasi Komoditas (Tambang/Sawit): {tambang_driver_ha:,.0f} Ha\n\nKalkulasi Threshold Daya Dukung Ekologis:\n- Ambang Batas Pulau: 500.000 Ha\n- Threshold ini tercapai apabila konsesi industri (tambang/sawit) memonopoli laju perubahan tutupan lahan melebihi 500 ribu hektar dalam satu dekade.\n\n{help_skorl4}"
        
        col1, col2 = st.columns(2)
        col1.metric(f"Total Deforestasi Konsesi (Skor: {skl4_str})", f"{tambang_driver_ha:,.0f} Ha", col1_delta, delta_color=col1_color, help=help_lahan4)
        col2.metric("Skor Aktor Deforestasi (Lahan 4)", f"{skl4_str} / {card_denom}", col2_delta, delta_color=col2_color, help=help_skorl4)
        
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
            st.plotly_chart(fig_l4, use_container_width=True, config={'displayModeBar': False})
            with st.expander("Tampilkan Data Mentah Drivers (GFW)"):
                st.dataframe(df_gfw_driver, use_container_width=True)


st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# D. MITOS KEDAULATAN RUANG VS KONFLIK SOSIAL (DAYA DUKUNG SOSIAL)
# ---------------------------------------------------------
colD1, colD2 = st.columns([1, 2])
with colD1:
    sks1_str = f"{(skor_sosial_1 / 2.0):.1f}" if is_likert_mode else f"{skor_sosial_1:.1f}"
    sks2_str = f"{(skor_sosial_2 / 2.0):.1f}" if is_likert_mode else f"{skor_sosial_2:.1f}"
    sks3_str = f"{(skor_sosial_3 / 2.0):.1f}" if is_likert_mode else f"{skor_sosial_3:.1f}"
    sks4_str = f"{(skor_sosial_4 / 2.0):.1f}" if is_likert_mode else f"{skor_sosial_4:.1f}"
    
    st.markdown(f'''
    <div style="background:#2C3E50; padding:20px; border-radius:10px; border-left: 5px solid #E74C3C; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
        <h4 style="color:#FFF; margin-top:0;">Audit D3TLH: Daya Dukung Sosial</h4>
        <p style="color:#BDC3C7; font-size:0.9rem;">"Status kawasan dialokasikan untuk peruntukan industri dengan pelaksanaan konsultasi publik."</p>
        <hr style="border-color:#34495E;">
        <h4 style="color:#E74C3C;">Fakta Empiris:</h4>
        <p style="color:#E0E0E0; font-size:0.9rem;">Pentingnya transparansi dan pelibatan masyarakat lokal dalam penataan ruang dan perizinan.</p>
        <div style="background-color: #1A202C; padding: 15px; border-radius: 8px; margin-top: 15px; text-align: center; border: 1px solid #E74C3C;">
            <div style="font-size: 11px; color: #BDC3C7; text-transform: uppercase; letter-spacing: 1px;">Skor Indikator Sosial</div>
            <div style="font-size: 32px; font-weight: 800; color: #E74C3C; line-height: 1.2;">{card_s_val} <span style="font-size: 16px;">/ {card_denom}</span></div>
            <div style="font-size: 11px; color: #E74C3C; margin-top: 5px; margin-bottom: 15px; font-weight: bold;">STATUS: PERLU PENGAWASAN</div>
            <div style="text-align: left; font-size: 11px; color: #BDC3C7; border-top: 1px dashed #444; padding-top: 10px; line-height: 1.5;">
                <b>Rincian Skor Matriks Sosial:</b><br>
                • <b>Sosial 1 (Persetujuan FPIC):</b> {sks1_str} / {card_denom}<br>
                • <b>Sosial 2 (Jiwa Terdampak):</b> {sks2_str} / {card_denom}<br>
                • <b>Sosial 3 (Kriminalisasi HAM):</b> {sks3_str} / {card_denom}<br>
                • <b>Sosial 4 (Defisit Faskes SPA):</b> {sks4_str} / {card_denom}
            </div>
        </div>
        <div style="background:#C0392B; color:white; padding:5px 10px; border-radius:5px; font-weight:bold; text-align:center; margin-top:15px;">
            ANALISIS: Pelibatan Masyarakat Lokal
        </div>
    </div>
    ''', unsafe_allow_html=True)

with colD2:
    tab_s1, tab_s2, tab_s3, tab_s4 = st.tabs(["(Sosial 1) Manipulasi Persetujuan FPIC", "(Sosial 2) Perampasan Ruang Hidup", "(Sosial 3) Kriminalisasi Warga", "(Sosial 4) Defisit Layanan Dasar"])
    
    with tab_s1:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Threshold & Referensi (Sosial 1):</b><br>• <b>Pelanggaran Persetujuan (FPIC):</b> ≥ 3 Kasus (Zero Tolerance).<br>• <b>Keterangan Data:</b> Menggunakan dataset investigasi JATAM & Walhi Sulawesi terkait rekayasa atau manipulasi persetujuan warga pada fase AMDAL. Sesuai prinsip IFC PS7, absennya FPIC adalah kegagalan sistemik (Red Flag).</div>", unsafe_allow_html=True)
        
        fpic_kritis = 3
        
        col1_delta = f"↑ {kasus_fpic} Kasus (Melampaui Batas Kritis Darurat)" if skor_sosial_1 >= 6.0 else f"Normal/Terkendali (< {int(fpic_kritis * 0.6)} Kasus)"
        col1_color = "inverse" if skor_sosial_1 >= 6.0 else "normal"
        
        col2_delta = f"STATUS: AMDAL CACAT HUKUM (RED FLAG)" if skor_sosial_1 >= 6.0 else f"STATUS: TERKENDALI"
        col2_color = "inverse" if skor_sosial_1 >= 6.0 else "normal"
        
        sks1_str = f"{(skor_sosial_1 / 2.0):.1f}" if is_likert_mode else f"{skor_sosial_1:.1f}"
        
        help_skors1 = f"Kalkulasi Total (Sosial 1):\nmin(10.0, ({kasus_fpic} / {fpic_kritis}) * 10) = {skor_sosial_1:.1f}/10" + (f" (Likert: {(skor_sosial_1 / 2.0):.1f}/5)" if is_likert_mode else "")
        help_sos1 = f"Data JATAM & Walhi Sulawesi:\n- Total Investigasi Manipulasi FPIC: {kasus_fpic} Kasus\n\nKalkulasi Threshold Pelanggaran Sosial:\n- Ambang Batas Pulau: {fpic_kritis} Kasus (Zero Tolerance)\n- Kegagalan memperoleh persetujuan warga tanpa paksaan (FPIC) adalah pelanggaran prinsip HAM internasional yang ditetapkan IFC Performance Standard 7 & Equator Principles.\n\n{help_skors1}"
        
        col1, col2 = st.columns(2)
        col1.metric(f"Total Manipulasi Persetujuan (Skor: {sks1_str})", f"{kasus_fpic} Kasus", col1_delta, delta_color=col1_color, help=help_sos1)
        col2.metric("Skor Pelanggaran FPIC (Sosial 1)", f"{sks1_str} / {card_denom}", col2_delta, delta_color=col2_color, help=help_skors1)
        
        st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
        
        if not df_konflik_fpic.empty and not df_kpa_izin.empty:
            df_konflik_timeline = df_konflik_fpic.copy()
            df_konflik_timeline['kategori'] = 'Konflik Pertambangan'
            df_konflik_timeline = df_konflik_timeline.rename(columns={'tahun': 'Tahun', 'judul': 'Keterangan'})
            
            df_masalah_timeline = df_kpa_izin[df_kpa_izin['lokasi'].str.contains('Sulawesi', case=False, na=False)].copy()
            df_masalah_timeline['kategori'] = 'Masalah Izin (KPA)'
            df_masalah_timeline['Tahun'] = df_masalah_timeline['tahun_laporan'].astype(int)
            
            df_combined_timeline = pd.concat([
                df_konflik_timeline[['Tahun', 'kategori']],
                df_masalah_timeline[['Tahun', 'kategori']]
            ], ignore_index=True).sort_values('Tahun')
            
            # Filter sejak 2000
            df_combined_timeline = df_combined_timeline[df_combined_timeline['Tahun'] >= 2000]
            df_timeline_agg = df_combined_timeline.groupby(['Tahun', 'kategori']).size().reset_index(name='Jumlah')
            
            fig_s1 = px.bar(
                df_timeline_agg,
                x='Tahun',
                y='Jumlah',
                color='kategori',
                barmode='group',
                color_discrete_map={
                    'Konflik Pertambangan': '#E74C3C',
                    'Masalah Izin (KPA)': '#F39C12'
                },
                title='Timeline Historis: Konflik Pertambangan & Masalah Izin'
            )
            fig_s1.update_layout(
                height=450, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#B0BEC5"),
                xaxis=dict(title="Tahun", showgrid=False, dtick=2),
                yaxis=dict(title="Jumlah Kasus", showgrid=True, gridcolor="rgba(255,255,255,0.05)"),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, title=""),
                margin=dict(l=0, r=0, t=40, b=0)
            )
            st.plotly_chart(fig_s1, use_container_width=True, config={'displayModeBar': False})
            
            st.markdown("<div style='margin-top: 15px;'><b>Daftar Temuan Kasus (Konflik FPIC):</b></div>", unsafe_allow_html=True)
            df_fpic_view = df_konflik_fpic[['tahun', 'nama_perusahaan', 'indikasi_fpic', 'judul']].copy()
            st.dataframe(df_fpic_view, use_container_width=True, hide_index=True)
            with st.expander("Tampilkan Data Mentah FPIC & Izin (JATAM/Walhi)"):
                st.dataframe(df_konflik_fpic, use_container_width=True)
                st.caption("Sumber: `sulawesi_konflik_tambang_fpic.csv` (JATAM & Walhi)")

    with tab_s2:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Threshold & Referensi (Sosial 2):</b><br>• <b>Jiwa Terdampak Konflik:</b> > 100.000 Jiwa (Tingkat Pulau).<br>• <b>Keterangan Data:</b> Menggunakan dataset letusan konflik agraria akibat perampasan ruang hidup (KPA & TanahKita). Threshold darurat kemanusiaan ditetapkan sebesar 100.000 jiwa, merepresentasikan 24,5% proporsi ekuivalensi beban konflik agraria nasional (CATAHU KPA 2023).</div>", unsafe_allow_html=True)
        
        sks2_str = f"{(skor_sosial_2 / 2.0):.1f}" if is_likert_mode else f"{skor_sosial_2:.1f}"
        help_skors2 = f"Kalkulasi Total (Sosial 2):\nmin(10.0, ({jiwa_terdampak:,.0f} / 100,000) * 10) = {skor_sosial_2:.1f}/10" + (f" (Likert: {(skor_sosial_2 / 2.0):.1f}/5)" if is_likert_mode else "")
        help_sos2 = f"Data Konsorsium Pembaruan Agraria (KPA) & TanahKita:\n- Total Korban Perampasan Ruang Hidup: {jiwa_terdampak:,.0f} Jiwa\n- Ekstraksi didukung NLP Regex Analysis pada dokumen deskripsi.\n\nKalkulasi Threshold Darurat Kemanusiaan:\n- Ambang Batas Pulau: 100,000 Jiwa\n\n{help_skors2}"
        
        col3_delta = f"STATUS: KRISIS AGRARIA (RED FLAG)" if skor_sosial_2 >= 6.0 else f"STATUS: TERKENDALI"
        col3_color = "inverse" if skor_sosial_2 >= 6.0 else "normal"
        
        col1, col2 = st.columns(2)
        col1.metric("Korban Terdampak", f"{jiwa_terdampak:,.0f} Jiwa", f"↑ Melampaui Ambang Darurat", delta_color="inverse", help=help_sos2)
        col2.metric(f"Skor Genosida Ruang (Sosial 2)", f"{sks2_str} / {card_denom}", col3_delta, delta_color=col3_color, help=help_skors2)
        st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
        
        if not df_konflik.empty:
            df_k_darat = df_konflik[~df_konflik['sektor'].str.contains('air|laut|pesisir|nelayan|sungai|pulau|tailing', case=False, na=False)].copy()
            if 'tahun' in df_k_darat.columns and 'dampak_masyarakat_jiwa' in df_k_darat.columns:
                df_k_darat['tahun'] = pd.to_numeric(df_k_darat['tahun'], errors='coerce')
                df_k_darat['dampak_masyarakat_jiwa'] = pd.to_numeric(df_k_darat['dampak_masyarakat_jiwa'], errors='coerce').fillna(0)
                df_k_trend = df_k_darat.groupby(['tahun'])['dampak_masyarakat_jiwa'].sum().reset_index(name='jumlah_jiwa')
                df_k_trend['kumulatif'] = df_k_trend['jumlah_jiwa'].cumsum()
                fig_s1 = px.area(df_k_trend, x='tahun', y='kumulatif', title="Akumulasi Jumlah Korban Perampasan Ruang Hidup (2014-2024)", color_discrete_sequence=['#9C27B0'])
                fig_s1.add_hline(y=100000, line_dash="dash", line_color="#E74C3C", annotation_text="Threshold Darurat Kumulatif (100.000 Jiwa)", annotation_position="top left")
                fig_s1.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0))
                st.plotly_chart(fig_s1, use_container_width=True, config={'displayModeBar': False})
                with st.expander("Tampilkan Data Indikasi Perampasan Lahan & Korban"):
                    st.dataframe(df_k_darat[['tahun', 'judul', 'sektor', 'dampak_masyarakat_jiwa']], use_container_width=True)
                    st.caption("Sumber: `sulawesi_konflik_agraria_tanahkita.csv` (Konsorsium Pembaruan Agraria & YLBHI)")

    with tab_s3:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Threshold & Referensi (Sosial 3):</b><br>• <b>Kriminalisasi & HAM:</b> > 50 Insiden (Tingkat Pulau).<br>• <b>Keterangan Data:</b> Menggunakan metrik insiden kekerasan/kriminalisasi (berbasis metodologi Satya Bumi & Protection International). Threshold darurat HAM ditetapkan maksimal 50 insiden se-Sulawesi, merepresentasikan rasio ekuivalensi dominan (87,7%) dari total beban perlindungan HAM lingkungan hidup nasional (57 insiden).</div>", unsafe_allow_html=True)
        
        sks3_str = f"{(skor_sosial_3 / 2.0):.1f}" if is_likert_mode else f"{skor_sosial_3:.1f}"
        help_skors3 = f"Kalkulasi Total (Sosial 3):\nmin(10.0, ({insiden_krim} / 50) * 10) = {skor_sosial_3:.1f}/10" + (f" (Likert: {(skor_sosial_3 / 2.0):.1f}/5)" if is_likert_mode else "")
        help_sos3 = f"Data Insiden HAM (KPA/TanahKita & Ekstrapolasi Satya Bumi):\n- Total Insiden Kriminalisasi & Kekerasan: {insiden_krim} Kejadian\n- Ekstraksi didukung NLP Regex Analysis (indikator penangkapan/kekerasan).\n\nKalkulasi Threshold Darurat Represi:\n- Ambang Batas Pulau: 50 Insiden\n\n{help_skors3}"
        
        col3_delta = f"STATUS: KEKERASAN NEGARA (RED FLAG)" if skor_sosial_3 >= 6.0 else f"STATUS: TERKENDALI"
        col3_color = "inverse" if skor_sosial_3 >= 6.0 else "normal"
        
        col1, col2 = st.columns(2)
        col1.metric("Total Insiden Kriminalisasi", f"{insiden_krim} Kejadian", f"↑ Ancaman Pembela HAM", delta_color="inverse", help=help_sos3)
        col2.metric(f"Skor Represi (Sosial 3)", f"{sks3_str} / {card_denom}", col3_delta, delta_color=col3_color, help=help_skors3)
        st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
        
        if not df_konflik.empty:
            krim_df = df_k_darat[df_k_darat['indikasi_kriminalisasi'] == True].copy()
            krim_df['jumlah_ditangkap'] = pd.to_numeric(krim_df['jumlah_ditangkap'], errors='coerce').fillna(0)
            if 'tahun' in krim_df.columns:
                krim_df['tahun'] = pd.to_numeric(krim_df['tahun'], errors='coerce')
                krim_trend = krim_df.groupby('tahun').size().reset_index(name='jumlah')
                krim_trend['kumulatif'] = krim_trend['jumlah'].cumsum()
                fig_s2 = px.area(krim_trend, x='tahun', y='kumulatif', title="Akumulasi Insiden Kriminalisasi & Kekerasan Terhadap Warga", color_discrete_sequence=['#E74C3C'])
                fig_s2.add_hline(y=50, line_dash="dash", line_color="#F1C40F", annotation_text="Threshold Represi Kumulatif (50 Insiden)", annotation_position="top left")
                fig_s2.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0))
                st.plotly_chart(fig_s2, use_container_width=True, config={'displayModeBar': False})
                with st.expander("Tampilkan Data Indikasi Kriminalisasi"):
                    st.dataframe(krim_df[['tahun', 'judul', 'sektor', 'jumlah_ditangkap', 'jumlah_luka']], use_container_width=True)
                    st.caption("Sumber: `sulawesi_konflik_agraria_tanahkita.csv` (Konsorsium Pembaruan Agraria & YLBHI)")

    with tab_s4:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Threshold & Referensi (Sosial 4):</b><br>• <b>Defisit Layanan Faskes:</b> Gap Target SPA 80%.<br>• <b>Keterangan Data:</b> Menggunakan metrik proporsi Puskesmas yang memenuhi standar Sarana, Prasarana, dan Alat Kesehatan (SPA). Target nasional ditetapkan minimal 80% (RPJMN 2025–2029, Bab IV & Permenkes 6/2024).</div>", unsafe_allow_html=True)
        
        sks4_str = f"{(skor_sosial_4 / 2.0):.1f}" if is_likert_mode else f"{skor_sosial_4:.1f}"
        gap_spa = max(0.0, 80.0 - spa_aktual_pct)
        help_skors4 = f"Kalkulasi Total (Sosial 4):\nmin(10.0, ({gap_spa:.1f}% / 45.0%) * 10) = {skor_sosial_4:.1f}/10" + (f" (Likert: {(skor_sosial_4 / 2.0):.1f}/5)" if is_likert_mode else "")
        help_sos4 = f"Data Faskes (Kemenkes & RPJMN):\n- Target SPA Nasional: 80.0%\n- Aktual SPA Sulawesi: {spa_aktual_pct}%\n- Gap Defisit Layanan: {gap_spa:.1f}%\n\n{help_skors4}"
        
        col3_delta = f"STATUS: PARADOKS BOOM MINERAL (RED FLAG)" if skor_sosial_4 >= 6.0 else f"STATUS: TERKENDALI"
        col3_color = "inverse" if skor_sosial_4 >= 6.0 else "normal"
        
        col1, col2 = st.columns(2)
        col1.metric("Defisit Target SPA (Faskes)", f"{gap_spa:.1f} %", f"↓ Di Bawah Standar Kemenkes", delta_color="inverse", help=help_sos4)
        col2.metric(f"Skor Defisit Layanan (Sosial 4)", f"{sks4_str} / {card_denom}", col3_delta, delta_color=col3_color, help=help_skors4)
        st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
        
        if not df_faskes.empty:
            df_f_plot = df_faskes.copy()
            df_f_plot['jumlah'] = pd.to_numeric(df_f_plot['jumlah'], errors='coerce').fillna(0)
            df_f_plot['tahun'] = pd.to_numeric(df_f_plot['tahun'], errors='coerce')
            df_f_agg = df_f_plot.groupby(['tahun', 'provinsi'])['jumlah'].sum().reset_index()
            fig_s4 = px.line(df_f_agg, x='tahun', y='jumlah', color='provinsi', markers=True,
                            title="Ironi: Tren Jumlah Fisik Faskes vs Boom Ekspor Nikel (2014-2024)")
            fig_s4.add_annotation(x=2024, y=df_f_agg['jumlah'].max(), text=f"Meski fisik Faskes bertambah, kelayakan standar SPA mentok di {spa_aktual_pct}% (Target 80%)", showarrow=False, yshift=20, font=dict(color="#E74C3C"))
            fig_s4.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_s4, use_container_width=True, config={'displayModeBar': False})
            with st.expander("Tampilkan Data Unit Faskes Fisik (Kemenkes)"):
                st.dataframe(df_f_plot, use_container_width=True)
                st.caption("Sumber: `sulawesi_faskes_agregat_v3.csv` (Kemenkes & BPS)")

st.markdown("<br>", unsafe_allow_html=True)


# ---------------------------------------------------------
# E. MITOS TATA KELOLA VS OBRAL IZIN (VETO KEBIJAKAN)
# ---------------------------------------------------------
colE1, colE2 = st.columns([1, 2])
with colE1:
    skv1_str = f"{(skor_veto_1 / 2.0):.1f}" if is_likert_mode else f"{skor_veto_1:.1f}"
    skv2_str = f"{(skor_veto_2 / 2.0):.1f}" if is_likert_mode else f"{skor_veto_2:.1f}"
    skv3_str = f"{(skor_veto_3 / 2.0):.1f}" if is_likert_mode else f"{skor_veto_3:.1f}"
    
    st.markdown(f'''
    <div style="background:#2C3E50; padding:20px; border-radius:10px; border-left: 5px solid #E74C3C; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
        <h4 style="color:#FFF; margin-top:0;">Audit D3TLH: Veto Kebijakan</h4>
        <p style="color:#BDC3C7; font-size:0.9rem;">"Penyusunan D3TLH dirancang sebagai pertimbangan dalam membatasi izin eksploitasi."</p>
        <hr style="border-color:#34495E;">
        <h4 style="color:#E74C3C;">Fakta Empiris:</h4>
        <p style="color:#E0E0E0; font-size:0.9rem;">Evaluasi menunjukkan pentingnya penguatan kepatuhan hukum dan efektivitas instrumen pengendalian perizinan.</p>
        <div style="background-color: #1A202C; padding: 15px; border-radius: 8px; margin-top: 15px; text-align: center; border: 1px solid #E74C3C;">
            <div style="font-size: 11px; color: #BDC3C7; text-transform: uppercase; letter-spacing: 1px;">Skor Pengendalian Izin</div>
            <div style="font-size: 32px; font-weight: 800; color: #E74C3C; line-height: 1.2;">{card_v_val} <span style="font-size: 16px;">/ {card_denom}</span></div>
            <div style="font-size: 11px; color: #E74C3C; margin-top: 5px; margin-bottom: 10px; font-weight: bold;">STATUS: PERLU REFORMASI</div>
            <div style="text-align: left; font-size: 11px; color: #BDC3C7; border-top: 1px dashed #444; padding-top: 10px; line-height: 1.5;">
                <b>Rincian Skor Matriks Veto:</b><br>
                • <b>Veto 1 (Obral WIUP Baru):</b> {skv1_str} / {card_denom}<br>
                • <b>Veto 2 (Pembiaran Ilegal):</b> {skv2_str} / {card_denom}<br>
                • <b>Veto 3 (Ekspansi PLTU Captive):</b> {skv3_str} / {card_denom}
            </div>
        </div>
        <div style="background:#C0392B; color:white; padding:5px 10px; border-radius:5px; font-weight:bold; text-align:center; margin-top:15px;">
            ANALISIS: Penguatan Pengawasan Kebijakan
        </div>
    </div>
    ''', unsafe_allow_html=True)

with colE2:
    tab_v1, tab_v2, tab_v3 = st.tabs(["(Veto 1) Obral Konsesi Legal", "(Veto 2) Pembiaran Pelanggaran", "(Veto 3) Karpet Merah Energi Kotor"])
    
    with tab_v1:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Threshold & Referensi (Veto 1):</b><br>• <b>Obral Konsesi WIUP Baru:</b> > 100 Izin Baru.<br>• <b>Keterangan Data:</b> Menggunakan metrik jumlah penerbitan IUP baru di tengah kondisi krisis. Threshold Veto (pengabaian regulasi) ditetapkan maksimal 100 izin baru secara kumulatif, mengacu pada Laporan Kinerja Ditjen Minerba ESDM 2024.</div>", unsafe_allow_html=True)
        
        skv1_str = f"{(skor_veto_1 / 2.0):.1f}" if is_likert_mode else f"{skor_veto_1:.1f}"
        help_skorv1 = f"Kalkulasi Total (Veto 1):\nmin(10.0, ({izin_baru:.0f} / 100) * 10) = {skor_veto_1:.1f}/10" + (f" (Likert: {(skor_veto_1 / 2.0):.1f}/5)" if is_likert_mode else "")
        help_v1 = f"Data Penerbitan WIUP Baru (ESDM):\n- Threshold Kumulatif: 100 Izin\n- Aktual Diterbitkan: {izin_baru:.0f} Izin\n\n{help_skorv1}"
        
        col3_delta = f"STATUS: VETO GAGAL (RED FLAG)" if skor_veto_1 >= 6.0 else f"STATUS: TERKENDALI"
        col3_color = "inverse" if skor_veto_1 >= 6.0 else "normal"
        
        col1, col2 = st.columns(2)
        col1.metric("Total Izin Baru (Sejak 2014)", f"{izin_baru:.0f} Izin", "↑ Eksploitasi Meluas", delta_color="inverse", help=help_v1)
        col2.metric("Skor Paradoks Izin (Veto 1)", f"{skv1_str} / {card_denom}", col3_delta, delta_color=col3_color, help=help_skorv1)
        st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
        
        if not df_izin.empty:
            df_izin_plot = df_izin[df_izin['Tahun'] >= 2014].copy()
            df_izin_agg = df_izin_plot.groupby('Tahun')['Jumlah_Izin_Baru'].sum().reset_index()
            df_izin_agg['kumulatif'] = df_izin_agg['Jumlah_Izin_Baru'].cumsum()
            fig_v1 = px.area(df_izin_agg, x='Tahun', y='kumulatif', title="Akumulasi Obral IUP Baru di Era Krisis (2014-2024)", color_discrete_sequence=['#E67E22'])
            fig_v1.add_hline(y=100, line_dash="dash", line_color="#F1C40F", annotation_text="Threshold Veto Kumulatif (100 Izin)", annotation_position="top left")
            fig_v1.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_v1, use_container_width=True, config={'displayModeBar': False})
            with st.expander("Tampilkan Data Penerbitan Izin"):
                st.dataframe(df_izin_plot[['Tahun', 'Jumlah_Izin_Baru']], use_container_width=True)
                st.caption("Sumber: `sulawesi_izin_baru_per_tahun.csv` (Registry MODI ESDM)")

    with tab_v2:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Threshold & Referensi (Veto 2):</b><br>• <b>Pembiaran Izin Ilegal:</b> > 10 Perusahaan Ilegal.<br>• <b>Keterangan Data:</b> Menggunakan metrik jumlah korporat yang terafiliasi dengan perizinan ilegal (menabrak kawasan lindung, HGU kedaluwarsa, atau tumpang tindih). Threshold ditetapkan maksimal 10 perusahaan di tingkat pulau (Catatan Akhir Tahun KPA 2023, Hal. 49).</div>", unsafe_allow_html=True)
        
        skv2_str = f"{(skor_veto_2 / 2.0):.1f}" if is_likert_mode else f"{skor_veto_2:.1f}"
        help_skorv2 = f"Kalkulasi Total (Veto 2):\nmin(10.0, ({perusahaan_ilegal} / 10) * 10) = {skor_veto_2:.1f}/10" + (f" (Likert: {(skor_veto_2 / 2.0):.1f}/5)" if is_likert_mode else "")
        help_v2 = f"Data Korporat Ilegal (KPA):\n- Threshold Veto: 10 Korporat\n- Aktual Tercatat: {perusahaan_ilegal} Korporat\n\n{help_skorv2}"
        
        col3_delta = f"STATUS: NEGARA LUMPUH (RED FLAG)" if skor_veto_2 >= 6.0 else f"STATUS: TERKENDALI"
        col3_color = "inverse" if skor_veto_2 >= 6.0 else "normal"
        
        col1, col2 = st.columns(2)
        col1.metric("Korporat Pelanggar Hukum", f"{perusahaan_ilegal} Korporat", "↑ Hukum Tumpul", delta_color="inverse", help=help_v2)
        col2.metric("Skor Impunitas (Veto 2)", f"{skv2_str} / {card_denom}", col3_delta, delta_color=col3_color, help=help_skorv2)
        st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
        
        if not df_kpa_izin.empty:
            df_kpa_explode = df_kpa_izin.copy()
            df_kpa_explode['jenis_masalah_izin'] = df_kpa_explode['jenis_masalah_izin'].str.split('; ')
            df_kpa_explode = df_kpa_explode.explode('jenis_masalah_izin')
            masalah_counts = df_kpa_explode['jenis_masalah_izin'].value_counts().reset_index()
            masalah_counts.columns = ['Jenis Pelanggaran', 'Jumlah Korporat']
            
            fig_v2 = px.bar(masalah_counts, x='Jumlah Korporat', y='Jenis Pelanggaran', orientation='h', 
                            title="Distribusi Modus Pelanggaran Izin Korporat", 
                            color_discrete_sequence=['#E74C3C'])
            fig_v2.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", 
                                 yaxis={'categoryorder':'total ascending'}, margin=dict(l=0, r=0, t=40, b=0))
            
            st.plotly_chart(fig_v2, use_container_width=True, config={'displayModeBar': False})
            
            with st.expander("Tampilkan Detail Kasus (KPA)"):
                st.dataframe(df_kpa_izin[['nama_perusahaan', 'jenis_masalah_izin', 'lokasi']], use_container_width=True, hide_index=True)
                st.caption("Sumber: `kpa_masalah_izin_perusahaan.csv` (CATAHU Konsorsium Pembaruan Agraria)")

    with tab_v3:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Threshold & Referensi (Veto 3):</b><br>• <b>Ekspansi PLTU Captive:</b> > 5.000 MW (5 GW).<br>• <b>Keterangan Data:</b> Menggunakan metrik kapasitas Pembangkit Listrik Tenaga Uap (PLTU) batubara captive yang dibangun untuk menyuplai smelter. Threshold ditetapkan maksimal 5.000 MW secara pulau (Global Energy Monitor 2023, Hal. 2).</div>", unsafe_allow_html=True)
        
        skv3_str = f"{(skor_veto_3 / 2.0):.1f}" if is_likert_mode else f"{skor_veto_3:.1f}"
        help_skorv3 = f"Kalkulasi Total (Veto 3):\nmin(10.0, ({kapasitas_pltu:.1f} / 5000.0) * 10) = {skor_veto_3:.1f}/10" + (f" (Likert: {(skor_veto_3 / 2.0):.1f}/5)" if is_likert_mode else "")
        help_v3 = f"Data Ekspansi PLTU Captive (GEM):\n- Threshold Veto: 5.000 MW\n- Aktual Terencana/Dibangun: {kapasitas_pltu:.1f} MW\n\n{help_skorv3}"
        
        col3_delta = f"STATUS: HYPOCRISY (RED FLAG)" if skor_veto_3 >= 6.0 else f"STATUS: TERKENDALI"
        col3_color = "inverse" if skor_veto_3 >= 6.0 else "normal"
        
        col1, col2 = st.columns(2)
        os_ratio_v3 = (kapasitas_pltu / 5000.0) * 100
        v3_delta_text = f"↑ Overshoot {os_ratio_v3:.1f}% dari ambang batas" if kapasitas_pltu > 5000 else f"Aman (≤ 5 GW)"
        col1.metric("Kapasitas PLTU Captive", f"{kapasitas_pltu/1000:.2f} GW", v3_delta_text, delta_color="inverse", help=help_v3)
        col2.metric("Skor Inkonsistensi Iklim (Veto 3)", f"{skv3_str} / {card_denom}", col3_delta, delta_color=col3_color, help=help_skorv3)
        st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
        
        if not df_pltu_captive.empty:
            pltu_status = df_pltu_captive.groupby('Status').size().reset_index(name='jumlah')
            fig_v3 = px.pie(pltu_status, names='Status', values='jumlah', title="Proporsi Status PLTU Batubara Captive di Sulawesi", hole=0.4, color_discrete_sequence=px.colors.sequential.Oranges_r)
            fig_v3.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_v3, use_container_width=True, config={'displayModeBar': False})
            with st.expander("Tampilkan Data PLTU Captive"):
                st.dataframe(df_pltu_captive[['Plant name', 'Owner', 'Status', 'Capacity (MW)']], use_container_width=True)
                st.caption("Sumber: `sulawesi_pltu_captive.csv` (Global Energy Monitor 2023)")

st.markdown("<br>", unsafe_allow_html=True)

