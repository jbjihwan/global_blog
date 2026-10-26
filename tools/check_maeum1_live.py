#!/usr/bin/env python3
import urllib.request
import re
from PIL import Image
import io

url = "https://globaldevlog.com/ko/blog/maeumjigi-1"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=10) as resp:
    html = resp.read().decode('utf-8', errors='ignore')
    matches = re.findall(r'(/ko/assets/images/01_cover-[^"\']+\.png)', html)
    print("Found cover PNGs:")
    for m in set(matches):
        full_url = "https://globaldevlog.com" + m
        print(f"  {full_url}")
        img_req = urllib.request.Request(full_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(img_req, timeout=10) as img_resp:
            im = Image.open(io.BytesIO(img_resp.read()))
            print(f"     -> Live Size: {im.size}, Format: {im.format}")
