import os
import re
from pathlib import Path

DIRS = [
    Path(r"D:\ai\antigravity\global_blog\blog"),
    Path(r"D:\ai\antigravity\global_blog\i18n\ko\docusaurus-plugin-content-blog"),
    Path(r"D:\ai\antigravity\global_blog\배포대기\2026-12-03-sdc-01-architecture-klm-model\blog"),
    Path(r"D:\ai\antigravity\global_blog\배포대기\2026-12-03-sdc-01-architecture-klm-model\i18n\ko"),
    Path(r"D:\ai\antigravity\global_blog\배포대기\2026-12-04-sdc-02-stack-spike-doctrine-hypotheses\blog"),
    Path(r"D:\ai\antigravity\global_blog\배포대기\2026-12-04-sdc-02-stack-spike-doctrine-hypotheses\i18n\ko"),
]

def classify_slug(slug: str):
    s = slug.lower()
    
    # 1. Theory
    if "stanford-cs146s" in s:
        return "theory", "ai", "lecture", ["theory", "ai", "lecture", "stanford-cs146s"]
    if "stanford-cs329a" in s:
        return "theory", "ai", "lecture", ["theory", "ai", "lecture", "stanford-cs329a"]
        
    # 2. Practice -> Security
    if any(k in s for k in ["static-site-security", "npm-overrides", "cloudflare", "custom-domain", "adsense", "ads-txt"]):
        if "npm-overrides" in s:
            return "practice", "security", "project-npm-cve", ["practice", "security", "cve", "npm"]
        return "practice", "security", "project-security-infra", ["practice", "security", "infra"]
        
    # 2. Practice -> AI
    if "sdc-" in s:
        return "practice", "ai", "project-sdc", ["practice", "ai", "sdc", "avionics"]
    if any(k in s for k in ["national-budget", "autonomous-budget", "local-subsidy", "education-grant"]):
        return "practice", "ai", "project-budget", ["practice", "ai", "budget-audit"]
    if any(k in s for k in ["mental-crisis", "crisis-detection"]):
        return "practice", "ai", "project-crisis", ["practice", "ai", "crisis-nlp"]
    if "maeumjigi" in s:
        return "practice", "ai", "project-maeumjigi", ["practice", "ai", "maeumjigi"]
    if "vision-anpr" in s:
        return "practice", "ai", "project-anpr", ["practice", "ai", "anpr", "cv"]
    if "rl-qlearning" in s:
        return "practice", "ai", "project-rl", ["practice", "ai", "reinforcement-learning"]
        
    return "practice", "misc", "unknown", ["practice"]

def process_file(md_path: Path):
    if not md_path.exists() or md_path.suffix != ".md":
        return False
        
    content = md_path.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return False
        
    parts = content.split("---", 2)
    if len(parts) < 3:
        return False
        
    fm_raw = parts[1]
    body = parts[2]
    
    # Classify based on parent folder or slug
    folder_name = md_path.parent.name
    l1, l2, l3, new_tags = classify_slug(folder_name)
    
    # Clean existing category fields if present
    lines = fm_raw.splitlines()
    filtered_lines = []
    tags_line_idx = -1
    
    for i, line in enumerate(lines):
        if line.startswith("category_l1:") or line.startswith("category_l2:") or line.startswith("category_l3:"):
            continue
        if line.startswith("tags:"):
            tags_line_idx = len(filtered_lines)
        filtered_lines.append(line)
        
    # Insert category fields
    cat_block = [
        f"category_l1: {l1}",
        f"category_l2: {l2}",
        f"category_l3: {l3}"
    ]
    
    # Update tags if tags line exists
    if tags_line_idx != -1:
        tags_line = filtered_lines[tags_line_idx]
        m = re.search(r"tags:\s*\[(.*?)\]", tags_line)
        if m:
            curr_tags = [t.strip().strip("'\"") for t in m.group(1).split(",") if t.strip()]
            for t in new_tags:
                if t not in curr_tags:
                    curr_tags.append(t)
            filtered_lines[tags_line_idx] = f"tags: [{', '.join(curr_tags)}]"
            
    # Put category block right after slug or at top
    insert_pos = 0
    for idx, l in enumerate(filtered_lines):
        if l.startswith("slug:"):
            insert_pos = idx + 1
            break
            
    new_fm_lines = filtered_lines[:insert_pos] + cat_block + filtered_lines[insert_pos:]
    new_fm = "\n".join(new_fm_lines)
    
    new_content = f"---{new_fm}\n---{body}"
    md_path.write_text(new_content, encoding="utf-8")
    return True

total_processed = 0
for d in DIRS:
    if not d.exists():
        continue
    for p in d.rglob("*.md"):
        if p.name == "index.md":
            if process_file(p):
                total_processed += 1

print(f"[+] Successfully injected taxonomy metadata into {total_processed} files.")
