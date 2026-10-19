import os
import re
import subprocess
import shutil
import glob

BASE_DIR = r"D:\ai\antigravity\global_blog"
LOCALE_DIRS = {
    "en": "blog",
    "ko": "i18n/ko/docusaurus-plugin-content-blog",
    "ja": "i18n/ja/docusaurus-plugin-content-blog",
    "es": "i18n/es/docusaurus-plugin-content-blog",
}

# 1. Update Episode #4 images with real Data Preprocessing graphs
W5_DIR = os.path.join(BASE_DIR, r"extracted_ppt_images\week5_docx")
img1_src = os.path.join(W5_DIR, "image1.png") # v1 소스별 변환 건수 (1차 시도)
img2_src = os.path.join(W5_DIR, "image2.png") # v1 vs v2 소스별 변환 건수 비교

for loc, dir_rel in LOCALE_DIRS.items():
    ep4_img_dir = os.path.join(BASE_DIR, dir_rel, "2026-04-01-maeumjigi-4", "images")
    if os.path.exists(ep4_img_dir):
        shutil.copy2(img1_src, os.path.join(ep4_img_dir, "01_cover.png"))
        shutil.copy2(img2_src, os.path.join(ep4_img_dir, "02_term.png"))
        print(f"Updated #4 images for {loc} -> {ep4_img_dir}")

# 2. Sync all images from KO to EN, JA, ES to ensure 100% real research images across all languages
ko_img_dir = os.path.join(BASE_DIR, LOCALE_DIRS["ko"])
for ko_file in glob.glob(os.path.join(ko_img_dir, "**", "images", "*.*"), recursive=True):
    rel_from_ko = os.path.relpath(ko_file, ko_img_dir)
    # Don't overwrite #4 since we just set the real ones
    if "2026-04-01-maeumjigi-4" in rel_from_ko:
        continue
    for other_loc in ["en", "ja", "es"]:
        target_file = os.path.join(BASE_DIR, LOCALE_DIRS[other_loc], rel_from_ko)
        if os.path.exists(os.path.dirname(target_file)):
            shutil.copy2(ko_file, target_file)

print("Synchronized all images across locales.")

# 3. Restore all 23 Maeumjigi post bodies from git commit c8c51044ed77753d4f92df6af993ed182643499a~1
restored_count = 0
for loc, dir_rel in LOCALE_DIRS.items():
    pattern = os.path.join(BASE_DIR, dir_rel, "*-maeumjigi-*", "index.md")
    for fpath in glob.glob(pattern):
        rel_path = os.path.relpath(fpath, BASE_DIR).replace('\\', '/')
        
        # Read current frontmatter (which contains description & keywords)
        with open(fpath, 'r', encoding='utf-8') as cur_f:
            cur_content = cur_f.read()
        
        cur_fm_match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", cur_content, re.DOTALL)
        if not cur_fm_match:
            continue
        cur_fm = cur_fm_match.group(1)
        
        # Fetch original file content from git
        res = subprocess.run(
            ['git', 'show', f'c8c51044ed77753d4f92df6af993ed182643499a~1:{rel_path}'],
            capture_output=True, text=True, encoding='utf-8'
        )
        if res.returncode != 0:
            print(f"Failed to fetch git history for {rel_path}")
            continue
        
        orig_content = res.stdout
        orig_fm_match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n(.*)$", orig_content, re.DOTALL)
        if not orig_fm_match:
            continue
        orig_body = orig_fm_match.group(2).strip()
        
        # Insert {/* truncate */} safely before the first H3 or after the first paragraph following cover image
        if "{/* truncate */}" not in orig_body:
            # Look for the first '### '
            h3_pos = orig_body.find("\n### ")
            if h3_pos != -1:
                intro = orig_body[:h3_pos].strip()
                rest = orig_body[h3_pos:].strip()
                new_body = f"{intro}\n\n{{/* truncate */}}\n\n{rest}"
            else:
                # Split by double newline
                parts = orig_body.split("\n\n")
                if len(parts) >= 2:
                    new_body = f"{parts[0]}\n\n{parts[1]}\n\n{{/* truncate */}}\n\n" + "\n\n".join(parts[2:])
                else:
                    new_body = f"{orig_body}\n\n{{/* truncate */}}"
        else:
            new_body = orig_body
        
        full_restored = f"---\n{cur_fm}\n---\n\n{new_body}\n"
        with open(fpath, 'w', encoding='utf-8', newline='\n') as out_f:
            out_f.write(full_restored)
        restored_count += 1

print(f"Successfully restored full technical content for {restored_count} Maeumjigi dev logs!")
