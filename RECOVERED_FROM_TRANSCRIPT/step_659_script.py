import os
import json
import shutil
import urllib.parse
from datetime import datetime, timedelta

history_dir = os.path.expandvars(r'%APPDATA%\Code\User\History')
project_str = "celios2"
recovered = []

now = datetime.now().timestamp()
two_days_ago = now - (3 * 24 * 3600) # last 3 days

for root, dirs, files in os.walk(history_dir):
    if 'entries.json' in files:
        entries_path = os.path.join(root, 'entries.json')
        try:
            with open(entries_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                resource = data.get('resource', '')
                
                # Loose matching for our project folder
                if 'celios2' in resource.lower() and 'duniahub' in resource.lower():
                    # Parse path
                    parsed = urllib.parse.unquote(resource.replace('file:///', ''))
                    # e.g., c:/Users/yooma/OneDrive/Desktop/duniahub/client/4. Celios2/pages/2_Kualitas_Lingkungan.py
                    
                    # Split at "Celios2" to get the relative path inside the project
                    if 'celios2/' in parsed.lower():
                        rel_path = parsed.lower().split('celios2/')[1]
                    elif 'celios2\\' in parsed.lower():
                        rel_path = parsed.lower().split('celios2\\')[1]
                    else:
                        continue # Couldn't parse
                        
                    # find the entry from right BEFORE my git reset (which was around 10:30 AM local time today)
                    # Actually, the user wants their 2 days of work back. Let's just grab the most recent version 
                    # that is from BEFORE my destructive actions, or just the absolute latest if they didn't edit it since my reset.
                    # Wait, my destructive action was git reset, which OVERWROTE files. So VS Code might have saved the git reset version!
                    # We need the version from right BEFORE the git reset. The git reset happened at approx 10:31 AM (current time is 10:36 AM).
                    
                    entries = data.get('entries', [])
                    if entries:
                        # Find the newest entry that is older than 10 minutes ago
                        # Or just dump the last 5 versions to a recovery folder!
                        
                        target_file_to_save = os.path.join(os.getcwd(), rel_path)
                        recovery_dir = os.path.join(os.getcwd(), "RECOVERY_" + rel_path.replace('/', '_').replace('\\', '_'))
                        os.makedirs(recovery_dir, exist_ok=True)
                        
                        for idx, entry in enumerate(sorted(entries, key=lambda x: x.get('timestamp', 0), reverse=True)[:5]):
                            ts = entry.get('timestamp', 0) / 1000.0 # ms to seconds
                            dt = datetime.fromtimestamp(ts)
                            
                            src_file = os.path.join(root, entry['id'])
                            if os.path.exists(src_file):
                                time_str = dt.strftime("%Y%m%d_%H%M%S")
                                dst_file = os.path.join(recovery_dir, f"version_{time_str}_{entry['id']}.txt")
                                shutil.copy(src_file, dst_file)
                        
                        recovered.append(rel_path)
        except Exception as e:
            pass

print(f"Scanned and exported history for {len(recovered)} files to RECOVERY_ folders.")