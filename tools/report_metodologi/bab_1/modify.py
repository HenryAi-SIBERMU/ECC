import re

file_path = r"C:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\tools\report_metodologi\bab_1\bab1 bismillah.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update DOCX master_headers and master_rows
content = content.replace(
    'master_headers = ["No", "Nama Indikator", "Kategori Analisis", "Satuan Ukur", "Cakupan Tahun", "Institusi & Sumber Data Resmi"]',
    'master_headers = ["No", "Nama Indikator", "Kategori Analisis", "Satuan Ukur", "Cakupan Tahun", "Institusi & Sumber Data Resmi", "Data File Asli"]'
)

docx_rows_old = """    master_rows = [
        ["1", "Izin Usaha Pertambangan (IUP) Baru", "Faktor Tekanan Ekstraktif", "Unit Izin", "2014-2024", "Data Registry ESDM MODI (Minerbaone)"],
        ["2", "Luas Wilayah Konsesi Tambang Baru", "Faktor Tekanan Ekstraktif", "Hektar (Ha)", "2014-2024", "Data Registry ESDM MODI (Minerbaone)"],
        ["3", "Kapasitas Terpasang PLTU Captive", "Infrastruktur Energi Khusus", "Megawatt (MW)", "2014-2024", "NGO (Global Energy Monitor / GEM)"],
        ["4", "Fasilitas Smelter Nikel", "Fasilitas Industri Hilir", "Unit Fasilitas", "2014-2024", "Database Smelter CGS & ESDM MODI"],
        ["5", "Realisasi Investasi PMDN & Nikel", "Arus Modal Domestik", "Triliun Rupiah", "2016-2024", "API BPS & BKPM"],
        ["6", "PDRB Provinsi (Ekstraktif vs Akar Rumput)", "Struktur Ekonomi Makro", "Triliun Rupiah", "2016-2024", "API BPS (Subject 52)"],
        ["7", "PDRB Kabupaten Sentra Tambang", "Struktur Ekonomi Daerah", "Triliun Rupiah", "2016-2024", "API BPS (Subject 52)"],
        ["8", "Pendapatan Asli Daerah (PAD) & Breakdown Pajak", "Kapasitas Fiskal Daerah", "Triliun Rupiah", "2016-2024", "API BPS"],
        ["9", "Luas Total Deforestasi Alam & Komoditas", "Dampak Ekologis", "Hektar (Ha)", "2014-2023", "Global Forest Watch (GFW API)"],
        ["10", "Simpul Pelabuhan & Terminal Logistik", "Infrastruktur Rantai Pasok", "Titik Koordinat & DWT", "2014-2024", "Laporan Publik (KNKT, Perpres PSN, Korporasi)"]
    ]"""

docx_rows_new = """    master_rows = [
        ["1", "Izin Usaha Pertambangan (IUP) Baru", "Faktor Tekanan Ekstraktif", "Unit Izin", "2014-2024", "Data Registry ESDM MODI (Minerbaone)", "sulawesi_izin_baru_per_tahun.csv"],
        ["2", "Luas Wilayah Konsesi Tambang Baru", "Faktor Tekanan Ekstraktif", "Hektar (Ha)", "2014-2024", "Data Registry ESDM MODI (Minerbaone)", "sulawesi_kawasan_nikel_luas.csv"],
        ["3", "Kapasitas Terpasang PLTU Captive", "Infrastruktur Energi Khusus", "Megawatt (MW)", "2014-2024", "NGO (Global Energy Monitor / GEM)", "sulawesi_pltu_captive.csv"],
        ["4", "Fasilitas Smelter Nikel", "Fasilitas Industri Hilir", "Unit Fasilitas", "2014-2024", "Database Smelter CGS & ESDM MODI", "sulawesi_esdm_nikel.csv"],
        ["5", "Realisasi Investasi PMDN & Nikel", "Arus Modal Domestik", "Triliun Rupiah", "2016-2024", "API BPS & BKPM", "sulawesi_investasi_pmdn_2016_2024.csv"],
        ["6", "PDRB Provinsi (Ekstraktif vs Akar Rumput)", "Struktur Ekonomi Makro", "Triliun Rupiah", "2016-2024", "API BPS (Subject 52)", "sulawesi_pdrb_sektoral_2016_2024.csv"],
        ["7", "PDRB Kabupaten Sentra Tambang", "Struktur Ekonomi Daerah", "Triliun Rupiah", "2016-2024", "API BPS (Subject 52)", "sulawesi_pdrb_sektoral_kabupaten_2016_2024.csv"],
        ["8", "Pendapatan Asli Daerah (PAD) & Breakdown Pajak", "Kapasitas Fiskal Daerah", "Triliun Rupiah", "2016-2024", "API BPS", "sulawesi_pad_breakdown_2016_2024.csv"],
        ["9", "Luas Total Deforestasi Alam & Komoditas", "Dampak Ekologis", "Hektar (Ha)", "2014-2023", "Global Forest Watch (GFW API)", "sulawesi_gfw_master_1_dekade_2014_2023_v3.csv"],
        ["10", "Simpul Pelabuhan & Terminal Logistik", "Infrastruktur Rantai Pasok", "Titik Koordinat & DWT", "2014-2024", "Laporan Publik (KNKT, Perpres PSN, Korporasi)", "sulawesi_logistik_simpul_nikel.csv"]
    ]"""

content = content.replace(docx_rows_old, docx_rows_new)

# Update docx table param
content = content.replace(
    "add_table_1col(doc, master_headers, master_rows, [1.0, 4.0, 3.5, 2.5, 2.5, 4.5], ['C', 'L', 'L', 'C', 'C', 'L'])",
    "add_table_1col(doc, master_headers, master_rows, [1.0, 3.5, 3.0, 2.0, 2.0, 3.5, 3.0], ['C', 'L', 'L', 'C', 'C', 'L', 'L'])"
)

# 2. Update HTML
html_old = """    <tr>
      <th class="data-th" style="width:6%;">No</th>
      <th class="data-th" style="width:26%;">Nama Indikator</th>
      <th class="data-th" style="width:20%;">Kategori Analisis</th>
      <th class="data-th" style="width:12%;">Satuan Ukur</th>
      <th class="data-th" style="width:12%;">Cakupan Tahun</th>
      <th class="data-th" style="width:24%;">Institusi & Sumber Data Resmi</th>
    </tr>
  </thead>
    <tr><td class="data-td" style="text-align:center;">1</td><td class="data-td">Izin Usaha Pertambangan (IUP) Baru</td><td class="data-td">Faktor Tekanan Ekstraktif</td><td class="data-td" style="text-align:center;">Unit Izin</td><td class="data-td" style="text-align:center;">2014–2024</td><td class="data-td">Data Registry ESDM MODI (Minerbaone)</td></tr>
    <tr class="data-tr-even"><td class="data-td" style="text-align:center;">2</td><td class="data-td">Luas Wilayah Konsesi Tambang Baru</td><td class="data-td">Faktor Tekanan Ekstraktif</td><td class="data-td" style="text-align:center;">Hektar (Ha)</td><td class="data-td" style="text-align:center;">2014–2024</td><td class="data-td">Data Registry ESDM MODI (Minerbaone)</td></tr>
    <tr><td class="data-td" style="text-align:center;">3</td><td class="data-td">Kapasitas Terpasang PLTU Captive</td><td class="data-td">Infrastruktur Energi Khusus</td><td class="data-td" style="text-align:center;">Megawatt (MW)</td><td class="data-td" style="text-align:center;">2014–2024</td><td class="data-td">NGO (Global Energy Monitor / GEM)</td></tr>
    <tr class="data-tr-even"><td class="data-td" style="text-align:center;">4</td><td class="data-td">Fasilitas Smelter Nikel</td><td class="data-td">Fasilitas Industri Hilir</td><td class="data-td" style="text-align:center;">Unit Fasilitas</td><td class="data-td" style="text-align:center;">2014–2024</td><td class="data-td">Database Smelter CGS & ESDM MODI</td></tr>
    <tr><td class="data-td" style="text-align:center;">5</td><td class="data-td">Realisasi Investasi PMDN & Nikel</td><td class="data-td">Arus Modal Domestik</td><td class="data-td" style="text-align:center;">Triliun Rupiah</td><td class="data-td" style="text-align:center;">2016–2024</td><td class="data-td">API BPS & BKPM</td></tr>
    <tr class="data-tr-even"><td class="data-td" style="text-align:center;">6</td><td class="data-td">PDRB Provinsi (Ekstraktif vs Akar Rumput)</td><td class="data-td">Struktur Ekonomi Makro</td><td class="data-td" style="text-align:center;">Triliun Rupiah</td><td class="data-td" style="text-align:center;">2016–2024</td><td class="data-td">API BPS (Subject 52)</td></tr>
    <tr><td class="data-td" style="text-align:center;">7</td><td class="data-td">PDRB Kabupaten Sentra Tambang</td><td class="data-td">Struktur Ekonomi Daerah</td><td class="data-td" style="text-align:center;">Triliun Rupiah</td><td class="data-td" style="text-align:center;">2016–2024</td><td class="data-td">API BPS (Subject 52)</td></tr>
    <tr class="data-tr-even"><td class="data-td" style="text-align:center;">8</td><td class="data-td">Pendapatan Asli Daerah (PAD) & Breakdown Pajak</td><td class="data-td">Kapasitas Fiskal Daerah</td><td class="data-td" style="text-align:center;">Triliun Rupiah</td><td class="data-td" style="text-align:center;">2016–2024</td><td class="data-td">API BPS</td></tr>
    <tr><td class="data-td" style="text-align:center;">9</td><td class="data-td">Luas Total Deforestasi Alam & Komoditas</td><td class="data-td">Dampak Ekologis</td><td class="data-td" style="text-align:center;">Hektar (Ha)</td><td class="data-td" style="text-align:center;">2014–2023</td><td class="data-td">Global Forest Watch (GFW API)</td></tr>
    <tr class="data-tr-even"><td class="data-td" style="text-align:center;">10</td><td class="data-td">Simpul Pelabuhan & Terminal Logistik</td><td class="data-td">Infrastruktur Rantai Pasok</td><td class="data-td" style="text-align:center;">Titik & DWT</td><td class="data-td" style="text-align:center;">2014–2024</td><td class="data-td">Laporan Publik (KNKT, Perpres PSN, Korporasi)</td></tr>"""

html_new = """    <tr>
      <th class="data-th" style="width:4%;">No</th>
      <th class="data-th" style="width:20%;">Nama Indikator</th>
      <th class="data-th" style="width:16%;">Kategori Analisis</th>
      <th class="data-th" style="width:10%;">Satuan Ukur</th>
      <th class="data-th" style="width:10%;">Cakupan Tahun</th>
      <th class="data-th" style="width:20%;">Institusi & Sumber Data Resmi</th>
      <th class="data-th" style="width:20%;">Data File Asli</th>
    </tr>
  </thead>
  <tbody>
    <tr><td class="data-td" style="text-align:center;">1</td><td class="data-td">Izin Usaha Pertambangan (IUP) Baru</td><td class="data-td">Faktor Tekanan Ekstraktif</td><td class="data-td" style="text-align:center;">Unit Izin</td><td class="data-td" style="text-align:center;">2014-2024</td><td class="data-td">Data Registry ESDM MODI (Minerbaone)</td><td class="data-td" style="font-family:monospace; font-size:0.9em; background:#f4f4f4;">sulawesi_izin_baru_per_tahun.csv</td></tr>
    <tr class="data-tr-even"><td class="data-td" style="text-align:center;">2</td><td class="data-td">Luas Wilayah Konsesi Tambang Baru</td><td class="data-td">Faktor Tekanan Ekstraktif</td><td class="data-td" style="text-align:center;">Hektar (Ha)</td><td class="data-td" style="text-align:center;">2014-2024</td><td class="data-td">Data Registry ESDM MODI (Minerbaone)</td><td class="data-td" style="font-family:monospace; font-size:0.9em; background:#f4f4f4;">sulawesi_kawasan_nikel_luas.csv</td></tr>
    <tr><td class="data-td" style="text-align:center;">3</td><td class="data-td">Kapasitas Terpasang PLTU Captive</td><td class="data-td">Infrastruktur Energi Khusus</td><td class="data-td" style="text-align:center;">Megawatt (MW)</td><td class="data-td" style="text-align:center;">2014-2024</td><td class="data-td">NGO (Global Energy Monitor / GEM)</td><td class="data-td" style="font-family:monospace; font-size:0.9em; background:#f4f4f4;">sulawesi_pltu_captive.csv</td></tr>
    <tr class="data-tr-even"><td class="data-td" style="text-align:center;">4</td><td class="data-td">Fasilitas Smelter Nikel</td><td class="data-td">Fasilitas Industri Hilir</td><td class="data-td" style="text-align:center;">Unit Fasilitas</td><td class="data-td" style="text-align:center;">2014-2024</td><td class="data-td">Database Smelter CGS & ESDM MODI</td><td class="data-td" style="font-family:monospace; font-size:0.9em; background:#f4f4f4;">sulawesi_esdm_nikel.csv</td></tr>
    <tr><td class="data-td" style="text-align:center;">5</td><td class="data-td">Realisasi Investasi PMDN & Nikel</td><td class="data-td">Arus Modal Domestik</td><td class="data-td" style="text-align:center;">Triliun Rupiah</td><td class="data-td" style="text-align:center;">2016-2024</td><td class="data-td">API BPS & BKPM</td><td class="data-td" style="font-family:monospace; font-size:0.9em; background:#f4f4f4;">sulawesi_investasi_pmdn_2016_2024.csv</td></tr>
    <tr class="data-tr-even"><td class="data-td" style="text-align:center;">6</td><td class="data-td">PDRB Provinsi (Ekstraktif vs Akar Rumput)</td><td class="data-td">Struktur Ekonomi Makro</td><td class="data-td" style="text-align:center;">Triliun Rupiah</td><td class="data-td" style="text-align:center;">2016-2024</td><td class="data-td">API BPS (Subject 52)</td><td class="data-td" style="font-family:monospace; font-size:0.9em; background:#f4f4f4;">sulawesi_pdrb_sektoral_2016_2024.csv</td></tr>
    <tr><td class="data-td" style="text-align:center;">7</td><td class="data-td">PDRB Kabupaten Sentra Tambang</td><td class="data-td">Struktur Ekonomi Daerah</td><td class="data-td" style="text-align:center;">Triliun Rupiah</td><td class="data-td" style="text-align:center;">2016-2024</td><td class="data-td">API BPS (Subject 52)</td><td class="data-td" style="font-family:monospace; font-size:0.9em; background:#f4f4f4;">sulawesi_pdrb_sektoral_kabupaten_2016_2024.csv</td></tr>
    <tr class="data-tr-even"><td class="data-td" style="text-align:center;">8</td><td class="data-td">Pendapatan Asli Daerah (PAD) & Breakdown Pajak</td><td class="data-td">Kapasitas Fiskal Daerah</td><td class="data-td" style="text-align:center;">Triliun Rupiah</td><td class="data-td" style="text-align:center;">2016-2024</td><td class="data-td">API BPS</td><td class="data-td" style="font-family:monospace; font-size:0.9em; background:#f4f4f4;">sulawesi_pad_breakdown_2016_2024.csv</td></tr>
    <tr><td class="data-td" style="text-align:center;">9</td><td class="data-td">Luas Total Deforestasi Alam & Komoditas</td><td class="data-td">Dampak Ekologis</td><td class="data-td" style="text-align:center;">Hektar (Ha)</td><td class="data-td" style="text-align:center;">2014-2023</td><td class="data-td">Global Forest Watch (GFW API)</td><td class="data-td" style="font-family:monospace; font-size:0.9em; background:#f4f4f4;">sulawesi_gfw_master_1_dekade_2014_2023_v3.csv</td></tr>
    <tr class="data-tr-even"><td class="data-td" style="text-align:center;">10</td><td class="data-td">Simpul Pelabuhan & Terminal Logistik</td><td class="data-td">Infrastruktur Rantai Pasok</td><td class="data-td" style="text-align:center;">Titik & DWT</td><td class="data-td" style="text-align:center;">2014-2024</td><td class="data-td">Laporan Publik (KNKT, Perpres PSN, Korporasi)</td><td class="data-td" style="font-family:monospace; font-size:0.9em; background:#f4f4f4;">sulawesi_logistik_simpul_nikel.csv</td></tr>"""

html_new = html_new.replace("2014-2024", "2014–2024").replace("2014-2023", "2014–2023").replace("2016-2024", "2016–2024")

content = content.replace(html_old, html_new)


# 3. Update Markdown 
md_old = """        "| No | Nama Indikator | Kategori Analisis | Satuan Ukur | Cakupan Tahun | Institusi & Sumber Data Resmi |",
        "| :---: | :--- | :--- | :---: | :---: | :--- |",
        "| 1 | Izin Usaha Pertambangan (IUP) Baru | Faktor Tekanan Ekstraktif | Unit Izin | 2014-2024 | Data Registry ESDM MODI (Minerbaone) |",
        "| 2 | Luas Wilayah Konsesi Tambang Baru | Faktor Tekanan Ekstraktif | Hektar (Ha) | 2014-2024 | Data Registry ESDM MODI (Minerbaone) |",
        "| 3 | Kapasitas Terpasang PLTU Captive | Infrastruktur Energi Khusus | Megawatt (MW) | 2014-2024 | NGO (Global Energy Monitor / GEM) |",
        "| 4 | Fasilitas Smelter Nikel | Fasilitas Industri Hilir | Unit Fasilitas | 2014-2024 | Database Smelter CGS & ESDM MODI |",
        "| 5 | Realisasi Investasi PMDN & Nikel | Arus Modal Domestik | Triliun Rupiah | 2016-2024 | API BPS & BKPM |",
        "| 6 | PDRB Provinsi (Ekstraktif vs Akar Rumput) | Struktur Ekonomi Makro | Triliun Rupiah | 2016-2024 | API BPS (Subject 52) |",
        "| 7 | PDRB Kabupaten Sentra Tambang | Struktur Ekonomi Daerah | Triliun Rupiah | 2016-2024 | API BPS (Subject 52) |",
        "| 8 | Pendapatan Asli Daerah (PAD) & Breakdown Pajak | Kapasitas Fiskal Daerah | Triliun Rupiah | 2016-2024 | API BPS |",
        "| 9 | Luas Total Deforestasi Alam & Komoditas | Dampak Ekologis | Hektar (Ha) | 2014-2023 | Global Forest Watch (GFW API) |",
        "| 10 | Simpul Pelabuhan & Terminal Logistik | Infrastruktur Rantai Pasok | Titik Koordinat & DWT | 2014-2024 | Laporan Publik (KNKT, Perpres PSN, Korporasi) |\""""

md_new = """        "| No | Nama Indikator | Kategori Analisis | Satuan Ukur | Cakupan Tahun | Institusi & Sumber Data Resmi | Data File Asli |",
        "| :---: | :--- | :--- | :---: | :---: | :--- | :--- |",
        "| 1 | Izin Usaha Pertambangan (IUP) Baru | Faktor Tekanan Ekstraktif | Unit Izin | 2014-2024 | Data Registry ESDM MODI (Minerbaone) | `sulawesi_izin_baru_per_tahun.csv` |",
        "| 2 | Luas Wilayah Konsesi Tambang Baru | Faktor Tekanan Ekstraktif | Hektar (Ha) | 2014-2024 | Data Registry ESDM MODI (Minerbaone) | `sulawesi_kawasan_nikel_luas.csv` |",
        "| 3 | Kapasitas Terpasang PLTU Captive | Infrastruktur Energi Khusus | Megawatt (MW) | 2014-2024 | NGO (Global Energy Monitor / GEM) | `sulawesi_pltu_captive.csv` |",
        "| 4 | Fasilitas Smelter Nikel | Fasilitas Industri Hilir | Unit Fasilitas | 2014-2024 | Database Smelter CGS & ESDM MODI | `sulawesi_esdm_nikel.csv` |",
        "| 5 | Realisasi Investasi PMDN & Nikel | Arus Modal Domestik | Triliun Rupiah | 2016-2024 | API BPS & BKPM | `sulawesi_investasi_pmdn_2016_2024.csv` |",
        "| 6 | PDRB Provinsi (Ekstraktif vs Akar Rumput) | Struktur Ekonomi Makro | Triliun Rupiah | 2016-2024 | API BPS (Subject 52) | `sulawesi_pdrb_sektoral_2016_2024.csv` |",
        "| 7 | PDRB Kabupaten Sentra Tambang | Struktur Ekonomi Daerah | Triliun Rupiah | 2016-2024 | API BPS (Subject 52) | `sulawesi_pdrb_sektoral_kabupaten_2016_2024.csv` |",
        "| 8 | Pendapatan Asli Daerah (PAD) & Breakdown Pajak | Kapasitas Fiskal Daerah | Triliun Rupiah | 2016-2024 | API BPS | `sulawesi_pad_breakdown_2016_2024.csv` |",
        "| 9 | Luas Total Deforestasi Alam & Komoditas | Dampak Ekologis | Hektar (Ha) | 2014-2023 | Global Forest Watch (GFW API) | `sulawesi_gfw_master_1_dekade_2014_2023_v3.csv` |",
        "| 10 | Simpul Pelabuhan & Terminal Logistik | Infrastruktur Rantai Pasok | Titik Koordinat & DWT | 2014-2024 | Laporan Publik (KNKT, Perpres PSN, Korporasi) | `sulawesi_logistik_simpul_nikel.csv` |\""""

content = content.replace(md_old, md_new)

if html_old in content:
    print("WARNING: html_old not found!")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Berhasil mengupdate bab1 bismillah.py")
