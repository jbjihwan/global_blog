import os
import glob
import re

BLOG_ROOT = r"D:\ai\antigravity\global_blog"
locales = {
    "en": os.path.join(BLOG_ROOT, "blog"),
    "ko": os.path.join(BLOG_ROOT, "i18n", "ko", "docusaurus-plugin-content-blog"),
    "ja": os.path.join(BLOG_ROOT, "i18n", "ja", "docusaurus-plugin-content-blog"),
    "es": os.path.join(BLOG_ROOT, "i18n", "es", "docusaurus-plugin-content-blog"),
}

path = locales["ko"]
print(f"\n=== Locale: ko ===")
posts = sorted(glob.glob(os.path.join(path, "*", "index.md")))
for p in posts:
    folder = os.path.basename(os.path.dirname(p))
    with open(p, "r", encoding="utf-8") as f:
        c = f.read(500)
        m = re.search(r"title:\s*['\"]?(.*?)['\"]?\n", c)
        t = m.group(1) if m else "NO TITLE"
        print(f"  [{folder}]: {t}")
