import streamlit as st
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.components.sidebar import render_sidebar

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
    df_kes = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_kesehatan_detail_2014_2024.csv")) if os.path.exists(os.path.join(DATA_DIR, "sulawesi_kesehatan_detail_2014_2024.csv")) else pd.DataFrame()
    df_ika = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_ika_2016_2024.csv")) if os.path.exists(os.path.join(DATA_DIR, "sulawesi_ika_2016_2024.csv")) else pd.DataFrame()
    df_bencana = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_bencana_bnpb_2014_2024.csv")) if os.path.exists(os.path.join(DATA_DIR, "sulawesi_bencana_bnpb_2014_2024.csv")) else pd.DataFrame()
    df_konflik = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_konflik_agraria_tanahkita.csv")) if os.path.exists(os.path.join(DATA_DIR, "sulawesi_konflik_agraria_tanahkita.csv")) else pd.DataFrame()
    df_izin = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_izin_baru_per_tahun.csv")) if os.path.exists(os.path.join(DATA_DIR, "sulawesi_izin_baru_per_tahun.csv")) else pd.DataFrame()
    df_iku = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_iku_2015_2024.csv")) if os.path.exists(os.path.join(DATA_DIR, "sulawesi_iku_2015_2024.csv")) else pd.DataFrame()
    df_b3 = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_limbah_b3.csv")) if os.path.exists(os.path.join(DATA_DIR, "sulawesi_limbah_b3.csv")) else pd.DataFrame()
    df_pltu_op = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_pltu_captive.csv")) if os.path.exists(os.path.join(DATA_DIR, "sulawesi_pltu_captive.csv")) else pd.DataFrame()
    df_gfw = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_gfw_master_1_dekade_2014_2023.csv")) if os.path.exists(os.path.join(DATA_DIR, "sulawesi_gfw_master_1_dekade_2014_2023.csv")) else pd.DataFrame()
    df_gfw_lindung = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_gfw_kawasan_lindung_loss_2014_2023.csv")) if os.path.exists(os.path.join(DATA_DIR, "sulawesi_gfw_kawasan_lindung_loss_2014_2023.csv")) else pd.DataFrame()
    df_gfw_driver = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_gfw_loss_by_driver_2014_2023.csv")) if os.path.exists(os.path.join(DATA_DIR, "sulawesi_gfw_loss_by_driver_2014_2023.csv")) else pd.DataFrame()
    df_konflik_fpic = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_konflik_tambang_fpic.csv")) if os.path.exists(os.path.join(DATA_DIR, "sulawesi_konflik_tambang_fpic.csv")) else pd.DataFrame()
    df_kpa_izin = pd.read_csv(os.path.join(DATA_DIR, "kpa_masalah_izin_perusahaan.csv")) if os.path.exists(os.path.join(DATA_DIR, "kpa_masalah_izin_perusahaan.csv")) else pd.DataFrame()
    df_pltu_captive = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_pltu_captive.csv")) if os.path.exists(os.path.join(DATA_DIR, "sulawesi_pltu_captive.csv")) else pd.DataFrame()
    df_kawasan_nikel = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_kawasan_nikel_luas_per_provinsi.csv")) if os.path.exists(os.path.join(DATA_DIR, "sulawesi_kawasan_nikel_luas_per_provinsi.csv")) else pd.DataFrame()
    df_faskes = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_faskes_agregat.csv")) if os.path.exists(os.path.join(DATA_DIR, "sulawesi_faskes_agregat.csv")) else pd.DataFrame()
    return df_kes, df_ika, df_bencana, df_konflik, df_izin, df_iku, df_b3, df_pltu_op, df_gfw, df_gfw_lindung, df_gfw_driver, df_konflik_fpic, df_kpa_izin, df_pltu_captive, df_kawasan_nikel, df_faskes

df_kes, df_ika, df_bencana, df_konflik, df_izin, df_iku, df_b3, df_pltu_op, df_gfw, df_gfw_lindung, df_gfw_driver, df_konflik_fpic, df_kpa_izin, df_pltu_captive, df_kawasan_nikel, df_faskes = load_data()

# =====================================================================
# PRE-CALCULATE SCORES SECTION A & B (Yang sudah ada datanya)
# =====================================================================

# --- SECTION A: UDARA ---
kapasitas_terkini = 0
iku_terkini = 75
if not df_pltu_op.empty:
    kapasitas_terkini = df_pltu_op[(df_pltu_op['Status'].str.lower() == 'operating')]['Capacity (MW)'].sum()
if not df_iku.empty:
    df_iku_avg_pre = df_iku.groupby('Tahun')['IKU'].mean().reset_index()
    if 2024 in df_iku_avg_pre['Tahun'].values:
        iku_terkini = df_iku_avg_pre[df_iku_avg_pre['Tahun'] == 2024]['IKU'].values[0]
skor_1 = min(10.0, (kapasitas_terkini / 10000) * 5 + max(0, (80 - iku_terkini) / 30) * 5)

skor_2 = 0
rasio_anomali = 0
kasus_sentra = 0
if not df_kes.empty:
    df_ts_pre = df_kes[df_kes['indikator'].str.contains('ISPA', case=False, na=False)]
    kasus_sentra = df_ts_pre[df_ts_pre['provinsi'].isin(['Sulawesi Tengah', 'Sulawesi Tenggara'])]['nilai'].sum()
    kasus_non_sentra = df_ts_pre[~df_ts_pre['provinsi'].isin(['Sulawesi Tengah', 'Sulawesi Tenggara'])]['nilai'].sum()
    rasio_anomali = (kasus_sentra / 2) / (kasus_non_sentra / 4) if kasus_non_sentra > 0 else 0
    skor_2 = min(10.0, max(0.0, (rasio_anomali - 1) * 10.0))

skor_3 = 0
skor_overcapacity = 0
total_b3_sulteng = 0
if not df_b3.empty:
    df_b3['Estimasi Timbulan (Ton/Tahun)'] = pd.to_numeric(df_b3['Estimasi Timbulan (Ton/Tahun)'], errors='coerce').fillna(0)
    total_b3_all_pre = df_b3['Estimasi Timbulan (Ton/Tahun)'].sum()
    total_b3_sulteng = df_b3[df_b3['Provinsi'] == 'Sulawesi Tengah']['Estimasi Timbulan (Ton/Tahun)'].sum()
    skor_overcapacity = total_b3_sulteng / 1_000_000
    skor_3 = min(10.0, (skor_overcapacity / 30.0) * 10)

skor_4 = 0
total_emisi_co2 = 0
if not df_gfw.empty:
    df_gfw['Total_Emisi_CO2_Megagram'] = pd.to_numeric(df_gfw['Total_Emisi_CO2_Megagram'], errors='coerce').fillna(0)
    total_emisi_co2 = df_gfw['Total_Emisi_CO2_Megagram'].sum() / 1_000_000
    skor_4 = min(10.0, (total_emisi_co2 / 150.0) * 10)

skor_akumulasi_udara = (skor_1 + skor_2 + skor_3 + skor_4) / 4

# --- SECTION B: AIR ---
ika_terkini = 50
ika_sulteng = 50
if not df_ika.empty:
    df_ika_avg = df_ika.groupby('Tahun')['Indeks Kualitas Air'].mean().reset_index()
    if 2024 in df_ika_avg['Tahun'].values:
        ika_terkini = df_ika_avg[df_ika_avg['Tahun'] == 2024]['Indeks Kualitas Air'].values[0]
    
    df_sulteng = df_ika[df_ika['Provinsi'] == 'Sulawesi Tengah']
    if not df_sulteng.empty and 2024 in df_sulteng['Tahun'].values:
        ika_sulteng = df_sulteng[df_sulteng['Tahun'] == 2024]['Indeks Kualitas Air'].values[0]

skor_air_1 = min(10.0, max(0, (80 - ika_sulteng) / 30) * 10)

skor_air_2 = 0
kasus_diare_sentra = 0
if not df_kes.empty:
    df_diare = df_kes[df_kes['indikator'].str.contains('Diare', case=False, na=False)]
    kasus_diare_sentra = df_diare[df_diare['provinsi'].isin(['Sulawesi Tengah', 'Sulawesi Tenggara'])]['nilai'].sum()
    k_non = df_diare[~df_diare['provinsi'].isin(['Sulawesi Tengah', 'Sulawesi Tenggara'])]['nilai'].sum()
    ir_s = (kasus_diare_sentra / 5_700_000) * 1000
    ir_n = (k_non / 14_200_000) * 1000 if k_non > 0 else 1
    r_diare = ir_s / ir_n if ir_n > 0 else 0
    skor_air_2 = min(10.0, max(0.0, (r_diare - 1) * 10.0))

skor_air_3 = 0
jumlah_konflik_air = 0
if not df_konflik.empty:
    keywords = 'air|laut|pesisir|nelayan|sungai|pulau|tailing'
    df_konflik_air = df_konflik[df_konflik['sektor'].str.contains(keywords, case=False, na=False) | 
                                df_konflik['judul'].str.contains(keywords, case=False, na=False) | 
                                df_konflik['deskripsi'].str.contains(keywords, case=False, na=False)]
    jumlah_konflik_air = len(df_konflik_air)
    skor_air_3 = min(10.0, (jumlah_konflik_air / 15.0) * 10)

skor_air_4 = 0
if not df_b3.empty:
    t_b3_sulteng = df_b3[df_b3['Provinsi'] == 'Sulawesi Tengah']['Estimasi Timbulan (Ton/Tahun)'].sum()
    skor_air_4 = min(10.0, (t_b3_sulteng / 25_000_000) * 10)

skor_akumulasi_air = (skor_air_1 + skor_air_2 + skor_air_3 + skor_air_4) / 4

# --- SECTION C: LAHAN, SOSIAL & TATA KELOLA ---
skor_lahan_1 = 0
bencana_sulteng_sultra = 0
if not df_bencana.empty:
    df_bencana_sentra = df_bencana[df_bencana['provinsi'].isin(['Sulawesi Tengah', 'Sulawesi Tenggara'])].copy()
    df_bencana_sentra['jumlah_kejadian'] = pd.to_numeric(df_bencana_sentra['jumlah_kejadian'], errors='coerce').fillna(0)
    bencana_sulteng_sultra = df_bencana_sentra['jumlah_kejadian'].sum()    # Skor 1: Bencana (Threshold Opsi C: 877 kejadian)
    skor_lahan_1 = min(10.0, (bencana_sulteng_sultra / 877) * 10)

skor_lahan_2 = 0
deforestasi_sentra = 0
if not df_gfw.empty:
    df_gfw_sentra = df_gfw[df_gfw['Provinsi'].isin(['Sulawesi Tengah', 'Sulawesi Tenggara'])].copy()
    df_gfw_sentra['Total_Deforestasi_Ha'] = pd.to_numeric(df_gfw_sentra['Total_Deforestasi_Ha'], errors='coerce').fillna(0)
    deforestasi_sentra = df_gfw_sentra['Total_Deforestasi_Ha'].sum()    # Skor 2: Deforestasi (Threshold Opsi C: 638,000 Ha)
    skor_lahan_2 = min(10.0, (deforestasi_sentra / 638_000) * 10)


# Calculate Lahan 3 & 4
skor_lahan_3 = 0.0
skor_lahan_4 = 0.0
lindung_hilang = 0
tambang_driver_ha = 0

if not df_gfw_lindung.empty:
    df_l = df_gfw_lindung[df_gfw_lindung['Provinsi'].isin(['Sulawesi Tengah', 'Sulawesi Tenggara'])].copy()
    df_l['Luas_Hilang_Kawasan_Lindung_Ha'] = pd.to_numeric(df_l['Luas_Hilang_Kawasan_Lindung_Ha'], errors='coerce').fillna(0)
    lindung_hilang = df_l['Luas_Hilang_Kawasan_Lindung_Ha'].sum()    # Skor 3: Pelanggaran Lindung (Threshold Opsi C: 638,000 Ha)
    skor_lahan_3 = min(10.0, (lindung_hilang / 638_000) * 10)

if not df_gfw_driver.empty:
    df_d = df_gfw_driver[df_gfw_driver['Provinsi'].isin(['Sulawesi Tengah', 'Sulawesi Tenggara'])].copy()
    df_d['Luas_Deforestasi_Ha'] = pd.to_numeric(df_d['Luas_Deforestasi_Ha'], errors='coerce').fillna(0)
    tambang_driver = df_d[df_d['Faktor_Pendorong'] == 'Deforestasi Komoditas (Tambang/Sawit)']
    tambang_driver_ha = tambang_driver['Luas_Deforestasi_Ha'].sum()    # Skor 4: Tambang Driver (Threshold Opsi C: 500,000 Ha)
    skor_lahan_4 = min(10.0, (tambang_driver_ha / 500_000) * 10)

# Skor 5: Gap AMDAL vs IUP (Ekspansi Spekulatif)
skor_lahan_5 = 0.0
total_iup_nikel = 0.0
total_amdal_nikel = 0.0
gap_amdal_iup = 0.0
if not df_kawasan_nikel.empty:
    sentra_kn = df_kawasan_nikel[df_kawasan_nikel['provinsi'].isin(['Sulawesi Tengah', 'Sulawesi Tenggara'])].copy()
    sentra_kn['total_luas_iup_ha'] = pd.to_numeric(sentra_kn['total_luas_iup_ha'], errors='coerce').fillna(0)
    sentra_kn['total_luas_amdal_ha'] = pd.to_numeric(sentra_kn['total_luas_amdal_ha'], errors='coerce').fillna(0)
    total_iup_nikel = sentra_kn['total_luas_iup_ha'].sum()
    total_amdal_nikel = sentra_kn['total_luas_amdal_ha'].sum()
    gap_amdal_iup = total_amdal_nikel - total_iup_nikel  # Positif = AMDAL > IUP (Spekulatif)
    rasio_ekspansi = gap_amdal_iup / total_iup_nikel if total_iup_nikel > 0 else 0
    skor_lahan_5 = min(10.0, rasio_ekspansi * 10)  # 100% gap = skor 10

skor_akumulasi_lahan = (skor_lahan_1 + skor_lahan_2 + skor_lahan_3 + skor_lahan_4) / 4


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
    # Threshold 12 = total aktual kasus FPIC di dataset kita (proporsional, bukan bias)
    skor_sosial_1 = min(10.0, (kasus_fpic / 12) * 10)

# Skor 4: Defisit Layanan Dasar (Faskes & SPA)
skor_sosial_4 = 0.0
spa_aktual_pct = 42.5  # Proxy data: estimasi Puskesmas memenuhi standar SPA di Sulteng/Sultra
target_rpjmn = 80.0    # Target RPJMN 2025-2029

if not df_faskes.empty:
    # Mengukur gap antara pemenuhan standar SPA aktual vs target RPJMN (80%)
    # Makin besar gap-nya, makin tinggi skor defisit
    gap_spa = max(0.0, target_rpjmn - spa_aktual_pct)
    skor_sosial_4 = min(10.0, (gap_spa / target_rpjmn) * 10)  # Skala defisit proporsional

skor_akumulasi_sosial = (skor_sosial_1 + skor_sosial_2 + skor_sosial_3 + skor_sosial_4) / 4


# Calculate Veto
skor_veto_1 = 0.0
skor_veto_2 = 0.0
skor_veto_3 = 0.0
izin_baru = 0
perusahaan_ilegal = 0
kapasitas_pltu = 0.0

if not df_izin.empty:
    df_izin['Tahun'] = pd.to_numeric(df_izin['Tahun'], errors='coerce')
    df_izin['Jumlah_Izin_Baru'] = pd.to_numeric(df_izin['Jumlah_Izin_Baru'], errors='coerce').fillna(0)
    df_izin_recent = df_izin[df_izin['Tahun'] >= 2014]
    izin_baru = df_izin_recent['Jumlah_Izin_Baru'].sum()
    skor_veto_1 = min(10.0, (izin_baru / 100) * 10) # 100 izin baru di masa krisis = 10.0

if not df_kpa_izin.empty:
    perusahaan_ilegal = len(df_kpa_izin['nama_perusahaan'].unique())
    skor_veto_2 = min(10.0, (perusahaan_ilegal / 10) * 10) # 10 perusahaan dibiarkan beroperasi ilegal = 10.0

if not df_pltu_captive.empty:
    df_pltu_captive['Capacity (MW)'] = pd.to_numeric(df_pltu_captive['Capacity (MW)'], errors='coerce').fillna(0)
    kapasitas_pltu = df_pltu_captive['Capacity (MW)'].sum()
    skor_veto_3 = min(10.0, (kapasitas_pltu / 5000) * 10) # > 5 GW PLTU Captive = 10.0 (Kenyataannya > 16 GW)

skor_akumulasi_veto = (skor_veto_1 + skor_veto_2 + skor_veto_3) / 3


# =====================================================================
# KESIMPULAN EKSEKUTIF
# =====================================================================
st.markdown("""
<div style="background: #1E1E1E; padding: 20px; border-radius: 8px; border-left: 5px solid #F44336; margin-bottom: 30px;">
    <h3 style="color: #EF5350; margin-top: 0;">Kesimpulan Eksekutif</h3>
    <p style="color: #E0E0E0; font-size: 1.05rem; line-height: 1.6; margin-bottom: 0;">
        D3TLH dan AMDAL telah gagal dan mati sebagai alat pelindung nyawa ruang hidup. Dokumen-dokumen perizinan tersebut telah mereduksi penderitaan manusia menjadi sekadar angka-angka spasial di atas kertas, berfungsi tak lebih dari "stempel birokrasi" untuk melegalkan pengrusakan ekologis secara sistematis.
    </p>
</div>
""", unsafe_allow_html=True)

# =====================================================================
# KARTU METRIK (Style PERSIS Page 3)
# =====================================================================
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">DAYA TAMPUNG UDARA</div>
            <div class="metric-value" style="color: #E53935;">{skor_akumulasi_udara:.1f}</div>
            <div class="metric-desc">
                <b>STATUS: DAYA TAMPUNG JEBOL</b><br><br>
                Lonjakan drastis persentase Kasus ISPA dan penyakit saluran pernapasan di lingkar tambang.
            </div>
        </div>
        <div class="metric-source">
            <b>VONIS:</b> Kegagalan Deteksi Morbiditas Akumulatif<br>
            <i>Kapasitas PLTU: {kapasitas_terkini:,.0f} MW / IKU: {iku_terkini:.1f} / Rasio ISPA: {rasio_anomali:.1f}x</i>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">DAYA TAMPUNG AIR</div>
            <div class="metric-value" style="color: #E53935;">{skor_akumulasi_air:.1f}</div>
            <div class="metric-desc">
                <b>STATUS: DAYA TAMPUNG JEBOL</b><br><br>
                Penurunan drastis Indeks Kualitas Air dan hancurnya pesisir ditandai ledakan morbiditas air.
            </div>
        </div>
        <div class="metric-source">
            <b>VONIS:</b> Kegagalan Pengukuran Toksisitas<br>
            <i>IKA Sulteng: {ika_sulteng:.1f} / Kasus Diare: {kasus_diare_sentra:,.0f} / Konflik Air: {jumlah_konflik_air}</i>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

# Row 2: Placeholder untuk 3 kartu yang belum ada datanya
col3, col4, col5 = st.columns(3)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">DAYA DUKUNG LAHAN</div>
            <div class="metric-value" style="color: #E53935;">{skor_akumulasi_lahan:.1f}</div>
            <div class="metric-desc">
                <b>STATUS: KRISIS RUANG DARAT</b><br><br>
                Hancurnya sabuk hijau memicu rentetan bencana hidrometeorologi parah.
            </div>
        </div>
        <div class="metric-source">
            <b>VONIS:</b> Kegagalan Mengukur Efek Domino Lanskap<br>
            <i>Bencana: {bencana_sulteng_sultra:,.0f} Kejadian / Deforestasi: {deforestasi_sentra:,.0f} Ha</i>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">DAYA DUKUNG SOSIAL</div>
            <div class="metric-value" style="color: #E53935;">{skor_akumulasi_sosial:.1f}</div>
            <div class="metric-desc">
                <b>STATUS: DARURAT AGRARIA</b><br><br>
                Eskalasi konflik perampasan lahan produktif dan represi aparat ke masyarakat sipil.
            </div>
        </div>
        <div class="metric-source">
            <b>VONIS:</b> Ilusi Jasa Budaya & Kedaulatan Ruang<br>
            <i>Konflik Lahan: {konflik_darat} Kasus TanahKita</i>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">VETO KEBIJAKAN</div>
            <div class="metric-value" style="color: #E53935;">{skor_akumulasi_veto:.1f}</div>
            <div class="metric-desc">
                <b>STATUS: REGULATORY CAPTURE</b><br><br>
                Lonjakan IUP raksasa di saat indikator kesehatan & ekologi sudah menjerit merah.
            </div>
        </div>
        <div class="metric-source">
            <b>VONIS:</b> Kegagalan Tata Kelola Negara<br>
            <i>{izin_baru:,.0f} Izin Baru & {kapasitas_pltu/1000:,.1f} GW PLTU Captive Diloloskan</i>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><hr style='border: 1px dashed #333;'><br>", unsafe_allow_html=True)


# =====================================================================
# SECTION 1: FILOSOFI AUDIT FORENSIK
# =====================================================================
st.markdown("""
<div class="content-box">
<h2>1. Filosofi Audit Forensik (Sistem Alarm Rakyat)</h2>
<p>
AMDAL dan D3TLH pemerintah mengklaim bersifat "prediktif"—menilai batasan daya dukung alam <i>sebelum</i> izin diberikan. Namun, data lapangan membuktikan bahwa dokumen-dokumen tersebut secara sistematis cacat dan gagal melindungi ruang hidup masyarakat.
</p>
<p><b>Standpoint Riset ECC:</b><br>
Kita melakukan <b>Pembuktian Terbalik</b>. Kita tidak perlu berdebat soal rumus "daya dukung spasial" milik konsultan korporasi. Fakta empiris bahwa <span class="highlight-text">kasus ISPA meroket, banjir bandang rutin terjadi, konflik berdarah bereskalasi, dan izin terus diobral secara anomali</span> adalah <b>Bukti Mutlak (Definitive Proof)</b> bahwa daya dukung ekologis dan sosial wilayah tersebut <b>SUDAH JEBOL</b>.
</p>
<p>
Halaman ini merangkum semua indikator krisis menjadi sebuah palu godam untuk memvonis bahwa sistem AMDAL/D3TLH saat ini sekadar "stempel birokrasi" yang buta terhadap penderitaan manusia.
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
iku_terkini = 75
if not df_pltu_op.empty:
    kapasitas_terkini = df_pltu_op[(df_pltu_op['Status'].str.lower() == 'operating')]['Capacity (MW)'].sum()
if not df_iku.empty:
    df_iku_avg_pre = df_iku.groupby('Tahun')['IKU'].mean().reset_index()
    if 2024 in df_iku_avg_pre['Tahun'].values:
        iku_terkini = df_iku_avg_pre[df_iku_avg_pre['Tahun'] == 2024]['IKU'].values[0]
# Normalisasi: PLTU Max 10.000 MW, IKU kritis pada 50 (range 80 ke 50)
skor_1 = min(10.0, (kapasitas_terkini / 10000) * 5 + max(0, (80 - iku_terkini) / 30) * 5)

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
    skor_2 = min(10.0, max(0.0, (rasio_anomali - 1) * 10.0))

# Skor 3: Over-Capacity B3
skor_3 = 0
skor_overcapacity = 0
total_b3_sulteng = 0
if not df_b3.empty:
    df_b3['Estimasi Timbulan (Ton/Tahun)'] = pd.to_numeric(df_b3['Estimasi Timbulan (Ton/Tahun)'], errors='coerce').fillna(0)
    total_b3_all_pre = df_b3['Estimasi Timbulan (Ton/Tahun)'].sum()
    total_b3_sulteng = df_b3[df_b3['Provinsi'] == 'Sulawesi Tengah']['Estimasi Timbulan (Ton/Tahun)'].sum()
    skor_overcapacity = total_b3_sulteng / 1_000_000
    # Normalisasi: Batas ekstrem 30x lipat dari daya tampung = skor 10
    skor_3 = min(10.0, (skor_overcapacity / 30.0) * 10)

# Skor 4: Defisit Ekosistem
skor_4 = 0
if not df_gfw.empty:
    df_gfw['Total_Emisi_CO2_Megagram'] = pd.to_numeric(df_gfw['Total_Emisi_CO2_Megagram'], errors='coerce').fillna(0)
    total_emisi_pre = df_gfw['Total_Emisi_CO2_Megagram'].sum() / 1_000_000
    # Normalisasi: Emisi 150 Juta Ton = skor 10
    skor_4 = min(10.0, (total_emisi_pre / 150.0) * 10)

skor_akumulasi_udara = (skor_1 + skor_2 + skor_3 + skor_4) / 4

colA1, colA2 = st.columns([1, 2])
with colA1:
    st.markdown(f"""
<div style="background:#2C3E50; padding:20px; border-radius:10px; border-left:5px solid #E74C3C; height:100%;">
    <h4 style="color:#FFF; margin-top:0;">Audit D3TLH: Daya Tampung Udara</h4>
    <p style="color:#BDC3C7; font-size:0.9rem;">"Daya tampung udara (berdasarkan peta tutupan lahan) diklaim masih luas dan mampu menyerap emisi."</p>
    <hr style="border-color:#34495E;">
    <h4 style="color:#E74C3C;">Fakta Forensik ECC:</h4>
    <p style="color:#E0E0E0; font-size:0.9rem;">Lonjakan drastis persentase Kasus ISPA dan penyakit saluran pernapasan di lingkar tambang.</p>
    <div style="background-color: #1A202C; padding: 15px; border-radius: 8px; margin-top: 15px; text-align: center; border: 1px solid #E74C3C;">
        <div style="font-size: 11px; color: #BDC3C7; text-transform: uppercase; letter-spacing: 1px;">Akumulasi Skor Kerusakan</div>
        <div style="font-size: 32px; font-weight: 800; color: #E74C3C; line-height: 1.2;">{skor_akumulasi_udara:.1f} <span style="font-size: 16px;">/ 10</span></div>
        <div style="font-size: 11px; color: #E74C3C; margin-top: 5px; font-weight: bold;">STATUS: DAYA TAMPUNG JEBOL</div>
    </div>
    <div style="background:#C0392B; color:white; padding:5px 10px; border-radius:5px; font-weight:bold; text-align:center; margin-top:15px;">
        VONIS: Kegagalan Deteksi Morbiditas Akumulatif
    </div>
</div>
    """, unsafe_allow_html=True)

with colA2:
    if not df_kes.empty:
        tab1, tab2, tab3, tab4 = st.tabs(["Korelasi PLTU & Kualitas Udara", "Dampak Kasus ISPA/Pneumonia", "Fakta Beban Limbah & Emisi", "Hilangnya Paru-Paru Udara"])
        
        with tab1:
            # --- 1. Ekspansi PLTU vs Penurunan Kualitas Udara ---
            st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Narasi Anomali:</b> Pemerintah sering merilis angka rata-rata IKU tahunan seolah 'Masih Aman', menutupi tren eksponensial di mana kualitas udara terjun bebas tepat setelah keran mega-smelter dibuka lebar pada 2014-2015. <b>Threshold Kritis: IKU = 50</b> (batas terbawah Kategori Sedang/awal Kurang — <i>PermenLHK No.27/2021, Lampiran Tbl.1</i>).</div>", unsafe_allow_html=True)
            
            if not df_pltu_op.empty and not df_iku.empty:
                years = list(range(2010, 2025))
                prov_map = {
                    'Central Sulawesi': 'Sulawesi Tengah', 'South East Sulawesi': 'Sulawesi Tenggara',
                    'South Sulawesi': 'Sulawesi Selatan', 'North Sulawesi': 'Sulawesi Utara',
                    'West Sulawesi': 'Sulawesi Barat', 'Gorontalo': 'Gorontalo'
                }
                df_pltu_op['Provinsi'] = df_pltu_op['Subnational unit (province, state)'].replace(prov_map)
                df_pltu_op = df_pltu_op[(df_pltu_op['Status'].str.lower() == 'operating') & df_pltu_op['Start year'].notna()]
                
                panel_data_pltu = []
                for y in years:
                    for prov in prov_map.values():
                        cap = df_pltu_op[(df_pltu_op['Provinsi'] == prov) & (df_pltu_op['Start year'] <= y)]['Capacity (MW)'].sum()
                        panel_data_pltu.append({'Tahun': y, 'Provinsi': prov, 'Kapasitas_PLTU_MW': cap})
                df_pltu_trend = pd.DataFrame(panel_data_pltu)
                df_iku_avg = df_iku[df_iku['Tahun'].between(2010, 2024)].groupby('Tahun')['IKU'].mean().reset_index()
                
                # Gunakan skor pre-calculated
                kapasitas_grafik = df_pltu_trend[df_pltu_trend['Tahun'] == 2024]['Kapasitas_PLTU_MW'].sum()
                iku_grafik = df_iku_avg[df_iku_avg['Tahun'] == 2024]['IKU'].values[0] if not df_iku_avg[df_iku_avg['Tahun'] == 2024].empty else 75
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Kapasitas PLTU Aktif", f"{kapasitas_grafik:,.0f} MW", "Max threshold: 10.000 MW")
                col2.metric("Rata-rata IKU Sulawesi", f"{iku_grafik:.1f}", "Kritis jika turun ke 50 (PermenLHK 27/2021)", delta_color="inverse")
                col3.metric("Skor Ancaman Udara", f"{skor_1:.1f} / 10", "STATUS: KRITIS", delta_color="inverse")
                st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
                
                owid_colors = ['#9B5A40', '#E58872', '#5E85B4', '#A09CAE', '#82B989', '#E3D7A4']
                fig_2_2_combined = make_subplots(specs=[[{"secondary_y": True}]])
                
                for i, prov in enumerate(df_pltu_trend['Provinsi'].unique()):
                    d = df_pltu_trend[df_pltu_trend['Provinsi'] == prov]
                    fig_2_2_combined.add_trace(
                        go.Scatter(
                            x=d['Tahun'], y=d['Kapasitas_PLTU_MW'], name=prov, mode='lines', stackgroup='one',
                            line=dict(width=0.5, color='#444444'), fillcolor=owid_colors[i % len(owid_colors)],
                            hoveron='points+fills', hovertemplate='%{y:.0f} MW<extra></extra>'
                        ), secondary_y=False
                    )
                
                fig_2_2_combined.add_trace(
                    go.Scatter(
                        x=df_iku_avg['Tahun'], y=df_iku_avg['IKU'], name="Rata-rata IKU Sulawesi", mode='lines+markers', 
                        marker=dict(color='#FFFFFF', size=8, line=dict(width=2, color='#D32F2F')), 
                        line=dict(color='#D32F2F', width=4), hovertemplate='IKU: %{y:.2f}<extra></extra>'
                    ), secondary_y=True
                )
                
                # Threshold IKU = 50 (batas terbawah Sedang/awal Kurang — PermenLHK No.27/2021 Lampiran Tbl.1)
                fig_2_2_combined.add_hline(y=50, line_dash="dot", line_color="#FF5252", secondary_y=True)
                fig_2_2_combined.add_hline(y=70, line_dash="dash", line_color="#FFA726", secondary_y=True)
                
                # Manual annotations positioned ABOVE the lines
                fig_2_2_combined.add_annotation(
                    x=2010, y=52, yref="y2", text="IKU=50: Batas Kritis Kurang (PermenLHK 27/2021)",
                    showarrow=False, font=dict(color="#FF5252", size=10), xanchor="left"
                )
                fig_2_2_combined.add_annotation(
                    x=2010, y=72, yref="y2", text="IKU=70: Batas Bawah Baik",
                    showarrow=False, font=dict(color="#FFA726", size=10), xanchor="left"
                )
                
                fig_2_2_combined.add_vline(x=2014, line_dash="dash", line_color="rgba(255,255,255,0.3)", annotation_text="Booming Smelter Dimulai", annotation_position="top right")
                
                fig_2_2_combined.update_layout(
                    title=dict(text="Ekspansi PLTU vs Penurunan Kualitas Udara (2010-2024)", font=dict(color='#ECEFF1', size=16)),
                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#ECEFF1', family='Arial, sans-serif'),
                    legend=dict(orientation="v", yanchor="top", y=0.98, xanchor="left", x=0.02, bgcolor='rgba(30,30,30,0.8)', bordercolor='#555', borderwidth=1),
                    xaxis=dict(title="", tickmode='linear', dtick=2, tickformat='d', showgrid=False, showline=True, linecolor='#555555'),
                    yaxis=dict(title="Kapasitas PLTU Kumulatif (MW)", showgrid=True, gridcolor='rgba(255,255,255,0.1)', side='left'),
                    yaxis2=dict(title="Indeks Kualitas Udara (IKU)", showgrid=False, overlaying='y', side='right', range=[50, 100]),
                    hovermode="x unified", margin=dict(l=0, r=0, t=40, b=0)
                )
                st.plotly_chart(fig_2_2_combined, use_container_width=True, config={'displayModeBar': False})
                
                with st.expander("Lihat Data Mentah: Kapasitas PLTU per Provinsi", expanded=False):
                    df_pivot_pltu = df_pltu_trend.pivot(index='Tahun', columns='Provinsi', values='Kapasitas_PLTU_MW').reset_index()
                    st.dataframe(df_pivot_pltu, use_container_width=True, hide_index=True)
                    st.caption("Sumber: `sulawesi_pltu_captive.csv`")

        with tab2:
            # --- 2. Tren Historis Kasus ISPA/Pneumonia ---
            st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Narasi Anomali:</b> Dokumen daya dukung mengabaikan lonjakan tajam pasien ISPA di RSUD Morowali dan Kendari. Grafik membuktikan bahwa tren ISPA di provinsi non-tambang relatif stabil, namun meroket secara paralel dengan asap di provinsi sentra nikel.</div>", unsafe_allow_html=True)
            
            df_ts_filtered = df_kes[df_kes['indikator'].str.contains('ISPA', case=False, na=False)].copy()
            if not df_ts_filtered.empty:
                df_ts_filtered['Kategori'] = df_ts_filtered['provinsi'].apply(lambda x: 'Sentra Industri (Sulteng & Sultra)' if x in ['Sulawesi Tengah', 'Sulawesi Tenggara'] else 'Non-Sentra Industri (Lainnya)')
                df_ts_agg = df_ts_filtered.groupby(['tahun', 'provinsi', 'Kategori'])['nilai'].sum().reset_index()
                
                # Gunakan skor pre-calculated
                kasus_sentra_grafik = df_ts_filtered[df_ts_filtered['Kategori'] == 'Sentra Industri (Sulteng & Sultra)']['nilai'].sum()
                kasus_non_sentra_grafik = df_ts_filtered[df_ts_filtered['Kategori'] == 'Non-Sentra Industri (Lainnya)']['nilai'].sum()
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Kasus ISPA Sentra", f"{kasus_sentra_grafik:,.0f}", "Sulteng & Sultra")
                col2.metric("Total Kasus ISPA Lainnya", f"{kasus_non_sentra_grafik:,.0f}", "4 Provinsi Non-Sentra", delta_color="normal")
                col3.metric("Skor Rasio Anomali", f"{skor_2:.1f} / 10", f"Rasio: {rasio_anomali:.1f}x Lipat", delta_color="inverse")
                st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
                
                fig_3_3 = px.line(
                    df_ts_agg, x='tahun', y='nilai', color='provinsi', markers=True, line_dash='Kategori',
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                
                for trace in fig_3_3.data:
                    if trace.name in ['Sulawesi Tengah', 'Sulawesi Tenggara']:
                        trace.line.width = 4
                    else:
                        trace.line.width = 2
                        trace.opacity = 0.6
                
                fig_3_3.add_vline(x=2015, line_dash="dash", line_color="#FFEB3B", annotation_text="Eskalasi Pabrik Nikel", annotation_position="top left")
                
                fig_3_3.update_layout(
                    title="Tren Historis Kasus ISPA/Pneumonia (2014-2024)",
                    height=450, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                    legend=dict(title="Provinsi", orientation="v", yanchor="top", y=1, xanchor="left", x=1.02),
                    font=dict(color='#B0BEC5'),
                    xaxis=dict(title="Tahun", showgrid=True, gridcolor='rgba(255,255,255,0.1)', dtick=1),
                    yaxis=dict(title="Jumlah Kasus", showgrid=True, gridcolor='rgba(255,255,255,0.1)', zeroline=False),
                    margin=dict(l=0, r=0, t=40, b=0)
                )
                st.plotly_chart(fig_3_3, use_container_width=True, config={'displayModeBar': False})
                
                with st.expander("Lihat Data Panel: Kasus ISPA/Pneumonia (2014-2024)", expanded=False):
                    df_ts_pivot = df_ts_agg.pivot(index='tahun', columns='provinsi', values='nilai').reset_index()
                    st.dataframe(df_ts_pivot, use_container_width=True, hide_index=True)
                    st.caption("Sumber File: `sulawesi_kesehatan_detail_2014_2024.csv`")
                    
        with tab3:
            # --- 3. Fakta Data Timbulan Limbah Udara & B3 ---
            st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Narasi Anomali:</b> Data perizinan D3TLH fokus pada syarat emisi cerobong di atas kertas, tetapi mengabaikan gunung-gunung debu slag (fly ash) di darat yang bebas tertiup angin memapari puluhan desa setiap harinya. <b>Threshold Kritis: 30 Juta Ton/Tahun</b> = 7% dari total neraca B3 nasional 427 juta ton dari 1 provinsi (anomali 2,4x proporsional). Sumber: <i>KLHK LKj 2022, IKK Pengelolaan Limbah B3, Hal. 47</i>.</div>", unsafe_allow_html=True)
            
            # Gunakan nilai pre-calculated
            col_f1, col_f2, col_f3 = st.columns(3)
            col_f1.metric("Total Limbah B3 Sulteng", f"{total_b3_sulteng/1_000_000:.1f} Jt Ton/Thn", "Threshold kritis: 30 Jt Ton (KLHK LKj 2022 Hal.47)")
            col_f2.metric("Total Kasus ISPA Sentra", f"{kasus_sentra:,.0f}", "2014-2024", delta_color="inverse")
            col_f3.metric("Skor Over-Capacity B3", f"{skor_3:.1f} / 10", f"Beban: {skor_overcapacity:.1f} Jt dari 30 Jt", delta_color="inverse")
            
            st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
            
            if not df_b3.empty:
                df_b3_prov = df_b3.groupby('Provinsi')['Estimasi Timbulan (Ton/Tahun)'].sum().reset_index()
                fig_b3 = px.bar(df_b3_prov, x='Estimasi Timbulan (Ton/Tahun)', y='Provinsi', orientation='h',
                                text='Estimasi Timbulan (Ton/Tahun)', color='Estimasi Timbulan (Ton/Tahun)',
                                color_continuous_scale='Reds', title="Beban Timbulan B3 per Provinsi")
                
                # Threshold B3 = 30 Juta Ton (7% nasional dari 1 prov — KLHK LKj 2022 Hal.47)
                fig_b3.add_vline(x=30_000_000, line_dash="dot", line_color="#FF5252", annotation_text="Threshold Kritis: 30 Jt Ton (KLHK LKj 2022 Hal.47)", annotation_font_color="#FF5252", annotation_position="top left")
                
                fig_b3.update_traces(texttemplate='%{text:,.0f} ton', textposition='outside')
                fig_b3.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0))
                st.plotly_chart(fig_b3, use_container_width=True, config={'displayModeBar': False})
                
                with st.expander("Lihat Data Mentah: Timbulan Limbah B3", expanded=False):
                    st.dataframe(df_b3, use_container_width=True, hide_index=True)
                    st.caption("Sumber File: `sulawesi_limbah_b3.csv`")
                    
        with tab4:
            # --- 4. Hilangnya Paru-Paru Udara (Deforestasi CO2) ---
            st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Narasi Anomali:</b> Audit resmi pemerintah hanya menghitung 'emisi yang keluar dari corong pabrik', tetapi dengan sengaja mengaburkan 'emisi dari jutaan pohon yang mati' akibat ekspansi lahan tambang itu sendiri. <b>Threshold Kritis: 150 Juta Ton CO2e</b> = melampaui target NDC FOLU Net Sink 2030 (-140 juta ton CO2e). Sumber: <i>SK MenLHK No.SK.168/MENLHK/PKTL/PLA.1/2/2022, Bag. III, Hal. 5</i>.</div>", unsafe_allow_html=True)
            
            if not df_gfw.empty:
                df_gfw['Total_Emisi_CO2_Megagram'] = pd.to_numeric(df_gfw['Total_Emisi_CO2_Megagram'], errors='coerce').fillna(0)
                total_emisi = df_gfw['Total_Emisi_CO2_Megagram'].sum() / 1_000_000 # Juta Ton
                total_deforestasi = df_gfw['Total_Deforestasi_Ha'].sum() / 1_000 # Ribu Ha
                
                col_e1, col_e2, col_e3 = st.columns(3)
                col_e1.metric("Total Emisi CO2 Lepas", f"{total_emisi:.1f} Jt Ton", f"Threshold: 150 Jt Ton (SK.168 NDC FOLU Hal.5)")
                col_e2.metric("Total Hutan Hilang", f"{total_deforestasi:.1f} Ribu Ha", "Filter Karbon Alami", delta_color="inverse")
                col_e3.metric("Skor Defisit Ekosistem", f"{skor_4:.1f} / 10", "STATUS: DARURAT KARBON / GAGAL NDC", delta_color="inverse")
                
                st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
                
                df_emisi_trend = df_gfw.groupby(['Tahun', 'Provinsi'])['Total_Emisi_CO2_Megagram'].sum().reset_index()
                fig_emisi = px.area(df_emisi_trend, x='Tahun', y='Total_Emisi_CO2_Megagram', color='Provinsi',
                                   title="Tren Emisi Karbon Akibat Deforestasi (2014-2023)")
                # Threshold CO2 = 150 Juta Ton (>NDC FOLU -140 juta ton — SK.168/MENLHK Bag.III Hal.5)
                fig_emisi.add_hline(y=150_000_000, line_dash="dot", line_color="#FF5252",
                                   annotation_text="Threshold Kritis: 150 Jt Ton CO2e (Gagal NDC FOLU — SK.168/MENLHK)",
                                   annotation_font_color="#FF5252", annotation_position="top left")
                fig_emisi.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0))
                st.plotly_chart(fig_emisi, use_container_width=True, config={'displayModeBar': False})
                
                with st.expander("Lihat Data Panel: Emisi CO2 Deforestasi", expanded=False):
                    df_emisi_pivot = df_emisi_trend.pivot(index='Tahun', columns='Provinsi', values='Total_Emisi_CO2_Megagram').reset_index()
                    st.dataframe(df_emisi_pivot, use_container_width=True, hide_index=True)
                    st.caption("Sumber File: `sulawesi_gfw_master_1_dekade_2014_2023.csv`")

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
skor_air_1 = min(10.0, max(0, (80 - ika_sulteng) / 30) * 10)

# Skor 2: Morbiditas Diare
skor_air_2 = 0
kasus_diare_sentra = 0
kasus_diare_non = 0
rasio_diare = 0
if not df_kes.empty:
    df_diare = df_kes[df_kes['indikator'].str.contains('Diare', case=False, na=False)]
    kasus_diare_sentra = df_diare[df_diare['provinsi'].isin(['Sulawesi Tengah', 'Sulawesi Tenggara'])]['nilai'].sum()
    kasus_diare_non = df_diare[~df_diare['provinsi'].isin(['Sulawesi Tengah', 'Sulawesi Tenggara'])]['nilai'].sum()
    
    # Penduduk 2023: Sentra ~5.7M, Non-Sentra ~14.2M
    populasi_sentra = 5_700_000
    populasi_non = 14_200_000
    
    ir_sentra = (kasus_diare_sentra / populasi_sentra) * 1000
    ir_non = (kasus_diare_non / populasi_non) * 1000 if populasi_non > 0 else 1
    
    rasio_diare = ir_sentra / ir_non if ir_non > 0 else 0
    skor_air_2 = min(10.0, max(0.0, (rasio_diare - 1) * 10.0))

# Skor 3: Konflik Air/Pesisir
skor_air_3 = 0
jumlah_konflik_air = 0
luas_konflik_air = 0
df_konflik_air = pd.DataFrame()
if not df_konflik.empty:
    keywords = 'air|laut|pesisir|nelayan|sungai|pulau|tailing'
    df_konflik_air = df_konflik[df_konflik['sektor'].str.contains(keywords, case=False, na=False) | 
                                df_konflik['judul'].str.contains(keywords, case=False, na=False) | 
                                df_konflik['deskripsi'].str.contains(keywords, case=False, na=False)]
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

colB1, colB2 = st.columns([1, 2])
with colB1:
    st.markdown(f"""
<div style="background:#2C3E50; padding:20px; border-radius:10px; border-left:5px solid #E74C3C; height:100%;">
<h4 style="color:#FFF; margin-top:0;">Audit D3TLH: Daya Tampung Air</h4>
<p style="color:#BDC3C7; font-size:0.9rem;">"Pembuangan tailing diizinkan selama beban cemaran sungai/laut masih secara teori mampu mengencerkan."</p>
<hr style="border-color:#34495E;">
<h4 style="color:#E74C3C;">Fakta Forensik ECC:</h4>
<p style="color:#E0E0E0; font-size:0.9rem;">Penurunan drastis Indeks Kualitas Air dan hancurnya pesisir ditandai ledakan morbiditas air.</p>
<div style="background-color: #1A202C; padding: 15px; border-radius: 8px; margin-top: 15px; text-align: center; border: 1px solid #E74C3C;">
<div style="font-size: 11px; color: #BDC3C7; text-transform: uppercase; letter-spacing: 1px;">Akumulasi Skor Kerusakan</div>
<div style="font-size: 32px; font-weight: 800; color: #E74C3C; line-height: 1.2;">{skor_akumulasi_air:.1f} <span style="font-size: 16px;">/ 10</span></div>
<div style="font-size: 11px; color: #E74C3C; margin-top: 5px; font-weight: bold;">STATUS: DAYA TAMPUNG JEBOL</div>
</div>
<div style="background:#C0392B; color:white; padding:5px 10px; border-radius:5px; font-weight:bold; text-align:center; margin-top:15px;">
VONIS: Kegagalan Pengukuran Toksisitas
</div>
</div>
""", unsafe_allow_html=True)

with colB2:
    tab_w1, tab_w2, tab_w3, tab_w4 = st.tabs(["Kualitas Air", "Morbiditas Diare", "Konflik Nelayan", "Beban Tailing"])
    
    with tab_w1:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Narasi Anomali:</b> Klaim sungai/laut mampu mengencerkan limbah berbanding terbalik dengan hancurnya Indeks Kualitas Air BPS hingga menyentuh batas cemar kotor.</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("IKA Sulteng Terkini", f"{ika_sulteng:.1f}", "Indeks BPS", delta_color="inverse")
        col2.metric("Rata-rata IKA Sulawesi", f"{ika_terkini:.1f}", "Skala 0-100", delta_color="inverse")
        col3.metric("Skor Kualitas Air", f"{skor_air_1:.1f} / 10", "STATUS: CEMAR KRITIS", delta_color="inverse")
        st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
        
        if not df_ika.empty:
            df_ika_long = df_ika.rename(columns={'Indeks Kualitas Air': 'Nilai IKA'})
            fig_w1 = px.line(df_ika_long, x='Tahun', y='Nilai IKA', color='Provinsi', markers=True,
                           title="Runtuhnya Indeks Kualitas Air (IKA) di Area Sentra Nikel")
            fig_w1.add_hline(y=50, line_dash="dot", annotation_text="Batas Kritis Cemar (50)", annotation_position="bottom right", line_color="#E74C3C")
            fig_w1.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_w1, use_container_width=True, config={'displayModeBar': False})
            
    with tab_w2:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Narasi Anomali:</b> AMDAL gagal menghitung dampak kontaminasi logam berat ke air tanah yang dikonsumsi warga, dibuktikan dengan ledakan pasien Diare di lingkar tambang. <b>Threshold Kritis: Incidence Rate Ratio (IRR) > 2.0</b> (Risiko 2x lipat dari populasi rata-rata). Sumber: <i>Kemenkes Profil Kesehatan 2023, Hal. 112</i>.</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Kasus Diare Sentra Nikel", f"{kasus_diare_sentra:,.0f}", "Sulteng & Sultra")
        col2.metric("Kasus Diare Daerah Lain", f"{kasus_diare_non:,.0f}", "4 Provinsi Non-Sentra", delta_color="normal")
        col3.metric("Skor Beban Penyakit", f"{skor_air_2:.1f} / 10", f"IRR: {rasio_diare:.1f}x Lipat", delta_color="inverse")
        st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
        
        if not df_kes.empty:
            df_diare_trend = df_diare.copy()
            df_diare_trend['Kategori'] = df_diare_trend['provinsi'].apply(lambda x: 'Sentra Tambang' if x in ['Sulawesi Tengah', 'Sulawesi Tenggara'] else 'Non-Sentra')
            df_d_agg = df_diare_trend.groupby(['tahun', 'Kategori'])['nilai'].sum().reset_index()
            fig_w2 = px.area(df_d_agg, x='tahun', y='nilai', color='Kategori', title="Ledakan Kasus Diare (Indikator Kualitas Air Tanah)")
            fig_w2.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_w2, use_container_width=True, config={'displayModeBar': False})

    with tab_w3:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Narasi Anomali:</b> Ekosistem tangkap nelayan dihancurkan oleh limbah tailing dan privatisasi pesisir untuk Smelter, memicu lonjakan konflik agraria laut.</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Konflik Pesisir/Air", f"{jumlah_konflik_air} Kasus", "Data TanahKita")
        col2.metric("Estimasi Luas Terdampak", f"{luas_konflik_air:,.0f} Ha", "Ruang Hidup Nelayan", delta_color="inverse")
        col3.metric("Skor Konflik Ruang Air", f"{skor_air_3:.1f} / 10", "STATUS: DARURAT AGRARIA", delta_color="inverse")
        st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
        
        if not df_konflik_air.empty and 'Tahun' in df_konflik_air.columns:
            df_k_trend = df_konflik_air.groupby('Tahun').size().reset_index(name='Jumlah')
            fig_w3 = px.bar(df_k_trend, x='Tahun', y='Jumlah', title="Frekuensi Letusan Konflik Pesisir & Nelayan per Tahun")
            fig_w3.add_vline(x=2015, line_dash="dot", line_color="#E74C3C", annotation_text="Awal Eskalasi Smelter")
            fig_w3.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_w3, use_container_width=True, config={'displayModeBar': False})

    with tab_w4:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Narasi Anomali:</b> Resiko kebocoran Tailings Dam (Bendungan Tailing) atau Deep Sea Tailing Placement (DSTP) yang ditutupi oleh klaim 'mitigasi teknologi'. <b>Threshold Kritis: 25 Juta Ton/Tahun</b> (Batas Kapasitas AMDAL Gabungan Kawasan IMIP & OSS). Sumber: <i>Dokumen AMDAL KLHK, PPID</i>.</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Timbulan Tailing/B3", f"{total_tailing_sulteng/1_000_000:.1f} Jt Ton", "Mayoritas Slag/Tailing Sulteng")
        col2.metric("Titik Resiko", "Smelter & Laut Dalam", "DSTP & Tailing Dam", delta_color="inverse")
        col3.metric("Skor Ancaman Tailing", f"{skor_air_4:.1f} / 10", f"AMDAL Limit: 25 Jt Ton", delta_color="inverse")
        st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
        
        if not df_b3.empty:
            fig_w4 = px.treemap(df_b3, path=['Provinsi', 'Kawasan/Perusahaan'], values='Estimasi Timbulan (Ton/Tahun)', 
                                color='Estimasi Timbulan (Ton/Tahun)', color_continuous_scale='Blues',
                                title="Proporsi Beban Limbah Tailing & B3 ke Ekosistem Air")
            fig_w4.update_layout(template="plotly_dark", margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_w4, use_container_width=True, config={'displayModeBar': False})

st.markdown("<br>", unsafe_allow_html=True)



# ---------------------------------------------------------
# C. MITOS DEFORESTASI VS BENCANA ALAM (DAYA DUKUNG LAHAN)
# ---------------------------------------------------------
colC1, colC2 = st.columns([1, 2])
with colC1:
    st.markdown(f'''
    <div style="background:#2C3E50; padding:20px; border-radius:10px; border-left:5px solid #E74C3C; height:100%;">
        <h4 style="color:#FFF; margin-top:0;">Audit D3TLH: Daya Dukung Lahan</h4>
        <p style="color:#BDC3C7; font-size:0.9rem;">"Daya dukung lahan dan tata air tanah dinilai aman secara matematis karena rasio ekoregion hutan dianggap masih mencukupi."</p>
        <hr style="border-color:#34495E;">
        <h4 style="color:#E74C3C;">Fakta Forensik ECC:</h4>
        <p style="color:#E0E0E0; font-size:0.9rem;">Hancurnya sabuk hijau alam memicu rentetan bencana hidrometeorologi parah di lingkar tambang, menabrak batas fungsi kawasan lindung.</p>
        <div style="background-color: #1A202C; padding: 15px; border-radius: 8px; margin-top: 15px; text-align: center; border: 1px solid #E74C3C;">
            <div style="font-size: 11px; color: #BDC3C7; text-transform: uppercase; letter-spacing: 1px;">Skor Kerusakan Lahan</div>
            <div style="font-size: 32px; font-weight: 800; color: #E74C3C; line-height: 1.2;">{skor_akumulasi_lahan:.1f} <span style="font-size: 16px;">/ 10</span></div>
            <div style="font-size: 11px; color: #E74C3C; margin-top: 5px; font-weight: bold;">STATUS: KRISIS RUANG DARAT</div>
        </div>
        <div style="background:#C0392B; color:white; padding:5px 10px; border-radius:5px; font-weight:bold; text-align:center; margin-top:15px;">
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
            fig_l1.add_hline(y=88, line_dash="dash", line_color="#E74C3C", annotation_text="Batas Darurat Bencana (88/Tahun)", annotation_position="top left")
            fig_l1.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_l1, use_container_width=True, config={'displayModeBar': False})
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
            fig_l2.add_hline(y=63800, line_dash="dash", line_color="#E74C3C", annotation_text="Batas Kritis Tahunan (63.800 Ha)", annotation_position="bottom right")
            fig_l2.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_l2, use_container_width=True, config={'displayModeBar': False})
            with st.expander("Tampilkan Data Mentah (Global Forest Watch)"):
                st.dataframe(df_gfw, use_container_width=True)

    with tab_l3:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Narasi Anomali:</b> Temuan <b>paling mematikan</b>: Data GFW membuktikan bahwa <b>100% dari setiap Ha deforestasi</b> yang terjadi di Sulteng dan Sultra selama 10 tahun (2014–2023) terjadi di dalam <b>Kawasan Lindung / Protected Areas (IUCN)</b>. Tidak ada satu pun hektar yang dibabat di luar batas kawasan yang seharusnya tidak boleh disentuh.</div>", unsafe_allow_html=True)
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
            st.plotly_chart(fig_l3, use_container_width=True, config={'displayModeBar': False})
            with st.expander("Tampilkan Data Mentah Kawasan Lindung (GFW)"):
                st.dataframe(df_gfw_lindung, use_container_width=True)

    with tab_l4:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Narasi Anomali:</b> Data atribusi GFW mematahkan alibi 'ladang berpindah'. Pertambangan dan Sawit adalah aktor dominan penghancur hutan. ⚠️ <i>Catatan: Data GFW untuk Sulteng absen/kosong, angka setengah juta hektar ini MURNI dari Sulawesi Tenggara saja.</i></div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Aktor Komoditas (Tambang/Sawit)", f"{tambang_driver_ha:,.0f} Ha", "Sultra Saja (Data GFW)")
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
            st.plotly_chart(fig_l4, use_container_width=True, config={'displayModeBar': False})
            with st.expander("Tampilkan Data Mentah Drivers (GFW)"):
                st.dataframe(df_gfw_driver, use_container_width=True)


st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# D. MITOS KEDAULATAN RUANG VS KONFLIK SOSIAL (DAYA DUKUNG SOSIAL)
# ---------------------------------------------------------
colD1, colD2 = st.columns([1, 2])
with colD1:
    st.markdown(f'''
    <div style="background:#2C3E50; padding:20px; border-radius:10px; border-left:5px solid #E74C3C; height:100%;">
        <h4 style="color:#FFF; margin-top:0;">Audit D3TLH: Daya Dukung Sosial</h4>
        <p style="color:#BDC3C7; font-size:0.9rem;">"Status kawasan dialokasikan untuk peruntukan tambang dengan klaim bahwa masyarakat telah memberikan persetujuan (FPIC) dalam sosialisasi amdal."</p>
        <hr style="border-color:#34495E;">
        <h4 style="color:#E74C3C;">Fakta Forensik ECC:</h4>
        <p style="color:#E0E0E0; font-size:0.9rem;">Alur penindasan terbukti jelas: Persetujuan dimanipulasi, ruang hidup jutaan hektar dirampas, dan penolakan dibungkam dengan bui.</p>
        <div style="background-color: #1A202C; padding: 15px; border-radius: 8px; margin-top: 15px; text-align: center; border: 1px solid #E74C3C;">
            <div style="font-size: 11px; color: #BDC3C7; text-transform: uppercase; letter-spacing: 1px;">Skor Kerusakan Sosial</div>
            <div style="font-size: 32px; font-weight: 800; color: #E74C3C; line-height: 1.2;">{skor_akumulasi_sosial:.1f} <span style="font-size: 16px;">/ 10</span></div>
            <div style="font-size: 11px; color: #E74C3C; margin-top: 5px; font-weight: bold;">STATUS: KRISIS KEMANUSIAAN</div>
        </div>
        <div style="background:#C0392B; color:white; padding:5px 10px; border-radius:5px; font-weight:bold; text-align:center; margin-top:15px;">
            VONIS: Ilusi Kedaulatan Ruang Warga
        </div>
    </div>
    ''', unsafe_allow_html=True)

with colD2:
    tab_s1, tab_s2, tab_s3, tab_s4 = st.tabs(["Manipulasi Persetujuan FPIC", "Perampasan Ruang Hidup", "Kriminalisasi Warga", "Defisit Layanan Dasar"])
    
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
                st.plotly_chart(fig_s1, use_container_width=True, config={'displayModeBar': False})

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
                st.plotly_chart(fig_s2, use_container_width=True, config={'displayModeBar': False})
                with st.expander("Tampilkan Data Indikasi Kriminalisasi"):
                    st.dataframe(krim_df[['tahun', 'judul', 'sektor', 'jumlah_ditangkap', 'jumlah_luka']], use_container_width=True)

    with tab_s4:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Narasi Anomali:</b> Di tengah ekspor nikel sentra Sulawesi yang meledak ratusan kali lipat, kualitas layanan dasar hancur. Mayoritas Puskesmas gagal memenuhi standar minimal <b>Sarana, Prasarana, dan Alat Kesehatan (SPA)</b>. Klaim AMDAL tentang 'peningkatan kesejahteraan' adalah fiksi belaka.</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Target SPA (RPJMN 2025-2029)", f"{target_rpjmn} %", "Standar Minimal Kemenkes")
        col2.metric("Aktual SPA Sulteng & Sultra", f"{spa_aktual_pct} %", f"Gap Kritis: -{target_rpjmn - spa_aktual_pct}%", delta_color="inverse")
        col3.metric("Skor Defisit Faskes", f"{skor_sosial_4:.1f} / 10", "STATUS: PARADOKS BOOM MINERAL", delta_color="inverse")
        st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
        
        if not df_faskes.empty:
            df_f_plot = df_faskes[df_faskes['provinsi'].isin(['Sulawesi Tengah', 'Sulawesi Tenggara'])].copy()
            df_f_plot['jumlah'] = pd.to_numeric(df_f_plot['jumlah'], errors='coerce').fillna(0)
            df_f_plot['tahun'] = pd.to_numeric(df_f_plot['tahun'], errors='coerce')
            df_f_agg = df_f_plot.groupby(['tahun', 'provinsi'])['jumlah'].sum().reset_index()
            fig_s4 = px.line(df_f_agg, x='tahun', y='jumlah', color='provinsi', markers=True,
                            title="Ironi: Tren Jumlah Fisik Faskes vs Boom Ekspor Nikel (2014-2024)",
                            color_discrete_map={'Sulawesi Tengah': '#27AE60', 'Sulawesi Tenggara': '#3498DB'})
            fig_s4.add_annotation(x=2024, y=df_f_agg['jumlah'].max(), text=f"Meski unit bertambah, standar SPA mentok di {spa_aktual_pct}% (Target RPJMN 80%)", showarrow=False, yshift=20, font=dict(color="#E74C3C"))
            fig_s4.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_s4, use_container_width=True, config={'displayModeBar': False})
            with st.expander("Tampilkan Data Unit Faskes Fisik (Kemenkes)"):
                st.dataframe(df_f_plot, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)


# ---------------------------------------------------------
# E. MITOS TATA KELOLA VS OBRAL IZIN (VETO KEBIJAKAN)
# ---------------------------------------------------------
colE1, colE2 = st.columns([1, 2])
with colE1:
    st.markdown(f'''
    <div style="background:#2C3E50; padding:20px; border-radius:10px; border-left:5px solid #E74C3C; height:100%;">
        <h4 style="color:#FFF; margin-top:0;">Audit D3TLH: Veto Kebijakan</h4>
        <p style="color:#BDC3C7; font-size:0.9rem;">"Penyusunan D3TLH adalah dokumen sakti (veto) yang dapat membatasi izin eksploitasi jika daya dukung lingkungan telah terlampaui."</p>
        <hr style="border-color:#34495E;">
        <h4 style="color:#E74C3C;">Fakta Forensik ECC:</h4>
        <p style="color:#E0E0E0; font-size:0.9rem;">Negara mengalami kelumpuhan tata kelola (Regulatory Capture). Izin diobral massal, perusahaan ilegal dibiarkan, dan infrastruktur energi kotor diloloskan di episentrum krisis.</p>
        <div style="background-color: #1A202C; padding: 15px; border-radius: 8px; margin-top: 15px; text-align: center; border: 1px solid #E74C3C;">
            <div style="font-size: 11px; color: #BDC3C7; text-transform: uppercase; letter-spacing: 1px;">Skor Kegagalan Tata Kelola</div>
            <div style="font-size: 32px; font-weight: 800; color: #E74C3C; line-height: 1.2;">{skor_akumulasi_veto:.1f} <span style="font-size: 16px;">/ 10</span></div>
            <div style="font-size: 11px; color: #E74C3C; margin-top: 5px; font-weight: bold;">STATUS: REGULATORY CAPTURE</div>
        </div>
        <div style="background:#C0392B; color:white; padding:5px 10px; border-radius:5px; font-weight:bold; text-align:center; margin-top:15px;">
            VONIS: Kegagalan Supremasi Hukum
        </div>
    </div>
    ''', unsafe_allow_html=True)

with colE2:
    tab_v1, tab_v2, tab_v3 = st.tabs(["Obral Konsesi Legal", "Pembiaran Pelanggaran", "Karpet Merah Energi Kotor"])
    
    with tab_v1:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Narasi Anomali:</b> Di tengah memuncaknya status krisis daya dukung lingkungan, pemerintah secara paradoks justru menerbitkan ratusan izin eksploitasi tambang (IUP) baru. Dokumen veto tidak berfungsi.</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Obral IUP Baru (Sejak 2014)", f"{izin_baru:.0f} Izin", "Eksploitasi Meluas", delta_color="inverse")
        col2.metric("Skor Paradoks Izin", f"{skor_veto_1:.1f} / 10", "STATUS: VETO GAGAL", delta_color="inverse")
        col3.metric("Fungsi Pembatasan", "Nihil", "Hanya Formalitas", delta_color="inverse")
        st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
        
        if not df_izin.empty:
            df_izin_plot = df_izin[df_izin['Tahun'] >= 2014].copy()
            fig_v1 = px.bar(df_izin_plot, x='Tahun', y='Jumlah_Izin_Baru', title="Lonjakan Penerbitan IUP di Era Krisis Lingkungan", color_discrete_sequence=['#E67E22'])
            fig_v1.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_v1, use_container_width=True, config={'displayModeBar': False})
            with st.expander("Tampilkan Data Penerbitan Izin (Ditjen Minerba)"):
                st.dataframe(df_izin_plot, use_container_width=True)

    with tab_v2:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Narasi Anomali:</b> Bukti mutlak 'Regulatory Capture'—bahkan ketika perusahaan beroperasi ilegal, menabrak izin, tumpang tindih, atau HGU kedaluwarsa, negara tidak berani melakukan penegakan hukum dan membiarkannya.</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Perusahaan Melanggar Hukum", f"{perusahaan_ilegal} Korporat", "Hukum Tumpul", delta_color="inverse")
        col2.metric("Tindakan Tegas Negara", "0", "Pembiaran Sistematis", delta_color="inverse")
        col3.metric("Skor Impunitas", f"{skor_veto_2:.1f} / 10", "STATUS: NEGARA LUMPUH", delta_color="inverse")
        st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
        
        if not df_kpa_izin.empty:
            st.dataframe(df_kpa_izin[['nama_perusahaan', 'jenis_masalah_izin', 'lokasi']], use_container_width=True, hide_index=True)
            with st.expander("Tampilkan Detail Kasus (KPA)"):
                st.dataframe(df_kpa_izin, use_container_width=True)

    with tab_v3:
        st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Narasi Anomali:</b> Inkonsistensi paling telanjang terhadap komitmen iklim. Di wilayah ekoregion krisis, pemerintah memberikan karpet merah pembangunan infrastruktur penyumbang emisi terbesar (PLTU Batubara Captive) khusus untuk menyuplai kawasan smelter nikel.</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Kapasitas PLTU Captive", f"{kapasitas_pltu/1000:.1f} GW", "Energi Kotor Masif", delta_color="inverse")
        col2.metric("Dampak Ekologi", "Emisi & Abu Beracun", "Mematikan", delta_color="inverse")
        col3.metric("Skor Inkonsistensi Iklim", f"{skor_veto_3:.1f} / 10", "STATUS: HYPOCRISY", delta_color="inverse")
        st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
        
        if not df_pltu_captive.empty:
            pltu_status = df_pltu_captive.groupby('Status').size().reset_index(name='jumlah')
            fig_v3 = px.pie(pltu_status, names='Status', values='jumlah', title="Proporsi Status PLTU Batubara Captive di Sulawesi", hole=0.4, color_discrete_sequence=px.colors.sequential.Oranges_r)
            fig_v3.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_v3, use_container_width=True, config={'displayModeBar': False})
            with st.expander("Tampilkan Data PLTU Captive (Global Energy Monitor)"):
                st.dataframe(df_pltu_captive[['Plant name', 'Owner', 'Status', 'Capacity (MW)']], use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

