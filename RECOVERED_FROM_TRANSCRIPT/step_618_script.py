import os
import glob
import time

history_dir = os.path.expandvars(r'%APPDATA%\Code\User\History')
all_files = []
for root, dirs, files in os.walk(history_dir):
    if 'entries.json' in files:
        for file in files:
            if file != 'entries.json':
                full_path = os.path.join(root, file)
                all_files.append((full_path, os.path.getmtime(full_path)))

all_files.sort(key=lambda x: x[1], reverse=True)

found_versions = []
for file_path, mtime in all_files[:500]: # Check 500
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(5000) 
            # Looking for 2_Kualitas_Lingkungan.py specifically
            if '2. Kualitas Udara (IKU)' in content or 'Indeks Kualitas Lingkungan Hidup' in content or 'Kepungan Asap: Kapasitas PLTU' in content:
                found_versions.append((file_path, mtime))
    except Exception:
        pass

for i, (path, mtime) in enumerate(found_versions[:15]):
    print(f"{i+1}. {time.ctime(mtime)} - {path}")