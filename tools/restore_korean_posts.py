import os
import re

NAVER_POSTS_ROOT = r"D:\ai\antigravity\naver_blog\posts"
KO_BLOG_ROOT = r"D:\ai\antigravity\global_blog\i18n\ko\docusaurus-plugin-content-blog"
EN_BLOG_ROOT = r"D:\ai\antigravity\global_blog\blog"

EPISODES = [
    ("2026-03-26", "2026-03-26-maeumjigi-1", 1),
    ("2026-03-30", "2026-03-30-maeumjigi-2", 2),
    ("2026-03-31", "2026-03-31-maeumjigi-3", 3),
    ("2026-04-01", "2026-04-01-maeumjigi-4", 4),
    ("2026-04-03", "2026-04-03-maeumjigi-5", 5),
    ("2026-04-05", "2026-04-05-maeumjigi-6", 6),
    ("2026-04-07", "2026-04-07-maeumjigi-7", 7),
    ("2026-04-08", "2026-04-08-maeumjigi-8", 8),
    ("2026-04-09", "2026-04-09-maeumjigi-9", 9),
    ("2026-04-14", "2026-04-14-maeumjigi-10", 10),
    ("2026-04-19", "2026-04-19-maeumjigi-11", 11),
    ("2026-05-03", "2026-05-03-maeumjigi-12", 12),
    ("2026-05-04", "2026-05-04-maeumjigi-13", 13),
    ("2026-05-06", "2026-05-06-maeumjigi-14", 14),
    ("2026-05-07", "2026-05-07-maeumjigi-15", 15),
    ("2026-05-08", "2026-05-08-maeumjigi-16", 16),
    ("2026-05-12", "2026-05-12-maeumjigi-17", 17),
    ("2026-05-13", "2026-05-13-maeumjigi-18", 18),
    ("2026-05-17", "2026-05-17-maeumjigi-19", 19),
    ("2026-05-20", "2026-05-20-maeumjigi-20", 20),
    ("2026-05-22", "2026-05-22-maeumjigi-21", 21),
    ("2026-05-30", "2026-05-30-maeumjigi-22", 22),
    ("2026-06-18", "2026-06-18-maeumjigi-23", 23),
]

def restore_korean_posts():
    print("=== Restoring 23 Maeumjigi Posts to Authentic Korean ===")
    restored_count = 0
    for date_str, folder_slug, ep_num in EPISODES:
        naver_post_path = os.path.join(NAVER_POSTS_ROOT, date_str, "maeumjigi", "post.md")
        target_post_path = os.path.join(KO_BLOG_ROOT, folder_slug, "index.md")
        en_post_path = os.path.join(EN_BLOG_ROOT, folder_slug, "index.md")

        if not os.path.exists(naver_post_path):
            print(f"[ERROR] Source not found: {naver_post_path}")
            continue

        with open(naver_post_path, "r", encoding="utf-8") as f:
            naver_raw = f.read()

        # Parse frontmatter and body from naver post
        fm_match = re.search(r"^---\s*\n(.*?)\n---\s*\n(.*)$", naver_raw, re.DOTALL)
        if not fm_match:
            print(f"[ERROR] Could not parse frontmatter in {naver_post_path}")
            continue

        fm_text = fm_match.group(1)
        body = fm_match.group(2).strip()

        # Extract title
        title_match = re.search(r"^title:\s*['\"]?(.*?)['\"]?$", fm_text, re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()
        else:
            m_titles = re.search(r"titles:\s*\n((?:\s*-\s*[^\n]+\n?)+)", fm_text)
            if m_titles:
                items = re.findall(r"-\s*([^\n\r]+)", m_titles.group(1))
                title = items[0].strip()
            else:
                title = f"[마음지기 캡스톤 개발일지 #{ep_num}]"

        # Clean title
        title = title.replace('"', '').replace("'", "")

        # Extract slug from EN version
        slug = folder_slug
        if os.path.exists(en_post_path):
            with open(en_post_path, "r", encoding="utf-8") as ef:
                en_raw = ef.read()
                s_match = re.search(r"slug:\s*([^\n\r]+)", en_raw)
                if s_match:
                    slug = s_match.group(1).strip()

        # Tags
        tags_match = re.search(r"tags:\s*(.*)", fm_text)
        if tags_match:
            tags_raw = tags_match.group(1).strip()
            if tags_raw.startswith("[") and tags_raw.endswith("]"):
                tags_str = tags_raw
            else:
                tag_list = [t.strip() for t in tags_raw.split(",") if t.strip()]
                tags_str = "[" + ", ".join(tag_list) + "]"
        else:
            tags_str = "[개발일지, AI챗봇, 캡스톤디자인, 파인튜닝, Llama3.1]"

        # Ensure image paths in body use ./images/
        body = re.sub(r'!\[(.*?)\]\(images/', r'![\1](./images/', body)

        # Assemble new Docusaurus frontmatter
        seo_keywords = "[마음지기 AI 챗봇, LLM 파인튜닝, AI 안전 가드레일, 캡스톤 디자인, 프롬프트 엔지니어링]"
        new_content = f"""---
slug: {slug}
title: "{title}"
authors: [jbgih]
tags: {tags_str}
date: {date_str}
keywords: {seo_keywords}
---

{body}
"""

        os.makedirs(os.path.dirname(target_post_path), exist_ok=True)
        with open(target_post_path, "w", encoding="utf-8") as tf:
            tf.write(new_content)

        restored_count += 1
        print(f"[RESTORED] #{ep_num} ({date_str}): {title}")

    print(f"\nSuccessfully restored {restored_count} / {len(EPISODES)} posts to Korean!")

if __name__ == "__main__":
    restore_korean_posts()
