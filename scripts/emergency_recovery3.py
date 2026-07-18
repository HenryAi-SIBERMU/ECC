import os
import json
import urllib.parse
from datetime import datetime
import shutil

history_dir = os.path.expandvars(r'%APPDATA%\Code\User\History')
recovery_base = os.path.join(os.getcwd(), "EMERGENCY_RECOVERY")
os.makedirs(recovery_base, exist_ok=True)
recovered_count = 0

current_project_dir = os.getcwd().lower()

for root, dirs, files in os.walk(history_dir):
    if 'entries.json' in files:
        entries_path = os.path.join(root, 'entries.json')
        try:
            with open(entries_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                resource = data.get('resource', '')
                parsed_path = urllib.parse.unquote(resource.replace('file:///', '')).replace('/', '\\').lower()
                
                if current_project_dir in parsed_path:
                    # Get the relative path
                    rel_path = parsed_path.replace(current_project_dir + '\\', '')
                    
                    entries = data.get('entries', [])
                    if entries:
                        # Find versions from BEFORE today 10:30 AM local time (which is approx timestamp 1720668600)
                        # We will just grab the latest version of EACH file in the history that is not the EXACT current file
                        entries.sort(key=lambda x: x.get('timestamp', 0), reverse=True)
                        
                        target_dir = os.path.join(recovery_base, os.path.dirname(rel_path))
                        os.makedirs(target_dir, exist_ok=True)
                        
                        for entry in entries[:10]: # save up to 10 recent versions per file
                            ts = entry.get('timestamp', 0) / 1000.0
                            dt = datetime.fromtimestamp(ts)
                            time_str = dt.strftime("%Y-%m-%d_%H-%M-%S")
                            
                            src_file = os.path.join(root, entry['id'])
                            if os.path.exists(src_file):
                                filename = os.path.basename(rel_path)
                                dst_file = os.path.join(target_dir, f"{time_str}_{filename}")
                                shutil.copy(src_file, dst_file)
                        
                        # ALso restore the LATEST version directly to the working directory if it's an uncommitted file
                        # Wait, we don't want to overwrite blindly. We'll just put them in EMERGENCY_RECOVERY.
                        recovered_count += 1
                        print(f"Recovered history for: {rel_path}")
        except Exception as e:
            pass

print(f"Recovered {recovered_count} files' history into EMERGENCY_RECOVERY folder.")
