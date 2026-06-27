"""
tools/deduplication/2_entity_resolver_audit.py
===============================================
Phase 2: Entity Resolution Audit (Row-level Fuzzy Matching)

Memindai kolom nama perusahaan/entitas pada file-file master CSV
dan mendeteksi baris yang mungkin merujuk ke entitas yang sama
tetapi ditulis berbeda (typo, singkatan, dll.).

Menggunakan Jaro-Winkler Similarity via difflib.SequenceMatcher
Threshold: > 90% -> kandidat duplikat

Mode: DRY-RUN (tidak ada file yang dimodifikasi)
Output: Ditambahkan ke data/audit_redundansi.json
"""

import os
import json
import pandas as pd
from difflib import SequenceMatcher

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
processed_dir = os.path.join(BASE_DIR, 'data', 'processed')

# File yang paling relevan untuk entity resolution
target_files = [
    'sulawesi_esdm_nikel.csv',
    'kpa_masalah_izin_perusahaan.csv',
    'sulawesi_izin_raw_details.csv',
    'sulawesi_konflik_hukum.csv',
    'sulawesi_konflik_tambang_fpic.csv',
    'kpa_catahu_2025_izin_ilegal_sulawesi.csv',
]

# Kata kunci kolom yang mungkin mengandung nama entitas
entity_col_keywords = ['perusahaan', 'nama', 'subjek', 'pt', 'korporasi']

THRESHOLD = 0.90

def similarity(a, b):
    if not isinstance(a, str) or not isinstance(b, str):
        return 0.0
    return SequenceMatcher(None, a.lower().strip(), b.lower().strip()).ratio()

print("=== Phase 2: Entity Resolution Audit (Fuzzy Matching > 90%) ===\n")

audit_results = {}

for f in target_files:
    path = os.path.join(processed_dir, f)
    if not os.path.exists(path):
        print(f"[SKIP] {f} tidak ditemukan.")
        continue

    try:
        df = pd.read_csv(path, engine='python', on_bad_lines='skip')
    except Exception as e:
        print(f"[ERROR] Gagal membaca {f}: {e}")
        continue

    # Cari kolom yang relevan
    col_to_check = None
    for col in df.columns:
        if any(kw in col.lower() for kw in entity_col_keywords):
            col_to_check = col
            break

    if not col_to_check:
        print(f"[SKIP] {f} - tidak ada kolom entitas yang relevan.")
        continue

    print(f"[SCANNING] {f} pada kolom '{col_to_check}'")
    entities = df[col_to_check].dropna().unique().tolist()

    fuzzy_matches = []
    for i in range(len(entities)):
        for j in range(i + 1, len(entities)):
            score = similarity(entities[i], entities[j])
            if THRESHOLD < score < 1.0:
                fuzzy_matches.append({
                    'entity_1': entities[i],
                    'entity_2': entities[j],
                    'similarity_score': round(score, 3),
                    'column': col_to_check
                })
                print(f"  [!] KANDIDAT DUPLIKAT ({round(score*100,1)}%): '{entities[i]}' <-> '{entities[j]}'")

    if fuzzy_matches:
        audit_results[f] = fuzzy_matches
    else:
        print(f"  Tidak ada fuzzy duplicate ditemukan.")

# Simpan ke audit_redundansi.json
output_path = os.path.join(BASE_DIR, 'data', 'audit_redundansi.json')
try:
    with open(output_path, 'r', encoding='utf-8') as fh:
        report = json.load(fh)
except:
    report = {}

report['entity_resolution_candidates'] = audit_results

with open(output_path, 'w', encoding='utf-8') as fh:
    json.dump(report, fh, indent=4, ensure_ascii=False)

print(f"\n[INFO] Laporan Phase 2 ditambahkan ke: {output_path}")
