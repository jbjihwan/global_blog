#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import shutil

src = r"C:\Users\jbgih\.gemini\antigravity-cli\brain\a2c8435f-707b-431d-a280-dad177e26fdc\cs146s_lecture7_automated_code_review_1792895779518.jpg"
dst_dir = r"D:\ai\antigravity\global_blog\배포대기\2026-10-28-stanford-cs146s-7\blog\images"
dst = os.path.join(dst_dir, "07_cs146s_code_review_at_scale.png")

os.makedirs(dst_dir, exist_ok=True)
shutil.copy2(src, dst)
print(f"[SUCCESS] Staged image to {dst}")
