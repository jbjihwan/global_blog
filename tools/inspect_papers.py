import os

papers_dir = r"D:\ai\antigravity\stanford_ai\github_materials\self-improving-agent-notebook\papers"
if os.path.exists(papers_dir):
    lectures = os.listdir(papers_dir)
    print("Lectures in papers:", lectures)
    for l in lectures[:5]:
        p = os.path.join(papers_dir, l)
        print(l, ":", os.listdir(p))
else:
    print("papers dir not found")
