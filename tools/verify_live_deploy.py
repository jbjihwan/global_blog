# -*- coding: utf-8 -*-
import urllib.request
import urllib.error

urls = [
    "https://globaldevlog.com/",
    "https://globaldevlog.com/de/blog",
    "https://globaldevlog.com/fr/blog",
    "https://globaldevlog.com/pt-BR/blog",
    "https://globaldevlog.com/sitemap.xml",
    "https://globaldevlog.com/ads.txt"
]

print("Checking live URLs on https://globaldevlog.com...")
for u in urls:
    req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"[{resp.status}] {u}")
    except urllib.error.HTTPError as e:
        print(f"[{e.code}] {u}")
    except Exception as e:
        print(f"[ERR: {e}] {u}")
