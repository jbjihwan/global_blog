import os
import re

base_dir = r"D:\ai\antigravity\global_blog"

for lang in ["zh-Hans", "zh-Hant"]:
    lang_dir = os.path.join(base_dir, "i18n", lang, "docusaurus-plugin-content-blog")
    for root, dirs, files in os.walk(lang_dir):
        for f in files:
            if f.endswith(".md"):
                file_path = os.path.join(root, f)
                with open(file_path, "r", encoding="utf-8") as fp:
                    lines = fp.readlines()
                
                in_code_block = False
                in_frontmatter = False
                frontmatter_count = 0
                
                for idx, line in enumerate(lines):
                    stripped = line.strip()
                    if stripped == "---":
                        frontmatter_count += 1
                        if frontmatter_count <= 2:
                            in_frontmatter = (frontmatter_count == 1)
                            continue
                    if in_frontmatter:
                        continue
                    
                    if stripped.startswith("```"):
                        in_code_block = not in_code_block
                        continue
                    
                    if in_code_block:
                        continue
                    
                    if "{/* truncate */}" in line:
                        continue
                    
                    # check for { or } in line
                    if "{" in line or "}" in line:
                        print(f"[{lang}] {os.path.basename(os.path.dirname(file_path))}:{idx+1}: {line.strip()}")
