import json
import os

log_file = r'C:\Users\yooma\.gemini\antigravity\brain\5cbb4aa9-d124-4cdf-b5e8-9fbc22cfaf9e\.system_generated\logs\transcript_full.jsonl'
recovery_dir = r'C:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\RECOVERED_FROM_TRANSCRIPT_PRE_RESET'
os.makedirs(recovery_dir, exist_ok=True)

with open(log_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

count = 0
found_steps = []
# Find the step index of the git reset
reset_line_idx = -1
for i, line in enumerate(lines):
    if 'git reset --hard' in line:
        reset_line_idx = i
        break

if reset_line_idx != -1:
    print(f"Found git reset at line {reset_line_idx}")
    # Now look BEFORE the reset
    for i in range(reset_line_idx - 1, max(-1, reset_line_idx - 2000), -1):
        try:
            step = json.loads(lines[i])
            if step.get('type') == 'PLANNER_RESPONSE' and 'tool_calls' in step:
                for call in step['tool_calls']:
                    if call['name'] in ['replace_file_content', 'multi_replace_file_content']:
                        count += 1
                        found_steps.append(step['step_index'])
                        out_file = os.path.join(recovery_dir, f"step_{step['step_index']}_{call['name']}.json")
                        with open(out_file, 'w', encoding='utf-8') as out_f:
                            json.dump(call['args'], out_f, indent=2)
                    elif call['name'] == 'run_command':
                        cmd = call['args'].get('CommandLine', '')
                        if 'Set-Content' in cmd and ' = @' in cmd:
                            script_content = cmd.split(' = @"')[1].split('"@')[0].strip()
                            if 'with open(' in script_content and '.py' in script_content:
                                count += 1
                                found_steps.append(step['step_index'])
                                out_file = os.path.join(recovery_dir, f"step_{step['step_index']}_script.py")
                                with open(out_file, 'w', encoding='utf-8') as out_f:
                                    out_f.write(script_content)
        except Exception as e:
            pass

print(f"Recovered {count} tool calls from before git reset.")
print(f"Steps: {found_steps}")
