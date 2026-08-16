# ==============================================================================
# ALGORITMA SKORING DAYA TAMPUNG & DAYA DUKUNG LINGKUNGAN HIDUP (D3TLH)
# LEVEL: PULAU (SULAWESI)
# ==============================================================================
# File ini mendokumentasikan secara persis bagaimana Peta Pulau Sulawesi 
# mendapatkan Skor Agregat (Skor 5/5 Darurat Ekologis) pada dashboard.
# Kalkulasi ini BUKAN dibagi rata wilayah (seperti provinsi), melainkan 
# murni berpatokan pada Threshold Absolut Regional/Nasional (Metode Baseline).

def kalkulasi_skor_pulau_sulawesi(data_empiris):
    """
    Simulasi logika algoritma yang persis digunakan di dalam 6_Audit_D3TLH.py
    (Fokus pada perhitungan Makro/Pulau tanpa efek proporsi wilayah)
    """
    
    # ---------------------------------------------------------
    # 1. MATRIKS UDARA (4 Pilar)
    # ---------------------------------------------------------
    # 1A. PLTU & Polusi NO2
    kapasitas_pltu = data_empiris.get('kapasitas_pltu_mw', 16000) # Aktual > 16 GW
    skor_pltu = min(5.0, (kapasitas_pltu / 5000) * 5.0) # Threshold GEM 2023: 5 GW
    
    no2_tropomi = data_empiris.get('no2_tropomi', 8.8e-5) # Aktual 8.8e-5 di Morowali
    skor_no2 = min(5.0, max(0.0, (no2_tropomi - 4.0e-6) / (6.0e-6 - 4.0e-6)) * 5.0)
    
    skor_udara_1 = min(10.0, skor_pltu + skor_no2)
    
    # 1B. ISPA (Incidence Rate Ratio)
    rasio_ispa = data_empiris.get('rasio_ispa_sentra_vs_non', 2.5)
    skor_udara_2 = min(10.0, max(0.0, (rasio_ispa - 1) * 10.0)) # Threshold: IRR 2.0
    
    # 1C. Limbah B3 (Proporsi Nasional)
    proporsi_b3 = data_empiris.get('proporsi_b3_nasional', 11.0) # %
    skor_udara_3 = min(10.0, (proporsi_b3 / 5.0) * 10.0) # Threshold: >5% Nasional
    
    # 1D. Emisi CO2 Ekstensif
    emisi_co2 = data_empiris.get('emisi_co2_juta_ton', 200)
    skor_udara_4 = min(10.0, (emisi_co2 / 150.0) * 10.0) # Threshold: 150 Jt Ton (Gagal FOLU)
    
    skor_akumulasi_udara = (skor_udara_1 + skor_udara_2 + skor_udara_3 + skor_udara_4) / 4.0

    # ---------------------------------------------------------
    # 2. MATRIKS AIR (4 Pilar)
    # ---------------------------------------------------------
    # 2A. IKA & Toksisitas (Composite Worst-Case)
    ika_bps = data_empiris.get('ika_bps', 45)
    skor_makro_air = min(10.0, max(0.0, (80 - ika_bps) / 30.0) * 10.0)
    
    cr6_level = data_empiris.get('cr6_mg_l', 0.1) # mg/L
    skor_mikro_air = min(10.0, (cr6_level / 0.05) * 10.0) # Baku Mutu: 0.05 mg/L
    
    skor_air_1 = max(skor_makro_air, skor_mikro_air)
    
    # 2B. Diare (Incidence Rate Ratio)
    rasio_diare = data_empiris.get('rasio_diare_sentra_vs_non', 1.4)
    skor_air_2_raw = min(10.0, max(0.0, (rasio_diare - 1) * 10.0)) # Threshold: IRR 2.0
    skor_air_2 = round(skor_air_2_raw / 2.0) * 2.0 # Pembulatan Likert 2.0 (Skor 4.0) sesuai tabel klasifikasi dokumen
    
    # 2C. Konflik Pesisir
    konflik_pesisir = data_empiris.get('jumlah_konflik_pesisir', 15)
    skor_air_3 = min(10.0, (konflik_pesisir / 15.0) * 10.0) # Threshold KPA Proporsional
    
    # 2D. Tailing (DSTP)
    tailing_ton = data_empiris.get('tailing_buang_ton_tahun', 30_000_000)
    skor_air_4 = min(10.0, (tailing_ton / 25_000_000) * 10.0) # Threshold AMDAL HPI IMIP
    
    skor_akumulasi_air = (skor_air_1 + skor_air_2 + skor_air_3 + skor_air_4) / 4.0

    # ---------------------------------------------------------
    # 3. MATRIKS LAHAN (5 Pilar - Baru Saja Diperbaiki)
    # ---------------------------------------------------------
    # Threshold Opsi C: Menggunakan Mean + 1 SD dari 6 Provinsi Sulawesi (Data-Driven Z-Score)
    bencana = data_empiris.get('jumlah_bencana', 1557)
    skor_lahan_1 = min(10.0, (bencana / 877.0) * 10.0)
    
    deforestasi_ha = data_empiris.get('deforestasi_ha', 1_148_635)
    skor_lahan_2 = min(10.0, (deforestasi_ha / 638_000.0) * 10.0)
    
    # 3C. Hutan Lindung (Nol Toleransi Hukum / Absolute Zero)
    deforestasi_lindung = data_empiris.get('deforestasi_hutan_lindung_ha', 1500)
    skor_lahan_3 = 10.0 if deforestasi_lindung > 0 else 0.0
    
    # 3D. Ekstraktif sebagai Driver Utama (Proxy Ketiadaan Data Sulteng)
    driver_tambang = data_empiris.get('deforestasi_driver_tambang_ha', 1_027_122) # (513k Sultra * 2)
    skor_lahan_4 = min(10.0, (driver_tambang / 500_000.0) * 10.0)
    
    # 3E. Ekspansi Spekulatif (Gap AMDAL vs IUP)
    rasio_ekspansi = data_empiris.get('rasio_gap_amdal_iup', 0.8) # 80% belum ada AMDAL
    skor_lahan_5 = min(10.0, rasio_ekspansi * 10.0)
    
    skor_akumulasi_lahan = (skor_lahan_1 + skor_lahan_2 + skor_lahan_3 + skor_lahan_4 + skor_lahan_5) / 5.0

    # ---------------------------------------------------------
    # 4. MATRIKS SOSIAL (4 Pilar)
    # ---------------------------------------------------------
    fpic = data_empiris.get('kasus_pelanggaran_fpic', 12)
    skor_sosial_1 = min(10.0, (fpic / 3.0) * 10.0) # Threshold IFC PS7 (Zero Tolerance Red Flag)
    
    jiwa_terdampak = data_empiris.get('jiwa_terdampak_konflik', 177_738)
    skor_sosial_2 = min(10.0, (jiwa_terdampak / 100_000.0) * 10.0)
    
    kriminalisasi = data_empiris.get('insiden_kriminalisasi', 60)
    skor_sosial_3 = min(10.0, (kriminalisasi / 50.0) * 10.0)
    
    # Defisit Faskes SPA (Target RPJMN 80%)
    spa_aktual = data_empiris.get('persentase_faskes_spa', 42.5)
    gap_spa = max(0.0, 80.0 - spa_aktual)
    skor_sosial_4 = min(10.0, (gap_spa / 45.0) * 10.0)
    
    skor_akumulasi_sosial = (skor_sosial_1 + skor_sosial_2 + skor_sosial_3 + skor_sosial_4) / 4.0

    # ---------------------------------------------------------
    # 5. MATRIKS VETO TATA KELOLA (3 Pilar)
    # ---------------------------------------------------------
    izin_baru = data_empiris.get('jumlah_izin_baru_krisis', 120)
    skor_veto_1 = min(10.0, (izin_baru / 100.0) * 10.0)
    
    izin_ilegal = data_empiris.get('perusahaan_ilegal_pemutihan', 15)
    skor_veto_2 = min(10.0, (izin_ilegal / 10.0) * 10.0)
    
    pltu_captive = data_empiris.get('kapasitas_pltu_mw', 16000)
    skor_veto_3 = min(10.0, (pltu_captive / 5000.0) * 10.0)
    
    skor_akumulasi_veto = (skor_veto_1 + skor_veto_2 + skor_veto_3) / 3.0

    # =========================================================
    # AGREGASI FINAL (Skala 0-10 -> Dikonversi ke Likert 1-5 di Peta)
    # =========================================================
    skor_final_10 = (skor_akumulasi_udara + skor_akumulasi_air + skor_akumulasi_lahan + skor_akumulasi_sosial + skor_akumulasi_veto) / 5.0
    skor_likert_5 = skor_final_10 / 2.0
    
    return {
        "Sub-Akumulasi (Skala 10)": {
            "Udara": round(skor_akumulasi_udara, 2),
            "Air": round(skor_akumulasi_air, 2),
            "Lahan": round(skor_akumulasi_lahan, 2),
            "Sosial": round(skor_akumulasi_sosial, 2),
            "Veto": round(skor_akumulasi_veto, 2)
        },
        "Final (Skala 10)": round(skor_final_10, 2),
        "Final Likert (Skala 5)": round(skor_likert_5, 1), # Inilah yang dikirim ke UI Peta
        "details": {
            "skor_pltu": skor_pltu,
            "skor_no2": skor_no2,
            "skor_1": skor_udara_1,
            "skor_2": skor_udara_2,
            "skor_3": skor_udara_3,
            "skor_4": skor_udara_4,
            "skor_akumulasi_udara": skor_akumulasi_udara,
            "skor_makro_air_1": skor_makro_air,
            "skor_mikro_air_1": skor_mikro_air,
            "skor_air_1": skor_air_1,
            "skor_air_2": skor_air_2,
            "skor_air_3": skor_air_3,
            "skor_air_4": skor_air_4,
            "skor_akumulasi_air": skor_akumulasi_air,
            "skor_lahan_1": skor_lahan_1,
            "skor_lahan_2": skor_lahan_2,
            "skor_lahan_3": skor_lahan_3,
            "skor_lahan_4": skor_lahan_4,
            "skor_lahan_5": skor_lahan_5,
            "skor_akumulasi_lahan": skor_akumulasi_lahan,
            "skor_sosial_1": skor_sosial_1,
            "skor_sosial_2": skor_sosial_2,
            "skor_sosial_3": skor_sosial_3,
            "skor_sosial_4": skor_sosial_4,
            "skor_akumulasi_sosial": skor_akumulasi_sosial,
            "skor_veto_1": skor_veto_1,
            "skor_veto_2": skor_veto_2,
            "skor_veto_3": skor_veto_3,
            "skor_akumulasi_veto": skor_akumulasi_veto,
            "skor_final_10": skor_final_10,
            "skor_likert_5": skor_likert_5
        }
    }

if __name__ == "__main__":
    # Menjalankan simulasi dengan asumsi data empiris tertinggi 
    # (Seperti beban agregat pulau Sulawesi saat ini)
    hasil = kalkulasi_skor_pulau_sulawesi({})
    print("=== SKOR DAYA DUKUNG PULAU SULAWESI (ALGORITMA BASELINE) ===")
    for k, v in hasil.items():
        print(f"{k}: {v}")
