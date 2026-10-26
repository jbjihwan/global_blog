import os

base_dir = r"D:\ai\antigravity\global_blog\배포대기\2026-10-29-stanford-cs146s-8"
files = [
    os.path.join(base_dir, "blog", "index.md"),
    os.path.join(base_dir, "i18n", "ko", "index.md"),
    os.path.join(base_dir, "i18n", "ja", "index.md"),
    os.path.join(base_dir, "i18n", "es", "index.md"),
    os.path.join(base_dir, "i18n", "zh-Hans", "index.md"),
    os.path.join(base_dir, "i18n", "zh-Hant", "index.md"),
]

for fpath in files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace math expressions containing \text{k}
    content = content.replace(r"$32\text{k}$", "32k")
    content = content.replace(r"$<32\text{k}$", "< 32k")
    content = content.replace(r"\text{k}", "k")
    
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Sanitized: {fpath}")
