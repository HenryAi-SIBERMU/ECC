import os

appdata = os.environ.get('APPDATA')
for ide in ['Cursor', 'Code', 'VSCodium', 'windsurf', 'antigravity']:
    hist_dir = os.path.join(appdata, ide, 'User', 'History')
    if os.path.exists(hist_dir):
        print(f"Found history dir: {hist_dir}")
        
        # Check how many entries.json files it has
        count = 0
        for root, dirs, files in os.walk(hist_dir):
            if 'entries.json' in files:
                count += 1
        print(f"  -> Contains {count} entries")
