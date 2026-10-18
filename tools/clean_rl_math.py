#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clean unrendered math formulas ($...$) in RL series (5 posts across 4 locales)
into standard Unicode / inline code expressions.
"""

import os
import glob
import re

BASE_DIR = r"D:\ai\antigravity\global_blog"

LOCALE_DIRS = [
    os.path.join(BASE_DIR, "blog"),
    os.path.join(BASE_DIR, "i18n", "ko", "docusaurus-plugin-content-blog"),
    os.path.join(BASE_DIR, "i18n", "ja", "docusaurus-plugin-content-blog"),
    os.path.join(BASE_DIR, "i18n", "es", "docusaurus-plugin-content-blog"),
]

REPLACEMENTS = [
    (r"\$O\(1\)\$", "O(1)"),
    (r"\$×\$", "×"),
    (r"\$\[-π,\s*π\]\$", "[-π, π]"),
    (r"\$45°\$", "45°"),
    (r"\$648\s*×\s*4\s*=\s*2,592\$", "648 × 4 = 2,592"),
    (r"\$`<=\s*0\.10m`\s*\\rightarrow\$", "≤ 0.10m →"),
    (r"\$`<=\s*0\.08m`\s*\\rightarrow\$", "≤ 0.08m →"),
    (r"\$\\epsilon\$-greedy", "ε-greedy"),
    (r"\$\\epsilon\$\s*-\s*greedy", "ε-greedy"),
    (r"\$\\epsilon__min\$", "ε_min"),
    (r"\$\\epsilon_min\$", "ε_min"),
    (r"\$\\epsilon\s*\\approx\s*0\.22\$", "ε ≈ 0.22"),
    (r"\$\\epsilon\s*=\s*1\.0\$", "ε = 1.0"),
    (r"\$\\epsilon\s*=\s*0\.05\$", "ε = 0.05"),
    (r"\$\\epsilon\$", "ε"),
    (r"\$Q\(s,\s*a\)\$", "Q(s, a)"),
    (r"\$\\alpha\s*=\s*0\.1\$", "α = 0.1"),
    (r"\$\\alpha\$", "α"),
    (r"\$\\gamma\s*=\s*0\.99\$", "γ = 0.99"),
    (r"\$\\gamma\$", "γ"),
    (r"\$1\.2m\s*\\times\s*1\.2m\$", "1.2m × 1.2m"),
]

def clean_file(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    new_text = text
    for pat, repl in REPLACEMENTS:
        new_text = re.sub(pat, repl, new_text)

    if new_text != text:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(new_text)
        return True
    return False

def main():
    cleaned_count = 0
    for d in LOCALE_DIRS:
        for ep in range(1, 6):
            files = glob.glob(os.path.join(d, f"*-rl-qlearning-{ep}", "index.md"))
            for fpath in files:
                if clean_file(fpath):
                    cleaned_count += 1
                    print(f"Cleaned math in: {os.path.relpath(fpath, BASE_DIR)}")
    print(f"Total files updated: {cleaned_count}")

if __name__ == "__main__":
    main()
