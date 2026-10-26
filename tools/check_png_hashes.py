#!/usr/bin/env python3
import urllib.request
import re

url = "https://globaldevlog.com/ko/blog/static-site-security-npm-audit-truth"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=10) as resp:
    html = resp.read().decode('utf-8', errors='ignore')
    matches = re.findall(r'(/ko/assets/images/[^"\']+\.png)', html)
    print("Found matching PNGs:")
    for m in set(matches):
        print("  https://globaldevlog.com" + m)
