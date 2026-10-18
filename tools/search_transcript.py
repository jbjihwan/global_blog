import json

transcript_path = r"C:\Users\jbgih\.gemini\antigravity-cli\brain\a2c8435f-707b-431d-a280-dad177e26fdc\.system_generated\logs\transcript.jsonl"
keywords = ["권한", "permission", "allow", "승인", "허가", "허용", "동의", "영구"]

with open(transcript_path, "r", encoding="utf-8") as f:
    for line_num, line in enumerate(f, 1):
        try:
            data = json.loads(line)
            source = data.get("source")
            content = data.get("content", "")
            step_index = data.get("step_index")
            if source == "USER_EXPLICIT":
                if any(k in content.lower() for k in keywords):
                    print(f"[Line {line_num} / Step {step_index}] USER:\n{content}\n")
        except Exception:
            pass
