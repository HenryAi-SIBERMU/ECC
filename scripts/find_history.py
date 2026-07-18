import os
import glob
import time

history_dir = os.path.expandvars(r'%APPDATA%\Code\User\History')
# pages/2_Kualitas_Lingkungan.py has a specific hash or we can just search all entries
all_files = []
for root, dirs, files in os.walk(history_dir):
    if 'entries.json' in files:
        for file in files:
            if file != 'entries.json':
                full_path = os.path.join(root, file)
                all_files.append((full_path, os.path.getmtime(full_path)))

# Sort by modification time, newest first
all_files.sort(key=lambda x: x[1], reverse=True)

found_versions = []
for file_path, mtime in all_files[:200]: # Check the 200 most recent history files
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read(1000) # Read just beginning to identify
            if 'import streamlit as st' in content and 'Kualitas_Lingkungan' in content or 'fig_map1' in content:
                found_versions.append((file_path, mtime))
    except Exception:
        pass

for i, (path, mtime) in enumerate(found_versions[:10]):
    print(f"{i+1}. {time.ctime(mtime)} - {path}")
