import os
import json
import re

roots = [
    r"D:\ai\antigravity\global_blog\blog",
    r"D:\ai\antigravity\global_blog\i18n",
    r"D:\ai\antigravity\global_blog\배포대기"
]

fixed_files = []

for r in roots:
    for dirpath, _, filenames in os.walk(r):
        for f in filenames:
            if f.endswith(".md"):
                full = os.path.join(dirpath, f)
                with open(full, "r", encoding="utf-8") as file:
                    content = file.read()
                
                orig = content
                
                # Look for broken keywords line: keywords: ["Portail Web d"Audit", ...]
                # or any keywords with unescaped internal double quote
                if 'd"Audit' in content:
                    content = content.replace('d"Audit', "d'Audit")
                
                # Check all keywords lines in frontmatter
                def fix_kw_line(m):
                    kw_line = m.group(0)
                    # replace d"Audit with d'Audit
                    return kw_line.replace('d"Audit', "d'Audit")

                content = re.sub(r'^keywords:\s*\[.*?\]', fix_kw_line, content, flags=re.M)

                if content != orig:
                    with open(full, "w", encoding="utf-8") as file:
                        file.write(content)
                    fixed_files.append(full)

print(f"Total fixed keyword files: {len(fixed_files)}")
for ff in fixed_files:
    print(f" - {ff}")
