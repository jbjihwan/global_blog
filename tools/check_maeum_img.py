import os

img1 = r"D:\ai\antigravity\global_blog\blog\2026-03-26-maeumjigi-1\images\01_cover.png"
img2 = r"D:\ai\antigravity\global_blog\blog\2026-03-26-maeumjigi-1\images\02_term.png"

for p in [img1, img2]:
    if os.path.exists(p):
        print(p, "size:", os.path.getsize(p), "bytes")
    else:
        print(p, "NOT FOUND")
