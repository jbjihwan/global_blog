import os

s_dir = r"D:\ai\antigravity\stanford_cs146s"
files = [f for f in os.listdir(s_dir) if f.endswith(".md")]
print("Files in stanford_cs146s:", sorted(files))
