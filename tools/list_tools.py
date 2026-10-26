#!/usr/bin/env python3
import os

TOOLS_DIR = r"D:\ai\antigravity\global_blog\tools"
for f in sorted(os.listdir(TOOLS_DIR)):
    if f.endswith(".py"):
        print(f)
