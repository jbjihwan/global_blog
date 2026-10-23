# -*- coding: utf-8 -*-
import os
import re

gb_root = r"D:\ai\antigravity\global_blog"
folder_name = "2026-06-26-vision-anpr-2"

locales = [
    (f"{gb_root}/blog/{folder_name}/index.md", r'\|\s*\\?text\{slope\}\s*\|', '|slope|'),
    (f"{gb_root}/i18n/ko/docusaurus-plugin-content-blog/{folder_name}/index.md", r'\|\s*\\?text\{slope\}\s*\|', '|slope|'),
    (f"{gb_root}/i18n/ja/docusaurus-plugin-content-blog/{folder_name}/index.md", r'\|\s*\\?text\{slope\}\s*\|', '|slope|'),
    (f"{gb_root}/i18n/es/docusaurus-plugin-content-blog/{folder_name}/index.md", r'\|\s*\\?text\{pendiente\}\s*\|', '|pendiente|'),
    (f"{gb_root}/i18n/zh-Hans/docusaurus-plugin-content-blog/{folder_name}/index.md", r'\|\s*\\?text\{slope\}\s*\|', '|slope|'),
    (f"{gb_root}/i18n/zh-Hant/docusaurus-plugin-content-blog/{folder_name}/index.md", r'\|\s*\\?text\{slope\}\s*\|', '|slope|'),
]

for p, pattern, replacement in locales:
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            c = f.read()
        # Replace LaTeX with simple math
        c = re.sub(pattern, replacement, c)
        # Also clean any remaining naked {\text{...}}
        c = re.sub(r'\$\\text\{([^}]+)\}\$', r'\1', c)
        with open(p, "w", encoding="utf-8") as f:
            f.write(c)
        print(f"Fixed MDX curly braces in: {p}")
