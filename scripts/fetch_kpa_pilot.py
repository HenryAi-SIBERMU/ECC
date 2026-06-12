"""
PILOT SCRIPT: KPA Catatan Akhir Tahun -- PDF Parser
Target : Ekstrak data konflik agraria per provinsi Sulawesi
File   : data/raw/kpa_ylbhi/catahu-2016-...pdf
Output : Disimpan ke pilot_output_2016.txt untuk review
"""

import pdfplumber
import re
import os

PILOT_PDF = os.path.join(
    "data", "raw", "kpa_ylbhi",
    "catahu-2016-liberalisasi-agraria-diperhebat-reforma-agraria-dibelokkan.pdf"
)

SULAWESI_KEYWORDS = [
    "Sulawesi Selatan", "Sulawesi Tengah", "Sulawesi Utara",
    "Sulawesi Tenggara", "Sulawesi Barat", "Gorontalo",
    "Sulsel", "Sulteng", "Sulut", "Sultra", "Sulbar"
]

KONFLIK_KEYWORDS = [
    "konflik", "letusan", "luas", "lahan", "kriminalisasi",
    "kekerasan", "korban", "warga", "petani", "hektar"
]

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def contains_keyword(text, keywords):
    text_lower = text.lower()
    return any(kw.lower() in text_lower for kw in keywords)

def parse_pilot_pdf(pdf_path):
    sep  = "=" * 70
    line = "-" * 70

    out = []
    out.append(sep)
    out.append("[PILOT] PARSING: " + os.path.basename(pdf_path))
    out.append(sep)

    if not os.path.exists(pdf_path):
        out.append("[ERROR] File tidak ditemukan: " + pdf_path)
        print('\n'.join(out))
        return

    sulawesi_pages    = []
    tables_found      = []
    sulawesi_snippets = []

    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        out.append("Total halaman: " + str(total_pages))
        out.append("Scanning untuk kata kunci Sulawesi...\n")

        for i, page in enumerate(pdf.pages):
            page_num = i + 1
            text = page.extract_text() or ""

            if contains_keyword(text, SULAWESI_KEYWORDS):
                sulawesi_pages.append(page_num)
                for sentence in text.split('.'):
                    if contains_keyword(sentence, SULAWESI_KEYWORDS):
                        snippet = clean_text(sentence)
                        if len(snippet) > 20:
                            sulawesi_snippets.append({
                                "halaman": page_num,
                                "teks": snippet[:300]
                            })

            if contains_keyword(text, KONFLIK_KEYWORDS) or contains_keyword(text, SULAWESI_KEYWORDS):
                tables = page.extract_tables()
                if tables:
                    for table in tables:
                        if table and len(table) > 1:
                            tables_found.append({
                                "halaman": page_num,
                                "tabel": table
                            })

    out.append(line)
    out.append("[HALAMAN SULAWESI] Ditemukan di " + str(len(sulawesi_pages)) + " halaman")
    out.append("  -> " + str(sulawesi_pages))

    out.append("\n" + line)
    out.append("[KUTIPAN TEKS SULAWESI] " + str(len(sulawesi_snippets)) + " snippet:")
    for s in sulawesi_snippets[:30]:
        out.append("\n  [Hal." + str(s['halaman']) + "] " + s['teks'])

    out.append("\n" + line)
    out.append("[TABEL KONFLIK/SULAWESI] Ditemukan " + str(len(tables_found)) + " tabel:")
    for idx, t in enumerate(tables_found[:15]):
        out.append("\n  --- Tabel #" + str(idx+1) + " (Hal. " + str(t['halaman']) + ") ---")
        for row in t['tabel'][:10]:
            cleaned = [clean_text(str(cell)) if cell else "-" for cell in row]
            out.append("  " + " | ".join(cleaned))
        if len(t['tabel']) > 10:
            out.append("  ... (+" + str(len(t['tabel'])-10) + " baris lagi)")

    out.append("\n" + sep)
    out.append("[SELESAI] Silakan review file output.")
    out.append(sep)

    out_file = os.path.join("data", "raw", "kpa_ylbhi", "pilot_output_2016.txt")
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))

    print("[OK] Output disimpan ke: " + out_file)
    print("     Halaman Sulawesi : " + str(len(sulawesi_pages)))
    print("     Snippet teks     : " + str(len(sulawesi_snippets)))
    print("     Tabel ditemukan  : " + str(len(tables_found)))

if __name__ == "__main__":
    parse_pilot_pdf(PILOT_PDF)
