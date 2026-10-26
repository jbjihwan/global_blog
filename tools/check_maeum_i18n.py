import os

i18n_dir = r"D:\ai\antigravity\global_blog\i18n"
locales = ["ko", "ja", "es", "zh-Hans", "zh-Hant"]

for loc in locales:
    loc_post = os.path.join(i18n_dir, loc, "docusaurus-plugin-content-blog", "2026-03-26-maeumjigi-1")
    if os.path.exists(loc_post):
        print(f"[{loc}] exists. Files:", os.listdir(loc_post))
        img_dir = os.path.join(loc_post, "images")
        if os.path.exists(img_dir):
            print(f"  images: {os.listdir(img_dir)}")
        else:
            print("  images: NO IMAGES DIR")
    else:
        print(f"[{loc}] NOT FOUND")
