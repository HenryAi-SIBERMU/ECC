import json
import os

log_file = r'C:\Users\yooma\.gemini\antigravity\brain\5cbb4aa9-d124-4cdf-b5e8-9fbc22cfaf9e\.system_generated\logs\transcript_full.jsonl'
target_file = r'C:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\pages\2_Kualitas_Lingkungan.py'

os.system(f'git checkout HEAD -- "{target_file}"')

with open(log_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

applied_count = 0
for line in lines:
    try:
        step = json.loads(line)
        step_idx = step.get('step_index', 0)
        
        # We want to restore exactly to the state at step 2380 (before the bad edits)
        if step_idx > 2380:
            break
            
        if step.get('type') == 'PLANNER_RESPONSE' and 'tool_calls' in step:
            for call in step['tool_calls']:
                if call['name'] == 'run_command':
                    cmd = call['args'].get('CommandLine', '')
                    if 'Set-Content' in cmd and ' = @' in cmd:
                        script_content = cmd.split(' = @"')[1].split('"@')[0].strip()
                        if '2_Kualitas_Lingkungan.py' in script_content:
                            with open("temp_replay.py", 'w', encoding='utf-8') as sf:
                                sf.write(script_content)
                            os.system(f'python temp_replay.py')
                            applied_count += 1
                            
                elif call['name'] in ['replace_file_content', 'multi_replace_file_content']:
                    args = call['args']
                    if '2_Kualitas_Lingkungan.py' in args.get('TargetFile', ''):
                        with open(target_file, 'r', encoding='utf-8') as tf:
                            content = tf.read()
                        
                        if call['name'] == 'replace_file_content':
                            content = content.replace(args['TargetContent'], args['ReplacementContent'])
                        else:
                            for chunk in args['ReplacementChunks']:
                                content = content.replace(chunk['TargetContent'], chunk['ReplacementContent'])
                                
                        with open(target_file, 'w', encoding='utf-8') as tf:
                            tf.write(content)
                        applied_count += 1
    except Exception as e:
        pass

print(f"Replayed {applied_count} edits up to step 2380!")
