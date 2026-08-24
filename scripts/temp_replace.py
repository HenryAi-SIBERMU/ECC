with open('c:/Users/yooma/OneDrive/Desktop/duniahub/client/4. Celios2/pages/6_Audit_D3TLH.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('ika_sulteng = 50', 'ika_terkini = 50')
content = content.replace(\"df_sulteng = df_ika[df_ika['Provinsi'] == 'Sulawesi Tengah']\", \"df_ika_avg = df_ika.groupby('Tahun')['Indeks Kualitas Air'].mean().reset_index()\")
content = content.replace(\"if not df_sulteng.empty and 2024 in df_sulteng['Tahun'].values:\", \"if 2024 in df_ika_avg['Tahun'].values:\")
content = content.replace(\"ika_sulteng = df_sulteng[df_sulteng['Tahun'] == 2024]['Indeks Kualitas Air'].values[0]\", \"ika_terkini = df_ika_avg[df_ika_avg['Tahun'] == 2024]['Indeks Kualitas Air'].values[0]\")
content = content.replace(\"'ika_bps': ika_sulteng\", \"'ika_bps': ika_terkini\")
content = content.replace('80 - ika_sulteng', '80 - ika_terkini')
content = content.replace('IKA Sulteng: {ika_sulteng', 'IKA Sulawesi: {ika_terkini')
content = content.replace('ika_sulteng < 50', 'ika_terkini < 50')
content = content.replace('f\"{ika_sulteng:.1f}\"', 'f\"{ika_terkini:.1f}\"')

with open('c:/Users/yooma/OneDrive/Desktop/duniahub/client/4. Celios2/pages/6_Audit_D3TLH.py', 'w', encoding='utf-8') as f:
    f.write(content)
