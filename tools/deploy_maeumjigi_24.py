import os
import shutil
import json

GB_ROOT = r"D:\ai\antigravity\global_blog"
STAGE_ROOT = os.path.join(GB_ROOT, "배포대기", "2026-09-16-maeumjigi-24")

# 1. Target paths
blog_dst = os.path.join(GB_ROOT, "blog", "2026-09-16-maeumjigi-24")
ko_dst = os.path.join(GB_ROOT, "i18n", "ko", "docusaurus-plugin-content-blog", "2026-09-16-maeumjigi-24")
naver_dst = os.path.join(r"D:\ai\antigravity\naver_blog\posts\staged", "2026-09-16-maeumjigi-24")

os.makedirs(blog_dst, exist_ok=True)
os.makedirs(ko_dst, exist_ok=True)
os.makedirs(naver_dst, exist_ok=True)

# 2. Copy English blog
src_blog = os.path.join(STAGE_ROOT, "blog")
shutil.copy2(os.path.join(src_blog, "index.md"), os.path.join(blog_dst, "index.md"))
os.makedirs(os.path.join(blog_dst, "images"), exist_ok=True)
shutil.copy2(os.path.join(src_blog, "images", "01_cover.png"), os.path.join(blog_dst, "images", "01_cover.png"))
print("Copied English blog to", blog_dst)

# 3. Copy Korean blog
src_ko = os.path.join(STAGE_ROOT, "i18n", "ko")
shutil.copy2(os.path.join(src_ko, "index.md"), os.path.join(ko_dst, "index.md"))
os.makedirs(os.path.join(ko_dst, "images"), exist_ok=True)
shutil.copy2(os.path.join(src_blog, "images", "01_cover.png"), os.path.join(ko_dst, "images", "01_cover.png"))
# Also ensure staging i18n/ko has the image
os.makedirs(os.path.join(src_ko, "images"), exist_ok=True)
shutil.copy2(os.path.join(src_blog, "images", "01_cover.png"), os.path.join(src_ko, "images", "01_cover.png"))
print("Copied Korean blog to", ko_dst)

# 4. Copy Naver blog
src_naver = os.path.join(STAGE_ROOT, "naver")
if os.path.exists(src_naver):
    shutil.copy2(os.path.join(src_naver, "post.md"), os.path.join(naver_dst, "post.md"))
    if os.path.exists(os.path.join(src_naver, "meta.json")):
        shutil.copy2(os.path.join(src_naver, "meta.json"), os.path.join(naver_dst, "meta.json"))
    os.makedirs(os.path.join(naver_dst, "images"), exist_ok=True)
    shutil.copy2(os.path.join(src_blog, "images", "01_cover.png"), os.path.join(naver_dst, "images", "01_cover.png"))
    print("Copied Naver post to", naver_dst)

# 5. Update stage_info.json
stage_json_file = os.path.join(STAGE_ROOT, "stage_info.json")
if os.path.exists(stage_json_file):
    with open(stage_json_file, "r", encoding="utf-8") as f:
        meta = json.load(f)
    meta["status"] = "deployed"
    meta["deployed_at"] = "2026-11-02T21:45:00+09:00"
    with open(stage_json_file, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print("Updated stage_info.json to deployed")

print("All file synchronization complete.")
