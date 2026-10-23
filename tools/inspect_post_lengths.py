# -*- coding: utf-8 -*-
import os
import glob

gb_root = r"D:\ai\antigravity\global_blog"

episodes = [
    ("Episode 1", "2026-10-22-stanford-cs146s-1"),
    ("Episode 2", "2026-10-23-stanford-cs146s-2"),
    ("Episode 3", "2026-10-24-stanford-cs146s-3"),
]

locales = [
    ("EN (Base)", f"{gb_root}/blog"),
    ("KO", f"{gb_root}/i18n/ko/docusaurus-plugin-content-blog"),
    ("JA", f"{gb_root}/i18n/ja/docusaurus-plugin-content-blog"),
    ("ES", f"{gb_root}/i18n/es/docusaurus-plugin-content-blog"),
    ("ZH-Hans", f"{gb_root}/i18n/zh-Hans/docusaurus-plugin-content-blog"),
    ("ZH-Hant", f"{gb_root}/i18n/zh-Hant/docusaurus-plugin-content-blog"),
]

print(f"{'Episode':<12} | {'Locale':<10} | {'Char Count':<12} | {'Word Count':<12} | {'Status':<15}")
print("-" * 70)

results = []
for ep_name, ep_folder in episodes:
    for loc_name, loc_base in locales:
        file_path = os.path.join(loc_base, ep_folder, "index.md")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                # Exclude frontmatter for pure content length
                parts = content.split("---", 2)
                body = parts[2] if len(parts) >= 3 else content
                char_len = len(body.strip())
                word_len = len(body.split())
                
                # Evaluation rule:
                # Korean / English: target at least 2,500 chars (preferably 4,000+ chars)
                # If char_len < 2500, mark as UNDER_LENGTH
                status = "OK" if char_len >= 3000 else ("MODERATE" if char_len >= 2000 else "UNDER_LENGTH")
                results.append((ep_name, loc_name, char_len, word_len, status, file_path))
                print(f"{ep_name:<12} | {loc_name:<10} | {char_len:<12} | {word_len:<12} | {status:<15}")
        else:
            print(f"{ep_name:<12} | {loc_name:<10} | NOT FOUND")

# Also check Naver Blog posts
print("\n=== Naver Blog Companion Posts ===")
nb_root = r"D:\ai\antigravity\naver_blog\posts"
nb_posts = [
    ("Episode 1", f"{nb_root}/2026-10-22/stanford_cs146s_1/post.md"),
    ("Episode 2", f"{nb_root}/2026-10-23/stanford_cs146s_2/post.md"),
    ("Episode 3", f"{nb_root}/2026-10-24/stanford_cs146s_3/post.md"),
]
for ep_name, p in nb_posts:
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            c = f.read()
            char_len = len(c.strip())
            word_len = len(c.split())
            status = "OK" if char_len >= 2000 else "UNDER_LENGTH"
            print(f"{ep_name:<12} | {'Naver Blog':<10} | {char_len:<12} | {word_len:<12} | {status:<15}")
    else:
        print(f"{ep_name:<12} | {'Naver Blog':<10} | NOT FOUND")
