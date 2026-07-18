import os

filepath = r'C:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\pages\13_Infografis_Fakta.py'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

html_start_idx = content.find('html = f"""')
before_html = content[:html_start_idx]
html_string_1 = content[html_start_idx:]

html_string_1 = html_string_1.replace('html = f"""', 'html1 = f"""')
html2_str = html_string_1.replace('html1 = f"""', 'html2 = f"""')

replacements = {
    'Darurat Kesehatan Publik': 'Tumbal Kesehatan',
    'Beban Penyakit ISPA': 'Ratusan Ribu Paru-Paru Sesak',
    'Warga lingkar tambang (Konawe/Morowali) dipaksa menghirup udara mematikan setiap hari': 'Warga dipaksa menghirup debu beracun smelter di setiap tarikan napas mereka',
    'Kasus Diare Akut': 'Krisis Air = Krisis Nyawa',
    'Krisis air bersih dan hancurnya sanitasi akibat sumber air tanah tercemar berat': 'Sanitasi hancur, air tanah tercemar pekat, penyakit diare meledak menyerang anak-anak',
    'Penyakit Tropis & Zoonosis': 'Wabah dari Hutan yang Gundul',
    'Kasus Demam Berdarah dan Malaria meroket imbas deforestasi hutan yang agresif': 'Hutan dibabat habis, nyamuk DBD & Malaria terpaksa turun gunung serang pemukiman',
    
    'Eksploitasi & Kejahatan Ekologis': 'Tanah yang Dirampok',
    'Lonjakan Gila Izin Tambang': 'Banjir Izin, Obral Tanah',
    'Pasca-pandemi dan Omnibus Law, perizinan diobral tanpa rem dan daya dukung lingkungan': 'Izin tambang diobral gila-gilaan pasca-Omnibus Law tanpa ampun dan tanpa rem',
    'Sindikasi Izin Hantu & Ilegal': 'Bekingan Tambang Ilegal',
    'Beroperasi secara ilegal dan kebal hukum di dalam kawasan hutan tanpa sanksi tegas': 'Puluhan korporasi "nakal" keruk hutan seenaknya tanpa rasa takut terhadap hukum',
    'Kawasan Lindung Dihancurkan': 'Kawasan Suci Dibuldoser',
    'Area konservasi sakral yang secara legal dirobek dan dicaplok demi memuluskan megaproyek': 'Ratusan ribu hektar kawasan lindung resmi disembelih demi memuluskan megaproyek',
    'Gunung Limbah Beracun': 'Gunung Tailing Mengerikan',
    'Bom waktu limbah B3 dan tailing nikel yang meracuni pesisir dan mematikan ekosistem laut': 'Jutaan ton limbah B3 siap mengubur dan membunuh ekosistem pesisir kapan saja',
    'Hutan Primer Purba Musnah': 'Kiamat Hutan Perawan',
    'Hilangnya kanopi hutan perawan yang mustahil untuk direklamasi dan dikembalikan fungsinya': 'Jutaan hektar kanopi hutan yang tak tergantikan, kini hilang dan hancur selamanya',
    'Ancaman Kepunahan Satwa': 'Satwa Endemik Tinggal Nama',
    'Satwa endemik Sulawesi didorong paksa ke jurang kepunahan massal dalam Daftar Merah IUCN': 'Habitat dikeruk habis, satwa ikonik Sulawesi didesak menuju kepunahan massal',
    
    'Penderitaan Warga & Paradoks Ekonomi': 'Warga Lokal Dapat Apa?',
    'Ledakan Bencana Ekologis': 'Langganan Banjir & Longsor',
    'Banjir dan longsor menahun yang memaksa jutaan jiwa menjadi pengungsi di tanah sendiri': 'Jutaan jiwa terancam, kampung tenggelam akibat hilangnya hutan penahan air alami',
    'Polusi Beracun NO2 (Satelit)': 'Langit Pekat Kematian',
    'Pantauan satelit TROPOMI NASA merekam pekatnya polusi udara di langit kawasan industri nikel': 'Satelit NASA jadi saksi bisu ngerinya polusi beracun yang menyelimuti langit warga',
    'Kiamat Pertanian Rakyat': 'Petani Digilas Tambang',
    'Lahan produktif digilas alat berat, kontribusi sektor penopang kedaulatan pangan hancur berantakan': 'Lahan produktif hancur lebur, ketahanan pangan warga dipastikan tamat',
    'Konflik Agraria & Kekerasan': 'Tanah Dirampas Paksa',
    'Ledakan kasus kekerasan aparat, kriminalisasi, dan pengusiran paksa warga lokal dari kampungnya': 'Warga yang menolak digusur, dikriminalisasi, dan dibungkam paksa oleh aparat',
    'Pabrik Asap PLTU Captive': 'Hipokrisi Energi Hijau',
    'Ironi hilirisasi nikel untuk baterai EV, namun justru disokong oleh ribuan Megawatt batubara kotor': 'Katanya demi transisi energi hijau, nyatanya ditenagai ribuan Megawatt batu bara kotor!',
    'Dominasi Sektor Ekstraktif': 'Kaya di Atas Penderitaan',
    'Kekayaan segelintir elit bersumber dari bisnis ekstraktif yang mengeksploitasi sumber daya alam': 'Hanya segelintir elit oligarki yang untung besar, warga lokal tetap miskin gigit jari',
    
    'Paradoks Investasi & Hukum': 'Aturan Tumpul ke Atas',
    'Investasi Asing Kuasai Nikel': 'Asing Berpesta, Kita Merana',
    'Kedaulatan sumber daya tergadai, mayoritas keuntungan lari ke luar negeri tanpa dinikmati warga lokal': 'Kedaulatan tergadai! Mayoritas cuan nikel lari keluar negeri, kita cuma dapat ampasnya',
    'Pencemaran Sungai & Laut': 'Sungai Darah & Laut Mati',
    'Air bersih warga dan wilayah tangkap nelayan berubah warna jadi merah karat, beracun, dan mematikan': 'Air berubah merah karat, lumpur limbah racun matikan sumber mata pencaharian nelayan',
    'Kecelakaan Kerja Tambang': 'Nyawa Pekerja Murah Meriah',
    'Nyawa pekerja melayang sia-sia akibat buruknya standar K3 demi menggenjot produksi tanpa henti': 'Keselamatan diabaikan total demi kejar target produksi brutal, nyawa pekerja melayang',
    'Izin Tumpang Tindih Lahan': 'Legalitas Penyerobotan Tanah',
    'Konsesi pertambangan dengan sengaja menabrak dan merampas wilayah kelola rakyat dan tanah adat': 'Konsesi sengaja didesain untuk menabrak dan merampas tanah adat secara dilegalkan',
    'Moratorium Dilanggar': 'Aturan Cuma Macan Kertas',
    'Kebijakan penghentian izin baru hanya sekadar macan kertas, obral izin tetap berjalan mulus di belakang layar': 'Obral izin terus jalan diam-diam di belakang layar, moratorium cuma janji manis',
    'Kecepatan Izin Pasca Omnibus': 'Karpet Merah Para Oligarki',
    'Karpet merah bagi oligarki: persetujuan lingkungan yang rumit dipangkas dan disetujui dalam hitungan hari': 'Amdal yang harusnya ketat, disetujui kilat cuma dalam hitungan hari demi investor'
}

for old, new in replacements.items():
    html2_str = html2_str.replace(old, new)

html_string_1 = html_string_1.replace("st.markdown(html.replace('\\n', ''), unsafe_allow_html=True)", "")
html2_str = html2_str.replace("st.markdown(html.replace('\\n', ''), unsafe_allow_html=True)", "")

tabs_code = """
tab1, tab2 = st.tabs(["📈 Opsi 1: Format Analitis (Akademis Populer)", "🔥 Opsi 2: Format Viral Sosmed (Hard Selling)"])

with tab1:
    st.markdown(html1.replace('\\n', ''), unsafe_allow_html=True)

with tab2:
    st.markdown(html2.replace('\\n', ''), unsafe_allow_html=True)
"""

final_content = before_html + '\\n' + html_string_1 + '\\n' + html2_str + '\\n' + tabs_code

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(final_content)
