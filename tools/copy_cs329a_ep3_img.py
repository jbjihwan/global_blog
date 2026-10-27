# -*- coding: utf-8 -*-
import shutil
import os

src = r"C:\Users\jbgih\.gemini\antigravity-cli\brain\a2c8435f-707b-431d-a280-dad177e26fdc\cs329a_lecture3_robust_verification_1793100452343.jpg"
dst = r"D:\ai\antigravity\global_blog\배포대기\2026-11-03-stanford-cs329a-3\blog\images\03_cs329a_robust_verification_prm.png"

os.makedirs(os.path.dirname(dst), exist_ok=True)
shutil.copyfile(src, dst)
print(f"Copied image to: {dst} ({os.path.getsize(dst)} bytes)")
