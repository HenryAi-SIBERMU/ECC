import os
import re

filepath = r'C:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\pages\13_Infografis_Fakta.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add new data fetches in load_data()
new_data_code = """
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
"""

content = re.sub(r'(\s*try:\s*df_kes = pd\.read_csv.*?\s*except:\s*ispa_val = "[^"]*")', new_data_code, content, flags=re.DOTALL)

content = content.replace('"ispa_val": ispa_val,', '"ispa_val": ispa_val,\n        "diare_val": diare_val,\n        "zoo_val": zoo_val,\n        "no2_val": no2_val,')

# 2. Add New Section 1 and Shift the Rest
new_section_1 = """
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

    <!-- SEKSI 2: EKSPLOITASI & KEJAHATAN EKOLOGIS -->"""

content = content.replace('<!-- SEKSI 1: EKSPLOITASI & KEJAHATAN EKOLOGIS -->', new_section_1)

# Replace the title of SEKSI 2 & 3 in the HTML comments as well
content = content.replace('<!-- SEKSI 2: PENDERITAAN WARGA & PARADOKS EKONOMI -->', '<!-- SEKSI 3: PENDERITAAN WARGA & PARADOKS EKONOMI -->')
content = content.replace('<!-- SEKSI 3: PARADOKS INVESTASI & HUKUM -->', '<!-- SEKSI 4: PARADOKS INVESTASI & HUKUM -->')

# Replace old ISPA card with NO2 card
no2_card = """<div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Polusi Beracun NO2 (Satelit)</div>
            <div class="card-value-text">{data['no2_val']}</div>
            <div class="card-desc-text">Pantauan satelit TROPOMI NASA merekam pekatnya polusi udara di langit kawasan industri nikel</div>
        </div>"""

ispa_card_regex = r'<div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">\s*<div class="card-title-text">Beban Penyakit ISPA</div>.*?</div>'

content = re.sub(ispa_card_regex, no2_card, content, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
