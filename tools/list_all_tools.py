import os

tools_dir = r"D:\ai\antigravity\global_blog\tools"
for f in sorted(os.listdir(tools_dir)):
    if f.endswith(".py"):
        print(f" - {f}")
