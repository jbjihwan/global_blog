# -*- coding: utf-8 -*-
import os

for path in [
    r"D:\ai\antigravity\global_blog\HANDOFF.md",
    r"D:\ai\antigravity\naver_blog\HANDOFF.md"
]:
    if os.path.exists(path):
        print(f"=== {path} ===")
        with open(path, "r", encoding="utf-8") as f:
            print(f.read()[:500])
    else:
        print(f"{path} not found.")
