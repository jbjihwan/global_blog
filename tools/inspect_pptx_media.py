import zipfile
import os

pptx_path = r"C:\Users\jbgih\Downloads\[6팀]2학기_1차발표_마음이_여름방학_진행보고.pptx"
if os.path.exists(pptx_path):
    print("PPTX exists. Size:", os.path.getsize(pptx_path))
    with zipfile.ZipFile(pptx_path, 'r') as z:
        media_files = [f for f in z.namelist() if f.startswith("ppt/media/")]
        print(f"Found {len(media_files)} media files in PPTX:")
        for mf in media_files:
            info = z.getinfo(mf)
            print(f" - {mf} ({info.file_size} bytes)")
else:
    print("PPTX does not exist.")
