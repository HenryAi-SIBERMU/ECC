import streamlit as st
import pandas as pd
import numpy as np
import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.components.sidebar import render_sidebar

st.set_page_config(page_title="Poster Viral: 12 Fakta Ekologis", page_icon="refrensi/Celios China-Indonesia Energy Transition.png", layout="wide", initial_sidebar_state="expanded")
render_sidebar()

# --- Data Loading (Reusing logic from 12_Infografis_Summary) ---
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data", "processed")

@st.cache_data
def load_data():
    try:
        # Koreksi Omnibus Law: Bandingkan rata-rata sebelum (2014-2020) dan sesudah (2021-2024)
        df_izin = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_izin_baru_per_tahun.csv"))
        pre_omnibus = df_izin[df_izin['Tahun'] <= 2020]['Jumlah_Izin_Baru'].sum() / 7  # 7 tahun (2014-2020)
        post_omnibus = df_izin[df_izin['Tahun'] >= 2021]['Jumlah_Izin_Baru'].sum() / 4 # 4 tahun (2021-2024)
        lonjakan_izin = f"+{((post_omnibus - pre_omnibus) / pre_omnibus) * 100:,.0f}%"
    except:
        lonjakan_izin = "+475%"
        
    try:
        df_hukum = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_konflik_hukum.csv"))
        df_kpa = pd.read_csv(os.path.join(DATA_DIR, "kpa_masalah_izin_perusahaan.csv"))
        izin_hantu = f"{len(df_hukum) + len(df_kpa)} Korporasi"
    except:
        izin_hantu = "53 Korporasi"

    try:
        df_lindung = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_gfw_kawasan_lindung_loss_2014_2023.csv"))
        lindung = df_lindung['Luas_Hilang_Kawasan_Lindung_Ha'].sum()
        kawasan_lindung = f"{lindung / 1000:,.0f} Ribu Ha"
    except:
        kawasan_lindung = "2,079 Ribu Ha"
        
    try:
        df_limbah = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_limbah_b3.csv"))
        limbah = pd.to_numeric(df_limbah['Estimasi Timbulan (Ton/Tahun)'].astype(str).str.replace(',', '').str.replace('.', ''), errors='coerce').sum()
        limbah_val = f"{limbah / 1_000_000:,.0f} Juta Ton"
    except:
        limbah_val = "35 Juta Ton"

    try:
        df_prim = pd.read_csv(os.path.join("data", "raw", "klhk_gfw", "mega_fetch_v2", "primary_forest_loss_sulawesi_2001_2025.csv"))
        prim = df_prim[df_prim['is__umd_regional_primary_forest_2001'] == True]['area__ha'].sum()
        hutan_primer = f"{prim / 1_000_000:,.1f} Juta Ha"
    except:
        hutan_primer = "15.4 Juta Ha"
        
    try:
        df_iucn = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_biodiversitas_iucn_fase5_exploded.csv"))
        spesies = df_iucn[df_iucn['Mining Threat'] == 'Yes']['Scientific Name'].nunique()
        kepunahan = f"{spesies} Spesies Kunci"
    except:
        kepunahan = "4 Spesies Kunci"
        
    try:
        df_bencana = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_bencana_bnpb_2014_2024.csv"))
        bencana = df_bencana['jumlah_kejadian'].sum()
        bencana_val = f"{bencana:,.0f} Bencana"
    except:
        bencana_val = "1,557 Bencana"
    try:
        df_kes = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_kesehatan_detail_2014_2024.csv"))
        ispa = df_kes[df_kes['indikator'] == 'Kasus ISPA/Pneumonia']['nilai'].sum()
        ispa_val = f"{ispa / 1000:,.0f} Ribu Pasien"
        
        diare = df_kes[df_kes['indikator'] == 'Kasus Diare Dilayani']['nilai'].sum()
        diare_val = f"{diare / 1000:,.0f} Ribu Pasien"
    except:
        ispa_val = "233 Ribu Pasien"
        diare_val = "145 Ribu Pasien"

    try:
        df_zoo = pd.read_csv(os.path.join(DATA_DIR, "zoonosis_kab_kota_2015_2024.csv"))
        zoo = df_zoo['total_kasus'].sum()
        zoo_val = f"{zoo:,.0f} Kasus"
    except:
        zoo_val = "31,738 Kasus"

    try:
        df_no2 = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_tropomi_no2_bbox_aggregates.csv"))
        no2_max = df_no2['mean'].max() * 1000000  # convert scale
        no2_val = f"Pekat (Satelit)"
    except:
        no2_val = "Pekat"

        
    try:
        df_konf = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_konflik_agraria_tanahkita.csv"))
        konflik = len(df_konf)
        konflik_val = f"{konflik} Kasus"
    except:
        konflik_val = "84 Kasus"
        
    try:
        df_pltu = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_pltu_captive.csv"))
        pltu = df_pltu['Capacity (MW)'].sum()
        pltu_val = f"{pltu:,.0f} MW"
    except:
        pltu_val = "12,245 MW"

    # --- Seksi 3: Paradoks Investasi & Hukum ---

    # Investasi Asing
    try:
        df_inv = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_investasi_nikel.csv"))
        total_inv = df_inv['investment_usd_million'].sum()
        asing_inv = df_inv[~df_inv['company'].str.contains('Merdeka|Indonesia|Harita|Vale', case=False, na=False)]['investment_usd_million'].sum()
        pct_asing = (asing_inv / total_inv) * 100 if total_inv > 0 else 85
        investasi_asing = f"{pct_asing:.0f}% Asing"
    except:
        investasi_asing = "85% Asing"

    # Sungai Tercemar
    try:
        df_sungai = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_sungai_tercemar.csv"))
        total_sungai = df_sungai['Jumlah_Sungai_Tercemar'].sum()
        sungai_tercemar = f"{int(total_sungai)} Sungai Tercemar"
    except:
        sungai_tercemar = "8 Sungai Tercemar"

    # Konflik FPIC / Pelanggaran Hak Adat
    try:
        df_fpic = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_konflik_tambang_fpic.csv"))
        kecelakaan_tambang = f"{len(df_fpic)} Konflik FPIC"
    except:
        kecelakaan_tambang = "12 Konflik FPIC"

    # Total Luas Konsesi Nikel (tumpang tindih)
    try:
        df_kaw = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_kawasan_nikel_luas.csv"))
        total_ha = df_kaw['total_luas_ha'].sum()
        tumpang_tindih = f"{total_ha / 1_000_000:.1f} Juta Ha"
    except:
        tumpang_tindih = "851 Ribu Ha"

    # IUP Ilegal (Moratorium dilanggar)
    try:
        df_ilegal = pd.read_csv(os.path.join(DATA_DIR, "kpa_catahu_2025_izin_ilegal_sulawesi.csv"))
        moratorium = f"{len(df_ilegal)} IUP Ilegal"
    except:
        moratorium = "112 IUP Ilegal"

    # Pertanian (Kiamat Pertanian)
    try:
        df_pdrb = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_pdrb_sektoral_2016_2024.csv"))
        agri = df_pdrb[df_pdrb['sektor_kode'] == 'A']
        agri_2016 = agri[agri['tahun'] == 2016]['pct_dari_total'].mean()
        agri_2024 = agri[agri['tahun'] == 2024]['pct_dari_total'].mean()
        drop = agri_2016 - agri_2024
        pertanian = f"Turun {drop:.1f}%"
    except:
        pertanian = "Anjlok 10%"

    # Dominasi PDRB Ekstraktif (Tambang & Industri Pengolahan)
    try:
        df_pdrb = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_pdrb_sektoral_2016_2024.csv"))
        df_2024 = df_pdrb[df_pdrb['tahun'] == df_pdrb['tahun'].max()]
        total_pdrb = df_2024['nilai_miliar_rp'].sum()
        ekstraktif_val = df_2024[df_2024['sektor_kode'].isin(['B','C'])]['nilai_miliar_rp'].sum()
        pct_ext = (ekstraktif_val / total_pdrb) * 100 if total_pdrb > 0 else 58
        pdrb = f"{pct_ext:.0f}%"
    except:
        pdrb = "58%"

    # Kecepatan Izin Pasca Omnibus (IUP diterbitkan setelah 2020)
    try:
        df_izin = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_izin_baru_per_tahun.csv"))
        post_omnibus = df_izin[df_izin['Tahun'] > 2020]['Jumlah_Izin_Baru'].sum()
        kecepatan_izin = f"{int(post_omnibus)} IUP Kilat"
    except:
        kecepatan_izin = "Kebut 9 Hari"

    return {
        "lonjakan_izin": lonjakan_izin,
        "izin_hantu": izin_hantu,
        "kawasan_lindung": kawasan_lindung,
        "limbah_val": limbah_val,
        "hutan_primer": hutan_primer,
        "kepunahan": kepunahan,
        "bencana_val": bencana_val,
        "ispa_val": ispa_val,
        "diare_val": diare_val,
        "zoo_val": zoo_val,
        "no2_val": no2_val,
        "konflik_val": konflik_val,
        "pltu_val": pltu_val,
        "pertanian": pertanian,
        "pdrb": pdrb,
        "investasi_asing": investasi_asing,
        "sungai_tercemar": sungai_tercemar,
        "kecelakaan_tambang": kecelakaan_tambang,
        "tumpang_tindih": tumpang_tindih,
        "moratorium": moratorium,
        "kecepatan_izin": kecepatan_izin,
    }

data = load_data()

import base64
logo_path = os.path.join(BASE_DIR, "refrensi", "logo.png")
try:
    with open(logo_path, "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode()
    logo_html = f'<img src="data:image/png;base64,{logo_b64}" alt="CELIOS Logo" style="height: 110px; margin: 0 auto 20px auto; display:block; filter: brightness(0) invert(1); opacity: 0.95;">'
except Exception as e:
    logo_html = ''

html1 = f"""
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap" rel="stylesheet">

<style>
    .font-inter {{ font-family: 'Inter', sans-serif; }}
    
    .poster-container {{
        background-color: #215e39; /* Hijau dasar CELIOS */
        background-image: 
            linear-gradient(rgba(255, 255, 255, 0.07) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.07) 1px, transparent 1px);
        background-size: 50px 50px;
    }}
    
    .card-title-text {{
        color: #215e39;
        font-weight: 700;
        font-size: 0.95rem;
    }}
    
    .card-value-text {{
        color: #215e39;
        font-weight: 800;
        font-size: 3.5rem;
        line-height: 1.1;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }}
    
    .card-desc-text {{
        color: #555555;
        font-size: 0.75rem;
        line-height: 1.3;
        font-weight: 400;
        padding-left: 0.5rem;
        padding-right: 0.5rem;
    }}
</style>

<div class="poster-container font-inter w-full min-h-screen p-8 md:p-12 lg:p-16 relative overflow-hidden">
    
    <!-- BACKGROUND ACCENTS -->
    <div class="absolute" style="top: -150px; right: -100px; width: 500px; height: 500px; border-radius: 50%; border: 40px solid rgba(255, 232, 124, 0.08); z-index: 0; pointer-events: none;"></div>
    <div class="absolute" style="bottom: 10%; left: -200px; width: 600px; height: 600px; border-radius: 50%; border: 60px solid rgba(255, 232, 124, 0.06); z-index: 0; pointer-events: none;"></div>
    <div class="absolute" style="top: 30%; left: 5%; font-size: 150px; color: rgba(255, 232, 124, 0.08); z-index: 0; font-weight: 900; line-height: 1; pointer-events: none;">+</div>
    <div class="absolute" style="bottom: 20%; right: 10%; font-size: 200px; color: rgba(255, 232, 124, 0.06); z-index: 0; font-weight: 900; line-height: 1; pointer-events: none;">+</div>

    <!-- MAIN CONTENT -->
    <div class="relative z-10 w-full">
        <!-- HEADER -->
    <div class="text-center mb-12 mt-4 flex flex-col items-center justify-center">
        {logo_html}
        <h1 class="text-white text-4xl md:text-5xl font-bold tracking-wide mb-3">Temuan Utama</h1>
        <p style="color: rgba(255,255,255,0.75); font-size: 1rem; font-weight: 500; max-width: 600px; margin: 0 auto; letter-spacing: 0.02em;">Daya Dukung &amp; Daya Tampung Lingkungan Hidup (D3TLH) — Sulawesi 2014–2024</p>
    </div>

    
    <!-- SEKSI 1: DARURAT KESEHATAN PUBLIK -->
    <div class="w-full text-center font-bold text-xl md:text-2xl py-3 rounded-full mb-8 shadow-sm" style="background-color: #FFE87C; color: #215e39;">
        Darurat Kesehatan Publik
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-3 gap-5 mb-14">
        
        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Beban Penyakit ISPA</div>
            <div class="card-value-text">{data['ispa_val']}</div>
            <div class="card-desc-text">Warga lingkar tambang (Konawe/Morowali) dipaksa menghirup udara mematikan setiap hari</div>
        </div>
        
        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Kasus Diare Akut</div>
            <div class="card-value-text">{data['diare_val']}</div>
            <div class="card-desc-text">Krisis air bersih dan hancurnya sanitasi akibat sumber air tanah tercemar berat</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Penyakit Tropis & Zoonosis</div>
            <div class="card-value-text">{data['zoo_val']}</div>
            <div class="card-desc-text">Kasus Demam Berdarah dan Malaria meroket imbas deforestasi hutan yang agresif</div>
        </div>
        
    </div>

    <!-- SEKSI 2: EKSPLOITASI & KEJAHATAN EKOLOGIS -->
    <div class="w-full text-center font-bold text-xl md:text-2xl py-3 rounded-full mb-8 shadow-sm" style="background-color: #FFE87C; color: #215e39;">
        Eksploitasi & Kejahatan Ekologis
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 mb-14">
        
        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Lonjakan Gila Izin Tambang</div>
            <div class="card-value-text">{data['lonjakan_izin']}</div>
            <div class="card-desc-text">Pasca-pandemi dan Omnibus Law, perizinan diobral tanpa rem dan daya dukung lingkungan</div>
        </div>
        
        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Sindikasi Izin Hantu & Ilegal</div>
            <div class="card-value-text">{data['izin_hantu']}</div>
            <div class="card-desc-text">Beroperasi secara ilegal dan kebal hukum di dalam kawasan hutan tanpa sanksi tegas</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Kawasan Lindung Dihancurkan</div>
            <div class="card-value-text">{data['kawasan_lindung']}</div>
            <div class="card-desc-text">Area konservasi sakral yang secara legal dirobek dan dicaplok demi memuluskan megaproyek</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Gunung Limbah Beracun</div>
            <div class="card-value-text">{data['limbah_val']}</div>
            <div class="card-desc-text">Bom waktu limbah B3 dan tailing nikel yang meracuni pesisir dan mematikan ekosistem laut</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Hutan Primer Purba Musnah</div>
            <div class="card-value-text">{data['hutan_primer']}</div>
            <div class="card-desc-text">Hilangnya kanopi hutan perawan yang mustahil untuk direklamasi dan dikembalikan fungsinya</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Ancaman Kepunahan Satwa</div>
            <div class="card-value-text">{data['kepunahan']}</div>
            <div class="card-desc-text">Satwa endemik Sulawesi didorong paksa ke jurang kepunahan massal dalam Daftar Merah IUCN</div>
        </div>
        
    </div>

    <!-- SEKSI 3: PENDERITAAN WARGA & PARADOKS EKONOMI -->
    <div class="w-full text-center font-bold text-xl md:text-2xl py-3 rounded-full mb-8 shadow-sm" style="background-color: #FFE87C; color: #215e39;">
        Penderitaan Warga & Paradoks Ekonomi
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 mb-8">
        
        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Ledakan Bencana Ekologis</div>
            <div class="card-value-text">{data['bencana_val']}</div>
            <div class="card-desc-text">Banjir dan longsor menahun yang memaksa jutaan jiwa menjadi pengungsi di tanah sendiri</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Polusi Beracun NO2 (Satelit)</div>
            <div class="card-value-text">{data['no2_val']}</div>
            <div class="card-desc-text">Pantauan satelit TROPOMI NASA merekam pekatnya polusi udara di langit kawasan industri nikel</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Kiamat Pertanian Rakyat</div>
            <div class="card-value-text">{data['pertanian']}</div>
            <div class="card-desc-text">Lahan produktif digilas alat berat, kontribusi sektor penopang kedaulatan pangan hancur berantakan</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Konflik Agraria & Kekerasan</div>
            <div class="card-value-text">{data['konflik_val']}</div>
            <div class="card-desc-text">Ledakan kasus kekerasan aparat, kriminalisasi, dan pengusiran paksa warga lokal dari kampungnya</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Pabrik Asap PLTU Captive</div>
            <div class="card-value-text">{data['pltu_val']}</div>
            <div class="card-desc-text">Ironi hilirisasi nikel untuk baterai EV, namun justru disokong oleh ribuan Megawatt batubara kotor</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Dominasi Sektor Ekstraktif</div>
            <div class="card-value-text">{data['pdrb']}</div>
            <div class="card-desc-text">Kekayaan segelintir elit bersumber dari bisnis ekstraktif yang mengeksploitasi sumber daya alam</div>
        </div>
        
    </div>

    <!-- SEKSI 4: PARADOKS INVESTASI & HUKUM -->
    <div class="w-full text-center font-bold text-xl md:text-2xl py-3 rounded-full mb-8 shadow-sm mt-4" style="background-color: #FFE87C; color: #215e39;">
        Paradoks Investasi & Hukum
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 mb-8">
        
        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Investasi Asing Kuasai Nikel</div>
            <div class="card-value-text">{data['investasi_asing']}</div>
            <div class="card-desc-text">Kedaulatan sumber daya tergadai, mayoritas keuntungan lari ke luar negeri tanpa dinikmati warga lokal</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Pencemaran Sungai & Laut</div>
            <div class="card-value-text">{data['sungai_tercemar']}</div>
            <div class="card-desc-text">Air bersih warga dan wilayah tangkap nelayan berubah warna jadi merah karat, beracun, dan mematikan</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Kecelakaan Kerja Tambang</div>
            <div class="card-value-text">{data['kecelakaan_tambang']}</div>
            <div class="card-desc-text">Nyawa pekerja melayang sia-sia akibat buruknya standar K3 demi menggenjot produksi tanpa henti</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Izin Tumpang Tindih Lahan</div>
            <div class="card-value-text">{data['tumpang_tindih']}</div>
            <div class="card-desc-text">Konsesi pertambangan dengan sengaja menabrak dan merampas wilayah kelola rakyat dan tanah adat</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Moratorium Dilanggar</div>
            <div class="card-value-text">{data['moratorium']}</div>
            <div class="card-desc-text">Kebijakan penghentian izin baru hanya sekadar macan kertas, obral izin tetap berjalan mulus di belakang layar</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Kecepatan Izin Pasca Omnibus</div>
            <div class="card-value-text">{data['kecepatan_izin']}</div>
            <div class="card-desc-text">Karpet merah bagi oligarki: persetujuan lingkungan yang rumit dipangkas dan disetujui dalam hitungan hari</div>
        </div>
        
    </div>

    </div> <!-- END MAIN CONTENT -->

</div>
"""


html2 = f"""
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap" rel="stylesheet">

<style>
    .font-inter {{ font-family: 'Inter', sans-serif; }}
    
    .poster-container {{
        background-color: #215e39; /* Hijau dasar CELIOS */
        background-image: 
            linear-gradient(rgba(255, 255, 255, 0.07) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.07) 1px, transparent 1px);
        background-size: 50px 50px;
    }}
    
    .card-title-text {{
        color: #215e39;
        font-weight: 700;
        font-size: 0.95rem;
    }}
    
    .card-value-text {{
        color: #215e39;
        font-weight: 800;
        font-size: 3.5rem;
        line-height: 1.1;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }}
    
    .card-desc-text {{
        color: #555555;
        font-size: 0.75rem;
        line-height: 1.3;
        font-weight: 400;
        padding-left: 0.5rem;
        padding-right: 0.5rem;
    }}
</style>

<div class="poster-container font-inter w-full min-h-screen p-8 md:p-12 lg:p-16 relative overflow-hidden">
    
    <!-- BACKGROUND ACCENTS -->
    <div class="absolute" style="top: -150px; right: -100px; width: 500px; height: 500px; border-radius: 50%; border: 40px solid rgba(255, 232, 124, 0.08); z-index: 0; pointer-events: none;"></div>
    <div class="absolute" style="bottom: 10%; left: -200px; width: 600px; height: 600px; border-radius: 50%; border: 60px solid rgba(255, 232, 124, 0.06); z-index: 0; pointer-events: none;"></div>
    <div class="absolute" style="top: 30%; left: 5%; font-size: 150px; color: rgba(255, 232, 124, 0.08); z-index: 0; font-weight: 900; line-height: 1; pointer-events: none;">+</div>
    <div class="absolute" style="bottom: 20%; right: 10%; font-size: 200px; color: rgba(255, 232, 124, 0.06); z-index: 0; font-weight: 900; line-height: 1; pointer-events: none;">+</div>

    <!-- MAIN CONTENT -->
    <div class="relative z-10 w-full">
        <!-- HEADER -->
    <div class="text-center mb-12 mt-4 flex flex-col items-center justify-center">
        {logo_html}
        <h1 class="text-white text-4xl md:text-5xl font-bold tracking-wide mb-3">Temuan Utama</h1>
        <p style="color: rgba(255,255,255,0.75); font-size: 1rem; font-weight: 500; max-width: 600px; margin: 0 auto; letter-spacing: 0.02em;">Daya Dukung &amp; Daya Tampung Lingkungan Hidup (D3TLH) — Sulawesi 2014–2024</p>
    </div>

    
    <!-- SEKSI 1: DARURAT KESEHATAN PUBLIK -->
    <div class="w-full text-center font-bold text-xl md:text-2xl py-3 rounded-full mb-8 shadow-sm" style="background-color: #FFE87C; color: #215e39;">
        Tumbal Kesehatan
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-3 gap-5 mb-14">
        
        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Ratusan Ribu Paru-Paru Sesak</div>
            <div class="card-value-text">{data['ispa_val']}</div>
            <div class="card-desc-text">Warga dipaksa menghirup debu beracun smelter di setiap tarikan napas mereka</div>
        </div>
        
        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Krisis Air = Krisis Nyawa</div>
            <div class="card-value-text">{data['diare_val']}</div>
            <div class="card-desc-text">Sanitasi hancur, air tanah tercemar pekat, penyakit diare meledak menyerang anak-anak</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Wabah dari Hutan yang Gundul</div>
            <div class="card-value-text">{data['zoo_val']}</div>
            <div class="card-desc-text">Hutan dibabat habis, nyamuk DBD & Malaria terpaksa turun gunung serang pemukiman</div>
        </div>
        
    </div>

    <!-- SEKSI 2: EKSPLOITASI & KEJAHATAN EKOLOGIS -->
    <div class="w-full text-center font-bold text-xl md:text-2xl py-3 rounded-full mb-8 shadow-sm" style="background-color: #FFE87C; color: #215e39;">
        Tanah yang Dirampok
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 mb-14">
        
        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Banjir Izin, Obral Tanah</div>
            <div class="card-value-text">{data['lonjakan_izin']}</div>
            <div class="card-desc-text">Izin tambang diobral gila-gilaan pasca-Omnibus Law tanpa ampun dan tanpa rem</div>
        </div>
        
        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Bekingan Tambang Ilegal</div>
            <div class="card-value-text">{data['izin_hantu']}</div>
            <div class="card-desc-text">Puluhan korporasi "nakal" keruk hutan seenaknya tanpa rasa takut terhadap hukum</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Kawasan Suci Dibuldoser</div>
            <div class="card-value-text">{data['kawasan_lindung']}</div>
            <div class="card-desc-text">Ratusan ribu hektar kawasan lindung resmi disembelih demi memuluskan megaproyek</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Gunung Tailing Mengerikan</div>
            <div class="card-value-text">{data['limbah_val']}</div>
            <div class="card-desc-text">Jutaan ton limbah B3 siap mengubur dan membunuh ekosistem pesisir kapan saja</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Kiamat Hutan Perawan</div>
            <div class="card-value-text">{data['hutan_primer']}</div>
            <div class="card-desc-text">Jutaan hektar kanopi hutan yang tak tergantikan, kini hilang dan hancur selamanya</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Satwa Endemik Tinggal Nama</div>
            <div class="card-value-text">{data['kepunahan']}</div>
            <div class="card-desc-text">Habitat dikeruk habis, satwa ikonik Sulawesi didesak menuju kepunahan massal</div>
        </div>
        
    </div>

    <!-- SEKSI 3: PENDERITAAN WARGA & PARADOKS EKONOMI -->
    <div class="w-full text-center font-bold text-xl md:text-2xl py-3 rounded-full mb-8 shadow-sm" style="background-color: #FFE87C; color: #215e39;">
        Warga Lokal Dapat Apa?
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 mb-8">
        
        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Langganan Banjir & Longsor</div>
            <div class="card-value-text">{data['bencana_val']}</div>
            <div class="card-desc-text">Jutaan jiwa terancam, kampung tenggelam akibat hilangnya hutan penahan air alami</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Langit Pekat Kematian</div>
            <div class="card-value-text">{data['no2_val']}</div>
            <div class="card-desc-text">Satelit NASA jadi saksi bisu ngerinya polusi beracun yang menyelimuti langit warga</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Petani Digilas Tambang</div>
            <div class="card-value-text">{data['pertanian']}</div>
            <div class="card-desc-text">Lahan produktif hancur lebur, ketahanan pangan warga dipastikan tamat</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Tanah Dirampas Paksa</div>
            <div class="card-value-text">{data['konflik_val']}</div>
            <div class="card-desc-text">Warga yang menolak digusur, dikriminalisasi, dan dibungkam paksa oleh aparat</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Hipokrisi Energi Hijau</div>
            <div class="card-value-text">{data['pltu_val']}</div>
            <div class="card-desc-text">Katanya demi transisi energi hijau, nyatanya ditenagai ribuan Megawatt batu bara kotor!</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Kaya di Atas Penderitaan</div>
            <div class="card-value-text">{data['pdrb']}</div>
            <div class="card-desc-text">Hanya segelintir elit oligarki yang untung besar, warga lokal tetap miskin gigit jari</div>
        </div>
        
    </div>

    <!-- SEKSI 4: PARADOKS INVESTASI & HUKUM -->
    <div class="w-full text-center font-bold text-xl md:text-2xl py-3 rounded-full mb-8 shadow-sm mt-4" style="background-color: #FFE87C; color: #215e39;">
        Aturan Tumpul ke Atas
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 mb-8">
        
        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Asing Berpesta, Kita Merana</div>
            <div class="card-value-text">{data['investasi_asing']}</div>
            <div class="card-desc-text">Kedaulatan tergadai! Mayoritas cuan nikel lari keluar negeri, kita cuma dapat ampasnya</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Sungai Darah & Laut Mati</div>
            <div class="card-value-text">{data['sungai_tercemar']}</div>
            <div class="card-desc-text">Air berubah merah karat, lumpur limbah racun matikan sumber mata pencaharian nelayan</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Nyawa Pekerja Murah Meriah</div>
            <div class="card-value-text">{data['kecelakaan_tambang']}</div>
            <div class="card-desc-text">Keselamatan diabaikan total demi kejar target produksi brutal, nyawa pekerja melayang</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Legalitas Penyerobotan Tanah</div>
            <div class="card-value-text">{data['tumpang_tindih']}</div>
            <div class="card-desc-text">Konsesi sengaja didesain untuk menabrak dan merampas tanah adat secara dilegalkan</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Aturan Cuma Macan Kertas</div>
            <div class="card-value-text">{data['moratorium']}</div>
            <div class="card-desc-text">Obral izin terus jalan diam-diam di belakang layar, moratorium cuma janji manis</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Karpet Merah Para Oligarki</div>
            <div class="card-value-text">{data['kecepatan_izin']}</div>
            <div class="card-desc-text">Amdal yang harusnya ketat, disetujui kilat cuma dalam hitungan hari demi investor</div>
        </div>
        
    </div>

    </div> <!-- END MAIN CONTENT -->

</div>
"""



html3 = f"""
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap" rel="stylesheet">

<style>
    .font-inter {{ font-family: 'Inter', sans-serif; }}
    
    .poster-container {{
        background-color: #215e39; /* Hijau dasar CELIOS */
        background-image: 
            linear-gradient(rgba(255, 255, 255, 0.07) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.07) 1px, transparent 1px);
        background-size: 50px 50px;
    }}
    
    .card-title-text {{
        color: #215e39;
        font-weight: 700;
        font-size: 0.95rem;
    }}
    
    .card-value-text {{
        color: #215e39;
        font-weight: 800;
        font-size: 3.5rem;
        line-height: 1.1;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }}
    
    .card-desc-text {{
        color: #555555;
        font-size: 0.75rem;
        line-height: 1.3;
        font-weight: 400;
        padding-left: 0.5rem;
        padding-right: 0.5rem;
    }}
</style>

<div class="poster-container font-inter w-full min-h-screen p-8 md:p-12 lg:p-16 relative overflow-hidden">
    
    <!-- BACKGROUND ACCENTS -->
    <div class="absolute" style="top: -150px; right: -100px; width: 500px; height: 500px; border-radius: 50%; border: 40px solid rgba(255, 232, 124, 0.08); z-index: 0; pointer-events: none;"></div>
    <div class="absolute" style="bottom: 10%; left: -200px; width: 600px; height: 600px; border-radius: 50%; border: 60px solid rgba(255, 232, 124, 0.06); z-index: 0; pointer-events: none;"></div>
    <div class="absolute" style="top: 30%; left: 5%; font-size: 150px; color: rgba(255, 232, 124, 0.08); z-index: 0; font-weight: 900; line-height: 1; pointer-events: none;">+</div>
    <div class="absolute" style="bottom: 20%; right: 10%; font-size: 200px; color: rgba(255, 232, 124, 0.06); z-index: 0; font-weight: 900; line-height: 1; pointer-events: none;">+</div>
    
    <!-- MAIN CONTENT -->
    <div class="relative z-10 w-full">
        <!-- HEADER -->
    <div class="text-center mb-12 mt-4 flex flex-col items-center justify-center">
        {logo_html}
        <h1 class="text-white text-4xl md:text-5xl font-bold tracking-wide mb-3">Temuan Utama</h1>
        <p style="color: rgba(255,255,255,0.75); font-size: 1rem; font-weight: 500; max-width: 600px; margin: 0 auto; letter-spacing: 0.02em;">Daya Dukung &amp; Daya Tampung Lingkungan Hidup (D3TLH) — Sulawesi 2014–2024</p>
    </div>

    <!-- SEKSI 1: ILUSI HILIRISASI & EKONOMI -->
    <div class="w-full text-center font-bold text-xl md:text-2xl py-3 rounded-full mb-8 shadow-sm" style="background-color: #FFE87C; color: #215e39;">
        Ilusi Hilirisasi &amp; Ekonomi
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 mb-14">
        
        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Asing Berpesta, Kita Merana</div>
            <div class="card-value-text">{data['investasi_asing']}</div>
            <div class="card-desc-text">Kedaulatan tergadai! Mayoritas cuan nikel lari keluar negeri, kita cuma dapat ampasnya</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Kaya Tapi Jatuh Miskin</div>
            <div class="card-value-text">{data['pdrb']}</div>
            <div class="card-desc-text">Hanya oligarki yang untung, PDRB meroket tapi nyatanya warga lokal tetap miskin gigit jari</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Petani Digilas Tambang</div>
            <div class="card-value-text">{data['pertanian']}</div>
            <div class="card-desc-text">Lahan produktif dihancurkan, kedaulatan pangan warga tamat riwayatnya</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Hipokrisi Energi Hijau</div>
            <div class="card-value-text">{data['pltu_val']}</div>
            <div class="card-desc-text">Katanya demi transisi energi, nyatanya ditenagai ribuan Megawatt batu bara super kotor</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Nyawa Pekerja Murah</div>
            <div class="card-value-text">{data['kecelakaan_tambang']}</div>
            <div class="card-desc-text">Standar K3 diabaikan demi kejar target produksi brutal, pekerja tewas sia-sia</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Tanah Dirampas Paksa</div>
            <div class="card-value-text">{data['konflik_val']}</div>
            <div class="card-desc-text">Aparat bungkam dan gusur warga lokal yang mencoba mempertahankan ruang hidupnya</div>
        </div>
    </div>

    <!-- SEKSI 2: EKOSIDA & PENGHANCURAN ALAM -->
    <div class="w-full text-center font-bold text-xl md:text-2xl py-3 rounded-full mb-8 shadow-sm" style="background-color: #FFE87C; color: #215e39;">
        Ekosida &amp; Penghancuran Alam
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 mb-14">
        
        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Kiamat Hutan Perawan</div>
            <div class="card-value-text">{data['hutan_primer']}</div>
            <div class="card-desc-text">Jutaan hektar kanopi hutan yang tak tergantikan hilang dan hancur selamanya</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Kawasan Suci Dibuldoser</div>
            <div class="card-value-text">{data['kawasan_lindung']}</div>
            <div class="card-desc-text">Hutan lindung yang harusnya sakral resmi 'disembelih' demi memuluskan megaproyek nikel</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Satwa Endemik Terbantai</div>
            <div class="card-value-text">{data['kepunahan']}</div>
            <div class="card-desc-text">Habitat dikeruk habis, satwa ikonik Sulawesi di ujung jurang kepunahan massal</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Gunung Tailing Mengerikan</div>
            <div class="card-value-text">{data['limbah_val']}</div>
            <div class="card-desc-text">Bom waktu jutaan ton limbah B3 beracun siap menenggelamkan ekosistem pesisir kapan saja</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Sungai Darah &amp; Laut Mati</div>
            <div class="card-value-text">{data['sungai_tercemar']}</div>
            <div class="card-desc-text">Air laut berubah merah karat beracun, lumpur nikel matikan total mata pencaharian nelayan</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Langganan Bencana Buatan</div>
            <div class="card-value-text">{data['bencana_val']}</div>
            <div class="card-desc-text">Hilangnya penahan air alami bikin jutaan jiwa terus-terusan diusir dari kampung halamannya oleh banjir dan longsor</div>
        </div>
    </div>

    <!-- SEKSI 3: TUMBAL NYAWA WARGA -->
    <div class="w-full text-center font-bold text-xl md:text-2xl py-3 rounded-full mb-8 shadow-sm" style="background-color: #FFE87C; color: #215e39;">
        Tumbal Nyawa Warga
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 mb-14">
        
        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Paru-Paru Sesak</div>
            <div class="card-value-text">{data['ispa_val']}</div>
            <div class="card-desc-text">Warga dipaksa menghirup debu beracun smelter tiap kali bernapas</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Langit Pekat Kematian</div>
            <div class="card-value-text">{data['no2_val']}</div>
            <div class="card-desc-text">Satelit NASA saksi bisu langit beracun yang mengintai jutaan warga tiap hari</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Krisis Air = Krisis Nyawa</div>
            <div class="card-value-text">{data['diare_val']}</div>
            <div class="card-desc-text">Air tanah tercemar pekat, penyakit diare ganas meledak serang warga kecil</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Wabah Hutan Gundul</div>
            <div class="card-value-text">{data['zoo_val']}</div>
            <div class="card-desc-text">Hutan dibabat habis, nyamuk DBD &amp; Malaria turun gunung serang pemukiman tak berdosa</div>
        </div>
    </div>

    <!-- SEKSI 4: HUKUM TUMPUL & PERMAINAN KOTOR OLIGARKI -->
    <div class="w-full text-center font-bold text-xl md:text-2xl py-3 rounded-full mb-8 shadow-sm" style="background-color: #FFE87C; color: #215e39;">
        Hukum Tumpul &amp; Permainan Kotor Oligarki
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-3 gap-5 mb-14">
        
        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Banjir Izin Pasca Omnibus</div>
            <div class="card-value-text">{data['lonjakan_izin']}</div>
            <div class="card-desc-text">Izin tambang diobral gila-gilaan tanpa ampun dan tanpa rem pasca-Omnibus Law disahkan</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Karpet Merah Amdal Kilat</div>
            <div class="card-value-text">{data['kecepatan_izin']}</div>
            <div class="card-desc-text">Aturan ditebas: Amdal yang ketat disetujui kilat cuma hitungan hari demi muluskan investor</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Moratorium Cuma Macan Kertas</div>
            <div class="card-value-text">{data['moratorium']}</div>
            <div class="card-desc-text">Obral izin terus jalan terang-terangan di belakang layar, moratorium cuma pemanis mulut</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Bekingan Tambang Ilegal</div>
            <div class="card-value-text">{data['izin_hantu']}</div>
            <div class="card-desc-text">Korporasi 'nakal' keruk hutan seenaknya tanpa takut hukum karena dibeking orang kuat</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Legalitas Merampok Tanah</div>
            <div class="card-value-text">{data['tumpang_tindih']}</div>
            <div class="card-desc-text">Pemerintah sengaja keluarkan izin tambang yang menabrak dan merampas tanah adat/warga</div>
        </div>

    </div>

    </div> <!-- END MAIN CONTENT -->

</div>
"""

tab2, tab3 = st.tabs(["Opsi 2", "Opsi 3"])

with tab2:
    st.markdown(html2.replace('\n', ''), unsafe_allow_html=True)

with tab3:
    st.markdown(html3.replace('\n', ''), unsafe_allow_html=True)
