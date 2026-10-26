import os

search_roots = [
    r"D:\ai",
    r"D:\Projects",
    r"C:\Users\jbgih\Pictures",
    r"C:\Users\jbgih\Desktop",
    r"C:\Users\jbgih\Downloads",
    r"C:\Users\jbgih\Documents",
]

matches = []

for sroot in search_roots:
    if not os.path.exists(sroot):
        continue
    for root, dirs, files in os.walk(sroot):
        if any(skip in root for skip in ["node_modules", ".git", "venv", ".venv", "AppData", "Cache"]):
            continue
        for f in files:
            fl = f.lower()
            if any(k in fl for k in ["바탕", "마음이", "wallpaper", "maeumi", "캐릭터", "character", "mascot", "logo", "마음"]):
                matches.append(os.path.join(root, f))

print(f"Total matches: {len(matches)}")
for m in matches[:60]:
    print(" -", m)
