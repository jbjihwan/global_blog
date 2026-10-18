import os
from PIL import Image, ImageDraw, ImageFont
import matplotlib.font_manager as fm

FONTS = {
    "ko": r"C:\Windows\Fonts\malgun.ttf",
    "ja": r"C:\Windows\Fonts\msgothic.ttc",
    "en": r"C:\Windows\Fonts\segoeui.ttf",
    "es": r"C:\Windows\Fonts\segoeui.ttf",
}

for loc, path in FONTS.items():
    print(f"[{loc}] Checking {path}")
    if os.path.exists(path):
        f = ImageFont.truetype(path, 20)
        im = Image.new("RGB", (200, 50), color="#1e293b")
        d = ImageDraw.Draw(im)
        test_str = {
            "ko": "테스트 한글 123",
            "ja": "テスト日本語 123",
            "en": "Test English 123",
            "es": "Prueba Español 123",
        }[loc]
        d.text((10, 10), test_str, font=f, fill="#ffffff")
        print(f"  Pillow rendered successfully for {loc}!")
    else:
        print(f"  [ERROR] Font not found for {loc}")
