from PIL import Image

logo_path = r"D:\Projects\26_1\CapDe\maeumjigi\maeum-app\assets\logo.png"
with Image.open(logo_path) as im:
    print("Logo size:", im.size)
    # Check what colors are in the logo
    im_rgb = im.convert("RGB")
    colors = im_rgb.getcolors(maxcolors=10000)
    print("Distinct colors:", len(colors) if colors else ">10000")

f1 = r"D:\ai\antigravity\global_blog\tools\pptx_extracted\fImage12799565441.png"
with Image.open(f1) as im1:
    print("f1 size:", im1.size)
