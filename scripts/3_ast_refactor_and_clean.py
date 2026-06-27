import os
import re
import pandas as pd

processed_dir = 'data/processed'
pages_dir = 'pages'

print("=== Phase 3: Eksekusi Fisik (Deletion + Entity Merger + Rerouting) ===\n")

# -----------------------------------------------------------------------
# STEP 1: Entity Merger - STARGATE di sulawesi_esdm_nikel.csv
# -----------------------------------------------------------------------
print("[STEP 1] Menggabungkan entitas STARGATE di sulawesi_esdm_nikel.csv...")
nikel_path = os.path.join(processed_dir, 'sulawesi_esdm_nikel.csv')

df_nikel = pd.read_csv(nikel_path, engine='python', on_bad_lines='skip')

# Cek kolom
entity_col = None
for col in df_nikel.columns:
    if 'nama' in col.lower() and 'perusahaan' in col.lower():
        entity_col = col
        break

if entity_col:
    before_rows = len(df_nikel)
    
    # Tampilkan baris yang akan digabung
    stargate_mask = df_nikel[entity_col].str.upper().str.contains('STARGATE', na=False)
    print(f"  Baris STARGATE ditemukan:")
    print(df_nikel.loc[stargate_mask, [entity_col]].to_string())
    
    # Standarisasi: ganti "STARGATE DUA PASIFIC RESOURCES" -> "STARGATE PASIFIC RESOURCES"
    df_nikel[entity_col] = df_nikel[entity_col].str.replace(
        'STARGATE DUA PASIFIC RESOURCES', 
        'STARGATE PASIFIC RESOURCES', 
        regex=False
    )
    
    # Hapus duplikat baris jika setelah merger ada baris identik
    df_nikel = df_nikel.drop_duplicates()
    after_rows = len(df_nikel)
    
    df_nikel.to_csv(nikel_path, index=False)
    print(f"  Sebelum: {before_rows} baris -> Sesudah: {after_rows} baris")
    print(f"  [OK] sulawesi_esdm_nikel.csv telah diperbarui.\n")
else:
    print("  Kolom entity tidak ditemukan, skip merger.\n")


# -----------------------------------------------------------------------
# STEP 2: Reroute semua referensi di pages/*.py ke file nasional
# -----------------------------------------------------------------------
print("[STEP 2] Memindai pages/*.py untuk mereroute referensi sulawesi_ekspor_2022_2026.csv...")

old_file = 'sulawesi_ekspor_2022_2026.csv'
new_file = 'nasional_ekspor_2022_2026.csv'

rerouted_files = []
for py_file in os.listdir(pages_dir):
    if not py_file.endswith('.py'):
        continue
    
    filepath = os.path.join(pages_dir, py_file)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if old_file in content:
        new_content = content.replace(old_file, new_file)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        rerouted_files.append(py_file)
        print(f"  [REROUTED] {py_file}: '{old_file}' -> '{new_file}'")

if not rerouted_files:
    print("  Tidak ada referensi ke sulawesi_ekspor_2022_2026.csv di folder pages/.")

# Also check Home.py / src/ if exist
for extra_file in ['Home.py']:
    if os.path.exists(extra_file):
        with open(extra_file, 'r', encoding='utf-8') as f:
            content = f.read()
        if old_file in content:
            new_content = content.replace(old_file, new_file)
            with open(extra_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            rerouted_files.append(extra_file)
            print(f"  [REROUTED] {extra_file}: '{old_file}' -> '{new_file}'")


# -----------------------------------------------------------------------
# STEP 3: Hapus file redundan
# -----------------------------------------------------------------------
print(f"\n[STEP 3] Menghapus file redundan: {old_file}...")
old_path = os.path.join(processed_dir, old_file)

if os.path.exists(old_path):
    os.remove(old_path)
    print(f"  [DELETED] {old_path}")
else:
    print(f"  File {old_file} tidak ditemukan, skip.")

print("\n=== Eksekusi Fase 3 Selesai ===")
print(f"  Entitas merger: STARGATE DUA PASIFIC RESOURCES -> STARGATE PASIFIC RESOURCES")
print(f"  File dihapus: {old_file}")
print(f"  Rerouted di pages: {rerouted_files if rerouted_files else 'Tidak ada'}")
