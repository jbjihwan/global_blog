# -*- coding: utf-8 -*-
import shutil
import os

src = r"C:\Users\jbgih\.gemini\antigravity-cli\brain\a2c8435f-707b-431d-a280-dad177e26fdc\stanford_cs329a_test_time_compute_scaling_1793098975970.jpg"
targets = [
    r"D:\ai\antigravity\global_blog\배포대기\2026-11-02-stanford-cs329a-2\blog\images\02_cs329a_test_time_compute_scaling.png",
    r"D:\ai\antigravity\global_blog\blog\2026-11-02-stanford-cs329a-2\images\02_cs329a_test_time_compute_scaling.png"
]

for dst in targets:
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src, dst)
    print(f"Copied to: {dst} ({os.path.getsize(dst)} bytes)")
