import os
import glob

history_dir = os.path.expandvars(r'%APPDATA%\Code\User\History')
print(f"Checking {history_dir}...")
if os.path.exists(history_dir):
    print("VS Code Local History found!")
else:
    print("VS Code Local History NOT found.")
