#!/usr/bin/env python3
import shutil

src = r"D:\ai\antigravity\global_blog\tools\test_vertical_threat.png"
dst = r"C:\Users\jbgih\.gemini\antigravity-cli\brain\a2c8435f-707b-431d-a280-dad177e26fdc\test_vertical_threat.png"
shutil.copy(src, dst)
print("Copied to artifacts.")
