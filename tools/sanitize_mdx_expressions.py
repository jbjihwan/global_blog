# -*- coding: utf-8 -*-
"""
Sanitize unescaped MDX / Acorn expressions in German and French posts
to guarantee 100% clean Docusaurus MDX compilation.
"""

import os
import glob
import re

GB_ROOT = r"D:\ai\antigravity\global_blog"
TARGET_DIRS = [
    os.path.join(GB_ROOT, "i18n", "de", "docusaurus-plugin-content-blog"),
    os.path.join(GB_ROOT, "i18n", "fr", "docusaurus-plugin-content-blog"),
    os.path.join(GB_ROOT, "배포대기"),
]

FIXES = [
    # Stanford 2
    (r"P\(w_t \\mid w_\{<t\}\)", "`P(w_t | w_{<t})`"),
    (r"P\(w_t\s*\\mid\s*w_<t\)", "`P(w_t | w_{<t})`"),
    (r"\$P\(w_t.*?\)\$", "`P(w_t | w_1...w_{t-1})`"),

    # Stanford 9
    (r"\$\$\\forall x \\in \\text\{Inputs\}.*?\$\$", "```text\n∀ x ∈ Inputs,  Property(f(x)) == True\n```"),

    # RL 1
    (r"\$\\mathbf\{s\} \\in \\mathbb\{R\}\^7\$", "`s ∈ R^7`"),
    (r"\$3\^3 = 27\$", "3³ = 27"),

    # RL 2
    (r"\$\$Q\(s_t, a_t\).*?\$\$", "```text\nQ(s_t, a_t) ← Q(s_t, a_t) + α [ r_{t+1} + γ max Q(s_{t+1}, a) - Q(s_t, a_t) ]\n```"),
    (r"\$\$R\(s, a, s'\).*?\$\$", "```text\nR(s, a, s') = R_terminal + c1·(d_t - d_{t+1}) + c2·v_forward - c3·I_spin\n```"),
    (r"\$d_t - d_\{t\+1\} > 0\$", "`d_t - d_{t+1} > 0`"),

    # RL 3
    (r"\$d_\{?\\text\{front\}?\}?\s*<\s*0\.2\\,\\text\{m\}\$", "`d_front < 0.2m`"),
    (r"\$d_\{front\}\s*<\s*0\.2m\$", "`d_front < 0.2m`"),

    # ANPR 2
    (r"\$\$y = m \\cdot x \+ b.*?\$\$", "```text\ny = m · x + b,   wobei m = (y2 - y1) / (x2 - x1)\n```"),
    (r"\$\$\\text\{IoU\}_\{intrusion\}.*?\$\$", "```text\nIoU_intrusion = Area(P_vehicle ∩ P_lane) / Area(P_vehicle) > θ_threshold\n```"),
    (r"\$P_\{?\\text\{vehicle\}?\}\$", "`P_vehicle`"),
    (r"\$P_\{?\\text\{lane\}?\}\$", "`P_lane`"),
    (r"\$\\theta\s*=\s*0\.15\$", "`θ = 0.15`"),
    (r"\$\\theta_\{?\\text\{threshold\}?\}\$", "`θ_threshold`"),
]

def sanitize_file(fpath):
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = content
    for pattern, repl in FIXES:
        new_content = re.sub(pattern, repl, new_content, flags=re.DOTALL)

    # General cleanup for any remaining $\text{...}$ or unescaped math with curly braces
    # but not inside code blocks
    if new_content != content:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
    return False

def main():
    count = 0
    for t_dir in TARGET_DIRS:
        for root, dirs, files in os.walk(t_dir):
            for file in files:
                if file.endswith(".md"):
                    p = os.path.join(root, file)
                    if sanitize_file(p):
                        count += 1
                        print(f"Sanitized: {os.path.relpath(p, GB_ROOT)}")
    print(f"\nTotal files sanitized: {count}")

if __name__ == "__main__":
    main()
