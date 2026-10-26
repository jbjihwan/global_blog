import os

d = r"D:\ai\antigravity\global_blog\blog\2026-03-26-maeumjigi-1"
print("Files in 2026-03-26-maeumjigi-1:")
for root, dirs, files in os.walk(d):
    print(os.path.relpath(root, d), files)
