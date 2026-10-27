# -*- coding: utf-8 -*-
import os
import shutil

staging_dir = r"D:\ai\antigravity\global_blog\배포대기\2026-11-02-stanford-cs329a-2"
prod_blog = r"D:\ai\antigravity\global_blog\blog\2026-11-02-stanford-cs329a-2"
prod_i18n = r"D:\ai\antigravity\global_blog\i18n"
img_src = os.path.join(staging_dir, "blog", "images", "02_cs329a_test_time_compute_scaling.png")

# 1. Copy English
os.makedirs(prod_blog, exist_ok=True)
shutil.copyfile(os.path.join(staging_dir, "blog", "index.md"), os.path.join(prod_blog, "index.md"))
os.makedirs(os.path.join(prod_blog, "images"), exist_ok=True)
shutil.copyfile(img_src, os.path.join(prod_blog, "images", "02_cs329a_test_time_compute_scaling.png"))
print("Copied en: blog/index.md and image")

# 2. Copy Locales
locales = ["de", "es", "fr", "ja", "ko", "pt-BR", "zh-Hans", "zh-Hant"]
for loc in locales:
    src_md = os.path.join(staging_dir, "i18n", loc, "index.md")
    dst_dir = os.path.join(prod_i18n, loc, "docusaurus-plugin-content-blog", "2026-11-02-stanford-cs329a-2")
    os.makedirs(dst_dir, exist_ok=True)
    shutil.copyfile(src_md, os.path.join(dst_dir, "index.md"))
    
    # copy image
    dst_img_dir = os.path.join(dst_dir, "images")
    os.makedirs(dst_img_dir, exist_ok=True)
    shutil.copyfile(img_src, os.path.join(dst_img_dir, "02_cs329a_test_time_compute_scaling.png"))
    print(f"Copied {loc}: index.md + image")

print("\nAll files and images synchronized to production!")
