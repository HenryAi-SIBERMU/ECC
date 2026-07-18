import codecs
import re

def fix_bab2():
    with codecs.open('pages/2_Kualitas_Lingkungan.py', 'r', 'utf-8') as f:
        content = f.read()

    # 1. Ganti Terminologi "Industri Ekstraktif (Tambang/Sawit)" -> "Pertambangan dan Sawit"
    content = content.replace("'Industri Ekstraktif (Tambang/Sawit)'", "'Pertambangan dan Sawit'")
    content = content.replace("INDUSTRI EKSTRAKTIF", "PERTAMBANGAN DAN SAWIT")
    content = content.replace("Industri Ekstraktif (Tambang Nikel & Sawit)", "Pertambangan dan Sawit")
    content = content.replace("Industri Ekstraktif (merah gelap)", "Pertambangan dan Sawit (merah gelap)")
    content = content.replace("Industri Ekstraktif", "Pertambangan dan Sawit")

    # 2. Extract Data Prep Block
    prep_start_marker = "# Data Loading & Prep"
    prep_end_marker = 'pertanyaan_text = """'
    
    prep_start_idx = content.find(prep_start_marker)
    prep_end_idx = content.find(prep_end_marker)
    
    if prep_start_idx == -1 or prep_end_idx == -1:
        print("Marker prep tidak ditemukan")
        return
        
    prep_block = content[prep_start_idx:prep_end_idx]
    
    # 3. Extract df_driver_total_all
    agg_start = "df_driver_total_all = df_driver_focus.groupby('Faktor_Pendorong').agg({"
    # Using regex to find the end of the chain
    match = re.search(r"\}\)\.reset_index\(\)\.sort_values\('Luas_Deforestasi_Ha', ascending=False\)[ \t\r\n]*", content[agg_start_idx:] if 'agg_start_idx' in locals() else content[content.find(agg_start):])
    if match:
        agg_end_rel = match.end()
    else:
        print("Agg end tidak ditemukan")
        return
        
    agg_start_idx = content.find(agg_start)
    agg_end_idx = agg_start_idx + agg_end_rel
    
    agg_block = content[agg_start_idx:agg_end_idx]
    agg_block_dedented = agg_block.replace("    df_driver_total_all", "df_driver_total_all").replace("    }).reset_index", "}).reset_index")
    
    content = content[:agg_start_idx] + content[agg_end_idx:]
    
    # Update indices after cut
    prep_start_idx = content.find(prep_start_marker)
    prep_end_idx = content.find(prep_end_marker)
    prep_block = content[prep_start_idx:prep_end_idx]
    
    # 4. Extract Emisi CO2 Visualization (2.4.3)
    emisi_start = "# ── VISUALIZATION 2.4.3: CO2 Emissions by Driver ──"
    # Find the end of interp_text_243 markdown block
    emisi_end_marker = "</div>\\n\"\"\", unsafe_allow_html=True)"
    
    emisi_start_idx = content.find(emisi_start)
    
    # Search for the closing of the markdown using regex to handle newlines
    match_emisi = re.search(r'</div>\r?\n\"\"\", unsafe_allow_html=True\)', content[emisi_start_idx:])
    if match_emisi:
        emisi_end_idx = emisi_start_idx + match_emisi.end()
    else:
        print("Emisi end tidak ditemukan")
        return
    
    emisi_block = content[emisi_start_idx:emisi_end_idx]
    
    # Delete prep_block and emisi_block
    # Because prep comes before emisi, delete emisi first to preserve prep indices
    content = content[:emisi_start_idx] + content[emisi_end_idx:]
    content = content[:prep_start_idx] + content[prep_end_idx:]
    
    # 5. Insert Prep + Agg + Emisi ke akhir bab 2.2 (sebelum 2.3)
    # The header for 2.3 is:
    sec23_marker = "# SECTION 2.3:"
    # Search backwards from sec23_marker to find the start of its block line
    sec23_idx = content.find(sec23_marker)
    
    # We want to insert just above the '═════════════════' line above SECTION 2.3
    insert_point = content.rfind("# ════════", 0, sec23_idx)
    if insert_point == -1:
        insert_point = sec23_idx
        
    insert_payload = prep_block + "\n" + agg_block_dedented + "\n" + emisi_block + "\n\n"
    
    content = content[:insert_point] + insert_payload + content[insert_point:]
    
    with codecs.open('pages/2_Kualitas_Lingkungan.py', 'w', 'utf-8') as f:
        f.write(content)

fix_bab2()
print("OK")
