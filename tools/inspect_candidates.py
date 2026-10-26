from PIL import Image

p = r"C:\Users\jbgih\OneDrive\사진\1.png"
with Image.open(p) as im:
    print("1.png format:", im.format, "size:", im.size, "mode:", im.mode)
    print("1.png extrema:", im.getextrema())

p2 = r"C:\Users\jbgih\OneDrive\바탕 화면\img_67048_2.jpg"
with Image.open(p2) as im2:
    print("img_67048_2 format:", im2.format, "size:", im2.size, "mode:", im2.mode)
    print("img_67048_2 extrema:", im2.getextrema())
