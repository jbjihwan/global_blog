# -*- coding: utf-8 -*-
import re
from pathlib import Path

ROOT = Path(r"D:\ai\antigravity\global_blog")
BLOG_EN = ROOT / "blog"
BLOG_KO = ROOT / "i18n" / "ko" / "docusaurus-plugin-content-blog"
BUILD = ROOT / "build"

def check_links():
    en_sitemap = (BUILD / "sitemap.xml").read_text(encoding="utf-8")
    ko_sitemap = (BUILD / "ko" / "sitemap.xml").read_text(encoding="utf-8")
    valid_urls = set(re.findall(r"<loc>(.*?)</loc>", en_sitemap) + re.findall(r"<loc>(.*?)</loc>", ko_sitemap))
    valid_paths = set()
    for u in valid_urls:
        p = u.replace("https://globaldevlog.com", "")
        if not p:
            p = "/"
        valid_paths.add(p)
        valid_paths.add(p.rstrip("/"))

    print(f"Valid active paths count: {len(valid_paths)}")

    broken = []
    for lang, base in [("EN", BLOG_EN), ("KO", BLOG_KO)]:
        for d in sorted(base.iterdir()):
            if not d.is_dir():
                continue
            md_path = d / "index.md"
            text = md_path.read_text(encoding="utf-8")
            # find markdown links [text](url) and raw urls
            links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", text)
            for label, href in links:
                if href.startswith("!") or href.endswith((".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp")):
                    continue
                if "globaldevlog.com" in href or href.startswith("/"):
                    norm = href.replace("https://globaldevlog.com", "").split("#")[0].split("?")[0].rstrip("/")
                    if not norm:
                        norm = "/"
                    if norm not in valid_paths:
                        broken.append((lang, d.name, label, href))
            # Also check any mention of mental-crisis, stanford, public-finance, budget-surveillance, adsense
            for m in re.finditer(r"(mental-crisis|stanford-cs|public-finance|national-budget|budget-surveillance|adsense)", text, re.I):
                start = max(0, m.start() - 60)
                end = min(len(text), m.end() + 60)
                broken.append((lang, d.name, f"MATCH:{m.group(1)}", text[start:end].replace("\n", " ")))

    print(f"Broken links or archived post references found: {len(broken)}")
    for item in broken:
        print(" ", item)

if __name__ == "__main__":
    check_links()
