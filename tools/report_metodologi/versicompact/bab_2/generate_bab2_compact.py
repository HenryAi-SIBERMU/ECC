#!/usr/bin/env python3
"""
Generator Metodologi Versi Compact Bab 2 — GAYA AKADEMIS TERPADU (CELIOS)
Mengadopsi arsitektur metodologi ringkas terstandarisasi konsisten dengan Bab 1:
- FORMAT: 1 KOLOM PENUH (Single Column Layout)
- PANJANG: 2–3 Halaman Maksimal (Elegan, proporsional, tanpa pemadatan berlebihan)
- PENOMORAN SEKSI UTAMA: Huruf kapital A, B, C, D, E, F
- SUB-BAB SEKSI D: 2.1, 2.2, 2.3, 2.4, 2.5 (Judul persis dokumen induk)
- OPERASIONALISASI INDIKATOR: 10 Indikator Empiris Lengkap (Matriks Indikator & Sumber Data Resmi)
- FORMULASI & TABEL CROSSTAB: Format standar Tabel 1.5b (Komponen Uji per baris, murni konfigurasi teknis tanpa hasil empiris)
- KORESPONDENSI METODOLOGI: 3 kolom bersih (Sub-bab, Fokus Kajian Empiris, Metode Analitis Utama)
- FLOWCHART: Mermaid JS horizontal (flowchart LR) dirender tajam ke DOCX (16.5 cm) dan blok kode di MD
- SINKRONISASI: Dual-save ke direktori versicompact/bab_2 dan bab_2.
"""

import os
import sys
import shutil
import base64
import requests
from pathlib import Path

try:
    from docx import Document
    from docx.shared import Pt, RGBColor, Cm
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-docx"])
    from docx import Document
    from docx.shared import Pt, RGBColor, Cm
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement

# ── Palet Warna Resmi CELIOS ─────────────────────────────────
G_DARK  = RGBColor(0x1B, 0x5E, 0x20)  # Forest Dark Green (#1B5E20)
G_MID   = RGBColor(0x2E, 0x7D, 0x32)  # Celios Accent Green (#2E7D32)
G_LIGHT = RGBColor(0x38, 0x8E, 0x3C)  # Medium Green (#388E3C)
C_BODY  = RGBColor(0x22, 0x22, 0x22)  # Charcoal Body Text (#222222)
C_GREY  = RGBColor(0x55, 0x55, 0x55)  # Muted Grey Text (#555555)
C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)  # Pure White

# ── Helper Fungsi XML Word ───────────────────────────────────
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

def cell_margin(cell, left=80, right=80, top=40, bottom=40):
    tcPr = cell._tc.get_or_add_tcPr()
    m    = OxmlElement('w:tcMar')
    for side, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        el = OxmlElement(f'w:{side}')
        el.set(qn('w:w'), str(val))
        el.set(qn('w:type'), 'dxa')
        m.append(el)
    tcPr.append(m)

def cell_shd(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    s    = OxmlElement('w:shd')
    s.set(qn('w:val'), 'clear')
    s.set(qn('w:color'), 'auto')
    s.set(qn('w:fill'), fill_hex)
    tcPr.append(s)

def para_shd(p, fill_hex):
    pPr = p._p.get_or_add_pPr()
    s   = OxmlElement('w:shd')
    s.set(qn('w:val'), 'clear')
    s.set(qn('w:color'), 'auto')
    s.set(qn('w:fill'), fill_hex)
    pPr.append(s)

def para_border_bottom(p, color='1B5E20', sz='12'):
    pPr  = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    el   = OxmlElement('w:bottom')
    el.set(qn('w:val'), 'single')
    el.set(qn('w:sz'), sz)
    el.set(qn('w:space'), '3')
    el.set(qn('w:color'), color)
    pBdr.append(el)
    pPr.append(pBdr)

def para_border_left(p, color='2E7D32', sz='12'):
    pPr  = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    el   = OxmlElement('w:left')
    el.set(qn('w:val'), 'single')
    el.set(qn('w:sz'), sz)
    el.set(qn('w:space'), '4')
    el.set(qn('w:color'), color)
    pBdr.append(el)
    pPr.append(pBdr)

def all_border_para(p, color='1B5E20', sz='8'):
    pPr  = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    for edge in ['top', 'left', 'bottom', 'right']:
        el = OxmlElement(f'w:{edge}')
        el.set(qn('w:val'), 'single')
        el.set(qn('w:sz'), sz)
        el.set(qn('w:space'), '4')
        el.set(qn('w:color'), color)
        pBdr.append(el)
    pPr.append(pBdr)

# ── Helper Typography & Content ──────────────────────────────
def add_run(p, text, bold=False, italic=False, pt=8.5, color=C_BODY, mono=False):
    r = p.add_run(text)
    r.bold           = bold
    r.italic         = italic
    r.font.size      = Pt(pt)
    r.font.color.rgb = color
    if mono:
        r.font.name = 'Consolas'
        r._element.rPr.rFonts.set(qn('w:ascii'), 'Consolas')
    else:
        r.font.name = 'Calibri'
        r._element.rPr.rFonts.set(qn('w:ascii'), 'Calibri')
    return r

def add_h2(doc, prefix, title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after  = Pt(3)
    p.paragraph_format.keep_with_next = True
    para_border_bottom(p, color='1B5E20', sz='8')
    add_run(p, f"{prefix}.  ", bold=True, pt=11, color=G_DARK)
    add_run(p, title.upper(), bold=True, pt=11, color=G_DARK)
    return p

def add_h3(doc, title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(5)
    p.paragraph_format.space_after  = Pt(2)
    p.paragraph_format.keep_with_next = True
    add_run(p, title, bold=True, pt=9.5, color=G_MID)
    return p

def add_body(doc, parts, space_after=3):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after  = Pt(space_after)
    p.paragraph_format.line_spacing = 1.05
    for text, bold, italic in parts:
        add_run(p, text, bold=bold, italic=italic, pt=8.5, color=C_BODY)
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
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after  = Pt(2)
        if alignments and j < len(alignments):
            align = alignments[j]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if align == 'C' else (WD_ALIGN_PARAGRAPH.RIGHT if align == 'R' else WD_ALIGN_PARAGRAPH.LEFT)
        else:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_run(p, h, bold=True, pt=8, color=C_WHITE)

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

def download_mermaid_png(mermaid_str, filepath):
    if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
        return True
    try:
        encoded = base64.urlsafe_b64encode(mermaid_str.encode('utf-8')).decode('utf-8')
        url = f'https://mermaid.ink/img/{encoded}'
        print(f"[INFO] Mendownload Mermaid JS flowchart ke {filepath}...")
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(resp.content)
            return True
        else:
            print(f"[WARN] Gagal download mermaid (Status Code: {resp.status_code})")
            return False
    except Exception as e:
        print(f"[WARN] Exception saat download mermaid: {e}")
        return False


def generate_bab2_compact():
    print("[1/3] Membangun dokumen compact Bab 2 (Format 1-Kolom, 2-3 Halaman)...")
    
    out_dir_compact = Path(__file__).resolve().parent
    out_dir_bab2    = out_dir_compact.parent.parent / "bab_2"

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
    p_t.paragraph_format.space_after  = Pt(1)
    add_run(p_t, "RINGKASAN EKSEKUTIF METODOLOGIS", bold=True, pt=8.5, color=G_MID)

    p_h = doc.add_paragraph()
    p_h.paragraph_format.space_before = Pt(0)
    p_h.paragraph_format.space_after  = Pt(2)
    para_border_bottom(p_h, color='1B5E20', sz='12')
    add_run(p_h, "BAB 2: METODOLOGI ANALISIS KUALITAS LINGKUNGAN DI KAWASAN SMELTER", bold=True, pt=15, color=G_DARK)

    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_before = Pt(1)
    p_meta.paragraph_format.space_after  = Pt(5)
    add_run(p_meta, "Studi Daya Dukung & Daya Tampung Lingkungan Hidup (D3TLH) Sulawesi · ", italic=True, pt=8, color=C_GREY)
    add_run(p_meta, "Center of Economic and Law Studies (CELIOS)", bold=True, italic=True, pt=8, color=G_DARK)

    # ── A. DESAIN PENELITIAN & TUJUAN ───────────────────────────
    add_h2(doc, "A", "Desain Penelitian & Tujuan")
    add_body(doc, [
        ("Penelitian ini menggunakan ", False, False),
        ("desain audit spasial-statistik kuantitatif dan inferensial bivariat terintegrasi", True, False),
        (" untuk mengukur dampak degradasi lingkungan hidup akibat pemusatan fasilitas smelter nikel dan kawasan industri bertenaga PLTU captive batubara di enam provinsi Pulau Sulawesi sepanjang satu dekade (", False, False),
        ("2014–2024", True, False),
        ("). Tiga tujuan utama metodologis Bab 2 meliputi:", False, False)
    ])
    add_body(doc, [
        ("1. ", True, False), ("Membongkar Bias Pengenceran Agregat (Aggregate Dilution Bias): ", True, False),
        ("Membuktikan bahwa indeks mutu air (IKA) dan udara (IKU) resmi pada skala provinsi menyamarkan tingkat keparahan polusi riil di sekitar tapak cerobong PLTU captive dan sungai pembuangan limbah tailing smelter.\n", False, False),
        ("2. ", True, False), ("Menguji Kausalitas Eksekusi Ruang vs Deforestasi: ", True, False),
        ("Mengukur kekuatan hubungan dan rasio peluang (Odds Ratio) antara alokasi luasan izin konsesi industri nikel terhadap percepatan kehilangan tutupan hutan alam primer.\n", False, False),
        ("3. ", True, False), ("Kuantifikasi Atribusi Karbon & Ancaman Kepunahan Satwa: ", True, False),
        ("Mendekomposisi faktor pendorong deforestasi guna membuktikan dominasi pelepasan emisi CO₂ serta memetakan pertampalan spasial titik perjumpaan spesies endemik kunci Wallacea dengan konsesi tambang.", False, False)
    ])

    # ── B. SUMBER DATA & CAKUPAN WILAYAH ─────────────────────────
    add_h2(doc, "B", "Sumber Data & Cakupan Wilayah")
    add_body(doc, [
        ("Penelitian mencakup seluruh wilayah daratan dan pesisir Pulau Sulawesi yang terbagi ke dalam ", False, False),
        ("6 provinsi", True, False),
        (" (Sulawesi Tengah, Sulawesi Tenggara, Sulawesi Selatan, Sulawesi Barat, Gorontalo, Sulawesi Utara) serta ", False, False),
        ("kawasan industri terpadu sentra nikel", True, False),
        (". Data yang dihimpun berbentuk panel tahunan (2014–2024) berbasis data terbuka resmi lintas kementerian, registri global, dan citra satelit independen:", False, False)
    ])
    add_body(doc, [
        ("• ", True, False), ("Kementerian Lingkungan Hidup dan Kehutanan (Ditjen PPKL): ", True, False),
        ("Indeks Kualitas Lingkungan Hidup (IKLH), Indeks Kualitas Air (IKA), Indeks Kualitas Udara (IKU), dan data status mutu sungai.\n", False, False),
        ("• ", True, False), ("ESDM (MODI & MinerbaOne) & Kementerian Investasi (BKPM): ", True, False),
        ("Inventarisasi unit fasilitas smelter nikel dan alokasi konsesi pertambangan.\n", False, False),
        ("• ", True, False), ("Global Energy Monitor (GEM) & RUPTL PLN: ", True, False),
        ("Registri geospasial unit dan kapasitas operasional PLTU captive industri batubara off-grid (Megawatt).\n", False, False),
        ("• ", True, False), ("Global Forest Watch (GFW / Hansen UMD) & IPCC: ", True, False),
        ("Time-series kehilangan tutupan pohon (Ha) dan estimasi emisi gas rumah kaca (Megagram CO₂e) per faktor pendorong.\n", False, False),
        ("• ", True, False), ("NASA TROPOMI (Sentinel-5P): ", True, False),
        ("Konsentrasi troposferik nitrogen dioksida (NO₂ rasio µmol/m²) di atas kawasan industri nikel.\n", False, False),
        ("• ", True, False), ("GBIF & IUCN Red List: ", True, False),
        ("269 titik koordinat geospasial perjumpaan aktual (occurrences) 7 spesies endemik kunci Wallacea dan status ancaman pertambangan (Mining Threat).", False, False)
    ])

    # ── C. OPERASIONALISASI VARIABEL & INDIKATOR RISET ──────────
    add_h2(doc, "C", "Operasionalisasi Variabel & Indikator Riset")
    add_body(doc, [
        ("Seluruh variabel lingkungan, emisi, ruang, dan keanekaragaman hayati dioperasionalkan secara terukur ke dalam ", False, False),
        ("10 indikator empiris terpadu", True, False),
        (" sebagaimana dirangkum pada matriks operasional berikut:", False, False)
    ])

    add_caption(doc, "Matriks Operasionalisasi Variabel dan Sumber Data Resmi Bab 2")
    table_indikator_data = [
        ["1", "Kepadatan Fasilitas Smelter", "Pemusatan Industri Pirometalurgi & HPAL", "Unit Fasilitas", "ESDM MODI & MinerbaOne"],
        ["2", "Indeks Kualitas Air (IKA)", "Status Mutu Air Sungai & Pesisir", "Poin Skor (0–100)", "Ditjen PPKL KLHK (IKLH)"],
        ["3", "Estimasi Timbulan Limbah B3", "Residu Tailing & Terak Slag Nikel", "Ton / Tahun", "Amdal Industri & Neraca KLHK"],
        ["4", "Kapasitas PLTU Captive Batubara", "Intensitas Pembangkit Listrik Off-Grid", "Megawatt (MW)", "Global Energy Monitor & RUPTL"],
        ["5", "Indeks Kualitas Udara (IKU)", "Status Mutu Udara Ambien Agregat", "Poin Skor (0–100)", "Ditjen PPKL KLHK (IKLH)"],
        ["6", "Konsentrasi Troposferik NO₂", "Pencemaran Polutan Udara Satelit", "µmol/m²", "Satelit NASA TROPOMI (Sentinel-5P)"],
        ["7", "Luas Konsesi IUP & Kawasan", "Alokasi Ruang Industri Ekstraktif", "Hektar (Ha)", "ESDM MODI & ATR/BPN"],
        ["8", "Luas Deforestasi Hutan Alam", "Kehilangan Tutupan Pohon Alami", "Hektar (Ha)", "Global Forest Watch (Hansen UMD)"],
        ["9", "Atribusi Emisi Karbon CO₂", "Pelepasan GRK per Faktor Pendorong", "Megagram CO₂e", "GFW & IPCC Tier-1 Methodology"],
        ["10", "Sebaran Spesies Endemik & IUCN", "Keterancaman Habitat Wallacea", "Titik & Kategori", "GBIF API & IUCN Red List"]
    ]

    add_table_styled(
        doc,
        headers=["No", "Indikator Riset", "Fokus Pengukuran", "Satuan", "Sumber Data Primer Resmi"],
        rows=table_indikator_data,
        col_widths_cm=[0.8, 4.5, 4.5, 2.2, 5.0],
        alignments=['C', 'L', 'L', 'C', 'L']
    )

    # ── D. KERANGKA ANALISIS & FORMULASI MATEMATIS ──────────────
    add_h2(doc, "D", "Kerangka Analisis & Formulasi Matematis")

    # 2.1
    add_h3(doc, "2.1 Dampak Limbah Tailing: Konsentrasi Smelter vs Indeks Kualitas Air (IKA)")
    add_body(doc, [
        ("Pemusatan unit pengolahan pirometalurgi dan hidrometalurgi dihitung berdasarkan agregasi titik fasilitas di setiap provinsi guna mengukur tekanan potensi pelepasan tailing dan slag nikel terhadap baku mutu sungai:", False, False)
    ])
    add_formula(doc, "Kepadatan Smelter (Unit) = Σ [ Fasilitas Smelter Beroperasi & Konstruksi di Provinsi ]")
    add_body(doc, [
        ("Status mutu air diukur menggunakan rata-rata indeks IKA provinsi. Protokol pengujian kontinjensi 2×2 diterapkan untuk menguji signifikansi hubungan antara kepadatan smelter dan status IKA kritis berbasis ambang median:", False, False)
    ])

    add_caption(doc, "Tabel 2.1a: Konfigurasi Variabel Uji Chi-Square (Sub-bab 2.1)")
    tabel_2_1a_rows = [
        ["Variabel Independen (X)", "Jumlah Smelter: Total fasilitas smelter (beroperasi maupun konstruksi)."],
        ["Variabel Dependen (Y)", "Indeks Kualitas Air: Skor baku mutu air per provinsi."],
        ["Hipotesis Nol (H0)", "Tidak ada hubungan signifikan secara statistik antara kepadatan smelter dengan Indeks Kualitas Air."],
        ["Hipotesis Alternatif (H1)", "Ada hubungan negatif antara kepadatan smelter dengan Indeks Kualitas Air (semakin padat smelter, semakin kritis mutu air)."],
        ["Decision Rule (Alpha 5%)", "Jika P-Value < 0.05, maka Tolak H0 (Terbukti signifikan bahwa smelter menurunkan mutu air)."],
        ["Threshold Kategori", "Nilai Median Data Panel 2016-2024 (N=54): X >= 75.0 fasilitas; Y >= 55.9 poin."],
        ["Orientasi Odds Ratio", "OR = ( a × d ) / ( b × c ) dengan a = Smelter Tinggi & IKA Kritis; mengukur risiko IKA kritis pada kelompok kepadatan smelter tinggi."]
    ]
    add_table_styled(
        doc,
        headers=["Komponen Uji", "Definisi Variabel (Sub-bab 2.1)"],
        rows=tabel_2_1a_rows,
        col_widths_cm=[4.5, 12.5],
        alignments=['L', 'L']
    )

    # 2.2
    add_h3(doc, "2.2 Kepungan Asap: Kapasitas PLTU vs Indeks Kualitas Udara (IKU)")
    add_body(doc, [
        ("Akumulasi beban emisi pembakaran batubara dihitung dari total kapasitas pembangkit listrik tenaga uap captive terpasang pada kawasan industri nikel:", False, False)
    ])
    add_formula(doc, "Total Kapasitas PLTU (MW) = Σ [ Kapasitas PLTU Captive Terpasang di Koridor Industri ]")
    add_body(doc, [
        ("Pengujian statistik tabulasi silang mengevaluasi interaksi antara kapasitas pembangkit off-grid terhadap penurunan skor mutu udara ambien (IKU) serta divalidasi oleh densitas polutan satelit NO₂:", False, False)
    ])

    add_caption(doc, "Tabel 2.2a: Konfigurasi Variabel Uji Chi-Square (Sub-bab 2.2)")
    tabel_2_2a_rows = [
        ["Variabel Independen (X)", "Kapasitas PLTU (MW): Total kapasitas PLTU Captive yang beroperasi."],
        ["Variabel Dependen (Y)", "Indeks Kualitas Udara: Skor baku mutu udara ambien per provinsi."],
        ["Hipotesis Nol (H0)", "Tidak ada hubungan signifikan secara statistik antara kapasitas PLTU dengan Indeks Kualitas Udara."],
        ["Hipotesis Alternatif (H1)", "Ada hubungan negatif antara kapasitas PLTU dengan Indeks Kualitas Udara (semakin besar kapasitas, semakin kritis mutu udara)."],
        ["Decision Rule (Alpha 5%)", "Jika P-Value < 0.05, maka Tolak H0 (Terbukti signifikan bahwa emisi PLTU menurunkan kualitas udara)."],
        ["Threshold Kategori", "Nilai Median Data Panel (N=54): X >= 220.0 MW; Y >= 91.0 poin."],
        ["Orientasi Odds Ratio", "OR = ( a × d ) / ( b × c ) dengan a = PLTU Tinggi & IKU Kritis; mengukur risiko IKU kritis pada kelompok kapasitas PLTU tinggi."]
    ]
    add_table_styled(
        doc,
        headers=["Komponen Uji", "Definisi Variabel (Sub-bab 2.2)"],
        rows=tabel_2_2a_rows,
        col_widths_cm=[4.5, 12.5],
        alignments=['L', 'L']
    )

    # 2.3
    add_h3(doc, "2.3 Eksekusi Ruang: Ekspansi Kawasan Industri vs Tekanan Ekologis (Deforestasi)")
    add_body(doc, [
        ("Total alokasi ruang konsesi industri nikel dihitung melalui penjumlahan luasan izin usaha pertambangan (IUP) aktif dan zonasi kawasan industri terpadu:", False, False)
    ])
    add_formula(doc, "Total Alokasi Ruang (Ha) = Σ [ Luas Konsesi IUP Tambang + Luas Tapak Kawasan Industri ]")
    add_body(doc, [
        ("Uji independensi Chi-Square (α = 5%, df = 1) dan Odds Ratio diterapkan untuk menguji hipotesis pembuktian apakah penguasaan ruang skala besar meningkatkan risiko deforestasi terbuka secara eksponensial:", False, False)
    ])

    add_caption(doc, "Tabel 2.3a: Konfigurasi Variabel Uji Chi-Square (Sub-bab 2.3)")
    tabel_2_3a_rows = [
        ["Variabel Independen (X)", "Luas Ekspansi Industri (Ha) / Luas IUP & Kawasan (Ha)"],
        ["Variabel Dependen (Y)", "Kehilangan Tutupan Pohon (Ha) / Total Deforestasi Alam (Ha)"],
        ["Hipotesis Nol (H0)", "Luasan ekspansi kawasan industri dan perizinan tambang tidak berhubungan dengan laju deforestasi."],
        ["Hipotesis Alternatif (H1)", "Alokasi izin lahan (Luas IUP & Kawasan) berkorelasi positif dengan laju deforestasi."],
        ["Decision Rule (Alpha 5%)", "Jika P-Value < 0.05, maka Tolak H0 (terbukti signifikan bahwa ekspansi izin lahan mendorong deforestasi)."],
        ["Threshold Kategori", "Nilai Median Data Panel (N=60): X >= 138,148.8 Ha; Y >= 15,917.7 Ha."],
        ["Orientasi Odds Ratio", "OR = ( a × d ) / ( b × c ) dengan a = IUP Tinggi & Deforestasi Tinggi/Parah; mengukur risiko deforestasi parah pada kelompok luas IUP tinggi."]
    ]
    add_table_styled(
        doc,
        headers=["Komponen Uji", "Definisi Variabel (Sub-bab 2.3)"],
        rows=tabel_2_3a_rows,
        col_widths_cm=[4.5, 12.5],
        alignments=['L', 'L']
    )

    # 2.4
    add_h3(doc, "2.4 Driver Deforestasi: Analisis Faktor Pendorong Perubahan Tutupan Hutan")
    add_body(doc, [
        ("Dekomposisi faktor pendorong deforestasi mengkuantifikasi porsi relatif pembabatan hutan alami ke dalam empat kategori pendorong utama, serta menghitung kuantitas pelepasan karbon teratribusi:", False, False)
    ])
    add_formula(doc, "Proporsi Driver (%) = [ Deforestasi Driver Spesifik (Ha) / Total Deforestasi (Ha) ] × 100")
    add_formula(doc, "Atribusi Emisi CO₂ (Mg) = Total Deforestasi Driver (Ha) × Koefisien Karbon Lanskap (Mg CO₂/Ha)")

    # 2.5
    add_h3(doc, "2.5 Kehancuran Biodiversitas: Dampak Terhadap Habitat Satwa Endemik")
    add_body(doc, [
        ("Analisis keterancaman keanekaragaman hayati mengintegrasikan 269 titik perjumpaan aktual (occurrences) GBIF dari 7 spesies endemik kunci Wallacea dengan analisis tumpang tindih spasial (overlay) poligon konsesi pertambangan dan status ancaman kepunahan internasional (IUCN Red List):", False, False)
    ])
    add_formula(doc, "Kepadatan Occurrence (Titik/Km²) = Jumlah Titik Perjumpaan GBIF / Luas Wilayah Observasi (Km²)")

    # ── E. KORESPONDENSI METODOLOGI TERHADAP SUB-BAB LAPORAN ────
    add_h2(doc, "E", "Korespondensi Metodologi terhadap Sub-bab Laporan Bab 2")
    add_body(doc, [
        ("Setiap sub-bab analitis pada Bab 2 ditopang oleh metode kuantitatif yang presisi dan menghasilkan sintesis bukti empiris terstandarisasi sebagaimana dirangkum pada matriks berikut:", False, False)
    ])

    table_korespondensi = [
        ["Sub-bab 2.1", "Limbah Tailing & Mutu Air (IKA)", "Pemetaan Spasial Smelter, Uji Non-parametrik Chi-Square (χ²), Odds Ratio (OR)"],
        ["Sub-bab 2.2", "Emisi PLTU Captive & Mutu Udara (IKU)", "Pemetaan Kapasitas Pembangkit MW, Uji Chi-Square (χ²), Validasi Satelit NO₂"],
        ["Sub-bab 2.3", "Ekspansi Ruang Industri vs Deforestasi", "Animated Bubble Chart Temporal, Uji Chi-Square (χ²), Odds Ratio Risiko (OR)"],
        ["Sub-bab 2.4", "Dekomposisi Driver Deforestasi & Emisi CO₂", "Agregasi Tabular Atribusi Kausalitas, Proporsi Pendorong, Koefisien Emisi Karbon"],
        ["Sub-bab 2.5", "Fragmentasi Habitat & Satwa Endemik", "Spatial Overlay GBIF Occurrence, Sintesis Status Keterancaman IUCN Red List"]
    ]

    add_table_styled(
        doc,
        headers=["Sub-bab", "Fokus Kajian Empiris", "Metode Analitis Utama"],
        rows=table_korespondensi,
        col_widths_cm=[2.5, 5.5, 9.0],
        alignments=['C', 'L', 'L']
    )

    # ── F. BAGAN ALUR KERANGKA KERJA RISET BAB 2 ────────────────
    add_h2(doc, "F", "Bagan Alur Kerangka Kerja Riset (Research Workflow)")
    add_body(doc, [
        ("Kerangka operasional metodologi Bab 2 berjalan secara terpadu melalui empat fase berurutan sebagaimana divisualisasikan pada bagan alur kerja riset berikut:", False, False)
    ])

    mermaid_str_f = """flowchart LR
    subgraph F1["Fase I: Akuisisi Data"]
        A1["Kurasi Data Resmi Terbuka<br/><i>KLHK, ESDM, GEM, GFW, NASA, GBIF</i>"]
        A2["Panel Provinsi-Tahun<br/><i>6 Provinsi Se-Sulawesi (N=54 s.d. 60)</i>"]
    end
    subgraph F2["Fase II: Harmonisasi Spasial"]
        B1["Penyelarasan Koordinat<br/><i>Smelter, PLTU, Konsesi & Titik GBIF</i>"]
        B2["Overlay Geospasial<br/><i>Baku Mutu vs Tekanan Industri</i>"]
    end
    subgraph F3["Fase III: Uji Statistik"]
        C1["Tabel Kontinjensi 2x2<br/><i>Ambang Median High vs Low</i>"]
        C2["Uji Chi-Square & Odds Ratio<br/><i>Signifikansi & Kelipatan Risiko</i>"]
    end
    subgraph F4["Fase IV: Atribusi & Sintesis"]
        D1["Dekomposisi Driver CO2<br/><i>Pertambangan vs Agrikultur</i>"]
        D2["Bukti Kausalitas D3TLH<br/><i>Degradasi Air, Udara & Biodiversitas</i>"]
    end
    F1 --> F2 --> F3 --> F4"""

    png_workflow_path = str(out_dir_compact / "mermaid_workflow_bab2.png")
    is_downloaded = download_mermaid_png(mermaid_str_f, png_workflow_path)

    add_caption(doc, "Bagan Alur 2.1: Alur Logika Kerangka Kerja Riset Bab 2 (Research Workflow)")
    if is_downloaded and os.path.exists(png_workflow_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(3)
        p_img.paragraph_format.space_after  = Pt(4)
        r_img = p_img.add_run()
        r_img.add_picture(png_workflow_path, width=Cm(16.5))
        try:
            shutil.copyfile(png_workflow_path, str(out_dir_bab2 / "mermaid_workflow_bab2.png"))
        except Exception:
            pass

    # Box Output Kesimpulan
    p_box = doc.add_paragraph()
    p_box.paragraph_format.space_before = Pt(4)
    p_box.paragraph_format.space_after  = Pt(4)
    all_border_para(p_box, color='1B5E20', sz='8')
    para_shd(p_box, 'F1F8E9')
    add_run(p_box, "KERANGKA KELUARAN METODOLOGIS BAB 2:\n", bold=True, pt=8.5, color=G_DARK)
    add_run(p_box, "1. Konfigurasi Baku Mutu Lingkungan vs Titik Tekanan Industri: Mengisolasi anomali aggregate dilution bias pada indeks agregat provinsi (IKA dan IKU) terhadap pencemaran riil di tapak industri.\n"
                   "2. Konfigurasi Inferensial Eksekusi Ruang: Menguji signifikansi kausalitas alokasi izin lahan terhadap percepatan laju deforestasi tutupan hutan melalui matriks kontinjensi Chi-Square dan rasio peluang (OR).\n"
                   "3. Konfigurasi Dekomposisi Driver & Integritas Biodiversitas: Mengkuantifikasi kontribusi dominan sektor pertambangan terhadap pelepasan emisi karbon dan memvalidasi krisis keterancaman habitat satwa endemik Wallacea.",
            pt=8, color=C_BODY)

    # ── SIMPAN DOKUMEN DOCX (DUAL SAVE) ─────────────────────────
    docx_compact = out_dir_compact / "Metodologi_Bab2_Kualitas_Lingkungan_Compact.docx"
    docx_bab2    = out_dir_bab2 / "Metodologi_Bab2_Kualitas_Lingkungan_Compact.docx"
    
    doc.save(str(docx_compact))
    shutil.copyfile(docx_compact, docx_bab2)
    print(f"  [OK] Tersimpan DOCX: {docx_compact}")
    print(f"  [OK] Salinan DOCX : {docx_bab2}")

    # ── GENERATE MARKDOWN PADANAN ───────────────────────────────
    print("[2/3] Membangun dokumen Markdown padanan...")
    MD_CONTENT = """# METODOLOGI PENELITIAN: BAB 2 — ANALISIS KUALITAS LINGKUNGAN DI KAWASAN SMELTER
*CELIOS (Center of Economic and Law Studies) · Audit Spasial-Statistik D3TLH Sulawesi (2014–2024) · Ringkasan Eksekutif Metodologis*

---

## A. Desain Penelitian & Tujuan
Penelitian ini menggunakan **desain audit spasial-statistik kuantitatif dan inferensial bivariat terintegrasi** untuk mengukur dampak degradasi lingkungan hidup akibat pemusatan fasilitas smelter nikel dan kawasan industri bertenaga PLTU captive batubara di enam provinsi Pulau Sulawesi sepanjang satu dekade (**2014–2024**). Tiga tujuan utama metodologis Bab 2 meliputi:

1. **Membongkar Bias Pengenceran Agregat (Aggregate Dilution Bias):** Membuktikan bahwa indeks mutu air (IKA) dan udara (IKU) resmi pada skala provinsi menyamarkan tingkat keparahan polusi riil di sekitar tapak cerobong PLTU captive dan sungai pembuangan limbah tailing smelter.
2. **Menguji Kausalitas Eksekusi Ruang vs Deforestasi:** Mengukur kekuatan hubungan dan rasio peluang (Odds Ratio) antara alokasi luasan izin konsesi industri nikel terhadap percepatan kehilangan tutupan hutan alam primer.
3. **Kuantifikasi Atribusi Karbon & Ancaman Kepunahan Satwa:** Mendekomposisi faktor pendorong deforestasi guna membuktikan dominasi pelepasan emisi CO₂ serta memetakan pertampalan spasial titik perjumpaan spesies endemik kunci Wallacea dengan konsesi tambang.

---

## B. Sumber Data & Cakupan Wilayah
Penelitian mencakup seluruh wilayah daratan dan pesisir Pulau Sulawesi yang terbagi ke dalam **6 provinsi** (Sulawesi Tengah, Sulawesi Tenggara, Sulawesi Selatan, Sulawesi Barat, Gorontalo, Sulawesi Utara) serta **kawasan industri terpadu sentra nikel**. Data yang dihimpun berbentuk panel tahunan (2014–2024) berbasis data terbuka resmi lintas kementerian, registri global, dan citra satelit independen:

- **Kementerian Lingkungan Hidup dan Kehutanan (Ditjen PPKL):** Indeks Kualitas Lingkungan Hidup (IKLH), Indeks Kualitas Air (IKA), Indeks Kualitas Udara (IKU), dan data status mutu sungai.
- **ESDM (MODI & MinerbaOne) & Kementerian Investasi (BKPM):** Inventarisasi unit fasilitas smelter nikel dan alokasi konsesi pertambangan.
- **Global Energy Monitor (GEM) & RUPTL PLN:** Registri geospasial unit dan kapasitas operasional PLTU captive industri batubara off-grid (Megawatt).
- **Global Forest Watch (GFW / Hansen UMD) & IPCC:** Time-series kehilangan tutupan pohon (Ha) dan estimasi emisi gas rumah kaca (Megagram CO₂e) per faktor pendorong.
- **NASA TROPOMI (Sentinel-5P):** Konsentrasi troposferik nitrogen dioksida (NO₂ rasio µmol/m²) di atas kawasan industri nikel.
- **GBIF & IUCN Red List:** 269 titik koordinat geospasial perjumpaan aktual (occurrences) 7 spesies endemik kunci Wallacea dan status ancaman pertambangan (Mining Threat).

---

## C. Operasionalisasi Variabel & Indikator Riset
Seluruh variabel lingkungan, emisi, ruang, dan keanekaragaman hayati dioperasionalkan secara terukur ke dalam **10 indikator empiris terpadu** sebagaimana dirangkum pada matriks operasional berikut:

##### Matriks Operasionalisasi Variabel dan Sumber Data Resmi Bab 2
| No | Indikator Riset | Fokus Pengukuran | Satuan | Sumber Data Primer Resmi |
| :-: | :--- | :--- | :-: | :--- |
| 1 | Kepadatan Fasilitas Smelter | Pemusatan Industri Pirometalurgi & HPAL | Unit Fasilitas | ESDM MODI & MinerbaOne |
| 2 | Indeks Kualitas Air (IKA) | Status Mutu Air Sungai & Pesisir | Poin Skor (0–100) | Ditjen PPKL KLHK (IKLH) |
| 3 | Estimasi Timbulan Limbah B3 | Residu Tailing & Terak Slag Nikel | Ton / Tahun | Amdal Industri & Neraca KLHK |
| 4 | Kapasitas PLTU Captive Batubara | Intensitas Pembangkit Listrik Off-Grid | Megawatt (MW) | Global Energy Monitor & RUPTL |
| 5 | Indeks Kualitas Udara (IKU) | Status Mutu Udara Ambien Agregat | Poin Skor (0–100) | Ditjen PPKL KLHK (IKLH) |
| 6 | Konsentrasi Troposferik NO₂ | Pencemaran Polutan Udara Satelit | µmol/m² | Satelit NASA TROPOMI (Sentinel-5P) |
| 7 | Luas Konsesi IUP & Kawasan | Alokasi Ruang Industri Ekstraktif | Hektar (Ha) | ESDM MODI & ATR/BPN |
| 8 | Luas Deforestasi Hutan Alam | Kehilangan Tutupan Pohon Alami | Hektar (Ha) | Global Forest Watch (Hansen UMD) |
| 9 | Atribusi Emisi Karbon CO₂ | Pelepasan GRK per Faktor Pendorong | Megagram CO₂e | GFW & IPCC Tier-1 Methodology |
| 10 | Sebaran Spesies Endemik & IUCN | Keterancaman Habitat Wallacea | Titik & Kategori | GBIF API & IUCN Red List |

---

## D. Kerangka Analisis & Formulasi Matematis

### 2.1 Dampak Limbah Tailing: Konsentrasi Smelter vs Indeks Kualitas Air (IKA)
Pemusatan unit pengolahan pirometalurgi dan hidrometalurgi dihitung berdasarkan agregasi titik fasilitas di setiap provinsi guna mengukur tekanan potensi pelepasan tailing dan slag nikel terhadap baku mutu sungai:

> `Kepadatan Smelter (Unit) = Σ [ Fasilitas Smelter Beroperasi & Konstruksi di Provinsi ]`

Status mutu air diukur menggunakan rata-rata indeks IKA provinsi. Protokol pengujian kontinjensi 2×2 diterapkan untuk menguji signifikansi hubungan antara kepadatan smelter dan status IKA kritis berbasis ambang median:

##### Tabel 2.1a: Konfigurasi Variabel Uji Chi-Square (Sub-bab 2.1)
| Komponen Uji | Definisi Variabel (Sub-bab 2.1) |
| :--- | :--- |
| **Variabel Independen (X)** | Jumlah Smelter: Total fasilitas smelter (beroperasi maupun konstruksi). |
| **Variabel Dependen (Y)** | Indeks Kualitas Air: Skor baku mutu air per provinsi. |
| **Hipotesis Nol (H0)** | Tidak ada hubungan signifikan secara statistik antara kepadatan smelter dengan Indeks Kualitas Air. |
| **Hipotesis Alternatif (H1)** | Ada hubungan negatif antara kepadatan smelter dengan Indeks Kualitas Air (semakin padat smelter, semakin kritis mutu air). |
| **Decision Rule (Alpha 5%)** | Jika P-Value < 0.05, maka Tolak H0 (Terbukti signifikan bahwa smelter menurunkan mutu air). |
| **Threshold Kategori** | Nilai Median Data Panel 2016-2024 (N=54): X >= 75.0 fasilitas; Y >= 55.9 poin. |
| **Orientasi Odds Ratio** | OR = ( a × d ) / ( b × c ) dengan a = Smelter Tinggi & IKA Kritis; mengukur risiko IKA kritis pada kelompok kepadatan smelter tinggi. |

### 2.2 Kepungan Asap: Kapasitas PLTU vs Indeks Kualitas Udara (IKU)
Akumulasi beban emisi pembakaran batubara dihitung dari total kapasitas pembangkit listrik tenaga uap captive terpasang pada kawasan industri nikel:

> `Total Kapasitas PLTU (MW) = Σ [ Kapasitas PLTU Captive Terpasang di Koridor Industri ]`

Pengujian statistik tabulasi silang mengevaluasi interaksi antara kapasitas pembangkit off-grid terhadap penurunan skor mutu udara ambien (IKU) serta divalidasi oleh densitas polutan satelit NO₂:

##### Tabel 2.2a: Konfigurasi Variabel Uji Chi-Square (Sub-bab 2.2)
| Komponen Uji | Definisi Variabel (Sub-bab 2.2) |
| :--- | :--- |
| **Variabel Independen (X)** | Kapasitas PLTU (MW): Total kapasitas PLTU Captive yang beroperasi. |
| **Variabel Dependen (Y)** | Indeks Kualitas Udara: Skor baku mutu udara ambien per provinsi. |
| **Hipotesis Nol (H0)** | Tidak ada hubungan signifikan secara statistik antara kapasitas PLTU dengan Indeks Kualitas Udara. |
| **Hipotesis Alternatif (H1)** | Ada hubungan negatif antara kapasitas PLTU dengan Indeks Kualitas Udara (semakin besar kapasitas, semakin kritis mutu udara). |
| **Decision Rule (Alpha 5%)** | Jika P-Value < 0.05, maka Tolak H0 (Terbukti signifikan bahwa emisi PLTU menurunkan kualitas udara). |
| **Threshold Kategori** | Nilai Median Data Panel (N=54): X >= 220.0 MW; Y >= 91.0 poin. |
| **Orientasi Odds Ratio** | OR = ( a × d ) / ( b × c ) dengan a = PLTU Tinggi & IKU Kritis; mengukur risiko IKU kritis pada kelompok kapasitas PLTU tinggi. |

### 2.3 Eksekusi Ruang: Ekspansi Kawasan Industri vs Tekanan Ekologis (Deforestasi)
Total alokasi ruang konsesi industri nikel dihitung melalui penjumlahan luasan izin usaha pertambangan (IUP) aktif dan zonasi kawasan industri terpadu:

> `Total Alokasi Ruang (Ha) = Σ [ Luas Konsesi IUP Tambang + Luas Tapak Kawasan Industri ]`

Uji independensi Chi-Square (α = 5%, df = 1) dan Odds Ratio diterapkan untuk menguji hipotesis pembuktian apakah penguasaan ruang skala besar meningkatkan risiko deforestasi terbuka secara eksponensial:

##### Tabel 2.3a: Konfigurasi Variabel Uji Chi-Square (Sub-bab 2.3)
| Komponen Uji | Definisi Variabel (Sub-bab 2.3) |
| :--- | :--- |
| **Variabel Independen (X)** | Luas Ekspansi Industri (Ha) / Luas IUP & Kawasan (Ha) |
| **Variabel Dependen (Y)** | Kehilangan Tutupan Pohon (Ha) / Total Deforestasi Alam (Ha) |
| **Hipotesis Nol (H0)** | Luasan ekspansi kawasan industri dan perizinan tambang tidak berhubungan dengan laju deforestasi. |
| **Hipotesis Alternatif (H1)** | Alokasi izin lahan (Luas IUP & Kawasan) berkorelasi positif dengan laju deforestasi. |
| **Decision Rule (Alpha 5%)** | Jika P-Value < 0.05, maka Tolak H0 (terbukti signifikan bahwa ekspansi izin lahan mendorong deforestasi). |
| **Threshold Kategori** | Nilai Median Data Panel (N=60): X >= 138,148.8 Ha; Y >= 15,917.7 Ha. |
| **Orientasi Odds Ratio** | OR = ( a × d ) / ( b × c ) dengan a = IUP Tinggi & Deforestasi Tinggi/Parah; mengukur risiko deforestasi parah pada kelompok luas IUP tinggi. |

### 2.4 Driver Deforestasi: Analisis Faktor Pendorong Perubahan Tutupan Hutan
Dekomposisi faktor pendorong deforestasi mengkuantifikasi porsi relatif pembabatan hutan alami ke dalam empat kategori pendorong utama, serta menghitung kuantitas pelepasan karbon teratribusi:

> `Proporsi Driver (%) = [ Deforestasi Driver Spesifik (Ha) / Total Deforestasi (Ha) ] × 100`

> `Atribusi Emisi CO₂ (Mg) = Total Deforestasi Driver (Ha) × Koefisien Karbon Lanskap (Mg CO₂/Ha)`

### 2.5 Kehancuran Biodiversitas: Dampak Terhadap Habitat Satwa Endemik
Analisis keterancaman keanekaragaman hayati mengintegrasikan 269 titik perjumpaan aktual (occurrences) GBIF dari 7 spesies endemik kunci Wallacea dengan analisis tumpang tindih spasial (overlay) poligon konsesi pertambangan dan status ancaman kepunahan internasional (IUCN Red List):

> `Kepadatan Occurrence (Titik/Km²) = Jumlah Titik Perjumpaan GBIF / Luas Wilayah Observasi (Km²)`

---

## E. Korespondensi Metodologi terhadap Sub-bab Laporan Bab 2
Setiap sub-bab analitis pada Bab 2 ditopang oleh metode kuantitatif yang presisi dan menghasilkan sintesis bukti empiris terstandarisasi sebagaimana dirangkum pada matriks berikut:

##### Matriks Korespondensi Sub-bab terhadap Metode Analitis
| Sub-bab | Fokus Kajian Empiris | Metode Analitis Utama |
| :---: | :--- | :--- |
| **Sub-bab 2.1** | Limbah Tailing & Mutu Air (IKA) | Pemetaan Spasial Smelter, Uji Non-parametrik Chi-Square (χ²), Odds Ratio (OR) |
| **Sub-bab 2.2** | Emisi PLTU Captive & Mutu Udara (IKU) | Pemetaan Kapasitas Pembangkit MW, Uji Chi-Square (χ²), Validasi Satelit NO₂ |
| **Sub-bab 2.3** | Ekspansi Ruang Industri vs Deforestasi | Animated Bubble Chart Temporal, Uji Chi-Square (χ²), Odds Ratio Risiko (OR) |
| **Sub-bab 2.4** | Dekomposisi Driver Deforestasi & Emisi CO₂ | Agregasi Tabular Atribusi Kausalitas, Proporsi Pendorong, Koefisien Emisi Karbon |
| **Sub-bab 2.5** | Fragmentasi Habitat & Satwa Endemik | Spatial Overlay GBIF Occurrence, Sintesis Status Keterancaman IUCN Red List |

---

## F. Bagan Alur Kerangka Kerja Riset (Research Workflow)

```mermaid
flowchart LR
    subgraph F1["Fase I: Akuisisi Data"]
        A1["Kurasi Data Resmi Terbuka<br/><i>KLHK, ESDM, GEM, GFW, NASA, GBIF</i>"]
        A2["Panel Provinsi-Tahun<br/><i>6 Provinsi Se-Sulawesi (N=54 s.d. 60)</i>"]
    end
    subgraph F2["Fase II: Harmonisasi Spasial"]
        B1["Penyelarasan Koordinat<br/><i>Smelter, PLTU, Konsesi & Titik GBIF</i>"]
        B2["Overlay Geospasial<br/><i>Baku Mutu vs Tekanan Industri</i>"]
    end
    subgraph F3["Fase III: Uji Statistik"]
        C1["Tabel Kontinjensi 2x2<br/><i>Ambang Median High vs Low</i>"]
        C2["Uji Chi-Square & Odds Ratio<br/><i>Signifikansi & Kelipatan Risiko</i>"]
    end
    subgraph F4["Fase IV: Atribusi & Sintesis"]
        D1["Dekomposisi Driver CO2<br/><i>Pertambangan vs Agrikultur</i>"]
        D2["Bukti Kausalitas D3TLH<br/><i>Degradasi Air, Udara & Biodiversitas</i>"]
    end
    F1 --> F2 --> F3 --> F4
```

> **KERANGKA KELUARAN METODOLOGIS BAB 2:**  
> 1. **Konfigurasi Baku Mutu Lingkungan vs Titik Tekanan Industri:** Mengisolasi anomali aggregate dilution bias pada indeks agregat provinsi (IKA dan IKU) terhadap pencemaran riil di tapak industri.  
> 2. **Konfigurasi Inferensial Eksekusi Ruang:** Menguji signifikansi kausalitas alokasi izin lahan terhadap percepatan laju deforestasi tutupan hutan melalui matriks kontinjensi Chi-Square dan rasio peluang (OR).  
> 3. **Konfigurasi Dekomposisi Driver & Integritas Biodiversitas:** Mengkuantifikasi kontribusi dominan sektor pertambangan terhadap pelepasan emisi karbon dan memvalidasi krisis keterancaman habitat satwa endemik Wallacea.
"""

    md_compact = out_dir_compact / "Metodologi_Bab2_Kualitas_Lingkungan_Compact.md"
    md_bab2    = out_dir_bab2 / "Metodologi_Bab2_Kualitas_Lingkungan_Compact.md"
    for pth in [md_compact, md_bab2]:
        with open(pth, "w", encoding="utf-8") as f:
            f.write(MD_CONTENT)
    print(f"  [OK] Tersimpan MD  : {md_compact}")
    print(f"  [OK] Salinan MD   : {md_bab2}")

    print("[3/3] Selesai menghasilkan dokumen metodologi Bab 2 versi compact (1-Kolom, 2-3 Halaman).")


if __name__ == "__main__":
    generate_bab2_compact()
