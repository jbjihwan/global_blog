# -*- coding: utf-8 -*-
import os
import re

gb_root = r"D:\ai\antigravity\global_blog"
folder_name = "2026-05-21-rl-qlearning-5"

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
        # Replace \$1\.2\\text\{m\}\s*\\times\s*1\.2\\text\{m\}\$ with 1.2m × 1.2m
        c = re.sub(r'\$1\.2\\text\{m\}\s*\\times\s*1\.2\\text\{m\}\$', '1.2m × 1.2m', c)
        c = re.sub(r'\\text\{([^}]+)\}', r'\1', c)
        c = re.sub(r'\$\(x,\s*y,\s*\\theta\)\$', '(x, y, θ)', c)
        with open(p, "w", encoding="utf-8") as f:
            f.write(c)
        print(f"Fixed MDX LaTeX in: {p}")
