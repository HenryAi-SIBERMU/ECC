import sys

file_path = "bab1 bismillah.py"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
skip = False

for i in range(len(lines)):
    line = lines[i]
    if skip:
        if "add_table_1col(doc, master_headers, master_rows" in line:
            skip = False
            # insert docx
            new_lines.append('    master_headers = ["No", "Nama Indikator", "Kategori Analisis", "Satuan Ukur", "Cakupan Tahun", "Institusi & Sumber Data Resmi", "Data File Asli"]\n')
            new_lines.append('    master_rows = [\n')
            new_lines.append('        ["1", "Izin Usaha Pertambangan (IUP) Baru", "Faktor Tekanan Ekstraktif", "Unit Izin", "2014-2024", "Data Registry ESDM MODI (Minerbaone)", "sulawesi_izin_baru_per_tahun.csv"],\n')
            new_lines.append('        ["2", "Luas Wilayah Konsesi Tambang Baru", "Faktor Tekanan Ekstraktif", "Hektar (Ha)", "2014-2024", "Data Registry ESDM MODI (Minerbaone)", "sulawesi_kawasan_nikel_luas.csv"],\n')
            new_lines.append('        ["3", "Kapasitas Terpasang PLTU Captive", "Infrastruktur Energi Khusus", "Megawatt (MW)", "2014-2024", "NGO (Global Energy Monitor / GEM)", "sulawesi_pltu_captive.csv"],\n')
            new_lines.append('        ["4", "Fasilitas Smelter Nikel", "Fasilitas Industri Hilir", "Unit Fasilitas", "2014-2024", "Database Smelter CGS & ESDM MODI", "sulawesi_esdm_nikel.csv"],\n')
            new_lines.append('        ["5", "Realisasi Investasi PMDN & Nikel", "Arus Modal Domestik", "Triliun Rupiah", "2016-2024", "API BPS & BKPM", "sulawesi_investasi_pmdn_2016_2024.csv"],\n')
            new_lines.append('        ["6", "PDRB Provinsi (Ekstraktif vs Akar Rumput)", "Struktur Ekonomi Makro", "Triliun Rupiah", "2016-2024", "API BPS (Subject 52)", "sulawesi_pdrb_sektoral_2016_2024.csv"],\n')
            new_lines.append('        ["7", "PDRB Kabupaten Sentra Tambang", "Struktur Ekonomi Daerah", "Triliun Rupiah", "2016-2024", "API BPS (Subject 52)", "sulawesi_pdrb_sektoral_kabupaten_2016_2024.csv"],\n')
            new_lines.append('        ["8", "Pendapatan Asli Daerah (PAD) & Breakdown Pajak", "Kapasitas Fiskal Daerah", "Triliun Rupiah", "2016-2024", "API BPS", "sulawesi_pad_breakdown_2016_2024.csv"],\n')
            new_lines.append('        ["9", "Luas Total Deforestasi Alam & Komoditas", "Dampak Ekologis", "Hektar (Ha)", "2014-2023", "Global Forest Watch (GFW API)", "sulawesi_gfw_master_1_dekade_2014_2023_v3.csv"],\n')
            new_lines.append('        ["10", "Simpul Pelabuhan & Terminal Logistik", "Infrastruktur Rantai Pasok", "Titik Koordinat & DWT", "2014-2024", "Laporan Publik (KNKT, Perpres PSN, Korporasi)", "sulawesi_logistik_simpul_nikel.csv"]\n')
            new_lines.append('    ]\n')
            new_lines.append("    add_table_1col(doc, master_headers, master_rows, [0.8, 3.5, 3.0, 2.0, 2.0, 3.5, 3.2], ['C', 'L', 'L', 'C', 'C', 'L', 'L'])\n")
        continue

    if "master_headers = [" in line and '"No", "Nama Indikator"' in line:
        skip = True
        continue
        
    new_lines.append(line)

lines2 = new_lines.copy()
new_lines = []
skip = False

for i in range(len(lines2)):
    line = lines2[i]
    if skip:
        if '<tr class="data-tr-even"><td class="data-td" style="text-align:center;">10</td>' in line or 'Simpul Pelabuhan' in line and '<td' in line and '</tr>' in line:
            skip = False
            # insert html
            new_lines.append('    <tr>\n')
            new_lines.append('      <th class="data-th" style="width:4%;">No</th>\n')
            new_lines.append('      <th class="data-th" style="width:20%;">Nama Indikator</th>\n')
            new_lines.append('      <th class="data-th" style="width:16%;">Kategori Analisis</th>\n')
            new_lines.append('      <th class="data-th" style="width:10%;">Satuan Ukur</th>\n')
            new_lines.append('      <th class="data-th" style="width:10%;">Cakupan Tahun</th>\n')
            new_lines.append('      <th class="data-th" style="width:20%;">Institusi & Sumber Data Resmi</th>\n')
            new_lines.append('      <th class="data-th" style="width:20%;">Data File Asli</th>\n')
            new_lines.append('    </tr>\n')
            new_lines.append('  </thead>\n')
            new_lines.append('  <tbody>\n')
            new_lines.append('    <tr><td class="data-td" style="text-align:center;">1</td><td class="data-td">Izin Usaha Pertambangan (IUP) Baru</td><td class="data-td">Faktor Tekanan Ekstraktif</td><td class="data-td" style="text-align:center;">Unit Izin</td><td class="data-td" style="text-align:center;">2014-2024</td><td class="data-td">Data Registry ESDM MODI (Minerbaone)</td><td class="data-td" style="font-family:monospace; font-size:0.9em; background:#f4f4f4;">sulawesi_izin_baru_per_tahun.csv</td></tr>\n')
            new_lines.append('    <tr class="data-tr-even"><td class="data-td" style="text-align:center;">2</td><td class="data-td">Luas Wilayah Konsesi Tambang Baru</td><td class="data-td">Faktor Tekanan Ekstraktif</td><td class="data-td" style="text-align:center;">Hektar (Ha)</td><td class="data-td" style="text-align:center;">2014-2024</td><td class="data-td">Data Registry ESDM MODI (Minerbaone)</td><td class="data-td" style="font-family:monospace; font-size:0.9em; background:#f4f4f4;">sulawesi_kawasan_nikel_luas.csv</td></tr>\n')
            new_lines.append('    <tr><td class="data-td" style="text-align:center;">3</td><td class="data-td">Kapasitas Terpasang PLTU Captive</td><td class="data-td">Infrastruktur Energi Khusus</td><td class="data-td" style="text-align:center;">Megawatt (MW)</td><td class="data-td" style="text-align:center;">2014-2024</td><td class="data-td">NGO (Global Energy Monitor / GEM)</td><td class="data-td" style="font-family:monospace; font-size:0.9em; background:#f4f4f4;">sulawesi_pltu_captive.csv</td></tr>\n')
            new_lines.append('    <tr class="data-tr-even"><td class="data-td" style="text-align:center;">4</td><td class="data-td">Fasilitas Smelter Nikel</td><td class="data-td">Fasilitas Industri Hilir</td><td class="data-td" style="text-align:center;">Unit Fasilitas</td><td class="data-td" style="text-align:center;">2014-2024</td><td class="data-td">Database Smelter CGS & ESDM MODI</td><td class="data-td" style="font-family:monospace; font-size:0.9em; background:#f4f4f4;">sulawesi_esdm_nikel.csv</td></tr>\n')
            new_lines.append('    <tr><td class="data-td" style="text-align:center;">5</td><td class="data-td">Realisasi Investasi PMDN & Nikel</td><td class="data-td">Arus Modal Domestik</td><td class="data-td" style="text-align:center;">Triliun Rupiah</td><td class="data-td" style="text-align:center;">2016-2024</td><td class="data-td">API BPS & BKPM</td><td class="data-td" style="font-family:monospace; font-size:0.9em; background:#f4f4f4;">sulawesi_investasi_pmdn_2016_2024.csv</td></tr>\n')
            new_lines.append('    <tr class="data-tr-even"><td class="data-td" style="text-align:center;">6</td><td class="data-td">PDRB Provinsi (Ekstraktif vs Akar Rumput)</td><td class="data-td">Struktur Ekonomi Makro</td><td class="data-td" style="text-align:center;">Triliun Rupiah</td><td class="data-td" style="text-align:center;">2016-2024</td><td class="data-td">API BPS (Subject 52)</td><td class="data-td" style="font-family:monospace; font-size:0.9em; background:#f4f4f4;">sulawesi_pdrb_sektoral_2016_2024.csv</td></tr>\n')
            new_lines.append('    <tr><td class="data-td" style="text-align:center;">7</td><td class="data-td">PDRB Kabupaten Sentra Tambang</td><td class="data-td">Struktur Ekonomi Daerah</td><td class="data-td" style="text-align:center;">Triliun Rupiah</td><td class="data-td" style="text-align:center;">2016-2024</td><td class="data-td">API BPS (Subject 52)</td><td class="data-td" style="font-family:monospace; font-size:0.9em; background:#f4f4f4;">sulawesi_pdrb_sektoral_kabupaten_2016_2024.csv</td></tr>\n')
            new_lines.append('    <tr class="data-tr-even"><td class="data-td" style="text-align:center;">8</td><td class="data-td">Pendapatan Asli Daerah (PAD) & Breakdown Pajak</td><td class="data-td">Kapasitas Fiskal Daerah</td><td class="data-td" style="text-align:center;">Triliun Rupiah</td><td class="data-td" style="text-align:center;">2016-2024</td><td class="data-td">API BPS</td><td class="data-td" style="font-family:monospace; font-size:0.9em; background:#f4f4f4;">sulawesi_pad_breakdown_2016_2024.csv</td></tr>\n')
            new_lines.append('    <tr><td class="data-td" style="text-align:center;">9</td><td class="data-td">Luas Total Deforestasi Alam & Komoditas</td><td class="data-td">Dampak Ekologis</td><td class="data-td" style="text-align:center;">Hektar (Ha)</td><td class="data-td" style="text-align:center;">2014-2023</td><td class="data-td">Global Forest Watch (GFW API)</td><td class="data-td" style="font-family:monospace; font-size:0.9em; background:#f4f4f4;">sulawesi_gfw_master_1_dekade_2014_2023_v3.csv</td></tr>\n')
            new_lines.append('    <tr class="data-tr-even"><td class="data-td" style="text-align:center;">10</td><td class="data-td">Simpul Pelabuhan & Terminal Logistik</td><td class="data-td">Infrastruktur Rantai Pasok</td><td class="data-td" style="text-align:center;">Titik & DWT</td><td class="data-td" style="text-align:center;">2014-2024</td><td class="data-td">Laporan Publik (KNKT, Perpres PSN, Korporasi)</td><td class="data-td" style="font-family:monospace; font-size:0.9em; background:#f4f4f4;">sulawesi_logistik_simpul_nikel.csv</td></tr>\n')
        continue
    
    if "<tr>" in line and lines2[i+1] and '<th class="data-th"' in lines2[i+1] and lines2[i+2] and 'Nama Indikator' in lines2[i+2]:
        skip = True
        continue
        
    new_lines.append(line)


lines3 = new_lines.copy()
new_lines = []
skip = False

for i in range(len(lines3)):
    line = lines3[i]
    if skip:
        if '| 10 |' in line and 'Simpul Pelabuhan' in line:
            skip = False
            # insert md
            new_lines.append('        "| No | Nama Indikator | Kategori Analisis | Satuan Ukur | Cakupan Tahun | Institusi & Sumber Data Resmi | Data File Asli |",\n')
            new_lines.append('        "| :---: | :--- | :--- | :---: | :---: | :--- | :--- |",\n')
            new_lines.append('        "| 1 | Izin Usaha Pertambangan (IUP) Baru | Faktor Tekanan Ekstraktif | Unit Izin | 2014-2024 | Data Registry ESDM MODI (Minerbaone) | `sulawesi_izin_baru_per_tahun.csv` |",\n')
            new_lines.append('        "| 2 | Luas Wilayah Konsesi Tambang Baru | Faktor Tekanan Ekstraktif | Hektar (Ha) | 2014-2024 | Data Registry ESDM MODI (Minerbaone) | `sulawesi_kawasan_nikel_luas.csv` |",\n')
            new_lines.append('        "| 3 | Kapasitas Terpasang PLTU Captive | Infrastruktur Energi Khusus | Megawatt (MW) | 2014-2024 | NGO (Global Energy Monitor / GEM) | `sulawesi_pltu_captive.csv` |",\n')
            new_lines.append('        "| 4 | Fasilitas Smelter Nikel | Fasilitas Industri Hilir | Unit Fasilitas | 2014-2024 | Database Smelter CGS & ESDM MODI | `sulawesi_esdm_nikel.csv` |",\n')
            new_lines.append('        "| 5 | Realisasi Investasi PMDN & Nikel | Arus Modal Domestik | Triliun Rupiah | 2016-2024 | API BPS & BKPM | `sulawesi_investasi_pmdn_2016_2024.csv` |",\n')
            new_lines.append('        "| 6 | PDRB Provinsi (Ekstraktif vs Akar Rumput) | Struktur Ekonomi Makro | Triliun Rupiah | 2016-2024 | API BPS (Subject 52) | `sulawesi_pdrb_sektoral_2016_2024.csv` |",\n')
            new_lines.append('        "| 7 | PDRB Kabupaten Sentra Tambang | Struktur Ekonomi Daerah | Triliun Rupiah | 2016-2024 | API BPS (Subject 52) | `sulawesi_pdrb_sektoral_kabupaten_2016_2024.csv` |",\n')
            new_lines.append('        "| 8 | Pendapatan Asli Daerah (PAD) & Breakdown Pajak | Kapasitas Fiskal Daerah | Triliun Rupiah | 2016-2024 | API BPS | `sulawesi_pad_breakdown_2016_2024.csv` |",\n')
            new_lines.append('        "| 9 | Luas Total Deforestasi Alam & Komoditas | Dampak Ekologis | Hektar (Ha) | 2014-2023 | Global Forest Watch (GFW API) | `sulawesi_gfw_master_1_dekade_2014_2023_v3.csv` |",\n')
            new_lines.append('        "| 10 | Simpul Pelabuhan & Terminal Logistik | Infrastruktur Rantai Pasok | Titik Koordinat & DWT | 2014-2024 | Laporan Publik (KNKT, Perpres PSN, Korporasi) | `sulawesi_logistik_simpul_nikel.csv` |",\n')
        continue
    
    if '"| No | Nama Indikator' in line and 'Kategori Analisis' in line:
        skip = True
        continue
        
    new_lines.append(line)

with open(file_path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)
print("Updated successfully")
