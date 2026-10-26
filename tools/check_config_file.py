import os

base = r"D:\ai\antigravity\global_blog"
for f in ["docusaurus.config.ts", "docusaurus.config.js", "package.json"]:
    p = os.path.join(base, f)
    if os.path.exists(p):
        print(f"Found: {f}")
