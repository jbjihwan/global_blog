import os
from PIL import Image

CAPDE_ROOT = r"D:\서울과기대 컴퓨터공학과\26-1\CapDe\팀플"

def inspect_specific_images():
    files = [
        os.path.join(CAPDE_ROOT, r"Week12\_preview\s01.png"),
        os.path.join(CAPDE_ROOT, r"Week12\_preview\s07.png"),
        os.path.join(CAPDE_ROOT, r"Week15\견적_1차시도.png"),
        os.path.join(CAPDE_ROOT, r"Week6\프론트엔드버그.png"),
    ]
    for fp in files:
        if os.path.exists(fp):
            with Image.open(fp) as im:
                print(f"File: {os.path.basename(fp)}, Size: {im.size}, Mode: {im.mode}")

if __name__ == "__main__":
    inspect_specific_images()
