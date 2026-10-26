import os

theme_dir = r"C:\Users\jbgih\AppData\Roaming\Microsoft\Windows\Themes"
if os.path.exists(theme_dir):
    print("Files in Themes:")
    for f in os.listdir(theme_dir):
        fp = os.path.join(theme_dir, f)
        print(f" - {f} ({os.path.getsize(fp)} bytes)")
else:
    print("Themes dir not found")
