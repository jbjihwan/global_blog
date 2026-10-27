# -*- coding: utf-8 -*-
import os

GB_ROOT = r"D:\ai\antigravity\global_blog"
pages_dir = os.path.join(GB_ROOT, "i18n")

for root, dirs, files in os.walk(pages_dir):
    for f in files:
        if f.endswith('.md'):
            p = os.path.join(root, f)
            with open(p, "r", encoding="utf-8") as file:
                content = file.read()
                for loc in ['/ko/', '/ja/', '/es/', '/zh-Hans/', '/zh-Hant/', '/de/', '/fr/', '/pt-BR/']:
                    if f"{loc}contact" in content or f"{loc}about" in content:
                        print(f"Found hardcoded locale link in {p}: {loc}")
