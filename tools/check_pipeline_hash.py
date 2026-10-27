#!/usr/bin/env python3
import glob
import os
from PIL import Image

imgs = glob.glob(r"D:\ai\antigravity\global_blog\build\ko\assets\images\02_security_pipeline-*.png")
for img in imgs:
    with Image.open(img) as im:
        print(f"{os.path.basename(img)} -> {im.size}")
