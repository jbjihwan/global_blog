import shutil, os

src_dir = r"D:\ai\antigravity\global_blog\배포대기\2026-10-30-stanford-cs146s-9\naver"
dst_dir = r"D:\ai\antigravity\naver_blog\posts\staged\2026-10-30-stanford-cs146s-9"
os.makedirs(dst_dir, exist_ok=True)

for f in ["post.md", "meta.json"]:
    src_f = os.path.join(src_dir, f)
    dst_f = os.path.join(dst_dir, f)
    shutil.copy2(src_f, dst_f)
    print("Copied", f, "to", dst_dir)

# Also copy image to naver images
img_src = r"D:\ai\antigravity\global_blog\배포대기\2026-10-30-stanford-cs146s-9\blog\images\09_cs146s_autonomous_tdd_formal_verification.png"
dst_img_dir = os.path.join(dst_dir, "images")
os.makedirs(dst_img_dir, exist_ok=True)
dst_img = os.path.join(dst_img_dir, "09_cs146s_autonomous_tdd_formal_verification.png")
shutil.copy2(img_src, dst_img)
print("Copied image to", dst_img)
