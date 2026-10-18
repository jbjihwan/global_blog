import os
import glob

SEARCH_ROOTS = [
    r"D:\서울과기대 컴퓨터공학과\26-1",
    r"D:\서울과기대 컴퓨터공학과\26-2",
    r"D:\CV",
    r"D:\RL",
    r"D:\ai",
    r"C:\Users\jbgih\Documents",
    r"C:\Users\jbgih\Downloads",
    r"C:\Users\jbgih\Desktop",
]

def find_ppts():
    print("=== PPTX / PPT / PDF Presentations Found ===")
    count = 0
    for root in SEARCH_ROOTS:
        if not os.path.exists(root):
            continue
        for ext in ["*.pptx", "*.ppt", "*.pdf"]:
            for f in glob.glob(os.path.join(root, "**", ext), recursive=True):
                # Filter out node_modules or venv
                if "node_modules" in f or ".venv" in f or "site-packages" in f or "MikTeX" in f:
                    continue
                print(f"[PPT/PDF] {f}")
                count += 1
    print(f"Total found: {count}")

if __name__ == "__main__":
    find_ppts()
