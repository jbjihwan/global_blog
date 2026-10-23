import json

with open(r'C:\Users\jbgih\.gemini\antigravity-cli\brain\a2c8435f-707b-431d-a280-dad177e26fdc\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        idx = data.get('step_index', 0)
        if 3420 <= idx <= 3445:
            tc = data.get('tool_calls')
            c = data.get('content', '')
            c_sub = c[:120].replace('\n', ' ') if c else ''
            print(f"Step {idx}: {data.get('type')} - {tc if tc else c_sub}")
