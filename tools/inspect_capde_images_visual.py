import os
from PIL import Image

f_paths = [
    r"D:\ai\antigravity\global_blog\tools\pptx_extracted\fImage24500161641.png",
    r"D:\ai\antigravity\global_blog\tools\pptx_extracted\fImage12799565441.png",
    r"D:\ai\antigravity\global_blog\tools\pptx_extracted\fImage4964726188467.jpeg",
    r"D:\ai\antigravity\global_blog\tools\pptx_extracted\fImage1531666196334.jpeg",
    r"D:\Projects\26_1\CapDe\maeumjigi\maeum-app\assets\logo.png",
    r"D:\Projects\26_1\CapDe\maeumjigi\maeum-app\assets\icon.png",
]

for p in f_paths:
    if os.path.exists(p):
        with Image.open(p) as im:
            print(f"File: {os.path.basename(p)}")
            print(f"  Size: {im.size}, Mode: {im.mode}")
            # Get color bounding box
            if im.mode == "RGBA":
                bbox = im.getbbox()
                print(f"  Bbox: {bbox}")
