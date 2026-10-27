# -*- coding: utf-8 -*-
import glob
import os
import re

blog_dir = r"D:\ai\antigravity\global_blog\blog\2026-11-02-stanford-cs329a-2\index.md"
i18n_dirs = sorted(glob.glob(r"D:\ai\antigravity\global_blog\i18n\*\docusaurus-plugin-content-blog\2026-11-02-stanford-cs329a-2\index.md"))

all_files = [blog_dir] + i18n_dirs
print(f"{'Locale':<12} | {'Lines':<6} | {'Words':<7} | {'Chars':<7} | Path")
print("-" * 80)
for bf in all_files:
    if "i18n" in bf:
        locale = bf.split("i18n")[1].split(os.sep)[1]
    else:
        locale = "en (default)"
    with open(bf, "r", encoding="utf-8") as fp:
        content = fp.read()
    lines = content.splitlines()
    words = len(re.findall(r'\S+', content))
    chars = len(content)
    print(f"{locale:<12} | {len(lines):<6} | {words:<7} | {chars:<7} | {os.path.basename(os.path.dirname(bf))}")
