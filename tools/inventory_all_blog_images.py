import os
from PIL import Image

blog_dir = r"D:\ai\antigravity\global_blog\blog"
post_dirs = sorted([d for d in os.listdir(blog_dir) if os.path.isdir(os.path.join(blog_dir, d))])

print(f"Total blog posts in blog/: {len(post_dirs)}")

all_images = []

for pd in post_dirs:
    img_dir = os.path.join(blog_dir, pd, "images")
    if os.path.exists(img_dir):
        for f in os.listdir(img_dir):
            if any(f.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".webp"]):
                fp = os.path.join(img_dir, f)
                try:
                    with Image.open(fp) as im:
                        all_images.append((pd, f, fp, im.size, im.format, os.path.getsize(fp)))
                except:
                    pass

print(f"Total images found: {len(all_images)}")
for pd, f, fp, sz, fmt, fsz in all_images:
    print(f" - [{pd}] {f}: size {sz}, {fsz} bytes")
