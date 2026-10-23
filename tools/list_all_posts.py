# -*- coding: utf-8 -*-
import os
import glob

blog_dir = r"D:\ai\antigravity\global_blog\blog"
post_dirs = [d for d in os.listdir(blog_dir) if os.path.isdir(os.path.join(blog_dir, d))]
post_dirs.sort()

print(f"Total post directories found: {len(post_dirs)}")
print(f"{'Post Directory':<50} | {'Has Summary?':<15}")
print("-" * 70)

for d in post_dirs:
    idx_path = os.path.join(blog_dir, d, "index.md")
    if not os.path.exists(idx_path):
        idx_path = os.path.join(blog_dir, d, "index.mdx")
    
    if os.path.exists(idx_path):
        with open(idx_path, "r", encoding="utf-8") as f:
            content = f.read()
            has_sum = ("Executive Summary" in content or "최종 요약" in content or "3–5 Line" in content or "3-5 Line" in content or "3~5줄" in content)
            print(f"{d:<50} | {str(has_sum):<15}")
    else:
        print(f"{d:<50} | NO INDEX FILE")
