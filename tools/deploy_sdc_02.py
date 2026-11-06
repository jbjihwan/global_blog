import os
import shutil
import json
import re

GB_ROOT = r"D:\ai\antigravity\global_blog"
STAGE_DIR = os.path.join(GB_ROOT, "배포대기", "2026-12-04-sdc-02-stack-spike-doctrine-hypotheses")

dst_blog = os.path.join(GB_ROOT, "blog", "2026-12-04-sdc-02-stack-spike-doctrine-hypotheses")
dst_ko = os.path.join(GB_ROOT, "i18n", "ko", "docusaurus-plugin-content-blog", "2026-12-04-sdc-02-stack-spike-doctrine-hypotheses")

os.makedirs(dst_blog, exist_ok=True)
os.makedirs(dst_ko, exist_ok=True)
os.makedirs(os.path.join(dst_blog, "images"), exist_ok=True)
os.makedirs(os.path.join(dst_ko, "images"), exist_ok=True)

# 1. Copy English blog and images
shutil.copy2(os.path.join(STAGE_DIR, "blog", "index.md"), os.path.join(dst_blog, "index.md"))
for img_f in os.listdir(os.path.join(STAGE_DIR, "blog", "images")):
    shutil.copy2(os.path.join(STAGE_DIR, "blog", "images", img_f), os.path.join(dst_blog, "images", img_f))
print("Copied English blog and images to", dst_blog)

# 2. Copy Korean blog and images
shutil.copy2(os.path.join(STAGE_DIR, "i18n", "ko", "index.md"), os.path.join(dst_ko, "index.md"))
for img_f in os.listdir(os.path.join(STAGE_DIR, "i18n", "ko", "images")):
    shutil.copy2(os.path.join(STAGE_DIR, "i18n", "ko", "images", img_f), os.path.join(dst_ko, "images", img_f))
print("Copied Korean blog and images to", dst_ko)

# 3. Update stage_info.json
stage_json_file = os.path.join(STAGE_DIR, "stage_info.json")
with open(stage_json_file, "r", encoding="utf-8") as f:
    meta = json.load(f)
meta["status"] = "deployed"
meta["deployed_at"] = "2026-11-06T13:20:00+09:00"
with open(stage_json_file, "w", encoding="utf-8") as f:
    json.dump(meta, f, ensure_ascii=False, indent=2)
print("Updated stage_info.json")

# 4. Link EP. 01 to EP. 02
ep01_en = os.path.join(GB_ROOT, "blog", "2026-12-03-sdc-01-architecture-klm-model", "index.md")
if os.path.exists(ep01_en):
    with open(ep01_en, "r", encoding="utf-8") as f:
        text = f.read()
    text = text.replace(
        "**[Air Combat Mission Replanning #2 (Next Episode)]**",
        "[Air Combat Mission Replanning #2: Stack Spike & Doctrine](/blog/sdc-02-stack-spike-doctrine-hypotheses)"
    )
    with open(ep01_en, "w", encoding="utf-8") as f:
        f.write(text)
    print("Linked EP. 01 EN to EP. 02")

ep01_ko = os.path.join(GB_ROOT, "i18n", "ko", "docusaurus-plugin-content-blog", "2026-12-03-sdc-01-architecture-klm-model", "index.md")
if os.path.exists(ep01_ko):
    with open(ep01_ko, "r", encoding="utf-8") as f:
        text = f.read()
    text = text.replace(
        "**[공중전 임무계획 변경 실증 #2 (다음 에피소드)]**",
        "[공중전 임무계획 변경 실증 #2: 스택 스파이크와 교리 가설](/blog/sdc-02-stack-spike-doctrine-hypotheses)"
    )
    with open(ep01_ko, "w", encoding="utf-8") as f:
        f.write(text)
    print("Linked EP. 01 KO to EP. 02")

print("[+] Deployment staging completed successfully!")
