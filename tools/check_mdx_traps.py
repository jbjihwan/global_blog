# -*- coding: utf-8 -*-
import glob
import re

def check_mdx_traps():
    files = [
        r"D:\ai\antigravity\global_blog\blog\2026-11-01-stanford-cs329a-1\index.md",
        r"D:\ai\antigravity\global_blog\i18n\ko\docusaurus-plugin-content-blog\2026-11-01-stanford-cs329a-1\index.md"
    ]
    for f in files:
        with open(f, "r", encoding="utf-8") as fp:
            lines = fp.readlines()
        in_code_block = False
        for idx, line in enumerate(lines):
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                continue
            if not in_code_block:
                # Look for { something } or <tag without closing or <number
                if "{" in line and "}" in line:
                    # check if it looks like jsx or latex
                    print(f"Braces outside code block at {f}:{idx+1}: {line.strip()[:80]}")
                # look for < not in html tags or markdown links
                # e.g. x < y
                matches = re.findall(r'[^\`]<[^\`a-zA-Z\/!]', line)
                if matches:
                    print(f"Possible unescaped '<' at {f}:{idx+1}: {line.strip()[:80]}")

if __name__ == "__main__":
    check_mdx_traps()
