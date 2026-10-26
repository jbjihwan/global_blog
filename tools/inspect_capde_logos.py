import os
from PIL import Image

p = r"D:\Projects\26_1\CapDe\maeumjigi\maeum-app\assets\logo.png"
if os.path.exists(p):
    with Image.open(p) as im:
        print("Logo dimensions:", im.size, "Mode:", im.mode)
        # Check colors
        colors = im.getcolors(maxcolors=1000)
        print("Logo colors count:", len(colors) if colors else ">1000")

# Check all images in CapDe
for root, dirs, files in os.walk(r"D:\Projects\26_1\CapDe"):
    for f in files:
        if any(f.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg"]):
            fp = os.path.join(root, f)
            if "logo" in f.lower() or "icon" in f.lower() or "character" in f.lower() or "splash" in f.lower():
                print("Asset:", fp, os.path.getsize(fp))
