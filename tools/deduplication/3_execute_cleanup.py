"""
tools/deduplication/3_execute_cleanup.py
=========================================
Phase 3: Eksekusi Fisik (Safe Deletion + Entity Merger + AST Rerouting)

PERINGATAN: Skrip ini bersifat DESTRUKTIF.
Jalankan HANYA setelah meninjau laporan audit di data/audit_redundansi.json
dan mendapat persetujuan eksplisit dari pemilik data.

Tindakan yang dilakukan:
  1. Merger entitas fuzzy (nama perusahaan yang hampir identik)
  2. Reroute semua referensi pd.read_csv() di pages/*.py ke file master
  3. Hapus file redundan dari data/processed/

Mode: LIVE (perubahan permanen)
"""

import os
import json
import re
import pandas as pd
from difflib import SequenceMatcher

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
processed_dir = os.path.join(BASE_DIR, 'data', 'processed')
pages_dir = os.path.join(BASE_DIR, 'pages')
audit_path = os.path.join(BASE_DIR, 'data', 'audit_redundansi.json')

print("=== Phase 3: Eksekusi Fisik ===\n")

# Muat laporan audit
try:
    with open(audit_path, 'r', encoding='utf-8') as fh:
        audit_report = json.load(fh)
except FileNotFoundError:
    print("[ERROR] File audit_redundansi.json tidak ditemukan.")
    print("        Jalankan Phase 1 & 2 terlebih dahulu.")
    exit(1)

# -----------------------------------------------------------------------
# STEP 1: Entity Merger (berdasarkan entity_resolution_candidates)
# -----------------------------------------------------------------------
print("[STEP 1] Entity Merger (Fuzzy Match > 90%) ...")
entity_candidates = audit_report.get('entity_resolution_candidates', {})

for filename, matches in entity_candidates.items():
    filepath = os.path.join(processed_dir, filename)
    if not os.path.exists(filepath):
        print(f"  [SKIP] {filename} tidak ditemukan.")
        continue

    df = pd.read_csv(filepath, engine='python', on_bad_lines='skip')

    for match in matches:
        col = match['column']
        e1 = match['entity_1']
        e2 = match['entity_2']

        # Pertahankan entitas yang lebih pendek (lebih ringkas)
        canonical = e1 if len(e1) <= len(e2) else e2
        to_replace = e2 if len(e1) <= len(e2) else e1

        if col in df.columns:
            count = df[col].eq(to_replace).sum()
            df[col] = df[col].str.replace(to_replace, canonical, regex=False)
            print(f"  [MERGE] {filename}[{col}]: '{to_replace}' -> '{canonical}' ({count} baris)")

    df = df.drop_duplicates()
    df.to_csv(filepath, index=False)
    print(f"  [SAVED] {filename} diperbarui.\n")

# -----------------------------------------------------------------------
# STEP 2: Reroute pd.read_csv() di pages/*.py
# -----------------------------------------------------------------------
print("[STEP 2] Rerouting referensi file di pages/*.py ...")
subset_list = audit_report.get('subset_redundancies', [])

for entry in subset_list:
    redundant = entry['redundant_file']
    master = entry['master_file']

    for py_file in os.listdir(pages_dir):
        if not py_file.endswith('.py'):
            continue

        filepath = os.path.join(pages_dir, py_file)
        with open(filepath, 'r', encoding='utf-8') as fh:
            content = fh.read()

        if redundant in content:
            new_content = content.replace(redundant, master)
            with open(filepath, 'w', encoding='utf-8') as fh:
                fh.write(new_content)
            print(f"  [REROUTED] {py_file}: '{redundant}' -> '{master}'")

# -----------------------------------------------------------------------
# STEP 3: Hapus file redundan
# -----------------------------------------------------------------------
print("\n[STEP 3] Menghapus file redundan ...")

for entry in subset_list:
    redundant = entry['redundant_file']
    redundant_path = os.path.join(processed_dir, redundant)

    if os.path.exists(redundant_path):
        os.remove(redundant_path)
        print(f"  [DELETED] {redundant_path}")
    else:
        print(f"  [SKIP] {redundant} tidak ditemukan (mungkin sudah dihapus).")

print("\n=== Eksekusi Phase 3 Selesai ===")
print("Jalankan dashboard Streamlit untuk memverifikasi tidak ada error.")
