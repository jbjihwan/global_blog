#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch deploy Stanford CS146S Lectures #8, #9, #10 from staging into production.
"""
import os
import sys
import json
from datetime import datetime

GB_ROOT = r"D:\ai\antigravity\global_blog"
sys.path.insert(0, os.path.join(GB_ROOT, "tools"))

from deploy_staged_post import deploy_post

SLUGS_TO_DEPLOY = [
    "2026-10-29-stanford-cs146s-8",
    "2026-10-30-stanford-cs146s-9",
    "2026-10-31-stanford-cs146s-10",
]

def main():
    print("=" * 70)
    print("Promoting Stanford CS146S Lectures #8, #9, #10 to Production...")
    print("=" * 70)
    
    for slug in SLUGS_TO_DEPLOY:
        print(f"\n---> Promoting: {slug}")
        success = deploy_post(slug, trigger_publish=False)
        if not success:
            print(f"[FAIL] Failed to promote {slug}", file=sys.stderr)
            sys.exit(1)
            
        # Update stage_info.json
        info_path = os.path.join(GB_ROOT, "배포대기", slug, "stage_info.json")
        if os.path.exists(info_path):
            try:
                with open(info_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                data["status"] = "deployed"
                data["deployed_at"] = datetime.now().isoformat()
                with open(info_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                print(f"[OK] Updated {slug}/stage_info.json status to 'deployed'.")
            except Exception as e:
                print(f"[WARN] Failed to update stage_info.json for {slug}: {e}")
                
    print("\n[ALL PROMOTIONS SUCCESSFUL]")
    print("All 3 lectures promoted across blog/, i18n/ (ko, ja, es, zh-Hans, zh-Hant), and naver_blog/posts/staged/.")

if __name__ == "__main__":
    main()
