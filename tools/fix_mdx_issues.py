import os
import re

dirs_to_check = [
    r"D:\ai\antigravity\global_blog\blog",
    r"D:\ai\antigravity\global_blog\i18n",
    r"D:\ai\antigravity\global_blog\배포대기"
]

def fix_file(fpath):
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    orig = content

    # 1. Fix LaTeX equations with \frac or \text that trigger Acorn MDX parser
    # Ep2: DEI equation
    content = re.sub(
        r'\$\$DEI\s*=\s*\\frac\{[^}]*\}\{[^}]*\}\s*\\times\s*100\$\$',
        '`DEI = (Direct Beneficiary Disbursement / Total Allocated Budget) * 100`',
        content
    )
    content = re.sub(
        r'\$\$DEI\s*=\s*\\frac\{[^}]*\}\{[^}]*\}\s*\\times\s*100\s*\$\$',
        '`DEI = (직접 수혜 지출액 / 전체 배정 예산) * 100`',
        content
    )
    # Generic \frac or $$ with \text
    content = re.sub(
        r'\$\$\\text\{Target Sector\}[^$]*\$\$',
        '`Target Sector = Agency Type × Budget Item × Contract Method`',
        content
    )
    content = re.sub(
        r'\$\$[^\n$]*표적\s*구역[^\n$]*\$\$',
        '`표적 구역 = 기관 유형 × 예산 비목 × 계약 방식`',
        content
    )
    content = re.sub(
        r'\$\$\\text\{Threshold Proximity\}[^$]*\$\$',
        '`Threshold Proximity = (Contract Amount / 50,000,000 KRW) * 100`',
        content
    )
    content = re.sub(
        r'\$\$[^\n$]*한도\s*근접도[^\n$]*\$\$',
        '`한도 근접도 = (계약 금액 / 50,000,000원) * 100`',
        content
    )
    
    # 2. Fix < followed by numbers or non-tag text outside backticks, like (<180 days) or (<180일)
    content = re.sub(r'\(<(\d+)\s*days\)', r'(`<\1 days`)', content)
    content = re.sub(r'\(<(\d+)\s*일\)', r'(`<\1일`)', content)
    content = re.sub(r'<(\d+)\s*일', r'`<\1일`', content)
    content = re.sub(r'<(\d+)\s*days', r'`<\1 days`', content)

    if content != orig:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Fixed: {fpath}")

for d in dirs_to_check:
    for root, _, files in os.walk(d):
        for file in files:
            if file.endswith(".md"):
                fix_file(os.path.join(root, file))

print("All fixes applied!")
