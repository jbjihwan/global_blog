# -*- coding: utf-8 -*-
import os
import glob
import re

GB_ROOT = r"D:\ai\antigravity\global_blog"

dirs = [
    os.path.join(GB_ROOT, "i18n", "de", "docusaurus-plugin-content-blog"),
    os.path.join(GB_ROOT, "i18n", "fr", "docusaurus-plugin-content-blog"),
    os.path.join(GB_ROOT, "i18n", "pt-BR", "docusaurus-plugin-content-blog"),
    os.path.join(GB_ROOT, "배포대기"),
]

def clean_file(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    orig = text

    # Specific replacements
    text = text.replace(r"$\theta_{\text{target}}$", "θ_target")
    text = text.replace(r"$\text{Zustände gesamt} = 27 \times 4 \times 6 = 648 \text{ diskrete Zustände}$", "`Zustände gesamt = 27 × 4 × 6 = 648 Bins`")
    text = text.replace(r"$d_{\text{front}} < 0.2\,\text{m}$", "d_front < 0.2m")
    text = text.replace(r"$P_{\text{vehicle}}$", "P_vehicle")
    text = text.replace(r"$P_{\text{lane}}$", "P_lane")
    text = text.replace(r"$`P(w_t | w_{<t})`$", "`P(w_t | w_<t)`")
    text = text.replace(r"P(w_t \mid w_{<t})", "P(w_t | w_<t)")
    
    # Clean IoU formula
    text = re.sub(r"\$\$\\?text\{IoU\}.*?\$\$", "```text\nIoU_intrusion = Area(P_vehicle ∩ P_lane) / Area(P_vehicle) > θ_threshold\n```", text, flags=re.DOTALL)
    text = re.sub(r"\$\\?text\{IoU\}.*?\$", "`IoU_intrusion > θ_threshold`", text, flags=re.DOTALL)

    # Clean forall formula
    text = re.sub(r"\$\$\\?forall.*?\$\$", "```text\n∀ x ∈ Inputs,  Property(f(x)) == True\n```", text, flags=re.DOTALL)
    text = re.sub(r"\$\\?forall.*?\$", "`∀ x ∈ Inputs, Property(f(x)) == True`", text, flags=re.DOTALL)

    # Clean any $...{...}...$
    text = re.sub(r"\$([^\$\n]*\{[^\$\n]*)\$", r"`\1`", text)

    if text != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        return True
    return False

count = 0
for d in dirs:
    for root, _, files in os.walk(d):
        for fl in files:
            if fl.endswith(".md"):
                p = os.path.join(root, fl)
                if clean_file(p):
                    count += 1
                    print("Fixed math in:", os.path.relpath(p, GB_ROOT))

print(f"Total fixed: {count}")
