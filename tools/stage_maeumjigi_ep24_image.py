#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import shutil

src = r"C:\Users\jbgih\.gemini\antigravity-cli\brain\a2c8435f-707b-431d-a280-dad177e26fdc\maeumjigi_devlog_24_clinical_preprocessing_mnar_1792806235487.jpg"
dst_dir = r"D:\ai\antigravity\global_blog\배포대기\2026-09-16-maeumjigi-24\blog\images"
dst = os.path.join(dst_dir, "01_cover.png")

os.makedirs(dst_dir, exist_ok=True)
shutil.copy2(src, dst)
print(f"[SUCCESS] Staged image to {dst}")
