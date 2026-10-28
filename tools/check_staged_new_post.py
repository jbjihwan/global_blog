# -*- coding: utf-8 -*-
import glob
import re
import os

post_dir = r"D:\ai\antigravity\global_blog\배포대기\2026-11-18-autonomous-budget-audit-agent-text-to-sql-graphrag"
print("=" * 80)
print("🔍 [신규 포스트 검증] 배포대기 원고 메타데이터 및 글자 수 검사")
print("=" * 80)

for f in sorted(glob.glob(os.path.join(post_dir, "**", "index.md"), recursive=True)):
    with open(f, "r", encoding="utf-8") as fp:
        content = fp.read(1000)
    m_title = re.search(r'title:\s*\"?(.*?)\"?\s*$', content, re.MULTILINE)
    m_desc = re.search(r'description:\s*\"?(.*?)\"?\s*$', content, re.MULTILINE)
    rel = os.path.relpath(f, post_dir)
    title = m_title.group(1) if m_title else ""
    desc = m_desc.group(1) if m_desc else ""
    print(f"{rel:<25} | Title ({len(title):2d}c): {title:<40} | Desc ({len(desc):3d}c)")

print("=" * 80)
print("✅ 검증 완료")
