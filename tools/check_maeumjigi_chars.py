import os
import glob
import re

def strip_frontmatter(content):
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            return parts[2]
    return content

def get_chars(path):
    if not os.path.exists(path):
        return 0
    with open(path, 'r', encoding='utf-8') as fp:
        body = strip_frontmatter(fp.read())
    return len(body.strip())

episodes = []
for ep in range(1, 24):
    # find dir
    gb_en_matches = glob.glob(f"D:/ai/antigravity/global_blog/blog/*maeumjigi-{ep}/index.md")
    if not gb_en_matches:
        continue
    gb_en = gb_en_matches[0]
    folder_name = os.path.basename(os.path.dirname(gb_en))
    
    gb_ko = f"D:/ai/antigravity/global_blog/i18n/ko/docusaurus-plugin-content-blog/{folder_name}/index.md"
    
    # naver blog
    # date is in folder_name (e.g. 2026-06-18-maeumjigi-23 -> date 2026-06-18)
    date_part = "-".join(folder_name.split("-")[:3])
    nb = f"D:/ai/antigravity/naver_blog/posts/{date_part}/maeumjigi/post.md"
    
    en_chars = get_chars(gb_en)
    ko_chars = get_chars(gb_ko)
    nb_chars = get_chars(nb)
    
    episodes.append({
        'ep': ep,
        'folder': folder_name,
        'en': en_chars,
        'ko': ko_chars,
        'nb': nb_chars,
        'under_2000_en': en_chars < 2000,
        'under_2000_ko': ko_chars < 2000,
    })

print(f"{'Ep':<4} | {'Folder':<26} | {'EN':<6} | {'KO':<6} | {'NB':<6} | {'EN < 2000':<10} | {'KO < 2000'}")
print("-" * 75)
for e in episodes:
    print(f"{e['ep']:<4} | {e['folder']:<26} | {e['en']:<6} | {e['ko']:<6} | {e['nb']:<6} | {str(e['under_2000_en']):<10} | {str(e['under_2000_ko'])}")

print("\nSummary:")
print("EN < 2000:", [e['ep'] for e in episodes if e['under_2000_en']])
print("KO < 2000:", [e['ep'] for e in episodes if e['under_2000_ko']])
