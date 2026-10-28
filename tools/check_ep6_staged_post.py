import os
import re
import json

base_dir = r"D:\ai\antigravity\global_blog\배포대기\2026-11-23-national-budget-ai-inspector-portal-verification-system"

locales = {
    "en": os.path.join(base_dir, "blog", "index.md"),
    "ko": os.path.join(base_dir, "i18n", "ko", "index.md"),
    "ja": os.path.join(base_dir, "i18n", "ja", "index.md"),
    "zh-Hans": os.path.join(base_dir, "i18n", "zh-Hans", "index.md"),
    "zh-Hant": os.path.join(base_dir, "i18n", "zh-Hant", "index.md"),
    "es": os.path.join(base_dir, "i18n", "es", "index.md"),
    "de": os.path.join(base_dir, "i18n", "de", "index.md"),
    "fr": os.path.join(base_dir, "i18n", "fr", "index.md"),
    "pt-BR": os.path.join(base_dir, "i18n", "pt-BR", "index.md")
}

errors = []

# 1. Check all index.md
print("=== Checking Locales Frontmatter and SERP Constraints ===")
for loc, path in locales.items():
    if not os.path.exists(path):
        errors.append(f"Missing file: {path}")
        continue
    
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check title
    m_title = re.search(r'^title:\s*["\']?(.*?)["\']?$', content, re.M)
    if not m_title:
        errors.append(f"[{loc}] Missing title in frontmatter")
    else:
        title = m_title.group(1).strip()
        t_len = len(title)
        print(f"[{loc}] Title ({t_len} chars): {title}")
        if t_len > 65:
            errors.append(f"[{loc}] Title exceeds 65 chars: {t_len} chars")

    # Check description
    m_desc = re.search(r'^description:\s*["\']?(.*?)["\']?$', content, re.M)
    if not m_desc:
        errors.append(f"[{loc}] Missing description in frontmatter")
    else:
        desc = m_desc.group(1).strip()
        d_len = len(desc)
        print(f"[{loc}] Desc ({d_len} chars): {desc}")
        if d_len > 160:
            errors.append(f"[{loc}] Description exceeds 160 chars: {d_len} chars")
    
    # Check image reference
    if "./images/01_national_budget_inspector_portal.png" not in content:
        errors.append(f"[{loc}] Missing cover image reference in markdown")

print("\n=== Checking Image Files ===")
image_rel_paths = [
    os.path.join("blog", "images", "01_national_budget_inspector_portal.png"),
    os.path.join("i18n", "ko", "images", "01_national_budget_inspector_portal.png"),
    os.path.join("i18n", "ja", "images", "01_national_budget_inspector_portal.png"),
    os.path.join("i18n", "zh-Hans", "images", "01_national_budget_inspector_portal.png"),
    os.path.join("i18n", "zh-Hant", "images", "01_national_budget_inspector_portal.png"),
    os.path.join("i18n", "es", "images", "01_national_budget_inspector_portal.png"),
    os.path.join("i18n", "de", "images", "01_national_budget_inspector_portal.png"),
    os.path.join("i18n", "fr", "images", "01_national_budget_inspector_portal.png"),
    os.path.join("i18n", "pt-BR", "images", "01_national_budget_inspector_portal.png")
]
for img_rel in image_rel_paths:
    full_img = os.path.join(base_dir, img_rel)
    if not os.path.exists(full_img):
        errors.append(f"Missing image: {full_img}")
    else:
        sz = os.path.getsize(full_img)
        if sz < 1000:
            errors.append(f"Suspicious image size ({sz} bytes): {full_img}")
        else:
            print(f"Image OK ({sz} bytes): {img_rel}")

print("\n=== Checking Naver and Metadata Files ===")
naver_post = os.path.join(base_dir, "naver", "post.md")
naver_meta = os.path.join(base_dir, "naver", "meta.json")
stage_info = os.path.join(base_dir, "stage_info.json")

for p in [naver_post, naver_meta, stage_info]:
    if not os.path.exists(p):
        errors.append(f"Missing file: {p}")
    else:
        sz = os.path.getsize(p)
        print(f"File OK ({sz} bytes): {os.path.basename(p)}")

# Anonymization check
forbidden_keywords = [
    "한국지능정보사회진흥원",
    "정보통신산업진흥원",
    "소상공인시장진흥공단",
    "한국인터넷진흥원",
    "서울올림픽기념국민체육진흥공단"
]

print("\n=== Checking Anonymization Mandate ===")
all_files_to_check = list(locales.values()) + [naver_post]
for fpath in all_files_to_check:
    if os.path.exists(fpath):
        with open(fpath, "r", encoding="utf-8") as f:
            text = f.read()
        for kw in forbidden_keywords:
            if kw in text:
                errors.append(f"Anonymization violation in {fpath}: found '{kw}'")

print("\n====================")
print("VERIFICATION RESULT")
print("====================")
if errors:
    print(f"FAILED with {len(errors)} errors:")
    for err in errors:
        print(f" - {err}")
    exit(1)
else:
    print("ALL CHECKS PASSED PERFECTLY! (Episode #6 ready)")
