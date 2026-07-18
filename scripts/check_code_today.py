import os
import time
from datetime import datetime

appdata = os.environ.get('APPDATA')
code_hist = os.path.join(appdata, 'Code', 'User', 'History')

if os.path.exists(code_hist):
    print("Checking VS Code history for files modified TODAY...")
    today = datetime.now().date()
    
    recent_files = []
    for root, dirs, files in os.walk(code_hist):
        for f in files:
            path = os.path.join(root, f)
            mtime = os.path.getmtime(path)
            dt = datetime.fromtimestamp(mtime)
            if dt.date() == today:
                recent_files.append((path, dt))
                
    recent_files.sort(key=lambda x: x[1], reverse=True)
    
    print(f"Found {len(recent_files)} files modified today in VS Code History.")
