import os

base_dir = r"D:\ai\antigravity"
items = os.listdir(base_dir)

print(f"Items in {base_dir}:")
for item in items:
    full_path = os.path.join(base_dir, item)
    is_dir = os.path.isdir(full_path)
    print(f" - {'[DIR]' if is_dir else '[FILE]'} {item}")
