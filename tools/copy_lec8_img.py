import shutil
import os

src = r"C:\Users\jbgih\.gemini\antigravity-cli\brain\a2c8435f-707b-431d-a280-dad177e26fdc\ai_native_refactoring_pipeline_png_1792926019727.jpg"
dst_dir = r"D:\ai\antigravity\global_blog\배포대기\2026-10-29-stanford-cs146s-8\blog\images"
os.makedirs(dst_dir, exist_ok=True)
dst = os.path.join(dst_dir, "08_cs146s_ai_native_architecture_refactoring.png")

shutil.copy2(src, dst)
print("Copied successfully to:", dst, "Size:", os.path.getsize(dst))
