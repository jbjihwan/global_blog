import os

def read_head(path, lines=25):
    if not os.path.exists(path):
        return f"[Not found: {path}]"
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return "".join([f.readline() for _ in range(lines)])

print("=== crisis_detection ===")
print(read_head(r"D:\ai\antigravity\crisis_detection\위기감지모델_v2_모델설계_단순화검토.md"))

print("\n=== verso_analysis ===")
print(read_head(r"D:\ai\antigravity\verso_analysis\analysis.md"))

print("\n=== capde ===")
print(read_head(r"D:\ai\antigravity\capde\HANDOFF.md"))

print("\n=== stanford_cs146s ===")
print(read_head(r"D:\ai\antigravity\stanford_cs146s\lecture_01_overview.md"))

print("\n=== stanford_cs221 ===")
print(read_head(r"D:\ai\antigravity\stanford_cs221\lecture_01_overview.md"))
