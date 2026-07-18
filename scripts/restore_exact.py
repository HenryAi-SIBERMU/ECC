import os

history_dir = os.path.expandvars(r'%APPDATA%\Code\User\History')
found_file = ""

for root, dirs, files in os.walk(history_dir):
    if 'entries.json' in files:
        for file in files:
            if file != 'entries.json':
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read(5000)
                        if 'Pembedahan Spasial (Validasi Kehancuran Ekologis):' in content and 'Timbulan Limbah B3 (Realita)' in content and 'Indeks Kualitas Udara (IKU)' in content:
                            print(f"FOUND MATCHING FILE: {full_path}")
                            found_file = full_path
                except Exception:
                    pass

if found_file:
    import shutil
    shutil.copy(found_file, "pages/2_Kualitas_Lingkungan.py")
    print("RESTORED SUCCESSFULLY FROM LOCAL HISTORY!")
else:
    print("Could not find the exact version in history.")
