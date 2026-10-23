# -*- coding: utf-8 -*-
import os
import re

gb_root = r"D:\ai\antigravity\global_blog"
folder_name = "2026-10-21-github-pages-custom-domain-cloudflare-dns"

locales = [
    f"{gb_root}/blog/{folder_name}/index.md",
    f"{gb_root}/i18n/ko/docusaurus-plugin-content-blog/{folder_name}/index.md",
    f"{gb_root}/i18n/ja/docusaurus-plugin-content-blog/{folder_name}/index.md",
    f"{gb_root}/i18n/es/docusaurus-plugin-content-blog/{folder_name}/index.md",
    f"{gb_root}/i18n/zh-Hans/docusaurus-plugin-content-blog/{folder_name}/index.md",
    f"{gb_root}/i18n/zh-Hant/docusaurus-plugin-content-blog/{folder_name}/index.md",
]

for p in locales:
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            c = f.read()
        # Ensure blank line before ---
        c = re.sub(r'([^\n])\n---', r'\1\n\n---', c)
        with open(p, "w", encoding="utf-8") as f:
            f.write(c)
        print(f"Fixed spacing in: {p}")
