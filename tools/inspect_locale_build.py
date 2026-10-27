# -*- coding: utf-8 -*-
import os

for loc in ["de", "fr", "pt-BR"]:
    d = os.path.join(r"D:\ai\antigravity\global_blog\build", loc)
    if os.path.exists(d):
        print(f"Items in build/{loc}:", os.listdir(d))
