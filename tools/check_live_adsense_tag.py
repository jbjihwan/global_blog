# -*- coding: utf-8 -*-
import urllib.request

url = "https://globaldevlog.com/"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8')
    print("HTML length:", len(html))
    print("Contains adsbygoogle script tag:", "pagead2.googlesyndication.com" in html)
    print("Contains pub-4654073335496617:", "pub-4654073335496617" in html)
    
    # Check if there is any ad code or slots
    lines = [l.strip() for l in html.split('\n') if "googlesyndication" in l]
    for l in lines:
        print("Ad script line:", l)
