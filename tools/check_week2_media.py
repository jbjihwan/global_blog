import os
from PIL import Image

EXTRACT_DIR = r"D:\ai\antigravity\global_blog\extracted_ppt_images\week2"
for f in ["image1.png", "image11.png"]:
    fp = os.path.join(EXTRACT_DIR, f)
    if os.path.exists(fp):
        im = Image.open(fp)
        print(f"{f}: size={im.size}, mode={im.mode}")
