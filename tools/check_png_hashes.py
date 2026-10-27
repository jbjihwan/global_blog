#!/usr/bin/env python3
import urllib.request
import re
from PIL import Image
import io

url = "https://globaldevlog.com/ko/blog/static-site-security-npm-audit-truth"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=10) as resp:
    html = resp.read().decode('utf-8', errors='ignore')
    matches = re.findall(r'(/ko/assets/images/[^"\']+\.png)', html)
    print("Found matching PNGs on live site:")
    for m in set(matches):
        full_url = "https://globaldevlog.com" + m
        print(f"  {full_url}")
        img_req = urllib.request.Request(full_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(img_req, timeout=10) as img_resp:
            im = Image.open(io.BytesIO(img_resp.read()))
            print(f"     -> Status: {img_resp.status}, Size: {im.size}")
