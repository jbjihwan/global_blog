# -*- coding: utf-8 -*-
import os
import re

STAGE_DIR = r"D:\ai\antigravity\global_blog\배포대기\2026-11-19-national-budget-ai-audit-findings-performance-evaluation"

forbidden_keywords = [
    "알파아이티", "메트로시스", "시티소프트",
    "소상공인시장진흥공단", "과기부", "과학기술정보통신부"
]

def check():
    all_passed = True
    print(f"Checking directory: {STAGE_DIR}")

    # Check files
    locales = ["en", "ko", "ja", "zh-Hans", "zh-Hant", "es", "de", "fr", "pt-BR"]
    for loc in locales:
        if loc == "en":
            file_path = os.path.join(STAGE_DIR, "blog", "index.md")
            img_path = os.path.join(STAGE_DIR, "blog", "images", "01_national_budget_audit_findings.png")
        else:
            file_path = os.path.join(STAGE_DIR, "i18n", loc, "index.md")
            img_path = os.path.join(STAGE_DIR, "i18n", loc, "images", "01_national_budget_audit_findings.png")

        if not os.path.exists(file_path):
            print(f"[FAIL] Missing post file for {loc}: {file_path}")
            all_passed = False
            continue

        if not os.path.exists(img_path):
            print(f"[FAIL] Missing image file for {loc}: {img_path}")
            all_passed = False

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check frontmatter
        title_match = re.search(r'title:\s*["\']?(.*?)["\']?\n', content)
        desc_match = re.search(r'description:\s*["\']?(.*?)["\']?\n', content)

        if not title_match or not desc_match:
            print(f"[FAIL] Missing title or desc in {loc}")
            all_passed = False
        else:
            title = title_match.group(1)
            desc = desc_match.group(1)
            print(f"[{loc}] Title ({len(title)} chars): {title}")
            print(f"[{loc}] Desc ({len(desc)} chars): {desc}")
            if len(title) > 65:
                print(f"[WARN] Title > 65 chars in {loc}: {len(title)}")
            if len(desc) > 160:
                print(f"[WARN] Desc > 160 chars in {loc}: {len(desc)}")

        # Check forbidden unmasked names
        for kw in forbidden_keywords:
            if kw in content:
                print(f"[CRITICAL FAIL] Unmasked keyword '{kw}' found in {file_path}!")
                all_passed = False

    # Check Naver
    naver_post = os.path.join(STAGE_DIR, "naver", "post.md")
    naver_meta = os.path.join(STAGE_DIR, "naver", "meta.json")
    if not os.path.exists(naver_post) or not os.path.exists(naver_meta):
        print("[FAIL] Missing naver files!")
        all_passed = False
    else:
        with open(naver_post, "r", encoding="utf-8") as f:
            np_content = f.read()
        for kw in forbidden_keywords:
            if kw in np_content:
                print(f"[CRITICAL FAIL] Unmasked keyword '{kw}' found in naver/post.md!")
                all_passed = False
        print("[PASS] Naver blog post verified and clean of forbidden names.")

    if all_passed:
        print("\n=== ALL VERIFICATIONS PASSED SUCCESSFULLY ===")
    else:
        print("\n=== SOME CHECKS FAILED ===")

if __name__ == "__main__":
    check()
