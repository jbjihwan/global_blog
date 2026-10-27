#!/usr/bin/env python3
import subprocess

out = subprocess.check_output(["git", "log", "-n", "3", "--oneline"], cwd=r"D:\ai\antigravity\global_blog")
print(out.decode('utf-8'))
