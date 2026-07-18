import codecs
import re

def fix_driver_scope():
    with codecs.open('pages/2_Kualitas_Lingkungan.py', 'r', 'utf-8') as f:
        content = f.read()
        
    # We will search for the block that defines df_driver_clean down to df_driver_total_all
    # and remove it so it doesn't cause any duplicate/late execution issues.
    
    # Let's find the start of the block
    start_marker = "# Data Loading & Prep\ndf_driver_clean = df_driver.copy()"
    # Since windows might have \r\n:
    match_start = re.search(r"# Data Loading & Prep\r?\ndf_driver_clean = df_driver\.copy\(\)", content)
    
    if match_start:
        start_idx = match_start.start()
        
        # Find the end of df_driver_total_all
        match_end = re.search(r"df_driver_total_all = df_driver_focus\.groupby.*?\}\)\.reset_index\(\)\.sort_values\('Luas_Deforestasi_Ha', ascending=False\)", content[start_idx:], flags=re.DOTALL)
        
        if match_end:
            end_idx = start_idx + match_end.end()
            # Remove this block from its current late position
            content = content[:start_idx] + content[end_idx:]
            print("Removed late data prep block.")
        else:
            print("Could not find the end of the block to remove.")
    else:
        print("Could not find the start of the block to remove.")

    # Now, we define the clean, definitive global block
    global_block = """
# --- GLOBAL DATA PREP FOR DEFORESTATION DRIVERS ---
df_driver_clean = df_driver.copy()
driver_mapping = {
    'Deforestasi Komoditas (Tambang/Sawit)': 'Pertambangan dan Sawit',
    'Kehutanan': 'Kehutanan Komersial',
    'Pertanian Berpindah': 'Pertanian Berpindah (Masyarakat)',
    'Urbanisasi': 'Urbanisasi & Infrastruktur',
    'Tidak Diketahui': 'Tidak Teridentifikasi'
}
df_driver_clean['Faktor_Pendorong'] = df_driver_clean['Faktor_Pendorong'].replace(driver_mapping)
df_driver_total = df_driver_clean.groupby(['Provinsi', 'Faktor_Pendorong']).agg({
    'Luas_Deforestasi_Ha': 'sum',
    'Emisi_CO2_Megagram': 'sum'
}).reset_index()
df_driver_pct = df_driver_total.copy()
total_per_prov = df_driver_pct.groupby('Provinsi')['Luas_Deforestasi_Ha'].transform('sum')
df_driver_pct['Persentase'] = (df_driver_pct['Luas_Deforestasi_Ha'] / total_per_prov * 100).round(2)
focus_provinces = ['Sulawesi Tengah', 'Sulawesi Tenggara', 'Sulawesi Utara', 'Sulawesi Selatan', 'Gorontalo']
df_driver_focus = df_driver_clean[df_driver_clean['Provinsi'].isin(focus_provinces)]

df_driver_total_all = df_driver_focus.groupby('Faktor_Pendorong').agg({
    'Luas_Deforestasi_Ha': 'sum',
    'Emisi_CO2_Megagram': 'sum'
}).reset_index().sort_values('Luas_Deforestasi_Ha', ascending=False)
# --------------------------------------------------
"""

    # Insert it right after load_all_data()
    load_marker = "    df_ika, df_iku, df_gfw, df_smelter, df_pltu, df_b3, df_driver = load_all_data()"
    match_load = re.search(r"df_ika, df_iku, df_gfw, df_smelter, df_pltu, df_b3, df_driver = load_all_data\(\)\r?\n", content)
    
    if match_load:
        insert_idx = match_load.end()
        content = content[:insert_idx] + global_block + content[insert_idx:]
        print("Inserted global block successfully.")
    else:
        print("Could not find load_all_data() to insert global block.")

    with codecs.open('pages/2_Kualitas_Lingkungan.py', 'w', 'utf-8') as f:
        f.write(content)

fix_driver_scope()
print("DONE")
