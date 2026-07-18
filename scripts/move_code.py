import sys

with open('pages/2_Kualitas_Lingkungan.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace terminologi
text = text.replace('Industri Ekstraktif (Tambang/Sawit)', 'Pertambangan dan Sawit')

lines = text.splitlines(keepends=True)

# Find start and end of Emisi CO2 block
start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if '# ── VISUALIZATION 2.4.3: CO2 Emissions by Driver ──' in line:
        start_idx = i
    if start_idx != -1 and '</div>' in line and i > start_idx + 40:
        if '\"\"\", unsafe_allow_html=True)' in lines[i+1]:
            end_idx = i + 2
            break

if start_idx == -1 or end_idx == -1:
    print('Could not find Emisi CO2 block')
    sys.exit(1)

emisi_block = lines[start_idx:end_idx]

# Remove the block from its original position
del lines[start_idx:end_idx]

# Find where to insert it (before Section 2.3)
insert_idx = -1
for i, line in enumerate(lines):
    if 'st.markdown("### 2.3. Eksekusi Ruang:' in line:
        insert_idx = i - 1 # Insert before the 'st.markdown("---")'
        break

if insert_idx == -1:
    print('Could not find Section 2.3')
    sys.exit(1)

# Add the dataframe prep code to the top of emisi_block
prep_code = '''
# ── Pra-kalkulasi untuk Emisi CO2 (Dipindah dari 2.4) ──
df_driver_clean_tmp = df_driver.copy()
driver_mapping_tmp = {
    'Deforestasi Komoditas (Tambang/Sawit)': 'Pertambangan dan Sawit',
    'Kehutanan': 'Kehutanan Komersial',
    'Pertanian Berpindah': 'Pertanian Berpindah (Masyarakat)',
    'Urbanisasi': 'Urbanisasi & Infrastruktur',
    'Tidak Diketahui': 'Tidak Teridentifikasi'
}
df_driver_clean_tmp['Faktor_Pendorong'] = df_driver_clean_tmp['Faktor_Pendorong'].replace(driver_mapping_tmp)
df_driver_focus_tmp = df_driver_clean_tmp[df_driver_clean_tmp['Provinsi'].isin(['Sulawesi Tengah', 'Sulawesi Tenggara', 'Sulawesi Utara', 'Sulawesi Selatan', 'Gorontalo'])]
df_driver_total_all_tmp = df_driver_focus_tmp.groupby('Faktor_Pendorong').agg({
    'Luas_Deforestasi_Ha': 'sum',
    'Emisi_CO2_Megagram': 'sum'
}).reset_index().sort_values('Luas_Deforestasi_Ha', ascending=False)
'''

emisi_block_str = ''.join(emisi_block)
emisi_block_str = emisi_block_str.replace('df_driver_total_all.copy()', 'df_driver_total_all_tmp.copy()')

lines.insert(insert_idx, prep_code + '\n' + emisi_block_str + '\n\n')

with open('pages/2_Kualitas_Lingkungan.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('Success')
