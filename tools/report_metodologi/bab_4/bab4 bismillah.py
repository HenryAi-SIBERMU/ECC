#!/usr/bin/env python3
"""
Generator Laporan Metodologi Bab 4: Ruang Hidup yang Terampas

Fokus awal: Sub-bab 4.1 Tren Eskalasi Konflik Agraria Seiring Ekspansi
Industri. Pilar 1 ditulis langsung dalam generator Python agar selaras
dengan SOP dokumentasi Celios2.
"""

import base64
import sys
from pathlib import Path

try:
    import pandas as pd
    import requests
    from docx import Document
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Cm, Pt, RGBColor
except ImportError:
    import subprocess

    print("[INFO] Memasang dependensi yang diperlukan...")
    subprocess.check_call([
        sys.executable,
        "-m",
        "pip",
        "install",
        "pandas",
        "requests",
        "python-docx",
    ])
    import pandas as pd
    import requests
    from docx import Document
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Cm, Pt, RGBColor


G_DARK = RGBColor(0x1B, 0x5E, 0x20)
G_MID = RGBColor(0x2E, 0x7D, 0x32)
C_BODY = RGBColor(0x22, 0x22, 0x22)
C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
C_RED = RGBColor(0xB7, 0x1C, 0x1C)


def download_mermaid_png(mermaid_str, filepath):
    try:
        encoded = base64.urlsafe_b64encode(mermaid_str.encode("utf-8")).decode("utf-8")
        url = f"https://mermaid.ink/img/{encoded}"
        print(f"[INFO] Mendownload Mermaid JS flowchart ke {filepath}...")
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            with open(filepath, "wb") as f:
                f.write(resp.content)
            return True
        print(f"[WARN] Gagal download Mermaid. Status: {resp.status_code}")
        return False
    except Exception as exc:
        print(f"[WARN] Exception saat download Mermaid: {exc}")
        return False


def set_cell_borders(cell, top=None, left=None, bottom=None, right=None):
    tc_pr = cell._tc.get_or_add_tcPr()
    bdr = OxmlElement("w:tcBorders")
    for edge, cfg in [("top", top), ("left", left), ("bottom", bottom), ("right", right)]:
        el = OxmlElement(f"w:{edge}")
        if cfg is None:
            el.set(qn("w:val"), "none")
        else:
            for key, val in cfg.items():
                el.set(qn(f"w:{key}"), str(val))
        bdr.append(el)
    tc_pr.append(bdr)


def cell_margin(cell, left=100, right=100, top=60, bottom=60):
    tc_pr = cell._tc.get_or_add_tcPr()
    margin = OxmlElement("w:tcMar")
    for side, val in [("top", top), ("bottom", bottom), ("left", left), ("right", right)]:
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:w"), str(val))
        el.set(qn("w:type"), "dxa")
        margin.append(el)
    tc_pr.append(margin)


def para_shd(paragraph, fill):
    p_pr = paragraph._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    p_pr.append(shd)


def cell_shd(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def para_border_bottom(paragraph, color="2E7D32", sz="6"):
    p_pr = paragraph._p.get_or_add_pPr()
    p_bdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), sz)
    bottom.set(qn("w:space"), "2")
    bottom.set(qn("w:color"), color)
    p_bdr.append(bottom)
    p_pr.append(p_bdr)


def para_border_left(paragraph, color="2E7D32", sz="18"):
    p_pr = paragraph._p.get_or_add_pPr()
    p_bdr = OxmlElement("w:pBdr")
    left = OxmlElement("w:left")
    left.set(qn("w:val"), "single")
    left.set(qn("w:sz"), sz)
    left.set(qn("w:space"), "6")
    left.set(qn("w:color"), color)
    p_bdr.append(left)
    p_pr.append(p_bdr)


def all_border_para(paragraph, color="444444", sz="4"):
    p_pr = paragraph._p.get_or_add_pPr()
    p_bdr = OxmlElement("w:pBdr")
    for side in ["top", "left", "bottom", "right"]:
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), sz)
        el.set(qn("w:space"), "4")
        el.set(qn("w:color"), color)
        p_bdr.append(el)
    p_pr.append(p_bdr)


def run(paragraph, text, bold=False, italic=False, pt=9.5, color=None, mono=False):
    r = paragraph.add_run(text)
    r.bold = bold
    r.italic = italic
    r.font.size = Pt(pt)
    r.font.color.rgb = color if color else C_BODY
    if mono:
        r.font.name = "Courier New"
        r._element.rPr.rFonts.set(qn("w:ascii"), "Courier New")
    return r


def add_h1(doc, title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    para_border_bottom(p, color="1B5E20", sz="12")
    run(p, title.upper(), bold=True, pt=13, color=G_DARK)


def add_h2(doc, title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    para_border_bottom(p, color="2E7D32", sz="6")
    run(p, title.upper(), bold=True, pt=11, color=G_MID)


def add_h4(doc, title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    run(p, title, bold=True, pt=9.5, color=G_MID)


def add_p(doc, parts, space_after=5, indent=0):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(space_after)
    if indent > 0:
        p.paragraph_format.left_indent = Pt(indent)
    for text, bold, italic in parts:
        run(p, text, bold=bold, italic=italic, pt=9.5)
    return p


def add_formula(doc, title, formula_text, var_desc=None):
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(6)
    p_title.paragraph_format.space_after = Pt(1)
    run(p_title, f"Persamaan: {title}", bold=True, italic=True, pt=8.5, color=G_MID)
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.left_indent = Pt(12)
    para_shd(p, "EDF7EE")
    all_border_para(p, color="A5D6A7", sz="4")
    run(p, formula_text, pt=8.5, color=G_DARK, mono=True)
    if var_desc:
        p_desc = doc.add_paragraph()
        p_desc.paragraph_format.space_before = Pt(2)
        p_desc.paragraph_format.space_after = Pt(6)
        p_desc.paragraph_format.left_indent = Pt(14)
        run(p_desc, "Keterangan Variabel:\n", bold=True, italic=True, pt=8, color=RGBColor(0x33, 0x33, 0x33))
        for idx, item in enumerate(var_desc):
            trailing = "\n" if idx < len(var_desc) - 1 else ""
            run(p_desc, f"- {item[0]}: ", bold=True, pt=8, color=G_DARK)
            run(p_desc, f"{item[1]}{trailing}", pt=8, color=RGBColor(0x44, 0x44, 0x44))


def add_note_box(doc, title, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.left_indent = Pt(10)
    para_border_left(p, color="2E7D32", sz="16")
    para_shd(p, "F1F8E9")
    run(p, f"{title.upper()}: ", bold=True, pt=8.5, color=G_DARK)
    run(p, text, italic=True, pt=8.5, color=RGBColor(0x33, 0x33, 0x33))


def add_caption(doc, caption_text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    run(p, caption_text, bold=True, italic=True, pt=8.5, color=G_MID)
    return p


def add_table_1col(doc, headers, rows, col_widths_cm, alignments=None):
    tbl = doc.add_table(rows=1 + len(rows), cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.style = "Table Grid"
    tbl.autofit = False
    bd_cfg = {"val": "single", "sz": "4", "color": "D0D0D0", "space": "0"}
    for j, (header, width) in enumerate(zip(headers, col_widths_cm)):
        cell = tbl.rows[0].cells[j]
        cell.width = Cm(width)
        cell_shd(cell, "2E7D32")
        cell_margin(cell, left=100, right=100, top=70, bottom=70)
        set_cell_borders(cell, top=bd_cfg, left=bd_cfg, bottom={"val": "single", "sz": "8", "color": "1B5E20", "space": "0"}, right=bd_cfg)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if alignments and alignments[j] == "C" else WD_ALIGN_PARAGRAPH.LEFT
        run(p, header, bold=True, pt=8.5, color=C_WHITE)
    for i, row_data in enumerate(rows):
        fill = "F5FBF5" if i % 2 == 0 else "FFFFFF"
        for j, val in enumerate(row_data):
            cell = tbl.cell(i + 1, j)
            cell.width = Cm(col_widths_cm[j])
            cell_shd(cell, fill)
            cell_margin(cell, left=100, right=100, top=50, bottom=50)
            set_cell_borders(cell, top=bd_cfg, left=bd_cfg, bottom=bd_cfg, right=bd_cfg)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if alignments and alignments[j] == "C" else WD_ALIGN_PARAGRAPH.LEFT
            run(p, str(val), pt=8.5)
    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_after = Pt(4)
    return tbl


def html_table(headers, rows):
    header_html = "".join(f'<th class="data-th">{h}</th>' for h in headers)
    body = []
    for i, row in enumerate(rows):
        cls = ' class="data-tr-even"' if i % 2 == 1 else ""
        cells = "".join(f'<td class="data-td">{cell}</td>' for cell in row)
        body.append(f"<tr{cls}>{cells}</tr>")
    return f"""<table>
<thead><tr>{header_html}</tr></thead>
<tbody>
{chr(10).join(body)}
</tbody>
</table>"""


def markdown_table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join([":---" for _ in headers]) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(lines)


def map_sektor(status):
    status = str(status).lower()
    if "kebun" in status:
        return "Perkebunan"
    if "tambang" in status:
        return "Pertambangan"
    if "hutan" in status:
        return "Kehutanan"
    if any(x in status for x in ["infrastruktur", "bendungan", "transmigrasi", "energi", "fasilitas", "jalan", "industri"]):
        return "Infrastruktur & PSN"
    if any(x in status for x in ["pariwisata", "laut", "pesisir"]):
        return "Pariwisata & Pesisir"
    return "Lainnya"


def generate_all_bab4():
    base_dir = Path(__file__).resolve().parent.parent.parent.parent
    data_dir = base_dir / "data" / "processed"
    tool_dir = base_dir / "tools" / "report_metodologi" / "bab_4"
    tool_dir.mkdir(parents=True, exist_ok=True)

    print("[1/4] Mengekstraksi dataset empiris Bab 4 sub-bab 4.1...")
    df_raw = pd.read_csv(data_dir / "sulawesi_konflik_agraria_tanahkita.csv")
    keywords = r"\b(?:sulawesi|sulsel|sulteng|sultra|sulut|sulbar|gorontalo|morowali|konawe|kolaka|bombana|poso|donggala|makassar|manado|minahasa|sangihe|mamuju|majene|polewali|halmahera|maluku utara|weda|obi|soroako|luwu|bantaeng|buton|muna|wakatobi|banggai|buol|toli-toli|parigi|luwuk|kendari|baubau|palu|bitung|tomohon|kotamobagu|gowa|takalar|jeneponto|bulukumba|sinjai|bone|maros|pangkep|barru|pinrang|enrekang|toraja|palopo)\b"
    mask = (
        df_raw["judul"].str.contains(keywords, case=False, na=False, regex=True)
        | df_raw["deskripsi"].str.contains(keywords, case=False, na=False, regex=True)
        | df_raw["narasi"].str.contains(keywords, case=False, na=False, regex=True)
        | df_raw["lokasi"].str.contains(keywords, case=False, na=False, regex=True)
    )
    df_konflik = df_raw[mask].copy()
    df_konflik["tahun"] = pd.to_numeric(df_konflik["tahun"], errors="coerce")
    df_konflik = df_konflik.dropna(subset=["tahun"])
    df_konflik["tahun"] = df_konflik["tahun"].astype(int)
    df_konflik["Sektor_Grup"] = df_konflik["status"].apply(map_sektor)
    df_konflik["dampak_masyarakat_jiwa"] = pd.to_numeric(df_konflik["dampak_masyarakat_jiwa"], errors="coerce").fillna(0)

    total_konflik = len(df_konflik)
    konflik_kebun = len(df_konflik[df_konflik["status"].str.contains("Perkebunan", case=False, na=False)])
    konflik_tambang = len(df_konflik[df_konflik["status"].str.contains("Pertambangan", case=False, na=False)])
    konflik_hutan = len(df_konflik[df_konflik["status"].str.contains("Hutan", case=False, na=False)])
    konflik_infrastruktur = len(df_konflik[df_konflik["status"].str.contains("Infrastruktur|Bendungan|Transmigrasi|Energi|Fasilitas|Jalan", case=False, na=False)])
    konflik_pariwisata = len(df_konflik[df_konflik["status"].str.contains("Pariwisata|Konservasi Laut", case=False, na=False)])
    rasio_ekstraktif = ((konflik_tambang + konflik_kebun + konflik_hutan) / total_konflik) * 100 if total_konflik else 0
    total_jiwa = int(df_konflik["dampak_masyarakat_jiwa"].sum())
    status_belum_selesai = len(df_konflik[df_konflik["status_konflik"].str.contains("Belum Ditangani", na=False)])
    libat_masyarakat = df_konflik["keterlibatan_masyarakat"].notna().sum()

    df_ts_modern = df_konflik[df_konflik["tahun"] >= 1990].copy()
    total_ts = len(df_konflik)
    pasca_2005 = len(df_konflik[df_konflik["tahun"] >= 2005])
    pra_2005 = len(df_konflik[df_konflik["tahun"] < 2005])
    lonjakan = (pasca_2005 / pra_2005 * 100) if pra_2005 > 0 else 0

    df_agg = df_ts_modern.groupby(["tahun", "Sektor_Grup"]).size().reset_index(name="Jumlah")
    df_total_per_tahun = df_ts_modern.groupby("tahun").size().reset_index(name="Jumlah")
    peak_year = 0
    peak_value = 0
    if not df_total_per_tahun.empty:
        max_year_row = df_total_per_tahun.loc[df_total_per_tahun["Jumlah"].idxmax()]
        peak_year = int(max_year_row["tahun"])
        peak_value = int(max_year_row["Jumlah"])

    sector_rows = []
    sector_total = df_ts_modern.groupby("Sektor_Grup").size().reset_index(name="Jumlah").sort_values("Jumlah", ascending=False)
    for _, row in sector_total.iterrows():
        sector_rows.append([row["Sektor_Grup"], f"{int(row['Jumlah']):,}", f"{row['Jumlah'] / len(df_ts_modern) * 100:.1f}%"])

    annual_rows = []
    for _, row in df_total_per_tahun.sort_values("tahun").iterrows():
        annual_rows.append([str(int(row["tahun"])), f"{int(row['Jumlah']):,}"])

    peak_sector_rows = []
    if peak_year:
        peak_sector = df_agg[df_agg["tahun"] == peak_year].sort_values("Jumlah", ascending=False)
        for _, row in peak_sector.iterrows():
            peak_sector_rows.append([str(peak_year), row["Sektor_Grup"], f"{int(row['Jumlah']):,}"])

    mermaid_str_4_1 = """flowchart LR
    subgraph Data_Input["1. Input Data Dashboard"]
        A["Data Konflik Agraria KPA/Tanah Kita<br/><i>judul, deskripsi, lokasi, status, tahun</i>"]
    end
    subgraph Regional_Filter["2. Filter Regional & Klasifikasi Sektor"]
        A --> B["Filter keyword Sulawesi, Maluku Utara,<br/>dan sentra nikel terkait"]
        B --> C["Klasifikasi sektor pemicu<br/>Perkebunan, Kehutanan, Pertambangan, PSN, Pesisir"]
    end
    subgraph Trend_Analysis["3. Time-Series Trend Analysis"]
        C --> D["Agregasi konflik tahunan sejak 1990"]
        D --> E["Komparasi pra-2005 vs pasca-2005"]
        D --> F["Identifikasi puncak insidensi konflik"]
    end
    E --> G["Pembacaan eskalasi konflik agraria"]
    F --> G"""
    mermaid_png_path_4_1 = str(tool_dir / "mermaid_flowchart_4_1.png")
    download_success_4_1 = download_mermaid_png(mermaid_str_4_1, mermaid_png_path_4_1)

    print("[2/4] Membangun DOCX Metodologi_Bab4_Ruang_Hidup.docx...")
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
    run(p_hdr, "CELIOS - CENTER OF ECONOMIC AND LAW STUDIES  |  LAPORAN RISET METODOLOGI D3TLH", bold=True, pt=8, color=G_MID)

    add_h1(doc, "BAB IV: METODOLOGI ANALISIS RUANG HIDUP YANG TERAMPAS")
    add_p(doc, [
        ("Dokumen laporan metodologi ini menyajikan kerangka ilmiah, prosedur pengolahan data, dan pembacaan empiris yang dioperasionalkan pada ", False, False),
        ("Bab 4: Ruang Hidup yang Terampas", True, False),
        (" dalam studi Daya Dukung dan Daya Tampung Lingkungan Hidup (D3TLH) Sulawesi.", False, False),
    ])

    add_h2(doc, "4.1 Tren Eskalasi Konflik Agraria Seiring Ekspansi Industri")
    add_note_box(doc, "Sumber Data Resmi & Deskripsi Visualisasi", "Catatan Konflik Agraria: data/processed/sulawesi_konflik_agraria_tanahkita.csv. Visualisasi dashboard menggunakan Analisis Tren Time-Series untuk melacak eskalasi letupan konflik agraria historis berdasarkan tahun pencatatan dan sektor pemicu.")

    add_h4(doc, "A. Pengantar & Kerangka Narasi")
    add_p(doc, [
        (f"Ekspansi industri ekstraktif dan proyek strategis berimplikasi pada dinamika sosial dan penggunaan lahan masyarakat. Data empiris mencatat akumulasi {total_konflik:,} kasus konflik agraria, dengan estimasi {total_jiwa:,} jiwa terdampak dan {status_belum_selesai:,} kasus berstatus belum ditangani. ", False, False),
        (f"Tiga sektor utama (Perkebunan, Kehutanan, dan Pertambangan) menyumbang porsi {rasio_ekstraktif:.1f}% dari keseluruhan catatan konflik regional.", False, False),
    ])
    add_p(doc, [
        (f"Pada periode pra-2005, sistem pendataan mencatat {pra_2005:,} kasus konflik agraria. Pada periode pasca-2005 hingga saat ini, data mencatat {pasca_2005:,} kasus konflik lahan, atau setara peningkatan sebesar {lonjakan:,.1f}% dibandingkan periode sebelumnya.", False, False),
    ])

    add_h4(doc, "B. Alur Logika Metodologis Analisis Tren Time-Series")
    add_p(doc, [
        ("Kerangka analisis tren runtun waktu untuk melacak eskalasi kasus perampasan lahan secara historis diilustrasikan pada ", False, False),
        ("Bagan Alur 4.1", True, False),
        (" berikut. Sub-bab ini tidak menggunakan uji inferensial Chi-Square, melainkan agregasi time-series dan komparasi periodik.", False, False),
    ])
    add_caption(doc, "Bagan Alur 4.1: Alur Logika Metodologis Time-Series Trend Analysis Konflik Agraria")
    if download_success_4_1:
        try:
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.add_run().add_picture(mermaid_png_path_4_1, width=Cm(15))
        except Exception as exc:
            print(f"[WARN] Gagal memasukkan gambar Mermaid 4.1 ke DOCX: {exc}")
            p_err = doc.add_paragraph()
            run(p_err, "[Gambar Flowchart Gagal Dimuat]", color=C_RED, pt=9)
    else:
        p_err = doc.add_paragraph()
        run(p_err, "[Gambar Flowchart Gagal Diunduh, silakan periksa koneksi internet saat generate]", color=C_RED, pt=9)

    add_h4(doc, "C. Formulasi Matematis: Agregasi Konflik Tahunan dan Lonjakan Eskalasi")
    add_p(doc, [("Agregasi konflik berdasarkan tahun pencatatan dan sektor industri dihitung menggunakan sistem formulasi matematis berikut:", False, False)])
    add_formula(doc, "Total Konflik Tahunan per Sektor", "K_{t,s} = Σ c_i, untuk setiap kasus i pada tahun t dan sektor s", [
        ("K_{t,s}", "Total letupan konflik pada tahun t dan sektor pemicu s."),
        ("c_i", "Indikator kasus konflik ke-i; bernilai 1 jika kasus masuk tahun t dan sektor s."),
        ("t", "Tahun pencatatan konflik."),
        ("s", "Sektor pemicu konflik: Perkebunan, Kehutanan, Pertambangan, Infrastruktur & PSN, Pariwisata & Pesisir, atau Lainnya."),
    ])
    add_formula(doc, "Lonjakan Eskalasi Pasca-2005", "E (%) = ( K_Pasca / K_Pra ) × 100", [
        ("E (%)", "Rasio eskalasi konflik pasca-2005 terhadap periode pra-2005."),
        ("K_Pasca", f"Jumlah konflik periode pasca-2005 ({pasca_2005:,} kasus)."),
        ("K_Pra", f"Jumlah konflik periode pra-2005 ({pra_2005:,} kasus)."),
    ])
    add_formula(doc, "Substitusi Lonjakan Eskalasi", f"E = ({pasca_2005:,} / {pra_2005:,}) × 100 = {lonjakan:,.1f}%")

    add_h4(doc, "D. Matriks Hasil Uji Empiris: Tren Tahunan dan Sektor Pemicu Konflik")
    add_p(doc, [("Distribusi jumlah konflik agraria modern sejak 1990 disajikan pada Tabel 4.1 berikut:", False, False)])
    add_caption(doc, "Tabel 4.1: Tren Tahunan Konflik Agraria Regional (1990-2025)")
    add_table_1col(doc, ["Tahun", "Jumlah Konflik"], annual_rows, [3.0, 3.0], ["C", "C"])

    add_caption(doc, "Tabel 4.2: Distribusi Konflik Agraria menurut Sektor Pemicu")
    add_table_1col(doc, ["Sektor Pemicu", "Jumlah Konflik", "Proporsi"], sector_rows, [5.5, 3.0, 3.0], ["L", "C", "C"])

    add_caption(doc, f"Tabel 4.3: Komposisi Sektor pada Tahun Puncak Insidensi ({peak_year})")
    add_table_1col(doc, ["Tahun", "Sektor Pemicu", "Jumlah Konflik"], peak_sector_rows, [2.5, 5.5, 3.0], ["C", "L", "C"])

    add_h4(doc, "E. Analisis Temuan Empiris: Puncak Insidensi dan Eskalasi Konflik")
    add_p(doc, [
        (f"Grafik time-series pada dashboard memperlihatkan peningkatan insidensi konflik yang memuncak pada tahun {peak_year} dengan {peak_value:,} kasus konflik. Pembedahan data sektoral menunjukkan konsentrasi konflik pada sektor-sektor berbasis penguasaan ruang. ", False, False),
        ("Peningkatan insidensi konflik beririsan dengan dinamika perizinan kawasan, sehingga pengelolaan alokasi ruang dan perlindungan hak masyarakat di wilayah investasi menjadi faktor penting untuk meminimalkan dampak sosial.", False, False),
    ])

    docx_path = tool_dir / "Metodologi_Bab4_Ruang_Hidup.docx"
    doc.save(str(docx_path))
    print(f"  [OK] Tersimpan: {docx_path}")

    print("[3/4] Membangun HTML dan Markdown Bab 4...")
    html_content = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Laporan Metodologi Bab 4 - Ruang Hidup yang Terampas</title>
<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
<script>mermaid.initialize({{startOnLoad:true, theme:'dark'}});</script>
<style>
body {{ font-family: Arial, sans-serif; max-width: 920px; margin: 0 auto; padding: 32px; background: #0E1117; color: #D4D4D4; line-height: 1.65; }}
.hdr-sub {{ color: #43A047; font-size: 8.5pt; font-weight: 700; text-transform: uppercase; }}
.hdr-title {{ color: #81C784; font-size: 15pt; font-weight: 800; text-transform: uppercase; border-bottom: 2px solid #2E7D32; padding-bottom: 8px; }}
h2 {{ color: #81C784; text-transform: uppercase; border-bottom: 1px solid #2E7D32; }}
h4 {{ color: #A5D6A7; }}
.note-box {{ background: #132213; border-left: 4px solid #2E7D32; padding: 10px 14px; margin: 12px 0; }}
.formula {{ background: #0D1B0E; border: 1px solid #2E7D32; color: #A5D6A7; padding: 8px 12px; font-family: monospace; }}
.data-th {{ background: #1B5E20; color: white; padding: 6px; text-align: left; border: 1px solid #2E7D32; }}
.data-td {{ padding: 6px; border: 1px solid #243524; vertical-align: top; }}
.data-tr-even .data-td {{ background: #131B13; }}
.mermaid {{ background: #0D1610; border: 1px solid #2E7D32; padding: 12px; margin: 10px 0; }}
</style>
</head>
<body>
<div class="hdr-sub">CELIOS - Center of Economic and Law Studies | Laporan Riset Metodologi D3TLH</div>
<div class="hdr-title">BAB IV: Metodologi Analisis Ruang Hidup yang Terampas</div>
<p>Dokumen laporan metodologi ini menyajikan kerangka ilmiah, prosedur pengolahan data, dan pembacaan empiris yang dioperasionalkan pada <strong>Bab 4: Ruang Hidup yang Terampas</strong>.</p>
<h2>4.1 Tren Eskalasi Konflik Agraria Seiring Ekspansi Industri</h2>
<div class="note-box"><strong>Sumber Data Resmi & Deskripsi Visualisasi:</strong> Catatan Konflik Agraria: <code>data/processed/sulawesi_konflik_agraria_tanahkita.csv</code>. Visualisasi dashboard menggunakan Analisis Tren Time-Series.</div>
<h4>A. Pengantar & Kerangka Narasi</h4>
<p>Ekspansi industri ekstraktif dan proyek strategis berimplikasi pada dinamika sosial dan penggunaan lahan masyarakat. Data empiris mencatat akumulasi <strong>{total_konflik:,} kasus konflik agraria</strong>, dengan estimasi <strong>{total_jiwa:,} jiwa terdampak</strong>. Tiga sektor utama (Perkebunan, Kehutanan, dan Pertambangan) menyumbang <strong>{rasio_ekstraktif:.1f}%</strong> dari keseluruhan catatan konflik regional.</p>
<h4>B. Alur Logika Metodologis Analisis Tren Time-Series</h4>
<div class="mermaid">{mermaid_str_4_1}</div>
<h4>C. Formulasi Matematis</h4>
<div class="formula">K_{{t,s}} = Σ c_i, untuk setiap kasus i pada tahun t dan sektor s</div>
<div class="formula">E (%) = ( K_Pasca / K_Pra ) × 100</div>
<div class="formula">E = ({pasca_2005:,} / {pra_2005:,}) × 100 = {lonjakan:,.1f}%</div>
<h4>D. Matriks Hasil Uji Empiris</h4>
<div class="table-caption">Tabel 4.1: Tren Tahunan Konflik Agraria Regional (1990-2025)</div>
{html_table(["Tahun", "Jumlah Konflik"], annual_rows)}
<div class="table-caption">Tabel 4.2: Distribusi Konflik Agraria menurut Sektor Pemicu</div>
{html_table(["Sektor Pemicu", "Jumlah Konflik", "Proporsi"], sector_rows)}
<div class="table-caption">Tabel 4.3: Komposisi Sektor pada Tahun Puncak Insidensi ({peak_year})</div>
{html_table(["Tahun", "Sektor Pemicu", "Jumlah Konflik"], peak_sector_rows)}
<h4>E. Analisis Temuan Empiris</h4>
<p>Grafik time-series pada dashboard memperlihatkan peningkatan insidensi konflik yang memuncak pada tahun <strong>{peak_year}</strong> dengan <strong>{peak_value:,} kasus konflik</strong>. Peningkatan insidensi konflik beririsan dengan dinamika perizinan kawasan.</p>
</body>
</html>
"""
    html_path = tool_dir / "Metodologi_Bab4_Ruang_Hidup.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"  [OK] Tersimpan: {html_path}")

    md_lines = [
        "# BAB IV: METODOLOGI ANALISIS RUANG HIDUP YANG TERAMPAS",
        "",
        "Dokumen laporan metodologi ini menyajikan kerangka ilmiah, prosedur pengolahan data, dan pembacaan empiris yang dioperasionalkan pada **Bab 4: Ruang Hidup yang Terampas**.",
        "",
        "## 4.1 Tren Eskalasi Konflik Agraria Seiring Ekspansi Industri",
        "",
        "> **Sumber Data Resmi & Deskripsi Visualisasi:** Catatan Konflik Agraria: `data/processed/sulawesi_konflik_agraria_tanahkita.csv`. Visualisasi dashboard menggunakan *Analisis Tren Time-Series* untuk melacak eskalasi letupan konflik agraria historis berdasarkan tahun pencatatan dan sektor pemicu.",
        "",
        "#### A. Pengantar & Kerangka Narasi",
        f"Ekspansi industri ekstraktif dan proyek strategis berimplikasi pada dinamika sosial dan penggunaan lahan masyarakat. Data empiris mencatat akumulasi **{total_konflik:,} kasus konflik agraria**, dengan estimasi **{total_jiwa:,} jiwa terdampak** dan **{status_belum_selesai:,} kasus** berstatus belum ditangani.",
        "",
        f"Pada periode pra-2005, sistem pendataan mencatat **{pra_2005:,} kasus** konflik agraria. Pada periode pasca-2005 hingga saat ini, data mencatat **{pasca_2005:,} kasus** konflik lahan, atau setara peningkatan sebesar **{lonjakan:,.1f}%** dibandingkan periode sebelumnya.",
        "",
        "#### B. Alur Logika Metodologis Analisis Tren Time-Series",
        "```mermaid",
        mermaid_str_4_1,
        "```",
        "",
        "#### C. Formulasi Matematis: Agregasi Konflik Tahunan dan Lonjakan Eskalasi",
        "```text",
        "K_{t,s} = Σ c_i, untuk setiap kasus i pada tahun t dan sektor s",
        "E (%) = ( K_Pasca / K_Pra ) × 100",
        f"E = ({pasca_2005:,} / {pra_2005:,}) × 100 = {lonjakan:,.1f}%",
        "```",
        "",
        "#### D. Matriks Hasil Uji Empiris",
        "##### Tabel 4.1: Tren Tahunan Konflik Agraria Regional (1990-2025)",
        markdown_table(["Tahun", "Jumlah Konflik"], annual_rows),
        "",
        "##### Tabel 4.2: Distribusi Konflik Agraria menurut Sektor Pemicu",
        markdown_table(["Sektor Pemicu", "Jumlah Konflik", "Proporsi"], sector_rows),
        "",
        f"##### Tabel 4.3: Komposisi Sektor pada Tahun Puncak Insidensi ({peak_year})",
        markdown_table(["Tahun", "Sektor Pemicu", "Jumlah Konflik"], peak_sector_rows),
        "",
        "#### E. Analisis Temuan Empiris: Puncak Insidensi dan Eskalasi Konflik",
        f"Grafik time-series pada dashboard memperlihatkan peningkatan insidensi konflik yang memuncak pada tahun **{peak_year}** dengan **{peak_value:,} kasus konflik**. Peningkatan insidensi konflik beririsan dengan dinamika perizinan kawasan, sehingga pengelolaan alokasi ruang dan perlindungan hak masyarakat di wilayah investasi menjadi faktor penting untuk meminimalkan dampak sosial.",
        "",
    ]
    md_path = tool_dir / "Metodologi_Bab4_Ruang_Hidup.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print(f"  [OK] Tersimpan: {md_path}")

    print("[4/4] Selesai membangun Bab 4 sub-bab 4.1.")


if __name__ == "__main__":
    generate_all_bab4()
