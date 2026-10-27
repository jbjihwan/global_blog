import os

blog_dir = r"D:\ai\antigravity\global_blog\blog"
stanford_posts = [d for d in os.listdir(blog_dir) if "stanford" in d.lower()]
stanford_posts.sort()
print(f"Total stanford posts: {len(stanford_posts)}")
for p in stanford_posts:
    print(p)
