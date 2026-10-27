# -*- coding: utf-8 -*-
import glob
import os

TARGET = r"$$\max_\theta \mathbb{E}_{(x, y) \sim \mathcal{D}} \left[ r_\psi(x, y) \right] - \beta \, \mathbb{D}_{\text{KL}}\left(\pi_\theta(y \mid x) \,||\, \pi_{\text{ref}}(y \mid x)\right)$$"

REPLACEMENT = """```text
max_θ E_{(x, y) ~ D} [ r_ψ(x, y) ] - β · D_KL( π_θ(y | x) || π_ref(y | x) )
```"""

def fix():
    paths = [
        r"D:\ai\antigravity\global_blog\blog\2026-11-01-stanford-cs329a-1\index.md",
        r"D:\ai\antigravity\global_blog\배포대기\2026-11-01-stanford-cs329a-1\**\index.md",
        r"D:\ai\antigravity\global_blog\i18n\*\docusaurus-plugin-content-blog\2026-11-01-stanford-cs329a-1\index.md"
    ]
    all_files = []
    for p in paths:
        all_files.extend(glob.glob(p, recursive=True))
    all_files = sorted(list(set(all_files)))
    
    count = 0
    for f in all_files:
        with open(f, "r", encoding="utf-8") as fp:
            content = fp.read()
        if TARGET in content:
            new_content = content.replace(TARGET, REPLACEMENT)
            with open(f, "w", encoding="utf-8") as fp:
                fp.write(new_content)
            count += 1
            print(f"Fixed: {f}")
        else:
            print(f"Target not found in: {f}")
            
    print(f"Total fixed: {count} of {len(all_files)}")

if __name__ == "__main__":
    fix()
