#!/usr/bin/env python3
import shutil
import os

blog_root = r"D:\ai\antigravity\global_blog"
art_dir = r"C:\Users\jbgih\.gemini\antigravity-cli\brain\a2c8435f-707b-431d-a280-dad177e26fdc"

files = {
    "threat_en.png": os.path.join(blog_root, "blog", "2026-10-18-static-site-security-hardening", "images", "01_threat_model.png"),
    "threat_ja.png": os.path.join(blog_root, "i18n", "ja", "docusaurus-plugin-content-blog", "2026-10-18-static-site-security-hardening", "images", "01_threat_model.png"),
    "threat_es.png": os.path.join(blog_root, "i18n", "es", "docusaurus-plugin-content-blog", "2026-10-18-static-site-security-hardening", "images", "01_threat_model.png"),
    "threat_zh.png": os.path.join(blog_root, "i18n", "zh-Hans", "docusaurus-plugin-content-blog", "2026-10-18-static-site-security-hardening", "images", "01_threat_model.png"),
}

for name, src in files.items():
    dst = os.path.join(art_dir, name)
    shutil.copy(src, dst)
    print(f"Copied {name}")
