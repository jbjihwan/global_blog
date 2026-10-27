#!/usr/bin/env python3
import urllib.request
import re
import time

url = "https://globaldevlog.com/ko/blog/static-site-security-npm-audit-truth?t=" + str(int(time.time()))
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Cache-Control': 'no-cache', 'Pragma': 'no-cache'})
with urllib.request.urlopen(req, timeout=10) as resp:
    html = resp.read().decode('utf-8', errors='ignore')
    matches = re.findall(r'(/ko/assets/images/[^"\']+\.png)', html)
    print("Found matching PNGs on live site (with cache-bust):")
    for m in set(matches):
        print(f"  https://globaldevlog.com{m}")
