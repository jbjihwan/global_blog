#!/usr/bin/env python3
import os

TOOLS_DIR = r"D:\ai\antigravity\global_blog\tools"
for f in sorted(os.listdir(TOOLS_DIR)):
    if f.endswith(".py"):
        p = os.path.join(TOOLS_DIR, f)
        try:
            with open(p, "r", encoding="utf-8", errors="ignore") as fp:
                if "ads_txt_crawler_flow" in fp.read():
                    print(f"Found in: {f}")
        except Exception:
            pass
