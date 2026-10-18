import os
import glob

NAVER_POSTS = r"D:\ai\antigravity\naver_blog\posts"
post_files = sorted(glob.glob(os.path.join(NAVER_POSTS, "*", "maeumjigi", "post.md")))
print(f"Total maeumjigi post.md found: {len(post_files)}")
for p in post_files:
    date_str = os.path.basename(os.path.dirname(os.path.dirname(p)))
    with open(p, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.startswith("title:") or line.startswith("number:")]
    print(f"  [{date_str}]: {lines}")
