import os

s_dir = r"D:\ai\antigravity\stanford_ai"
files = [f for f in os.listdir(s_dir) if os.path.isfile(os.path.join(s_dir, f))]
print("Files in stanford_ai:", files)
