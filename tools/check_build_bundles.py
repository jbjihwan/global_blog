# -*- coding: utf-8 -*-
import re
from pathlib import Path

BUILD = Path(r"D:\ai\antigravity\global_blog\build")

def scan_build():
    html_hits = []
    js_hits = []
    for p in BUILD.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix in [".html", ".js", ".json", ".xml"]:
            text = p.read_text(encoding="utf-8", errors="ignore")
            matches = re.findall(r"suicide|자살|자해|mental-crisis", text, re.I)
            if matches:
                rel = p.relative_to(BUILD)
                if p.suffix == ".html":
                    html_hits.append((str(rel), len(matches), set(matches)))
                else:
                    js_hits.append((str(rel), len(matches), set(matches)))

    print(f"HTML files with hits: {len(html_hits)}")
    for f, cnt, m in html_hits[:20]:
        print("  HTML:", f, cnt, m)
    print(f"JS/JSON/XML files with hits: {len(js_hits)}")
    for f, cnt, m in js_hits[:20]:
        print("  ASSET:", f, cnt, m)

if __name__ == "__main__":
    scan_build()
