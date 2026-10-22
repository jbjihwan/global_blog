import os
import glob

files = glob.glob(r"D:\ai\antigravity\global_blog\blog\**\images\*", recursive=True)
print(f"Found {len(files)} image files in global blog.")
for f in files[:10]:
    print(" ", os.path.relpath(f, r"D:\ai\antigravity\global_blog\blog"))
