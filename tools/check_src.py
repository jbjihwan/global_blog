import os

src_dir = r"D:\ai\antigravity\global_blog\src"
if os.path.exists(src_dir):
    for root, dirs, files in os.walk(src_dir):
        print(os.path.relpath(root, src_dir), files)
