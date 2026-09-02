#!/usr/bin/env python3
"""
Generator Metodologi Versi Compact Bab 1 — GAYA V3 (EBT PODES)
Mengadopsi arsitektur docs/generate_methodology_docx_v3.py dari proyek 8.1 Celios4-EBTsmallstack:
- SATU HALAMAN, layout dua kolom (tabel layout kiri/kanan)
- Seksi bernomor ringkas: 1 Desain, 2 Sumber Data, 3 Operasionalisasi, 4 Kerangka Analisis (4.x),
  5 Korespondensi Sub-bab-Metode, 6 Bagan Alur snake Fase I-IV
- Formula box satu baris bernotasi mudah dibaca publik (tanpa Sigma/subscript kriptik)
- TIDAK mereplikasi tabel data & persamaan substitusi dokumen root non-compact
- Sumber data ditulis sebagai institusi resmi (tanpa nama file CSV)
- Tanpa icon/emoji
"""

import os
import shutil
from pathlib import Path

try:
    from docx import Document
    from docx.shared import Pt, RGBColor, Cm
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_ALIGN_VERTICAL
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-docx"])
    from docx import Document
    from docx.shared import Pt, RGBColor, Cm
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_ALIGN_VERTICAL
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement

# ── Warna ───────────────────────────────────────────────────
G_DARK  = RGBColor(0x1B, 0x5E, 0x20)
G_MID   = RGBColor(0x2E, 0x7D, 0x32)
C_BODY  = RGBColor(0x22, 0x22, 0x22)
C_GREY  = RGBColor(0x55, 0x55, 0x55)
C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)

# ── Pembantu XML ────────────────────────────────────────────
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

def cell_margin(cell, left=0, right=0, top=0, bottom=0):
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

def para_border_bottom(p, color='2E7D32'):
    pPr  = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    el   = OxmlElement('w:bottom')
    el.set(qn('w:val'), 'single')
    el.set(qn('w:sz'), '4')
    el.set(qn('w:space'), '1')
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

def all_border_para(p, color='444444', sz='4'):
    pPr  = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    for side in ['top', 'left', 'bottom', 'right']:
        el = OxmlElement(f'w:{side}')
        el.set(qn('w:val'), 'single')
        el.set(qn('w:sz'), sz)
        el.set(qn('w:space'), '2')
        el.set(qn('w:color'), color)
        pBdr.append(el)
    pPr.append(pBdr)

# ── Pembantu konten ─────────────────────────────────────────
def run(p, text, bold=False, italic=False, pt=8.5, color=None, mono=False):
    r = p.add_run(text)
    r.bold           = bold
    r.italic         = italic
    r.font.size      = Pt(pt)
    r.font.color.rgb = color if color else C_BODY
    if mono:
        r.font.name = 'Courier New'
        r._element.rPr.rFonts.set(qn('w:ascii'), 'Courier New')
    return r

def h2(cell, num, title):
    p = cell.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after  = Pt(2)
    para_border_bottom(p)
    run(p, f'{num}.  {title.upper()}', bold=True, pt=7.5, color=G_DARK)

def h3(cell, text):
    p = cell.add_paragraph()
    p.paragraph_format.space_before = Pt(3.5)
    p.paragraph_format.space_after  = Pt(1)
    run(p, text, bold=True, pt=8, color=G_MID)

def body(cell, parts, after=3):
    p = cell.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(after)
    for text, bold, italic in parts:
        run(p, text, bold=bold, italic=italic)
    return p

def formula(cell, text):
    p = cell.add_paragraph()
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.left_indent = Pt(4)
    para_shd(p, 'EDF7EE')
    run(p, text, pt=7.5, color=G_MID, mono=True)

def note_box(cell, text):
    p = cell.add_paragraph()
    p.paragraph_format.space_after  = Pt(2)
    p.paragraph_format.left_indent  = Pt(8)
    para_border_left(p)
    para_shd(p, 'F1F8E9')
    run(p, text, italic=True, pt=7.5, color=C_GREY)

def data_table(doc, cell, headers, rows, col_widths_cm):
    tbl = doc.add_table(rows=1 + len(rows), cols=len(headers))
    tbl.style = 'Table Grid'
    tbl.autofit = False
    for j, (h, w) in enumerate(zip(headers, col_widths_cm)):
        c = tbl.rows[0].cells[j]
        c.width = Cm(w)
        cell_shd(c, '2E7D32')
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after  = Pt(1)
        run(p, h, bold=True, pt=7, color=C_WHITE)
    for i, row_data in enumerate(rows):
        fill = 'F5FBF5' if i % 2 == 0 else 'FFFFFF'
        for j, val in enumerate(row_data):
            c = tbl.cell(i + 1, j)
            c.width = Cm(col_widths_cm[j])
            cell_shd(c, fill)
            p = c.paragraphs[0]
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after  = Pt(1)
            run(p, str(val), pt=7)
    doc.element.body.remove(tbl._tbl)
    cell._tc.append(tbl._tbl)
    return tbl

def fc_terminal(cell, text, is_output=False):
    p = cell.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(1)
    if is_output:
        all_border_para(p, color='1B5E20', sz='8')
        para_shd(p, 'F1F8E9')
        run(p, text, bold=True, pt=7, color=G_DARK)
    else:
        all_border_para(p, color='444444', sz='4')
        run(p, text, bold=True, pt=7, color=C_BODY)

def fc_arrow(cell):
    p = cell.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after  = Pt(0)
    run(p, '↓', pt=9, color=G_MID)

# ═══════════════════════════════════════════════════════════
# BANGUN DOKUMEN
# ═══════════════════════════════════════════════════════════
doc = Document()

sec = doc.sections[0]
sec.page_width    = Cm(21.0)
sec.page_height   = Cm(29.7)
sec.left_margin   = Cm(1.5)
sec.right_margin  = Cm(1.5)
sec.top_margin    = Cm(1.5)
sec.bottom_margin = Cm(1.5)

doc.styles['Normal'].font.name = 'Calibri'
doc.styles['Normal'].font.size = Pt(8.5)

# ── Judul Dokumen ───────────────────────────────────────────
p_t = doc.add_paragraph()
p_t.paragraph_format.space_after = Pt(1)
run(p_t, 'METODOLOGI PENELITIAN — BAB 1: EKSPANSI INDUSTRI EKSTRAKTIF DAN INFRASTRUKTUR PENUNJANG DI PULAU SULAWESI',
    bold=True, pt=9.5, color=G_DARK)
p_s = doc.add_paragraph()
p_s.paragraph_format.space_after = Pt(2)
para_border_bottom(p_s, color='1B5E20')
run(p_s, 'CELIOS — Center of Economic and Law Studies  ·  Riset Daya Dukung & Daya Tampung Lingkungan Hidup (D3TLH) Sulawesi  ·  2014–2024',
    italic=True, pt=7.5, color=C_GREY)

# ── Tabel tata letak dua kolom ─────────────────────────────
avail = sec.page_width - sec.left_margin - sec.right_margin
cw    = avail // 2

layout = doc.add_table(rows=1, cols=2)
layout.autofit = False
layout.columns[0].width = cw
layout.columns[1].width = cw

LC = layout.cell(0, 0)
RC = layout.cell(0, 1)
LC.vertical_alignment = WD_ALIGN_VERTICAL.TOP
RC.vertical_alignment = WD_ALIGN_VERTICAL.TOP

set_cell_borders(LC, right={'val': 'single', 'sz': '4', 'color': 'BBBBBB', 'space': '0'})
set_cell_borders(RC)

cell_margin(LC, left=0,   right=150, top=0, bottom=0)
cell_margin(RC, left=150, right=0,   top=0, bottom=0)

for c in [LC, RC]:
    for p in c.paragraphs:
        p._element.getparent().remove(p._element)

# ── KOLOM KIRI ──────────────────────────────────────────────

h2(LC, '1', 'Desain Penelitian & Tujuan')
body(LC, [
    ('Penelitian ini menggunakan ', False, False),
    ('desain audit spasial-statistik kuantitatif', True, False),
    (' untuk membedah ekspansi industri ekstraktif (tambang, smelter, PLTU captive) di enam provinsi Pulau Sulawesi sepanjang ', False, False),
    ('2014–2024', True, False),
    (' berbasis data resmi terbuka lintas kementerian/lembaga. Tiga tujuan utama: (1) ', False, False),
    ('mengukur', True, False),
    (' dominasi sektor ekstraktif dalam struktur PDRB provinsi dan kabupaten; (2) ', False, False),
    ('mengidentifikasi', True, False),
    (' konsentrasi spasial fasilitas smelter, PLTU captive, izin tambang, dan modal PMDN; serta (3) ', False, False),
    ('menguji', True, False),
    (' keterkaitan statistik antara tekanan industri dan kehilangan tutupan hutan.', False, False),
])

h2(LC, '2', 'Sumber Data & Cakupan')
body(LC, [
    ('Seluruh data bersumber dari institusi resmi (', False, False),
    ('BPS, ESDM/Minerbaone, BKPM, GEM, GFW, KNKT', True, False),
    (' — diolah CELIOS), mencakup 6 provinsi se-Sulawesi 2014–2024 dan membentuk data panel provinsi-tahun (N = 60) untuk seluruh pengujian statistik.', False, False),
])

h2(LC, '3', 'Operasionalisasi Indikator')
data_table(doc, LC,
    headers=['#', 'Indikator', 'Institusi Sumber Resmi'],
    rows=[
        ('1', 'PDRB Sektoral Provinsi & Kabupaten', 'BPS (Subject 52)'),
        ('2', 'IUP Tambang Baru & Luas Konsesi',    'ESDM — Minerbaone'),
        ('3', 'Smelter Nikel (778 unit)',           'ESDM & CGS'),
        ('4', 'PLTU Captive (9.825 MW)',            'Global Energy Monitor'),
        ('5', 'Realisasi Investasi PMDN',           'Kement. Investasi/BKPM'),
        ('6', 'Deforestasi & Driver',               'Global Forest Watch'),
        ('7', 'Pelabuhan & Terminal Ekspor',        'KNKT · Perpres PSN'),
    ],
    col_widths_cm=[0.5, 4.3, 3.0])

h2(LC, '6', 'Bagan Alur Desain Penelitian')
fc_terminal(LC, 'MULAI')
fc_arrow(LC)

_BD = {'val': 'single', 'sz': '4', 'color': '333333', 'space': '0'}

def _phase_cell(c, lbl, ttl, sub):
    cell_shd(c, 'FFFFFF')
    cell_margin(c, left=60, right=60, top=40, bottom=40)
    set_cell_borders(c, top=_BD, left=_BD, bottom=_BD, right=_BD)
    p0 = c.paragraphs[0]
    for r in list(p0.runs): r._element.getparent().remove(r._element)
    p0.paragraph_format.space_before = Pt(0)
    p0.paragraph_format.space_after  = Pt(0)
    run(p0, lbl.upper(), bold=True, pt=5.5, color=G_MID)
    p2 = c.add_paragraph()
    p2.paragraph_format.space_before = Pt(1)
    p2.paragraph_format.space_after  = Pt(1)
    run(p2, ttl, bold=True, pt=7, color=RGBColor(0x1a, 0x1a, 0x1a))
    p3 = c.add_paragraph()
    p3.paragraph_format.space_before = Pt(0)
    p3.paragraph_format.space_after  = Pt(0)
    run(p3, sub, pt=6.5, color=RGBColor(0x44, 0x44, 0x44))

def _conn_cell(c, char=''):
    set_cell_borders(c)
    p0 = c.paragraphs[0]
    for r in list(p0.runs): r._element.getparent().remove(r._element)
    p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p0.paragraph_format.space_before = Pt(0)
    p0.paragraph_format.space_after  = Pt(0)
    if char:
        run(p0, char, bold=True, pt=9, color=G_MID)

ph_w = int(cw * 0.46)
cn_w = cw - ph_w * 2

snake = doc.add_table(rows=4, cols=3)
snake.autofit = False
for row_s in snake.rows:
    row_s.cells[0].width = ph_w
    row_s.cells[1].width = cn_w
    row_s.cells[2].width = ph_w

_phase_cell(snake.cell(0, 0), 'Fase I — Akuisisi',
    'Pengumpulan & Kurasi Data',
    'BPS · Minerbaone · BKPM · GEM · GFW  ·  6 provinsi · 2014–2024')
_conn_cell(snake.cell(0, 1), '→')
_phase_cell(snake.cell(0, 2), 'Fase II — Klasifikasi',
    'Reklasifikasi Rantai Pasok Hukum',
    'UU 3/2020 · PP 96/2021 · Perpres 112/2022 → 3 klaster makro')

_conn_cell(snake.cell(1, 0))
_conn_cell(snake.cell(1, 1))
_conn_cell(snake.cell(1, 2), '↓')

_phase_cell(snake.cell(2, 0), 'Fase IV — Sintesis',
    'Pemetaan Rantai Pasok Ekspor',
    'KNKT · Perpres PSN · Kurva Bézier · 6 simpul pelabuhan')
_conn_cell(snake.cell(2, 1), '←')
_phase_cell(snake.cell(2, 2), 'Fase III — Analisis',
    'Pengujian Statistik Inferensial',
    'Chi-Square · Odds Ratio · Panel N=60 · Ambang Median')

_conn_cell(snake.cell(3, 0), '↓')
_conn_cell(snake.cell(3, 1))
_conn_cell(snake.cell(3, 2))

doc.element.body.remove(snake._tbl)
LC._tc.append(snake._tbl)

fc_terminal(LC,
    'Dominasi Ekstraktif PDRB  ·  Konsentrasi Spasial Industri  ·  Risiko Deforestasi hingga 21× (Signifikan)',
    is_output=True)

# ── KOLOM KANAN ─────────────────────────────────────────────

h2(RC, '4', 'Kerangka Analisis')

h3(RC, '4.1  Reklasifikasi Rantai Pasok Hukum (PDRB)')
body(RC, [
    ('Tujuh belas sektor KBLI 2020 direklasifikasi menjadi tiga klaster berbasis mandat hukum: ', False, False),
    ('Ekstraktif', True, False),
    (' (pertambangan, smelter, listrik PLTU), ', False, False),
    ('Akar Rumput', True, False),
    (' (pertanian-perikanan), dan ', False, False),
    ('Jasa & Lainnya', True, False),
    ('. Hasil kunci: klaster ekstraktif menguasai 55,85% PDRB Sulawesi Tengah 2024, tumbuh 7,4× dalam satu dekade.', False, False),
])
formula(RC, 'Pangsa Ekstraktif (%) = ( PDRB Ekstraktif ÷ Total PDRB ) × 100')

h3(RC, '4.2  Dekomposisi Spasial Kabupaten')
body(RC, [
    ('Pemecahan PDRB ke level 13 kabupaten/kota membongkar ', False, False),
    ('bias ilusi agregat', False, True),
    (': sektor ekstraktif Morowali (Rp157,17 T) melampaui gabungan 8 kabupaten non-sentra, sementara pertanian rakyatnya tersisa 0,78%.', False, False),
])
formula(RC, 'Rasio Kesenjangan = Ekstraktif ÷ Pertanian Rakyat = 58,21× (Morowali)')

h3(RC, '4.3  Konsentrasi Kawasan Industri & PLTU Captive')
body(RC, [
    ('Analisis spasial deskriptif memetakan pemusatan ', False, False),
    ('778 smelter', True, False),
    (' dan ', False, False),
    ('9.825 MW PLTU captive batu bara off-grid', True, False),
    (' — 89,06% daya terkunci hanya di koridor Morowali–Konawe.', False, False),
])
formula(RC, 'Porsi Konsentrasi (%) = ( Kapasitas Sentra ÷ Total Sulawesi ) × 100')

h3(RC, '4.4  Tren Perizinan & Laju Alih Ruang')
body(RC, [
    ('Deret waktu ', False, False),
    ('574 IUP baru (819.452 Ha)', True, False),
    (' dianalisis dengan laju pertumbuhan tahunan — melonjak +246% pada 2022–2024 — lalu dikonversi menjadi laju alih fungsi ruang harian.', False, False),
])
formula(RC, 'Laju Alih Ruang = 819.452,54 Ha ÷ 3.650 Hari = 224,51 Ha/Hari')

h3(RC, '4.5  Tabulasi Silang & Uji Hipotesis')
body(RC, [
    ('Panel provinsi-tahun (N=60) dikategorikan Tinggi/Rendah pada ', False, False),
    ('ambang median', True, False),
    (', lalu diuji ', False, False),
    ('Chi-Square independensi', True, False),
    (' (α = 5%) dan ', False, False),
    ('odds ratio', True, False),
    (' untuk mengukur arah serta kelipatan risiko tekanan industri terhadap deforestasi.', False, False),
])
formula(RC, 'χ² = Jumlah( (Observasi − Harapan)² ÷ Harapan )   ·   OR = (a×d) ÷ (b×c)')
data_table(doc, RC,
    headers=['Skenario Uji (X → Y)', 'χ²', 'OR', 'Hasil'],
    rows=[
        ('PLTU Captive → Deforestasi',      '18,05', '18,0×', 'Signifikan'),
        ('IUP Baru → Deforestasi Alam',      '17,24', '13,8×', 'Signifikan'),
        ('IUP Baru → Def. Komoditas',        '21,82', '21,4×', 'Signifikan'),
        ('Luas Konsesi → Def. Komoditas',    '19,27', '16,0×', 'Signifikan'),
        ('PMDN → Def. Komoditas',            '2,08',  '2,8×',  'Tidak (time-lag)'),
    ],
    col_widths_cm=[3.6, 1.0, 1.0, 2.2])

h3(RC, '4.6  Pemetaan Rantai Pasok Logistik Ekspor')
body(RC, [
    ('Enam simpul pelabuhan ekspor nikel diverifikasi melalui triangulasi ', False, False),
    ('Laporan KNKT, regulasi PSN (Perpres 109/2020), dan laporan emiten', True, False),
    ('; alur pelayaran menuju Tiongkok–Jepang–Korea (>78% kargo) dimodelkan dengan kurva Bézier di permukaan bumi.', False, False),
])

h2(RC, '5', 'Korespondensi Sub-bab — Metode')
data_table(doc, RC,
    headers=['Sub-bab', 'Metode Utama'],
    rows=[
        ('1.1 Konteks Makro PDRB',      'Reklasifikasi hukum, pangsa sektor, laju pertumbuhan'),
        ('1.2 Kawasan Industri & PLTU', 'Analisis spasial, crosstab χ², odds ratio'),
        ('1.3 Tren Izin Tambang',       'Deret waktu, laju alih ruang, uji signifikansi'),
        ('1.4 Investasi PMDN',          'Konsentrasi modal, atribusi driver deforestasi'),
        ('1.5–1.6 Logistik Nikel', 'Triangulasi dokumen, kurva Bézier, pemetaan rute'),
    ],
    col_widths_cm=[2.9, 4.9])

note_box(RC, (
    'Seluruh prosedur statistik diterapkan pada data panel provinsi-tahun '
    '(N = 60; 6 provinsi × 10 tahun) kecuali dinyatakan lain. Angka empiris '
    'lengkap per indikator tersaji pada dokumen metodologi utuh Bab 1 (diolah CELIOS).'
))

# ── Simpan (dual save) ──────────────────────────────────────
out_dir_compact = Path(__file__).resolve().parent
out_dir_bab1    = out_dir_compact.parent.parent / "bab_1"

docx_compact = out_dir_compact / "Metodologi_Bab1_Ekspansi_Industri_Compact.docx"
docx_bab1    = out_dir_bab1 / "Metodologi_Bab1_Ekspansi_Industri_Compact.docx"
doc.save(str(docx_compact))
shutil.copyfile(docx_compact, docx_bab1)
print(f"[OK] DOCX: {docx_compact}")
print(f"[OK] Salinan: {docx_bab1}")

# ── Naskah Markdown padanan ─────────────────────────────────
MD = """# METODOLOGI PENELITIAN — BAB 1: EKSPANSI INDUSTRI EKSTRAKTIF DAN INFRASTRUKTUR PENUNJANG DI PULAU SULAWESI
*CELIOS — Center of Economic and Law Studies · Riset D3TLH Sulawesi · 2014–2024*

## 1. Desain Penelitian & Tujuan
Penelitian ini menggunakan **desain audit spasial-statistik kuantitatif** untuk membedah ekspansi industri ekstraktif (tambang, smelter, PLTU captive) di enam provinsi Pulau Sulawesi sepanjang **2014–2024** berbasis data resmi terbuka lintas kementerian/lembaga. Tiga tujuan utama: (1) **mengukur** dominasi sektor ekstraktif dalam struktur PDRB provinsi dan kabupaten; (2) **mengidentifikasi** konsentrasi spasial fasilitas smelter, PLTU captive, izin tambang, dan modal PMDN; serta (3) **menguji** keterkaitan statistik antara tekanan industri dan kehilangan tutupan hutan.

## 2. Sumber Data & Cakupan
Seluruh data bersumber dari institusi resmi — **BPS, Kementerian ESDM (MODI/Minerbaone), Kementerian Investasi/BKPM, Global Energy Monitor, Global Forest Watch (University of Maryland), dan KNKT** — diolah CELIOS. Cakupan: 6 provinsi se-Sulawesi, dekade 2014–2024, membentuk data panel provinsi-tahun (N = 60 observasi) untuk seluruh pengujian statistik.

## 3. Operasionalisasi Indikator
| # | Indikator | Institusi Sumber Resmi |
| :---: | :--- | :--- |
| 1 | PDRB Sektoral Provinsi & Kabupaten | BPS (Subject 52) |
| 2 | IUP Tambang Baru & Luas Konsesi | ESDM — Minerbaone |
| 3 | Smelter Nikel (778 unit) | ESDM & CGS |
| 4 | PLTU Captive (9.825 MW) | Global Energy Monitor |
| 5 | Realisasi Investasi PMDN | Kement. Investasi/BKPM |
| 6 | Deforestasi & Driver | Global Forest Watch |
| 7 | Pelabuhan & Terminal Ekspor | KNKT · Perpres PSN |

## 4. Kerangka Analisis

### 4.1 Reklasifikasi Rantai Pasok Hukum (PDRB)
Tujuh belas sektor KBLI 2020 direklasifikasi menjadi tiga klaster berbasis mandat hukum: **Ekstraktif** (pertambangan, smelter, listrik PLTU), **Akar Rumput** (pertanian-perikanan), dan **Jasa & Lainnya**. Hasil kunci: klaster ekstraktif menguasai 55,85% PDRB Sulawesi Tengah 2024, tumbuh 7,4× dalam satu dekade.

> `Pangsa Ekstraktif (%) = ( PDRB Ekstraktif ÷ Total PDRB ) × 100`

### 4.2 Dekomposisi Spasial Kabupaten
Pemecahan PDRB ke level 13 kabupaten/kota membongkar *bias ilusi agregat*: sektor ekstraktif Morowali (Rp157,17 T) melampaui gabungan 8 kabupaten non-sentra, sementara pertanian rakyatnya tersisa 0,78%.

> `Rasio Kesenjangan = Ekstraktif ÷ Pertanian Rakyat = 58,21× (Morowali)`

### 4.3 Konsentrasi Kawasan Industri & PLTU Captive
Analisis spasial deskriptif memetakan pemusatan **778 smelter** dan **9.825 MW PLTU captive batu bara off-grid** — 89,06% daya terkunci hanya di koridor Morowali–Konawe.

> `Porsi Konsentrasi (%) = ( Kapasitas Sentra ÷ Total Sulawesi ) × 100`

### 4.4 Tren Perizinan & Laju Alih Ruang
Deret waktu **574 IUP baru (819.452 Ha)** dianalisis dengan laju pertumbuhan tahunan — melonjak +246% pada 2022–2024 — lalu dikonversi menjadi laju alih fungsi ruang harian.

> `Laju Alih Ruang = 819.452,54 Ha ÷ 3.650 Hari = 224,51 Ha/Hari`

### 4.5 Tabulasi Silang & Uji Hipotesis
Panel provinsi-tahun (N=60) dikategorikan Tinggi/Rendah pada **ambang median**, lalu diuji **Chi-Square independensi** (α = 5%) dan **odds ratio** untuk mengukur arah serta kelipatan risiko tekanan industri terhadap deforestasi.

> `χ² = Jumlah( (Observasi − Harapan)² ÷ Harapan )   ·   OR = (a×d) ÷ (b×c)`

| Skenario Uji (X → Y) | χ² | OR | Hasil |
| :--- | :---: | :---: | :--- |
| PLTU Captive → Deforestasi | 18,05 | 18,0× | Signifikan |
| IUP Baru → Deforestasi Alam | 17,24 | 13,8× | Signifikan |
| IUP Baru → Def. Komoditas | 21,82 | 21,4× | Signifikan |
| Luas Konsesi → Def. Komoditas | 19,27 | 16,0× | Signifikan |
| PMDN → Def. Komoditas | 2,08 | 2,8× | Tidak (time-lag) |

### 4.6 Pemetaan Rantai Pasok Logistik Ekspor
Enam simpul pelabuhan ekspor nikel diverifikasi melalui triangulasi **Laporan KNKT, regulasi PSN (Perpres 109/2020), dan laporan emiten**; alur pelayaran menuju Tiongkok–Jepang–Korea (>78% kargo) dimodelkan dengan kurva Bézier di permukaan bumi.

## 5. Korespondensi Sub-bab — Metode
| Sub-bab | Metode Utama |
| :--- | :--- |
| 1.1 Konteks Makro PDRB | Reklasifikasi hukum, pangsa sektor, laju pertumbuhan |
| 1.2 Kawasan Industri & PLTU | Analisis spasial, crosstab χ², odds ratio |
| 1.3 Tren Izin Tambang | Deret waktu, laju alih ruang, uji signifikansi |
| 1.4 Investasi PMDN | Konsentrasi modal, atribusi driver deforestasi |
| 1.5–1.6 Logistik Nikel | Triangulasi dokumen, kurva Bézier, pemetaan rute |

## 6. Bagan Alur Desain Penelitian
MULAI → **Fase I — Akuisisi** (BPS · Minerbaone · BKPM · GEM · GFW; 6 provinsi, 2014–2024) → **Fase II — Klasifikasi** (UU 3/2020 · PP 96/2021 · Perpres 112/2022 → 3 klaster makro) → **Fase III — Analisis** (Chi-Square · Odds Ratio · Panel N=60 · Ambang Median) → **Fase IV — Sintesis** (KNKT · Perpres PSN · Kurva Bézier · 6 simpul pelabuhan) → **KELUARAN: Dominasi Ekstraktif PDRB · Konsentrasi Spasial Industri · Risiko Deforestasi hingga 21× (Signifikan)**

> *Seluruh prosedur statistik diterapkan pada data panel provinsi-tahun (N = 60; 6 provinsi × 10 tahun) kecuali dinyatakan lain. Angka empiris lengkap per indikator tersaji pada dokumen metodologi utuh Bab 1 (diolah CELIOS).*
"""

md_compact = out_dir_compact / "Metodologi_Bab1_Ekspansi_Industri_Compact.md"
md_bab1    = out_dir_bab1 / "Metodologi_Bab1_Ekspansi_Industri_Compact.md"
for pth in [md_compact, md_bab1]:
    with open(pth, "w", encoding="utf-8") as f:
        f.write(MD)
print(f"[OK] MD: {md_compact}")
print(f"[OK] Salinan: {md_bab1}")
