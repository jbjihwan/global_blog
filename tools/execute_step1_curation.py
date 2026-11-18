# -*- coding: utf-8 -*-
"""Step 1 실행: 83편 전수 선별 보고서(CURATION_PLAN_83_POSTS.md) 생성 및 비대상 60편·미사용 다국어 폴더 _old 이동."""
import pathlib
import shutil
from audit_and_curate_83_posts import BLOG_DIR, KO_DIR, ROOT, classify, parse_post

OLD_DIR = ROOT / "_old"


def main():
    en_posts = {p.parent.name: parse_post(p) for p in sorted(BLOG_DIR.glob("*/index.md*"))}
    ko_posts = {p.parent.name: parse_post(p) for p in sorted(KO_DIR.glob("*/index.md*"))}

    keep_rows = []
    arch_rows = []

    for folder, en in sorted(en_posts.items()):
        ko = ko_posts.get(folder, {"prose_chars": 0, "prose_words": 0})
        decision, reason = classify(en, ko)
        row = {
            "decision": decision,
            "folder": folder,
            "date": en["date"],
            "slug": en["slug"],
            "en_words": en["prose_words"],
            "ko_chars": ko["prose_chars"],
            "title": en["title"],
            "reason": reason,
        }
        if decision.startswith("KEEP"):
            keep_rows.append(row)
        else:
            arch_rows.append(row)

    # 1. Write CURATION_PLAN_83_POSTS.md
    lines = [
        "# 글로벌 블로그 83편 전수 선별 및 정예화 계획표 (Step 1)",
        "",
        "> 작성일: 2026-11-18 · 기준: Google AdSense 「가치가 별로 없는 콘텐츠」 및 Search Console `Crawled - currently not indexed` 해소",
        "",
        "## 1. 선별 요약",
        "",
        f"- **기존 전체 게시글**: {len(en_posts)}편 (영문 `blog/` {len(en_posts)}편, 한국어 `i18n/ko/` {len(ko_posts)}편)",
        f"- **유지 및 고도화(`KEEP`)**: **{len(keep_rows)}편** (실제 에러 트레이스백·아키텍처 병목·하드웨어/보안 트러블슈팅 중심 + Step 3 신규 오류 해결 글 1편 추가 예정 = 총 24편 체제)",
        f"- **보관 이동(`_old/` 분리)**: **{len(arch_rows)}편**",
        "  - `ARCHIVE_LECTURE` (27편): 스탠포드 CS329A(17편)·CS146S(10편) 공개 강의 요약본 (2차 요약 콘텐츠 성격)",
        "  - `ARCHIVE_DIARY` (17편): 마음지기 캡스톤 단문 일기·중간보고·일반 진행 기록",
        "  - `ARCHIVE_SIMULATION` (9편): `[Simulation]` 합성 데이터·재구성 로그 경고문이 포함된 공공예산 감사 시리즈",
        "  - `ARCHIVE_YMYL` (4편): 자살·정신건강 위기 감지 YMYL 고위험 민감 주제 시리즈",
        "  - `ARCHIVE_ADSENSE_META` (3편): 애드센스 승인·ads.txt 메타 가이드",
        "",
        "---",
        "",
        f"## 2. 유지 및 집중 고도화 대상 ({len(keep_rows)}편)",
        "",
        "| 구분 | 폴더명 | 기존 날짜 | 영문 본문(단어) | 한국어 본문(자) | 제목 | 조치 내용 |",
        "| :---: | :--- | :---: | :---: | :---: | :--- | :--- |",
    ]
    for r in keep_rows:
        lines.append(
            f"| `{r['decision']}` | `{r['folder']}` | {r['date']} | {r['en_words']}w | {r['ko_chars']}자 | {r['title']} | {r['reason']} |"
        )

    lines.extend([
        "",
        "---",
        "",
        f"## 3. `_old/` 보관(비공개 분리) 대상 ({len(arch_rows)}편)",
        "",
        "| 분류 | 폴더명 | 기존 날짜 | 영문 본문(단어) | 한국어 본문(자) | 제목 | 분리 사유 |",
        "| :---: | :--- | :---: | :---: | :---: | :--- | :--- |",
    ])
    for r in arch_rows:
        lines.append(
            f"| `{r['decision']}` | `{r['folder']}` | {r['date']} | {r['en_words']}w | {r['ko_chars']}자 | {r['title']} | {r['reason']} |"
        )

    report_path = ROOT / "CURATION_PLAN_83_POSTS.md"
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Created {report_path} (KEEP={len(keep_rows)}, ARCHIVE={len(arch_rows)})")

    # 2. Move archived posts to _old/blog and _old/i18n_ko_blog
    old_blog = OLD_DIR / "blog"
    old_ko_blog = OLD_DIR / "i18n_ko_blog"
    old_blog.mkdir(parents=True, exist_ok=True)
    old_ko_blog.mkdir(parents=True, exist_ok=True)

    moved_en = 0
    moved_ko = 0
    for r in arch_rows:
        folder = r["folder"]
        src_en = BLOG_DIR / folder
        if src_en.exists():
            dst_en = old_blog / folder
            if dst_en.exists():
                shutil.rmtree(dst_en)
            shutil.move(str(src_en), str(dst_en))
            moved_en += 1
        src_ko = KO_DIR / folder
        if src_ko.exists():
            dst_ko = old_ko_blog / folder
            if dst_ko.exists():
                shutil.rmtree(dst_ko)
            shutil.move(str(src_ko), str(dst_ko))
            moved_ko += 1

    # 3. Move unused 7 locale directories from i18n/ to _old/i18n_other/
    old_i18n = OLD_DIR / "i18n_other"
    old_i18n.mkdir(parents=True, exist_ok=True)
    moved_locales = []
    for loc_dir in sorted((ROOT / "i18n").iterdir()):
        if loc_dir.is_dir() and loc_dir.name not in ("ko",):
            dst_loc = old_i18n / loc_dir.name
            if dst_loc.exists():
                shutil.rmtree(dst_loc)
            shutil.move(str(loc_dir), str(dst_loc))
            moved_locales.append(loc_dir.name)

    print(f"Moved to _old: EN={moved_en}, KO={moved_ko}, unused locales={moved_locales}")
    print(f"Remaining active posts: EN={len(list(BLOG_DIR.glob('*/index.md*')))}, KO={len(list(KO_DIR.glob('*/index.md*')))}")


if __name__ == "__main__":
    main()
