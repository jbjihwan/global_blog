#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Collect all generated images from the current conversation brain, subagents, and blog posts
into a single dedicated folder for user inspection and revision requests.
"""

import os
import shutil
import glob
from pathlib import Path

DEST_DIR = r"D:\ai\antigravity\global_blog\review_images"
os.makedirs(DEST_DIR, exist_ok=True)

BRAIN_DIR = r"C:\Users\jbgih\.gemini\antigravity-cli\brain"
CONV_ID = "a2c8435f-707b-431d-a280-dad177e26fdc"
CURR_BRAIN = os.path.join(BRAIN_DIR, CONV_ID)

BLOG_DIR = r"D:\ai\antigravity\global_blog\blog"

copied = []

# 1. Collect from Current Brain directory
for ext in ["*.png", "*.jpg", "*.jpeg"]:
    for f in glob.glob(os.path.join(CURR_BRAIN, ext)):
        fname = os.path.basename(f)
        dest_path = os.path.join(DEST_DIR, f"brain_{fname}")
        shutil.copy2(f, dest_path)
        copied.append(("Current Conversation Brain", fname, dest_path))

# 2. Collect from Subagent brain directories
for sub_brain in glob.glob(os.path.join(BRAIN_DIR, "*")):
    if not os.path.isdir(sub_brain) or os.path.abspath(sub_brain) == os.path.abspath(CURR_BRAIN):
        continue
    sub_id = os.path.basename(sub_brain)
    for ext in ["*.png", "*.jpg", "*.jpeg"]:
        for f in glob.glob(os.path.join(sub_brain, ext)):
            fname = os.path.basename(f)
            dest_name = f"subagent_{sub_id[:8]}_{fname}"
            dest_path = os.path.join(DEST_DIR, dest_name)
            shutil.copy2(f, dest_path)
            copied.append((f"Subagent {sub_id[:8]}", fname, dest_path))

# 3. Collect from Blog posts
for post_dir in glob.glob(os.path.join(BLOG_DIR, "*")):
    if os.path.isdir(post_dir):
        post_slug = os.path.basename(post_dir)
        img_dir = os.path.join(post_dir, "images")
        if os.path.exists(img_dir):
            for ext in ["*.png", "*.jpg", "*.jpeg"]:
                for f in glob.glob(os.path.join(img_dir, ext)):
                    fname = os.path.basename(f)
                    dest_name = f"blog_{post_slug[:20]}_{fname}"
                    dest_path = os.path.join(DEST_DIR, dest_name)
                    shutil.copy2(f, dest_path)
                    copied.append((f"Blog Post {post_slug}", fname, dest_path))

print(f"Total images collected: {len(copied)}")
for src, fn, dst in copied:
    print(f"- [{src}] {fn} -> {os.path.basename(dst)}")

# Generate a catalog README in DEST_DIR
readme_path = os.path.join(DEST_DIR, "README.md")
with open(readme_path, "w", encoding="utf-8") as rf:
    rf.write("# 🎨 생성 및 검토 대상 이미지 모음 (Review Images Catalog)\n\n")
    rf.write("사용자가 한 번에 검토하고 피드백/수정 요청을 줄 수 있도록 모든 생성 이미지를 한곳에 모았습니다.\n\n")
    rf.write("| 번호 | 파일명 | 출처 / 원본 설명 | 미리보기 링크 |\n")
    rf.write("| :--- | :--- | :--- | :--- |\n")
    for idx, (src, fn, dst) in enumerate(copied, 1):
        dst_name = os.path.basename(dst)
        rf.write(f"| {idx} | `{dst_name}` | {src} ({fn}) | [{dst_name}](./{dst_name}) |\n")

print(f"\nCatalog written to: {readme_path}")
