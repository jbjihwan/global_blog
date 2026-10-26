import os
from PIL import Image

imgs = [
    r"C:\Users\jbgih\OneDrive\바탕 화면\img_67048_2.jpg",
    r"C:\Users\jbgih\OneDrive\사진\1.png",
    r"C:\Users\jbgih\OneDrive\사진\KakaoTalk_20250313_012952653.jpg",
    r"C:\Users\jbgih\OneDrive\사진\KakaoTalk_20250313_012952653_01.png",
    r"C:\Users\jbgih\OneDrive\사진\그림.png",
    r"C:\Users\jbgih\OneDrive\사진\그림 (1).png",
    r"C:\Users\jbgih\OneDrive\사진\금.png",
]

for p in imgs:
    if os.path.exists(p):
        with Image.open(p) as im:
            print(f"Path: {p}")
            print(f"  Format: {im.format}, Size: {im.size}, Mode: {im.mode}")
