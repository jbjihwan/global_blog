import shutil, os

art_dir = r"C:\Users\jbgih\.gemini\antigravity-cli\brain\a2c8435f-707b-431d-a280-dad177e26fdc"
os.makedirs(art_dir, exist_ok=True)

shutil.copy2(r"D:\Projects\26_1\CapDe\maeumjigi\maeum-app\assets\logo.png", os.path.join(art_dir, "maeum_app_logo.png"))
shutil.copy2(r"D:\ai\antigravity\global_blog\tools\pptx_extracted\fImage12799565441.png", os.path.join(art_dir, "pptx_graphic_1.png"))
shutil.copy2(r"D:\ai\antigravity\global_blog\tools\pptx_extracted\fImage24500161641.png", os.path.join(art_dir, "pptx_graphic_2.png"))

print("Copied files to artifact directory.")
