import os

if os.path.exists(r"D:\Projects"):
    print("Folders in D:\\Projects:")
    for d in os.listdir(r"D:\Projects"):
        print(" -", d)
else:
    print("D:\\Projects does not exist.")
