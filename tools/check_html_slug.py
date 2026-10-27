# -*- coding: utf-8 -*-
import os

p = r"D:\ai\antigravity\global_blog\build\blog\stanford-cs146s-1-modern-software-developer.html"
if os.path.exists(p):
    with open(p, "r", encoding="utf-8") as f:
        html = f.read()
    print("Found HTML file! Length:", len(html))
    print("Contains ad-card-container:", "ad-card-container" in html)
    print("Contains ADVERTISEMENT:", "ADVERTISEMENT" in html)
else:
    print("File not found:", p)
