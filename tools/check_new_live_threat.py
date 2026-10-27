#!/usr/bin/env python3
import urllib.request
from PIL import Image
import io

url = "https://globaldevlog.com/ko/assets/images/01_threat_model-2aaa310bf540a6931d25420d6d2c07ff.png"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        im = Image.open(io.BytesIO(resp.read()))
        print(f"Status: {resp.status}, Size: {im.size}, Format: {im.format}")
except Exception as e:
    print(f"Error: {e}")
