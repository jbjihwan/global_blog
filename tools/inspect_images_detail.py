from PIL import Image

f1 = r"D:\ai\antigravity\global_blog\tools\pptx_extracted\fImage24500161641.png"
f2 = r"D:\ai\antigravity\global_blog\tools\pptx_extracted\fImage12799565441.png"
logo = r"D:\Projects\26_1\CapDe\maeumjigi\maeum-app\assets\logo.png"

for p in [f1, f2, logo]:
    with Image.open(p) as im:
        print(f"Path: {p}")
        print(f"  Size: {im.size}, Mode: {im.mode}")
        # Sample non-transparent pixels
        im_rgba = im.convert("RGBA")
        non_trans = [pixel for pixel in im_rgba.getdata() if pixel[3] > 0]
        print(f"  Non-transparent pixels: {len(non_trans)} / {im.size[0]*im.size[1]}")
        if non_trans:
            sample_colors = set(non_trans[:20])
            print(f"  Sample colors: {sample_colors}")
