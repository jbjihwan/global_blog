# -*- coding: utf-8 -*-
import os
import shutil
import sys

def copy_ep6_images(src_img_path):
    if not os.path.exists(src_img_path):
        print(f"Error: Source image does not exist: {src_img_path}")
        sys.exit(1)

    base_dir = r"D:\ai\antigravity\global_blog\배포대기\2026-11-06-stanford-cs329a-6"
    dst = os.path.join(base_dir, "blog", "images", "06_cs329a_train_time_scaling_grpo.png")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src_img_path, dst)
    print(f"Copied Ep6 image to default blog: {dst} ({os.path.getsize(dst)} bytes)")

    locales = ["de", "es", "fr", "ja", "ko", "pt-BR", "zh-Hans", "zh-Hant"]
    for loc in locales:
        loc_img_dir = os.path.join(base_dir, "i18n", loc, "images")
        os.makedirs(loc_img_dir, exist_ok=True)
        loc_dst = os.path.join(loc_img_dir, "06_cs329a_train_time_scaling_grpo.png")
        shutil.copyfile(src_img_path, loc_dst)
    print("Copied Ep6 image to all 8 staging locales!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        copy_ep6_images(sys.argv[1])
    else:
        print("Usage: python copy_ep6_staging_images.py <src_image_path>")
