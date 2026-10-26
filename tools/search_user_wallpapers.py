import os

candidates = []
for root, dirs, files in os.walk(r"C:\Users\jbgih"):
    if any(k in root for k in ["AppData", "node_modules", ".git", ".cache", "Cache", ".vscode", ".rustup"]):
        continue
    for f in files:
        fl = f.lower()
        if any(w in fl for w in ["바탕화면", "wallpaper", "마음이", "배경화면", "배경"]):
            full = os.path.join(root, f)
            try:
                candidates.append((full, os.path.getsize(full)))
            except:
                pass

print(f"Total matching files in C:\\Users\\jbgih: {len(candidates)}")
for c, sz in candidates:
    print(f" - {c} ({sz} bytes)")
