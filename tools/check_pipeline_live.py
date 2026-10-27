#!/usr/bin/env python3
import urllib.request
from PIL import Image
import io

url = "https://globaldevlog.com/ko/assets/images/02_security_pipeline-33264c3ef7dbb1e377e55c32148ab400.png"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        im = Image.open(io.BytesIO(resp.read()))
        print(f"Status: {resp.status}, Size: {im.size}, Format: {im.format}")
except Exception as e:
    print(f"Error: {e}")
