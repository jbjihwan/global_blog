# -*- coding: utf-8 -*-
import urllib.request

sitemap_url = "https://globaldevlog.com/sitemap.xml"
pings = [
    f"https://www.google.com/ping?sitemap={sitemap_url}",
    f"https://www.bing.com/ping?sitemap={sitemap_url}"
]

for p in pings:
    try:
        req = urllib.request.Request(p, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"[{resp.status}] Pinged {p}")
    except Exception as e:
        print(f"[NOTE] Ping response: {e}")
