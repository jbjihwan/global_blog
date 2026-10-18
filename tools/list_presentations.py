import os
import glob

SEARCH_DIRS = [
    r"D:\서울과기대 컴퓨터공학과\26-1\CapDe\팀플",
    r"D:\서울과기대 컴퓨터공학과\26-2\CapDe\팀플",
    r"D:\서울과기대 컴퓨터공학과\26-1\RL\팀플",
    r"D:\CV\Term_project",
    r"D:\RL",
]

def list_presentations():
    print("=== PPT / PPTX / PDF Presentation Files ===")
    for d in SEARCH_DIRS:
        if not os.path.exists(d):
            continue
        for ext in ["*.pptx", "*.ppt", "*.pdf"]:
            for f in glob.glob(os.path.join(d, "**", ext), recursive=True):
                print(f"[PPT] {f}")

    print("\n=== Specific Image Files in CapDe ===")
    capde_dir = r"D:\서울과기대 컴퓨터공학과\26-1\CapDe\팀플"
    for r, dirs, files in os.walk(capde_dir):
        for f in files:
            if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                rel = os.path.relpath(os.path.join(r, f), capde_dir)
                print(f"[CapDe Img] {rel}")

    print("\n=== Specific Image Files in CV Term_project ===")
    cv_dir = r"D:\CV\Term_project"
    if os.path.exists(cv_dir):
        for r, dirs, files in os.walk(cv_dir):
            for f in files:
                if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                    rel = os.path.relpath(os.path.join(r, f), cv_dir)
                    print(f"[CV Img] {rel}")

    print("\n=== Specific Image Files in RL realbot / 보고서 ===")
    rl_dirs = [r"D:\RL\realbot\사진", r"D:\서울과기대 컴퓨터공학과\26-1\RL\팀플\보고서_그림_v2", r"D:\RL\결과분석\통합비교_figs"]
    for rld in rl_dirs:
        if os.path.exists(rld):
            for f in os.listdir(rld):
                if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                    print(f"[RL Img] {os.path.basename(rld)} / {f}")

if __name__ == "__main__":
    list_presentations()
