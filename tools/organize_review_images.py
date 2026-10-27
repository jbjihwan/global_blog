#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Organize the review images into clean, categorized directories:
- 01_stanford_cs146s
- 02_maeumjigi_capstone
- 03_threat_model_cybersecurity
- 04_rl_qlearning_and_anpr_vision
- 05_devops_dns_adsense_infra

Generates a master Markdown catalog with direct markdown image links and descriptions.
"""

import os
import shutil
import glob

REVIEW_DIR = r"D:\ai\antigravity\global_blog\review_images"

CATEGORIES = {
    "01_threat_model_cybersecurity": [
        "threat", "security_pipeline", "crop_left"
    ],
    "02_stanford_cs146s": [
        "cs146s", "stanford"
    ],
    "03_maeumjigi_capstone": [
        "maeum", "hardcoding", "lora", "alpha", "adapter", "checkpoint", "dataset", "db_401", "eval_completion", "expo"
    ],
    "04_rl_qlearning_and_anpr_vision": [
        "rl-qlearn", "vision-an", "qlearning", "anpr", "edsr", "csrt", "voting", "lane", "intrusion", "plate", "hardware_setup", "aruco"
    ],
    "05_devops_dns_adsense_infra": [
        "dns", "ads_txt", "indexing", "pptx"
    ],
}

# Create category folders
for cat in CATEGORIES:
    os.makedirs(os.path.join(REVIEW_DIR, cat), exist_ok=True)
os.makedirs(os.path.join(REVIEW_DIR, "99_archive_misc"), exist_ok=True)

all_files = [f for f in glob.glob(os.path.join(REVIEW_DIR, "*")) if os.path.isfile(f) and f.lower().endswith(('.png', '.jpg', '.jpeg'))]

catalog = {cat: [] for cat in CATEGORIES}
catalog["99_archive_misc"] = []

for f in all_files:
    fname = os.path.basename(f)
    fname_lower = fname.lower()
    matched = False
    for cat, keywords in CATEGORIES.items():
        if any(kw in fname_lower for kw in keywords):
            dest = os.path.join(REVIEW_DIR, cat, fname)
            shutil.copy2(f, dest)
            catalog[cat].append(fname)
            matched = True
            break
    if not matched:
        dest = os.path.join(REVIEW_DIR, "99_archive_misc", fname)
        shutil.copy2(f, dest)
        catalog["99_archive_misc"].append(fname)

# Generate README.md
readme_path = os.path.join(REVIEW_DIR, "README.md")
with open(readme_path, "w", encoding="utf-8") as rf:
    rf.write("# 🎨 생성 및 블로그 이미지 전체 리뷰 디렉터리 (Review Images)\n\n")
    rf.write("> 사용자 요청: 지금까지 생성된 이미지들을 한눈에 검토하고 하나씩 수정 요청을 진행할 수 있도록 주제별로 분류하여 모아두었습니다.\n")
    rf.write("> **폴더 위치:** `D:\\ai\\antigravity\\global_blog\\review_images\\`\n\n")

    cat_titles = {
        "01_threat_model_cybersecurity": "🛡️ 1. 위협 모델링 & 사이버보안 다이어그램 (수정 대상 1순위)",
        "02_stanford_cs146s": "🎓 2. 스탠포드 CS146S 강의 시리즈 (Lecture 1 ~ 10 다이어그램)",
        "03_maeumjigi_capstone": "🧠 3. 마음지기 캡스톤 프로젝트 (커버, 아키텍처, 개발 일지)",
        "04_rl_qlearning_and_anpr_vision": "🤖 4. 강화학습(RL) & 비전 ANPR 시스템 (평가 곡선, 파이프라인)",
        "05_devops_dns_adsense_infra": "🌐 5. 인프라 / DNS / 애드센스 / SEO 다이어그램",
        "99_archive_misc": "📦 6. 기타 및 이전 생성 아카이브",
    }

    for cat_key, title in cat_titles.items():
        files = catalog.get(cat_key, [])
        rf.write(f"## {title} ({len(files)}개)\n\n")
        rf.write(f"경로: `D:\\ai\\antigravity\\global_blog\\review_images\\{cat_key}\\`\n\n")
        rf.write("| 번호 | 파일명 | 파일 열기 링크 |\n")
        rf.write("| :--- | :--- | :--- |\n")
        for i, fn in enumerate(sorted(files), 1):
            rf.write(f"| {i} | `{fn}` | [{fn}](./{cat_key}/{fn}) |\n")
        rf.write("\n")

print("Review images categorized successfully!")
for k, v in catalog.items():
    print(f"- {k}: {len(v)} files")
