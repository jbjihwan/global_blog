# -*- coding: utf-8 -*-
import os
import re
from optimize_serp_snippets import OPTIMIZATIONS, update_file, BASE_DIR

STAGING_DIR = os.path.join(BASE_DIR, "배포대기")

def sync_staging():
    print("=" * 70)
    print("🚀 [Staging 동기화] 배포대기 폴더 내 SERP 스니펫 업데이트")
    print("=" * 70)

    count = 0
    for post_dir, locale_dict in OPTIMIZATIONS.items():
        staged_post_dir = os.path.join(STAGING_DIR, post_dir)
        if not os.path.exists(staged_post_dir):
            continue

        for locale, meta in locale_dict.items():
            if locale == "en":
                path = os.path.join(staged_post_dir, "blog", "index.md")
            else:
                path = os.path.join(staged_post_dir, "i18n", locale, "index.md")

            if os.path.exists(path):
                if update_file(path, meta):
                    print(f"[STAGED {locale:^7}] {post_dir} -> {path}")
                    count += 1

    print(f"✅ 배포대기 내 총 {count}개 파일 동기화 완료!")

if __name__ == "__main__":
    sync_staging()
