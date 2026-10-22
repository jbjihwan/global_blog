import os

candidates = [
    "crisis_detection",
    "csa_compare",
    "stanford_cs146s",
    "stanford_cs221",
    "stanford_ai",
    "synth_gen",
    "verso_analysis",
    "g123_style_rpg",
    "rpg_idle",
    "capde",
    "gpu_cost_request",
    "security_check"
]

base_dir = r"D:\ai\antigravity"

for c in candidates:
    p = os.path.join(base_dir, c)
    if os.path.exists(p):
        files = os.listdir(p)
        print(f"\n=== {c} ===")
        print(f"Files ({len(files)}): {files[:10]}")
        # check if README or similar exists
        for f in files:
            if "readme" in f.lower() or f.endswith(".md"):
                print(f"  Doc: {f}")
