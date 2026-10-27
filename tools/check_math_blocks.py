# -*- coding: utf-8 -*-
import glob
import os

def check():
    paths = [
        r"D:\ai\antigravity\global_blog\blog\2026-11-01-stanford-cs329a-1\index.md",
        r"D:\ai\antigravity\global_blog\배포대기\2026-11-01-stanford-cs329a-1\**\index.md",
        r"D:\ai\antigravity\global_blog\i18n\*\docusaurus-plugin-content-blog\2026-11-01-stanford-cs329a-1\index.md"
    ]
    all_files = []
    for p in paths:
        all_files.extend(glob.glob(p, recursive=True))
    all_files = sorted(list(set(all_files)))
    
    print(f"Total files found: {len(all_files)}")
    for f in all_files:
        with open(f, "r", encoding="utf-8") as fp:
            lines = fp.readlines()
        math_lines = [(i+1, line.strip()) for i, line in enumerate(lines) if "$$" in line]
        if math_lines:
            print(f"\n[FILE] {f}: {len(math_lines)} lines with '$$'")
            for line_no, content in math_lines:
                print(f"  Line {line_no}: {content[:100]}")
        else:
            print(f"[OK] {f} has no '$$'")

if __name__ == "__main__":
    check()
