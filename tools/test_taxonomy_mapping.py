import os
import re
from pathlib import Path

BLOG_DIR = Path(r"D:\ai\antigravity\global_blog\blog")

def classify_slug(slug: str):
    s = slug.lower()
    
    # 1. Theory
    if "stanford-cs146s" in s:
        return "theory", "ai", "lecture"
    if "stanford-cs329a" in s:
        return "theory", "ai", "lecture"
        
    # 2. Practice -> Security
    if any(k in s for k in ["static-site-security", "npm-overrides", "cloudflare", "custom-domain", "adsense", "ads-txt"]):
        if "npm-overrides" in s:
            return "practice", "security", "project-npm-cve"
        return "practice", "security", "project-security-infra"
        
    # 2. Practice -> AI
    if "sdc-" in s:
        return "practice", "ai", "project-sdc"
    if any(k in s for k in ["national-budget", "autonomous-budget", "local-subsidy", "education-grant"]):
        return "practice", "ai", "project-budget"
    if any(k in s for k in ["mental-crisis", "crisis-detection"]):
        return "practice", "ai", "project-crisis"
    if "maeumjigi" in s:
        return "practice", "ai", "project-maeumjigi"
    if "vision-anpr" in s:
        return "practice", "ai", "project-anpr"
    if "rl-qlearning" in s:
        return "practice", "ai", "project-rl"
        
    return "practice", "misc", "unknown"

posts = []
for p in sorted(BLOG_DIR.iterdir()):
    if p.is_dir():
        l1, l2, l3 = classify_slug(p.name)
        posts.append((p.name, l1, l2, l3))

print(f"Total posts checked: {len(posts)}")
stats = {}
for name, l1, l2, l3 in posts:
    key = f"{l1} > {l2} > {l3}"
    stats[key] = stats.get(key, 0) + 1

for k, v in sorted(stats.items()):
    print(f"  {k}: {v} posts")
