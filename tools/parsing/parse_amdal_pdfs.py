"""
Parse AMDAL PDFs - Ekstraktor Limbah B3 Berbasis Satuan + Tabel
================================================================
Strategi duplikat:
1. Ekstrak TABEL (pdfplumber) -> Cari kolom/baris yang mengandung satuan limbah
2. Fallback teks -> Regex satuan, 1 nilai = 1 baris

Keyword pencarian hanya untuk parameter fisik/kimia lingkungan:
- tailing, slag, limbah b3, efluen, logam berat, residu, slurry

BUKAN kata dokumen seperti 'amdal', 'rkl-rpl', 'izin' dsb.

Output: data/processed/amdal_parsed_limbah_b3_v2.csv
Kolom:
    file | perusahaan | kategori_sumber | asal_ekstraksi
    keyword_konteks | jenis_besaran | nilai | satuan | satuan_kode | snippet
"""

import os
import re
import csv
from pathlib import Path

try:
    import pdfplumber
    PDF_ENGINE = 'pdfplumber'
except ImportError:
    PDF_ENGINE = None

try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False

BASE_DIR = Path(__file__).resolve().parent.parent.parent
INPUT_DIR  = BASE_DIR / 'data' / 'raw' / 'amdal_leaks'
OUTPUT_CSV = BASE_DIR / 'data' / 'processed' / 'amdal_parsed_limbah_b3_v2.csv'

# ---------------------------------------------------------------
# 1. MAP KATEGORI SUMBER
# ---------------------------------------------------------------
file_category_map = {}
dir_cat = [
    (INPUT_DIR / 'official_amdal', 'Official AMDAL'),
    (INPUT_DIR / 'ngo_reports', 'NGO Report'),
    (INPUT_DIR / 'corporate_reports', 'Corporate Report'),
    (INPUT_DIR / 'academic_reports', 'Academic Report'),
    (INPUT_DIR / 'other_reports', 'Other'),
]
for d, cat in dir_cat:
    if d.exists():
        for f in d.glob('*.pdf'):
            file_category_map[f.name] = cat

# ---------------------------------------------------------------
# 2. DEFINISI SATUAN + KATEGORI (dari tabel user)
# ---------------------------------------------------------------
UNIT_DEFS = [
    # (regex_pattern, jenis_besaran, satuan_kode)
    # --- Massa ---
    (r'(\d[\d.,]*)\s*(juta\s+ton)',           'Massa',   'Mt'),
    (r'(\d[\d.,]*)\s*(ribu\s+ton)',            'Massa',   'Ribu Ton'),
    (r'(\d[\d.,]*)\s*(ton/tahun|ton\s+per\s+tahun)', 'Laju', 'ton/tahun'),
    (r'(\d[\d.,]*)\s*(ton)',                   'Massa',   'ton'),
    (r'(\d[\d.,]*)\s*(kg|kilogram)',           'Massa',   'kg'),
    # --- Volume ---
    (r'(\d[\d.,]*)\s*(m3/hari|m\^3/hari)',    'Laju Cairan','m3/hari'),
    (r'(\d[\d.,]*)\s*(m3|m\^3|meter\s*kubik)','Volume',  'm3'),
    (r'(\d[\d.,]*)\s*(liter\b)',               'Volume',  'L'),
    # --- Konsentrasi ---
    (r'(\d[\d.,]*)\s*(ppm)',                  'Konsentrasi', 'ppm'),
    (r'(\d[\d.,]*)\s*(mg/l)',                 'Konsentrasi', 'mg/L'),
    (r'(\d[\d.,]*)\s*(mg/kg)',                'Konsentrasi', 'mg/kg'),
    # --- Emisi Udara ---
    (r'(\d[\d.,]*)\s*(mg/nm3)',               'Emisi Udara', 'mg/Nm3'),
    (r'(\d[\d.,]*)\s*(µg/nm3|ug/nm3)',        'Emisi Udara', 'µg/Nm3'),
    # --- Kualitas Air/Lingkungan ---
    (r'(\d[\d.,]*)\s*(ntu)',                  'Kualitas Air', 'NTU'),
    (r'(\d[\d.,]*)\s*(dba)',                  'Kebisingan',  'dBA'),
    (r'(\d[\d.,]*)\s*(mm/sec)',               'Getaran',     'mm/sec'),
    (r'(\d[\d.,]*)\s*(mpn/100ml)',            'Kualitas Air', 'MPN/100mL'),
    # --- Area ---
    (r'(\d[\d.,]*)\s*(ha\b|hektar)',          'Area', 'Ha'),
]
COMPILED_UNITS = [(re.compile(p, re.IGNORECASE), jenis, satuan) for p, jenis, satuan in UNIT_DEFS]

# ---------------------------------------------------------------
# 3. KEYWORD UNTUK KONTEKS (HANYA PARAMETER FISIK/KIMIA)
# ---------------------------------------------------------------
KEYWORDS = [
    'tailing', 'slag', 'limbah b3', 'limbah bahan berbahaya',
    'tsf', 'tailings storage', 'tailings dam',
    'efluen', 'air limbah', 'slurry', 'residu',
    'logam berat', 'chromium', 'merkuri', 'sianida',
    'air asam tambang', 'acid mine drainage',
    'deep sea tailings', 'dstp',
]

# ---------------------------------------------------------------
# 4. HELPER FUNCTIONS
# ---------------------------------------------------------------
def to_float(s):
    try:
        return float(s.replace('.', '').replace(',', '.'))
    except:
        try:
            return float(s.replace(',', ''))
        except:
            return None

def extract_text_pages(pdf_path, max_pages=30):
    """Ekstrak list teks per halaman."""
    pages = []
    if PDF_ENGINE == 'pdfplumber':
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages[:max_pages]:
                    t = page.extract_text()
                    if t: pages.append(t)
        except: pass
    if not pages and PYPDF2_AVAILABLE:
        try:
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages[:max_pages]:
                    t = page.extract_text()
                    if t: pages.append(t)
        except: pass
    return pages

def extract_tables_from_pdf(pdf_path, max_pages=30):
    """Ekstrak semua tabel dari PDF menggunakan pdfplumber."""
    tables = []
    if PDF_ENGINE != 'pdfplumber':
        return tables
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages[:max_pages]:
                for tbl in page.extract_tables():
                    if tbl:
                        tables.append(tbl)
    except:
        pass
    return tables

def parse_value_unit(text):
    """Ekstrak SEMUA pasangan nilai+satuan dari teks, return list of (nilai_float, satuan_kode, jenis_besaran, matched_str)."""
    results = []
    for regex, jenis, satuan_kode in COMPILED_UNITS:
        for m in regex.finditer(text):
            num_str = m.group(1)
            val = to_float(num_str)
            if val is not None and val > 0:
                results.append({
                    'nilai': val,
                    'nilai_raw': num_str.strip(),
                    'satuan': m.group(2).strip().lower(),
                    'satuan_kode': satuan_kode,
                    'jenis_besaran': jenis,
                    'matched_str': m.group(0).strip()
                })
    # Deduplicate
    seen = set()
    deduped = []
    for r in results:
        key = (round(r['nilai'], 2), r['satuan_kode'])
        if key not in seen:
            seen.add(key)
            deduped.append(r)
    return deduped

def has_b3_keyword(text):
    text_low = text.lower()
    return any(kw in text_low for kw in KEYWORDS)

def find_keyword_in_text(text):
    text_low = text.lower()
    for kw in KEYWORDS:
        if kw in text_low:
            return kw
    return ''

# ---------------------------------------------------------------
# 5. MAIN PARSE FUNCTION
# ---------------------------------------------------------------
def parse_all_pdfs():
    all_pdf_files = list(INPUT_DIR.rglob('*.pdf'))
    if not all_pdf_files:
        print("[!] Tidak ada PDF ditemukan.")
        return

    rows = []
    fieldnames = ['file', 'perusahaan', 'kategori_sumber', 'asal_ekstraksi',
                  'keyword_konteks', 'jenis_besaran', 'nilai', 'satuan_kode',
                  'snippet']

    for i, pdf_path in enumerate(all_pdf_files, 1):
        fname = pdf_path.name
        cat_sumber = file_category_map.get(fname, 'Unknown')
        # Tebak nama perusahaan dari nama file
        stem_parts = pdf_path.stem.split('_')
        company_guess = ' '.join(stem_parts[:-1]).upper() if len(stem_parts) > 1 else pdf_path.stem.upper()

        print(f"[{i}/{len(all_pdf_files)}] Parsing: {fname}")

        # --- STRATEGI 1: Ekstrak Tabel ---
        tables_found = 0
        tables = extract_tables_from_pdf(pdf_path)
        for tbl in tables:
            # Flatten tabel jadi satu string untuk cek keyword
            flat_rows = [' '.join(str(c) for c in row if c) for row in tbl]
            tbl_text = ' '.join(flat_rows)
            if not has_b3_keyword(tbl_text):
                continue
            # Jika relevan, parse tiap sel
            for row_cells in tbl:
                row_text = ' '.join(str(c) for c in row_cells if c)
                if not has_b3_keyword(row_text):
                    continue
                kw_hit = find_keyword_in_text(row_text)
                extractions = parse_value_unit(row_text)
                for ext in extractions:
                    tables_found += 1
                    rows.append({
                        'file': fname,
                        'perusahaan': company_guess,
                        'kategori_sumber': cat_sumber,
                        'asal_ekstraksi': 'TABEL',
                        'keyword_konteks': kw_hit,
                        'jenis_besaran': ext['jenis_besaran'],
                        'nilai': ext['nilai_raw'],
                        'satuan_kode': ext['satuan_kode'],
                        'snippet': row_text[:300].replace('\n', ' ')
                    })
        if tables_found > 0:
            print(f"    [TABEL] {tables_found} nilai dari tabel")

        # --- STRATEGI 2: Teks (per keyword match) ---
        pages = extract_text_pages(pdf_path)
        if not pages:
            continue
        full_text = '\n'.join(pages)
        full_text_low = full_text.lower()
        text_found = 0

        for keyword in KEYWORDS:
            idx = 0
            while True:
                pos = full_text_low.find(keyword, idx)
                if pos == -1:
                    break
                start = max(0, pos - 250)
                end = min(len(full_text), pos + 250)
                snippet = full_text[start:end].replace('\n', ' ')
                snippet = re.sub(r'\s{2,}', ' ', snippet).strip()

                extractions = parse_value_unit(snippet)
                for ext in extractions:
                    text_found += 1
                    rows.append({
                        'file': fname,
                        'perusahaan': company_guess,
                        'kategori_sumber': cat_sumber,
                        'asal_ekstraksi': 'TEKS',
                        'keyword_konteks': keyword,
                        'jenis_besaran': ext['jenis_besaran'],
                        'nilai': ext['nilai_raw'],
                        'satuan_kode': ext['satuan_kode'],
                        'snippet': snippet[:300]
                    })
                idx = pos + len(keyword)

        if text_found > 0:
            print(f"    [TEKS ] {text_found} nilai dari teks")

    # Tulis CSV
    # Deduplicate berdasarkan (file, nilai, satuan_kode, keyword)
    seen = set()
    final_rows = []
    for r in rows:
        key = (r['file'], r['nilai'], r['satuan_kode'], r['keyword_konteks'])
        if key not in seen:
            seen.add(key)
            final_rows.append(r)

    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(final_rows)

    print(f"\n{'='*55}")
    print(f"[SELESAI] {len(final_rows)} baris (1 nilai = 1 baris).")
    print(f"[OUTPUT ] {OUTPUT_CSV}")

if __name__ == "__main__":
    parse_all_pdfs()
