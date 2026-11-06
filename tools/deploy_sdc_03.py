import os
import shutil
import json

GB_ROOT = r"D:\ai\antigravity\global_blog"
STAGE_DIR = os.path.join(GB_ROOT, "배포대기", "2026-12-05-sdc-03-deterministic-jcs-ed25519-fragmentation")

dst_blog = os.path.join(GB_ROOT, "blog", "2026-12-05-sdc-03-deterministic-jcs-ed25519-fragmentation")
dst_ko = os.path.join(GB_ROOT, "i18n", "ko", "docusaurus-plugin-content-blog", "2026-12-05-sdc-03-deterministic-jcs-ed25519-fragmentation")

os.makedirs(dst_blog, exist_ok=True)
os.makedirs(dst_ko, exist_ok=True)
os.makedirs(os.path.join(dst_blog, "images"), exist_ok=True)
os.makedirs(os.path.join(dst_ko, "images"), exist_ok=True)

# 1. Copy English blog and images
shutil.copy2(os.path.join(STAGE_DIR, "blog", "index.md"), os.path.join(dst_blog, "index.md"))
for img_f in os.listdir(os.path.join(STAGE_DIR, "blog", "images")):
    shutil.copy2(os.path.join(STAGE_DIR, "blog", "images", img_f), os.path.join(dst_blog, "images", img_f))
print("[+] Copied English blog and images to", dst_blog)

# 2. Copy Korean blog and images
shutil.copy2(os.path.join(STAGE_DIR, "i18n", "ko", "index.md"), os.path.join(dst_ko, "index.md"))
for img_f in os.listdir(os.path.join(STAGE_DIR, "i18n", "ko", "images")):
    shutil.copy2(os.path.join(STAGE_DIR, "i18n", "ko", "images", img_f), os.path.join(dst_ko, "images", img_f))
print("[+] Copied Korean blog and images to", dst_ko)

# 3. Update stage_info.json
stage_json_file = os.path.join(STAGE_DIR, "stage_info.json")
with open(stage_json_file, "r", encoding="utf-8") as f:
    meta = json.load(f)
meta["status"] = "deployed"
meta["deployed_at"] = "2026-11-06T13:45:00+09:00"
with open(stage_json_file, "w", encoding="utf-8") as f:
    json.dump(meta, f, ensure_ascii=False, indent=2)
print("[+] Updated stage_info.json")

# 4. Link EP. 02 to EP. 03
ep02_en = os.path.join(GB_ROOT, "blog", "2026-12-04-sdc-02-stack-spike-doctrine-hypotheses", "index.md")
if os.path.exists(ep02_en):
    with open(ep02_en, "r", encoding="utf-8") as f:
        text = f.read()
    text = text.replace(
        "**[Air Combat Mission Replanning #3: Deterministic JCS, Ed25519 & Fragmentation (Next Episode)]**",
        "[Air Combat Mission Replanning #3: Deterministic JCS & Ed25519 Frag Fix](/blog/sdc-03-deterministic-jcs-ed25519-fragmentation)"
    )
    with open(ep02_en, "w", encoding="utf-8") as f:
        f.write(text)
    print("[+] Linked EP. 02 EN to EP. 03")

ep02_ko = os.path.join(GB_ROOT, "i18n", "ko", "docusaurus-plugin-content-blog", "2026-12-04-sdc-02-stack-spike-doctrine-hypotheses", "index.md")
if os.path.exists(ep02_ko):
    with open(ep02_ko, "r", encoding="utf-8") as f:
        text = f.read()
    text = text.replace(
        "**[Air Combat Mission Replanning #3: Deterministic JCS, Ed25519 & Fragmentation (Next Episode)]**",
        "[공중전 임무계획 변경 실증 #3: 결정적 JCS와 Ed25519 서명 조각화 결함 격파](/blog/sdc-03-deterministic-jcs-ed25519-fragmentation)"
    )
    with open(ep02_ko, "w", encoding="utf-8") as f:
        f.write(text)
    print("[+] Linked EP. 02 KO to EP. 03")

print("[+] EP. 03 deployment staging completed successfully!")
