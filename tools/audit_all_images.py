#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audit all image assets in global_blog to find all images containing text or diagrams.
"""

import os
import glob
from PIL import Image

BLOG_DIR = r"D:\ai\antigravity\global_blog\blog"

def main():
    print(f"Scanning images in: {BLOG_DIR}")
    image_files = glob.glob(os.path.join(BLOG_DIR, "**", "*.png"), recursive=True) + \
                  glob.glob(os.path.join(BLOG_DIR, "**", "*.jpg"), recursive=True)

    print(f"Total image files found: {len(image_files)}\n")

    for img_path in sorted(image_files):
        rel_path = os.path.relpath(img_path, BLOG_DIR)
        try:
            with Image.open(img_path) as im:
                width, height = im.size
                format_name = im.format
                print(f"{rel_path:<60} | {width}x{height:<6} | {format_name}")
        except Exception as e:
            print(f"{rel_path:<60} | ERROR: {e}")

if __name__ == "__main__":
    main()
