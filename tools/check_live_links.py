import re

with open(r"D:\ai\antigravity\global_blog\build\blog\index.html", "r", encoding="utf-8") as f:
    text = f.read()

links = set(re.findall(r'href=["\'](/[^"\']+)["\']', text))
budget_links = [l for l in links if "budget" in l]

print(f"Total links: {len(links)}")
print("Budget links in build/blog/index.html:")
for bl in sorted(budget_links):
    print(" -", bl)
