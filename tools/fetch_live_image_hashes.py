#!/usr/bin/env python3
import urllib.request
import re

urls = [
    ("Security Post (Threat Model)", "https://globaldevlog.com/ko/blog/static-site-security-npm-audit-truth"),
    ("Maeumjigi #1 (Cover)", "https://globaldevlog.com/ko/blog/maeumjigi-1"),
    ("AdSense SEO Guide (DNS)", "https://globaldevlog.com/ko/blog/github-pages-custom-domain-adsense-seo-guide"),
    ("ANPR #1 (Pipeline)", "https://globaldevlog.com/ko/blog/2026-06-25-vision-anpr-1"),
]

headers = {'User-Agent': 'Mozilla/5.0'}

for name, u in urls:
    print(f"=== {name} ===")
    req = urllib.request.Request(u, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        matches = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html)
        for m in matches:
            if "assets/images" in m:
                print(f"   Image URL: {m}")
