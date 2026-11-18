# -*- coding: utf-8 -*-
"""유지된 23편 내 민감어·AI 대필 표현·단문 여부 점검 스크립트."""
import pathlib
import re

ROOT = pathlib.Path(r"D:\ai\antigravity\global_blog")
BLOG_DIR = ROOT / "blog"
KO_DIR = ROOT / "i18n" / "ko" / "docusaurus-plugin-content-blog"

PATTERNS = [
    "suicide", "suicidal", "self-harm", "자살", "자해", "극단적",
    "claude code", "artificial intelligence (ai)", "ai와 ", "d:\\ai",
]


def scan_dir(d: pathlib.Path, label: str):
    print(f"=== Scanning {label} ===")
    for p in sorted(d.glob("*/index.md*")):
        txt = p.read_text(encoding="utf-8", errors="ignore")
        low = txt.lower()
        hits = [k for k in PATTERNS if k in low]
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", txt, re.S)
        body = m.group(2) if m else txt
        prose = re.sub(r"```.*?```", "", body, flags=re.S)
        words = len(prose.split())
        chars = len(re.sub(r"\s+", "", prose))
        if hits or (label == "EN" and words < 450) or (label == "KO" and chars < 1600):
            print(f"  {p.parent.name}: words={words}, chars={chars}, hits={hits}")
            for h in hits:
                for line in txt.splitlines():
                    if h in line.lower():
                        print(f"    [{h}] {line[:110]}")


if __name__ == "__main__":
    scan_dir(BLOG_DIR, "EN")
    scan_dir(KO_DIR, "KO")
