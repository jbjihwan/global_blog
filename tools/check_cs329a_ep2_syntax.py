# -*- coding: utf-8 -*-
import glob
import os
import re

files = [
    r"D:\ai\antigravity\global_blog\blog\2026-11-02-stanford-cs329a-2\index.md"
] + glob.glob(r"D:\ai\antigravity\global_blog\i18n\*\docusaurus-plugin-content-blog\2026-11-02-stanford-cs329a-2\index.md")

print(f"Checking {len(files)} files for CS329A Ep2...")
for f in files:
    with open(f, "r", encoding="utf-8") as fp:
        lines = fp.readlines()
    
    # 1. Check for $$
    has_double_dollar = [i+1 for i, l in enumerate(lines) if "$$" in l]
    if has_double_dollar:
        print(f"[FAIL] {f}: $$ on lines {has_double_dollar}")
    else:
        print(f"[OK] {os.path.basename(os.path.dirname(os.path.dirname(f)))}: {len(lines)} lines, no '$$'")

