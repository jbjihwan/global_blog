import os
import glob
from PIL import Image
from PIL.ExifTags import TAGS

BLOG_DIR = r"D:\ai\antigravity\global_blog\blog"

def check_image_metadata():
    print("=== 1. Checking EXIF & Metadata in Blog Images ===")
    img_files = glob.glob(os.path.join(BLOG_DIR, "**", "images", "*.*"), recursive=True)
    metadata_leaks = 0
    
    for img_path in sorted(img_files):
        if not img_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue
        rel = os.path.relpath(img_path, BLOG_DIR)
        try:
            with Image.open(img_path) as im:
                # Check EXIF
                exif_data = im.getexif()
                if exif_data:
                    for tag_id, value in exif_data.items():
                        tag_name = TAGS.get(tag_id, tag_id)
                        # Check for GPS or sensitive device info
                        if "GPS" in str(tag_name) or tag_name in [306, 272, 315, 316]:
                            print(f"[EXIF ALERT] {rel}: {tag_name} = {str(value)[:40]}")
                            metadata_leaks += 1
                
                # Check PNG text chunks
                if hasattr(im, "text") and im.text:
                    for k, v in im.text.items():
                        if any(s in str(v).lower() for s in ["c:\\", "d:\\", "user", "jbgih", "jihwan"]):
                            print(f"[PNG TEXT ALERT] {rel}: {k} = {v[:50]}")
                            metadata_leaks += 1
        except Exception as e:
            print(f"Error checking {rel}: {e}")
            
    if metadata_leaks == 0:
        print("[OK] No GPS, device identifiers, or local filepath metadata detected in image headers.")

if __name__ == "__main__":
    check_image_metadata()
