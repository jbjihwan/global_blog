import os
from PIL import Image

p = r"D:\Projects\26_1\CapDe\maeumjigi\test-results\관련사진"
for f in os.listdir(p):
    fp = os.path.join(p, f)
    if os.path.isfile(fp):
        try:
            with Image.open(fp) as im:
                print(f"{f}: size {im.size}, mode {im.mode}, file size {os.path.getsize(fp)}")
        except Exception as e:
            print(f"{f}: error {e}")
