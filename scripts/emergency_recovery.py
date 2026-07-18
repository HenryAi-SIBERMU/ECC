import os
import json
import shutil
import urllib.parse

history_dir = os.path.expandvars(r'%APPDATA%\Code\User\History')
project_path_str = "duniahub/client/4. Celios2".lower()
recovered_count = 0

print("Scanning VS Code Local History for lost files...")

# Find all entries.json
for root, dirs, files in os.walk(history_dir):
    if 'entries.json' in files:
        entries_path = os.path.join(root, 'entries.json')
        try:
            with open(entries_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                resource = data.get('resource', '')
                
                # Check if it belongs to our project
                if project_path_str in resource.lower():
                    # Parse the actual file path
                    # Format: file:///c%3A/Users/yooma/...
                    parsed_path = urllib.parse.unquote(resource.replace('file:///', ''))
                    
                    # Convert to backslashes for Windows
                    parsed_path = os.path.normpath(parsed_path)
                    
                    # Ensure it's the exact project directory we're in
                    current_dir = os.getcwd()
                    if current_dir.lower() in parsed_path.lower():
                        
                        # Find the most recent entry
                        entries = data.get('entries', [])
                        if entries:
                            # Sort by timestamp descending
                            entries.sort(key=lambda x: x.get('timestamp', 0), reverse=True)
                            latest_entry = entries[0]
                            latest_file = os.path.join(root, latest_entry['id'])
                            
                            if os.path.exists(latest_file):
                                # Determine relative path for logging
                                rel_path = os.path.relpath(parsed_path, current_dir)
                                
                                # Copy it back!
                                os.makedirs(os.path.dirname(parsed_path), exist_ok=True)
                                shutil.copy(latest_file, parsed_path)
                                print(f"Recovered: {rel_path} (from {latest_file})")
                                recovered_count += 1
        except Exception as e:
            pass

print(f"\nSuccessfully recovered {recovered_count} files from VS Code Local History!")
