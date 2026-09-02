# ==============================================================================
# BAB 6 SUB-BAB 6.6: GENERATOR METODOLOGI SKORING D3TLH TINGKAT PROVINSI
# DOKUMEN SATUAN (KOMPILASI SELURUH PROVINSI SULAWESI BERTAHAP)
# PROVINSI CAKUPAN:
#   6.6.1: SULAWESI TENGAH (SULTENG)
#   6.6.2: SULAWESI TENGGARA (SULTRA)
# METODE: HYBRID Z-SCORE ANOMALI STANDAR DEVIASI + ENTROPY WEIGHT METHOD (EWM)
# SINKRONISASI: 100% PERSIS TAB 3 STREAMLIT PAGE 6 (pages/6_Audit_D3TLH.py)
# ==============================================================================

import sys
import os
import urllib.request
import base64
from pathlib import Path

# Setup paths
current_file = Path(__file__).resolve()
project_root = current_file.parents[3]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import numpy as np
import pandas as pd
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

import tools.algo_skoring_provinsi_ZscoreEWM.kalkulasi_provinsi_sulawesi as algo_prov_mod

# -----------------------------------------------------------------------------
# PALET WARNA RESMI CELIOS (SOP KORPORAT & LAPORAN AKADEMIK)
# -----------------------------------------------------------------------------
C_NAVY = RGBColor(0x14, 0x36, 0x42)
C_DARK = RGBColor(0x20, 0x24, 0x26)
C_RED = RGBColor(0xA8, 0x20, 0x1A)
C_TEAL = RGBColor(0x0F, 0x4C, 0x5C)
C_AMBER = RGBColor(0xE3, 0x64, 0x14)
C_MUTED = RGBColor(0x55, 0x55, 0x55)
C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)

C_HEX_PRIMARY = "143642"
C_HEX_LIGHT_BG = "F4F5F6"
C_HEX_RED = "A8201A"

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex):
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shd)

def set_table_borders(table, border_color="D3D3D3"):
    tblPr = table._tbl.tblPr
    tblBorders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="6" w:space="0" w:color="{border_color}"/>'
        f'  <w:bottom w:val="single" w:sz="8" w:space="0" w:color="{C_HEX_PRIMARY}"/>'
        f'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>'
        f'  <w:insideV w:val="none"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(tblBorders)

def add_h1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(14)
    r.font.color.rgb = C_NAVY
    return p

def add_h2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = C_RED
    return p

def add_h3(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(11)
    r.font.color.rgb = C_TEAL
    return p

def add_h4(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(9.5)
    r.font.color.rgb = C_NAVY
    return p

def add_p(doc, runs, space_after=5):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    for text, bold, italic in runs:
        r = p.add_run(text)
        r.bold = bold
        r.italic = italic
        r.font.size = Pt(9.0)
        r.font.color.rgb = C_DARK
    return p

def add_caption(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.bold = True
    r.italic = True
    r.font.size = Pt(8.5)
    r.font.color.rgb = C_NAVY
    return p

def add_note_box(doc, title, body):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = tbl.cell(0, 0)
    c.width = Cm(17.0)
    set_cell_shading(c, C_HEX_LIGHT_BG)
    set_cell_margins(c, top=120, bottom=120, left=160, right=160)
    tcPr = c._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'  <w:left w:val="single" w:sz="24" w:space="0" w:color="{C_HEX_PRIMARY}"/>'
        f'  <w:top w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'  <w:bottom w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    p = c.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    r_t = p.add_run(f"PROFIL BIOREGION: {title}\n")
    r_t.bold = True
    r_t.font.size = Pt(8.5)
    r_t.font.color.rgb = C_NAVY
    r_b = p.add_run(body)
    r_b.font.size = Pt(8.0)
    r_b.font.color.rgb = C_DARK
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(4)

def add_formula_box(doc, title, formula_text, variable_tuples):
    p_t = doc.add_paragraph()
    p_t.paragraph_format.space_before = Pt(5)
    p_t.paragraph_format.space_after = Pt(2)
    p_t.paragraph_format.keep_with_next = True
    r_t = p_t.add_run(f"• {title}")
    r_t.bold = True
    r_t.font.size = Pt(9.0)
    r_t.font.color.rgb = C_TEAL

    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = tbl.cell(0, 0)
    c.width = Cm(17.0)
    set_cell_shading(c, "F8F9FA")
    set_cell_margins(c, top=80, bottom=80, left=120, right=120)
    tcPr = c._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'  <w:left w:val="single" w:sz="16" w:space="0" w:color="{C_HEX_PRIMARY}"/>'
        f'  <w:top w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'  <w:bottom w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    p = c.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(formula_text)
    r.font.name = "Consolas"
    r.font.size = Pt(8.5)
    r.bold = True
    r.font.color.rgb = C_NAVY

    if variable_tuples:
        p_v = doc.add_paragraph()
        p_v.paragraph_format.space_before = Pt(2)
        p_v.paragraph_format.space_after = Pt(5)
        p_v.paragraph_format.left_indent = Cm(0.5)
        p_v.paragraph_format.line_spacing = 1.1
        for var_name, var_desc in variable_tuples:
            r1 = p_v.add_run(f"  - {var_name}: ")
            r1.bold = True
            r1.font.size = Pt(8.0)
            r1.font.color.rgb = C_DARK
            r2 = p_v.add_run(f"{var_desc}\n")
            r2.font.size = Pt(8.0)
            r2.font.color.rgb = C_MUTED

def add_table_styled(doc, headers, rows, col_widths, col_alignments):
    tbl = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl)

    hdr_cells = tbl.rows[0].cells
    for i, h_text in enumerate(headers):
        cell = hdr_cells[i]
        cell.width = Cm(col_widths[i])
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        set_cell_shading(cell, C_HEX_PRIMARY)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.bold = True
        r.font.size = Pt(8.0)
        r.font.color.rgb = C_WHITE

    trPr = tbl.rows[0]._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

    for r_idx, row_data in enumerate(rows):
        row_cells = tbl.rows[r_idx + 1].cells
        bg = C_HEX_LIGHT_BG if r_idx % 2 == 1 else "FFFFFF"
        is_total = (str(row_data[0]).strip().upper() == "TOTAL" or "SKOR KOMPOSIT" in str(row_data[0]).upper())
        if is_total:
            bg = "E6ECF0"

        for c_idx, val in enumerate(row_data):
            cell = row_cells[c_idx]
            cell.width = Cm(col_widths[c_idx])
            set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
            set_cell_shading(cell, bg)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            align = col_alignments[c_idx]
            if align == "C":
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif align == "R":
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT

            r = p.add_run(str(val))
            r.font.size = Pt(7.5 if len(headers) > 6 else 8.0)
            r.font.color.rgb = C_DARK
            if is_total:
                r.bold = True

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(6)

def download_mermaid_png(mermaid_str, output_path):
    try:
        b64 = base64.b64encode(mermaid_str.encode('utf-8')).decode('ascii')
        url = f"https://mermaid.ink/img/{b64}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=12) as resp, open(output_path, 'wb') as f:
            f.write(resp.read())
        return True
    except Exception as e:
        print(f"[WARN] Gagal download Mermaid: {e}")
        return False

def get_likert_label(skor_likert):
    val = round(float(skor_likert))
    if val >= 4:
        return "Melampaui Batas"
    elif val == 3:
        return "Mendekati Batas"
    else:
        return "Tidak Melampaui Batas"

def html_table(headers, rows):
    out = ['<div class="table-container"><table>']
    out.append('<thead><tr>')
    for h in headers:
        out.append(f'<th class="data-th">{h}</th>')
    out.append('</tr></thead><tbody>')
    for r in rows:
        is_total = (str(r[0]).strip().upper() == "TOTAL" or "SKOR KOMPOSIT" in str(r[0]).upper())
        row_cls = ' class="total-row"' if is_total else ''
        out.append(f'<tr{row_cls}>')
        for idx, val in enumerate(r):
            align_cls = 'text-center' if idx in [0, 5, 6, 7, 8] else ('text-right' if idx in [2, 3, 4] else 'text-left')
            val_str = str(val)
            if "Melampaui Batas" in val_str:
                val_str = f'<span class="badge-danger">{val_str}</span>'
            elif "Mendekati Batas" in val_str:
                val_str = f'<span class="badge-warning">{val_str}</span>'
            elif "Tidak Melampaui Batas" in val_str:
                val_str = f'<span class="badge-success">{val_str}</span>'
            out.append(f'<td class="{align_cls}">{val_str}</td>')
        out.append('</tr>')
    out.append('</tbody></table></div>')
    return "\n".join(out)

def markdown_table(headers, rows):
    lines = []
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join([":---" if i in [1, 8] else ":---:" for i in range(len(headers))]) + " |")
    for r in rows:
        lines.append("| " + " | ".join([str(x) for x in r]) + " |")
    return "\n".join(lines)


# =============================================================================
# EXTRACT DATA PROVINSI (HELPER MODULAR)
# =============================================================================
INDICATOR_META = {
    'pltu_mw': ('Pilar Udara', 'Kapasitas PLTU Captive Beroperasi', 'MW'),
    'no2': ('Pilar Udara', 'Konsentrasi Gas NO2 Troposferik Satelit', 'mol/m²'),
    'ispa_irr': ('Pilar Udara', 'Morbiditas ISPA (Incidence Rate Ratio)', 'x lipat'),
    'b3_ton': ('Pilar Udara', 'Proporsi Timbulan Limbah B3 Industri', 'Jt Ton'),
    'co2_mton': ('Pilar Udara', 'Pelepasan Emisi Karbon Deforestasi GFW', 'Jt Ton CO2e'),
    'ika': ('Pilar Air', 'Indeks Kualitas Air (IKA) Terkini', 'Poin'),
    'diare_irr': ('Pilar Air', 'Morbiditas Diare (Incidence Rate Ratio)', 'x lipat'),
    'konflik_pesisir': ('Pilar Air', 'Konflik Ruang Laut Nelayan vs Tambang', 'Kasus'),
    'tailing_ton': ('Pilar Air', 'Akumulasi Beban Tailing, Slag & DSTP', 'Jt Ton'),
    'bencana': ('Pilar Lahan', 'Bencana Hidrometeorologi (Banjir & Longsor)', 'Kejadian'),
    'deforestasi_ha': ('Pilar Lahan', 'Deforestasi Hutan Alam Primer GFW', 'Ha'),
    'lindung_ha': ('Pilar Lahan', 'Perambahan Tambang di Kawasan Hutan Lindung', 'Ha'),
    'driver_ha': ('Pilar Lahan', 'Aktor Deforestasi Komoditas Tambang & Sawit', 'Ha'),
    'kepadatan_iup': ('Pilar Lahan', 'Kepadatan Konsesi IUP Nikel vs Daratan', '% Daratan'),
    'fpic': ('Pilar Sosial', 'Manipulasi Persetujuan Konsultasi Warga (FPIC)', 'Kasus'),
    'jiwa_terdampak': ('Pilar Sosial', 'Korban Perampasan Ruang Hidup & Krisis Agraria', 'Jiwa'),
    'kriminalisasi': ('Pilar Sosial', 'Insiden Kriminalisasi Warga & Pembela HAM', 'Insiden'),
    'gap_spa': ('Pilar Sosial', 'Defisit Kelayakan Standar Faskes SPA', '% Gap'),
    'izin_baru': ('Pilar Veto', 'Penerbitan Obral Konsesi WIUP Baru Pasca-2014', 'Izin'),
    'ilegal': ('Pilar Veto', 'Korporat Tambang Pelanggar Hukum Beroperasi Ilegal', 'Korporasi')
}

def extract_prov_table_rows(prov_data):
    math_details = prov_data['math_details']
    raw_absolut = prov_data['raw_absolut']
    raw_zscores = prov_data['raw_zscores']
    likert_dict = math_details['likert']
    ewm_weights = math_details['ewm_weights']
    means = math_details['mean']
    stds = math_details['std']

    table_rows = []
    for col, (pilar, nama_ind, satuan) in INDICATOR_META.items():
        val_a = raw_absolut.get(col, 0.0)
        val_b = means.get(col, 0.0)
        val_c = stds.get(col, 1.0)
        z_val = raw_zscores.get(col, 0.0)
        w_val = ewm_weights.get(col, 0.0)
        l_val = likert_dict.get(col, 0.0)
        label_ekologis = get_likert_label(l_val)

        if col == 'no2':
            str_a = f"{val_a:.2e}"
            str_b = f"{val_b:.2e}"
            str_c = f"{val_c:.2e}"
        elif col in ['pltu_mw', 'deforestasi_ha', 'lindung_ha', 'driver_ha', 'jiwa_terdampak']:
            str_a = f"{val_a:,.0f} {satuan}"
            str_b = f"{val_b:,.0f}"
            str_c = f"{val_c:,.0f}"
        elif col in ['b3_ton', 'co2_mton', 'tailing_ton']:
            str_a = f"{val_a:,.2f} {satuan}"
            str_b = f"{val_b:,.2f}"
            str_c = f"{val_c:,.2f}"
        elif col == 'kepadatan_iup':
            str_a = f"{val_a*100:.2f}%"
            str_b = f"{val_b*100:.2f}%"
            str_c = f"{val_c*100:.2f}%"
        elif col in ['ispa_irr', 'diare_irr']:
            str_a = f"{val_a:.2f}x"
            str_b = f"{val_b:.2f}x"
            str_c = f"{val_c:.2f}x"
        else:
            str_a = f"{val_a:,.1f} {satuan}" if isinstance(val_a, float) else f"{val_a} {satuan}"
            str_b = f"{val_b:,.1f}"
            str_c = f"{val_c:,.1f}"

        table_rows.append([
            pilar,
            nama_ind,
            str_a,
            str_b,
            str_c,
            f"{z_val:+.2f}",
            f"{w_val:.4f}",
            f"{l_val:.1f} / 5",
            label_ekologis
        ])
    return table_rows


# =============================================================================
# EKSEKUTOR UTAMA PEMBANGUN DOKUMEN SATUAN TINGKAT PROVINSI
# =============================================================================
def generate_bab6_skoring_provinsi():
    print("[1/4] Mengekstraksi dataset empiris seluruh provinsi (Model Z-Score EWM)...")
    tool_dir = Path(__file__).parent
    
    # Engine resmi
    all_prov_results = algo_prov_mod.kalkulasi_skor_provinsi_sulawesi()
    sulteng = all_prov_results['Sulawesi Tengah']
    sultra = all_prov_results['Sulawesi Tenggara']

    table_math_sulteng = extract_prov_table_rows(sulteng)
    table_math_sultra = extract_prov_table_rows(sultra)

    # Rekapitulasi 5 Pilar Sulteng
    rekap_sulteng = [
        ["Pilar 1: Udara", "PLTU (7.325 MW), NO2 (6.5e-6), ISPA (3.5x), B3 (25.3 Jt Ton), CO2 (291 Jt Ton)", f"{sulteng['udara']:.1f} / 5", get_likert_label(sulteng['udara']), "Episentrum PLTU Captive Terbesar & Konsentrasi B3"],
        ["Pilar 2: Air", "IKA (62.07), Diare (1.52x), Tailing (24.5 Jt Ton), Logam Cr6+", f"{sulteng['air']:.1f} / 5", get_likert_label(sulteng['air']), "Beban Tailing Raksasa & Morbiditas Pencernaan Tinggi"],
        ["Pilar 3: Lahan", "Bencana (458), Deforestasi (481k Ha), Lindung (19.8k Ha), Driver (383k Ha)", f"{sulteng['lahan']:.1f} / 5", get_likert_label(sulteng['lahan']), "Deforestasi Primer Masif & Perambahan Hutan Lindung"],
        ["Pilar 4: Sosial", "FPIC (1 Kasus), Korban (12.231 Jiwa), Kriminalisasi (6 Insiden), Defisit SPA", f"{sulteng['sosial']:.1f} / 5", get_likert_label(sulteng['sosial']), "Kriminalisasi Warga Pembela HAM & Defisit Sarana Kesehatan"],
        ["Pilar 5: Veto", "Obral Izin (260 IUP Baru), Korporat Ilegal (3 Perusahaan), PLTU Ekspansi", f"{sulteng['veto']:.1f} / 5", get_likert_label(sulteng['veto']), "Kegagalan Pengendalian Izin & Impunitas Pelanggaran"],
        ["SKOR KOMPOSIT SULTENG", "Agregasi 5 Pilar EWM Weighted Average (Z-Score Standardization)", f"{sulteng['total_likert']:.1f} / 5", sulteng['likert_label'], "STATUS RED ALERT: DARURAT DAYA DUKUNG LINGKUNGAN"]
    ]

    # Rekapitulasi 5 Pilar Sultra
    rekap_sultra = [
        ["Pilar 1: Udara", "PLTU (1.900 MW), NO2 (6.6e-6), ISPA (0.91x), B3 (6.5 Jt Ton), CO2 (189 Jt Ton)", f"{sultra['udara']:.1f} / 5", get_likert_label(sultra['udara']), "Emisi Smelter Morosi/VDNI & Peningkatan NO2 Satelit"],
        ["Pilar 2: Air", "IKA (65.32), Diare (1.11x), Tailing (6.5 Jt Ton), Konflik Pesisir (5 Kasus)", f"{sultra['air']:.1f} / 5", get_likert_label(sultra['air']), "Sedimentasi Tailing Pesisir & Konflik Ruang Tangkap Nelayan"],
        ["Pilar 3: Lahan", "Bencana (158), Deforestasi (337k Ha), Lindung (8.2k Ha), Kepadatan IUP (11.72%)", f"{sultra['lahan']:.1f} / 5", get_likert_label(sultra['lahan']), "Outlier Kepadatan Konsesi Tambang Nikel Terpadat Se-Sulawesi"],
        ["Pilar 4: Sosial", "FPIC (5 Kasus), Korban (39.821 Jiwa), Kriminalisasi (4 Insiden), Gap SPA (17.9%)", f"{sultra['sosial']:.1f} / 5", get_likert_label(sultra['sosial']), "Krisis Kemanusiaan & Perampasan Ruang Hidup Terparah Se-Sulawesi"],
        ["Pilar 5: Veto", "Obral Izin (160 IUP Baru), Korporat Ilegal (1 Perusahaan), Ekspansi Smelter", f"{sultra['veto']:.1f} / 5", get_likert_label(sultra['veto']), "Obral Izin Tambang Nikel Baru Pasca-2014 di Pesisir & Pulau"],
        ["SKOR KOMPOSIT SULTRA", "Agregasi 5 Pilar EWM Weighted Average (Z-Score Standardization)", f"{sultra['total_likert']:.1f} / 5", sultra['likert_label'], "STATUS AMBANG BATAS: KRISIS RUANG HIDUP & KEPADATAN IUP"]
    ]

    # Flowchart Mermaid LR Sulteng & Sultra
    mermaid_sulteng = """flowchart LR
    subgraph S1["1. Data Empiris Input"]
        A1["20 Indikator Empiris<br/><i>6 Provinsi Se-Sulawesi</i>"]
        A2["Fokus Data Sulteng<br/><i>Episentrum Nikel & PLTU</i>"]
    end
    subgraph S2["2. Standardisasi & Pembobotan"]
        B1["Z-Score Deviasi Standar<br/><i>Z = (x - mean) / std</i>"]
        B2["Inversi Parameter IKA<br/><i>Z_ika = -Z_ika</i>"]
        B3["Entropy Weight Method (EWM)<br/><i>Bobot Objektif Dispersi W_j</i>"]
    end
    subgraph S3["3. Transformasi & Agregasi"]
        C1["Mapping Likert Diskret (0-5)<br/><i>Threshold Outlier >= +1.0σ</i>"]
        C2["EWM Weighted Average<br/><i>5 Pilar: Udara, Air, Lahan, Sosial, Veto</i>"]
    end
    subgraph S4["4. Sintesis & Vonis Sulteng"]
        D1["Skor Komposit: 4.0 / 5.0<br/><i>(WSM: 7.92 / 10.0)</i>"]
        D2["STATUS: MELAMPAUI BATAS<br/><i>Darurat Ekologis Provinsi</i>"]
    end
    A1 & A2 --> B1 & B3
    B1 --> B2 --> C1
    B3 & C1 --> C2 --> D1 --> D2"""

    mermaid_sultra = """flowchart LR
    subgraph S1["1. Data Empiris Input"]
        A1["20 Indikator Empiris<br/><i>6 Provinsi Se-Sulawesi</i>"]
        A2["Fokus Data Sultra<br/><i>Episentrum Konflik Agraria & IUP</i>"]
    end
    subgraph S2["2. Standardisasi & Pembobotan"]
        B1["Z-Score Deviasi Standar<br/><i>Z = (x - mean) / std</i>"]
        B2["Inversi Parameter IKA<br/><i>Z_ika = -Z_ika</i>"]
        B3["Entropy Weight Method (EWM)<br/><i>Bobot Objektif Dispersi W_j</i>"]
    end
    subgraph S3["3. Transformasi & Agregasi"]
        C1["Mapping Likert Diskret (0-5)<br/><i>Kepadatan IUP (+1.50σ) & Sosial (+1.95σ)</i>"]
        C2["EWM Weighted Average<br/><i>5 Pilar: Udara, Air, Lahan, Sosial, Veto</i>"]
    end
    subgraph S4["4. Sintesis & Vonis Sultra"]
        D1["Skor Komposit: 3.4 / 5.0<br/><i>(WSM: 6.78 / 10.0)</i>"]
        D2["STATUS: MENDEKATI BATAS<br/><i>Krisis Sosial & Kepadatan Tambang Kritis</i>"]
    end
    A1 & A2 --> B1 & B3
    B1 --> B2 --> C1
    B3 & C1 --> C2 --> D1 --> D2"""

    png_sulteng = str(tool_dir / "mermaid_flowchart_6_6_sulteng.png")
    png_sultra = str(tool_dir / "mermaid_flowchart_6_6_sultra.png")
    dl_sulteng = download_mermaid_png(mermaid_sulteng, png_sulteng)
    dl_sultra = download_mermaid_png(mermaid_sultra, png_sultra)

    # =========================================================================
    # [2/4] MEMBANGUN DOKUMEN WORD SATUAN (DOCX)
    # =========================================================================
    print("[2/4] Membangun DOCX Metodologi_Bab6_Skoring_Provinsi.docx...")
    doc = Document()
    sec = doc.sections[0]
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.left_margin = Cm(2.0)
    sec.right_margin = Cm(2.0)
    sec.top_margin = Cm(2.0)
    sec.bottom_margin = Cm(2.0)
    doc.styles["Normal"].font.name = "Calibri"
    doc.styles["Normal"].font.size = Pt(9.5)

    p_hdr = doc.add_paragraph()
    p_hdr.paragraph_format.space_before = Pt(0)
    p_hdr.paragraph_format.space_after = Pt(2)
    run_hdr = p_hdr.add_run("CELIOS - CENTER OF ECONOMIC AND LAW STUDIES  |  LAPORAN RISET METODOLOGI D3TLH TINGKAT PROVINSI")
    run_hdr.bold = True
    run_hdr.font.size = Pt(8.0)
    run_hdr.font.color.rgb = C_RED

    add_h1(doc, "BAB VI: AUDIT FORENSIK METODOLOGI D3TLH")
    add_h2(doc, "SUB-BAB 6.6: ALGORITMA SKORING TINGKAT PROVINSI (MODEL HYBRID Z-SCORE & EWM)")

    # -------------------------------------------------------------------------
    # SEKSI 6.6.1: SULAWESI TENGAH
    # -------------------------------------------------------------------------
    add_h3(doc, "6.6.1 Evaluasi Forensik D3TLH: Provinsi Sulawesi Tengah (Sulteng)")
    add_note_box(
        doc,
        "Provinsi Sulawesi Tengah (Episentrum Hilirisasi & PLTU Captive)",
        "Data empiris: Gabungan sensor satelit NASA TROPOMI NO2, Global Energy Monitor (GEM 2023), Rekam Medis Kemenkes (ISPA & Diare), Laporan Kinerja KLHK (Limbah B3 & Tailing), Global Forest Watch (Deforestasi & Emisi Karbon), BNPB (Bencana Alam), KPA & TanahKita (Konflik Agraria & Kriminalisasi), serta Minerba ESDM (IUP Nikel & Obral Izin). "
        "Diolah menggunakan model hybrid Z-Score Anomali Deviasi Standar dan Entropy Weight Method (EWM) sesuai antarmuka Dashboard Streamlit Tab 3 (Bedah Matematika Z-Score + EWM per Provinsi)."
    )

    add_h4(doc, "A. Pengantar & Kerangka Narasi")
    add_p(doc, [
        ("Sebagaimana ditampilkan pada antarmuka Streamlit ", False, False),
        ("Dashboard Page 6 (Audit D3TLH - Tab Bedah Matematika Z-Score + EWM per Provinsi)", True, False),
        (", evaluasi daya dukung dan daya tampung lingkungan hidup tingkat provinsi dirancang untuk membongkar kelemahan metodologi pemerintah yang kerap mengaburkan krisis lokal melalui teknik perataan wilayah (dilution effect). "
         "AMDAL dan dokumen D3TLH resmi selama ini berasumsi bahwa kapasitas asimilasi lingkungan bersifat homogen di seluruh daratan. Namun, fakta empiris membuktikan disparitas ekstrem antara provinsi episentrum industri nikel dengan wilayah sekitarnya.", False, False)
    ])
    add_p(doc, [
        ("Di sini pembaca dapat melihat persis bagaimana angka ", False, False),
        ("Fakta Lapangan (Raw Absolute Data)", True, False),
        (" ditransformasikan secara objektif oleh fungsi komputasi matematika ", False, False),
        ("(Z-Score Anomali dan Pembobotan Entropi EWM Shannon)", True, False),
        (" menjadi Skor Likert diskret 0.0 - 5.0. Analisis forensik membuktikan bahwa ", False, False),
        ("Provinsi Sulawesi Tengah berada pada status RED ALERT (Skor Komposit 4.0 / 5.0 - Melampaui Batas)", True, False),
        (", di mana beban pencemaran udara, akumulasi limbah B3, beban tailing, dan deforestasi primer telah melampaui batas toleransi daya lentur ekologis.", False, False)
    ])

    add_h4(doc, "B. Alur Logika Metodologis Skoring Tingkat Provinsi (Flowchart Sulteng)")
    add_caption(doc, "Bagan Alur 6.6a: Alur Logika Pemrosesan Algoritma Skoring Provinsi Sulawesi Tengah")
    if dl_sulteng:
        try:
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.add_run().add_picture(png_sulteng, width=Cm(15.0))
        except Exception as exc:
            print(f"[WARN] Gagal pasang gambar Sulteng: {exc}")

    add_h4(doc, "C. Formulasi Matematis & Definisi Variabel")
    add_formula_box(
        doc,
        "Tahap 1: Standardisasi Deviasi Z-Score Regional (Anomali Spasial)",
        "Z_ij = (x_ij - mean(x_j)) / std(x_j)    ;    Khusus IKA: Z_ika = - (ika_i - mean(ika)) / std(ika)",
        [
            ("x_ij", "Nilai empiris absolut provinsi i pada indikator j."),
            ("mean(x_j)", "Rata-rata aritmatika indikator j dari seluruh 6 provinsi di Pulau Sulawesi."),
            ("std(x_j)", "Standar deviasi sampel indikator j se-Sulawesi (substitusi 1.0 jika bernilai 0)."),
            ("Inversi IKA", "Indeks Kualitas Air diinversi tandanya karena nilai IKA tinggi mencerminkan kualitas air baik.")
        ]
    )
    add_formula_box(
        doc,
        "Tahap 2: Pembobotan Objektif Entropi Informasi (Entropy Weight Method - EWM)",
        "r_ij = (x_ij - min(x_j)) / (max(x_j) - min(x_j))  -->  P_ij = r_ij / SUM(r_ij)\n"
        "E_j = - (1 / ln(n)) * SUM(P_ij * ln(P_ij + eps))  -->  D_j = 1 - E_j  -->  W_j = D_j / SUM(D_j)",
        [
            ("r_ij", "Matriks ternormalisasi skala Min-Max [0, 1] per kolom indikator."),
            ("P_ij", "Proporsi probabilitas kontribusi provinsi i terhadap total nilai indikator j."),
            ("E_j", "Nilai entropi informasi Shannon indikator j (konstanta k = 1 / ln(6) = 0.5581)."),
            ("W_j", "Bobot objektif final EWM. Indikator dengan disparitas paling timpang otomatis berbobot tertinggi.")
        ]
    )
    add_formula_box(
        doc,
        "Tahap 3, 4 & 5: Mapping Likert Diskret & Agregasi Skor Komposit",
        "L_ij = 5.0 (Z >= +1.0) ; 4.0 (0.5 <= Z < 1.0) ; 3.0 (0.0 <= Z < 0.5) ; 2.0 (-0.5 <= Z < 0.0) ; 1.0 (-1.0 <= Z < -0.5) ; 0.0 (Z < -1.0)\n"
        "Skor_Pilar = SUM(L_ij * W_j) / SUM(W_j)    ;    Skor_Komposit = (Udara + Air + Lahan + Sosial + Veto) / 5.0",
        [
            ("Skor 5.0 (Z >= +1.0σ)", "Outlier Kritis Ekstrem / Red Alert (Beban melampaui rata-rata regional > 1 SD)."),
            ("Vonis Status", "Melampaui Batas (Skor >= 4.0), Mendekati Batas (Skor = 3.0), Tidak Melampaui Batas (Skor < 3.0).")
        ]
    )

    add_h4(doc, "D. Matriks Hasil Uji Empiris (Sulteng)")
    add_caption(doc, "Tabel 6.12: Bedah Matematika 20 Indikator Empiris Provinsi Sulawesi Tengah (Model Hybrid Z-Score & EWM)")
    add_table_styled(
        doc,
        ["Pilar", "Indikator Empiris", "Fakta Mentah (A)", "Rata-rata (B)", "Deviasi (C)", "Z-Score", "Bobot EWM", "Likert", "Status Ekologis"],
        table_math_sulteng,
        [1.5, 3.2, 2.0, 1.8, 1.7, 1.5, 1.5, 1.6, 2.2],
        ["C", "L", "R", "R", "R", "C", "C", "C", "C"]
    )
    add_caption(doc, "Tabel 6.13: Rekapitulasi Skor 5 Pilar & Status Ekologis Komposit Provinsi Sulawesi Tengah")
    add_table_styled(
        doc,
        ["Pilar / Dimensi", "Cakupan Indikator Kunci", "Skor Likert Pilar (0-5)", "Status Ekologis", "Interpretasi Temuan Lapangan Sulteng"],
        rekap_sulteng,
        [2.5, 4.5, 2.2, 2.8, 5.0],
        ["C", "L", "C", "C", "L"]
    )

    add_h4(doc, "E. Analisis Temuan Empiris (Sulteng)")
    add_p(doc, [
        ("1. ", True, False), ("Daya Tampung Udara (Skor 4.9 / 5 — Melampaui Batas): ", True, False),
        (f"Sulawesi Tengah memikul beban polusi udara terparah se-Sulawesi. Kapasitas PLTU captive batubara mencapai 7.325,0 MW (Z = +1.97σ), timbulan limbah B3 menyentuh 25,30 Juta Ton (Z = +1.97σ), emisi karbon 291,34 Juta Ton CO2e (Z = +1.67σ), dan rasio anomali ISPA mencapai 3,50x lipat (Z = +1.66σ).\n", False, False),
        ("2. ", True, False), ("Daya Tampung Air (Skor 3.3 / 5 — Mendekati Batas): ", True, False),
        (f"Meskipun rerata IKA bernilai 62,07, timbulan tailing dan slag mencapai 24,50 Juta Ton/Tahun (Z = +1.97σ) serta memicu lonjakan morbiditas diare sebesar 1,52x lipat dibanding kontrol (Z = +1.34σ, Likert 5.0).\n", False, False),
        ("3. ", True, False), ("Daya Dukung Lahan (Skor 4.7 / 5 — Melampaui Batas): ", True, False),
        (f"Kehancuran tutupan daratan terberat dengan total deforestasi primer 481.908 Ha (Z = +1.57σ), perambahan 19.804 Ha di kawasan hutan lindung (Z = +1.89σ), serta 383.304 Ha deforestasi komoditas tambang/sawit (Z = +1.69σ).\n", False, False),
        ("4. ", True, False), ("Daya Dukung Sosial (Skor 2.5 / 5 — Tidak Melampaui Batas): ", True, False),
        (f"Tercatat 12.231 jiwa masyarakat adat dan petani terancam kehilangan ruang hidup, serta terjadi 6 insiden kriminalisasi warga dan aktivis lingkungan hidup (Z = +0.71σ, Likert 4.0).\n", False, False),
        ("5. ", True, False), ("Veto Kebijakan (Skor 4.4 / 5 — Melampaui Batas): ", True, False),
        (f"Terjadi kegagalan pengendalian perizinan dengan diterbitkannya 260 IUP baru pasca-2014 (Z = +1.64σ, Likert 5.0) dan pembiaran 3 korporasi besar beroperasi ilegal di kawasan hutan.\n", False, False),
        ("6. ", True, False), ("Vonis Komposit Sulawesi Tengah (Skor 4.0 / 5.0 — Melampaui Batas): ", True, False),
        (f"Secara agregat, Sulawesi Tengah memperoleh Skor Komposit 4.0 / 5.0 (Ekuivalen WSM 7.92 / 10.0) dengan status MELAMPAUI BATAS (RED ALERT).", False, False)
    ])

    # -------------------------------------------------------------------------
    # SEKSI 6.6.2: SULAWESI TENGGARA
    # -------------------------------------------------------------------------
    doc.add_page_break()

    add_h3(doc, "6.6.2 Evaluasi Forensik D3TLH: Provinsi Sulawesi Tenggara (Sultra)")
    add_note_box(
        doc,
        "Provinsi Sulawesi Tenggara (Episentrum Konflik Agraria & Kepadatan IUP Ekstrem)",
        "Data empiris: Gabungan sensor satelit NASA TROPOMI NO2, Global Energy Monitor (PLTU Captive Morosi & Konawe 1.900 MW), Rekam Medis Kemenkes (Diare & ISPA), Laporan Kinerja KLHK (Limbah B3 & Tailing 6,5 Jt Ton), Global Forest Watch (Deforestasi 337k Ha), BNPB (158 Bencana Alam), Konsorsium Pembaruan Agraria & TanahKita (39.821 Jiwa Terdampak & 5 Kasus Pelanggaran FPIC), serta Minerba ESDM (Kepadatan IUP 11,72% Daratan & 160 IUP Baru). "
        "Diolah menggunakan model hybrid Z-Score Anomali Deviasi Standar dan Entropy Weight Method (EWM) sesuai antarmuka Dashboard Streamlit Tab 3 (Bedah Matematika Z-Score + EWM per Provinsi)."
    )

    add_h4(doc, "A. Pengantar & Kerangka Narasi")
    add_p(doc, [
        ("Berdasarkan hasil pemetaan empiris di antarmuka Streamlit ", False, False),
        ("Dashboard Page 6 (Audit D3TLH - Tab Bedah Matematika Z-Score + EWM per Provinsi)", True, False),
        (", Provinsi Sulawesi Tenggara memperlihatkan profil anomali yang sangat spesifik dan kontras dibandingkan Sulawesi Tengah. "
         "Jika tekanan ekologis di Sulawesi Tengah didominasi oleh polusi udara PLTU raksasa dan deforestasi daratan, maka ", False, False),
        ("Sulawesi Tenggara mengalami ledakan krisis daya dukung sosial, perampasan ruang hidup masyarakat pesisir, dan kepadatan konsesi tambang tertinggi se-Sulawesi.", True, False)
    ])
    add_p(doc, [
        ("Fakta lapangan mencatat bahwa konsesi tambang nikel di Sulawesi Tenggara telah mencaplok ", False, False),
        ("11,72% dari seluruh luas daratan provinsi", True, False),
        (" (skor Z-Score anomali Z = +1.50σ). Akibatnya, terjadi eskalasi perampasan ruang hidup yang berdampak langsung pada ", False, False),
        ("39.821 jiwa petani, nelayan, dan masyarakat pesisir (Z = +1.95σ, Skor Likert 5.0 - Outlier Tertinggi se-Sulawesi)", True, False),
        (", serta memicu 5 kasus sengketa pelanggaran persetujuan warga (FPIC) di pulau-pulau kecil seperti Pulau Wawonii (Konawe Kepulauan).", False, False)
    ])

    add_h4(doc, "B. Alur Logika Metodologis Skoring Tingkat Provinsi (Flowchart Sultra)")
    add_caption(doc, "Bagan Alur 6.6b: Alur Logika Pemrosesan Algoritma Skoring Provinsi Sulawesi Tenggara")
    if dl_sultra:
        try:
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.add_run().add_picture(png_sultra, width=Cm(15.0))
        except Exception as exc:
            print(f"[WARN] Gagal pasang gambar Sultra: {exc}")

    add_h4(doc, "C. Formulasi Matematis & Definisi Variabel")
    add_p(doc, [("Operasionalisasi skoring di Sulawesi Tenggara menggunakan model normalisasi dan pembobotan EWM yang konsisten dengan standar regional se-Sulawesi:", False, False)])

    add_formula_box(
        doc,
        "Tahap 1: Anomali Z-Score Sultra vs Rata-rata Bioregion",
        "Z_sultra,j = (x_sultra,j - mean(x_j)) / std(x_j)",
        [
            ("Kepadatan IUP Sultra", "Nilai 11,72% menghasilkan Z = +1.50σ (Outlier Ekstrem Likert 5.0; rerata regional hanya 5,08%)."),
            ("Korban Agraria Sultra", "Nilai 39.821 jiwa menghasilkan Z = +1.95σ (Skor Likert 5.0; mencakup 73% total korban se-Sulawesi)."),
            ("Pelanggaran FPIC Sultra", "Nilai 5 kasus menghasilkan Z = +1.86σ (Skor Likert 5.0; tertinggi di seluruh bioregion).")
        ]
    )
    add_formula_box(
        doc,
        "Tahap 2 & 3: Pembobotan Entropi EWM & Transformasi Likert Sultra",
        "W_j = (1 - E_j) / SUM(1 - E_j)    ;    Skor_Pilar = SUM(L_sultra,j * W_j) / SUM(W_j)",
        [
            ("Bobot EWM Korban Jiwa", "Indikator jiwa terdampak memiliki varians disparitas tinggi sehingga memperoleh bobot EWM w = 0.0781."),
            ("Bobot EWM FPIC", "Indikator FPIC memiliki bobot w = 0.0635, melipatgandakan sensitivitas penilaian pilar sosial."),
            ("Skor Pilar Sosial Sultra", "Mencapai 4.5 / 5.0 (Status: Melampaui Batas / Red Alert).")
        ]
    )

    add_h4(doc, "D. Matriks Hasil Uji Empiris (Sultra)")
    add_caption(doc, "Tabel 6.14: Bedah Matematika 20 Indikator Empiris Provinsi Sulawesi Tenggara (Model Hybrid Z-Score & EWM)")
    add_table_styled(
        doc,
        ["Pilar", "Indikator Empiris", "Fakta Mentah (A)", "Rata-rata (B)", "Deviasi (C)", "Z-Score", "Bobot EWM", "Likert", "Status Ekologis"],
        table_math_sultra,
        [1.5, 3.2, 2.0, 1.8, 1.7, 1.5, 1.5, 1.6, 2.2],
        ["C", "L", "R", "R", "R", "C", "C", "C", "C"]
    )
    add_caption(doc, "Tabel 6.15: Rekapitulasi Skor 5 Pilar & Status Ekologis Komposit Provinsi Sulawesi Tenggara")
    add_table_styled(
        doc,
        ["Pilar / Dimensi", "Cakupan Indikator Kunci", "Skor Likert Pilar (0-5)", "Status Ekologis", "Interpretasi Temuan Lapangan Sultra"],
        rekap_sultra,
        [2.5, 4.5, 2.2, 2.8, 5.0],
        ["C", "L", "C", "C", "L"]
    )

    add_h4(doc, "E. Analisis Temuan Empiris (Sultra)")
    add_p(doc, [
        ("1. ", True, False), (f"Daya Tampung Udara (Skor {sultra['udara']:.1f} / 5 — {get_likert_label(sultra['udara'])}): ", True, False),
        (f"Kapasitas PLTU captive beroperasi mencapai 1.900,0 MW (Z = +0.09σ), konsentrasi gas NO2 troposferik 6,62e-06 mol/m² (Z = +0.82σ, Likert 4.0), dan pelepasan emisi karbon deforestasi 189,02 Juta Ton CO2e (Z = +0.59σ, Likert 4.0). Tekanan polusi terkonsentrasi di kawasan industri Morosi (Konawe).\n", False, False),
        ("2. ", True, False), (f"Daya Tampung Air (Skor {sultra['air']:.1f} / 5 — {get_likert_label(sultra['air'])}): ", True, False),
        (f"Meskipun IKA sungai bernilai 65,32, tercatat timbulan tailing dan slag 6,52 Juta Ton (Z = +0.12σ) serta meletusnya 5 kasus sengketa ruang tangkap laut antara nelayan pesisir dan armada tongkang tambang (Z = +0.87σ, Likert 4.0).\n", False, False),
        ("3. ", True, False), (f"Daya Dukung Lahan (Skor {sultra['lahan']:.1f} / 5 — {get_likert_label(sultra['lahan'])}): ", True, False),
        (f"Ditemukan anomali ekstrem pada Kepadatan Konsesi IUP yang mencaplok 11,72% dari total daratan daratan provinsi (Z = +1.50σ, Likert 5.0 - Outlier Tertinggi se-Sulawesi), menyebabkan 337.434 Ha deforestasi hutan primer (Z = +0.67σ) dan perambahan 8.236 Ha hutan lindung.\n", False, False),
        ("4. ", True, False), (f"Daya Dukung Sosial (Skor {sultra['sosial']:.1f} / 5 — {get_likert_label(sultra['sosial'])}): ", True, False),
        (f"Sulawesi Tenggara mencatat krisis sosial terparah di seluruh bioregion Pulau Sulawesi. Sebanyak 39.821 jiwa warga terancam kehilangan ruang hidup (Z = +1.95σ, Likert 5.0), terjadi 5 kasus manipulasi persetujuan FPIC (Z = +1.86σ, Likert 5.0), 4 insiden kriminalisasi aktivis, dan defisit fasilitas SPA Puskesmas sebesar 17,92% (Z = +0.79σ, Likert 4.0).\n", False, False),
        ("5. ", True, False), (f"Veto Kebijakan (Skor {sultra['veto']:.1f} / 5 — {get_likert_label(sultra['veto'])}): ", True, False),
        (f"Diterbitkan 160 IUP baru pasca-2014 (Z = +0.64σ, Likert 4.0), memperparah pengkapalan bijih nikel ilegal di pulau-pulau kecil.\n", False, False),
        ("6. ", True, False), (f"Vonis Komposit Sulawesi Tenggara (Skor {sultra['total_likert']:.1f} / 5.0 — {sultra['likert_label']}): ", True, False),
        (f"Secara agregat, Sulawesi Tenggara memperoleh Skor Komposit 3.4 / 5.0 (Ekuivalen WSM 6.78 / 10.0) dengan status MENDEKATI BATAS. Namun, pengujian forensik membuktikan bahwa Pilar Daya Dukung Sosial (4.5 / 5) dan Kepadatan Konsesi Tambang (11,72%) telah berada pada status RED ALERT (MELAMPAUI BATAS EKSTREM).", False, False)
    ])

    docx_path = tool_dir / "Metodologi_Bab6_Skoring_Provinsi.docx"
    doc.save(str(docx_path))
    print(f"  [OK] Tersimpan: {docx_path}")

    # =========================================================================
    # [3/4] MEMBANGUN DOKUMEN HTML SATUAN
    # =========================================================================
    print("[3/4] Membangun HTML dan Markdown...")
    html_content = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Bab VI: Audit Forensik Metodologi D3TLH — Sub-bab 6.6 Algoritma Skoring Tingkat Provinsi</title>
<style>
  body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #202426; max-width: 1150px; margin: 0 auto; padding: 25px; background-color: #FAFAFA; }}
  h1 {{ color: #143642; border-bottom: 2px solid #143642; padding-bottom: 8px; font-size: 24px; }}
  h2 {{ color: #A8201A; margin-top: 25px; font-size: 20px; }}
  h3 {{ color: #0F4C5C; margin-top: 30px; font-size: 18px; border-bottom: 1px solid #0F4C5C; padding-bottom: 5px; }}
  h4 {{ color: #143642; margin-top: 15px; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px; }}
  .note-box {{ background-color: #F4F5F6; border-left: 5px solid #143642; padding: 12px 18px; margin: 15px 0; font-size: 13px; }}
  .formula {{ background-color: #F8F9FA; border-left: 4px solid #0F4C5C; padding: 10px 15px; margin: 10px 0; font-family: Consolas, monospace; font-size: 13px; color: #143642; font-weight: bold; }}
  .table-container {{ overflow-x: auto; margin: 15px 0; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 12px; background-color: #FFF; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
  th {{ background-color: #143642; color: #FFF; padding: 9px 10px; text-align: center; border: 1px solid #143642; font-size: 11px; }}
  td {{ padding: 7px 10px; border: 1px solid #E0E0E0; }}
  tr:nth-child(even) {{ background-color: #F9FAFA; }}
  tr.total-row {{ background-color: #EAEBED; font-weight: bold; }}
  .text-center {{ text-align: center; }}
  .text-right {{ text-align: right; }}
  .text-left {{ text-align: left; }}
  .badge-danger {{ background-color: #A8201A; color: white; padding: 2px 6px; border-radius: 3px; font-weight: bold; font-size: 10px; display: inline-block; }}
  .badge-warning {{ background-color: #E36414; color: white; padding: 2px 6px; border-radius: 3px; font-weight: bold; font-size: 10px; display: inline-block; }}
  .badge-success {{ background-color: #1E7E34; color: white; padding: 2px 6px; border-radius: 3px; font-weight: bold; font-size: 10px; display: inline-block; }}
  .mermaid {{ margin: 20px 0; text-align: center; background: #FFF; padding: 15px; border: 1px solid #E0E0E0; }}
  .table-caption {{ font-weight: bold; font-style: italic; color: #143642; margin-top: 15px; margin-bottom: 5px; font-size: 13px; }}
  .divider {{ margin: 40px 0; border-top: 2px dashed #CCCCCC; }}
</style>
<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
<script>mermaid.initialize({{startOnLoad:true}});</script>
</head>
<body>

<h1>BAB VI: AUDIT FORENSIK METODOLOGI D3TLH</h1>
<h2>SUB-BAB 6.6: ALGORITMA SKORING TINGKAT PROVINSI (MODEL HYBRID Z-SCORE & EWM)</h2>

<!-- SEKSI 6.6.1 SULTENG -->
<h3>6.6.1 Evaluasi Forensik D3TLH: Provinsi Sulawesi Tengah (Sulteng)</h3>
<div class="note-box">
  <strong>PROFIL BIOREGION: Provinsi Sulawesi Tengah (Episentrum Hilirisasi & PLTU Captive)</strong><br>
  Data empiris: Gabungan sensor satelit NASA TROPOMI NO2, Global Energy Monitor (GEM 2023), Rekam Medis Kemenkes (ISPA & Diare), Laporan Kinerja KLHK (Limbah B3 & Tailing), Global Forest Watch (Deforestasi & Emisi Karbon), BNPB (Bencana Alam), KPA & TanahKita (Konflik Agraria & Kriminalisasi), serta Minerba ESDM (IUP Nikel & Obral Izin). Diolah menggunakan model hybrid Z-Score Anomali Deviasi Standar dan Entropy Weight Method (EWM) sesuai antarmuka Dashboard Streamlit Tab 3 (Bedah Matematika Z-Score + EWM per Provinsi).
</div>

<h4>A. Pengantar & Kerangka Narasi</h4>
<p>Sebagaimana ditampilkan pada antarmuka Streamlit <strong>Dashboard Page 6 (Audit D3TLH - Tab Bedah Matematika Z-Score + EWM per Provinsi)</strong>, evaluasi daya dukung dan daya tampung lingkungan hidup tingkat provinsi dirancang untuk membongkar kelemahan metodologi pemerintah yang kerap mengaburkan krisis lokal melalui teknik perataan wilayah (dilution effect). Analisis forensik membuktikan bahwa <strong>Provinsi Sulawesi Tengah berada pada status RED ALERT (Skor Komposit 4.0 / 5.0 - Melampaui Batas)</strong>, di mana beban pencemaran udara, limbah B3, tailing, dan deforestasi primer telah melampaui batas lentur ekologis.</p>

<h4>B. Alur Logika Metodologis Skoring Tingkat Provinsi (Flowchart Sulteng)</h4>
<div class="mermaid">
{mermaid_sulteng}
</div>

<h4>C. Formulasi Matematis & Definisi Variabel</h4>
<div class="formula">Z_ij = (x_ij - mean(x_j)) / std(x_j) &nbsp;&nbsp;|&nbsp;&nbsp; Khusus IKA: Z_ika = - (ika_i - mean(ika)) / std(ika)</div>
<div class="formula">r_ij = (x_ij - min(x_j)) / (max(x_j) - min(x_j)) &nbsp;➔&nbsp; P_ij = r_ij / &Sigma;r_ij &nbsp;➔&nbsp; E_j = -k * &Sigma;(P_ij * ln(P_ij)) &nbsp;➔&nbsp; W_j = (1 - E_j) / &Sigma;(1 - E_j)</div>
<div class="formula">Skor_Pilar = &Sigma;(Likert_ij * W_j) / &Sigma;W_j &nbsp;&nbsp;|&nbsp;&nbsp; Skor_Komposit = (Udara + Air + Lahan + Sosial + Veto) / 5.0 = {sulteng['total_likert']:.1f} / 5</div>

<h4>D. Matriks Hasil Uji Empiris (Sulteng)</h4>
<div class="table-caption">Tabel 6.12: Bedah Matematika 20 Indikator Empiris Provinsi Sulawesi Tengah (Model Hybrid Z-Score & EWM)</div>
{html_table(["Pilar", "Indikator Empiris", "Fakta Mentah (A)", "Rata-rata (B)", "Deviasi (C)", "Z-Score", "Bobot EWM", "Likert", "Status Ekologis"], table_math_sulteng)}

<div class="table-caption">Tabel 6.13: Rekapitulasi Skor 5 Pilar & Status Ekologis Komposit Provinsi Sulawesi Tengah</div>
{html_table(["Pilar / Dimensi", "Cakupan Indikator Kunci", "Skor Likert Pilar (0-5)", "Status Ekologis", "Interpretasi Temuan Lapangan Sulteng"], rekap_sulteng)}

<h4>E. Analisis Temuan Empiris (Sulteng)</h4>
<p><strong>1. Daya Tampung Udara (Skor {sulteng['udara']:.1f} / 5 — Melampaui Batas):</strong> Beban PLTU captive batubara 7.325,0 MW (Z = +1.97&sigma;), limbah B3 25,30 Jt Ton (Z = +1.97&sigma;), emisi CO2 291,34 Jt Ton, dan anomali ISPA 3,50x lipat (Z = +1.66&sigma;).<br>
<strong>2. Daya Tampung Air (Skor {sulteng['air']:.1f} / 5 — Mendekati Batas):</strong> Timbulan tailing/slag 24,50 Jt Ton (Z = +1.97&sigma;) dan morbiditas diare 1,52x lipat (Z = +1.34&sigma;).<br>
<strong>3. Daya Dukung Lahan (Skor {sulteng['lahan']:.1f} / 5 — Melampaui Batas):</strong> Deforestasi primer 481.908 Ha (Z = +1.57&sigma;), perambahan hutan lindung 19.804 Ha (Z = +1.89&sigma;), dan 458 kejadian bencana hidrometeorologi.<br>
<strong>4. Daya Dukung Sosial (Skor {sulteng['sosial']:.1f} / 5 — Tidak Melampaui Batas):</strong> 12.231 jiwa terdampak konflik agraria dan 6 insiden kriminalisasi pembela HAM.<br>
<strong>5. Veto Kebijakan (Skor {sulteng['veto']:.1f} / 5 — Melampaui Batas):</strong> Obral 260 IUP baru pasca-2014 (Z = +1.64&sigma;) dan impunitas korporat ilegal.<br>
<strong>6. Vonis Komposit Sulteng (Skor {sulteng['total_likert']:.1f} / 5.0 — Melampaui Batas):</strong> Status <span class="badge-danger">MELAMPAUI BATAS (RED ALERT)</span> membuktikan keruntuhan daya dukung lingkungan akibat ekspansi smelter nikel.</p>

<div class="divider"></div>

<!-- SEKSI 6.6.2 SULTRA -->
<h3>6.6.2 Evaluasi Forensik D3TLH: Provinsi Sulawesi Tenggara (Sultra)</h3>
<div class="note-box">
  <strong>PROFIL BIOREGION: Provinsi Sulawesi Tenggara (Episentrum Konflik Agraria & Kepadatan IUP Ekstrem)</strong><br>
  Data empiris: Sensor satelit NASA NO2, PLTU Captive Morosi & Konawe 1.900 MW, Rekam Medis Diare & ISPA, Limbah B3 & Tailing 6,5 Jt Ton, Deforestasi 337k Ha, 158 Bencana Alam, 39.821 Jiwa Terdampak Konflik Agraria & 5 Kasus FPIC, serta Kepadatan IUP 11,72% Daratan & 160 IUP Baru. Diolah menggunakan model hybrid Z-Score Anomali Deviasi Standar dan Entropy Weight Method (EWM).
</div>

<h4>A. Pengantar & Kerangka Narasi</h4>
<p>Berdasarkan hasil pemetaan empiris di antarmuka Streamlit <strong>Dashboard Page 6 (Audit D3TLH - Tab Bedah Matematika Z-Score + EWM per Provinsi)</strong>, Provinsi Sulawesi Tenggara memperlihatkan profil anomali yang sangat kontras dengan Sulawesi Tengah. Sulawesi Tenggara mengalami <strong>ledakan krisis daya dukung sosial, perampasan ruang hidup masyarakat pesisir, dan kepadatan konsesi tambang tertinggi se-Sulawesi</strong>. Konsesi tambang nikel mencaplok <strong>11,72% daratan provinsi (Z = +1.50&sigma;, Likert 5.0)</strong> dan berdampak langsung pada <strong>39.821 jiwa (Z = +1.95&sigma;, Likert 5.0 - Outlier Tertinggi se-Sulawesi)</strong>.</p>

<h4>B. Alur Logika Metodologis Skoring Tingkat Provinsi (Flowchart Sultra)</h4>
<div class="mermaid">
{mermaid_sultra}
</div>

<h4>C. Formulasi Matematis & Definisi Variabel</h4>
<div class="formula">Z_sultra,j = (x_sultra,j - mean(x_j)) / std(x_j)</div>
<div class="formula">W_j = (1 - E_j) / &Sigma;(1 - E_j) &nbsp;&nbsp;|&nbsp;&nbsp; Skor_Pilar_Sosial = &Sigma;(Likert_sultra,j * W_j) / &Sigma;W_j = {sultra['sosial']:.1f} / 5</div>

<h4>D. Matriks Hasil Uji Empiris (Sultra)</h4>
<div class="table-caption">Tabel 6.14: Bedah Matematika 20 Indikator Empiris Provinsi Sulawesi Tenggara (Model Hybrid Z-Score & EWM)</div>
{html_table(["Pilar", "Indikator Empiris", "Fakta Mentah (A)", "Rata-rata (B)", "Deviasi (C)", "Z-Score", "Bobot EWM", "Likert", "Status Ekologis"], table_math_sultra)}

<div class="table-caption">Tabel 6.15: Rekapitulasi Skor 5 Pilar & Status Ekologis Komposit Provinsi Sulawesi Tenggara</div>
{html_table(["Pilar / Dimensi", "Cakupan Indikator Kunci", "Skor Likert Pilar (0-5)", "Status Ekologis", "Interpretasi Temuan Lapangan Sultra"], rekap_sultra)}

<h4>E. Analisis Temuan Empiris (Sultra)</h4>
<p><strong>1. Daya Tampung Udara (Skor {sultra['udara']:.1f} / 5 — {get_likert_label(sultra['udara'])}):</strong> Kapasitas 1.900 MW PLTU captive (Morosi/Konawe), emisi karbon 189,02 Jt Ton CO2e (Z = +0.59&sigma;), dan NO2 satelit 6,62e-06 mol/m².<br>
<strong>2. Daya Tampung Air (Skor {sultra['air']:.1f} / 5 — {get_likert_label(sultra['air'])}):</strong> IKA 65,32, beban tailing 6,52 Jt Ton, dan meletusnya 5 kasus konflik ruang tangkap laut nelayan vs tongkang nikel (Z = +0.87&sigma;, Likert 4.0).<br>
<strong>3. Daya Dukung Lahan (Skor {sultra['lahan']:.1f} / 5 — {get_likert_label(sultra['lahan'])}):</strong> Kepadatan Konsesi IUP mencapai 11,72% daratan provinsi (Z = +1.50&sigma;, Likert 5.0 - Outlier Ekstrem Se-Sulawesi) yang menggerus 337.434 Ha hutan alam primer.<br>
<strong>4. Daya Dukung Sosial (Skor {sultra['sosial']:.1f} / 5 — {get_likert_label(sultra['sosial'])}):</strong> Krisis sosial terparah se-Sulawesi dengan 39.821 jiwa warga terancam kehilangan ruang hidup (Z = +1.95&sigma;, Likert 5.0), 5 kasus manipulasi persetujuan FPIC (Z = +1.86&sigma;, Likert 5.0), dan defisit SPA 17,92%.<br>
<strong>5. Veto Kebijakan (Skor {sultra['veto']:.1f} / 5 — {get_likert_label(sultra['veto'])}):</strong> Obral 160 IUP baru pasca-2014 (Z = +0.64&sigma;, Likert 4.0).<br>
<strong>6. Vonis Komposit Sulawesi Tenggara (Skor {sultra['total_likert']:.1f} / 5.0 — {sultra['likert_label']}):</strong> Status <span class="badge-warning">MENDEKATI BATAS</span>, dengan catatan kritis bahwa Pilar Sosial (4.5 / 5) dan Kepadatan Konsesi Tambang (11,72%) telah berada pada status RED ALERT (MELAMPAUI BATAS EKSTREM).</p>

</body>
</html>
"""
    html_path = tool_dir / "Metodologi_Bab6_Skoring_Provinsi.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"  [OK] Tersimpan: {html_path}")

    # =========================================================================
    # [4/4] MEMBANGUN DOKUMEN MARKDOWN SATUAN
    # =========================================================================
    md_lines = [
        "# BAB VI: AUDIT FORENSIK METODOLOGI D3TLH",
        "## SUB-BAB 6.6: ALGORITMA SKORING TINGKAT PROVINSI (MODEL HYBRID Z-SCORE & EWM)",
        "",
        "### 6.6.1 Evaluasi Forensik D3TLH: Provinsi Sulawesi Tengah (Sulteng)",
        '> **PROFIL BIOREGION: Provinsi Sulawesi Tengah (Episentrum Hilirisasi & PLTU Captive)**  ',
        '> Data empiris: Gabungan sensor satelit NASA TROPOMI NO2, Global Energy Monitor (GEM 2023), Rekam Medis Kemenkes (ISPA & Diare), Laporan Kinerja KLHK (Limbah B3 & Tailing), Global Forest Watch (Deforestasi & Emisi Karbon), BNPB (Bencana Alam), KPA & TanahKita (Konflik Agraria & Kriminalisasi), serta Minerba ESDM (IUP Nikel & Obral Izin). Diolah menggunakan model hybrid Z-Score Anomali Deviasi Standar dan Entropy Weight Method (EWM) sesuai antarmuka Dashboard Streamlit Tab 3 (Bedah Matematika Z-Score + EWM per Provinsi).',
        "",
        "#### A. Pengantar & Kerangka Narasi",
        "Sebagaimana ditampilkan pada antarmuka Streamlit **Dashboard Page 6 (Audit D3TLH - Tab Bedah Matematika Z-Score + EWM per Provinsi)**, evaluasi daya dukung dan daya tampung lingkungan hidup tingkat provinsi dirancang untuk membongkar kelemahan metodologi pemerintah yang kerap mengaburkan krisis lokal melalui teknik perataan wilayah (dilution effect). Analisis forensik membuktikan bahwa **Provinsi Sulawesi Tengah berada pada status RED ALERT (Skor Komposit 4.0 / 5.0 - Melampaui Batas)**, di mana beban pencemaran udara, limbah B3, tailing, dan deforestasi primer telah melampaui batas lentur ekologis.",
        "",
        "#### B. Alur Logika Metodologis Skoring Tingkat Provinsi (Flowchart Sulteng)",
        "```mermaid",
        mermaid_sulteng,
        "```",
        "",
        "#### C. Formulasi Matematis & Definisi Variabel",
        "```text",
        "1. Z-Score Standard: Z_ij = (x_ij - mean(x_j)) / std(x_j)  |  Khusus IKA: Z_ika = - (ika_i - mean(ika)) / std(ika)",
        "2. Min-Max Normalisasi: r_ij = (x_ij - min(x_j)) / (max(x_j) - min(x_j))",
        "3. Proporsi Probabilitas: P_ij = r_ij / SUM(r_ij)",
        "4. Entropi Informasi: E_j = - (1 / ln(n)) * SUM(P_ij * ln(P_ij + eps))",
        "5. Koefisien Dispersi: D_j = 1 - E_j  -->  Bobot EWM: W_j = D_j / SUM(D_j)",
        "6. Mapping Likert: Z >= 1.0 -> 5.0 ; 0.5 <= Z < 1.0 -> 4.0 ; 0.0 <= Z < 0.5 -> 3.0 ; -0.5 <= Z < 0.0 -> 2.0 ; -1.0 <= Z < -0.5 -> 1.0 ; Z < -1.0 -> 0.0",
        f"7. Agregasi Komposit Sulteng: (Udara + Air + Lahan + Sosial + Veto) / 5.0 = {sulteng['total_likert']:.1f} / 5 (WSM: {sulteng['total']:.2f} / 10.0)",
        "```",
        "",
        "#### D. Matriks Hasil Uji Empiris (Sulteng)",
        "##### Tabel 6.12: Bedah Matematika 20 Indikator Empiris Provinsi Sulawesi Tengah (Model Hybrid Z-Score & EWM)",
        markdown_table(["Pilar", "Indikator Empiris", "Fakta Mentah (A)", "Rata-rata (B)", "Deviasi (C)", "Z-Score", "Bobot EWM", "Likert", "Status Ekologis"], table_math_sulteng),
        "",
        "##### Tabel 6.13: Rekapitulasi Skor 5 Pilar & Status Ekologis Komposit Provinsi Sulawesi Tengah",
        markdown_table(["Pilar / Dimensi", "Cakupan Indikator Kunci", "Skor Likert Pilar (0-5)", "Status Ekologis", "Interpretasi Temuan Lapangan Sulteng"], rekap_sulteng),
        "",
        "#### E. Analisis Temuan Empiris (Sulteng)",
        f"1. **Daya Tampung Udara (Skor {sulteng['udara']:.1f} / 5 — Melampaui Batas):** Beban PLTU captive batubara 7.325,0 MW (Z = +1.97σ), limbah B3 25,30 Jt Ton (Z = +1.97σ), emisi CO2 291,34 Jt Ton, dan anomali ISPA 3,50x lipat (Z = +1.66σ).",
        f"2. **Daya Tampung Air (Skor {sulteng['air']:.1f} / 5 — Mendekati Batas):** Timbulan tailing/slag 24,50 Jt Ton (Z = +1.97σ) dan morbiditas diare 1,52x lipat (Z = +1.34σ).",
        f"3. **Daya Dukung Lahan (Skor {sulteng['lahan']:.1f} / 5 — Melampaui Batas):** Deforestasi primer 481.908 Ha (Z = +1.57σ), perambahan hutan lindung 19.804 Ha (Z = +1.89σ), dan 458 kejadian bencana hidrometeorologi.",
        f"4. **Daya Dukung Sosial (Skor {sulteng['sosial']:.1f} / 5 — Tidak Melampaui Batas):** 12.231 jiwa terdampak konflik agraria dan 6 insiden kriminalisasi pembela HAM.",
        f"5. **Veto Kebijakan (Skor {sulteng['veto']:.1f} / 5 — Melampaui Batas):** Obral 260 IUP baru pasca-2014 (Z = +1.64σ) dan impunitas korporat ilegal.",
        f"6. **Vonis Komposit Sulteng (Skor {sulteng['total_likert']:.1f} / 5.0 — Melampaui Batas):** Status **Melampaui Batas** *(STATUS: RED ALERT)* membuktikan keruntuhan daya dukung lingkungan akibat ekspansi smelter nikel.",
        "",
        "---",
        "",
        "### 6.6.2 Evaluasi Forensik D3TLH: Provinsi Sulawesi Tenggara (Sultra)",
        '> **PROFIL BIOREGION: Provinsi Sulawesi Tenggara (Episentrum Konflik Agraria & Kepadatan IUP Ekstrem)**  ',
        '> Data empiris: Sensor satelit NASA NO2, PLTU Captive Morosi & Konawe 1.900 MW, Rekam Medis Diare & ISPA, Limbah B3 & Tailing 6,5 Jt Ton, Deforestasi 337k Ha, 158 Bencana Alam, 39.821 Jiwa Terdampak Konflik Agraria & 5 Kasus FPIC, serta Kepadatan IUP 11,72% Daratan & 160 IUP Baru. Diolah menggunakan model hybrid Z-Score Anomali Deviasi Standar dan Entropy Weight Method (EWM).',
        "",
        "#### A. Pengantar & Kerangka Narasi",
        "Berdasarkan hasil pemetaan empiris di antarmuka Streamlit **Dashboard Page 6 (Audit D3TLH - Tab Bedah Matematika Z-Score + EWM per Provinsi)**, Provinsi Sulawesi Tenggara memperlihatkan profil anomali yang sangat kontras dengan Sulawesi Tengah. Sulawesi Tenggara mengalami **ledakan krisis daya dukung sosial, perampasan ruang hidup masyarakat pesisir, dan kepadatan konsesi tambang tertinggi se-Sulawesi**. Konsesi tambang nikel mencaplok **11,72% daratan provinsi (Z = +1.50σ, Likert 5.0)** dan berdampak langsung pada **39.821 jiwa (Z = +1.95σ, Likert 5.0 - Outlier Tertinggi se-Sulawesi)**.",
        "",
        "#### B. Alur Logika Metodologis Skoring Tingkat Provinsi (Flowchart Sultra)",
        "```mermaid",
        mermaid_sultra,
        "```",
        "",
        "#### C. Formulasi Matematis & Definisi Variabel",
        "```text",
        "1. Anomali Z-Score Sultra: Z_sultra,j = (x_sultra,j - mean(x_j)) / std(x_j)",
        "2. Kepadatan IUP Sultra: 11,72% -> Z = +1.50σ (Skor Likert 5.0 - Outlier Ekstrem se-Sulawesi)",
        "3. Korban Jiwa Sultra: 39.821 Jiwa -> Z = +1.95σ (Skor Likert 5.0 - Mencakup 73% Korban se-Sulawesi)",
        "4. Pelanggaran FPIC Sultra: 5 Kasus -> Z = +1.86σ (Skor Likert 5.0 - Tertinggi se-Sulawesi)",
        f"5. Skor Komposit Total Sultra: (Udara + Air + Lahan + Sosial + Veto) / 5.0 = {sultra['total_likert']:.1f} / 5 (WSM: {sultra['total']:.2f} / 10.0)",
        "```",
        "",
        "#### D. Matriks Hasil Uji Empiris (Sultra)",
        "##### Tabel 6.14: Bedah Matematika 20 Indikator Empiris Provinsi Sulawesi Tenggara (Model Hybrid Z-Score & EWM)",
        markdown_table(["Pilar", "Indikator Empiris", "Fakta Mentah (A)", "Rata-rata (B)", "Deviasi (C)", "Z-Score", "Bobot EWM", "Likert", "Status Ekologis"], table_math_sultra),
        "",
        "##### Tabel 6.15: Rekapitulasi Skor 5 Pilar & Status Ekologis Komposit Provinsi Sulawesi Tenggara",
        markdown_table(["Pilar / Dimensi", "Cakupan Indikator Kunci", "Skor Likert Pilar (0-5)", "Status Ekologis", "Interpretasi Temuan Lapangan Sultra"], rekap_sultra),
        "",
        "#### E. Analisis Temuan Empiris (Sultra)",
        f"1. **Daya Tampung Udara (Skor {sultra['udara']:.1f} / 5 — {get_likert_label(sultra['udara'])}):** Kapasitas 1.900 MW PLTU captive (Morosi/Konawe), emisi karbon 189,02 Jt Ton CO2e (Z = +0.59σ), dan NO2 satelit 6,62e-06 mol/m².",
        f"2. **Daya Tampung Air (Skor {sultra['air']:.1f} / 5 — {get_likert_label(sultra['air'])}):** IKA 65,32, beban tailing 6,52 Jt Ton, dan meletusnya 5 kasus konflik ruang tangkap laut nelayan vs tongkang nikel (Z = +0.87σ, Likert 4.0).",
        f"3. **Daya Dukung Lahan (Skor {sultra['lahan']:.1f} / 5 — {get_likert_label(sultra['lahan'])}):** Kepadatan Konsesi IUP mencapai 11,72% daratan provinsi (Z = +1.50σ, Likert 5.0 - Outlier Ekstrem Se-Sulawesi) yang menggerus 337.434 Ha hutan alam primer.",
        f"4. **Daya Dukung Sosial (Skor {sultra['sosial']:.1f} / 5 — {get_likert_label(sultra['sosial'])}):** Krisis sosial terparah se-Sulawesi dengan 39.821 jiwa warga terancam kehilangan ruang hidup (Z = +1.95σ, Likert 5.0), 5 kasus manipulasi persetujuan FPIC (Z = +1.86σ, Likert 5.0), dan defisit SPA 17,92%.",
        f"5. **Veto Kebijakan (Skor {sultra['veto']:.1f} / 5 — {get_likert_label(sultra['veto'])}):** Obral 160 IUP baru pasca-2014 (Z = +0.64σ, Likert 4.0).",
        f"6. **Vonis Komposit Sulawesi Tenggara (Skor {sultra['total_likert']:.1f} / 5.0 — {sultra['likert_label']}):** Status **Mendekati Batas**, dengan catatan kritis bahwa Pilar Sosial (4.5 / 5) dan Kepadatan Konsesi Tambang (11,72%) telah berada pada status **Melampaui Batas Ekstrem** *(RED ALERT)*.",
        ""
    ]

    md_path = tool_dir / "Metodologi_Bab6_Skoring_Provinsi.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print(f"  [OK] Tersimpan: {md_path}")
    print("[4/4] Selesai membangun Sub-bab 6.6 untuk Provinsi Sulawesi Tengah & Sulawesi Tenggara.")


if __name__ == "__main__":
    generate_bab6_skoring_provinsi()
