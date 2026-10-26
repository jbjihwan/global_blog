import os

search_roots = [
    r"D:\ai",
    r"D:\Projects",
    r"C:\Users\jbgih\Pictures",
    r"C:\Users\jbgih\Desktop",
    r"C:\Users\jbgih\Downloads",
    r"C:\Users\jbgih\Documents",
]

found = []
for sroot in search_roots:
    if not os.path.exists(sroot):
        continue
    for root, dirs, files in os.walk(sroot):
        if any(skip in root for skip in ["node_modules", ".git", "venv", ".venv", "AppData", "Cache"]):
            continue
        for f in files:
            if "마음" in f:
                fp = os.path.join(root, f)
                try:
                    found.append((fp, os.path.getsize(fp)))
                except:
                    pass

print(f"Total files with '마음' in filename: {len(found)}")
for fp, sz in found:
    print(f" - {fp} ({sz} bytes)")
