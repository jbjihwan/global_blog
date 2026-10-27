# -*- coding: utf-8 -*-
import glob
import os
import re

base_dir = r"D:\ai\antigravity\global_blog\배포대기\2026-11-03-stanford-cs329a-3"
blog_file = os.path.join(base_dir, "blog", "index.md")
i18n_files = sorted(glob.glob(os.path.join(base_dir, "i18n", "*", "index.md")))

all_files = [blog_file] + i18n_files
print(f"=== Stanford CS329A Episode 3 Staging Length Verification ===\n")
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
