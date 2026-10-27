# -*- coding: utf-8 -*-
import os

build_dir = r"D:\ai\antigravity\global_blog\build"
for loc in ["de", "fr", "pt-BR"]:
    p = os.path.join(build_dir, loc, "blog", "index.html")
    print(f"Local build {loc}/blog/index.html exists:", os.path.exists(p))
