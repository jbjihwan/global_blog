import re, os

base_dir = r"D:\ai\antigravity\global_blog\배포대기\2026-10-29-stanford-cs146s-8"
files = [
    os.path.join(base_dir, "blog", "index.md"),
    os.path.join(base_dir, "i18n", "ko", "index.md"),
    os.path.join(base_dir, "i18n", "ja", "index.md"),
    os.path.join(base_dir, "i18n", "es", "index.md"),
    os.path.join(base_dir, "i18n", "zh-Hans", "index.md"),
    os.path.join(base_dir, "i18n", "zh-Hant", "index.md"),
]

for fpath in files:
    if not os.path.exists(fpath):
        print(f"Missing: {fpath}")
        continue
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check for unescaped curly braces outside code blocks
    lines = content.splitlines()
    in_code_block = False
    issues = []
    for idx, line in enumerate(lines, 1):
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if not in_code_block:
            # Check for JSX/MDX expression risks like {something} that isn't {/* truncate */}
            matches = re.findall(r'\{[^\*\#\/\}]+?\}', line)
            if matches:
                # Filter out valid markdown or harmless patterns if any
                issues.append((idx, line, matches))
    if issues:
        print(f"Issues in {fpath}:")
        for idx, line, matches in issues[:5]:
            print(f"  Line {idx}: {matches} in: {line}")
    else:
        print(f"OK: {os.path.basename(os.path.dirname(fpath))}/{os.path.basename(fpath)}")
