# -*- coding: utf-8 -*-
import os
import re

p = r"D:\ai\antigravity\naver_blog\posts\2026-10-22\stanford_cs146s_1\post.md"
if os.path.exists(p):
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub(r'---\s*\r?\n\s*---', '---', content)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Cleaned formatting in: {p}")
