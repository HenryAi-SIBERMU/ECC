import os
import time
from datetime import datetime

appdata = os.environ.get('APPDATA')
ag_hist = os.path.join(appdata, 'antigravity', 'User', 'History')

if os.path.exists(ag_hist):
    print("Checking Antigravity history for files modified TODAY...")
    today = datetime.now().date()
    
    recent_files = []
    for root, dirs, files in os.walk(ag_hist):
        for f in files:
            path = os.path.join(root, f)
            mtime = os.path.getmtime(path)
            dt = datetime.fromtimestamp(mtime)
            if dt.date() == today:
                recent_files.append((path, dt))
                
    recent_files.sort(key=lambda x: x[1], reverse=True)
    
    print(f"Found {len(recent_files)} files modified today in Antigravity History.")
    
    import json
    for path, dt in recent_files[:20]:
        if 'entries.json' in path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"  {dt.time()} - {data.get('resource')}")
            except:
                pass
