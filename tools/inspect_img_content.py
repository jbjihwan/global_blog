from PIL import Image
import os

img_path = r"D:\ai\antigravity\global_blog\blog\2026-03-26-maeumjigi-1\images\01_cover.png"
with Image.open(img_path) as im:
    print("Format:", im.format, "Size:", im.size, "Mode:", im.mode)
    colors = im.getcolors(maxcolors=256)
    if colors:
        print("Unique colors count:", len(colors))
    else:
        print("More than 256 colors.")
    extrema = im.getextrema()
    print("Extrema:", extrema)

img2_path = r"D:\ai\antigravity\global_blog\blog\2026-03-26-maeumjigi-1\images\02_term.png"
with Image.open(img2_path) as im2:
    print("\nImg2 Format:", im2.format, "Size:", im2.size, "Mode:", im2.mode)
    print("Extrema:", im2.getextrema())
