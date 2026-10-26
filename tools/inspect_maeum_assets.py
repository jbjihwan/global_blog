import os

paths = [
    r"D:\Projects\26_1\CapDe\maeumjigi\maeum-app\assets",
    r"D:\Projects\26_1\CapDe\maeumjigi\frontend\public",
    r"D:\Projects\26_1\CapDe\maeumjigi\test-results\관련사진",
]

for p in paths:
    if os.path.exists(p):
        print(f"\nFiles in {p}:")
        for f in os.listdir(p):
            fp = os.path.join(p, f)
            if os.path.isfile(fp):
                print(f" - {f} ({os.path.getsize(fp)} bytes)")
