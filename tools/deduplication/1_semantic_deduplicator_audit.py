"""
tools/deduplication/1_semantic_deduplicator_audit.py
====================================================
Phase 1: LSH & Semantic Redundancy Audit

Memindai seluruh file CSV di data/processed/ untuk mendeteksi:
A. Byte-level Hash Check (SHA-256) - duplikat absolut
B. Semantic Schema & Subset Match - file yang 100% isinya terkandung di file lain

Mode: DRY-RUN (tidak ada file yang dihapus atau dimodifikasi)
Output: data/audit_redundansi.json
"""

import os
import sys
import pandas as pd
import hashlib
import json

# Sesuaikan base path relatif ke root project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
processed_dir = os.path.join(BASE_DIR, 'data', 'processed')

files = sorted([f for f in os.listdir(processed_dir) if f.endswith('.csv')])
print(f"Total file CSV ditemukan: {len(files)}\n")

# -----------------------------------------------------------------------
# A. Byte-Level & Hash Check (Absolute Duplication)
# -----------------------------------------------------------------------
print("=== A. Byte-Level & Hash Check ===")
file_hashes = {}
duplicate_bytes = []

for f in files:
    path = os.path.join(processed_dir, f)
    with open(path, 'rb') as fh:
        file_hash = hashlib.sha256(fh.read()).hexdigest()
        if file_hash in file_hashes:
            duplicate_bytes.append({'file': f, 'identical_to': file_hashes[file_hash]})
            print(f"[!] ABSOLUTE DUPLICATE: {f} == {file_hashes[file_hash]}")
        else:
            file_hashes[file_hash] = f

if not duplicate_bytes:
    print("Tidak ditemukan duplikat absolut (byte-level).\n")

# -----------------------------------------------------------------------
# B. Semantic Schema & Subset Match
# -----------------------------------------------------------------------
print("=== B. Semantic Schema & Subset Match ===")
dataframes = {}

for f in files:
    path = os.path.join(processed_dir, f)
    try:
        dataframes[f] = pd.read_csv(path, engine='python', on_bad_lines='skip')
    except Exception as e:
        print(f"Error membaca {f}: {e}")

subset_redundancies = []
file_list = list(dataframes.keys())

for i in range(len(file_list)):
    for j in range(i + 1, len(file_list)):
        f1, f2 = file_list[i], file_list[j]
        df1, df2 = dataframes[f1], dataframes[f2]

        if set(df1.columns) == set(df2.columns):
            df1_str = df1.astype(str)
            df2_str = df2.astype(str)

            merged1 = pd.merge(df1_str, df2_str, how='inner')
            if len(merged1) == len(df1_str) and len(df1_str) < len(df2_str):
                subset_redundancies.append({'redundant_file': f1, 'master_file': f2})
                print(f"[!] SUBSET: {f1} 100% terkandung di {f2}")

            merged2 = pd.merge(df2_str, df1_str, how='inner')
            if len(merged2) == len(df2_str) and len(df2_str) < len(df1_str):
                subset_redundancies.append({'redundant_file': f2, 'master_file': f1})
                print(f"[!] SUBSET: {f2} 100% terkandung di {f1}")

if not subset_redundancies:
    print("Tidak ditemukan relasi subset antar file.\n")

# -----------------------------------------------------------------------
# Output JSON Report
# -----------------------------------------------------------------------
audit_report = {
    'absolute_duplicates_byte_level': duplicate_bytes,
    'subset_redundancies': subset_redundancies,
}

output_path = os.path.join(BASE_DIR, 'data', 'audit_redundansi.json')
with open(output_path, 'w') as fh:
    json.dump(audit_report, fh, indent=4)

print(f"\n[INFO] Laporan audit disimpan ke: {output_path}")
