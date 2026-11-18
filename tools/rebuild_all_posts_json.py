# -*- coding: utf-8 -*-
"""활성 게시글(blog/ 및 i18n/ko/)을 스캔하여 src/data/all_posts.json을 최신 상태(영문·한국어 제목 포함)로 갱신한다."""
import json
import pathlib
import re

ROOT = pathlib.Path(r"D:\ai\antigravity\global_blog")
BLOG_DIR = ROOT / "blog"
KO_DIR = ROOT / "i18n" / "ko" / "docusaurus-plugin-content-blog"
OUT_JSON = ROOT / "src" / "data" / "all_posts.json"


def extract_meta(md_path: pathlib.Path):
    txt = md_path.read_text(encoding="utf-8", errors="ignore")
    m = re.match(r"^---\s*\n(.*?)\n---", txt, re.S)
    fm = m.group(1) if m else ""
    title_m = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', fm, re.M)
    slug_m = re.search(r'^slug:\s*(\S+)', fm, re.M)
    date_m = re.search(r'^date:\s*(\S+)', fm, re.M)
    c1_m = re.search(r'^category_l1:\s*(\S+)', fm, re.M)
    c2_m = re.search(r'^category_l2:\s*(\S+)', fm, re.M)
    c3_m = re.search(r'^category_l3:\s*(\S+)', fm, re.M)
    folder = md_path.parent.name
    slug = slug_m.group(1) if slug_m else folder
    date_str = (date_m.group(1) if date_m else folder[:10])[:10]
    return {
        "title": title_m.group(1) if title_m else folder,
        "permalink": f"/blog/{slug}",
        "date": date_str,
        "cat_l1": c1_m.group(1) if c1_m else "practice",
        "cat_l2": c2_m.group(1) if c2_m else "ai",
        "cat_l3": c3_m.group(1) if c3_m else "project",
        "folder": folder,
    }


def main():
    items = []
    for p in sorted(BLOG_DIR.glob("*/index.md*")):
        meta = extract_meta(p)
        ko_p = KO_DIR / p.parent.name / "index.md"
        if ko_p.exists():
            ko_meta = extract_meta(ko_p)
            meta["title_ko"] = ko_meta["title"]
        else:
            meta["title_ko"] = meta["title"]
        items.append(meta)

    items.sort(key=lambda x: (x["date"], x["folder"]), reverse=True)
    OUT_JSON.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Updated {OUT_JSON.relative_to(ROOT)} with {len(items)} active posts.")
    for it in items:
        print(f"  {it['date']} | {it['permalink']} | EN: {it['title'][:45]} | KO: {it['title_ko'][:35]}")


if __name__ == "__main__":
    main()
