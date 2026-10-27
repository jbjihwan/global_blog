# -*- coding: utf-8 -*-
import os
import shutil

base_dir = r"D:\ai\antigravity\global_blog\배포대기\2026-11-03-stanford-cs329a-3"
img_src = os.path.join(base_dir, "blog", "images", "03_cs329a_robust_verification_prm.png")

locales = ["de", "es", "fr", "ja", "ko", "pt-BR", "zh-Hans", "zh-Hant"]
for loc in locales:
    dst_img_dir = os.path.join(base_dir, "i18n", loc, "images")
    os.makedirs(dst_img_dir, exist_ok=True)
    dst_img = os.path.join(dst_img_dir, "03_cs329a_robust_verification_prm.png")
    shutil.copyfile(img_src, dst_img)
    print(f"Copied image to: {dst_img}")
