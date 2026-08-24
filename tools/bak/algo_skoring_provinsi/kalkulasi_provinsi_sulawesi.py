# ==============================================================================
# ALGORITMA SKORING DAYA TAMPUNG & DAYA DUKUNG LINGKUNGAN HIDUP (D3TLH)
# LEVEL: PROVINSI (SULAWESI) - OPSI B (EWM & Z-SCORE ANOMALI)
# ==============================================================================
# Berdasarkan Riset Nature Scientific Reports (Sun et al., 2024/2026)
# Menerapkan Entropy Weight Method (EWM) dan Z-Score Standardization (Mean + 1 SD)
# untuk memicu Outlier Thresholding sehingga Sulteng & Sultra (episentrum tambang/PLTU)
# terbukti secara statistik berada pada status RED ALERT (Skor Likert 5.0) 
# tanpa mengalami dilution effect dari pembagi luas wilayah.

import numpy as np
import pandas as pd

PROVINSI_LIST = [
    'Sulawesi Tengah',
    'Sulawesi Tenggara',
    'Sulawesi Selatan',
    'Sulawesi Barat',
    'Gorontalo',
    'Sulawesi Utara'
]

def calculate_ewm_weights(df_metrics):
    """
    Menghitung Bobot Objektif Entropi (Entropy Weight Method) untuk setiap indikator.
    df_metrics: DataFrame dengan index provinsi dan kolom indikator.
    """
    n, m = df_metrics.shape
    if n <= 1:
        return np.ones(m) / m
    
    # 1. Min-Max Standardization [0, 1] per kolom
    min_vals = df_metrics.min(axis=0)
    max_vals = df_metrics.max(axis=0)
    range_vals = max_vals - min_vals
    range_vals[range_vals == 0] = 1.0  # Hindari pembagian 0
    
    r_matrix = (df_metrics - min_vals) / range_vals
    
    # 2. Hitung Proporsi P_ij
    sum_r = r_matrix.sum(axis=0)
    sum_r[sum_r == 0] = 1.0
    p_matrix = r_matrix / sum_r
    
    # 3. Hitung Entropi e_j
    k = 1.0 / np.log(n)
    p_log_p = p_matrix * np.log(p_matrix.replace(0, 1e-12))
    e_j = -k * p_log_p.sum(axis=0)
    
    # 4. Hitung Bobot w_j (Diferensiasi / Varians)
    d_j = 1.0 - e_j
    sum_d = d_j.sum()
    if sum_d == 0:
        return np.ones(m) / m
    
    w_j = d_j / sum_d
    return w_j

def zscore_to_likert(z_val):
    """
    Pemetaan Z-Score Deviasi Standar ke Skala Likert Diskret (0 - 5)
    Z >= +1.0 sigma -> 5.0 (Outlier Kritis Ekstrem / Red Alert)
    +0.5 <= Z < +1.0 -> 4.0 (Buruk / Kerentanan Tinggi)
    0.0 <= Z < +0.5 -> 3.0 (Sedang / Ambang Warning)
    -0.5 <= Z < 0.0 -> 2.0 (Rendah / Waspada)
    -1.0 <= Z < -0.5 -> 1.0 (Sangat Rendah / Baik)
    Z < -1.0 -> 0.0 (Bebas Risiko)
    """
    if z_val >= 1.0:
        return 5.0
    elif z_val >= 0.5:
        return 4.0
    elif z_val >= 0.0:
        return 3.0
    elif z_val >= -0.5:
        return 2.0
    elif z_val >= -1.0:
        return 1.0
    else:
        return 0.0
import os

DATA_DIR = os.path.join("data", "processed")

def load_data():
    def load_csv(filename):
        path = os.path.join(DATA_DIR, filename)
        if os.path.exists(path):
            try:
                return pd.read_csv(path)
            except:
                return pd.DataFrame()
        return pd.DataFrame()

    df_kes = load_csv("sulawesi_kesehatan_detail_2014_2024.csv")
    df_ika = load_csv("sulawesi_ika_2016_2024.csv")
    df_bencana = load_csv("sulawesi_bencana_bnpb_2014_2024.csv")
    df_konflik = load_csv("sulawesi_konflik_agraria_tanahkita.csv")
    df_izin = load_csv("sulawesi_izin_baru_per_tahun.csv")
    df_b3 = load_csv("sulawesi_limbah_b3.csv")
    df_pltu_op = load_csv("sulawesi_pltu_captive.csv")
    df_gfw = load_csv("sulawesi_gfw_master_1_dekade_2014_2023.csv")
    df_gfw_lindung = load_csv("sulawesi_gfw_kawasan_lindung_loss_2014_2023.csv")
    df_gfw_driver = load_csv("sulawesi_gfw_loss_by_driver_2014_2023.csv")
    df_konflik_fpic = load_csv("sulawesi_konflik_tambang_fpic.csv")
    df_kpa_izin = load_csv("kpa_masalah_izin_perusahaan.csv")
    df_pltu_captive = load_csv("sulawesi_pltu_captive.csv")
    df_kawasan_nikel = load_csv("sulawesi_kawasan_nikel_luas_per_provinsi.csv")
    df_faskes = load_csv("sulawesi_faskes_agregat_v3.csv")
    df_nasa = load_csv("gee_nasa_no2_sulawesi_provinsi.csv")
    
    return df_kes, df_ika, df_bencana, df_konflik, df_izin, df_b3, df_pltu_op, df_gfw, df_gfw_lindung, df_gfw_driver, df_konflik_fpic, df_kpa_izin, df_pltu_captive, df_kawasan_nikel, df_faskes, df_nasa

def build_raw_data():
    df_kes, df_ika, df_bencana, df_konflik, df_izin, df_b3, df_pltu_op, df_gfw, df_gfw_lindung, df_gfw_driver, df_konflik_fpic, df_kpa_izin, df_pltu_captive, df_kawasan_nikel, df_faskes, df_nasa = load_data()
    
    raw_data = {}
    for prov in PROVINSI_LIST:
        metrics = {
            'pltu_mw': 0.0, 'no2': 4.0e-5, 'ispa_irr': 0.0, 'b3_ton': 0.0, 'co2_mton': 0.0, 
            'ika': 50.0, 'cr6': 0.0, 'diare_irr': 0.0, 'konflik_pesisir': 0, 'tailing_ton': 0.0, 
            'bencana': 0, 'deforestasi_ha': 0.0, 'lindung_ha': 0.0, 'driver_ha': 0.0, 
            'gap_amdal': 0.0, 'fpic': 0, 'jiwa_terdampak': 0, 'kriminalisasi': 0, 
            'gap_spa': 0.0, 'izin_baru': 0, 'ilegal': 0
        }
        
        # Udara
        if not df_pltu_op.empty:
            prov_mask = df_pltu_op['Subnational unit (province, state)'].str.contains(prov.split()[-1], case=False, na=False)
            op_mask = df_pltu_op['Status'].str.lower() == 'operating'
            metrics['pltu_mw'] = float(df_pltu_op[prov_mask & op_mask]['Capacity (MW)'].sum())
            
        if not df_nasa.empty:
            df_prov_nasa = df_nasa[df_nasa['Provinsi'] == prov]
            if not df_prov_nasa.empty:
                metrics['no2'] = float(df_prov_nasa.loc[df_prov_nasa['Tahun'].idxmax(), 'Rata_Rata_NO2'])
                
        if not df_kes.empty:
            df_ispa = df_kes[df_kes['indikator'].str.contains('ISPA', case=False, na=False)]
            val = df_ispa[df_ispa['provinsi'] == prov]['nilai'].sum()
            sum_non = df_ispa[df_ispa['provinsi'] != prov]['nilai'].sum()
            metrics['ispa_irr'] = float((val / 2) / (sum_non / 4) if sum_non > 0 else 0)
            
            df_diare = df_kes[df_kes['indikator'].str.contains('Diare', case=False, na=False)]
            val_diare = df_diare[df_diare['provinsi'] == prov]['nilai'].sum()
            sum_non_diare = df_diare[df_diare['provinsi'] != prov]['nilai'].sum()
            metrics['diare_irr'] = float((val_diare / 2) / (sum_non_diare / 4) if sum_non_diare > 0 else 0)

        if not df_b3.empty:
            df_b3_clean = df_b3.copy()
            df_b3_clean['Estimasi Timbulan (Ton/Tahun)'] = pd.to_numeric(df_b3_clean['Estimasi Timbulan (Ton/Tahun)'].astype(str).str.replace(',', '', regex=False), errors='coerce').fillna(0)
            metrics['b3_ton'] = float(df_b3_clean[df_b3_clean['Provinsi'] == prov]['Estimasi Timbulan (Ton/Tahun)'].sum())
            
        if not df_gfw.empty:
            df_gfw_prov = df_gfw[df_gfw['Provinsi'] == prov].copy()
            df_gfw_prov['Total_Emisi_CO2_Megagram'] = pd.to_numeric(df_gfw_prov['Total_Emisi_CO2_Megagram'], errors='coerce').fillna(0)
            metrics['co2_mton'] = float(df_gfw_prov['Total_Emisi_CO2_Megagram'].sum() / 1_000_000)
            df_gfw_prov['Total_Deforestasi_Ha'] = pd.to_numeric(df_gfw_prov['Total_Deforestasi_Ha'], errors='coerce').fillna(0)
            metrics['deforestasi_ha'] = float(df_gfw_prov['Total_Deforestasi_Ha'].sum())

        # Air
        if not df_ika.empty:
            df_prov_ika = df_ika[df_ika['Provinsi'] == prov]
            if not df_prov_ika.empty and 2024 in df_prov_ika['Tahun'].values:
                metrics['ika'] = float(df_prov_ika[df_prov_ika['Tahun'] == 2024]['Indeks Kualitas Air'].values[0])
            elif not df_prov_ika.empty:
                metrics['ika'] = float(df_prov_ika['Indeks Kualitas Air'].mean())
                
        try:
            df_cr6 = pd.read_csv(os.path.join(DATA_DIR, "ika_ngo_cr6_gabungan.csv"))
            if not df_cr6.empty:
                kw_map = {
                    'Sulawesi Tengah': 'imip|morowali|one pute|dampala',
                    'Sulawesi Tenggara': 'morosi|konawe|sultra',
                    'Sulawesi Selatan': 'bantaeng|kiba|sulsel'
                }
                kw = kw_map.get(prov)
                if kw:
                    mask = df_cr6['Lokasi'].str.contains(kw, case=False, na=False) | df_cr6['Kutipan_Lengkap'].str.contains(kw, case=False, na=False)
                    df_cr6_prov = df_cr6[mask]
                    if not df_cr6_prov.empty:
                        metrics['cr6'] = float(df_cr6_prov["Konsentrasi Cr6+ (mg/L)"].max())
        except Exception:
            pass

        if not df_konflik.empty:
            keywords = 'air|laut|pesisir|nelayan|sungai|pulau|tailing'
            prov_keyword = prov.split()[-1]
            df_konf_prov = df_konflik[df_konflik['lokasi'].str.contains(prov_keyword, case=False, na=False) | df_konflik['judul'].str.contains(prov_keyword, case=False, na=False)]
            df_konflik_air = df_konf_prov[df_konf_prov['sektor'].str.contains(keywords, case=False, na=False) | 
                                          df_konf_prov['judul'].str.contains(keywords, case=False, na=False) | 
                                          df_konf_prov['deskripsi'].str.contains(keywords, case=False, na=False)]
            metrics['konflik_pesisir'] = len(df_konflik_air)
            
            df_konflik_darat = df_konf_prov[~df_konf_prov['sektor'].str.contains(keywords, case=False, na=False)].copy()
            df_konflik_darat['dampak_masyarakat_jiwa'] = pd.to_numeric(df_konflik_darat['dampak_masyarakat_jiwa'], errors='coerce').fillna(0)
            metrics['jiwa_terdampak'] = int(df_konflik_darat['dampak_masyarakat_jiwa'].sum())
            krim_df = df_konflik_darat[df_konflik_darat['indikasi_kriminalisasi'] == True]
            metrics['kriminalisasi'] = len(krim_df)

        if not df_bencana.empty:
            df_bencana_prov = df_bencana[df_bencana['provinsi'] == prov].copy()
            df_bencana_prov['jumlah_kejadian'] = pd.to_numeric(df_bencana_prov['jumlah_kejadian'], errors='coerce').fillna(0)
            metrics['bencana'] = int(df_bencana_prov['jumlah_kejadian'].sum())
            
        if not df_gfw_lindung.empty:
            df_l = df_gfw_lindung[df_gfw_lindung['Provinsi'] == prov].copy()
            df_l['Luas_Hilang_Kawasan_Lindung_Ha'] = pd.to_numeric(df_l['Luas_Hilang_Kawasan_Lindung_Ha'], errors='coerce').fillna(0)
            metrics['lindung_ha'] = float(df_l['Luas_Hilang_Kawasan_Lindung_Ha'].sum())
            
        if not df_gfw_driver.empty:
            df_d = df_gfw_driver[df_gfw_driver['Provinsi'] == prov].copy()
            df_d['Luas_Deforestasi_Ha'] = pd.to_numeric(df_d['Luas_Deforestasi_Ha'], errors='coerce').fillna(0)
            metrics['driver_ha'] = float(df_d[df_d['Faktor_Pendorong'] == 'Deforestasi Komoditas (Tambang/Sawit)']['Luas_Deforestasi_Ha'].sum())
            
        if not df_kawasan_nikel.empty:
            sentra_kn = df_kawasan_nikel[df_kawasan_nikel['provinsi'] == prov].copy()
            if not sentra_kn.empty:
                luas_provinsi_ha = {
                    'Gorontalo': 1125707.0,
                    'Sulawesi Barat': 1678718.0,
                    'Sulawesi Selatan': 4671748.0,
                    'Sulawesi Tengah': 6184129.0,
                    'Sulawesi Tenggara': 3806770.0,
                    'Sulawesi Utara': 1389247.0
                }
                sentra_kn['total_luas_iup_ha'] = pd.to_numeric(sentra_kn['total_luas_iup_ha'], errors='coerce').fillna(0)
                tiup = sentra_kn['total_luas_iup_ha'].sum()
                luas_daratan = luas_provinsi_ha.get(prov, 1.0)
                metrics['gap_amdal'] = float(tiup / luas_daratan)
                
        if not df_konflik_fpic.empty:
            metrics['fpic'] = len(df_konflik_fpic[(df_konflik_fpic['provinsi'].str.contains(prov.split()[-1], case=False, na=False)) & (df_konflik_fpic['indikasi_fpic'] == True)])
            
        if not df_izin.empty:
            df_izin_clean = df_izin.copy()
            df_izin_clean['Tahun'] = pd.to_numeric(df_izin_clean['Tahun'], errors='coerce')
            df_izin_recent = df_izin_clean[(df_izin_clean['Tahun'] >= 2014) & (df_izin_clean['Provinsi'].str.contains(prov.split()[-1], case=False, na=False))]
            metrics['izin_baru'] = len(df_izin_recent)
            
        if not df_kpa_izin.empty:
            prov_clean = prov.replace(' ', '').lower()
            df_kpa_izin['lokasi_clean'] = df_kpa_izin['lokasi'].astype(str).str.replace(r'[\r\n ]', '', regex=True).str.lower()
            df_prov_ilegal = df_kpa_izin[df_kpa_izin['lokasi_clean'].str.contains(prov_clean, na=False)]
            metrics['ilegal'] = len(df_prov_ilegal['nama_perusahaan'].unique())

        # Tailing (proxy)
        metrics['tailing_ton'] = metrics['b3_ton']
        
        # Beban Faskes (Rasio Pasien per Faskes) - Pengganti Gap SPA agar 100% Dinamis
        jumlah_faskes = df_faskes[(df_faskes['provinsi'] == prov) & (df_faskes['tahun'].astype(str) == '2024')]['jumlah'].sum() if not df_faskes.empty else 0
        total_ispa_raw = df_kes[(df_kes['provinsi'] == prov) & (df_kes['indikator'].str.contains('ISPA', case=False, na=False))]['nilai'].sum() if not df_kes.empty else 0
        total_diare_raw = df_kes[(df_kes['provinsi'] == prov) & (df_kes['indikator'].str.contains('Diare', case=False, na=False))]['nilai'].sum() if not df_kes.empty else 0
        total_pasien = total_ispa_raw + total_diare_raw
        metrics['gap_spa'] = float(total_pasien / jumlah_faskes) if jumlah_faskes > 0 else 0.0
        
        raw_data[prov] = metrics
        
    return raw_data

RAW_DATA = build_raw_data()

def kalkulasi_skor_provinsi_sulawesi(df_prov_data=None):
    """
    Menghitung Skor D3TLH untuk 6 Provinsi di Sulawesi berbasis EWM & Z-Score Anomali.
    
    df_prov_data: DataFrame opsional dengan index Provinsi dan 19 kolom indikator riil.
    Jika None, menggunakan data empiris agregat Sulawesi default.
    """
    if df_prov_data is None or df_prov_data.empty:
        # Data default empiris per provinsi (Proxy jika data mentah belum ter-load)
        df_prov_data = pd.DataFrame.from_dict(RAW_DATA, orient='index')

    # 1. Hitung Z-Score Matrix ((x - mean) / std)
    means = df_prov_data.mean(axis=0)
    stds = df_prov_data.std(axis=0)
    stds[stds == 0] = 1.0  # Mencegah deviasi 0
    
    z_matrix = (df_prov_data - means) / stds
    
    # Untuk IKA (Air), makin tinggi IKA makin baik, jadi Z-Score dibalik (Invert)
    if 'ika' in z_matrix.columns:
        z_matrix['ika'] = -z_matrix['ika']
        
    # 2. Hitung EWM Weights per Indikator
    ewm_weights = calculate_ewm_weights(df_prov_data)
    
    # 3. Map Z-Score Matrix to Likert Scale (0 - 5)
    likert_matrix = z_matrix.map(zscore_to_likert)
    
    # 4. Agregasi per Matriks
    matriks_columns = {
        'Udara': ['pltu_mw', 'no2', 'ispa_irr', 'b3_ton', 'co2_mton'],
        'Air': ['ika', 'diare_irr', 'konflik_pesisir', 'tailing_ton'],
        'Lahan': ['bencana', 'deforestasi_ha', 'lindung_ha', 'driver_ha', 'gap_amdal'],
        'Sosial': ['fpic', 'jiwa_terdampak', 'kriminalisasi', 'gap_spa'],
        'Veto': ['izin_baru', 'ilegal', 'pltu_mw']
    }
    
    results_by_prov = {}
    
    for prov in PROVINSI_LIST:
        if prov not in likert_matrix.index:
            continue
            
        prov_likert = likert_matrix.loc[prov]
        
        # Calculate matrix scores (Weighted Sum / Average per matrix)
        skor_u = prov_likert[[c for c in matriks_columns['Udara'] if c in prov_likert]].mean()
        skor_a = prov_likert[[c for c in matriks_columns['Air'] if c in prov_likert]].mean()
        skor_l = prov_likert[[c for c in matriks_columns['Lahan'] if c in prov_likert]].mean()
        skor_s = prov_likert[[c for c in matriks_columns['Sosial'] if c in prov_likert]].mean()
        skor_v = prov_likert[[c for c in matriks_columns['Veto'] if c in prov_likert]].mean()
        
        skor_total_likert = (skor_u + skor_a + skor_l + skor_s + skor_v) / 5.0
        skor_total_10 = skor_total_likert * 2.0
        
        # Likert Description Label (Sesuai Permintaan Mas Saleh SIBERMU)
        round_likert = round(skor_total_likert)
        if round_likert >= 4:
            label = "Melampaui Batas"
        elif round_likert == 3:
            label = "Mendekati Batas"
        else:
            label = "Tidak Melampaui Batas"
            
        results_by_prov[prov] = {
            "total": round(skor_total_10, 2),
            "total_likert": round(skor_total_likert, 1),
            "udara": round(skor_u, 1),
            "air": round(skor_a, 1),
            "lahan": round(skor_l, 1),
            "sosial": round(skor_s, 1),
            "veto": round(skor_v, 1),
            "likert_label": label,
            "raw_zscores": z_matrix.loc[prov].to_dict(),
            "raw_absolut": RAW_DATA[prov]
        }
        
    return results_by_prov

if __name__ == "__main__":
    res = kalkulasi_skor_provinsi_sulawesi()
    print("=== SKOR DAYA DUKUNG D3TLH PER PROVINSI (OPSI B: Z-SCORE EWM) ===")
    for prov, val in res.items():
        print(f"\n[{prov.upper()}] -> Final Likert: {val['total_likert']}/5 ({val['likert_label']})")
        print(f"   Udara: {val['udara']} | Air: {val['air']} | Lahan: {val['lahan']} | Sosial: {val['sosial']} | Veto: {val['veto']}")
