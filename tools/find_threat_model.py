import os

blog_dir = r"D:\ai\antigravity\global_blog\blog"

for root, dirs, files in os.walk(blog_dir):
    for f in files:
        if "threat_model" in f.lower():
            print(f"Found image: {os.path.join(root, f)}")
        if f.endswith(".md"):
            fp = os.path.join(root, f)
            with open(fp, "r", encoding="utf-8") as file:
                content = file.read()
                if "threat_model" in content:
                    print(f"Referenced in: {fp}")
