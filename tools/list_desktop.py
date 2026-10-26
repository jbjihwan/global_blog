import os

desktop = r"C:\Users\jbgih\Desktop"
print("Files on Desktop:")
for f in os.listdir(desktop):
    fp = os.path.join(desktop, f)
    print(f" - {f} ({'DIR' if os.path.isdir(fp) else f'{os.path.getsize(fp)} bytes'})")
