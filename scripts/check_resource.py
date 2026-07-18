import os
import json

history_dir = os.path.expandvars(r'%APPDATA%\Code\User\History')
found_one = False
for root, dirs, files in os.walk(history_dir):
    if 'entries.json' in files:
        entries_path = os.path.join(root, 'entries.json')
        try:
            with open(entries_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                resource = data.get('resource', '')
                if 'Celios2' in resource or 'celios2' in resource or 'duniahub' in resource:
                    print("Found resource string example:", resource)
                    found_one = True
                    break
        except Exception:
            pass
    if found_one:
        break
