import os

search_paths = [
    r"D:\Projects",
    r"D:\ai\claude",
    r"D:\ai\antigravity",
    r"D:\ai\grok",
    r"C:\Users\jbgih\Desktop",
    r"C:\Users\jbgih\Downloads",
    r"C:\Users\jbgih\Pictures",
]

keywords = ["바탕화면", "마음이", "wallpaper", "maeumi", "maeum_i"]

found_files = []

for sp in search_paths:
    if not os.path.exists(sp):
        continue
    for root, dirs, files in os.walk(sp):
        if any(skip in root for skip in ["node_modules", ".git", "venv", ".venv", "build", ".docusaurus"]):
            continue
        for f in files:
            fl = f.lower()
            if any(k in fl or k in root.lower() for k in keywords):
                if any(fl.endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".webp", ".svg", ".ico"]):
                    full = os.path.join(root, f)
                    try:
                        found_files.append((full, os.path.getsize(full)))
                    except:
                        pass

print(f"Total matching image files: {len(found_files)}")
for p, sz in found_files:
    print(f" - {p} ({sz} bytes)")
