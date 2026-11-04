import os
import shutil
import json
import re

GB_ROOT = r"D:\ai\antigravity\global_blog"
STAGE_DIR = os.path.join(GB_ROOT, "배포대기", "2026-12-03-sdc-01-architecture-klm-model")

dst_blog = os.path.join(GB_ROOT, "blog", "2026-12-03-sdc-01-architecture-klm-model")
dst_ko = os.path.join(GB_ROOT, "i18n", "ko", "docusaurus-plugin-content-blog", "2026-12-03-sdc-01-architecture-klm-model")

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
meta["deployed_at"] = "2026-11-04T16:05:00+09:00"
with open(stage_json_file, "w", encoding="utf-8") as f:
    json.dump(meta, f, ensure_ascii=False, indent=2)
print("Updated stage_info.json")

# 4. Update BlogListPage
page_file = os.path.join(GB_ROOT, "src", "theme", "BlogListPage", "index.tsx")
with open(page_file, "r", encoding="utf-8") as f:
    page_content = f.read()

# Add to KNOWN_SLUG_DATES
if "'sdc-01-architecture-klm-model'" not in page_content:
    page_content = page_content.replace(
        "const KNOWN_SLUG_DATES: Record<string, string> = {",
        "const KNOWN_SLUG_DATES: Record<string, string> = {\n  'sdc-01-architecture-klm-model': '2026-12-03',"
    )

# Add to getEpisodeNumber
if "sdc" not in page_content:
    page_content = page_content.replace(
        "if (permalink.includes('surveillance-automated-audit-ledger')) return 9;",
        "if (permalink.includes('surveillance-automated-audit-ledger')) return 9;\n  const sdcM = permalink.match(/sdc-(\\d+)/);\n  if (sdcM) return parseInt(sdcM[1], 10);"
    )

with open(page_file, "w", encoding="utf-8") as f:
    f.write(page_content)
print("Updated BlogListPage/index.tsx")
