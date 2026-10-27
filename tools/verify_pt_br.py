# -*- coding: utf-8 -*-
import os

GB_ROOT = r"D:\ai\antigravity\global_blog"
STAGING_ROOT = os.path.join(GB_ROOT, "배포대기")
PROD_PT = os.path.join(GB_ROOT, "i18n", "pt-BR", "docusaurus-plugin-content-blog")
PROD_PAGES = os.path.join(GB_ROOT, "i18n", "pt-BR", "docusaurus-plugin-content-pages")

# 1. Staging count
staged_pt = 0
for d in os.listdir(STAGING_ROOT):
    p = os.path.join(STAGING_ROOT, d, "i18n", "pt-BR", "index.md")
    if os.path.isfile(p):
        staged_pt += 1

# 2. Production blog count
prod_pt = 0
for d in os.listdir(PROD_PT):
    p = os.path.join(PROD_PT, d, "index.md")
    if os.path.isfile(p):
        prod_pt += 1

# 3. Production pages count
pages = [f for f in os.listdir(PROD_PAGES) if f.endswith('.md')]

print(f"Staged pt-BR posts count:     {staged_pt} / 47")
print(f"Production pt-BR posts count: {prod_pt} / 47")
print(f"Production pt-BR pages count: {len(pages)} (pages: {pages})")
