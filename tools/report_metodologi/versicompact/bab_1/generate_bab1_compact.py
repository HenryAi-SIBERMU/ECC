#!/usr/bin/env python3
"""
Generator Laporan Metodologi Statistik (Versi Compact) Bab 1:
Ekspansi Industri Ekstraktif dan Infrastruktur Penunjang di Pulau Sulawesi

Format: Standar Versi Compact CELIOS
- Header dan Judul SAMA PERSIS dengan dokumen non-compact / root
- Penomoran sub-bab persis: 1.1, 1.2, 1.3, dst.
- Target Panjang: 2-4 lembar (halaman) di Microsoft Word
- Layout super-padat (dense layout): margin 1.2 cm, font 8.5 pt, tabel 7.5 pt, spasi mikro
- Tanpa icon / emoji
- Narasi, rumus, dan tabel murni dari Metodologi_Bab1_Ekspansi_Industri.md

Output:
1. tools/report_metodologi/versicompact/bab_1/Metodologi_Bab1_Ekspansi_Industri_Compact.docx
2. tools/report_metodologi/versicompact/bab_1/Metodologi_Bab1_Ekspansi_Industri_Compact.md
3. tools/report_metodologi/bab_1/Metodologi_Bab1_Ekspansi_Industri_Compact.docx
4. tools/report_metodologi/bab_1/Metodologi_Bab1_Ekspansi_Industri_Compact.md
"""

import os
import sys
import shutil
from pathlib import Path

try:
    from docx import Document
    from docx.shared import Pt, RGBColor, Cm
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-docx"])
    from docx import Document
    from docx.shared import Pt, RGBColor, Cm
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement

# ── Warna Tema CELIOS D3TLH ─────────────────────────────────
G_DARK   = RGBColor(0x1B, 0x5E, 0x20)  # Hijau Hutan Gelap (#1B5E20)
G_MID    = RGBColor(0x2E, 0x7D, 0x32)  # Hijau Utama CELIOS (#2E7D32)
C_BODY   = RGBColor(0x22, 0x22, 0x22)  # Abu Gelap Teks (#222222)
C_WHITE  = RGBColor(0xFF, 0xFF, 0xFF)  # Putih

# ── Helper XML Word Formatting (Ultra-Compact) ──────────────
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

def cell_margin(cell, left=60, right=60, top=30, bottom=30):
    tcPr = cell._tc.get_or_add_tcPr()
    m    = OxmlElement('w:tcMar')
    for side, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        el = OxmlElement(f'w:{side}')
        el.set(qn('w:w'), str(val))
        el.set(qn('w:type'), 'dxa')
        m.append(el)
    tcPr.append(m)

def cell_shd(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    s    = OxmlElement('w:shd')
    s.set(qn('w:val'), 'clear')
    s.set(qn('w:color'), 'auto')
    s.set(qn('w:fill'), fill)
    tcPr.append(s)

def para_shd(p, fill):
    pPr = p._p.get_or_add_pPr()
    s   = OxmlElement('w:shd')
    s.set(qn('w:val'), 'clear')
    s.set(qn('w:color'), 'auto')
    s.set(qn('w:fill'), fill)
    pPr.append(s)

def para_border_left(p, color='2E7D32', sz='14'):
    pPr  = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    el   = OxmlElement('w:left')
    el.set(qn('w:val'), 'single')
    el.set(qn('w:sz'), sz)
    el.set(qn('w:space'), '4')
    el.set(qn('w:color'), color)
    pBdr.append(el)
    pPr.append(pBdr)

def para_border_bottom(p, color='2E7D32', sz='6'):
    pPr  = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    el   = OxmlElement('w:bottom')
    el.set(qn('w:val'), 'single')
    el.set(qn('w:sz'), sz)
    el.set(qn('w:space'), '1')
    el.set(qn('w:color'), color)
    pBdr.append(el)
    pPr.append(pBdr)

# ── Helper Tipografi Padat ──────────────────────────────────
def run(p, text, bold=False, italic=False, pt=8.5, color=None, mono=False):
    r = p.add_run(text)
    r.bold           = bold
    r.italic         = italic
    r.font.size      = Pt(pt)
    r.font.color.rgb = color if color else C_BODY
    if mono:
        r.font.name = 'Consolas'
        r._element.rPr.rFonts.set(qn('w:ascii'), 'Consolas')
    return r

def add_h1(doc, title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after  = Pt(2)
    para_border_bottom(p, color='1B5E20', sz='8')
    run(p, title.upper(), bold=True, pt=10.5, color=G_DARK)

def add_h2(doc, title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after  = Pt(1.5)
    para_border_bottom(p, color='2E7D32', sz='4')
    run(p, title, bold=True, pt=9.5, color=G_DARK)

def add_h3(doc, title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after  = Pt(1)
    run(p, title, bold=True, pt=8.5, color=G_MID)

def add_p(doc, parts, space_after=2, indent=0):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after  = Pt(space_after)
    p.paragraph_format.line_spacing = 1.05
    if indent > 0:
        p.paragraph_format.left_indent = Pt(indent)
    for text, bold, italic in parts:
        run(p, text, bold=bold, italic=italic, pt=8.5)
    return p

def add_note_inline(doc, title, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after  = Pt(2)
    p.paragraph_format.left_indent  = Pt(6)
    p.paragraph_format.line_spacing = 1.05
    para_border_left(p, color='2E7D32', sz='10')
    para_shd(p, 'F1F8E9')
    run(p, f"{title}: ", bold=True, pt=7.5, color=G_DARK)
    run(p, text, italic=True, pt=7.5, color=RGBColor(0x33, 0x33, 0x33))

def add_formula_compact(doc, title, formula_str, var_str=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after  = Pt(2)
    p.paragraph_format.left_indent  = Pt(6)
    p.paragraph_format.line_spacing = 1.05
    para_shd(p, 'EDF7EE')
    para_border_left(p, color='43A047', sz='12')
    run(p, f"Formulasi ({title}): ", bold=True, pt=7.5, color=G_DARK)
    run(p, formula_str, pt=7.5, color=RGBColor(0x10, 0x40, 0x10), mono=True)
    if var_str:
        run(p, f" | Ket: {var_str}", italic=True, pt=7.0, color=RGBColor(0x55, 0x55, 0x55))

def add_caption_compact(doc, caption_text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2.5)
    p.paragraph_format.space_after  = Pt(1)
    run(p, caption_text, bold=True, italic=True, pt=7.5, color=G_MID)

def add_table_compact(doc, headers, rows, col_widths_cm, alignments=None):
    tbl = doc.add_table(rows=1 + len(rows), cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.style = 'Table Grid'
    tbl.autofit = False

    bd_cfg = {'val': 'single', 'sz': '4', 'color': 'D8D8D8', 'space': '0'}

    # Header
    for j, (h, w) in enumerate(zip(headers, col_widths_cm)):
        c = tbl.rows[0].cells[j]
        c.width = Cm(w)
        cell_shd(c, '2E7D32')
        cell_margin(c, left=50, right=50, top=30, bottom=30)
        set_cell_borders(c, top=bd_cfg, left=bd_cfg, bottom={'val': 'single', 'sz': '8', 'color': '1B5E20', 'space': '0'}, right=bd_cfg)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if (alignments and alignments[j] == 'C') else WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after  = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        run(p, h, bold=True, pt=7.5, color=C_WHITE)

    # Rows
    for i, row in enumerate(rows):
        bg = 'F9FBF9' if i % 2 == 1 else 'FFFFFF'
        for j, (val, w) in enumerate(zip(row, col_widths_cm)):
            c = tbl.rows[1 + i].cells[j]
            c.width = Cm(w)
            cell_shd(c, bg)
            cell_margin(c, left=50, right=50, top=20, bottom=20)
            set_cell_borders(c, top=bd_cfg, left=bd_cfg, bottom=bd_cfg, right=bd_cfg)
            p = c.paragraphs[0]
            align = alignments[j] if alignments else 'L'
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if align == 'C' else (WD_ALIGN_PARAGRAPH.RIGHT if align == 'R' else WD_ALIGN_PARAGRAPH.LEFT)
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after  = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            is_bold = (j == 0) or ('Total' in str(val)) or ('Ekstraktif' in str(val))
            run(p, str(val), bold=is_bold, pt=7.0, color=C_BODY)

# ── Main Generator ──────────────────────────────────────────
def build_compact_report():
    print("[1/4] Menginisialisasi dokumen Word python-docx dengan layout padat...")
    doc = Document()

    # Margin Halaman Padat (1.2 cm di seluruh sisi)
    for section in doc.sections:
        section.top_margin    = Cm(1.2)
        section.bottom_margin = Cm(1.2)
        section.left_margin   = Cm(1.2)
        section.right_margin  = Cm(1.2)

    doc.styles['Normal'].font.name = 'Calibri'
    doc.styles['Normal'].font.size = Pt(8.5)

    # ── HEADER BANNER ───────────────────────────────────────────
    p_hdr = doc.add_paragraph()
    p_hdr.paragraph_format.space_before = Pt(0)
    p_hdr.paragraph_format.space_after  = Pt(1)
    run(p_hdr, "CELIOS — CENTER OF ECONOMIC AND LAW STUDIES  |  LAPORAN RISET METODOLOGI D3TLH", bold=True, pt=7.5, color=G_MID)

    add_h1(doc, "BAB I: METODOLOGI ANALISIS EKSPANSI INDUSTRI EKSTRAKTIF DAN INFRASTRUKTUR PENUNJANG DI PULAU SULAWESI")

    add_p(doc, [
        ("Dokumen laporan metodologi ini menyajikan kerangka ilmiah, landasan regulasi, formulasi matematis, prosedur analisis statistik, serta metodologi pembuktian berbasis data terbuka yang dioperasionalkan pada ", False, False),
        ("Bab 1: Ekspansi Industri Ekstraktif", True, False),
        (" dalam studi Daya Dukung dan Daya Tampung Lingkungan Hidup (D3TLH) Sulawesi periode 2014–2024.", False, False),
    ], space_after=3)

    # ═══════════════════════════════════════════════════════════
    # 1.1 KONTEKS MAKRO: BREAKDOWN PDRB PER KOMODITAS
    # ═══════════════════════════════════════════════════════════
    add_h2(doc, "1.1 Konteks Makro: Breakdown PDRB per Komoditas")

    # 1.1.1
    add_h3(doc, "1.1.1 Konteks Makro: Dominasi Ekstraktif vs Ekonomi Akar Rumput")
    add_p(doc, [
        ("Bagian ini menganalisis struktur Produk Domestik Regional Bruto (PDRB) pada enam provinsi di Pulau Sulawesi sepanjang periode 2016–2024 menggunakan visualisasi grafik area bertumpuk (*Stacked Area Chart*). Analisis ini ditujukan untuk menguji secara empiris apakah percepatan pertumbuhan ekonomi daerah benar-benar bersumber dari sektor produktif masyarakat lokal atau didominasi oleh industri ekstraktif padat modal yang mengalihkan pemanfaatan ruang dan sumber daya alam. Di ", False, False),
        ("Sulawesi Tengah (sebagai pusat hilirisasi)", True, False),
        (", ekspansi industri ekstraktif menguasai ", False, False),
        ("55.8% dari total PDRB provinsi pada tahun 2024", True, False),
        (" (melonjak dari Rp28,45 T pada 2016 menjadi Rp210,51 T pada 2024).", False, False)
    ])
    add_note_inline(doc, "Sumber Data", "BPS Provinsi se-Sulawesi (SIMDASI Subject 52 PDRB ADHB 2016–2024 diolah CELIOS).")

    add_caption_compact(doc, "Tabel 1.1: Reklasifikasi Sektoral PDRB KBLI 2020 Berdasarkan Pendekatan Rantai Pasok Hukum (Legal Supply-Chain)")
    t1_headers = ["Kategori BPS", "Sektor Lapangan Usaha", "Klasifikasi", "Dasar Regulasi & Mandat Hukum", "Intisari Ketentuan Hukum"]
    t1_rows = [
        ["Kategori B", "Pertambangan dan Penggalian", "Ekstraktif", "Perpres No. 26/2010", "Pasal 1 Ayat (2) pengambilan komoditas tambang."],
        ["Kategori C", "Industri Pengolahan (Smelter Logam)", "Ekstraktif", "UU No. 3/2020 & PP 96/2021", "Pasal 102–103 kewajiban hilirisasi smelter terintegrasi tambang."],
        ["Kategori D", "Pengadaan Listrik & Gas (PLTU Captive)", "Ekstraktif", "Perpres No. 112/2022", "Pasal 3 Ayat (4) huruf b pengecualian PLTU off-grid khusus smelter."],
        ["Kategori A", "Pertanian, Kehutanan, Perikanan", "Akar Rumput", "KBLI 2020 BPS", "Pemanfaatan sumber daya hayati terbarukan & tenaga kerja lokal."],
        ["Kategori E–U", "13 Sektor Jasa & Konstruksi", "Jasa & Lainnya", "Klasifikasi Standar BPS", "Sektor sekunder dan tersier penunjang perekonomian daerah."]
    ]
    add_table_compact(doc, t1_headers, t1_rows, [2.2, 4.4, 2.2, 4.2, 5.6], ['C', 'L', 'C', 'L', 'L'])

    add_formula_compact(
        doc,
        "Agregasi Legal Supply-Chain",
        "Sektor_Ekstraktif = PDRB(Kat.B) + PDRB(Kat.C) + PDRB(Kat.D); Pangsa_Ekstraktif(%) = (Sektor_Ekstraktif / Total_PDRB) * 100",
        "Total_PDRB = Sektor_Ekstraktif + Sektor_Akar_Rumput(Kat.A) + Sektor_Jasa(Kat.E s.d. U)"
    )

    # 1.1.2
    add_h3(doc, "1.1.2 Pemusatan Sektor Ekstraktif di Kabupaten se-Sulawesi Tengah")
    add_p(doc, [
        ("Dekomposisi spasial tingkat kabupaten membuktikan terjadinya ", False, False),
        ("Bias Ilusi Agregat (Aggregate Illusion Bias)", True, False),
        (". Kabupaten ", False, False),
        ("Morowali", True, False),
        (" mendominasi dengan nilai sektor ekstraktif sebesar ", False, False),
        ("Rp 157.17 Triliun (45.2% dari total PDRB Rp 347.72 Triliun)", True, False),
        (", melampaui gabungan total PDRB dari delapan kabupaten lainnya. Bersama Morowali Utara (Rp 19.22 T ekstraktif), kedua daerah mengunci output hilirisasi, sementara 8 kabupaten lainnya memiliki porsi ekstraktif <11% dan bergantung pada pertanian rakyat berproduktivitas rendah.", False, False)
    ])
    add_caption_compact(doc, "Tabel 1.2: Matriks Polarisasi Sektoral PDRB Kabupaten di Sulawesi Tengah (Tahun 2024)")
    t2_headers = ["Kabupaten / Tipologi", "Akar Rumput (T Rp)", "Ekstraktif (T Rp)", "Jasa (T Rp)", "Total PDRB (T Rp)", "Porsi Akar (%)", "Porsi Eks (%)", "Basis Utama Ekonomi"]
    t2_rows = [
        ["Morowali (Sentra Smelter)", "2.70", "157.17", "187.85", "347.72", "0.8%", "45.2%", "Hilirisasi Nikel (Smelter & PLTU)"],
        ["Morowali Utara (Sentra Smelter)", "5.17", "19.22", "36.08", "60.47", "8.5%", "31.8%", "Hilirisasi Nikel (Smelter GNI)"],
        ["Banggai (Sentra Migas/Tambang)", "8.85", "20.63", "51.99", "81.47", "10.9%", "25.3%", "Migas, Tambang & Perdagangan"],
        ["Kota Palu (Pusat Jasa/Pemerintahan)", "1.24", "4.56", "60.03", "65.84", "1.9%", "6.9%", "Jasa & Perdagangan"],
        ["9 Kab. Non-Sentra Lainnya (Rata-rata)", "4.86", "1.13", "18.59", "24.58", "21.3%", "4.3%", "Pertanian Rakyat & Perikanan"]
    ]
    add_table_compact(doc, t2_headers, t2_rows, [4.6, 2.0, 2.0, 2.0, 2.2, 1.8, 1.8, 2.2], ['L', 'R', 'R', 'R', 'R', 'C', 'C', 'L'])

    # 1.1.3
    add_h3(doc, "1.1.3 Perbandingan Distribusi 17 Sektor Komoditas per Provinsi (Small Multiples, Tahun Terbaru)")
    add_p(doc, [
        ("Analisis komparatif ", False, False),
        ("Small Multiples", True, False),
        (" terhadap 17 sektor KBLI 2020 (BPS 2024) membuktikan dualisme regional: Sulawesi Tengah (44.1% smelter, 11.8% tambang) dan Sulawesi Tenggara (22.4% pertanian, 20.9% tambang) terpolarisasi pada sektor ekstraktif, sedangkan Sulawesi Selatan (21.8%), Sulawesi Utara (20.5%), Sulawesi Barat (38.2%), dan Gorontalo (36.4%) tetap bertumpu pada Sektor Pertanian dan Jasa Perdagangan.", False, False)
    ])

    # ═══════════════════════════════════════════════════════════
    # 1.2 KONSENTRASI KAWASAN INDUSTRI & PLTU CAPTIVE
    # ═══════════════════════════════════════════════════════════
    add_h2(doc, "1.2 Konsentrasi Kawasan Industri & PLTU Captive")
    add_p(doc, [
        ("Pengoperasian ", False, False),
        ("778 fasilitas smelter", True, False),
        (" di Sulawesi didukung oleh kapasitas energi fosil ", False, False),
        ("9,825 MW PLTU Captive batu bara off-grid", True, False),
        (" (ESDM & GEM). Uji tabulasi silang panel (Crosstab SPSS, N=60) membuktikan keterkaitan signifikan antara keberadaan PLTU captive dengan eskalasi kehilangan tutupan hutan di tapak industri.", False, False)
    ])
    add_formula_compact(
        doc,
        "Chi-Square & Odds Ratio",
        "χ² = Σ [ (O - E)² / E ] ; E_ij = (R_i * C_j) / N ; OR = (a * d) / (b * c)",
        "O: observasi aktual, E: frekuensi harapan, OR: kelipatan rasio risiko kelompok perlakuan"
    )

    # ═══════════════════════════════════════════════════════════
    # 1.3 TREN PERTUMBUHAN IZIN TAMBANG BARU & UJI STATISTIK
    # ═══════════════════════════════════════════════════════════
    add_h2(doc, "1.3 Tren Pertumbuhan Izin Tambang Baru & Uji Signifikansi Statistik")
    add_p(doc, [
        ("Data Minerbaone mencatat penerbitan ", False, False),
        ("574 Izin Usaha Pertambangan (IUP) baru", True, False),
        (" sepanjang 2014–2024 seluas ", False, False),
        ("819,452 Hektar", True, False),
        (". Terjadi lonjakan sebesar ", False, False),
        ("246% pada periode 2022–2024", True, False),
        (". Uji inferensial Chi-Square membuktikan peningkatan frekuensi dan luas konsesi izin berkorelasi positif sangat kuat terhadap eskalasi deforestasi alam dan komoditas (p < 0.0001).", False, False)
    ])

    # ═══════════════════════════════════════════════════════════
    # 1.4 ANALISIS REALISASI INVESTASI PMDN & TUTUPAN HUTAN
    # ═══════════════════════════════════════════════════════════
    add_h2(doc, "1.4 Analisis Realisasi Investasi PMDN dan Dampak Terhadap Tutupan Hutan")
    add_p(doc, [
        ("Realisasi Penanaman Modal Dalam Negeri (PMDN) sebesar ", False, False),
        ("Rp 218 Triliun", True, False),
        (" (BKPM 2016–2024) berbanding lurus dengan ", False, False),
        ("1,001,654 Hektar", True, False),
        (" kehilangan tutupan hutan komoditas (GFW). Pembedahan data GFW Driver Classification (2001–2025) membuktikan sektor komoditas ekstraktif menyumbang ", False, False),
        ("48.4% (1,890,659 Ha)", True, False),
        (" dari 3,904,079 Ha kehilangan hutan primer Sulawesi (emisi: 1,28 Miliar Mg CO2), sedangkan perladangan rakyat hanya 2.9% (115,404 Ha). Uji crosstab mengonfirmasi ", False, False),
        ("Efek Jeda Waktu (Time-Lagging Effect)", True, False),
        (": modal yang masuk hari ini tertahan birokrasi dan baru berdampak pada deforestasi fisik 1 hingga 2 tahun berikutnya.", False, False)
    ])

    # SINTESIS TABEL INFERENSIAL BAB 1 (SUB-BAB 1.2, 1.3, 1.4)
    add_caption_compact(doc, "Tabel 1.3: Ringkasan Hasil Uji Independensi Chi-Square (χ²) dan Odds Ratio (OR) Data Panel Bab 1 (N=60)")
    inf_headers = ["Faktor Tekanan Industri (X)", "Indikator Dampak Lingkungan (Y)", "Chi-Square (χ²)", "P-Value", "Odds Ratio", "df", "Kesimpulan Ilmiah"]
    inf_rows = [
        ["Kapasitas PLTU Captive (MW)", "Deforestasi Komoditas (≥10,961 Ha)", "18.049", "p < 0.0001", "18.00x", "1", "SIGNIFIKAN (Risiko 18x Lipat)"],
        ["Jumlah IUP Tambang Baru (Unit)", "Total Deforestasi Alam (Ha)", "17.239", "p < 0.0001", "13.75x", "1", "SIGNIFIKAN (Risiko 13.7x Lipat)"],
        ["Jumlah IUP Tambang Baru (Unit)", "Deforestasi Komoditas (Ha)", "21.818", "p < 0.0001", "21.36x", "1", "SIGNIFIKAN (Risiko 21.4x Lipat)"],
        ["Luas Konsesi Tambang Baru (Ha)", "Deforestasi Komoditas (Ha)", "19.267", "p < 0.0001", "16.00x", "1", "SIGNIFIKAN (Risiko 16.0x Lipat)"],
        ["Realisasi Investasi PMDN (Juta Rp)", "Deforestasi Komoditas (Ha)", "2.083", "p = 0.1489", "2.80x", "1", "TIDAK SIGNIFIKAN (Efek Time-Lag)"]
    ]
    add_table_compact(doc, inf_headers, inf_rows, [4.2, 4.4, 2.0, 2.0, 1.8, 1.0, 3.2], ['L', 'L', 'C', 'C', 'C', 'C', 'C'])

    # ═══════════════════════════════════════════════════════════
    # 1.5 PELABUHAN EKSPOR & LOGISTIK NIKEL
    # ═══════════════════════════════════════════════════════════
    add_h2(doc, "1.5 Pelabuhan Ekspor & Peta Jalur Distribusi Logistik Nikel Sulawesi")
    add_p(doc, [
        ("Eksploitasi nikel terhubung langsung ke pasar global melalui 6 simpul pelabuhan samudera dan terminal khusus utama di pesisir Sulawesi yang diverifikasi melalui triangulasi Laporan KNKT, Regulasi PSN (Perpres No. 109/2020), dan laporan emiten.", False, False)
    ])
    add_caption_compact(doc, "Tabel 1.4: Inventarisasi Enam Simpul Pelabuhan dan Terminal Khusus Ekspor Nikel di Pulau Sulawesi")
    port_headers = ["Kawasan Industri", "Wilayah Administrasi", "Fasilitas Pelabuhan / Terminal", "Status Regulasi", "Kapasitas Kapal", "Tujuan Utama Ekspor"]
    port_rows = [
        ["IMIP Morowali", "Morowali, Sulteng", "Pelabuhan Samudera & Dermaga Curah", "PSN (Perpres 109/2020)", "Hingga 52.378 DWT", "Pasar Global (Tiongkok)"],
        ["GNI Morowali Utara", "Morowali Utara, Sulteng", "Terminal Khusus Pesisir Tomori", "Izin Industri Mandiri", "Hingga 30.000 DWT", "Pasar Global (Tiongkok)"],
        ["VDNI Konawe", "Konawe, Sultra", "Dermaga Khusus Curah & Kargo", "PSN (Perpres 109/2020)", "Hingga 50.000 DWT", "Pasar Global (Tiongkok)"],
        ["OSS Konawe", "Konawe, Sultra", "Dermaga Terintegrasi Konawe", "PSN (Perpres 109/2020)", "Hingga 50.000 DWT", "Pasar Global (Tiongkok)"],
        ["Pomalaa (ANTAM)", "Kolaka, Sultra", "Dermaga Pomalaa & Konveyor", "Kawasan BUMN Industri", "Hingga 12.000 DWT", "Jepang & Korsel"],
        ["Sorowako (Vale)", "Luwu Timur, Sulsel", "Pelabuhan Balantang Malili", "Kontrak Karya Tambang", "Hingga 15.000 DWT", "Jepang & Skandinavia"]
    ]
    add_table_compact(doc, port_headers, port_rows, [2.8, 3.2, 4.4, 2.8, 2.2, 3.2], ['L', 'L', 'L', 'C', 'C', 'L'])

    # ═══════════════════════════════════════════════════════════
    # 1.6 PETA JALUR DISTRIBUSI LOGISTIK NIKEL SULAWESI
    # ═══════════════════════════════════════════════════════════
    add_h2(doc, "1.6 Peta Jalur Distribusi Logistik Nikel Sulawesi")
    add_p(doc, [
        ("Pemodelan spasial alur pelayaran kargo nikel dari 6 pelabuhan muat Sulawesi menuju negara tujuan utama (Tiongkok, Jepang, Korea Selatan) dikonstruksi menggunakan kurva parametrik Bézier untuk merepresentasikan jarak tempuh aktual di permukaan bumi.", False, False)
    ])
    add_formula_compact(
        doc,
        "Kurva Parametrik Bézier",
        "Kurva(t) = (1 - t)² * P_Asal + 2*(1 - t)*t * P_Kontrol + t² * P_Tujuan , t in [0, 1]",
        "P_Asal: koordinat pelabuhan Sulawesi, P_Kontrol: jangkar perairan internasional, P_Tujuan: pelabuhan bongkar"
    )

    # ═══════════════════════════════════════════════════════════
    # 1.7 MATRIKS INDIKATOR DAN SUMBER DATA RESMI BAB 1
    # ═══════════════════════════════════════════════════════════
    add_h2(doc, "1.7 Matriks Indikator dan Sumber Data Resmi Bab 1")
    add_caption_compact(doc, "Tabel 1.5: Matriks Indikator dan Sumber Data Primer Resmi Bab 1")
    m_headers = ["No", "Nama Indikator", "Kategori Analisis", "Satuan", "Cakupan", "Institusi Sumber Data Primer", "Dataset File"]
    m_rows = [
        ["1", "IUP Tambang Baru", "Tekanan Ekstraktif", "Unit", "2014-2024", "ESDM MODI (Minerbaone)", "sulawesi_izin_baru_per_tahun.csv"],
        ["2", "Luas Konsesi Baru", "Tekanan Ekstraktif", "Hektar", "2014-2024", "ESDM MODI (Minerbaone)", "sulawesi_kawasan_nikel_luas.csv"],
        ["3", "PLTU Captive", "Energi Fosil Khusus", "MW", "2014-2024", "Global Energy Monitor (GEM)", "sulawesi_pltu_captive.csv"],
        ["4", "Smelter Nikel", "Fasilitas Industri", "Unit", "2014-2024", "ESDM & Center for Global Sustainability", "sulawesi_esdm_nikel.csv"],
        ["5", "Investasi PMDN", "Arus Modal", "Triliun Rp", "2016-2024", "Kementerian Investasi / BKPM & BPS", "sulawesi_investasi_pmdn_2016_2024.csv"],
        ["6", "PDRB Provinsi Sektoral", "Ekonomi Makro", "Triliun Rp", "2016-2024", "BPS Provinsi (Subject 52)", "sulawesi_pdrb_sektoral_2016_2024.csv"],
        ["7", "PDRB Kabupaten Sentra", "Ekonomi Daerah", "Triliun Rp", "2016-2024", "BPS Kabupaten se-Sulteng", "sulawesi_pdrb_sektoral_kabupaten_2016_2024.csv"],
        ["8", "Deforestasi Komoditas", "Dampak Ekologis", "Hektar", "2014-2023", "Global Forest Watch (GFW API v2)", "sulawesi_gfw_master_1_dekade_2014_2023_v3.csv"],
        ["9", "Pelabuhan & Terminal Khusus", "Logistik Maritim", "DWT / Titik", "2014-2024", "KNKT, Perpres PSN, Laporan Korporasi", "sulawesi_logistik_simpul_nikel.csv"]
    ]
    add_table_compact(doc, m_headers, m_rows, [0.8, 3.4, 2.6, 1.4, 1.8, 4.4, 4.2], ['C', 'L', 'L', 'C', 'C', 'L', 'L'])

    # ═══════════════════════════════════════════════════════════
    # 1.8 BAGAN ALUR KERANGKA KERJA RISET BAB 1
    # ═══════════════════════════════════════════════════════════
    add_h2(doc, "1.8 Bagan Alur Kerangka Kerja Riset Bab 1")
    add_caption_compact(doc, "Tabel 1.6: Matriks Tahapan dan Alur Kerangka Kerja Riset Bab 1")
    f_headers = ["Fase Riset", "Fokus Metodologis", "Bahan & Sumber Data Primer", "Keluaran Analisis"]
    f_rows = [
        ["Fase I: Pengumpulan Data", "Kurasi data resmi lintas K/L", "Publikasi BPS, Minerbaone, BKPM, GEM, GFW", "Basis Data Tabular Panel Provinsi (2014–2024)"],
        ["Fase II: Reklasifikasi Hukum", "Penyusunan rantai pasok hukum", "UU 3/2020, PP 96/2021, Perpres 112/2022", "3 Klaster Makro (Ekstraktif, Akar Rumput, Jasa)"],
        ["Fase III: Pengujian Statistik", "Uji signifikansi & rasio risiko", "Tabel Kontinjensi, Chi-Square, Odds Ratio", "Kausalitas Signifikan Tekanan vs Deforestasi (N=60)"],
        ["Fase IV: Pemetaan Rantai Pasok", "Triangulasi logistik & rute kapal", "KNKT, Perpres PSN, Kurva Parametrik Bézier", "Peta Alur Rantai Pasok Ekspor & Konsentrasi Maritim"]
    ]
    add_table_compact(doc, f_headers, f_rows, [3.4, 4.4, 5.4, 5.4], ['L', 'L', 'L', 'L'])

    # Simpan File DOCX
    out_dir_compact = Path(__file__).resolve().parent
    out_dir_bab1    = out_dir_compact.parent.parent / "bab_1"
    out_dir_compact.mkdir(parents=True, exist_ok=True)
    out_dir_bab1.mkdir(parents=True, exist_ok=True)

    docx_path_compact = out_dir_compact / "Metodologi_Bab1_Ekspansi_Industri_Compact.docx"
    docx_path_bab1    = out_dir_bab1 / "Metodologi_Bab1_Ekspansi_Industri_Compact.docx"

    doc.save(str(docx_path_compact))
    shutil.copyfile(docx_path_compact, docx_path_bab1)
    print(f"[OK] Berhasil menyimpan DOCX di: {docx_path_compact}")
    print(f"[OK] Salinan tersimpan di: {docx_path_bab1}")

# ── Generator Naskah Markdown Compact ───────────────────────
def generate_compact_markdown():
    print("[2/4] Menyusun naskah Markdown Metodologi Versi Compact...")
    md_content = """# BAB I: METODOLOGI ANALISIS EKSPANSI INDUSTRI EKSTRAKTIF DAN INFRASTRUKTUR PENUNJANG DI PULAU SULAWESI

Dokumen laporan metodologi ini menyajikan kerangka ilmiah, landasan regulasi, formulasi matematis, prosedur analisis statistik, serta metodologi pembuktian berbasis data terbuka yang dioperasionalkan pada **Bab 1: Ekspansi Industri Ekstraktif** dalam studi Daya Dukung dan Daya Tampung Lingkungan Hidup (D3TLH) Sulawesi periode 2014–2024.

---

## 1.1 Konteks Makro: Breakdown PDRB per Komoditas

### 1.1.1 Konteks Makro: Dominasi Ekstraktif vs Ekonomi Akar Rumput
Bagian ini menganalisis struktur Produk Domestik Regional Bruto (PDRB) pada enam provinsi di Pulau Sulawesi sepanjang periode 2016–2024 menggunakan visualisasi grafik area bertumpuk (*Stacked Area Chart*). Analisis ini ditujukan untuk menguji secara empiris apakah percepatan pertumbuhan ekonomi daerah benar-benar bersumber dari sektor produktif masyarakat lokal atau didominasi oleh industri ekstraktif padat modal yang mengalihkan pemanfaatan ruang dan sumber daya alam. Di **Sulawesi Tengah (sebagai pusat hilirisasi)**, ekspansi industri ekstraktif menguasai **55.8% dari total PDRB provinsi pada tahun 2024** (melonjak dari Rp28,45 T pada 2016 menjadi Rp210,51 T pada 2024).

> **Sumber Data:** BPS Provinsi se-Sulawesi (SIMDASI Subject 52 PDRB ADHB 2016–2024 diolah CELIOS).

##### Tabel 1.1: Reklasifikasi Sektoral PDRB KBLI 2020 Berdasarkan Pendekatan Rantai Pasok Hukum (Legal Supply-Chain)
| Kategori BPS | Sektor Lapangan Usaha | Klasifikasi Analisis | Dasar Regulasi & Mandat Hukum | Intisari Ketentuan Hukum |
| :--- | :--- | :---: | :--- | :--- |
| **Kategori B** | Pertambangan dan Penggalian | Ekstraktif | Perpres No. 26/2010 | Ketentuan Pasal 1 Ayat (2) mengenai pengambilan komoditas tambang. |
| **Kategori C** | Industri Pengolahan (Smelter Logam) | Ekstraktif | UU No. 3/2020 & PP 96/2021 | Pasal 102–103 kewajiban hilirisasi smelter terintegrasi pertambangan. |
| **Kategori D** | Pengadaan Listrik & Gas (PLTU Captive) | Ekstraktif | Perpres No. 112/2022 | Pasal 3 Ayat (4) huruf b pengecualian PLTU off-grid khusus smelter. |
| **Kategori A** | Pertanian, Kehutanan, Perikanan | Akar Rumput | KBLI 2020 BPS | Sektor pemanfaatan sumber daya hayati terbarukan & tenaga kerja lokal. |
| **Kategori E–U** | 13 Sektor Jasa & Konstruksi | Jasa & Lainnya | Klasifikasi Standar BPS | Sektor sekunder dan tersier penunjang perekonomian daerah. |

**Formulasi Agregasi Legal Supply-Chain:**
```text
Sektor_Ekstraktif = PDRB(Kat.B) + PDRB(Kat.C) + PDRB(Kat.D)
Total_PDRB = Sektor_Ekstraktif + Sektor_Akar_Rumput(Kat.A) + Sektor_Jasa(Kat.E s.d. U)
Pangsa_Ekstraktif (%) = ( Sektor_Ekstraktif / Total_PDRB ) * 100
```

---

### 1.1.2 Pemusatan Sektor Ekstraktif di Kabupaten se-Sulawesi Tengah
Dekomposisi spasial tingkat kabupaten membuktikan terjadinya *Aggregate Illusion Bias*. Kabupaten **Morowali** mendominasi dengan nilai sektor ekstraktif sebesar **Rp 157.17 Triliun (45.2% dari total PDRB Rp 347.72 Triliun)**, melampaui gabungan total PDRB dari delapan kabupaten lainnya. Bersama Morowali Utara (Rp 19.22 T ekstraktif), kedua daerah mengunci output hilirisasi, sementara 8 kabupaten lainnya memiliki porsi ekstraktif <11% dan bergantung pada pertanian rakyat berproduktivitas rendah.

##### Tabel 1.2: Matriks Polarisasi Sektoral PDRB Kabupaten di Sulawesi Tengah (Tahun 2024)
| Kabupaten / Tipologi | Akar Rumput (T Rp) | Ekstraktif (T Rp) | Jasa (T Rp) | Total PDRB (T Rp) | Porsi Akar (%) | Porsi Eks (%) | Basis Utama Ekonomi |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Morowali (Sentra Smelter)** | 2.70 | 157.17 | 187.85 | **347.72** | 0.8% | 45.2% | Hilirisasi Nikel (Smelter & PLTU) |
| **Morowali Utara (Sentra Smelter)** | 5.17 | 19.22 | 36.08 | **60.47** | 8.5% | 31.8% | Hilirisasi Nikel (Smelter GNI) |
| **Banggai (Sentra Migas/Tambang)** | 8.85 | 20.63 | 51.99 | **81.47** | 10.9% | 25.3% | Migas, Tambang & Perdagangan |
| **Kota Palu (Pusat Jasa/Pemerintahan)** | 1.24 | 4.56 | 60.03 | **65.84** | 1.9% | 6.9% | Jasa & Perdagangan |
| **9 Kab. Non-Sentra Lainnya (Rata-rata)** | 4.86 | 1.13 | 18.59 | **24.58** | 21.3% | 4.3% | Pertanian Rakyat & Perikanan |

---

### 1.1.3 Perbandingan Distribusi 17 Sektor Komoditas per Provinsi (Small Multiples, Tahun Terbaru)
Analisis komparatif *Small Multiples* terhadap 17 sektor KBLI 2020 (BPS 2024) membuktikan dualisme regional: Sulawesi Tengah (44.1% smelter, 11.8% tambang) dan Sulawesi Tenggara (22.4% pertanian, 20.9% tambang) terpolarisasi pada sektor ekstraktif, sedangkan Sulawesi Selatan (21.8%), Sulawesi Utara (20.5%), Sulawesi Barat (38.2%), dan Gorontalo (36.4%) tetap bertumpu pada Sektor Pertanian dan Jasa Perdagangan.

---

## 1.2 Konsentrasi Kawasan Industri & PLTU Captive

Pengoperasian **778 fasilitas smelter** di Sulawesi didukung oleh kapasitas energi fosil **9,825 MW PLTU Captive batu bara off-grid** (ESDM & GEM). Uji tabulasi silang panel (Crosstab SPSS, N=60) membuktikan keterkaitan signifikan antara keberadaan PLTU captive dengan eskalasi kehilangan tutupan hutan di tapak industri.

**Formulasi Chi-Square & Odds Ratio:**
```text
χ² = Σ [ (O - E)² / E ]  |  E_ij = (R_i * C_j) / N  |  OR = (a * d) / (b * c)
```

---

## 1.3 Tren Pertumbuhan Izin Tambang Baru & Uji Signifikansi Statistik

Data Minerbaone mencatat penerbitan **574 Izin Usaha Pertambangan (IUP) baru** sepanjang 2014–2024 seluas **819,452 Hektar**, dengan lonjakan sebesar **246% pada periode 2022–2024**. Uji inferensial Chi-Square membuktikan peningkatan frekuensi dan luas konsesi izin berkorelasi positif sangat kuat terhadap eskalasi deforestasi alam dan komoditas (p < 0.0001).

---

## 1.4 Analisis Realisasi Investasi PMDN dan Dampak Terhadap Tutupan Hutan

Realisasi Penanaman Modal Dalam Negeri (PMDN) sebesar **Rp 218 Triliun** (BKPM 2016–2024) berbanding lurus dengan **1,001,654 Hektar** kehilangan tutupan hutan komoditas (GFW). Pembedahan data GFW Driver Classification (2001–2025) membuktikan sektor komoditas ekstraktif menyumbang **48.4% (1,890,659 Ha)** dari 3,904,079 Ha kehilangan hutan primer Sulawesi (emisi: 1,28 Miliar Mg CO2), sedangkan perladangan rakyat hanya 2.9% (115,404 Ha). Uji crosstab mengonfirmasi **Efek Jeda Waktu (Time-Lagging Effect)**: modal yang masuk hari ini tertahan birokrasi dan baru berdampak pada deforestasi fisik 1 hingga 2 tahun berikutnya.

##### Tabel 1.3: Ringkasan Hasil Uji Independensi Chi-Square (χ²) dan Odds Ratio (OR) Data Panel Bab 1 (N=60)
| Faktor Tekanan Industri (X) | Indikator Dampak Lingkungan (Y) | Chi-Square (χ²) | P-Value | Odds Ratio | df | Kesimpulan Ilmiah |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Kapasitas PLTU Captive (MW)** | Deforestasi Komoditas (≥10,961 Ha) | 18.049 | p < 0.0001 | 18.00x | 1 | SIGNIFIKAN (Risiko 18x Lipat) |
| **Jumlah IUP Tambang Baru (Unit)** | Total Deforestasi Alam (Ha) | 17.239 | p < 0.0001 | 13.75x | 1 | SIGNIFIKAN (Risiko 13.7x Lipat) |
| **Jumlah IUP Tambang Baru (Unit)** | Deforestasi Komoditas (Ha) | 21.818 | p < 0.0001 | 21.36x | 1 | SIGNIFIKAN (Risiko 21.4x Lipat) |
| **Luas Konsesi Tambang Baru (Ha)** | Deforestasi Komoditas (Ha) | 19.267 | p < 0.0001 | 16.00x | 1 | SIGNIFIKAN (Risiko 16.0x Lipat) |
| **Realisasi Investasi PMDN (Juta Rp)** | Deforestasi Komoditas (Ha) | 2.083 | p = 0.1489 | 2.80x | 1 | TIDAK SIGNIFIKAN (Efek Time-Lag) |

---

## 1.5 Pelabuhan Ekspor & Peta Jalur Distribusi Logistik Nikel Sulawesi

Eksploitasi nikel terhubung langsung ke pasar global melalui 6 simpul pelabuhan samudera dan terminal khusus utama di pesisir Sulawesi yang diverifikasi melalui triangulasi Laporan KNKT, Regulasi PSN (Perpres No. 109/2020), dan laporan emiten.

##### Tabel 1.4: Inventarisasi Enam Simpul Pelabuhan dan Terminal Khusus Ekspor Nikel di Pulau Sulawesi
| Kawasan Industri | Wilayah Administrasi | Fasilitas Pelabuhan / Terminal | Status Regulasi | Kapasitas Kapal | Tujuan Utama Ekspor |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **IMIP Morowali** | Morowali, Sulteng | Pelabuhan Samudera & Dermaga Curah | PSN (Perpres 109/2020) | Hingga 52.378 DWT | Pasar Global (Tiongkok) |
| **GNI Morowali Utara** | Morowali Utara, Sulteng | Terminal Khusus Pesisir Tomori | Izin Industri Mandiri | Hingga 30.000 DWT | Pasar Global (Tiongkok) |
| **VDNI Konawe** | Konawe, Sultra | Dermaga Khusus Curah & Kargo | PSN (Perpres 109/2020) | Hingga 50.000 DWT | Pasar Global (Tiongkok) |
| **OSS Konawe** | Konawe, Sultra | Dermaga Terintegrasi Konawe | PSN (Perpres 109/2020) | Hingga 50.000 DWT | Pasar Global (Tiongkok) |
| **Pomalaa (ANTAM)** | Kolaka, Sultra | Dermaga Pomalaa & Konveyor | Kawasan BUMN Industri | Hingga 12.000 DWT | Jepang & Korsel |
| **Sorowako (Vale)** | Luwu Timur, Sulsel | Pelabuhan Balantang Malili | Kontrak Karya Tambang | Hingga 15.000 DWT | Jepang & Skandinavia |

---

## 1.6 Peta Jalur Distribusi Logistik Nikel Sulawesi

Pemodelan spasial alur pelayaran kargo nikel dari 6 pelabuhan muat Sulawesi menuju negara tujuan utama (Tiongkok, Jepang, Korea Selatan) dikonstruksi menggunakan kurva parametrik Bézier untuk merepresentasikan jarak tempuh aktual di permukaan bumi:
```text
Kurva(t) = (1 - t)² * P_Asal + 2*(1 - t)*t * P_Kontrol + t² * P_Tujuan , t in [0, 1]
```

---

## 1.7 Matriks Indikator dan Sumber Data Resmi Bab 1

##### Tabel 1.5: Matriks Indikator dan Sumber Data Primer Resmi Bab 1
| No | Nama Indikator | Kategori Analisis | Satuan | Cakupan | Institusi Sumber Data Primer | Dataset File |
| :---: | :--- | :--- | :---: | :---: | :--- | :--- |
| 1 | IUP Tambang Baru | Tekanan Ekstraktif | Unit | 2014-2024 | ESDM MODI (Minerbaone) | `sulawesi_izin_baru_per_tahun.csv` |
| 2 | Luas Konsesi Baru | Tekanan Ekstraktif | Hektar | 2014-2024 | ESDM MODI (Minerbaone) | `sulawesi_kawasan_nikel_luas.csv` |
| 3 | PLTU Captive | Energi Fosil Khusus | MW | 2014-2024 | Global Energy Monitor (GEM) | `sulawesi_pltu_captive.csv` |
| 4 | Smelter Nikel | Fasilitas Industri | Unit | 2014-2024 | ESDM & CGS | `sulawesi_esdm_nikel.csv` |
| 5 | Investasi PMDN | Arus Modal | Triliun Rp | 2016-2024 | BKPM & BPS | `sulawesi_investasi_pmdn_2016_2024.csv` |
| 6 | PDRB Provinsi Sektoral | Ekonomi Makro | Triliun Rp | 2016-2024 | BPS Provinsi (Subject 52) | `sulawesi_pdrb_sektoral_2016_2024.csv` |
| 7 | PDRB Kabupaten Sentra | Ekonomi Daerah | Triliun Rp | 2016-2024 | BPS Kabupaten se-Sulteng | `sulawesi_pdrb_sektoral_kabupaten_2016_2024.csv` |
| 8 | Deforestasi Komoditas | Dampak Ekologis | Hektar | 2014-2023 | Global Forest Watch (GFW API) | `sulawesi_gfw_master_1_dekade_2014_2023_v3.csv` |
| 9 | Pelabuhan Ekspor | Logistik Maritim | DWT | 2014-2024 | KNKT, Perpres PSN, Korporasi | `sulawesi_logistik_simpul_nikel.csv` |

---

## 1.8 Bagan Alur Kerangka Kerja Riset Bab 1

##### Tabel 1.6: Matriks Tahapan dan Alur Kerangka Kerja Riset Bab 1
| Fase Riset | Fokus Metodologis | Bahan & Sumber Data Primer | Keluaran Analisis |
| :--- | :--- | :--- | :--- |
| **Fase I: Pengumpulan Data** | Kurasi data resmi lintas K/L | Publikasi BPS, Minerbaone, BKPM, GEM, GFW | Basis Data Tabular Panel Provinsi (2014–2024) |
| **Fase II: Reklasifikasi Hukum** | Penyusunan rantai pasok hukum | UU 3/2020, PP 96/2021, Perpres 112/2022 | 3 Klaster Makro (Ekstraktif, Akar Rumput, Jasa) |
| **Fase III: Pengujian Statistik** | Uji signifikansi & rasio risiko | Tabel Kontinjensi, Chi-Square, Odds Ratio | Kausalitas Signifikan Tekanan vs Deforestasi (N=60) |
| **Fase IV: Pemetaan Rantai Pasok** | Triangulasi logistik & rute kapal | KNKT, Perpres PSN, Kurva Parametrik Bézier | Peta Alur Rantai Pasok Ekspor & Konsentrasi Maritim |
"""

    out_dir_compact = Path(__file__).resolve().parent
    out_dir_bab1    = out_dir_compact.parent.parent / "bab_1"
    out_dir_compact.mkdir(parents=True, exist_ok=True)
    out_dir_bab1.mkdir(parents=True, exist_ok=True)
    
    md_path_compact = out_dir_compact / "Metodologi_Bab1_Ekspansi_Industri_Compact.md"
    md_path_bab1    = out_dir_bab1 / "Metodologi_Bab1_Ekspansi_Industri_Compact.md"

    with open(md_path_compact, "w", encoding="utf-8") as f:
        f.write(md_content)
    with open(md_path_bab1, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"[OK] Berhasil menyimpan Markdown di: {md_path_compact}")
    print(f"[OK] Salinan tersimpan di: {md_path_bab1}")

if __name__ == "__main__":
    print("=" * 70)
    print("GENERATOR METODOLOGI STATISTIK VERSI COMPACT - BAB 1 (DENSE LAYOUT)")
    print("=" * 70)
    build_compact_report()
    generate_compact_markdown()
    print("=" * 70)
    print("SELESAI! Seluruh dokumen Versi Compact Bab 1 berhasil digenerate.")
    print("=" * 70)
