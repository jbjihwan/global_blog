import os

target = "8강"
for root, dirs, files in os.walk(r"D:\ai\antigravity\global_blog"):
    for f in files:
        if f.endswith(".md") or f.endswith(".json"):
            path = os.path.join(root, f)
            try:
                with open(path, "r", encoding="utf-8") as file:
                    content = file.read()
                    if target in content or "Lecture #8" in content or "Lecture 8" in content:
                        print(f"Found in: {path}")
            except Exception:
                pass
