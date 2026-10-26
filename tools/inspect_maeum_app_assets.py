from PIL import Image

logo_path = r"D:\Projects\26_1\CapDe\maeumjigi\maeum-app\assets\logo.png"
with Image.open(logo_path) as im:
    print("Logo Format:", im.format, "Size:", im.size, "Mode:", im.mode)
    print("Logo Extrema:", im.getextrema())

icon_path = r"D:\Projects\26_1\CapDe\maeumjigi\maeum-app\assets\icon.png"
with Image.open(icon_path) as im:
    print("Icon Format:", im.format, "Size:", im.size, "Mode:", im.mode)
    print("Icon Extrema:", im.getextrema())

splash_path = r"D:\Projects\26_1\CapDe\maeumjigi\maeum-app\assets\splash-icon.png"
with Image.open(splash_path) as im:
    print("Splash Format:", im.format, "Size:", im.size, "Mode:", im.mode)
    print("Splash Extrema:", im.getextrema())
