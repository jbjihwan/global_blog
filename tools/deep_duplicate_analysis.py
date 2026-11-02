# -*- coding: utf-8 -*-
"""
deep_duplicate_analysis.py - Detailed inspection of date overlaps, top similarity pairs, and image reuse.
"""

import os
import re
import hashlib
from collections import defaultdict
from itertools import combinations

BLOG_EN_DIR = "global_blog/blog"
BLOG_KO_DIR = "global_blog/i18n/ko/docusaurus-plugin-content-blog"

def parse_frontmatter(content):
    meta = {}
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    meta[k] = v
            body = parts[2]
    return meta, body

def clean_body(body_text):
    text = re.sub(r"```[\s\S]*?```", " ", body_text)
    text = re.sub(r"\{/\*[\s\S]*?\*/\}", " ", text)
    text = re.sub(r"<!--[\s\S]*?-->", " ", text)
    text = re.sub(r"!\[.*?\]\(.*?\)", " ", text)
    text = re.sub(r"\[.*?\]\(.*?\)", " ", text)
    text = re.sub(r"[#*`>|~_\-\+]", " ", text)
    words = [w.lower() for w in re.findall(r"\b\w+\b", text) if len(w) > 2]
    return words

def get_3grams(words):
    if len(words) < 3:
        return set(words)
    return set(zip(words[:-2], words[1:-1], words[2:]))

def jaccard(set_a, set_b):
    if not set_a or not set_b:
        return 0.0
    u = len(set_a.union(set_b))
    return len(set_a.intersection(set_b)) / u if u > 0 else 0.0

def main():
    en_folders = sorted([f for f in os.listdir(BLOG_EN_DIR) if os.path.isdir(os.path.join(BLOG_EN_DIR, f)) and f != 'authors'])

    posts = {}
    dates = defaultdict(list)
    image_hashes = defaultdict(list)

    for f in en_folders:
        p = os.path.join(BLOG_EN_DIR, f, "index.md")
        with open(p, "r", encoding="utf-8") as fp:
            c = fp.read()
        meta, body = parse_frontmatter(c)
        d = meta.get("date", f[:10])
        dates[d].append(f)
        posts[f] = {
            "meta": meta,
            "date": d,
            "title": meta.get("title", ""),
            "body": body,
            "words": clean_body(body),
            "3grams": get_3grams(clean_body(body))
        }

        # Check images
        img_dir = os.path.join(BLOG_EN_DIR, f, "images")
        if os.path.exists(img_dir):
            for img in os.listdir(img_dir):
                ip = os.path.join(img_dir, img)
                if os.path.isfile(ip):
                    with open(ip, "rb") as ifp:
                        h = hashlib.md5(ifp.read()).hexdigest()
                    image_hashes[h].append((f, img))

    print("=" * 80)
    print("📊 [DEEP DUPLICATE ANALYSIS RESULTS]")
    print("=" * 80)

    # 1. Dates Analysis
    print("\n[1] Dates Analysis (Multiple Posts on Same Date):")
    mult_dates = {d: fs for d, fs in dates.items() if len(fs) > 1}
    print(f"Total dates with > 1 post: {len(mult_dates)}")
    for d in sorted(mult_dates.keys()):
        print(f"  • Date: {d} ({len(mult_dates[d])} posts)")
        for post in mult_dates[d]:
            print(f"      - {post}: {posts[post]['title'][:60]}")

    # 2. Image Re-use Analysis
    print("\n[2] Cover & Content Image Re-use Analysis:")
    reused_images = {h: imgs for h, imgs in image_hashes.items() if len(imgs) > 1}
    if reused_images:
        print(f"Found {len(reused_images)} instances where an image hash is shared:")
        for h, imgs in reused_images.items():
            print(f"  • Hash {h[:8]}: {len(imgs)} occurrences")
            for f, img in imgs:
                print(f"      - {f}/{img}")
    else:
        print("  ✓ Zero image hash collisions detected. Every image is uniquely generated.")

    # 3. Top 15 Highest Similarity Pairs (3-Grams)
    print("\n[3] Top 15 Highest Jaccard 3-Gram Similarity Pairs:")
    pairs_sim = []
    for f1, f2 in combinations(en_folders, 2):
        sim = jaccard(posts[f1]["3grams"], posts[f2]["3grams"])
        vocab_sim = jaccard(set(posts[f1]["words"]), set(posts[f2]["words"]))
        pairs_sim.append((sim, vocab_sim, f1, f2))

    pairs_sim.sort(key=lambda x: x[0], reverse=True)
    for sim, v_sim, f1, f2 in pairs_sim[:15]:
        print(f"  • 3-gram Sim: {sim*100:5.2f}% | Vocab Sim: {v_sim*100:5.2f}%")
        print(f"      A: {f1} -> {posts[f1]['title'][:50]}")
        print(f"      B: {f2} -> {posts[f2]['title'][:50]}")

    # 4. Same check for Korean
    ko_folders = sorted([f for f in os.listdir(BLOG_KO_DIR) if os.path.isdir(os.path.join(BLOG_KO_DIR, f)) and f != 'authors'])
    ko_posts = {}
    for f in ko_folders:
        p = os.path.join(BLOG_KO_DIR, f, "index.md")
        with open(p, "r", encoding="utf-8") as fp:
            c = fp.read()
        meta, body = parse_frontmatter(c)
        ko_posts[f] = {
            "meta": meta,
            "title": meta.get("title", ""),
            "words": clean_body(body),
            "3grams": get_3grams(clean_body(body))
        }

    print("\n[4] Top 15 Highest Jaccard 3-Gram Similarity Pairs in KO:")
    ko_pairs = []
    for f1, f2 in combinations(ko_folders, 2):
        sim = jaccard(ko_posts[f1]["3grams"], ko_posts[f2]["3grams"])
        vocab_sim = jaccard(set(ko_posts[f1]["words"]), set(ko_posts[f2]["words"]))
        ko_pairs.append((sim, vocab_sim, f1, f2))

    ko_pairs.sort(key=lambda x: x[0], reverse=True)
    for sim, v_sim, f1, f2 in ko_pairs[:15]:
        print(f"  • 3-gram Sim: {sim*100:5.2f}% | Vocab Sim: {v_sim*100:5.2f}%")
        print(f"      A: {f1} -> {ko_posts[f1]['title'][:50]}")
        print(f"      B: {f2} -> {ko_posts[f2]['title'][:50]}")

if __name__ == "__main__":
    main()
