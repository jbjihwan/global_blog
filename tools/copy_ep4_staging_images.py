# -*- coding: utf-8 -*-
import os
import shutil

src = r"C:\Users\jbgih\.gemini\antigravity-cli\brain\a2c8435f-707b-431d-a280-dad177e26fdc\cs329a_lecture4_architecture_v3_1793105841006.jpg"
dst = r"D:\ai\antigravity\global_blog\배포대기\2026-11-04-stanford-cs329a-4\blog\images\04_cs329a_tool_use_code_feedback.png"

os.makedirs(os.path.dirname(dst), exist_ok=True)
shutil.copyfile(src, dst)
print(f"Copied image for Ep4 to: {dst} ({os.path.getsize(dst)} bytes)")

locales = ["de", "es", "fr", "ja", "ko", "pt-BR", "zh-Hans", "zh-Hant"]
base_dir = r"D:\ai\antigravity\global_blog\배포대기\2026-11-04-stanford-cs329a-4"
for loc in locales:
    dst_img_dir = os.path.join(base_dir, "i18n", loc, "images")
    os.makedirs(dst_img_dir, exist_ok=True)
    dst_img = os.path.join(dst_img_dir, "04_cs329a_tool_use_code_feedback.png")
    shutil.copyfile(src, dst_img)
print("Copied Ep4 image to all staging locales!")
