import json
import os

log_file = r'C:\Users\yooma\.gemini\antigravity\brain\5cbb4aa9-d124-4cdf-b5e8-9fbc22cfaf9e\.system_generated\logs\transcript_full.jsonl'
files_modified = set()

with open(log_file, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            step = json.loads(line)
            if step.get('type') == 'PLANNER_RESPONSE' and 'tool_calls' in step:
                for call in step['tool_calls']:
                    if call['name'] in ['replace_file_content', 'multi_replace_file_content', 'write_to_file']:
                        files_modified.add(call['args'].get('TargetFile', ''))
                    elif call['name'] == 'run_command':
                        cmd = call['args'].get('CommandLine', '')
                        if 'Set-Content' in cmd and ' = @' in cmd:
                            script_content = cmd.split(' = @"')[1].split('"@')[0].strip()
                            if 'file_path =' in script_content:
                                for l in script_content.split('\n'):
                                    if 'file_path =' in l:
                                        files_modified.add(l.split('=')[1].strip().strip('"').strip("'"))
                                        break
        except:
            pass

print("Files modified during this entire session:")
for f in files_modified:
    if f:
        print(f" - {f}")
