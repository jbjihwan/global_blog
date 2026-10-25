#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch deploy Stanford CS146S Lectures #4, #5, #6, #7 from staging into production.
"""
import os
import sys

GB_ROOT = r"D:\ai\antigravity\global_blog"
sys.path.insert(0, os.path.join(GB_ROOT, "tools"))

from deploy_staged_post import deploy_post

SLUGS_TO_DEPLOY = [
    "2026-10-25-stanford-cs146s-4",
    "2026-10-26-stanford-cs146s-5",
    "2026-10-27-stanford-cs146s-6",
    "2026-10-28-stanford-cs146s-7",
]

def main():
    print("=" * 70)
    print("Promoting Stanford CS146S Lectures #4, #5, #6, #7 to Production...")
    print("=" * 70)
    
    for slug in SLUGS_TO_DEPLOY:
        print(f"\n---> Promoting: {slug}")
        success = deploy_post(slug, trigger_publish=False)
        if not success:
            print(f"[FAIL] Failed to promote {slug}", file=sys.stderr)
            sys.exit(1)
            
    print("\n[ALL PROMOTIONS SUCCESSFUL]")
    print("All 4 lectures promoted across blog/, i18n/ (ko, ja, es, zh-Hans, zh-Hant), and naver_blog/posts/staged/.")

if __name__ == "__main__":
    main()
