# -*- coding: utf-8 -*-
import urllib.request
import re

urls = [
    "https://globaldevlog.com/blog/stanford-cs146s-2-coding-llms-prompt-engineering",
    "https://globaldevlog.com/ko/blog/stanford-cs146s-2-coding-llms-prompt-engineering",
    "https://globaldevlog.com/ko/blog",
]

for url in urls:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            code = resp.getcode()
            html = resp.read().decode("utf-8")
            print(f"[OK] {code}: {url}")
            if "stanford-cs146s-2" in url:
                has_author = "Jaybee" in html
                has_title = "CS146S" in html
                print(f"     Author Jaybee: {has_author}, Title CS146S: {has_title}")
            elif url.endswith("/ko/blog"):
                has_ep2_tab = "2편" in html
                print(f"     Hub Tab 2편: {has_ep2_tab}")
    except Exception as e:
        print(f"[FAIL] {url}: {e}")
