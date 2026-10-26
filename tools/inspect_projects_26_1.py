import os

p = r"D:\Projects\26_1"
print("Contents of D:\\Projects\\26_1:")
for root, dirs, files in os.walk(p):
    if any(s in root for s in [".git", "node_modules", "venv", ".venv", "__pycache__"]):
        continue
    for f in files:
        if any(f.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".webp", ".svg", ".ico"]):
            fp = os.path.join(root, f)
            print(f" Image: {fp} ({os.path.getsize(fp)} bytes)")
