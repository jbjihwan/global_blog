# -*- coding: utf-8 -*-
import os
import re

gb_root = r"D:\ai\antigravity\global_blog"
folder_name = "2026-10-22-stanford-cs146s-1"

files = [
    f"{gb_root}/blog/{folder_name}/index.md",
    f"{gb_root}/i18n/ko/docusaurus-plugin-content-blog/{folder_name}/index.md",
    f"{gb_root}/i18n/ja/docusaurus-plugin-content-blog/{folder_name}/index.md",
    f"{gb_root}/i18n/es/docusaurus-plugin-content-blog/{folder_name}/index.md",
    f"{gb_root}/i18n/zh-Hans/docusaurus-plugin-content-blog/{folder_name}/index.md",
    f"{gb_root}/i18n/zh-Hant/docusaurus-plugin-content-blog/{folder_name}/index.md",
]

for p in files:
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            content = f.read()
        # Clean double hr
        content = re.sub(r'---\s*\r?\n\s*---', '---', content)
        with open(p, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Cleaned formatting in: {p}")
