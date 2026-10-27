import os

blog_dir = r"D:\ai\antigravity\global_blog\blog"
posts = os.listdir(blog_dir)
for p in sorted(posts):
    if "cs329" in p.lower() or "agent" in p.lower() or "329" in p.lower():
        print(p)
