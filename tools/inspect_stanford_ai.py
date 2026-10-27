import os

base_dir = r"D:\ai\antigravity\stanford_ai"
if os.path.exists(base_dir):
    for root, dirs, files in os.walk(base_dir):
        depth = root.replace(base_dir, "").count(os.sep)
        if depth <= 2:
            print(root)
            for f in files[:10]:
                print(f"  - {f}")
else:
    print("Not found")
