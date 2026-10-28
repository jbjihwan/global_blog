import os
import re

ep_slugs = [
    "2026-11-18-autonomous-budget-audit-agent-text-to-sql-graphrag",
    "2026-11-19-national-budget-ai-audit-findings-performance-evaluation",
    "2026-11-20-national-budget-ai-sector-partition-live-monitoring",
    "2026-11-21-national-budget-ai-corporate-registry-cartel-detection",
    "2026-11-22-national-budget-ai-6-sector-full-suite",
    "2026-11-23-national-budget-ai-inspector-portal-verification-system"
]

roots = [
    r"D:\ai\antigravity\global_blog\blog",
    r"D:\ai\antigravity\global_blog\i18n",
    r"D:\ai\antigravity\global_blog\배포대기"
]

target_files = []
for r in roots:
    for dirpath, _, filenames in os.walk(r):
        for f in filenames:
            if f.endswith(".md"):
                full = os.path.join(dirpath, f)
                if any(slug in full for slug in ep_slugs):
                    target_files.append(full)

print(f"Total markdown files found: {len(target_files)}")

modified_count = 0

for fpath in target_files:
    with open(fpath, "r", encoding="utf-8") as f:
        text = f.read()

    orig = text

    # 1. Replace any $$...$$ blocks or lines with backtick inline code
    # Replace DEI equation:
    text = re.sub(
        r'\s*\$\$DEI\s*=.*?100\$\$\s*',
        '\n\n`DEI = (Direct Beneficiary Disbursement / Total Allocated Budget) * 100`\n\n',
        text
    )
    # Replace any other $$...$$ pattern
    def replace_double_dollar(match):
        inner = match.group(1).strip()
        # Clean latex commands like \text{...}, \frac{a}{b}, \times, etc.
        clean = inner.replace('\\text{', '').replace('}', '').replace('\\times', '×').replace('\\frac', '').replace('\\,', ' ')
        clean = re.sub(r'\s+', ' ', clean)
        return f"`{clean}`"

    text = re.sub(r'\$\$([^$]+)\$\$', replace_double_dollar, text)

    # 2. Replace (<180 days) or (<180일) with (`< 180 days`)
    text = re.sub(r'\(<(\d+)\s*days\)', r'(`<\1 days`)', text)
    text = re.sub(r'\(<(\d+)\s*일\)', r'(`<\1일`)', text)
    text = re.sub(r'<(\d+)\s*일', r'`<\1일`', text)
    text = re.sub(r'<(\d+)\s*days', r'`<\1 days`', text)

    if text != orig:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(text)
        modified_count += 1
        print(f"Modified: {fpath}")

print(f"Total modified files: {modified_count}")
