#!/usr/bin/env python3
import urllib.request
import re

urls = [
    "https://globaldevlog.com/ko/blog/static-site-security-npm-audit-truth",
    "https://globaldevlog.com/blog/static-site-security-npm-audit-truth",
    "https://globaldevlog.com/ko/blog/maeumjigi-1",
    "https://globaldevlog.com/blog/maeumjigi-1",
    "https://globaldevlog.com/ko/blog/github-pages-custom-domain-adsense-seo-guide",
    "https://globaldevlog.com/ko/blog/static-site-adsense-ads-txt-guide",
    "https://globaldevlog.com/ko/blog/2026-06-25-vision-anpr-1",
    "https://globaldevlog.com/ko/blog/2026-05-17-rl-qlearning-1",
    "https://globaldevlog.com/ko/blog/2026-06-18-maeumjigi-23",
]

headers = {'User-Agent': 'Mozilla/5.0'}

print("Checking live pages with exact frontmatter slugs:")
for u in urls:
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            status = resp.status
            html = resp.read().decode('utf-8', errors='ignore')
            imgs = re.findall(r'src=["\']([^"\']+\.(?:png|jpg|jpeg)[^"\']*)["\']', html)
            print(f"[OK {status}] {u}")
            for img in imgs[:2]:
                print(f"       -> img: {img}")
    except Exception as e:
        print(f"[ERR] {u} -> {e}")
