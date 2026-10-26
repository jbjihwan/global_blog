#!/usr/bin/env python3
import os
from PIL import Image

BLOG_ROOT = r"D:\ai\antigravity\global_blog"
LOCALES = {
    "en": os.path.join(BLOG_ROOT, "blog"),
    "ko": os.path.join(BLOG_ROOT, "i18n", "ko", "docusaurus-plugin-content-blog"),
    "ja": os.path.join(BLOG_ROOT, "i18n", "ja", "docusaurus-plugin-content-blog"),
    "es": os.path.join(BLOG_ROOT, "i18n", "es", "docusaurus-plugin-content-blog"),
    "zh-Hans": os.path.join(BLOG_ROOT, "i18n", "zh-Hans", "docusaurus-plugin-content-blog"),
    "zh-Hant": os.path.join(BLOG_ROOT, "i18n", "zh-Hant", "docusaurus-plugin-content-blog"),
}

for loc, root in LOCALES.items():
    p = os.path.join(root, "2026-03-26-maeumjigi-1", "images", "01_cover.png")
    if os.path.exists(p):
        with Image.open(p) as im:
            print(f"[{loc}] {p} -> {im.size}")
    else:
        print(f"[{loc}] NOT FOUND")
