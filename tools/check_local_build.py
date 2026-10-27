#!/usr/bin/env python3
import os
import glob
from PIL import Image

imgs = glob.glob(r"D:\ai\antigravity\global_blog\build\ko\assets\images\01_threat_model-*.png")
print("Found in build/ko/assets/images/:")
for img in imgs:
    with Image.open(img) as im:
        print(f"  {os.path.basename(img)} -> {im.size}")
