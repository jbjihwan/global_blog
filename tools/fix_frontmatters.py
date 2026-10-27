# -*- coding: utf-8 -*-
import os
import re

GB_ROOT = r"D:\ai\antigravity\global_blog"
STAGING_ROOT = os.path.join(GB_ROOT, "배포대기")
BLOG_ROOT = os.path.join(GB_ROOT, "blog")

from translate_maeumjigi_de import DE_METAS
from translate_maeumjigi_fr import FR_METAS
from translate_maeumjigi_pt import PT_METAS

def retranslate(locale, metas):
    prod_root = os.path.join(GB_ROOT, "i18n", locale, "docusaurus-plugin-content-blog")
    for slug, meta in metas.items():
        src_idx = os.path.join(BLOG_ROOT, slug, "index.md")
        if not os.path.exists(src_idx):
            continue
        with open(src_idx, "r", encoding="utf-8") as f:
            content = f.read()

        parts = content.split("---", 2)
        if len(parts) < 3:
            continue
        fm_lines = parts[1].strip().splitlines()
        body = parts[2]

        new_fm = []
        for l in fm_lines:
            if l.startswith("title:"):
                new_fm.append(f'title: "{meta["title"]}"')
            elif l.startswith("description:"):
                new_fm.append(f'description: "{meta["desc"]}"')
            elif l.startswith("keywords:"):
                kw_str = "[" + ", ".join([f'"{k}"' for k in meta["keywords"]]) + "]"
                new_fm.append(f"keywords: {kw_str}")
            else:
                new_fm.append(l)

        fixed_content = "---\n" + "\n".join(new_fm) + "\n---" + body

        # 1. Update staging
        stg_file = os.path.join(STAGING_ROOT, slug, "i18n", locale, "index.md")
        os.makedirs(os.path.dirname(stg_file), exist_ok=True)
        with open(stg_file, "w", encoding="utf-8") as f:
            f.write(fixed_content)

        # 2. Update production i18n
        prod_file = os.path.join(prod_root, slug, "index.md")
        os.makedirs(os.path.dirname(prod_file), exist_ok=True)
        with open(prod_file, "w", encoding="utf-8") as f:
            f.write(fixed_content)

    print(f"Fixed all frontmatters for [{locale}]")

if __name__ == "__main__":
    retranslate("de", DE_METAS)
    retranslate("fr", FR_METAS)
    retranslate("pt-BR", PT_METAS)
