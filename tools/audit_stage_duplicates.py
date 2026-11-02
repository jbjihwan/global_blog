import os
import json
import glob
import hashlib
import re
from collections import defaultdict

STAGE_DIR = r"D:\ai\antigravity\global_blog\배포대기"
BLOG_DIR = r"D:\ai\antigravity\global_blog\blog"

def get_frontmatter(file_path):
    if not os.path.exists(file_path):
        return {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
        if not match:
            return {"_body": content}
        fm_text, body = match.groups()
        meta = {"_body": body}
        for line in fm_text.splitlines():
            line = line.strip()
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip("'\"")
        return meta
    except Exception as e:
        return {"_error": str(e)}

def compute_hash(text):
    # Normalize whitespace before hashing
    norm = re.sub(r"\s+", " ", text).strip()
    return hashlib.md5(norm.encode("utf-8")).hexdigest()

def get_ngrams(text, n=3):
    tokens = [w for w in re.findall(r"[\w가-힣]+", text.lower()) if len(w) > 1]
    if len(tokens) < n:
        return set(tokens)
    return set(tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1))

def jaccard(s1, s2):
    if not s1 or not s2:
        return 0.0
    return len(s1 & s2) / len(s1 | s2)

def main():
    items = sorted(os.listdir(STAGE_DIR))
    print(f"Total entries in 배포대기: {len(items)}")

    stage_records = []
    
    for item in items:
        item_path = os.path.join(STAGE_DIR, item)
        if not os.path.isdir(item_path):
            print(f"[NON-DIR FILE] {item}")
            continue

        stage_json_file = os.path.join(item_path, "stage_info.json")
        blog_idx = os.path.join(item_path, "blog", "index.md")
        naver_post = os.path.join(item_path, "naver", "post.md")

        # Find all md files inside
        all_md_files = []
        for root, _, files in os.walk(item_path):
            for f in files:
                if f.endswith(".md"):
                    all_md_files.append(os.path.relpath(os.path.join(root, f), item_path))

        stage_info = {}
        if os.path.exists(stage_json_file):
            try:
                with open(stage_json_file, "r", encoding="utf-8") as f:
                    stage_info = json.load(f)
            except Exception as e:
                stage_info = {"_error": str(e)}

        fm_blog = get_frontmatter(blog_idx)
        fm_naver = get_frontmatter(naver_post)

        title = stage_info.get("title") or fm_blog.get("title") or fm_naver.get("title") or ""
        slug = stage_info.get("slug") or fm_blog.get("slug") or item
        date = stage_info.get("date") or fm_blog.get("date") or ""

        blog_body = fm_blog.get("_body", "")
        naver_body = fm_naver.get("_body", "")

        record = {
            "folder": item,
            "title": title,
            "slug": slug,
            "date": date,
            "has_stage_json": os.path.exists(stage_json_file),
            "has_blog_idx": os.path.exists(blog_idx),
            "has_naver_post": os.path.exists(naver_post),
            "all_md_files": all_md_files,
            "blog_hash": compute_hash(blog_body) if blog_body else None,
            "naver_hash": compute_hash(naver_body) if naver_body else None,
            "blog_body": blog_body,
            "naver_body": naver_body,
            "blog_ngrams": get_ngrams(blog_body, 3) if blog_body else set(),
            "naver_ngrams": get_ngrams(naver_body, 3) if naver_body else set(),
        }
        stage_records.append(record)

    print(f"Total post directories audited: {len(stage_records)}")

    # 1. Check for Duplicate Slugs or Titles
    slug_map = defaultdict(list)
    title_map = defaultdict(list)
    blog_hash_map = defaultdict(list)
    naver_hash_map = defaultdict(list)

    for r in stage_records:
        if r["slug"]:
            slug_map[r["slug"]].append(r["folder"])
        if r["title"]:
            title_map[r["title"]].append(r["folder"])
        if r["blog_hash"]:
            blog_hash_map[r["blog_hash"]].append(r["folder"])
        if r["naver_hash"]:
            naver_hash_map[r["naver_hash"]].append(r["folder"])

    dup_slugs = {k: v for k, v in slug_map.items() if len(v) > 1}
    dup_titles = {k: v for k, v in title_map.items() if len(v) > 1}
    dup_blog_hashes = {k: v for k, v in blog_hash_map.items() if len(v) > 1}
    dup_naver_hashes = {k: v for k, v in naver_hash_map.items() if len(v) > 1}

    print("\n=== [1] DUPLICATE CHECK WITHIN 배포대기 ===")
    print(f"Duplicate Slugs: {len(dup_slugs)}")
    for k, v in dup_slugs.items():
        print(f"  Slug '{k}': {v}")

    print(f"Duplicate Titles: {len(dup_titles)}")
    for k, v in dup_titles.items():
        print(f"  Title '{k}': {v}")

    print(f"Duplicate Blog Content Hashes: {len(dup_blog_hashes)}")
    for k, v in dup_blog_hashes.items():
        print(f"  Hash {k}: {v}")

    print(f"Duplicate Naver Content Hashes: {len(dup_naver_hashes)}")
    for k, v in dup_naver_hashes.items():
        print(f"  Hash {k}: {v}")

    # 2. Check for High N-gram Similarity between distinct folders
    print("\n=== [2] HIGH SIMILARITY PAIRS (3-gram Jaccard > 0.30) ===")
    high_sim_count = 0
    for i in range(len(stage_records)):
        for j in range(i + 1, len(stage_records)):
            r1, r2 = stage_records[i], stage_records[j]
            # Check blog
            if r1["blog_ngrams"] and r2["blog_ngrams"]:
                sim = jaccard(r1["blog_ngrams"], r2["blog_ngrams"])
                if sim > 0.30:
                    high_sim_count += 1
                    print(f"  [Blog Similarity {sim*100:.1f}%] {r1['folder']} <--> {r2['folder']}")
            # Check naver
            if r1["naver_ngrams"] and r2["naver_ngrams"]:
                sim = jaccard(r1["naver_ngrams"], r2["naver_ngrams"])
                if sim > 0.30:
                    high_sim_count += 1
                    print(f"  [Naver Similarity {sim*100:.1f}%] {r1['folder']} <--> {r2['folder']}")

    if high_sim_count == 0:
        print("  None found! (All posts are highly unique)")

    # 3. Check for Incomplete / Fragmented folders
    print("\n=== [3] INCOMPLETE / FRAGMENTED / ABNORMAL FOLDERS ===")
    abnormal_count = 0
    for r in stage_records:
        issues = []
        if not r["has_stage_json"]:
            issues.append("Missing stage_info.json")
        if not r["has_blog_idx"]:
            issues.append("Missing blog/index.md")
        if not r["has_naver_post"]:
            issues.append("Missing naver/post.md")
        if issues:
            abnormal_count += 1
            print(f"  {r['folder']}: {', '.join(issues)} | Files: {r['all_md_files']}")

    # 4. Compare 배포대기 vs Active blog/
    print("\n=== [4] COMPARISON WITH ACTIVE blog/ DIRECTORY ===")
    active_folders = set(os.listdir(BLOG_DIR))
    stage_folder_set = set(r["folder"] for r in stage_records)

    in_stage_not_in_blog = stage_folder_set - active_folders
    in_blog_not_in_stage = active_folders - stage_folder_set

    print(f"In 배포대기 but NOT in active blog/ ({len(in_stage_not_in_blog)}):")
    for f in sorted(in_stage_not_in_blog):
        # Check if slug matches any active folder
        matching_rec = next((r for r in stage_records if r["folder"] == f), None)
        s = matching_rec["slug"] if matching_rec else ""
        print(f"  - {f} (slug: {s}, files: {matching_rec['all_md_files'] if matching_rec else []})")

    print(f"\nIn active blog/ but NOT in 배포대기 ({len(in_blog_not_in_stage)}):")
    for f in sorted(in_blog_not_in_stage):
        print(f"  - {f}")

if __name__ == "__main__":
    main()
