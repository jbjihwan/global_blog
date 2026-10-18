import os
from PIL import Image

EXTRACT_DIR = r"D:\ai\antigravity\global_blog\extracted_ppt_images"
CAPDE_ROOT = r"D:\서울과기대 컴퓨터공학과\26-1\CapDe\팀플"

# Let's inspect images in detail
def inspect_images():
    print("=== Extracted Week12 _preview images ===")
    p_dir = os.path.join(CAPDE_ROOT, r"Week12\_preview")
    for f in sorted(os.listdir(p_dir)):
        fp = os.path.join(p_dir, f)
        try:
            with Image.open(fp) as im:
                print(f"  {f}: {im.size}, {im.format}")
        except Exception as e:
            print(f"  {f}: {e}")

    print("\n=== Extracted week16_final web_feature images ===")
    w16_dir = os.path.join(EXTRACT_DIR, "week16_final")
    for f in sorted(os.listdir(w16_dir)):
        fp = os.path.join(w16_dir, f)
        try:
            with Image.open(fp) as im:
                print(f"  {f}: {im.size}, {im.format}")
        except Exception as e:
            print(f"  {f}: {e}")

    print("\n=== Week8 & Week9 figures ===")
    for w in [r"Week8", r"Week9\fine_tuning\results\figures\eval", r"Week9\fine_tuning\results\figures\training", r"Week9\GPU사용량"]:
        full_w = os.path.join(CAPDE_ROOT, w)
        if os.path.exists(full_w):
            print(f"Folder: {w}")
            for f in os.listdir(full_w):
                if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                    fp = os.path.join(full_w, f)
                    try:
                        with Image.open(fp) as im:
                            print(f"  {f}: {im.size}")
                    except:
                        pass

if __name__ == "__main__":
    inspect_images()
