# -*- coding: utf-8 -*-
import os
import sys

post_slug = sys.argv[1] if len(sys.argv) > 1 else "2026-10-21-static-site-adsense-ads-txt-guide"
gb_root = r"D:\ai\antigravity\global_blog"

locales = [
    ("EN (Base)", f"{gb_root}/blog"),
    ("KO", f"{gb_root}/i18n/ko/docusaurus-plugin-content-blog"),
    ("JA", f"{gb_root}/i18n/ja/docusaurus-plugin-content-blog"),
    ("ES", f"{gb_root}/i18n/es/docusaurus-plugin-content-blog"),
    ("ZH-Hans", f"{gb_root}/i18n/zh-Hans/docusaurus-plugin-content-blog"),
    ("ZH-Hant", f"{gb_root}/i18n/zh-Hant/docusaurus-plugin-content-blog"),
]

print(f"Checking post: {post_slug}")
for loc_name, loc_base in locales:
    p = os.path.join(loc_base, post_slug, "index.md")
    if not os.path.exists(p):
        p = os.path.join(loc_base, post_slug, "index.mdx")
    
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            content = f.read()
            lines = content.splitlines()
            last_lines = "\n".join(lines[-15:])
            print(f"[{loc_name}] Found ({len(content)} chars, {len(lines)} lines)")
            print(f"--- Last 5 lines of {loc_name} ---")
            print("\n".join(lines[-5:]))
            print("-" * 50)
    else:
        print(f"[{loc_name}] NOT FOUND")
