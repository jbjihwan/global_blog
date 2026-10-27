import os

base = r"D:\ai\antigravity\stanford_ai\github_materials\self-improving-agent-notebook\papers"
for l in ["lecture-12", "lecture-13", "lecture-14", "lecture-15", "lecture-16", "lecture-17"]:
    p = os.path.join(base, l)
    if os.path.exists(p):
        print(l, ":", os.listdir(p))
    else:
        print(l, "not found")
