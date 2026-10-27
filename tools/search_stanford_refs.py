import os

search_dirs = [r"D:\ai\antigravity", r"D:\ai\claude"]
keywords = ["cs146s", "stanford", "cs229", "cs224", "cs25", "cs329"]

for sdir in search_dirs:
    if not os.path.exists(sdir):
        continue
    for root, dirs, files in os.walk(sdir):
        if "node_modules" in root or ".git" in root or "build" in root or ".docusaurus" in root or "review_images" in root:
            continue
        for f in files:
            if f.endswith((".md", ".txt", ".json")):
                path = os.path.join(root, f)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as fp:
                        content = fp.read()
                        for kw in keywords:
                            if kw in content.lower():
                                count = content.lower().count(kw)
                                if "global_blog\\blog" not in path and "배포대기" not in path:
                                    print(f"Found {kw} ({count}x) in: {path}")
                                break
                except Exception as e:
                    pass
