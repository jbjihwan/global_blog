# -*- coding: utf-8 -*-
import urllib.request

url = "https://globaldevlog.com/blog/stanford-cs146s-1-modern-software-developer"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8')
        print(f"[HTTP {resp.status}] Fetched post page ({len(html)} bytes)")
        print("Contains ad-card-container:", "ad-card-container" in html)
        print("Contains ADVERTISEMENT label:", "ADVERTISEMENT" in html)
except Exception as e:
    print(f"Error: {e}")
