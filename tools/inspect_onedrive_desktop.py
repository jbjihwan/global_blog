import os

p1 = r"C:\Users\jbgih\OneDrive\바탕 화면"
p2 = r"C:\Users\jbgih\OneDrive\사진"

for p in [p1, p2]:
    if os.path.exists(p):
        print(f"\nContents of {p}:")
        for f in os.listdir(p):
            fp = os.path.join(p, f)
            print(f" - {f} ({'DIR' if os.path.isdir(fp) else f'{os.path.getsize(fp)} bytes'})")
