import os

for root, dirs, files in os.walk(r"D:\ai\antigravity\global_blog"):
    for f in files:
        if f.endswith(".py"):
            fp = os.path.join(root, f)
            try:
                with open(fp, "r", encoding="utf-8") as file:
                    c = file.read()
                    if "threat_model" in c:
                        print(f"Found in script: {fp}")
            except:
                pass
