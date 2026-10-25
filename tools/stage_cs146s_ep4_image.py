#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import shutil

src = r"C:\Users\jbgih\.gemini\antigravity-cli\brain\a2c8435f-707b-431d-a280-dad177e26fdc\cs146s_lecture4_self_healing_pipeline_1792805999723.jpg"
dst_dir = r"D:\ai\antigravity\global_blog\배포대기\2026-10-25-stanford-cs146s-4\blog\images"
dst = os.path.join(dst_dir, "04_cs146s_spec_driven_test_harness.png")

os.makedirs(dst_dir, exist_ok=True)
shutil.copy2(src, dst)
print(f"[SUCCESS] Staged image to {dst}")
