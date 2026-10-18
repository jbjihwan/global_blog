import os

capde_root = r"D:\서울과기대 컴퓨터공학과\26-1\CapDe\팀플"
for root, dirs, files in os.walk(capde_root):
    for f in files:
        if f.lower().endswith(('.pptx', '.ppt', '.pdf', '.hwp', '.docx')):
            print(f"[CapDe 26-1] {os.path.relpath(os.path.join(root, f), capde_root)}")

capde_root2 = r"D:\서울과기대 컴퓨터공학과\26-2\CapDe\팀플"
if os.path.exists(capde_root2):
    for root, dirs, files in os.walk(capde_root2):
        for f in files:
            if f.lower().endswith(('.pptx', '.ppt', '.pdf', '.hwp', '.docx')):
                print(f"[CapDe 26-2] {os.path.relpath(os.path.join(root, f), capde_root2)}")
