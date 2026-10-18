#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import glob

blog_dir = r"D:\ai\antigravity\global_blog\blog"
posts = sorted(glob.glob(os.path.join(blog_dir, "*maeumjigi*", "index.md")))

for p in posts:
    dirname = os.path.basename(os.path.dirname(p))
    with open(p, "r", encoding="utf-8") as f:
        lines = f.readlines()
    title = ""
    has_desc = False
    has_truncate = False
    for line in lines:
        if line.startswith("title:"):
            title = line.strip()
        if line.startswith("description:"):
            has_desc = True
        if "{/* truncate */}" in line:
            has_truncate = True
    print(f"{dirname} | desc={has_desc} | trunc={has_truncate} | {title[:50]}")
