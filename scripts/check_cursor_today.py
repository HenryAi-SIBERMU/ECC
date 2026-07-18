import os
import time
from datetime import datetime

appdata = os.environ.get('APPDATA')
cursor_hist = os.path.join(appdata, 'Cursor', 'User', 'History')

if os.path.exists(cursor_hist):
    print("Checking Cursor history for files modified TODAY...")
    today = datetime.now().date()
    
    recent_files = []
    for root, dirs, files in os.walk(cursor_hist):
        for f in files:
            path = os.path.join(root, f)
            mtime = os.path.getmtime(path)
            dt = datetime.fromtimestamp(mtime)
            if dt.date() == today:
                recent_files.append((path, dt))
                
    recent_files.sort(key=lambda x: x[1], reverse=True)
    
    print(f"Found {len(recent_files)} files modified today in Cursor History.")
