import subprocess

res = subprocess.run(["git", "status", "--short"], cwd=r"D:\ai\antigravity\global_blog", capture_output=True, text=True)
print("Git Status:")
print(res.stdout)
