import os

path = r"D:\ai\antigravity\global_blog\tools\deploy_stanford_lectures_4_to_7.py"
if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        print(f.read())
else:
    print("deploy_stanford_lectures_4_to_7.py not found")
