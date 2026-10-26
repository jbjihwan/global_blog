import os

static_dir = r"D:\ai\antigravity\global_blog\static"
if os.path.exists(static_dir):
    print("Files in static/:", os.listdir(static_dir))
    ads_txt = os.path.join(static_dir, "ads.txt")
    if os.path.exists(ads_txt):
        with open(ads_txt, "r", encoding="utf-8") as f:
            print("ads.txt content:\n", f.read())
    else:
        print("ads.txt DOES NOT EXIST!")
