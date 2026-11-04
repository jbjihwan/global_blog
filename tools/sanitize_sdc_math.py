import os
import re

files = [
    r"D:\ai\antigravity\global_blog\blog\2026-12-03-sdc-01-architecture-klm-model\index.md",
    r"D:\ai\antigravity\global_blog\i18n\ko\docusaurus-plugin-content-blog\2026-12-03-sdc-01-architecture-klm-model\index.md",
    r"D:\ai\antigravity\global_blog\배포대기\2026-12-03-sdc-01-architecture-klm-model\blog\index.md",
    r"D:\ai\antigravity\global_blog\배포대기\2026-12-03-sdc-01-architecture-klm-model\i18n\ko\index.md"
]

def sanitize_content(text: str) -> str:
    # 1. Block math $$...$$
    text = re.sub(
        r'\$\$\\frac\{100,000\\text\{ m\}\}\{30\\text\{ m\}\}\s*\\times\s*\\frac\{100,000\\text\{ m\}\}\{30\\text\{ m\}\}\s*\\approx\s*1\.11\s*\\times\s*10\^7\\text\{.*?\}\$\$',
        '`(100,000 m / 30 m) × (100,000 m / 30 m) ≈ 1.11 × 10^7 nodes`',
        text
    )
    text = re.sub(
        r'\$\$\\text\{KV-Cache\}\s*=\s*2\s*\\times\s*2\s*\\times.*?=\s*1\.04\\text\{ GB\}\$\$',
        '`KV-Cache = 2 × 2 × n_layers × n_heads × d_head × seq_len × bytes ≈ 0.52 GB × 2 = 1.04 GB`',
        text
    )
    text = re.sub(
        r'\$\$\\mathbf\{w\}\s*=\s*\(.*?\)\s*\\in\s*\[0,\s*1\]\^4\$\$',
        '`w = (α_terrain, β_threat, γ_fuel, δ_time) ∈ [0, 1]^4`',
        text
    )
    text = re.sub(
        r'\$\$\\frac\{dW\}\{dt\}\s*=\s*-\s*c_0\s*\\cdot\s*T\s*\\cdot\s*\\eta\(h,\s*M\)\$\$',
        '`dW/dt = - c0 · T · η(h, M)`',
        text
    )
    text = re.sub(
        r'\$\$c_0\s*=\s*0\.131227\\text\{ hr\}\^\{-1\}\$\$',
        '`c0 = 0.131227 hr^-1`',
        text
    )
    # RK4 multi-line block
    text = re.sub(
        r'\$\$k_1\s*=\s*f\(t_n,\s*W_n\),.*?\$\$W_\{n\+1\}\s*=\s*W_n.*?\$\$',
        '```text\n'
        'k1 = f(t_n, W_n)\n'
        'k2 = f(t_n + dt/2, W_n + dt/2 * k1)\n'
        'k3 = f(t_n + dt/2, W_n + dt/2 * k2)\n'
        'k4 = f(t_n + dt,   W_n + dt * k3)\n'
        'W_{n+1} = W_n + (dt/6) * (k1 + 2*k2 + 2*k3 + k4)\n'
        '```',
        text,
        flags=re.DOTALL
    )
    text = re.sub(
        r'\$\$\\text\{Error\}_\{.*?\}\s*=\s*\\left\|\s*\\frac\{.*?\}.*?\\right\|\s*\\le\s*1\.0\s*\\times\s*10\^\{-2\}\$\$',
        '`Error_fuel = |(Fuel_runtime - Fuel_RK4) / Fuel_RK4| <= 1.0 × 10^-2`',
        text
    )
    
    # Inline math cleanups
    # Replace $...$ containing \text or math braces
    def clean_inline(m):
        inner = m.group(1)
        clean = inner.replace(r'\text{', '').replace(r'\mathbf{', '').replace('}', '').replace(r'\times', '×').replace(r'\cdot', '·')
        clean = clean.replace(r'\le', '<=').replace(r'\ge', '>=').replace(r'\approx', '≈').replace(r'\in', '∈')
        clean = clean.replace(r'\alpha', 'α').replace(r'\beta', 'β').replace(r'\gamma', 'γ').replace(r'\delta', 'δ')
        clean = clean.replace(r'\eta', 'η').replace(r'\Delta', 'Δ').replace(r'\_', '_')
        return f"`{clean.strip()}`"
        
    text = re.sub(r'\$([^\$\n]+?)\$', clean_inline, text)
    
    return text

for f in files:
    if os.path.exists(f):
        with open(f, 'r', encoding='utf-8') as fp:
            content = fp.read()
        sanitized = sanitize_content(content)
        with open(f, 'w', encoding='utf-8') as fp:
            fp.write(sanitized)
        print("Sanitized", f)
