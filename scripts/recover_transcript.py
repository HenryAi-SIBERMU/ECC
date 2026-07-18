import json
import os

log_file = r'C:\Users\yooma\.gemini\antigravity\brain\5cbb4aa9-d124-4cdf-b5e8-9fbc22cfaf9e\.system_generated\logs\transcript_full.jsonl'
recovery_dir = r'C:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\RECOVERED_FROM_TRANSCRIPT'
os.makedirs(recovery_dir, exist_ok=True)

with open(log_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

count = 0
for i, line in enumerate(reversed(lines)): # Look backwards
    if count >= 30: # Limit to last 30 major code blocks
        break
    try:
        step = json.loads(line)
        if step.get('type') == 'PLANNER_RESPONSE' and 'tool_calls' in step:
            for call in step['tool_calls']:
                if call['name'] == 'run_command':
                    cmd = call['args'].get('CommandLine', '')
                    if 'Set-Content' in cmd and ' = @' in cmd:
                        # Extract the script content
                        script_content = cmd.split(' = @"')[1].split('"@')[0].strip()
                        if 'with open(' in script_content and '.py' in script_content:
                            count += 1
                            out_file = os.path.join(recovery_dir, f'step_{len(lines)-i}_script.py')
                            with open(out_file, 'w', encoding='utf-8') as out_f:
                                out_f.write(script_content)
                                
                elif call['name'] in ['replace_file_content', 'multi_replace_file_content', 'write_to_file']:
                    count += 1
                    out_file = os.path.join(recovery_dir, f'step_{len(lines)-i}_{call["name"]}.json')
                    with open(out_file, 'w', encoding='utf-8') as out_f:
                        json.dump(call['args'], out_f, indent=2)
    except:
        pass

print(f"Recovered {count} tool calls from transcript.")
