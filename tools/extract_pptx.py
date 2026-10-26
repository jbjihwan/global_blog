import zipfile, os
from PIL import Image

pptx_path = r"C:\Users\jbgih\Downloads\[6팀]2학기_1차발표_마음이_여름방학_진행보고.pptx"
out_dir = r"D:\ai\antigravity\global_blog\tools\pptx_extracted"
os.makedirs(out_dir, exist_ok=True)

with zipfile.ZipFile(pptx_path, 'r') as z:
    for f in z.namelist():
        if f.startswith("ppt/media/"):
            out_file = os.path.join(out_dir, os.path.basename(f))
            with open(out_file, "wb") as fo:
                fo.write(z.read(f))
            with Image.open(out_file) as im:
                print(f"Extracted {os.path.basename(f)}: size {im.size}, mode {im.mode}, file size {os.path.getsize(out_file)}")
