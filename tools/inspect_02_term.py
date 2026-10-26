from PIL import Image

p = r"D:\ai\antigravity\global_blog\blog\2026-03-26-maeumjigi-1\images\02_term.png"
with Image.open(p) as im:
    print("02_term.png format:", im.format, "size:", im.size, "mode:", im.mode)
