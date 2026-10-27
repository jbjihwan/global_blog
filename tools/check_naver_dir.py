# -*- coding: utf-8 -*-
import os

naver_dir = r"D:\ai\antigravity\naver_blog"
if os.path.exists(naver_dir):
    print("Files in naver_blog:")
    for root, dirs, files in os.walk(naver_dir):
        for f in files:
            print(os.path.join(root, f))
else:
    print("naver_blog directory does not exist.")
