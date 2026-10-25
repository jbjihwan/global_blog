#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import shutil

src = r"C:\Users\jbgih\.gemini\antigravity-cli\brain\a2c8435f-707b-431d-a280-dad177e26fdc\cs146s_lecture5_multi_agent_swarm_orchestration_1792806503329.jpg"
dst_dir = r"D:\ai\antigravity\global_blog\배포대기\2026-10-26-stanford-cs146s-5\blog\images"
dst = os.path.join(dst_dir, "05_cs146s_multi_agent_swarm.png")

os.makedirs(dst_dir, exist_ok=True)
shutil.copy2(src, dst)
print(f"[SUCCESS] Staged image to {dst}")
