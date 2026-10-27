#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Organize all blog images by language (ko, en, ja, es, zh-Hans, zh-Hant)
and by post comparison (side-by-side language comparison).
"""

import os
import shutil
import glob
from pathlib import Path

BASE_DIR = r"D:\ai\antigravity\global_blog"
BLOG_DIR = os.path.join(BASE_DIR, "blog")
I18N_DIR = os.path.join(BASE_DIR, "i18n")
REVIEW_DIR = os.path.join(BASE_DIR, "review_images")

BY_LANG_DIR = os.path.join(REVIEW_DIR, "by_language")
BY_POST_DIR = os.path.join(REVIEW_DIR, "by_post_multilingual")

LOCALES = ["ko", "en", "ja", "es", "zh-Hans", "zh-Hant"]

for loc in LOCALES:
    os.makedirs(os.path.join(BY_LANG_DIR, loc), exist_ok=True)
os.makedirs(BY_POST_DIR, exist_ok=True)

# 1. Process English (default in blog/)
posts = [d for d in os.listdir(BLOG_DIR) if os.path.isdir(os.path.join(BLOG_DIR, d))]
stats = {loc: 0 for loc in LOCALES}
posts_processed = set()

for post in posts:
    img_dir = os.path.join(BLOG_DIR, post, "images")
    if os.path.exists(img_dir):
        post_comp_dir = os.path.join(BY_POST_DIR, post)
        os.makedirs(post_comp_dir, exist_ok=True)
        for ext in ["*.png", "*.jpg", "*.jpeg"]:
            for f in glob.glob(os.path.join(img_dir, ext)):
                fname = os.path.basename(f)
                stem, ext_str = os.path.splitext(fname)
                
                # To by_language/en/
                dst_lang = os.path.join(BY_LANG_DIR, "en", f"{post}_{fname}")
                shutil.copy2(f, dst_lang)
                stats["en"] += 1
                
                # To by_post_multilingual/<post>/
                dst_post = os.path.join(post_comp_dir, f"{stem}_en{ext_str}")
                shutil.copy2(f, dst_post)
                posts_processed.add(post)

# 2. Process i18n locales
for loc in ["ko", "ja", "es", "zh-Hans", "zh-Hant"]:
    loc_blog = os.path.join(I18N_DIR, loc, "docusaurus-plugin-content-blog")
    if not os.path.exists(loc_blog):
        continue
    for post in os.listdir(loc_blog):
        img_dir = os.path.join(loc_blog, post, "images")
        if os.path.exists(img_dir):
            post_comp_dir = os.path.join(BY_POST_DIR, post)
            os.makedirs(post_comp_dir, exist_ok=True)
            for ext in ["*.png", "*.jpg", "*.jpeg"]:
                for f in glob.glob(os.path.join(img_dir, ext)):
                    fname = os.path.basename(f)
                    stem, ext_str = os.path.splitext(fname)
                    
                    # To by_language/<loc>/
                    dst_lang = os.path.join(BY_LANG_DIR, loc, f"{post}_{fname}")
                    shutil.copy2(f, dst_lang)
                    stats[loc] += 1
                    
                    # To by_post_multilingual/<post>/
                    dst_post = os.path.join(post_comp_dir, f"{stem}_{loc}{ext_str}")
                    shutil.copy2(f, dst_post)
                    posts_processed.add(post)

print("Language collection complete!")
for loc, cnt in stats.items():
    print(f"- Locale [{loc}]: {cnt} images")
print(f"Total comparison post folders: {len(posts_processed)}")

# Write README for by_language
readme_lang = os.path.join(BY_LANG_DIR, "README.md")
with open(readme_lang, "w", encoding="utf-8") as rf:
    rf.write("# 🌐 언어별 이미지 전체 모음 (By Language)\n\n")
    rf.write("각 언어별로 이미지에 포함된 텍스트, 번역 정확도, 상자 크기, 가시성을 한눈에 검토할 수 있습니다.\n\n")
    rf.write("| 언어 코드 | 언어명 | 이미지 수 | 폴더 링크 |\n")
    rf.write("| :--- | :--- | :--- | :--- |\n")
    rf.write(f"| `ko` | 한국어 (Korean) | {stats['ko']}개 | [ko 폴더](./ko/) |\n")
    rf.write(f"| `en` | 영어 (English) | {stats['en']}개 | [en 폴더](./en/) |\n")
    rf.write(f"| `ja` | 일본어 (Japanese) | {stats['ja']}개 | [ja 폴더](./ja/) |\n")
    rf.write(f"| `es` | 스페인어 (Spanish) | {stats['es']}개 | [es 폴더](./es/) |\n")
    rf.write(f"| `zh-Hans` | 중국어 간체 (Simplified Chinese) | {stats['zh-Hans']}개 | [zh-Hans 폴더](./zh-Hans/) |\n")
    rf.write(f"| `zh-Hant` | 중국어 번체 (Traditional Chinese) | {stats['zh-Hant']}개 | [zh-Hant 폴더](./zh-Hant/) |\n")

# Write README for by_post_multilingual
readme_post = os.path.join(BY_POST_DIR, "README.md")
with open(readme_post, "w", encoding="utf-8") as rf:
    rf.write("# 📊 글(포스트)별 6개국어 다이어그램 비교 모음 (Side-by-Side Comparison)\n\n")
    rf.write("한 포스트의 다이어그램이 6개 국어(`ko`, `en`, `ja`, `es`, `zh-Hans`, `zh-Hant`)에서 어떻게 다르게 표현되는지 나란히 비교할 수 있습니다.\n\n")
    rf.write("| 글 폴더명 | 포함된 비교 이미지 |\n")
    rf.write("| :--- | :--- |\n")
    for p in sorted(list(posts_processed)):
        p_dir = os.path.join(BY_POST_DIR, p)
        files = [f for f in os.listdir(p_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        rf.write(f"| [{p}](./{p}/) | {len(files)}개 이미지 (6개국어 버전) |\n")

print(f"Readmes generated in {BY_LANG_DIR} and {BY_POST_DIR}")
