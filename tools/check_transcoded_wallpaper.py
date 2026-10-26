from PIL import Image

tw = r"C:\Users\jbgih\AppData\Roaming\Microsoft\Windows\Themes\TranscodedWallpaper"
try:
    with Image.open(tw) as im:
        print("TranscodedWallpaper format:", im.format, "size:", im.size, "mode:", im.mode)
        extrema = im.getextrema()
        print("TranscodedWallpaper extrema:", extrema)
except Exception as e:
    print("Error opening TranscodedWallpaper:", e)
