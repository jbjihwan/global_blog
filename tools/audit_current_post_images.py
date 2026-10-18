import os
import re

BLOG_DIR = r"D:\ai\antigravity\global_blog\blog"

def audit_images():
    posts = sorted(os.listdir(BLOG_DIR))
    for p in posts:
        post_path = os.path.join(BLOG_DIR, p, "index.md")
        if not os.path.exists(post_path):
            continue
        with open(post_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        imgs = re.findall(r'!\[.*?\]\((.*?)\)', content)
        img_folder = os.path.join(BLOG_DIR, p, "images")
        actual_files = os.listdir(img_folder) if os.path.exists(img_folder) else []
        print(f"[{p}]")
        for img in imgs:
            print(f"  Markdown Ref: {img}")
        print(f"  Files on disk: {actual_files}")

if __name__ == "__main__":
    audit_images()
