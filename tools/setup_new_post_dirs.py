import os
import shutil

base_dir = r"D:\ai\antigravity\global_blog"
post_name = "2026-10-21-static-site-adsense-ads-txt-guide"
src_img = os.path.join(base_dir, "blog", "2026-10-20-custom-domain-adsense-seo-guide", "images", "02_indexing_pipeline.png")

target_dirs = [
    os.path.join(base_dir, "blog", post_name, "images"),
    os.path.join(base_dir, "i18n", "ko", "docusaurus-plugin-content-blog", post_name, "images"),
    os.path.join(base_dir, "i18n", "es", "docusaurus-plugin-content-blog", post_name, "images"),
    os.path.join(base_dir, "i18n", "ja", "docusaurus-plugin-content-blog", post_name, "images"),
    os.path.join(base_dir, "i18n", "zh-Hans", "docusaurus-plugin-content-blog", post_name, "images"),
    os.path.join(base_dir, "i18n", "zh-Hant", "docusaurus-plugin-content-blog", post_name, "images")
]

for d in target_dirs:
    os.makedirs(d, exist_ok=True)
    dst_img = os.path.join(d, "01_ads_txt_crawler_flow.png")
    shutil.copy(src_img, dst_img)

print("Images copied to all 6 locale directories successfully.")
