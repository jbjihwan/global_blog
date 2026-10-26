#!/usr/bin/env python3
import os

posts = [
    "2026-10-18-static-site-security-hardening",
    "2026-03-26-maeumjigi-1",
    "2026-10-20-custom-domain-adsense-seo-guide",
    "2026-10-21-static-site-adsense-ads-txt-guide"
]

for p in posts:
    fpath = os.path.join(r"D:\ai\antigravity\global_blog\blog", p, "index.md")
    if os.path.exists(fpath):
        with open(fpath, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("slug:"):
                    print(f"{p} -> {line.strip()}")
                    break
