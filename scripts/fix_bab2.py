import codecs

def fix_bab2():
    with codecs.open('pages/2_Kualitas_Lingkungan.py', 'r', 'utf-8') as f:
        content = f.read()

    # 1. Ganti Terminologi "Industri Ekstraktif (Tambang/Sawit)" -> "Pertambangan dan Sawit"
    content = content.replace("'Industri Ekstraktif (Tambang/Sawit)'", "'Pertambangan dan Sawit'")
    content = content.replace("INDUSTRI EKSTRAKTIF", "PERTAMBANGAN DAN SAWIT")
    content = content.replace("Industri Ekstraktif (Tambang Nikel & Sawit)", "Pertambangan dan Sawit")
    # Replace in HTML texts if any
    content = content.replace("Industri Ekstraktif (merah gelap)", "Pertambangan dan Sawit (merah gelap)")

    # 2. Extract Data Prep Block
    prep_start_marker = "# Data Loading & Prep\ndf_driver_clean = df_driver.copy()"
    prep_end_marker = "pertanyaan_text = \"\"\""
    
    prep_start_idx = content.find(prep_start_marker)
    prep_end_idx = content.find(prep_end_marker)
    
    if prep_start_idx == -1 or prep_end_idx == -1:
        print("Marker prep tidak ditemukan")
        return
        
    prep_block = content[prep_start_idx:prep_end_idx]
    
    # 3. Extract df_driver_total_all (because it's needed for emissions)
    # It is currently in 2.4.2
    agg_start = "df_driver_total_all = df_driver_focus.groupby('Faktor_Pendorong').agg({"
    agg_end = "    }).reset_index().sort_values('Luas_Deforestasi_Ha', ascending=False)\n"
    
    agg_start_idx = content.find(agg_start)
    agg_end_idx = content.find(agg_end) + len(agg_end)
    
    agg_block = content[agg_start_idx:agg_end_idx]
    # We must dedent it because it was inside a with col_24a:
    agg_block_dedented = agg_block.replace("    df_driver_total_all", "df_driver_total_all").replace("    }).reset_index", "}).reset_index")
    
    # We will remove agg_block from its original place and just use df_driver_total_all since it will be globally computed
    content = content[:agg_start_idx] + content[agg_end_idx:]
    
    # 4. Extract Emisi CO2 Visualization (2.4.3)
    emisi_start = "# ── VISUALIZATION 2.4.3: CO2 Emissions by Driver ──"
    emisi_end = "st.markdown(f\"\"\"\n<div style=\"color: #BDBDBD; font-size: 0.95rem; line-height: 1.6; margin-bottom: 25px; margin-top: 15px; border-left: 3px solid #555; padding-left: 15px;\">\n    {interp_text_243}\n</div>\n\"\"\", unsafe_allow_html=True)\n"
    
    emisi_start_idx = content.find(emisi_start)
    emisi_end_idx = content.find(emisi_end) + len(emisi_end)
    
    emisi_block = content[emisi_start_idx:emisi_end_idx]
    
    # Hapus prep_block dan emisi_block dari tempat aslinya
    # Harus dilakukan dari bawah ke atas agar index tidak bergeser
    if emisi_start_idx > prep_end_idx:
        content = content[:emisi_start_idx] + content[emisi_end_idx:]
        content = content[:prep_start_idx] + content[prep_end_idx:]
    else:
        content = content[:prep_start_idx] + content[prep_end_idx:]
        content = content[:emisi_start_idx] + content[emisi_end_idx:]
    
    # 5. Insert Prep + Agg + Emisi ke akhir bab 2.2 (sebelum 2.3)
    # Cari "# ═══════════════════════════════════════════════════════════════════════════\n# SECTION 2.3:"
    sec23_marker = "# ═══════════════════════════════════════════════════════════════════════════\n# SECTION 2.3:"
    sec23_idx = content.find(sec23_marker)
    
    insert_payload = prep_block + "\n" + agg_block_dedented + "\n" + emisi_block + "\n\n"
    
    content = content[:sec23_idx] + insert_payload + content[sec23_idx:]
    
    with codecs.open('pages/2_Kualitas_Lingkungan.py', 'w', 'utf-8') as f:
        f.write(content)

fix_bab2()
print("OK")
