#!/usr/bin/env python3
import os

TOOLS_DIR = r"D:\ai\antigravity\global_blog\tools"
for f in sorted(os.listdir(TOOLS_DIR)):
    if f.endswith(".py"):
        p = os.path.join(TOOLS_DIR, f)
        try:
            with open(p, "r", encoding="utf-8", errors="ignore") as fp:
                content = fp.read()
                if "matplotlib" in content or "savefig" in content or "FancyBboxPatch" in content or "PIL" in content:
                    print(f"{f:<40} (has matplotlib/savefig/PIL)")
        except Exception:
            pass
