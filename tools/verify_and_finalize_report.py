import os
import re
from pathlib import Path

ROOT = Path(r"D:\ai\antigravity\global_blog")
BLOG_EN = ROOT / "blog"
BLOG_KO = ROOT / "i18n" / "ko" / "docusaurus-plugin-content-blog"
OLD_EN = ROOT / "_old" / "blog"
BUILD = ROOT / "build"

def get_stats(md_path: Path):
    text = md_path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    fm = parts[1] if len(parts) >= 3 else ""
    body = parts[2] if len(parts) >= 3 else text
    m_title = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', fm, re.M)
    m_date = re.search(r'^date:\s*["\']?(.*?)["\']?\s*$', fm, re.M)
    title = m_title.group(1) if m_title else md_path.parent.name
    date_str = m_date.group(1) if m_date else ""
    words = len(body.split())
    chars = len(body.strip())
    return date_str, words, chars, title

def update_curation_plan():
    active_dirs = sorted([d for d in BLOG_EN.iterdir() if d.is_dir()])
    old_dirs = sorted([d for d in OLD_EN.iterdir() if d.is_dir()])
    
    lines = [
        "# 글로벌 블로그 83편 전수 선별 및 정예화 결과표 (Step 1~3 완료)",
        "",
        "> 작성일: 2026-11-18 · 기준: Google AdSense 「가치가 별로 없는 콘텐츠」 및 Search Console `Crawled - currently not indexed` 해소",
        "",
        "## 1. 최종 선별 및 고도화 요약",
        "",
        f"- **기존 전체 게시글**: 83편 (영문 `blog/` 83편, 한국어 `i18n/ko/` 83편)",
        f"- **최종 라이브 게시(`ACTIVE`)**: **{len(active_dirs)}편** (기존 핵심 엔지니어링·오류 해결 19편 고도화 + Step 3 신규 오류 해결 글 1편 추가)",
        f"- **보관 이동(`_old/` 분리)**: **{len(old_dirs)}편**",
        "  - `ARCHIVE_LECTURE` (27편): 스탠포드 CS329A(17편)·CS146S(10편) 공개 강의 요약본 (2차 요약 콘텐츠 성격)",
        "  - `ARCHIVE_DIARY` (20편): 마음지기 캡스톤 단문 일기·중간보고·일반 진행 기록 (`#9`, `#12`, `#16` 추가 포함)",
        "  - `ARCHIVE_SIMULATION` (9편): `[Simulation]` 합성 데이터·재구성 로그 경고문이 포함된 공공예산 감사 시리즈",
        "  - `ARCHIVE_YMYL` (5편): 자살·정신건강 위기 감지 YMYL 고위험 민감 주제 시리즈 (`mental-crisis` 4편 + 자살 정규식 포함 `maeumjigi-23` 1편)",
        "  - `ARCHIVE_ADSENSE_META` (3편): 애드센스 승인·ads.txt 메타 가이드",
        "",
        "---",
        "",
        f"## 2. 라이브 게시 및 고도화 완료 목록 ({len(active_dirs)}편)",
        "",
        "| 구분 | 폴더명 | 게시일 | 영문 본문(단어) | 한국어 본문(자) | 영문 제목 | 조치 내용 |",
        "| :---: | :--- | :---: | :---: | :---: | :--- | :--- |",
    ]
    
    for d in active_dirs:
        en_md = d / "index.md"
        ko_md = BLOG_KO / d.name / "index.md"
        date_str, en_w, _, title = get_stats(en_md)
        _, _, ko_c, _ = get_stats(ko_md)
        if "2026-11-16-python-urlopen" in d.name:
            cat = "`NEW_STEP3`"
            note = "신규 작성: Windows Python `urlopen(timeout=8)` DNS 블로킹(`_socket.getaddrinfo`) 및 UTF-16 널 바이트 해결기"
        elif "vision-anpr" in d.name and not d.name.endswith("-1"):
            cat = "`KEEP_ENRICHED`"
            note = "실제 OpenCV/CUDA/EasyOCR 런타임 에러 트레이스백 및 해결 코드 대폭 보강 완료"
        elif "maeumjigi" in d.name:
            cat = "`KEEP_CLEANED`"
            note = "실제 에러 해결(Llama 3.1 Chat Template·API 429·FastAPI 401) 집중 유지 및 AI/임상 문구 정화 완료"
        elif "2026-11-05" in d.name or "2026-11-10" in d.name or "2026-11-12" in d.name or "2026-11-14" in d.name:
            cat = "`KEEP_DATE_FIXED`"
            note = "미래 날짜(11/28~12/05)를 실제 과거 날짜(11/05~11/14)로 교정 (기존 slug URL 유지)"
        else:
            cat = "`KEEP_CORE`"
            note = "핵심 엔지니어링 오류 해결·구현기 유지"
        lines.append(f"| {cat} | `{d.name}` | {date_str} | {en_w}w | {ko_c}자 | {title} | {note} |")

    lines.extend([
        "",
        "---",
        "",
        f"## 3. `_old/` 보관(비공개 분리) 목록 ({len(old_dirs)}편)",
        "",
        "| 분류 | 폴더명 | 기존 날짜 | 영문 본문(단어) | 제목 | 분리 사유 |",
        "| :---: | :--- | :---: | :---: | :--- | :--- |",
    ])
    for d in old_dirs:
        en_md = d / "index.md"
        date_str, en_w, _, title = get_stats(en_md)
        name = d.name
        if "stanford-cs329a" in name or "stanford-cs146s" in name:
            cat = "`ARCHIVE_LECTURE`"
            reason = "스탠포드 공개 강의 2차 요약본 — 독창적 1차 경험 집중을 위해 `_old/` 이동"
        elif "mental-crisis" in name or "maeumjigi-23" in name:
            cat = "`ARCHIVE_YMYL`"
            reason = "자살/위기 감지 YMYL 민감 키워드 및 정규식 포함 — 애드센스 정책 리스크 해소를 위해 `_old/` 이동"
        elif "public-finance-audit" in name or "budget-surveillance" in name:
            cat = "`ARCHIVE_SIMULATION`"
            reason = "`[Simulation]` 합성/재구성 데이터 면책조항 포함 — 실제 엔지니어링 기록만 남기기 위해 `_old/` 이동"
        elif "adsense" in name:
            cat = "`ARCHIVE_ADSENSE_META`"
            reason = "애드센스 승인/ads.txt 메타 가이드 — 사이트 주제 통일성을 위해 `_old/` 이동"
        else:
            cat = "`ARCHIVE_DIARY`"
            reason = "단문 캡스톤 일기/중간보고 성격 — 얇은 일기성 콘텐츠 해소를 위해 `_old/` 이동"
        lines.append(f"| {cat} | `{name}` | {date_str} | {en_w}w | {title} | {reason} |")

    out_path = ROOT / "CURATION_PLAN_83_POSTS.md"
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Updated {out_path} ({len(active_dirs)} active, {len(old_dirs)} archived)")

def verify_build():
    en_index = (BUILD / "index.html").read_text(encoding="utf-8")
    ko_index = (BUILD / "ko" / "index.html").read_text(encoding="utf-8")
    en_sitemap = (BUILD / "sitemap.xml").read_text(encoding="utf-8")
    ko_sitemap = (BUILD / "ko" / "sitemap.xml").read_text(encoding="utf-8")
    
    en_urls = re.findall(r"<loc>(.*?)</loc>", en_sitemap)
    ko_urls = re.findall(r"<loc>(.*?)</loc>", ko_sitemap)
    
    print("=== BUILD VERIFICATION ===")
    print("EN index.html adsbygoogle.js static occurrences:", en_index.count("adsbygoogle.js"))
    print("KO index.html adsbygoogle.js static occurrences:", ko_index.count("adsbygoogle.js"))
    print("KO index.html has Korean track heading:", "5대 핵심 엔지니어링 & 트러블슈팅 트랙" in ko_index)
    print("EN index.html has suicide/자살:", ("suicide" in en_index.lower()) or ("자살" in en_index))
    print("KO index.html has suicide/자살:", ("suicide" in ko_index.lower()) or ("자살" in ko_index))
    print("EN sitemap URL count:", len(en_urls))
    print("KO sitemap URL count:", len(ko_urls))
    print("New post in EN sitemap:", any("python-urlopen-timeout-dns-hang-windows-fix" in u for u in en_urls))
    print("New post in KO sitemap:", any("python-urlopen-timeout-dns-hang-windows-fix" in u for u in ko_urls))
    print("KO terms in KO sitemap:", any("/ko/terms" in u for u in ko_urls))
    print("Any mental-crisis or stanford in EN sitemap:", any(("mental-crisis" in u or "stanford" in u) for u in en_urls))

if __name__ == "__main__":
    update_curation_plan()
    verify_build()
