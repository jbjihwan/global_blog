# -*- coding: utf-8 -*-
import os

src_dir = r"D:\ai\antigravity\global_blog\src"
for root, dirs, files in os.walk(src_dir):
    for f in files:
        print(os.path.relpath(os.path.join(root, f), src_dir))
