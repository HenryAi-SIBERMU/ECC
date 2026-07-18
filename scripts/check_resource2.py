import os
import json
import urllib.parse

history_dir = os.path.expandvars(r'%APPDATA%\Code\User\History')

for root, dirs, files in os.walk(history_dir):
    if 'entries.json' in files:
        entries_path = os.path.join(root, 'entries.json')
        try:
            with open(entries_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                resource = data.get('resource', '')
                if 'celios2' in resource.lower():
                    parsed = urllib.parse.unquote(resource.replace('file:///', '')).replace('/', '\\').lower()
                    print("Found celios2 resource:", resource)
                    print("Parsed to:", parsed)
                    print("Current dir:", os.getcwd().lower())
                    break
        except Exception:
            pass
