import os

blog_dir = r"D:\ai\antigravity\global_blog\blog"
for d in sorted(os.listdir(blog_dir)):
    p = os.path.join(blog_dir, d, "images")
    if os.path.exists(p):
        imgs = [f for f in os.listdir(p) if not f.startswith(".")]
        print(f"{d:<45} : {imgs}")
