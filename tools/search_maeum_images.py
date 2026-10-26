import os

search_roots = [
    r"D:\ai\antigravity",
    r"D:\ai",
    r"D:\Projects"
]

keywords = ["maeum", "마음", "wallpaper", "cover", "바탕화면", "character", "캐릭터"]

found = []

for sroot in search_roots:
    if not os.path.exists(sroot):
        continue
    for root, dirs, files in os.walk(sroot):
        # Skip node_modules, .git, venv
        if "node_modules" in root or ".git" in root or "venv" in root or ".venv" in root or "build" in root:
            continue
        for f in files:
            fl = f.lower()
            if any(fl.endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".webp", ".svg"]):
                for kw in keywords:
                    if kw in fl or kw in root.lower():
                        full_path = os.path.join(root, f)
                        try:
                            sz = os.path.getsize(full_path)
                            found.append((full_path, sz))
                        except:
                            pass
                        break

print(f"Total matching images found: {len(found)}")
for p, sz in found[:50]:
    print(f" - {p} ({sz} bytes)")
