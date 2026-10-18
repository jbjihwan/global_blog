import os

p_dir = r"D:\서울과기대 컴퓨터공학과\26-1\CapDe\팀플\Week12\_preview"
if os.path.exists(p_dir):
    print("=== Week12 _preview ===")
    for f in os.listdir(p_dir):
        fp = os.path.join(p_dir, f)
        print(f"  {f} ({os.path.getsize(fp) // 1024} KB)")

# Let's also check other CapDe Week folders
capde_root = r"D:\서울과기대 컴퓨터공학과\26-1\CapDe\팀플"
for w in sorted(os.listdir(capde_root)):
    wp = os.path.join(capde_root, w)
    if os.path.isdir(wp):
        imgs = [f for f in os.listdir(wp) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if imgs:
            print(f"=== {w} Direct Images ({len(imgs)}) ===")
            for img in imgs:
                print(f"  {img}")
