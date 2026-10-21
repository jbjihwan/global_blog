import os
import glob

folders = [
    "2026-06-18-maeumjigi-23",
    "2026-05-30-maeumjigi-22",
    "2026-05-17-maeumjigi-19",
    "2026-04-14-maeumjigi-10",
    "2026-04-05-maeumjigi-6",
    "2026-04-01-maeumjigi-4",
    "2026-03-26-maeumjigi-1"
]

locales = ["ko", "es", "ja", "zh-Hans", "zh-Hant"]

for f in folders:
    gb_en = f"D:/ai/antigravity/global_blog/blog/{f}/index.md"
    print(f"=== {f} ===")
    print("EN exists:", os.path.exists(gb_en))
    for loc in locales:
        loc_path = f"D:/ai/antigravity/global_blog/i18n/{loc}/docusaurus-plugin-content-blog/{f}/index.md"
        print(f"  {loc} exists: {os.path.exists(loc_path)}")
