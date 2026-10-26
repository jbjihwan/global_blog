import os

bdir = r"D:\ai\antigravity\global_blog\build"
for root, dirs, files in os.walk(bdir):
    for f in files:
        if "01_cover" in f:
            full = os.path.join(root, f)
            print(f, os.path.getsize(full), "in", os.path.relpath(root, bdir))
