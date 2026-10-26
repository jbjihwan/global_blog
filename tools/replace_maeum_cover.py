import shutil
import os

new_img = r"C:\Users\jbgih\.gemini\antigravity-cli\brain\a2c8435f-707b-431d-a280-dad177e26fdc\maeumjigi_devlog_01_cover_1793009752128.jpg"

targets = [
    r"D:\ai\antigravity\global_blog\blog\2026-03-26-maeumjigi-1\images\01_cover.png",
    r"D:\ai\antigravity\global_blog\i18n\ko\docusaurus-plugin-content-blog\2026-03-26-maeumjigi-1\images\01_cover.png",
    r"D:\ai\antigravity\global_blog\i18n\ja\docusaurus-plugin-content-blog\2026-03-26-maeumjigi-1\images\01_cover.png",
    r"D:\ai\antigravity\global_blog\i18n\es\docusaurus-plugin-content-blog\2026-03-26-maeumjigi-1\images\01_cover.png",
    r"D:\ai\antigravity\global_blog\i18n\zh-Hans\docusaurus-plugin-content-blog\2026-03-26-maeumjigi-1\images\01_cover.png",
    r"D:\ai\antigravity\global_blog\i18n\zh-Hant\docusaurus-plugin-content-blog\2026-03-26-maeumjigi-1\images\01_cover.png",
]

for t in targets:
    os.makedirs(os.path.dirname(t), exist_ok=True)
    shutil.copy2(new_img, t)
    print("Replaced:", t, "Size:", os.path.getsize(t))
