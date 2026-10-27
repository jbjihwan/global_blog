import os

blog_dir = r"D:\ai\antigravity\global_blog\blog"
posts = os.listdir(blog_dir)
for p in sorted(posts):
    if "cs221" in p.lower() or "221" in p.lower():
        print(p)
