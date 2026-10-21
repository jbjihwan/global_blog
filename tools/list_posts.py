import os

blog_dir = r"D:\ai\antigravity\global_blog\blog"
posts = sorted([d for d in os.listdir(blog_dir) if os.path.isdir(os.path.join(blog_dir, d))])
for p in posts:
    print(p)
