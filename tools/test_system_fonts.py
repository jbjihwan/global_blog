import os

font_checks = [
    ("ko", r"C:\Windows\Fonts\malgunbd.ttf"),
    ("ja", r"C:\Windows\Fonts\meiryo.ttc"),
    ("zh-Hans", r"C:\Windows\Fonts\msyh.ttc"),
    ("zh-Hant", r"C:\Windows\Fonts\msjh.ttc"),
    ("en", r"C:\Windows\Fonts\segoeuib.ttf"),
    ("es", r"C:\Windows\Fonts\segoeuib.ttf"),
]

for name, fp in font_checks:
    print(f"[{name}] {fp}: {'EXISTS' if os.path.exists(fp) else 'NOT FOUND'}")
