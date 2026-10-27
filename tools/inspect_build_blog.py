# -*- coding: utf-8 -*-
import os

blog_dir = r"D:\ai\antigravity\global_blog\build\blog"
if os.path.exists(blog_dir):
    items = os.listdir(blog_dir)
    print("Items in build/blog (count):", len(items))
    for it in items[:10]:
        print(" ", it)
