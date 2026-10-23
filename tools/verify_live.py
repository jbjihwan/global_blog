# -*- coding: utf-8 -*-
import urllib.request
import re

urls = [
    "https://globaldevlog.com/blog/stanford-cs146s-3-mcp-tool-use-architecture",
    "https://globaldevlog.com/ko/blog/stanford-cs146s-3-mcp-tool-use-architecture",
    "https://globaldevlog.com/blog/static-site-security-npm-audit-truth",
    "https://globaldevlog.com/ko/blog",
]

for url in urls:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            code = resp.getcode()
            html = resp.read().decode("utf-8")
            print(f"[OK] {code}: {url}")
            if "stanford-cs146s-3" in url:
                has_author = "Jaybee" in html
                has_mcp = "MCP" in html or "Model Context Protocol" in html
                print(f"     Author Jaybee: {has_author}, Has MCP: {has_mcp}")
            elif "static-site-security" in url:
                has_2026 = "2026" in html
                print(f"     Updated CTR Title: {has_2026}")
            elif url.endswith("/ko/blog"):
                has_ep3_tab = "3편" in html
                print(f"     Hub Tab 3편: {has_ep3_tab}")
    except Exception as e:
        print(f"[FAIL] {url}: {e}")
