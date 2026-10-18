import os
import glob

SEARCH_ROOTS = [
    r"D:\서울과기대 컴퓨터공학과",
    r"D:\CV",
    r"D:\RL",
    r"D:\ai\claude",
    r"D:\ai\antigravity\capde",
    r"D:\ai\antigravity\naver_blog",
    r"C:\Users\jbgih\Downloads",
    r"C:\Users\jbgih\Documents",
    r"C:\Users\jbgih\Desktop",
]

def find_files():
    print("=== Scanning for PPTX and Presentations ===")
    ppt_files = []
    for root in SEARCH_ROOTS:
        if not os.path.exists(root):
            continue
        for ext in ["*.pptx", "*.ppt", "*.pdf"]:
            for f in glob.glob(os.path.join(root, "**", ext), recursive=True):
                ppt_files.append(f)
                
    for f in sorted(ppt_files):
        print(f"[PPT/DOC] {f}")
        
    print("\n=== Scanning for Relevant Project Image Directories ===")
    image_dirs = []
    for root in SEARCH_ROOTS:
        if not os.path.exists(root):
            continue
        for r, dirs, files in os.walk(root):
            img_count = sum(1 for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg')))
            if img_count > 3:
                print(f"[IMG DIR] ({img_count} images) {r}")

if __name__ == "__main__":
    find_files()
