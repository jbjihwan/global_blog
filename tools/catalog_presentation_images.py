import zipfile
import os
import shutil

EXTRACT_DIR = r"D:\ai\antigravity\global_blog\extracted_ppt_images"
os.makedirs(EXTRACT_DIR, exist_ok=True)

PPT_FILES = [
    (r"D:\서울과기대 컴퓨터공학과\26-1\CapDe\팀플\Week2\[6팀]캡스톤 디자인 2주차 보고서.pptx", "week2"),
    (r"D:\서울과기대 컴퓨터공학과\26-1\CapDe\팀플\Week6\캡디_6주차_발표자료.pptx", "week6"),
    (r"D:\서울과기대 컴퓨터공학과\26-1\CapDe\팀플\Week8\마음이_8주차_발표.pptx", "week8"),
    (r"D:\서울과기대 컴퓨터공학과\26-1\CapDe\팀플\Week10\6팀 10주차 발표자료.pptx", "week10"),
    (r"D:\서울과기대 컴퓨터공학과\26-1\CapDe\팀플\Week12\1학기_최종발표_마음이.pptx", "week12_final"),
    (r"D:\서울과기대 컴퓨터공학과\26-1\CapDe\팀플\Week16\1학기_최종발표_마음이.pptx", "week16_final"),
]

def extract_and_catalog():
    print("=== Extracting Images from PPTX files ===")
    for ppt_path, prefix in PPT_FILES:
        if not os.path.exists(ppt_path):
            continue
        dest_folder = os.path.join(EXTRACT_DIR, prefix)
        os.makedirs(dest_folder, exist_ok=True)
        try:
            with zipfile.ZipFile(ppt_path, 'r') as z:
                media = [n for n in z.namelist() if n.startswith("ppt/media/")]
                for m in media:
                    fname = os.path.basename(m)
                    out_path = os.path.join(dest_folder, fname)
                    with z.open(m) as src, open(out_path, 'wb') as dst:
                        shutil.copyfileobj(src, dst)
                print(f"Extracted {len(media)} images from {os.path.basename(ppt_path)} into {prefix}/")
        except Exception as e:
            print(f"Error {ppt_path}: {e}")

    print("\n=== Summary of Extracted Images by Folder ===")
    for d in sorted(os.listdir(EXTRACT_DIR)):
        dp = os.path.join(EXTRACT_DIR, d)
        if os.path.isdir(dp):
            files = [f for f in os.listdir(dp) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            print(f"Folder '{d}': {len(files)} images")
            for f in files[:8]:
                size_kb = os.path.getsize(os.path.join(dp, f)) // 1024
                print(f"   {f} ({size_kb} KB)")
            if len(files) > 8:
                print(f"   ... and {len(files) - 8} more")

if __name__ == "__main__":
    extract_and_catalog()
