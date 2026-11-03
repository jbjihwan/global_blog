import os
import shutil
import json

GB_ROOT = r"D:\ai\antigravity\global_blog"
STAGE_DIR = os.path.join(GB_ROOT, "배포대기", "2026-12-02-national-budget-surveillance-automated-audit-ledger")

dst_blog = os.path.join(GB_ROOT, "blog", "2026-12-02-national-budget-surveillance-automated-audit-ledger")
dst_ko = os.path.join(GB_ROOT, "i18n", "ko", "docusaurus-plugin-content-blog", "2026-12-02-national-budget-surveillance-automated-audit-ledger")
dst_naver = os.path.join(r"D:\ai\antigravity\naver_blog\posts", "2026-12-02-national-budget-surveillance-automated-audit-ledger")

os.makedirs(dst_blog, exist_ok=True)
os.makedirs(dst_ko, exist_ok=True)
os.makedirs(dst_naver, exist_ok=True)

# 1. Copy English blog
shutil.copy2(os.path.join(STAGE_DIR, "blog", "index.md"), os.path.join(dst_blog, "index.md"))
os.makedirs(os.path.join(dst_blog, "images"), exist_ok=True)
shutil.copy2(os.path.join(STAGE_DIR, "blog", "images", "01_cover.png"), os.path.join(dst_blog, "images", "01_cover.png"))
print("Copied English blog to", dst_blog)

# 2. Copy Korean blog
shutil.copy2(os.path.join(STAGE_DIR, "i18n", "ko", "index.md"), os.path.join(dst_ko, "index.md"))
os.makedirs(os.path.join(dst_ko, "images"), exist_ok=True)
shutil.copy2(os.path.join(STAGE_DIR, "blog", "images", "01_cover.png"), os.path.join(dst_ko, "images", "01_cover.png"))
print("Copied Korean blog to", dst_ko)

# 3. Copy Naver post
shutil.copy2(os.path.join(STAGE_DIR, "naver", "post.md"), os.path.join(dst_naver, "post.md"))
shutil.copy2(os.path.join(STAGE_DIR, "naver", "meta.json"), os.path.join(dst_naver, "meta.json"))
os.makedirs(os.path.join(dst_naver, "images"), exist_ok=True)
shutil.copy2(os.path.join(STAGE_DIR, "blog", "images", "01_cover.png"), os.path.join(dst_naver, "images", "01_cover.png"))
print("Copied Naver post to", dst_naver)

# 4. Update stage_info.json
stage_json_file = os.path.join(STAGE_DIR, "stage_info.json")
with open(stage_json_file, "r", encoding="utf-8") as f:
    meta = json.load(f)
meta["status"] = "deployed"
meta["deployed_at"] = "2026-11-03T14:25:00+09:00"
with open(stage_json_file, "w", encoding="utf-8") as f:
    json.dump(meta, f, ensure_ascii=False, indent=2)
print("Updated stage_info.json")
