import os

cv_root = r"D:\CV"
for root, dirs, files in os.walk(cv_root):
    # Skip venv
    if ".venv" in root or "gpu_env" in root:
        continue
    for f in files:
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.mp4', '.avi')):
            print(f"[CV Media] {os.path.relpath(os.path.join(root, f), cv_root)}")
