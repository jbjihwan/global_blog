# -*- coding: utf-8 -*-
import os

p = r"D:\ai\antigravity\global_blog\build\blog\stanford-cs146s-1-modern-software-developer\index.html"
if os.path.exists(p):
    with open(p, "r", encoding="utf-8") as f:
        html = f.read()
    print("Local build has ad-card-container:", "ad-card-container" in html)
    print("Local build has ADVERTISEMENT:", "ADVERTISEMENT" in html)
else:
    print("Local file not found:", p)
