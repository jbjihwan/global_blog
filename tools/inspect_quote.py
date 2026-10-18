import os
from PIL import Image

fp = r"D:\서울과기대 컴퓨터공학과\26-1\CapDe\팀플\Week15\견적_1차시도.png"
if os.path.exists(fp):
    im = Image.open(fp)
    print(f"견적_1차시도.png size: {im.size}")
    # Check if there are other files in Week15 or Week12
