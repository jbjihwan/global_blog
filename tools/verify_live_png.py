#!/usr/bin/env python3
import urllib.request
from PIL import Image
import io

url = "https://globaldevlog.com/ko/assets/images/01_threat_model-fabf3aa1d591b6e0065c2a0938c31269.png"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=10) as resp:
    data = resp.read()
    im = Image.open(io.BytesIO(data))
    print(f"Downloaded from live: {url}")
    print(f"Status: {resp.status}, Size: {im.size}, Format: {im.format}")
