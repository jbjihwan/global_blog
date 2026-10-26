import shutil
import os

src = r"C:\Users\jbgih\.gemini\antigravity-cli\brain\a2c8435f-707b-431d-a280-dad177e26fdc\cs146s_lecture10_grand_finale_architecture_1793009783729.jpg"
dst_dir = r"D:\ai\antigravity\global_blog\배포대기\2026-10-31-stanford-cs146s-10\blog\images"
os.makedirs(dst_dir, exist_ok=True)
dst = os.path.join(dst_dir, "10_cs146s_future_software_engineering_ai_fleets.png")

shutil.copy2(src, dst)
print("Copied Lecture 10 finale image to:", dst, "Size:", os.path.getsize(dst))
