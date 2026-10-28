import os
import re

roots = [
    r"D:\ai\antigravity\global_blog\blog",
    r"D:\ai\antigravity\global_blog\i18n",
    r"D:\ai\antigravity\global_blog\배포대기"
]

modified = []

for r in roots:
    for dirpath, _, filenames in os.walk(r):
        for f in filenames:
            if f.endswith(".md"):
                full = os.path.join(dirpath, f)
                with open(full, "r", encoding="utf-8") as file:
                    content = file.read()
                
                orig = content
                
                # Replace any $DEI = ...$ or $$DEI = ...$$
                content = re.sub(
                    r'\$+\s*DEI\s*=[^$\n]+\$+',
                    '`DEI = (Direct Beneficiary Disbursement / Total Allocated Budget) * 100`',
                    content
                )
                
                # Replace any remaining $...$ that contains \frac or \text or {
                def clean_inline_math(m):
                    inner = m.group(1)
                    if '{' in inner or '\\' in inner or 'frac' in inner or 'text' in inner:
                        # clean it
                        clean = re.sub(r'\\(?:text|frac|times|\,)', '', inner)
                        clean = clean.replace('{', '(').replace('}', ')')
                        clean = re.sub(r'\s+', ' ', clean).strip()
                        return f"`{clean}`"
                    return m.group(0)

                content = re.sub(r'\$([^$\n]+)\$', clean_inline_math, content)

                if content != orig:
                    with open(full, "w", encoding="utf-8") as file:
                        file.write(content)
                    modified.append(full)

print(f"Total modified files: {len(modified)}")
for m in modified:
    print(f" - {m}")
