#!/usr/bin/env python3
import subprocess

out = subprocess.check_output(["git", "show", "--stat", "d7b82e5"], cwd=r"D:\ai\antigravity\global_blog")
print(out.decode('utf-8')[:2000])
