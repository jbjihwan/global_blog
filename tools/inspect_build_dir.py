# -*- coding: utf-8 -*-
import os

build_dir = r"D:\ai\antigravity\global_blog\build"
if os.path.exists(build_dir):
    print("Items in build/:")
    for item in os.listdir(build_dir):
        p = os.path.join(build_dir, item)
        if os.path.isdir(p):
            print(f"  [DIR]  {item}")
        else:
            print(f"  [FILE] {item}")
else:
    print("build dir does not exist.")
