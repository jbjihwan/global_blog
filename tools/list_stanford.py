import os

blog_dir = r"D:\ai\antigravity\global_blog\blog"
cs_posts = [d for d in os.listdir(blog_dir) if "stanford-cs146s" in d]
print("Existing Stanford posts in blog/:", sorted(cs_posts))
