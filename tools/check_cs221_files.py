import os

s_dir = r"D:\ai\antigravity\stanford_cs221"
if os.path.exists(s_dir):
    files = [f for f in os.listdir(s_dir) if os.path.isfile(os.path.join(s_dir, f))]
    print("Files in stanford_cs221:", files)
else:
    print("stanford_cs221 not found")
