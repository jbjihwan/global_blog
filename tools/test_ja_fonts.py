import os

for f in ["msgothic.ttc", "yugothb.ttc", "yugothm.ttc", "yumin.ttf"]:
    fp = os.path.join(r"C:\Windows\Fonts", f)
    print(f"{f}: {'EXISTS' if os.path.exists(fp) else 'NOT FOUND'}")
