# -*- coding: utf-8 -*-
import os
import re

f = r"D:\ai\antigravity\global_blog\배포대기\2026-11-03-stanford-cs329a-3\blog\index.md"
with open(f, "r", encoding="utf-8") as fp:
    lines = fp.readlines()

content = "".join(lines)
words = len(re.findall(r'\S+', content))
chars = len(content)

print(f"File: {f}")
print(f"Lines: {len(lines)}")
print(f"Words: {words}")
print(f"Chars: {chars}")

# Check for $$
math_lines = [i+1 for i, l in enumerate(lines) if "$$" in l]
if math_lines:
    print(f"[FAIL] Found '$$' on lines: {math_lines}")
else:
    print("[OK] Zero '$$' lines found.")
