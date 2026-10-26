import os

blog_dir = r"D:\ai\antigravity\global_blog\blog"
maeum_posts = sorted([d for d in os.listdir(blog_dir) if "maeumjigi" in d])

print("Maeumjigi Posts and their images:")
for mp in maeum_posts:
    img_dir = os.path.join(blog_dir, mp, "images")
    if os.path.exists(img_dir):
        imgs = os.listdir(img_dir)
        print(f" {mp}: {imgs}")
    else:
        print(f" {mp}: NO IMAGES DIR")
