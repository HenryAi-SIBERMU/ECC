#!/usr/bin/env python3
"""
Generator Metodologi Versi Compact Bab 1 — GAYA AKADEMIS TERPADU (CELIOS)
Mengadopsi arsitektur metodologi ringkas dari proyek 8.1 Celios4-EBTsmallstack:
- FORMAT: 1 KOLOM PENUH (Single Column Layout)
- PANJANG: 2–3 Halaman Maksimal (Elegan, tidak sesak, proporsional)
- OPERASIONALISASI INDIKATOR: 10 Indikator Empiris Lengkap (Matriks Indikator & Sumber Data Resmi)
- FORMULASI: Formula box bernotasi standar akademik dan praktis
- ALUR RISET: 4 Fase Terintegrasi (Akuisisi, Reklasifikasi, Inferensial, Sintesis)
- SINKRONISASI: Menghasilkan dokumen DOCX dan Markdown sekaligus.
"""

import os
import shutil
from pathlib import Path

try:
    from docx import Document
    from docx.shared import Pt, RGBColor, Cm
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-docx"])
    from docx import Document
    from docx.shared import Pt, RGBColor, Cm
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement

# ── Palet Warna Resmi CELIOS ─────────────────────────────────
G_DARK  = RGBColor(0x1B, 0x5E, 0x20)  # Forest Dark Green
G_MID   = RGBColor(0x2E, 0x7D, 0x32)  # Celios Accent Green
G_LIGHT = RGBColor(0x38, 0x8E, 0x3C)  # Medium Green
C_BODY  = RGBColor(0x22, 0x22, 0x22)  # Charcoal Body Text
C_GREY  = RGBColor(0x55, 0x55, 0x55)  # Muted Grey Text
C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)  # Pure White

# ── Pembantu XML & Format Word ──────────────────────────────
def set_cell_borders(cell, top=None, left=None, bottom=None, right=None):
    tcPr = cell._tc.get_or_add_tcPr()
    bdr  = OxmlElement('w:tcBorders')
    for edge, cfg in [('top', top), ('left', left), ('bottom', bottom), ('right', right)]:
        el = OxmlElement(f'w:{edge}')
        if cfg is None:
            el.set(qn('w:val'), 'none')
        else:
            for k, v in cfg.items():
                el.set(qn(f'w:{k}'), str(v))
        bdr.append(el)
    tcPr.append(bdr)

def cell_margin(cell, left=100, right=100, top=60, bottom=60):
    tcPr = cell._tc.get_or_add_tcPr()
    m    = OxmlElement('w:tcMar')
    for side, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        el = OxmlElement(f'w:{side}')
        el.set(qn('w:w'), str(val))
        el.set(qn('w:type'), 'dxa')
        m.append(el)
    tcPr.append(m)

def para_shd(p, fill):
    pPr = p._p.get_or_add_pPr()
    s   = OxmlElement('w:shd')
    s.set(qn('w:val'), 'clear')
    s.set(qn('w:color'), 'auto')
    s.set(qn('w:fill'), fill)
    pPr.append(s)

def cell_shd(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    s    = OxmlElement('w:shd')
    s.set(qn('w:val'), 'clear')
    s.set(qn('w:color'), 'auto')
    s.set(qn('w:fill'), fill)
    tcPr.append(s)

def para_border_bottom(p, color='2E7D32', sz='6'):
    pPr  = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    el   = OxmlElement('w:bottom')
    el.set(qn('w:val'), 'single')
    el.set(qn('w:sz'), sz)
    el.set(qn('w:space'), '2')
    el.set(qn('w:color'), color)
    pBdr.append(el)
    pPr.append(pBdr)

def para_border_left(p, color='2E7D32', sz='12'):
    pPr  = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    el   = OxmlElement('w:left')
    el.set(qn('w:val'), 'single')
    el.set(qn('w:sz'), sz)
    el.set(qn('w:space'), '6')
    el.set(qn('w:color'), color)
    pBdr.append(el)
    pPr.append(pBdr)

def all_border_para(p, color='1B5E20', sz='6'):
    pPr  = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    for side in ['top', 'left', 'bottom', 'right']:
        el = OxmlElement(f'w:{side}')
        el.set(qn('w:val'), 'single')
        el.set(qn('w:sz'), sz)
        el.set(qn('w:space'), '3')
        el.set(qn('w:color'), color)
        pBdr.append(el)
    pPr.append(pBdr)

# ── Pembantu Penulisan Konten ───────────────────────────────
def add_run(p, text, bold=False, italic=False, pt=8.5, color=None, mono=False):
    r = p.add_run(text)
    r.bold           = bold
    r.italic         = italic
    r.font.size      = Pt(pt)
    r.font.color.rgb = color if color else C_BODY
    if mono:
        r.font.name = 'Courier New'
        r._element.rPr.rFonts.set(qn('w:ascii'), 'Courier New')
    return r

def add_h2(doc, num, title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(11)
    p.paragraph_format.space_after  = Pt(3)
    p.paragraph_format.keep_with_next = True
    para_border_bottom(p, color='2E7D32', sz='6')
    add_run(p, f"{num}.  {title.upper()}", bold=True, pt=10, color=G_DARK)

def add_h3(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(7)
    p.paragraph_format.space_after  = Pt(2)
    p.paragraph_format.keep_with_next = True
    add_run(p, text, bold=True, pt=9, color=G_MID)

def add_body(doc, parts, after=4):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.line_spacing = 1.15
    for text, bold, italic in parts:
        add_run(p, text, bold=bold, italic=italic, pt=8.5)
    return p

def add_formula(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(4)
    p.paragraph_format.left_indent  = Pt(8)
    para_shd(p, 'EDF7EE')
    add_run(p, text, pt=8, color=G_MID, mono=True)

def add_caption(doc, caption_text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(5)
    p.paragraph_format.space_after  = Pt(2)
    add_run(p, caption_text, bold=True, italic=True, pt=8.5, color=G_MID)
    return p

def add_note_box(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after  = Pt(5)
    p.paragraph_format.left_indent  = Pt(8)
    para_border_left(p, color='2E7D32', sz='12')
    para_shd(p, 'F1F8E9')
    add_run(p, text, italic=True, pt=8, color=C_GREY)

def add_table_styled(doc, headers, rows, col_widths_cm, alignments=None):
    tbl = doc.add_table(rows=1 + len(rows), cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False

    bd_subtle = {'val': 'single', 'sz': '4', 'color': 'D0D7DE', 'space': '0'}
    
    # Header Row
    for j, (h, w) in enumerate(zip(headers, col_widths_cm)):
        c = tbl.rows[0].cells[j]
        c.width = Cm(w)
        cell_shd(c, '2E7D32')
        cell_margin(c, left=80, right=80, top=50, bottom=50)
        set_cell_borders(c, top=bd_subtle, left=bd_subtle, bottom=bd_subtle, right=bd_subtle)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after  = Pt(2)
        add_run(p, h, bold=True, pt=7.5, color=C_WHITE)

    # Data Rows
    for i, row_data in enumerate(rows):
        fill = 'F9FBF9' if i % 2 == 0 else 'FFFFFF'
        for j, val in enumerate(row_data):
            c = tbl.cell(i + 1, j)
            c.width = Cm(col_widths_cm[j])
            c.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            cell_shd(c, fill)
            cell_margin(c, left=80, right=80, top=40, bottom=40)
            set_cell_borders(c, top=bd_subtle, left=bd_subtle, bottom=bd_subtle, right=bd_subtle)
            p = c.paragraphs[0]
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after  = Pt(1)
            
            # Text alignment
            if alignments and j < len(alignments):
                align = alignments[j]
                if align == 'C':
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                elif align == 'R':
                    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT

            add_run(p, str(val), pt=7.5, color=C_BODY)

    p_space = doc.add_paragraph()
    p_space.paragraph_format.space_before = Pt(0)
    p_space.paragraph_format.space_after  = Pt(3)
    return tbl


def generate_bab1_compact():
    print("[1/3] Membangun dokumen compact Bab 1 (Format 1-Kolom, 2-3 Halaman)...")
    
    doc = Document()
    sec = doc.sections[0]
    sec.page_width    = Cm(21.0)
    sec.page_height   = Cm(29.7)
    sec.left_margin   = Cm(2.0)
    sec.right_margin  = Cm(2.0)
    sec.top_margin    = Cm(1.8)
    sec.bottom_margin = Cm(1.8)

    doc.styles['Normal'].font.name = 'Calibri'
    doc.styles['Normal'].font.size = Pt(8.5)

    # ── HEADER DOKUMEN ──────────────────────────────────────────
    p_t = doc.add_paragraph()
    p_t.paragraph_format.space_before = Pt(0)
    p_t.paragraph_format.space_after  = Pt(2)
    add_run(p_t, "METODOLOGI PENELITIAN: BAB 1 — EKSPANSI INDUSTRI EKSTRAKTIF DAN INFRASTRUKTUR PENUNJANG DI PULAU SULAWESI",
            bold=True, pt=12, color=G_DARK)

    p_s = doc.add_paragraph()
    p_s.paragraph_format.space_before = Pt(0)
    p_s.paragraph_format.space_after  = Pt(8)
    para_border_bottom(p_s, color='1B5E20', sz='8')
    add_run(p_s, "CELIOS (Center of Economic and Law Studies) · Audit Spasial-Statistik D3TLH Sulawesi (2014–2024) · Ringkasan Eksekutif Metodologis",
            italic=True, pt=8, color=C_GREY)

    # ── A. DESAIN PENELITIAN & TUJUAN ───────────────────────────
    add_h2(doc, "A", "Desain Penelitian & Tujuan")
    add_body(doc, [
        ("Penelitian ini menggunakan ", False, False),
        ("desain audit spasial-statistik kuantitatif terintegrasi", True, False),
        (" untuk membedah akselerasi ekspansi industri ekstraktif (tambang nikel, fasilitas pemurnian smelter, dan kawasan industri bertenaga PLTU captive batubara) di enam provinsi Pulau Sulawesi sepanjang satu dekade (", False, False),
        ("2014–2024", True, False),
        ("). Riset ini memanfaatkan data tabular panel resmi lintas kementerian dan lembaga yang disinkronkan secara spasial untuk mengatasi bias perataan makro. Tiga tujuan utama riset meliputi:\n", False, False),
        ("1. ", True, False), ("Mengukur Derajat Dominasi Sektoral: ", True, False),
        ("Mendekomposisi struktur PDRB provinsi dan kabupaten guna membuktikan pergeseran monolitik menuju sektor ekstraktif mengorbankan ekonomi pertanian rakyat.\n", False, False),
        ("2. ", True, False), ("Memetakan Konsentrasi Spasial Klaster Industri: ", True, False),
        ("Mengidentifikasi pengelompokan geografis 778 smelter, 9.825 MW PLTU captive, serta 574 izin tambang nikel baru seluas 819.452 Ha.\n", False, False),
        ("3. ", True, False), ("Menguji Kausalitas Tekanan Industri vs Deforestasi: ", True, False),
        ("Membuktikan secara inferensial signifikansi hubungan antara ekspansi pertambangan/energi dengan laju kehilangan tutupan hutan alam primer dan komoditas.", False, False)
    ])

    # ── B. SUMBER DATA & CAKUPAN WILAYAH ────────────────────────
    add_h2(doc, "B", "Sumber Data & Cakupan Wilayah")
    add_body(doc, [
        ("Riset ini bersandar secara ketat pada data sekunder resmi dari otoritas statistik, kementerian teknis, dan lembaga pemantau global independen yang telah melalui audit konsistensi: ", False, False),
        ("Badan Pusat Statistik (BPS)", True, False), (" (Subject 52 PDRB Lapangan Usaha & Keuangan Daerah), ", False, False),
        ("Kementerian ESDM", True, False), (" (MODI Minerbaone & Database Smelter CGS), ", False, False),
        ("Kementerian Investasi / BKPM", True, False), (" (Realisasi PMDN Sektoral), ", False, False),
        ("Global Energy Monitor (GEM)", True, False), (" (Coal Plant Tracker), ", False, False),
        ("Global Forest Watch / Hansen UMD", True, False), (" (Tree Cover Loss & Commodity Drivers), serta ", False, False),
        ("Komite Nasional Keselamatan Transportasi (KNKT)", True, False), (" dan Perpres PSN (Simpul Logistik Maritim). Seluruh observasi dihimpun dalam struktur ", False, False),
        ("data panel provinsi-tahun (N = 60 observasi: 6 provinsi × 10 tahun)", True, False),
        (" untuk menjamin validitas pengujian parametrik dan non-parametrik.", False, False)
    ])

    # ── C. OPERASIONALISASI VARIABEL & INDIKATOR RISET ─────────
    add_h2(doc, "C", "Operasionalisasi Variabel & Indikator Riset")
    add_body(doc, [
        ("Seluruh variabel kuantitatif, kategori analisis, satuan ukur, periode observasi, dan institusi primer resmi yang digunakan dalam penelitian ini disajikan pada matriks operasionalisasi berikut:", False, False)
    ])

    table_10_indikator = [
        ["1", "Izin Usaha Pertambangan (IUP) Baru", "Faktor Tekanan Ekstraktif", "Unit Izin", "2014–2024", "Data Registry ESDM MODI (Minerbaone)"],
        ["2", "Luas Wilayah Konsesi Tambang Baru", "Faktor Tekanan Ekstraktif", "Hektar (Ha)", "2014–2024", "Data Registry ESDM MODI (Minerbaone)"],
        ["3", "Kapasitas Terpasang PLTU Captive", "Infrastruktur Energi Khusus", "Megawatt (MW)", "2014–2024", "Global Energy Monitor (GEM Tracker)"],
        ["4", "Fasilitas Smelter Nikel", "Fasilitas Industri Hilir", "Unit Fasilitas", "2014–2024", "Database Smelter CGS & ESDM MODI"],
        ["5", "Realisasi Investasi PMDN & Nikel", "Arus Modal Domestik", "Triliun Rp", "2016–2024", "API BPS & Kementerian Investasi / BKPM"],
        ["6", "PDRB Provinsi (Ekstraktif vs Akar Rumput)", "Struktur Ekonomi Makro", "Triliun Rp", "2016–2024", "API BPS (Subject 52: PDRB Lapangan Usaha)"],
        ["7", "PDRB Kabupaten Sentra Tambang", "Struktur Ekonomi Daerah", "Triliun Rp", "2016–2024", "API BPS (Subject 52 Kabupaten/Kota)"],
        ["8", "Pendapatan Asli Daerah (PAD) & Pajak", "Kapasitas Fiskal Daerah", "Triliun Rp", "2016–2024", "API BPS (Statistik Keuangan Daerah)"],
        ["9", "Luas Total Deforestasi Alam & Komoditas", "Dampak Ekologis Lanskap", "Hektar (Ha)", "2014–2023", "Global Forest Watch (GFW API / Hansen UMD)"],
        ["10", "Simpul Pelabuhan & Terminal Logistik Ekspor", "Infrastruktur Rantai Pasok", "Titik & DWT", "2014–2024", "KNKT, Regulasi Perpres PSN & Korporasi"]
    ]

    add_table_styled(
        doc,
        headers=["#", "Nama Indikator Empiris", "Kategori Analisis", "Satuan", "Periode", "Institusi & Sumber Data Resmi"],
        rows=table_10_indikator,
        col_widths_cm=[0.8, 4.5, 3.2, 1.8, 2.0, 4.7],
        alignments=['C', 'L', 'L', 'C', 'C', 'L']
    )

    # ── D. KERANGKA ANALISIS & FORMULASI MATEMATIS ──────────────
    add_h2(doc, "D", "Kerangka Analisis & Formulasi Matematis")

    add_h3(doc, "1.1 Konteks Makro: Breakdown PDRB per Komoditas")
    add_body(doc, [
        ("Tujuh belas sektor KBLI 2020 direklasifikasi menjadi tiga klaster makro berdasarkan relasi hukum hilirisasi nikel (UU No. 3/2020 jo. PP No. 96/2021): ", False, False),
        ("Klaster Ekstraktif", True, False), (" (Pertambangan B, Industri Logam C24, dan Pengadaan Listrik D), ", False, False),
        ("Klaster Akar Rumput", True, False), (" (Pertanian, Kehutanan & Perikanan A), serta ", False, False),
        ("Klaster Jasa & Manufaktur Lain", True, False),
        (". Konfigurasi reklasifikasi ini dirancang untuk mengisolasi porsi kontribusi murni sektor industri hilirisasi terhadap total struktur perekonomian daerah:", False, False)
    ])
    add_formula(doc, "Pangsa Sektor Ekstraktif (%) = [ PDRB Ekstraktif (B + C24 + D) / Total PDRB ] × 100")
    add_body(doc, [
        ("Untuk membongkar ilusi agregat provinsi, PDRB didekomposisi ke seluruh kabupaten/kota sentra nikel guna mengukur derajat polarisasi ekonomi industri ekstraktif terhadap basis mata pencaharian pertanian-perikanan lokal:", False, False)
    ])
    add_formula(doc, "Rasio Kesenjangan Spasial = PDRB Sektor Ekstraktif (Kabupaten) / PDRB Pertanian Rakyat (Kabupaten)")

    add_h3(doc, "1.2 Konsentrasi Kawasan Industri & PLTU Captive")
    add_body(doc, [
        ("Derajat konsentrasi fasilitas pengolahan nikel dan kapasitas pembangkit listrik captive batubara diukur menggunakan rasio aglomerasi spasial untuk memetakan pemusatan beban energi dan lingkungan antar-wilayah:", False, False)
    ])
    add_formula(doc, "Porsi Konsentrasi Sentra (%) = [ Kapasitas Sentra Industri (MW) / Total Kapasitas Se-Sulawesi (MW) ] × 100")

    add_h3(doc, "1.3 Tren Pertumbuhan Izin Tambang Baru & Uji Signifikansi Statistik")
    add_body(doc, [
        ("Akumulasi izin konsesi tambang baru dievaluasi laju pertumbuhannya dan dinormalisasi ke dalam unit waktu harian untuk mengukur kecepatan konversi bentang lahan alami menjadi kawasan pertambangan:", False, False)
    ])
    add_formula(doc, "Laju Alih Ruang Harian (Ha/Hari) = Total Luas Konsesi Tambang Baru (Ha) / Jumlah Hari Observasi (t)")
    add_body(doc, [
        ("Pengujian inferensial menggunakan desain matriks kontinjensi 2×2 berbasis ", False, False),
        ("ambang median panel provinsi-tahun (N = 60)", True, False),
        (". Uji Chi-Square independensi (α = 5%, df = 1) diterapkan untuk menguji signifikansi hubungan bivariat, sedangkan rasio peluang (Odds Ratio) mengukur magnitudo kelipatan risiko dampak ekologis:", False, False)
    ])
    add_formula(doc, "χ² = Σ [ (O_ij - E_ij)² / E_ij ]   |   Odds Ratio (OR) = (a × d) / (b × c)")

    add_caption(doc, "Tabel 1.5b: Konfigurasi Variabel Uji Chi-Square (Sub-bab 1.3)")
    table_1_5b_rows = [
        ["Variabel Independen (X)", "Jumlah Izin Baru (IUP) / Luas Konsesi Baru (Ha)"],
        ["Variabel Dependen (Y)", "Deforestasi Komoditas (Ha) / Total Deforestasi Alam (Ha)"],
        ["Hipotesis Nol (H0)", "Tingkat penerbitan izin/luas konsesi tidak berhubungan dengan laju deforestasi."],
        ["Hipotesis Alternatif (H1)", "Ada hubungan positif antara tingginya penerbitan izin dengan tingginya laju deforestasi."],
        ["Decision Rule (Alpha 5%)", "Jika P-Value < 0.05, maka Tolak H0 (terbukti signifikan bahwa ekspansi perizinan mendorong deforestasi)."],
        ["Threshold Kategori", "Nilai Median Data Panel (N=60): X >= 2.0 izin; Y >= 10,961.8 Ha."],
        ["Orientasi Odds Ratio", "OR = ( a × d ) / ( b × c ) dengan a = Izin Tinggi & Deforestasi Tinggi; mengukur risiko deforestasi tinggi pada kelompok penerbitan izin tinggi."]
    ]

    add_table_styled(
        doc,
        headers=["Komponen Uji", "Definisi Variabel (Sub-bab 1.3)"],
        rows=table_1_5b_rows,
        col_widths_cm=[4.5, 12.5],
        alignments=['L', 'L']
    )

    add_h3(doc, "1.4 Analisis Realisasi Investasi PMDN dan Dampak Terhadap Tutupan Hutan")
    add_body(doc, [
        ("Analisis arus modal investasi PMDN mengevaluasi elastisitas suntikan modal terhadap laju alih fungsi hutan dan emisi komoditas. Formulasi pengujian inferensial Chi-Square dan Odds Ratio pada Sub-bab 1.4 mengadopsi protokol pengujian kontinjensi 2×2 yang sama, dengan variabel independen realisasi investasi modal domestik (X > Rp3.146,4 Miliar) dan evaluasi efek jeda waktu (time-lag) ekspansi fisik di lapangan.", False, False)
    ])

    add_h3(doc, "1.5 Pelabuhan Ekspor: Ke Mana Nikel Sulawesi Dikirim?")
    add_body(doc, [
        ("Verifikasi titik pelabuhan dan terminal khusus ekspor nikel dilakukan melalui protokol triangulasi informasi publik (OSINT): Laporan Investigasi Keselamatan Transportasi Laut KNKT (bobot muatan tongkang hingga 52.378 DWT), lampiran regulasi Proyek Strategis Nasional (Perpres No. 109/2020), laporan keberlanjutan emiten terbuka (PT Vale Indonesia Tbk dan PT ANTAM Tbk), serta publikasi riset audit independen mengenai operasional pelabuhan khusus.", False, False)
    ])

    add_h3(doc, "1.6 Peta Jalur Distribusi Logistik Nikel Sulawesi")
    add_body(doc, [
        ("Pemodelan spasial rute pelayaran internasional pengangkutan produk olahan nikel dari simpul pelabuhan Sulawesi menuju negara tujuan utama (Tiongkok dan Jepang) dimodelkan menggunakan persamaan parametrik kurva Bézier kuadratik di atas koordinat bola bumi guna memetakan jalur lintas laut aktual:", False, False)
    ])
    add_formula(doc, "Kurva(t) = (1 - t)² × Titik_Asal + 2(1 - t)t × Titik_Kontrol + t² × Titik_Tujuan")

    # ── E. KORESPONDENSI METODOLOGI TERHADAP SUB-BAB LAPORAN ────
    add_h2(doc, "E", "Korespondensi Metodologi terhadap Sub-bab Laporan Bab 1")
    add_body(doc, [
        ("Setiap sub-bab analitis pada Bab 1 ditopang oleh metode kuantitatif yang presisi dan menghasilkan sintesis bukti empiris terstandarisasi sebagaimana dirangkum pada matriks berikut:", False, False)
    ])

    table_korespondensi = [
        ["Sub-bab 1.1", "Struktur Makro PDRB Provinsi & Kabupaten", "Reklasifikasi Hukum KBLI, Pangsa Sektoral, Rasio Kesenjangan Spasial"],
        ["Sub-bab 1.2", "Kawasan Industri & PLTU Captive", "Analisis Aglomerasi Spasial, Rasio Kapasitas Off-grid"],
        ["Sub-bab 1.3", "Tren Perizinan Konsesi Tambang", "Deret Waktu Tahunan, Laju Alih Ruang Ha/Hari, Uji Chi-Square (χ²)"],
        ["Sub-bab 1.4", "Arus Investasi PMDN & Deforestasi", "Uji Non-parametrik Chi-Square (χ²), Odds Ratio (OR), Efek Time-lag"],
        ["Sub-bab 1.5", "Simpul Pelabuhan Ekspor & Terminal Khusus", "Triangulasi Validasi Silang (OSINT: KNKT, Regulasi PSN, Laporan Emiten)"],
        ["Sub-bab 1.6", "Peta Jalur Distribusi Logistik Maritim", "Pemodelan Spasial Rute Parametrik Kurva Bézier Kuadratik (Scattergeo)"]
    ]

    add_table_styled(
        doc,
        headers=["Sub-bab", "Fokus Kajian Empiris", "Metode Analitis Utama"],
        rows=table_korespondensi,
        col_widths_cm=[2.5, 5.5, 9.0],
        alignments=['C', 'L', 'L']
    )

    # ── F. BAGAN ALUR KERANGKA KERJA RISET BAB 1 ────────────────
    add_h2(doc, "F", "Bagan Alur Kerangka Kerja Riset (Research Workflow)")
    add_body(doc, [
        ("Kerangka kerja operasional metodologi Bab 1 berjalan secara sekuensial melalui empat fase sistematis:", False, False)
    ])

    table_workflow = [
        ["Fase I", "Akuisisi & Kurasi Data", "Pengumpulan basis data resmi terbuka: BPS (PDRB & Keuangan Daerah), ESDM MODI (IUP & Konsesi), GEM (PLTU), BKPM (PMDN), GFW (Deforestasi), KNKT (Logistik)."],
        ["Fase II", "Reklasifikasi Hukum & Spasial", "Standardisasi klasifikasi ekonomi berbasis mandat regulasi hilirisasi (UU 3/2020 & Perpres 112/2022) menjadi 3 klaster makro serta dekomposisi data ke level kabupaten."],
        ["Fase III", "Pengujian Statistik Inferensial", "Konstruksi tabel kontinjensi 2×2 berbasis ambang median (Panel N=60), uji independensi Chi-Square (χ²), perhitungan rasio peluang risiko (Odds Ratio), dan uji asosiasi."],
        ["Fase IV", "Pemodelan Spasial & Sintesis Kebijakan", "Pemodelan geospasial alur pasok maritim dengan kurva Bézier, sintesis disparitas ekonomi makro, serta perumusan bukti empiris dominasi ekstraktif bagi dokumen D3TLH."]
    ]

    add_table_styled(
        doc,
        headers=["Fase Riset", "Tahapan Metodologis", "Rincian Operasional & Bahan Analisis"],
        rows=table_workflow,
        col_widths_cm=[2.0, 4.5, 10.5],
        alignments=['C', 'L', 'L']
    )

    # Box Output Kesimpulan
    p_box = doc.add_paragraph()
    p_box.paragraph_format.space_before = Pt(4)
    p_box.paragraph_format.space_after  = Pt(4)
    all_border_para(p_box, color='1B5E20', sz='8')
    para_shd(p_box, 'F1F8E9')
    add_run(p_box, "KERANGKA KELUARAN METODOLOGIS BAB 1:\n", bold=True, pt=8.5, color=G_DARK)
    add_run(p_box, "1. Konfigurasi Dekomposisi Sektoral: Menghasilkan matriks pangsa dan rasio kesenjangan spasial guna mengukur ketergantungan monolitik ekonomi makro-mikro.\n"
                   "2. Konfigurasi Aglomerasi Geospasial: Memetakan derajat konsentrasi spasial fasilitas hilirisasi, pembangkit off-grid, dan simpul maritim rantai pasok ekspor.\n"
                   "3. Konfigurasi Inferensial Tabulasi Silang: Menetapkan protokol pengujian Chi-Square dan Odds Ratio untuk membuktikan signifikansi kausalitas tekanan industri terhadap degradasi lingkungan.",
            pt=8, color=C_BODY)

    add_note_box(doc, (
        "Catatan Metodologis: Seluruh analisis statistik kuantitatif dalam dokumen ini dijalankan pada matriks data panel "
        "provinsi-tahun (N = 60 observasi) dan kabupaten sentra industri. Angka komputasi dan sebaran spasial terperinci "
        "terintegrasi penuh pada naskah laporan Bab 1 dan antarmuka interaktif dashboard CELIOS."
    ))

    # ── SIMPAN DOKUMEN DOCX (DUAL SAVE) ─────────────────────────
    out_dir_compact = Path(__file__).resolve().parent
    out_dir_bab1    = out_dir_compact.parent.parent / "bab_1"

    docx_compact = out_dir_compact / "Metodologi_Bab1_Ekspansi_Industri_Compact.docx"
    docx_bab1    = out_dir_bab1 / "Metodologi_Bab1_Ekspansi_Industri_Compact.docx"
    
    doc.save(str(docx_compact))
    shutil.copyfile(docx_compact, docx_bab1)
    print(f"  [OK] Tersimpan DOCX: {docx_compact}")
    print(f"  [OK] Salinan DOCX : {docx_bab1}")

    # ── GENERATE MARKDOWN PADANAN ───────────────────────────────
    print("[2/3] Membangun dokumen Markdown padanan...")
    MD_CONTENT = """# METODOLOGI PENELITIAN: BAB 1 — EKSPANSI INDUSTRI EKSTRAKTIF DAN INFRASTRUKTUR PENUNJANG DI PULAU SULAWESI
*CELIOS (Center of Economic and Law Studies) · Audit Spasial-Statistik D3TLH Sulawesi (2014–2024) · Ringkasan Eksekutif Metodologis*

---

## A. Desain Penelitian & Tujuan
Penelitian ini menggunakan **desain audit spasial-statistik kuantitatif terintegrasi** untuk membedah akselerasi ekspansi industri ekstraktif (tambang nikel, fasilitas pemurnian smelter, dan kawasan industri bertenaga PLTU captive batubara) di enam provinsi Pulau Sulawesi sepanjang satu dekade (**2014–2024**). Riset ini memanfaatkan data tabular panel resmi lintas kementerian dan lembaga yang disinkronkan secara spasial untuk mengatasi bias perataan makro. Tiga tujuan utama riset meliputi:

1. **Mengukur Derajat Dominasi Sektoral:** Mendekomposisi struktur PDRB provinsi dan kabupaten guna membuktikan pergeseran monolitik menuju sektor ekstraktif mengorbankan ekonomi pertanian rakyat.
2. **Memetakan Konsentrasi Spasial Klaster Industri:** Mengidentifikasi pengelompokan geografis 778 smelter, 9.825 MW PLTU captive, serta 574 izin tambang nikel baru seluas 819.452 Ha.
3. **Menguji Kausalitas Tekanan Industri vs Deforestasi:** Membuktikan secara inferensial signifikansi hubungan antara ekspansi pertambangan/energi dengan laju kehilangan tutupan hutan alam primer dan komoditas.

---

## B. Sumber Data & Cakupan Wilayah
Riset ini bersandar secara ketat pada data sekunder resmi dari otoritas statistik, kementerian teknis, dan lembaga pemantau global independen yang telah melalui audit konsistensi: **Badan Pusat Statistik (BPS)** (Subject 52 PDRB Lapangan Usaha & Keuangan Daerah), **Kementerian ESDM** (MODI Minerbaone & Database Smelter CGS), **Kementerian Investasi / BKPM** (Realisasi PMDN Sektoral), **Global Energy Monitor (GEM)** (Coal Plant Tracker), **Global Forest Watch / Hansen UMD** (Tree Cover Loss & Commodity Drivers), serta **Komite Nasional Keselamatan Transportasi (KNKT)** dan Perpres PSN (Simpul Logistik Maritim). Seluruh observasi dihimpun dalam struktur **data panel provinsi-tahun (N = 60 observasi: 6 provinsi × 10 tahun)** untuk menjamin validitas pengujian parametrik dan non-parametrik.

---

## C. Operasionalisasi Variabel & Indikator Riset
Seluruh variabel kuantitatif, kategori analisis, satuan ukur, periode observasi, dan institusi primer resmi yang digunakan dalam penelitian ini disajikan secara komprehensif pada matriks operasionalisasi berikut:

##### Matriks Operasionalisasi Variabel dan Sumber Data Resmi
| # | Nama Indikator Empiris | Kategori Analisis | Satuan | Periode | Institusi & Sumber Data Resmi |
| :---: | :--- | :--- | :---: | :---: | :--- |
| 1 | Izin Usaha Pertambangan (IUP) Baru | Faktor Tekanan Ekstraktif | Unit Izin | 2014–2024 | Data Registry ESDM MODI (Minerbaone) |
| 2 | Luas Wilayah Konsesi Tambang Baru | Faktor Tekanan Ekstraktif | Hektar (Ha) | 2014–2024 | Data Registry ESDM MODI (Minerbaone) |
| 3 | Kapasitas Terpasang PLTU Captive | Infrastruktur Energi Khusus | Megawatt (MW) | 2014–2024 | Global Energy Monitor (GEM Tracker) |
| 4 | Fasilitas Smelter Nikel | Fasilitas Industri Hilir | Unit Fasilitas | 2014–2024 | Database Smelter CGS & ESDM MODI |
| 5 | Realisasi Investasi PMDN & Nikel | Arus Modal Domestik | Triliun Rp | 2016–2024 | API BPS & Kementerian Investasi / BKPM |
| 6 | PDRB Provinsi (Ekstraktif vs Akar Rumput) | Struktur Ekonomi Makro | Triliun Rp | 2016–2024 | API BPS (Subject 52: PDRB Lapangan Usaha) |
| 7 | PDRB Kabupaten Sentra Tambang | Struktur Ekonomi Daerah | Triliun Rp | 2016–2024 | API BPS (Subject 52 Kabupaten/Kota) |
| 8 | Pendapatan Asli Daerah (PAD) & Pajak | Kapasitas Fiskal Daerah | Triliun Rp | 2016–2024 | API BPS (Statistik Keuangan Daerah) |
| 9 | Luas Total Deforestasi Alam & Komoditas | Dampak Ekologis Lanskap | Hektar (Ha) | 2014–2023 | Global Forest Watch (GFW API / Hansen UMD) |
| 10 | Simpul Pelabuhan & Terminal Logistik Ekspor | Infrastruktur Rantai Pasok | Titik & DWT | 2014–2024 | KNKT, Regulasi Perpres PSN & Korporasi |

---

## D. Kerangka Analisis & Formulasi Matematis

### 1.1 Konteks Makro: Breakdown PDRB per Komoditas
Tujuh belas sektor KBLI 2020 direklasifikasi menjadi tiga klaster makro berdasarkan relasi hukum hilirisasi nikel (UU No. 3/2020 jo. PP No. 96/2021): **Klaster Ekstraktif** (Pertambangan B, Industri Logam C24, dan Pengadaan Listrik D), **Klaster Akar Rumput** (Pertanian, Kehutanan & Perikanan A), serta **Klaster Jasa & Manufaktur Lain**. Konfigurasi reklasifikasi ini dirancang untuk mengisolasi porsi kontribusi murni sektor industri hilirisasi terhadap total struktur perekonomian daerah:

> `Pangsa Sektor Ekstraktif (%) = [ PDRB Ekstraktif (B + C24 + D) / Total PDRB ] × 100`

Untuk membongkar ilusi agregat provinsi, PDRB didekomposisi ke seluruh kabupaten/kota sentra nikel guna mengukur derajat polarisasi ekonomi industri ekstraktif terhadap basis mata pencaharian pertanian-perikanan lokal:

> `Rasio Kesenjangan Spasial = PDRB Sektor Ekstraktif (Kabupaten) / PDRB Pertanian Rakyat (Kabupaten)`

### 1.2 Konsentrasi Kawasan Industri & PLTU Captive
Derajat konsentrasi fasilitas pengolahan nikel dan kapasitas pembangkit listrik captive batubara diukur menggunakan rasio aglomerasi spasial untuk memetakan pemusatan beban energi dan lingkungan antar-wilayah:

> `Porsi Konsentrasi Sentra (%) = [ Kapasitas Sentra Industri (MW) / Total Kapasitas Se-Sulawesi (MW) ] × 100`

### 1.3 Tren Pertumbuhan Izin Tambang Baru & Uji Signifikansi Statistik
Akumulasi izin konsesi tambang baru dievaluasi laju pertumbuhannya dan dinormalisasi ke dalam unit waktu harian untuk mengukur kecepatan konversi bentang lahan alami menjadi kawasan pertambangan:

> `Laju Alih Ruang Harian (Ha/Hari) = Total Luas Konsesi Tambang Baru (Ha) / Jumlah Hari Observasi (t)`

Pengujian inferensial menggunakan desain matriks kontinjensi 2×2 berbasis **ambang median panel provinsi-tahun (N = 60)**. Uji Chi-Square independensi (α = 5%, df = 1) diterapkan untuk menguji signifikansi hubungan bivariat, sedangkan rasio peluang (Odds Ratio) mengukur magnitudo kelipatan risiko dampak ekologis:

> `χ² = Σ [ (O_ij - E_ij)² / E_ij ]   |   Odds Ratio (OR) = (a × d) / (b × c)`

##### Tabel 1.5b: Konfigurasi Variabel Uji Chi-Square (Sub-bab 1.3)
| Komponen Uji | Definisi Variabel (Sub-bab 1.3) |
| :--- | :--- |
| **Variabel Independen (X)** | Jumlah Izin Baru (IUP) / Luas Konsesi Baru (Ha) |
| **Variabel Dependen (Y)** | Deforestasi Komoditas (Ha) / Total Deforestasi Alam (Ha) |
| **Hipotesis Nol (H0)** | Tingkat penerbitan izin/luas konsesi tidak berhubungan dengan laju deforestasi. |
| **Hipotesis Alternatif (H1)** | Ada hubungan positif antara tingginya penerbitan izin dengan tingginya laju deforestasi. |
| **Decision Rule (Alpha 5%)** | Jika P-Value < 0.05, maka Tolak H0 (terbukti signifikan bahwa ekspansi perizinan mendorong deforestasi). |
| **Threshold Kategori** | Nilai Median Data Panel (N=60): X >= 2.0 izin; Y >= 10,961.8 Ha. |
| **Orientasi Odds Ratio** | OR = ( a × d ) / ( b × c ) dengan a = Izin Tinggi & Deforestasi Tinggi; mengukur risiko deforestasi tinggi pada kelompok penerbitan izin tinggi. |

### 1.4 Analisis Realisasi Investasi PMDN dan Dampak Terhadap Tutupan Hutan
Analisis arus modal investasi PMDN mengevaluasi elastisitas suntikan modal terhadap laju alih fungsi hutan dan emisi komoditas. Formulasi pengujian inferensial Chi-Square dan Odds Ratio pada Sub-bab 1.4 mengadopsi protokol pengujian kontinjensi 2×2 yang sama, dengan variabel independen realisasi investasi modal domestik (X > Rp3.146,4 Miliar) dan evaluasi efek jeda waktu (time-lag) ekspansi fisik di lapangan.

### 1.5 Pelabuhan Ekspor: Ke Mana Nikel Sulawesi Dikirim?
Verifikasi titik pelabuhan dan terminal khusus ekspor nikel dilakukan melalui protokol triangulasi informasi publik (OSINT): Laporan Investigasi Keselamatan Transportasi Laut KNKT (bobot muatan tongkang hingga 52.378 DWT), lampiran regulasi Proyek Strategis Nasional (Perpres No. 109/2020), laporan keberlanjutan emiten terbuka (PT Vale Indonesia Tbk dan PT ANTAM Tbk), serta publikasi riset audit independen mengenai operasional pelabuhan khusus.

### 1.6 Peta Jalur Distribusi Logistik Nikel Sulawesi
Pemodelan spasial rute pelayaran internasional pengangkutan produk olahan nikel dari simpul pelabuhan Sulawesi menuju negara tujuan utama (Tiongkok dan Jepang) dimodelkan menggunakan persamaan parametrik kurva Bézier kuadratik di atas koordinat bola bumi guna memetakan jalur lintas laut aktual:

> `Kurva(t) = (1 - t)² × Titik_Asal + 2(1 - t)t × Titik_Kontrol + t² × Titik_Tujuan`

---

## E. Korespondensi Metodologi terhadap Sub-bab Laporan Bab 1
Setiap sub-bab analitis pada Bab 1 ditopang oleh metode kuantitatif yang presisi dan menghasilkan sintesis bukti empiris terstandarisasi sebagaimana dirangkum pada matriks berikut:

##### Matriks Korespondensi Sub-bab terhadap Metode Analitis
| Sub-bab | Fokus Kajian Empiris | Metode Analitis Utama |
| :---: | :--- | :--- |
| **Sub-bab 1.1** | Struktur Makro PDRB Provinsi & Kabupaten | Reklasifikasi Hukum KBLI, Pangsa Sektoral, Rasio Kesenjangan Spasial |
| **Sub-bab 1.2** | Kawasan Industri & PLTU Captive | Analisis Aglomerasi Spasial, Rasio Kapasitas Off-grid |
| **Sub-bab 1.3** | Tren Perizinan Konsesi Tambang | Deret Waktu Tahunan, Laju Alih Ruang Ha/Hari, Uji Chi-Square (χ²) |
| **Sub-bab 1.4** | Arus Investasi PMDN & Deforestasi | Uji Non-parametrik Chi-Square (χ²), Odds Ratio (OR), Efek Time-lag |
| **Sub-bab 1.5** | Simpul Pelabuhan Ekspor & Terminal Khusus | Triangulasi Validasi Silang (OSINT: KNKT, Regulasi PSN, Laporan Emiten) |
| **Sub-bab 1.6** | Peta Jalur Distribusi Logistik Maritim | Pemodelan Spasial Rute Parametrik Kurva Bézier Kuadratik (Scattergeo) |

---

## F. Bagan Alur Kerangka Kerja Riset (Research Workflow)

```mermaid
flowchart LR
    subgraph F1["Fase I: Akuisisi Data"]
        A1["Kurasi Data Resmi Terbuka<br/><i>BPS, ESDM, GEM, BKPM, GFW, KNKT</i>"]
        A2["Panel Provinsi-Tahun<br/><i>6 Provinsi Se-Sulawesi (N=60)</i>"]
    end
    subgraph F2["Fase II: Reklasifikasi"]
        B1["Reklasifikasi Rantai Pasok Hukum<br/><i>UU 3/2020 & Perpres 112/2022</i>"]
        B2["Dekomposisi Spasial<br/><i>13 Kabupaten Sentra Tambang</i>"]
    end
    subgraph F3["Fase III: Uji Statistik"]
        C1["Tabel Kontinjensi 2×2<br/><i>Ambang Median High vs Low</i>"]
        C2["Uji Chi-Square & Odds Ratio<br/><i>Signifikansi & Kelipatan Risiko</i>"]
    end
    subgraph F4["Fase IV: Pemodelan & Sintesis"]
        D1["Pemodelan Rantai Pasok Ekspor<br/><i>Kurva Bézier 6 Pelabuhan</i>"]
        D2["Bukti Kausalitas D3TLH<br/><i>Dominasi Ekstraktif & Deforestasi</i>"]
    end
    F1 --> F2 --> F3 --> F4
```

> **KERANGKA KELUARAN METODOLOGIS BAB 1:**  
> 1. **Konfigurasi Dekomposisi Sektoral:** Menghasilkan matriks pangsa dan rasio kesenjangan spasial guna mengukur ketergantungan monolitik ekonomi makro-mikro.  
> 2. **Konfigurasi Aglomerasi Geospasial:** Memetakan derajat konsentrasi spasial fasilitas hilirisasi, pembangkit off-grid, dan simpul maritim rantai pasok ekspor.  
> 3. **Konfigurasi Inferensial Tabulasi Silang:** Menetapkan protokol pengujian Chi-Square dan Odds Ratio untuk membuktikan signifikansi kausalitas tekanan industri terhadap degradasi lingkungan.

> *Catatan Metodologis: Seluruh analisis statistik kuantitatif dalam dokumen ini dijalankan pada matriks data panel provinsi-tahun (N = 60 observasi) dan kabupaten sentra industri. Angka komputasi dan sebaran spasial terperinci terintegrasi penuh pada naskah laporan Bab 1 dan antarmuka interaktif dashboard CELIOS.*
"""

    md_compact = out_dir_compact / "Metodologi_Bab1_Ekspansi_Industri_Compact.md"
    md_bab1    = out_dir_bab1 / "Metodologi_Bab1_Ekspansi_Industri_Compact.md"
    for pth in [md_compact, md_bab1]:
        with open(pth, "w", encoding="utf-8") as f:
            f.write(MD_CONTENT)
    print(f"  [OK] Tersimpan MD  : {md_compact}")
    print(f"  [OK] Salinan MD   : {md_bab1}")

    print("[3/3] Selesai menghasilkan dokumen metodologi Bab 1 versi compact (1-Kolom, 2-3 Halaman).")


if __name__ == "__main__":
    generate_bab1_compact()
