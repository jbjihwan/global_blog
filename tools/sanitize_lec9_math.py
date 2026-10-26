import os

base_dir = r"D:\ai\antigravity\global_blog\배포대기\2026-10-30-stanford-cs146s-9"
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
    
    # Replace LaTeX curly brace expressions
    content = content.replace(r"$2^{128}$", "2^128")
    content = content.replace(r"$\Phi_{code}(X, Y)$", "`Phi_code(X, Y)`")
    content = content.replace(r"$\neg \Psi_{spec}(X, Y)$", "`NOT Psi_spec(X, Y)`")
    content = content.replace(r"$\Psi_{spec}$", "`Psi_spec`")
    content = content.replace(r"\Phi_{code}", "Phi_code")
    content = content.replace(r"\Psi_{spec}", "Psi_spec")
    
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Sanitized: {fpath}")
