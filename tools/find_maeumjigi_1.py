import os

blog_dir = r"D:\ai\antigravity\global_blog\blog"
matches = []
for d in os.listdir(blog_dir):
    if "maeumjigi" in d.lower():
        matches.append(d)

print("Found Maeumjigi folders in blog/:")
for m in sorted(matches)[:10]:
    print(" -", m)
