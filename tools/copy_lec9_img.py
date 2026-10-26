import shutil
import os

src = r"C:\Users\jbgih\.gemini\antigravity-cli\brain\a2c8435f-707b-431d-a280-dad177e26fdc\cs146s_lec9_formal_verification_z3_1793005073953.jpg"
dst_dir = r"D:\ai\antigravity\global_blog\배포대기\2026-10-30-stanford-cs146s-9\blog\images"
os.makedirs(dst_dir, exist_ok=True)
dst = os.path.join(dst_dir, "09_cs146s_autonomous_tdd_formal_verification.png")

shutil.copy2(src, dst)
print("Copied successfully to:", dst, "Size:", os.path.getsize(dst))
