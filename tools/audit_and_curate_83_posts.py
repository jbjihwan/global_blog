# -*- coding: utf-8 -*-
"""Step 1: 83개 블로그 게시글 전수 감사 및 선별 분류표 생성 스크립트."""
import pathlib
import re

ROOT = pathlib.Path(r"D:\ai\antigravity\global_blog")
BLOG_DIR = ROOT / "blog"
KO_DIR = ROOT / "i18n" / "ko" / "docusaurus-plugin-content-blog"


def parse_post(md_path: pathlib.Path):
    txt = md_path.read_text(encoding="utf-8", errors="ignore")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", txt, re.S)
    fm, body = (m.group(1), m.group(2)) if m else ("", txt)
    title_m = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', fm, re.M)
    date_m = re.search(r'^date:\s*(\S+)', fm, re.M)
    slug_m = re.search(r'^slug:\s*(\S+)', fm, re.M)
    title = title_m.group(1) if title_m else md_path.parent.name
    date = date_m.group(1) if date_m else md_path.parent.name[:10]
    slug = slug_m.group(1) if slug_m else md_path.parent.name
    prose = re.sub(r"```.*?```", "", body, flags=re.S)
    prose_words = len(prose.split())
    prose_chars = len(re.sub(r"\s+", "", prose))
    code_blocks = len(re.findall(r"```", body)) // 2
    has_sim = "simulation notice" in txt.lower() or "[simulation]" in txt.lower()
    has_ai_mention = any(k in txt.lower() for k in ["claude code", "artificial intelligence (ai) we", "ai와 ", "시킬"])
    has_local_path = "d:\\ai\\" in txt.lower()
    return {
        "folder": md_path.parent.name,
        "slug": slug,
        "date": date[:10],
        "title": title,
        "prose_words": prose_words,
        "prose_chars": prose_chars,
        "code_blocks": code_blocks,
        "has_sim": has_sim,
        "has_ai_mention": has_ai_mention,
        "has_local_path": has_local_path,
    }


def classify(en_info, ko_info):
    f = en_info["folder"].lower()
    slug = en_info["slug"].lower()
    title = en_info["title"]

    # 1. Stanford lecture notes (27 posts) -> Secondary course summaries
    if "stanford-cs329a" in f or "stanford-cs146s" in f:
        return "ARCHIVE_LECTURE", "대학 공개 강의 요약(2차 콘텐츠) — 고유 1차 트러블슈팅 집중을 위해 _old 이동"

    # 2. YMYL Suicide / Mental Crisis NLP (4 posts) -> Sensitive YMYL topic
    if "mental-crisis" in f or "crisis-nlp" in slug:
        return "ARCHIVE_YMYL", "자살·정신건강 위기 YMYL 민감 주제 — 애드센스 정책 리스크 차단을 위해 _old 이동"

    # 3. Synthetic simulation budget posts (9 posts) -> Reconstructed logs notice
    if "budget" in f or en_info["has_sim"]:
        return "ARCHIVE_SIMULATION", "가상 데이터 시뮬레이션·재구성 로그 경고문 포함 — 신뢰도 감점 방지를 위해 _old 이동"

    # 4. AdSense meta posts -> Reviewers dislike "how to pass AdSense" posts
    if "adsense" in f or "adsense" in slug:
        return "ARCHIVE_ADSENSE_META", "애드센스 승인/ads.txt 메타 주제 — 심사 시 저품질 신호로 작용할 수 있어 _old 이동"

    # 5. Maeumjigi Capstone Devlogs (24 posts) -> Keep only deep technical troubleshooting posts, archive short/diary ones
    if "maeumjigi" in f:
        # Check which Maeumjigi posts are genuine error troubleshooting with decent depth
        keep_maeum = {
            "2026-04-01-maeumjigi-4",   # Llama 3.1 Chat Template & JSONL preprocessing
            "2026-04-09-maeumjigi-9",   # Llama 3.1 Fine-Tuning Error Struggle (CUDA/LoRA)
            "2026-04-14-maeumjigi-10",  # API Rate Limits 429 & Resilient Pipeline
            "2026-05-03-maeumjigi-12",  # 70B GPU Memory OOM Struggle
            "2026-05-08-maeumjigi-16",  # React Native / Fine-tuning fatal bug fix
            "2026-05-17-maeumjigi-19",  # FastAPI PostgreSQL 401 JWT/Bcrypt Debugging
            "2026-06-18-maeumjigi-23",  # Dual-Layer Safety Wrapper & AWS EC2 GPU
        }
        if en_info["folder"] in keep_maeum:
            return "KEEP_UPGRADE", "실제 에러 해결(OOM·401·429·Chat Template) 포함 — 일기투·AI 언급 제거 및 한국어 분량 보강 후 유지"
        return "ARCHIVE_DIARY", "단문 캡스톤 일기/중간보고·내담자 정서 주제 — 얇은 일기성 콘텐츠 해소를 위해 _old 이동"

    # 6. Genuine technical troubleshooting & engineering posts (Security, RL, ANPR, SDC)
    return "KEEP_CORE", "핵심 엔지니어링 오류 해결·구현기 — 미래 날짜를 실제 작성일(과거)로 교정 및 템플릿 다변화 후 유지"


def main():
    en_posts = {p.parent.name: parse_post(p) for p in sorted(BLOG_DIR.glob("*/index.md*"))}
    ko_posts = {p.parent.name: parse_post(p) for p in sorted(KO_DIR.glob("*/index.md*"))}

    rows = []
    counts = {}
    for folder, en in sorted(en_posts.items()):
        ko = ko_posts.get(folder, {"prose_chars": 0, "prose_words": 0})
        decision, reason = classify(en, ko)
        counts[decision] = counts.get(decision, 0) + 1
        rows.append((decision, folder, en["date"], en["slug"], en["prose_words"], ko["prose_chars"], en["title"], reason))

    print("=== Summary Counts ===")
    for k, v in sorted(counts.items()):
        print(f"  {k}: {v}")

    print("\n=== KEEP Posts ===")
    for r in rows:
        if r[0].startswith("KEEP"):
            print(f"  [{r[0]}] {r[1]} | date={r[2]} | EN={r[4]}w | KO={r[5]}c | {r[6]}")

    print("\n=== ARCHIVE Posts (Sample/Summary) ===")
    for r in rows:
        if r[0].startswith("ARCHIVE"):
            print(f"  [{r[0]}] {r[1]} | date={r[2]} | EN={r[4]}w | KO={r[5]}c | {r[6][:55]}")


if __name__ == "__main__":
    main()
