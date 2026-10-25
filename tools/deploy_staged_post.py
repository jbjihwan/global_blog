#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deploy Staged Post Utility
Copies a staged post from `배포대기/<slug>` into production directories (`blog/` and `i18n/`)
and optionally triggers the zero-popup publish.ps1 deployment script.
"""

import os
import sys
import shutil
import argparse
import subprocess

GB_ROOT = r"D:\ai\antigravity\global_blog"
STAGING_ROOT = os.path.join(GB_ROOT, "배포대기")

def deploy_post(slug_dir_name: str, trigger_publish: bool = True):
    stage_path = os.path.join(STAGING_ROOT, slug_dir_name)
    if not os.path.exists(stage_path):
        print(f"[ERROR] Staged folder not found: {stage_path}", file=sys.stderr)
        return False
        
    print(f"[INFO] Deploying staged post: {slug_dir_name}")
    
    # 1. Copy blog/ (English)
    src_blog = os.path.join(stage_path, "blog")
    dst_blog = os.path.join(GB_ROOT, "blog", slug_dir_name)
    if os.path.exists(src_blog):
        os.makedirs(dst_blog, exist_ok=True)
        for item in os.listdir(src_blog):
            s = os.path.join(src_blog, item)
            d = os.path.join(dst_blog, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)
        print(f"[OK] Deployed English blog to {dst_blog}")
        
    # 2. Copy i18n/ (ko, ja, es, zh-Hans, zh-Hant)
    locales = ["ko", "ja", "es", "zh-Hans", "zh-Hant"]
    src_i18n = os.path.join(stage_path, "i18n")
    if os.path.exists(src_i18n):
        for loc in locales:
            loc_src = os.path.join(src_i18n, loc)
            if os.path.exists(loc_src):
                dst_loc = os.path.join(GB_ROOT, "i18n", loc, "docusaurus-plugin-content-blog", slug_dir_name)
                os.makedirs(dst_loc, exist_ok=True)
                for item in os.listdir(loc_src):
                    s = os.path.join(loc_src, item)
                    d = os.path.join(dst_loc, item)
                    if os.path.isdir(s):
                        shutil.copytree(s, d, dirs_exist_ok=True)
                    else:
                        shutil.copy2(s, d)
                # Also copy images folder to locale if present in blog
                blog_images = os.path.join(src_blog, "images")
                if os.path.exists(blog_images):
                    dst_images = os.path.join(dst_loc, "images")
                    shutil.copytree(blog_images, dst_images, dirs_exist_ok=True)
                print(f"[OK] Deployed [{loc}] translation to {dst_loc}")

    # 3. Copy Naver post if present
    src_naver = os.path.join(stage_path, "naver")
    if os.path.exists(src_naver):
        dst_naver = os.path.join(r"D:\ai\antigravity\naver_blog\posts\staged", slug_dir_name)
        os.makedirs(dst_naver, exist_ok=True)
        shutil.copytree(src_naver, dst_naver, dirs_exist_ok=True)
        print(f"[OK] Synced Naver blog draft to {dst_naver}")
        
    print(f"[SUCCESS] All files staged for {slug_dir_name} copied to production tree.")
    
    if trigger_publish:
        print("[INFO] Triggering publish.ps1...")
        publish_script = os.path.join(GB_ROOT, "tools", "publish.ps1")
        cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-File", publish_script]
        res = subprocess.run(cmd)
        return res.returncode == 0
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deploy a staged post to production")
    parser.add_argument("slug", help="Staged post folder name")
    parser.add_argument("--no-publish", action="store_true", help="Only copy files, do not run publish.ps1")
    args = parser.parse_args()
    
    success = deploy_post(args.slug, trigger_publish=not args.no_publish)
    sys.exit(0 if success else 1)
